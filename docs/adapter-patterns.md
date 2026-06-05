# Light Adapter Patterns

Adapters should make skills easier to use with real artifacts while keeping the core skills tool-agnostic.

## Principles

- Keep `SKILL.md` independent of specific vendors.
- Prefer exported artifacts, logs, CSVs, diffs, and markdown over direct tool coupling at first.
- Add scripts only when they perform deterministic extraction, filtering, or validation.
- Keep credentials, tokens, customer data, and private system details out of the repo.

## Engineering Ops

Useful adapter inputs:

- CI log excerpts;
- failed job summaries;
- PR descriptions and changed-file lists;
- commit ranges and ticket summaries.

Level 3 example:

- `ci-failure-triage/scripts/extract_ci_signal.py` extracts the first high-confidence failure signal, likely failure class, context, detected commands/tests, and caveats from exported CI logs.

Possible future scripts:

- summarize changed files by extension and directory;
- normalize commit messages into release-note buckets.

## Revenue Ops

Useful adapter inputs:

- CRM CSV exports;
- opportunity notes;
- account research excerpts;
- discovery notes and proposal constraints.

Level 3 example:

- `crm-hygiene-auditor/scripts/audit_crm_csv.py` audits exported CRM CSVs for missing required values, stale activity, weak forecast evidence, and duplicate-looking records.

Possible future scripts:

- normalize account research sources into evidence labels.

## Knowledge Ops

Useful adapter inputs:

- document exports;
- meeting notes;
- support threads;
- policy text;
- source excerpts with dates and authors.

Level 3 example:

- `knowledge-base-capture/scripts/check_kb_metadata.py` checks markdown KB drafts for metadata completeness, stale review dates, unresolved assumptions, owner gaps, and publishing readiness.

Possible future scripts:

- split source bundles into cited excerpts;

## Adapter Readiness Checklist

- Artifact input is clear and repeatable.
- Script output can be reviewed by a human.
- Failure modes are explicit.
- Sensitive data handling is documented.
- Core skill remains useful without the adapter.
