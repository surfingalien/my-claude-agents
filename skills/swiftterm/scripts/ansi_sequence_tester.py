#!/usr/bin/env python3
"""Generates ANSI test sequences to validate SwiftTerm VT100/xterm rendering."""

import sys
import json
import argparse

ESC = "\x1b"
BEL = "\x07"


def suite_cursor() -> list[dict]:
    return [
        {"name": "Cursor Home",          "seq": f"{ESC}[H",       "expect": "Cursor at top-left (0,0)"},
        {"name": "Cursor Up 3",          "seq": f"{ESC}[3A",      "expect": "Cursor moves 3 rows up"},
        {"name": "Cursor Down 2",        "seq": f"{ESC}[2B",      "expect": "Cursor moves 2 rows down"},
        {"name": "Cursor Right 5",       "seq": f"{ESC}[5C",      "expect": "Cursor moves 5 columns right"},
        {"name": "Cursor Left 5",        "seq": f"{ESC}[5D",      "expect": "Cursor moves 5 columns left"},
        {"name": "Cursor to Row 5 Col 10", "seq": f"{ESC}[5;10H", "expect": "Cursor at row 5, col 10"},
        {"name": "Save Cursor",          "seq": f"{ESC}[s",       "expect": "Cursor position saved"},
        {"name": "Restore Cursor",       "seq": f"{ESC}[u",       "expect": "Cursor position restored"},
        {"name": "Cursor Invisible",     "seq": f"{ESC}[?25l",    "expect": "Cursor hidden"},
        {"name": "Cursor Visible",       "seq": f"{ESC}[?25h",    "expect": "Cursor shown"},
    ]


def suite_sgr() -> list[dict]:
    return [
        {"name": "Reset",          "seq": f"{ESC}[0m",        "expect": "All attributes cleared"},
        {"name": "Bold",           "seq": f"{ESC}[1mBold{ESC}[0m", "expect": "Text appears bold"},
        {"name": "Dim",            "seq": f"{ESC}[2mDim{ESC}[0m",  "expect": "Text appears dim"},
        {"name": "Italic",         "seq": f"{ESC}[3mItalic{ESC}[0m", "expect": "Text appears italic"},
        {"name": "Underline",      "seq": f"{ESC}[4mUnder{ESC}[0m", "expect": "Text underlined"},
        {"name": "Blink",          "seq": f"{ESC}[5mBlink{ESC}[0m", "expect": "Text blinks (or rendered specially)"},
        {"name": "Reverse Video",  "seq": f"{ESC}[7mRev{ESC}[0m",   "expect": "FG/BG colors swapped"},
        {"name": "Strikethrough",  "seq": f"{ESC}[9mStrike{ESC}[0m","expect": "Text struck through"},
        {"name": "Red FG",         "seq": f"{ESC}[31mRed{ESC}[0m",  "expect": "Red foreground text"},
        {"name": "Green FG",       "seq": f"{ESC}[32mGreen{ESC}[0m","expect": "Green foreground text"},
        {"name": "Yellow BG",      "seq": f"{ESC}[43mYellowBG{ESC}[0m", "expect": "Yellow background"},
        {"name": "256-color FG",   "seq": f"{ESC}[38;5;196mRed256{ESC}[0m", "expect": "256-color red (index 196)"},
        {"name": "True color FG",  "seq": f"{ESC}[38;2;255;100;0mOrange{ESC}[0m", "expect": "24-bit orange (255,100,0)"},
        {"name": "True color BG",  "seq": f"{ESC}[48;2;0;100;200mBlueBG{ESC}[0m", "expect": "24-bit blue background"},
        {"name": "Bright Red FG",  "seq": f"{ESC}[91mBrightRed{ESC}[0m", "expect": "Bright red (ANSI 16-color)"},
    ]


def suite_erase() -> list[dict]:
    return [
        {"name": "Erase to End of Line",    "seq": f"{ESC}[K",   "expect": "Erases from cursor to EOL"},
        {"name": "Erase to Start of Line",  "seq": f"{ESC}[1K",  "expect": "Erases from SOL to cursor"},
        {"name": "Erase Entire Line",       "seq": f"{ESC}[2K",  "expect": "Entire current line cleared"},
        {"name": "Erase to End of Screen",  "seq": f"{ESC}[J",   "expect": "Clears below cursor"},
        {"name": "Erase to Start of Screen","seq": f"{ESC}[1J",  "expect": "Clears above cursor"},
        {"name": "Erase Entire Screen",     "seq": f"{ESC}[2J",  "expect": "Full screen cleared"},
        {"name": "Erase Saved Lines",       "seq": f"{ESC}[3J",  "expect": "Scrollback buffer cleared"},
    ]


def suite_osc() -> list[dict]:
    return [
        {"name": "Set Window Title",
         "seq": f"{ESC}]0;MyTitle{BEL}",
         "expect": "Window/tab title changes to 'MyTitle'"},
        {"name": "Set Icon Name",
         "seq": f"{ESC}]1;Icon{BEL}",
         "expect": "Icon label set to 'Icon'"},
        {"name": "Hyperlink",
         "seq": f"{ESC}]8;;https://example.com{BEL}Click{ESC}]8;;{BEL}",
         "expect": "Clickable hyperlink 'Click' pointing to example.com"},
        {"name": "iTerm2 Notification",
         "seq": f"{ESC}]9;Alert: process done{BEL}",
         "expect": "System notification posted (iTerm2 protocol)"},
        {"name": "Working Directory",
         "seq": f"{ESC}]7;file:///tmp/work{BEL}",
         "expect": "Terminal working directory hint set"},
    ]


def suite_colors() -> list[dict]:
    """Generate a visible color ramp test."""
    seqs = []
    # 16 ANSI colors
    for i in range(8):
        seqs.append({
            "name": f"ANSI Standard Color {i}",
            "seq": f"{ESC}[{30+i}m█{ESC}[0m",
            "expect": f"Standard ANSI color {i} foreground block"
        })
    for i in range(8):
        seqs.append({
            "name": f"ANSI Bright Color {i}",
            "seq": f"{ESC}[{90+i}m█{ESC}[0m",
            "expect": f"Bright ANSI color {i} foreground block"
        })
    # 256-color ramp sample
    for idx in [0, 21, 46, 82, 118, 154, 196, 208, 226, 255]:
        seqs.append({
            "name": f"256-color index {idx}",
            "seq": f"{ESC}[38;5;{idx}m▓{ESC}[0m",
            "expect": f"256-color palette index {idx}"
        })
    return seqs


SUITES = {
    "cursor": suite_cursor,
    "sgr": suite_sgr,
    "colors": suite_colors,
    "erase": suite_erase,
    "osc": suite_osc,
}


def all_suites() -> list[dict]:
    result = []
    for name, fn in SUITES.items():
        for test in fn():
            test["suite"] = name
            result.append(test)
    return result


def generate_shell_script(tests: list[dict]) -> str:
    lines = ["#!/bin/bash", "# SwiftTerm ANSI Test Script", "# Generated by ansi_sequence_tester.py", ""]
    for test in tests:
        safe_name = test["name"].replace("'", "\\'")
        lines.append(f"echo '--- {safe_name} ---'")
        # Escape the sequence for printf
        seq_escaped = test["seq"].replace(ESC, "\\033").replace(BEL, "\\007")
        lines.append(f"printf '{seq_escaped}'")
        expect = test["expect"]
        lines.append(f"echo '  [{expect}]'")
        lines.append("sleep 0.1")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate ANSI test sequences for SwiftTerm validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python ansi_sequence_tester.py --suite colors\n"
            "  python ansi_sequence_tester.py --suite full --format json\n"
            "  python ansi_sequence_tester.py --suite sgr > test.sh && bash test.sh"
        )
    )
    parser.add_argument(
        "--suite",
        choices=list(SUITES.keys()) + ["full"],
        default="full",
        help="Test suite to generate (default: full)"
    )
    parser.add_argument("--format", choices=["shell", "json"], default="shell")
    args = parser.parse_args()

    if args.suite == "full":
        tests = all_suites()
    else:
        tests = SUITES[args.suite]()
        for t in tests:
            t["suite"] = args.suite

    if args.format == "json":
        # Sanitize non-printable chars for JSON output
        safe_tests = []
        for t in tests:
            st = dict(t)
            st["seq"] = repr(t["seq"])
            safe_tests.append(st)
        print(json.dumps(safe_tests, indent=2))
    else:
        print(generate_shell_script(tests))


if __name__ == "__main__":
    main()
