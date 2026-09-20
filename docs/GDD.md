# Unstable Depths — Game Design Document

> **Living document · Version 0.1 prototype · Last updated September 2026**
>
> This is the current, buildable game target. It is intentionally narrower than
> the long-term vision; future ideas belong in the [roadmap](ROADMAP.md), and
> reasons for changes belong in the [design log](DESIGN_LOG.md).

## Pitch

*Unstable Depths* is a text-based dungeon-crawling roguelite where the player
explores a blind, shifting dungeon and maps it in an in-game notebook. Every
door may reveal a new room. Every move spends resources. Reality Integrity
gradually falls, making the map less trustworthy and eventually ending the run.

The player must explore enough unique rooms to unseal the entrance, then find
their way back out with their loot.

## Current prototype goal

The v0.1 vertical slice answers one question: **is blind exploration plus the
notebook fun?** It deliberately does not yet include the later odds-authoring
game, combat, contracts, themes, artifacts, or progression.

The desired play loop is:

```text
enter room → read a reliable description → map / make a decision
    → loot, rest, or move → spend resources → repeat
```

The player should make meaningful decisions about pushing onward, gathering
loot, preserving supplies, trusting an old map entry, and returning safely.

## Design pillars

1. **The map is the player's responsibility.** Room descriptions are clear and
   truthful. Reality Integrity is the only system allowed to undermine known
   information, and it must signal that it has done so.
2. **Reality is both resource and clock.** Integrity limits the run and creates
   tension without a conventional turn timer.
3. **Blind rooms persist.** Once a room is generated, it stays generated unless
   a visible reality effect changes it.
4. **Extraction is the win condition.** Loot has value only when carried out.
5. **Minimum meters.** HP, Supplies, and Reality Integrity are enough for the
   slice; there is no separate sanity meter.

## Run structure

```text
Start → explore blind rooms → entrance unseals → return → extract
                                      └→ death / reality collapse
```

The entrance begins hard-locked. It cannot be used to abandon a run before the
exploration requirement is met.

### Extraction threshold

The slice commits to a hidden planned room count, `R0 = 10`.

```text
threshold T = round(R0 × 0.4) = 4
```

- Entering four unique non-entrance rooms unseals the entrance.
- The player sees `explore 40% of the dungeon` and their explored count, but
  not the exact threshold or room count.
- Exploration credit is permanent, even if a later system changes a room.
- After unsealing, the player must physically return to the entrance.
- The generator must always preserve enough reachable unexplored rooms to make
  the threshold achievable.

## Player resources

| Resource | Start | Purpose |
| --- | ---: | --- |
| HP | 10 | Reaching 0 ends the run. |
| Supplies | 15 | One is spent per move; at 0, movement costs 1 HP instead. |
| Loot | 0 | Collected score; banked only on extraction. |
| Reality Integrity | 300 | Dungeon stability and the run clock. |

Rest costs 2 Supplies and restores up to 2 HP.

## Reality Integrity

Reality Integrity (RI) is always visible. The Playtest 1 balance is:

| Event | RI change |
| --- | ---: |
| Enter a newly generated room | −8 |
| Move into a known room | −2 |
| Rest | −2 |
| Use an anchor, once | +45 |
| Reach 0 RI | Run ends in reality collapse |

### Instability symptoms

Thresholds are percentages of starting RI so the system can later support
different configurations.

| RI level | Slice behavior |
| --- | --- |
| Above 70% | Stable dungeon. |
| 70% or below (210) | A previously visited room may become stale in the notebook until revisited. |
| 40% or below (120) | Leaving a known room may reveal a new exit. |
| 0 | Reality collapse; the run ends. |

### Anchor pity rule

Anchors are the prototype's only repair source. To reduce runs lost solely to
bad luck, each newly generated non-anchor room adds `+1` to the anchor weight
for the next room, capped at `+15`. Generating an anchor resets the bonus.

## Dungeon generation

The dungeon is a square grid with north, east, south, and west exits. Rooms are
resolved lazily—when the player first enters them—and then stored permanently.

### Exits

Exit generation uses a 2d6 roll relative to the direction of entry:

| 2d6 | Result |
| --- | --- |
| 2 | Dead end |
| 3–4 | One turning exit |
| 5–6 | One forward exit |
| 7 | Forward plus one side exit |
| 8–9 | Left and right exits |
| 10–12 | All three exits |

The back exit always leads to the room the player came from. Before the entrance
unseals, the lifeline rule guarantees an onward route even when the rolled
result would otherwise stop the run. A collision with an existing position
becomes a loop link.

### Room table

| Room type | Base weight | Behavior |
| --- | ---: | --- |
| Empty | 40 | Safe passage and flavor. |
| Supplies | 20 | Immediately restores a small amount of Supplies. |
| Hazard | 20 | Immediately costs 1–3 HP in the slice. |
| Loot | 15 | Contains 2–5 loot; player chooses when to take it. |
| Anchor | 5 + pity | Restores RI once. |

## Notebook

The notebook is the player's map. It shows the grid with room icons, the player
position, stale entries, and free-text notes.

- Opening the notebook costs no time.
- A stale room is shown with `?` and only becomes confirmed on revisit.
- The prototype includes an auto-track setting and awards a small score bonus
  when auto-tracking is disabled. Full manual placement remains an upcoming UI
  improvement.

## Scoring and endings

| Ending | Result |
| --- | --- |
| Extraction | `loot × rooms explored`, plus the manual-mapping bonus when applicable. |
| HP reaches 0 | Run ends; no loot is banked. |
| RI reaches 0 | Run ends; no loot is banked. |

## Technical constraints

- Platform: terminal, keyboard-only, readable at 80×24.
- Language: Python 3.9+ with no runtime dependencies.
- Engine and terminal UI remain separate so game logic can be tested headlessly.
- A run seed makes room generation reproducible.
- Content tables live separately from the engine so additional content can be
  added without changing core rules.
