#!/usr/bin/env bash
# SubagentStop hook (proposal §4.4). Settings-level so it sees agent_type/agent_id.
# Appends a mechanical record that a subagent actually ran and finished, to the
# active course's subagent-events.jsonl. The audit uses this to trust that a
# domain-builder ran before its log, and that an evaluator ran after a note's
# last edit. It NEVER blocks (no exit 2 here) — retry logic lives in the
# orchestrator + Stop gate, not this layer.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INPUT="$(cat || true)"

# Route the record to whichever course is currently building.
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
  --arg ts "$TS" \
  '{timestamp: $ts,
    agent_type: (.agent_type // "unknown"),
    agent_id: (.agent_id // "unknown"),
    transcript_path: (.transcript_path // null)}' \
  >> "$ROOT/.claude/state/$COURSE/subagent-events.jsonl" 2>/dev/null || true

exit 0
