# UNSTABLE DEPTHS — Game Design Document

> **Living document · Version 0.5 · Last updated September 2026**
>
> This document describes the intended game direction, not a locked promise.
> Mechanics, balance values, scope, and milestones change through prototyping
> and playtesting. The playable implementation may cover only a subset of it.

**Working title:** Unstable Depths (placeholder)
**Version:** 0.5 (playtest 1 rebalance of Reality Integrity, anchor pity rule, playtest log. v0.4 was v0.3 plus: Blockworld theme cut, combat reading and danger-rating hiding confirmed. v0.3 added decisions: fixed threshold ratio, room-count config, unseal notification, RI-first bend prices, timing-based bend triggers, turn-based combat direction, first themes, Bettor removed, hot-seat first, AI Host hooks)
**Platform:** Terminal (text-based, keyboard only)
**Genre:** Roguelite dungeon crawler / survival / procedural-generation-as-gameplay
**Status:** Pre-production. Everything marked **[TUNABLE]** is a starting value to be changed by playtesting. Everything marked **[OPEN]** is an undecided question, collected in Section 20.

---

## Table of Contents

1. [Vision and Pitch](#1-vision-and-pitch)
2. [Design Pillars](#2-design-pillars)
3. [Glossary](#3-glossary)
4. [Game Structure and Run Flow](#4-game-structure-and-run-flow)
5. [Roles, Modes and Relations](#5-roles-modes-and-relations)
6. [The Generation Game](#6-the-generation-game)
7. [Devices (Random Sources)](#7-devices-random-sources)
8. [Dungeon Model and Map Generation](#8-dungeon-model-and-map-generation)
9. [Exploration Gameplay](#9-exploration-gameplay)
10. [The Notebook](#10-the-notebook)
11. [Reality Integrity](#11-reality-integrity)
12. [Reality Bending](#12-reality-bending)
13. [Extraction, Win and Lose](#13-extraction-win-and-lose)
14. [Scoring, Favor and Economy](#14-scoring-favor-and-economy)
15. [Meta-Progression](#15-meta-progression)
16. [Terminal UI and UX](#16-terminal-ui-and-ux)
17. [Technical Design](#17-technical-design)
18. [Vertical Slice Specification (v0.1)](#18-vertical-slice-specification-v01)
19. [Roadmap, Testing and Risks](#19-roadmap-testing-and-risks)
20. [Open Questions](#20-open-questions)
21. [Appendices](#21-appendices)

---

## 1. Vision and Pitch

### 1.1 One-sentence pitch

A text-based dungeon crawler where **building the dungeon is a gambling game of its own**, and where the dungeon you build (or someone builds for you) is a **blind, shifting place that you must map by hand** while reality slowly falls apart around you.

### 1.2 Elevator description

Before the run, a creator sets up the rules of a dungeon: which random devices (dice, wheels, card decks, tile draws, token bags) decide its layout, room types, loot, quirks and dangers, and how they are weighted. Every tweak to the odds has a price, so the creator shapes *probabilities*, never *outcomes*. The explorer then enters the result, reads room descriptions in plain text, and draws the map in an in-game notebook. As they explore, **Reality Integrity** drains. When it gets low the dungeon stops being trustworthy: rooms shift, vanish and merge, and the notebook becomes wrong. The explorer must explore enough of the dungeon to unlock the entrance as an exit, then get back out alive with their loot before reality falls. A rare found exit can let them leave earlier, at any time.

Rarely, the player finds artifacts or latent powers that let them **bend reality** themselves, at a great cost, with unpredictable, chaotic and often comedic results.

### 1.3 Target experience

- **Pre-run:** strategic, tense, gambling-flavored. "What kind of game do I want to play?"
- **In-run:** careful survival and resource management, with mapping as a real skill.
- **Reality-bend moments:** chaos and comedy. The plan was good; reality does not care.

The contrast between the strategic pre-run and the chaotic in-run bends is deliberate and must feel intentional, not like two separate games.

### 1.4 Target audience

Players who like Minecraft-style survival and resource management, roguelites, tabletop RPG randomizers (d20/2d6 tables, "wheel of fate" character creators), and text games. Comfortable with a terminal.

### 1.5 Inspirations

| Source | What we take |
|---|---|
| "Wheel of fate" character-generation trend | Random spins as entertainment; wheels as a device |
| Vault Hunters (Minecraft modpack) | Themed dungeons with special rooms and modifiers |
| Balatro | Player shapes odds and rules, never fully controls the draw |
| Slay the Spire | Run structure, choice-driven progression |
| Wizardry-style dungeon crawlers | Hand-mapping as part of play |
| Hypixel Skyblock reforges | Item modifiers (lucky/unlucky/chaotic/calm) that alter weights |
| Orv (Omniscient Reader's Viewpoint) | Dokaebi/constellations: gods who watch and sponsor for entertainment |
| Minecraft | Survival, soft goals, sandbox feel |

---

## 2. Design Pillars

1. **Control the odds, never the outcome.** Every random choice must be a real decision with a price. If a player can remove all bad outcomes for free, the system has failed.
2. **Generation is a game.** Building the dungeon must be as engaging as exploring it, with suspense, stakes and decisions at the moment of the roll.
3. **The map is the player's responsibility.** The game describes reliably and truthfully. The *only* thing that lies to the player is Reality Integrity, and it lies visibly and for a reason.
4. **Reality is a resource and a clock.** Integrity is what limits both the run and the power of bending. Nothing is free.
5. **Everything plugs into one engine.** Dice, wheels, decks, tiles, reforges, contracts and relations are all configurations of the same random-source system. Build once, extend with data.
6. **Depth is opt-in.** A new player can use one die and one table. A veteran can run eight concurrent modules with dynamic odds.

---

## 3. Glossary

| Term | Meaning |
|---|---|
| **Run** | One full play of one dungeon, from creation through extraction or failure |
| **Creator** | The role that configures generation (human or the game itself in solo contract play) |
| **Explorer** | The role that enters and plays the dungeon |
| **Device** | A random source: die, wheel, deck, tile draw, token bag, draft, etc. |
| **Table** | A list of outcomes with weights that a device resolves |
| **Module** | One step of the generation pipeline (e.g. Direction, Room Type, Loot, Quirk) |
| **Mask** | A set of outcomes disabled on a table (banned dice faces, removed wheel segments) |
| **Budget** | Generation points the creator spends on modifying odds and enabling modules |
| **Heat** | A dynamic modifier that shifts future odds based on previous results |
| **Reality Integrity (RI)** | The stability meter of the dungeon; the run's slow-burn clock |
| **Bend** | An event that changes reality (rooms, exits, contents) |
| **Reforge** | A modifier applied to a reality-bending item, altering its bend weights |
| **Favor** | Currency earned by a creator during the run, depending on their relation to the explorer |
| **Relation** | The creator's role during the run: Architect, Warden, or Patron |
| **Notebook** | The in-game map and notes the explorer maintains |
| **Stale room** | A notebook room that may have changed since it was last seen; shown greyed out |
| **Threshold (T)** | Number of unique rooms that must be explored before the entrance works as an exit. The player is shown the **ratio**, not T itself |
| **Found exit** | A rare exit room that works as an extraction point immediately, with no threshold |
| **Reachable count (R0)** | Number of rooms reachable from the entrance at the start of the run. Set by the creator as the dungeon's **room count** |
| **Extraction** | Leaving through the entrance after the threshold is met, banking your loot |
| **Contract** | A saved creator config authored by the game, with visible danger and reward ratings |

---

## 4. Game Structure and Run Flow

### 4.1 Run structure

One run = **one dungeon**. Death or reality collapse ends the run. Some progress carries between runs (Section 15). A chain of dungeons and a persistent shared dungeon are future ideas, not part of the base design.

### 4.2 Phases of a run

```
 SETUP  ->  GENERATION  ->  BRIEFING  ->  EXPLORATION  ->  END
 (pick      (creator rolls   (explorer     (blind crawl,     (extraction,
  mode &     the dungeon or   sees what     notebook,         death, or
  config)    sets odds)       they are      Integrity clock)  collapse)
                              allowed)
```

1. **Setup:** choose a mode (Contract, Odds-Only, Two-Player) and, for two-player, the creator's relation.
2. **Generation:** the creator configures modules and rolls devices. In Contract mode the config is preset. In Odds-Only mode the config is set here but the layout and contents are resolved later, when doors are opened.
3. **Briefing:** the explorer sees only what the config allows. **Default: the theme, and the danger rating** (the creator may hide the danger rating). Nothing about the layout, contents or room count unless the creator explicitly chooses to share it.
4. **Exploration:** the core loop (Section 9).
5. **End:** extraction, death, or collapse; score and meta rewards are computed.

### 4.3 Generation timing modes

| Mode | When rooms are resolved | Explorer knowledge |
|---|---|---|
| **Pre-generated** (two-player) | All at generation time, then stored | Creator knows everything; explorer knows the theme and danger rating by default; anything more is up to the creator |
| **Blind / lazy** (solo, odds-only) | When a door is first opened; then stored permanently | Only what the explorer has seen and written down |
| **Contract** | Saved config resolved either way, as the contract specifies | As the contract specifies |

**Rule:** once a room is generated it is stored and never re-rolled. It changes only through Reality Integrity effects or bends, which are visible and have a cause.

---

## 5. Roles, Modes and Relations

### 5.1 Play modes

| Mode | Description | Priority |
|---|---|---|
| **Contract** | Job-board of preset dungeons with visible danger and reward ratings. Fastest to play; also the lowest-effort way to start | v0.3 |
| **Odds-Only Authoring** | Solo player uses the creator screen to set devices, weights and budget, then explores a fully blind dungeon resolved as they go | v0.3 |
| **Two-Player** | Creator builds a full dungeon and hands it to an explorer; relation preset decides the creator's role | v0.6+ |
| **Solo AI Host** | Game plays a creator personality (Warden/Patron) commenting and intervening | Later; not part of the base game |

Solo play uses a **plain crawl with no host** to start.

### 5.2 Creator/explorer relations

All relations run on one engine. The creator screen picks a **preset**. The creator earns **Favor** during the run. The relation defines what earns Favor, what Favor can buy, and the catch that stops it from being abused.

| Relation | Earns Favor when... | Can do during run | The catch |
|---|---|---|---|
| **Architect (neutral)** | Explorer goes deep, loots and extracts, scaled by the dungeon's declared danger rating | Nothing; builds and leaves | Safe and predictable; a royalty model |
| **Warden (opponent)** | Explorer is stressed: HP loss, supplies burned, near-death moments | Spend Favor to spawn hazards or trigger events | Payout peaks at surviving with very low HP, not at death, so brutal-but-unwinnable dungeons pay badly |
| **Patron (collaborator)** | Explorer creates good moments: clutch escapes, discoveries, comedic bends, extraction | Spend Favor on gifts, hints, curses, shops, small nudges | Repeated moments earn less, so the patron needs the explorer to keep being interesting |

### 5.3 The Host-Patron arc (ORV-inspired)

The creator can be the **Host** who builds the scenario and then becomes the **Patron** who watches and sponsors. Like the Dokaebi and constellations, entertainment is the currency: what the creator finds *interesting* is what earns Favor.

**Constraint:** every Patron or Warden intervention is a reality bend and **drains Reality Integrity**. A god who meddles too much breaks the world they are watching.

### 5.4 Fairness guardrails (all relations)

- **Valid path guarantee:** at least one valid path exists from the entrance to reaching the threshold, with enough resource availability to survive it at baseline play.
- **Survivability check:** the creator screen runs a simulation (Section 17.6) and warns or rejects configs where a baseline bot cannot reach the threshold within a set success rate.
- **Interference caps:** Warden and Patron actions per run are capped by Favor and by Integrity cost.
- **No pure-kill dungeons:** the Warden's Favor formula peaks at survival with low HP, not at death.

---

## 6. The Generation Game

This is the game's core innovation and its biggest design risk. Generation must be fun *as a game*, not a form to fill in.

### 6.1 The problem being solved

If the player controls the odds and the odds are free, the player picks safe odds and generation is meaningless. It is only interesting if **every knob is a trade-off**.

### 6.2 The pipeline

Generation is a chain of **modules**. Each module has a **device** attached and one of three modes.

| Module | Decides |
|---|---|
| Layout | Optional pre-layout algorithm for large maps (Section 8.4) |
| Direction/Exits | How the dungeon expands from the current room |
| Room Type | Empty, Supplies, Hazard, Loot, Anchor, Shrine, Boss, etc. |
| Loot | Loot type and value in loot rooms |
| Hazards | Traps, monsters, environmental effects |
| Special Rooms | Themed rooms, vault-style special encounters |
| Quirks | Weird properties of a room or the dungeon |
| Anchors/Exits | Frequency of Integrity repair and rare found exits |
| Reality Events | Availability and rarity of bends, artifacts and the latent power |
| Theme | Bundle of table swaps and modifiers (Section 8.5) |
| Room Count | Planned number of rooms (R0). The threshold follows from a **fixed global ratio** (Section 13.3) |

**Three modes per module:**

- **Off:** module does nothing (e.g. no reality events).
- **Plain random:** default weights, one basic device, no configuration; cheap.
- **Custom:** player picks the device, edits weights and masks, and adds quirks; costs and earns points.

### 6.3 Budget and pricing

The creator has a **Generation Budget**. Modifying odds costs points. Options that make the dungeon *more valuable for the explorer* and *more dangerous* earn back points or raise the reward rating.

Principles:

1. **Price volatility and payoff, not menu depth.** Eight modules that add nothing dangerous earn nothing; a single well-placed high-stakes module can earn a lot.
2. **Weighting toward good things costs points.** Weighting toward Loot, banning Traps, or adding anchor rooms all cost budget.
3. **Weighting toward danger earns points but starts the dungeon with lower Reality Integrity if the source is chaotic or cursed.**
4. **Risk-reward coupling.** Each config gets a computed **Danger Rating** and **Reward Rating**. Reward multiplier on the final score scales with the ratings.
5. **A "simple" one-roll dungeon** is the low-effort, low-reward option.

Illustrative price list **[TUNABLE]**:

| Action | Budget cost (+ earns, - costs) |
|---|---|
| Ban one die face from a device | -2 (or more depending on face impact) |
| Double a wheel segment's weight | -1 to -3 depending on segment value |
| Add a Trap-heavy weighting | +2 |
| Enable Reality Events module | +2, lowers starting Integrity |
| Add a Cursed device quirk | +2 |
| Add Anchor room weight | -3 (repair is valuable to the explorer) |
| Add a bet on a roll (Section 6.5) | Variable: wager amount |
| Raise room count (R0) | Raises Reward Rating; also raises T and total RI burn, so it is capped by the RI guardrail (Section 11.7) |

### 6.4 Rules that keep control from becoming "just random"

- **No free rerolls.** Rerolls cost budget, with rising cost.
- **Commitment:** a result taken is a result kept. Locked decisions are visible.
- **Stakes at the roll:** bets, heat, drafts and doom tracks (below).
- **The creator must live with it.** In solo, the creator is the explorer. In two-player, the creator's reward depends on the relation, so an unfair dungeon does not pay.

### 6.5 Making generation intense (the biggest concern)

Rolls feel flat when they resolve instantly and their consequences appear much later. Intensity comes from putting something at risk **at the moment of the roll**.

| Lever | Description |
|---|---|
| **Bets at roll time** | Wager budget on a result before spinning. Near-misses on bets hurt much more than near-misses on nothing |
| **Heat (dynamic odds)** | Outcomes shift future odds. Good results push toward danger; bad results toward relief. Streaks have momentum and the player reads trends |
| **Decisions between rolls** | After a result, choose: pay to adjust odds, draft one of three outcomes, or place a tile. Rolls become checkpoints in a chain of decisions |
| **Cascades** | One outcome changes the next table. A Boss result swaps the loot wheel for a better one; a Shrine result adds a curse die. Rolls interact |
| **Doom track** | Instead of a fixed room budget, a track advances on bad rolls. Keep expanding for more payout or stop before it fills. If it fills, generation ends mid-build leaving the dungeon unfinished |
| **Reveal presentation** | The spin slows, hovers on a neighbor, then lands. Cheap in ASCII, big for feel |

**Tone sketch:**

```
STEP 3/6 · ROOM TYPE          Budget: 12   Heat: ▮▮▯▯▯
Wheel: Empty 40 · Trap 25 · Loot 20 · Shrine 10 · Boss 5
[1] Spin   [2] Pay 2: halve Trap   [3] Bet 3 on "Loot or better"
> 3
spinning... Trap... Trap... Loot?... Trap.
Bet lost (-3). Heat +1: next spin leans dangerous.
```

### 6.6 Editing mid-generation

Between rolls (never during a roll) the creator can:
- Disable a device or module for the remaining steps
- Ban a face or remove a segment (at cost)
- Swap a device for another (at cost)
- Stop generation early if a doom track allows it

The **Generation Menu** presents modules as a pipeline with per-module mode toggles (Off / Plain / Custom), a running budget, and ratings updated live.

### 6.7 Generation must connect to consequences

Generation choices should show up as felt gameplay effects: room and resource tables set scarcity of food and light; anchor frequency sets how findable repair is; chaos modules lower starting Integrity. If a menu choice has no consequence in play, cut it.

---

## 7. Devices (Random Sources)

### 7.1 Core abstraction

Every device implements the same interface: it takes a **table** (outcomes with weights), a **mask** (disabled outcomes), optional **state**, and a **quirk**, and returns an outcome. Dice, wheels and decks differ in how the player manipulates them and how they keep state, not in the math.

```
RandomSource {
  table:   [ { id, weight, tags } ]
  mask:    set<id>
  state:   device-specific (deck contents, depleted segments, streak count)
  quirk:   optional rule modifier
  roll(rng, context) -> Outcome
}
```

Player edits are changes to weights, masks, and state.

### 7.2 Device catalog

| Device | How it works | Player manipulation | Notes |
|---|---|---|---|
| **d6 / d20** | Uniform roll | Modifiers, banned faces, rerolls | Simplest; starter device |
| **2d6** | Bell curve: 7 most likely | Modifiers, ban totals | Direction: 7 = straight ahead, extremes = sharp turns |
| **Weighted die** | Uneven faces | Move weight between faces | Same math as wheel |
| **Wheel** | Segments with sizes | Resize or remove segments | Great presentation |
| **Deck of cards** | Draw without replacement | Add, remove, stack; reshuffle when empty | Best for "controlled randomness"; player plans around what is left |
| **Tile draw (Carcassonne-style)** | Draw a room tile with a door configuration; choose where and how to place it (rotate) | Draw pool edits | Controlled randomness with a spatial puzzle; strong map generator |
| **Token bag** | Pull tokens, return them | Add or remove tokens = tune odds directly | Intuitive weighting |
| **Draft** | Roll or draw three outcomes, pick one (or the creator picks for the explorer) | Number of options, who picks | Good decision device |
| **Coin streak** | Flip until you fail | Coin bias | Push-your-luck for bigger rooms or bonus loot |
| **Slot machine** | Reels with hold and nudge | Hold and nudge counts | Presentation-heavy |
| **Plinko** | A ball falls through pegs the player can place | Peg placement | Easy in ASCII, satisfying |
| **Betting** | Wager budget on a result | Wager size and target | Not a device alone: a layer applicable to any device |

**Starter kit (v0.1 to v0.3):** 2d6, weighted table, coin streak. Everything else is unlocked through meta-progression (Section 15) or added in later milestones.

### 7.3 Depletion and state

Every device has a state. Options set per device or quirk:

- **Depleting:** an outcome is removed after landing, permanently or until refilled
- **Replenishing:** resets when exhausted (deck reshuffle)
- **Stable:** never changes (default dice)

### 7.4 Device quirks

Each device can carry a quirk. Examples **[TUNABLE, content grows over time]**:

| Quirk | Effect |
|---|---|
| **Cursed die** | Cannot roll the same number twice in a row |
| **Greedy wheel** | Segment sizes grow for outcomes that have not landed recently |
| **Hoarder deck** | Discard pile is not reshuffled until a Boss outcome |
| **Fickle die** | One random face swaps each roll |
| **Hungry bag** | Removes a token each time a good outcome lands |
| **Echo coin** | A streak of 3 doubles the reward but halves the next roll's odds |

Quirks are priced like everything else.

### 7.5 Heat

Heat is a shared modifier track: results shift weights on future rolls in the same pipeline. It is visible to the creator. Tuning is a core intensity lever (Section 6.5).

---

## 8. Dungeon Model and Map Generation

### 8.1 Grid model

The dungeon is a **square grid** with four cardinal directions (N/E/S/W). Each cell holds at most one room. Rooms connect through **exits** in cardinal directions. The entrance is the origin.

Room data:

```
Room {
  id, position (x, y), type, exits: {N,E,S,W: link|none|hidden},
  contents, quirks, description_seed,
  visited: bool, stale: bool (in notebook), theme_tags
}
```

### 8.2 Room types (base set) **[TUNABLE]**

| Type | Function |
|---|---|
| Empty | Nothing; safe passage; sometimes flavor |
| Supplies | Refills supplies (food/light) |
| Hazard | Costs HP or resources; may be avoidable with tools |
| Loot | Adds to loot total |
| Anchor | Restores Reality Integrity (once) |
| Shrine | Gamble/choice room (curse or blessing) |
| Boss | Guardian room with high loot; optional |
| Vault | Themed special room (Section 8.5) |
| Exit (rare) | Found exit; works immediately with no threshold (Section 13.5) |

### 8.3 Expansion algorithm (blind/lazy and pre-generated)

Generation grows the dungeon room by room from a current cell.

**Direction/exit roll (baseline, 2d6 relative to entry direction) [TUNABLE]:**

| 2d6 | Result |
|---|---|
| 2 | Dead end |
| 3-4 | One exit, a turn |
| 5-6 | One exit, straight ahead |
| 7 | Ahead plus one side |
| 8-9 | Left and right |
| 10-12 | All three |

**Collision rule.** When an exit points into an existing room, the generator chooses among a **loop link**, a **wall**, or a **door**. Loops are encouraged: they make mapping interesting ("is this a room I visited?").

**Termination.** A pre-generated dungeon ends by a room budget, a distance-based boss placement, or a doom track. A blind dungeon never ends by itself: it generates as long as the player opens doors, subject to the guardrails below.

### 8.4 Optional layout algorithms ("big map mode")

For larger dungeons, an optional pre-layout algorithm sets the *skeleton* before rolls fill in details:

- **Random walk / drunkard's walk:** organic, winding
- **BSP (binary space partition):** rooms and corridors in divided regions
- **Cellular automata:** cave-like
- **Template/prefab:** fixed shapes for themes (a cross, a spiral)

Skeleton first, then rolls decide contents and quirks room by room, several at a time. This is a later-milestone feature (v0.8+).

### 8.5 Themes (Vault-style)

A theme is a **bundle of modifiers** that changes how a dungeon looks, reads and plays. In most games a theme is a re-skin plus a few rule changes; here it is data first.

A theme can contain:
- Room-type weights and loot tables
- Theme-specific special rooms and enemies
- Theme quirks
- Starting Integrity and decay adjustments
- Flavor text pools
- Optionally, **one theme rule or meter** (see tiers below)

**Theme tiers (by engine cost):**

| Tier | What it adds | Cost |
|---|---|---|
| **Tier 1: Data-only** | Tables, flavor text, special rooms, enemies, quirks | Cheap; only content |
| **Tier 2: Theme rule or meter** | One extra rule or meter that interacts with an existing resource | Moderate; small engine hook |
| **Tier 3: New action system** | Player actions that reshape the world | Expensive; touches the map, the notebook and the guardrails. **No Tier 3 theme is planned** (see cut ideas below) |

**Rule for Tier 2:** a theme gets at most one extra meter, and it must interact with an existing resource rather than sit beside it. This protects the minimum-meter goal (Section 9.4).

**Planned themes:**

| Theme | Tier | Notes |
|---|---|---|
| **Medieval (no magic)** | 1 | Baseline theme; stone halls, cellars, crypts. The default and the slice's theme |
| **Arcane** | 1 | Advanced magic dungeon: spell items and magical hazards. Natural synergy with reality bending (more bend and anchor content, lower starting Integrity). Content-only at first |
| **Candyworld** | 2 | Adds a **Sugar** meter: candy restores Supplies but raises Sugar, and medicine lowers it. High Sugar gives penalties, and a full meter kills. A comedic trade-off with Supplies, not a fourth free-standing meter |

**First three themes:** Medieval, Arcane, Candyworld.

**Cut idea:** a Minecraft-inspired "Blockworld" theme (placing and breaking blocks) was dropped as too complex. It would need player-editable walls, which interact with the notebook and the rule that keeps the threshold reachable. It can be revisited only if the engine proves stable.

### 8.6 Generator guardrails

1. Every new room connects back to where the player came from.
2. No forced dead-end deaths: a generated dungeon must always have at least one unexplored exit, unless the doom track legitimately ends it.
3. Rooms persist once generated.
4. **Lifeline rule:** at any moment, the number of reachable, unexplored rooms must be at least `T - rooms_explored`, so the threshold can always be reached (see Section 13.3). If any generation or reality change would break this, the generator adds a room instead (conservation).

---

## 9. Exploration Gameplay

### 9.1 Core loop

```
enter a room -> read description -> decide -> update notebook -> repeat
                                   |
                       loot / rest / use item / move through a door
```

Every move spends time and resources; Integrity ticks; the player weighs "one more room" against risk.

### 9.2 Room description format

The text is the interface. Descriptions have a **fixed structure** so the notebook is reliable:

```
== Room: Damp Cellar ==
Type hint: (flavor text describing the room)
You see: (objects, hazards, loot)
Exits: N, E, W         <- always listed; fixed format
Special: (anchor glow / shrine / strange feature)
```

**Truthfulness rule:** the game never lies except via Integrity effects. If the description is wrong, the player must be able to tell it is a reality symptom and not a writing bug.

### 9.3 Actions

| Action | Effect |
|---|---|
| Move (N/E/S/W) | Costs 1 Supply; ticks Integrity |
| Search | Costs time/supplies; may find hidden items or exits |
| Loot | Collect loot in the room |
| Rest | Recover HP at Supply cost; ticks Integrity |
| Use item | Consumables and tools |
| Notebook | Open the notebook (free action) |
| Inspect | Read more detail, costs nothing |
| Extract | Available only at the entrance and only after the threshold is met |

### 9.4 Resources

| Resource | Purpose | Start **[TUNABLE]** |
|---|---|---|
| **HP** | Survival | 10 |
| **Supplies** | Fuel for movement and rest; if depleted, moves cost HP | 15 |
| **Loot** | Score; banked only on extraction | 0 |
| **Reality Integrity** | The clock (Section 11) | 300 (config modifies) |

**Minimum meter count:** HP, Integrity, Supplies. Knowledge costs are paid by erasing notebook pages, so there is no extra meter. There is **no sanity meter** (decided).

### 9.5 Hazards and combat

**Direction (decided):** combat is **turn-based and menu-driven, Pokemon-style**: entering a fight switches to an encounter screen where each side takes turns choosing an action. This fits a terminal well because it needs only menus and text. It is **not** a creature-collecting game; the explorer fights alone with their items.

**Scope control:** turn-based combat is still a real system (enemy data, balance, animations of text). It is built **after generation feels fun** (milestone M3.5), not in the v0.1 slice. Until then, Hazard rooms use the simple resolution described below.

**Interim hazard resolution (v0.1 to M3):** a Hazard room presents a problem with a small set of responses (fight, avoid, use an item) resolved by simple rules.

**Turn-based combat (M3.5):**

| Element | Design |
|---|---|
| Format | 1v1 encounter screen, triggered by Hazard/Boss rooms or monsters |
| Player actions | Attack, Guard, Use Item, Flee |
| Enemy | Data-driven (HP, damage, moves, drops, tags). Shows its **intent** for the next turn, so choices are about reading it, not guessing |
| Resources | Fights spend the same HP and Supplies as exploration, so combat is a resource decision, not a separate game |
| Flee | Costs Supplies and Integrity; may fail |
| Rewards | Loot and drops (some enemies drop reality-bending items) |
| Themes | Enemy tables come from the theme (Section 8.5) |

```
== Bone Warden ==                       Integrity ▮▮▮▮▮▮▯▯ 204/300
Bone Warden  HP ▮▮▮▮▯▯   intends: HEAVY STRIKE
You          HP ▮▮▮▮▮▮▮▯  Supplies 11
 [1] Attack   [2] Guard (halves next hit)   [3] Item   [4] Flee
```

Fights should never be the reason a run is fun; they are a hazard that tests resource decisions.

### 9.6 Information as a resource

In a blind dungeon, supplies buy knowledge:

| Item | Effect |
|---|---|
| Lantern | Shows the type of an adjacent room |
| Scroll of Direction | Reveals the direction of the nearest exit or anchor |
| Chalk | Marks a room so stale-state changes are detected |
| Echo stone | Hints at how many rooms remain to the threshold |

The creator prices item availability (Section 6.3).

### 9.7 Difficulty scaling

Difficulty is defined by the generation config, not a global slider: room-type weights, hazard density, resource scarcity, decay rate, threshold ratio.

---

## 10. The Notebook

### 10.1 Purpose

The notebook is the explorer's **only map**. In a text game the game describes rooms in words, and the notebook is the only grid the player sees.

### 10.2 Features

- Grid view (N up); rooms placed by position
- Room icons (built-in set) and free-text notes per room
- Exits marked per direction
- Player can label, annotate, erase and move entries
- Opens with a single key, free action (no time cost)

### 10.3 Auto-track toggle

| Setting | Behavior | Bonus |
|---|---|---|
| **Manual (off)** | Player places everything, including position and exits | Small score bonus **[TUNABLE]** |
| **Auto-track (on)** | Fills in grid position and exits only; notes and icons remain manual | None |

Auto-track is free but less detailed. Manual mapping is slightly rewarded.

### 10.4 Stale rooms (grey-out rule)

- When a reality effect changes an already-mapped area, the notebook **does not update on its own**.
- Affected rooms **grey out** as "unverified" (when the player has a way to know) or stay unchanged (when they do not).
- Greyed rooms only update when the player **returns and confirms**.
- A player who trusts a greyed room and walks into a changed one pays for it.

**Design note:** the notebook's usefulness is the point of the Integrity system. Integrity symptoms attack the notebook, not just the character.

### 10.5 Notebook as a cost

Some prices in the game are paid in **notebook pages** (rooms erased, notes lost). Knowledge is a currency.

### 10.6 Backtracking

If extraction is at the entrance, the trail you walked is your lifeline. The notebook is survival gear.

---

## 11. Reality Integrity

### 11.1 Concept

**Reality Integrity (RI)** measures how stable the dungeon is. It starts at a value set by the config and drains as the player explores and bends reality. As it falls, the dungeon becomes unreliable, then collapses.

### 11.2 Clock behavior

RI is the run's **slow-burn clock**. It gives a reason to end the run without forcing it at any moment. Every extra room adds loot and risk; Integrity keeps making the risk bigger.

**Visible clock rule:** the player sees RI and roughly how fast it drops. If it decays invisibly, running out feels like the game cheating rather than the player misjudging.

### 11.3 Drain and repair **[TUNABLE, baseline]**

| Event | RI change |
|---|---|
| Enter a new room | -8 |
| Move into a known room | -2 |
| Reality bend | Scales with the size of the change (Section 12.4) |
| Anchor room (once each) | +45 |
| Anchor item / ritual | Varies; costs time or supplies |

Repair is **not guaranteed**. The chance of anchors comes from the generation config, so a creator who spent points on chaos and skipped anchors is knowingly gambling.

**Scale (changed after playtest 1):** starting RI is **300**, not 100. The pool has to fund both baseline exploration *and* reality bending. The design target is that a typical run (about 15 new rooms and 15 moves through known rooms) burns **about half the pool** on baseline decay, leaving the other half as buffer, repair headroom and bend fuel. With the old 100 / -4 / -1 numbers, the same run burned about 75%, which left no room for bends and made the player afraid to leave the start.

**Anchor pity rule:** anchor rooms are the only repair, so pure bad luck should not decide a run. Each new room generated without an anchor adds +1 to the Anchor weight in the room table (capped at +15). The bonus resets when an anchor is generated. With the slice weights this roughly cuts the chance of seeing no anchor in 15 rooms from about 46% to about 19% **[TUNABLE]**. Creators can price or remove the pity bonus in the generation menu.

### 11.4 Symptom tiers **[TUNABLE]**

| RI | Symptoms |
|---|---|
| **75% and above** | Stable |
| **~75% or below** | Notebook flickers or shows small errors; one visited room greys out and needs a revisit to confirm |
| **~50% or below** | Rooms shift on their own; when leaving a visited room, one exit may change |
| **~25% or below** | Rooms vanish or merge |
| **0** | Reality falls; run ends |

All tier thresholds are **percentages of the run's starting RI**, so they keep working when a config changes the starting value. The v0.1 slice implements two tiers (Section 18).

### 11.5 Repair sources

- **Anchor rooms:** placed by the creator (priced) or rolled
- **Anchor items:** consumable repair, rarer
- **Rituals:** cost time or supplies

### 11.6 Starting RI

Starting RI is set by the config. Chaotic or cursed modules pay more but start the dungeon closer to falling apart. What the creator does in the menu has a felt cost later.

### 11.7 Guardrail

At baseline decay, RI must not reach zero before the threshold is reachable: `T * decay_per_new_room <= starting_RI - safety_margin`. Configs that violate it are rejected in the creator screen. Chaos modules may lower starting RI only within this limit. The same limit caps how large a room count (R0) a creator can pick for a given starting RI. Example with the slice numbers: T = 4, so 4 × 8 = 32, far below 300 minus the margin.

---

## 12. Reality Bending

Reality bending is the game's central concept and a rare, powerful, expensive mechanic.

### 12.1 Sources

| Source | Rarity | Notes |
|---|---|---|
| **Pre-forged artifacts** | Rare | Safe to use as-is; predictable. Found as loot, boss drops, or through rituals (Section 12.8) |
| **Unforged artifacts** | Rare | Must be reforged before use (gamble). Same sources |
| **Latent ability** | Extremely rare | A player-innate power; very hard to trigger. Exact acquisition still open (Section 20) |
| **External events** | Super rare | Reality bends without the player's action |
| **Patron/Warden interventions** | Relation-dependent | Cost Integrity |

The **reality events module** in generation controls availability. It is optional and priced.

### 12.2 What a bend can do

| Bend type | Effect |
|---|---|
| Add room | Creates a room in a chosen or random location |
| Remove room | Removes a room and its links |
| Swap rooms | Exchange two rooms' positions or contents |
| Relocate exit | Moves the exit mechanics or a found exit |
| Reshape exits | Adds/removes exits on a room |
| Rewrite room type | Changes a room's type and contents |
| Shift section | Moves a section of the map |
| Generate section ("god mode") | Opens the generator for a small section; **layout is revealed, contents hidden**. The rarest bend |
| Reveal | Shows a piece of the map |

### 12.3 Conservation

Reality can be moved but not created for free. Adding a room somewhere means one disappears or degrades elsewhere. This keeps chaos from being a pure power-up.

### 12.4 Price

**Reality Integrity is the main price of every bend.** Bigger bends add further costs on top. Prices are **fixed by bend size** (the player does not choose the price). All numbers are **[TUNABLE]**.

| Bend size | Examples | RI cost | Added costs |
|---|---|---|---|
| **Minor** | Reveal a room, change one exit | -10 to -15 | None |
| **Moderate** | Rewrite a room's type, swap two rooms | -25 to -35 | 1 to 2 notebook pages erased |
| **Major** | Add or remove a group of rooms, relocate a found exit | -45 to -75 | Notebook pages erased, and 1 max HP |
| **Extreme** | Generate section ("god mode") | -90 or more | Max HP, a region of the notebook wiped, and reality debt (later collapses or shifts) |

These costs are about 3 to 5% (minor), 8 to 12% (moderate), 15 to 25% (major) and 30%+ (extreme) of a 300 start. Integrity loss is central: **too many bends without fixing the cracks can end the run very quickly.**

### 12.5 Reforges

Reforges use the **same system as generation**: they are preset weight and mask edits on the bend-event table.

| Reforge | Effect on bend table |
|---|---|
| **Lucky** | Weights toward beneficial bends |
| **Unlucky** | Weights toward harmful bends |
| **Chaotic** | Flattens weights; extreme results more likely; more comedy |
| **Calm** | Narrows toward small, safe bends |
| *(more added as content)* | |

- Pre-forged items are the safe, rare option.
- Reforging is a gamble: the reforge result is not in the player's control.
- To avoid "it is just random," the player has a stake: they can accept the result, **pay to reroll with rising cost**, or **lock a reforge in permanently**.

### 12.6 Tone

Bends are chaos and comedy. Reality does not care about the plan. The player can influence *odds* through reforges but not *outcomes*.

### 12.7 Reality bending and the notebook

Bending changes reality silently in mapped areas. The map does not auto-update; it greys out until the player goes back and confirms (Section 10.4).

### 12.8 Acquiring and triggering bends

**Where bending items come from:**
- **Loot chests** (rare)
- **Boss drops**
- **Special rituals** (ritual rooms that cost Supplies, time, or HP and may grant an item)

How often any of these appear is controlled by the reality events module (Section 12.1), so it is priced for the creator.

**How a bend is triggered:**

| Bend size | Trigger |
|---|---|
| **Minor** | Simple use: one key press, the bend happens |
| **Moderate to Extreme** | **Timing challenge** (lock-picking style): a marker sweeps along a bar and the player presses a key inside the target zone |

**Timing results:**
- **Hit:** the bend happens as intended.
- **Near miss:** a weakened version of the bend.
- **Miss:** the item **fails** (used up or cracked) **or** triggers a **bad event** drawn from the item's reforge table.

**Zone width [TUNABLE]:** bigger bends have a narrower zone. Reforges tie in: Calm gives a wider zone, Chaotic a narrower one but a bigger upside.

**Terminal notes:**
- The game is otherwise turn-based, so the timing challenge is used only for bends, which keeps it special and matches the "god-granted power" feel.
- It needs non-blocking real-time key input, which is doable in a terminal.
- **Accessibility:** provide an alternative that is not real-time (for example, a stepped bar or a fixed-odds roll at a slightly worse chance) so players who cannot or do not want to play a timing game can still use bends.

---

## 13. Extraction, Win and Lose

### 13.1 Structure

The run has no boss-kill win condition. **Extraction plus Integrity as the clock** is the goal structure: leave alive with your loot before reality falls. Optional goals (a boss, an artifact, a depth target) can add bonus score but are not required.

### 13.2 End conditions

| End | Trigger | Result |
|---|---|---|
| **Extraction** | Leave via the entrance after the threshold is met, or via a found exit at any time | Loot banked; full score |
| **Death** | HP reaches 0 | Run ends; partial meta rewards (Section 15) |
| **Reality collapse** | RI reaches 0 | Run ends; partial meta rewards |

The entrance is **hard-locked** until the threshold is met. Its purpose is to stop the player from leaving as their first move, so every run involves real exploration. There is no retreat through the entrance before then. The one exception is a **found exit** (Section 13.5).

### 13.3 The threshold rule (hard lock)

The entrance is **sealed** until the explorer has explored **T unique rooms**. The threshold **is derived from the number of rooms reachable from the entrance at the start of the run**, not from the room count at any later moment.

**Definitions:**

- **R0** = number of rooms reachable from the entrance at run start.
- **T** = threshold, computed once at run start as `T = clamp(round(R0 * ratio), T_min, R0)`.
  - `ratio` is a **fixed global constant [TUNABLE default: 0.4]** that creators cannot change. To make the entrance unlock later or sooner, the creator changes the **room count (R0)** instead.
  - `T_min` **[TUNABLE, default 3]** prevents trivial dungeons.
- **Example:** R0 = 10, ratio 0.4, T = 4.

**Rules:**

1. **T is fixed at run start** and never recalculated, even if reality changes the number of rooms.
2. **Explored rooms** = unique rooms **entered** (not generated, not steps, not revisits). The entrance does not count.
3. **Rooms explored are permanent credit.** A room that later vanishes, merges, or changes still counts.
4. **Rooms added later do not raise T.** If new rooms appear, T stays the same.
5. When explored count reaches T, the **entrance becomes an active exit**, regardless of whether new rooms have appeared or old ones are gone.
6. The player then walks back to the entrance and extracts.
7. **What the player sees:** the **ratio** (for example "explore 40% of the dungeon") and their running count of explored rooms, e.g. `Rooms explored: 3 · entrance sealed`. The player is **not** shown T or R0, so they estimate progress from the ratio. When the threshold is met, the game shows a **popup notification and plays a sound** (terminal bell), with a matching on-screen banner so the cue still works with sound off. Items such as the Echo Stone (Section 9.6) can reveal how many rooms remain.
8. **Purpose:** the threshold is an anti-trivial-exit gate, not a completion requirement.

**Lifeline rule (guardrail).** Because retreat is impossible before T, the game must never make T unreachable. At all times, `reachable unexplored rooms >= T - explored`. Any bend, Integrity effect or generation step that would break this instead adds a room (conservation).

**Blind mode (decided):** in blind/lazy mode the generator commits at run start to a hidden **planned room count** that acts as R0. This is a **creator config value** (in odds-only mode, the player's own setting; in contracts, part of the contract). T is derived from it with the ratio. The player sees the ratio only; R0 and T stay hidden. In pre-generated two-player mode the same visibility default applies, unless the creator's briefing settings or an item reveal more.

**Hard-lock fairness.** A hard lock can produce unfair deaths, so:
- Baseline supplies must be enough to reach T (the simulation checks it).
- The RI guardrail (Section 11.7) ensures reality does not collapse before T at baseline play.
- Danger ratings are shown in contracts.

### 13.4 Walking back

After T is reached, the explorer must return to the entrance. RI keeps ticking with each move, and mid-late-game symptoms can change the path back. This is the second half of the gamble: the route you mapped may not be there.

### 13.5 Found exits (decided)

Rare **exit rooms** can be generated (Section 8.2). A found exit **works immediately**: the threshold does not apply to it, and the player can extract through it at any time. The threshold exists only to stop players leaving via the entrance as their first move; it is not meant to restrict exits that the player had to find.

- Found exits are a lucky break, so they must be rare. Frequency is a priced creator knob (Section 6.3): more exits means shorter, cheaper runs and a lower reward rating. Default: a very low room-table weight, roughly 1 to 2% **[TUNABLE]**.
- Bends can relocate or collapse found exits (Section 12.2). The entrance remains the fallback once T is met.
- Because a found exit can appear early, extraction score still depends on loot and rooms explored (Section 14.1), so leaving early is safe but pays little. **No extra score penalty** applies beyond that (decided in v0.3).
- The lifeline rule (Section 13.3) still applies, since the entrance is sealed and a found exit is never guaranteed.
- Not in the v0.1 slice.

---

## 14. Scoring, Favor and Economy

### 14.1 Explorer score **[TUNABLE]**

```
score = banked_loot × rooms_explored × reward_multiplier
        + manual_mapping_bonus
```

- `reward_multiplier` comes from the config's Reward Rating (Section 6.3).
- On death or collapse, no loot is banked: score is zero, but meta-currency is still earned (Section 15).

### 14.2 Creator Favor

Favor is earned per relation (Section 5.2) and spent on interventions. In solo modes there is no Favor.

### 14.3 Contract ratings

Every config has a visible:
- **Danger Rating** (how likely and how bad)
- **Reward Rating** (score multiplier)
- **Depth** (threshold or planned room count)

### 14.4 Economy sinks and sources

| Currency | Source | Sink |
|---|---|---|
| Budget (generation points) | Per run, or per contract | Odds modifications, modules, rerolls |
| Loot | Rooms | Score |
| Supplies | Rooms, start | Movement, rest |
| Favor | Creator play | Interventions |
| Shards (meta) | End of run | Unlocks (Section 15) |

---

## 15. Meta-Progression

Roguelite structure: single-dungeon runs, permanent unlocks between runs.

### 15.1 Meta-currency

**Shards** are earned at the end of every run, based on how well the run went (loot collected and rooms explored).

- **Extraction:** full Shards.
- **Death or collapse:** no score, but the run still pays `fail_fraction` of the Shards it had earned so far. `fail_fraction` is a **config value, default 50% [TUNABLE]**.

**Framing note:** the fraction only reduces what a failed run *earns*. It never takes away Shards the player already banked from earlier runs. Losing half of stored progress feels much worse than earning half of a run's payout, so the UI should say what you *keep* ("You keep 50%: 12 Shards"), not what you lose.

### 15.2 What can be unlocked

| Category | Examples |
|---|---|
| Devices | Wheel, deck, tile draw, token bag, draft, slot, plinko |
| Quirks | New device quirks |
| Room types and special rooms | Shrines, vault rooms |
| Themes | Flooded Crypt, Bone Library, etc. |
| Reality items | Artifacts, reforge types |
| Modules | Access to deeper generation modules |
| Notebook features | Icons, stamps, tools |

### 15.3 Purpose

- **Scope control:** starter kit is 2d6 plus one table; players are not overwhelmed by an 8-module menu on day one.
- **Progression:** the gallery of random events grows over time.
- **Risk:** unlocks expand choice, not raw power, wherever possible. Power unlocks should be sidegrades.

### 15.4 Future run structures (not in base design)

- **Chain of dungeons** with escalating size and danger
- **Persistent dungeon** where the next explorer enters the same dungeon with previous changes intact. Fits creator/explorer and reality bending, but is the most complex.

---

## 16. Terminal UI and UX

### 16.1 Principles

- Keyboard only, numbered options plus single-key shortcuts
- Readable at 80×24, better at larger sizes
- ASCII/Unicode box drawing, minimal color (with accessible options)
- Suspense through pacing: animated reveals, delays that can be skipped

### 16.2 Screens

| Screen | Purpose |
|---|---|
| Main menu | New run, contracts, continue, unlocks, settings |
| Mode/setup | Pick mode, relation |
| Generation menu | Pipeline modules, mode toggles (Off/Plain/Custom), budget, ratings |
| Roll screen | Device presentation, options between rolls |
| Briefing | What the explorer is told |
| Exploration | Room text, resources, actions |
| Notebook | Grid, icons, notes |
| End screen | Score, meta rewards, run recap |
| Unlocks | Meta-progression shop |

### 16.3 Exploration screen sketch

```
┌ Damp Cellar ─────────────────────────────────────────────┐
│ You descend into a low cellar. Water pools around old    │
│ barrels. A faint hum comes from the north wall.          │
│                                                          │
│ You see: rotting barrels, a glint of coins.              │
│ Exits: N, E, W                                           │
└──────────────────────────────────────────────────────────┘
 HP 8/10   Supplies 11   Loot 3   Integrity ▮▮▮▮▮▮▯▯ 204/300
 Rooms explored: 3 · entrance sealed (explore 40% of the dungeon)
 [N/E/S/W] Move  [L] Loot  [R] Rest  [I] Item  [B] Notebook
```

### 16.4 Notebook screen sketch

```
         N
   ┌───┐ │
   │ ? │──┼── ┌───┐   ┌───┐
   └───┘ │    │ C │───│ $ │  (greyed = stale)
   ┌───┐ │    └───┘   └───┘
   │ @ │─┘        (@ = entrance)
   └───┘
 [Arrows] move cursor  [T] note  [I] icon  [X] erase  [A] auto-track: ON
```

### 16.5 Accessibility

Color-blind safe palettes, no color-only information, adjustable animation speed, screen-reader-friendly plain text mode.

---

## 17. Technical Design

### 17.1 Language and stack **[OPEN]**

Language is undecided. Suggestions:

| Option | Pros | Cons |
|---|---|---|
| **Python + Rich/Textual** | Fastest prototyping; good TUI libraries | Distribution is heavier |
| **Rust + ratatui** | Fast, single binary | Slower iteration |
| **Go + Bubble Tea** | Simple, single binary | Less expressive for data-heavy logic |
| **TypeScript + Ink** | Familiar to web devs | Node dependency |

**Recommendation:** prototype the vertical slice in Python to prove the design; decide on a production stack later.

### 17.2 Architecture

Separate the **engine** (pure logic, no I/O) from the **UI** (rendering, input). The engine should be runnable headlessly for simulation and tests.

```
/engine
  rng.py         seeded RNG streams
  devices/       dice, wheel, deck, tiles, bag, draft, coin, ...
  tables/        table + weight + mask logic
  generation/    pipeline, modules, budget, ratings
  dungeon/       rooms, grid, expansion, guardrails
  reality/       integrity, symptoms, bends, reforges
  run/           state, actions, resources, threshold rule
  notebook/      map data model, stale logic
  score/         scoring, favor, meta rewards
/data
  tables/*.yaml  room types, loot, quirks, themes (data-driven)
/ui
  screens/       menu, generation, exploration, notebook
/sim
  bots.py        headless bot explorers for balancing
/tests
```

### 17.3 Data-driven content

Tables, themes, quirks, room descriptions and reforges live in data files (YAML/JSON/TOML), not code. Adding content should not require changing engine code.

### 17.4 Randomness and determinism

- One **run seed** feeds separate RNG streams per device/module, so a change in one module does not change others.
- **Every roll is logged** (device, table state, result). This enables replays, debugging, sharing seeds, and verifying the "no free rerolls" rule.
- Room generation is deterministic given the seed and the order of door openings.

### 17.5 Save and share format

- **Run save:** full state (rooms, resources, notebook, RNG streams, roll log).
- **Dungeon file:** for two-player, the creator exports a `.dungeon` file (JSON) that the explorer loads. This makes **asynchronous Architect play** possible with no networking.
- Warden and Patron relations need **live interaction**. **Hot-seat first** (both players on the same machine, alternating input); networking is a later milestone.

### 17.6 Simulation and balancing

A headless simulation runs bot explorers (random, greedy, cautious) through configs to check:
- Threshold reachable within the RI guardrail
- Survival rate at baseline
- Danger and Reward Ratings roughly match observed outcomes
- No generator softlocks (lifeline rule)

The creator screen can call a lightweight simulation to warn about unbeatable configs.

### 17.7 Testing

- Unit tests for tables, masks, devices, depletion, threshold logic
- Property tests for generation guardrails (every generated dungeon satisfies the lifeline rule)
- Replay tests using logged rolls

### 17.8 Creator-agent hooks (for a future AI Host)

The AI Host is deferred, but the engine reserves the seams for it now so it can be added without rewrites. Cost is small and no AI-specific code is written yet.

- **`CreatorAgent` interface:** the creator during a run is an agent with `on_run_start(config)`, `on_event(event)` and `available_actions(favor)`. Implementations: `NoCreator` (solo default), `HumanCreator` (hot-seat, later network), and a future `AIHost`.
- **Event bus:** the engine emits structured events (`RoomEntered`, `HpChanged`, `IntegrityChanged`, `BendUsed`, `ClutchEscape`, and so on). Favor scoring and any future host commentary consume the same stream.
- **One intervention path:** every creator action goes through the same bend/action API and costs Integrity, so an AI Host is just another agent under the same rules.

---

## 18. Vertical Slice Specification (v0.1)

**Goal:** answer "is blind exploring plus the notebook fun?" before building any generation menu.

### 18.1 Core loop

Enter a room → read description → decide (loot, rest, move) → update notebook (manual or auto) → repeat until extraction or death.

### 18.2 Generation (blind; resolved on door open, then stored)

- **Exits:** 2d6 relative to entry direction (table in Section 8.3).
- **Room type:** one weighted table **[TUNABLE]**: Empty 40, Supplies 20, Hazard 20, Loot 15, Anchor 5. **Anchor pity:** +1 Anchor weight for each new room generated since the last anchor, capped at +15, reset when an anchor generates (Section 11.3).
- **Collision:** if an exit points into an existing room, it becomes a loop link.
- **Guardrail:** the map never has zero unexplored exits; lifeline rule holds.

### 18.3 Resources

- HP 10, Supplies 15.
- Each move costs 1 Supply; at 0 Supplies, each move costs 1 HP.
- Hazard: costs HP. Supplies room: refills some Supplies. Loot room: adds to loot.

### 18.4 Reality Integrity

- Start **300**; **-8** per new room; **-2** per move into a known room. (Playtest 1 change from 100 / -4 / -1.)
- Anchor: **+45**, once per anchor.
- Two symptom tiers (as percentages of the starting RI):
  - **RI <= 70% (210):** one random visited room greys out in the notebook and needs a revisit to confirm.
  - **RI <= 40% (120):** when leaving a visited room, one of its exits may change.
- **RI = 0:** reality falls; run ends.

### 18.5 Threshold (hard lock)

- **Planned room count (R0 for blind mode):** a hidden number rolled or set at run start. **[TUNABLE, v0.1 fixed: 10]**
- **T = round(R0 × 0.4) = 4** for the slice's fixed R0 = 10. (The design example: 10 rooms, T = 4.)
- The entrance is sealed until 4 unique rooms are entered. Rooms explored is permanent credit; new or vanished rooms do not change T.
- The player is shown the ratio (40%) and their explored count, not T or R0.
- After T, walk back to the entrance and extract.
- **No retreat before T.**
- **Baseline check:** `T × 8 = 32 RI` spent by threshold: comfortably under 300.

### 18.6 Notebook

- Grid, room icons, text note per room.
- Auto-track toggle: on = grid position and exits only; off = manual with a small score bonus.
- Stale rooms grey out and update only on revisit.

### 18.7 Score

`score = loot × rooms_explored` (+ small manual mapping bonus).

### 18.8 Not in the slice

Wheels, cards, bets, quirks, reforges, reality bends, roles, contracts, budget, themes, combat, meta-progression, found exits. All plug into the room-type and exit tables later.

### 18.9 The test

Play 20 runs. If the player makes real decisions about when to push on, what to write in the notebook, and when to head back, the core works. If it feels like walking a corridor, fix that before adding features.

**Tuning note:** the slice's purpose is feel, not balance. Change one variable per playtest and log the result (Section 19.4).

---

## 19. Roadmap, Testing and Risks

### 19.1 Milestones

| Milestone | Content | Exit criterion |
|---|---|---|
| **M0** | Engine skeleton: RNG, table/device interface, data loading, headless run | Unit tests pass |
| **M1: v0.1 Slice** | Section 18 | 20 runs playable |
| **M2: Playtest** | Tuning, notebook UX pass, bot simulation | Real decisions observed; slice is fun |
| **M3: v0.3 Generation + Contracts** | Creator screen (2d6, weighted table, coin streak), budget, ratings, Off/Plain/Custom modes, contract board, odds-only mode | Generation feels fun on its own |
| **M3.5: Combat** | Turn-based encounter screen (Attack/Guard/Item/Flee), data-driven enemies, Hazard/Boss integration | Fights are a decision, not a chore |
| **M4: v0.4 Devices** | Wheel, deck, token bag, draft, betting layer, depletion, quirks, Heat | Each device has a distinct feel |
| **M5: v0.5 Reality Bending** | Artifacts, reforges, bend table, conservation, price system, symptom tiers 3-4 | Bends are chaotic yet fair |
| **M6: v0.6 Meta and Themes** | Shards, unlocks, first three themes (Medieval, Arcane, Candyworld), special rooms | Reasons to replay |
| **M7: v0.7 Two-Player (async)** | `.dungeon` export/import, Architect relation | Two people can play |
| **M8: v0.8 Big Maps** | Pre-layout algorithms, tile draw device | Large maps work |
| **M9: v0.9 Live Relations** | Warden and Patron via hot-seat first (networking later), Favor | Relations feel distinct |
| **Later** | AI Host solo, persistent dungeon, chain runs, puzzle mode | |

### 19.2 Risks

| Risk | Mitigation |
|---|---|
| **Generation feels like a form** | Stakes at the roll (Section 6.5); build the slice first; playtest generation as its own game |
| **Player-controlled randomness is just randomness** | Budget, commitment, ratings, no free rerolls |
| **Scope explosion** (infinite event gallery) | Data-driven tables, starter kit, unlock model, strict milestones |
| **Manual mapping is tedious** | Auto-track toggle, in-game notebook, information items |
| **Hard lock causes unfair deaths** | Guardrails, simulation, lifeline rule, clear ratings |
| **Two-player live modes are heavy** | Async Architect first; live later |
| **Tone whiplash (strategy vs chaos)** | Design the contrast on purpose; playtest transitions |
| **Reality bending becomes an everything button** | Conservation, price scaling, Integrity cost, rarity |
| **Blind text ambiguity confuses the player** | Fixed description format; truthfulness rule |
| **Depleting or dynamic odds are hard to communicate** | Always display current weights and state in the UI |

### 19.3 Playtest plan

1. Solo, 20 runs of the slice, log decisions and death causes.
2. Watch a second person play blind; observe notebook use.
3. Simulate bots to find generator edge cases.
4. Generation-only playtest: does the creator screen hold attention without an explorer?

**Metrics to log every run:** rooms explored, farthest distance from the entrance, RI at the end, cause of end (extraction, death, collapse), anchors found, moves through known rooms, and the moment the player decided to head back. The "farthest distance" figure is the key one for spotting players who hug the start.

### 19.4 Playtest log

**Playtest 1 (2 runs, v0.1 slice, designer only)**

| Finding | Reading | Change |
|---|---|---|
| Run 1: Integrity almost hit zero because the first anchor was slow to appear | Anchors are the only repair, so bad luck decided the run. 100 RI at -4 per room is about 25 rooms of budget, and the way back also costs RI | Anchor pity rule (Section 11.3) |
| Run 2 felt good: roaming, looting and exploring, and the notebook worked well | The core loop and notebook feel are working | None |
| The player stayed close to the start out of fear of running out of Integrity | The clock is meant to create a gamble, but here it made "stay close" the only sensible play. Also, the pool must fund bending later, so baseline decay must leave headroom | Starting RI 100 to 300, per-room costs rescaled to -8 / -2 (Section 11.3) |

**Rejected option:** 300 or 500 starting RI with the old -4 / -1 costs. That makes baseline decay only 15 to 25% of the pool, so with no bending in the slice, Integrity would barely matter and the symptom tiers would rarely appear.

**Next experiments (one at a time):**
1. Replay with the new numbers. Check that the farthest-distance figure grows and that tier 1 symptoms appear in longer runs.
2. If players still hug the start, add a pull: loot value rising with distance from the entrance.
3. If Integrity is now irrelevant, lower the starting RI (a config value) before touching per-room costs.

---

## 20. Open Questions

### Resolved in v0.3

| Question | Decision |
|---|---|
| Blind-mode R0 | Creator config value (the room count); the threshold ratio is fixed (40%) |
| Progress feedback | Running explored count plus a popup and sound when the entrance unseals |
| Found exit tuning | No extra early-extraction penalty; frequency stays a priced creator knob |
| Death reward amount | Config fraction, default 50%, framed as what you keep |
| Two-player information | Theme and danger rating shown by default (creator may hide the rating); nothing else |
| Threshold ratio bounds | Ratio is fixed; creators change room count instead |
| Latent ability and triggers | Items come from loot, boss drops and rituals; minor bends are simple use, bigger bends use a timing challenge |
| Bend price presets | RI first; knowledge and max HP added as bends grow; fixed by size |
| Sanity meter | No |
| Combat depth | Turn-based, Pokemon-style (single fighter, no creature collecting; confirmed), built after generation (M3.5) |
| First themes | Medieval, Arcane, Candyworld; Blockworld cut as too complex |
| Language and stack | Confirm after prototype |
| Live relations | Hot-seat first |
| Bettor relation | Removed |
| AI Host hooks | Reserved (Section 17.8) |

### Still open

1. **Latent ability:** the innate, item-free bend power is still undefined. Proposal: the rarest outcome of a ritual. Needs a decision.
2. **Timing challenge details:** exact zone widths, the near-miss rule, and the non-real-time accessibility alternative.
3. **Found exit default weight:** the 1 to 2% figure needs playtesting.
4. **Candyworld Sugar rules:** rates for Sugar gain and medicine, penalty thresholds, and what fills the meter.
5. **Arcane theme content:** which spell items and hazards, and how strongly it pushes reality bending.
6. **Bend price numbers:** the ladder in Section 12.4 is a starting guess.
7. **Language and stack:** confirm after the prototype.

---

## 21. Appendices

### 21.1 Example blind run (v0.1 slice, abridged)

```
You stand at the entrance. Rooms explored: 0 · entrance sealed (explore 40% of the dungeon).
Integrity 300. HP 10. Supplies 15.

> N
== Damp Cellar ==  (new room)   Integrity 292
You see: rotting barrels. Exits: N, E, W.
> B   (notebook: place room at (0,1), note "cellar - safe")

> E
== Bone Hall ==  (new room)   Integrity 284
Hazard: falling ceiling stones. HP -2.
Exits: E.

> E
== Quiet Nook ==  (new room)   Integrity 276
You see: a chest. Loot +3. Exits: W.
Rooms explored: 3 · entrance sealed.

> W, W, N ...
== Glowing Alcove ==  (new room)   Integrity 268
Anchor: a faint glow. Integrity +45 (once).
Rooms explored: 4 · ENTRANCE UNSEALED.

> (walk back; Integrity ticks; at 70% (210) a room in the notebook greys out)
```

### 21.2 Example creator relation config (future)

```
Relation: Patron
Favor earned: clutch escape +3, discovery +2, comedic bend +2, extraction +5
Favor decay: repeated moment type earns half
Spend: gift item (3), hint (1), curse (2), nudge door (2, drains Integrity 3)
Integrity cost per intervention: yes
Guardrail: cannot make threshold unreachable
```

### 21.3 Example generation module config (future)

```
module: room_type
mode: custom
device: wheel
table:
  empty:  40
  hazard: 25
  loot:   20
  shrine: 10
  boss:   5
mask: []
quirk: greedy_wheel
cost: +1 budget (danger up), starting RI -5
bet: enabled
```

### 21.4 Design decision log

| Decision | Reason |
|---|---|
| Control odds, not outcomes | Avoid free "pick the safe result" |
| Blind, lazy generation for solo | Resolves the "why map if you generated it" contradiction |
| Rooms persist after generation | Notebook must be meaningful |
| Integrity as the clock | Reason to leave without a timer; ties to the notebook |
| Starting RI 300 with -8 / -2 per room (playtest 1) | Baseline decay about half the pool; the rest funds anchors, buffer and bends |
| Anchor pity rule | Repair is the only counter to the clock; luck alone should not end a run |
| Extraction plus threshold, hard lock | Gives every run a goal without a boss win condition; the lock stops leaving as a first move |
| Player sees the ratio, not T | Keeps blind mode blind while still telling the player roughly how much to explore |
| Found exits work immediately | The threshold only gates the entrance; a found exit is a lucky break the player earned |
| Failed runs still pay Shards, no score | Keeps failed runs feeling worthwhile for progression |
| Fail payout is a config fraction (default 50%), framed as what you keep | Never take away banked progress; losing stored currency feels bad |
| Threshold ratio is fixed; creators set room count instead | One rule for the lock; creators still control commitment length |
| Unseal notification is a popup plus sound | Clear cue without forcing the run to end |
| Bend price is RI first, extras scale with size | Simple, readable price ladder; RI stays the central resource |
| Minor bends are simple use; bigger bends use a timing challenge | Makes big bends feel earned and risky |
| No sanity meter | Keep meters to HP, Supplies, Integrity |
| Turn-based Pokemon-style combat, built after generation | Fits a terminal; generation is the higher risk |
| First themes: Medieval, Arcane, Candyworld; Blockworld cut | Data-first content; Blockworld was too complex |
| Creator may hide the danger rating in two-player | Confirmed; the explorer sees theme, and danger rating unless hidden |
| Bettor relation removed | Judged unnecessary |
| Hot-seat before networking | Cheapest way to test live relations |
| Reserve AI Host hooks now | Small cost, avoids a rewrite later |
| Threshold derived from R0 at run start | Stable target regardless of later bends |
| Single dungeon per run | Scope; meta-progression handles growth |
| Relations as presets on one engine | One system, many roles |
| Combat minimal | Text combat is expensive; survival first |
| Data-driven content | Gallery of events will grow forever |
