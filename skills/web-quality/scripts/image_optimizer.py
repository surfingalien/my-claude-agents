#!/usr/bin/env python3
"""
Scan a directory for unoptimized images: oversized files, missing modern formats,
no width/height attributes in co-located HTML, and non-lazy loaded images.
Usage: python image_optimizer.py <directory> [--max-size KB] [--json]
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".avif"}
MODERN_FORMATS = {".webp", ".avif"}
LEGACY_RASTER = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

DEFAULT_MAX_SIZE_KB = 200


def scan_images(directory: str, max_size_kb: int) -> list[dict]:
    findings = []
    root = Path(directory)
    if not root.exists():
        print(f"Error: directory not found: {directory}", file=sys.stderr)
        sys.exit(1)

    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        size_kb = path.stat().st_size / 1024
        issues = []

        if size_kb > max_size_kb:
            issues.append(f"oversized ({size_kb:.0f} KB > {max_size_kb} KB limit)")

        if path.suffix.lower() in LEGACY_RASTER:
            # Check if a modern format sibling exists
            has_modern = any(
                path.with_suffix(ext).exists() for ext in MODERN_FORMATS
            )
            if not has_modern:
                issues.append("no WebP/AVIF alternate found")

        if issues:
            findings.append({
                "path": str(path.relative_to(root)),
                "size_kb": round(size_kb, 1),
                "issues": issues,
            })

    return findings


def scan_html_for_img_issues(directory: str) -> list[dict]:
    """Check HTML/JSX files for <img> tags missing width, height, or loading=lazy."""
    issues = []
    root = Path(directory)
    html_extensions = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte"}
    img_tag_re = re.compile(r"<img\b([^>]*)>", re.IGNORECASE | re.DOTALL)

    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in html_extensions:
            continue
        try:
            content = path.read_text(errors="ignore")
        except OSError:
            continue

        for match in img_tag_re.finditer(content):
            attrs = match.group(1)
            tag_issues = []
            if "width" not in attrs:
                tag_issues.append("missing width")
            if "height" not in attrs:
                tag_issues.append("missing height")
            if "loading" not in attrs:
                tag_issues.append("missing loading=lazy")
            if tag_issues:
                line_no = content[: match.start()].count("\n") + 1
                issues.append({
                    "file": str(path.relative_to(root)),
                    "line": line_no,
                    "issues": tag_issues,
                    "snippet": match.group(0)[:120],
                })
    return issues


def run(directory: str, max_size_kb: int, as_json: bool) -> None:
    image_findings = scan_images(directory, max_size_kb)
    html_findings = scan_html_for_img_issues(directory)

    if as_json:
        print(json.dumps({
            "directory": directory,
            "max_size_kb": max_size_kb,
            "image_issues": image_findings,
            "html_img_issues": html_findings,
        }, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"Image Optimization Audit: {directory}")
    print(f"{'='*60}\n")

    if image_findings:
        print(f"Image Issues ({len(image_findings)} files)")
        print("-" * 50)
        for f in image_findings:
            print(f"  {f['path']} ({f['size_kb']} KB)")
            for issue in f["issues"]:
                print(f"    • {issue}")
        print()
    else:
        print("  No image file issues found.\n")

    if html_findings:
        print(f"<img> Tag Issues ({len(html_findings)} occurrences)")
        print("-" * 50)
        for f in html_findings:
            print(f"  {f['file']}:{f['line']}")
            for issue in f["issues"]:
                print(f"    • {issue}")
        print()
    else:
        print("  No <img> tag issues found.\n")

    if image_findings or html_findings:
        print("Recommendations:")
        print("  • Convert JPEG/PNG to WebP: `cwebp -q 80 input.jpg -o output.webp`")
        print("  • Convert to AVIF: `avifenc --min 0 --max 63 input.png output.avif`")
        print("  • Use <picture> with WebP/AVIF source + JPEG fallback")
        print("  • Always set width & height to prevent layout shift (CLS)")
        print("  • Add loading=lazy to below-fold images")
        print("  • Use srcset for responsive images")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan for unoptimized images")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("--max-size", type=int, default=DEFAULT_MAX_SIZE_KB,
                        metavar="KB", dest="max_size", help=f"Max image size in KB (default: {DEFAULT_MAX_SIZE_KB})")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    run(args.directory, args.max_size, args.json)


if __name__ == "__main__":
    main()
