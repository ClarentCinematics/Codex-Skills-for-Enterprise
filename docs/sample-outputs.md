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
