#!/usr/bin/env python3
"""Audit CSV data-quality signals using deterministic checks."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


BLANK_RE = re.compile(r"(?i)^\s*(n/a|none|null|unknown|tbd|to be determined|-)?\s*$")


def is_blank(value: str | None) -> bool:
    return value is None or bool(BLANK_RE.match(value))


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def load_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return [{key: (value or "") for key, value in row.items()} for row in reader], list(reader.fieldnames or [])


def split_fields(value: str) -> list[str]:
    return [field.strip() for field in value.split(",") if field.strip()]


def infer_date_fields(fieldnames: list[str]) -> list[str]:
    return [field for field in fieldnames if "date" in field.lower() or field.lower().endswith("_at")]


def audit(rows: list[dict[str, str]], fieldnames: list[str], key_fields: list[str], date_fields: list[str], stale_days: int, today: date) -> dict[str, object]:
    row_count = len(rows)
    null_rates = []
    for field in fieldnames:
        missing = sum(1 for row in rows if is_blank(row.get(field)))
        rate = (missing / row_count) if row_count else 0
        if missing:
            null_rates.append({"field": field, "missing": missing, "rate": round(rate, 4)})

    duplicate_keys = []
    missing_key_fields = [field for field in key_fields if field not in fieldnames]
    if key_fields and not missing_key_fields:
        counts: Counter[str] = Counter()
        examples: dict[str, list[int]] = defaultdict(list)
        for index, row in enumerate(rows, start=1):
            key = "|".join(row.get(field, "") for field in key_fields)
            counts[key] += 1
            examples[key].append(index)
        duplicate_keys = [{"key": key, "count": count, "rows": examples[key][:10]} for key, count in counts.items() if key and count > 1]

    stale_dates = []
    for field in date_fields:
        if field not in fieldnames:
            continue
        stale_rows = []
        invalid_rows = []
        for index, row in enumerate(rows, start=1):
            raw = row.get(field, "")
            parsed = parse_date(raw)
            if is_blank(raw):
                continue
            if parsed is None:
                invalid_rows.append({"row": index, "value": raw})
            elif (today - parsed).days > stale_days:
                stale_rows.append({"row": index, "value": parsed.isoformat(), "days_stale": (today - parsed).days})
        if stale_rows or invalid_rows:
            stale_dates.append({"field": field, "stale_rows": stale_rows[:10], "invalid_rows": invalid_rows[:10]})

    enum_inconsistencies = []
    for field in fieldnames:
        values = [row.get(field, "").strip() for row in rows if not is_blank(row.get(field))]
        unique_values = sorted(set(values))
        if not 2 <= len(unique_values) <= 30:
            continue
        buckets: dict[str, set[str]] = defaultdict(set)
        for value in unique_values:
            buckets[normalize(value)].add(value)
        variants = [{"normalized": key, "values": sorted(bucket)} for key, bucket in buckets.items() if len(bucket) > 1]
        if variants:
            enum_inconsistencies.append({"field": field, "variants": variants})

    severity = "low"
    if missing_key_fields or duplicate_keys:
        severity = "high"
    elif null_rates or stale_dates or enum_inconsistencies:
        severity = "medium"

    return {
        "row_count": row_count,
        "field_count": len(fieldnames),
        "severity": severity,
        "missing_key_fields": missing_key_fields,
        "null_rates": null_rates,
        "duplicate_keys": duplicate_keys,
        "stale_dates": stale_dates,
        "enum_inconsistencies": enum_inconsistencies,
        "caveats": ["This audit checks the provided CSV sample only and does not infer missing values, metric definitions, or source-of-truth status."],
    }


def print_human(result: dict[str, object]) -> None:
    print("Data Quality Audit")
    print("==================")
    print(f"Rows reviewed: {result['row_count']}")
    print(f"Fields reviewed: {result['field_count']}")
    print(f"Severity: {result['severity']}")
    for title, key in (
        ("Missing key fields", "missing_key_fields"),
        ("Null rates", "null_rates"),
        ("Duplicate keys", "duplicate_keys"),
        ("Stale dates", "stale_dates"),
        ("Enum inconsistencies", "enum_inconsistencies"),
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
    parser = argparse.ArgumentParser(description="Audit CSV data-quality signals.")
    parser.add_argument("--input", required=True, help="Path to CSV file.")
    parser.add_argument("--key-fields", default="", help="Comma-separated key fields used for duplicate checks.")
    parser.add_argument("--date-fields", default="", help="Comma-separated date fields used for stale-date checks.")
    parser.add_argument("--stale-days", type=int, default=30, help="Days after which a date is considered stale.")
    parser.add_argument("--today", help="Override today's date as YYYY-MM-DD.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows, fieldnames = load_csv(Path(args.input))
    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    key_fields = split_fields(args.key_fields)
    date_fields = split_fields(args.date_fields) or infer_date_fields(fieldnames)
    result = audit(rows, fieldnames, key_fields, date_fields, args.stale_days, today)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
