---
name: vendor-security-review
description: Review vendor security questionnaires, procurement security notes, SOC2 summaries, DPA excerpts, subprocessor lists, security answer drafts, or risk-review packets for missing coverage, weak evidence, follow-up questions, and human-review risks. Use when Codex needs to prepare a vendor security review without making legal, compliance, or approval decisions.
---

# Vendor Security Review

## Workflow

1. Identify vendor, product, data involved, intended use, review stage, and source documents.
2. Check coverage for security, privacy, data handling, access control, auditability, and contractual evidence.
3. Separate supplied evidence from vendor claims, assumptions, missing answers, and review questions.
4. Flag gaps, weak answers, risks, and required human review.
5. Produce a concise review packet for security, legal, procurement, or business owners.

## Script-Assisted Workflow

When given a questionnaire or answer draft, run `scripts/check_vendor_security_answers.py --input <path>` first. Use `--json` for structured coverage output. The helper detects missing topic coverage and weak answers; it does not approve vendors or provide legal/security certification.

## Output Standard

Use this structure by default:

- **Review Summary**: vendor, product, intended use, data sensitivity, and readiness.
- **Coverage Check**: SOC2, DPA, subprocessors, retention, breach notification, encryption, SSO, and audit logs.
- **Evidence Gaps**: missing or weak answers with source excerpts.
- **Risk Questions**: security, privacy, legal, procurement, and business-owner follow-ups.
- **Recommended Next Steps**: review actions and owners when stated.
- **Human Review Required**: approvals, exceptions, legal terms, or risk acceptance.
- **Caveats**: non-inferred approvals and source limitations.

## Rules

- Do not approve vendors, accept risk, provide legal advice, or certify compliance.
- Do not invent SOC2 status, DPA terms, subprocessors, encryption controls, SSO support, or breach-notification terms.
- Mark missing answers as missing, not failed, unless the source explicitly says a control is absent.
- Treat customer, employee, health, financial, or regulated data as requiring human review.

## References

Read `references/vendor-security-rubric.md` when preparing security, privacy, procurement, or legal follow-up questions.
