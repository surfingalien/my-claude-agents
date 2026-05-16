#!/usr/bin/env python3
"""
Analyze webpack/Vite bundle stats JSON for size issues and duplicate dependencies.
Usage: python bundle_analyzer.py <stats.json> [--budget KB] [--duplicates] [--json]

Generate stats:
  webpack:  npx webpack --json > stats.json
  vite:     npx vite-bundle-visualizer --json > stats.json (community plugin)
"""
import argparse
import json
import sys
from collections import defaultdict


def bytes_to_kb(b: int) -> float:
    return round(b / 1024, 1)


def parse_webpack_assets(stats: dict) -> list[dict]:
    assets = []
    for asset in stats.get("assets", []):
        name = asset.get("name", "")
        size = asset.get("size", 0)
        if name.endswith((".js", ".css", ".mjs")):
            assets.append({"name": name, "size_bytes": size, "size_kb": bytes_to_kb(size)})
    assets.sort(key=lambda a: a["size_bytes"], reverse=True)
    return assets


def find_duplicates(stats: dict) -> dict[str, list[str]]:
    """Find the same module included in multiple chunks."""
    module_chunks: dict[str, list[str]] = defaultdict(list)
    for chunk in stats.get("chunks", []):
        chunk_name = chunk.get("id", "unknown")
        for mod in chunk.get("modules", []):
            mod_name = mod.get("name", "")
            if mod_name and not mod_name.startswith("(webpack)"):
                module_chunks[mod_name].append(str(chunk_name))
    return {mod: chunks for mod, chunks in module_chunks.items() if len(chunks) > 1}


def run(stats_path: str, budget_kb: int | None, show_duplicates: bool, as_json: bool) -> None:
    try:
        with open(stats_path) as f:
            stats = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {stats_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    assets = parse_webpack_assets(stats)
    total_kb = sum(a["size_kb"] for a in assets)
    over_budget = [a for a in assets if budget_kb and a["size_kb"] > budget_kb]
    duplicates = find_duplicates(stats) if show_duplicates else {}

    if as_json:
        print(json.dumps({
            "total_kb": total_kb,
            "asset_count": len(assets),
            "assets": assets[:20],
            "over_budget": over_budget,
            "duplicate_modules": list(duplicates.keys())[:20],
        }, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"Bundle Analysis: {stats_path}")
    print(f"{'='*60}\n")
    print(f"  Total JS/CSS size : {total_kb:.1f} KB")
    print(f"  Asset count       : {len(assets)}")
    if budget_kb:
        status = "OK" if not over_budget else f"OVER BUDGET ({len(over_budget)} chunks)"
        print(f"  Budget ({budget_kb} KB/chunk): {status}")
    print()

    print("Largest Assets")
    print("-" * 50)
    for asset in assets[:10]:
        flag = " !" if budget_kb and asset["size_kb"] > budget_kb else "  "
        print(f"{flag} {asset['name']:<40} {asset['size_kb']:>8.1f} KB")
    print()

    if show_duplicates and duplicates:
        print(f"Duplicate Modules ({len(duplicates)} found)")
        print("-" * 50)
        for mod, chunks in list(duplicates.items())[:10]:
            short = mod[-60:] if len(mod) > 60 else mod
            print(f"  {short}")
            print(f"    → chunks: {', '.join(chunks)}")
        print()
    elif show_duplicates:
        print("No duplicate modules detected.\n")

    if over_budget:
        print(f"Chunks Exceeding {budget_kb} KB Budget")
        print("-" * 50)
        for asset in over_budget:
            print(f"  {asset['name']:<40} {asset['size_kb']:>8.1f} KB")
        print()
        print("Suggestions:")
        print("  • Split large chunks with dynamic import() at route boundaries")
        print("  • Use React.lazy / Vue defineAsyncComponent for heavy components")
        print("  • Check for accidentally bundled node_modules (externals config)")
        print("  • Run --duplicates to find modules included in multiple chunks")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze JS bundle stats for size issues")
    parser.add_argument("stats", help="Path to webpack/Vite stats JSON")
    parser.add_argument("--budget", type=int, metavar="KB", help="Max chunk size in KB")
    parser.add_argument("--duplicates", action="store_true", help="Detect duplicate modules")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    run(args.stats, args.budget, args.duplicates, args.json)


if __name__ == "__main__":
    main()
