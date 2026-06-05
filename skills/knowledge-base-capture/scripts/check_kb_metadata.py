#!/usr/bin/env python3
"""Check knowledge-base draft metadata and publishing readiness."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path


SECTION_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^\s*([A-Za-z][A-Za-z _-]{1,40})\s*:\s*(.+?)\s*$")
UNRESOLVED_RE = re.compile(r"(?i)\b(tbd|tk|to be determined|needs review|open question|assumption)\b")


def parse_date(value: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    return None


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def extract_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                match = FIELD_RE.match(line)
                if match:
                    metadata[normalize(match.group(1))] = match.group(2).strip()

    for line in text.splitlines()[:40]:
        match = FIELD_RE.match(line)
        if match:
            metadata[normalize(match.group(1))] = match.group(2).strip()
    return metadata


def extract_sections(text: str) -> set[str]:
    sections = {normalize(match.group(2)) for match in SECTION_RE.finditer(text)}
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if title_match:
        sections.add("title")
    return sections


def find_unresolved(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if UNRESOLVED_RE.search(line):
            findings.append({"line": line_number, "text": line.strip()})
    return findings


def check(text: str, required_sections: list[str], today: date) -> dict[str, object]:
    metadata = extract_metadata(text)
    sections = extract_sections(text)
    required_normalized = [normalize(section) for section in required_sections]

    missing_sections = [section for section, normalized in zip(required_sections, required_normalized) if normalized not in sections and normalized not in metadata]
    missing_metadata = [field for field in ("owner", "audience", "summary") if field not in metadata and field not in sections]

    owner_value = metadata.get("owner", "")
    owner_gaps = []
    if not owner_value and "owner" not in sections:
        owner_gaps.append("Owner is missing.")
    elif normalize(owner_value) in {"", "unknown", "none", "to be determined"}:
        owner_gaps.append("Owner value is not publishable.")

    review_value = metadata.get("review date") or metadata.get("review_date") or metadata.get("next review")
    stale_review_date = None
    if review_value:
        review_date = parse_date(review_value)
        if review_date is None:
            stale_review_date = {"value": review_value, "issue": "Review date could not be parsed."}
        elif review_date < today:
            stale_review_date = {"value": review_value, "issue": "Review date is before today."}
    else:
        stale_review_date = {"value": None, "issue": "Review date is missing."}

    unresolved = find_unresolved(text)
    blocking = bool(missing_sections or missing_metadata or owner_gaps or stale_review_date or unresolved)

    return {
        "missing_metadata": missing_metadata,
        "missing_sections": missing_sections,
        "stale_review_date": stale_review_date,
        "unresolved_assumptions": unresolved,
        "owner_gaps": owner_gaps,
        "publishing_readiness": "needs_review" if blocking else "ready",
        "caveats": ["This checker does not rewrite article content or verify factual accuracy."],
    }


def print_human(result: dict[str, object]) -> None:
    print("KB Metadata Check")
    print("=================")
    print(f"Publishing readiness: {result['publishing_readiness']}")
    for title, key in (
        ("Missing metadata", "missing_metadata"),
        ("Missing sections", "missing_sections"),
        ("Owner gaps", "owner_gaps"),
        ("Unresolved assumptions", "unresolved_assumptions"),
    ):
        print(f"\n{title}:")
        values = result[key]
        if not values:
            print("- None detected")
        else:
            for value in values:
                print(f"- {value}")
    print("\nReview date:")
    print(f"- {result['stale_review_date'] or 'Current or not flagged'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check KB markdown metadata and readiness.")
    parser.add_argument("--input", required=True, help="Path to markdown KB draft.")
    parser.add_argument("--required-sections", default="Title,Audience,Summary,Owner", help="Comma-separated section or metadata names.")
    parser.add_argument("--today", help="Override today's date as YYYY-MM-DD.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        raise SystemExit("--today must be YYYY-MM-DD or another supported date format")
    text = Path(args.input).read_text(encoding="utf-8")
    required_sections = [section.strip() for section in args.required_sections.split(",") if section.strip()]
    result = check(text, required_sections, today)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
