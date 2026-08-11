#!/usr/bin/env bash
# Fail if any flagship theorem depends on an axiom beyond Lean's standard three.
#
# `lake build` already rejects `sorry`, but it says nothing about custom axioms
# that a contributor might introduce to make a proof go through. This check is
# the backstop: it reads the actual kernel-level dependencies.
set -euo pipefail

cd "$(dirname "$0")/.."

ALLOWED='propext|Classical.choice|Quot.sound'
OUT=$(lake env lean scripts/AxiomFootprint.lean)

echo "$OUT"

# Strip the allowed axiom names and the surrounding boilerplate; anything left
# that looks like an identifier is an unexpected dependency.
LEFTOVER=$(echo "$OUT" \
  | sed -E "s/'[^']*' depends on axioms: //" \
  | tr -d "[]" \
  | tr ',' '\n' \
  | sed -E 's/^[[:space:]]+|[[:space:]]+$//g' \
  | grep -vE "^($ALLOWED)$" \
  | grep -v '^$' || true)

if [ -n "$LEFTOVER" ]; then
  echo ""
  echo "FAIL: unexpected axiom dependencies:" >&2
  echo "$LEFTOVER" >&2
  exit 1
fi

echo ""
echo "ok: flagship theorems depend only on Lean's standard axioms"
