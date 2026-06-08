# Skill Catalog

This catalog is generated from `skill-registry.json`. Do not edit it by hand; run `python3 scripts/generate_catalog.py` after registry changes.

| Skill | Pack | Maturity | Audience | Scripts | Fixtures | Risk | Featured |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`ci-failure-triage`](../skills/ci-failure-triage/SKILL.md) | `engineering-ops` | Level 3 | Engineering and platform teams | Yes | Yes | Medium | Yes |
| [`pr-review-brief`](../skills/pr-review-brief/SKILL.md) | `engineering-ops` | Level 2 | Engineering teams | No | No | Medium | No |
| [`release-notes-generator`](../skills/release-notes-generator/SKILL.md) | `engineering-ops` | Level 2 | Product and engineering teams | No | No | Medium | No |
| [`automation-opportunity-map`](../skills/automation-opportunity-map/SKILL.md) | `executive-ops` | Level 2 | Operations and transformation teams | No | No | Medium | No |
| [`cao-operating-pulse`](../skills/cao-operating-pulse/SKILL.md) | `executive-ops` | Level 2 | Chief AI Officers and AI operating teams | No | Yes | High | Yes |
| [`decision-memo`](../skills/decision-memo/SKILL.md) | `executive-ops` | Level 2 | Leadership and strategy teams | No | No | Medium | No |
| [`meeting-intelligence`](../skills/meeting-intelligence/SKILL.md) | `executive-ops` | Level 2 | Executives, operators, and project leaders | No | Yes | Medium | Yes |
| [`project-status-brief`](../skills/project-status-brief/SKILL.md) | `executive-ops` | Level 2 | Program and project leaders | No | No | Medium | No |
| [`weekly-executive-report`](../skills/weekly-executive-report/SKILL.md) | `executive-ops` | Level 2 | Executive and operating teams | No | No | Medium | No |
| [`knowledge-base-capture`](../skills/knowledge-base-capture/SKILL.md) | `knowledge-ops` | Level 3 | Knowledge, support, and operations teams | Yes | Yes | Medium | Yes |
| [`policy-impact-analysis`](../skills/policy-impact-analysis/SKILL.md) | `knowledge-ops` | Level 2 | Policy, compliance, and operations teams | No | No | High | No |
| [`research-synthesis-brief`](../skills/research-synthesis-brief/SKILL.md) | `knowledge-ops` | Level 2 | Strategy and research teams | No | No | Medium | No |
| [`account-research-brief`](../skills/account-research-brief/SKILL.md) | `revenue-ops` | Level 2 | Sales and revenue teams | No | No | Medium | No |
| [`crm-hygiene-auditor`](../skills/crm-hygiene-auditor/SKILL.md) | `revenue-ops` | Level 3 | Revenue operations and sales managers | Yes | Yes | High | Yes |
| [`proposal-drafting-assistant`](../skills/proposal-drafting-assistant/SKILL.md) | `revenue-ops` | Level 2 | Sales and customer teams | No | No | High | No |

## Maintenance

- Update `skill-registry.json` when a skill changes pack, maturity, risk level, audience, fixture status, or featured status.
- Run `python3 scripts/generate_catalog.py` after registry changes.
- Run `python3 scripts/validate_skills.py` to confirm this file is current.
