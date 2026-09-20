# Unstable Depths

> Build the odds. Enter the dark. Get out before reality comes apart.

**Unstable Depths** is a terminal roguelite dungeon crawler in which mapping is
survival gear. Rooms are generated only when you open a door, then persist for
the rest of the run. You must map the dungeon, manage supplies and health, and
return to the entrance with your loot before Reality Integrity collapses.

This repository is an early, dependency-free Python prototype. It currently
implements the **v0.1 exploration vertical slice**—the part of the game meant
to test whether blind exploration and the notebook are fun. The larger
odds-shaping, dungeon-authoring game described in the design document is not
implemented yet.

## Features today

- Seeded, lazy dungeon generation: a room is created when first entered and
  remains part of that run.
- Four-directional exploration with 2d6-based exits, loops, and a route
  guardrail before the entrance can unlock.
- HP, Supplies, loot, hazards, supply caches, and one-use Reality Anchors.
- Reality Integrity: a visible clock that drains as you travel, destabilizes
  your notebook at low levels, and ends the run at zero.
- Terminal notebook with room icons, stale-room markers, and player notes.
- Sealed entrance / extraction loop: explore enough unique rooms, then find
  your way back and bank the loot.
- Reproducible runs using a seed, plus a small automated test suite.

## Quick start

Requires Python 3.9 or newer. No packages need to be installed.

```sh
git clone <your-repository-url>
cd RougeLite
python3 main.py
```

To replay the same dungeon:

```sh
python3 main.py --seed 42
```

## How to play

Every command is entered at the prompt.

| Command | Action |
| --- | --- |
| `n`, `e`, `s`, `w` | Move north, east, south, or west |
| `l` | Take loot in the current room |
| `r` | Rest: spend 2 Supplies to recover up to 2 HP |
| `b` | View the notebook |
| `note` | Add or replace a note for the current room |
| `t` | Toggle the manual-mapping score bonus |
| `i` | Inspect the current room again |
| `x` | Extract at the entrance after it has unsealed |
| `q` | Abandon the run |

The entrance begins sealed. It unlocks after you enter four unique rooms; the
game intentionally shows only your explored-room count and the 40% target
ratio, rather than the exact threshold. Loot is only scored after extraction.

## Current balance: Playtest 1

| System | Current value |
| --- | --- |
| Starting HP / Supplies | 10 / 15 |
| Starting Reality Integrity | 300 |
| New room / known room RI cost | −8 / −2 |
| Anchor repair | +45 RI, once per anchor |
| Instability symptoms | 70% RI: notebook room becomes stale; 40% RI: a new exit may open |
| Anchor pity | Every non-anchor room adds +1 anchor weight, capped at +15 and reset by an anchor |

These numbers are deliberately provisional and will change with playtests.

## Development

Run the tests:

```sh
python3 -m unittest discover -s tests -v
```

The project keeps game rules separate from terminal rendering:

```text
main.py                    Command-line entry point
unstable_depths/engine.py  Deterministic run state and game rules
unstable_depths/content.py Starter room tables and flavor content
unstable_depths/ui.py      Terminal input and rendering
tests/                     Engine tests
```

## Roadmap

The next focus is playtesting and improving the notebook/exploration loop. The
design then expands toward creator-configured odds, contracts, additional
random devices, combat, reality-bending artifacts, themes, and eventually
two-player creator/explorer modes.

Project design is split into three living documents:

- [GDD](docs/GDD.md): the current game and immediate design target.
- [Roadmap](docs/ROADMAP.md): planned and exploratory future work.
- [Design log](docs/DESIGN_LOG.md): decisions and playtest-driven changes.
- [Full original GDD](docs/UNSTABLE%20DEPTHS%20-%20Game%20Design%20Document.md):
  the complete, detailed design reference.

## Status

Pre-alpha prototype. Expect incomplete systems and balance changes.
