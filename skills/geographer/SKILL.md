# Geographer Skill

## Overview

Provides physical and human geography frameworks for building geographically coherent worlds where terrain, climate, resources, and settlement patterns make scientific sense. Covers plate tectonics, Koppen climate classification, hydrology, biome distribution, and human geography (Christaller's central place theory, geopolitical analysis). Built for worldbuilding, game design, narrative settings, and geographic analysis.

## Capabilities

### Geographic Design Workflow

```
1. Plate tectonics first: Where are the mountains?
   - Subduction zones → volcanic mountain ranges (Andes, Cascades)
   - Collision zones → tall fold mountains (Himalayas, Alps)
   - This determines everything downstream

2. Climate from first principles: Latitude + ocean currents + terrain
   - Prevailing winds follow Hadley, Ferrel, Polar cells
   - Rain shadows on lee side of mountains
   - Coastal currents warm or cool adjacent land

3. Hydrology: Rivers flow downhill, always merge, rarely split
   - Watersheds divide at ridgelines
   - Rivers carved by erosion follow valleys

4. Biomes: Climate + soil + water determines what grows
   - Koppen classification maps predictably onto climate data

5. Human settlement: Water access + defensibility + trade routes
   - Settlements at river confluences, natural harbors, valley mouths
```

### Geographic Coherence Report Template

```markdown
GEOGRAPHIC COHERENCE REPORT
============================
Region: [Area being analyzed]

Physical Geography:
- Terrain: [Landforms and their tectonic/erosional origin]
- Climate Zone: [Koppen classification, latitude, elevation effects]
  - A: Tropical (humid throughout)
  - B: Arid/Semi-arid (evaporation > precipitation)
  - C: Temperate (mild winters, warm/hot summers)
  - D: Continental (cold winters, warm summers, large range)
  - E: Polar (no warm season)
- Hydrology: [River systems, watersheds, water sources — no impossible splits]
- Biome: [Vegetation type consistent with climate and soil]
- Natural Hazards: [Earthquakes, volcanoes, floods, droughts — 

Resource Distribution:
- Agricultural potential: [Soil quality, growing season, rainfall — Fertile Crescent logic]
- Minerals/Metals: [Geologically plausible deposits — igneous intrusions for metals]
- Timber/Fuel: [Forest coverage consistent with biome]
- Water access: [Rivers, aquifers, rainfall patterns]

Human Geography:
- Settlement logic: [Why people would live here — water, defense, trade]
- Trade routes: [Following geographic paths of least resistance]
  - River valleys, mountain passes, coastal roads
  - Avoid swamps, deserts, high mountain crossings unless no alternative
- Strategic value: [Chokepoints, defensible positions, resource control]
- Carrying capacity: [How many people this geography can support]

Coherence Issues:
- [Specific problem]: [Why it's geographically impossible/implausible and what would work]
```

### Climate System Design Template

```markdown
CLIMATE SYSTEM: [World/Region Name]
====================================
Global Factors:
- Axial tilt: [Affects seasonality — Earth's 23.5° creates our seasons]
- Ocean currents: [Warm/cold, coastal effects]
  - Warm currents (Gulf Stream type): warm NW Europe, enable higher-latitude agriculture
  - Cold currents (Humboldt type): cool coastal deserts, rich fisheries
- Prevailing winds: [Direction follows Hadley/Ferrel/Polar cells]
  - 0-30°N/S: Trade winds blow toward equator (easterlies)
  - 30-60°N/S: Westerlies blow toward poles
  - 60-90°N/S: Polar easterlies
- Continental position: [Maritime vs. continental climate]

Regional Effects:
- Rain shadows: Mountain ranges force air up (cools, rains) on windward side;
  descending dry air on leeward side = arid (Atacama, Gobi, Great Basin)
- Coastal moderation: Ocean buffers temperature extremes within ~100km of coast
- Altitude effects: ~6.5°C decrease per 1,000m elevation
- Seasonal patterns: [Monsoons, dry seasons — driven by land/sea pressure differential]

Biome Mapping:
- Tropical rainforest: Hot + wet year-round (equatorial, no dry season)
- Savanna: Hot + seasonal dry season (tropical with pronounced dry months)
- Desert: Hot or cold + very low precipitation (<250mm/yr)
- Mediterranean: Mild/wet winters, hot/dry summers (30-40° latitude, west coast)
- Temperate forest: Moderate temp, year-round rainfall (mid-latitudes)
- Taiga/Boreal: Cold winters, short summers, coniferous (50-70° latitude)
- Tundra: Permafrost, very short growing season (above 70° or high altitude)
```

### River System Rules

```
HYDROLOGY PRINCIPLES
====================
Rivers always:
- Flow downhill (gravity)
- Merge tributaries into main channel (confluence)
- Enter the sea, a lake, or an inland basin (endorheic drainage)
- Erode headward over time, capturing other drainages
- Follow valleys carved by their own erosion

Rivers never:
- Flow uphill (without human engineering)
- Split into two separate rivers flowing to different oceans (impossible)
  Exception: river capture/piracy creates historic divisions, not active splits
  Exception: deltas split near sea level (many channels, same ocean)
- Cross a ridge line naturally

River → Settlement Pattern:
- Confluence cities: Two rivers meet → strategic and trade (Pittsburgh model)
- Floodplain agriculture: Broad valleys, annual flooding deposits fertile silt (Egypt)
- Gorge barriers: Rivers in canyons = natural borders, hard to cross
- Inland harbors: Where river becomes navigable = trade break point
```

### Human Geography Frameworks

**Settlement Hierarchy (Christaller's Central Place Theory)**
```
Hamlet/Village: Local daily needs (market days)
Town:           Regional weekly needs (market town)
City:           Sub-regional monthly needs (specialized services)
Regional center: Regional annual needs (major specialized functions)
Primate city:   Disproportionately large, often capital (breaks ideal model)

Spacing: Each level serves a hexagonal hinterland; centers equidistant
Real-world distortions: Rivers, terrain, historical accidents
```

**Trade Route Logic**
```
Preferred routes (in order):
1. Navigable water (cheapest ton-mile historically)
2. River valleys (follow water, avoid elevation change)
3. Coastal roads (water on one side, navigable supply)
4. Passes through mountain ranges (lowest elevation crossing)
5. Desert routes (only where oases permit — caravan water logistics)

Chokepoints create power:
- Mountain passes: control access (Thermopylae, Khyber)
- River crossings: ford/bridge locations become towns
- Strait/harbor: control sea lanes (Constantinople, Gibraltar)
- Isthmus: only land crossing between regions
```

**Geographic Scale Constraints**
```
Empire communication limits (pre-modern):
- Horse relay: ~300km/day for urgent messages
- Army movement: ~25-30km/day on good roads, less in rough terrain
- Supply lines: typically <15 days march from supply base (else army starves)
- Administrative coherence: degrades rapidly beyond 1,000-1,500km from capital

Implications:
- Vast empires require rivers, roads, or exceptional administrative innovation
- Mountain empires are smaller than lowland empires (terrain multiplies distance)
- Island empires require naval supremacy (different constraint set)
```

## Scripts

### `scripts/climate_zone_mapper.py`

Generates Koppen climate zones and biomes for a region given latitude, terrain, ocean proximity, and prevailing winds.

```
Usage: python climate_zone_mapper.py --latitude 45 --terrain coastal_plain --ocean west --hemisphere north
Options:
  --latitude      Degrees from equator (0-90)
  --terrain       [coastal_plain | inland | mountain_windward | mountain_leeward | plateau]
  --ocean         [west | east | both | landlocked]
  --hemisphere    [north | south]
  --altitude      Meters above sea level (default: 0)
Output:
  - Koppen classification with code (Csa, Dfb, BWh, etc.)
  - Biome type
  - Annual temperature range estimate
  - Precipitation pattern (wet/dry seasons)
  - Agricultural potential assessment
```

### `scripts/settlement_analyzer.py`

Analyzes geographic features to determine optimal settlement locations and trade route networks.

```
Usage: python settlement_analyzer.py terrain.json [--population-target 50000]
Input JSON: rivers[], mountains[], coastline[], resources{}, elevation_grid
Output:
  - Ranked settlement location candidates with rationale
  - Trade route recommendations between settlements
  - Chokepoint identification
  - Carrying capacity estimate per region
  - Strategic vulnerability assessment
```

### `scripts/geographic_coherence_checker.py`

Validates geographic claims for physical impossibility and internal consistency.

```
Usage: python geographic_coherence_checker.py world_description.txt [--strict]
Input: Free-text world description with geographic features
Output:
  - Flagged impossible features (rivers flowing uphill, desert next to rainforest without explanation)
  - Flagged improbable features with confidence level
  - Missing implied features (mountain range → should have rain shadow)
  - Real-world analog suggestions
```

## References

### `references/koppen_climate_guide.md`
Complete Koppen climate classification with codes, criteria, characteristic biomes, agricultural potential, and real-world examples for each zone. Includes modified Koppen for fantasy/science fiction applications.

### `references/geological_resources_guide.md`
Guide to geologically plausible resource placement: where to find iron (sedimentary, banded iron formations), copper (hydrothermal, porphyry deposits), gold (placer, quartz veins), salt (evaporite basins), coal (ancient swamp sediments), oil (sedimentary basins, anticlines).

### `references/trade_route_history.md`
Historical analysis of why major trade routes formed where they did: Silk Road, Indian Ocean trade, Mediterranean networks, Atlantic triangular trade. Pattern extraction for fictional world application.

### `references/geographic_determinism_debate.md`
Balanced analysis of Jared Diamond's geographic determinism thesis (Guns, Germs, Steel), Acemoglu & Robinson's institutional critique (Why Nations Fail), and the scholarly debate on how much geography determines civilizational outcomes.

## Assets

### `assets/world_building_geography_checklist.md`
Step-by-step checklist for building a geographically coherent world from first principles: tectonics → climate → hydrology → biomes → resources → settlement.

### `assets/map_critique_template.md`
Template for critiquing existing maps for geographic coherence: river direction check, climate zone consistency, settlement location logic, resource plausibility.

## Quality Standards

- Climate systems follow real atmospheric circulation logic
- River systems obey hydrology (downhill, merging, no impossible splits)
- Settlement patterns have geographic justification (water, defense, trade)
- Resource distribution follows geological plausibility
- Geographic features have explained consequences for human civilization
- Scale constraints acknowledged for governance, communication, and supply
