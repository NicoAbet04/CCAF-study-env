# Exam intel — topics reported on the real exam

> **What this file is.** Topics that colleagues who passed the CCAF reported
> seeing on the exam but which the prep courses cover poorly or not at all.
>
> **The bar for entry is non-negotiable:** an entry may only be added after it
> has been verified against an official documentation page, and it must cite
> that page. Hearsay does not go in a study note. This keeps the environment's
> ground rule ("every claim traceable to a source") intact while still giving
> exam intel somewhere to live.
>
> Entries render in domain notes inside a `> [!tip] 📌 Reported on the exam`
> callout, carrying their citation.

**How to add an entry:** append it here with source, date, domain, the claim,
and the doc link — then re-run `/course-build ccaf`. The verdict-freshness
check will route it into the right domain note and re-evaluate that note.

---

## 3.6 — System prompt flags vs CLAUDE.md in CI

- **Reported by:** teammate who passed (comment, 2026-09)
- **Domain / task:** 3 — Claude Code Configuration & Workflows, task 3.6
- **Verified against:** [CLI reference](https://code.claude.com/docs/en/cli-reference) (checked 2026-09-05)

Three mechanisms that look interchangeable and are not:

- **`--append-system-prompt`** — appends your text to the end of the default
  system prompt, so Claude Code's default behaviour is **retained**. This is the
  right choice for temporary, stage-specific instructions: different stages of a
  multi-step CI workflow may need different roles or rules.
- **`--system-prompt`** — **replaces** the system prompt entirely. Reach for it
  only when you genuinely need to override default behaviour.
- **`CLAUDE.md`** — persistent, shared project context that should apply across
  both CI runs and ordinary interactive sessions.

There is also `--append-system-prompt-file`, which takes the text from a file.

The exam framing to expect: given a CI scenario, pick the mechanism whose
*scope and persistence* match the requirement. Temporary and additive →
append. Total override → replace. Durable and shared → CLAUDE.md.

## 3.6 — Managed GitHub Code Review reads CLAUDE.md *and* REVIEW.md

- **Reported by:** teammate who passed (comment, 2026-09)
- **Domain / task:** 3 — Claude Code Configuration & Workflows, task 3.6
- **Verified against:** [Code review docs](https://code.claude.com/docs/en/code-review) (checked 2026-09-05)

Claude's managed GitHub Code Review reads **two** files, with a division of
labour:

- **`CLAUDE.md`** — general project context and standards.
- **`REVIEW.md`** (root level) — review-specific instructions: what to flag,
  severity calibration, exclusions, and reporting preferences.

`REVIEW.md` is freeform markdown. Documented patterns include redefining what
counts as an *Important* finding for your repo (the default calibration targets
production code, which suits a docs or prototype repo poorly), capping how many
nit-level comments one review may post, and skip rules for paths, branch
patterns, and finding categories — generated code, lockfiles, vendored
dependencies, machine-authored branches.

The trap to watch: assuming `CLAUDE.md` alone configures review behaviour. The
review-specific knobs live in `REVIEW.md`.

## 5.1 — Rolling window context (the most-reported surprise)

- **Reported by:** multiple public exam write-ups (2026-07 → 2026-09); several
  passers say they had "never heard of a rolling window context prior to taking
  the test"
- **Domain / task:** 5 — Context Management & Reliability, task 5.1
- **Verified against:** [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) (checked 2026-09-05)

Two different context behaviours, and the exam expects you to tell them apart:

- **The API accumulates.** As a conversation advances, each user message and
  assistant response accumulates in the context window and **previous turns are
  preserved completely**. Nothing is dropped for you. Everything counts: system
  prompt, every message, tool results, images, documents, tool definitions, and
  the output — including extended thinking.
- **Chat interfaces can roll.** The docs note that chat interfaces such as
  claude.ai "can also manage the context window on a rolling **first in, first
  out** basis" — the oldest turns fall out as new ones arrive.

The practical consequence, and the reason it makes a good exam question: if you
are building on the API, no rolling window is happening unless you implement
it. Long conversations need an explicit strategy — **compaction** (server-side
summarization of earlier turns) or **context editing** (tool-result clearing,
thinking-block clearing) — otherwise you hit the limit.

Adjacent facts from the same page worth knowing: exceeding the window on input
alone returns a 400 `invalid_request_error`; on 4.5-and-later models, running
out mid-generation stops with `stop_reason: "model_context_window_exceeded"`.
Accuracy also degrades as the window fills ("context rot"), so curating what is
in context matters as much as how much room remains.

---

## Calibration notes (not a topic — how the exam behaves)

- **Distractors are engineered to be plausible.** Multiple write-ups describe
  the wrong answers as "mistakes real engineers actually make," not filler.
  Elimination on obvious-wrongness will not work; you have to reason about the
  mechanism.
- **Domains 1 and 3 carry the most surprises**, with questions getting specific
  about CLAUDE.md structure and subagent context isolation. (Matches the plan's
  decision to weight flashcards toward the high-failure domains.)
- **Symptoms look alike; mechanisms differ.** A recurring theme in passer
  accounts: several answer options describe the same observed symptom, and the
  question is which underlying mechanism explains it. Study why a mechanism
  works, not which answer was right last time.
- **Hands-on beats re-reading.** The most-repeated preparation advice is to
  read the docs for a domain, then immediately build a small proof of concept.
  This is what the exam guide's own §8 exercises are for — see `/study`
  option (e).
