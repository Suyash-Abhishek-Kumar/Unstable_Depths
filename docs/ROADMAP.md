# Unstable Depths — Roadmap

> **Living document · Last updated September 2026**
>
> This is an ordered set of intentions, not a release promise. Scope is driven
> by playtests, so milestones may be cut, combined, or reordered.

## Current focus: validate the vertical slice

The immediate work is not feature expansion. First, play enough v0.1 runs to
learn whether blind exploration, notebook use, and Integrity create interesting
decisions. Track distance reached, extraction rate, supplies, anchor timing,
death cause, and whether players use the notebook voluntarily.

Near-term improvements:

- Tighten room text and notebook usability.
- Add a lightweight headless bot simulation for generator softlocks and balance.
- Finish true manual notebook placement, rather than only its scoring toggle.
- Tune one variable per playtest and record the outcome in the design log.

## Planned milestones

| Milestone | Intent | Exit criterion |
| --- | --- | --- |
| M0 | Engine skeleton, deterministic RNG, data loading, tests | Headless engine tests pass. |
| M1 | v0.1 exploration slice | Twenty playable runs. |
| M2 | Playtest and notebook pass | Players make real push/return/map decisions. |
| M3 | Odds-only generation and contracts | Generation is entertaining on its own. |
| M3.5 | Minimal turn-based combat | Fights create decisions, not chores. |
| M4 | More random devices and device state | Each device feels mechanically distinct. |
| M5 | Reality-bending artifacts and reforges | Bends are chaotic but fair. |
| M6 | Meta-progression and first themes | Replay variety grows without raw power creep. |
| M7 | Async two-player Architect mode | One player can author and another explore a dungeon file. |
| M8 | Larger maps and layout algorithms | Big maps remain readable and safe. |
| M9 | Hot-seat Warden and Patron relations | Relations feel distinct and respect guardrails. |

## Future systems under consideration

### Odds-authoring generation

The central long-term concept is that a creator controls probabilities, never
specific outcomes. A generation budget prices safer odds, more valuable rooms,
chaos, rerolls, masks, and devices. Early devices are 2d6, weighted tables, and
coin streaks; later candidates include wheels, decks, token bags, tile draws,
drafts, and Plinko.

### Contracts and two-player roles

Contracts provide preset dungeons with visible danger and reward ratings.
Two-player mode begins asynchronously: an Architect creates a dungeon file for
an Explorer. Live Warden and Patron roles are deferred until hot-seat play can
validate their Favor and intervention systems.

### Combat

Combat, if added, is a simple 1v1 turn-based encounter: Attack, Guard, Item,
and Flee. Enemies reveal intent. It must use the same HP and Supplies economy
as exploration rather than become a separate game.

### Reality bending

Rare artifacts may add, remove, swap, reveal, or reshape rooms at an Integrity
cost. Larger bends would add notebook-page and HP costs. Moderate and larger
bends may use an accessible timing or stepped-input challenge. This system is
deferred until normal exploration is stable.

### Themes and progression

The first planned themes are Medieval (baseline), Arcane (content-first), and
Candyworld (one Sugar meter coupled to Supplies). Meta-progression should unlock
new choices and content, primarily as sidegrades rather than raw power.

## Guardrails for all future work

- Never allow an impossible threshold or forced dead-end death.
- Preserve the engine/UI separation and deterministic replayability.
- Do not add a feature unless it produces a felt exploration consequence.
- Prefer data-driven content to one-off code branches.
- Add complexity only after the previous layer survives playtesting.
