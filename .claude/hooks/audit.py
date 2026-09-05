#!/usr/bin/env python3
"""Deterministic completion audit for a course build (proposal §4.1).

Single source of truth for "is the build done?". Called by the Stop hook
(.claude/hooks/stop-gate.sh) and by /course-audit. Reads ONLY JSON state under
.claude/state/<course>/ plus the vault files — never parses course.yaml, so it
needs no YAML library. /course-build Phase 0 resolves the manifest into
run.json (vault, domains, max_cycles) and inventory.json.

Side effects: merges domain-*-log.json statuses into inventory.json and
regenerates SOURCE_INVENTORY.md and COVERAGE_GAPS.md in the vault.

Usage:  python3 .claude/hooks/audit.py <course>
Prints a JSON report to stdout; exit 0 always (the caller decides what to do
with `complete`). Missing state is reported as failures, never a crash.
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def state_dir(course):
    return os.path.join(ROOT, ".claude", "state", course)


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def dump_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def resolve_vault(run):
    vault = run.get("vault", "")
    vault = os.path.expanduser(vault)
    if not os.path.isabs(vault):
        vault = os.path.join(ROOT, vault)
    return vault


def find_domain_note(vault, domain):
    """Domain note is '<N> - <Domain Name>.md'; match tolerantly on the id."""
    pattern = os.path.join(vault, f"{domain['id']} - *.md")
    matches = sorted(glob.glob(pattern))
    return matches[0] if matches else None


def count_flashcards(note_path):
    """Cards use the Spaced-Repetition multi-line format; the lone '?' line is
    the question/answer separator, so counting those counts cards.

    Fenced code blocks (``` or ~~~) are skipped first: a bare '?' inside a code
    sample or mermaid diagram is not a flashcard, and counting it would make the
    gate leniently pass a note that is short on cards. A separator also needs a
    non-blank line before and after it — a real card has a question and an
    answer around the '?'.
    """
    try:
        with open(note_path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return 0

    fence = None  # the fence string that opened the current block, if any
    count = 0
    for i, raw in enumerate(lines):
        stripped = raw.strip()
        if fence is None:
            m = re.match(r"^(`{3,}|~{3,})", stripped)
            if m:
                fence = m.group(1)[0]
                continue
        else:
            if re.match(r"^(`{3,}|~{3,})$", stripped) and stripped[0] == fence:
                fence = None
            continue

        if stripped != "?":
            continue
        prev_line = lines[i - 1].strip() if i > 0 else ""
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if prev_line and next_line:
            count += 1
    return count


def merge_logs_into_inventory(course):
    """Fold every domain-*-log.json into inventory.json statuses (§4.3).

    A source becomes 'covered' if any domain used/partial it, 'logged-irrelevant'
    if only marked irrelevant, else stays 'pending'. Returns (inventory,
    failed_entries) where failed_entries are logs with status 'failed'.
    """
    sd = state_dir(course)
    inventory = load_json(os.path.join(sd, "inventory.json"), default=None)
    failed = []
    if inventory is None:
        return None, failed

    # index inventory by normalized path
    by_path = {os.path.expanduser(e["path"]): e for e in inventory}
    for e in inventory:
        e.setdefault("claimed_by", [])

    for log_path in sorted(glob.glob(os.path.join(sd, "domain-*-log.json"))):
        m = re.search(r"domain-(\d+)-log\.json$", log_path)
        if not m:
            continue
        did = int(m.group(1))
        for entry in load_json(log_path, default=[]) or []:
            p = os.path.expanduser(entry.get("path", ""))
            status = entry.get("status", "")
            if status == "failed":
                failed.append({"domain": did, **entry})
            inv = by_path.get(p)
            if inv is None:
                continue
            if did not in inv["claimed_by"]:
                inv["claimed_by"].append(did)
            if status in ("used", "partial"):
                inv["status"] = "covered"
            elif status == "irrelevant" and inv["status"] == "pending":
                inv["status"] = "logged-irrelevant"

    dump_json(os.path.join(sd, "inventory.json"), inventory)
    return inventory, failed


def regenerate_views(vault, inventory, gaps):
    """Write the human-readable SOURCE_INVENTORY.md and COVERAGE_GAPS.md."""
    if not os.path.isdir(vault):
        return
    ts = datetime.now(timezone.utc).isoformat()

    lines = [f"# Source Inventory (generated {ts})", "",
             "_Authoritative data: `.claude/state/<course>/inventory.json`._", ""]
    for e in inventory or []:
        claimed = ", ".join(str(c) for c in e.get("claimed_by", [])) or "—"
        lines.append(f"- `{e['path']}` — **{e['status']}** (domains: {claimed})")
    with open(os.path.join(vault, "SOURCE_INVENTORY.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    glines = [f"# Coverage Gaps (generated {ts})", "",
              f"**Gap count: {len(gaps)}**", ""]
    glines += ([f"- {g}" for g in gaps] if gaps else ["_No gaps._"])
    with open(os.path.join(vault, "COVERAGE_GAPS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(glines) + "\n")


def audit(course):
    sd = state_dir(course)
    failures = []

    run = load_json(os.path.join(sd, "run.json"), default=None)
    if run is None:
        return {"course": course, "complete": False, "cycle": 0, "max_cycles": 0,
                "failures": [f"no run.json for '{course}' — run Phase 0 of /course-build"],
                "summary": "build not initialized"}

    vault = resolve_vault(run)
    domains = run.get("domains", [])

    inventory, failed_logs = merge_logs_into_inventory(course)

    # Criterion 1: every inventory entry covered or logged-irrelevant.
    if inventory is None:
        failures.append("inventory.json missing")
        inventory = []
    else:
        unclaimed = [e["path"] for e in inventory
                     if e["status"] not in ("covered", "logged-irrelevant")]
        if unclaimed:
            failures.append(f"{len(unclaimed)} source(s) unclaimed: "
                            + ", ".join(unclaimed[:5]) + ("…" if len(unclaimed) > 5 else ""))

    # Criteria 3 & 4: per-domain approval freshness + flashcard minimums.
    for d in domains:
        note = find_domain_note(vault, d)
        if note is None:
            failures.append(f"domain {d['id']} note missing")
            continue
        note_mtime = os.path.getmtime(note)

        n_cards = count_flashcards(note)
        fmin = d.get("flashcards_min", 0)
        if n_cards < fmin:
            failures.append(f"domain {d['id']} has {n_cards}/{fmin} flashcards")

        verdict = load_json(os.path.join(sd, f"eval-domain-{d['id']}.json"), default=None)
        if verdict is None:
            failures.append(f"domain {d['id']} has no evaluator verdict")
        elif verdict.get("verdict") != "approve":
            failures.append(f"domain {d['id']} verdict is '{verdict.get('verdict')}'")
        else:
            vts = verdict.get("timestamp")
            try:
                vt = datetime.fromisoformat(vts.replace("Z", "+00:00")).timestamp()
                if vt < note_mtime:
                    failures.append(f"domain {d['id']} verdict is stale "
                                    "(note edited after approval)")
            except (AttributeError, ValueError):
                failures.append(f"domain {d['id']} verdict has no valid timestamp")

    # Criterion 5: vault-wide files exist; every domain note linked from the MOC.
    for req in ("Glossary.md", "Weak Areas.md"):
        if not os.path.isfile(os.path.join(vault, req)):
            failures.append(f"missing {req}")
    moc_matches = glob.glob(os.path.join(vault, "* MOC.md"))
    if not moc_matches:
        failures.append("missing '<Course> MOC.md'")
    else:
        try:
            with open(moc_matches[0], encoding="utf-8") as f:
                moc_text = f.read()
        except OSError:
            moc_text = ""
        for d in domains:
            note = find_domain_note(vault, d)
            if note:
                stem = os.path.splitext(os.path.basename(note))[0]
                if stem not in moc_text:
                    failures.append(f"domain {d['id']} not linked from MOC")

    # Criterion 6: failed logs must each be surfaced in FLAGGED.md.
    if failed_logs:
        flagged_path = os.path.join(vault, "FLAGGED.md")
        flagged_text = ""
        if os.path.isfile(flagged_path):
            with open(flagged_path, encoding="utf-8") as f:
                flagged_text = f.read()
        for fl in failed_logs:
            if os.path.basename(fl.get("path", "")) not in flagged_text:
                failures.append(f"failed source not in FLAGGED.md: {fl.get('path')}")

    # Criterion 2: gaps == unmet criteria; regenerate the views from them.
    regenerate_views(vault, inventory, failures)

    run["last_audit"] = datetime.now(timezone.utc).isoformat()
    dump_json(os.path.join(sd, "run.json"), run)

    return {
        "course": course,
        "complete": len(failures) == 0,
        "cycle": run.get("cycle", 0),
        "max_cycles": run.get("max_cycles", 0),
        "failures": failures,
        "summary": ("build complete" if not failures
                    else f"{len(failures)} unmet criteria"),
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: audit.py <course>"}))
        return
    print(json.dumps(audit(sys.argv[1]), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
