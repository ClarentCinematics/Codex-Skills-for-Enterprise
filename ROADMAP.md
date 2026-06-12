# Roadmap

This roadmap describes the maturity direction for Codex Skills for Enterprise. It is intentionally conservative: the repository should stay curated, validated, and useful before it becomes larger.

## Current State

- 20 skills across executive ops, engineering ops, revenue ops, knowledge ops, reliability ops, customer ops, data ops, product ops, and risk governance.
- Registry-backed catalog metadata in `skill-registry.json`.
- Generated human-readable catalog in `docs/catalog.md`.
- Level 3 helper scripts for CI triage, CRM hygiene auditing, KB metadata checks, incident timelines, support themes, data-quality triage, requirements readiness, and vendor security coverage.
- Smoke fixtures for the ten featured skills.
- Deterministic eval definitions for all featured skills and trigger cases for all 20 skills.
- Helper unit tests, capability scanning, CodeQL, OpenSSF Scorecard, and Dependabot.
- Umbrella Codex plugin and repository marketplace distribution.

## Next Maturity Targets

- Review real opt-in Codex CLI eval results and tighten assertions where wording creates false negatives.
- Expand deterministic behavioral fixtures beyond featured skills.
- Add sample inputs and outputs for every skill that becomes featured.
- Promote additional high-volume skills to Level 3 when deterministic parsing or validation would reduce repeated manual work.
- Add stronger registry checks for sample-output coverage and fixture coverage as the catalog grows.
- Add release notes for each tagged release.
- Add one approval to the `main` ruleset when a second active maintainer joins.

## Planned Pack Directions

Potential future packs:

- `ai-governance`: AI risk register, control gap review, and board AI reporting.
- `finance-ops`: budget variance, procurement intake, month-end narrative, and investment memo workflows.
- `people-ops`: hiring scorecard synthesis, onboarding knowledge capture, performance calibration briefs.
- `customer-success`: escalation briefs, QBR synthesis, renewal risk review, customer health narratives.

## Level 3 Upgrade Candidates

Potential helper scripts:

- `pr-review-brief`: changed-file and test-plan signal extraction.
- `release-notes-generator`: changelog fragment quality checks.
- `decision-memo`: decision memo completeness checks.
- `policy-impact-analysis`: obligation and action extraction from policy text.
- `cao-operating-pulse`: AI portfolio table normalization.
- `account-research-brief`: account signal extraction from sanitized research notes.
- `proposal-drafting-assistant`: proposal completeness and review-gate checks.

## Out Of Scope For Now

- Direct vendor authentication or system-of-record integrations in core skills.
- Automatic legal, compliance, financial, hiring, or customer-impacting decisions.
- Large generated catalogs of shallow skills.
- LLM-based evaluation in CI.
- API-based model evaluation or required credentials in repository CI.
- Private customer artifacts, credentials, or unsanitized logs in fixtures.

## Release Direction

- `v0.1.0`: validated enterprise skill catalog with registry, catalog generation, smoke fixtures, and MIT license.
- `v0.2.0`: plugin distribution, trust metadata, deterministic evals, helper unit tests, capability scanning, CodeQL, Scorecard, and protected release workflow.
- Future releases should tag meaningful changes to skill count, maturity level, validation tooling, or adoption documentation.
