---
tags: [ccaf, directories, claude-code, configuration]
---

# Claude Main Files and Directories

A single map of every `.claude/` directory and every project-root companion
file mentioned across the domain notes: what lives there, who it's shared
with (project, user, or managed-policy), and whether git sees it. This page
is the directory map; [[Glossary]] is where the *concepts* those files carry
are defined (`CLAUDE.md`, [[Glossary#Hook|Hook]], [[Glossary#Skill|Skill]],
...), and [[Claude Commands]] is where the slash commands and CLI flags you
type live. Where a directory already has a full concept-level entry in the
Glossary, this page keeps its own entry short and links there instead of
repeating it.

```text
<project root>/
├── CLAUDE.md                 project-level memory file
├── CLAUDE.local.md           personal, git-ignored memory file
├── REVIEW.md                 managed Code Review configuration
├── .mcp.json                 shared MCP server registry
├── .worktreeinclude          git-ignored files to copy into every new worktree
└── .claude/
    ├── agents/               one Markdown file per subagent
    ├── commands/             custom slash commands
    ├── hooks/                (convention only) scripts your settings.json hooks call
    ├── output-styles/        custom output styles
    ├── rules/                path-scoped convention files
    ├── skills/               one folder per skill, each with a SKILL.md
    ├── settings.json         shared project settings, committed
    └── settings.local.json   personal overrides, auto-git-ignored

~/.claude/                    user-level counterpart: agents/, commands/,
                               skills/, output-styles/, settings.json, CLAUDE.md
~/.claude.json                user-level MCP server registry
```

Every directory here also has a **managed-policy** counterpart your
organization's platform team can deploy to a fixed OS-specific path (the
same one [[Glossary#CLAUDE.md|CLAUDE.md]] uses) — it applies to every
project on the machine and cannot be excluded. The project rows below focus
on the project/user split; see the Glossary's `CLAUDE.md` entry for the full
three-level (managed/user/project) pattern that repeats across most of them.

## Inside `.claude/`

### .claude/agents/

Project-scoped subagent definitions, one Markdown file per subagent —
[[Glossary#Frontmatter|YAML frontmatter]] (required: `name`, `description`;
optional: `tools`, `model`, and others) followed by the Markdown body that
becomes the subagent's system prompt. Check these into version control so
the whole team shares and improves them. Both this and its personal
counterpart, `~/.claude/agents/`, are scanned recursively, so you can group
definitions into subfolders. When a name collides across scopes, the
priority is managed-policy, then a `--agents` CLI flag, then
`.claude/agents/`, then `~/.claude/agents/`, then a plugin's own `agents/`
folder (which is namespaced, so it never actually collides). See
[[Glossary#AgentDefinition|AgentDefinition]],
[[Glossary#Subagent|Subagent]], and
[[1 - Agentic Architecture & Orchestration]].
*Verified against the [sub-agents docs](https://code.claude.com/docs/en/sub-agents) (checked 2026-09-07).*

### .claude/commands/

Project-scoped custom slash commands, checked into the repository and
shared with the whole team through version control. Each file's contents
become the prompt that runs when you invoke it by name, and `$ARGUMENTS` is
replaced everywhere it appears with whatever you pass on invocation. The
personal counterpart is `~/.claude/commands/`, which never reaches
teammates. See
[[3 - Claude Code Configuration & Workflows#3.2 — Custom slash commands and skills|3 - Claude Code Configuration & Workflows]].

### .claude/conventions/

Not a directory Claude Code treats specially — it is just the example path
the course material uses with the [[Glossary#CLAUDE.md|CLAUDE.md]]
`@import` syntax (`@.claude/conventions/testing.md`,
`@.claude/conventions/code-style.md`), to show how you might organize
shared convention files that several packages' `CLAUDE.md` files pull in.
Any directory name works with `@import`; unlike `.claude/rules/` or
`.claude/skills/`, Claude Code does not load `.claude/conventions/` on its
own. See
[[3 - Claude Code Configuration & Workflows#3.1 — CLAUDE.md hierarchy, scoping, and modular organization|3 - Claude Code Configuration & Workflows]].

### .claude/hooks/

Also not a directory Claude Code reads automatically. A
[[Glossary#Hook|hook]] is *defined* under the `hooks` key inside a settings
file — `.claude/settings.json`, `.claude/settings.local.json`,
`~/.claude/settings.json`, managed-policy settings, or a plugin's own
`hooks/hooks.json` — organized by event name, then an optional matcher, then
the handler to run. `.claude/hooks/` is only the conventional place to save
the *script files* those handler commands point at by path (for example
`${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh`); nothing scans that
folder on its own, and a hook script could just as easily live anywhere
else. Hooks from every settings level merge rather than replace one
another — a plugin's `PreToolUse` hook and your own both fire on the same
tool call. See [[1 - Agentic Architecture & Orchestration]].
*Verified against the [hooks docs](https://code.claude.com/docs/en/hooks) (checked 2026-09-07).*

### .claude/output-styles/

Holds custom [[Glossary#Output style|output styles]] as Markdown files —
frontmatter plus the instructions to add to the system prompt. The full
explanation of how a style is chosen, persisted, and scoped
(`~/.claude/output-styles` for personal styles, a managed-policy
`output-styles/` folder, a plugin's own `output-styles/` folder) lives in
the Glossary entry linked above; this row exists so the directory shows up
in the map.

### .claude/rules/

Holds topic-specific rule files as an alternative to one monolithic
[[Glossary#CLAUDE.md|CLAUDE.md]]. A rule file's YAML
[[Glossary#Frontmatter|frontmatter]] can carry a `paths` field — a glob
pattern — so the rule loads only when Claude edits a matching file, rather
than at every launch. This is the fix for a convention that applies to a
file *type* scattered across many directories (all test files, say), where
a per-directory `CLAUDE.md` would have to be duplicated everywhere. See
[[3 - Claude Code Configuration & Workflows#3.3 — Path-specific rules for conditional convention loading|3 - Claude Code Configuration & Workflows]].

### .claude/settings.json

The shared, project-level settings file: permissions, [[Glossary#Hook|hook]]
definitions, telemetry, plugin installs, and similar configuration for the
whole team. Commit it so everyone who clones the repository gets the same
behaviour. Its personal, git-ignored sibling is
[[Glossary#.claude/settings.local.json|`.claude/settings.local.json`]],
which overrides it for you alone in this one project; the user-level
counterpart, `~/.claude/settings.json`, applies the same idea across every
project on your machine instead of one. In the settings precedence,
managed-policy settings win first, then the command line's `--settings`
flag, then project local, then this shared project file, then the user
file. See [[1 - Agentic Architecture & Orchestration]] for hooks as an
enforcement mechanism and
[[3 - Claude Code Configuration & Workflows]] for permission modes.
*Verified against the [settings docs](https://code.claude.com/docs/en/settings) (checked 2026-09-07).*

### .claude/settings.local.json

The personal, git-ignored sibling of `.claude/settings.json` above — a
standing permission approval, a personal model override, your chosen
output style, and similar overrides for you alone in this one project. See
[[Glossary#.claude/settings.local.json|the full Glossary entry]] for how
Claude Code writes and auto-excludes this file, and where it sits in the
settings precedence.

### .claude/skills/

Project-scoped [[Glossary#Skill|skills]], each a folder with a
[[Glossary#SKILL.md|SKILL.md]] file. The personal counterpart is
`~/.claude/skills/`, used for a private variant of a shared skill so you
don't affect teammates. See
[[3 - Claude Code Configuration & Workflows#3.2 — Custom slash commands and skills|3 - Claude Code Configuration & Workflows]].

## Project-root companion files

These sit next to `.claude/`, not inside it, but are configured the same
project/user/managed-policy way. Each already has a full explanation in the
Glossary; the entries below exist only so the file shows up in this map.

### CLAUDE.md

The project's persistent memory file. See
[[Glossary#CLAUDE.md|the full Glossary entry]] for its four load locations
(managed-policy, user, project, directory) and how it differs from a hook.

### CLAUDE.local.md

The git-ignored, project-root sibling of `CLAUDE.md`, for private notes on
one specific repository. See [[Glossary#CLAUDE.local.md|the full Glossary entry]].

### .mcp.json and ~/.claude.json

The two places MCP servers get registered — `.mcp.json` at the project
root, committed and shared; `~/.claude.json`, user-scoped and personal. See
[[Glossary#.mcp.json and ~/.claude.json|the full Glossary entry]] and
[[2 - Tool Design & MCP Integration]].

### REVIEW.md

The root-level file that configures managed GitHub Code Review specifically
— what to flag, severity, exclusions. See
[[Glossary#REVIEW.md|the full Glossary entry]].

### .worktreeinclude

A repo-root file listing git-ignored files (like a local env file) to copy
into every new [[Glossary#Worktree|worktree]]. See
[[3 - Claude Code Configuration & Workflows#Custom commands in practice: parallel work with worktrees|3 - Claude Code Configuration & Workflows]].

## Packaging the whole shape as a plugin

A [[Glossary#Plugin|plugin]] bundles this same `.claude` shape into one
installable, versioned unit: one folder per skill under `skills/`, one
Markdown file per subagent under `agents/`, and `hooks/hooks.json` together
with `.mcp.json` at the plugin root. An optional manifest at
`.claude-plugin/plugin.json` holds the plugin's name (the only required
field — it namespaces the plugin's skills, agents, and commands so they
never clash with yours), version, description, and author. See
[[3 - Claude Code Configuration & Workflows#3.2 — Custom slash commands and skills|3 - Claude Code Configuration & Workflows]].
