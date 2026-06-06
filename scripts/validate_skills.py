#!/usr/bin/env python3
"""Validate repository skill structure and core metadata."""

from __future__ import annotations

import json
import re
import stat
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - depends on local environment
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PACKS_FILE = ROOT / "skill-packs.json"
REGISTRY_FILE = ROOT / "skill-registry.json"
README_FILE = ROOT / "README.md"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DISALLOWED_SKILL_DOCS = {
    "README.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
    "CHANGELOG.md",
}
SCRIPT_PLACEHOLDERS = ("TODO", "FIXME", "PLACEHOLDER", "REPLACE_ME", "YOUR_")
REGISTRY_KEYS = {
    "name",
    "pack",
    "maturity",
    "audience",
    "primary_artifacts",
    "has_references",
    "has_scripts",
    "risk_level",
    "featured",
}
VALID_RISK_LEVELS = {"low", "medium", "high"}


def validate_script_file(skill_name: str, script_path: Path) -> list[str]:
    errors: list[str] = []

    if script_path.suffix != ".py":
        errors.append(f"{skill_name}: script must be a Python file: {script_path.name}")
        return errors

    text = script_path.read_text(encoding="utf-8")
    try:
        compile(text, str(script_path), "exec")
    except SyntaxError as exc:
        errors.append(f"{skill_name}: script {script_path.name} has invalid Python syntax: {exc}")

    for placeholder in SCRIPT_PLACEHOLDERS:
        if placeholder in text:
            errors.append(f"{skill_name}: script {script_path.name} contains placeholder text: {placeholder}")

    mode = script_path.stat().st_mode
    executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    runnable_by_python = script_path.suffix == ".py"
    if not executable and not runnable_by_python:
        errors.append(f"{skill_name}: script {script_path.name} is neither executable nor runnable by python3")

    return errors


def validate_scripts_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_name = skill_dir.name
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return errors

    if not scripts_dir.is_dir():
        return [f"{skill_name}: scripts exists but is not a directory"]

    script_files = sorted(path for path in scripts_dir.iterdir() if path.is_file())
    if not script_files:
        errors.append(f"{skill_name}: scripts directory is empty")

    nested_files = [path for path in scripts_dir.glob("*/*") if path.is_file() and "__pycache__" not in path.parts]
    if nested_files:
        errors.append(f"{skill_name}: scripts must be one level deep")

    for script_path in script_files:
        errors.extend(validate_script_file(skill_name, script_path))

    return errors


def parse_frontmatter(path: Path) -> tuple[dict[str, str] | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "missing YAML frontmatter"

    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "unterminated YAML frontmatter"

    raw = text[4:end]
    if yaml is not None:
        data = yaml.safe_load(raw)
    else:
        data = {}
        for line in raw.splitlines():
            if ":" not in line:
                return None, f"cannot parse frontmatter line without PyYAML: {line}"
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

    if not isinstance(data, dict):
        return None, "frontmatter must be a mapping"
    return data, None


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_name = skill_dir.name

    if not NAME_RE.fullmatch(skill_name):
        errors.append(f"{skill_name}: folder name must be lowercase hyphen-case")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{skill_name}: missing SKILL.md")
        return errors

    data, parse_error = parse_frontmatter(skill_md)
    if parse_error:
        errors.append(f"{skill_name}: {parse_error}")
        return errors

    assert data is not None
    keys = set(data)
    if keys != {"name", "description"}:
        errors.append(f"{skill_name}: frontmatter must contain only name and description")

    if data.get("name") != skill_name:
        errors.append(f"{skill_name}: frontmatter name must match folder name")

    description = str(data.get("description", "")).strip()
    if len(description) < 120:
        errors.append(f"{skill_name}: description is too short for reliable triggering")
    if "use when" not in description.lower():
        errors.append(f"{skill_name}: description must include explicit 'Use when' trigger language")

    body = skill_md.read_text(encoding="utf-8")
    if "[TODO" in body or "TODO:" in body:
        errors.append(f"{skill_name}: SKILL.md contains placeholder TODO text")

    agents_file = skill_dir / "agents" / "openai.yaml"
    if not agents_file.exists():
        errors.append(f"{skill_name}: missing agents/openai.yaml")
    else:
        agents_text = agents_file.read_text(encoding="utf-8")
        if "default_prompt" not in agents_text:
            errors.append(f"{skill_name}: agents/openai.yaml missing default_prompt")
        if f"${skill_name}" not in agents_text:
            errors.append(f"{skill_name}: default_prompt must mention ${skill_name}")

    for filename in DISALLOWED_SKILL_DOCS:
        if (skill_dir / filename).exists():
            errors.append(f"{skill_name}: disallowed auxiliary doc {filename}")

    references_dir = skill_dir / "references"
    if references_dir.exists():
        nested = [path for path in references_dir.glob("*/*") if path.is_file()]
        if nested:
            errors.append(f"{skill_name}: references must be one level deep")

    errors.extend(validate_scripts_dir(skill_dir))

    return errors


def validate_packs(skill_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    skill_names = {path.name for path in skill_dirs}

    if not PACKS_FILE.exists():
        errors.append("missing skill-packs.json")
        return errors

    try:
        data = json.loads(PACKS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid skill-packs.json: {exc}")
        return errors

    if not isinstance(data, dict):
        errors.append("skill-packs.json must contain an object")
        return errors

    required_packs = {"executive-ops", "engineering-ops", "revenue-ops", "knowledge-ops", "all"}
    missing_packs = required_packs - set(data)
    if missing_packs:
        errors.append(f"skill-packs.json missing pack(s): {', '.join(sorted(missing_packs))}")

    for pack_name, skills in data.items():
        if not NAME_RE.fullmatch(pack_name):
            errors.append(f"pack '{pack_name}' must use lowercase hyphen-case")
        if not isinstance(skills, list) or not skills:
            errors.append(f"pack '{pack_name}' must contain a non-empty skill list")
            continue
        seen: set[str] = set()
        for skill_name in skills:
            if not isinstance(skill_name, str):
                errors.append(f"pack '{pack_name}' contains a non-string skill reference")
                continue
            if skill_name in seen:
                errors.append(f"pack '{pack_name}' contains duplicate skill '{skill_name}'")
            seen.add(skill_name)
            if skill_name not in skill_names:
                errors.append(f"pack '{pack_name}' references unknown skill '{skill_name}'")

    all_pack = data.get("all")
    if isinstance(all_pack, list) and set(all_pack) != skill_names:
        missing = skill_names - set(all_pack)
        extra = set(all_pack) - skill_names
        if missing:
            errors.append(f"pack 'all' missing skill(s): {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"pack 'all' has unknown skill(s): {', '.join(sorted(extra))}")

    return errors


def load_json_file(path: Path, label: str) -> tuple[object | None, list[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [f"missing {label}"]
    except json.JSONDecodeError as exc:
        return None, [f"invalid {label}: {exc}"]


def load_pack_data() -> tuple[dict[str, list[str]] | None, list[str]]:
    data, errors = load_json_file(PACKS_FILE, "skill-packs.json")
    if errors:
        return None, errors
    if not isinstance(data, dict):
        return None, ["skill-packs.json must contain an object"]
    packs: dict[str, list[str]] = {}
    for pack_name, skills in data.items():
        if isinstance(pack_name, str) and isinstance(skills, list):
            packs[pack_name] = [str(skill) for skill in skills]
    return packs, []


def validate_registry(skill_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    skill_names = {path.name for path in skill_dirs}
    registry_data, load_errors = load_json_file(REGISTRY_FILE, "skill-registry.json")
    if load_errors:
        return load_errors

    if not isinstance(registry_data, dict) or not isinstance(registry_data.get("skills"), list):
        return ["skill-registry.json must contain an object with a skills list"]

    packs, pack_errors = load_pack_data()
    errors.extend(pack_errors)
    pack_lookup: dict[str, str] = {}
    if packs is not None:
        for pack_name, pack_skills in packs.items():
            if pack_name == "all":
                continue
            for skill_name in pack_skills:
                if skill_name in pack_lookup:
                    errors.append(f"registry: skill '{skill_name}' appears in multiple non-all packs")
                pack_lookup[skill_name] = pack_name

    registry_names: set[str] = set()
    for index, item in enumerate(registry_data["skills"], start=1):
        if not isinstance(item, dict):
            errors.append(f"registry: skill entry {index} must be an object")
            continue

        keys = set(item)
        if keys != REGISTRY_KEYS:
            missing = REGISTRY_KEYS - keys
            extra = keys - REGISTRY_KEYS
            if missing:
                errors.append(f"registry: entry {index} missing key(s): {', '.join(sorted(missing))}")
            if extra:
                errors.append(f"registry: entry {index} has unexpected key(s): {', '.join(sorted(extra))}")
            continue

        name = item["name"]
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"registry: entry {index} has invalid skill name")
            continue
        if name in registry_names:
            errors.append(f"registry: duplicate skill '{name}'")
        registry_names.add(name)
        if name not in skill_names:
            errors.append(f"registry: skill '{name}' is not present under skills/")

        pack = item["pack"]
        if not isinstance(pack, str) or not NAME_RE.fullmatch(pack) or pack == "all":
            errors.append(f"registry: skill '{name}' has invalid pack")
        elif packs is not None and pack_lookup.get(name) != pack:
            errors.append(f"registry: skill '{name}' pack '{pack}' does not match skill-packs.json")

        maturity = item["maturity"]
        if not isinstance(maturity, int) or maturity < 1 or maturity > 5:
            errors.append(f"registry: skill '{name}' maturity must be an integer from 1 to 5")

        if not isinstance(item["audience"], str) or not item["audience"].strip():
            errors.append(f"registry: skill '{name}' audience must be a non-empty string")

        artifacts = item["primary_artifacts"]
        if not isinstance(artifacts, list) or not artifacts or not all(isinstance(value, str) and value.strip() for value in artifacts):
            errors.append(f"registry: skill '{name}' primary_artifacts must be a non-empty string list")

        if item["risk_level"] not in VALID_RISK_LEVELS:
            errors.append(f"registry: skill '{name}' risk_level must be one of {', '.join(sorted(VALID_RISK_LEVELS))}")

        for bool_key in ("has_references", "has_scripts", "featured"):
            if not isinstance(item[bool_key], bool):
                errors.append(f"registry: skill '{name}' {bool_key} must be boolean")

        skill_dir = SKILLS_DIR / name
        if skill_dir.exists():
            has_references = (skill_dir / "references").is_dir()
            has_scripts = (skill_dir / "scripts").is_dir()
            if item["has_references"] != has_references:
                errors.append(f"registry: skill '{name}' has_references does not match filesystem")
            if item["has_scripts"] != has_scripts:
                errors.append(f"registry: skill '{name}' has_scripts does not match filesystem")
            if maturity == 3 and not has_scripts:
                errors.append(f"registry: skill '{name}' maturity 3 requires a scripts directory")

    missing_registry = skill_names - registry_names
    extra_registry = registry_names - skill_names
    if missing_registry:
        errors.append(f"registry missing skill(s): {', '.join(sorted(missing_registry))}")
    if extra_registry:
        errors.append(f"registry has unknown skill(s): {', '.join(sorted(extra_registry))}")

    return errors


def validate_readme_badge(skill_dirs: list[Path]) -> list[str]:
    if not README_FILE.exists():
        return ["missing README.md"]
    text = README_FILE.read_text(encoding="utf-8")
    match = re.search(r"img\.shields\.io/badge/skills-(\d+)-", text)
    if not match:
        return ["README.md missing skills count badge"]
    badge_count = int(match.group(1))
    actual_count = len(skill_dirs)
    if badge_count != actual_count:
        return [f"README.md skills badge count {badge_count} does not match actual skill count {actual_count}"]
    return []


def main() -> int:
    if not SKILLS_DIR.exists():
        print("Missing skills/ directory", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    if not skill_dirs:
        print("No skills found", file=sys.stderr)
        return 1

    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))
    errors.extend(validate_packs(skill_dirs))
    errors.extend(validate_registry(skill_dirs))
    errors.extend(validate_readme_badge(skill_dirs))

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
