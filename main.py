#!/usr/bin/env python3
"""Terminal entry point for the Unstable Depths v0.1 slice."""

from __future__ import annotations

import argparse
import random

from unstable_depths.ui import TerminalUI


def main() -> None:
    parser = argparse.ArgumentParser(description="Play Unstable Depths v0.1")
    parser.add_argument("--seed", type=int, help="Use a reproducible run seed")
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(1, 2**31)
    TerminalUI(seed).play()


if __name__ == "__main__":
    main()
