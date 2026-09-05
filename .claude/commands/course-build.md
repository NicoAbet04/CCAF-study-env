---
description: Build or resume a course's study vault (inventory → plan → domain
  dispatch → evaluate → gap-fill) under the completion gate.
argument-hint: <course-id, e.g. ccaf>
---

Build or resume the study vault for course **$ARGUMENTS**. You are the
orchestrator — the main session, not a subagent (you need plan mode,
AskUserQuestion, and the ability to spawn agents; the Stop-hook gate binds to
this session). Read `CLAUDE.md` for the ground rules, conventions, and build
state model before starting.

## Phase 0 — resolve manifest and inventory (STOP for confirmation)

1. Read `courses/$ARGUMENTS/course.yaml`.
2. **Resolve it into machine state** so the deterministic audit never parses
   YAML (there is no `pyyaml` here):
   - Write `.claude/state/$ARGUMENTS/run.json`:
     `{course, goal_active: true, cycle: 0, max_cycles: <max_gap_fill_cycles>,
       last_audit: null, vault: <vault>, domains: [{id, name, flashcards_min}, …]}`.
     Setting `goal_active: true` **arms the Stop gate**.
   - Build `.claude/state/$ARGUMENTS/inventory.json` by walking the manifest's
     `sources` (PRIMARY tier only), keeping files whose extension is in
     `content_extensions`, applying every `exclude` pattern **at any depth**.
     Each entry: `{path, status: "pending", claimed_by: []}`.
3. As a belt-and-braces layer, also run the built-in `/goal` with a
   transcript-checkable phrasing (e.g. "the last audit reported 0 gaps and all
   domains approved"). The Stop hook — not `/goal` — is the real enforcement.
4. Verify the *Spaced Repetition* Obsidian plugin is installed in the vault
   (§9.1); note it if missing.
5. Report the file count and the exclusion list, then **STOP for the user to
   confirm the inventory** (this checkpoint is load-bearing — it is where
   `.trees/` and nested `.venv` junk would otherwise sneak in).

## Phase 1 — plan the domain assignment (plan mode)

Enter plan mode. Propose the domain assignment: files AND section ranges for
multi-domain files like `Claude_API.md` (a single file may be claimed by several
domains — this is not a partition), driven by each domain's blueprint task list.
Populate the blueprint `tasks` from the official exam guide's task statements
(Knowledge-of / Skills-in bullets); use the community exam repo's task index to
fill the domains the PDF copy truncates. Flag ambiguities. Get approval.

## Phase 2 — dispatch builders

Dispatch one `domain-builder` per blueprint domain (parallel is fine). Give each
the course name, its domain entry, its assignment list (with section ranges),
and the vault path.

## Phase 3 — evaluate and repair (per note)

For each returned note, dispatch `study-evaluator`. It is read-only and returns
a JSON verdict — **you persist it** to `.claude/state/$ARGUMENTS/eval-domain-N.json`.
On `reject`: repair-dispatch that domain's `domain-builder` with the fix list
appended and instructions to **edit, not rewrite**. Re-evaluate after repair
(a repair invalidates the old approval).

## Phase 4 — attempt to stop (the gate runs)

Attempt to end your turn. The Stop hook runs the deterministic audit
(`.claude/hooks/audit.py`): it merges the domain logs into `inventory.json`,
regenerates `SOURCE_INVENTORY.md` and `COVERAGE_GAPS.md`, counts flashcards,
checks MOC links and verdict freshness. If it blocks, fix **exactly** what its
reason lists, then attempt to stop again. After `max_cycles` failed cycles the
gate disarms itself and escalates unresolved items via `COVERAGE_GAPS.md` /
`FLAGGED.md`.

## User spot-check (before declaring done)

After the first full approval set, present ONE domain note (the highest-weight
domain) plus the gap and flag lists for human review before declaring the build
complete.
