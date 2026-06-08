# Sample Outputs

These samples show the expected output shape for featured skills. They use fictional, sanitized inputs and are not customer artifacts.

## Meeting Intelligence

Input summary: leadership notes mention a delayed billing migration, an unresolved owner for customer messaging, and a proposed Friday decision deadline.

Expected output:

```text
Decisions:
- Billing migration moves to phased rollout. Owner: Maya. Date: Friday.

Action Items:
- Draft customer messaging for affected accounts. Owner: Not stated. Due: Not stated.
- Confirm rollback criteria before rollout. Owner: Platform lead. Due: Friday.

Risks:
- Customer messaging owner is not stated.
- Rollback criteria are unresolved.

Follow-Up Email:
Subject: Billing migration follow-ups
...
```

Must not invent: unstated customer names, dates, owners, revenue impact, or executive approval.

## CI Failure Triage

Input summary: CI log shows `npm test`, one assertion failure in `payment.test.ts`, then a generic exit-code line.

Expected output:

```text
Failure Summary: Test job failed during `npm test`.

Primary Signal:
- `AssertionError: expected status 200 actual 500`
- File signal: `payment.test.ts`

Likely Root Cause:
1. Payment endpoint behavior changed or test fixture no longer matches expected status.
2. Downstream exit-code line is noise, not the primary cause.

Reproduction Path:
- Run `npm test`.
- Narrow to `payment.test.ts` if the test runner supports file-level execution.

Caveats:
- Changed files and service ownership were not provided.
```

Must not invent: changed files, service owner, branch name, or incident severity.

## CRM Hygiene Auditor

Input summary: CRM CSV has a committed opportunity with missing owner, stale activity, and no current next step.

Expected output:

```text
Audit Summary: High hygiene risk due to missing owner and weak forecast evidence.

Critical Issues:
- Missing owner on committed opportunity.
- Last activity is older than the stale-days threshold.
- Next step is blank.

Pipeline / Forecast Risk:
- Forecast confidence is unsupported until owner and next step are confirmed.

Cleanup Actions:
- Assign an accountable owner from CRM source-of-truth.
- Confirm next customer action and close-date basis.
```

Must not invent: owner, next step, close date rationale, amount, or forecast category.

## Knowledge Base Capture

Input summary: draft SOP has audience and summary, but missing owner, stale review date, and unresolved `TBD`.

Expected output:

```text
Title: Reset Billing Sync

Audience: Support engineers

Summary: Explains how to restart a failed billing sync.

Ownership And Freshness:
- Owner: Not stated.
- Review date: stale.
- Source: Draft SOP.

Review Questions:
- Who owns this article?
- What escalation path replaces the TBD item?
```

Must not invent: owner, escalation path, approval state, or production safety guarantee.

## CAO Operating Pulse

Input summary: AI portfolio notes include three pilots, one vendor claim, a shadow-AI concern, and no confirmed ROI metrics.

Expected output:

```text
AI Weather Report: Bright demos, cloudy operating evidence.

30-Second Board Slide:
AI activity is increasing, but only one workflow has enough adoption evidence to consider scaling.

Hype-o-meter: Warm
Evidence: vendor claim is unverified; pilot usage is real but limited.

Portfolio Pulse:
- Customer support summarization: Watch.
- Finance variance explainer: Fund discovery.
- Generic email bot: Park.

Governance & Shadow AI:
- Shadow-AI usage needs policy review and approved tooling guidance.

Decisions Needed:
- Decide whether finance variance explainer gets a two-week validation sprint.
```

Must not invent: ROI, compliance approval, legal conclusion, budget, or production readiness.

## Incident Postmortem Assistant

Input summary: incident timeline has repeated `09:08` entries, a mitigation action, missing final severity, and unresolved customer-notification owner.

Expected output:

```text
Incident Summary:
Checkout latency degraded during the incident window. Final severity: Not stated.

Timeline:
- 09:04 Alert fired. Owner: Platform on-call. Action: triage started.
- 09:08 Support reported fictional merchant timeout errors. Owner: Not stated.
- 09:08 Payments lead checked dependency dashboard.
- 09:14 Fraud-score enrichment flag disabled.

Root-Cause Hypotheses:
1. Fraud-score enrichment may have contributed to checkout latency. Confidence: Medium; evidence is mitigation-correlated, not proven.

Corrective Actions:
- Confirm whether retry behavior contributed to queue growth. Owner: Not stated.

Caveats:
- Impact duration and final severity were not provided.
- Customer notification owner was not stated.
```

Must not invent: final severity, confirmed root cause, customer notification status, revenue impact, or corrective-action owners.

## Support Deflection Miner

Input summary: fictional ticket subjects repeat billing sync reset, SSO login loop, and CSV custom-field export issues.

Expected output:

```text
Deflection Summary:
Three repeated support themes appear in the provided subjects. Counts are sample-only.

Top Themes:
- Billing sync reset: repeated setup/troubleshooting issue.
- SSO login loop: repeated authentication issue.
- CSV custom fields missing: repeated export expectation issue.

KB Opportunities:
- "Restart a failed billing sync"
- "Resolve SSO login loop after password reset"
- "Export custom fields to CSV"

Caveats:
- Ticket subjects alone do not prove root cause or total support volume.
```

Must not invent: customer segment, SLA breach, full ticket volume, root cause, or product commitment.

## Data Quality Triage

Input summary: CSV sample has duplicate `account_id`, mixed `status` values, blank owners, stale dates, and an invalid date.

Expected output:

```text
Triage Summary:
High quality risk in the provided CSV sample because duplicate keys and stale/invalid dates are present.

Critical Findings:
- Duplicate key candidate: account_id `A-101`.
- Owner is blank on two rows.
- `last_updated` contains stale and invalid values.

Field-Level Evidence:
- `status` includes casing and naming variants: Active, active, Paused, Pause.

Cleanup Actions:
- Confirm dataset grain and key fields.
- Normalize status values against an approved enum.
- Re-export after source-system owner values are corrected.

Caveats:
- Findings apply only to the provided CSV sample.
```

Must not invent: source of truth, full warehouse impact, metric definition, business owner, or replacement values.

## Requirements To Acceptance Criteria

Input summary: PRD draft describes bulk invite upload but lacks acceptance criteria, test scenarios, and launch constraints.

Expected output:

```text
Requirement Summary:
Workspace admins need CSV-based user invitation. Owner is stated; launch constraints are not stated.

Acceptance Criteria:
1. Given an admin uploads a CSV with email and role columns, the system creates pending invites for valid rows.
2. Given a row has an invalid email, the system rejects that row and reports the row-level error.
3. Given a duplicate email exists in the upload, the system does not create duplicate pending invites.

Test Scenarios:
- Valid upload with multiple roles.
- Invalid email row.
- Duplicate email row.
- Missing required column.

Caveats:
- Launch date, rollout plan, metric target, and design approval were not provided.
```

Must not invent: launch date, design approval, metric target, customer commitment, or implementation architecture.

## Vendor Security Review

Input summary: vendor notes mention SOC2, encryption, SSO, and audit logs, but omit DPA and subprocessors and leave breach notification timing unresolved.

Expected output:

```text
Review Summary:
Vendor packet is not ready for approval because required privacy and notification evidence is missing.

Coverage Check:
- SOC2: Present.
- Encryption: Present.
- SSO: Present.
- Audit logs: Present.
- DPA: Missing from packet.
- Subprocessors: Missing from packet.
- Breach notification: Timing unresolved.

Risk Questions:
- Provide DPA terms for legal review.
- Provide current subprocessor list and change-notification process.
- Confirm breach-notification timing and contact path.

Human Review Required:
Security, legal, and procurement review are required before any approval or risk acceptance.
```

Must not invent: vendor approval, risk acceptance, legal conclusion, compliance certification, DPA terms, or subprocessor list.
