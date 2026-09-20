"""Pure game logic for the v0.1 blind exploration slice."""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Dict, Optional, Tuple

from .content import ROOM_CONTENT, ROOM_WEIGHTS

Position = Tuple[int, int]
DIRECTIONS: Dict[str, Position] = {"n": (0, 1), "e": (1, 0), "s": (0, -1), "w": (-1, 0)}
OPPOSITE = {"n": "s", "s": "n", "e": "w", "w": "e"}
LEFT = {"n": "w", "w": "s", "s": "e", "e": "n"}
RIGHT = {value: key for key, value in LEFT.items()}


@dataclass
class Room:
    position: Position
    kind: str
    name: str
    description: str
    exits: set[str] = field(default_factory=set)
    visited: bool = False
    stale: bool = False
    loot: int = 0
    claimed: bool = False
    used: bool = False


class Run:
    """A deterministic, lazy-generated dungeon run with no UI dependency."""

    planned_rooms = 10
    threshold_ratio = 0.4
    threshold = 4
    starting_integrity = 300
    new_room_integrity_cost = 8
    known_room_integrity_cost = 2
    anchor_repair = 45
    max_anchor_pity = 15

    def __init__(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)
        self.hp = 10
        self.max_hp = 10
        self.supplies = 15
        self.loot = 0
        self.integrity = self.starting_integrity
        # Every non-anchor room raises the next anchor's table weight by one.
        # This is intentionally generator state, not a player-visible resource.
        self.anchor_pity = 0
        self.position: Position = (0, 0)
        self.explored = 0
        self.unsealed = False
        self.status = "active"  # active, extracted, dead, collapsed, quit
        self.messages: list[str] = []
        self.auto_track = True
        self.notes: dict[Position, str] = {}
        self.rooms: dict[Position, Room] = {
            (0, 0): Room((0, 0), "entrance", "The Sealed Entrance", "The stair behind you is sealed by cold, unmoving stone.", {"n", "e"}, True)
        }

    @property
    def room(self) -> Room:
        return self.rooms[self.position]

    def visible_exits(self) -> list[str]:
        return sorted(direction.upper() for direction in self.room.exits)

    def weighted_kind(self) -> str:
        weights = dict(ROOM_WEIGHTS)
        weights["anchor"] += self.anchor_pity
        roll = self.rng.randrange(sum(weights.values()))
        for kind, weight in weights.items():
            if roll < weight:
                return kind
            roll -= weight
        return "empty"

    def _roll_exits(self, entry: str) -> set[str]:
        """Resolve 2d6 exits relative to the direction the player entered from."""
        total = self.rng.randint(1, 6) + self.rng.randint(1, 6)
        forward, left, right, back = entry, LEFT[entry], RIGHT[entry], OPPOSITE[entry]
        if total == 2:
            exits = {back}
        elif total <= 4:
            exits = {back, left if self.rng.random() < 0.5 else right}
        elif total <= 6:
            exits = {back, forward}
        elif total == 7:
            exits = {back, forward, left if self.rng.random() < 0.5 else right}
        elif total <= 9:
            exits = {back, left, right}
        else:
            exits = {back, forward, left, right}
        # Lifeline: while the lock remains, a new room always offers a fresh way onward.
        if self.explored < self.threshold:
            exits.add(forward)
        return exits

    def _make_room(self, position: Position, entry: str) -> Room:
        kind = self.weighted_kind()
        if kind == "anchor":
            self.anchor_pity = 0
        else:
            self.anchor_pity = min(self.max_anchor_pity, self.anchor_pity + 1)
        name, description = self.rng.choice(ROOM_CONTENT[kind])
        room = Room(position, kind, name, description, self._roll_exits(entry))
        if kind == "loot":
            room.loot = self.rng.randint(2, 5)
        self.rooms[position] = room
        return room

    def _enter(self, room: Room, new: bool) -> None:
        self.position = room.position
        if new:
            room.visited = True
            self.explored += 1
            self._change_integrity(-self.new_room_integrity_cost, "You press into uncharted space. Integrity -8.")
            self._resolve_room(room)
            if self.explored >= self.threshold and not self.unsealed:
                self.unsealed = True
                self.messages.append("THE ENTRANCE UNSEALS. A distant mechanism answers with a heavy click.")
        else:
            room.stale = False
            self._change_integrity(-self.known_room_integrity_cost, "You retrace a known route. Integrity -2.")
        self._integrity_symptoms(new)

    def _resolve_room(self, room: Room) -> None:
        if room.kind == "supplies":
            gain = self.rng.randint(3, 6)
            self.supplies += gain
            room.used = True
            self.messages.append(f"You find usable provisions. Supplies +{gain}.")
        elif room.kind == "hazard":
            damage = self.rng.randint(1, 3)
            self.hp -= damage
            room.used = True
            self.messages.append(f"The room bites back. HP -{damage}.")
            if self.hp <= 0:
                self.status = "dead"
                self.messages.append("You collapse in the dark.")
        elif room.kind == "anchor":
            repaired = min(self.anchor_repair, self.starting_integrity - self.integrity)
            self.integrity += repaired
            room.used = True
            self.messages.append(f"The anchor steadies the world. Integrity +{repaired}.")

    def _change_integrity(self, amount: int, message: Optional[str] = None) -> None:
        self.integrity = max(0, min(self.starting_integrity, self.integrity + amount))
        if message:
            self.messages.append(message)
        if self.integrity == 0 and self.status == "active":
            self.status = "collapsed"
            self.messages.append("Reality gives way. The dungeon falls out from under you.")

    def _integrity_symptoms(self, entered_new: bool) -> None:
        visited = [room for room in self.rooms.values() if room.visited and room.position != self.position and room.kind != "entrance"]
        if self.integrity <= self.starting_integrity * 0.70 and visited:
            target = self.rng.choice(visited)
            if not target.stale:
                target.stale = True
                self.messages.append("Your notebook flickers: one earlier room is now unverified.")
        if self.integrity <= self.starting_integrity * 0.40 and not entered_new and self.status == "active":
            # Add an unexplored branch rather than remove a connection; this changes the map without softlocking it.
            candidates = [d for d in DIRECTIONS if d not in self.room.exits]
            if candidates:
                direction = self.rng.choice(candidates)
                self.room.exits.add(direction)
                self.messages.append(f"Stone scrapes somewhere nearby. A new exit opens to the {direction.upper()}.")

    def move(self, direction: str) -> bool:
        direction = direction.lower()
        if self.status != "active":
            return False
        if direction not in self.room.exits:
            self.messages.append("There is no exit in that direction.")
            return False
        dx, dy = DIRECTIONS[direction]
        destination = (self.position[0] + dx, self.position[1] + dy)
        if self.supplies > 0:
            self.supplies -= 1
        else:
            self.hp -= 1
            self.messages.append("With no supplies left, the march costs 1 HP.")
            if self.hp <= 0:
                self.status = "dead"
                return False
        if destination in self.rooms:
            target = self.rooms[destination]
            target.exits.add(OPPOSITE[direction])
            self._enter(target, not target.visited and target.kind != "entrance")
        else:
            target = self._make_room(destination, direction)
            self._enter(target, True)
        return True

    def take_loot(self) -> None:
        room = self.room
        if room.kind != "loot" or room.claimed:
            self.messages.append("There is no loot left to take here.")
            return
        room.claimed = True
        self.loot += room.loot
        self.messages.append(f"You take {room.loot} loot. It only counts if you escape.")

    def rest(self) -> None:
        if self.status != "active":
            return
        if self.supplies < 2:
            self.messages.append("You need 2 Supplies to rest.")
            return
        self.supplies -= 2
        healed = min(2, self.max_hp - self.hp)
        self.hp += healed
        self._change_integrity(-self.known_room_integrity_cost, f"You rest. HP +{healed}; Integrity -2.")
        self._integrity_symptoms(False)

    def extract(self) -> bool:
        if self.position != (0, 0):
            self.messages.append("Extraction is only possible at the entrance.")
            return False
        if not self.unsealed:
            self.messages.append("The entrance is still sealed. Explore further.")
            return False
        self.status = "extracted"
        self.messages.append("You climb into daylight with what you can carry.")
        return True

    def score(self) -> int:
        if self.status != "extracted":
            return 0
        return self.loot * self.explored + (2 if not self.auto_track else 0)

    def consume_messages(self) -> list[str]:
        messages, self.messages = self.messages, []
        return messages
