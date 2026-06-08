---
name: data-quality-triage
description: Review CSV exports, dataset samples, schema notes, metric inputs, or dashboard source data for null rates, duplicate keys, stale dates, inconsistent enum values, schema gaps, and quality caveats. Use when Codex needs to turn data-quality evidence into a triage report without inventing missing values or metric definitions.
---

# Data Quality Triage

## Workflow

1. Identify dataset purpose, grain, source date, key fields, date fields, and business use.
2. Detect missing values, duplicate records, stale dates, inconsistent categories, and schema gaps.
3. Separate deterministic data-quality findings from metric interpretation or business conclusions.
4. Prioritize risks by downstream impact on reporting, operations, decisions, and automation.
5. Recommend cleanup actions, source-system checks, and owner questions.

## Script-Assisted Workflow

When given a CSV sample, run `scripts/audit_data_quality.py --input <csv>` before writing the triage. Add `--key-fields`, `--date-fields`, `--stale-days`, and `--today` when the dataset contract is known. Use `--json` for structured evidence. Do not let the helper infer missing values, metric definitions, or business truth.

## Output Standard

Use this structure by default:

- **Triage Summary**: dataset, scope, row count, and overall quality risk.
- **Critical Findings**: duplicate keys, high-null fields, stale dates, schema blockers, or enum conflicts.
- **Field-Level Evidence**: field, issue, examples, and affected count or rate.
- **Downstream Risk**: dashboard, metric, workflow, or decision impact.
- **Cleanup Actions**: source-system checks, owner actions, and validation queries.
- **Questions To Resolve**: missing grain, key, owner, metric definition, or freshness context.
- **Caveats**: sample limitations and non-inferred fields.

## Rules

- Do not invent missing values, metric definitions, row ownership, or source-of-truth status.
- Mark sample-based findings as sample-based.
- Treat high-impact reporting, finance, customer, or compliance data as requiring human review.
- Prefer deterministic checks before narrative interpretation.

## References

Read `references/data-quality-rubric.md` when prioritizing findings or mapping data-quality risks to reporting, automation, or operational impact.
