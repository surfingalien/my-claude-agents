#!/usr/bin/env python3
"""Analyzes Metal performance data and reports bottlenecks."""

import json
import sys
import argparse
import statistics
from pathlib import Path


def analyze_frame_times(frame_times_ms: list[float], target_fps: float):
    """Compute frame time statistics and drop rate."""
    if not frame_times_ms:
        return {}
    target_ms = 1000.0 / target_fps
    drops = [t for t in frame_times_ms if t > target_ms]
    return {
        "count": len(frame_times_ms),
        "p50_ms": round(statistics.median(frame_times_ms), 2),
        "p95_ms": round(sorted(frame_times_ms)[int(len(frame_times_ms) * 0.95)], 2),
        "p99_ms": round(sorted(frame_times_ms)[int(len(frame_times_ms) * 0.99)], 2),
        "max_ms": round(max(frame_times_ms), 2),
        "drop_count": len(drops),
        "drop_rate_pct": round(len(drops) / len(frame_times_ms) * 100, 1),
        "target_ms": round(target_ms, 2),
    }


def analyze_gpu_stages(frames: list[dict]):
    """Break down CPU vs GPU time per stage."""
    cpu_times, vertex_times, fragment_times, compute_times = [], [], [], []
    for f in frames:
        if "cpu_ms" in f:
            cpu_times.append(f["cpu_ms"])
        if "vertex_ms" in f:
            vertex_times.append(f["vertex_ms"])
        if "fragment_ms" in f:
            fragment_times.append(f["fragment_ms"])
        if "compute_ms" in f:
            compute_times.append(f["compute_ms"])

    def avg(lst): return round(statistics.mean(lst), 2) if lst else None

    return {
        "avg_cpu_ms": avg(cpu_times),
        "avg_vertex_ms": avg(vertex_times),
        "avg_fragment_ms": avg(fragment_times),
        "avg_compute_ms": avg(compute_times),
    }


def recommend_optimizations(stats: dict, stages: dict, target_ms: float):
    """Generate prioritized optimization recommendations."""
    recs = []

    p95 = stats.get("p95_ms", 0)
    drop_rate = stats.get("drop_rate_pct", 0)

    if drop_rate > 5:
        recs.append({
            "priority": "HIGH",
            "issue": f"{drop_rate}% frame drops (>{target_ms:.1f}ms)",
            "action": "Profile with Metal System Trace — look for CPU/GPU sync stalls"
        })

    vertex_ms = stages.get("avg_vertex_ms") or 0
    fragment_ms = stages.get("avg_fragment_ms") or 0
    cpu_ms = stages.get("avg_cpu_ms") or 0
    budget = target_ms

    if cpu_ms > budget * 0.25:
        recs.append({
            "priority": "HIGH",
            "issue": f"CPU encode time {cpu_ms}ms exceeds 25% budget ({budget * 0.25:.1f}ms)",
            "action": "Reduce draw call count via instancing; cache pipeline states"
        })

    if vertex_ms > budget * 0.40:
        recs.append({
            "priority": "HIGH",
            "issue": f"Vertex stage {vertex_ms}ms exceeds 40% budget",
            "action": "Add GPU frustum culling; reduce vertex count with LOD; check register pressure"
        })

    if fragment_ms > budget * 0.40:
        recs.append({
            "priority": "HIGH",
            "issue": f"Fragment stage {fragment_ms}ms exceeds 40% budget",
            "action": "Reduce overdraw; simplify fragment shader; use depth pre-pass"
        })

    if p95 < budget and drop_rate < 2:
        recs.append({
            "priority": "LOW",
            "issue": "Performance within target",
            "action": "Monitor GPU utilization — keep below 80% for thermal headroom"
        })

    return sorted(recs, key=lambda r: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[r["priority"]])


def load_input(path: str):
    """Load Instruments JSON export or synthetic test data."""
    if path == "--test":
        import random
        random.seed(42)
        base = 8.5
        frames = []
        for _ in range(300):
            cpu = random.gauss(1.5, 0.3)
            vertex = random.gauss(3.5, 0.8)
            fragment = random.gauss(3.0, 0.6)
            total = cpu + vertex + fragment + random.uniform(0.2, 0.8)
            frames.append({
                "total_ms": round(total, 2),
                "cpu_ms": round(max(0, cpu), 2),
                "vertex_ms": round(max(0, vertex), 2),
                "fragment_ms": round(max(0, fragment), 2),
            })
        return {"frames": frames}

    p = Path(path)
    if not p.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(p.read_text())


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Metal performance data from Instruments exports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Usage:\n  python metal_performance_checker.py instruments.json --target-fps 90\n  python metal_performance_checker.py --test"
    )
    parser.add_argument("input", help="Instruments JSON export path, or --test for synthetic data")
    parser.add_argument("--target-fps", type=float, default=90, help="Target frame rate (default: 90)")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    data = load_input(args.input)
    frames = data.get("frames", [])

    if not frames:
        print("Error: no frame data found in input", file=sys.stderr)
        sys.exit(1)

    frame_times = [f["total_ms"] for f in frames if "total_ms" in f]
    stats = analyze_frame_times(frame_times, args.target_fps)
    stages = analyze_gpu_stages(frames)
    recs = recommend_optimizations(stats, stages, stats["target_ms"])

    if args.format == "json":
        print(json.dumps({"stats": stats, "stages": stages, "recommendations": recs}, indent=2))
        return

    print(f"\n=== Metal Performance Report (target: {args.target_fps}fps / {stats['target_ms']}ms) ===\n")
    print("Frame Time Distribution:")
    print(f"  Frames analyzed : {stats['count']}")
    print(f"  p50 (median)    : {stats['p50_ms']}ms")
    print(f"  p95             : {stats['p95_ms']}ms")
    print(f"  p99             : {stats['p99_ms']}ms")
    print(f"  Max             : {stats['max_ms']}ms")
    print(f"  Drop rate       : {stats['drop_rate_pct']}% ({stats['drop_count']} frames)")

    print("\nGPU Stage Breakdown (avg):")
    for stage, val in stages.items():
        label = stage.replace("avg_", "").replace("_ms", "").title()
        print(f"  {label:<12}: {val}ms" if val is not None else f"  {label:<12}: n/a")

    print(f"\nRecommendations ({len(recs)} items):")
    for i, rec in enumerate(recs, 1):
        print(f"\n  [{rec['priority']}] {rec['issue']}")
        print(f"  → {rec['action']}")


if __name__ == "__main__":
    main()
