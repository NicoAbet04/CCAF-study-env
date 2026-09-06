---
name: cert-exam
description: Interactive Claude Certified Architect Foundations practice exam. Presents questions one by one using AskUserQuestion, tracks answers, and gives a final scaled score (100-1000, pass at 720).
context: fork
allowed-tools: Read, AskUserQuestion
argument-hint: "[number of questions, e.g. /cert-exam 20 — defaults to 20]"
---

# Claude Certified Architect Exam Runner

Run an interactive practice exam for the Claude Certified Architect – Foundations certification.

## Step 1: Setup

Read both exam files and concatenate their questions into one bank:

1. `/home/nico/Projects/PyCharmProjects/Claude-Certified-Architect-Foundations-Certification-Exam-main/Claude Certification Exam.md`
   — Q1-Q77, community-authored practice bank (PRACTICE tier, unofficial —
   author and sourcing unstated; see `courses/ccaf/course.yaml`).
2. `courses/ccaf/practice/exam-guide-sample-questions.md` — Q78-Q89, transcribed
   verbatim from the official Exam Guide's own §9 "Sample Questions" (PRACTICE
   tier, but each question carries a real citation to the guide).

<!-- Path fixed on adoption (§0.1): the original skill referenced a relative
     `Claude Certification/Claude Certification Exam.md` that does not resolve
     from study-env. This points at repo 1's exam file — the same PRIMARY source
     listed in courses/ccaf/course.yaml. -->

Parse all questions from both files. Questions follow this pattern:
- Start with `**Q[number].**`
- Followed by scenario context and question stem
- Then options `A) ... B) ... C) ... D) ...`
- Then `**Correct Answer: X**`
- Then explanation

Build one internal list of 89 questions: question number, scenario, stem,
options A-D, correct answer letter, explanation, and (if present) a
`*Citation: ...*` line — surface the citation in feedback when a question has
one, so the user knows which answers are backed by an official source versus
the unofficial bank.

If the user provided an argument (e.g., `/cert-exam 20`), use that as the question count. Otherwise default to 20.

## Step 2: Configure the session

Use ONE AskUserQuestion call with up to 3 questions:

**Question 1** — How many questions?
- header: "Questions"
- Options: "10 questions", "20 questions" (Recommended), "40 questions", "All 89"

**Question 2** — Domain focus?
- header: "Domain"
- Options: "All domains" (Recommended), "D1: Agentic Architecture", "D2: Tool Design & MCP", "D3: Claude Code Config"
- (Note: If user picks D4 or D5, they can type it as Other)

**Question 3** — Feedback mode?
- header: "Feedback"
- Options: "After each question" (Recommended), "Summary at the end only"

Apply the user's choices to build the question queue:
- If a domain is selected, filter to only questions in that domain (check the domain index in the exam file)
- Randomly shuffle the filtered list
- Take the first N questions per the count chosen

## Step 3: Run the exam

For each question in the queue:

1. Output a progress line: `**Question [current] of [total] | Score: [correct]/[answered so far]**`

2. Before building the question, shuffle the display order of the four options
   for THIS question only (a fresh random shuffle per question, independent of
   any other question). The source bank's correct-answer letter is not evenly
   distributed across A/B/C/D, so echoing the source order lets the position
   alone become a shortcut (e.g. several correct answers landing on "B" in a
   row). Never change an option's wording and never change which option is
   correct — only randomize which of the four texts is shown in each of the
   four slots. Keep a mapping from the displayed slot back to the option's
   original source letter so you can score it correctly afterward.

   Use AskUserQuestion with 1 question:
   - `question`: Include the scenario context followed by the question stem. Format it as:
     "[Scenario context]. [Question stem]?"
     Keep it readable — trim to the most essential parts if very long.
   - `header`: "Q[number]" (e.g., "Q13")
   - `multiSelect`: false
   - Options (4 options, in the shuffled order from above, always labeled A-D
     positionally):
     - label: "A", description: [text of whichever original option landed in slot 1]
     - label: "B", description: [text of whichever original option landed in slot 2]
     - label: "C", description: [text of whichever original option landed in slot 3]
     - label: "D", description: [text of whichever original option landed in slot 4]

3. Record the user's answer. Map the displayed slot they picked back to its
   original source letter using the mapping from step 2, then compare that
   original letter to the correct answer letter from the source.

4. If feedback mode is "After each question":
   - If correct: output `Correct.` then the explanation in brief (1-2 sentences).
   - If incorrect: output `Incorrect. Correct answer: [X]` then the explanation
     (2-3 sentences max, focused on why the correct answer is right). `[X]` is
     the DISPLAYED slot letter (A-D as shown to the user for this question),
     found via the step-2 mapping — never the source file's original letter,
     which the user never saw.

5. If feedback mode is "Summary at the end only": just acknowledge and move on with no answer reveal.

6. Continue to the next question. Do not use AskUserQuestion between questions for anything other than the question itself.

## Step 4: Final score

After all questions are answered, calculate and display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   EXAM COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Raw score:     [correct] / [total] ([percent]%)
Scaled score:  [scaled] / 1000
Pass mark:     720 / 1000 (~69% correct)

Result:        PASS  /  FAIL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Scaled score formula: `round(100 + (correct / total) * 900)`

Then show a domain breakdown:
```
Domain breakdown:
  D1 Agentic Architecture    [correct]/[total] ([%]%)
  D2 Tool Design & MCP       [correct]/[total] ([%]%)
  D3 Claude Code Config      [correct]/[total] ([%]%)
  D4 Prompt Engineering      [correct]/[total] ([%]%)
  D5 Context Management      [correct]/[total] ([%]%)
```

Then if feedback mode was "Summary at the end only", show all missed questions:
```
Questions you missed:
  Q[n]: Correct answer was [X]. [1-sentence explanation]
  ...
```
Here too, `[X]` is the displayed slot letter shown to the user for that
question (via the step-2 mapping), not the source file's original letter.

End with a short note pointing to the weakest domain if any scored below 60%.

## Rules

- Never reveal the correct answer before the user selects an option.
- Never skip or truncate questions mid-exam.
- If the exam file cannot be read, stop and report the error clearly.
- Keep all output outside of AskUserQuestion calls clean and brief. This is an exam, not a conversation.
