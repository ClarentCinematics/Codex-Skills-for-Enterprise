# V2 Skill Examples

These examples define realistic invocation prompts and quality criteria for the Engineering Ops, Revenue Ops, and Knowledge Ops skills.

## Engineering Ops

### CI Failure Triage

Prompt:

```text
Use $ci-failure-triage to diagnose this failed pipeline. Include likely root cause, owner, reproduction steps, fix path, and escalation needs.
```

Quality criteria:

- identifies the primary failure signal instead of summarizing all logs;
- separates root-cause hypotheses from downstream noise;
- marks missing owners or commands as `Not stated`;
- recommends a validation path that would prove the fix.

### PR Review Brief

Prompt:

```text
Use $pr-review-brief to prepare a risk-focused review brief for this merge request description, changed-file list, and reviewer comments.
```

Quality criteria:

- summarizes behavior change separately from refactor or test-only work;
- identifies review focus areas grounded in the source material;
- separates blockers from non-blocking suggestions;
- flags missing tests, rollout, migration, security, or privacy review when relevant.

### Release Notes Generator

Prompt:

```text
Use $release-notes-generator to turn these merged PRs and ticket summaries into customer-facing and internal release notes.
```

Quality criteria:

- translates technical changes into user or business impact;
- separates customer-facing notes from internal enablement notes;
- includes breaking changes, migrations, and known issues only when supported;
- avoids exposing internal implementation noise.

## Revenue Ops

### CRM Hygiene Auditor

Prompt:

```text
Use $crm-hygiene-auditor to audit this opportunity export for stale records, missing fields, ownership gaps, and forecast risk.
```

Quality criteria:

- identifies missing, stale, duplicate, inconsistent, or unsupported CRM data;
- ties hygiene issues to business impact;
- does not invent owners, amounts, close dates, or next steps;
- prioritizes cleanup actions by severity.

### Account Research Brief

Prompt:

```text
Use $account-research-brief to synthesize these account notes and research excerpts into ICP fit, buying signals, stakeholder map, risks, and outreach angles.
```

Quality criteria:

- labels sourced facts, inferences, hypotheses, and unknowns;
- produces specific outreach angles tied to evidence;
- avoids fabricated company facts or stakeholders;
- surfaces disqualifiers and research questions.

### Proposal Drafting Assistant

Prompt:

```text
Use $proposal-drafting-assistant to draft an executive proposal from these discovery notes, customer goals, solution capabilities, constraints, and proof points.
```

Quality criteria:

- maps solution scope to confirmed customer needs;
- labels assumptions and review-required commitments;
- avoids invented pricing, legal terms, guarantees, or compliance claims;
- includes implementation path, risks, and next steps.

## Knowledge Ops

### Research Synthesis Brief

Prompt:

```text
Use $research-synthesis-brief to synthesize these reports and interview notes into claims, evidence, caveats, contradictions, and recommended actions.
```

Quality criteria:

- answers the research question rather than summarizing source-by-source;
- includes confidence levels and evidence caveats;
- preserves contradictions instead of forcing consensus;
- produces decision implications and next steps.

### Policy Impact Analysis

Prompt:

```text
Use $policy-impact-analysis to analyze this new internal AI usage policy and identify affected teams, workflow gaps, controls, and action plan.
```

Quality criteria:

- separates explicit policy requirements from interpretation;
- maps impacts to teams, workflows, systems, data, and controls;
- flags legal, compliance, security, privacy, or leadership review needs;
- avoids presenting legal advice as final determination.

### Knowledge Base Capture

Prompt:

```text
Use $knowledge-base-capture to convert this support thread and team discussion into a publish-ready troubleshooting article.
```

Quality criteria:

- removes transient discussion and preserves reusable knowledge;
- includes audience, prerequisites, procedure, troubleshooting, ownership, and freshness metadata;
- marks unresolved assumptions for review;
- makes the article usable by someone who was not present for the source conversation.
