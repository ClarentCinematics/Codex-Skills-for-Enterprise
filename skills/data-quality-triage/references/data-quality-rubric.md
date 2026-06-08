# Data Quality Rubric

Use this rubric to keep data-quality triage focused on evidence.

## Common Findings

- Missing values in required fields.
- Duplicate keys at the stated dataset grain.
- Stale date fields relative to the expected refresh cadence.
- Inconsistent enum values such as casing, spelling, punctuation, or deprecated categories.
- Schema gaps where required fields are absent from the sample.

## Priority Guidance

- High: duplicate business keys, missing required identifiers, stale operational dates, or fields used by executive metrics.
- Medium: inconsistent categories, moderate null rates, unclear grain, or missing owner context.
- Low: cosmetic field naming issues or low-volume gaps with no stated downstream consumer.

## Safe Language

- Use `Not stated` when grain, owner, source, or metric definition is missing.
- Say "sample shows" instead of generalizing to the full warehouse.
- Do not infer business meaning from field names alone.
