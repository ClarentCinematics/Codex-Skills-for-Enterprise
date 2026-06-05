# Enterprise Skill Maturity Levels

Use maturity levels to decide how much rigor a skill needs before broader adoption.

| Level | Name | Description | Evidence needed |
| --- | --- | --- | --- |
| 1 | Prompted workflow | Concise skill instructions produce a better artifact than an ad hoc prompt. | One realistic prompt and reviewed output |
| 2 | Structured reference | Skill has rubrics, output standards, or patterns in `references/`. | Multiple realistic prompts across variants |
| 3 | Script-assisted | Deterministic helper scripts reduce repeated manual parsing or validation. | Script smoke tests and skill validation |
| 4 | Tool-connected | Skill uses approved tools or exports from systems of record. | Access model, error handling, and human-review path |
| 5 | Audited pack | Skill is part of a governed pack with forward-test evidence and owner review. | Pack validation, documented owner, and recurring review |

## Current Repository Position

Most skills in this repository are Level 2: concise skills with structured reference rubrics. `ci-failure-triage`, `crm-hygiene-auditor`, and `knowledge-base-capture` are Level 3 examples because they include deterministic helper scripts plus smoke-testable script interfaces. The installer and pack metadata make pack-level adoption easier, while tool-connected adapters remain optional and deliberately separate.

## Advancement Rules

- Move to Level 3 when repeated deterministic parsing or validation is slowing users down.
- Move to Level 4 only when tool access, permissions, and failure modes are clear.
- Move to Level 5 for executive, production, customer, legal, compliance, or revenue-sensitive workflows.
