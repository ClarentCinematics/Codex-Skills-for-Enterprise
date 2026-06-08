---
name: incident-postmortem-assistant
description: Create blameless incident postmortems from incident timelines, alert notes, status updates, chat excerpts, repair notes, or reliability summaries and produce impact, root-cause hypotheses, contributing factors, corrective actions, owners, and follow-up questions. Use when Codex needs to turn operational incident evidence into a reviewable postmortem without inventing missing facts.
---

# Incident Postmortem Assistant

## Workflow

1. Identify incident scope, affected systems, customer or business impact, timeline, responders, and available evidence.
2. Separate observed facts from hypotheses, assumptions, downstream symptoms, and missing context.
3. Build a blameless narrative with impact, detection, mitigation, resolution, and learning points.
4. Convert lessons into corrective actions with owners and due dates only when stated.
5. Flag unresolved questions, evidence gaps, repeated timestamps, ambiguous ownership, and follow-up needs.

## Script-Assisted Workflow

When given a timeline or incident notes file, run `scripts/check_incident_timeline.py --input <path>` before drafting the postmortem. Use `--json` when structured evidence is needed. Treat the script output as deterministic evidence about timeline quality, not as the final root cause.

## Output Standard

Use this structure by default:

- **Incident Summary**: scope, status, impact, and confidence.
- **Timeline**: observed events with timestamps, owners, and actions when stated.
- **Impact**: affected users, services, duration, and business effect; use `Not stated` when absent.
- **Root-Cause Hypotheses**: ranked hypotheses with evidence and uncertainty.
- **Contributing Factors**: process, system, monitoring, release, dependency, or handoff factors.
- **Corrective Actions**: action, owner, due date, and validation method when stated.
- **Open Questions**: missing facts needed before publication.
- **Caveats**: source limitations and non-inferred fields.

## Rules

- Keep the postmortem blameless and evidence-grounded.
- Do not invent severity, customer impact, owners, dates, root cause, or corrective action commitments.
- Label hypotheses as hypotheses until supported by source evidence.
- Treat unresolved timeline gaps, repeated timestamps, and missing owners as review risks.
- Escalate legal, customer-notification, or compliance conclusions to human review.

## References

Read `references/postmortem-rubric.md` when preparing a formal postmortem, executive incident recap, or corrective-action review.
