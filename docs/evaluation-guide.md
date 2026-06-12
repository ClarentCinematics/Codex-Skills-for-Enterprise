# Evaluation Guide

The repository separates deterministic release gates from optional model-assisted comparisons.

## Deterministic Gates

Run these before opening a pull request:

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_evals.py
python3 scripts/scan_skill_security.py
python3 tests/run_smoke_tests.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

These commands validate:

- registry, packs, catalog, plugin, marketplace, and skill structure;
- smoke fixture completeness for featured skills;
- three eval cases for each featured skill;
- positive, paraphrased, hard-negative, and collision cases for every skill;
- helper human and JSON interfaces, deterministic output, empty inputs, malformed paths, and redaction;
- undeclared network, process, dynamic execution, credential, destructive, and filesystem-write capabilities.

No deterministic gate calls a model or external service.

## Eval Cases

Each featured skill has a file under `tests/evals/` with:

- one representative case;
- one incomplete-evidence case;
- one unsupported-claim case;
- a fictional fixture path;
- required output sections;
- forbidden unsupported claims;
- required caveat markers.

These assertions are intentionally strict and advisory for live model output. A missing phrase can indicate wording drift rather than a behavioral failure, so a maintainer must review live results.

## Optional Codex CLI Comparison

The optional runner uses the existing authenticated Codex CLI. It never reads an API key and is not part of CI.

Preview commands without invoking Codex:

```bash
python3 scripts/run_codex_evals.py --dry-run --all-featured
python3 scripts/run_codex_evals.py --dry-run --skill ci-failure-triage --case failed-test-log
python3 scripts/run_codex_evals.py --dry-run --skill ci-failure-triage --trigger-only
```

Run advisory comparisons:

```bash
python3 scripts/run_codex_evals.py --all-featured
python3 scripts/run_codex_evals.py --skill ci-failure-triage
```

Behavioral mode runs each case with the repository skill present and as a baseline with explicit instructions not to use installed skills. Trigger mode loads all repository skills and asks Codex to identify the best match.

Results are written to ignored `eval-results/` JSON files with output, duration, exit status, and assertion results. User-level skills may still be visible to Codex, so baseline comparisons are directional evidence rather than isolated scientific benchmarks.

## Updating Coverage

- Update trigger cases whenever a skill description changes.
- Update featured evals and sample outputs whenever behavior changes.
- Keep fixtures fictional and free of credentials, customer data, or private logs.
- Promote a non-featured skill from `trigger-only` to `behavioral-fixtures` only after adding its smoke fixture and three eval cases.
