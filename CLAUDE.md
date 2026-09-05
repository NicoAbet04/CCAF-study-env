# study-env — a reusable courseware environment

This repo turns course/cert source material into an Obsidian study vault. A
**course is one manifest file** (`courses/<id>/course.yaml`); everything else —
agents, hooks, commands, the loop body — is shared and parameterized by it.
First tenant: **CCAF** (Claude Certified Architect – Foundations).

The source repos under `~/Projects/PyCharmProjects/` are **read-only sources**.
Never write to them. All generated output goes to the course's vault
(`vaults/<id>/`) and machine state (`.claude/state/<id>/`).

---

## Ground rules for generated content (A.1 — non-negotiable)

These bind the `domain-builder` subagent and any note writing:

1. **Faithful to sources.** Every claim in a note (and every flashcard) must be
   traceable to an assigned source file. Do not blend in facts the sources do
   not support.
2. **Condensed, never pasted.** Restate in your own words. Never copy source
   prose verbatim. Fix clumsy phrasing rather than preserving it.
3. **Training knowledge is quarantined.** If you know something relevant that
   the sources lack, put it in a clearly marked `> [!note] Beyond the sources
   (unverified)` callout — never in the main body and never in a flashcard.
4. **Nothing is silently dropped.** A source file you cannot process is logged
   as `failed` with a reason and surfaced in `FLAGGED.md` — never omitted
   quietly.
5. **Exam-intel is the one curated exception** and still obeys rule 1: teammate-
   reported exam topics enter `notes/exam-intel.md` only after being verified
   against an official doc page, each entry citing that page. In notes they
   render in a distinct `> [!tip] 📌 Reported on the exam` callout.

## Source tiers (§0.4)

- **Primary** — inventoried, coverage-gated, condensed into notes (the two
  course repos, the official exam guide, `exam-intel.md`, `module-05-mcp.md`).
- **Reference** — linked from notes and citable in gap-fill, never inventoried
  (Claude Cookbooks, official docs).
- **Cross-check** — compared against our output *after* generation, never
  ingested (CCA Playbook Anki decks — no license, must not be condensed in).
- **Practice** — quizzes/mocks/labs, **quarantined from notes and flashcards
  entirely**; they only feed `Weak Areas.md`. Studying mock answers inflates
  practice scores and destroys the Weak-Areas signal.

---

## Vault conventions (A.4)

Every domain note is `<N> - <Domain Name>.md` in the vault and contains:

- **YAML frontmatter** with `tags` and `domain`.
- Prose **condensed in your own words**, structured around the domain's
  **blueprint task list** (what the exam tests), not the source files' order.
- **`[[wikilinks]]`** to related concepts; every term of art linked to
  `[[Glossary]]` on first use.
- **Exactly one mermaid diagram** (`graph TD` or `mindmap`) of the domain's
  sub-topics, with node labels understandable on their own.
- At least `flashcards_min` **spaced-repetition flashcards** in the Obsidian
  *Spaced Repetition* plugin format — `Question` / `?` / `Answer` on their own
  lines — tagged `#flashcards/domain-N`. Cards skew toward **scenario
  judgment**, not recall.
- A closing **"Traps & distractors"** section covering **every task in the
  domain, at least one trap each** (raised from "official anti-patterns only"
  to close a real gap found by inspection, 2026-09-05): ground each trap in an
  official ANTI-PATTERN bullet, a wrong answer implied by a task's own
  knowledge/skills bullets, or a doc-verified exam-intel entry — never in a
  mock question, which stays quarantined.

Vault-wide files (written only by the orchestrator / audit, never by a builder):
`SOURCE_INVENTORY.md`, `COVERAGE_GAPS.md`, `Glossary.md`, `<Course> MOC.md`,
`Weak Areas.md`, `FLAGGED.md`.

### Writing style contract (§8.2)

Plain, natural prose in complete sentences; short sentences over subclause
chains; one idea per paragraph; define every term of art on first use; prefer
"you" and active voice; no telegram-style bullet fragments — a bullet may be
short but must read as a sentence a person would say. A factually perfect note
with laborious prose is a defect, not a pass.

---

## Build state model (§4)

State lives in `.claude/state/<course>/` as plain JSON — it survives compaction,
restarts, and resumed sessions. **The JSON is authoritative; the Markdown views
in the vault (`SOURCE_INVENTORY.md`, `COVERAGE_GAPS.md`) are generated from it.**

```
.claude/state/<course>/
├── run.json              # resolved runtime config + gate state (see below)
├── inventory.json        # [{path, status: pending|covered|logged-irrelevant, claimed_by: [ids]}]
├── domain-<N>-log.json   # written by each domain-builder
├── eval-domain-<N>.json  # verdicts (persisted by the ORCHESTRATOR from evaluator summaries)
├── subagent-events.jsonl # appended by the SubagentStop hook (mechanical record)
└── build-log.jsonl       # appended by the PostToolUse hook (every write, timestamped)
```

**`run.json` is resolved from `course.yaml` by `/course-build` Phase 0** so the
deterministic audit never has to parse YAML (there is no `pyyaml` here). Shape:

```json
{
  "course": "ccaf",
  "goal_active": false,
  "cycle": 0,
  "max_cycles": 3,
  "last_audit": null,
  "vault": "vaults/ccaf",
  "domains": [{"id": 1, "name": "...", "flashcards_min": 12}, ...]
}
```

`goal_active: true` **arms the Stop gate**. Only then does the Stop hook run the
audit and block completion until every §4.1 criterion holds (or `cycle`
reaches `max_cycles`, when the gate disarms itself and escalates to the user).

## Completion criteria (§4.1 — all machine-checked by the audit)

A build is **done** only when all hold:

1. `inventory.json` exists and every entry is `covered` or `logged-irrelevant`.
2. `COVERAGE_GAPS.md` was regenerated after the last content write and its gap
   count is 0.
3. Every blueprint domain has an evaluator verdict `approve`, timestamped
   **after** that note's last modification (a repair invalidates old approval).
4. Every domain note meets its `flashcards_min` (counted by regex, not
   self-reported).
5. `Glossary.md`, `<Course> MOC.md`, and `Weak Areas.md` exist; every domain
   note is linked from the MOC.
6. No domain-log entry has status `failed` without a matching `FLAGGED.md`
   entry.

The audit (`.claude/hooks/audit.py`) is the single implementation of these
checks; the Stop hook and `/course-audit` both call it. It is deterministic —
never let an agent "decide" a checkmark.

## Enforcement layers (§5, stated once)

- **Commands** frame and sequence the work.
- **Built-in `/goal`** adds transcript-level persistence pressure (belt-and-
  braces; its evaluator reads only the transcript, so it cannot verify disk).
- **The Stop hook is the only real gate** — it alone reads disk state.

Do not shadow the built-in `/goal` or the bundled `/loop` with custom commands.

## What is deliberately NOT used

Worktrees (§3 — no colliding writes; default-branch base would start builders
from a stale vault), agent teams (§2.3 — experimental, wrong shape). The main
session is the orchestrator; there is no orchestrator agent.
