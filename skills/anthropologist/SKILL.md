# Anthropologist Skill

## Overview

Provides cultural anthropology frameworks for designing and evaluating culturally coherent societies, belief systems, kinship structures, and ritual practices. Grounded in structural anthropology (Lévi-Strauss), symbolic anthropology (Geertz), practice theory (Bourdieu), kinship theory, and ritual analysis (Turner, van Gennep). Built for worldbuilding, narrative design, game development, and cultural analysis.

## Capabilities

### Cultural System Design

**Core Design Workflow**
```
1. Start with subsistence: How do these people eat? (Harris, cultural materialism)
   - Mode of production: Foraging / Pastoral / Agricultural / Industrial / Mixed
   - This shapes settlement, social structure, and belief systems

2. Build social organization: Kinship, residence, descent — the skeleton of society

3. Layer meaning-making: Beliefs, rituals, cosmology — the flesh on the bones

4. Check for coherence: Do the pieces fit together?

5. Stress-test: What happens when this culture faces crisis?
```

**Subsistence → Social Structure Links**
```
Foraging:    → Band organization, bilateral kinship, egalitarian, high mobility
Pastoral:    → Tribal/chiefdom, usually patrilineal, transhumant residence
Agricultural:→ Village/chiefdom/state, varied kinship, more permanent hierarchy
Maritime:    → Trade emphasis, cross-cutting ties, flexible alliances
```

### Cultural System Analysis Template

```markdown
CULTURAL SYSTEM: [Society Name]
================================
Analytical Framework: [Structural / Functionalist / Symbolic / Practice Theory]

Subsistence & Economy:
- Mode of production: [Foraging / Pastoral / Agricultural / Industrial / Mixed]
- Exchange system: [Reciprocity / Redistribution / Market — per Polanyi]
  - Generalized reciprocity: gift-giving without immediate return (kin)
  - Balanced reciprocity: equivalent exchange (trade partners)
  - Negative reciprocity: getting more than you give (strangers, enemies)
- Key resources and who controls them

Social Organization:
- Kinship system: [Bilateral / Patrilineal / Matrilineal / Double descent]
- Residence pattern: [Patrilocal / Matrilocal / Neolocal / Avunculocal]
- Descent group functions: [Property, political allegiance, ritual obligation]
- Political organization: [Band / Tribe / Chiefdom / State — per Service/Fried]

Belief System:
- Cosmology: [How they explain the world's origin and structure]
- Ritual calendar: [Key ceremonies and their social functions]
- Sacred/Profane boundary: [What is taboo and why — per Douglas]
- Specialists: [Shaman / Priest / Prophet — per Weber's typology]
  - Shaman: ecstatic, personal power, access via trance
  - Priest: bureaucratic, institutional, access via training/office
  - Prophet: charismatic, reform-oriented, access via revelation

Identity & Boundaries:
- How they define "us" vs. "them"
- Rites of passage: van Gennep's model
  - Separation: removal from current status
  - Liminality: "betwixt and between" (Turner's communitas emerges here)
  - Incorporation: reintegration with new status
- Status markers: [How social position is displayed]

Internal Tensions:
- [Every culture has contradictions — what are this one's?]
- [No utopias: what are the unresolved conflicts?]
```

### Cultural Coherence Check Template

```markdown
COHERENCE CHECK: [Element being evaluated]
==========================================
Element: [Specific cultural practice or feature]
Function: [What social need does it serve?]
  - Social cohesion? Resource management? Identity formation? Conflict resolution?
Consistency: [Does it fit with the rest of the cultural system?]
Red Flags: [Contradictions with other established elements]
Real-world parallels: [Cultures that have similar practices and why]
Recommendation: Keep / Modify / Rethink — with reasoning
```

### Kinship System Reference

**Descent Systems and Their Consequences**
```
Bilateral (most Western societies):
- Children related equally to both parents' kin
- No corporate descent groups
- Individual networks, ego-centered kinship
- Consequence: flexible, less property-binding, weaker lineage politics

Patrilineal (most common worldwide):
- Descent traced through father
- Property, name, rights pass through male line
- Father's brother's children = siblings (parallel cousins)
- Mother's brother's children = marriageable (cross cousins, in many systems)
- Consequence: patrilocal residence common, women as alliance-makers between groups

Matrilineal (~15% of societies):
- Descent traced through mother
- Property passes through female line, but men often hold political power
- A man's heirs are his sister's children, not his own
- Classic tension: loyalty to natal lineage vs. wife's household
- Examples: Minangkabau (Indonesia), Khasi (India), many Bantu groups

Double Descent (rare):
- Individuals belong to both patrilineal and matrilineal groups
- Different properties/rights governed by different descent lines
- Example: Yako of Nigeria
```

**Residence Patterns**
```
Patrilocal:  Bride moves to groom's family → daughters leave, sons stay
Matrilocal:  Groom moves to bride's family → sons leave, daughters stay
Neolocal:    Couple forms independent household (common in industrial societies)
Avunculocal: Couple moves to groom's mother's brother (common in matrilineal societies)
Bilocal:     Choice depending on resources
```

### Exchange System Design (Polanyi's Framework)

**Reciprocity Types**
```
Generalized: Give freely, no immediate return expected
  - Creates and maintains close social bonds
  - Failure to reciprocate over time damages relationship
  - Example: parents feeding children, sharing food in band society

Balanced: Equivalent return expected within defined timeframe
  - Maintains relationships between equals
  - Example: potlatch (formalized), trade partnerships, bride-wealth

Negative: Maximize gain at other's expense
  - Appropriate with strangers/enemies
  - When applied to kin = social disruption
  - Example: market bargaining, raiding
```

**Redistribution**
```
Goods flow to central authority then redistributed
Requires: political hierarchy (chief, chief, state)
Functions: risk pooling, public goods, elite legitimation
Example: Hawaiian chiefdoms, Inca mit'a labor system, taxation
```

### Ritual Design Framework (van Gennep + Turner)

**Rites of Passage Structure**
```
Phase 1 — Separation (Preliminal):
- Individual removed from existing status
- Symbolic death of old self
- Physical removal (seclusion, journey)
- Removal of status markers (shaving head, removing clothing/jewelry)

Phase 2 — Liminality (Liminal):
- "Neither here nor there" — between statuses
- Rules suspended or inverted
- Turner's communitas: equality and solidarity among initiates
- Danger period: the person is powerful and dangerous in their ambiguity
- Instruction, ordeal, transformation

Phase 3 — Incorporation (Postliminal):
- Reintegration with new status
- New name, new clothing, new rights and obligations
- Public recognition by community
- New social relationships activated
```

## Scripts

### `scripts/cultural_coherence_checker.py`

Validates cultural system consistency across subsistence mode, social organization, and belief system elements.

```
Usage: python cultural_coherence_checker.py culture.json [--format json|report]
Input JSON fields: subsistence_mode, exchange_system, kinship_type, residence_pattern,
                   political_organization, ritual_specialists, cosmology_elements[]
Output:
  - Coherence score per dimension
  - Flagged contradictions with explanation
  - Missing elements for completeness
  - Real-world parallel cultures
```

### `scripts/kinship_mapper.py`

Generates kinship terminology and relationship rules for a given descent system.

```
Usage: python kinship_mapper.py --descent [bilateral|patrilineal|matrilineal|double]
                                 --residence [patrilocal|matrilocal|neolocal|avunculocal]
Output:
  - Kinship terminology chart (ego-centered)
  - Cousin marriage rules (parallel vs. cross)
  - Inheritance and succession rules
  - Residence and alliance implications
```

### `scripts/ritual_designer.py`

Designs rites of passage following van Gennep's tripartite model with culturally consistent elements.

```
Usage: python ritual_designer.py --transition [birth|puberty|marriage|death|office]
                                   --social-org [band|tribe|chiefdom|state]
                                   --subsistence [foraging|pastoral|agricultural]
Output:
  - Separation phase design (symbols, duration, practices)
  - Liminal phase design (ordeals, instruction, communitas elements)
  - Incorporation phase design (markers, obligations, community recognition)
  - Real-world ethnographic parallels
```

## References

### `references/theoretical_frameworks.md`
Quick reference to key anthropological theories: structural (Lévi-Strauss binary oppositions), symbolic (Geertz thick description), practice (Bourdieu habitus/field/capital), functionalist (Malinowski, Radcliffe-Brown), materialist (Harris), exchange (Mauss, Polanyi).

### `references/ethnographic_parallels.md`
Curated database of real-world cultural practices organized by function: kinship systems, exchange mechanisms, ritual structures, cosmological frameworks, political organizations. For grounding fictional cultures in anthropological reality.

### `references/common_cliches.md`
Catalog of cultural design clichés to avoid: noble savage trope, culture salad, exotic othering, primitive/advanced hierarchy, Western default assumptions. With better alternatives for each.

### `references/anti_ethnocentrism_guide.md`
Framework for analyzing cultures on their own terms: emic vs. etic distinction, cultural relativism (and its limits), anthropology's colonial history, ethical considerations in cultural representation.

## Assets

### `assets/cultural_system_template.md`
Blank cultural system design template with all required fields, prompting questions, and coherence checkpoints.

### `assets/kinship_diagram_template.md`
Standard kinship diagram notation guide with ego-centered charts for bilateral, patrilineal, matrilineal, and double descent systems.

## Quality Standards

- Every cultural element has an identified social function (no decoration)
- Kinship and social organization are internally consistent
- Real-world ethnographic parallels cited to support or challenge designs
- Cultural borrowing done with understanding of original context
- Internal tensions and contradictions identified (no utopias)
- Emic perspective established before applying etic analytical categories
