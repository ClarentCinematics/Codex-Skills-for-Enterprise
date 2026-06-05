# Forward-Test Playbook

Use forward-testing to verify that a skill works on realistic enterprise artifacts, not only on ideal prompts.

## Test Setup

Use one realistic prompt per skill with raw source material:

- noisy logs or partial pipeline output for CI triage;
- messy PR descriptions or changed-file lists for PR review;
- mixed commit, ticket, and support notes for release notes;
- imperfect CRM exports for hygiene audit;
- account notes with both facts and gaps for account research;
- customer discovery notes for proposals;
- conflicting research excerpts for synthesis;
- policy text with ambiguous operational impact;
- meeting or support threads for KB capture.

## Evaluation Questions

For every skill, ask:

- Did the output follow the skill's declared output standard?
- Did it avoid inventing facts, owners, dates, claims, or commitments?
- Did it preserve uncertainty and flag missing context?
- Did it produce an artifact the intended enterprise audience could use?
- Did it identify human-review points for sensitive or high-impact decisions?

## Category Smoke Tests

Engineering:

```text
Use $ci-failure-triage to diagnose this failed build log and identify the likely owner, fix path, and escalation risk.
```

Revenue:

```text
Use $crm-hygiene-auditor to audit this opportunity list for missing data, stale next steps, and forecast confidence issues.
```

Knowledge:

```text
Use $research-synthesis-brief to synthesize these three conflicting source excerpts into decision implications and next steps.
```

## Pass Criteria

A skill passes forward-testing when:

- the output is structured, actionable, and audience-appropriate;
- the source-to-output reasoning is auditable;
- missing or ambiguous source data is not silently filled in;
- the user would save meaningful time versus asking Codex without the skill;
- any high-risk output requires appropriate human review.

## Failure Patterns

Revise the skill if the output:

- summarizes instead of triaging, auditing, or deciding;
- invents facts or overstates confidence;
- hides risks to sound polished;
- produces generic advice not grounded in the artifact;
- ignores privacy, legal, customer, production, or revenue sensitivity.
