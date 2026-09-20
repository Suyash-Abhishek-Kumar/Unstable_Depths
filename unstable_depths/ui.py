"""Small, readable keyboard UI for the prototype."""

from __future__ import annotations

from .content import TYPE_ICONS
from .engine import DIRECTIONS, Run


class TerminalUI:
    def __init__(self, seed: int):
        self.run = Run(seed)

    def _bar(self, value: int, maximum: int, width: int = 10) -> str:
        filled = round(value / maximum * width)
        return "█" * filled + "░" * (width - filled)

    def _show_room(self) -> None:
        run, room = self.run, self.run.room
        print(f"\n== {room.name} ==")
        print(room.description)
        if room.kind == "loot" and not room.claimed:
            print(f"You see: a cache worth {room.loot} loot. [L]oot it.")
        elif room.kind == "anchor" and room.used:
            print("Special: the anchor's glow has faded.")
        elif room.kind == "hazard" and room.used:
            print("The immediate danger has passed, leaving a sour smell behind.")
        print("Exits: " + ", ".join(run.visible_exits()))
        seal = "ENTRANCE UNSEALED" if run.unsealed else "entrance sealed"
        print(f"HP {run.hp}/{run.max_hp}  Supplies {run.supplies}  Loot {run.loot}  Integrity {self._bar(run.integrity, run.starting_integrity)} {run.integrity}/{run.starting_integrity}")
        print(f"Rooms explored: {run.explored} · {seal} (explore 40% of the dungeon)")

    def _show_notebook(self) -> None:
        rooms = [room for room in self.run.rooms.values() if room.visited or room.position == (0, 0)]
        xs = [room.position[0] for room in rooms]
        ys = [room.position[1] for room in rooms]
        print("\n== NOTEBOOK ==  N is up; ? marks a stale, unverified room.")
        for y in range(max(ys), min(ys) - 1, -1):
            cells = []
            for x in range(min(xs), max(xs) + 1):
                position = (x, y)
                if position == self.run.position:
                    cells.append("[P]")
                elif position in self.run.rooms and self.run.rooms[position].visited:
                    room = self.run.rooms[position]
                    icon = "?" if room.stale else TYPE_ICONS[room.kind]
                    cells.append(f"[{icon}]")
                else:
                    cells.append("   ")
            print(" ".join(cells))
        print("@ entrance · . empty · + supplies · ! hazard · $ loot · * anchor · ? stale")
        if self.run.notes:
            print("Notes:")
            for position, note in sorted(self.run.notes.items()):
                print(f"  {position}: {note}")
        print(f"Auto-track: {'ON' if self.run.auto_track else 'OFF'}")

    def _messages(self) -> None:
        for message in self.run.consume_messages():
            print(f"! {message}")

    def play(self) -> None:
        print("UNSTABLE DEPTHS — v0.1 vertical slice")
        print(f"Run seed: {self.run.seed}. Reach the entrance again after it unseals.")
        self._show_room()
        while self.run.status == "active":
            self._messages()
            command = input("[N/E/S/W] Move  [L]oot [R]est [B]ook [T]rack [Note] [I]nspect [X]tract [Q]uit > ").strip().lower()
            if command in DIRECTIONS:
                self.run.move(command)
                self._messages()
                if self.run.status == "active":
                    self._show_room()
            elif command == "l":
                self.run.take_loot(); self._messages()
            elif command == "r":
                self.run.rest(); self._messages()
            elif command == "b":
                self._show_notebook()
            elif command == "t":
                self.run.auto_track = not self.run.auto_track
                print(f"Auto-track {'enabled' if self.run.auto_track else 'disabled'}.")
            elif command == "note":
                note = input("Note for this room (blank cancels): ").strip()
                if note:
                    self.run.notes[self.run.position] = note
            elif command == "i":
                self._show_room()
            elif command == "x":
                self.run.extract(); self._messages()
            elif command == "q":
                self.run.status = "quit"
            elif command:
                print("Unknown command.")
        print("\n== RUN OVER ==")
        if self.run.status == "extracted":
            print(f"Extracted. Loot banked: {self.run.loot}. Score: {self.run.score()}.")
        elif self.run.status == "dead":
            print(f"You died. Loot lost. Rooms explored: {self.run.explored}.")
        elif self.run.status == "collapsed":
            print(f"Reality collapsed. Loot lost. Rooms explored: {self.run.explored}.")
        else:
            print("Run abandoned; nothing was banked.")
