#!/usr/bin/env python3
"""Validate smoke-test fixture completeness and expectation schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "tests" / "fixtures"
REGISTRY_FILE = ROOT / "skill-registry.json"
EXPECTED_KEYS = {"skill", "required_sections", "forbidden_claims", "required_caveats"}


def load_registry_featured_skills() -> tuple[set[str], list[str]]:
    try:
        data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return set(), ["missing skill-registry.json"]
    except json.JSONDecodeError as exc:
        return set(), [f"invalid skill-registry.json: {exc}"]

    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        return set(), ["skill-registry.json must contain a skills list"]

    featured = {
        item.get("name")
        for item in data["skills"]
        if isinstance(item, dict) and item.get("featured") is True and isinstance(item.get("name"), str)
    }
    return featured, []


def validate_string_list(value: object, key: str, skill: str) -> list[str]:
    if not isinstance(value, list) or not value:
        return [f"{skill}: {key} must be a non-empty list"]
    if not all(isinstance(item, str) and item.strip() for item in value):
        return [f"{skill}: {key} must contain only non-empty strings"]
    return []


def validate_fixture(skill: str) -> list[str]:
    errors: list[str] = []
    fixture_dir = FIXTURES_DIR / skill
    input_file = fixture_dir / "input.md"
    expectations_file = fixture_dir / "expectations.json"

    if not fixture_dir.is_dir():
        return [f"{skill}: missing fixture directory"]
    if not input_file.is_file():
        errors.append(f"{skill}: missing input.md")
    elif len(input_file.read_text(encoding="utf-8").strip()) < 80:
        errors.append(f"{skill}: input.md is too short to be a realistic fixture")

    if not expectations_file.is_file():
        errors.append(f"{skill}: missing expectations.json")
        return errors

    try:
        data = json.loads(expectations_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{skill}: invalid expectations.json: {exc}"]

    if not isinstance(data, dict):
        return [f"{skill}: expectations.json must contain an object"]

    keys = set(data)
    if keys != EXPECTED_KEYS:
        missing = EXPECTED_KEYS - keys
        extra = keys - EXPECTED_KEYS
        if missing:
            errors.append(f"{skill}: expectations.json missing key(s): {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"{skill}: expectations.json has unexpected key(s): {', '.join(sorted(extra))}")
        return errors

    if data["skill"] != skill:
        errors.append(f"{skill}: expectations skill must match fixture directory")
    errors.extend(validate_string_list(data["required_sections"], "required_sections", skill))
    errors.extend(validate_string_list(data["forbidden_claims"], "forbidden_claims", skill))
    errors.extend(validate_string_list(data["required_caveats"], "required_caveats", skill))
    return errors


def main() -> int:
    featured_skills, errors = load_registry_featured_skills()
    if not featured_skills:
        errors.append("no featured skills found in registry")

    if not FIXTURES_DIR.is_dir():
        errors.append("missing tests/fixtures directory")
    else:
        fixture_names = {path.name for path in FIXTURES_DIR.iterdir() if path.is_dir()}
        missing = featured_skills - fixture_names
        extra = fixture_names - featured_skills
        if missing:
            errors.append(f"missing fixture(s): {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"unexpected fixture(s): {', '.join(sorted(extra))}")
        for skill in sorted(featured_skills):
            errors.extend(validate_fixture(skill))

    if errors:
        print("Smoke fixture validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated smoke fixtures for {len(featured_skills)} featured skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
