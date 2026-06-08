# Roadmap

This roadmap describes the maturity direction for Codex Skills for Enterprise. It is intentionally conservative: the repository should stay curated, validated, and useful before it becomes larger.

## Current State

- 20 skills across executive ops, engineering ops, revenue ops, knowledge ops, reliability ops, customer ops, data ops, product ops, and risk governance.
- Registry-backed catalog metadata in `skill-registry.json`.
- Generated human-readable catalog in `docs/catalog.md`.
- Level 3 helper scripts for CI triage, CRM hygiene auditing, KB metadata checks, incident timelines, support themes, data-quality triage, requirements readiness, and vendor security coverage.
- Smoke fixtures for the ten featured skills.
- CI validation for skill structure, registry consistency, smoke fixtures, and Python syntax.

## Next Maturity Targets

- Expand deterministic smoke fixtures beyond featured skills.
- Add sample inputs and outputs for every skill that becomes featured.
- Promote additional high-volume skills to Level 3 when deterministic parsing or validation would reduce repeated manual work.
- Add stronger registry checks for sample-output coverage and fixture coverage as the catalog grows.
- Add release notes for each tagged release.

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
- Private customer artifacts, credentials, or unsanitized logs in fixtures.

## Release Direction

- `v0.1.0`: validated enterprise skill catalog with registry, catalog generation, smoke fixtures, and MIT license.
- Next release candidate: expanded Level 3 workflow catalog with 20 skills, 10 featured smoke fixtures, and five new operating packs.
- Future releases should tag meaningful changes to skill count, maturity level, validation tooling, or adoption documentation.
