#!/usr/bin/env python3
"""Validate deterministic skill eval and trigger definitions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "skill-registry.json"
EVALS_DIR = ROOT / "tests" / "evals"
TRIGGERS_FILE = ROOT / "tests" / "trigger-cases.json"
EVAL_KEYS = {"skill", "cases"}
CASE_KEYS = {
    "id",
    "category",
    "prompt",
    "fixture",
    "required_sections",
    "forbidden_claims",
    "required_caveats",
}
TRIGGER_KEYS = {"positive", "paraphrases", "hard_negatives", "confusable_with"}
VALID_CATEGORIES = {"representative", "incomplete-evidence", "unsupported-claim"}


def load_json(path: Path, label: str) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [f"missing {label}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid {label}: {exc}"]


def load_registry() -> tuple[dict[str, dict[str, object]], list[str]]:
    data, errors = load_json(REGISTRY_FILE, "skill-registry.json")
    if errors:
        return {}, errors
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        return {}, ["skill-registry.json must contain a skills list"]
    skills = {
        item["name"]: item
        for item in data["skills"]
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    return skills, []


def validate_string_list(value: object, label: str, minimum: int = 1) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum:
        return [f"{label} must contain at least {minimum} item(s)"]
    if not all(isinstance(item, str) and item.strip() for item in value):
        return [f"{label} must contain only non-empty strings"]
    return []


def normalize_prompt(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def duplicate_prompts(prompts: list[str]) -> list[str]:
    normalized = [normalize_prompt(prompt) for prompt in prompts]
    return sorted({prompt for prompt in normalized if normalized.count(prompt) > 1})


def validate_eval_file(path: Path, skill: str) -> tuple[list[str], list[str]]:
    data, errors = load_json(path, str(path.relative_to(ROOT)))
    prompts: list[str] = []
    if errors:
        return errors, prompts
    if not isinstance(data, dict) or set(data) != EVAL_KEYS:
        return [f"{skill}: eval file must contain exactly skill and cases"], prompts
    if data.get("skill") != skill:
        errors.append(f"{skill}: eval skill must match filename")
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) != 3:
        return errors + [f"{skill}: eval file must contain exactly three cases"], prompts

    seen_ids: set[str] = set()
    categories: set[str] = set()
    for index, case in enumerate(cases, start=1):
        label = f"{skill}: case {index}"
        if not isinstance(case, dict) or set(case) != CASE_KEYS:
            errors.append(f"{label} must contain exactly {', '.join(sorted(CASE_KEYS))}")
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case_id):
            errors.append(f"{label} id must use lowercase hyphen-case")
        elif case_id in seen_ids:
            errors.append(f"{label} duplicates case id {case_id}")
        else:
            seen_ids.add(case_id)
        category = case["category"]
        if category not in VALID_CATEGORIES:
            errors.append(f"{label} has invalid category")
        else:
            categories.add(category)
        prompt = case["prompt"]
        if not isinstance(prompt, str) or len(prompt.strip()) < 40:
            errors.append(f"{label} prompt must be a realistic non-empty request")
        else:
            prompts.append(prompt)
        fixture = case["fixture"]
        if not isinstance(fixture, str) or not fixture.startswith("tests/"):
            errors.append(f"{label} fixture must be a repository-relative tests/ path")
        else:
            fixture_path = (ROOT / fixture).resolve()
            if ROOT.resolve() not in fixture_path.parents or not fixture_path.is_file():
                errors.append(f"{label} fixture does not exist: {fixture}")
        for key in ("required_sections", "forbidden_claims", "required_caveats"):
            errors.extend(validate_string_list(case[key], f"{label} {key}"))
    if categories != VALID_CATEGORIES:
        errors.append(f"{skill}: cases must cover {', '.join(sorted(VALID_CATEGORIES))}")
    return errors, prompts


def validate_trigger_cases(skills: dict[str, dict[str, object]]) -> tuple[list[str], list[str]]:
    data, errors = load_json(TRIGGERS_FILE, "tests/trigger-cases.json")
    prompts: list[str] = []
    if errors:
        return errors, prompts
    if not isinstance(data, dict):
        return ["tests/trigger-cases.json must contain an object"], prompts

    expected = set(skills)
    actual = set(data)
    if expected != actual:
        missing = expected - actual
        extra = actual - expected
        if missing:
            errors.append(f"trigger cases missing skill(s): {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"trigger cases reference unknown skill(s): {', '.join(sorted(extra))}")

    for skill, entry in data.items():
        if not isinstance(entry, dict) or set(entry) != TRIGGER_KEYS:
            errors.append(f"{skill}: trigger entry must contain exactly {', '.join(sorted(TRIGGER_KEYS))}")
            continue
        for key, minimum in (("positive", 2), ("paraphrases", 1), ("hard_negatives", 1)):
            errors.extend(validate_string_list(entry[key], f"{skill}: {key}", minimum))
            if isinstance(entry[key], list):
                prompts.extend(item for item in entry[key] if isinstance(item, str))
        confusable = entry["confusable_with"]
        errors.extend(validate_string_list(confusable, f"{skill}: confusable_with"))
        if isinstance(confusable, list):
            for other in confusable:
                if other not in skills:
                    errors.append(f"{skill}: confusable skill does not exist: {other}")
                if other == skill:
                    errors.append(f"{skill}: cannot be confusable with itself")
    return errors, prompts


def main() -> int:
    skills, errors = load_registry()
    featured = {name for name, item in skills.items() if item.get("featured") is True}
    if not EVALS_DIR.is_dir():
        errors.append("missing tests/evals directory")
    else:
        eval_files = {path.stem: path for path in EVALS_DIR.glob("*.json")}
        if set(eval_files) != featured:
            missing = featured - set(eval_files)
            extra = set(eval_files) - featured
            if missing:
                errors.append(f"missing featured eval(s): {', '.join(sorted(missing))}")
            if extra:
                errors.append(f"unexpected eval(s): {', '.join(sorted(extra))}")

        all_prompts: list[str] = []
        for skill in sorted(featured & set(eval_files)):
            file_errors, prompts = validate_eval_file(eval_files[skill], skill)
            errors.extend(file_errors)
            all_prompts.extend(prompts)
        trigger_errors, trigger_prompts = validate_trigger_cases(skills)
        errors.extend(trigger_errors)
        all_prompts.extend(trigger_prompts)
        duplicates = duplicate_prompts(all_prompts)
        if duplicates:
            errors.append(f"duplicate eval or trigger prompt(s): {len(duplicates)}")

    if errors:
        print("Eval validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated evals for {len(featured)} featured skills and trigger cases for {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
