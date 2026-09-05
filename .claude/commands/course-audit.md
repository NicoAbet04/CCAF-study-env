---
description: Run the coverage/completion audit for a course and report the
  result, without arming the completion gate.
argument-hint: <course-id, e.g. ccaf>
---

Run the deterministic audit for course **$ARGUMENTS** and report where things
stand. This is the same audit the Stop hook runs, but it **arms nothing** — use
it for "where do things stand?" checks and for re-auditing after you hand-edit
notes.

Run:

```
python3 .claude/hooks/audit.py $ARGUMENTS
```

The script:

- merges `domain-*-log.json` into `inventory.json` statuses,
- regenerates `SOURCE_INVENTORY.md` and `COVERAGE_GAPS.md` in the vault,
- checks all §4.1 completion criteria (inventory coverage, gap count,
  per-domain approval freshness, flashcard minimums, MOC links, flagged files),
- prints a JSON report `{course, complete, failures: [...], summary}`.

Show the user the report. If `complete` is false, summarize the failures
plainly; do not start fixing anything unless asked (this command only reports).
