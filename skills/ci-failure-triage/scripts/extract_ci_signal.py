#!/usr/bin/env python3
"""Extract the strongest failure signal from noisy CI logs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd|authorization)\b\s*[:=]\s*([^\s]+)"),
    re.compile(r"(?i)\b(bearer)\s+([a-z0-9._~+/=-]{12,})"),
    re.compile(r"\b[A-Za-z0-9_=-]{20,}\.[A-Za-z0-9_=-]{20,}\.[A-Za-z0-9_=-]{10,}\b"),
]

FAILURE_PATTERNS = [
    ("test", re.compile(r"(?i)\b(assertionerror|expected .* actual|test .* failed|failures?:|failed tests?)\b")),
    ("compile", re.compile(r"(?i)\b(syntaxerror|typeerror:|cannot find symbol|compilation failed|ts\d{4})\b")),
    ("dependency", re.compile(r"(?i)\b(module not found|cannot find module|no matching distribution|package .* not found|dependency)\b")),
    ("configuration", re.compile(r"(?i)\b(missing .* env|environment variable|invalid config|permission denied|forbidden|unauthorized)\b")),
    ("infrastructure", re.compile(r"(?i)\b(timeout|connection refused|network is unreachable|service unavailable|runner lost|no space left)\b")),
    ("command", re.compile(r"(?i)\b(exit code [1-9]\d*|command failed|process completed with exit code [1-9]\d*)\b")),
]

COMMAND_RE = re.compile(r"^\s*(?:\$|>|run:|command:|\+)\s*(.+)$", re.IGNORECASE)
TEST_RE = re.compile(r"(?i)\b(test|spec|pytest|jest|vitest|rspec|go test|cargo test|xcodebuild test)\b")


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(lambda match: f"{match.group(1)} [REDACTED]" if len(match.groups()) > 1 else "[REDACTED]", redacted)
    return redacted


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    return sys.stdin.read()


def classify(line: str) -> tuple[str, re.Pattern[str]] | None:
    for failure_class, pattern in FAILURE_PATTERNS:
        if pattern.search(line):
            return failure_class, pattern
    return None


def extract(lines: list[str], context_lines: int) -> dict[str, object]:
    matches: list[dict[str, object]] = []
    commands: list[str] = []
    tests: list[str] = []

    for index, line in enumerate(lines):
        clean_line = redact(line.rstrip("\n"))
        command_match = COMMAND_RE.match(clean_line)
        if command_match:
            command = command_match.group(1).strip()
            if command and command not in commands:
                commands.append(command)
        if TEST_RE.search(clean_line) and clean_line.strip() not in tests:
            tests.append(clean_line.strip())

        classified = classify(clean_line)
        if not classified:
            continue

        failure_class, pattern = classified
        start = max(0, index - context_lines)
        end = min(len(lines), index + context_lines + 1)
        matches.append(
            {
                "line_number": index + 1,
                "failure_class": failure_class,
                "matched_pattern": pattern.pattern,
                "line": clean_line,
                "context": [redact(item.rstrip("\n")) for item in lines[start:end]],
            }
        )

    primary = matches[0] if matches else None
    caveats: list[str] = []
    if not matches:
        caveats.append("No high-confidence failure pattern was matched; inspect the full log manually.")
    if len(matches) > 1:
        caveats.append("Multiple failure-like lines were found; later matches may be downstream noise.")
    if not commands:
        caveats.append("No command line was detected in the provided log.")

    return {
        "primary_failure_signal": primary,
        "likely_failure_class": primary["failure_class"] if primary else "unknown",
        "matched_error_lines": matches[:10],
        "commands_detected": commands[:10],
        "tests_detected": tests[:10],
        "caveats": caveats,
    }


def print_human(result: dict[str, object]) -> None:
    primary = result["primary_failure_signal"]
    print("CI Failure Signal")
    print("=================")
    if isinstance(primary, dict):
        print(f"Primary signal: line {primary['line_number']} ({primary['failure_class']})")
        print(f"  {primary['line']}")
        print("\nContext:")
        for line in primary["context"]:
            print(f"  {line}")
    else:
        print("Primary signal: Not detected")

    print(f"\nLikely failure class: {result['likely_failure_class']}")
    print("\nCommands detected:")
    for command in result["commands_detected"] or ["Not detected"]:
        print(f"- {command}")
    print("\nTests detected:")
    for test in result["tests_detected"] or ["Not detected"]:
        print(f"- {test}")
    if result["caveats"]:
        print("\nCaveats:")
        for caveat in result["caveats"]:
            print(f"- {caveat}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract primary failure signal from a CI log.")
    parser.add_argument("--input", help="Path to a CI log file. Reads stdin when omitted.")
    parser.add_argument("--context-lines", type=int, default=3, help="Context lines around the primary match.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.context_lines < 0:
        raise SystemExit("--context-lines must be zero or greater")
    text = read_input(args.input)
    result = extract(text.splitlines(), args.context_lines)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
