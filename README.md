# Unstable Depths

A dependency-free Python terminal prototype of the v0.1 vertical slice from the
game design document. It focuses on blind exploration, hand mapping, Reality
Integrity, and extraction—not the later creator/odds systems.

## Run

```sh
python3 main.py
```

Optional deterministic seed:

```sh
python3 main.py --seed 42
```

## Test

```sh
python3 -m unittest discover -s tests -v
```

## Controls

`n/e/s/w` move · `l` loot · `r` rest · `b` notebook · `t` toggle auto-map ·
`note` add a note · `i` inspect · `x` extract · `q` quit.

The entrance unlocks after four unique non-entrance rooms have been entered.
The displayed progress deliberately gives the ratio and explored count, not the
hidden exact threshold. The current Playtest 1 balance starts at 300 Reality
Integrity: new rooms cost 8, known rooms cost 2, and anchors restore 45. Each
non-anchor room slightly raises the chance that the next generated room is an
anchor (up to a capped pity bonus).
