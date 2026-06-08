---
name: requirements-to-acceptance-criteria
description: Convert product requirements, feature notes, customer asks, PRD drafts, issue descriptions, or rough specifications into acceptance criteria, test scenarios, dependencies, launch constraints, owners, and open questions. Use when Codex needs to make requirements implementation-ready without inventing scope, owners, or commitments.
---

# Requirements To Acceptance Criteria

## Workflow

1. Identify product goal, users, problem, scope, non-goals, dependencies, owner, and launch constraints.
2. Extract explicit requirements and separate them from assumptions, questions, and suggested implementation details.
3. Convert requirements into testable acceptance criteria with observable behavior.
4. Add test scenarios for happy path, edge cases, permissions, errors, data states, and rollout.
5. Flag missing owners, dependencies, launch constraints, metrics, and unresolved assumptions.

## Script-Assisted Workflow

When given a Markdown spec or PRD draft, run `scripts/check_requirements_spec.py --input <path>` before drafting criteria. Use `--json` when structured readiness evidence is needed. The helper checks for missing sections and unresolved assumptions; Codex still writes the final criteria and questions.

## Output Standard

Use this structure by default:

- **Requirement Summary**: goal, user, scope, and readiness.
- **Acceptance Criteria**: numbered, testable criteria using provided facts.
- **Test Scenarios**: happy path, edge cases, error states, permissions, and rollout checks.
- **Dependencies**: systems, teams, data, designs, decisions, or approvals when stated.
- **Launch Constraints**: rollout, migration, support, documentation, metrics, or risk constraints.
- **Open Questions**: missing facts that block implementation or testing.
- **Caveats**: assumptions, non-inferred fields, and review needs.

## Rules

- Do not invent scope, owner, launch date, metric target, design approval, or customer commitment.
- Keep criteria observable and testable.
- Separate requirements from implementation suggestions unless the source requires a specific implementation.
- Mark unsupported assumptions and unresolved questions explicitly.

## References

Read `references/acceptance-rubric.md` when converting ambiguous requirements into acceptance criteria and test scenarios.
