#!/usr/bin/env python3
"""Check Markdown requirement specs for implementation-readiness gaps."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_REQUIRED_SECTIONS = ("Acceptance Criteria", "Test Scenarios", "Dependencies", "Owner", "Launch Constraints")
UNRESOLVED_RE = re.compile(r"\b(todo|tbd|unknown|not stated|to be decided|assumption|needs decision)\b", re.I)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def split_sections(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def check_spec(text: str, required_sections: list[str]) -> dict[str, object]:
    headings = [match.group(1).strip() for match in HEADING_RE.finditer(text)]
    normalized_headings = {normalize(heading) for heading in headings}
    missing_sections = [section for section in required_sections if normalize(section) not in normalized_headings]

    unresolved_items = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = UNRESOLVED_RE.search(line)
        if match:
            unresolved_items.append({"line": line_number, "marker": match.group(0), "text": line.strip()})

    readiness = "ready"
    if missing_sections or unresolved_items:
        readiness = "needs_review"
    if len(text.strip()) < 80:
        readiness = "blocked"

    return {
        "readiness": readiness,
        "headings_detected": headings,
        "missing_sections": missing_sections,
        "unresolved_assumptions": unresolved_items,
        "caveats": ["This helper checks Markdown readiness only and does not invent scope, owners, dates, metrics, or launch commitments."],
    }


def print_human(result: dict[str, object]) -> None:
    print("Requirements Spec Check")
    print("=======================")
    print(f"Readiness: {result['readiness']}")
    print("\nMissing sections:")
    for item in result["missing_sections"] or ["None detected"]:
        print(f"- {item}")
    print("\nUnresolved assumptions:")
    for item in result["unresolved_assumptions"] or [{"text": "None detected"}]:
        print(f"- {item['text']}")
    print("\nCaveats:")
    for caveat in result["caveats"]:
        print(f"- {caveat}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check a Markdown requirements spec for readiness gaps.")
    parser.add_argument("--input", required=True, help="Path to Markdown spec.")
    parser.add_argument("--required-sections", default=",".join(DEFAULT_REQUIRED_SECTIONS), help="Comma-separated required sections.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = Path(args.input).read_text(encoding="utf-8")
    result = check_spec(text, split_sections(args.required_sections))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
