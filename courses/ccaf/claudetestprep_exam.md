# Claude Certified Architect – Foundations Exam Review

Source: `exam.txt` (post-exam review export, 60 questions). Formatted for study — no question, option, or explanation text has been altered or removed; only layout, grouping, and the notes below were added.

**Score:** 45 / 60 correct (15 wrong)

**Data-capture notes (from the raw export, not from me editing content):**
- Q23 and Q56 each appear multiple times in the source log, word-for-word identical. Shown once each here, noted at the question.
- Q24 and Q57 do not appear anywhere in the source log (the question numbering skips them). No content exists to format for these two.
- Q4's header block (topic tags) wasn't captured in the source, though its question/options/explanation were.
- Q11 (option D), Q12 (option C), and Q14 (option C) have no "why this fails" text in the source export — marked as *not captured* rather than invented.

---

## Missed questions at a glance

| Q# | Section | Topic | Your answer | Correct | 
|----|---------|-------|:---:|:---:|
| [1](#question-1) | S2 · Claude Code dev workflow | D3·3.3 rule loading | D | B |
| [3](#question-3) | S2 · Claude Code dev workflow | D5·5.1 lost-in-the-middle | A | C |
| [5](#question-5) | S2 · Claude Code dev workflow | D3·3.4 plan vs direct mode | C | B |
| [7](#question-7) | S2 · Claude Code dev workflow | D3·3.3 glob patterns | C | D |
| [11](#question-11) | S2 · Claude Code dev workflow | D3·3.6 `--bare` flag | C | B |
| [15](#question-15) | S2 · Claude Code dev workflow | D3·3.5 slash command examples | D | C |
| [20](#question-20) | S3 · Multi-agent research | D5·5.6 temporal metadata | B | D |
| [23](#question-23) | S3 · Multi-agent research | D5·5.2 ambiguous scope | C | A |
| [28](#question-28) | S3 · Multi-agent research | D2·2.4 custom MCP server | C | D |
| [38](#question-38) | S4 · Developer productivity tools | D2·2.2 error classification | D | B |
| [47](#question-47) | S6 · Structured data extraction | D4·4.6 confidence vs schema | D | B |
| [49](#question-49) | S6 · Structured data extraction | D4·4.6 second review pass | B | D |
| [50](#question-50) | S6 · Structured data extraction | D5·5.4 compaction persistence | C | B |
| [54](#question-54) | S6 · Structured data extraction | D5·5.2 sentiment as proxy | A | B |
| [56](#question-56) | S6 · Structured data extraction | D5·5.5 schema validation failure | A | C |

**By section:** S2 (Claude Code dev workflow) 6 wrong · S3 (Multi-agent research) 3 wrong · S4 (Developer productivity tools) 1 wrong · S6 (Structured data extraction) 5 wrong

**By domain:** D3 (Claude Code workflow mechanics) 5 · D5 (context/state management & synthesis judgment) 6 · D2 (tool design & error handling) 2 · D4 (schema/confidence calibration) 2

---

## S2 · Claude Code dev workflow

### Question 1
`D3 · 3.3`

Your team's CLAUDE.md references a rule file in .claude/rules/api-style.md with paths frontmatter scoped to src/api/**/*.ts. When exactly does Claude Code load this rule into the active context?

- A) When any tool call targeting a file under src/api/ is executed during the session
- B) When Claude reads a file matching src/api/**/*.ts during the session
- C) When a slash command explicitly references the api-style rule by name
- D) At session launch, alongside all other files in the .claude/rules/ directory

**Correct answer:** B
**Your answer:** D ✗

**Why B is correct**
The paths frontmatter binds api-style.md's activation to the src/api/**/*.ts glob, so the trigger is Claude actually reading a matching file's contents into context, not merely operating near that path. This is what keeps the rule dormant — and its tokens unspent — for the many sessions that never touch src/api/ TypeScript files.

**Why the others fail**
- A) A practitioner aware of path-scoped loading might conflate 'file in scope is touched' with 'file in scope is read.' Only a file-read matching the glob triggers the rule; writes, searches, or directory listings against src/api/ do not qualify, even when they target the same path.
- C) No slash command mechanism exists in Claude Code for explicitly invoking a named rule file; rule loading is automatic and glob-driven, not command-triggered. This conflates slash commands — which invoke user-defined or built-in actions — with the entirely separate path-scoped rule loading system.
- D) Rules without a paths field load unconditionally at session launch, so this is the correct behavior for any .claude/rules/ file lacking that frontmatter. A practitioner unfamiliar with conditional loading will default to this assumption and miss that the paths key converts an always-loaded rule into a conditionally loaded one.

---

### Question 2
`D3 · 3.5`

Your team's CLAUDE.md instructs Claude Code to reformat log entries into a structured JSON schema. Initial results are inconsistent. To apply iterative refinement, what is the most effective next step?

- A) Expand the prose description in CLAUDE.md to explain the desired JSON schema fields in more detail.
- B) Switch to plan mode so Claude proposes a transformation approach before executing any formatting changes.
- C) Create a slash command that re-runs the formatting task until Claude reports high confidence in the output.
- D) Add concrete before/after examples showing raw log input and the exact expected JSON output directly in CLAUDE.md.

**Correct answer:** D

**Why D is correct**
Log reformatting is a deterministic transformation, so the fastest route to consistency is pinning the exact input-to-output mapping: a raw log line paired with its target JSON. This removes the interpretive gap causing inconsistent results and gives Claude a pattern to match rather than a schema to infer, directly resolving the root cause named in the scenario.

**Why the others fail**
- A) Expand the prose description appeals when the schema feels underdocumented — more field definitions seem like tighter specification. Prose still requires Claude to interpret intent; it would be the right move if the gap were missing field-level context (e.g., nullable rules, enum constraints) rather than an absent demonstration of the input-to-output mapping itself.
- B) Switch to plan mode so Claude proposes delays execution in favor of an upfront proposal, which helps for architectural or multi-step decisions where surfacing assumptions matters. For a deterministic transformation task, the bottleneck is the example-free spec, not the absence of a planning phase; plan mode defers the problem without resolving it.
- C) Create a slash command that re-runs addresses loop mechanics: retry until confidence is high. This conflates iteration frequency with specification quality — running a poorly-specified task more times cannot resolve the underlying ambiguity. It would be appropriate once the spec is solid and the failure mode is non-determinism rather than misinterpretation.

---

### Question 3
`D5 · 5.1`

Your team uses Claude Code for a multi-hour refactor session. Midway through, the agent documents a critical constraint (a shared mutex in module X) in its working context, then continues through many files. Near the end, it reintroduces a race condition in module X. What change to your CLAUDE.md workflow best mitigates this lost-in-the-middle failure?

- A) Add a /checkpoint slash command under .claude/commands/ that summarizes progress and appends it to the running transcript.
- B) Increase the context window budget and instruct the agent in CLAUDE.md to re-read earlier tool outputs before editing.
- C) Record durable invariants like the module X mutex in CLAUDE.md so they are reloaded into every turn's context window.
- D) Switch long refactor sessions from direct execution to plan mode so the agent reviews its plan before each file edit.

**Correct answer:** C
**Your answer:** A ✗

**Why C is correct**
Because the mutex constraint was discovered mid-session rather than known upfront, it only survives future turns if promoted out of the decaying transcript into a fixed instruction Claude reloads every turn. CLAUDE.md content sits outside the eroding attention region entirely, so the invariant is re-asserted at full strength on the very file edits — including the late-session module X change — that triggered the regression.

**Why the others fail**
- A) "Add a /checkpoint slash command" appends a summary to the running transcript, placing it in the same middle region where attention already degrades — adding tokens rather than promoting the invariant to a persistent preamble. It is the right pattern for session handoffs or human-review milestones, not for guaranteeing mid-session invariant recall.
- B) "Increase the context window budget" treats the failure as hard truncation, but lost-in-the-middle is an attention-degradation effect that worsens as the window grows larger. Expanding the budget is the correct fix when critical content falls outside the context entirely, not when it sits inside the window but receives diminished attention.
- D) "Switch long refactor sessions" inserts a planning gate before each edit, reducing hasty changes but leaving the mutex constraint buried in the same degraded attention region. It is the right mitigation when the failure mode is premature or unchecked execution, not when a critical finding was formed mid-conversation and then lost.

---

### Question 4
*(Topic tags not captured in source export — this question's header block was missing, though its full content was present, positioned between Q3 and Q5.)*

Your team shares a project-level CLAUDE.md for shared conventions. Where should you store your personal coding style preferences so they apply across every project you open?

- A) In the project-level CLAUDE.md alongside team conventions
- B) In ./CLAUDE.local.md at each project root
- C) In ~/.claude/CLAUDE.md as user-level instructions
- D) In a .claude/rules/ file inside the project

**Correct answer:** C

**Why C is correct**
The user-level file at ~/.claude/CLAUDE.md lives outside any single repo and loads for every project session under that account, so it's the correct home for personal style preferences that must persist regardless of which project-level CLAUDE.md is checked out. It stays entirely outside source control, keeping individual taste separate from the team conventions the project-level file governs.

**Why the others fail**
- A) Practitioners who conflate personal and shared preferences reach for the project-level file because it's already open and authoritative. Project-level CLAUDE.md is the correct location for conventions every contributor should follow — but it's committed to source control, so personal style preferences added there become team mandates.
- B) CLAUDE.local.md is the correct pattern for personal, git-ignored overrides — but it is scoped to a single project root. Practitioners who know it stays out of source control reasonably guess it's the answer, missing that "across every project" requires the user-level file, not a per-root copy maintained in each repo.
- D) A .claude/rules/ path sounds like modular, private configuration, making it a plausible guess for practitioners familiar with Claude's config directory layout. It is project-scoped, not cross-project, and carries no personal-override semantics — a category mismatch for preferences meant to follow the user across all projects.

---

### Question 5
`D3 · 3.4`

A senior engineer needs to rename a single private helper function and its three call sites in one file, then run the existing test. She is debating whether to use plan mode or direct execution in Claude Code. The change is mechanical, the blast radius is one file, and the tests are fast. Which choice best fits this task?

- A) Plan mode, so Claude produces an explicit plan she approves before any edit lands.
- B) Direct execution in default mode, with the standard pre-edit approval prompt confirming each change.
- C) Auto-accept mode from the start so edits land without prompts, since the change is mechanical.
- D) Plan mode with --permission-mode plan set as the project default so every collaborator starts the same way.

**Correct answer:** B
**Your answer:** C ✗

**Why B is correct**
This task's scope is exactly what default mode is built for: a single file, three call sites, and a fast test suite give her full context in her head already, so per-edit approval is the right-sized checkpoint. She gets a confirmation gate before each change lands without paying for a planning round-trip that a one-file mechanical rename doesn't need.

**Why the others fail**
- A) "Plan mode, so Claude produces" an explicit plan sounds like the safe choice whenever pre-edit visibility matters. That pattern pays off for multi-file investigations or architectural refactors where understanding full scope before any edit is worth the planning round-trip; for a one-file mechanical rename it adds an extra approval cycle with no corresponding safety gain.
- C) "Auto-accept mode from the start" feels proportionate when the change is described as mechanical and the blast radius is bounded. Auto-accept is the right mode for CI pipelines or bulk throwaway scripts where interactive prompts would block automation; applying it to shared code bypasses the per-edit confirmation that provides a lightweight, low-friction safety check.
- D) "Plan mode with --permission-mode plan" as a project default looks like principled team hygiene — standardizing behaviour across collaborators. That default is appropriate for infra-as-code or safety-critical repos where every task carries architectural risk; forcing it across a mixed-workflow codebase imposes planning overhead on trivially small tasks and inverts the mode-selection logic for the majority of routine edits.

---

### Question 6
`D5 · 5.6`

Your team's /market-sizing slash command in .claude/commands/ synthesizes TAM estimates from analyst reports. For one segment, Gartner reports $4.2B and Forrester reports $6.8B, both from 2024. The command currently picks the higher figure and proceeds. How should you modify the command to handle such conflicts correctly?

- A) Surface both figures with source attribution and flag the discrepancy, leaving resolution to the human reviewer
- B) Select the more recent publication date, or the larger sample size if dates match, and cite that source
- C) Prompt the model to reason about which methodology is more credible and proceed with the chosen figure
- D) Average the two figures and cite both sources, noting the midpoint as a reasonable consensus estimate

**Correct answer:** A

**Why A is correct**
Presenting both the $4.2B and $6.8B figures with attribution keeps the disagreement visible instead of collapsing it, which matters because a $2.6B spread between two credible 2024 analyst reports is a substantive signal, not noise to be resolved automatically. This preserves provenance for downstream consumers and routes the judgment call to the human reviewer, who can weigh methodology or context the command itself cannot verify.

**Why the others fail**
- B) Select the more recent publication imposes a recency heuristic that sounds methodologically principled, and it would be appropriate when one source is materially stale (e.g., years apart). Here, both reports are from 2024 — the heuristic produces no clean tiebreak and masks a $2.6B substantive disagreement that recency cannot explain away.
- C) Prompt the model to reason about which methodology asks the LLM to adjudicate between two credible, peer-tier analyst firms — exactly the arbitration role the agent must not assume. A practitioner might reach for this believing chain-of-thought reasoning adds rigor, but the output is still an unverifiable model opinion substituting for a domain judgment that belongs to the human reviewer.
- D) Average the two figures appeals to a 'split the difference' instinct that feels neutral, but the midpoint ($5.5B) is a number neither Gartner nor Forrester published — it fabricates a synthetic datum while superficially citing both. This pattern would be correct only if the command's charter explicitly authorized interpolation and downstream consumers understood the figure was derived, not sourced.

---

### Question 7
`D3 · 3.3`

Your CLAUDE.md workflow applies a type-safety rule whenever Claude reads TypeScript or JavaScript files under src/. You want a single paths pattern in a .claude/rules/ file that matches both src/**/*.ts and src/**/*.js. Which pattern is correct?

- A) src/**/[ts,js]
- B) src/**/*.ts OR src/**/*.js
- C) src/**/*.[ts|js]
- D) src/**/*.{ts,js}

**Correct answer:** D
**Your answer:** C ✗

**Why D is correct**
Brace expansion expands to the full set of literal alternatives before matching, so src/**/*.{ts,js} is evaluated as exactly src/**/*.ts and src/**/*.js — matching TypeScript and JavaScript files under src/ and nothing else. This lets one paths entry in the rules file cover both extensions the type-safety rule needs, without a multi-pattern list or a character class that would fragment the extensions into single characters.

**Why the others fail**
- A) src/**/[ts,js] omits the dot-and-wildcard prefix that separates filename from extension, which a reader focused on the bracket contents might overlook. Like the character-class mistake in src/**/*.[ts|js], [ts,js] matches a single character from {t, s, ,, j} — not the strings ts or js — and no extension separator is present at all, making this a category mistake rather than a near-miss.
- B) src/**/*.ts OR src/**/*.js reads naturally as an English logical union and mirrors how some tools accept multiple patterns in CLI arguments or YAML sequences. OR is not a valid glob operator; it has no defined meaning in path-pattern syntax and would be treated as a literal string. A multi-entry pattern list (two separate patterns in an array) would be the correct structure if brace expansion were unsupported.
- C) src/**/*.[ts|js] looks plausible because square brackets are valid glob syntax, and practitioners familiar with regex may expect | to mean alternation inside them. In POSIX glob character classes, brackets match any single character in the set — so [ts|js] matches one character from {t, s, |, j}, not a full extension. Square-bracket character classes are correct for single-character alternatives like [ch] matching .c or .h files.

---

### Question 8
`D5 · 5.6`

A slash command in .claude/commands/ summarizes API migration guides from three sources into a single paragraph. A developer later disputes a claim in the summary but cannot determine which source it came from. What design prevents this provenance loss?

- A) Emit each summarized claim as a tagged object pairing the claim text with its originating source ID
- B) Log the source URLs in a separate summary file the developer can cross-reference manually
- C) Require the slash command to output a fixed number of claims to limit summarization scope
- D) Store the full text of all three sources in CLAUDE.md so the original content is always recoverable

**Correct answer:** A

**Why A is correct**
Tagging each claim with its originating source ID at generation time keeps the claim-source mapping structurally embedded in the output itself, so a disputed sentence in the summary resolves to one of the three guides without re-reading any of them. This survives the summarization step precisely because attribution is carried as data alongside the claim, not reconstructed after the fact from external notes or full-text stores.

**Why the others fail**
- B) Logging source URLs in a separate file breaks the claim-to-source link at the point of output, reducing attribution to a manual grep across three full documents. This approach is sufficient when summaries are informational only and no claim-level traceability is required.
- C) Requiring a fixed number of claims constrains output cardinality but is orthogonal to provenance — a bounded set of unattributed claims is still unattributed. Claim-count limits are a quality heuristic, not a structural solution to source-mapping loss.
- D) Storing full text in CLAUDE.md preserves the raw sources but creates no mapping between a specific output claim and the source that produced it — a developer still faces an N-source search problem for any disputed assertion. This pattern is appropriate when the goal is replayability or prompt injection of source material, not attribution tracing.

---

### Question 9
`D3 · 3.6`

Your team wants to call Claude Code from a CI pipeline without any interactive prompts. Which flag enables CLAUDE.md-configured Claude Code to run non-interactively and print its response?

- A) Use --bare to skip all configuration and run headless
- B) Use --permission-mode dontAsk to suppress all prompts
- C) Use --no-session-persistence to prevent interactive state
- D) Use -p to run Claude Code in non-interactive print mode

**Correct answer:** D

**Why D is correct**
The -p (--print) flag is the documented switch that keeps CLAUDE.md configuration loaded while suspending the interactive REPL, so the pipeline gets a single printed response and a clean exit — exactly the CI contract this scenario needs. Unlike flags that strip configuration or only touch permissions, -p directly changes the execution mode from interactive to non-interactive.

**Why the others fail**
- A) --bare skips all configuration and runs headless — a practitioner who conflates 'headless' with 'non-interactive' would reach for this. The adjacent correct use of --bare is when you explicitly want to bypass CLAUDE.md and project configuration, the opposite of what the scenario requires.
- B) --permission-mode dontAsk to suppress all prompts is attractive because CI pipelines must never block on permission dialogs. It controls whether tool-use requires approval, but does not switch Claude Code into non-interactive mode or cause it to print and exit.
- C) --no-session-persistence to prevent interactive state sounds plausible because CI environments are stateless by design. This flag does not exist in Claude Code's CLI; it is a category mistake that confuses session storage concerns with interactive/non-interactive execution mode.

---

### Question 10
`D3 · 3.4`

Your team is adopting Claude Code and must refactor a legacy authentication module spanning 12 files and three services. A junior engineer asks whether to run Claude Code in plan mode or direct execution. Which factor most justifies choosing plan mode for this task?

- A) Plan mode prevents Claude from running shell commands, reducing the risk of accidental deletions during refactoring across the 12 files in the legacy authentication module.
- B) Plan mode requires explicit approval before writing files, letting the team review the full change strategy before any edits land.
- C) Plan mode automatically creates a CLAUDE.md entry summarizing the refactor plan for future sessions.
- D) Plan mode switches the underlying model to Opus, improving reasoning quality for large architectural changes.

**Correct answer:** B

**Why B is correct**
A refactor spanning 12 files across three services carries high blast radius if Claude misjudges scope or interaction points; plan mode's write-gate surfaces the full proposed change set as a plan the team can inspect and correct before a single edit lands. That upfront checkpoint is what lets a junior engineer and reviewers validate approach against all three services rather than discovering scope errors mid-edit.

**Why the others fail**
- A) Plan mode does constrain Claude's action surface, making this feel directionally correct to someone who knows plan mode limits execution. The actual restriction covers all write tools — file edits, patch operations, content creation — not shell commands specifically; shell access is governed by a separate tool-permissions layer.
- C) A practitioner who knows CLAUDE.md persists architectural context across sessions might infer that plan mode's output lands there automatically. CLAUDE.md is manually maintained; plan mode produces a reviewable plan in the active conversation only. Capturing refactor decisions in CLAUDE.md afterward is genuine best practice, but it is a deliberate editorial step, not an automatic plan-mode behavior.
- D) Conflating plan mode with a reasoning-model upgrade is tempting because both concepts are associated with deliberate, high-quality output on complex tasks. Model selection (e.g., switching to Opus) is a separate, orthogonal configuration; plan mode is a write-restriction mechanism that operates independently of whichever model is active.

---

### Question 11
`D3 · 3.6`

A team's CI job invokes Claude Code headlessly with -p. The CLAUDE.md at the project root defines coding conventions. After switching to --bare -p, the generated code ignores those conventions. What explains this change?

- A) --bare forces Claude Code to use the global ~/.claude/CLAUDE.md instead of the project CLAUDE.md
- B) --bare disables CLAUDE.md auto-discovery, so the coding conventions are not injected into the CI session
- C) Headless mode (-p) always ignores CLAUDE.md; the conventions only applied in interactive sessions
- D) -p combined with --bare activates a restricted token budget that truncates CLAUDE.md injection

**Correct answer:** B
**Your answer:** C ✗

**Why B is correct**
The team's regression traces directly to --bare's context-loading behavior: it suppresses the auto-discovery step that would otherwise locate and inject the project-root CLAUDE.md into the CI session. With no conventions ever entering context, the generated code has nothing to conform to — this is a pure context-omission failure, not a truncation or misrouting to a different file.

**Why the others fail**
- A) --bare forces Claude Code to use the global ~/.claude/CLAUDE.md is plausible because Claude Code does maintain a tiered discovery hierarchy where the global CLAUDE.md sits above project level. However, --bare disables auto-discovery entirely rather than redirecting it; no tier of the hierarchy is loaded.
- C) Headless mode (-p) always ignores CLAUDE.md is a category mistake — -p suppresses the interactive UI only and has no effect on CLAUDE.md loading. Because both flags changed simultaneously, attributing the regression to -p rather than --bare is an easy but incorrect misread of causation.
- D) *(No explanation text was captured in the source export for this option.)*

---

### Question 12
`D3 · 3.1`

Your team's CLAUDE.md has grown unwieldy mixing testing conventions, refactoring style, and slash commands guidance. A teammate moves the testing section into .claude/rules/testing.md expecting Claude Code to pick it up automatically on the next session, but the new rules are ignored during refactoring tasks. What is the minimal correct fix?

- A) Rename the file to .claude/rules/testing.CLAUDE.md so Claude Code's recursive memory discovery picks it up.
- B) Move testing.md into .claude/commands/ so it loads alongside the team's existing slash commands.
- C) Place the file at the repo root as TESTING.md, since Claude Code auto-loads top-level markdown rule files.
- D) Add an @./.claude/rules/testing.md import line in the project CLAUDE.md so the file is pulled into context.

**Correct answer:** D

**Why D is correct**
An @import line makes the pull-in explicit rather than assumed: CLAUDE.md is already loaded at session start, so appending @./.claude/rules/testing.md gives the loader a concrete path to resolve into context on every task, including refactoring work. This restores the teammate's intended split without reverting to one monolithic file or relying on discovery that .claude/rules/ doesn't have.

**Why the others fail**
- A) A practitioner familiar with Claude Code's recursive CLAUDE.md discovery might assume any file bearing '.CLAUDE.md' in its name qualifies for the same lookup. Discovery matches files named exactly 'CLAUDE.md' or 'CLAUDE.local.md' at recognized hierarchy levels; a '.CLAUDE.md' suffix appended to a differently-named file inside '.claude/rules/' is never matched.
- B) A practitioner who knows '.claude/commands/' is a recognized, auto-processed directory might conflate that loading with rule injection into session context. That directory exclusively defines slash commands — the correct pattern when you want a '/test' invocable prompt, not persistent conventions applied automatically during ordinary tasks.
- C) *(No explanation text was captured in the source export for this option.)*

---

### Question 13
`D3 · 3.5`

You are using Claude Code to rename process_order to handle_order in orders.py, and the three call sites in checkout.py, refund.py, and api.py must be updated to use the new name. How should you prompt Claude Code?

- A) Send the rename first; after Claude applies it, send each call-site update as a separate follow-up message so Claude can focus on one file at a time.
- B) Send each of the four edits as its own message, letting Claude infer the rename from the pattern of subsequent call-site updates.
- C) Send the rename and all three call-site updates in a single message, since the call sites must be edited to match the new name the rename introduces.
- D) Send the rename, then in a second message send all three call-site updates together after Claude confirms the rename succeeded.

**Correct answer:** C

**Why C is correct**
The rename and its three call sites are one atomic change: handle_order and every reference to it must land together or the codebase sits in a broken intermediate state. Submitting all four edits in one message lets Claude apply them as a single consistent transaction, guaranteeing no window where orders.py and its callers disagree on the function name.

**Why the others fail**
- A) "Send the rename first" looks like correct dependency sequencing, so practitioners who equate ordered prompting with careful work reach for it. Sequential per-file follow-ups are right when edits are genuinely independent; here the codebase is broken between turns because call sites reference a function name that no longer exists in the source.
- B) "Send each of the four edits" inverts the dependency: call-site messages arrive before the rename, asking Claude to update references to a name that does not yet exist. There is no adjacent scenario where letting Claude infer a rename from downstream call-site edits is the right approach — it is a category mistake in dependency direction.
- D) *(Not separately explained in source — D was not the selected wrong answer and its "why it fails" paragraph was not captured in the export; only A and B were shown.)*

---

### Question 14
`D3 · 3.4`

A developer uses plan mode to review a proposed refactoring before execution. In plan mode, Claude Code produces a plan but the developer cannot approve individual steps selectively. Which statement accurately describes plan mode behavior?

- A) Plan mode is equivalent to direct execution but logs each step to CLAUDE.md for audit
- B) Plan mode runs a dry-run simulation and shows predicted file changes without generating a textual plan, updating a live preview of the affected files as it simulates each edit
- C) Plan mode executes each step immediately after the developer confirms it individually, applying file edits and running commands one at a time as each step is approved
- D) Plan mode presents the full plan for review; the developer approves or rejects the entire plan before execution begins

**Correct answer:** D

**Why D is correct**
This matches the scenario exactly: because the developer cannot approve individual steps, the only granularity plan mode offers is a binary gate on the complete plan — the developer sees the whole proposed refactoring up front and either greenlights it in full or rejects it, with no partial-execution state in between. This all-or-nothing approval is what makes plan mode a review checkpoint rather than an interactive execution mode.

**Why the others fail**
- A) Plan mode is equivalent to direct execution... is a category mistake: plan mode withholds execution until approval, making it fundamentally different from direct execution in control flow, not merely in logging verbosity. CLAUDE.md is a project-context file read by Claude Code, not an audit sink written to during execution. Any step logging would be an external integration responsibility, not a native plan mode behavior.
- B) Plan mode runs a dry-run simulation... mistakes the output artifact: plan mode produces a human-readable textual plan, not a filesystem diff or change preview. Developers expecting IDE-style 'preview changes' behavior may assume a simulation layer exists, but Claude Code performs no trial execution to derive predicted file deltas. Dry-run diff output is a separate, shell-level concern (e.g., git diff --stat) outside plan mode entirely.
- C) *(Not separately explained in source — its "why it fails" paragraph was not captured in the export; only A and B were shown.)*

---

### Question 15
`D3 · 3.5`

Your team's /normalize-changelog slash command in .claude/commands/ converts free-form release notes into a strict markdown structure. Initial output keeps formatting headings inconsistently across releases. The release-notes inputs vary wildly in length and tone. Iterative-refinement guidance points at examples, but space in the command file is tight. Which refinement to the command file most directly improves transformation consistency?

- A) Wrap the command logic in plan mode so Claude produces a plan for each transformation before writing the normalized output.
- B) Move the rules into CLAUDE.md so they load every session and remove them from the slash command file entirely.
- C) Append two before/after pairs to the command body — each showing a raw release note and the exact normalized markdown output.
- D) Add a numbered prose checklist of every required heading, ordering rule, and bullet style at the top of the command file.

**Correct answer:** C
**Your answer:** D ✗

**Why C is correct**
With inputs varying widely in length and tone, two before/after pairs anchor the mapping directly in the command body: Claude pattern-matches raw note to normalized heading structure instead of re-deriving formatting rules from prose each run. That concrete demonstration is what disciplines heading and bullet consistency across releases despite the tight file space, since one worked example per pair fixes exact structure while still generalizing across varied release-note styles.

**Why the others fail**
- A) Wrap the command logic in plan mode addresses approval workflows and transparency — useful when a human needs to confirm intent before destructive writes. It adds a round-trip on every invocation without giving Claude any new signal about what the normalized output should look like. Plan mode is the correct pattern for agentic steps requiring human sign-off, not for improving format consistency on a deterministic conversion task.
- B) Moving rules into CLAUDE.md ensures they load on every session and aren't forgotten — a legitimate fix for scope or amnesia problems. But it relocates prose rules without changing their form: the prose-vs-example gap that causes inconsistent transformation output persists unchanged. CLAUDE.md is the right destination for project-wide invariants, not for per-command transformation exemplars.
- D) A numbered prose checklist appeals because it makes every rule explicit and reviewable. However, prose descriptions of format rules ("use H2 for sections, indent bullets two spaces") force Claude to infer the target shape from abstract language on each novel input — exactly where inconsistency originates. Concrete before/after examples would be the right tool here; a checklist is correct for policy enforcement, not transformation shaping.

---

## S3 · Multi-agent research

### Question 16
`D2 · 2.3`

The report generation subagent in a research system has access to fetch_document, synthesize_findings, and generate_report. Logs show it calls synthesize_findings directly on documents instead of delegating synthesis to the synthesis subagent. What design change best prevents this cross-specialization misuse?

- A) Add a system prompt rule to the report generation subagent instructing it not to call synthesize_findings
- B) Add a runtime hook that logs and blocks synthesize_findings calls from the report generation subagent
- C) Move synthesize_findings to a separate MCP server only the synthesis subagent can connect to
- D) Remove synthesize_findings from the report generation subagent's tool list at initialization

**Correct answer:** D

**Why D is correct**
Excluding synthesize_findings from the report generation subagent's tool list at initialization means the capability simply doesn't exist for that agent — there's no call path for it to invoke regardless of prompt content or context complexity. This guarantees the synthesis subagent is the sole route to that function, closing the cross-specialization gap the logs revealed with zero runtime enforcement cost.

**Why the others fail**
- A) A system prompt rule leaves synthesize_findings in the tool list, making the constraint probabilistic rather than structural — a sufficiently complex context or prompt injection can still trigger the call. This pattern is correct when access should be conditional (e.g., call synthesize_findings only if document count exceeds a threshold), not when the capability should be absent entirely.
- B) A runtime hook blocking calls enforces the boundary with full certainty, making it strictly stronger than a prompt rule. It introduces unnecessary per-call overhead, however, when the same structural guarantee is achievable for free by excluding the tool at initialization. Runtime hooks are the right pattern when tool access must be gated on dynamic state — rate limits, compliance audit trails, or caller identity — that cannot be resolved at startup.
- C) Routing synthesize_findings through a dedicated MCP server that the synthesis subagent alone can connect to is a valid hard-isolation architecture, appropriate when network-level separation or multi-team ownership justifies the infrastructure overhead. When tool list scoping at initialization already creates a structural boundary within the same agent framework, adding a separate server is disproportionate complexity for the problem.

---

### Question 17
`D5 · 5.4`

Your coordinator agent runs a four-hour research job that delegates to web search, document analysis, synthesis, and report generation subagents via the Task tool. After hitting the context limit, /compact runs and the coordinator continues. On resume, the synthesis subagent re-runs prior queries because it has lost which sources were already analyzed. What change best preserves cross-session subagent state?

- A) Add a Compact Instructions section to CLAUDE.md telling the coordinator to retain the synthesis subagent's reasoning when /compact runs.
- B) Re-run the job under claude --resume <id> --fork-session so the prior conversation history is preserved in a forked session for the synthesis subagent.
- C) Move the list of analyzed sources into project-root CLAUDE.md so it is re-injected automatically after every /compact pass.
- D) Have each subagent write a structured manifest of completed work to disk, and have the coordinator load that manifest on resume before re-dispatching the Task tool.

**Correct answer:** D

**Why D is correct**
Writing completed-work state to disk as a structured manifest survives both /compact and the isolation boundary between Task invocations, since the coordinator reads it back explicitly rather than relying on context carryover. This is the only option that gives the synthesis subagent a durable record of which sources were already analyzed before the coordinator re-dispatches it, eliminating the redundant re-querying the scenario describes.

**Why the others fail**
- A) "Add a Compact Instructions section" controls what /compact retains in the coordinator's own context window — the correct lever when protecting the coordinator's reasoning chains across compaction. Subagent context windows are isolated per Task invocation and never enter the coordinator's window, so /compact has nothing to preserve on their behalf.
- B) "Re-run the job under claude --resume" restores the coordinator's conversation history, which practitioners often conflate with subagent internal state. Forking a session preserves what the coordinator observed in its own window — not what subagents computed internally — because each Task invocation spawns a fresh, isolated context window regardless of how the coordinator session was resumed.
- C) "Move the list of analyzed sources into project-root CLAUDE.md" survives compaction via auto-injection and is a viable pattern for a small, bounded source list in a short single-session job. A four-hour research run accumulates state orders of magnitude beyond the 200-line sub-context budget, making this approach brittle under scale.

---

### Question 18
`D1 · 1.6`

The synthesis subagent in your multi-agent research system must evaluate each source for credibility, relevance, and coverage before combining findings. Which task decomposition approach best ensures consistent, auditable evaluation across all three aspects?

- A) Run a separate chained prompt for each evaluation aspect, passing results forward as structured context to the next step.
- B) Let the coordinator agent evaluate sources and pass final verdicts to the synthesis subagent to reduce round-trips.
- C) Issue a single prompt asking the synthesis subagent to evaluate all three aspects together in one response.
- D) Use the document analysis subagent to perform all three evaluations since it already processes source documents.

**Correct answer:** A

**Why A is correct**
Chaining one prompt per aspect gives credibility, relevance, and coverage each a discrete, inspectable output that feeds forward as structured context, so any downstream synthesis decision can be traced back to the specific step and verdict that drove it. This isolation is what makes the evaluation auditable across all three aspects rather than a single opaque judgment call.

**Why the others fail**
- B) "Coordinator agent evaluate sources" is attractive when minimizing round-trips is the priority and the coordinator holds richer global context. It is the correct pattern when the synthesizer is a pure aggregator with no judgment role — not when the agent combining findings must own and be accountable for the credibility, relevance, and coverage verdicts driving its output.
- C) "Single prompt asking the synthesis subagent" reduces latency and is the correct pattern when evaluation dimensions are tightly coupled and only a holistic verdict is needed downstream. When each dimension must be independently auditable, conflated outputs make it impossible to isolate which aspect drove an inclusion or exclusion decision.
- D) "Document analysis subagent to perform all three" appeals to practitioners avoiding duplicated document-access logic by colocating all source-touching work in one agent. Routing evaluation there is appropriate when parsing and quality assessment are inseparable within a single-document scope — not when relevance and coverage require cross-document awareness that belongs to the synthesis stage.

---

### Question 19
`D1 · 1.7`

A multi-agent research system completes a web search phase but the coordinator agent's session is interrupted before synthesis. When restarting, the coordinator agent must decide whether to resume the old session or start fresh. The web search subagent's results are now 48 hours old. What should the coordinator agent do?

- A) Resume the interrupted session but clear only the web search subagent's tool results before invoking synthesis
- B) Start a fresh session with a structured summary of research goals and re-invoke the web search subagent for current data
- C) Start a fresh session and re-run the entire research pipeline from scratch without any context from the interrupted session
- D) Resume the interrupted session and pass the cached web search results directly to the synthesis subagent without re-querying

**Correct answer:** B

**Why B is correct**
The 48-hour-old web search results are the specific asset that has decayed; carrying research goals forward in a structured summary preserves the coordinator's synthesis framing without re-deriving intent, while re-invoking the web search subagent guarantees synthesis runs against current data rather than approximating freshness by trusting a stale cache. This gets both correctness and continuity that a full restart or a stale resume each sacrifice one of.

**Why the others fail**
- A) "Resume the interrupted session but clear" specific tool results treats session state as selectively mutable. Session resumption in the Agent SDK loads the full prior context atomically; there is no supported mechanism to surgically invalidate individual tool-call results before continuing.
- C) "Start a fresh session and re-run the entire" pipeline correctly avoids stale data but discards still-valid research framing unnecessarily. A full restart is warranted only when prior goals or parameters are themselves invalidated — not merely when retrieved data has aged out.
- D) "Resume the interrupted session and pass cached results" is the low-latency, cost-efficient choice when tool results remain fresh. When data freshness is not a constraint — e.g., querying static corpora or internal documents — resuming with prior tool output is the correct and preferred pattern.

---

### Question 20
`D5 · 5.6`

The synthesis subagent combines findings from multiple sources into a single report. Which metadata field is most critical to include with each source to prevent temporal misinterpretation?

- A) The confidence score assigned by the document analysis subagent
- B) The URL or document identifier for each source
- C) The token count consumed by each subagent call
- D) The publication date of each source

**Correct answer:** D
**Your answer:** B ✗

**Why D is correct**
When the synthesis subagent merges findings across sources, each source's publication date is what lets a reader distinguish a superseded finding from the current state of fact — without it, an older claim can silently overwrite or contradict a newer one with no way to detect the conflict. This directly addresses the stem's concern: preventing temporal misinterpretation in a combined report, not verifying where the content came from or how reliably it was extracted.

**Why the others fail**
- A) Confidence score assigned by the document analysis reflects retrieval or extraction quality, making it attractive when the concern is synthesis reliability. It would be the right field to surface when guarding against low-quality source material, not when preventing stale data from being mistaken for current fact.
- B) URL or document identifier tracks provenance and enables source verification — a practitioner focused on citation integrity would naturally reach for it. It would be the critical field when the goal is deduplication or audit trails, not temporal validity.
- C) Token count consumed by each subagent is an operational cost metric with no bearing on how readers interpret data freshness or recency. Unlike the other distractors, this is a category mistake — no plausible adjacent scenario makes it the answer to a question about temporal misinterpretation.

---

### Question 21
`D2 · 2.5`

The report generation subagent must locate all Markdown files produced by the synthesis subagent across nested output directories. Which Glob pattern correctly matches only Markdown files by extension regardless of directory depth?

- A) **/*synthesis*.md
- B) **/{*.md,*.txt}
- C) *.md
- D) **/*.md

**Correct answer:** D

**Why D is correct**
The ** segment recursively descends through any number of nested output directories the synthesis subagent may have produced, while *.md at the tail constrains matches to the Markdown extension exactly, no more and no less. This combination guarantees complete coverage of the nested tree without pulling in other extensions or requiring a naming convention, which is exactly what locating 'all Markdown files' at unknown depth demands.

**Why the others fail**
- A) **/*synthesis*.md would be correct if the task were to locate only the synthesis subagent's own output files, identified by a naming convention. Here the stem asks for all Markdown files regardless of filename, so requiring the 'synthesis' substring silently drops any Markdown outputs whose names don't match that token.
- B) **/{*.md,*.txt} correctly traverses nested directories and matches Markdown files, but the brace expansion also captures .txt files, exceeding the stated requirement of Markdown only. This pattern is appropriate when both extensions are valid targets, such as when raw notes and formatted reports must be collected together.
- C) *.md matches Markdown files in the current working directory only — no directory traversal occurs. A practitioner familiar with simple glob syntax but not recursive glob semantics would reach for this first. It is the correct pattern when all target files are guaranteed to sit in a single flat directory.

---

### Question 22
`D1 · 1.6`

The coordinator agent in a multi-agent research system must decide whether to invoke the web search subagent, document analysis subagent, or both, depending on whether a topic requires fresh data. Which decomposition strategy best handles this conditional routing?

- A) Dynamic adaptive decomposition where the coordinator evaluates topic requirements and selects subagents at runtime
- B) A fixed prompt chain that always invokes all subagents in sequence regardless of topic type, ignoring whether fresh web data is actually needed
- C) Parallel invocation of all subagents on every request, discarding outputs that are not relevant to the topic and wasting synthesis capacity
- D) A static workflow that pre-assigns subagents to topics based on keyword matching at startup

**Correct answer:** A

**Why A is correct**
Coordinator-time evaluation is the only strategy that matches the actual decision variable here — whether a given topic needs fresh data — since that can't be known until the topic is inspected. By selecting subagents at runtime, the coordinator invokes web search, document analysis, or both exactly when each is warranted, guaranteeing no wasted subagent calls and no missed data source.

**Why the others fail**
- B) A fixed prompt chain always invoking all subagents appeals when pipeline predictability and logging simplicity matter more than efficiency. It is the correct pattern when every topic genuinely requires both fresh web data and document analysis — conditional routing only adds overhead when all branches are always needed.
- C) Parallel invocation discarding outputs appears efficient by exploiting concurrency, and is the correct pattern when subagent latency dominates and results can't be predicted cheaply upfront. Here it wastes both compute and synthesis capacity because the coordinator has enough context to make a cheap routing decision before invoking any subagent.
- D) A static workflow pre-assigning subagents tempts practitioners who want to avoid runtime decision cost and trust that domain keywords reliably signal data needs. It would be appropriate for a closed, enumerable topic taxonomy where keyword categories are stable and exhaustive — not for open-ended research queries where topic nuance can't be anticipated at startup.

---

### Question 23
`D5 · 5.2`

*(This question appeared three times, verbatim identical, in the source export — shown once here.)*

The coordinator agent uses a Task tool call to delegate a research topic to the web search subagent. The query matches multiple cached prior research threads with different scopes. What should the coordinator agent do?

- A) Pause delegation and ask the user to clarify which research scope the current query should target.
- B) Randomly sample one matching thread and log the ambiguity for post-hoc review.
- C) Pass all matching thread identifiers to the synthesis subagent and let it resolve which scope is relevant.
- D) Select the cached thread with the highest recency score and proceed without interrupting the workflow.

**Correct answer:** A
**Your answer:** C ✗

**Why A is correct**
Because the matching threads have genuinely different scopes rather than overlapping variants, only the user can confirm which one reflects current intent — the coordinator has no basis in the query itself to break the tie. Pausing delegation here preserves accountability at the decision point instead of letting an unverified scope choice silently propagate through the research subagent's output.

**Why the others fail**
- B) Randomly sample one matching thread introduces non-determinism at a scope-selection decision point with no accountability until results surface — a category mistake for an agentic workflow. Logging ambiguity post-hoc cannot undo wrong-scope research that may have already propagated through downstream tool calls.
- C) Pass all matching thread identifiers to the synthesis subagent is the right pattern when scope disambiguation is part of synthesis (e.g., merging overlapping findings). When the scopes are mutually exclusive and the coordinator lacks authority to choose, forwarding the ambiguity downstream just relocates the decision to an agent with even less context about user intent.
- D) Select the cached thread with the highest recency score applies a recency heuristic as a proxy for relevance — plausible when scope is consistent across threads and recency genuinely correlates with intent. Here, multiple threads have *different* scopes, so recency selects a scope rather than confirming one, silently biasing the research outcome.

---

### Question 24
*(Not present in the source export. The question numbering in the log jumps directly from three consecutive "Q 23/60" captures to "Q 25/60" — no Q24 content was captured, so there is nothing to format here.)*

---

### Question 25
`D2 · 2.2`

The web search subagent calls search_recent_papers for a niche topic. The tool returns an empty array. The synthesis subagent then reports to the coordinator agent that the search system is down. What tool response design prevents this misinterpretation?

- A) Raise a no_results_found exception at the MCP transport layer for the agent framework to intercept, treating an empty result set as a protocol-level failure
- B) Return isError: true with an error message whenever the search returns no results, treating a zero-hit query the same as a tool execution failure
- C) Return a successful result with an empty results array and a query_succeeded: true field confirming the search executed without error
- D) Return a single placeholder result with text 'No papers found' so the agent has non-empty content to process

**Correct answer:** C

**Why C is correct**
Separating execution status from result cardinality is exactly what the synthesis subagent needs here: query_succeeded: true tells it the search tool ran cleanly against search_recent_papers, and the empty array is just the honest outcome for a niche topic with no matching papers. This lets the coordinator distinguish 'nothing exists for this query' from 'the search system is unreachable,' which a bare empty array alone cannot guarantee.

**Why the others fail**
- A) 'Raise a no_results_found exception at' the transport layer promotes a normal domain state into a protocol-level error, inflating exception paths with routine business outcomes. MCP transport exceptions are the correct mechanism for genuine protocol failures — malformed payloads, connection drops, or authentication rejections — not for a query that executed cleanly and matched nothing.
- B) 'Return isError: true with' no results conflates a domain outcome (empty set) with a tool failure — an intuitive mistake for practitioners who treat unexpected empty responses as errors. isError: true is the correct pattern when the search system itself fails: network timeout, auth rejection, or a malformed upstream API response.
- D) 'Return a single placeholder result' injects synthetic data into the results array, borrowing a UI convention (rendering a 'no results' string) into a structured data contract. Any downstream agent that reads result content will process a fabricated entry as real evidence, corrupting synthesis without any signal that the data is artificial.

---

### Question 26
`D2 · 2.1`

The coordinator agent in a research system must choose between search_web and search_arxiv for a user query. Both tools have no description. Which change would most directly help the agent select the right tool?

- A) Write a clear description for each tool explaining what it searches and when to use it
- B) Rename search_arxiv to academic_search to make its purpose self-evident
- C) Reduce the tool list to one generic search tool that handles both web and academic sources
- D) Add a few-shot example to the system prompt showing the correct tool being used

**Correct answer:** A

**Why A is correct**
With both tools undescribed, the coordinator has no basis to distinguish search_web from search_arxiv beyond their bare names. A description stating what each searches and when to use it — e.g. peer-reviewed literature versus general web content — gives the model the scope and selection criteria it needs to route the query correctly, since tool descriptions are what the LLM actually reasons over when choosing among candidates.

**Why the others fail**
- B) A more descriptive name reduces ambiguity and is a meaningful improvement over an opaque identifier. A name alone cannot carry usage constraints — conditions like 'prefer for peer-reviewed literature' or 'does not index news sources' require prose. Renaming is the correct primary fix only when a description already exists and the name is actively misleading.
- C) Collapsing to a single generic tool does eliminate selection errors — by eliminating the choice entirely. It sacrifices the precision of specialized tools rather than enabling correct routing between them. This consolidation is appropriate when the two search domains overlap enough that a single parameterized interface genuinely covers all query types without loss of fidelity.
- D) Few-shot examples in the system prompt do shape tool-routing and are a real technique. They work by demonstrated pattern, not by communicating a tool's scope or constraints, making them secondary to descriptions. They become the right lever when descriptions are already solid but edge-case calls still misfire.

---

### Question 27
`D1 · 1.2`

Your research coordinator assigns the web search subagent to retrieve sources on one subtopic and the document analysis subagent to analyze a second subtopic. Users report that cross-cutting themes are missing from reports. What is the most likely cause?

- A) The coordinator is not passing web search URLs to the document analysis subagent.
- B) The report generation subagent cannot handle topics discovered after initial task decomposition.
- C) Each subagent covers only its assigned subtopic, leaving cross-subtopic themes unaddressed.
- D) The synthesis subagent is not calling the report generation subagent after it completes.

**Correct answer:** C

**Why C is correct**
The coordinator split the research task along subtopic lines with no subagent scoped to cross-cutting analysis, so any theme spanning both the web-search subtopic and the document-analysis subtopic falls into the gap between assignments. This is the signature failure of overly narrow decomposition: coverage is complete per-slice but incomplete across slices, guaranteeing exactly the missing-themes symptom users report.

**Why the others fail**
- A) The coordinator not passing web search URLs points to a context-propagation defect — a real failure mode when subagents need each other's artifacts. It would be the correct diagnosis if the document analysis subagent were producing incomplete analysis due to missing source URLs, not if cross-cutting themes were absent from both subagents' scopes.
- B) The report generation cannot handle locates the defect in the final rendering stage, implying the themes were discovered but not expressible. This would apply if the report generator lacked a schema or template section for emergent topics — but missing themes that were never surfaced by any subagent cannot be a rendering problem.
- D) The synthesis subagent not calling misdiagnoses the failure as a pipeline-sequencing break rather than a coverage gap. This pattern would be the right diagnosis if reports were partially generated or truncated at the synthesis step — but here the themes are absent from source material entirely, upstream of any handoff.

---

### Question 28
`D2 · 2.4`

The research system needs to send notifications via email when reports are complete. An engineer evaluates building a custom MCP server vs using a community email MCP server. The team also needs custom filtering logic: only notify subscribers who opted into topic-specific alerts. Which approach is most appropriate?

- A) Use a community email MCP server since email sending is a standard integration need requiring no custom subscriber filtering logic
- B) Use the Bash tool to run an email CLI instead of deploying any MCP server
- C) Use a community email MCP server for sending but implement filtering in the coordinator agent's system prompt instructions instead of a dedicated tool
- D) Build a custom MCP server to implement the topic-based subscriber filtering logic alongside the email-sending capability

**Correct answer:** D
**Your answer:** C ✗

**Why D is correct**
Topic-based subscriber filtering is opt-in business logic unique to this research system, so it must live in code the coordinator can call deterministically rather than in a generic email tool. A custom MCP server co-locates the filtering check with the send action, guaranteeing every notification is gated by subscription state as a single atomic, auditable operation.

**Why the others fail**
- A) Preferring a community server for standard email sending is sound practice — it avoids unnecessary custom work. The gap is subscriber filtering: community servers don't ship topic-based opt-in logic. If the sole requirement were transactional delivery with no custom routing rules, a community server would be the appropriate choice.
- B) Reaching for Bash to avoid MCP deployment overhead is tempting for low-complexity scripts. Within an agent workflow, bypassing the MCP interface loses structured tool responses, typed error codes, and retry semantics the coordinator depends on. Outside an agent context — a standalone automation script — a CLI invocation is entirely appropriate.
- C) Splitting delivery and filtering across layers appears pragmatic: reuse the community server, extend logic in the agent. Subscriber opt-in rules encoded in a system prompt become probabilistic rather than deterministic; compliance-gating logic must be enforced programmatically. If filtering were advisory rather than a hard business rule, prompt-side heuristics might suffice.

---

### Question 29
`D2 · 2.2`

The web search subagent in your research system fails to retrieve results for a query. How should it communicate this failure to the coordinator agent via MCP?

- A) Return an empty result array and log the error to a separate diagnostics file
- B) Raise an exception and let the coordinator agent catch it at runtime
- C) Set a status field in the response body to 'failed' with an HTTP error code
- D) Return a result object with isError set to true and a descriptive error message

**Correct answer:** D

**Why D is correct**
Setting isError true keeps the failure inside the standard tool-result envelope, so the coordinator agent can branch on it deterministically instead of parsing logs, exceptions, or ad-hoc fields. A descriptive message alongside the flag gives the coordinator enough context to retry the search, reformulate the query, or escalate — the guarantee no other signaling path provides.

**Why the others fail**
- A) Return an empty result array and log silently swallows the failure from the coordinator's perspective — the coordinator sees a successful call with no results and cannot distinguish a genuine zero-result query from a retrieval error. Separate diagnostics files are appropriate for observability pipelines, not for in-band failure signaling to a consuming agent.
- B) Raise an exception and let the coordinator agent catch it breaks out of MCP's structured result contract entirely — unhandled exceptions propagate as transport-level noise, not inspectable tool results. This pattern is appropriate in native function calls within a single runtime, but MCP tool invocations expect a well-formed result object regardless of outcome.
- C) Set a status field in the response body conflates MCP tool response semantics with HTTP API conventions — MCP results are not HTTP responses, and coordinators parsing them have no standard contract for an ad-hoc status field or numeric error codes. This pattern would be correct when designing a REST endpoint, but MCP defines isError as the canonical failure indicator.

---

### Question 30
`D1 · 1.5`

The coordinator agent must block any web search subagent tool call whose query contains a restricted keyword before execution. Which PreToolUse hook output field enforces this at the SDK level?

- A) Return permissionDecision: "ask" to pause and prompt the user for approval.
- B) Return updatedInput replacing the restricted keyword with an empty string before the call runs.
- C) Return permissionDecision: "deny" with a permissionDecisionReason explaining the blocked keyword.
- D) Return additionalContext describing the restriction so Claude skips the call voluntarily.

**Correct answer:** C

**Why C is correct**
Deny is the SDK's categorical block: it prevents the tool call from ever executing, matching the requirement that any restricted-keyword search be stopped unconditionally rather than merely flagged, deferred, or rewritten. The permissionDecisionReason gives the coordinator an auditable record of why the call was refused, satisfying the compliance-enforcement intent of the scenario.

**Why the others fail**
- A) Return permissionDecision: "ask" appeals because it interrupts execution, which feels like blocking. It is the correct pattern when human-in-the-loop approval is required for sensitive but not categorically forbidden calls — here the requirement is unconditional enforcement, which ask cannot guarantee since user approval would permit the call.
- B) Return updatedInput replacing the restricted keyword is attractive because it neutralizes the offending content at the call site. It is the correct pattern when the goal is sanitization rather than prevention — it lets execution proceed on the rewritten input, so a keyword-blocking compliance rule is still violated at the tool-invocation level.
- D) Return additionalContext describing the restriction sounds authoritative because the field name implies enforcement context, making it plausible as a compliance mechanism. It is the correct pattern only when you want to inform Claude's reasoning before it decides whether to proceed — it cannot hard-block; Claude may still invoke the tool.

---

## S4 · Developer productivity tools

### Question 31
`D3 · 3.5`

A developer wants a rule in .claude/rules/ that only activates when Claude Code edits Terraform files. What frontmatter field scopes the rule to those files?

- A) The trigger: field in the YAML frontmatter, listing file extensions to match
- B) The scope: field in the YAML frontmatter, set to terraform
- C) The applies_to: field in the YAML frontmatter, set to [terraform]
- D) The paths: field in the YAML frontmatter, set to a glob like [**/*.tf]

**Correct answer:** D

**Why D is correct**
Scoping a Terraform-only rule requires matching against the file paths Claude is editing, which is exactly what paths: does — a glob such as [**/*.tf] restricts activation to Terraform files regardless of directory depth. This guarantees the rule fires only on matching edits, unlike a technology-name key that has no defined matching semantics in the rules schema.

**Why the others fail**
- A) trigger: listing file extensions mirrors the event-hook vocabulary of GitHub Actions and similar CI/CD tools, where trigger blocks gate execution on file-path patterns. In .claude/rules/ YAML, trigger: is not a recognized frontmatter key, and no file-extension list syntax exists in the spec.
- B) scope: set to terraform — practitioners familiar with ESLint flat config, where scoping keys restrict rules to named domains or file sets, may expect an analogous key here. In .claude/rules/ YAML, scope: is not a valid frontmatter field; no recognized key accepts a bare technology name for file matching.
- C) applies_to: set to [terraform] follows the convention of policy-enforcement tools like OPA and Stylelint, where an applies_to or applies key scopes a rule to a named technology category. In .claude/rules/ YAML, neither the key name nor the category-name value format is valid — glob patterns under paths: are required.

---

### Question 32
`D1 · 1.2`

Your coordinator agent has spent 30 turns exploring a legacy Java monorepo with Grep and Read, building a mental model of which modules own payment logic. It now spawns a subagent to refactor one specific class. The subagent's first Read call fails because it cannot locate the file. What best explains this failure?

- A) The subagent's Read tool permissions were not propagated from the coordinator, so filesystem access is denied by default.
- B) The subagent's working directory defaults to the user's home rather than the coordinator's current repo checkout.
- C) The subagent inherited the coordinator's history but its context window was truncated, dropping the earlier Grep output.
- D) The subagent starts with an isolated context and never saw the coordinator's earlier Grep results that located the file path.

**Correct answer:** D

**Why D is correct**
The coordinator's 30-turn exploration — every Grep hit and Read result that pinned down the class's location — lives only in the coordinator's own context; spawning a subagent starts a fresh session with no access to that history. Because the file path was never included in the spawn prompt, the subagent has no way to know where to look, and the Read call fails on a path it was never given.

**Why the others fail**
- A) "Read tool permissions were not propagated" conflates context isolation with access control. Tool permissions are configured at spawn time via the agent's tool list, not inherited or denied by default. This would be the correct diagnosis only if the subagent were explicitly launched without the Read tool in its allowed-tools set.
- B) "Working directory defaults to the user's home" invents a runtime behavior not defined by the SDK — the Agent SDK does not automatically shift cwd between coordinator and subagent. A practitioner might reach for this if debugging a shell-based tool invocation, where cwd genuinely matters, but the failure here is missing path knowledge, not a filesystem root mismatch.
- C) "Inherited the coordinator's history but" misstates the isolation model entirely — subagents receive no prior conversation history to truncate in the first place. Truncation is a real failure mode when a long-running conversation overflows a single agent's context window, but it presupposes inheritance, which the coordinator-subagent pattern does not provide.

---

### Question 33
`D3 · 3.2`

A productivity team creates a /analyze-codebase skill that uses Glob, Grep, and Read. The skill sometimes uses Bash to run analysis scripts. They want to prevent it from calling Bash and restrict it to only the read-only tools. Which SKILL.md frontmatter field enforces this restriction?

- A) Add a description field stating 'do not use Bash' to instruct Claude not to call it
- B) Set context: fork so Bash calls in the skill run in an isolated context away from the main session
- C) Set disable-model-invocation: true to prevent the skill from being auto-triggered with Bash access
- D) Set allowed-tools: [Glob, Grep, Read] to restrict the skill to only those three tools

**Correct answer:** D

**Why D is correct**
The team needs the /analyze-codebase skill locked to Glob, Grep, and Read specifically because it currently invokes Bash for analysis scripts — allowed-tools is the enforcement mechanism that runtime-restricts an invoked skill's tool set, so declaring only those three names makes any Bash call fail regardless of what the skill's logic attempts. This guarantees the restriction holds even if the underlying scripts still reference Bash, unlike approaches that merely isolate context or advise against it.

**Why the others fail**
- A) Natural-language instructions in a 'description' field do influence Claude's behavior, so practitioners comfortable with prompt engineering reach for this first. Such instructions are probabilistic — a sufficiently confident model can still call Bash under pressure. 'allowed-tools' is the correct pattern whenever hard, deterministic enforcement is required rather than soft guidance.
- B) 'context: fork' reads as sandboxing, so practitioners conflate context isolation with tool restriction. It isolates the skill's conversation context from the main session but leaves the available tool set unchanged — it's the correct setting when preventing skill output from bleeding into the primary context, not for enforcing a tool allowlist.
- C) 'disable-model-invocation: true' governs whether the model can auto-trigger the skill, not which tools it may call once invoked — conflating 'prevent unintended invocation' with 'prevent unintended tool use' is the trap. It's the correct setting when suppressing automatic skill activation, not for constraining an already-invoked skill's tool access.

---

### Question 34
`D3 · 3.1`

An engineer on the developer productivity agent project wants Claude Code to always use their preferred Bash alias expansions and personal code-exploration shortcuts across every project, without those preferences appearing in version control. Where should these settings live?

- A) In CLAUDE.local.md at the repository root, added to .gitignore so teammates never see it
- B) In ~/.claude/CLAUDE.md so personal preferences apply to all projects outside source control
- C) In the project-level CLAUDE.md under a personal section marked with HTML comments to strip them
- D) In a .claude/rules/ file committed to the repo with restricted file permissions

**Correct answer:** B

**Why B is correct**
~/.claude/CLAUDE.md sits outside any repository, so it's never cloned, staged, or pushed with project source — it loads for every project the engineer works in without teammates ever seeing it. That matches the requirement exactly: global scope across the developer productivity agent project and all others, plus guaranteed isolation from version control.

**Why the others fail**
- A) CLAUDE.local.md at the repository root is the right pattern for project-specific personal overrides that a developer doesn't want teammates to see — gitignoring it achieves that. However, it scopes only to that one repository, so Bash alias expansions and shortcuts would need duplicating in every project's root rather than being available globally.
- C) Embedding personal preferences inside the project-level CLAUDE.md — even behind HTML comments — still commits them to shared version control, exposing them to every teammate and every code review. HTML comment stripping is a token-budget technique, not a privacy or scoping mechanism.
- D) A .claude/rules/ file committed to the repository is team-shared by definition; file permissions on a version-controlled file do not prevent teammates from reading or reverting it. This pattern is appropriate for enforcing shared standards, not for isolating personal preferences from source control.

---

### Question 35
`D3 · 3.4`

An engineer uses your productivity agent to add a missing return type annotation to a single function in one well-understood file. The change requires only Read and Write. Which execution approach is most appropriate?

- A) Auto-accept edits mode, to skip all permission prompts for this session
- B) Plan mode, to prevent any unintended writes before a review step
- C) Direct execution, since the change is isolated to one file and fully scoped
- D) Plan mode, because Write tool usage always requires prior approval

**Correct answer:** C

**Why C is correct**
The target is a single function in one already-understood file, and the toolset needed — Read then Write — maps directly onto the task with no discovery or cross-file coordination required. Direct execution matches effort to risk here: the scope is fully known upfront, so a planning step would add process without reducing uncertainty that doesn't exist.

**Why the others fail**
- A) Auto-accept edits mode, to skip all permission prompts is attractive when batching many pre-approved changes in a controlled scripting session. Here it over-extends: it disables permission prompts project-wide for the session rather than calibrating the execution strategy to this one isolated, low-risk task.
- B) Plan mode, to prevent unintended writes is a sound instinct when a change touches shared utilities, multiple call sites, or has uncertain downstream effects — overhead that pays off in those contexts. A single annotation in one well-understood file has no cross-file surface and no ambiguous scope, so the review step adds latency without reducing risk.
- D) Plan mode, because Write tool usage always requires approval conflates a team policy choice with a platform constraint — Claude's plan mode is a deliberate workflow option, not a mandatory gate that Write triggers automatically. This rule would be appropriate if an org-level policy mandated pre-approval for all writes, but the stem describes no such constraint.

---

### Question 36
`D3 · 3.3`

Your developer productivity agent must apply a 'no inline SQL string concatenation' convention only when it uses Edit on Python files inside services/billing/, but not when editing Python files in services/reporting/ or under tests/. The convention lives in a .claude/rules/no-sql-concat.md file. Which frontmatter glob pattern restricts the rule to exactly this scope?

- A) paths: services/billing/**/*.py — match Python files at any depth under the billing service only.
- B) paths: services/**/*.py — match every Python file under any service directory in the repository.
- C) paths: services/billing/*.py — match Python files in the billing directory's top level only.
- D) paths: "**/*.py" with a separate exclude: tests/**/* clause for the test directory exception.

**Correct answer:** A

**Why A is correct**
The billing/**/*.py prefix anchors matching to services/billing/ specifically, so the rule fires on Edit calls there while services/reporting/ and tests/ fall outside the prefix entirely and never activate it. The double-star wildcard also recurses through any nested package structure inside billing, so files at arbitrary depth still trigger the SQL-concatenation convention.

**Why the others fail**
- B) services/**/*.py correctly recurses into nested packages and fits when a convention should span all service directories uniformly. Here it over-matches by including services/reporting/ alongside services/billing/, violating the scope boundary the stem requires.
- C) services/billing/*.py correctly anchors to the billing service, but the single wildcard stops at the directory's immediate contents, missing nested subpackages. It would be correct if the billing service guaranteed a flat layout with no subdirectories of its own.
- D) 'paths: **/*.py with a separate exclude:...' conflates the Claude rules frontmatter schema with tools like ESLint or webpack that support discrete include/exclude fields. The paths key has no exclude clause; fabricating one means the constraint is silently ignored rather than enforced.

---

### Question 37
`D2 · 2.5`

An agent uses Edit to update a configuration constant in a legacy codebase. Edit returns an error because the target string appears in three different files. What is the correct next step?

- A) Retry Edit with the same string but pass a replace_all flag to update every occurrence at once across all three files.
- B) Use Grep to identify which file contains the intended instance, then call Edit with a larger unique context string.
- C) Use Glob to list all files matching the pattern, then call Bash to apply a sed replacement across them without checking which occurrence is the intended target.
- D) Fall back to Read then Write on the target file to replace the constant across the entire file.

**Correct answer:** B

**Why B is correct**
Grep confirms exactly which of the three files holds the constant meant for this legacy update, letting the agent build a longer, file-specific context string that resolves Edit's uniqueness requirement without touching the file. This preserves Edit's atomic, verified single-match guarantee — the same edit-then-confirm safety the other two files never get exposed to.

**Why the others fail**
- A) 'Retry Edit with the same string' but via a replace_all flag is a category mistake — Edit exposes no such parameter; the flag is a hallucinated API surface. Even if it existed, overriding the uniqueness guard would indiscriminately mutate all three occurrences across different files, corrupting configurations unrelated to the intended change.
- C) 'Use Glob to list all files' appeals to practitioners who see a multi-file problem and want a systematic resolution. This pipeline is correct for intentional bulk cross-codebase renames, but here the goal is a single targeted update — bypassing Edit's built-in toolchain unnecessarily risks overwriting unrelated constant definitions in the other matched files.
- D) 'Fall back to Read then Write' is a recognized fallback for intractable Edit failures, so practitioners who know the pattern may reach for it prematurely. It becomes the correct choice only after Grep-assisted context-narrowing still cannot isolate a unique string — not as the immediate next step when Grep hasn't been attempted.

---

### Question 38
`D2 · 2.2`

The Grep tool in your codebase agent returns an error when a search pattern contains invalid regex syntax. How should this error be classified in the structured error response to prevent the orchestrator from issuing wasted retries?

- A) Mark it retryable with a short backoff, as transient failures often resolve on retry, since Grep's regex engine may occasionally stall under heavy load.
- B) Mark it non-retryable with error metadata indicating invalid input, so the orchestrator reformulates the query instead.
- C) Suppress the error and return an empty result set to allow the pipeline to continue.
- D) Mark it retryable with increased timeout, as regex parsing may need more processing time.

**Correct answer:** B
**Your answer:** D ✗

**Why B is correct**
Invalid regex syntax is a property of the input itself, not the execution environment, so classifying it non-retryable with an 'invalid input' metadata tag lets the orchestrator distinguish this from transient infrastructure failures. That signal routes the flow toward query reformulation — the only action that can actually resolve a malformed pattern — rather than burning retry budget on an attempt guaranteed to fail identically.

**Why the others fail**
- A) Mark it retryable with a short backoff applies correctly to transient failures — network timeouts, rate limits, or temporarily unavailable resources — where the same input may succeed moments later. Invalid regex syntax is deterministic: the same malformed pattern will fail on every attempt regardless of timing, making retries pure overhead.
- C) Suppress the error and return an empty result set would be appropriate only if an empty result is a valid, semantically meaningful outcome — for example, a legitimate search that matches nothing. Here it masks a broken query, causing the orchestrator to treat a failed operation as successful and propagate silently corrupt results downstream.
- D) Mark it retryable with increased timeout misdiagnoses the failure class: regex validation is a synchronous parse step with negligible CPU cost, not a latency-bound operation. Extended timeouts are the right lever for slow external I/O or resource contention, not for a parser rejecting ill-formed syntax before any search begins.

---

### Question 39
`D2 · 2.3`

Your codebase exploration agent must call Grep to find symbol definitions before generating any boilerplate. Engineers report the agent occasionally skips Grep and generates code with undefined references. What tool_choice setting enforces Grep as the first call?

- A) Set tool_choice to {"type": "none"} and rely on the system prompt to mandate Grep first.
- B) Set tool_choice to {"type": "any"} to require the model use at least one tool, making Grep likely.
- C) Set tool_choice to {"type": "tool", "name": "Grep"} to force Grep as the next tool call.
- D) Set tool_choice to {"type": "auto"} so the model selects Grep when context suggests it is needed.

**Correct answer:** C

**Why C is correct**
Forcing {"type": "tool", "name": "Grep"} removes the model's discretion entirely — the next turn must be a Grep call, not merely a likely one, which directly closes the gap engineers observed where boilerplate got generated against undefined symbols. This is the only setting that turns 'call Grep before generating boilerplate' from a convention into an API-enforced sequencing guarantee.

**Why the others fail**
- A) Set tool_choice to none disables all tool execution, making Grep uncallable regardless of system-prompt instructions. Prompt-level mandates cannot override an API-level tool lockout, so this is a category mistake rather than a stricter form of enforcement.
- B) Set tool_choice to any guarantees a tool call occurs but does not constrain which tool — the model may satisfy the requirement by calling a different tool entirely, leaving Grep optional. This setting fits workflows where using any available tool is sufficient, not ones that require a specific, ordered first step.
- D) Set tool_choice to auto leaves Grep selection probabilistic — the model may skip it when context seems sufficient to generate code directly, which is exactly the failure mode engineers are observing. Auto is the right setting when any of several tools may be appropriate and the model's judgment is trusted to choose.

---

### Question 40
`D2 · 2.1`

Your codebase exploration agent has an MCP tool find_symbol whose description says: "Locates a symbol definition in the repository." Engineers report the agent frequently calls Grep for symbol lookups instead, then falls back to find_symbol only after Grep returns too many hits. What revision to the find_symbol description would most reliably shift tool selection?

- A) Add a system prompt instruction telling the agent to try find_symbol first whenever an engineer mentions a symbol name.
- B) Add input format, an example query, and a boundary stating find_symbol should be preferred over Grep for definition lookups.
- C) Raise find_symbol in the tool array ordering so the model encounters it before Grep during tool selection reasoning.
- D) Rename the tool to grep_symbol_definition so the agent associates symbol queries with the existing Grep selection pathway.

**Correct answer:** B

**Why B is correct**
Co-locating an input format, a concrete example query, and an explicit precedence boundary in find_symbol's own description gives the model the exact semantic signal it lacks — that this is a definition lookup, not a text scan — right where tool-selection reasoning consults it. That directly reverses the observed pattern of exhausting Grep first: with a boundary stating find_symbol is preferred for definition lookups, the model can discriminate the two tools on the query itself rather than on trial-and-error fallback.

**Why the others fail**
- A) Add a system prompt instruction telling the agent to try find_symbol first moves the tool boundary out of the tool interface and into ambient context — a pattern that degrades as the system prompt grows and instructions compete for attention. This would be appropriate when a tool cannot be modified (e.g., a third-party MCP server), but the 2.1 principle is that boundaries belong in the tool description itself, co-located with the capability they govern.
- C) Raise find_symbol in the tool array ordering assumes the model performs a sequential, first-match scan during tool selection reasoning. A practitioner familiar with attention-based models might intuit that earlier positions carry salience weight. In practice, tool selection is driven by description semantics, not array position; reordering without enriching the description leaves the selection signal unchanged.
- D) Rename the tool to grep_symbol_definition so the agent associates symbol queries with the Grep pathway conflates tool naming with semantic clarity. A practitioner might reach for this when they observe the model anchoring on 'grep' as a pattern-match trigger. However, renaming without a description rewrite still leaves the model unable to distinguish definition lookup from broad text search — the semantic boundary is missing regardless of the tool name.

---

### Question 41
`D1 · 1.6`

Your developer-productivity agent must review a 47-file pull request touching three services. Per-file analysis fits in context; reasoning across all 47 files at once does not. Cross-service contracts (auth handshake, queue schema) must also be checked. Using Read and Grep, which decomposition handles both per-file detail and cross-file invariants?

- A) Read all 47 files into context in one turn and reason globally with Grep for cross-references.
- B) Run a per-file local pass on each of the 47 files, then a final cross-file integration pass over the per-file summaries.
- C) Spawn 47 parallel subagents, one per file, and let the coordinator merge their outputs, skipping the integration step for the auth handshake and queue schema contracts.
- D) Run Grep across all 47 files for cross-service contracts, then a single global pass on the matches.

**Correct answer:** B

**Why B is correct**
Each file stays within its own context window for local defect detection, and the final pass operates only over the condensed per-file summaries — small enough to fit alongside cross-service reasoning about the auth handshake and queue schema. This two-stage structure is what lets a 47-file PR clear the stated context ceiling while still guaranteeing invariants that span service boundaries get checked, not just detail within each file.

**Why the others fail**
- A) Read all 47 files into context violates the stem's explicit constraint that reasoning across all 47 files simultaneously exceeds context budget. A practitioner might reach for this when the file count is lower or the model's context window is larger — in those conditions, a single global pass is the simpler, correct choice.
- C) Spawn 47 parallel subagents is a legitimate fan-out pattern when per-file isolation is sufficient and results can be aggregated structurally. The gap is architectural: each subagent reasons in isolation, so cross-service contracts — auth handshakes, queue schemas — that span file boundaries are never resolved; the coordinator receives 47 independent reports with no integration pass to check invariants.
- D) Run Grep across all 47 files narrows the context problem by focusing only on contract-relevant matches, which is exactly right when cross-service invariants are the sole concern. It fails here because per-file detail (logic errors, intra-file bugs) is never examined — Grep surfaces references but not the surrounding implementation context each file requires.

---

### Question 42
`D1 · 1.3`

Your developer productivity coordinator uses Grep to find affected modules and then needs to run a Read subagent and a Bash subagent simultaneously on those modules. What enables parallel execution?

- A) Set the coordinator's system prompt to 'run subagents in parallel when independent'.
- B) Spawn the Read subagent first, then await its result via the Agent tool before spawning the Bash subagent on the same modules.
- C) Add 'Agent' to the coordinator's allowed_tools and issue both Agent tool calls in one response turn.
- D) Configure both subagents with the same AgentDefinition and set max_parallel=2.

**Correct answer:** C

**Why C is correct**
Because the modules from Grep are already resolved and neither subagent depends on the other's output, the coordinator can dispatch both in one turn: with 'Agent' present in allowed_tools, issuing the Read and Bash Agent calls together lets the SDK schedule them concurrently rather than one at a time. This invocation pattern — multiple tool calls in a single response turn — is the only lever that produces true concurrency here, guaranteeing overlap that sequential await-then-spawn can only approximate.

**Why the others fail**
- A) Set the coordinator's system prompt to 'run subagents in parallel...' is a category mistake: natural-language instructions in a system prompt cannot alter the SDK's execution model. Prompt instructions govern reasoning and tool-selection behavior; only issuing multiple Agent tool calls within a single response turn causes the runtime to schedule them concurrently.
- B) Spawn the Read subagent first, await...' describes correct sequential orchestration — the right pattern when the Bash subagent's inputs depend on Read's outputs. Here the modules are already known from the Grep step, so the two subagents are independent; awaiting Read before spawning Bash serializes work that could be concurrent.
- D) Configure both subagents with the same AgentDefinition' appeals because sibling agents sharing a definition feels like a natural parallelism control — but max_parallel is not an Agent SDK configuration field at any level. This option would be correct-shaped if the SDK exposed a concurrency parameter, but it does not; parallelism is a product of invocation pattern, not agent configuration.

---

### Question 43
`D1 · 1.7`

An engineer paused a Claude Agent SDK session mid-refactor; overnight, teammates hand-edited three of the files the agent had already loaded via Read. The next morning she calls query() with resume=session_id to finish the refactor. What is the most reliable way to ensure the resumed agent works from the current file contents rather than the versions captured earlier?

- A) Register a PostToolUse hook matching Edit|Write that logs file changes, then replay the hook log when the session resumes.
- B) Pass fork_session=True alongside resume=session_id so the branched session loads a fresh view of the working directory from disk.
- C) Use continue_conversation=True instead of resume, since continue re-scans the filesystem while resume only replays the stored conversation history.
- D) In the resume prompt, explicitly instruct the agent to Read the three modified files again before proposing any further edits.

**Correct answer:** D

**Why D is correct**
Since resume replays stored history and the SDK performs no automatic disk re-scan, the only mechanism that guarantees current content is an explicit new Read call in the resumed prompt, forcing the tool to re-fetch the three teammate-edited files from disk. This works regardless of session/fork/hook plumbing because it bypasses replayed state entirely and queries the filesystem fresh, which is exactly what the overnight hand-edits require.

**Why the others fail**
- A) "Register a PostToolUse hook matching Edit|Write" captures tool invocations the agent makes during a live session, not external edits applied while the process was paused. Hooks observe in-session events only; they cannot bridge out-of-band filesystem mutations. This pattern is correct for auditing or triggering side effects on changes the agent itself authors.
- B) "Pass fork_session=True alongside resume=session_id" is appealing because forking implies a clean divergence — practitioners assume that means fresh state. But fork_session branches conversation history only; the forked branch still replays the same stale Read results. Use fork_session when you need parallel exploration of alternative reasoning paths, not to refresh disk contents.
- C) "Use continue_conversation=True instead of resume" exploits a real API distinction, but both parameters replay stored conversation history — continue_conversation simply targets the most recent session without requiring an explicit ID. Neither triggers filesystem re-scanning. continue_conversation=True is the correct parameter when you want same-process continuation without pinning a specific session_id.

---

### Question 44
`D2 · 2.1`

An agent helping engineers explore codebases has tools named search_code and search_docs. Both have empty descriptions. The agent calls search_docs when looking for function definitions instead of search_code. What is the most direct fix?

- A) Swap the positions of search_code and search_docs in the tool list so search_code appears first
- B) Add a router layer in the system prompt that maps query types like 'function definitions' or 'documentation lookups' to tool names, requiring the agent to parse natural-language routing rules before every search call
- C) Add descriptions that define what each tool searches: search_code for source file content and function definitions; search_docs for documentation and README files
- D) Merge the tools and add a type parameter so the agent selects the search domain at call time

**Correct answer:** C

**Why C is correct**
With both tools currently undescribed, the agent has no signal distinguishing source code from documentation, so it defaults to whichever tool name or ordering happens to match loosely. Populating each description with its concrete search domain — source file content and function definitions versus documentation and README files — gives the agent the exact disambiguating information needed to route the 'function definitions' query to search_code deterministically at selection time.

**Why the others fail**
- A) "Swap the positions of search_code" assumes list order influences the model's tool selection. Position matters only when a long tool list is truncated mid-context and earlier entries survive; with two tools, ordering has no effect — descriptions are the routing signal, and both tools have none.
- B) "Add a router layer in the system prompt" is a real disambiguation pattern, appropriate when tools have overlapping domains or routing logic too complex for a description. Here the domains are cleanly disjoint; a description-level fix is sufficient and more robust than probabilistic prompt instructions.
- D) "Merge the tools and add a type parameter" is valid when tools share substantial implementation and the distinction is minor. It shifts domain disambiguation to call time, requiring the agent to infer what each type value means — the same knowledge gap that well-written descriptions close earlier, at selection time.

---

### Question 45
`D1 · 1.3`

Your developer-productivity agent uses Grep to locate 14 legacy config files across the codebase, then spawns a config-migrator subagent via the Agent tool to rewrite them. The subagent returns 'no matching files found' even though the Grep hits are clearly visible in the parent transcript. What is the correct fix?

- A) Set fork_session=True on the parent options so the config-migrator branches from the parent session and inherits the accumulated Grep output.
- B) Load project CLAUDE.md via setting_sources=['project'] so the resolved file list is shared between parent and subagent through project memory.
- C) Embed the Grep result paths directly in the Agent tool prompt string; subagents receive no parent conversation history or tool results.
- D) Add Grep to the config-migrator AgentDefinition.tools so the subagent can rerun the search inside its own context before attempting any rewrites.

**Correct answer:** C

**Why C is correct**
The Agent tool is a prompt-in/result-out call: the config-migrator starts with an empty context and never sees the parent's transcript or Grep results. Because the 14 file paths only exist in the parent's tool output, the fix is to write them explicitly into the spawning prompt string — this is the only channel that reliably delivers them, guaranteeing the subagent operates on the exact resolved set rather than whatever it might rediscover on its own.

**Why the others fail**
- A) fork_session controls branching for resumed sessions, not Agent-tool spawning; no such parameter injects parent conversation history into a newly spawned subagent. Practitioners familiar with session-continuation semantics may reach for it, but Agent-tool invocations are prompt-in/result-out calls with no shared transcript.
- B) setting_sources=['project'] correctly propagates static project instructions — conventions, constraints, personas — into a subagent's context. Runtime Grep output is ephemeral and never written to CLAUDE.md, so this channel cannot carry the resolved file paths the subagent needs.
- D) A practitioner reasoning 'subagent can't find files → give it search capability' is correct when the subagent must perform its own discovery independently. Here the parent already holds the Grep output; equipping the subagent with Grep triggers redundant re-search and still does not transfer the parent's findings into the subagent's prompt.

---

## S6 · Structured data extraction

### Question 46
`D5 · 5.3`

An extraction pipeline submits a Message Batches API job. The batch processor encounters a malformed custom_id in one request and silently skips it, returning a results array without the skipped entry. The caller checks result count against submission count and finds a mismatch. What would have prevented the mismatch from becoming a silent data loss?

- A) The caller should have validated custom_id format before submission to prevent malformed entries
- B) The batch processor should have set isRetryable to false on the malformed request before skipping it, flagging the entry for asynchronous retry instead of surfacing the failure.
- C) The batch processor should have returned a structured error entry for the malformed custom_id rather than omitting it from results
- D) The Message Batches API automatically surfaces skipped entries in a separate errors array

**Correct answer:** C

**Why C is correct**
A structured error entry keyed to the malformed custom_id keeps the results array length matched to the submission count, so the caller's count-based check either passes cleanly or fails on a real, inspectable error record — never a silent gap. This converts the processor's internal skip decision into an observable failure the caller can branch on, which is the only way count reconciliation catches a dropped extraction instead of masking it as a false success.

**Why the others fail**
- A) "Caller validates custom_id before submission..." is sound defensive practice and would eliminate bad inputs upstream, but it leaves the processor's behavior on encountering one undefined. Input validation and structured error emission are complementary layers; the question targets what the processor must do once a malformed entry arrives despite upstream guards.
- B) "Set isRetryable to false..." governs retry disposition for permanently invalid inputs — a valid concern — but does not emit a result slot for the skipped entry. The right pattern when retry is inappropriate pairs that flag with a structured error entry so the caller sees a failure record rather than a gap.
- D) "Message Batches API automatically surfaces skipped entries..." misrepresents the API contract: the API returns results only for requests it actually processed; entries silently dropped by processor logic are invisible at the API layer entirely. This is a category error about how the API works, not an adjacent pattern.

---

### Question 47
`D4 · 4.6`

Your extraction system uses model self-reported confidence scores to route outputs for human review. When a JSON schema validation fails, the model reports high confidence but produces structurally invalid output. What routing strategy best handles this conflict?

- A) Run a second extraction pass automatically for any low-confidence result, bypassing schema checks on the retry.
- B) Override confidence scores with JSON schema validation results, flagging schema failures for human review regardless of reported confidence.
- C) Trust model confidence scores as the primary signal and skip JSON schema validation for high-confidence extractions.
- D) Combine confidence score and schema validity into a weighted score, routing to human review only when both signals fall below a jointly configured threshold.

**Correct answer:** B
**Your answer:** D ✗

**Why B is correct**
Schema validation is a deterministic pass/fail check on structural correctness, while confidence reflects the model's own (potentially miscalibrated) uncertainty estimate — the two operate on different failure modes, so the objective signal must take precedence when they conflict. Routing every schema failure to human review regardless of reported confidence guarantees no structurally invalid output silently reaches downstream systems, closing the exact gap this scenario exposes.

**Why the others fail**
- A) Run a second extraction pass... correctly identifies retry logic as a remediation tool and is the right pattern when low confidence signals ambiguous input. It fails here because schema failures are deterministic errors, not probabilistic ones — a second pass may reproduce the same structural violation, and skipping schema checks on retry removes the only objective gate.
- C) Trust model confidence scores... appeals to practitioners who treat confidence as a reliable proxy for output quality. However, confidence scores measure the model's uncertainty about its own generation, not structural compliance — a model can be highly certain about content that violates schema constraints, making confidence orthogonally miscalibrated for validation purposes.
- D) Combine confidence score and schema validity... reflects sound ensemble-signal thinking and would be appropriate when both signals are probabilistic. Schema validity is binary and non-negotiable: a weighted blend allows a high-confidence score to numerically offset structural invalidity, permitting malformed outputs to bypass review entirely.

---

### Question 48
`D4 · 4.2`

Your extraction system processes invoices with varying layouts. After adding few-shot examples to the prompt, validation against the JSON schema shows fewer missing fields. What does this improvement demonstrate?

- A) JSON schema validation automatically corrects missing fields at runtime.
- B) Increasing temperature improves extraction consistency across document types.
- C) Few-shot examples reduce token usage by compressing the output format.
- D) Few-shot examples help the model infer structure from varied document layouts.

**Correct answer:** D

**Why D is correct**
Invoices arrive with inconsistent layouts, so the model has no single template to rely on; demonstrated exemplars show it how field labels and values map across those variations. The drop in missing-field failures against the schema confirms the model is generalizing extraction patterns from the examples, not just memorizing one layout, which is exactly what few-shot prompting guarantees over a zero-shot approach.

**Why the others fail**
- A) JSON schema validation automatically corrects... appeals because schemas are a natural partner to extraction pipelines, and practitioners sometimes conflate validation with remediation. Schemas detect and reject malformed output; they do not synthesize missing field values. The scenario where schema tooling does fill gaps is a post-processing layer (e.g., a fallback default-injection step), which is a separate architectural component, not the validator itself.
- B) Increasing temperature improves extraction... is tempting when outputs feel rigid or incomplete, since higher temperature is associated with more generative breadth. In practice, extraction tasks demand low-temperature determinism; raising temperature increases output variance and hallucination risk, which worsens consistency across document types. Higher temperature is appropriate for creative generation, not structured field extraction.
- C) Few-shot examples reduce token usage... conflates two distinct mechanisms. Examples added to a prompt consume additional tokens rather than compressing output. Token efficiency techniques — such as constrained decoding, structured output modes, or schema-enforced generation — are orthogonal to few-shot prompting and operate at the inference layer, not the prompt layer.

---

### Question 49
`D4 · 4.6`

Your extraction system validates outputs against a JSON schema, but accuracy degrades on edge cases. You want a second review pass. What approach is most effective?

- A) Increase the temperature setting to improve edge-case handling
- B) Add more examples of edge cases to the JSON schema definition
- C) Add a system prompt instruction telling Claude to double-check its own output
- D) Run a separate Claude instance to independently validate the extracted output

**Correct answer:** D
**Your answer:** B ✗

**Why D is correct**
Instantiating a fresh Claude instance to check the extracted output against the schema gives a genuinely independent second opinion, with no exposure to whatever reasoning path produced the original edge-case error. Because the reviewer never inherited the extractor's assumptions, it can catch systematic misreads that the same instance reviewing itself would simply repeat, which is exactly the gap degrading accuracy here.

**Why the others fail**
- A) Increase the temperature setting controls sampling stochasticity, not the model's ability to detect schema violations or reason about edge-case constraints. A practitioner might reach for this when outputs feel repetitive or too conservative, but temperature is irrelevant to review quality and may introduce new errors.
- B) Add more examples of edge cases misapplies the purpose of JSON Schema: the spec defines structural constraints (types, required fields, allowed values), not worked examples for the model to learn from. Few-shot examples belong in the prompt context, not the schema definition, making this a category mistake rather than an adjacent-but-wrong pattern.
- C) Add a system prompt instruction relies on the same model instance reviewing its own output, making it susceptible to the same systematic errors and blind spots that produced the original result. Self-correction instructions are appropriate when the goal is stylistic refinement or formatting cleanup — not catching semantic extraction failures that stem from model-level misunderstanding.

---

### Question 50
`D5 · 5.4`

Your extraction system stores JSON schema validation rules only as conversation instructions. After running /compact mid-session, which of these rules are still active?

- A) Rules survive if they were referenced in the last tool_use call
- B) None — conversation-only instructions are lost after compaction
- C) All rules persist because /compact preserves tool definitions
- D) Rules are automatically written to MEMORY.md before compaction

**Correct answer:** B
**Your answer:** C ✗

**Why B is correct**
/compact rebuilds context from the summary plus a fresh disk read of project-root CLAUDE.md; conversation-only instructions like the JSON schema validation rules are never written to disk, so the summarizer has nothing to re-inject. Since this extraction system stored the rules purely as conversation instructions, none of them remain active after compaction — the coordinator must re-supply them or move them into CLAUDE.md to guarantee persistence.

**Why the others fail**
- A) Recency-of-reference feels like a plausible signal — one might expect /compact's summarizer to retain instructions that were active at the moment of compaction. In practice, /compact produces a prose summary of the session; it does not selectively persist instructions based on adjacency to the last tool_use block.
- C) Tool definitions in the API tools array do survive compaction — they're re-injected at the structural layer, not stored in conversation history. That persistence applies only to tool schemas, not to natural-language validation logic added as mid-session conversation instructions.
- D) CLAUDE.md is the correct persistence target for rules that must survive compaction, making this distractor feel close. The mechanism is manual, however — an agent must be explicitly directed to write state to disk; no automatic pre-compaction flush to MEMORY.md exists.

---

### Question 51
`D4 · 4.2`

Your extraction system uses a JSON schema to validate output, but fields like address are sometimes null, sometimes an empty string, and sometimes omitted entirely. Which few-shot strategy best demonstrates ambiguous-case handling for this scenario?

- A) Include examples where address is null, empty string, and omitted, each paired with the normalized output the schema expects.
- B) Add a schema constraint requiring address to always be a non-empty string, eliminating the ambiguity before extraction runs.
- C) Provide examples covering only the most common case and add a fallback prompt instruction for edge cases.
- D) Include one canonical example with a populated address and rely on the schema validator to reject malformed variants at runtime.

**Correct answer:** A

**Why A is correct**
Demonstrating all three inbound surface forms — null, empty string, and omitted key — each mapped to the same normalized output teaches the model the schema's convention directly from examples rather than inference. Since all three variants recur regularly in this extraction system, only exhaustive coverage guarantees consistent normalization; a validator or instruction can only catch or describe failures after the fact.

**Why the others fail**
- B) "Add a schema constraint..." appeals because upstream enforcement eliminates a whole class of extraction errors at the architecture level. It is the correct pattern when the source system is within your control and upstream normalization is feasible; here the ambiguity lives in inbound data the extractor must already handle, so tightening the output contract sidesteps rather than resolves it.
- C) "Provide examples covering only..." seems efficient when edge cases are sparse and a concise instruction unambiguously handles them. It is the right pattern when exceptions are genuinely rare; for competing normalization conventions like null vs. empty string vs. omitted, a natural-language fallback lacks the concrete referent that grounded examples supply.
- D) "Include one canonical example..." is reasonable when a single positive demonstration generalizes well and the schema validator functions as a correction backstop. It is the right split when ambiguous variants are rare; here null, empty string, and omitted each occur regularly, leaving two of the three surface forms undemonstrated and the normalization rule unenforced.

---

### Question 52
`D5 · 5.6`

An extraction pipeline uses a JSON schema that includes a 'regulation_status' field. Documents from different years are processed together. A downstream system applies an 'active' status from a 2019 document, unaware it was superseded in 2022. What field was missing from the JSON schema output?

- A) An isRetryable flag indicating whether the status field extraction should be reattempted
- B) A confidence score indicating extraction reliability for the regulation_status field
- C) A source document identifier field so the extraction can be traced back to its origin
- D) A document publication date field so downstream systems can assess temporal validity

**Correct answer:** D

**Why D is correct**
Because documents from different years are mixed in the same pipeline run, the schema needed a publication date on each extracted record so a downstream consumer could compare document vintage against known revision cycles before trusting a status value. Without it, 'active' from the 2019 document carries no signal that a newer, superseding document might exist, so the 2022 change silently gets ignored. This is the only field that directly encodes temporal ordering, which is what the misinterpretation actually hinged on.

**Why the others fail**
- A) An isRetryable flag is a pipeline-orchestration signal — it indicates whether a failed extraction step can be safely re-run — and has no bearing on data temporal validity or provenance. This is a category mismatch; no retry semantics would expose that a 2019 status was superseded by a later document.
- B) A confidence score addresses extraction fidelity — whether the pipeline correctly read the field from the source text — not whether that value remains temporally current. It would be appropriate when the extraction itself is unreliable (e.g., low-quality OCR, ambiguous markup), where flagging uncertain reads prevents incorrect values from propagating downstream.
- C) A source document identifier enables audit tracing — confirming which document produced a given value — but does not encode when that document was published. It would be the right missing field if the problem were inability to trace extracted values back to their origin for debugging or compliance purposes, rather than temporal supersession.

---

### Question 53
`D4 · 4.2`

Your extraction pipeline emits a JSON schema field employment_status with enum values employed, self_employed, unemployed. Production logs show Claude inconsistently classifies gig workers and contractors, sometimes picking employed, sometimes self_employed. How should few-shot examples in the prompt best address this ambiguity?

- A) Include examples of gig and contractor documents paired with the expected label and a brief rationale tying the decision to schema definitions.
- B) Expand the JSON schema description field for employment_status with explicit definitions of gig worker and contractor boundaries.
- C) Provide examples showing the model refusing to classify and emitting a null value whenever contractor language appears in the source.
- D) Add examples covering every enum value uniformly so the model sees balanced coverage across all possible employment classifications.

**Correct answer:** A

**Why A is correct**
Anchoring each gig/contractor example to a rationale that cites the schema's enum definitions gives the model a transferable decision rule for the exact boundary causing inconsistent labels, rather than just another data point to pattern-match. This directly targets the observed failure — flip-flopping between employed and self_employed on the same worker type — by showing how the schema's distinctions resolve it.

**Why the others fail**
- B) "Expand the JSON schema description field" addresses the right gap — defining gig and contractor boundaries — but through schema documentation, not a few-shot signal. It would be the correct fix if the schema had no definitions at all and the few-shot examples were already well-targeted at the ambiguous cases.
- C) "Provide examples showing the model refusing" trains abstention, a valid pattern when misclassification cost exceeds the cost of a null. The correct context is a pipeline where downstream logic handles nulls gracefully and a wrong employment label carries compliance or legal liability; the goal in this scenario is correct classification, not deferral.
- D) "Add examples covering every enum value" appeals to the intuition that uneven shot distribution causes label bias — a real concern if the model had never seen a particular enum value. Here the failure is localized to one boundary; spending shots on already-correct employed and unemployed cases dilutes the budget without targeting the actual failure mode.

---

### Question 54
`D5 · 5.2`

Your extraction system processes complaint letters via tool_use against a JSON schema. A reviewer proposes routing any document containing strong negative sentiment (angry tone, profanity) to senior human reviewers, leaving neutral letters for automated extraction. Pilot data shows the same complex multi-clause arbitration disclosures show up in both angry and neutral letters. Why is sentiment-based escalation a poor proxy for routing extraction complexity here?

- A) Sentiment scoring is non-deterministic across calls, causing identical letters to be routed inconsistently between automated and human queues even when their underlying arbitration clause structure is unchanged.
- B) Document tone and structural extraction complexity vary independently, so sentiment cannot signal which letters contain the multi-clause arbitration disclosures.
- C) Sentiment classification adds latency to the extraction pipeline and reduces overall throughput compared to a pure schema validation gate.
- D) Negative sentiment frequently triggers safety filters in Claude, so documents would be refused before reaching the JSON schema validation step, regardless of whether they contain arbitration disclosures or routine complaint language.

**Correct answer:** B
**Your answer:** A ✗

**Why B is correct**
Extraction difficulty is driven by document structure — clause count, nesting, cross-references in arbitration disclosures — not by the writer's emotional register, and the pilot's own data shows both attributes occur across all tone levels. A routing rule keyed on sentiment therefore sends structurally simple angry letters to scarce senior reviewers while letting structurally complex neutral letters through automated extraction unflagged, guaranteeing misrouting regardless of classifier accuracy.

**Why the others fail**
- A) LLM-based classifiers do exhibit run-to-run variance, and non-determinism is the decisive objection when a compliance audit trail requires identical documents to route identically on every call. Here, however, the routing logic fails even with a perfectly consistent classifier because tone and structural complexity vary independently.
- C) Throughput cost is a legitimate reason to prefer a cheaper routing signal over a heavier classifier stage, and latency alone can justify swapping sentiment for a faster heuristic. It does not refute the routing logic itself; sentiment would misroute letters even if the classifier were instantaneous.
- D) This mischaracterizes Claude's content-handling behavior: complaint letters and profanity-laden text in a tool_use extraction context are processed, not refused. Safety filters govern harmful generation outputs, not incoming document tone — making this a category mistake with no adjacent scenario where it holds.

---

### Question 55
`D4 · 4.3`

Your extraction system validates output with a JSON schema and all responses parse cleanly. A sample audit finds that extracted invoice totals match the numeric type constraint but are sometimes the subtotal rather than the final total. What does this reveal?

- A) The JSON schema enforces that total_amount is a number but cannot enforce which amount on the document is the correct total
- B) The JSON schema needs a minimum value constraint on total_amount, set higher than any subtotal, to exclude subtotals from the total_amount field
- C) The output_config json_schema enforcement is less strict than tool_use strict mode for numeric fields
- D) The extraction system should add a required subtotal field so Claude distinguishes the two amounts

**Correct answer:** A

**Why A is correct**
Type validation only confirms total_amount holds a number — it has no visibility into invoice layout or which line represents the pre-adjustment sum versus the final payable figure. Because subtotal and final total are both valid numbers, a schema-clean response can still populate the field with the wrong one, since selecting the correct amount is a document-understanding task the schema was never designed to perform.

**Why the others fail**
- B) A minimum value constraint would exclude totals below some threshold, but a subtotal can be larger than a final total (e.g., before discounts) and any plausible threshold is arbitrary. The minimum keyword enforces numeric range, not document-level semantic identity — it cannot distinguish 'this number is the invoice's bottom line' from 'this number is a line-item sum'.
- C) output_config json_schema and tool_use strict mode both enforce structural and type constraints; neither mechanism inspects the source document to verify semantic correctness of the extracted value. This conflation would be relevant if responses were structurally malformed, but all responses parse cleanly — the fault is semantic, not syntactic.
- D) Adding a required subtotal field adds a structural scaffold that would be correct if the bug were Claude conflating two clearly labeled fields. Here, the schema already has a total_amount field — the problem is that Claude's extraction judgment selects the wrong document amount for it, and introducing a parallel field does not constrain which value populates either one.

---

### Question 56
`D5 · 5.5`

*(This question appeared twice, verbatim identical, in the source export — shown once here.)*

Your extraction system validates output against a JSON schema before forwarding to downstream services. When Claude returns a response that fails schema validation, what should the system do?

- A) Log the failure and discard the document without further action
- B) Forward the invalid output with a warning flag to the downstream service
- C) Route the failed extraction to a human review queue for manual correction
- D) Retry the extraction request up to three times automatically

**Correct answer:** C
**Your answer:** A ✗

**Why C is correct**
A schema-validation failure is a deterministic signal that the extraction is unreliable, and since the system sits upstream of downstream services that depend on the schema contract, routing to a human review queue is the only path that both prevents propagation of bad data and preserves the document for correction. This guarantees the extraction is fixed and re-validated before it ever reaches those services, rather than merely masking or losing the failure.

**Why the others fail**
- A) "Log the failure and discard" is appropriate in high-throughput streams with automatic re-ingestion or TTL-bounded records. Extraction pipelines typically process unique, non-recoverable source documents — silent discard permanently forfeits the data with no path for manual correction.
- B) "Forward the invalid output" fits loosely-coupled audit pipelines where consumers are explicitly designed to handle partial or malformed records. In a strict schema-contract pipeline, propagating invalid output shifts the corruption burden downstream, risking cascading data integrity failures across every dependent service.
- D) "Retry the extraction request" appeals to practitioners who treat validation failure as a transient fault. Automatic retries are correct for stochastic errors (rate limits, timeouts); schema validation failure is deterministic — re-calling without changing the prompt or schema reproduces the same malformed output.

---

### Question 57
*(Not present in the source export. The question numbering jumps directly from two consecutive "Q 56/60" captures to "Q 58/60" — no Q57 content was captured, so there is nothing to format here.)*

---

### Question 58
`D5 · 5.3`

An extraction pipeline calls a tool that validates JSON schema compliance. The tool encounters a schema it cannot parse and returns an empty validation report instead of an error. Downstream steps treat an empty report as 'no violations found'. What antipattern does this exhibit?

- A) Retry exhaustion: the tool should have retried schema parsing before returning
- B) Silent error suppression: returning empty as success masks the parse failure from downstream steps
- C) Incorrect isRetryable flag: the tool should have set isRetryable to false on the empty report
- D) Policy gap: no escalation rule exists for unparseable schemas

**Correct answer:** B

**Why B is correct**
The defect is the tool fabricating a success signal: an unparseable schema is a distinct failure mode from zero violations, yet both collapse into the same empty report. Because downstream steps trust that emptiness means compliance, the parse failure is masked exactly where the pipeline needed to see it — the tool must surface the parse error as an error, not as a clean result.

**Why the others fail**
- A) "Retry exhaustion" targets a different failure mode — a tool that abandons a transient operation before exhausting its allotted attempts. It applies when schema parsing fails intermittently and a subsequent call could succeed; the defect here is the misleading return value itself, not the attempt count.
- C) "Incorrect isRetryable flag" addresses retry-metadata labeling, which only matters once an actual error object exists to label. The tool emitted an empty report — a fabricated success signal — so no error metadata was in play; correcting a flag on a non-error response leaves the suppression intact.
- D) "Policy gap" describes a missing escalation rule at the orchestration layer — relevant when a tool correctly surfaces an error but no handler is configured to route it. Here the error is never surfaced at all; suppression occurs before orchestration sees the result, so no policy could be triggered regardless.

---

### Question 59
`D4 · 4.5`

Your structured data extraction system submits documents to the Message Batches API. Results arrive out of order. Which field lets you match each result back to its original request?

- A) The batch id returned when the batch was created
- B) The position index of the result in the JSONL file
- C) The timestamp in the created_at field of the batch object
- D) The custom_id field provided when each request was submitted

**Correct answer:** D

**Why D is correct**
Because results arrive out of order, matching must rely on an identifier carried inside each result rather than its position or a batch-wide field. The custom_id is developer-assigned per request and echoed back on the corresponding result line, so it guarantees a correct one-to-one mapping regardless of return order — unlike the batch id or timestamp, which identify the batch, not the request.

**Why the others fail**
- A) The batch id returned when the batch was created identifies the entire batch as a whole, not individual requests within it. A practitioner new to the Batches API might conflate batch-level and request-level identifiers. The batch id is the correct field to use when polling for batch status or retrieving results from the API.
- B) The position index of the result in the JSONL file is tempting because JSONL is line-delimited and indexed. However, the API explicitly does not guarantee result ordering, so positional alignment with the original submission order is unreliable. Positional matching would be the right approach only if the API guaranteed order preservation, which it does not.
- C) The timestamp in the created_at field belongs to the batch object and records when the batch was created, not when any individual request was submitted. It carries no per-request identity. This would be a category mistake — timestamp fields convey when, not which.

---

### Question 60
`D4 · 4.3`

Your extraction system uses output_config with a JSON schema that includes a confidence field with enum [high, medium, low]. All outputs are schema-valid. A downstream system finds 15% of 'high' confidence extractions are factually wrong. What does this reveal?

- A) The extraction system needs stricter required fields in the schema to reduce hallucination
- B) The enum range is too narrow; adding a 'very_high' tier alongside high, medium, and low would improve accuracy discrimination on extraction outputs
- C) The confidence enum enforces which values are output but cannot guarantee the assigned confidence level is calibrated
- D) The output_config schema should be switched to tool_use instead of structured JSON output to get better confidence calibration on the enum field

**Correct answer:** C

**Why C is correct**
The 15% error rate lands specifically among 'high' confidence outputs, which is exactly what schema validation cannot catch: the enum guarantees Claude emits one of high/medium/low, not that its judgment of extraction correctness is trustworthy. Fixing this requires calibration work — human-labeled accuracy checks or confidence thresholding downstream — not tighter schema constraints.

**Why the others fail**
- A) Required fields address structural completeness, ensuring every output includes its expected properties. They are the right lever when downstream failures stem from missing fields, not from a model populating all fields with confidently wrong values. Semantic miscalibration is invisible to schema validators.
- B) Practitioners conflate expressive vocabulary with calibration resolution — more tiers feel like they give the model finer discrimination. A wider enum is the right fix when downstream systems need more routing granularity, but it cannot alter whether the model's chosen tier matches actual extraction accuracy.
- D) tool_use is the correct structural remedy when extractions violate the schema — it enforces format more reliably than output_config. Both mechanisms output whichever enum value the model assigns; neither enforces that the chosen value is semantically calibrated to factual correctness.
