#!/usr/bin/env python3
"""Mine repeated support ticket themes from CSV or plain text."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


SUBJECT_FIELDS = ("subject", "title", "summary", "ticket_subject", "issue")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "cannot", "for", "from", "how", "i", "in", "is",
    "it", "my", "of", "on", "or", "our", "please", "the", "to", "with", "we", "when", "why", "not", "error",
}


def normalize_subject(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


def load_subjects(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".csv":
        rows = list(csv.DictReader(text.splitlines()))
        if rows:
            fieldnames = {name.lower(): name for name in rows[0].keys()}
            subject_field = next((fieldnames[field] for field in SUBJECT_FIELDS if field in fieldnames), None)
            if subject_field:
                return [row.get(subject_field, "").strip() for row in rows if row.get(subject_field, "").strip()]
    subjects = []
    for line in text.splitlines():
        cleaned = re.sub(r"^\s*[-*]?\s*(ticket\s*\d+[:.-])?\s*", "", line.strip(), flags=re.I)
        if cleaned:
            subjects.append(cleaned)
    return subjects


def theme_key(subject: str) -> str:
    tokens = [token for token in normalize_subject(subject).split() if len(token) > 2 and token not in STOPWORDS]
    if not tokens:
        return "uncategorized"
    counts = Counter(tokens)
    return " ".join(token for token, _count in counts.most_common(3))


def mine(subjects: list[str]) -> dict[str, object]:
    normalized_counts = Counter(normalize_subject(subject) for subject in subjects if normalize_subject(subject))
    duplicate_subjects = [
        {"subject": subject, "count": count}
        for subject, count in normalized_counts.most_common()
        if count > 1
    ]

    grouped: dict[str, list[str]] = defaultdict(list)
    for subject in subjects:
        grouped[theme_key(subject)].append(subject)

    top_themes = []
    for key, values in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(values) < 2:
            continue
        top_themes.append({"theme": key, "count": len(values), "examples": values[:5]})

    return {
        "subject_count": len(subjects),
        "top_repeated_issues": top_themes[:10],
        "duplicate_looking_subjects": duplicate_subjects[:10],
        "caveats": [
            "Theme clustering is keyword-based and should be reviewed before creating KB, product, or automation work.",
            "Ticket subjects alone do not prove root cause or total support volume.",
        ],
    }


def print_human(result: dict[str, object]) -> None:
    print("Support Deflection Theme Mining")
    print("===============================")
    print(f"Subjects reviewed: {result['subject_count']}")
    print("\nTop repeated issues:")
    for item in result["top_repeated_issues"] or [{"theme": "None detected", "count": 0, "examples": []}]:
        print(f"- {item['theme']} ({item['count']})")
        for example in item.get("examples", [])[:3]:
            print(f"  - {example}")
    print("\nDuplicate-looking subjects:")
    for item in result["duplicate_looking_subjects"] or [{"subject": "None detected", "count": 0}]:
        print(f"- {item['subject']} ({item['count']})")
    print("\nCaveats:")
    for caveat in result["caveats"]:
        print(f"- {caveat}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mine repeated support themes from CSV or text subjects.")
    parser.add_argument("--input", required=True, help="Path to CSV or text file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = mine(load_subjects(Path(args.input)))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
