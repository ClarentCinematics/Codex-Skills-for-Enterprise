---
name: pr-review-brief
description: Turn pull request descriptions, diffs, changed files, review comments, or merge requests into reviewer-ready briefs with change summary, risk areas, missing tests, review focus, blockers, and suggested comments. Use when Codex needs to prepare, accelerate, or improve code review across PR platforms.
---

# PR Review Brief

## Workflow

1. Identify intent, changed surface area, affected users/systems, and stated rollout plan.
2. Summarize behavior changes separately from refactors, formatting, generated files, or test-only changes.
3. Inspect risk by correctness, security, data, performance, compatibility, operability, and maintainability.
4. Check whether tests, docs, migrations, rollout notes, and observability match the risk.
5. Produce a concise reviewer brief with focused questions and suggested comments.

## Output Standard

Use this structure by default:

- **Change Summary**: what changed and why.
- **Review Focus**: files, flows, or behaviors that deserve attention.
- **Risk Assessment**: severity, evidence, and potential impact.
- **Missing Coverage**: tests, docs, migrations, monitoring, or rollout gaps.
- **Merge Blockers**: issues that should block approval.
- **Suggested Comments**: concise review comments grounded in evidence.
- **Approval Readiness**: ready, ready with nits, needs changes, or unclear.

## Rules

- Do not claim a bug exists unless the evidence supports it.
- Separate blocking concerns from preferences and cleanup suggestions.
- Avoid generic review advice that does not reference the change.
- Flag security, privacy, migration, and production-risk concerns explicitly.

## References

Read `references/review-rubric.md` when the PR is large, cross-cutting, security-sensitive, or lacks tests.
