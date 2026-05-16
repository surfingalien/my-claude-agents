#!/usr/bin/env python3
"""
Narrative Debt Tracker — identifies story setups (Chekhov's guns) and tracks
whether they are paid off within a manuscript or outline.

Usage:
    python narrative_debt_tracker.py manuscript.txt
    python narrative_debt_tracker.py outline.txt --format json
    python narrative_debt_tracker.py story.txt --sensitivity high

A "narrative debt" is any story element that creates an expectation in the reader
that demands resolution: introduced objects, character traits, promises, mysteries,
foreshadowing, and dramatic irony setups.
"""

import argparse
import json
import re
import sys

# Patterns that typically create narrative debts (setups requiring payoff)
SETUP_PATTERNS = [
    # Objects that tend to reappear
    (r'\b(gun|weapon|sword|knife|pistol|revolver|rifle|bow)\b', "introduced weapon — Chekhov's gun principle"),
    (r'\b(letter|note|message|document|diary|journal|map|key|locket|ring|amulet|artifact)\b', "significant object introduced"),
    (r'\b(secret|hidden|concealed|buried|locked)\b', "secret/hidden element introduced"),
    (r'\b(scar|mark|tattoo|brand|birthmark)\b', "physical marking introduced — likely significant"),

    # Character introductions that promise development
    (r'\b(mysterious|enigmatic|unknown|stranger)\b', "mysterious element introduced — requires revelation"),
    (r'\b(will|shall|one day|someday|eventually|destiny|fate|prophecy|foretold)\b', "future promise / prophecy introduced"),
    (r'\b(never|always|swore|vowed|promised|oath|pledge)\b', "character vow/promise introduced"),
    (r'\b(hated|feared|obsessed|haunted|traumatized|never forgave)\b", "character wound/obsession introduced'),

    # Plot setups
    (r'\b(rumor|legend|myth|story|tale|said that|they say)\b', "legendary/mythic element introduced"),
    (r'\b(warning|beware|danger|careful|shouldn\'t)\b', "warning issued — likely to be ignored with consequences"),
    (r'\b(foreshadow|omen|sign|portent|dream|vision)\b', "foreshadowing element"),
    (r'\b(unfinished|incomplete|later|return|come back|pick up where)\b', "deferred action — must be resolved"),
]

# Patterns that suggest payoffs (resolutions of setups)
PAYOFF_PATTERNS = [
    r'\b(revealed|discovered|found|uncovered|exposed)\b',
    r'\b(finally|at last|realized|understood|knew)\b',
    r'\b(remembered|recalled|returned to|came back)\b',
    r'\b(used|fired|drew|pulled out|opened|unlocked)\b',
    r'\b(fulfilled|kept|broke|betrayed|honored)\b',
    r'\b(came true|proved|turned out|was right)\b',
]


def extract_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def find_setups(sentences):
    setups = []
    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        for pattern, description in SETUP_PATTERNS:
            matches = re.findall(pattern, sentence_lower)
            if matches:
                for match in set(matches):
                    setups.append({
                        "sentence_index": i,
                        "sentence_preview": sentence[:120] + ("..." if len(sentence) > 120 else ""),
                        "trigger_word": match,
                        "description": description,
                        "status": "outstanding",
                    })
                break  # One description per sentence to avoid duplicate flagging
    return setups


def find_payoffs(sentences):
    payoff_positions = []
    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        for pattern in PAYOFF_PATTERNS:
            if re.search(pattern, sentence_lower):
                payoff_positions.append(i)
                break
    return payoff_positions


def assess_debts(setups, payoff_positions, total_sentences):
    assessed = []
    for setup in setups:
        idx = setup["sentence_index"]
        # A payoff exists if there's a payoff-pattern sentence after the setup
        later_payoffs = [p for p in payoff_positions if p > idx]
        # Rough heuristic: if there's a payoff in the latter half of the story, likely resolved
        story_midpoint = total_sentences // 2
        has_likely_payoff = any(p > story_midpoint for p in later_payoffs)

        setup["status"] = "likely_paid" if has_likely_payoff else "outstanding"
        assessed.append(setup)
    return assessed


def print_report(debts, total_sentences):
    outstanding = [d for d in debts if d["status"] == "outstanding"]
    likely_paid = [d for d in debts if d["status"] == "likely_paid"]

    print(f"\n{'='*65}")
    print(f"  Narrative Debt Tracker")
    print(f"{'='*65}")
    print(f"\n  Sentences analyzed: {total_sentences}")
    print(f"  Setups detected: {len(debts)}")
    print(f"  Likely paid off: {len(likely_paid)}")
    print(f"  Outstanding (unresolved): {len(outstanding)}")

    if outstanding:
        print(f"\n  OUTSTANDING NARRATIVE DEBTS")
        print(f"  {'─'*55}")
        print(f"  These setups may not have been paid off — verify manually:\n")
        for i, debt in enumerate(outstanding, 1):
            print(f"  {i}. [{debt['trigger_word']}] — {debt['description']}")
            print(f"     Near: \"{debt['sentence_preview']}\"")
            print()

    if likely_paid:
        print(f"  LIKELY RESOLVED ({len(likely_paid)} setups)")
        print(f"  {'─'*55}")
        print(f"  (Verify manually — heuristic detection only)\n")
        for debt in likely_paid[:5]:  # Show first 5
            print(f"  ✓ [{debt['trigger_word']}] near: \"{debt['sentence_preview'][:80]}...\"")
        if len(likely_paid) > 5:
            print(f"  ... and {len(likely_paid) - 5} more")

    print(f"\n  ─── NOTE ──────────────────────────────────────────────────")
    print(f"  This is a heuristic detector, not a comprehensive reader.")
    print(f"  Always verify setups and payoffs through careful re-reading.")
    print(f"  Not all introduced elements need payoff — only those that")
    print(f"  create an expectation of significance in the reader.")


def main():
    parser = argparse.ArgumentParser(description="Narrative Debt Tracker (Chekhov's Gun)")
    parser.add_argument("manuscript", help="Text file to analyze")
    parser.add_argument("--format", choices=["report", "json"], default="report")
    parser.add_argument("--sensitivity", choices=["low", "medium", "high"], default="medium",
                        help="Detection sensitivity (high = more flags, more false positives)")
    args = parser.parse_args()

    try:
        with open(args.manuscript) as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.manuscript}' not found.", file=sys.stderr)
        sys.exit(1)

    sentences = extract_sentences(text)
    setups = find_setups(sentences)
    payoff_positions = find_payoffs(sentences)
    debts = assess_debts(setups, payoff_positions, len(sentences))

    # Deduplicate by trigger word (keep first occurrence)
    seen_triggers = set()
    unique_debts = []
    for debt in debts:
        if debt["trigger_word"] not in seen_triggers:
            seen_triggers.add(debt["trigger_word"])
            unique_debts.append(debt)

    if args.format == "json":
        print(json.dumps({
            "total_sentences": len(sentences),
            "debts_found": len(unique_debts),
            "outstanding": len([d for d in unique_debts if d["status"] == "outstanding"]),
            "items": unique_debts,
        }, indent=2))
    else:
        print_report(unique_debts, len(sentences))


if __name__ == "__main__":
    main()
