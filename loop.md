# loop body — picked up by the bundled /loop skill when invoked bare

This is the unattended drive-to-completion body for a course build. The bundled
`/loop` skill runs it repeatedly, self-pacing, while the session stays open. Do
not write custom loop machinery — this file is the whole implementation.

On each iteration:

1. Find the active course: the `.claude/state/*/run.json` with
   `goal_active: true`. If none is active, there is nothing to drive — say so
   and yield (the loop can stop).

2. Run the deterministic audit for that course:

   ```
   python3 .claude/hooks/audit.py <course>
   ```

3. From the audit's `failures` list, do the **single highest-value action** it
   implies, then yield (let the loop pace the next iteration):
   - a domain with no builder log or an unclaimed source → dispatch the missing
     `domain-builder`;
   - a domain with a `reject` verdict (or a note edited after its approval) →
     repair-dispatch that `domain-builder` with the fix list, then re-evaluate;
   - a source logged `failed` with no `FLAGGED.md` entry → process that one file
     (or flag it if genuinely unprocessable);
   - missing `Glossary.md` / MOC / `Weak Areas.md`, or a note missing from the
     MOC → produce/repair just that.

4. If the audit reports `complete: true`, or `cycle` has reached `max_cycles`,
   stop: the Stop gate has been satisfied or has disarmed and escalated.

Do exactly one action per iteration — the point is steady, resumable progress,
not a burst. The Stop hook, not this loop, is the real completeness gate.
