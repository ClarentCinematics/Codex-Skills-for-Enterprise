#!/usr/bin/env python3
"""Run optional advisory skill evaluations through the authenticated Codex CLI."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = ROOT / "tests" / "evals"
TRIGGERS_FILE = ROOT / "tests" / "trigger-cases.json"
SKILLS_DIR = ROOT / "skills"
RESULTS_DIR = ROOT / "eval-results"


def load_eval(skill: str) -> dict[str, object]:
    path = EVALS_DIR / f"{skill}.json"
    if not path.is_file():
        raise SystemExit(f"No featured eval definition for skill: {skill}")
    return json.loads(path.read_text(encoding="utf-8"))


def featured_skills() -> list[str]:
    return sorted(path.stem for path in EVALS_DIR.glob("*.json"))


def select_cases(skill: str, case_id: str | None) -> list[dict[str, object]]:
    cases = load_eval(skill)["cases"]
    assert isinstance(cases, list)
    selected = [case for case in cases if isinstance(case, dict) and (case_id is None or case.get("id") == case_id)]
    if case_id and not selected:
        raise SystemExit(f"Unknown case '{case_id}' for {skill}")
    return selected


def assertions(output: str, case: dict[str, object]) -> dict[str, object]:
    lower = output.lower()
    required_sections = [str(value) for value in case["required_sections"]]
    forbidden_claims = [str(value) for value in case["forbidden_claims"]]
    required_caveats = [str(value) for value in case["required_caveats"]]
    missing_sections = [value for value in required_sections if value.lower() not in lower]
    present_forbidden = [value for value in forbidden_claims if value.lower() in lower]
    missing_caveats = [value for value in required_caveats if value.lower() not in lower]
    return {
        "passed": not missing_sections and not present_forbidden and not missing_caveats,
        "missing_sections": missing_sections,
        "present_forbidden_claims": present_forbidden,
        "missing_caveats": missing_caveats,
    }


def codex_command(workspace: Path, output_file: Path, prompt: str) -> list[str]:
    return [
        "codex",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--ask-for-approval",
        "never",
        "--color",
        "never",
        "-C",
        str(workspace),
        "--output-last-message",
        str(output_file),
        prompt,
    ]


def prepare_workspace(skill: str | None, fixture: Path, include_all_skills: bool = False) -> tempfile.TemporaryDirectory[str]:
    temporary = tempfile.TemporaryDirectory(prefix="cse-codex-eval-")
    workspace = Path(temporary.name)
    shutil.copy2(fixture, workspace / "input.md")
    if include_all_skills:
        target = workspace / ".agents" / "skills"
        shutil.copytree(SKILLS_DIR, target)
    elif skill:
        target = workspace / ".agents" / "skills" / skill
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SKILLS_DIR / skill, target)
    return temporary


def run_codex(workspace: Path, prompt: str, dry_run: bool) -> dict[str, object]:
    output_file = workspace / "last-message.md"
    command = codex_command(workspace, output_file, prompt)
    if dry_run:
        return {"command": command, "duration_seconds": 0.0, "exit_code": None, "output": ""}
    started = time.monotonic()
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    duration = round(time.monotonic() - started, 3)
    output = output_file.read_text(encoding="utf-8") if output_file.exists() else completed.stdout
    return {
        "command": command,
        "duration_seconds": duration,
        "exit_code": completed.returncode,
        "output": output,
        "stderr": completed.stderr,
    }


def run_behavior_case(skill: str, case: dict[str, object], dry_run: bool) -> dict[str, object]:
    fixture = ROOT / str(case["fixture"])
    prompt = f"{case['prompt']}\n\nRead the source artifact from input.md."
    result: dict[str, object] = {"skill": skill, "case": case["id"], "category": case["category"]}

    with_skill_temp = prepare_workspace(skill, fixture)
    try:
        with_skill = run_codex(Path(with_skill_temp.name), prompt, dry_run)
    finally:
        with_skill_temp.cleanup()

    baseline_temp = prepare_workspace(None, fixture)
    try:
        baseline_task = prompt.replace(f"${skill}", "the relevant workflow")
        baseline_prompt = (
            "Complete the following task without using any installed skill. "
            "This is a baseline run for comparison.\n\n" + baseline_task
        )
        baseline = run_codex(Path(baseline_temp.name), baseline_prompt, dry_run)
    finally:
        baseline_temp.cleanup()

    if not dry_run:
        with_skill["assertions"] = assertions(str(with_skill["output"]), case)
        baseline["assertions"] = assertions(str(baseline["output"]), case)
    result["with_skill"] = with_skill
    result["baseline"] = baseline
    result["caveat"] = "User-level skills may still be visible to Codex; baseline instructions explicitly prohibit using them."
    return result


def run_trigger_cases(selected_skills: list[str], dry_run: bool) -> list[dict[str, object]]:
    trigger_data = json.loads(TRIGGERS_FILE.read_text(encoding="utf-8"))
    results: list[dict[str, object]] = []
    empty_fixture = ROOT / "tests" / "fixtures" / "meeting-intelligence" / "input.md"
    for skill in selected_skills:
        entry = trigger_data[skill]
        prompts = entry["positive"] + entry["paraphrases"] + entry["hard_negatives"]
        for index, candidate in enumerate(prompts, start=1):
            temporary = prepare_workspace(None, empty_fixture, include_all_skills=True)
            try:
                prompt = (
                    "For evaluation only, identify which installed skill best matches the request below. "
                    "Return exactly the skill name, or NONE if no skill should trigger.\n\n"
                    f"Request: {candidate}"
                )
                run = run_codex(Path(temporary.name), prompt, dry_run)
            finally:
                temporary.cleanup()
            is_positive = index <= len(entry["positive"]) + len(entry["paraphrases"])
            expected = skill if is_positive else f"not:{skill}"
            observed = str(run["output"]).strip()
            results.append(
                {
                    "skill": skill,
                    "prompt": candidate,
                    "expected": expected,
                    "observed": observed,
                    "passed": None if dry_run else (observed == skill if is_positive else observed != skill),
                    "run": run,
                }
            )
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run optional Codex CLI evaluations for enterprise skills.")
    parser.add_argument("--skill", action="append", default=[], help="Featured skill to evaluate; repeat as needed.")
    parser.add_argument("--case", help="Run one case id. Requires exactly one --skill.")
    parser.add_argument("--all-featured", action="store_true", help="Evaluate every featured skill.")
    parser.add_argument("--trigger-only", action="store_true", help="Run skill-selection prompts instead of behavioral cases.")
    parser.add_argument("--dry-run", action="store_true", help="Print the evaluation plan without invoking Codex.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.all_featured and args.skill:
        raise SystemExit("Use either --all-featured or --skill, not both.")
    selected = featured_skills() if args.all_featured else sorted(set(args.skill))
    if not selected:
        raise SystemExit("Provide --all-featured or at least one --skill.")
    if args.case and len(selected) != 1:
        raise SystemExit("--case requires exactly one --skill.")
    unknown = set(selected) - set(featured_skills())
    if unknown:
        raise SystemExit(f"Unknown or non-featured skill(s): {', '.join(sorted(unknown))}")
    if not args.dry_run and shutil.which("codex") is None:
        raise SystemExit("Codex CLI is not available on PATH.")

    if args.trigger_only:
        results: object = run_trigger_cases(selected, args.dry_run)
    else:
        results = [
            run_behavior_case(skill, case, args.dry_run)
            for skill in selected
            for case in select_cases(skill, args.case)
        ]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "trigger" if args.trigger_only else "behavioral",
        "dry_run": args.dry_run,
        "results": results,
    }
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    RESULTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"{timestamp}-{payload['mode']}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote advisory evaluation results to {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
