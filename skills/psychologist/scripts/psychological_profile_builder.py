#!/usr/bin/env python3
"""
Psychological Profile Builder — generates structured psychological profiles from
behavioral descriptions using Big Five and attachment theory frameworks.

Usage:
    python psychological_profile_builder.py character.json
    python psychological_profile_builder.py character.json --format json

Input JSON fields:
    name, behaviors[], key_relationships[], observed_reactions{stress, intimacy, conflict}

Example character.json:
{
  "name": "Aldric",
  "behaviors": ["meticulous planner", "avoids large gatherings", "keeps detailed journals",
                "becomes sarcastic under pressure", "rarely asks for help"],
  "key_relationships": ["protective of younger sister", "formal with superiors",
                        "maintains distance from peers"],
  "observed_reactions": {
    "stress": "becomes controlling, snaps at others, works longer hours",
    "intimacy": "deflects personal questions with humor, changes subject",
    "conflict": "uses logic to avoid emotional engagement, wins arguments but loses relationships",
    "success": "minimizes achievement, immediately focuses on next task",
    "failure": "catastrophizes privately, maintains composure publicly"
  }
}
"""

import argparse
import json
import sys

BIG_FIVE_INDICATORS = {
    "openness": {
        "high": ["creative", "curious", "imaginative", "unconventional", "artistic", "novel", "explores",
                 "reads widely", "philosophizes", "questions", "abstract"],
        "low": ["routine", "conventional", "practical", "traditional", "prefers familiar",
                "consistent", "structured", "predictable", "conservative"],
    },
    "conscientiousness": {
        "high": ["meticulous", "organized", "planned", "reliable", "disciplined", "thorough",
                 "careful", "detail-oriented", "prepared", "punctual", "systematic"],
        "low": ["spontaneous", "disorganized", "impulsive", "flexible", "scattered",
                "procrastinates", "forgets", "messy", "unpredictable"],
    },
    "extraversion": {
        "high": ["social", "outgoing", "talkative", "energized by people", "assertive",
                 "seeks attention", "enthusiastic", "gregarious", "dominant"],
        "low": ["reserved", "quiet", "prefers solitude", "avoids gatherings", "reflective",
                "private", "independent", "drained by crowds", "introspective"],
    },
    "agreeableness": {
        "high": ["cooperative", "trusting", "helpful", "empathetic", "accommodating",
                 "diplomatic", "forgiving", "compassionate", "warm"],
        "low": ["competitive", "skeptical", "critical", "direct", "demanding",
                "challenging", "sarcastic", "confrontational", "argumentative"],
    },
    "neuroticism": {
        "high": ["anxious", "moody", "stressed", "sensitive", "catastrophizes",
                 "worries", "emotional", "reactive", "volatile", "insecure"],
        "low": ["calm", "stable", "resilient", "even-tempered", "composed",
                "handles stress well", "secure", "unfazed"],
    },
}

ATTACHMENT_INDICATORS = {
    "secure": {
        "patterns": ["comfortable with closeness", "asks for help", "direct in conflict",
                     "trusts others", "recovers quickly from setbacks", "doesn't fear abandonment"],
    },
    "anxious_preoccupied": {
        "patterns": ["clings", "seeks reassurance", "fears abandonment", "monitors relationship health",
                     "escalates when ignored", "needs validation", "hypervigilant to rejection signals",
                     "possessive", "jealous"],
        "description": "Hyperactivating strategy: amplify attachment signals to get needs met",
    },
    "dismissive_avoidant": {
        "patterns": ["maintains distance", "self-reliant", "avoids intimacy", "deflects personal questions",
                     "rarely asks for help", "uncomfortable with closeness", "formally polite but distant",
                     "keeps emotional walls", "changes subject"],
        "description": "Deactivating strategy: suppress attachment needs, emphasize self-sufficiency",
    },
    "fearful_avoidant": {
        "patterns": ["inconsistent", "hot and cold", "pursues then withdraws", "wants closeness but fears it",
                     "sabotages relationships", "distrusts while craving connection"],
        "description": "Oscillates between hyperactivating and deactivating strategies",
    },
}

DEFENSE_MECHANISMS = {
    "intellectualization": ["uses logic", "analyzes emotions", "avoids emotional engagement",
                            "objective about personal pain", "theorizes about feelings"],
    "humor": ["deflects with humor", "jokes under pressure", "self-deprecating",
              "makes light of serious situations"],
    "reaction_formation": ["opposite of expected", "overly positive about disliked things",
                           "aggressive kindness"],
    "projection": ["attributes own feelings to others", "assumes others have hidden motives",
                   "blames others for own impulses"],
    "rationalization": ["explains away behavior", "post-hoc justifications", "excuses"],
    "displacement": ["redirects anger", "snaps at safe targets", "takes frustration elsewhere"],
    "compartmentalization": ["separates contradictory beliefs", "functions well despite trauma",
                             "walls off difficult emotions", "maintains composure publicly"],
    "sublimation": ["channels impulses productively", "uses energy for work or art",
                    "converts negative energy into achievement"],
    "passive_aggression": ["indirect anger", "procrastination as resistance", "forgets to help",
                           "subtle sabotage"],
    "suppression": ["conscious avoidance of thoughts", "puts aside for later",
                    "postpones dealing with problems"],
}


def score_trait(text, trait):
    text_lower = text.lower()
    high_score = sum(1 for kw in BIG_FIVE_INDICATORS[trait]["high"] if kw in text_lower)
    low_score = sum(1 for kw in BIG_FIVE_INDICATORS[trait]["low"] if kw in text_lower)
    net = high_score - low_score
    if net > 1:
        return "High"
    elif net < -1:
        return "Low"
    else:
        return "Mid"


def assess_attachment(text):
    text_lower = text.lower()
    scores = {}
    for style, data in ATTACHMENT_INDICATORS.items():
        scores[style] = sum(1 for p in data["patterns"] if p in text_lower)
    return max(scores, key=scores.get), scores


def identify_defenses(text):
    text_lower = text.lower()
    found = []
    for defense, keywords in DEFENSE_MECHANISMS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(defense.replace("_", " ").title())
    return found[:3] if found else ["Insufficient data for assessment"]


def build_profile(character):
    full_text = " ".join([
        " ".join(character.get("behaviors", [])),
        " ".join(character.get("key_relationships", [])),
        " ".join(character.get("observed_reactions", {}).values()),
    ])

    traits = {trait: score_trait(full_text, trait) for trait in BIG_FIVE_INDICATORS}
    attachment_style, attachment_scores = assess_attachment(full_text)
    defenses = identify_defenses(full_text)

    return {
        "name": character.get("name", "Unnamed"),
        "big_five": traits,
        "attachment_style": attachment_style.replace("_", "-").title(),
        "primary_defenses": defenses,
        "confidence": "Low-Medium (heuristic assessment — verify with narrative evidence)",
        "attachment_note": ATTACHMENT_INDICATORS.get(attachment_style, {}).get("description", ""),
    }


def print_profile(profile):
    print(f"\n{'='*60}")
    print(f"  Psychological Profile: {profile['name']}")
    print(f"{'='*60}")
    print(f"\n  ─── Big Five Personality Traits ───────────────────────")
    for trait, level in profile["big_five"].items():
        bar = "█" * (3 if level == "High" else 2 if level == "Mid" else 1)
        print(f"  {trait.capitalize():<20} {level:<6} {bar}")

    print(f"\n  ─── Attachment Style ──────────────────────────────────")
    print(f"  Style: {profile['attachment_style']}")
    if profile["attachment_note"]:
        print(f"  Pattern: {profile['attachment_note']}")

    print(f"\n  ─── Primary Defense Mechanisms ────────────────────────")
    for d in profile["primary_defenses"]:
        print(f"  • {d}")

    print(f"\n  ─── Confidence Level ──────────────────────────────────")
    print(f"  {profile['confidence']}")
    print(f"\n  NOTE: Always ground psychological assessments in specific")
    print(f"  behavioral evidence. These are hypotheses, not diagnoses.")
    print()


def main():
    parser = argparse.ArgumentParser(description="Psychological Profile Builder")
    parser.add_argument("character_file", help="JSON file with character description")
    parser.add_argument("--format", choices=["report", "json"], default="report")
    args = parser.parse_args()

    try:
        with open(args.character_file) as f:
            character = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{args.character_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    profile = build_profile(character)

    if args.format == "json":
        print(json.dumps(profile, indent=2))
    else:
        print_profile(profile)


if __name__ == "__main__":
    main()
