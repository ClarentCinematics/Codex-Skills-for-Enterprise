# Postmortem Rubric

Use this rubric to keep incident reviews useful, factual, and blameless.

## Evidence To Preserve

- Detection source: alert, customer report, synthetic check, internal user, or deploy signal.
- Timeline: first signal, triage, mitigation, resolution, and verification.
- Impact: service, users, regions, data, revenue, SLA, or internal workflow effect.
- Response: responders, decisions, attempted fixes, rollback or mitigation steps.
- Follow-up: corrective actions, owners, validation method, and review date.

## Review Risks

- Timeline entries with repeated timestamps that may collapse distinct events.
- Actions without owners or owners without stated actions.
- Root-cause statements that are not supported by evidence.
- Corrective actions without validation checks.
- Customer-impact claims without source evidence.

## Safe Language

- Use "hypothesis" when root cause is not proven.
- Use `Not stated` for missing owners, impact, dates, or severity.
- Use "requires human review" for customer notification, legal, compliance, or contractual conclusions.
