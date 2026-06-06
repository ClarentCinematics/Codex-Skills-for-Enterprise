# Enterprise Handbook

This handbook consolidates the company-facing explanation, user manual, proposed workflows, and maintenance model for Codex Skills for Enterprise.

## Enterprise Brief

Codex Skills for Enterprise is a curated operating library for teams that want AI assistance to produce consistent business artifacts, not just plausible drafts.

The repository packages repeatable workflows as Codex skills: concise instructions, deeper references, optional deterministic scripts, validation rules, and adoption guidance. The goal is to help companies move from individual prompt craft to shared operating standards.

### Who This Is For

This repository is built for:

- AI transformation leaders building internal enablement programs;
- Chief AI Officers and operating teams managing AI adoption;
- executive operations teams that need cleaner decisions, reports, and follow-ups;
- engineering organizations that want faster triage and release communication;
- revenue operations teams improving CRM quality and account workflows;
- knowledge teams preserving institutional knowledge in reusable form.

### What A Company Gets

Companies can use this repository as:

- a starter catalog of enterprise-grade Codex skills;
- a reference implementation for skill quality standards;
- a local installation and validation flow for internal pilots;
- a practical model for moving skills from prompt-only workflows to script-assisted and tool-connected workflows;
- a governance artifact that explains what should and should not become a maintained skill.

### Operating Philosophy

Good enterprise AI work has three properties:

- **Repeatability**: a team can invoke the same workflow against similar artifacts and get a comparable output shape.
- **Reviewability**: a human can inspect the output for evidence, assumptions, owners, dates, risks, and decisions.
- **Governability**: the organization can decide which workflows are safe to scale, which require review, and which should stay out of scope.

## User Manual

### Select The Right Skill

Start with the artifact and the business outcome, not the skill name.

| Artifact | Outcome | Suggested skill |
| --- | --- | --- |
| meeting transcript or notes | decisions, owners, risks, follow-up email | `meeting-intelligence` |
| weekly team updates | executive-ready report | `weekly-executive-report` |
| CI log or failed check summary | root-cause hypothesis and fix path | `ci-failure-triage` |
| CRM CSV export or opportunity notes | hygiene findings and cleanup actions | `crm-hygiene-auditor` |
| AI initiative portfolio notes | CAO operating pulse | `cao-operating-pulse` |
| support thread or incident learning | reusable KB article | `knowledge-base-capture` |

If no skill clearly fits, use the workflow map template before creating a new one.

### Install Skills

List skills and packs:

```bash
python3 scripts/install_skill.py --list
```

Install one skill:

```bash
python3 scripts/install_skill.py meeting-intelligence
```

Install a pack:

```bash
python3 scripts/install_skill.py --pack executive-ops
```

Preview without copying:

```bash
python3 scripts/install_skill.py --dry-run --pack all
```

### Invoke A Skill

Use the skill name explicitly and provide the source artifact.

```text
Use $meeting-intelligence to turn these leadership meeting notes into decisions, action items, risks, and a follow-up email.
```

Good inputs include:

- raw notes, not just summaries;
- relevant dates, owners, and source context;
- known constraints or audience requirements;
- explicit questions the output should answer.

Poor inputs include:

- vague requests with no artifact;
- missing source dates for time-sensitive work;
- unsupported instructions to invent owners, metrics, or commitments.

### Review The Output

For every output, check:

- facts are supported by the source material;
- missing owners, dates, or values are marked `Not stated`;
- risks and decisions are separated from general narrative;
- recommendations are practical and evidence-based;
- sensitive or regulated items are flagged for human review;
- output structure matches the skill's standard.

### Use Script-Assisted Skills

Some Level 3 skills include helper scripts for deterministic checks.

```bash
python3 skills/ci-failure-triage/scripts/extract_ci_signal.py --input /tmp/ci.log
python3 skills/crm-hygiene-auditor/scripts/audit_crm_csv.py --input /tmp/pipeline.csv --today 2026-06-06
python3 skills/knowledge-base-capture/scripts/check_kb_metadata.py --input /tmp/kb-draft.md --today 2026-06-06
```

Script output is evidence, not final judgment. Codex still uses the skill workflow to produce the final brief, audit, or recommendation.

## Quality Proof

The repository includes deterministic proof artifacts so skill quality can be inspected without relying on informal claims.

- `skill-registry.json` records catalog metadata, maturity, pack assignment, audience, risk level, and featured status.
- `scripts/validate_skills.py` validates skill structure, pack consistency, registry consistency, README skill count, helper scripts, and maturity expectations.
- `docs/sample-outputs.md` shows fictional outputs for featured skills, including caveats and facts that must not be invented.
- `tests/fixtures/` stores deterministic smoke fixtures for featured skills.
- `tests/run_smoke_tests.py` validates fixture completeness and expectation schema without calling an LLM.

Recommended proof commands:

```bash
python3 scripts/validate_skills.py
python3 tests/run_smoke_tests.py
```

## Proposed Workflows

### Executive Operating Rhythm

Recommended skills:

- `meeting-intelligence`
- `weekly-executive-report`
- `decision-memo`
- `project-status-brief`

Flow:

1. Run `meeting-intelligence` after leadership meetings.
2. Convert unresolved decisions into `decision-memo` drafts.
3. Roll project updates into `project-status-brief`.
4. Use `weekly-executive-report` to synthesize the operating narrative.
5. Review owners, dates, escalations, and decision asks before distribution.

### Chief AI Officer Pulse

Recommended skills:

- `cao-operating-pulse`
- `automation-opportunity-map`
- `policy-impact-analysis`
- `research-synthesis-brief`

Flow:

1. Collect initiative updates, usage signals, incidents, policy notes, and vendor claims.
2. Run `cao-operating-pulse` to separate signal from theatre.
3. Use `automation-opportunity-map` for new candidate workflows.
4. Use `policy-impact-analysis` when governance or regulatory changes affect rollout.
5. Convert external research into evidence using `research-synthesis-brief`.

### Engineering Release Readiness

Recommended skills:

- `ci-failure-triage`
- `pr-review-brief`
- `release-notes-generator`

Flow:

1. Run the CI signal extractor on long logs when available.
2. Use `ci-failure-triage` to produce root-cause hypotheses and fix paths.
3. Use `pr-review-brief` to focus review on risk, behavior, and missing tests.
4. Use `release-notes-generator` to translate merged changes into audience-ready release communication.

### Revenue Operations Hygiene

Recommended skills:

- `crm-hygiene-auditor`
- `account-research-brief`
- `proposal-drafting-assistant`

Flow:

1. Export CRM records to CSV and run the hygiene audit helper.
2. Use `crm-hygiene-auditor` to prioritize cleanup actions.
3. Use `account-research-brief` for key accounts with active opportunities.
4. Use `proposal-drafting-assistant` after needs, constraints, and review requirements are clear.

### Knowledge Capture And Reuse

Recommended skills:

- `knowledge-base-capture`
- `research-synthesis-brief`
- `policy-impact-analysis`

Flow:

1. Capture meeting notes, support threads, incident learnings, or process drafts.
2. Use `knowledge-base-capture` to create a reusable article.
3. Run the metadata checker before publishing.
4. Use `research-synthesis-brief` for evidence-heavy topics.
5. Use `policy-impact-analysis` when the article depends on policy or compliance changes.

### Automation Intake

Recommended skills:

- `automation-opportunity-map`
- `decision-memo`
- `project-status-brief`

Flow:

1. Collect workflow notes, systems involved, pain points, frequency, risks, and constraints.
2. Use `automation-opportunity-map` to classify opportunities by skill, script, integration, or process redesign.
3. Use `decision-memo` for build/buy/defer decisions.
4. Use `project-status-brief` once implementation starts.

## Maintenance Model

This repository should look and behave like an actively maintained enterprise asset. Maintenance is intentionally lightweight, but explicit.

### Maintained Surfaces

- `README.md`: public positioning, catalog, installation, and quality bar.
- `skills/`: skill instructions, references, scripts, and agent prompts.
- `docs/`: adoption, workflow, curation, maturity, and operating guidance.
- `scripts/`: local installer and validation tooling.
- `.github/`: validation workflow and contribution templates.

Internal planning notes, local artifacts, and OS metadata do not belong in the public root.

### Validation Standard

Run before every meaningful change:

```bash
python3 scripts/validate_skills.py
```

For script-assisted skills, also run syntax checks:

```bash
python3 -m py_compile scripts/validate_skills.py scripts/install_skill.py skills/*/scripts/*.py
```

### Release Hygiene

For each release-quality update:

1. Keep the working tree clean before starting.
2. Pull or fetch remote changes before editing.
3. Keep unrelated changes in separate commits.
4. Update `CHANGELOG.md` for user-visible changes.
5. Run validation.
6. Push only after validation passes.

### Branch Policy

Recommended branch use:

- `main`: validated, installable, public-facing state.
- feature branches: one coherent skill, doc set, or script-assisted upgrade.
- no long-lived branches without a clear owner and merge plan.

Before merging a branch, check:

- no `.DS_Store`, `__pycache__`, or local scratch files;
- no unresolved conflict markers;
- no placeholder docs such as `WIP.md`;
- skill count, pack metadata, and README badges remain accurate;
- validation passes.

### Current Maintained State

As of 2026-06-06:

- 15 skills are present.
- Validation passes with `python3 scripts/validate_skills.py`.
- Level 3 helper scripts exist for CI triage, CRM hygiene auditing, and KB metadata checks.
- Registry metadata and smoke fixtures support the five featured skills.
- `main` is the release branch.
