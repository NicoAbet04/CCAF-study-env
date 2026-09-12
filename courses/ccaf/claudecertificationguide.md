# CCAR-F Mock Exam Review (claudecertificationguide.com)

Source: `exam.txt` (post-exam review export, 60 questions, mock exam practice site). Formatted for study — no question, option, or explanation text has been altered or removed; only layout and grouping were added. Note this is a *different* exam session than the one previously formatted as `exam.md` (that one was your actual Claude Certified Architect – Foundations exam this morning; this one is a practice mock exam).

**Score:** 914 / 1000 — **PASSED** (pass mark 720/1000)
**Raw:** 55 / 60 correct (92%) · 5 incorrect · 0 skipped

**How scoring works** *(from the source, verbatim)*: Each domain's percentage correct is multiplied by its weight and scaled to 1000 points. For example, scoring 80% in Agentic Architecture (27% weight) contributes 0.80 × 0.27 × 1000 = 216 points. The pass mark is 720/1000 (72%). If a domain has no questions in the selected scenarios, its weight is redistributed proportionally among assessed domains. The real exam reports a scaled score from 100 to 1,000 plus your percent-correct by domain, so treat the percentages here as a readiness gauge rather than a prediction of your scaled score.

## Domain breakdown

| Domain | Correct | % | Points |
|---|---|---|---|
| D1 · Agentic Architecture & Orchestration | 13/14 | 93% | +251 |
| D2 · Tool Design & MCP Integration | 11/11 | 100% | +180 |
| D3 · Claude Code Configuration & Workflows | 10/12 | 83% | +167 |
| D4 · Prompt Engineering & Structured Output | 10/12 | 83% | +167 |
| D5 · Context Management & Reliability | 11/11 | 100% | +150 |

## Missed questions at a glance

| Q# | Domain | Topic | Your answer | Correct |
|----|--------|-------|:---:|:---:|
| [6](#question-6) | D4 · 4.3 | Structured output — enum fields | B | D |
| [35](#question-35) | D4 · 4.4 | Validation/retry — inter-step validation | A | B |
| [49](#question-49) | D3 · 3.2 | Skills frontmatter | B | D |
| [50](#question-50) | D3 · 3.5 | Iterative refinement — interview pattern | D | B |
| [60](#question-60) | D1 · 1.5 | Agent SDK hooks vs prompts | B | A |

All 5 misses land in only 3 domains: **D3** (2), **D4** (2), **D1** (1). D2 and D5 are clean sweeps.

---

## Question 1
`D2 · 2.4` — *Developer Productivity Tools* — mcp-server-integration / config-scope · `q-2-4-010` · **Correct**

A team's shared `.mcp.json` configures a PostgreSQL MCP server. A developer adds a personal staging database MCP server to their `~/.claude.json`, so both database tools are available in their session. When they query 'check user count', the agent calls the production tool instead of staging. What is the best resolution?

- **A)** Remove the production database from .mcp.json during testing so only the staging server is available.
  Modifying the shared .mcp.json affects all team members and removes production access for legitimate use. The configuration should not be altered for one developer's testing needs.
- **B)** Use tool_choice with forced selection of the staging database tool for all turns during testing.
  Forced selection prevents the agent from calling any other tool, including production database queries that may be needed for comparison or non-test tasks during the session.
- **C)** Move the personal staging server into the shared .mcp.json beside production and let the agent pick between them from each server's connection string.
  Personal staging infrastructure does not belong in the shared .mcp.json, and agents route by tool name and description, not by connection strings, so this neither isolates the config nor fixes selection.
- **D)** Rename the staging tool to a distinct name, put its environment in the description, and add a session rule that staging tools take precedence.
  Description tuning alone cannot route a context-free prompt like 'check user count' because the user gave the agent no environment cue. The fix is to make the two tools structurally distinguishable (distinct names, environment in the description) and to give the agent an explicit routing rule for the session. Renaming sits inside the developer's own ~/.claude.json so it does not affect the shared team configuration.

**Correct answer:** D

**Where this comes from**
- Lesson 2.4: MCP Server Integration (User vs project scope)
- Lesson 2.1: Tool Interface Design (Differentiating similar tools)

---

## Question 2
`D3 · 3.2` — *Developer Productivity Tools* — slash-commands-skills / skills-frontmatter · `q-3-2-002` · **Correct**

A platform engineering team creates a /security-audit skill that scans the codebase for vulnerabilities. The skill should be available to every developer on the project, must not be able to modify any files, and produces extensive analysis output. Which configuration is correct?

- **A)** Place the skill in CLAUDE.md as an always-loaded security scanning procedure
  CLAUDE.md is for universal, always-loaded standards, not on-demand task-specific workflows. A security audit is invoked when needed, not applied to every session. Placing it in CLAUDE.md wastes tokens in sessions where no audit is needed.
- **B)** Place the skill in .claude/commands/ with allowed-tools restricting it to Read, Grep, and Glob
  While .claude/commands/ is project-scoped (and equivalent to .claude/skills/ — both paths create identical /commands), this configuration is missing context: fork for isolating the extensive analysis output. Frontmatter features like context: fork and allowed-tools require a SKILL.md file in .claude/skills/, making that the better location for this use case.
- **C)** Place the skill in .claude/skills/ with a SKILL.md containing allowed-tools: ["Read", "Grep", "Glob"] and context: fork in the frontmatter
  .claude/skills/ is project-scoped and shared via version control, so every developer gets it. allowed-tools restricts the skill to read-only tools, preventing file modifications. context: fork isolates the extensive analysis output from the main conversation. This satisfies all three requirements. Current state (checked 14 August 2026): the live skills reference defines `allowed-tools` as "Tools Claude can use without asking permission during the turn that invokes this skill", with `disallowed-tools` removing tools from the pool. The exam guide frames it as restricting access, so answer that on the exam.
- **D)** Place the skill in ~/.claude/skills/ with allowed-tools restricting it to Read, Grep, and Glob, and context: fork in the frontmatter
  ~/.claude/skills/ is user-scoped and not shared via version control. The requirement states every developer on the project needs access, so it must be project-scoped.

**Correct answer:** C

**Where this comes from**
- Lesson 3.2: Custom Slash Commands and Skills (Skills frontmatter)
- Lesson 3.2: Custom Slash Commands and Skills (Project vs user scoping)
- Claude Code: Skills

---

## Question 3
`D5 · 5.5` — *Structured Data Extraction Pipeline* — human-review-calibration / aggregate-metrics-trap · `q-5-5-004` · **Correct**

A structured data extraction system processes invoices, purchase orders, and contracts. The monitoring dashboard shows 97% overall extraction accuracy and the team considers the system production-ready. A detailed audit reveals: invoices 99.5% accuracy (80% of volume), purchase orders 98% accuracy (15% of volume), contracts 72% accuracy (5% of volume). What does this reveal and what action is required?

- **A)** The system is performing well. 72% on contracts is acceptable since contracts represent only 5% of volume and barely affect the overall metric
  Acceptability depends on the business impact, not volume percentage. Contract extraction errors may have severe financial or legal consequences despite low volume. A 28% error rate on any document type is significant.
- **B)** The training data needs rebalancing so that contracts represent a larger proportion, which will naturally improve contract accuracy
  LLMs used for extraction are not retrained on production data this way. The issue is monitoring visibility and operational response, not model training data distribution.
- **C)** The aggregate metric is masking a severe per-type disparity. Give contracts mandatory review and report per-type metrics.
  This is a textbook case of aggregate metrics hiding per-type problems. 97% overall is misleading because high-volume invoice accuracy (99.5%) overwhelms the poor contract performance (72%). Per-type metrics would have surfaced this immediately. Contracts need different treatment until the extraction quality is acceptable.
- **D)** The 97% threshold should be raised to 99% overall to force improvement across all document types
  Raising the aggregate threshold does not address per-type disparities. Even at 99% overall, contract accuracy could remain low if invoice volume continues to dominate the metric. The solution is per-type metrics, not a higher aggregate bar.

**Correct answer:** C

**Where this comes from**
- Lesson 5.5: Human Review and Confidence Calibration (Aggregate metrics trap)

---

## Question 4
`D3 · 3.1` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — claude-md-hierarchy / enforcement · `q-3-1-007` · **Correct**

Project-level `.claude/CLAUDE.md` says 'use 4-space indentation matching the existing codebase.' A senior architect has 'use 2-space indentation' in their user-level `~/.claude/CLAUDE.md`. In recent sessions the architect's code has come back in 2 spaces and broken the build. The team needs a guarantee that 4-space indentation is applied on every save. What should they do?

- **A)** Move the 4-space rule into a `CLAUDE.local.md` at the project root so it is appended last and reads after the user-level file
  Load order does append `CLAUDE.local.md` after `CLAUDE.md` within a directory, but the docs are careful to call this 'load order,' not precedence, and warn that conflicts may resolve arbitrarily. `CLAUDE.local.md` is also gitignored, so a team standard cannot live there.
- **B)** Ask the architect to delete their user-level `~/.claude/CLAUDE.md` so there is no conflict to resolve
  This treats a personal config file as a team problem and doesn't scale — every new teammate would need to police their own home directory, and any future contradiction (from a different file, an `@import`, or a `.claude/rules/` entry) would resurface the same fragility. The fix is to remove reliance on guidance-style config for a rule that must be enforced, not to remove the conflicting file.
- **C)** Leave the rule in project-level `.claude/CLAUDE.md` — the more specific scope wins on conflicts, so the project rule will override the architect's user-level preference
  This is the popular paraphrase, but it's not what Anthropic's docs say. The docs describe a load order (broadest scope to most specific, so project instructions appear in context after user instructions) but explicitly state files are 'concatenated into context rather than overriding each other' and conflicts 'may [be] pick[ed] arbitrarily.' The team has already seen that assumption fail in production.
- **D)** Add a PostToolUse hook that runs the team's formatter after every Write/Edit, so 4-space indentation is enforced regardless of what Claude generates
  Anthropic's memory docs are explicit that CLAUDE.md is delivered as a user message with 'no guarantee of strict compliance,' and that 'if two rules contradict each other, Claude may pick one arbitrarily.' The docs themselves point at hooks for this case: hooks 'execute as shell commands at fixed lifecycle events and apply regardless of what Claude decides to do.' A PostToolUse hook running the formatter is the only option here that gives a hard guarantee.

**Correct answer:** D

**Where this comes from**
- Lesson 3.1: CLAUDE.md Hierarchy and Scoping (Loading order and conflict handling)
- Anthropic — How Claude remembers your project (memory docs)

---

## Question 5
`D1 · 1.7` — *Content Moderation and Classification System* — session-state-resumption / fresh-context · `q-1-7-008` · **Correct**

The moderation system handles appeals where users contest a moderation decision. Currently, the same agent that made the original decision re-evaluates the appeal. Appeal overturn rates are suspiciously low. What is the most effective architectural change?

- **A)** Automatically overturn decisions where the user provides any appeal justification to improve user trust
  Automatic overturn on any appeal completely undermines moderation. Users who genuinely violated policies would simply appeal every decision.
- **B)** Route every appeal to a human reviewer with full authority to overturn the automated decision, taking the original agent out of the appeal path entirely.
  Human review for every appeal does not scale and removes the benefit of automated moderation. Some appeals can be resolved automatically by a separate, unbiased instance.
- **C)** Add stronger instructions to the appeal handler's prompt requiring it to weigh the user's perspective fairly and set aside its earlier decision.
  Prompt instructions cannot overcome the bias of an agent reviewing its own decision. The original reasoning context still influences the re-evaluation regardless of instructions.
- **D)** Route appeals to a separate agent instance that cannot see the original reasoning, given only the content and the user's justification.
  A fresh agent instance without access to the original reasoning context evaluates the content independently. This avoids confirmation bias from the original decision. The appeal agent sees only the content and the user's argument, enabling a genuinely independent review.

**Correct answer:** D

**Where this comes from**
- Lesson 1.7: Session State and Resumption (Stale context)
- Lesson 1.2: Multi-Agent Orchestration (Isolation principle)

---

## Question 6
`D4 · 4.3` — *Content Moderation and Classification System* — structured-output / enum-fields · `q-4-3-004` · **Incorrect**

The moderation system's classification schema has a 'category' field defined as a free-text string. Auditors find 47 different category values in production data, including 'hate speech', 'Hate Speech', 'hate-speech', 'hateful content', and 'hate_speech' — all intended to be the same category. This makes downstream analytics and routing unreliable. What is the best schema fix?

- **A)** Add a post-processing normalisation step that maps all variations to canonical category names
  Post-processing normalisation adds complexity and requires constant maintenance as new variations appear. The schema should prevent the problem at the source rather than patching it downstream.
- **B)** *(your answer)* Add detailed instructions to the prompt listing the exact category names and their capitalisation so the model always emits the canonical string.
  Prompt instructions are probabilistic. The model may still produce variations despite instructions. Schema-level enforcement via enums is deterministic and cannot be overridden.
- **C)** Add few-shot examples showing the correct category formatting for each type
  Few-shot examples improve consistency but cannot guarantee exact string matching. Schema enums are the correct mechanism for constraining categorical output to a fixed set of values.
- **D)** *(correct answer)* Change 'category' from free-text to an enum with values like 'hate_speech', 'spam', and 'harassment', plus an 'other' option.
  Enum fields constrain the model to predefined values, eliminating spelling and formatting variations. Including 'other' as an enum value handles edge cases without allowing free-text drift. With strict: true, the schema guarantees only valid enum values are returned.

**Correct answer:** D
**Your answer:** B ✗

**Where this comes from**
- Lesson 4.3: Structured Output with Tool Use (Enum schema)

---

## Question 7
`D4 · 4.3` — *Structured Data Extraction Pipeline* — structured-output / nullable-fields · `q-4-3-001` · **Correct**

Your extraction system uses tool_use with a strict JSON schema. All fields are marked as required. Testers report that the model invents plausible-looking dates and amounts when processing documents that lack this information. What is the best fix?

- **A)** Add a validation step that checks all values against the source document
  Post-hoc validation is useful but does not address the root cause. Making fields optional prevents fabrication at the schema level.
- **B)** Switch from tool_use to prompt-based JSON extraction
  This moves backwards in reliability. Prompt-based JSON introduces syntax errors without solving the fabrication problem.
- **C)** Add an instruction telling the model not to hallucinate
  Vague instructions do not override the schema constraint. Required fields pressure the model to produce values.
- **D)** Make fields optional/nullable when source documents may not contain the information
  Optional/nullable fields allow the model to return null instead of fabricating values. This directly prevents fabrication for missing information.

**Correct answer:** D

**Where this comes from**
- Lesson 4.3: Structured Output with Tool Use (Nullable / optional fields)

---

## Question 8
`D5 · 5.5` — *Structured Data Extraction Pipeline* — human-review-calibration / aggregate-metrics-trap · `q-5-5-001` · **Correct**

A structured data extraction system achieves 97% overall accuracy across all document types. The team proposes automating all extractions where model confidence exceeds 95% to reduce human review costs. What is the critical risk in this approach?

- **A)** Aggregate accuracy can mask poor per-type performance, and confidence scores need calibration before use.
  97% overall can hide 40% error rates on specific document types. Without stratified validation and confidence calibration, automation will silently fail on certain inputs.
- **B)** The 95% confidence threshold is too low and should be raised to 99% for automation
  The threshold value is not the core issue — the problem is that aggregate metrics hide per-type performance disparities.
- **C)** The model will become overconfident over time as it processes more documents, requiring regular retraining
  LLMs do not train during inference. The issue is existing calibration gaps, not drift.
- **D)** Automated extractions should always have human review regardless of confidence, making the proposal fundamentally flawed
  Automation is valid when properly validated — the issue is doing it based on uncalibrated aggregate metrics, not the concept of automation itself.

**Correct answer:** A

**Where this comes from**
- Lesson 5.5: Human Review and Confidence Calibration (Aggregate metrics trap)
- Lesson 5.5: Human Review and Confidence Calibration (Confidence calibration)

---

## Question 9
`D4 · 4.6` — *Structured Data Extraction Pipeline* — multi-pass-review / attention-dilution · `q-4-6-007` · **Correct**

An extraction pipeline processes 50-page legal contracts in a single API call. It captures parties and dates from the first few pages but misses key financial terms in later pages, and occasionally contradicts itself across fields. A colleague suggests simply increasing the context window. What is the correct diagnosis and fix?

- **A)** Add more detailed instructions about the importance of financial terms to increase the model's focus on those sections
  Instructions cannot override the attention dilution effect of processing a 50-page document in one pass. The structural fix is breaking the extraction into focused per-section passes.
- **B)** The context window is too small; upgrading to a larger context model will fix the inconsistency
  If the document fits in the context window, a larger window does not improve attention quality. The problem is attention dilution over a long document, not context capacity.
- **C)** Run the full extraction three times and take the most common value for each field
  Multiple passes on the full document suffer from the same attention dilution pattern. The model will repeatedly extract early-page data well and miss later-page data.
- **D)** This is attention dilution; split into per-section extraction passes plus a cross-section reconciliation pass.
  Long documents cause attention dilution: the model attends thoroughly to early content but loses focus on later sections. Per-section passes ensure each part gets dedicated attention, and the integration pass catches contradictions and reconciles fields across sections.

**Correct answer:** D

**Where this comes from**
- Lesson 4.6: Multi-Instance Review and Output Validation (Multi-pass architecture)
- Lesson 4.6: Multi-Instance Review and Output Validation (Why bigger context does not fix it)

---

## Question 10
`D1 · 1.4` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — workflow-enforcement-handoff / prerequisite-gates · `q-1-4-012` · **Correct**

The refactoring coordinator delegates a database migration task to a subagent. The subagent sometimes executes destructive SQL migrations (DROP TABLE, ALTER TABLE DROP COLUMN) before verifying that a rollback script exists. The team requires that every destructive migration has a verified rollback before execution. What approach provides the strongest guarantee?

- **A)** Add a prerequisite check in the system prompt: 'Always verify rollback scripts exist before executing destructive migrations'
  Prompt instructions are probabilistic. The agent 'sometimes' skips verification, proving that instructions alone are insufficient. Destructive database operations require deterministic guardrails.
- **B)** A programmatic prerequisite gate that blocks any DROP or ALTER TABLE DROP until a rollback verification returns success.
  A programmatic prerequisite gate physically prevents destructive SQL execution until the rollback verification precondition is met. This provides a deterministic guarantee that no destructive migration runs without a verified rollback, eliminating the failure mode entirely.
- **C)** Have the coordinator agent review the subagent's SQL for destructive statements and withhold approval until a rollback script is present.
  The coordinator is another LLM agent and provides probabilistic review, not deterministic enforcement. It may also miss destructive patterns in complex SQL statements. Programmatic gates are the correct approach for safety-critical operations.
- **D)** Run all migrations in a sandboxed database first and check for errors before applying to the real database
  Sandboxing tests for execution errors, not for the existence of rollback scripts. A migration that runs successfully in a sandbox still lacks a rollback plan. The requirement is specifically about verifying rollback scripts before execution.

**Correct answer:** B

**Where this comes from**
- Lesson 1.4: Workflow Enforcement and Handoff (Prerequisite gates)
- Lesson 1.5: Agent SDK Hooks (PreToolUse hooks)

---

## Question 11
`D1 · 1.4` — *Content Moderation and Classification System* — workflow-enforcement-handoff / confidence-routing · `q-1-4-007` · **Correct**

The moderation system auto-removes posts classified as policy violations. Production logs reveal that 3% of auto-removed posts were legitimate content (false positives), generating user complaints and eroding platform trust. The team considers two approaches: (A) escalate all borderline cases to human reviewers, or (B) add a confidence threshold where only high-confidence violations are auto-removed and everything else goes to human review. Which approach is better and why?

- **A)** Approach A: escalate every borderline case, because human reviewers are more accurate than the classifier and a 3% false-positive rate is a trust problem.
  Escalating all borderline cases overwhelms the human review queue without leveraging the system's ability to handle clear-cut cases autonomously. The goal is to route intelligently, not to defer everything.
- **B)** Neither — instead lower the classification threshold so fewer posts are flagged as violations
  Lowering the threshold reduces false positives but increases false negatives (genuine violations going undetected). This trades one problem for another rather than adding an appropriate escalation path.
- **C)** Approach B: auto-remove only high-confidence violations, escalate uncertain cases to human review, and auto-approve high-confidence safe content.
  Confidence-based routing creates a tiered system: high-confidence violations are actioned immediately, high-confidence safe content passes through, and uncertain cases receive human review. This balances speed, accuracy, and reviewer workload while directly addressing the false positive problem.
- **D)** Approach B, but apply a single fixed 95% confidence threshold to every category regardless of how costly a false positive is for that content type.
  A single fixed threshold across all categories ignores that violation types have different risk profiles. The threshold should be calibrated per category based on the cost of false positives versus false negatives.

**Correct answer:** C

**Where this comes from**
- Lesson 1.4: Workflow Enforcement and Handoff (Confidence-based escalation)
- Lesson 1.4: Workflow Enforcement and Handoff (Enforcement spectrum)

---

## Question 12
`D4 · 4.2` — *Content Moderation and Classification System* — few-shot-prompting / few-shot-coded-content · `q-4-2-003` · **Correct**

The moderation system classifies hate speech accurately for explicit slurs but misses coded language and dog-whistle terms that human moderators easily recognise. The prompt includes detailed written rules about coded language patterns. What intervention would most improve detection of coded hate speech?

- **A)** Increase the model's context window so it can consider more of the user's post history for context
  Context window size is not the bottleneck. The model fails to recognise coded language in individual posts, which is a prompt engineering issue, not a context limitation.
- **B)** Add 20+ examples covering every known category of coded hate speech to maximise coverage
  Laundry lists of examples dilute attention and teach pattern-matching rather than generalisation. 2-4 targeted examples with reasoning are more effective than 20 examples without reasoning because they teach the analytical process.
- **C)** Add a comprehensive dictionary of every known coded term and dog-whistle to the system prompt so the classifier can match posts against the full list.
  A static dictionary becomes outdated immediately as coded language constantly evolves. It also bloats the prompt without teaching the model to recognise the underlying patterns of coded speech.
- **D)** Add 2-4 few-shot examples of coded hate speech, with reasoning naming the coded language and the targeted group.
  Few-shot examples with reasoning tags teach the model the pattern-recognition process, not just individual terms. Showing the reasoning chain — surface meaning, coded meaning, targeted group, contextual signals — enables the model to generalise to new coded terms it has not seen before.

**Correct answer:** D

**Where this comes from**
- Lesson 4.2: Few-Shot Prompting (Few-shot for nuanced detection)
- Anthropic: Multishot (Few-Shot) Prompting

---

## Question 13
`D5 · 5.3` — *(no scenario tag in source)* — error-propagation / coverage-annotations · `q-5-3-007` · **Correct**

A documentation generation pipeline uses Claude Code to produce docs from three sources: source code comments, existing wiki pages, and API schema files. During a run, the wiki page retrieval fails with a timeout, but the source code and API schema are available. The pipeline currently halts entirely on any source failure. What is the best error handling strategy?

- **A)** Return structured error context for the wiki failure, proceed with available sources, and mark the gaps that lack wiki content.
  This produces maximum value from available sources while maintaining transparency about what is missing. Structured error context enables intelligent recovery (retry later, alert the team). Explicit gap markers prevent users from trusting incomplete documentation as complete.
- **B)** Retry the wiki retrieval three times with exponential backoff. If all retries fail, halt the pipeline to prevent incomplete documentation
  Halting the entire pipeline because one of three sources is unavailable wastes the successful results from the other two sources. Documentation from source code and API schemas is still valuable even without wiki content.
- **C)** Use the source code comments to infer what the wiki pages would have contained, filling in the gaps with generated content
  Inferring wiki content from source code produces hallucinated documentation that appears authoritative. Wiki pages often contain operational context, known issues, and tribal knowledge that cannot be inferred from code.
- **D)** Silently skip the wiki source and generate documentation from the remaining two sources without noting the omission
  Silent omission hides the failure. Users would trust the documentation as complete, not knowing that wiki-sourced context (which may contain critical operational notes or caveats) is missing.

**Correct answer:** A

**Where this comes from**
- Lesson 5.3: Error Propagation in Multi-Agent Systems (Structured error context)
- Lesson 5.3: Error Propagation in Multi-Agent Systems (Coverage annotations)

---

## Question 14
`D1 · 1.7` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — session-state-resumption / fresh-start · `q-1-7-004` · **Correct**

A Claude Code agent has been working on a feature branch for 45 minutes and has accumulated extensive context about the codebase. The developer notices that several tool results from early in the session (file reads from 40 minutes ago) are now stale because a colleague pushed changes to those files. The agent is making recommendations based on the outdated file contents. What is the best recovery strategy?

- **A)** Start a fresh session with a summary of the key findings and decisions, then read the changed files for current state.
  Fresh start with summary injection is the prescribed recovery strategy for stale tool results. It preserves the valuable insights and decisions from the previous session while eliminating the stale data. Reading the changed files in the new session ensures the agent works from current state.
- **B)** Use fork_session to create a new branch that excludes the stale tool results while keeping the rest of the accumulated context.
  fork_session creates a branch from the current state, which includes the stale tool results. It does not allow selective exclusion of context. It is designed for divergent exploration, not for stale context recovery.
- **C)** Start a completely new session with no context carried over, so nothing from the previous 45 minutes can contaminate the new reasoning.
  Starting fresh discards 45 minutes of accumulated context and architectural understanding. The agent would need to rediscover all the insights it already found about the codebase.
- **D)** Continue in the current session and simply ask the agent to re-read the files a colleague changed, so it picks up the latest contents.
  Re-reading updates the file contents, but the stale results remain in the context window. The agent may still reference the outdated content from earlier in the conversation, leading to contradictory reasoning.

**Correct answer:** A

**Where this comes from**
- Lesson 1.7: Session State and Resumption (Stale context)
- Lesson 1.7: Session State and Resumption (Decision matrix)

---

## Question 15
`D5 · 5.5` — *Structured Data Extraction Pipeline* — human-review-calibration / stratified-sampling · `q-5-5-009` · **Correct** *(multi-select — choose 3)*

Your extraction pipeline reports 97% aggregate accuracy, and you want to automate high-confidence extractions. Which safeguards should be in place before you reduce human review? (Select 3)

- **A)** Verify accuracy separately by document type and field segment, not just in aggregate.
  A strong aggregate figure can mask poor performance on specific document types or fields.
- **B)** Expand the review team until every extraction can be checked by hand.
  Reviewing everything ignores the point of calibration: routing limited reviewer capacity to low-confidence and ambiguous cases.
- **C)** Calibrate field-level confidence thresholds against a labelled validation set.
  Confidence scores only route review attention correctly once they are calibrated on labelled data.
- **D)** Rely on the aggregate accuracy figure once it has held steady for a full quarter.
  Stability of the aggregate number does not reveal per-segment weaknesses, which is the risk the guide highlights.
- **E)** Keep stratified random samples of high-confidence extractions under review to measure error rates and catch novel patterns.
  Stratified sampling is the guide's mechanism for ongoing measurement after automation.

**Correct answer:** A, C, E

**Where this comes from**
- Lesson 5.5: Human Review and Confidence Calibration (Aggregate metrics trap)
- Lesson 5.5: Human Review and Confidence Calibration (Stratified sampling)
- Lesson 5.5: Human Review and Confidence Calibration (Field-level calibration)

---

## Question 16
`D5 · 5.5` — *Structured Data Extraction Pipeline* — human-review-calibration / stratified-sampling · `q-5-5-002` · **Correct**

A legal document extraction pipeline has been running for three months with calibrated confidence thresholds. Extractions above 90% confidence are auto-approved without human review, saving 60% of reviewer time. A new client submits contracts written in an unusual two-column legal format the system has not encountered before. The system reports 92% confidence on these extractions. What is the appropriate safeguard?

- **A)** Add a document format classifier that flags unknown formats for mandatory human review before any auto-approval
  While not wrong in principle, this adds ML infrastructure complexity that stratified sampling already handles. A format classifier requires training data and maintenance, whereas ongoing stratified sampling detects novel error patterns without additional models.
- **B)** Maintain stratified random sampling of high-confidence extractions across document types to catch the new format's error rate.
  Stratified random sampling is designed precisely for this scenario: detecting novel error patterns in high-confidence extractions that slip past threshold-based routing. By sampling across document types, the new format's errors would surface during routine verification even though the confidence scores appear acceptable.
- **C)** Trust the calibrated confidence threshold since it was validated against labelled data and the system reports 92% confidence, which exceeds the 90% auto-approval threshold
  Confidence calibration is only valid for document types represented in the calibration data. A novel format the system has never encountered can produce miscalibrated confidence scores — the model may be systematically overconfident because it does not recognise its own unfamiliarity with the format.
- **D)** Raise the confidence threshold from 90% to 98% for all document types to account for novel formats
  Raising the threshold globally penalises well-understood document types that are genuinely accurate at 90%+. This wastes reviewer capacity on documents that do not need review, while still not guaranteeing detection of format-specific issues.

**Correct answer:** B

**Where this comes from**
- Lesson 5.5: Human Review and Confidence Calibration (Stratified sampling)

---

## Question 17
`D3 · 3.6` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — cicd-integration / worktree-parallel · `q-3-6-008` · **Correct**

The team wants three Claude Code instances working in parallel: one extracting the authentication service, one extracting the billing service, and one updating shared libraries. All three need to commit to the same repository without conflicts. What is the correct setup?

- **A)** Use git worktree to create three separate working directories, each on its own branch, with one Claude Code instance per worktree
  git worktree creates multiple working directories from the same repository, each checked out to a different branch. Each Claude Code instance operates in its own isolated file system while sharing the same git history. This eliminates file system conflicts between parallel instances.
- **B)** Use fork_session to run the three tasks as parallel branches within a single Claude Code session
  fork_session creates parallel exploration branches within Claude Code's conversation context, not separate file system environments. Three large extraction tasks each need their own working directory to avoid file conflicts, which requires git worktree.
- **C)** Clone the repository three times into separate directories and merge the results manually
  Three separate clones create divergent git histories that must be reconciled manually. git worktree provides the same isolation with a shared repository, making merges straightforward through normal branch operations.
- **D)** Run all three instances in the same working directory on separate branches, switching branches as needed
  Multiple Claude Code instances in the same working directory will cause file system conflicts, dirty working trees, and race conditions, even on different branches. Git branch switching affects the entire working directory.

**Correct answer:** A

**Where this comes from**
- Claude Code Documentation — CLI Reference
- Git: Worktrees

---

## Question 18
`D2 · 2.4` — *Developer Productivity Tools* — mcp-server-integration / env-vars · `q-2-4-005` · **Correct**

A platform engineering team wants to share an MCP server for their internal ticketing system across all developers using Claude Code. The server requires an API token unique to each developer. Where should the MCP server be configured, and how should credentials be managed?

- **A)** Add the server to .mcp.json in the project root with each developer's API token hard-coded in the configuration.
  Hard-coding individual tokens in .mcp.json commits credentials to version control, which is a security risk. Each developer has a different token, so a single hard-coded value would not work for the team.
- **B)** Add the server to .mcp.json using ${TICKETING_API_TOKEN} expansion so each developer sets their own token.
  Project-level .mcp.json is version-controlled and shared, making the server available to everyone. Environment variable expansion keeps individual credentials out of version control while letting each developer authenticate with their own token.
- **C)** Create a shared .env file in the repository holding all the developer tokens, and reference it from .mcp.json.
  A shared .env file with all developer tokens still commits credentials to version control and creates a single file containing every team member's secrets, compounding the security risk.
- **D)** Have each developer add the server to their personal ~/.claude.json with their API token.
  User-level ~/.claude.json is for personal or experimental servers. A team-wide integration should be in project-level .mcp.json so it is version-controlled and consistently available to all developers.

**Correct answer:** B

**Where this comes from**
- Lesson 2.4: MCP Server Integration (Environment variable expansion)
- Lesson 2.4: MCP Server Integration (Scoping hierarchy)
- Claude Code: MCP Server Configuration

---

## Question 19
`D3 · 3.1` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — claude-md-hierarchy / posttooluse-formatting · `q-3-1-016` · **Correct**

The team wants to ensure that every Java file written by Claude Code during refactoring is automatically formatted with the project's Checkstyle rules before being saved. Developers occasionally forget to run the formatter manually. What is the correct hook configuration?

- **A)** A PreToolUse hook on the Write tool that runs Checkstyle on the content before the file is written
  PreToolUse fires before the tool executes. The file has not been written yet, so there is no file on disk to format. PreToolUse is suited for blocking or validating inputs, not for post-processing outputs.
- **B)** A PreToolUse hook on the Read tool that verifies all Java files are Checkstyle-compliant before they are read into context
  Checking files on read does not address the requirement. The goal is to format files when they are written, not to validate files when they are read. Existing legacy files may not be Checkstyle-compliant and should not block reading.
- **C)** Add 'Always run Checkstyle before saving files' to the CLAUDE.md system prompt
  Prompt instructions are probabilistic. The question states developers 'occasionally forget', and an LLM-based instruction has the same failure mode. A hook provides deterministic enforcement that cannot be skipped.
- **D)** A PostToolUse hook on file write operations that runs the Checkstyle formatter on the written file, automatically correcting any style violations
  PostToolUse fires after the file is written to disk. A hook that runs the Checkstyle formatter on the output file ensures every written Java file conforms to the project's style rules, regardless of what the model generated. This provides deterministic enforcement without relying on prompt instructions.

**Correct answer:** D

**Where this comes from**
- Claude Code: Hooks
- Anthropic: Agent SDK Hooks

---

## Question 20
`D1 · 1.6` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — task-decomposition / delegation · `q-1-6-008` · **Correct**

A coordinator agent receives a request to extract a payment processing module from the monolith into a standalone microservice. The task involves creating new API endpoints, migrating database tables, updating 40+ call sites, and writing integration tests. A junior developer suggests the coordinator should handle the entire task itself to avoid subagent communication overhead. Why is this approach wrong?

- **A)** The coordinator cannot access file system tools, so it physically cannot make code changes
  There is no inherent restriction preventing a coordinator from having file system tools. The issue is architectural — a single agent processing too many files suffers from attention dilution, not tool access limitations.
- **B)** The coordinator should never write code — it should only route tasks
  The coordinator can handle simple, well-scoped tasks directly. The issue here is not a blanket rule against the coordinator writing code, but that this specific task is too large and cross-cutting for a single agent to handle effectively.
- **C)** Loading 40+ files into one context dilutes attention — the coordinator should delegate to scoped subagents instead
  Large, multi-file tasks suffer from attention dilution when processed in a single context. Delegating to specialist subagents ensures each agent works with focused context. The coordinator should handle task decomposition and context injection, delegating implementation to specialists.
- **D)** The coordinator's API rate limits would be exceeded when processing 40+ files
  API rate limits are a practical concern but not the architectural reason to delegate. The root issue is attention dilution — quality degrades when one agent processes too many items in a single context, regardless of rate limits.

**Correct answer:** C

**Where this comes from**
- Lesson 1.6: Task Decomposition Strategies (Attention dilution)
- Lesson 1.2: Multi-Agent Orchestration (Coordinator responsibilities)

---

## Question 21
`D5 · 5.6` — *(no scenario tag in source)* — information-provenance / claim-source-mapping · `q-5-6-002` · **Correct**

A multi-agent research system has three subagents (financial filings, news, technical white papers) and a synthesis agent. Each subagent returns properly attributed findings, but the final synthesised report has no source attribution: stakeholders cannot trace which claim came from which source. Which fix addresses the root cause?

- **A)** Require subagents to output structured claim-source mappings and instruct the synthesis agent to preserve and merge them.
  Structured claim-source mappings survive synthesis because they are data structures, not prose that gets rewritten. The synthesis agent can merge mappings from multiple subagents while preserving the link between each claim and its source. This also enables content-appropriate rendering: financial data as tables, news as prose, technical findings as lists — each with attribution intact.
- **B)** Append a bibliography section at the end of the report listing all sources each subagent consulted
  A bibliography lists sources but does not map specific claims to specific sources. Stakeholders need to know which claim came from which document, not just which documents were consulted overall. This is document-level attribution, not claim-level provenance.
- **C)** Store all subagent outputs in a database and have the synthesis agent reference database entries by ID instead of incorporating content directly
  This adds infrastructure complexity without solving the synthesis problem. The synthesis agent still needs to merge and present findings coherently. Database references do not prevent attribution loss during the summarisation and rewriting that synthesis inherently requires.
- **D)** Have each subagent include source URLs as inline hyperlinks in their prose output so the synthesis agent can preserve them
  Inline hyperlinks in prose are fragile — the synthesis agent will rewrite, merge, and compress prose during summarisation, stripping or disconnecting links from their associated claims. Attribution must be in structured data, not embedded in prose that gets rewritten.

**Correct answer:** A

**Where this comes from**
- Lesson 5.6: Information Provenance and Multi-Source Synthesis (Structured claim-source mappings)
- Lesson 5.6: Information Provenance and Multi-Source Synthesis (Attribution preservation)

---

## Question 22
`D1 · 1.2` — *Content Moderation and Classification System* — orchestration-patterns / isolation · `q-1-2-010` · **Correct**

The moderation coordinator dispatches posts to specialist subagents. The text classifier has been extended to also handle image analysis: its prompt is now 2,500 tokens, its tool list has grown to 12 tools, and accuracy has dropped on both text and image tasks. What principle was violated and what is the fix?

- **A)** Split the combined agent into three narrower specialists: text sentiment, text policy, and image analysis
  Over-splitting into too many narrow specialists adds coordination overhead without clear benefit. The original architecture had a text classifier and an image analyser, which is the correct level of decomposition. Restoring that structure is the fix.
- **B)** The text classifier's context window is too small — upgrade to a model with a larger context window to handle the expanded prompt
  Context window size is not the issue. Combining unrelated responsibilities in a single agent degrades performance because the model must juggle competing instructions and tools. A larger context window does not fix scope creep.
- **C)** Isolation was violated; restore the text classifier to text-only work with scoped tools and keep image analysis separate.
  Each subagent should have a focused responsibility and a scoped tool set (4-5 tools maximum). Combining text and image analysis in one agent violates isolation, bloats the prompt, and confuses the model. Restoring separate specialists with scoped tools improves accuracy for both tasks.
- **D)** Add better instructions to the combined subagent's prompt to clarify when it should use text tools versus image tools
  Better instructions do not address the fundamental problem of an overloaded agent. Twelve tools and 2,500 tokens of instructions degrade performance regardless of instruction quality. The fix is architectural, not instructional.

**Correct answer:** C

**Where this comes from**
- Lesson 1.2: Multi-Agent Orchestration (Isolation principle)
- Lesson 1.4: Workflow Enforcement and Handoff (Scoped tool access)

---

## Question 23
`D5 · 5.4` — *(no scenario tag in source)* — codebase-exploration / crash-recovery · `q-5-4-011` · **Correct**

A coordinator spawns four Claude Code subagents to explore a large codebase overnight: one maps the data layer, one traces API routes, one audits tests, one catalogues dependencies. Three hours in, the machine restarts. On rerun, the coordinator starts every exploration again from zero. What design change lets a restarted run continue from where the crash left off?

- **A)** Resume the coordinator's previous session so the conversation history is restored
  Session resumption restores the coordinator's own conversation, not the subagents' accumulated findings: their contexts were separate and are gone. The coordinator would still have to re-run the explorations to regain that knowledge.
- **B)** Run the four explorations sequentially in one session so all findings stay in a single context
  Serialising the work gives up parallelism and pushes every verbose discovery into one context window, and a crash still loses the lot: an in-memory context is not durable state, however it is arranged.
- **C)** Have each agent export structured state to a manifest the coordinator loads on resume
  Structured state exports are the crash-recovery pattern: each agent persists its findings to a known location as it progresses, so after a failure the coordinator loads the manifest, sees what is complete, and seeds the remaining agents with prior findings instead of starting from zero.
- **D)** Wrap each subagent in automatic retries so transient failures cannot end the run
  Retries help an agent survive a failed tool call; they do nothing for a machine restart that kills the whole run. Recovery needs durable state that outlives the process, not more attempts within it.

**Correct answer:** C

**Where this comes from**
- Lesson 5.4: Codebase Exploration (Crash recovery via structured state manifests)
- Claude Docs: Agent SDK Sessions

---

## Question 24
`D1 · 1.2` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — orchestration-patterns / context-passing · `q-1-2-007` · **Correct**

A team runs a coordinator agent that delegates refactoring work to three specialist subagents: a schema-migration agent, an API-layer agent, and a test-update agent. The test-update agent frequently produces tests that reference database schemas the schema-migration agent has already renamed. The subagents do not communicate with each other. What is the root cause?

- **A)** The subagents need a shared message bus so the test-update agent can query the schema-migration agent for the latest schema names
  In a hub-and-spoke multi-agent architecture, subagents must never communicate directly. All communication flows through the coordinator. Adding a message bus violates this principle and creates coordination complexity.
- **B)** The test-update agent should have read access to the schema migration files so it can discover the new names itself
  While this might work as a workaround, it misses the architectural root cause. The coordinator is responsible for passing all necessary context to each subagent. The test-update agent should not need to discover information that the coordinator already has.
- **C)** The schema-migration agent and test-update agent should run sequentially rather than in parallel to avoid race conditions
  Sequencing alone does not solve the problem if the coordinator does not pass the schema-migration agent's results to the test-update agent. The issue is missing context injection, not execution order.
- **D)** The coordinator is not passing the schema-migration agent's output (including renamed schemas) as context when delegating to the test-update agent
  In hub-and-spoke orchestration, the coordinator manages all inter-agent communication. Subagents do not inherit each other's context. The coordinator must explicitly pass relevant outputs from earlier subagents as context to downstream subagents. Here, the renamed schema mappings must be injected into the test-update agent's context.

**Correct answer:** D

**Where this comes from**
- Lesson 1.2: Multi-Agent Orchestration (Isolation principle)
- Lesson 1.3: Subagent Invocation and Context Passing (Context passing)

---

## Question 25
`D1 · 1.6` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — task-decomposition / adaptive-decomposition · `q-1-6-009` · **Correct** *(multi-select — choose 2)*

You are planning how Claude should tackle a large, unfamiliar refactoring effort. Which characteristics of the work indicate dynamic adaptive decomposition rather than a fixed sequential pipeline? (Select 2)

- **A)** The review covers the same predictable set of aspects on every run.
  A predictable multi-aspect review is exactly where a fixed prompt-chaining pipeline fits best.
- **B)** The useful subtasks only become clear as intermediate findings come in.
  Adaptive plans generate subtasks from what each step discovers, which a fixed pipeline cannot do.
- **C)** Each step's output feeds the next in a stable, known order.
  A stable, known step order is the defining property of a sequential pipeline, not of adaptive decomposition.
- **D)** The task is open-ended, like adding comprehensive tests to a legacy codebase you have not mapped yet.
  This is the guide's example of open-ended work: map the structure first, then build a prioritised plan that adapts as dependencies surface.

**Correct answer:** B, D

**Where this comes from**
- Lesson 1.6: Task Decomposition Strategies (Dynamic adaptive decomposition)
- Lesson 1.6: Task Decomposition Strategies (Sequential pipelines)

---

## Question 26
`D4 · 4.1` — *Content Moderation and Classification System* — system-prompts / explicit-criteria · `q-4-1-006` · **Correct**

The moderation system's prompt instructs Claude to 'be conservative when moderating and err on the side of caution.' Reviewers find that innocuous posts about cooking with knives, news articles about violence, and fictional war stories are all being flagged as policy violations. What is the root cause and fix?

- **A)** Add an allowlist of safe topics such as cooking, news and fiction that should never be flagged at all by the classifier.
  Allowlists are brittle and impossible to maintain comprehensively. New safe topics will constantly appear. The fix is better criteria that teach the model to distinguish context, not a growing list of exceptions.
- **B)** Replace 'be conservative' with explicit categorical criteria defining each violation category with concrete examples.
  Vague directives like 'be conservative' give the model no basis for distinguishing between genuine violations and legitimate content that mentions sensitive topics. Explicit criteria with examples of both violations and non-violations (news, fiction, educational content) enable consistent, calibrated decisions.
- **C)** The model is too sensitive, so lower the temperature until it stops over-flagging borderline posts in the moderation queue.
  Temperature affects randomness, not the interpretation of moderation criteria. The over-flagging is caused by vague instructions, not sampling behaviour.
- **D)** Add a second moderation pass that re-reads each flagged post under the same 'be conservative' guidance and strips out the false positives before any action.
  A second pass using the same vague 'be conservative' criteria will reproduce the same false positives. Fix the criteria first; add verification layers second.

**Correct answer:** B

**Where this comes from**
- Lesson 4.1: System Prompts with Explicit Criteria (Explicit criteria over hedge phrases)
- Lesson 4.1: System Prompts with Explicit Criteria (Severity calibration)

---

## Question 27
`D4 · 4.4` — *Structured Data Extraction Pipeline* — validation-retry / pydantic-validation · `q-4-4-009` · **Correct**

Your extraction pipeline uses tool_use with a JSON schema, so outputs always parse. Finance still reports invoices where line items do not sum to the stated total, and where the due date precedes the invoice date. The team wants retries to receive precise, per-field error messages. What should you add?

- **A)** An instruction telling the model to double-check its own extraction in the same request before responding
  Same-session self-review retains the generation context and its bias, and produces no machine-readable error for the retry loop to feed back.
- **B)** A Pydantic model whose validators encode the sum and date-order rules, feeding its validation errors into retries
  Cross-field semantic rules live in validation code; Pydantic validators express them and raise per-field errors the retry request can quote verbatim.
- **C)** A more capable model, since semantic errors indicate the current one is under-powered
  No model tier guarantees semantic correctness; the fix is validation logic around the model, and an upgrade is the maximum-cost non-answer.
- **D)** Tighter JSON schema constraints: numeric minimum and maximum bounds on every amount field and format checks on every date field
  Range and format constraints check fields in isolation; both reported failures are relationships between fields, which a JSON schema cannot express.

**Correct answer:** B

**Where this comes from**
- Lesson 4.4: Validation, Retry, and Feedback Loops (Pydantic as the validation layer)

---

## Question 28
`D2 · 2.5` — *Developer Productivity Tools* — built-in-tools / edit-replace-all · `q-2-5-004` · **Correct**

A developer needs to rename a variable from 'userData' to 'customerData' in a specific file. The variable appears 12 times throughout the file. What is the most efficient approach using Claude Code's built-in tools?

- **A)** Use Bash with sed to perform a global find-and-replace across the file.
  While sed can perform the replacement, the exam expects candidates to use built-in tools for file modifications. Edit with replace_all is the purpose-built tool for this task.
- **B)** Use Read to load the whole file, then Write the entire file back with all twelve of the occurrences changed by hand.
  Read + Write rewrites the entire file, which is wasteful for a simple rename. The Edit tool with replace_all handles this more efficiently by sending only the diff.
- **C)** Use Edit with replace_all set to true, specifying 'userData' as the old string and 'customerData' as the new string.
  The Edit tool's replace_all parameter replaces all occurrences of the specified string in a single operation. This is the most efficient approach for renaming a variable throughout a file.
- **D)** Use Grep to find all 12 occurrences, then call Edit 12 times, once for each occurrence with unique surrounding context.
  Calling Edit 12 times is inefficient. The Edit tool's replace_all parameter is designed for exactly this use case — renaming a variable across an entire file in a single call.

**Correct answer:** C

**Where this comes from**
- Lesson 2.5: Built-in Tools (Edit replace_all)
- Claude Code: Built-in Tools

---

## Question 29
`D5 · 5.3` — *(no scenario tag in source)* — error-propagation / access-vs-empty · `q-5-3-002` · **Correct**

A research subagent queries an academic journal database for articles on renewable energy policy. The database responds successfully but returns zero matching articles. Meanwhile, a second subagent querying a government statistics API receives a connection timeout. The coordinator currently handles both cases identically by retrying three times. What should change?

- **A)** Remove retries entirely and immediately escalate both failures to a human operator for investigation
  This is disproportionate. The API timeout is a transient failure that retries can resolve. The empty journal result is not a failure at all — it is a valid answer. Neither case requires human escalation.
- **B)** Distinguish access failures from valid empty results: retry the API timeout as a transient failure, but accept the zero-match journal response as a valid finding and annotate the coverage gap
  Access failures (timeouts, connection errors) indicate the tool could not reach the data source and warrant retry. Valid empty results mean the tool reached the source and found no matches — this IS the answer. Conflating these leads to unnecessary retries on valid results and missed coverage annotations.
- **C)** Increase the retry count to five for both cases to give transient failures more time to resolve
  More retries do not fix the core problem. The journal database returned a valid empty result — it successfully searched and found nothing. Retrying it wastes time and API calls on an operation that already completed correctly.
- **D)** Add exponential backoff to all retries so the subagents wait progressively longer between attempts
  Backoff improves retry behaviour for transient failures but does not address the fundamental issue: the journal query does not need retries at all. It returned a valid response indicating no matches exist.

**Correct answer:** B

**Where this comes from**
- Lesson 5.3: Error Propagation in Multi-Agent Systems (Access failure vs empty)
- Lesson 5.3: Error Propagation in Multi-Agent Systems (Local recovery for transient)

---

## Question 30
`D2 · 2.5` — *Developer Productivity Tools* — built-in-tools / edit-recovery · `q-2-5-007` · **Correct**

A developer asks Claude Code to modify a function in a large file. The Edit tool fails with a 'non-unique match' error because the target text appears in multiple locations within the file. What is the correct recovery approach?

- **A)** Switch to Bash with sed to perform the replacement using line numbers instead of text matching.
  Bash with sed bypasses the Edit tool's safety guarantees and is fragile when line numbers shift. The guide's documented fallback for a non-unique match is Read + Write, not a shell rewrite.
- **B)** Use Read to load the full file contents, then use Write to output the complete modified file with the change applied.
  The exam guide names Read + Write as the documented fallback when Edit cannot find unique anchor text: load the full file with Read, then Write the complete modified file. That is the recovery path the exam tests for a non-unique match.
- **C)** Expand the Edit search string to include more surrounding context until it becomes unique in the file.
  Widening the anchor until it is unique, or using replace_all, is what current Claude Code documents and is sound engineering. It is not the fallback the exam guide names, and the guide is what this item tests: a non-unique Edit failure routes to Read + Write. See the lesson's current-state note for the divergence.
- **D)** Split the file into smaller files so that each occurrence appears in only one file, then use Edit on each.
  Restructuring files to accommodate tool limitations is disproportionate effort. The Edit tool's own recovery path (more context or replace_all) handles non-unique matches without changing the codebase.

**Correct answer:** B

*(Note: the exam guide's answer (B, Read+Write) diverges from current Claude Code documentation, which recommends widening the match context or using replace_all — option C. The explanations flag this divergence explicitly; answer per the guide on the exam.)*

**Where this comes from**
- Lesson 2.5: Built-in Tools (Edit non-unique match recovery)
- Claude Code: Built-in Tools

---

## Question 31
`D3 · 3.6` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — cicd-integration / worktree-coordination · `q-3-6-009` · **Correct**

Two Claude Code instances are running in separate git worktrees: Instance A is extracting the payment service (branch: extract/payment) and Instance B is extracting the inventory service (branch: extract/inventory). Both instances need to modify the shared OrderService.java file — Instance A to remove payment logic and Instance B to remove inventory logic. How should the team coordinate this?

- **A)** Create a third Claude Code instance dedicated to modifying only shared files, with Instances A and B handling everything else
  A dedicated shared-file instance adds coordination complexity without clear benefit. It needs to understand both extraction contexts to make correct modifications. Sequential merging with rebasing is simpler and more reliable.
- **B)** Have Instance A complete and merge first, then Instance B rebases onto the updated main before modifying OrderService.java
  Sequencing modifications to shared files avoids merge conflicts. Instance A completes its changes to OrderService.java and merges. Instance B then rebases onto the updated main, seeing Instance A's changes, and makes its modifications with full awareness of the current state. This is the standard coordination pattern for parallel Claude Code instances modifying shared files.
- **C)** Use file locking via git to prevent both instances from modifying OrderService.java simultaneously
  Git does not have built-in file locking for standard workflows. While Git LFS supports file locking, it is designed for binary files, not source code coordination. Sequential merge-and-rebase is the standard approach for coordinating parallel branches.
- **D)** Let both instances modify OrderService.java independently on their branches and resolve the merge conflict when merging to main
  Allowing both instances to make independent, potentially contradictory modifications to the same file risks complex merge conflicts that are difficult to resolve correctly. Coordinating changes to shared files upfront is safer.

**Correct answer:** B

**Where this comes from**
- Claude Code Documentation — CLI Reference
- Git: Worktrees

---

## Question 32
`D3 · 3.3` — *Developer Productivity Tools* — path-specific-rules / glob-patterns · `q-3-3-009` · **Correct**

A developer working on a React Native project notices that Claude Code applies web-specific React conventions (e.g., using div elements) when editing mobile components in the src/mobile/ directory, despite having mobile-specific conventions documented. The root CLAUDE.md contains general React standards, and there is no directory-level or rules-based configuration for mobile. What is the best fix?

- **A)** Add mobile-specific conventions to the root CLAUDE.md alongside the existing web React standards
  Adding mobile conventions to the root CLAUDE.md would load them for every session, including when editing web components, API handlers, or any other file. This wastes tokens and could cause confusion when both web and mobile conventions are present simultaneously.
- **B)** Create a .claude/rules/react-native.md file with paths: ["src/mobile/**/*"] containing the mobile-specific conventions
  A rules file with a path restriction to src/mobile/ ensures mobile conventions load only when editing mobile components. This keeps the root CLAUDE.md focused on universal standards while providing targeted, token-efficient mobile guidance.
- **C)** Create a CLAUDE.md file in src/mobile/ and remove all React standards from the root CLAUDE.md
  A directory-level CLAUDE.md in src/mobile/ would work for that directory, but removing React standards from the root CLAUDE.md would leave web components without guidance. The correct approach preserves root-level standards and adds path-scoped mobile rules.
- **D)** Replace the root CLAUDE.md web React conventions with mobile React Native conventions
  Replacing web conventions with mobile conventions would break guidance for the web portion of the codebase. Both web and mobile conventions are needed, but scoped to their respective file paths.

**Correct answer:** B

**Where this comes from**
- Lesson 3.3: Path-Specific Rules (Rule file examples)
- Lesson 3.3: Path-Specific Rules (Path-specific rules)

---

## Question 33
`D2 · 2.3` — *Developer Productivity Tools* — tool-distribution-choice / tool-choice · `q-2-3-006` · **Correct**

A team's agent must generate a weekly report on the first turn of each conversation by calling `generate_report`. With `tool_choice: 'auto'`, the agent sometimes responds with a text summary instead. The team wants to guarantee `generate_report` is called on turn one while allowing normal tool selection afterwards. What is the correct configuration?

- **A)** Remove all tools except generate_report from the first turn's tool list, then add the remaining tools for subsequent turns.
  While this would work, dynamically modifying the tool list between turns is unnecessarily complex. Forced tool_choice selection achieves the same guarantee with a simpler configuration change.
- **B)** Set tool_choice to 'any' on every turn of the conversation, so the agent is always obliged to call one of its available tools.
  'any' forces a tool call but does not guarantee which tool is called. The agent might call a different tool on the first turn. Additionally, forcing tool calls on every subsequent turn prevents normal text responses.
- **C)** Set tool_choice to forced selection of generate_report for the first turn, then switch to 'auto' for subsequent turns.
  Forced selection with the specific tool name guarantees generate_report is called on the first turn. Switching to 'auto' afterwards restores normal behaviour where the model decides whether and which tools to call.
- **D)** Add a system prompt instruction stating 'Always call generate_report on the first turn' and leave tool_choice on 'auto'.
  System prompt instructions are advisory, not enforced. With 'auto', the model can still choose to respond with text instead of calling the tool. This does not guarantee the mandatory first step.

**Correct answer:** C

**Where this comes from**
- Lesson 2.3: Tool Distribution and Tool Choice (Forced tool selection)
- Anthropic: Tool Use Documentation

---

## Question 34
`D1 · 1.3` — *Content Moderation and Classification System* — subagent-invocation-context / parallel-spawning · `q-1-3-011` · **Correct**

The coordinator receives a batch of 200 flagged posts to moderate. Currently it processes them sequentially, taking 45 minutes. Each post's moderation is independent — the decision on one post does not affect others. How should the coordinator handle this batch?

- **A)** Increase the iteration cap on the agentic loop to allow the agent more time to process all 200 posts
  The iteration cap controls how many tool calls the agent can make within a single task, not how many independent tasks it can process. The issue is parallelism, not loop duration.
- **B)** Process all 200 posts in a single API call by concatenating them into one large prompt
  Concatenating 200 posts into a single prompt causes attention dilution. Quality degrades for posts later in the sequence, and a single failure blocks the entire batch.
- **C)** Split into fixed batches of 20 posts and process each batch sequentially in a single prompt
  Batching 20 posts into a single prompt still risks attention dilution across posts within each batch. And sequential batch processing still takes much longer than parallel individual processing.
- **D)** Delegate independent posts to parallel subagent instances, with the coordinator aggregating results as they complete
  Since each post's moderation is independent, the coordinator should delegate them to parallel instances. This reduces total processing time from sequential (45 minutes) to roughly the time of the slowest individual moderation, and a failure on one post does not block others.

**Correct answer:** D

**Where this comes from**
- Lesson 1.3: Subagent Invocation and Context Passing (Parallel spawning)

---

## Question 35
`D4 · 4.4` — *Structured Data Extraction Pipeline* — validation-retry / inter-step-validation · `q-4-4-006` · **Incorrect**

Your document processing pipeline chains three steps: (1) extract raw text, (2) classify document type, (3) extract structured fields based on type. Step 2 occasionally misclassifies invoices as purchase orders, causing step 3 to extract the wrong fields. The team proposes combining steps 2 and 3 into a single prompt to reduce errors. What is the better approach?

- **A)** *(your answer)* Add more few-shot classification examples to step 2's prompt so misclassifications stop occurring
  Better examples may help, but without validation between steps, misclassifications still cascade silently into step 3. Inter-step validation is the structural fix.
- **B)** *(correct answer)* Keep steps separate and validate the classification between steps 2 and 3 before extraction
  Keeping steps separate maintains focused prompts. Adding validation between steps catches misclassifications before they cascade into wrong-field extraction. This is the core principle of prompt chaining: focused steps with inter-step validation.
- **C)** Run step 2 three times and use majority voting to determine the document type
  Majority voting adds cost and latency without addressing the root cause. Validation between steps is more efficient and catches the specific failure mode.
- **D)** Combine steps 2 and 3 exactly as proposed, on the grounds that fewer steps mean fewer points of failure.
  Combining steps creates a less focused prompt that must handle both classification and extraction simultaneously. This increases attention dilution and makes it harder to diagnose which part fails.

**Correct answer:** B
**Your answer:** A ✗

**Where this comes from**
- Lesson 4.4: Validation, Retry, and Feedback Loops (Self-correction flow)
- Lesson 4.4: Validation, Retry, and Feedback Loops (Retry boundary)

---

## Question 36
`D4 · 4.6` — *Content Moderation and Classification System* — multi-pass-review / self-review-bias · `q-4-6-005` · **Correct**

The moderation team asks a single Claude session to classify a post, then immediately asks the same session to independently review its own classification for quality assurance. The 'review' agrees with the original classification 98% of the time, including cases that human auditors later identify as errors. Why is this self-review ineffective?

- **A)** The model's temperature is too low, producing deterministic agreement — increase temperature for the review pass
  Temperature affects sampling randomness, not reasoning independence. Higher temperature may occasionally produce different outputs but does not create genuine independent review. The model is still anchored to its own prior reasoning in the same session.
- **B)** Self-review is effective but the 98% agreement rate simply reflects high initial accuracy — the 2% disagreement is the expected error rate
  Human auditors found errors in cases where the self-review agreed, proving the 98% agreement does not reflect accuracy. The self-review is confirming errors, not catching them, due to same-session reasoning bias.
- **C)** The model needs a stronger review prompt with explicit instructions to look for errors in the original classification
  Stronger instructions do not overcome the fundamental limitation. The same session retains the reasoning context from the original classification, biasing the review toward agreement.
- **D)** The same session retains the model's reasoning, so it stays anchored to its classification; use a fresh independent instance to review.
  Self-review within the same session is fundamentally limited because the model's conversation context includes the original reasoning. It will naturally be anchored to its prior conclusions. An independent instance with no access to the original decision evaluates the content fresh, providing genuine quality assurance.

**Correct answer:** D

**Where this comes from**
- Lesson 4.6: Multi-Instance Review and Output Validation (Self-review limitation)

---

## Question 37
`D1 · 1.7` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — session-state-resumption / fork-session · `q-1-7-007` · **Correct**

A developer is exploring two different strategies for decomposing the monolith's order processing module: (1) splitting by business capability (orders, payments, shipping) or (2) splitting by data ownership (order-db, payment-db, shipping-db). They want to explore both approaches in parallel without losing either analysis. What is the correct Claude Code approach?

- **A)** Use --resume to alternate between the two strategies in a single session, relying on conversation history to separate the analyses
  --resume continues a single linear session. Alternating between strategies in one context risks cross-contamination where analysis from one approach influences the other. fork_session provides clean isolation for parallel exploration.
- **B)** Instruct the agent to evaluate both strategies sequentially in the same session, then compare results
  Sequential evaluation in a single session means the first strategy's analysis occupies context when exploring the second, potentially biasing the comparison. fork_session allows true parallel exploration with isolated contexts.
- **C)** Open two terminal tabs and run separate Claude Code sessions with different instructions in each
  Separate sessions do not share the baseline context of the current analysis. Both explorations would need to re-do the initial codebase discovery, wasting time and losing the shared foundation.
- **D)** Use fork_session to create two parallel exploration branches from the current session's baseline, one for each decomposition strategy
  fork_session creates independent branches from a shared baseline. Both branches inherit the current codebase analysis and context but can diverge independently to explore different strategies. Neither branch's exploration affects the other, and both analyses are preserved.

**Correct answer:** D

**Where this comes from**
- Lesson 1.3: Subagent Invocation and Context Passing (fork_session)
- Lesson 1.7: Session State and Resumption (Session management options)

---

## Question 38
`D2 · 2.5` — *Developer Productivity Tools* — built-in-tools / edit-recovery · `q-2-5-002` · **Correct**

A developer is using Claude Code to update a configuration value in a file. They use the Edit tool, but it fails because the text they are trying to match appears in three places in the file. What is the correct next step?

- **A)** Use Glob to find all files containing the configuration value, then edit each one individually.
  Glob searches file paths, not file contents. It cannot find files containing a specific value. Additionally, the problem is within a single file, not across multiple files.
- **B)** Fall back to Read to load the full file, then Write the complete modified file.
  The exam guide names Read + Write as the documented fallback when Edit cannot find unique anchor text: load the full file with Read, then Write the complete modified file. That is the recovery path the exam tests for a non-unique match.
- **C)** Switch to using Bash with sed to perform the replacement, as it handles multiple matches natively.
  Sed bypasses the built-in tool designed for this task and may introduce errors with special characters. The exam expects the built-in tool sequence, which for a non-unique Edit failure is Read + Write.
- **D)** Use Grep to find which of the three occurrences is the correct one, then provide more surrounding context to Edit to make the match unique.
  Widening the anchor until it is unique, or using replace_all, is what current Claude Code documents and is sound engineering. It is not the fallback the exam guide names, and the guide is what this item tests: a non-unique Edit failure routes to Read + Write. See the lesson's current-state note for the divergence.

**Correct answer:** B

*(Same guide-vs-current-docs divergence as Q30: the guide wants Read + Write; current Claude Code docs would favor widening the match context, option D.)*

**Where this comes from**
- Lesson 2.5: Built-in Tools (Edit tool)
- Claude Code: Built-in Tools

---

## Question 39
`D4 · 4.4` — *Structured Data Extraction Pipeline* — validation-retry / retry-with-error · `q-4-4-002` · **Correct**

Your extraction pipeline retries failed documents, but the retry simply resends the original document with the same prompt. Success rates on retries are only marginally better than the first attempt. Developers have identified that most failures are format mismatches where the model places values in the wrong fields. How should you improve the retry mechanism?

- **A)** Skip retries altogether and route every failure directly to human review, so no API cost is wasted on a retry.
  Format mismatches are fixable errors. The model can self-correct when given proper error feedback. Skipping retries wastes the model's self-correction capability for errors that are resolvable.
- **B)** Send the original document, the failed extraction, and the validation error naming the misplaced fields.
  Retry-with-error-feedback is dramatically more effective than naive retries. Sending the original document, the failed extraction, and the specific validation error allows the model to self-correct. Format mismatches are fixable errors that respond well to this approach.
- **C)** Switch to a different model for retries so a fresh perspective catches the errors
  The issue is not the model but the absence of error context. Any model retrying without seeing the specific validation error will likely repeat the same mistakes.
- **D)** Increase the number of retries from 1 to 3, since extraction is non-deterministic and more attempts improve odds
  Naive retries without error feedback produce the same mistakes. More attempts at the same flawed approach yield diminishing returns. The model needs to see what went wrong.

**Correct answer:** B

**Where this comes from**
- Lesson 4.4: Validation, Retry, and Feedback Loops (Retry with error feedback)
- Lesson 4.4: Validation, Retry, and Feedback Loops (Self-correction flow)

---

## Question 40
`D2 · 2.5` — *Developer Productivity Tools* — built-in-tools / grep-then-edit · `q-2-5-006` · **Correct**

An engineering team needs to update all references to a renamed API endpoint across their 500,000-line codebase. They know the old endpoint name (POST /api/v1/users/create) but not which files reference it. After locating the files, they need to replace the old endpoint with the new one (POST /api/v2/users). What is the correct tool sequence?

- **A)** Use Bash with sed to perform a global find-and-replace across all files in a single command.
  A global sed command bypasses the built-in tools designed for this task and risks unintended modifications without the ability to review each change. Edit provides targeted modifications with unique text matching for safety.
- **B)** Use Read on the API router file to find all of the endpoint definitions, then trace each of the references through by hand.
  This approach only finds where the endpoint is defined, not where it is referenced. It also requires knowing which file contains the router definition, and manual tracing is unreliable across a large codebase.
- **C)** Grep for '/api/v1/users/create' to find every file with the old endpoint, then use Edit to replace it in each match.
  Grep searches file contents across the entire codebase, locating all references regardless of file type or location. Edit then makes targeted replacements in each matched file. This is the minimal, precise approach.
- **D)** Use Glob for '**/*.md' to find all documentation files, then Read each one to check for the old endpoint, then use Edit to update matches.
  Glob finds files by path pattern, but the endpoint reference could appear in any file type, not just Markdown. Reading every documentation file to search for the string wastes context tokens on irrelevant files.

**Correct answer:** C

**Where this comes from**
- Lesson 2.5: Built-in Tools (Grep for content)
- Lesson 2.5: Built-in Tools (Edit replacements)

---

## Question 41
`D2 · 2.4` — *Developer Productivity Tools* — mcp-server-integration / build-vs-use · `q-2-4-001` · **Correct**

A team needs to integrate with Jira for issue tracking in their Claude Code workflow. A developer proposes building a custom MCP server. What is the correct first step?

- **A)** Add the Jira integration to ~/.claude.json so each developer can configure it independently.
  A team-wide integration should be in project-level .mcp.json so it is version-controlled and shared. User-level ~/.claude.json is for personal/experimental servers.
- **B)** Evaluate existing community MCP servers for Jira and only build custom if they cannot handle team-specific workflows.
  Community servers should always be the first choice for standard integrations. They are maintained, tested, and cover common use cases. Custom builds are justified only when community servers cannot handle team-specific requirements.
- **C)** Use the Jira REST API directly from Bash commands instead of MCP.
  Direct API calls bypass the MCP tool interface, losing the benefits of tool descriptions, structured responses, and agent-native integration.
- **D)** Build a custom MCP server with the exact API endpoints the team needs.
  Building custom is premature. Community MCP servers for Jira already exist and cover standard use cases. Custom builds should be reserved for team-specific workflows.

**Correct answer:** B

**Where this comes from**
- Lesson 2.4: MCP Server Integration (Build-vs-use)
- Claude Code: MCP Server Configuration

---

## Question 42
`D3 · 3.2` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — slash-commands-skills / skills-placement · `q-3-2-014` · **Correct**

The team creates a reusable /extract-service skill that guides Claude Code through the standard steps of extracting a module from the monolith into a microservice (identify boundaries, create service scaffold, migrate code, update call sites, add tests). Where should this skill be stored so that every team member who clones the repository has access?

- **A)** In ~/.claude/skills/ on each developer's machine, distributed via the team wiki
  ~/.claude/skills/ is user-scoped and not version-controlled. Distributing via wiki requires manual copying and creates drift between developers' versions. The requirement is automatic availability on clone.
- **B)** In a shared MCP server that all team members connect to
  MCP servers provide tool integrations and external data access, not reusable prompt-based workflows. A skill file is the correct mechanism for a guided multi-step procedure.
- **C)** In the repository-root CLAUDE.md as an inline procedure
  CLAUDE.md is for always-loaded standards, not on-demand workflows. An extraction procedure is invoked when needed, not applied to every session. Placing it in CLAUDE.md wastes tokens when developers are not extracting services.
- **D)** In the repository's .claude/skills/ directory, committed to version control
  .claude/skills/ is project-scoped and version-controlled. When any team member clones the repository, the skill is automatically available as a /extract-service command. Updates to the skill flow through normal git pull, ensuring all developers have the same version.

**Correct answer:** D

**Where this comes from**
- Lesson 3.2: Custom Slash Commands and Skills (Project skill scoping)
- Claude Code: Skills

---

## Question 43
`D2 · 2.5` — *Developer Productivity Tools* — built-in-tools / grep-vs-glob · `q-2-5-001` · **Correct**

A developer needs to find all files that call a deprecated function processLegacyOrder() and also find all test files for those callers. Which tool sequence is correct?

- **A)** Glob for '*processLegacyOrder*' to find the callers, then Grep the results for the matching test files.
  Glob matches file paths, not file contents. It cannot find function callers — it would only match files named after the function, which is unlikely.
- **B)** Bash with 'find . -name "*.ts" | xargs grep processLegacyOrder' for the callers and again for the tests.
  While technically functional, this bypasses the built-in tools designed for these tasks. The exam expects candidates to use the right built-in tool for each task.
- **C)** Grep for 'processLegacyOrder' to find the callers, then Glob to match their test files by name.
  Grep searches file contents, which is correct for finding function callers. Glob matches file paths, which is correct for finding test files by naming pattern such as **/*.test.tsx. This is the optimal two-step sequence.
- **D)** Read every source file to search for the function calls, then Read every test file to confirm the callers.
  Reading all files upfront is a context-budget killer. It consumes tokens on irrelevant files and is the exact anti-pattern the exam penalises.

**Correct answer:** C

**Where this comes from**
- Lesson 2.5: Built-in Tools (Grep vs Glob)
- Claude Code: Built-in Tools

---

## Question 44
`D2 · 2.3` — *Developer Productivity Tools* — tool-distribution-choice / scoped-cross-role · `q-2-3-001` · **Correct**

A synthesis agent frequently returns control to the coordinator for simple fact verification, adding 2-3 round trips per task and 40% latency. Analysis shows 85% of verifications are simple lookups. What is the most effective solution?

- **A)** Add a coordinator-level cache of verification results so repeated lookups return instantly, removing most of the round-trip latency.
  Caching helps with repeated lookups but does not address the fundamental round-trip overhead for first-time verifications, which are the majority.
- **B)** Give the synthesis agent a scoped verify_fact tool for simple lookups, escalating only complex checks to the coordinator.
  A scoped cross-role tool handles the 85% simple case directly, eliminating round-trip latency. Complex cases still route through the coordinator for proper handling.
- **C)** Increase the coordinator's parallelism so it can process the queued verification requests faster and absorb the extra round trips.
  Faster processing does not eliminate unnecessary round trips. The latency comes from the routing overhead itself, not the coordinator's speed.
- **D)** Remove fact verification from the synthesis workflow altogether, which eliminates both the round trips and the latency they add.
  Removing verification compromises output quality. The goal is to make verification faster, not to skip it.

**Correct answer:** B

**Where this comes from**
- Lesson 2.3: Tool Distribution and Tool Choice (Scoped cross-role tools)

---

## Question 45
`D1 · 1.3` — *Content Moderation and Classification System* — subagent-invocation-context / parallel-spawning · `q-1-3-010` · **Correct**

A user reports a post that contains both potentially defamatory text and an embedded image that may violate graphic content policies. The coordinator receives this report as a single moderation request. What is the correct delegation strategy?

- **A)** Route the text to the text classifier and the image to the image analyser in parallel, then aggregate both results for the final decision.
  The coordinator should decompose multi-concern requests into independent subtasks. Text defamation and image policy violations are separate analysis dimensions that can be evaluated in parallel. The coordinator aggregates the results to make a unified moderation decision.
- **B)** Spawn a new combined text-and-image subagent for multi-modal reports so one specialist owns the whole decision rather than splitting it in two.
  Creating a new combined subagent duplicates capability that already exists in the specialist subagents. The coordinator's role is to decompose and delegate, not to spawn new agents for every combination of concerns.
- **C)** Send the entire report to the text classifier first, then forward its output to the image analyser so the image step runs only after the text step has finished.
  Sequential processing creates unnecessary latency when the two concerns are independent. The text and image analyses do not depend on each other and can run in parallel.
- **D)** Triage the whole report to whichever subagent handles the more severe category, so the moderation decision reflects the worst violation present.
  Severity cannot be determined until both analyses are complete, so there is nothing to triage on. Routing to a single subagent also means one concern goes unanalysed.

**Correct answer:** A

**Where this comes from**
- Lesson 1.3: Subagent Invocation and Context Passing (Parallel spawning)
- Lesson 1.4: Workflow Enforcement and Handoff (Multi-concern request handling)

---

## Question 46
`D5 · 5.6` — *Structured Data Extraction Pipeline* — information-provenance / claim-source-mapping · `q-5-6-003` · **Correct**

A data extraction pipeline extracts financial figures from annual reports. The pipeline cites sources using inline text references like 'According to page 12 of the 2024 Annual Report, revenue was $4.2B.' When the extracted data is consumed by a downstream analytics system, the source attribution is consistently lost. What is the root cause and fix?

- **A)** The downstream system needs to be modified to preserve all input text verbatim without any transformation
  Requiring downstream systems to preserve verbatim text is impractical and fragile. Systems legitimately need to transform, aggregate, and restructure data. Attribution should be in a format that survives transformation.
- **B)** Inline prose citations are fragile. Fix by outputting structured claim-source mappings pairing each value with source, page, and date.
  Structured claim-source mappings survive downstream processing because they are data fields, not prose. An analytics system can consume {'value': '4.2B', 'source': '2024 Annual Report', 'page': 12} without losing attribution, whereas it will discard 'According to page 12...' during text processing.
- **C)** Add a separate attribution database keyed by value hash that the downstream system queries to look up the source for any extracted figure.
  While a database could store attributions, this adds unnecessary infrastructure when the extraction pipeline can simply output structured mappings directly. The attribution should travel with the data, not require a separate lookup.
- **D)** The downstream system strips text formatting. Fix by making the citations bold or using a special delimiter
  The problem is not formatting but data structure. Regardless of text formatting, inline prose citations are lost when text is parsed, summarised, or restructured by downstream systems.

**Correct answer:** B

**Where this comes from**
- Lesson 5.6: Information Provenance and Multi-Source Synthesis (Structured claim-source mappings)

---

## Question 47
`D5 · 5.5` — *Structured Data Extraction Pipeline* — human-review-calibration / per-field-calibration · `q-5-5-005` · **Correct**

A contract extraction system reports 96% overall accuracy. The team plans to auto-approve all extractions where model confidence exceeds 90%. A pilot reveals party name extraction achieves 99% accuracy but indemnification clause extraction only 71%, even though the model reports high confidence on both. What should they implement before automating?

- **A)** Train a separate classification model to predict extraction accuracy before deciding whether to automate each extraction.
  A separate model adds infrastructure complexity when the solution is to calibrate the existing confidence scores against labelled data. Calibration directly addresses the unreliable confidence outputs without requiring additional ML infrastructure.
- **B)** Calibrate confidence thresholds per field type using labelled validation sets, and implement stratified sampling to continuously monitor accuracy by document type and field segment.
  Field-level confidence calibration using ground truth data exposes the discrepancy between reported confidence and actual accuracy. Stratified sampling provides ongoing monitoring to detect novel error patterns. Together, these ensure automation is only applied where validated accuracy justifies it.
- **C)** Exclude indemnification clauses from automation entirely and continue automating all other field types at the 90% threshold.
  This addresses the known problem but does not detect future calibration issues with other field types. Without systematic calibration and monitoring, other fields with hidden accuracy problems will be automated incorrectly.
- **D)** Raise the automation confidence threshold from 90% to 99% to ensure only the most reliable extractions are automated.
  Raising the threshold does not fix the calibration problem. The model reports high confidence even for indemnification clauses where it achieves only 71% accuracy. Raw confidence scores are unreliable without calibration.

**Correct answer:** B

**Where this comes from**
- Lesson 5.5: Human Review and Confidence Calibration (Field-level calibration)
- Lesson 5.5: Human Review and Confidence Calibration (Stratified sampling)

---

## Question 48
`D4 · 4.4` — *Structured Data Extraction Pipeline* — validation-retry / retry-with-error · `q-4-4-007` · **Correct**

Your extraction pipeline has a validation step that checks extracted financial data. When validation fails, the system retries by sending just the original document with the same prompt. Retry success rates are below 10%. The most common failure is the model placing the 'net amount' value in the 'gross amount' field and vice versa. How should the retry be restructured?

- **A)** Add a post-processing rule that automatically swaps net and gross amounts when validation detects the pattern
  Hard-coded swap rules are brittle and mask the underlying extraction error. They also fail if the issue manifests differently in other documents. Error feedback teaches the model to extract correctly.
- **B)** Switch to a different model for the retry, since the original model has a persistent field-mapping bias
  The issue is the absence of error context in the retry, not a model-specific bias. Any model retrying without seeing the specific validation error will have a low success rate.
- **C)** Increase retries from 1 to 5, since more attempts at the same prompt will eventually produce the correct field mapping by chance
  If the model consistently maps fields incorrectly with the same prompt, more retries without feedback will produce the same incorrect mapping. The model needs to see its specific error.
- **D)** Send the original document, the failed extraction, and the specific validation error naming the swapped fields.
  Retry-with-error-feedback is dramatically more effective than naive retries. The model seeing its specific mistake (net and gross amounts swapped) and the validation error allows targeted self-correction rather than repeating the same misinterpretation.

**Correct answer:** D

**Where this comes from**
- Lesson 4.4: Validation, Retry, and Feedback Loops (Retry with error feedback)
- Lesson 4.4: Validation, Retry, and Feedback Loops (Self-correction flow)

---

## Question 49
`D3 · 3.2` — *Developer Productivity Tools* — slash-commands-skills / skills-frontmatter · `q-3-2-013` · **Incorrect**

A team has a /deploy-check skill that verifies deployment readiness. It needs to: (1) read configuration files across the repo, (2) run bash commands to check service health, (3) produce a lengthy multi-page report, and (4) never modify any source code. The skill should be available to the entire team. Which SKILL.md configuration satisfies all four requirements?

- **A)** Place in .claude/skills/ with allowed-tools: ["Read", "Grep", "Glob", "Bash"]
  This configuration is missing context: fork. Without it, the lengthy multi-page deployment report would clutter the main conversation context, violating requirement 3.
- **B)** *(your answer)* Place in .claude/skills/ with allowed-tools: ["Read", "Grep", "Glob"] and context: fork
  This configuration excludes Bash, which is needed for running service health check commands (requirement 2). Without Bash access, the skill cannot verify that services are running and responsive.
- **C)** Place in ~/.claude/skills/ with allowed-tools: ["Read", "Grep", "Glob", "Bash", "Write"] and context: fork
  Two problems: ~/.claude/skills/ is user-scoped, not shared with the team. Including Write in allowed-tools violates the requirement that the skill must never modify source code.
- **D)** *(correct answer)* Place in .claude/skills/ with allowed-tools: ["Read", "Grep", "Glob", "Bash"] and context: fork
  The skill is in .claude/skills/ for team access (requirement 4 via version control). allowed-tools includes Read, Grep, and Glob for reading configuration files (requirement 1), Bash for running health check commands (requirement 2), and excludes Write and Edit to prevent source code modification (requirement 4). context: fork isolates the lengthy report from the main conversation (requirement 3). Current state (checked 14 August 2026): the live skills reference defines `allowed-tools` as "Tools Claude can use without asking permission during the turn that invokes this skill", with `disallowed-tools` removing tools from the pool. The exam guide frames it as restricting access, so answer that on the exam.

**Correct answer:** D
**Your answer:** B ✗

**Where this comes from**
- Lesson 3.2: Custom Slash Commands and Skills (Skills frontmatter)
- Claude Code: Skills

---

## Question 50
`D3 · 3.5` — *Developer Productivity Tools* — iterative-refinement / interview-pattern · `q-3-5-004` · **Incorrect**

A developer is new to a healthcare compliance domain and needs to build an audit logging system. They understand the technical implementation options but are unsure about regulatory requirements that might affect the design. Which Claude Code workflow technique is most appropriate?

- **A)** Start with direct execution using a simple implementation and iterate based on test failures
  Iterating from test failures works when the requirements are known and tests can be written upfront. Healthcare compliance requirements that the developer does not know about cannot be captured in tests. Missing a regulatory requirement is not something that shows up as a test failure.
- **B)** *(correct answer)* Use the interview pattern so Claude asks clarifying questions about compliance requirements, data retention policies, and access control needs before proposing a design
  The interview pattern is specifically designed for unfamiliar domains where the developer might miss important considerations. By having Claude ask probing questions about regulatory requirements, the developer surfaces constraints they might not have considered, leading to a more compliant design.
- **C)** Provide concrete input/output examples of the desired audit log format and let Claude implement it
  Concrete examples fix inconsistent interpretation of known transformations. The developer's problem is not inconsistency but rather gaps in domain knowledge about regulatory requirements. Examples cannot surface unknown compliance considerations.
- **D)** *(your answer)* Use plan mode to have Claude explore the codebase and propose multiple audit logging architectures
  Plan mode is for evaluating implementation strategies when the requirements are understood. The developer's gap is in domain requirements (regulatory compliance), not in technical approach selection.

**Correct answer:** B
**Your answer:** D ✗

**Where this comes from**
- Lesson 3.5: Iterative Refinement Techniques (Technique hierarchy)
- Lesson 3.5: Iterative Refinement Techniques (When to use each technique)

---

## Question 51
`D1 · 1.5` — *Developer Productivity Tools* — agent-sdk-hooks / pretooluse-hooks · `q-1-5-013` · **Correct**

A developer-tool agent writes code and runs shell commands. A system prompt instruction ('Do not run destructive commands or access files outside the project') is violated 3% of the time in testing. The team requires this rule to hold absolutely. What should the architect implement?

- **A)** Implement PostToolUse hooks that detect and roll back destructive commands after they execute
  PostToolUse hooks run after execution. By the time a PostToolUse hook detects 'rm -rf', the files are already deleted. Destructive commands cannot be reliably rolled back. Prevention via PreToolUse is required, not post-execution detection.
- **B)** Remove the shell execution tool entirely to prevent any possibility of destructive commands
  Removing shell execution eliminates the agent's ability to run any commands, including legitimate ones needed for its development workflow. The correct approach is surgical — block specific dangerous patterns while allowing legitimate usage.
- **C)** PreToolUse hooks that scan shell commands for destructive patterns and validate file paths before execution.
  PreToolUse hooks intercept tool calls before execution. A hook can pattern-match against destructive commands like 'rm -rf' and validate that file paths fall within the project directory, blocking any violation with 100% reliability. This is deterministic enforcement for a safety-critical requirement.
- **D)** Strengthen the system prompt with more specific examples of forbidden commands and add few-shot demonstrations
  The prompt already fails 3% of the time. Strengthening it may reduce the failure rate but cannot eliminate it. Destructive operations require 100% prevention, which only deterministic enforcement can guarantee.

**Correct answer:** C

**Where this comes from**
- Lesson 1.5: Agent SDK Hooks (PreToolUse hooks)
- Anthropic: Agent SDK Hooks

---

## Question 52
`D2 · 2.1` — *Developer Productivity Tools* — tool-schema-design / system-prompt · `q-2-1-002` · **Correct**

An agent has two tools: `analyze_content` ('Analyses content') and `extract_web_results` ('Extracts data from web pages'). After a system prompt update added 'Always analyse content before responding', the agent started routing web-extraction tasks to `analyze_content` despite the unchanged descriptions. What is the most likely cause and fix?

- **A)** The tool descriptions have degraded over time and need to be rewritten with clearer boundaries between the two tools.
  The question states tool descriptions were not changed and routing was correct before the system prompt update. The descriptions are not the root cause — the new system prompt instruction is.
- **B)** The analyze_content tool should be renamed to something less generic, such as summarize_document, to avoid all future conflicts.
  Renaming is a valid longer-term improvement but does not address the immediate cause: the system prompt instruction creating a keyword match. The prompt conflict would persist with any tool whose name overlaps with prompt wording.
- **C)** The tool descriptions need few-shot examples added to the system prompt showing when to use each tool.
  Few-shot examples add token overhead and do not address the root cause. The system prompt instruction is directly triggering the wrong tool via keyword association, and adding more content to the system prompt may compound the issue.
- **D)** The system prompt's 'analyse content' phrasing keyword-matches the analyze_content tool; rephrase it to remove the overlap.
  Keyword-sensitive instructions in system prompts can create unintended tool associations that override well-written descriptions. The phrase 'analyse content' directly matches the tool name, so the model favours it regardless of the task. The fix is to review and rephrase the system prompt after any update.

**Correct answer:** D

**Where this comes from**
- Lesson 2.1: Tool Interface Design (System prompt interactions)

---

## Question 53
`D3 · 3.1` — *Developer Productivity Tools* — claude-md-hierarchy / hierarchy · `q-3-1-005` · **Correct**

A consultancy works across 12 client projects simultaneously. Each developer has personal preferences (editor keybindings, alias shortcuts) and the consultancy has firm-wide coding standards. Each client project has its own specific conventions. Some client projects have subsystems with additional specialised rules. What is the correct configuration architecture?

- **A)** User ~/.claude/CLAUDE.md for personal preferences; project .claude/CLAUDE.md for firm-wide standards and client conventions; directory-level CLAUDE.md or .claude/rules/ with paths for subsystem rules
  Personal preferences are per-developer, so they live at user level, which is not shared via version control. Firm-wide standards and client conventions must reach everyone who works on a project, so they belong at the project level, which is committed to the repository and distributed on clone; firm-wide standards can be kept in a shared file and pulled into each project's CLAUDE.md with an @import to stay modular. Putting shared standards at the user level is the classic hierarchy bug, where a colleague who clones a project would not receive them. Subsystem rules belong at the directory level or in path-scoped .claude/rules/.
- **B)** A single CLAUDE.md at the root of each project containing all four levels of configuration, with clear section headings
  Combining all configuration levels into a single file defeats the purpose of the hierarchy. Personal preferences would be version-controlled and shared with the team, firm-wide standards would need duplication across 12 projects, and the file would be bloated with subsystem rules that only apply to specific directories.
- **C)** User ~/.claude/CLAUDE.md for personal preferences and firm-wide standards; project .claude/CLAUDE.md for client-specific conventions; directory-level CLAUDE.md or .claude/rules/ with paths for subsystem-specific rules
  User-level ~/.claude/CLAUDE.md applies only to the individual developer and is not shared via version control. Placing firm-wide standards there means a colleague who clones a client project does not receive them, which is the classic configuration-hierarchy bug. Shared standards belong at the project level.
- **D)** User ~/.claude/CLAUDE.md for everything; use @ path imports to pull in project-specific files from each repository
  User-level CLAUDE.md loads for every session across all projects. Importing 12 client project configurations into the user-level file would load all client conventions for every project, wasting tokens and causing conflicting instructions.

**Correct answer:** A

**Where this comes from**
- Lesson 3.1: CLAUDE.md Hierarchy and Scoping (Three-level hierarchy)
- Lesson 3.1: CLAUDE.md Hierarchy and Scoping (.claude/rules/)

---

## Question 54
`D4 · 4.3` — *Structured Data Extraction Pipeline* — structured-output / tool-choice-forcing · `q-4-3-006` · **Correct**

Your data extraction pipeline uses tool_use with tool_choice set to 'auto'. You need guaranteed structured output for every request, but some documents occasionally produce conversational text responses instead. You have only one extraction tool defined. What is the most reliable fix?

- **A)** Set tool_choice to force the specific extraction tool by name
  Setting tool_choice to {type: 'tool', name: 'extract_data'} forces the model to call that specific tool on every request, guaranteeing schema-compliant structured output with no possibility of text-only responses.
- **B)** Add a system prompt instruction: 'You must always use the extraction tool and never produce text responses'
  System prompt instructions cannot guarantee tool use when tool_choice is 'auto'. The API-level tool_choice parameter is the authoritative mechanism.
- **C)** Switch to prompt-based JSON extraction with strict formatting instructions for more predictable output
  Prompt-based JSON is less reliable than tool_use. It risks syntax errors and missing fields. Forcing the tool via tool_choice is the correct approach.
- **D)** Add a post-processing step that retries any request returning text instead of a tool call
  Retrying with the same 'auto' tool_choice may produce the same text response. Fixing tool_choice eliminates the problem at the API level rather than patching it after the fact.

**Correct answer:** A

**Where this comes from**
- Lesson 4.3: Structured Output with Tool Use (tool_choice modes)
- Anthropic: Tool Use Documentation

---

## Question 55
`D5 · 5.1` — *(no scenario tag in source)* — context-window-management / lost-in-the-middle · `q-5-1-008` · **Correct**

Claude Code is synthesising release notes from commit messages, PR descriptions, and changelog entries. During a 200+ commit session, summaries of early commits become vague ('various bug fixes') while recent commits are still detailed accurately. The context window is not full. What is the most likely cause?

- **A)** Claude Code applies progressive summarisation to older commits to conserve context for recent ones
  Claude Code does not automatically apply progressive summarisation to tool results within a single processing step. The context window is not full, so there is no space pressure triggering summarisation. The issue is attention distribution across long inputs.
- **B)** The commit messages for early commits are inherently less detailed than recent ones, so the vague summaries are accurate
  The question states the vagueness applies to early commits specifically, not commits with poor messages. The systematic pattern (early = vague, recent = detailed) points to a context positioning effect, not source quality variation.
- **C)** The lost-in-the-middle effect: the model favours the start and end of long input, losing middle commit detail.
  The lost-in-the-middle effect is a well-documented phenomenon where models attend more strongly to the start and end of long contexts, with reduced attention to middle content. With 200+ commits loaded sequentially, commits in the middle of the sequence receive less attention, producing vague summaries. Processing in smaller batches or reordering critical information to the start and end mitigates this.
- **D)** The model's temperature is set too high, causing it to generate vague summaries randomly
  Temperature affects output randomness but would produce inconsistent quality across all commits, not a systematic pattern where early commits are vague and recent commits are accurate.

**Correct answer:** C

**Where this comes from**
- Lesson 5.1: Context Window Management (Lost in the middle)

---

## Question 56
`D4 · 4.3` — *Structured Data Extraction Pipeline* — structured-output / tool-choice-forcing · `q-4-3-002` · **Correct**

Your legal document extraction pipeline uses tool_use with tool_choice set to 'auto'. The pipeline processes contracts and sometimes receives plain text analysis instead of the structured JSON extraction you need. The team suggests switching to prompt-based JSON with explicit formatting instructions. What is the correct approach?

- **A)** Keep tool_use but switch tool_choice from 'auto' to 'any' to guarantee the model always returns a structured tool call
  While 'any' guarantees a tool call, it lets the model choose which tool. If you have multiple tools defined, the model might call the wrong one. For a single extraction tool, this works, but the most precise solution is to force the specific extraction tool.
- **B)** Add stronger instructions in the system prompt telling the model to always use the extraction tool and never respond with plain text
  Instructions alone cannot guarantee tool use when tool_choice is 'auto'. The API-level tool_choice parameter is the correct mechanism for enforcing structured output, not prompt instructions.
- **C)** Switch to prompt-based JSON as suggested, since the model clearly prefers text responses for these documents
  Prompt-based JSON is less reliable than tool_use and can produce malformed output. The issue is tool_choice configuration, not the tool_use mechanism itself.
- **D)** Keep tool_use and set tool_choice to force the specific extraction tool by name, guaranteeing structured output on every request.
  Forcing a specific tool with tool_choice {type: 'tool', name: 'extract_contract'} guarantees the model calls that exact tool every time, eliminating both text-only responses and wrong-tool selection. This is the most reliable approach for guaranteed structured output.

**Correct answer:** D

**Where this comes from**
- Lesson 4.3: Structured Output with Tool Use (tool_choice forcing)
- Anthropic: Tool Use Documentation

---

## Question 57
`D1 · 1.3` — *Large-Scale Codebase Refactoring with Multi-Agent Claude Code* — subagent-invocation-context / goal-oriented-prompts · `q-1-3-018` · **Correct**

A coordinator delegates a large refactoring subtask to a specialist subagent, and the architect must write the subagent's prompt. Which prompt design should the architect use?

- **A)** Give an exact step-by-step procedure (open file X, change line 12, run command Y, then edit file Z) so the subagent cannot deviate
  A rigid procedure constrains the subagent and breaks the moment reality diverges from the script. The guide specifically warns against procedural instructions in favour of goal-oriented ones.
- **B)** Provide only the high-level goal with no success criteria, so the subagent has maximum freedom
  A goal with no quality criteria gives the subagent no way to know when it has actually succeeded. Effective goal-oriented prompts pair the objective with explicit success criteria.
- **C)** Omit the goal and instead list the tools the subagent may use, letting it infer the objective from the toolset
  Listing tools without stating the goal leaves the objective ambiguous, and the subagent may optimise for the wrong outcome. The prompt must state the goal.
- **D)** State the goal and its quality criteria (no breaking API changes, all tests pass) and let the subagent choose how to get there.
  Goal-oriented prompts specify what to achieve and the quality bar, not a fixed procedure. Pairing the objective with success criteria lets the subagent adapt its approach when it meets something unexpected, which is what the guide recommends.

**Correct answer:** D

**Where this comes from**
- Lesson 1.3: Subagent Invocation and Context Passing (Goal-oriented prompts)

---

## Question 58
`D3 · 3.4` — *Developer Productivity Tools* — plan-mode-execution / hybrid · `q-3-4-005` · **Correct**

A team is debugging a complex distributed system issue. The lead developer wants to use Claude Code to explore logs, trace request flows, and form hypotheses without making any changes to the codebase. Partway through the investigation, they identify a one-line fix in a configuration file and want to apply it immediately. What is the optimal workflow?

- **A)** Use direct execution throughout, with detailed upfront instructions describing both the investigation process and potential fix patterns
  Direct execution is inappropriate for the investigation phase because the problem and solution are not yet understood. Providing detailed upfront instructions assumes knowledge of the issue that the investigation is meant to discover.
- **B)** Start in plan mode for investigation, then switch to direct execution for the one-line fix once identified
  Plan mode is ideal for the investigation phase: exploring logs, tracing flows, and evaluating multiple hypotheses without committing to changes. Once the fix is identified and well-understood (a clear-scope, single-file change), switching to direct execution applies it efficiently without unnecessary planning overhead.
- **C)** Use allowedTools to restrict to read-only tools for investigation, then start a new session with write permissions for the fix
  Starting a new session for the fix would lose all the investigation context (log analysis, request tracing, hypothesis formation) that led to identifying the fix. Switching modes within the same session preserves this valuable context.
- **D)** Use plan mode for the entire session, including the one-line fix, to maintain consistency
  While plan mode is correct for investigation, continuing to use it for a well-understood one-line fix adds unnecessary overhead. Once the fix is identified and scoped, direct execution is the appropriate mode for a clear, limited change.

**Correct answer:** B

**Where this comes from**
- Lesson 3.4: Plan Mode vs Direct Execution (Hybrid plan then execute)

---

## Question 59
`D3 · 3.5` — *Developer Productivity Tools* — iterative-refinement / batch-vs-sequential · `q-3-5-002` · **Correct**

A developer is iterating on a data transformation function with Claude Code and has identified three issues: (1) date parsing mishandles timezone offsets, (2) currency formatting uses the wrong locale, and (3) the output JSON schema has an incorrect field name. Issues 1 and 2 are independent; issue 3 changes the output shape both must conform to. How should the developer provide feedback?

- **A)** Send all three issues in a single message to let Claude address them holistically
  Batching everything together is appropriate when all issues are interdependent. Here, issues 1 and 2 are independent of each other, and sending them together risks conflating the feedback for those fixes. The interdependency is only between issue 3 and the other two.
- **B)** Fix issue 3 (schema field name) first, then address issues 1 and 2 one at a time since they are independent
  Issue 3 changes the output schema that issues 1 and 2 must conform to, so it must be resolved first. Once the schema is correct, issues 1 and 2 are independent, so they are fixed one at a time rather than batched, since batching independent issues can confuse which feedback applies to which fix. This follows the principle: resolve dependencies first, batch when fixes interact, and sequence when independent.
- **C)** Send each of the three issues in a separate sequential message, waiting for confirmation after every single fix.
  Pure sequential iteration is appropriate when all issues are independent. Here, issue 3 (schema field name) affects the expected output that issues 1 and 2 must conform to. Fixing issues 1 and 2 first without correcting the schema would produce fixes targeting the wrong field name.
- **D)** Use the interview pattern to have Claude ask clarifying questions about all three issues before making any changes
  The interview pattern is for unfamiliar domains where the developer might miss considerations. Here, the developer has already identified the three specific issues and understands their interdependencies. The question is about feedback sequencing, not domain exploration.

**Correct answer:** B

**Where this comes from**
- Lesson 3.5: Iterative Refinement Techniques (Batch vs sequential)

---

## Question 60
`D1 · 1.5` — *Developer Productivity Tools* — agent-sdk-hooks / hooks-vs-prompts · `q-1-5-014` · **Incorrect**

A developer-tool agent working in a version-controlled project has two guardrails: a PreToolUse hook blocking file writes outside the project directory (enforced 100% of the time), and a system prompt instruction 'Always create a backup before overwriting existing files' (followed 88% of the time). A senior engineer wants all guardrails converted to hooks for consistency. What is the correct assessment?

- **A)** *(correct answer)* The directory restriction is rightly a hook; the backup instruction can stay a prompt because a missed backup is recoverable.
  The guardrail strategy should match the severity of the consequence. Writing outside the project directory could damage the host system — this demands deterministic enforcement via a hook. Missing a backup is inconvenient but recoverable (files are in version control). The 88% compliance rate from the prompt is acceptable for a non-critical best practice.
- **B)** *(your answer)* The senior engineer is correct: every guardrail, including the recoverable backup rule, should be converted to a deterministic hook for maximum reliability.
  Not all guardrails need deterministic enforcement. Converting everything to hooks adds implementation complexity for no benefit on recoverable rules. Match the enforcement mechanism to the severity of the requirement; a missed backup in version control is fine as a prompt.
- **C)** The backup instruction should be converted to a hook, because a 12% failure rate on any stated guardrail is too high to leave to the prompt.
  Whether 88% is acceptable depends on the consequences of failure. Missing a backup in a version-controlled codebase is recoverable, so 88% compliance is reasonable for a prompt-based best practice. The 12% failure rate does not justify the implementation complexity of a hook for a non-critical guideline.
- **D)** Both guardrails should be prompt instructions, since one enforcement mechanism is simpler to maintain than a mix of hooks and prompt rules.
  Prompt instructions for the directory restriction would have a non-zero failure rate for a safety-critical boundary. Writing outside the project directory could cause system damage. Safety-critical requirements must use deterministic hooks, not probabilistic prompts.

**Correct answer:** A
**Your answer:** B ✗

**Where this comes from**
- Lesson 1.5: Agent SDK Hooks (Hooks vs prompts)
- Lesson 1.5: Agent SDK Hooks (Decision framework)
