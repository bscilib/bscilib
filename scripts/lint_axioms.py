#!/usr/bin/env python3
"""Enforce BSciLib's two structural policies on the Lean tree.

1. No `sorry` anywhere. An unfinished proof must not enter the library; open
   claims live in `cards/` as statement cards instead.
2. No `axiom` declaration outside `BSciLib/Assumptions/`. Assumptions are
   allowed, but only where they are visible, named, and documented with their
   empirical standing. An axiom smuggled into a results file would let the
   library assert an empirical claim, which is the one thing it must never do.

Exit status 1 on any violation. Run: python3 scripts/lint_axioms.py
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEAN_ROOT = ROOT / "BSciLib"
ASSUMPTIONS_DIR = LEAN_ROOT / "Assumptions"

# Match declarations at the start of a line, so the words are harmless in prose.
AXIOM_RE = re.compile(r"^\s*axiom\s", re.MULTILINE)
SORRY_RE = re.compile(r"(?<![A-Za-z_])sorry(?![A-Za-z_])")

# Docstrings and comments are prose, not code; strip them before scanning.
BLOCK_COMMENT_RE = re.compile(r"/-.*?-/", re.DOTALL)
LINE_COMMENT_RE = re.compile(r"--[^\n]*")


def strip_comments(text: str) -> str:
    text = BLOCK_COMMENT_RE.sub(lambda m: "\n" * m.group().count("\n"), text)
    return LINE_COMMENT_RE.sub("", text)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def main() -> int:
    violations: list[str] = []

    lean_files = sorted(LEAN_ROOT.rglob("*.lean")) + [ROOT / "BSciLib.lean"]
    for path in lean_files:
        if not path.exists():
            continue
        source = strip_comments(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)

        for match in SORRY_RE.finditer(source):
            violations.append(
                f"{rel}:{line_of(source, match.start())}: `sorry` in the library; "
                f"move the open claim to cards/ instead"
            )

        if ASSUMPTIONS_DIR not in path.parents:
            for match in AXIOM_RE.finditer(source):
                violations.append(
                    f"{rel}:{line_of(source, match.start())}: `axiom` outside "
                    f"BSciLib/Assumptions/; assumptions must be declared, named, "
                    f"and documented there"
                )

    if violations:
        print("BSciLib policy violations:\n", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        print(f"\n{len(violations)} violation(s). See docs/assumptions.md.", file=sys.stderr)
        return 1

    print(f"ok: {len(lean_files)} Lean file(s) clean (no sorry, no stray axiom)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
