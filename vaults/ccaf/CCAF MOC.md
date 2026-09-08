---
tags: [ccaf, moc]
---

# CCAF — Claude Certified Architect (Foundations)

Your map of content for the CCAF exam vault. The exam is **60 questions, 120
minutes, 720/1000 to pass**, valid 12 months, scenario-heavy (4 of 6 scenarios).
Questions test **judgment**, not recall — so study the domain notes for the
*reasoning*, then drill scenarios with `/study ccaf`.

## The five domains (by exam weight)

| # | Domain | Weight | Flashcards |
|---|--------|:---:|:---:|
| 1 | [[1 - Agentic Architecture & Orchestration]] | 27% | 12+ |
| 3 | [[3 - Claude Code Configuration & Workflows]] | 20% | 8+ |
| 4 | [[4 - Prompt Engineering & Structured Output]] | 20% | 8+ |
| 2 | [[2 - Tool Design & MCP Integration]] | 18% | 12+ |
| 5 | [[5 - Context Management & Reliability]] | 15% | 8+ |

Domains **1** and **2** are the two highest-failure areas — weight your time there.
Each note is organised around the official exam guide's task list and ends with a
**Traps & distractors** section built from the guide's stated anti-patterns.

## How to use this vault

- Read a domain note end to end for the reasoning behind each task.
- Run `/study ccaf [domain]` for flashcard drills, the 89-question `cert-exam`
  scenario bank, freshly generated scenario rounds, or a hands-on lab.
- Misses are logged to [[Weak Areas]], which then steers later sessions.
- Every term of art is defined in [[Glossary]]; slash commands and CLI flags
  are in [[Claude Commands]]; every `.claude/` directory and config file is
  mapped in [[Claude Main Files and Directories]].
- Coverage and build health live in `SOURCE_INVENTORY.md`, `COVERAGE_GAPS.md`, and
  `FLAGGED.md` (all generated — don't hand-edit).

## Supporting pages

- [[Glossary]] — terms of art, defined plainly.
- [[Claude Commands]] — CLI flags and slash commands, defined plainly.
- [[Claude Main Files and Directories]] — every `.claude/` directory and
  project-root config file, mapped in one place.
- [[Weak Areas]] — your running miss log, appended by `/study`.

> [!info] Provenance
> Notes are condensed from the user's own course materials and the **official
> CCAF exam guide**. Practice questions (community bank, external mocks) are
> quarantined from the notes and flashcards — they only feed [[Weak Areas]].
