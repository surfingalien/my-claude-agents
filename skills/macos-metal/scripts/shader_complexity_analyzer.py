#!/usr/bin/env python3
"""Estimates Metal shader complexity and predicts occupancy/performance."""

import re
import sys
import json
import argparse
from pathlib import Path


# Approximate instruction weights for Apple GPU ISA estimation
INSTRUCTION_WEIGHTS = {
    # Arithmetic
    r'\bfloat\d*\s+\w+\s*=': 1,
    r'\bhalf\d*\s+\w+\s*=': 0.5,
    r'\bint\s+\w+\s*=': 1,
    r'\+=|-=|\*=|/=': 1,
    r'\*': 1,
    r'/': 4,  # Division is expensive
    r'sqrt\(': 8,
    r'rsqrt\(': 4,
    r'sin\(|cos\(|tan\(': 12,
    r'pow\(': 10,
    r'exp\(|log\(': 8,
    r'normalize\(': 5,
    r'dot\(': 4,
    r'cross\(': 8,
    # Memory
    r'\.sample\(': 16,
    r'\.read\(': 8,
    r'\.write\(': 8,
    r'texture2d<': 0,  # Declaration
    r'sampler\b': 0,
    # Control flow
    r'\bif\b': 2,
    r'\bfor\b': 3,
    r'\bwhile\b': 3,
    r'\bdiscard_fragment\(\)': 2,
}


def count_instructions(source: str) -> int:
    """Estimate instruction count from Metal shader source."""
    # Remove comments
    source = re.sub(r'//.*$', '', source, flags=re.MULTILINE)
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)

    total = 0
    for pattern, weight in INSTRUCTION_WEIGHTS.items():
        matches = re.findall(pattern, source)
        total += len(matches) * weight
    return int(total)


def count_samplers(source: str) -> int:
    return len(re.findall(r'\bsampler\b', source))


def count_textures(source: str) -> int:
    return len(re.findall(r'\btexture\w+<', source))


def count_branches(source: str) -> int:
    return len(re.findall(r'\b(if|else if|for|while|switch)\b', source))


def count_registers(source: str) -> int:
    """Estimate register usage from declared variables."""
    # Each float = 1 reg, float2 = 1, float3/float4 = 1 (packed on Apple GPU)
    scalar_vars = len(re.findall(r'\b(float|half|int|uint)\s+\w+\s*[=;,)]', source))
    vec_vars = len(re.findall(r'\b(float[234]|half[234]|int[234])\s+\w+\s*[=;,)]', source))
    mat_vars = len(re.findall(r'\b(float[234]x[234])\s+\w+\s*[=;,)]', source))
    return scalar_vars + vec_vars + mat_vars * 4


def predict_occupancy(registers: int, samplers: int, branches: int) -> str:
    """Predict GPU occupancy tier based on resource usage."""
    # Apple GPU: high register pressure and samplers reduce occupancy
    score = 100
    if registers > 64:
        score -= 30
    elif registers > 48:
        score -= 15
    elif registers > 32:
        score -= 5

    if samplers > 8:
        score -= 20
    elif samplers > 4:
        score -= 10

    if branches > 20:
        score -= 25
    elif branches > 10:
        score -= 10

    if score >= 75:
        return "HIGH (>75% — good parallelism)"
    elif score >= 50:
        return "MEDIUM (50-75% — acceptable)"
    else:
        return "LOW (<50% — consider simplification)"


def parse_stages(source: str) -> dict:
    """Separate source into vertex, fragment, and kernel stages."""
    stages = {"vertex": "", "fragment": "", "kernel": ""}

    # Extract vertex functions
    vertex_matches = re.findall(
        r'vertex\s+\w[\w<>]*\s+\w+\s*\([^{]*\)\s*\{[^}]*\}',
        source, re.DOTALL
    )
    stages["vertex"] = "\n".join(vertex_matches)

    # Extract fragment functions
    fragment_matches = re.findall(
        r'fragment\s+\w[\w<>]*\s+\w+\s*\([^{]*\)\s*\{[^}]*\}',
        source, re.DOTALL
    )
    stages["fragment"] = "\n".join(fragment_matches)

    # Extract kernel functions
    kernel_matches = re.findall(
        r'kernel\s+void\s+\w+\s*\([^{]*\)\s*\{[^}]*\}',
        source, re.DOTALL
    )
    stages["kernel"] = "\n".join(kernel_matches)

    return stages


def analyze_shader(source: str, target_gpu: str = "apple-m2") -> dict:
    stages = parse_stages(source)
    results = {"target_gpu": target_gpu, "stages": {}}

    for stage_name, stage_src in stages.items():
        if not stage_src.strip():
            continue
        instructions = count_instructions(stage_src)
        samplers = count_samplers(stage_src)
        textures = count_textures(stage_src)
        branches = count_branches(stage_src)
        registers = count_registers(stage_src)
        occupancy = predict_occupancy(registers, samplers, branches)

        suggestions = []
        if registers > 48:
            suggestions.append("High register count — consider splitting shader or using half precision")
        if samplers > 8:
            suggestions.append("Many samplers — consolidate into texture arrays where possible")
        if branches > 15:
            suggestions.append("High branch count — SIMD divergence reduces parallelism; consider step()/mix()")
        if "/(" in stage_src or re.search(r'/\s*[a-zA-Z_]', stage_src):
            suggestions.append("Divisions detected — replace with multiplication by reciprocal where safe")
        if re.search(r'sin\(|cos\(|tan\(', stage_src):
            suggestions.append("Trig functions are expensive — precompute or use lookup texture")
        if not suggestions:
            suggestions.append("No critical issues found")

        results["stages"][stage_name] = {
            "estimated_instructions": instructions,
            "sampler_count": samplers,
            "texture_count": textures,
            "branch_count": branches,
            "estimated_registers": registers,
            "predicted_occupancy": occupancy,
            "suggestions": suggestions,
        }

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Estimate Metal shader complexity and occupancy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Usage:\n  python shader_complexity_analyzer.py shader.metal\n  python shader_complexity_analyzer.py shader.metal --target-gpu apple-m3"
    )
    parser.add_argument("shader", help="Path to .metal shader file")
    parser.add_argument("--target-gpu", default="apple-m2", help="Target GPU (default: apple-m2)")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    path = Path(args.shader)
    if not path.exists():
        print(f"Error: file not found: {args.shader}", file=sys.stderr)
        sys.exit(1)

    source = path.read_text()
    results = analyze_shader(source, args.target_gpu)

    if args.format == "json":
        print(json.dumps(results, indent=2))
        return

    print(f"\n=== Metal Shader Complexity Analysis ({args.target_gpu}) ===")
    print(f"File: {path.name}\n")

    if not results["stages"]:
        print("No recognized shader stages found (vertex/fragment/kernel).")
        return

    for stage, data in results["stages"].items():
        print(f"--- {stage.upper()} STAGE ---")
        print(f"  Est. instructions : {data['estimated_instructions']}")
        print(f"  Samplers          : {data['sampler_count']}")
        print(f"  Textures          : {data['texture_count']}")
        print(f"  Branches          : {data['branch_count']}")
        print(f"  Est. registers    : {data['estimated_registers']}")
        print(f"  Predicted occupancy: {data['predicted_occupancy']}")
        print(f"  Suggestions:")
        for s in data["suggestions"]:
            print(f"    • {s}")
        print()


if __name__ == "__main__":
    main()
