#!/usr/bin/env python3
"""
Anachronism Checker — scans text descriptions for period-inconsistent technologies,
social structures, and cultural elements.

Usage:
    python anachronism_checker.py description.txt --period "14th century Europe"
    python anachronism_checker.py description.txt --period "Tang Dynasty China" --format json

Checks against a curated database of invention/appearance dates for common
anachronism traps in historical fiction and worldbuilding.
"""

import argparse
import json
import re
import sys

# Database: {term: {first_appears: description, regions: [], anachronistic_before: description}}
TECHNOLOGY_DATABASE = {
    # Armor
    "plate armor": {
        "appears": "Western Europe, ~1350-1420 CE (gradual development)",
        "before": "High Middle Ages Europe (before ~1350)",
        "note": "Before plate armor: chainmail + padding (hauberk, gambeson) was standard"
    },
    "full plate": {
        "appears": "Europe, ~1420-1500 CE",
        "before": "Medieval Europe before 15th century",
        "note": "Full suits of plate not common until late 15th century"
    },
    "chainmail": {
        "appears": "Ancient world (Celts, Romans); widely used medieval Europe",
        "before": "None for most medieval settings",
        "note": "Chainmail (maille) is appropriate for medieval settings; not anachronistic"
    },

    # Weapons
    "gunpowder": {
        "appears": "China, ~9th century CE; Europe, ~13th century CE",
        "before": "Ancient world, early medieval Europe",
        "note": "Chinese innovation; arrived in Europe via Mongol expansion ~1241"
    },
    "firearms": {
        "appears": "China, ~13th century; Europe, ~14th century (crude hand cannons)",
        "before": "Pre-medieval settings; early medieval Europe",
        "note": "Early firearms were slow, inaccurate, and unreliable; not dominant until 16th-17th c."
    },
    "cannon": {
        "appears": "China, 12th-13th c.; Europe, ~1320-1350 CE",
        "before": "Ancient world through early medieval Europe",
        "note": "Trebuchets and ballistae were the dominant siege weapons before cannon"
    },
    "crossbow": {
        "appears": "Ancient China; ancient Mediterranean; medieval Europe throughout",
        "before": "None for most settings — crossbow is ancient",
        "note": "Crossbow is NOT a medieval invention; it existed in ancient China and Rome"
    },
    "stirrup": {
        "appears": "Central Asia ~2nd century CE; China ~5th c.; Europe ~8th century CE",
        "before": "Ancient Roman cavalry, pre-8th century Europe",
        "note": "Roman cavalry rode without stirrups; stirrups transformed medieval warfare"
    },

    # Writing and Communication
    "printing press": {
        "appears": "Movable type China ~1040 CE; Gutenberg Europe ~1440 CE",
        "before": "Pre-1440 Europe; pre-1040 China",
        "note": "Before printing: manuscripts copied by hand; extremely expensive books"
    },
    "paper": {
        "appears": "China ~105 CE; Islamic world ~8th c.; Europe ~12th-13th c.",
        "before": "Ancient world outside China; early medieval Europe",
        "note": "Romans used papyrus and wax tablets; European paper mills from ~1150 CE"
    },
    "newspaper": {
        "appears": "Europe, ~1620s CE",
        "before": "Pre-17th century settings",
        "note": "Before newspapers: town criers, handwritten newsletters (avvisi), proclamations"
    },

    # Navigation
    "compass": {
        "appears": "China, ~11th century CE; Europe, ~12th century CE",
        "before": "Ancient world, early medieval",
        "note": "Before compass: celestial navigation (stars, sun), coastal piloting"
    },
    "accurate maps": {
        "appears": "Portolan charts (coastal) ~1300 CE; accurate inland maps much later",
        "before": "Pre-1300 CE for any setting",
        "note": "Medieval maps (mappae mundi) were schematic/religious, not navigational"
    },
    "chronometer": {
        "appears": "Harrison's H4, 1759 CE",
        "before": "Pre-1760 oceanic navigation",
        "note": "Without chronometer, longitude at sea was essentially unsolvable; ships navigated by dead reckoning"
    },

    # Medicine
    "germ theory": {
        "appears": "Pasteur and Koch, ~1860s-1880s CE",
        "before": "Pre-19th century settings",
        "note": "Before germ theory: miasma theory (bad air), humoral theory (imbalance of humors)"
    },
    "anesthesia": {
        "appears": "Ether, ~1846 CE; chloroform, ~1847 CE",
        "before": "Pre-1846 settings",
        "note": "Before anesthesia: alcohol, opium, speed; amputation without anesthesia was normal"
    },
    "antiseptic": {
        "appears": "Lister's carbolic acid, ~1867 CE",
        "before": "Pre-1867 settings",
        "note": "Before antiseptics: surgical infection (sepsis) killed more than surgery itself"
    },

    # Infrastructure
    "chimney": {
        "appears": "Europe, ~12th-13th century CE (widespread)",
        "before": "Pre-12th century Europe",
        "note": "Before chimneys: central hearths with smoke holes in roof; smoky interiors were normal"
    },
    "eyeglasses": {
        "appears": "Italy, ~1286-1300 CE",
        "before": "Ancient world through early medieval",
        "note": "Before eyeglasses: the farsighted simply went without; magnifying glasses existed but not wearable spectacles"
    },
    "mechanical clock": {
        "appears": "Europe, ~1280s CE",
        "before": "Pre-1280 settings",
        "note": "Before mechanical clocks: sundials, water clocks (clepsydra), hour candles; time was approximate"
    },
    "sugar": {
        "appears": "India ancient; Islamic world widespread ~8th c.; Europe ~11th c. (rare), common ~17th c.",
        "before": "Pre-11th century Europe (as common sweetener)",
        "note": "Medieval Europe used honey; sugar was a luxury spice in small quantities"
    },
    "potatoes": {
        "appears": "South America (ancient); Europe ~1570s CE (post-Columbian)",
        "before": "Pre-Columbian Europe (before ~1570)",
        "note": "Classic anachronism: Irish potato famines impossible before 16th century introduction"
    },
    "tomatoes": {
        "appears": "South America (ancient); Europe ~1520s CE (post-Columbian)",
        "before": "Pre-Columbian Europe and Mediterranean",
        "note": "Italian cuisine without tomatoes is historically accurate before ~1600 CE"
    },
    "coffee": {
        "appears": "Ethiopia (ancient); Arabia ~15th c.; Europe ~17th c.",
        "before": "Pre-15th century non-African settings; Europe before ~1600",
        "note": "First European coffee house in Oxford, 1650 CE"
    },
    "toilet": {
        "appears": "Flush toilets: ancient Indus Valley and Crete; modern flush toilet ~1596 (Harington)",
        "before": "Most historical settings",
        "note": "Privies, chamber pots, and street gutters were the norm in most periods"
    },
}

SOCIAL_ANACHRONISMS = {
    "universal literacy": "Literacy rates in pre-modern societies typically 5-30%; universal literacy is modern (19th-20th c.)",
    "nuclear family": "Nuclear family as dominant unit is largely modern/industrial; extended family/household groups were norm",
    "romantic love marriage": "Marriage for romantic love as primary motivation is largely post-Enlightenment; arranged marriages for alliance were standard",
    "childhood as protected": "Modern concept of protected childhood (play, school, no work) is post-industrial; children worked from young ages",
    "individual rights": "Individual rights as framework is largely Enlightenment/modern; most societies organized around group/status/duty",
    "privacy": "Personal privacy as valued norm is largely modern; shared sleeping, multi-use rooms, extended households were normal",
}


def find_anachronisms(text, period_hint=""):
    text_lower = text.lower()
    found = []

    for term, data in TECHNOLOGY_DATABASE.items():
        if term in text_lower:
            found.append({
                "term": term,
                "appears": data["appears"],
                "anachronistic_before": data["before"],
                "note": data["note"],
                "confidence": "HIGH" if term in ["potatoes", "tomatoes", "printing press", "germ theory"] else "MEDIUM",
            })

    for term, note in SOCIAL_ANACHRONISMS.items():
        if term in text_lower:
            found.append({
                "term": term,
                "type": "social",
                "note": note,
                "confidence": "MEDIUM",
            })

    return found


def print_report(anachronisms, period, text_preview):
    print(f"\n{'='*65}")
    print(f"  Anachronism Check")
    if period:
        print(f"  Period: {period}")
    print(f"{'='*65}")

    if not anachronisms:
        print("\n  ✓ No anachronisms detected from the checked term database.")
        print("  Note: Manual review recommended — this checker covers common traps,")
        print("  not comprehensive historical knowledge.")
        return

    print(f"\n  Found {len(anachronisms)} potential anachronism(s):\n")
    for i, item in enumerate(anachronisms, 1):
        conf = item.get("confidence", "MEDIUM")
        print(f"  {i}. [{conf}] \"{item['term']}\"")
        if item.get("type") == "social":
            print(f"     Issue: {item['note']}")
        else:
            print(f"     First appears: {item['appears']}")
            print(f"     Anachronistic before: {item['anachronistic_before']}")
            print(f"     Note: {item['note']}")
        print()

    print(f"  ─── REMINDER ───────────────────────────────────────────────")
    print(f"  This checker covers common traps. Always verify with primary")
    print(f"  sources and period-specific scholarship for your setting.")


def main():
    parser = argparse.ArgumentParser(description="Historical Anachronism Checker")
    parser.add_argument("description", help="Text file to check for anachronisms")
    parser.add_argument("--period", default="", help='Historical period (e.g., "14th century Europe")')
    parser.add_argument("--format", choices=["report", "json"], default="report")
    args = parser.parse_args()

    try:
        with open(args.description) as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.description}' not found.", file=sys.stderr)
        sys.exit(1)

    anachronisms = find_anachronisms(text, args.period)

    if args.format == "json":
        print(json.dumps({
            "period": args.period,
            "anachronisms_found": len(anachronisms),
            "items": anachronisms,
        }, indent=2))
    else:
        print_report(anachronisms, args.period, text[:200])


if __name__ == "__main__":
    main()
