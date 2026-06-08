#!/usr/bin/env python3
"""Check incident timelines for deterministic postmortem readiness signals."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


TIMESTAMP_RE = re.compile(r"(?P<ts>\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?\b|\b\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\b)")
OWNER_RE = re.compile(r"\b(owner|owned by|assignee|responder|commander|lead|@[\w.-]+)\b", re.I)
ACTION_RE = re.compile(r"\b(action|mitigat\w*|rollback|restart|deploy|disable|page|notify|investigat\w*|fix|resolve|verify)\b", re.I)
UNRESOLVED_RE = re.compile(r"\b(todo|tbd|unknown|not stated|to be determined|follow up needed)\b", re.I)


def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def check_timeline(lines: list[str]) -> dict[str, object]:
    timestamp_counts: Counter[str] = Counter()
    timestamped_events: list[dict[str, object]] = []
    missing_owner: list[dict[str, object]] = []
    missing_action: list[dict[str, object]] = []
    unresolved_items: list[dict[str, object]] = []

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        timestamp_match = TIMESTAMP_RE.search(stripped)
        unresolved_match = UNRESOLVED_RE.search(stripped)
        if unresolved_match:
            unresolved_items.append({"line": line_number, "marker": unresolved_match.group(0), "text": stripped})
        if not timestamp_match:
            continue
        timestamp = timestamp_match.group("ts")
        timestamp_counts[timestamp] += 1
        has_owner = bool(OWNER_RE.search(stripped))
        has_action = bool(ACTION_RE.search(stripped))
        event = {"line": line_number, "timestamp": timestamp, "has_owner": has_owner, "has_action": has_action, "text": stripped}
        timestamped_events.append(event)
        if not has_owner:
            missing_owner.append(event)
        if not has_action:
            missing_action.append(event)

    repeated_timestamps = [{"timestamp": ts, "count": count} for ts, count in timestamp_counts.items() if count > 1]
    readiness = "ready"
    if missing_owner or missing_action or unresolved_items:
        readiness = "needs_review"
    if not timestamped_events:
        readiness = "blocked"

    caveats = ["This helper checks timeline hygiene only and does not determine root cause, severity, or customer impact."]
    if not timestamped_events:
        caveats.append("No timestamped events were detected.")

    return {
        "event_count": len(timestamped_events),
        "readiness": readiness,
        "repeated_timestamps": repeated_timestamps,
        "missing_owner_events": missing_owner,
        "missing_action_events": missing_action,
        "unresolved_items": unresolved_items,
        "caveats": caveats,
    }


def print_human(result: dict[str, object]) -> None:
    print("Incident Timeline Check")
    print("=======================")
    print(f"Events reviewed: {result['event_count']}")
    print(f"Readiness: {result['readiness']}")
    for title, key in (
        ("Repeated timestamps", "repeated_timestamps"),
        ("Missing owner events", "missing_owner_events"),
        ("Missing action events", "missing_action_events"),
        ("Unresolved items", "unresolved_items"),
    ):
        print(f"\n{title}:")
        values = result[key]
        if not values:
            print("- None detected")
            continue
        for item in values:
            print(f"- {item}")
    print("\nCaveats:")
    for caveat in result["caveats"]:
        print(f"- {caveat}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check incident timeline notes for postmortem readiness signals.")
    parser.add_argument("--input", required=True, help="Path to incident timeline or notes.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = check_timeline(load_lines(Path(args.input)))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
