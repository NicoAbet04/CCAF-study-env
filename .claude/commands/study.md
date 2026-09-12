---
description: Run an interactive study session for a built course — flashcard
  drills, scenario quizzes, or a timed mock — and log weaknesses to Weak Areas.md.
argument-hint: <course-id> [domain-number]
---

Run an interactive study session for course **$ARGUMENTS**. This is the entry
point for every session *after* the vault is built. It is also the mechanism
that appends to `Weak Areas.md` (the baseline plan created that file but defined
nothing to feed it).

Read the course manifest (`courses/<id>/course.yaml`) and the vault's
`Weak Areas.md`. Then offer, via AskUserQuestion:

- **(a) Flashcard drill** — pull cards from the vault notes (filtered to the
  given domain if supplied, weighted toward Weak Areas topics), quiz one at a
  time via AskUserQuestion, and explain misses using the note content.
- **(b) Scenario quiz** — invoke the `cert-exam` skill (77 community questions).
- **(c) Generated scenario round** — write 5 FRESH scenario questions grounded
  ONLY in the vault notes for the chosen domain, so the bank never goes stale
  from memorization. Mark these `generated-not-verified`. For STYLE only (never
  for facts — content still comes only from the vault notes), use the two
  local mock-exam reviews in `courses/ccaf/` as exemplars of the official
  exam's voice: one scenario stem, one correct answer, three plausible
  distractors, and a one- or two-sentence "why this fails" for each wrong
  option that names the specific misconception it represents rather than just
  asserting it's wrong. `claudecertificationguide.md` is the MOST TRUSTED
  exemplar (its answer key is verified and it flags its own doc-currency
  checks) — prefer it as the primary model for phrasing, distractor shape, and
  trap construction. `claudetestprep_exam.md` is lower-confidence (sourcing
  unstated) — fine to draw structural variety from (e.g. its per-domain
  section grouping, its "why the others fail" bullet style) but never copy a
  factual claim from it without checking that claim against the vault note
  first.
- **(d) Mock-exam pointer** — link the external timed mocks from the manifest's
  practice tier (CyberSkill, CosX) for exam-day pacing; offer to debrief pasted
  results afterward.
- **(e) Hands-on lab** — pick one of the manifest's `prep_exercises` (the four
  exercises the OFFICIAL exam guide §8 recommends) filtered to the chosen
  domain, and coach the user through building it for real. The guide's own §7
  advice is to prepare with hands-on work, and domains 1 and 2 test judgment
  that reading cannot supply. Log what the user struggled to implement to
  `Weak Areas.md` the same way a missed question is logged.

After any round, append misses to `Weak Areas.md` as
`- [date] [[note#section]] — what was confused with what`, and suggest the next
session's focus from the running miss pattern.

Practice material is quarantined from notes and flashcards — it only feeds
`Weak Areas.md`. Never seed flashcards from mock questions.
