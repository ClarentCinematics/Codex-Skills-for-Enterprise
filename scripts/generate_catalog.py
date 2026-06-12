#!/usr/bin/env python3
"""Generate the registry-backed skill catalog documentation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "skill-registry.json"
CATALOG_FILE = ROOT / "docs" / "catalog.md"
FIXTURES_DIR = ROOT / "tests" / "fixtures"


def load_registry() -> list[dict[str, object]]:
    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise SystemExit("skill-registry.json must contain a skills list")
    return [item for item in skills if isinstance(item, dict)]


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def fixture_status(skill_name: str) -> str:
    fixture_dir = FIXTURES_DIR / skill_name
    if (fixture_dir / "input.md").is_file() and (fixture_dir / "expectations.json").is_file():
        return "Yes"
    return "No"


def generate_catalog() -> str:
    skills = sorted(load_registry(), key=lambda item: (str(item["pack"]), str(item["name"])))
    lines = [
        "# Skill Catalog",
        "",
        "This catalog is generated from `skill-registry.json`. Do not edit it by hand; run `python3 scripts/generate_catalog.py` after registry changes.",
        "",
        "| Skill | Pack | Maturity | Audience | Scripts | Fixtures | Risk | Human Review | Evaluation | Featured |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for item in skills:
        name = str(item["name"])
        skill_link = f"[`{name}`](../skills/{name}/SKILL.md)"
        lines.append(
            "| "
            + " | ".join(
                [
                    skill_link,
                    f"`{item['pack']}`",
                    f"Level {item['maturity']}",
                    str(item["audience"]),
                    yes_no(bool(item["has_scripts"])),
                    fixture_status(name),
                    str(item["risk_level"]).title(),
                    str(item["human_review"]).title(),
                    str(item["evaluation_status"]).replace("-", " ").title(),
                    yes_no(bool(item["featured"])),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Maintenance",
            "",
            "- Update `skill-registry.json` when skill trust, maturity, pack, audience, fixture, or featured metadata changes.",
            "- Run `python3 scripts/generate_catalog.py` after registry changes.",
            "- Run `python3 scripts/validate_skills.py` to confirm this file is current.",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate docs/catalog.md from skill-registry.json.")
    parser.add_argument("--check", action="store_true", help="Check whether docs/catalog.md is current without writing.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    expected = generate_catalog()
    if args.check:
        actual = CATALOG_FILE.read_text(encoding="utf-8") if CATALOG_FILE.exists() else ""
        if actual != expected:
            raise SystemExit("docs/catalog.md is out of date. Run python3 scripts/generate_catalog.py")
        print("docs/catalog.md is current.")
        return 0

    CATALOG_FILE.write_text(expected, encoding="utf-8")
    print(f"Generated {CATALOG_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
