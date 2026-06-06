# User Manual

This manual explains how to select, install, run, review, and maintain Codex Skills for Enterprise.

## 1. Select The Right Skill

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

## 2. Install Skills

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

Overwrite an installed skill only when you intend to replace it:

```bash
python3 scripts/install_skill.py meeting-intelligence --force
```

## 3. Invoke A Skill

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

## 4. Review The Output

For every output, check:

- facts are supported by the source material;
- missing owners, dates, or values are marked `Not stated`;
- risks and decisions are separated from general narrative;
- recommendations are practical and evidence-based;
- sensitive or regulated items are flagged for human review;
- output structure matches the skill's standard.

## 5. Use Script-Assisted Skills

Some Level 3 skills include helper scripts for deterministic checks.

Examples:

```bash
python3 skills/ci-failure-triage/scripts/extract_ci_signal.py --input /tmp/ci.log
python3 skills/crm-hygiene-auditor/scripts/audit_crm_csv.py --input /tmp/pipeline.csv --today 2026-06-06
python3 skills/knowledge-base-capture/scripts/check_kb_metadata.py --input /tmp/kb-draft.md --today 2026-06-06
```

Script output is evidence, not final judgment. Codex still uses the skill workflow to produce the final brief, audit, or recommendation.

## 6. Validate The Repository

Run validation before committing skill or pack changes:

```bash
python3 scripts/validate_skills.py
```

Validation checks skill metadata, folder structure, agent prompts, pack references, and helper scripts.

## 7. Scale Adoption

For a team rollout:

1. Choose one workflow and one skill.
2. Run it against three realistic artifacts.
3. Compare output quality against the current process.
4. Tune references only when the improvement generalizes.
5. Install the skill for the pilot team.
6. Add a review checkpoint for sensitive or executive-facing outputs.
7. Expand to a pack after the workflow is trusted.

