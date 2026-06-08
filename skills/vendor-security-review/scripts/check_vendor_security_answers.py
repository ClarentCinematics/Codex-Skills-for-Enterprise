#!/usr/bin/env python3
"""Check vendor security questionnaire text for required topic coverage."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TOPICS = {
    "soc2": ("soc2", "soc 2", "type ii", "independent audit", "audit report"),
    "dpa": ("dpa", "data processing agreement", "data protection agreement"),
    "subprocessors": ("subprocessor", "sub-processors", "third party processors", "processors"),
    "data_retention": ("retention", "deletion", "delete data", "data export", "data return"),
    "breach_notification": ("breach notification", "security incident notification", "incident notice", "notify within"),
    "encryption": ("encryption", "encrypted", "tls", "at rest", "in transit"),
    "sso": ("sso", "single sign", "saml", "oidc", "mfa", "multi-factor"),
    "audit_logs": ("audit log", "audit logs", "audit trail", "admin log", "admin logs", "activity log", "activity logs"),
}
WEAK_ANSWER_RE = re.compile(r"\b(tbd|unknown|not sure|pending|planned|roadmap|not available|not included|not provided|missing|to be determined)\b", re.I)
NEGATIVE_RE = re.compile(r"\b(tbd|unknown|pending|not available|not included|not provided|missing|to be determined)\b", re.I)


def keyword_present(line: str, keyword: str) -> bool:
    escaped = re.escape(keyword)
    if keyword.isalnum():
        return bool(re.search(rf"\b{escaped}\b", line, re.I))
    return bool(re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", line, re.I))


def find_lines(text: str, keywords: tuple[str, ...], *, positive_only: bool = False) -> list[dict[str, object]]:
    matches = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(keyword_present(line, keyword) for keyword in keywords):
            if positive_only and NEGATIVE_RE.search(line):
                continue
            matches.append({"line": line_number, "text": line.strip()})
    return matches


def check_answers(text: str) -> dict[str, object]:
    coverage = {}
    missing_topics = []
    for topic, keywords in TOPICS.items():
        lines = find_lines(text, keywords, positive_only=True)
        coverage[topic] = {"covered": bool(lines), "evidence": lines[:5]}
        if not lines:
            missing_topics.append(topic)

    weak_answers = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = WEAK_ANSWER_RE.search(line)
        if match:
            weak_answers.append({"line": line_number, "marker": match.group(0), "text": line.strip()})

    readiness = "ready"
    if missing_topics or weak_answers:
        readiness = "needs_review"
    if len(text.strip()) < 80:
        readiness = "blocked"

    return {
        "readiness": readiness,
        "coverage": coverage,
        "missing_topics": missing_topics,
        "weak_answers": weak_answers,
        "caveats": ["This helper checks topic coverage only and does not approve vendors, certify compliance, or provide legal advice."],
    }


def print_human(result: dict[str, object]) -> None:
    print("Vendor Security Coverage Check")
    print("==============================")
    print(f"Readiness: {result['readiness']}")
    print("\nMissing topics:")
    for item in result["missing_topics"] or ["None detected"]:
        print(f"- {item}")
    print("\nWeak answers:")
    for item in result["weak_answers"] or [{"text": "None detected"}]:
        print(f"- {item['text']}")
    print("\nCaveats:")
    for caveat in result["caveats"]:
        print(f"- {caveat}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check vendor security questionnaire coverage.")
    parser.add_argument("--input", required=True, help="Path to questionnaire or answer draft.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = check_answers(Path(args.input).read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
