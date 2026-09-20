"""Data-first starter content for the Medieval v0.1 slice."""

ROOM_WEIGHTS = {
    "empty": 40,
    "supplies": 20,
    "hazard": 20,
    "loot": 15,
    "anchor": 5,
}

ROOM_CONTENT = {
    "empty": [
        ("Damp Cellar", "Water pools between rotting barrels. The air tastes of iron."),
        ("Quiet Nook", "A shallow alcove shelters a nest of long-dead candles."),
        ("Stone Passage", "Old mortar flakes from the walls in small, patient drifts."),
    ],
    "supplies": [
        ("Provision Store", "A waxed crate holds travel bread and a half-full canteen."),
        ("Hunter's Cache", "Someone left a bundle of dry rations beneath a loose flagstone."),
    ],
    "hazard": [
        ("Bone Hall", "Loose ceiling stones shift above a floor bright with pale splinters."),
        ("Flooded Step", "Black water hides a jagged run of submerged masonry."),
    ],
    "loot": [
        ("Forgotten Strongbox", "A small iron chest waits beneath a cloth gone green with mildew."),
        ("Tax Collector's Room", "Coin glints under a collapsed writing desk."),
    ],
    "anchor": [
        ("Glowing Alcove", "A steady blue seam in the wall makes the air feel briefly solid."),
        ("Surveyor's Shrine", "A brass compass hums on a stone plinth."),
    ],
}

TYPE_ICONS = {"entrance": "@", "empty": ".", "supplies": "+", "hazard": "!", "loot": "$", "anchor": "*"}
