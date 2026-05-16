#!/usr/bin/env python3
"""
Cultural Coherence Checker — validates cultural system consistency across subsistence,
social organization, and belief system elements.

Usage:
    python cultural_coherence_checker.py culture.json
    python cultural_coherence_checker.py culture.json --format json

Input JSON fields:
    name, subsistence_mode, exchange_system, kinship_type, residence_pattern,
    political_organization, ritual_specialists[], cosmology_elements[]

Example culture.json:
{
  "name": "The Arathi",
  "subsistence_mode": "agricultural",
  "exchange_system": "redistribution",
  "kinship_type": "matrilineal",
  "residence_pattern": "patrilocal",
  "political_organization": "chiefdom",
  "ritual_specialists": ["priest"],
  "cosmology_elements": ["ancestor veneration", "agricultural fertility rites"]
}
"""

import argparse
import json
import sys

COHERENCE_RULES = [
    {
        "check": "patrilocal_matrilineal",
        "condition": lambda c: c.get("kinship_type") == "matrilineal" and c.get("residence_pattern") == "patrilocal",
        "severity": "HIGH",
        "message": "Patrilocal residence with matrilineal descent creates structural tension: "
                   "children belong to mother's lineage but live with father's kin. "
                   "This is rare and requires explicit explanation (e.g., Ashanti solve this "
                   "through avunculocal residence — consider avunculocal instead).",
        "recommendation": "Switch to matrilocal or avunculocal residence, OR add narrative "
                          "explanation for how the tension is managed politically.",
    },
    {
        "check": "state_foraging",
        "condition": lambda c: c.get("subsistence_mode") == "foraging" and c.get("political_organization") == "state",
        "severity": "HIGH",
        "message": "Foraging societies virtually never develop state-level organization. "
                   "States require surplus agriculture to feed non-producing specialists "
                   "(bureaucrats, soldiers, artisans). No documented forager states exist.",
        "recommendation": "Use band or tribe organization for foragers, OR change subsistence "
                          "to intensive agriculture/pastoralism if you need state organization.",
    },
    {
        "check": "market_band",
        "condition": lambda c: c.get("exchange_system") == "market" and c.get("political_organization") == "band",
        "severity": "MEDIUM",
        "message": "Market exchange in band-level societies is atypical. Bands rely on "
                   "generalized reciprocity internally. Market exchange requires surpluses, "
                   "standardized values, and enforcement mechanisms bands lack.",
        "recommendation": "Use generalized or balanced reciprocity for band societies. "
                          "Markets require at least chiefdom-level infrastructure.",
    },
    {
        "check": "priest_band",
        "condition": lambda c: "priest" in [s.lower() for s in c.get("ritual_specialists", [])]
                               and c.get("political_organization") == "band",
        "severity": "MEDIUM",
        "message": "Priestly specialist roles (institutionalized, bureaucratic) are rare in "
                   "band-level societies. Bands typically have shamans (personal charismatic "
                   "authority) rather than priests (office-based institutional authority).",
        "recommendation": "Consider shaman instead of priest for band organization, or "
                          "explain the institutional support system that maintains the priestly role.",
    },
    {
        "check": "redistribution_band",
        "condition": lambda c: c.get("exchange_system") == "redistribution" and c.get("political_organization") == "band",
        "severity": "LOW",
        "message": "Full redistribution (goods flow to central authority then redistributed) "
                   "typically requires chiefdom-level hierarchy. Bands have sharing norms "
                   "but not centralized redistribution infrastructure.",
        "recommendation": "Generalized reciprocity fits bands better. Redistribution fits "
                          "chiefdoms and states. Consider balanced reciprocity as a middle ground.",
    },
    {
        "check": "neolocal_foraging",
        "condition": lambda c: c.get("residence_pattern") == "neolocal" and c.get("subsistence_mode") == "foraging",
        "severity": "MEDIUM",
        "message": "Neolocal residence (independent nuclear family household) is rare in "
                   "foraging societies, which typically rely on extended kin cooperation "
                   "for subsistence. Neolocality is primarily an industrial/post-industrial pattern.",
        "recommendation": "Use bilateral band residence (flexible, following resources and kin) "
                          "for foragers. Neolocality requires economic independence not available in foraging.",
    },
]

REAL_WORLD_PARALLELS = {
    ("agricultural", "patrilineal", "chiefdom"): ["Ashanti (Ghana)", "Zulu (South Africa)", "many Polynesian chiefdoms"],
    ("agricultural", "matrilineal", "chiefdom"): ["Minangkabau (Indonesia)", "Khasi (India)", "Iroquois Confederacy"],
    ("foraging", "bilateral", "band"): ["!Kung San (Kalahari)", "Hadza (Tanzania)", "most Arctic foragers"],
    ("pastoral", "patrilineal", "tribe"): ["Nuer (South Sudan)", "Bedouin societies", "Maasai (East Africa)"],
    ("agricultural", "bilateral", "state"): ["most modern states", "Medieval European kingdoms"],
    ("agricultural", "patrilineal", "state"): ["Classical China", "Ancient Rome (early)", "most ancient empires"],
}

MISSING_ELEMENT_CHECKS = [
    {
        "check": "cosmology_missing",
        "condition": lambda c: not c.get("cosmology_elements"),
        "message": "No cosmology specified. Every society has explanations for the world's origin and structure. What do these people believe about creation, death, and cosmic order?",
    },
    {
        "check": "ritual_specialists_missing",
        "condition": lambda c: not c.get("ritual_specialists"),
        "message": "No ritual specialists specified. All known societies have some form of religious or ritual specialist. Who mediates between humans and the sacred?",
    },
    {
        "check": "exchange_missing",
        "condition": lambda c: not c.get("exchange_system"),
        "message": "No exchange system specified. How do goods and labor flow through this society? (Polanyi: reciprocity / redistribution / market)",
    },
]


def find_parallels(culture):
    key = (
        culture.get("subsistence_mode", ""),
        culture.get("kinship_type", ""),
        culture.get("political_organization", ""),
    )
    return REAL_WORLD_PARALLELS.get(key, [])


def check_coherence(culture):
    issues = []
    missing = []

    for rule in COHERENCE_RULES:
        try:
            if rule["condition"](culture):
                issues.append({
                    "check": rule["check"],
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "recommendation": rule["recommendation"],
                })
        except (KeyError, TypeError):
            pass

    for rule in MISSING_ELEMENT_CHECKS:
        try:
            if rule["condition"](culture):
                missing.append({
                    "check": rule["check"],
                    "message": rule["message"],
                })
        except (KeyError, TypeError):
            pass

    parallels = find_parallels(culture)
    score = max(0, 100 - len([i for i in issues if i["severity"] == "HIGH"]) * 30
                - len([i for i in issues if i["severity"] == "MEDIUM"]) * 15
                - len([i for i in issues if i["severity"] == "LOW"]) * 5
                - len(missing) * 5)

    return {
        "culture_name": culture.get("name", "Unnamed"),
        "coherence_score": score,
        "issues": issues,
        "missing_elements": missing,
        "real_world_parallels": parallels,
    }


def print_report(result):
    print(f"\n{'='*65}")
    print(f"  Cultural Coherence Check: {result['culture_name']}")
    print(f"{'='*65}")
    print(f"\n  Coherence Score: {result['coherence_score']}/100")

    if not result["issues"] and not result["missing_elements"]:
        print("\n  ✓ No coherence issues found. Cultural system appears internally consistent.")
    else:
        if result["issues"]:
            print(f"\n  COHERENCE ISSUES ({len(result['issues'])} found)")
            print(f"  {'─'*55}")
            for i, issue in enumerate(result["issues"], 1):
                sev = issue["severity"]
                print(f"\n  {i}. [{sev}] {issue['check'].replace('_', ' ').title()}")
                print(f"     Problem: {issue['message']}")
                print(f"     Fix: {issue['recommendation']}")

        if result["missing_elements"]:
            print(f"\n  MISSING ELEMENTS ({len(result['missing_elements'])} found)")
            print(f"  {'─'*55}")
            for item in result["missing_elements"]:
                print(f"\n  • {item['message']}")

    if result["real_world_parallels"]:
        print(f"\n  REAL-WORLD ETHNOGRAPHIC PARALLELS")
        print(f"  {'─'*55}")
        for p in result["real_world_parallels"]:
            print(f"  → {p}")
        print(f"\n  (Study these for authentic cultural detail and problem-solving patterns)")

    print()


def main():
    parser = argparse.ArgumentParser(description="Cultural Coherence Checker")
    parser.add_argument("culture_file", help="JSON file with cultural system description")
    parser.add_argument("--format", choices=["report", "json"], default="report")
    args = parser.parse_args()

    try:
        with open(args.culture_file) as f:
            culture = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{args.culture_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    result = check_coherence(culture)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
