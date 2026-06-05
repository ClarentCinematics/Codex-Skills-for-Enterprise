# Enterprise Skill Examples

These examples document realistic use cases for the starter skills. They live at the repo level so individual skill folders stay lean.

## Meeting Intelligence

Prompt:

```text
Use $meeting-intelligence to turn this leadership meeting transcript into decisions, action items, risks, and a follow-up email.
```

Validation focus:

- decisions are not invented;
- owners and dates are marked `Not stated` when missing;
- risks are separated from general discussion;
- follow-up is concise and stakeholder-ready.

## Weekly Executive Report

Prompt:

```text
Use $weekly-executive-report to synthesize these product, sales, operations, and finance updates into a weekly executive report.
```

Validation focus:

- activity is translated into business impact;
- incomplete metrics are caveated;
- decisions needed are explicit;
- report can be scanned in under five minutes.

## Decision Memo

Prompt:

```text
Use $decision-memo to frame whether we should build an internal automation intake platform or start with manual workflow audits.
```

Validation focus:

- options are viable and distinct;
- assumptions are labeled;
- recommendation is clear;
- implementation implications are practical.

## Project Status Brief

Prompt:

```text
Use $project-status-brief to turn these launch notes into a RAG status brief for the operating review.
```

Validation focus:

- health status follows evidence;
- blockers and dependencies are actionable;
- escalation asks are specific;
- vague updates become outcome-focused.

## Automation Opportunity Map

### Generic operating workflow

Prompt:

```text
Use $automation-opportunity-map to evaluate this monthly reporting workflow and recommend the first automations to build.
```

Validation focus:

- opportunities are classified correctly;
- privacy and human-review needs are flagged;
- quick wins are narrow and measurable;
- roadmap has a practical first experiment.

### Field-services discovery notes (sanitized fixture)

Use this when testing whether the skill generalizes beyond corporate back-office workflows.

Prompt:

```text
Use $automation-opportunity-map to map automation opportunities from these discovery notes. Prioritize quick wins, flag integration unknowns, and recommend a first experiment.
```

Sample input (sanitized; no customer-identifying details):

```text
Company: Two related field-service businesses (plumbing + electrical), often sold together. ~25 staff, ~EUR 2M revenue, B2B-heavy (municipal and institutional clients). Peak season in summer. Owner handles dispatch one office day per week; otherwise on site.

Stack: Industry ERP for quotes/invoices (mobile app), photo documentation app, personal Outlook calendar, WhatsApp for crew dispatch. No formal CRM.

Workflow A — collections / cash application (strongest pain):
Owner receives aged receivables lists from accountant 1–2 months late. Should reconcile against bank statement and send payment reminders; admits he does not do this consistently. Uses a regional bank; conversation suggested read-only payment feed may exist — not verified. Owner reacted strongly to automated friendly payment reminders.

Workflow B — purchase order intake:
B2B clients email PDF purchase orders. Owner reads PDF, creates job in ERP, adds Outlook calendar entry, assigns crew via WhatsApp. High frequency; core revenue path.

Workflow C — field ticket to invoice prep:
Crew returns handwritten field tickets (some customer-mandated forms). Owner reviews and manually creates ~500 invoices/year in ERP. Owner likes photo → structured draft concept; full automation depends on ERP API — unknown.

Workflow D — supplier price compare (lower priority):
Manual price checks skipped on small orders; interested in automated supplier quotes. Large inventory on hand; owner skeptical of inventory automation scope.

Explicitly out of scope per owner: phone AI for inbound calls (wants personal reachability for key accounts); generic email auto-replies (communications are case-specific); route optimization (owner tracks crews informally).

Open questions before scoping: ERP API availability; bank read access for payments; monthly PO volume; sample PDFs for extraction test; whether both business units are in scope; supplier systems/APIs; budget — not stated.
```

Validation focus:

- ranks opportunities by stated pain and frequency, not by novelty;
- classifies each candidate (skill, script, integration, process redesign) without assuming unverified APIs;
- marks bank feed, ERP API, and OCR feasibility as `unknown` or `requires validation` when not confirmed;
- excludes owner-rejected ideas (phone AI, generic email bots, route planning) from the roadmap;
- proposes a narrow first experiment (e.g., collections reminders) with success measures tied to cash flow or time saved;
- surfaces open questions as blockers for later packages, not as invented answers.
