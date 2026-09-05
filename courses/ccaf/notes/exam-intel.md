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
