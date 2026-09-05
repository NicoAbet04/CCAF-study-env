#!/usr/bin/env bash
# Stop-hook completion gate (proposal §4.3). Registered on the `Stop` event in
# .claude/settings.json. Armed only while some course has goal_active=true.
#
# Confirmed semantics (§0.3): exit 2 prevents Claude from stopping and feeds the
# block reason back so it keeps working; the reason is taken from a JSON
# {"decision":"block","reason":...} object or from stderr. The audit runs INSIDE
# this hook, so the coverage phase cannot be skipped.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_GLOB="$ROOT/.claude/state"/*/run.json

# Hook input JSON arrives on stdin (includes stop_hook_active). Read but don't
# require it; the cycle counter is the hard loop cap (§4.5), per docs guidance.
INPUT="$(cat || true)"
STOP_HOOK_ACTIVE="$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || echo false)"

# Find the active course (first run.json with goal_active=true).
COURSE=""
RUNFILE=""
for f in $STATE_GLOB; do
  [ -e "$f" ] || continue
  if [ "$(jq -r '.goal_active // false' "$f" 2>/dev/null)" = "true" ]; then
    RUNFILE="$f"
    COURSE="$(jq -r '.course // empty' "$f")"
    [ -z "$COURSE" ] && COURSE="$(basename "$(dirname "$f")")"
    break
  fi
done

# Gate is armed only during a build.
[ -z "$COURSE" ] && exit 0

CYCLE="$(jq -r '.cycle // 0' "$RUNFILE")"
MAX="$(jq -r '.max_cycles // 3' "$RUNFILE")"

# Safety valve: after max_cycles, disarm and escalate to the user (§4.5).
if [ "$CYCLE" -ge "$MAX" ]; then
  tmp="$(mktemp)"
  jq '.goal_active = false' "$RUNFILE" > "$tmp" && mv "$tmp" "$RUNFILE"
  printf '%s\n' "{\"systemMessage\": \"Gate DISARMED after $CYCLE cycle(s) for '$COURSE' — unresolved items are listed in the vault's COVERAGE_GAPS.md / FLAGGED.md; escalating to the user.\"}"
  exit 0
fi

# Run the deterministic audit (merges logs, regenerates views, checks §4.1).
REPORT="$(python3 "$ROOT/.claude/hooks/audit.py" "$COURSE")"
COMPLETE="$(printf '%s' "$REPORT" | jq -r '.complete')"

if [ "$COMPLETE" = "true" ]; then
  exit 0   # allow stop — build complete
fi

# Incomplete: bump the cycle counter and block the stop with the failure list.
tmp="$(mktemp)"
jq '.cycle += 1' "$RUNFILE" > "$tmp" && mv "$tmp" "$RUNFILE"

REASON="$(printf '%s' "$REPORT" | jq -r '"Build gate: " + (.failures | length | tostring) + " unmet criteria — " + (.failures | join("; "))')"
printf '%s\n' "$(jq -n --arg r "$REASON" '{decision: "block", reason: $r}')"
exit 2
