---
tags: [ccaf, glossary]
---

# Glossary

Short, plain definitions for the terms of art used across the CCAF domain notes.
Each entry says what the term means and, where useful, which domain note develops
it. Definitions are kept faithful to how the course sources and the official exam
guide use each term. For the directory or file *location* a term lives in — every
`.claude/` folder and its project-root companions — see
[[Claude Main Files and Directories]] instead of hunting across entries here.

## A

### AgentDefinition

The configuration object that describes a subagent type: its
description, system prompt, and the tools it is allowed to use. Lets a coordinator
spawn specialised subagents with scoped behaviour. See [[1 - Agentic Architecture & Orchestration]].

### Agentic loop

The cycle where you send a request, inspect the `stop_reason`,
run any tool the model asked for, append the result to the conversation, and send
again — continuing while `stop_reason` is `tool_use` and stopping on `end_turn`.
The loop is driven by the model's decisions, not by parsing its prose. See [[1 - Agentic Architecture & Orchestration]].

### AI fluency

The framework (Delegation, Description, Discernment, Diligence)
for working effectively with AI: deciding what to hand off, describing it well,
judging the output, and doing so responsibly. See [[4 - Prompt Engineering & Structured Output]].

### allowedTools

The configuration field that scopes which tools an agent or
subagent may call. A coordinator needs `Task` in its `allowedTools` before it can
spawn subagents at all — the first thing to check when delegation silently fails.
See [[1 - Agentic Architecture & Orchestration]].

## B

### BM25

A lexical (keyword) ranking function that scores documents by exact term
matches. Strong on rare identifiers and codes; combined with embeddings in a hybrid
search. See [[5 - Context Management & Reliability]].

## C

### CallToolRequest / CallToolResult

The MCP message pair for running a tool: the client sends a
`CallToolRequest` naming the tool and its arguments, and the server executes it
and replies with a `CallToolResult` carrying the output. Follows a
[[Glossary#ListToolsRequest / ListToolsResult|ListToolsRequest/ListToolsResult]]
exchange in the connection flow. See [[2 - Tool Design & MCP Integration]].

### Case facts block

A small block of the hard, precise facts relevant to the task at hand —
amounts, dates, names, statuses — kept as structured data outside any
summarized narrative and repeated in full in every prompt. The point is that
summarizing text tends to soften exact details into vague language, so
anything that must stay exact goes in this block instead of in the part of
the context that gets condensed. See [[5 - Context Management & Reliability]].

### CLAUDE.local.md

A project-root file, distinct from `CLAUDE.md`, for private
notes on one specific repository — sandbox URLs, personal setup quirks,
architectural decisions you want Claude to hold in mind on your own branch.
It loads alongside the project `CLAUDE.md` but is git-ignored, so it never
reaches teammates. See [[Glossary#CLAUDE.md|CLAUDE.md]] and
[[3 - Claude Code Configuration & Workflows]].

### CLAUDE.md

A Markdown file that gives Claude Code persistent context, loaded
automatically at the start of every session. Managed policy, user, and project
copies all load together at launch and stack — nothing is dropped. A
directory-level copy is the exception: it loads later, on demand, only when
Claude reads a file under that directory. Scopes, broadest to most specific:

- **Managed policy** — a fixed OS-specific path your organization's platform
  team deploys via MDM, Group Policy, or similar (`/etc/claude-code/CLAUDE.md`
  on Linux/WSL, `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS,
  `C:\Program Files\ClaudeCode\CLAUDE.md` on Windows). It applies to every user
  and every repository on the machine, takes precedence over every other
  scope, and **cannot be excluded** by any user, project, or local setting —
  the one scope an individual can't opt out of.
- **User** (`~/.claude/CLAUDE.md`) — your personal preferences, applied across
  every project on your machine, never shared through version control.
- **Project** (`.claude/CLAUDE.md` or root `CLAUDE.md`) — the team-shared
  file, checked into the repository.
- **Directory** (a `CLAUDE.md` inside a subdirectory) — conventions scoped to
  files under that directory.

Unlike command-line system-prompt flags, `CLAUDE.md` persists across sessions
and CI runs. It is guidance, not enforced configuration — see
[[Glossary#Hook|Hook]] for the enforcement alternative. Contrast with
[[Glossary#CLAUDE.local.md|CLAUDE.local.md]], a different file for private,
git-ignored, project-specific notes. See
[[3 - Claude Code Configuration & Workflows]] and
[[Claude Main Files and Directories]] for the `.claude/` directories that
pair with it.
*Managed-policy paths, deployment mechanism, precedence, and the directory
scope's on-demand loading verified against the
[Claude Code memory docs](https://code.claude.com/docs/en/memory)
(checked 2026-09-06); everything else is in the course's own primary sources.*

### Content block

One piece of an API message: a text block (Claude's visible
reasoning or reply), a `tool_use` block (naming a tool and its input), or a
`tool_result` block (a tool's output sent back). A single message can carry
several blocks — for example, text followed by two `tool_use` blocks. See
[[2 - Tool Design & MCP Integration]].

### Context window

The practical limit on how much information a model can
consider at once — the conversation history, tool results, and instructions
that fit in a single request. Distinct from [[Glossary#max_tokens|max_tokens]],
which caps only the length of one reply and has no effect on how much prior
content the request carries. See [[5 - Context Management & Reliability]].

### Context degradation

The decline in answer quality over a long session: the
model starts giving inconsistent answers and citing "typical patterns" instead of
the specific things it discovered earlier. Countered with scratchpads, subagents,
and `/compact`. See [[5 - Context Management & Reliability]].

### Coordinator

In a multi-agent system, the agent that decomposes the task,
delegates to subagents, routes all inter-agent communication, handles errors, and
aggregates results (a hub-and-spoke pattern). See [[1 - Agentic Architecture & Orchestration]].

### Cosine similarity

A measure of how close two embedding vectors point in the
same direction, from -1 to 1; cosine distance is `1 - similarity`. Used to rank
semantic matches in retrieval. See [[5 - Context Management & Reliability]].

### custom_id

A field you attach to each request in a Message Batches API
submission so you can match responses back to requests and, on partial failure,
resubmit only the documents that failed rather than the whole batch. See
[[4 - Prompt Engineering & Structured Output]].

## D

### Direct resource

An MCP resource addressed by a fixed URI (for example
`docs://documents`), returning one specific piece of data. Contrast with a
[[Glossary#Resource template|resource template]], whose URI is parameterized to
answer a whole family of queries. Both are application-controlled context,
not tools the model calls. See [[2 - Tool Design & MCP Integration]].

## E

### Embedding

A list of numbers representing the meaning of a piece of text, so
that semantically similar texts sit close together in vector space. The individual
dimensions are not human-interpretable. See [[5 - Context Management & Reliability]].

### Eval workflow

The disciplined alternative to testing a prompt once (or a
few times) and calling it done: write an initial prompt, build a dataset of
representative inputs, feed each one through Claude, score the outputs with
a [[Glossary#Grader|grader]], then rewrite the prompt and repeat. Running a
prompt through this loop before production catches the unexpected inputs
that one-off testing misses. See
[[4 - Prompt Engineering & Structured Output#4.4 — Validation, retry, and feedback loops|4 - Prompt Engineering & Structured Output]].

### Evaluator-optimizer

An agentic pattern where one step produces output and
another evaluates it for gaps, feeding targeted follow-up work until coverage is
sufficient. See [[1 - Agentic Architecture & Orchestration]].

### Extended thinking

A mode where the model produces explicit reasoning before
its final answer, improving hard multi-step problems at the cost of extra tokens.
See [[5 - Context Management & Reliability]].

## F

### Few-shot prompt

A prompt that includes a handful of worked examples to
demonstrate the format and judgment you want, so the model generalises to new cases
rather than matching only pre-specified ones. See [[4 - Prompt Engineering & Structured Output]].

### fork_session

Creating an independent branch from a shared analysis baseline so
you can explore divergent approaches without disturbing the original session. See
[[1 - Agentic Architecture & Orchestration]].

### Frontmatter

A block of structured metadata placed at the very top of a text or
Markdown file, enclosed by two lines of three dashes (`---`). Claude Code
reads it to configure how the file behaves — the `context`, `allowed-tools`,
and `argument-hint` fields on a [[Glossary#SKILL.md|SKILL.md]], or the
`paths` glob on a rule in
[[Claude Main Files and Directories#.claude/rules/|`.claude/rules/`]]. A typical block
looks like:

```yaml
---
title: "My Blog Post"
date: 2026-09-06
author: "Jane Doe"
tags:
  - markdown
  - yaml
---
```

See [[3 - Claude Code Configuration & Workflows]].

## G

### Grader

The component that scores a prompt's output during an
[[Glossary#Eval workflow|eval workflow]], distinguished by *who or what*
assigns the score:

- **Code-based** — a deterministic check (valid JSON/Python/regex, output
  length, presence of certain words). Best for objective, mechanical
  properties.
- **Model-based** — a second Claude call scores the output against a
  rubric, typically 1–10. Best for quality and instruction-following that
  code cannot easily check.
- **Human-based** — a person scores the output or compares two versions.
  Best for the qualities hardest to automate: overall quality,
  comprehensiveness, depth, conciseness, relevance.

See [[4 - Prompt Engineering & Structured Output#4.4 — Validation, retry, and feedback loops|4 - Prompt Engineering & Structured Output]].

## H

### Hook

A configured script that fires on a lifecycle event (e.g. `PreToolUse`,
`PostToolUse`, `Stop`) to intercept, transform, or block behaviour. Hooks give
deterministic guarantees where prompt instructions give only probabilistic
compliance. See [[1 - Agentic Architecture & Orchestration]] and [[3 - Claude Code Configuration & Workflows]].

## I

### InstructionsLoaded

A hook that fires whenever a CLAUDE.md or `.claude/rules/` file loads into
context — useful for auditing exactly what made it in, the scripted
counterpart to running `/memory` interactively. See
[[1 - Agentic Architecture & Orchestration#1.5 Apply Agent SDK hooks for tool call interception and data normalization|1 - Agentic Architecture & Orchestration]]
and [[3 - Claude Code Configuration & Workflows]].

## J

### jq

A command-line JSON processor, not a Claude Code feature itself, used
downstream of a `-p` run's `--output-format json` output to pull a specific
field — typically the `structured_output` object a `--json-schema` run
produces — out of the response so it can be posted as inline PR comments or
fed to another script. See
[[3 - Claude Code Configuration & Workflows#3.6 — Integrating Claude Code into CI/CD pipelines|3 - Claude Code Configuration & Workflows]].

### JSON Schema

A formal description of the shape of a JSON object (fields, types,
which are required). Used with tool definitions to force schema-compliant output and
eliminate JSON syntax errors. See [[4 - Prompt Engineering & Structured Output]].

## L

### ListToolsRequest / ListToolsResult

The MCP message pair used to discover a
server's tools: the client sends a `ListToolsRequest` and the server replies
with a `ListToolsResult` listing what it offers. This is the mechanism behind
"tools from a connected server are discovered at connection time" — the client
runs this exchange during setup, before it can hand any of that server's tools
to the model. Calling a discovered tool is the separate
[[Glossary#CallToolRequest / CallToolResult|CallToolRequest/CallToolResult]]
exchange. See [[2 - Tool Design & MCP Integration]].

### Lost in the middle

The tendency of models to reliably use information at the
start and end of a long input while under-using material buried in the middle.
Mitigated by putting key findings first and using clear section headers. See
[[5 - Context Management & Reliability]].

## M

### max_tokens

A required field on every Messages API request that caps how much
Claude may generate in that one reply. It bounds output length only — it has no
effect on how much conversation history or tool output the request can carry,
which is a separate [[Glossary#Context window|context-window]] concern. Hitting
the cap mid-generation is what produces the [[Glossary#stop_reason|stop_reason]]
value `max_tokens`. See [[2 - Tool Design & MCP Integration]] and
[[5 - Context Management & Reliability]].

### MCP (Model Context Protocol)

A protocol that lets an AI application connect
to outside capabilities through a server, instead of every app hand-rolling its
own integration. A server exposes three primitives — tools (model-controlled),
resources (application-controlled), and prompts (user-controlled) — and any
MCP-aware client, including Claude Code, can use them. See
[[2 - Tool Design & MCP Integration]].

### MCP structured error response

Returning a tool failure with `isError` set,
plus an `errorCategory` (transient, validation, business, or permission) and an
`isRetryable` boolean, so the agent has a basis for deciding whether to retry,
explain, or escalate. A uniform "Operation failed" strips away that basis. See
[[2 - Tool Design & MCP Integration]].

### Message Batches API

An asynchronous alternative to the standard
Messages API: instead of one request per document sent synchronously, you
submit a whole set of requests as a single job and Claude works through them
in the background, so you poll for or later retrieve the results rather than
getting an inline reply. It costs 50% less than the same requests sent
synchronously, and Claude processes the whole batch within an up to 24-hour
window — but there is no guaranteed latency SLA, so it suits non-blocking,
latency-tolerant workloads (overnight reports, weekly audits) and is the
wrong fit for a blocking workflow like a pre-merge check. It does not support
multi-turn tool calling within a single request. See
[[Glossary#custom_id|custom_id]] and
[[4 - Prompt Engineering & Structured Output#4.5 — Design efficient batch processing strategies|4 - Prompt Engineering & Structured Output]].

### `.mcp.json` and `~/.claude.json`

Two places to register MCP servers with
different reach. `.mcp.json` at the project root is committed and shared with the
whole team; `~/.claude.json` is user-scoped and personal, for experimental servers
nobody else needs. `.mcp.json` also supports environment-variable expansion (e.g.
`${GITHUB_TOKEN}`) so credentials are never committed. See
[[2 - Tool Design & MCP Integration]] and
[[Claude Main Files and Directories#.mcp.json and ~/.claude.json|Claude Main Files and Directories]].

## O

### Output style

A named set of instructions layered onto Claude Code's system prompt to
change how it responds — role, tone, and output format — set once and
persisted per project (or user, or managed-policy) rather than passed as a
one-off CLI flag. Selecting one, via `/config` or the `outputStyle` field, is
saved to `.claude/settings.local.json`, so every future session in that
project starts with it active until changed. A custom style is a Markdown
file — frontmatter plus instructions — saved under `~/.claude/output-styles`
(user), `.claude/output-styles` (project), or a managed-policy
`output-styles/` folder; its `keep-coding-instructions` frontmatter field
decides whether Claude Code's built-in software-engineering instructions
survive alongside it. Contrast with
[`--append-system-prompt`](<Claude Commands.md#--append-system-prompt>) and
[`--system-prompt`](<Claude Commands.md#--system-prompt>), which apply only
to a single invocation and are never saved. See
[[3 - Claude Code Configuration & Workflows#--system-prompt persistence, and how output styles differ|3 - Claude Code Configuration & Workflows]].
*Verified against the [output styles docs](https://code.claude.com/docs/en/output-styles) (checked 2026-09-07).*

## P

### Parallelisation

Fanning the same input out to several specialised
evaluations at once — each with its own prompt, tools, and criteria — then
aggregating the results, instead of one pass trying to juggle every criterion
together. Contrast with [[Glossary#Routing|routing]], which picks one path for
a request rather than running several at once. See
[[1 - Agentic Architecture & Orchestration#1.2 Orchestrate multi-agent systems with coordinator-subagent patterns|1 - Agentic Architecture & Orchestration]].

### permissionDecision

The field a `PreToolUse` hook returns to control a tool
call: `allow`, `deny`, or `ask` (hand the decision to the user). See
[[1 - Agentic Architecture & Orchestration]].

### Plugin

A versioned, installable bundle of Claude Code configuration —
skills, subagents, hooks, and MCP server configs together — installed by
name (`/plugin install org-name@plugin-name`) or through a shared
marketplace, rather than assembled by hand. Because a plugin runs with your
privileges and its hooks fire on every matching tool call, read what it does
before installing it. See [[3 - Claude Code Configuration & Workflows]].

### PostCompact

A hook that fires after context compaction completes. Its output is **not**
re-injected into the conversation — for restoring lost context after
compaction, use a [[Glossary#SessionStart|SessionStart]] hook with the
`compact` matcher instead. See [[1 - Agentic Architecture & Orchestration#1.5 Apply Agent SDK hooks for tool call interception and data normalization|1 - Agentic Architecture & Orchestration]].

### PostToolUse

A hook that fires after a tool runs; useful for normalising or
transforming a tool's result before the model sees it. It cannot stop the tool,
which already ran. See [[1 - Agentic Architecture & Orchestration]].

### PreCompact

A hook that fires before context compaction runs. See
[[Glossary#PostCompact|PostCompact]] for the matching after-event, and
[[1 - Agentic Architecture & Orchestration#1.5 Apply Agent SDK hooks for tool call interception and data normalization|1 - Agentic Architecture & Orchestration]].

### PreToolUse

A hook that fires before a tool runs and can allow, deny, or ask —
and can rewrite the tool's input (e.g. redact a value). The enforcement point for
deterministic policy. See [[1 - Agentic Architecture & Orchestration]].

### Prerequisite gate

Code — typically a `PreToolUse` hook — that blocks a tool
call until an earlier required step has actually completed and returned proof
(an id, a status, an approval token). Example: refuse `process_refund` unless a
prior `get_customer` call returned a verified customer id; refuse
`deploy_to_production` unless a prior `run_test_suite` call returned a pass.
Unlike a system-prompt instruction, which is only probabilistic, a gate is a
deterministic boolean check wired in front of the sensitive tool call. See
[[1 - Agentic Architecture & Orchestration#1.4 Implement multi-step workflows with enforcement and handoff patterns|Domain 1, §1.4]].

### Progressive summarization

Repeatedly condensing conversation history to save
tokens. The risk is losing exact figures, dates, and stated expectations, so pull
those into a persistent facts block kept outside the summary. See [[5 - Context Management & Reliability]].

### Prompt chaining

A fixed, sequential pipeline: predetermined steps that each
build on the previous one's output, with optional non-LLM processing between
them. Used when the steps are known in advance — e.g. reviewing each file in a
pull request individually, then running a separate cross-file pass — because
splitting the work avoids attention dilution from one giant multi-requirement
prompt. Contrast with dynamic (adaptive) decomposition, which discovers its
steps as it goes. See
[[1 - Agentic Architecture & Orchestration#1.6 Design task decomposition strategies for complex workflows|Domain 1, §1.6]].

### Prompt caching

Reusing the model's processing of a stable prefix (tools,
system prompt, long context) across requests to cut cost and latency. Order matters
(tools, then system, then messages) and small edits invalidate the cache. See
[[5 - Context Management & Reliability]].

### Provenance

Keeping track of which source each claim came from as findings pass
through summarisation and synthesis, so attribution and conflicts are preserved
rather than flattened. See [[5 - Context Management & Reliability]].

## R

### Reciprocal rank fusion (RRF)

A method for merging several ranked result lists
into one by summing `1/(k + rank)` across lists, used to combine lexical and
semantic search. See [[5 - Context Management & Reliability]].

### Resource template

An MCP resource addressed by a parameterized URI (for
example `docs://documents/{doc_id}`), so one definition answers a whole family
of queries and can support auto-completion. Contrast with a
[[Glossary#Direct resource|direct resource]], which is a fixed URI pointing at
one specific piece of data. See [[2 - Tool Design & MCP Integration]].

### Retrieval Augmented Generation (RAG)

A way to answer questions using a body of text too large to hand the model in
one go: instead of pasting the whole thing into the prompt, you split it into
pieces ahead of time, store those pieces so they can be searched, and then,
for each question, look up and hand the model only the few pieces likely to
be relevant. See [[5 - Context Management & Reliability]].

### Routing

Classifying an incoming request first, then sending it down one
specialised path instead of running every request through the same
one-size-fits-all pipeline. At the coordinator level this means selecting only
the subagents a query actually needs (a simple FAQ question does not need a
billing subagent invoked); at the prompt level it means categorising a request
and picking the matching handler prompt. Contrast with
[[Glossary#Parallelisation|parallelisation]], which runs several paths at once
instead of choosing one. See
[[1 - Agentic Architecture & Orchestration#1.2 Orchestrate multi-agent systems with coordinator-subagent patterns|1 - Agentic Architecture & Orchestration]].

### REVIEW.md

A root-level file that configures Claude's managed GitHub Code
Review specifically: what to flag, severity levels, exclusions, and reporting
preferences. `CLAUDE.md` supplies general project context to the same review;
`REVIEW.md` is the review-specific knob. See [[3 - Claude Code Configuration & Workflows]].

## S

### SessionStart

A hook that fires at session launch, and again later after `/clear` or a
compaction. A `SessionStart` hook with the `compact` matcher is the way to
re-inject context lost to compaction: unlike
[[Glossary#PostCompact|PostCompact]], plain text it prints on success is added
back into the conversation. See
[[1 - Agentic Architecture & Orchestration#1.5 Apply Agent SDK hooks for tool call interception and data normalization|1 - Agentic Architecture & Orchestration]].

### .claude/settings.local.json

A personal, project-scoped settings file that lives at the project root
alongside `.claude/settings.json`. It holds overrides for you alone in that
one project — a standing "yes, and don't ask again" permission approval, a
personal model override, your chosen [[Glossary#Output style|output style]],
or a few `/config` options such as Show tips. Claude Code often writes it for
you automatically (the first time you approve a permission prompt with
"don't ask again," or pick one of those `/config` settings) rather than you
creating it by hand.

In the settings precedence, project local sits above the shared
`.claude/settings.json` but below the command line's `--settings` flag and
any organization-managed settings, so it overrides a team default for you
without touching what your teammates load. Claude Code also keeps it out of
version control automatically: the first time it writes the file inside a
git repository, it adds `**/.claude/settings.local.json` to your global git
excludes, so it never shows up as a change to commit — you only need to
gitignore it yourself if you created the file by hand before Claude Code
touched it. This makes it the structured-settings counterpart to
[[Glossary#CLAUDE.local.md|CLAUDE.local.md]]: the same personal,
git-ignored-per-project idea, but for JSON settings rather than prose
context. See
[[3 - Claude Code Configuration & Workflows#--system-prompt persistence, and how output styles differ|3 - Claude Code Configuration & Workflows]].
*Verified against the [settings docs](https://code.claude.com/docs/en/settings) (checked 2026-09-07).*

### Skill

A reusable, task-specific capability that Claude invokes on its own when a
task matches the skill's description — unlike a custom slash command, which
you invoke by name. Skills live in `.claude/skills/` as folders, each with a
[[Glossary#SKILL.md|SKILL.md]] file. See
[[3 - Claude Code Configuration & Workflows]].

### SKILL.md

The file defining a [[Glossary#Skill|skill]] in `.claude/skills/`, with
[[Glossary#Frontmatter|frontmatter]] options including `context: fork` (run
the skill in an isolated subagent context
so its output doesn't clutter the main conversation), `allowed-tools`, and
`argument-hint`. See [[3 - Claude Code Configuration & Workflows]].

### Stop

A hook that fires when Claude wants to end its turn. It can refuse — telling
Claude it is not done yet — which is how you pair a permissive execution mode
with a guarantee that, say, the test suite actually passed before the turn
ends. [[Glossary#SubagentStop|SubagentStop]] is the matching event for a
finishing subagent. See
[[1 - Agentic Architecture & Orchestration#1.5 Apply Agent SDK hooks for tool call interception and data normalization|1 - Agentic Architecture & Orchestration]].

### stop_reason

The field on a Claude API response that drives the agentic
loop. `tool_use` means keep going; `end_turn` means stop. `max_tokens` means the
output was cut off, and `stop_sequence` means a stop string you supplied was hit
— the only other legitimate values. See [[1 - Agentic Architecture & Orchestration]].

### Scratchpad

A file the agent writes key findings to so they survive context
boundaries and long sessions, and can be re-read later. See [[5 - Context Management & Reliability]].

### Stratified random sampling

A sampling method that first splits a population into subgroups ("strata")
that share some characteristic — say, document type, region, or confidence
level — and then draws a separate random sample from each subgroup, rather
than one random sample from the population as a whole. This keeps a small or
unusual subgroup from being drowned out by a large, easy majority, so you can
track each subgroup's own error rate and catch problems that a single
overall average would hide. See [[5 - Context Management & Reliability]].

### Subagent

A separate agent invoked for a scoped task with its own isolated
context; it does not inherit the caller's conversation history, so context must be
passed explicitly. See [[1 - Agentic Architecture & Orchestration]].

### SubagentStop

The [[Glossary#Stop|Stop]] hook's counterpart for a finishing subagent instead
of the main conversation. See
[[1 - Agentic Architecture & Orchestration#1.5 Apply Agent SDK hooks for tool call interception and data normalization|1 - Agentic Architecture & Orchestration]].

## T

### Task tool

The mechanism a coordinator uses to spawn subagents; the coordinator
must have `Task` in its allowed tools. Emitting several `Task` calls in one response
runs subagents in parallel. See [[1 - Agentic Architecture & Orchestration]].

### Tool

A capability you make available to a model beyond generating text — a
function it can call to look something up, take an action, or affect the
outside world, such as running a search, reading a file, or placing an order.
The model decides for itself, based on the conversation, whether to call a
tool and with what input; you are the one who runs it and hands the result
back. See [[Glossary#Tool schema|Tool schema]] for how a tool is described to
the model, and [[2 - Tool Design & MCP Integration]] for how to design one
well.

### Tool schema

What you give the model to describe a tool: a name, a
description, and a [[Glossary#JSON Schema|JSON Schema]] for its inputs. The description is
the model's primary basis for choosing between tools, so it carries more weight
than the name. See [[2 - Tool Design & MCP Integration]].

### Temperature

A sampling setting: near 0 makes output deterministic (favours the
highest-probability token); higher values spread probability for more varied output.
See [[4 - Prompt Engineering & Structured Output]].

### tool_choice

The setting that controls tool calling: `auto` (model may answer in
text), `any` (must call some tool), or forced (`{"type":"tool","name":...}` — must
call that specific tool). See [[2 - Tool Design & MCP Integration]] and [[4 - Prompt Engineering & Structured Output]].

### tool_result block

What you send back after running a tool: a `user` message
containing a block with the tool's output, an `is_error` flag, and a `tool_use_id`
that matches the request it answers — matching the id matters because results can
arrive out of order when several tools were requested at once. See
[[1 - Agentic Architecture & Orchestration]].

## U

### updatedInput

The field a `PreToolUse` hook returns to rewrite a tool call
instead of blocking it outright — for example, stripping a secret out of a bash
command and letting the sanitised version run. It replaces the whole input object,
so echo back the fields you aren't changing. See
[[1 - Agentic Architecture & Orchestration]].

## V

### Vector database

A store that indexes embeddings and returns the nearest ones to
a query vector, enabling fast semantic retrieval. See [[5 - Context Management & Reliability]].

## W

### Worktree

A second working folder for the same project — a complete set of its files
checked out to a different branch, in a different directory — that you can
work in without touching your main one. Two Claude Code sessions can each
get their own so they work in separate directories instead of fighting over
the same files. 

A `.worktreeinclude` file at the repo root lists git-ignored files (like a
local env file) to copy into every new one. See
[[3 - Claude Code Configuration & Workflows#Custom commands in practice: parallel work with worktrees|3 - Claude Code Configuration & Workflows]].

## X

### XML tags

Using tags like `<document>` and `<instructions>` to structure a
prompt so the model can tell content apart cleanly. See [[4 - Prompt Engineering & Structured Output]].
