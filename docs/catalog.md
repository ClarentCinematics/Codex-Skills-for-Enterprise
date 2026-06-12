# Skill Catalog

This catalog is generated from `skill-registry.json`. Do not edit it by hand; run `python3 scripts/generate_catalog.py` after registry changes.

| Skill | Pack | Maturity | Audience | Scripts | Fixtures | Risk | Human Review | Evaluation | Featured |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`support-deflection-miner`](../skills/support-deflection-miner/SKILL.md) | `customer-ops` | Level 3 | Support, customer success, and knowledge teams | Yes | Yes | Medium | Recommended | Behavioral Fixtures | Yes |
| [`data-quality-triage`](../skills/data-quality-triage/SKILL.md) | `data-ops` | Level 3 | Data, analytics, and operations teams | Yes | Yes | High | Required | Behavioral Fixtures | Yes |
| [`ci-failure-triage`](../skills/ci-failure-triage/SKILL.md) | `engineering-ops` | Level 3 | Engineering and platform teams | Yes | Yes | Medium | Recommended | Behavioral Fixtures | Yes |
| [`pr-review-brief`](../skills/pr-review-brief/SKILL.md) | `engineering-ops` | Level 2 | Engineering teams | No | No | Medium | Recommended | Trigger Only | No |
| [`release-notes-generator`](../skills/release-notes-generator/SKILL.md) | `engineering-ops` | Level 2 | Product and engineering teams | No | No | Medium | Recommended | Trigger Only | No |
| [`automation-opportunity-map`](../skills/automation-opportunity-map/SKILL.md) | `executive-ops` | Level 2 | Operations and transformation teams | No | No | Medium | Recommended | Trigger Only | No |
| [`cao-operating-pulse`](../skills/cao-operating-pulse/SKILL.md) | `executive-ops` | Level 2 | Chief AI Officers and AI operating teams | No | Yes | High | Required | Behavioral Fixtures | Yes |
| [`decision-memo`](../skills/decision-memo/SKILL.md) | `executive-ops` | Level 2 | Leadership and strategy teams | No | No | Medium | Recommended | Trigger Only | No |
| [`meeting-intelligence`](../skills/meeting-intelligence/SKILL.md) | `executive-ops` | Level 2 | Executives, operators, and project leaders | No | Yes | Medium | Recommended | Behavioral Fixtures | Yes |
| [`project-status-brief`](../skills/project-status-brief/SKILL.md) | `executive-ops` | Level 2 | Program and project leaders | No | No | Medium | Recommended | Trigger Only | No |
| [`weekly-executive-report`](../skills/weekly-executive-report/SKILL.md) | `executive-ops` | Level 2 | Executive and operating teams | No | No | Medium | Recommended | Trigger Only | No |
| [`knowledge-base-capture`](../skills/knowledge-base-capture/SKILL.md) | `knowledge-ops` | Level 3 | Knowledge, support, and operations teams | Yes | Yes | Medium | Recommended | Behavioral Fixtures | Yes |
| [`policy-impact-analysis`](../skills/policy-impact-analysis/SKILL.md) | `knowledge-ops` | Level 2 | Policy, compliance, and operations teams | No | No | High | Required | Trigger Only | No |
| [`research-synthesis-brief`](../skills/research-synthesis-brief/SKILL.md) | `knowledge-ops` | Level 2 | Strategy and research teams | No | No | Medium | Recommended | Trigger Only | No |
| [`requirements-to-acceptance-criteria`](../skills/requirements-to-acceptance-criteria/SKILL.md) | `product-ops` | Level 3 | Product managers and engineering teams | Yes | Yes | Medium | Recommended | Behavioral Fixtures | Yes |
| [`incident-postmortem-assistant`](../skills/incident-postmortem-assistant/SKILL.md) | `reliability-ops` | Level 3 | Engineering, SRE, and incident response teams | Yes | Yes | High | Required | Behavioral Fixtures | Yes |
| [`account-research-brief`](../skills/account-research-brief/SKILL.md) | `revenue-ops` | Level 2 | Sales and revenue teams | No | No | Medium | Recommended | Trigger Only | No |
| [`crm-hygiene-auditor`](../skills/crm-hygiene-auditor/SKILL.md) | `revenue-ops` | Level 3 | Revenue operations and sales managers | Yes | Yes | High | Required | Behavioral Fixtures | Yes |
| [`proposal-drafting-assistant`](../skills/proposal-drafting-assistant/SKILL.md) | `revenue-ops` | Level 2 | Sales and customer teams | No | No | High | Required | Trigger Only | No |
| [`vendor-security-review`](../skills/vendor-security-review/SKILL.md) | `risk-governance` | Level 3 | Security, legal, procurement, and risk teams | Yes | Yes | High | Required | Behavioral Fixtures | Yes |

## Maintenance

- Update `skill-registry.json` when skill trust, maturity, pack, audience, fixture, or featured metadata changes.
- Run `python3 scripts/generate_catalog.py` after registry changes.
- Run `python3 scripts/validate_skills.py` to confirm this file is current.
