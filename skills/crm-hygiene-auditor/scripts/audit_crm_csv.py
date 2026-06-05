#!/usr/bin/env python3
"""Audit CRM CSV exports for deterministic hygiene signals."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path


COMMIT_STAGES = {"commit", "best case", "forecast", "proposal", "negotiation", "contracting", "closed won"}
ACCOUNT_FIELDS = ("account", "account_name", "company", "company_name", "name")
BLANK_VALUE_RE = re.compile(r"(?i)^\s*(n/?a|none|null|unknown|tbd|to be determined|-)?\s*$")


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


def is_blank(value: str | None) -> bool:
    return value is None or bool(BLANK_VALUE_RE.match(value))


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def load_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = [{key: (value or "") for key, value in row.items()} for row in reader]
        return rows, list(reader.fieldnames or [])


def record_label(row: dict[str, str], index: int) -> str:
    for field in ("id", "opportunity_id", "record_id", "name", "opportunity_name", "account", "account_name"):
        value = row.get(field)
        if value and not is_blank(value):
            return value
    return f"row {index}"


def audit(rows: list[dict[str, str]], fieldnames: list[str], required_fields: list[str], date_field: str, stale_days: int, today: date) -> dict[str, object]:
    missing_schema_fields = [field for field in required_fields if field not in fieldnames]
    missing_required_values: list[dict[str, object]] = []
    stale_next_steps: list[dict[str, object]] = []
    forecast_risks: list[dict[str, object]] = []
    duplicate_candidates: list[dict[str, object]] = []

    duplicate_index: dict[str, list[tuple[int, dict[str, str]]]] = defaultdict(list)
    account_field = next((field for field in ACCOUNT_FIELDS if field in fieldnames), None)

    for index, row in enumerate(rows, start=1):
        label = record_label(row, index)
        missing_fields = [field for field in required_fields if field in fieldnames and is_blank(row.get(field))]
        if missing_fields:
            missing_required_values.append({"record": label, "row": index, "missing_fields": missing_fields})

        activity_date = parse_date(row.get(date_field, "")) if date_field in fieldnames else None
        next_step = row.get("next_step", "")
        if activity_date and (today - activity_date).days > stale_days:
            stale_next_steps.append(
                {
                    "record": label,
                    "row": index,
                    "last_activity_date": activity_date.isoformat(),
                    "days_stale": (today - activity_date).days,
                    "next_step_present": not is_blank(next_step),
                }
            )

        stage = normalize(row.get("stage", ""))
        forecast = normalize(row.get("forecast_category", row.get("forecast", "")))
        probability = row.get("probability", row.get("probability_percent", "")).strip().rstrip("%")
        high_probability = probability.isdigit() and int(probability) >= 70
        committed = stage in COMMIT_STAGES or forecast in COMMIT_STAGES or high_probability
        weak_evidence = [field for field in ("next_step", "close_date", "owner") if field in fieldnames and is_blank(row.get(field))]
        if committed and weak_evidence:
            forecast_risks.append({"record": label, "row": index, "stage": row.get("stage", ""), "weak_evidence": weak_evidence})

        if account_field:
            account_value = normalize(row.get(account_field, ""))
            if account_value:
                key_parts = [account_value, normalize(row.get("close_date", "")), normalize(row.get("amount", ""))]
                duplicate_index["|".join(key_parts)].append((index, row))

    for records in duplicate_index.values():
        if len(records) > 1:
            duplicate_candidates.append(
                {
                    "records": [record_label(row, index) for index, row in records],
                    "rows": [index for index, _row in records],
                    "reason": "Matching normalized account plus close date and amount.",
                }
            )

    total_findings = len(missing_schema_fields) + len(missing_required_values) + len(stale_next_steps) + len(forecast_risks) + len(duplicate_candidates)
    severity = "low"
    if missing_schema_fields or forecast_risks:
        severity = "high"
    elif total_findings:
        severity = "medium"

    cleanup_actions = []
    if missing_schema_fields:
        cleanup_actions.append("Add missing required fields to the export or rerun with the correct schema.")
    if missing_required_values:
        cleanup_actions.append("Ask record owners to fill missing required values from source-of-truth notes.")
    if stale_next_steps:
        cleanup_actions.append("Review stale records and confirm whether next steps are still current.")
    if forecast_risks:
        cleanup_actions.append("Require forecast evidence before treating committed records as reliable.")
    if duplicate_candidates:
        cleanup_actions.append("Have CRM admins review duplicate-looking records before merging.")

    return {
        "row_count": len(rows),
        "severity": severity,
        "missing_fields": {"schema": missing_schema_fields, "records": missing_required_values},
        "stale_next_steps": stale_next_steps,
        "unsupported_forecast_risks": forecast_risks,
        "duplicate_looking_records": duplicate_candidates,
        "cleanup_actions": cleanup_actions,
        "caveats": ["This audit flags deterministic hygiene risks only and does not infer missing CRM values."],
    }


def print_human(result: dict[str, object]) -> None:
    print("CRM Hygiene Audit")
    print("=================")
    print(f"Rows reviewed: {result['row_count']}")
    print(f"Severity: {result['severity']}")
    for title, key in (
        ("Missing fields", "missing_fields"),
        ("Stale next steps", "stale_next_steps"),
        ("Unsupported forecast risks", "unsupported_forecast_risks"),
        ("Duplicate-looking records", "duplicate_looking_records"),
    ):
        print(f"\n{title}:")
        value = result[key]
        if not value or (isinstance(value, dict) and not value.get("schema") and not value.get("records")):
            print("- None detected")
            continue
        if isinstance(value, dict):
            for item in value.get("schema", []):
                print(f"- Missing export field: {item}")
            for item in value.get("records", []):
                print(f"- {item['record']} row {item['row']}: missing {', '.join(item['missing_fields'])}")
        else:
            for item in value:
                print(f"- {item}")
    print("\nCleanup actions:")
    for action in result["cleanup_actions"] or ["No cleanup actions generated."]:
        print(f"- {action}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit a CRM CSV export for hygiene risks.")
    parser.add_argument("--input", required=True, help="Path to CRM CSV export.")
    parser.add_argument("--required-fields", default="owner,stage,next_step,close_date", help="Comma-separated required fields.")
    parser.add_argument("--date-field", default="last_activity_date", help="Date field used for stale activity checks.")
    parser.add_argument("--stale-days", type=int, default=14, help="Days after which activity is stale.")
    parser.add_argument("--today", help="Override today's date as YYYY-MM-DD.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        raise SystemExit("--today must be YYYY-MM-DD or another supported date format")
    rows, fieldnames = load_rows(Path(args.input))
    required_fields = [field.strip() for field in args.required_fields.split(",") if field.strip()]
    result = audit(rows, fieldnames, required_fields, args.date_field, args.stale_days, today)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
