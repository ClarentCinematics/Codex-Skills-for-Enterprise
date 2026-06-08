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

## Incident Postmortem Assistant

Use `incident-postmortem-assistant/scripts/check_incident_timeline.py` for incident timelines or response notes.

```bash
python3 skills/incident-postmortem-assistant/scripts/check_incident_timeline.py --input /tmp/incident.md
python3 skills/incident-postmortem-assistant/scripts/check_incident_timeline.py --input /tmp/incident.md --json
```

Expected input: markdown or plain text with incident events, timestamps, owners, actions, and follow-up notes when available.

Output interpretation:

- `repeated_timestamps` flags timeline entries that may need ordering review.
- `missing_owner_events` and `missing_action_events` show events that need human clarification.
- `unresolved_items` lists unresolved markers such as `tbd`, `unknown`, or follow-up placeholders.
- `readiness` is a timeline-quality signal, not a postmortem approval.

Limitations: the script does not determine root cause, severity, customer impact, or corrective-action ownership.

## Support Deflection Miner

Use `support-deflection-miner/scripts/mine_support_themes.py` for ticket subjects in CSV or text form.

```bash
python3 skills/support-deflection-miner/scripts/mine_support_themes.py --input /tmp/tickets.csv
python3 skills/support-deflection-miner/scripts/mine_support_themes.py --input /tmp/tickets.txt --json
```

Expected input: a CSV with `subject`, `title`, `summary`, `ticket_subject`, or `issue`, or a plain-text list of ticket subjects.

Output interpretation:

- `top_repeated_issues` ranks keyword-based theme clusters.
- `duplicate_looking_subjects` lists exact normalized repeats.
- `examples` provide source subjects for review.

Limitations: keyword clustering does not prove root cause, total support volume, SLA impact, or customer segment.

## Data Quality Triage

Use `data-quality-triage/scripts/audit_data_quality.py` for CSV samples.

```bash
python3 skills/data-quality-triage/scripts/audit_data_quality.py --input /tmp/sample.csv
python3 skills/data-quality-triage/scripts/audit_data_quality.py --input /tmp/sample.csv --key-fields account_id --date-fields last_updated --stale-days 30 --today 2026-06-08 --json
```

Expected input: a CSV with headers. Add key and date fields when the dataset contract is known.

Output interpretation:

- `null_rates` lists fields with blank-like values.
- `duplicate_keys` requires `--key-fields` and flags repeated keys.
- `stale_dates` flags stale or invalid date values.
- `enum_inconsistencies` surfaces casing, punctuation, or spelling variants.

Limitations: the script checks only the provided sample and does not infer missing values, metric definitions, source-of-truth status, or full warehouse impact.

## Requirements To Acceptance Criteria

Use `requirements-to-acceptance-criteria/scripts/check_requirements_spec.py` for markdown specs or PRD drafts.

```bash
python3 skills/requirements-to-acceptance-criteria/scripts/check_requirements_spec.py --input /tmp/spec.md
python3 skills/requirements-to-acceptance-criteria/scripts/check_requirements_spec.py --input /tmp/spec.md --required-sections "Acceptance Criteria,Test Scenarios,Dependencies,Owner,Launch Constraints" --json
```

Expected input: markdown with requirement, owner, dependency, acceptance, test, and launch sections when available.

Output interpretation:

- `missing_sections` identifies readiness gaps.
- `unresolved_assumptions` lists unresolved markers and assumption lines.
- `readiness` indicates whether the draft needs review before implementation planning.

Limitations: the script does not write acceptance criteria and does not invent scope, owners, dates, metrics, or launch commitments.

## Vendor Security Review

Use `vendor-security-review/scripts/check_vendor_security_answers.py` for security questionnaires, answer drafts, or vendor review packets.

```bash
python3 skills/vendor-security-review/scripts/check_vendor_security_answers.py --input /tmp/vendor-security.md
python3 skills/vendor-security-review/scripts/check_vendor_security_answers.py --input /tmp/vendor-security.md --json
```

Expected input: markdown or plain text containing vendor security, privacy, procurement, or risk-review answers.

Output interpretation:

- `coverage` shows detected evidence for SOC2, DPA, subprocessors, retention, breach notification, encryption, SSO, and audit logs.
- `missing_topics` lists absent coverage areas.
- `weak_answers` lists unresolved or noncommittal answer lines.

Limitations: the script does not approve vendors, certify compliance, accept risk, or provide legal advice.
