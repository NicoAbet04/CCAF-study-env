#!/usr/bin/env bash
# PostToolUse hook on Write|Edit (proposal §4.4). Appends every write to the
# active course's build-log.jsonl — the mtime/audit-trail source the verdict-
# freshness check relies on. PostToolUse cannot block (the tool already ran);
# this is logging only. Always exit 0.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INPUT="$(cat || true)"

FILEPATH="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
[ -z "$FILEPATH" ] && exit 0

# Only log writes into a vault or into course state (ignore incidental writes).
case "$FILEPATH" in
  *"/vaults/"*|*"/.claude/state/"*) ;;
  *) exit 0 ;;
esac

COURSE=""
for f in "$ROOT/.claude/state"/*/run.json; do
  [ -e "$f" ] || continue
  if [ "$(jq -r '.goal_active // false' "$f" 2>/dev/null)" = "true" ]; then
    COURSE="$(basename "$(dirname "$f")")"
    break
  fi
done
[ -z "$COURSE" ] && exit 0

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf '%s' "$INPUT" | jq -c \
  --arg ts "$TS" --arg fp "$FILEPATH" \
  '{timestamp: $ts, tool: (.tool_name // "unknown"), path: $fp}' \
  >> "$ROOT/.claude/state/$COURSE/build-log.jsonl" 2>/dev/null || true

exit 0
