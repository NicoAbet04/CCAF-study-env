---
tags: [ccaf, weak-areas]
---

# Weak Areas

Your running record of what you got wrong or confused. **`/study ccaf` appends
here automatically** after every drill, quiz, generated round, or mock debrief —
one line per miss:

`- [date] [[note#section]] — what was confused with what`

Later `/study` sessions read this file and weight questions toward your recurring
misses, so the log steers your practice. Nothing is written here from the notes
themselves — only from your own answers, keeping the signal honest.

> [!tip] How to read it
> Cluster your misses by domain and by task. A topic that shows up three times is
> your next study target, not the domain you already feel shaky about.

---

## Miss log

- [2026-09-08] [[2 - Tool Design & MCP Integration#Task 2.5 — Select and apply Claude Code's built-in tools]] — on `Edit` "match not unique" errors, chose full `Write`-overwrite fallback instead of widening `old_string` context and retrying `Edit` first.
- [2026-09-08] [[2 - Tool Design & MCP Integration#Task 2.1 — Design tool interfaces with clear descriptions and boundaries]] — on free-text input format errors (date parsing), chose schema validation as the fix instead of adding format constraints/examples to the tool description itself.
- [2026-09-08] [[2 - Tool Design & MCP Integration#Task 2.5 — Select and apply Claude Code's built-in tools]] — for codebase-wide content search, chose `Bash find`+`grep` instead of the built-in `Grep` tool.
