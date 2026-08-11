#!/usr/bin/env python3
"""Validate statement cards in `cards/`.

A statement card is the non-Lean contribution path: an informal claim, the
assumptions it needs, and where it came from. Anyone can write one; a
formalizer later turns it into a theorem. This script checks the front matter
so that review can be about the substance rather than the format.

Checks:
  * filename is `NNNN-slug.md` with a unique, zero-padded 4-digit id
  * required front-matter keys are present and non-empty
  * `status` is one of the allowed values
  * `lean_decl` is present iff status is `formalized`

Deliberately dependency-free (no PyYAML) so it runs anywhere.
Exit status 1 on any violation. Run: python3 scripts/validate_cards.py
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"

NAME_RE = re.compile(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
STATUSES = {"proposed", "accepted", "formalized", "rejected"}
REQUIRED = ["title", "status", "assumptions", "source", "statement"]


def parse_front_matter(text: str) -> dict[str, str] | None:
    """Minimal `--- ... ---` front-matter reader. Values are raw strings;
    list-valued keys are kept as written and only checked for non-emptiness."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end]
    out: dict[str, str] = {}
    key = None
    for line in block.split("\n"):
        if not line.strip():
            continue
        if line.startswith(("  ", "\t", "- ")) and key:
            out[key] = (out[key] + " " + line.strip().lstrip("- ")).strip()
            continue
        if ":" not in line:
            return None
        key, _, value = line.partition(":")
        key = key.strip()
        out[key] = value.strip()
    return out


def main() -> int:
    if not CARDS.exists():
        print("ok: no cards/ directory yet")
        return 0

    violations: list[str] = []
    seen_ids: dict[str, str] = {}

    paths = sorted(p for p in CARDS.glob("*.md") if p.name != "README.md")
    for path in paths:
        name_match = NAME_RE.match(path.name)
        if not name_match:
            violations.append(f"{path.name}: filename must be NNNN-kebab-slug.md")
            continue

        card_id = name_match.group(1)
        if card_id in seen_ids:
            violations.append(f"{path.name}: duplicate id {card_id} (also {seen_ids[card_id]})")
        seen_ids[card_id] = path.name

        front = parse_front_matter(path.read_text(encoding="utf-8"))
        if front is None:
            violations.append(f"{path.name}: missing or malformed `---` front matter")
            continue

        for key in REQUIRED:
            if not front.get(key):
                violations.append(f"{path.name}: missing or empty required key `{key}`")

        status = front.get("status", "")
        if status and status not in STATUSES:
            violations.append(
                f"{path.name}: status `{status}` not in {sorted(STATUSES)}"
            )

        has_decl = bool(front.get("lean_decl"))
        if status == "formalized" and not has_decl:
            violations.append(f"{path.name}: status `formalized` requires `lean_decl`")
        if status != "formalized" and has_decl:
            violations.append(
                f"{path.name}: `lean_decl` set but status is `{status}`; "
                f"set status to `formalized`"
            )

    if violations:
        print("Statement card violations:\n", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        print(f"\n{len(violations)} violation(s). See cards/README.md.", file=sys.stderr)
        return 1

    print(f"ok: {len(paths)} card(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
