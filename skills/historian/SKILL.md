# Historian Skill

## Overview

Provides historical analysis frameworks for validating period authenticity, identifying anachronisms, enriching settings with material culture, and applying historiographical methodologies. Covers antiquity through the modern era with emphasis on material conditions, non-Western histories, and the Annales school approach to daily life. Built for historical fiction, worldbuilding, game design, and academic analysis.

## Capabilities

### Historical Analysis Workflow

```
1. Establish precise coordinates: When and where?
   - "Medieval" spans 1000 years and a continent — be specific
   - "Ancient" is useless — specify: Classical Athens? Shang Dynasty? Axum?
   
2. Check material base first: Economy, technology, agriculture
   - What did people eat? How did they trade? What technologies existed?
   - These constrain everything else (Annales school foundation)
   
3. Layer social structures: Power, class, gender, religion
   - How do they interact with the material base?
   
4. Evaluate claims against sources:
   - Primary sources > Secondary scholarship > Popular history > Hollywood
   
5. Flag confidence levels: Documented / Debated / Unknown
```

### Period Authenticity Report Template

```markdown
PERIOD AUTHENTICITY REPORT
==========================
Setting: [Time period, region, specific context — e.g., "Constantinople, 9th century CE, Byzantine merchant class"]
Confidence Level: Well-documented / Scholarly consensus / Debated / Speculative

Material Culture:
- Diet: [What people actually ate, class differences]
  - Specifics: grains, legumes, meats (availability by class), preservation methods
  - Seasonality: what's available when, famine periods
- Clothing: [Materials, styles, social markers]
  - Fiber availability (wool, linen, silk — regional and period-specific)
  - Color as status marker (purple = imperial, sumptuary laws)
- Architecture: [Building materials, styles, what survives vs. what's lost]
  - What we know from archaeology vs. what's been reconstructed
- Technology: [What existed, what didn't, what was regional]
  - Critical: stirrup availability, metallurgy level, watermill, printing
  - What's anachronistic: check invention dates carefully
- Currency/Trade: [Economic system, trade routes, commodities]

Social Structure:
- Power: [Who held it, how it was legitimized — divine right, conquest, law, tradition]
- Class/Caste: [Social stratification, mobility — how rigid?]
- Gender roles: [With acknowledgment of regional variation and class differences]
- Religion/Belief: [Practiced religion vs. official doctrine — often very different]
  - Local saints, folk practices, syncretic elements
- Law: [Formal and customary legal systems — written law vs. what actually happened]

Anachronism Flags:
- [Specific anachronism]: [Why it's wrong, what would be accurate, with confidence level]

Common Myths About This Period:
- [Myth]: [Reality, with source]
  Example: "People in the Middle Ages thought Earth was flat" — False. Educated people knew it was spherical (Bede, 8th c.)

Daily Life Texture:
- Sounds: [Bells, animals, trade, craft noise — no cars, electrical hum]
- Smells: [Animals, tanning, cooking, human density without modern sanitation]
- Light: [Candles, torches, oil lamps — darkness after sunset was real]
- Time: [Church bells, sun position — not clock time]
- Rhythms: [Agricultural calendar, market days, feast days]
```

### Historical Coherence Check Template

```markdown
COHERENCE CHECK
===============
Claim: [Statement being evaluated]
Verdict: Accurate / Partially accurate / Anachronistic / Myth
Evidence: [Source and reasoning]
  - Primary 
  - Secondary scholarship: [Historian and work]
  - Confidence: High / Medium / Low — and why
If fictional/inspired: [What historical parallels exist, what diverges]
Correction: [What would be accurate, with period/regional specifics]
```

### Key Historiographical Frameworks

**Annales School (Braudel et al.)**
```
Three temporal scales:
1. Longue durée (long duration): Geographic and structural constraints
   - Mountains, rivers, climate, disease environments
   - Changes over centuries, barely visible in a lifetime
   - Most powerful explanation for large-scale history

2. Conjuncture (medium duration): Economic cycles, social structures
   - Rise and fall of trade networks, demographic shifts
   - Changes over decades

3. Events (short duration): Political events, battles, reigns
   - Traditional "history" — but least explanatory of structural change
   - What people notice, but not what drives history
```

**Microhistory (Ginzburg, Levi)**
```
Focus on individual cases to illuminate larger structures:
- Carlo Ginzburg's "The Cheese and the Worms": single miller's cosmology reveals popular culture
- Use of notarial records, Inquisition transcripts, parish registers
- What ordinary people believed, not just what elites said they should believe
```

**Material Culture Analysis**
```
What physical evidence tells us that documents don't:
- Food remains → diet, trade networks, season of occupation
- Pottery → trade routes, technological level, cultural contact
- Housing → family structure, wealth distribution, privacy norms
- Coinage → economic integration, political authority, trade reach
- Burial goods → beliefs about afterlife, status at death, gender roles
```

### Non-Western History Quick Reference

**Civilizations typically omitted from Western-centric accounts**
```
Mali Empire (13th-16th c.): 
  - Mansa Musa's 1324 pilgrimage: ~27 tons of gold, crashed Cairo gold market
  - University of Timbuktu: ~25,000 students, major manuscript tradition
  - Control of West African gold and salt trade

Song Dynasty China (960-1279 CE):
  - Paper money, gunpowder weapons, printing press centuries before Europe
  - GDP estimated at ~30% of world GDP at peak
  - Urban populations larger than any European contemporary city

Abbasid Caliphate (750-1258 CE):
  - House of Wisdom: translation movement, algebra, optics, medicine
  - Agricultural revolution: cotton, citrus, rice diffusion across MENA
  - Inter-continental trade networks from Spain to China

Aztec/Mexica Empire (c. 1300-1521):
  - Tenochtitlan ~200,000-300,000 people (larger than any European city of the era)
  - Sophisticated hydraulic agriculture (chinampas)
  - Mandatory education system for both sexes

Indus Valley Civilization (3300-1300 BCE):
  - Cities with standardized weights, drainage systems, planned streets
  - Trade with Mesopotamia documented by seals
  - Still not deciphered — limits our understanding
```

### Technology Anachronism Reference

**Common Anachronisms by Period**
```
Pre-1000 CE Europe:
- No: plate armor (appears ~1350+), stirrups widely used (debate, but ~8th c. in Europe),
  chimneys (widespread ~12th c.), mechanical clocks (1280s), paper money
- Yes: chainmail, gambesons, crossbows (ancient, not medieval invention)

Medieval (1000-1450 CE):
- No: firearms broadly effective (early guns pre-1400, but slow/unreliable),
  accurate maps (portolan charts for coasts, distorted inland), eyeglasses before ~1290s
- Yes: windmills (12th c. Europe), universities (Bologna 1088), water mills

Early Modern (1450-1700 CE):
- No: accurate oceanic navigation without chronometer (longitude problem unsolved until 1765),
  germ theory, effective antiseptics, steam power
- Yes: printing press (1450), effective artillery, global trade networks

Ancient World:
- No: stirrups (Roman cavalry rode without), sugar widely available,
  mechanical clocks, paper (Romans used wax tablets, papyrus)
- Yes: concrete (Rome), aqueducts, steel (Wootz/Damascus steel, ancient India)
```

## Scripts

### `scripts/anachronism_checker.py`

Scans text descriptions for period-inconsistent technologies, social structures, and cultural elements.

```
Usage: python anachronism_checker.py description.txt --period "14th century Europe"
       python anachronism_checker.py description.txt --period "Tang Dynasty China"
Input: Free-text description of setting, characters, or events
Period options: Any historical period specified as free text; common periods pre-loaded
Output:
  - Flagged anachronisms with confidence level (certain / probable / possible)
  - Explanation of why each element is anachronistic
  - Period-accurate alternatives
  - Confidence level for the overall period accuracy
```

### `scripts/material_culture_generator.py`

Generates period-accurate material culture details (diet, clothing, architecture, technology) for a specified time, place, and social class.

```
Usage: python material_culture_generator.py --period "11th century" --region "Northern France"
                                             --class [peasant|merchant|noble|clergy]
Output:
  - Daily diet with seasonal variation
  - Clothing description with available materials
  - Dwelling description with construction methods
  - Available technologies and tools
  - Economic activities and currency
  - Sensory texture (sounds, smells, light, rhythm)
```

### `scripts/historical_parallel_finder.py`

Finds real historical parallels for fictional scenarios, institutions, or social structures.

```
Usage: python historical_parallel_finder.py --scenario "theocratic city-state controlling trade routes"
       python historical_parallel_finder.py --scenario "nomadic empire administering settled farmers"
Output:
  - 3-5 closest historical parallels with time period and location
  - Key similarities and differences
  - What worked and what failed in each parallel
  - Historiographical sources for further research
```

## References

### `references/historiography_guide.md`
Overview of major historiographical schools: Annales, Marxist history, social history, cultural history, postcolonial history, microhistory, counterfactual history. How each school changes what questions we ask.

### `references/primary_source_guide.md`
Guide to primary source types by period: chronicles, annals, legal codes, administrative records, letters, hagiography, archaeology, numismatics. How to read them critically (who wrote this? why? what's missing?).

### `references/common_historical_myths.md`
Documented list of popular historical myths with evidence-based corrections: medieval hygiene, Dark Ages as dark, horned Viking helmets, flat earth, Roman orgies as norm, samurai as noble class, etc.

### `references/non_western_history_overview.md`
Chronological overview of major non-Western civilizations with key developments, cultural achievements, and historiographical challenges. For counteracting Eurocentric default assumptions.

## Assets

### `assets/period_research_template.md`
Research template for building a historical setting: prompting questions for material culture, social structure, belief system, and daily life. Includes source hierarchy checklist.

### `assets/timeline_consistency_tracker.md`
Template for tracking historical claims across a project with confidence levels, sources, and internal consistency notes.

## Quality Standards

- Every historical claim includes a confidence level and source type
- Anachronisms caught with specific explanation of why and what's accurate
- Material culture details grounded in archaeological and historical evidence
- Non-Western histories included proactively, not as afterthoughts
- Line between documented history and plausible extrapolation always clear
- Myths corrected with evidence, not just assertion
