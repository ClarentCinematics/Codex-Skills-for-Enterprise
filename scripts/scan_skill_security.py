#!/usr/bin/env python3
"""Scan helper scripts for undeclared security-sensitive capabilities."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "skill-registry.json"
SKILLS_DIR = ROOT / "skills"
NETWORK_MODULES = {"ftplib", "http", "requests", "socket", "urllib", "webbrowser"}
PROCESS_MODULES = {"subprocess"}
PROCESS_CALLS = {"system", "popen", "spawnl", "spawnlp", "spawnv", "spawnvp"}
DYNAMIC_CALLS = {"eval", "exec", "compile", "__import__"}
DESTRUCTIVE_CALLS = {"rmtree", "remove", "unlink", "rmdir"}
WRITE_METHODS = {"write_text", "write_bytes", "touch", "mkdir", "rename", "replace"}
WRITE_OPEN_MODES = {"w", "a", "x", "+"}


def load_registry() -> tuple[dict[str, dict[str, object]], list[str]]:
    try:
        data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return {}, [f"cannot load skill-registry.json: {exc}"]
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        return {}, ["skill-registry.json must contain a skills list"]
    return {
        item["name"]: item
        for item in data["skills"]
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }, []


def call_name(node: ast.Call) -> tuple[str, bool]:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id, True
    if isinstance(func, ast.Attribute):
        return func.attr, False
    return "", False


def open_mode(node: ast.Call, is_bare: bool) -> str:
    position = 1 if is_bare else 0
    if len(node.args) > position and isinstance(node.args[position], ast.Constant) and isinstance(node.args[position].value, str):
        return node.args[position].value
    for keyword in node.keywords:
        if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
            return keyword.value.value
    return "r"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scan_script(path: Path, metadata: dict[str, object]) -> list[str]:
    errors: list[str] = []
    label = display_path(path)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [f"{label}: invalid Python: {exc}"]

    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".", 1)[0])

    network = sorted(imported & NETWORK_MODULES)
    process = sorted(imported & PROCESS_MODULES)
    if network and metadata.get("network_access") != "declared":
        errors.append(f"{label}: undeclared network module(s): {', '.join(network)}")
    if process:
        errors.append(f"{label}: subprocess execution is not allowed")

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name, is_bare = call_name(node)
        if is_bare and name in DYNAMIC_CALLS:
            errors.append(f"{label}:{node.lineno}: dynamic execution via {name} is not allowed")
        if name in PROCESS_CALLS:
            errors.append(f"{label}:{node.lineno}: process execution via {name} is not allowed")
        if name in DESTRUCTIVE_CALLS:
            errors.append(f"{label}:{node.lineno}: destructive filesystem call {name} is not allowed")
        if name in WRITE_METHODS and metadata.get("filesystem_effects") != "writes-output":
            errors.append(f"{label}:{node.lineno}: undeclared filesystem write via {name}")
        if name == "open" and any(marker in open_mode(node, is_bare) for marker in WRITE_OPEN_MODES):
            if metadata.get("filesystem_effects") != "writes-output":
                errors.append(f"{label}:{node.lineno}: undeclared writable open mode")
        if name in {"getenv", "environ"}:
            errors.append(f"{label}:{node.lineno}: credential/environment access is not allowed in skill helpers")
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "environ":
            errors.append(f"{label}:{node.lineno}: credential/environment access is not allowed in skill helpers")
    return errors


def main() -> int:
    registry, errors = load_registry()
    for script in sorted(SKILLS_DIR.glob("*/scripts/*.py")):
        metadata = registry.get(script.parents[1].name)
        if metadata is None:
            errors.append(f"{script.relative_to(ROOT)}: skill is missing registry metadata")
            continue
        errors.extend(scan_script(script, metadata))

    if errors:
        print("Skill security scan failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Security-scanned {len(list(SKILLS_DIR.glob('*/scripts/*.py')))} helper scripts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
