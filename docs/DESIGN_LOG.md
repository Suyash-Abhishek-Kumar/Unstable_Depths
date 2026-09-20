# Unstable Depths — Design Log

> **Living document · Last updated September 2026**
>
> This document records why decisions changed. It is not a specification; see
> [GDD.md](GDD.md) for the current build target.

## Playtest 1 — v0.1 slice

Two designer runs tested blind exploration, the notebook, anchors, and Reality
Integrity.

| Finding | Reading | Change |
| --- | --- | --- |
| The first anchor appeared too late and one run nearly collapsed. | Anchors are the only repair source, so anchor absence was deciding runs more than choices were. | Added the capped anchor-pity rule. |
| Roaming, looting, exploring, and notebook use felt good. | The core loop is worth testing further before expanding scope. | No feature change. |
| The player stayed close to the entrance out of fear of running out of RI. | The clock created caution but not an attractive gamble; baseline costs also left no future budget for bends. | Changed RI from `100 / −4 new / −1 known` to `300 / −8 new / −2 known`; anchors changed from `+15` to `+45`. |

### Rejected alternative

Increasing starting RI to 300 or 500 while retaining `−4 / −1` decay was
rejected. It would make ordinary exploration consume too little of the pool,
leaving Integrity irrelevant and making instability symptoms rare.

### Next experiments

1. Replay the new values and check whether tier-one instability appears in
   longer runs without causing players to hug the start.
2. If players still stay near the entrance, test loot value increasing with
   distance from it.
3. If RI becomes irrelevant, lower starting RI before changing the per-move
   costs again.

## Established design decisions

| Decision | Reason |
| --- | --- |
| Control odds, not outcomes. | Prevent free selection of safe results. |
| Use blind, lazy generation for solo runs. | Mapping matters only if the explorer does not already know the layout. |
| Store rooms after generation. | The notebook needs stable information to be meaningful. |
| Use Integrity as the clock. | It gives runs a reason to end and connects danger to map reliability. |
| Use an extraction threshold at the entrance. | Every run requires exploration without requiring a boss kill. |
| Show progress ratio, not exact threshold. | Preserve blind exploration while communicating the objective. |
| Use a fixed 40% threshold ratio. | Creators can eventually control depth with room count without changing the core rule. |
| Allow found exits in a later version. | A discovered exit is a lucky break; the entrance lock exists only to prevent immediate retreat. |
| Keep failure rewards separate from stored progress. | A failed run may earn a partial future currency payout, but must never take already banked currency. |
| No sanity meter. | Keep the slice focused on HP, Supplies, and Integrity. |
| Defer combat until generation is fun. | Exploration and generation are the larger design risks. |
| Start with hot-seat before networking. | It is the fastest way to validate live relation systems. |
| Cut Blockworld for now. | Player-editable walls would complicate maps, thresholds, and guardrails too early. |

## Open questions worth revisiting later

- What grants the rare, item-free latent reality-bending ability?
- What timing windows and non-real-time accessibility option should larger bends use?
- What should the default found-exit frequency be?
- What exact Sugar rules make Candyworld interesting rather than busy?
- Which Arcane hazards and spell items best support the reality-bending theme?
- What is the final bend-cost ladder once normal RI use is proven?
