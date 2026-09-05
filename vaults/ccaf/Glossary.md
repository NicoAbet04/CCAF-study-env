---
tags: [ccaf, glossary]
---

# Glossary

Short, plain definitions for the terms of art used across the CCAF domain notes.
Each entry says what the term means and, where useful, which domain note develops
it. Definitions are kept faithful to how the course sources and the official exam
guide use each term.

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

### `--append-system-prompt` vs `--system-prompt`

Two CLI flags that look
interchangeable and are not. `--append-system-prompt` adds text to the end of
Claude Code's default system prompt, keeping default behaviour — the right choice
for temporary, stage-specific CI instructions. `--system-prompt` replaces the
default prompt entirely; use it only to override default behaviour outright.
`CLAUDE.md` is the third option, for persistent context shared across CI runs and
ordinary sessions. See [[3 - Claude Code Configuration & Workflows]].

## B

### BM25

A lexical (keyword) ranking function that scores documents by exact term
matches. Strong on rare identifiers and codes; combined with embeddings in a hybrid
search. See [[5 - Context Management & Reliability]].

## C

### CLAUDE.md

A Markdown file that gives Claude Code persistent project or user
context. It loads in a hierarchy (user, project, directory) and, unlike command-line
system-prompt flags, persists across sessions and CI runs. See [[3 - Claude Code Configuration & Workflows]].

### Content block

One piece of an API message: a text block (Claude's visible
reasoning or reply), a `tool_use` block (naming a tool and its input), or a
`tool_result` block (a tool's output sent back). A single message can carry
several blocks — for example, text followed by two `tool_use` blocks. See
[[2 - Tool Design & MCP Integration]].

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

## E

### Embedding

A list of numbers representing the meaning of a piece of text, so
that semantically similar texts sit close together in vector space. The individual
dimensions are not human-interpretable. See [[5 - Context Management & Reliability]].

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

## H

### Hook

A configured script that fires on a lifecycle event (e.g. `PreToolUse`,
`PostToolUse`, `Stop`) to intercept, transform, or block behaviour. Hooks give
deterministic guarantees where prompt instructions give only probabilistic
compliance. See [[1 - Agentic Architecture & Orchestration]] and [[3 - Claude Code Configuration & Workflows]].

## J

### JSON Schema

A formal description of the shape of a JSON object (fields, types,
which are required). Used with tool definitions to force schema-compliant output and
eliminate JSON syntax errors. See [[4 - Prompt Engineering & Structured Output]].

## L

### Lost in the middle

The tendency of models to reliably use information at the
start and end of a long input while under-using material buried in the middle.
Mitigated by putting key findings first and using clear section headers. See
[[5 - Context Management & Reliability]].

## M

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

### `.mcp.json` and `~/.claude.json`

Two places to register MCP servers with
different reach. `.mcp.json` at the project root is committed and shared with the
whole team; `~/.claude.json` is user-scoped and personal, for experimental servers
nobody else needs. `.mcp.json` also supports environment-variable expansion (e.g.
`${GITHUB_TOKEN}`) so credentials are never committed. See
[[2 - Tool Design & MCP Integration]].

## P

### Parallelisation

Fanning the same input out to several specialised
evaluations at once — each with its own prompt, tools, and criteria — then
aggregating the results, instead of one pass trying to juggle every criterion
together. Contrast with [[Glossary#Routing|routing]], which picks one path for
a request rather than running several at once. See
[[1 - Agentic Architecture & Orchestration#1.2 Orchestrate multi-agent systems with coordinator-subagent patterns|1 - Agentic Architecture & Orchestration]].

### Path-specific rules (`.claude/rules/`)

Rule files with a YAML `paths:` glob
in their frontmatter, so a convention loads only when you're editing a matching
file (e.g. all `**/*.test.tsx` files) instead of always, or instead of needing a
directory-level `CLAUDE.md` for conventions that span many directories. See
[[3 - Claude Code Configuration & Workflows]].

### permissionDecision

The field a `PreToolUse` hook returns to control a tool
call: `allow`, `deny`, or `ask` (hand the decision to the user). See
[[1 - Agentic Architecture & Orchestration]].

### PostToolUse

A hook that fires after a tool runs; useful for normalising or
transforming a tool's result before the model sees it. It cannot stop the tool,
which already ran. See [[1 - Agentic Architecture & Orchestration]].

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

### Retrieval Augmented Generation (RAG)

Answering with the help of retrieved
source passages: chunk the corpus, embed and index it, retrieve the most relevant
chunks for a query, and give them to the model as context. See [[5 - Context Management & Reliability]].

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

### SKILL.md

The file defining a skill in `.claude/skills/`, with frontmatter
options including `context: fork` (run the skill in an isolated subagent context
so its output doesn't clutter the main conversation), `allowed-tools`, and
`argument-hint`. See [[3 - Claude Code Configuration & Workflows]].

### stop_reason

The field on a Claude API response that drives the agentic
loop. `tool_use` means keep going; `end_turn` means stop. `max_tokens` means the
output was cut off, and `stop_sequence` means a stop string you supplied was hit
— the only other legitimate values. See [[1 - Agentic Architecture & Orchestration]].

### Scratchpad

A file the agent writes key findings to so they survive context
boundaries and long sessions, and can be re-read later. See [[5 - Context Management & Reliability]].

### Stratified random sampling

Sampling within segments (e.g. by document type)
to measure error rates and catch novel failures that an aggregate accuracy number
would hide. See [[5 - Context Management & Reliability]].

### Subagent

A separate agent invoked for a scoped task with its own isolated
context; it does not inherit the caller's conversation history, so context must be
passed explicitly. See [[1 - Agentic Architecture & Orchestration]].

## T

### Task tool

The mechanism a coordinator uses to spawn subagents; the coordinator
must have `Task` in its allowed tools. Emitting several `Task` calls in one response
runs subagents in parallel. See [[1 - Agentic Architecture & Orchestration]].

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

## X

### XML tags

Using tags like `<document>` and `<instructions>` to structure a
prompt so the model can tell content apart cleanly. See [[4 - Prompt Engineering & Structured Output]].
