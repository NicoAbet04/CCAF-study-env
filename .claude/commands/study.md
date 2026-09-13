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
- **(c) Generated scenario round** — write FRESH scenario questions grounded
  ONLY in the vault notes, so the bank never goes stale from memorization.
  Mark these `generated-not-verified`. Before writing any questions, ask the
  following via AskUserQuestion (these are independent knobs, not a single
  combined question):

  - **Domain scope** — a specific domain number; all domains grouped by
    domain (the default shape); or **randomized** — a mixed set drawn from
    across domains that is NOT grouped or ordered by domain, so consecutive
    questions can come from any domain in any order. Weight domain sampling
    toward Weak Areas topics the same way the flashcard drill does.
  - **Question count** — ask the user for a number, maximum **60**. If they
    ask for more than 60, tell them the maximum is 60 and STOP — do not
    generate a round, do not silently cap it and proceed.
  - **Difficulty** — low, medium, or high. Low: single-fact recall dressed as
    a short scenario, close to a flashcard. Medium: a scenario requiring one
    inference step or distinguishing between two adjacent mechanisms (the
    default shape used previously). High: multi-part or compound scenarios,
    distractors that require noticing a subtler misconception, or scenarios
    that combine two tasks/domains the way the real exam's harder items do.
  - **Temperature** — low or high, governing how far a scenario departs from
    material actually seen in the two local mock-exam reviews. Low temp:
    scenarios can closely mirror a case shape already present in
    `claudecertificationguide.md` / `claudetestprep_exam.md`, changed only in
    surface details (names, numbers). High temp: invent genuinely new
    scenario premises not modeled on any specific mock question — but every
    fact and mechanism referenced must still trace to the vault notes; higher
    temperature licenses new *scenarios*, never new *facts*.
  - **Option formatting** — normal (each option gets a short bolded label
    plus a one-line summary, as in past rounds) or **plain** — no bold, no
    label/summary split; each option is presented as a single complete plain
    sentence or two with no distinguishing formatting at all, so the answer
    can't be skimmed from shape or emphasis alone. When presenting via
    AskUserQuestion under plain formatting, put the full option sentence
    itself directly in the option's `label` field (AskUserQuestion has no
    hard length cap on `label` despite the tool's general "keep it short"
    guidance — a full sentence is fine there) and leave `description` empty.
    Never use a placeholder like "Option 1"/"Option 2" as the label with the
    real text pushed into `description` — that renders as a meaningless
    numbered stub above the actual content instead of showing the answer
    text directly, which defeats the point of plain formatting entirely.

  For STYLE only (never for facts — content still comes only from the vault
  notes), use the two local mock-exam reviews in `courses/ccaf/` as exemplars
  of the official exam's voice: one scenario stem, one correct answer, three
  plausible distractors, and a one- or two-sentence "why this fails" for each
  wrong option that names the specific misconception it represents rather
  than just asserting it's wrong (fold this "why this fails" into the option
  text itself when Option formatting is set to plain, rather than dropping
  it). `claudecertificationguide.md` is the MOST TRUSTED exemplar (its answer
  key is verified and it flags its own doc-currency checks) — prefer it as
  the primary model for phrasing, distractor shape, and trap construction.
  `claudetestprep_exam.md` is lower-confidence (sourcing unstated) — fine to
  draw structural variety from (e.g. its per-domain section grouping, its
  "why the others fail" bullet style) but never copy a factual claim from it
  without checking that claim against the vault note first.

  **Correct-answer placement must be randomized.** Before presenting each
  question, choose which option slot (A/B/C/D, or whatever the option
  labeling is) holds the correct answer independently and at random — do not
  default to writing the correct answer first and shuffling only in your
  head, and do not let habit cluster correct answers on one letter. Across a
  round of N questions, the correct-answer letters should look like a random
  draw, not a pattern — spot-check your own round before presenting it: if
  one letter holds the correct answer for much more than its fair share of
  questions (as a rough guide, more than ~40% on a round of 8+), reshuffle
  before presenting.

  **Option length and detail must be balanced, not just answer placement.**
  A well-known tell in badly-written multiple choice is that the correct
  option is the longest, most hedged, or most thoroughly explained one,
  while distractors are terse one-liners — this leaks the answer through
  shape even when the correct letter itself is randomized. Write all four
  options to a comparable length and level of detail: if the correct answer
  needs to name a mechanism and explain why it's right, give at least one
  distractor (ideally all three) a similarly complete explanation of why it
  seems plausible and where it actually goes wrong, rather than a bare
  dismissal. Before presenting each question, sanity-check option lengths
  against each other — if the correct option is noticeably longer or more
  elaborated than every distractor, rewrite the distractors (add the missing
  "why this looks right" reasoning, or trim the correct answer) rather than
  presenting it as-is. This check applies regardless of Option formatting
  (normal or plain).
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
