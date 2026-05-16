# Narratologist Skill

## Overview

Provides narrative theory frameworks for analyzing and constructing story structures, character arcs, thematic systems, and genre conventions. Grounded in Russian Formalism, French Structuralism, cognitive narratology, and screenplay theory (McKee, Snyder, Field). Covers oral tradition, game narrative, and interactive storytelling. Built for fiction writing, screenplay development, game design, and narrative analysis.

## Capabilities

### Narrative Analysis Workflow

```
1. Identify the level of analysis:
   - Fabula (story): the chronological events as they happened
   - Sjuzhet (narrative): how those events are told, ordered, emphasized
   - Most "pacing problems" are sjuzhet problems, not fabula problems

2. Find the controlling idea (McKee) / premise (Egri):
   - What does this story argue about human experience?
   - Every scene, character, and plot turn should serve this argument

3. Select appropriate frameworks for the specific problem:
   - Structure problem → three-act, Kishōtenketsu, Hero's Journey
   - Character problem → Want/Need/Lie arc, attachment, wound
   - Genre problem → convention mapping before subversion
   
4. Diagnose before prescribing:
   - Name the structural problem precisely before offering solutions

5. Propose alternatives with trade-offs:
   - Multiple directions, grounded in precedent from existing works
```

### Story Structure Analysis Template

```markdown
STRUCTURAL ANALYSIS
==================
Controlling Idea: [What the story argues about human experience]
  Format: "[Value] is achieved/destroyed through [cause]"
  Example: "Love survives through sacrifice" or "Power corrupts through isolation"
Structure Model: Three-act / Five-act / Kishōtenketsu / Hero's Journey / Other

Act Breakdown (Three-Act):
- Act 1 (Setup, ~25%):
  - Ordinary World: Status quo established
  - Inciting Incident: Disrupts equilibrium (Todorov's model)
  - Dramatic Question: What does the protagonist want? (this MUST be answerable yes/no)
  - Turning Point 1: Protagonist commits to the journey
  
- Act 2 (Confrontation, ~50%):
  - Midpoint: False victory or false defeat — shifts the dynamic
  - Escalating complications and reversals (each worse than the last)
  - Dark Night of the Soul: lowest point, all seems lost
  - Turning Point 2: Discovery that enables the climax
  
- Act 3 (Resolution, ~25%):
  - Climax: Final confrontation with the dramatic question
  - Resolution: New equilibrium established
  - Controlling idea lands through action, not dialogue

Tension Curve: [Map key peaks and valleys — where does it sag?]
Information Asymmetry: [What reader knows vs. characters know]
  - Dramatic irony: reader knows more → tension
  - Mystery: reader knows less → curiosity
  - Suspense: reader knows same → identification
  
Narrative Debts (Chekhov's Gun):
  - [Setup]: [Expected payoff] — [Status: Paid / Outstanding / Broken]
  
Structural Issues: [Identified problems with framework reasoning]
```

### Character Arc Assessment Template

```markdown
CHARACTER ARC: [Name]
====================
Arc Type: Transformative / Steadfast / Flat / Tragic / Comedic
Framework: [Vogler's character arc / Truby's moral argument / Hauge's wound model]

Want vs. Need (fundamental distinction):
  Want: External, conscious goal (what they're chasing)
  Need: Internal, unconscious necessity (what they actually require to be whole)
  Conflict: The want and need should be in tension — pursuing the want delays the need

Ghost/Wound: [Backstory trauma driving current behavior]
  - Must be specific, not vague ("absent father" is a cliché; what specifically happened?)
  - Should explain current maladaptive behavior without excusing it

Lie Believed: [False belief the character operates under]
  - The internal logic that makes their self-defeating behavior make sense to them
  - Example: "I am unworthy of love" → pushes people away → confirms belief

Arc Checkpoints:
1. Ordinary World: [Starting state — how does the Lie manifest?]
2. Catalyst: [What disrupts their equilibrium]
3. False Victory: [Seems to be working — Lie temporarily rewarded]
4. Dark Night: [Lowest point — Lie costs them everything]
5. Confrontation with Lie: [Forced to choose between Lie and Truth]
6. Transformation: [How/whether the Lie is confronted — or tragically isn't]

Flat Arc (Steadfast protagonist):
  - Protagonist is right from the start; world changes, not the character
  - Character must have an active, positive belief that defeats the world's Lie
  - Example: Atticus Finch, Sherlock Holmes
```

### Genre Convention Framework

```markdown
GENRE ANALYSIS: [Genre]
=======================
Core Promise to Reader: [What this genre guarantees the reader will experience]
  - Thriller: mounting tension, protagonist in danger
  - Romance: emotional connection, satisfying relationship resolution
  - Horror: fear/dread, confrontation with the uncanny
  - Mystery: puzzle, fair play clues, satisfying solution
  
Core Conventions (must honor or consciously subvert):
  - [Convention 1]: [Function it serves for the reader]
  - [Convention 2]: [Function it serves for the reader]
  
Subversion Protocol:
  1. Establish the convention clearly (reader must recognize what's being subverted)
  2. Subvert with purpose (the reversal should illuminate the controlling idea)
  3. Don't subvert the emotional promise (can subvert plot, not feeling)
  
Genre Blending Rules:
  - Each genre brings its own conventions — contradictions must be resolved
  - Identify the primary genre (this sets the dominant emotional register)
  - Secondary genre provides complications and enrichment, not contradiction
```

### Key Theoretical Frameworks Reference

**Propp's Morphology (Fairy Tale / Quest)**
```
31 narrative functions, always in sequence if present. Key ones:
- Lack/Villainy: something is wrong, establishing the need for action
- Departure: hero leaves home
- Donor: tests hero, provides magical agent
- Helper: aids hero in quest
- Villain: opposes hero
- Recognition: hero is recognized as worthy
- Resolution: lack is liquidated
```

**Todorov's Equilibrium Model**
```
Equilibrium (status quo) →
Disruption (event breaks equilibrium) →
Recognition (disruption acknowledged) →
Repair attempt (protagonist acts) →
New equilibrium (different from original)
Note: The new equilibrium must be meaningfully different — otherwise no story
```

**Barthes' Five Narrative Codes**
```
Proairetic (action): What will happen next? (suspense engine)
Hermeneutic (mystery): What does this mean? (enigma code, delays resolution)
Semantic: Connotations of specific details (resonance, theme)
Symbolic: Binary oppositions organizing meaning (life/death, inside/outside)
Cultural: References to shared cultural knowledge (assumed context)
```

**Genette's Narratological Terms**
```
Focalization: Whose perception filters the narrative?
  - Zero focalization: omniscient narrator knows all
  - Internal focalization: limited to one character's knowledge
  - External focalization: less than any character knows (behaviorist)
  
Narrative voice: Who speaks?
  - Homodiegetic: narrator is character in story (first person)
  - Heterodiegetic: narrator outside story (third person)
  - Autodiegetic: narrator is main character
  
Temporal order: When does narration occur vs. when events occur?
  - Analepsis: flashback (past events narrated after)
  - Prolepsis: flash-forward (future events narrated before)
  - Anachrony: any deviation from chronological order
```

**Kishōtenketsu (4-Act, Japanese/Chinese)**
```
Ki: Introduction — establish setting, characters, status quo
Shō: Development — deepen the established elements without conflict
Ten: Twist — introduce an unexpected, seemingly unrelated element
Ketsu: Reconciliation — reveal how the twist illuminates the whole

Note: No obligatory conflict; transformation comes from unexpected perspective
Works best for: character-driven stories, literary fiction, certain game narratives
Contrast with Western conflict model: tension from surprise, not opposition
```

## Scripts

### `scripts/story_structure_analyzer.py`

Analyzes a story outline or synopsis for structural completeness against multiple narrative frameworks.

```
Usage: python story_structure_analyzer.py synopsis.txt [--framework three-act|heros-journey|kishōtenketsu]
Input: Text synopsis or beat sheet
Output:
  - Framework mapping (which beats are present/missing)
  - Tension curve assessment (where it sags)
  - Narrative debt tracker (setups without payoffs)
  - Controlling idea extraction attempt
  - Framework-specific recommendations
```

### `scripts/character_arc_checker.py`

Validates character arc completeness and internal consistency across Want/Need/Lie/Transformation checkpoints.

```
Usage: python character_arc_checker.py character.json [--arc-type transformative|steadfast|flat|tragic]
Input JSON: name, want, need, lie_believed, ghost_wound, arc_type, 
            checkpoints{ordinary_world, catalyst, midpoint, dark_night, transformation}
Output:
  - Arc completeness score
  - Want/Need tension assessment (are they actually in conflict?)
  - Lie-to-transformation logic check (does transformation follow from wound?)
  - Missing checkpoints
  - Consistency flags (does behavior in each checkpoint follow from established psychology?)
```

### `scripts/narrative_debt_tracker.py`

Tracks all narrative setups (Chekhov's guns) and whether they have been paid off within a story.

```
Usage: python narrative_debt_tracker.py manuscript.txt [--output debts.json]
Input: Full manuscript or scene-by-scene breakdown
Output:
  - List of all identified setups (explicit and implicit promises)
  - Payoff status per setup: paid / outstanding / broken
  - Broken promises flagged with scene reference
  - Unpaid setups that may feel like loose ends
  - Unnecessary setups that create false expectations
```

## References

### `references/narrative_theory_quick_reference.md`
Quick reference cards for 12 major narrative frameworks: Propp, Todorov, Barthes, Genette, Campbell/Vogler, McKee, Snyder, Hauge, Truby, Kishōtenketsu, Russian Formalism (fabula/sjuzhet), Cognitive Narratology. When to use each and what it illuminates.

### `references/genre_conventions_library.md`
Comprehensive genre convention maps for: thriller, mystery, horror, romance, literary fiction, fantasy, science fiction, western, crime, comedy. Core promises, must-have elements, earned subversions, and classic examples.

### `references/controlling_idea_examples.md`
Library of controlling ideas extracted from canonical works — showing how theme operates as argument in practice. Examples from literature, film, TV, and games.

### `references/character_wound_archetypes.md`
Catalog of psychologically grounded character wounds (not clichés) with behavioral manifestations, Lie beliefs, and transformation paths. Cross-referenced with psychological literature for authenticity.

## Assets

### `assets/story_structure_beat_sheet.md`
Multi-framework beat sheet template covering three-act, Hero's Journey, Save the Cat, and Story Grid structures simultaneously — for writers who want to cross-reference.

### `assets/character_arc_worksheet.md`
Character arc development worksheet with prompting questions for Want, Need, Lie, Ghost, Wound, and each arc checkpoint.

## Quality Standards

- Every structural recommendation cites at least one named framework
- Character arcs have clear Want/Need/Lie/Transformation checkpoints
- Pacing analysis identifies specific tension peaks and valleys, not vague "it feels slow"
- Theme analysis connects to the controlling idea consistently
- Genre expectations acknowledged before any subversion is proposed
- Narrative debt tracking: setups are paid off or consciously unresolved
