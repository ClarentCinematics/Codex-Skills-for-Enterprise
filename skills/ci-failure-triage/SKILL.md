---
name: ci-failure-triage
description: Diagnose failed CI runs, build logs, test output, deployment checks, or pipeline summaries and produce a root-cause hypothesis, reproduction path, likely owner, fix plan, and escalation guidance. Use when Codex needs to triage broken builds, flaky tests, failed checks, or release-blocking automation failures.
---

# CI Failure Triage

## Workflow

1. Identify the failing system, job, step, command, test, environment, and recent change context.
2. Separate primary failure signals from downstream noise, retries, warnings, and unrelated log output.
3. Form a ranked root-cause hypothesis using the smallest reliable evidence set.
4. Map the failure to likely ownership by component, file path, service, team, or changed area when available.
5. Produce a practical fix path with reproduction steps, investigation commands, and escalation needs.

## Script-Assisted Workflow

When given a long raw CI log, run `scripts/extract_ci_signal.py --input <log>` first to extract the primary failure candidate, likely failure class, detected commands/tests, context, and caveats. Use `--json` when another tool or report needs structured output. Treat the script output as evidence for triage, not as a final root-cause decision.

## Output Standard

Use this structure by default:

- **Failure Summary**: system, job, step, and business impact.
- **Primary Signal**: exact failing command, test, assertion, error, or status.
- **Likely Root Cause**: ranked hypotheses with evidence and confidence.
- **Likely Owner**: component, team, or file area; use `Not stated` if unclear.
- **Reproduction Path**: local or CI reproduction steps from provided material.
- **Fix Path**: concrete next actions and validation checks.
- **Escalation**: release risk, infrastructure dependency, or human decision needed.

## Rules

- Do not treat the last log line as root cause without supporting evidence.
- Mark missing context explicitly instead of inventing branch names, owners, or commands.
- Flag flaky-test, environment, dependency, and secret/config possibilities separately.
- Prefer fast unblock steps when production, release, or merge flow is blocked.

## References

Read `references/triage-patterns.md` when the failure involves noisy logs, flaky tests, infrastructure failures, or release-blocking checks.
