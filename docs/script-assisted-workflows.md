# Script-Assisted Workflows

Level 3 skills add deterministic helper scripts for repeated extraction or validation work. Scripts are advisory: they prepare evidence, while the skill workflow still makes the final judgment.

## CI Failure Triage

Use `ci-failure-triage/scripts/extract_ci_signal.py` for long or noisy CI logs.

```bash
python3 skills/ci-failure-triage/scripts/extract_ci_signal.py --input /tmp/ci.log
python3 skills/ci-failure-triage/scripts/extract_ci_signal.py --input /tmp/ci.log --context-lines 5 --json
cat /tmp/ci.log | python3 skills/ci-failure-triage/scripts/extract_ci_signal.py --json
```

Expected input: raw CI, build, test, or deploy log text.

Output interpretation:

- `primary_failure_signal` is the first high-confidence failure-like line with surrounding context.
- `likely_failure_class` is a heuristic class such as test, compile, dependency, configuration, infrastructure, or command.
- `commands_detected` and `tests_detected` help build the reproduction path.
- `caveats` list missing or ambiguous evidence.

Limitations: the script does not prove root cause, cannot know ownership, and may still surface downstream failures when the primary error is not represented by a known pattern. It redacts obvious secret-like values before output, but users should still avoid sharing sensitive logs unnecessarily.

## CRM Hygiene Auditor

Use `crm-hygiene-auditor/scripts/audit_crm_csv.py` for exported opportunity or account CSVs.

```bash
python3 skills/crm-hygiene-auditor/scripts/audit_crm_csv.py --input /tmp/pipeline.csv
python3 skills/crm-hygiene-auditor/scripts/audit_crm_csv.py --input /tmp/pipeline.csv --required-fields owner,stage,next_step,close_date --date-field last_activity_date --stale-days 14 --today 2026-06-05 --json
```

Expected input: a CSV with headers. Common useful fields include `owner`, `stage`, `next_step`, `close_date`, `last_activity_date`, `forecast_category`, `probability`, `account`, and `amount`.

Output interpretation:

- `missing_fields` separates missing export columns from records with blank required values.
- `stale_next_steps` flags records whose activity date is older than the configured threshold.
- `unsupported_forecast_risks` flags committed or high-probability records with weak evidence fields.
- `duplicate_looking_records` lists deterministic duplicate candidates based on normalized account, close date, and amount.
- `cleanup_actions` converts findings into sales-ops review steps.

Limitations: the script does not connect to Salesforce, HubSpot, or another CRM. It does not infer missing owners, dates, amounts, stages, or next steps.

## Knowledge Base Capture

Use `knowledge-base-capture/scripts/check_kb_metadata.py` for markdown KB drafts before publishing.

```bash
python3 skills/knowledge-base-capture/scripts/check_kb_metadata.py --input /tmp/kb-draft.md
python3 skills/knowledge-base-capture/scripts/check_kb_metadata.py --input /tmp/kb-draft.md --required-sections Title,Audience,Summary,Owner --today 2026-06-05 --json
```

Expected input: a markdown article with headings and/or simple metadata lines such as `Owner:`, `Audience:`, `Summary:`, and `Review Date:`.

Output interpretation:

- `missing_metadata` and `missing_sections` show structural publishing gaps.
- `stale_review_date` is present when the review date is missing, unparsable, or before the configured date.
- `unresolved_assumptions` lists lines with unresolved markers or assumptions.
- `owner_gaps` identifies missing or non-publishable ownership.
- `publishing_readiness` is `ready` only when no blocking metadata or unresolved-content signal is found.

Limitations: the script does not rewrite the article, verify factual accuracy, or decide whether sensitive content is appropriate to publish.
