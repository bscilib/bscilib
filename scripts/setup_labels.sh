#!/usr/bin/env bash
# Create BSciLib's issue labels. Idempotent: re-running updates colors/descriptions.
# Usage: ./scripts/setup_labels.sh <owner>/<repo>
set -euo pipefail

REPO="${1:?usage: setup_labels.sh <owner>/<repo>}"

# label|color|description
LABELS=(
  "good first formalization|7057ff|Scoped so a first-time contributor can finish it"
  "needs card|0e8a16|A claim that should be written up as a statement card"
  "needs assumptions|fbca04|The claim is stated but its assumptions are not pinned down"
  "formalization|1d76db|An accepted card awaiting a Lean proof"
  "assumption module|5319e7|Touches BSciLib/Assumptions and its stated empirical standing"
  "catalog-sourced|c2e0c6|Derived from a Behavioral Process Catalog entry"
  "blocked on mathlib|d93f0b|Waiting on an upstream Mathlib lemma or definition"
  "defect|b60205|Something in the library is wrong or misleading"
  "governance|bfd4f2|Working group decision required"
  "python|006b75|The executable half rather than the Lean tree"
)

for entry in "${LABELS[@]}"; do
  IFS='|' read -r name color desc <<< "$entry"
  if gh label create "$name" --repo "$REPO" --color "$color" --description "$desc" 2>/dev/null; then
    echo "created  $name"
  else
    gh label edit "$name" --repo "$REPO" --color "$color" --description "$desc" >/dev/null
    echo "updated  $name"
  fi
done

echo
echo "done: ${#LABELS[@]} labels on $REPO"
