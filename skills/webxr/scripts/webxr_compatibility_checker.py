#!/usr/bin/env python3
"""Checks WebXR feature support matrix across target browsers and devices."""

import sys
import json
import argparse

# Support matrix: device/browser -> feature -> status
# Status: "yes" | "partial" | "no" | "polyfill"
SUPPORT_MATRIX = {
    "quest2": {
        "browser": "Chrome/Edge for Meta",
        "immersive-vr": "yes",
        "immersive-ar": "no",
        "hand-tracking": "yes",
        "hit-test": "no",
        "depth-sensing": "no",
        "dom-overlay": "no",
        "layers": "yes",
        "anchors": "no",
        "mesh-detection": "no",
        "min_browser": "Chrome 90+",
        "performance_tier": "mid",
        "gpu": "Adreno 650",
        "notes": "Hand tracking requires headset setting enabled; no passthrough AR",
    },
    "quest3": {
        "browser": "Chrome/Edge for Meta",
        "immersive-vr": "yes",
        "immersive-ar": "yes",
        "hand-tracking": "yes",
        "hit-test": "yes",
        "depth-sensing": "partial",
        "dom-overlay": "yes",
        "layers": "yes",
        "anchors": "partial",
        "mesh-detection": "yes",
        "min_browser": "Chrome 110+",
        "performance_tier": "high",
        "gpu": "Snapdragon XR2 Gen 2",
        "notes": "Full color passthrough AR; mesh detection for room understanding",
    },
    "vision-pro": {
        "browser": "Safari (visionOS)",
        "immersive-vr": "partial",
        "immersive-ar": "partial",
        "hand-tracking": "partial",
        "hit-test": "no",
        "depth-sensing": "no",
        "dom-overlay": "no",
        "layers": "yes",
        "anchors": "no",
        "mesh-detection": "no",
        "min_browser": "Safari 17.4+",
        "performance_tier": "high",
        "gpu": "Apple M2",
        "notes": "WebXR experimental; immersive mode limited; native visionOS SDK preferred",
    },
    "hololens2": {
        "browser": "Edge (HoloLens)",
        "immersive-vr": "no",
        "immersive-ar": "yes",
        "hand-tracking": "partial",
        "hit-test": "yes",
        "depth-sensing": "no",
        "dom-overlay": "partial",
        "layers": "no",
        "anchors": "yes",
        "mesh-detection": "partial",
        "min_browser": "Edge 90+",
        "performance_tier": "mid",
        "gpu": "HPU 2.0 + Qualcomm Snapdragon 850",
        "notes": "AR-only (no VR mode); hand tracking via gesture recognition; anchors well supported",
    },
    "mobile-ar": {
        "browser": "Chrome Android (ARCore)",
        "immersive-vr": "no",
        "immersive-ar": "yes",
        "hand-tracking": "no",
        "hit-test": "yes",
        "depth-sensing": "partial",
        "dom-overlay": "yes",
        "layers": "no",
        "anchors": "partial",
        "mesh-detection": "no",
        "min_browser": "Chrome 81+",
        "performance_tier": "low",
        "gpu": "Varies (Adreno/Mali)",
        "notes": "Requires ARCore; input via screen tap/controller; no hand tracking",
    },
    "mobile-ios": {
        "browser": "Safari iOS (WebXR polyfill)",
        "immersive-vr": "no",
        "immersive-ar": "partial",
        "hand-tracking": "no",
        "hit-test": "partial",
        "depth-sensing": "no",
        "dom-overlay": "partial",
        "layers": "no",
        "anchors": "no",
        "mesh-detection": "no",
        "min_browser": "Safari 15.4+",
        "performance_tier": "low",
        "gpu": "Apple GPU (A-series)",
        "notes": "Requires WebXR polyfill; AR via Quick Look or limited WebXR AR",
    },
}

POLYFILLS = {
    "hand-tracking": "WebXR Hand Input Polyfill (not available for all devices)",
    "hit-test": "ARCore WebXR polyfill (Android only)",
    "anchors": "No widely-deployed polyfill; implement app-level anchor logic",
    "dom-overlay": "Simulate with HTML canvas overlay rendered to texture",
}

QUALITY_SETTINGS = {
    "high":  {"shadows": True,  "antialias": True,  "max_polygons": 500000, "texture_size": 2048, "target_fps": 90},
    "mid":   {"shadows": False, "antialias": True,  "max_polygons": 200000, "texture_size": 1024, "target_fps": 72},
    "low":   {"shadows": False, "antialias": False, "max_polygons": 50000,  "texture_size": 512,  "target_fps": 60},
}


def check_features(device: str, requested_features: list[str]) -> dict:
    if device not in SUPPORT_MATRIX:
        return {"error": f"Unknown device: {device}. Available: {', '.join(SUPPORT_MATRIX.keys())}"}

    profile = SUPPORT_MATRIX[device]
    results = {"device": device, "browser": profile["browser"], "features": {}}

    for feature in requested_features:
        status = profile.get(feature, "unknown")
        fallback = None
        if status == "no" and feature in POLYFILLS:
            fallback = POLYFILLS[feature]
            status = "polyfill"
        results["features"][feature] = {
            "status": status,
            "fallback": fallback,
        }

    results["performance_tier"] = profile["performance_tier"]
    results["recommended_quality"] = QUALITY_SETTINGS[profile["performance_tier"]]
    results["min_browser"] = profile["min_browser"]
    results["notes"] = profile["notes"]
    return results


def full_matrix(requested_features: list[str]) -> list[dict]:
    return [check_features(device, requested_features) for device in SUPPORT_MATRIX]


def print_table(results: list[dict], features: list[str]):
    print(f"\n{'Device':<15}", end="")
    for f in features:
        print(f"{f:<18}", end="")
    print("Tier")
    print("-" * (15 + 18 * len(features) + 6))

    for r in results:
        if "error" in r:
            print(f"{r.get('device', '?'):<15}ERROR: {r['error']}")
            continue
        print(f"{r['device']:<15}", end="")
        for f in features:
            status = r["features"].get(f, {}).get("status", "?")
            icon = {"yes": "✓", "partial": "~", "no": "✗", "polyfill": "P", "unknown": "?"}.get(status, "?")
            print(f"{icon + ' ' + status:<18}", end="")
        print(r["performance_tier"])

    print("\nLegend: ✓ yes | ~ partial | ✗ no | P polyfill available")


def main():
    parser = argparse.ArgumentParser(
        description="Check WebXR feature support matrix across target devices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python webxr_compatibility_checker.py --target quest3\n"
            "  python webxr_compatibility_checker.py --features hand-tracking,hit-test\n"
            "  python webxr_compatibility_checker.py --target all --format json"
        )
    )
    parser.add_argument("--target",
                        help=f"Target device (or 'all'). Choices: {', '.join(SUPPORT_MATRIX.keys())}, all")
    parser.add_argument("--features",
                        help="Comma-separated feature list: immersive-vr,immersive-ar,hand-tracking,hit-test,depth-sensing,dom-overlay,layers,anchors,mesh-detection")
    parser.add_argument("--browser", help="Filter by browser (informational only)")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    # Default feature set
    features = [f.strip() for f in args.features.split(",")] if args.features else [
        "immersive-vr", "immersive-ar", "hand-tracking", "hit-test", "dom-overlay"
    ]

    target = args.target or "all"

    if target == "all":
        results = full_matrix(features)
    elif target in SUPPORT_MATRIX:
        results = [check_features(target, features)]
    else:
        print(f"Error: unknown target '{target}'. Use: {', '.join(SUPPORT_MATRIX.keys())}, all", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print_table(results, features)
        # Print per-device notes
        print("\nDevice Notes:")
        for r in results:
            if "notes" in r:
                print(f"  {r['device']}: {r['notes']}")
            if r.get("recommended_quality"):
                q = r["recommended_quality"]
                print(f"    Quality ({r.get('performance_tier', '?')}): "
                      f"shadows={'on' if q['shadows'] else 'off'}, "
                      f"antialias={'on' if q['antialias'] else 'off'}, "
                      f"max polygons={q['max_polygons']:,}, "
                      f"target fps={q['target_fps']}")


if __name__ == "__main__":
    main()
