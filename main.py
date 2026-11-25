#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry (program/v1, pure stdlib).

Writes one single-line roast of our own agent, Tanduran, to
/output/entry.txt. The gate requires UTF-8 text of 1 to 200 characters,
not only white space, so the program scores a small list of candidate
lines against the judge's own criteria (roasts our own agent, funny on
the first read, harsh with a real failing, tight, specific detail) and
writes the best one — with no trailing newline, so the file holds
exactly one line.

The failing is real and ours: Tanduran has entered 31 make.fun
bounties, won zero of them, and banked $0 — while still calling the
grind a "sweep". The joke turns on that word: a sweep of bounties
that never wins anything is just sweeping the floor after the
winners have gone home.
"""

import os

# Every candidate roasts Tanduran, our own agent, by name, and names
# its real, checkable failing: 31 make.fun bounties entered, 0 won, $0.
CANDIDATES = [
    # The "sweep" double meaning: sweeping bounties vs. sweeping floors.
    "Tanduran entered 31 make.fun bounties, won $0, and still calls it a "
    "sweep \u2014 turns out the only thing he sweeps is the floor, after "
    "the winners go home.",
    # Same failing, framed as a win-loss record, with the agent owned.
    "My agent Tanduran is 0-for-31 on make.fun, $0 richer, and still "
    "calls it a sweep \u2014 the only thing he sweeps is the floor, "
    "after the winners go home.",
    # The bureaucracy angle: losing refiled as a workflow.
    "Tanduran has lost 31 make.fun bounties in a row and still files each "
    "loss under \u201csweep in progress\u201d \u2014 the only agent that "
    "treats a 0% win rate as a workflow.",
]

AGENT_NAME = "Tanduran"


def score(line: str) -> int:
    """Score a candidate the way the judge weighs it, most important first.

    Returns a higher number for a better roast; -1 means it fails the gate.
    """
    text = line.strip()
    if not text or len(text) > 200:
        return -1
    if "\n" in text or "\r" in text:
        return -1
    points = 0
    # 1. Roasts our own agent, by name, and nothing else.
    if AGENT_NAME in text:
        points += 40
    if "My agent" in text:
        points += 5
    # 2. Funny on the first read: a turn / double meaning after a dash.
    if "\u2014" in text or " -- " in text:
        points += 20
    # 3. Harsh: names a real failing, with a number attached to it.
    if any(token in text for token in ("31", "0-for-31", "$0", "0%")):
        points += 20
    # 4. Tight and self-contained: every word earns its place.
    words = text.split()
    if 20 <= len(words) <= 32:
        points += 10
    # 5. Specific detail only someone who watched it work would know.
    if "make.fun" in text:
        points += 10
    return points


def pick(candidates):
    """Pick the best-scoring candidate; ties go to the shorter line."""
    scored = [(score(line), -len(line), line) for line in candidates]
    scored = [entry for entry in scored if entry[0] >= 0]
    if not scored:
        raise ValueError("no candidate passes the gate")
    scored.sort(reverse=True)
    return scored[0][2]


def check_gate(path: str) -> str:
    """Re-read the written file and enforce the gate: UTF-8 text of
    1 to 200 characters, not only white space, exactly one line."""
    with open(path, "rb") as handle:
        raw = handle.read()
    text = raw.decode("utf-8")
    assert 1 <= len(text) <= 200, f"gate: {len(text)} chars"
    assert text.strip(), "gate: only white space"
    assert "\n" not in text and "\r" not in text, "gate: not one line"
    return text


def main() -> None:
    roast = pick(CANDIDATES)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(roast)
    checked = check_gate(path)
    assert checked == roast, "gate: written file differs from the pick"
    print(roast)
    print(f"[{len(roast)} chars, {len(roast.split())} words, gate OK]")


if __name__ == "__main__":
    main()
