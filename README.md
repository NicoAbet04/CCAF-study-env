# study-env

A reusable **courseware environment** that turns course and certification source
material into an [Obsidian](https://obsidian.md) study vault — domain notes,
spaced-repetition flashcards, scenario quizzes, and a running record of your weak
areas. A **course is defined by a single manifest file**; all the machinery
(agents, hooks, commands) is shared and parameterized by it.

First tenant: **CCAF** — Claude Certified Architect (Foundations). Adding another
course means writing one new `courses/<id>/course.yaml`.

---

## Two ways to use this repo

- **As a student** — open the vault, read the notes, drill flashcards, run
  quizzes, and let your misses accumulate in *Weak Areas*. Jump to
  [Studying](#studying-day-to-day).
- **As a maintainer** — (re)build a course's vault from its sources under an
  enforced completeness gate, or add a new course. Jump to
  [Building & maintaining](#building--maintaining-a-course).

---

## Directory structure

```
study-env/
├── CLAUDE.md                  # ground rules + conventions + build-state model
├── README.md                  # this file
├── loop.md                    # unattended drive-to-completion body (bundled /loop)
├── courses/
│   └── ccaf/
│       ├── course.yaml        # THE manifest — the only file a course must author
│       ├── notes/             # curated pre-build notes (exam-intel, module-05-mcp)
│       └── sources-cache/     # cached primary sources (e.g. the official exam guide PDF)
├── vaults/
│   └── ccaf/                  # ← the Obsidian vault you study from (open THIS folder)
│       ├── 1 - Agentic Architecture & Orchestration.md
│       ├── 2 - Tool Design & MCP Integration.md
│       ├── 3 - Claude Code Configuration & Workflows.md
│       ├── 4 - Prompt Engineering & Structured Output.md
│       ├── 5 - Context Management & Reliability.md
│       ├── CCAF MOC.md        # map of content — start here
│       ├── Glossary.md        # terms of art, defined plainly
│       ├── Weak Areas.md      # your running miss log (auto-appended by /study)
│       ├── FLAGGED.md         # anything the build couldn't process (human review)
│       ├── SOURCE_INVENTORY.md  # generated view of source coverage
│       └── COVERAGE_GAPS.md     # generated view of remaining gaps (0 when done)
└── .claude/
    ├── settings.json          # registers the hooks
    ├── agents/                # domain-builder (writes notes), study-evaluator (reviews)
    ├── commands/              # /course-build, /course-audit, /study
    ├── skills/cert-exam.md    # interactive 77-question practice exam
    ├── hooks/                 # stop-gate.sh (the completeness gate) + audit.py + loggers
    └── state/ccaf/            # machine-authoritative build state (JSON)
```

> The source course repos live **outside** this repo (under
> `~/Projects/PyCharmProjects/`) and are treated as **read-only**. Nothing here
> ever writes back to them.

---

## Studying day to day

### 1. Open the vault

Open **`vaults/ccaf/`** as a vault in Obsidian (Obsidian opens any folder). Start
at **`CCAF MOC.md`** — the map of content linking all five domain notes with their
exam weights.

The **Spaced Repetition** community plugin is already bundled in the vault's
`.obsidian/plugins/`; if Obsidian doesn't enable it automatically, turn it on in
*Settings → Community plugins*. Without it the flashcards still read fine as text,
but you lose the scheduling.

### 2. Read the domain notes

There are five notes, one per exam domain, each **organised around the official
exam guide's task list** (not the source material's order). Every note contains:

- prose condensed from the course sources and the official guide, in plain language;
- `[[wikilinks]]` to related concepts, with every term of art linked to `[[Glossary]]`;
- one **mermaid diagram** of the domain's sub-topics;
- a block of **flashcards**;
- a closing **"Traps & distractors"** section — the wrong-but-plausible answers the
  exam is built to tempt you with, one per task, grounded in the guide's stated
  anti-patterns.

The exam tests **judgment on scenarios**, so read for the *mechanism* behind each
task, not the vocabulary.

### 3. Drill flashcards

Flashcards use the Spaced Repetition plugin's format — a `Question` line, a `?` on
its own line, then the `Answer` — and are tagged `#flashcards/domain-N`. Start a
review from the plugin's sidebar; it schedules cards by how well you recall them.
Cards are written as **scenarios** ("your loop never terminates because … — what's
the fix?"), not definitions.

### 4. Quiz yourself and simulate the exam

Run **`/study ccaf [domain]`** in Claude Code for an interactive session. It offers:

- **(a) Flashcard drill** — pulled from the notes, weighted toward your weak areas;
- **(b) Scenario quiz** — the bundled `cert-exam` skill (77 community questions),
  which you can also launch directly with `/cert-exam`;
- **(c) Generated scenario round** — 5 fresh exam-style questions grounded only in
  the vault notes, so the bank never goes stale from memorisation;
- **(d) Mock-exam pointer** — links to external timed mocks for exam-day pacing,
  with an offer to debrief your pasted results.

Exam facts: **60 questions, 120 minutes, 720/1000 to pass**, valid 12 months.

### 5. Let Weak Areas steer you

After any round, `/study` appends your misses to **`Weak Areas.md`**
(`- [date] [[note#section]] — what was confused with what`). Later sessions read
that log and weight questions toward your recurring gaps. Practice questions are
deliberately **kept out of the notes and flashcards** — they only feed Weak Areas,
so your practice scores stay an honest signal.

---

## Building & maintaining a course

You only need this section if you're (re)generating a vault or adding a course.
Run these as slash commands in Claude Code from the repo root.

| Command | What it does |
|---|---|
| `/course-build <id>` | Build or resume a vault: inventory sources → plan the domain assignment → dispatch a note-builder per domain → evaluate each → gap-fill, all under the completeness gate. |
| `/course-audit <id>` | Run the same deterministic audit the gate uses and report where things stand — without arming anything. Use it after hand-editing notes. |
| `/study <id> [domain]` | The study session described above (for a vault that's already built). |

### How a build stays honest

- **The manifest is the source of truth.** `courses/<id>/course.yaml` lists the
  source tiers, the exclusion patterns, and the blueprint (domains, weights, task
  lists, and per-domain flashcard minimums). It's the only file a new course authors.
- **Two subagents, least privilege.** `domain-builder` writes one note per domain
  from its assigned sources; `study-evaluator` reviews each note read-only and
  returns a verdict. A rejected note is repaired and re-evaluated.
- **The Stop-hook gate is the real enforcement.** `.claude/hooks/stop-gate.sh`
  runs a deterministic audit (`audit.py`) and won't let the build "finish" until
  every criterion holds: all sources covered or logged-irrelevant, zero coverage
  gaps, every domain approved with a fresh verdict, flashcard minimums met, the MOC
  and glossary present, and nothing failed without a `FLAGGED.md` entry. A cycle cap
  prevents infinite loops.
- **State is JSON under `.claude/state/<id>/`** and survives restarts; the Markdown
  views in the vault (`SOURCE_INVENTORY.md`, `COVERAGE_GAPS.md`) are generated from it.

See `CLAUDE.md` for the full ground rules (faithfulness to sources, the quarantine
of practice material, the writing-style contract) and the complete state model.

### Adding another course

1. Create `courses/<id>/course.yaml` — copy CCAF's and edit the sources, excludes,
   and blueprint.
2. Run `/course-build <id>` and answer the two checkpoints (inventory confirmation,
   assignment plan).
3. Open `vaults/<id>/` in Obsidian and study.

---

## Source tiers (why some material never enters the notes)

- **Primary** — inventoried, coverage-gated, condensed into notes (the course
  repos, the official exam guide, curated pre-build notes).
- **Reference** — linked and citable, never inventoried (official docs, cookbooks).
- **Cross-check** — compared against our output after generation, never ingested.
- **Practice** — quizzes, mocks, and labs are **quarantined** from notes and
  flashcards; they only feed `Weak Areas.md`. Studying the answer key would inflate
  your practice scores and destroy the weak-areas signal.

---

## Notes on version control

The generated vault is committed on purpose — it gives history and rollback for the
notes. Obsidian's per-session UI state (`.obsidian/workspace.json`) is **gitignored**
because it churns on every open; the plugin and theme config under `.obsidian/` is
kept tracked so a fresh clone opens with the right setup.
