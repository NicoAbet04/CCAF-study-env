---
tags: [ccaf, commands]
---

# Claude Commands

Quick reference for the literal commands and CLI flags used across the domain
notes — the things you actually type, as opposed to [[Glossary]], which
covers concepts and terms of art. Each entry says what the command does and
links back to the domain note that teaches it in context. For every
`.claude/` directory and project-root config file (`.claude/commands/`,
`.claude/rules/`, `CLAUDE.md`, `SKILL.md`, `.mcp.json`, ...), see
[[Claude Main Files and Directories]] instead — this file stays focused on
commands and flags.

Mentions of these commands elsewhere link here with a Markdown link wrapped
around inline code (e.g. `` [`/compact`](<Claude Commands.md#/compact>) ``)
rather than a wikilink alias, so the command keeps its code styling instead
of showing raw backtick characters.

## Slash commands

### /clear

Resets the conversation history, discarding everything so far. Reach for it
between unrelated tasks in the same session, rather than letting old context
linger. See [[3 - Claude Code Configuration & Workflows]].

### /code-review

Reviews a diff locally, from your own terminal, rather than through the
hosted GitHub Code Review service. Its `--fix` flag applies the findings to
your working tree — which is how you act on a finding the hosted service
surfaced, after pulling the change down. See
[[3 - Claude Code Configuration & Workflows]].

### /compact

Summarizes the conversation and uses that summary as the new context,
freeing up room in a long session. Always steer it with an instruction naming
what to keep — for example `/compact focus on the refund-flow classes` —
because an unsteered `/compact` can drop the one specific detail you needed.
See [[1 - Agentic Architecture & Orchestration]],
[[3 - Claude Code Configuration & Workflows]], and
[[5 - Context Management & Reliability]].

### /config

Opens the Settings interface to adjust theme, model,
[[Glossary#Output style|output style]], and other preferences — for output
style specifically, the interactive equivalent of setting the `outputStyle`
field in a settings file by hand. Claude Code saves an output-style choice to
[[Glossary#.claude/settings.local.json|`.claude/settings.local.json`]] at the
project level, so every future session in that project starts with it
already active. See [[3 - Claude Code Configuration & Workflows]].
*Verified against the [commands reference](https://code.claude.com/docs/en/commands) (checked 2026-09-12).*

### /create_worktree

A custom command shipped with the course, not a Claude Code built-in. It
takes a feature name as `$ARGUMENTS`, checks that the
[[Glossary#Worktree|worktree]] doesn't already exist, creates it under
`.trees/`, and wires up the environment — paired with `/merge_worktree` for
parallelizing work across sessions. See
[[3 - Claude Code Configuration & Workflows]].

### /init

Bootstraps a project's `CLAUDE.md` by scanning the codebase and writing a
summary of its structure, dependencies, and conventions. See
[[Glossary#CLAUDE.md|CLAUDE.md]] and
[[3 - Claude Code Configuration & Workflows]].

### /install-github-app

Installs the Claude GitHub App on a repository (github.com only), with an
optional additional step to wire up the `anthropics/claude-code-action@v1`
GitHub Action workflow and secrets — the path to unattended runs (implementing
a change from a comment, running scheduled reports) tuned through
`claude_args` (for example `--max-turns`). This is the step beyond the
managed, hosted Code Review service, which the same GitHub App also powers.
See [[3 - Claude Code Configuration & Workflows]].
*Verified against the [commands reference](https://code.claude.com/docs/en/commands) (checked 2026-09-12).*

### /memory

Opens [[Glossary#CLAUDE.md|CLAUDE.md]] files for editing, toggles auto memory
on or off, and shows the auto memory entries currently stored — not just a
read-only listing. This is the tool to reach for when Claude's behaviour is
inconsistent across sessions and you suspect a `CLAUDE.md` file is or isn't
being picked up. See [[3 - Claude Code Configuration & Workflows]].
*Verified against the [commands reference](https://code.claude.com/docs/en/commands) (checked 2026-09-12).*

### /merge_worktree

The companion custom command to `/create_worktree`: merges that worktree's
branch back into main and walks through resolving any conflicts. Also not a
Claude Code built-in. See [[3 - Claude Code Configuration & Workflows]].

### /plugin

Installs a [[Glossary#Plugin|plugin]] by name (`/plugin install
org-name@plugin-name`) or through a shared marketplace, rather than
assembling skills, subagents, hooks, and MCP configs by hand. See
[[3 - Claude Code Configuration & Workflows]].

### /review

The illustrative name this vault uses for a team's shared, custom
code-review command — see
[[3 - Claude Code Configuration & Workflows#3.2 — Custom slash commands and skills|Domain 3 §3.2]]
for the project-vs-user scope decision it teaches. In current Claude Code,
`/review` also happens to be a real built-in alias for
[`/code-review`](<Claude Commands.md#/code-review>) — a fact about the
product, separate from that scope lesson.
*Verified against the [commands reference](https://code.claude.com/docs/en/commands) (checked 2026-09-06).*

### /rewind

Rewinds the session to an earlier checkpoint, undoing conversation and/or
code changes made since then. Reach for it when a session has gone off
course but you want to jump back to a specific prior point rather than
discarding all history the way [`/clear`](<Claude Commands.md#/clear>) does.
See [[3 - Claude Code Configuration & Workflows]].

## CLI flags

### --agents

Defines custom subagents inline as JSON for a single run, rather than
loading them from files. When a subagent name collides across sources, this
flag ranks just below managed-policy settings — above the project's own
[[Claude Main Files and Directories#.claude/agents/|`.claude/agents/`]], the
personal `~/.claude/agents/`, and a plugin's own `agents/` folder. See
[[1 - Agentic Architecture & Orchestration]].
*Verified against the [CLI reference](https://code.claude.com/docs/en/cli-reference) (checked 2026-09-12).*

### --append-system-prompt

Appends text to the end of Claude Code's default system prompt, keeping the
default behaviour intact. The right choice for temporary, stage-specific
instructions in a multi-step CI workflow — contrast with
[`--system-prompt`](<Claude Commands.md#--system-prompt>), which replaces the
default outright, and [[Glossary#CLAUDE.md|CLAUDE.md]], which is persistent
shared context rather than a one-off flag. There is also
`--append-system-prompt-file` to read the text from a file. See
[[3 - Claude Code Configuration & Workflows]].
*Verified against the [CLI reference](https://code.claude.com/docs/en/cli-reference) (checked 2026-09-05).*

### --bare

Puts Claude Code in a minimal mode that skips hooks, skills, custom commands,
subagents, plugins, MCP servers, auto memory, and
[[Glossary#CLAUDE.md|CLAUDE.md]] entirely — not just deterministic output,
but no local auto-discovery at all. CI scripts commonly combine it with
[`-p`](<Claude Commands.md#-p>) as `-p --bare` for a fast,
environment-independent run; because `CLAUDE.md` is skipped too, any project
context the run needs must be supplied manually — piped into the prompt, or
loaded with `--append-system-prompt-file`. See
[[3 - Claude Code Configuration & Workflows]].
*Verified against the [CLI reference](https://code.claude.com/docs/en/cli-reference) (checked 2026-09-12).*

### --fix

Flag on [`/code-review`](<Claude Commands.md#/code-review>) that applies its
findings to your working tree, rather than just reporting them. See
[[3 - Claude Code Configuration & Workflows]].

### --json-schema

Paired with [`--output-format json`](<Claude Commands.md#--output-format>) to
constrain Claude's output to a schema; the matching object lands in the
response's `structured_output` field, ready to pull out with `jq`. See
[[3 - Claude Code Configuration & Workflows]].

### --max-turns

A [`-p`](<Claude Commands.md#-p>)-only flag that caps how many agentic turns a
run may take, erroring out once the limit is reached instead of looping
forever. In CI it is typically passed through the GitHub Action's
`claude_args`, bounding an unattended run that has no human watching it. See
[[3 - Claude Code Configuration & Workflows]].
*Verified against the [CLI reference](https://code.claude.com/docs/en/cli-reference) (checked 2026-09-12).*

### --no-session-persistence

Runs the session without ever writing it to disk, so there is nothing later
to pick up with [`--resume`](<Claude Commands.md#--resume>). Reach for it in
a scripted [`-p`](<Claude Commands.md#-p>) call that never needs to be
resumed. See [[3 - Claude Code Configuration & Workflows]].

### --output-format

Set to `json` and paired with
[`--json-schema`](<Claude Commands.md#--json-schema>) for machine-readable,
schema-constrained results from a [`-p`](<Claude Commands.md#-p>) run — the
foundation of posting inline PR comments or feeding another script. See
[[3 - Claude Code Configuration & Workflows]].

### -p

Short for `--print`. Runs Claude Code as a one-shot, non-interactive command:
it reads standard in and writes standard out, so it pipes like any other
shell tool, and is the core mechanism for running Claude Code inside a CI
pipeline where no human can answer a prompt. On its own it still loads
[[Glossary#CLAUDE.md|CLAUDE.md]], hooks, skills, plugins, and MCP servers
exactly like an interactive session — it only changes the interaction mode,
not what gets auto-discovered. Pair it with
[`--bare`](<Claude Commands.md#--bare>) to skip that discovery too. See
[[3 - Claude Code Configuration & Workflows]].
*Verified against the [CLI reference](https://code.claude.com/docs/en/cli-reference) (checked 2026-09-12).*

### --resume

Continues a specific prior conversation by session name or id
(`--resume <session-name>`), picking up with full existing context. Contrast
with [[Glossary#fork_session|fork_session]], which branches off into a new,
independent session instead of continuing the same one. See
[[1 - Agentic Architecture & Orchestration]] and
[[3 - Claude Code Configuration & Workflows]].

### --settings

Points at a settings file for a single invocation. In the settings
precedence it ranks second — after managed-policy settings, before the
project's local, shared, and user-level settings files. See
[[Claude Main Files and Directories#.claude/settings.json|`.claude/settings.json`]].

### --system-prompt

Replaces Claude Code's default system prompt entirely. Use it only when you
genuinely need to override the default behaviour outright — for anything
temporary or additive, use
[`--append-system-prompt`](<Claude Commands.md#--append-system-prompt>)
instead. See [[3 - Claude Code Configuration & Workflows]].
*Verified against the [CLI reference](https://code.claude.com/docs/en/cli-reference) (checked 2026-09-05).*

## Config directories

Not commands you run — see [[Claude Main Files and Directories]] for every
`.claude/` directory (`.claude/commands/`, `.claude/rules/`,
`.claude/skills/`, `.claude/agents/`, `.claude/hooks/`,
`.claude/settings.json`, ...) and its project-root companion files
(`CLAUDE.md`, `.mcp.json`, `REVIEW.md`, ...) in one place, since "where do I
put this" is exactly the judgment the exam tests.
