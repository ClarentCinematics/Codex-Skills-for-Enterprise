---
name: crm-hygiene-auditor
description: Audit CRM records, opportunity notes, account fields, pipeline exports, forecast inputs, or sales activity summaries for missing, stale, duplicate, inconsistent, or risky data. Use when Codex needs to improve CRM quality, pipeline hygiene, forecast confidence, or account ownership clarity.
---

# CRM Hygiene Auditor

## Workflow

1. Identify record type, sales process stage, required fields, source date, and business purpose.
2. Detect missing, stale, conflicting, duplicate, vague, or low-confidence fields.
3. Assess business impact on forecast quality, handoffs, customer experience, and leadership reporting.
4. Recommend concrete updates, owner actions, validation steps, and follow-up questions.
5. Produce a prioritized hygiene report that can be used by sales ops, managers, or account owners.

## Script-Assisted Workflow

When given a CRM CSV export, run `scripts/audit_crm_csv.py --input <csv>` before writing the audit. Adjust `--required-fields`, `--date-field`, `--stale-days`, and `--today` when the sales process defines different hygiene rules. Use `--json` for structured evidence. Do not let the script infer missing CRM values; use it to surface records that need human review.

## Output Standard

Use this structure by default:

- **Audit Summary**: record set, scope, and overall hygiene risk.
- **Critical Issues**: gaps that affect forecast, ownership, compliance, or customer commitments.
- **Field-Level Findings**: field, issue, evidence, recommended update, owner.
- **Pipeline / Forecast Risk**: risk, affected deal/account, and confidence impact.
- **Cleanup Actions**: prioritized tasks with owners and due dates when stated.
- **Questions To Resolve**: missing context that requires human input.

## Rules

- Do not invent CRM values, next steps, close dates, stakeholders, or amounts.
- Mark inferred issues as inference and preserve source uncertainty.
- Flag stale next steps, missing decision criteria, unclear owners, and unsupported forecast confidence.
- Treat customer-sensitive and revenue-sensitive data as requiring human review.

## References

Read `references/hygiene-rubric.md` when auditing pipeline exports, opportunity records, duplicate risks, or forecast readiness.
