# Enterprise Adoption Guide

Codex Skills work best when they are introduced as operating standards, not as prompt experiments.

For day-to-day usage, see [User Manual](user-manual.md). For packaged operating flows, see [Proposed Workflows](proposed-workflows.md).

## 1. Select A High-Value Workflow

Start with a workflow that is frequent, painful, and quality-sensitive:

- executive meeting follow-up;
- weekly leadership reporting;
- project status synthesis;
- decision documentation;
- automation intake.

Avoid starting with a workflow that has unclear ownership or no consistent definition of quality.

## 2. Define The Current Standard

Collect the artifacts the team already uses: notes, reports, status updates, decision records, dashboards, or emails. Identify what great output looks like and where quality breaks down today.

Write down:

- who consumes the output;
- what decisions or actions the output supports;
- which fields must never be invented;
- what review step is required before the output is shared;
- how success will be measured after the pilot.

## 3. Install One Skill

Copy a selected skill folder into the Codex skills directory for the pilot environment.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/weekly-executive-report "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Then invoke it with real source material:

```text
Use $weekly-executive-report to synthesize these team updates into an executive-ready weekly report.
```

## 4. Compare Against The Standard

Review the output for:

- accuracy;
- usefulness to the audience;
- missing context;
- unnecessary verbosity;
- owner/action clarity;
- risk and escalation quality.

Update the skill only when the improvement would generalize across repeated use.

## 5. Roll Out With Governance

For broader adoption, require validation before each new skill is distributed:

```bash
python3 scripts/validate_skills.py
```

Keep a human review step for sensitive workflows, regulated decisions, customer-impacting communication, or executive commitments.

## 6. Recommended Rollout Plan

| Phase | Scope | Exit criteria |
| --- | --- | --- |
| Pilot | One team, one skill, three realistic artifacts | Output quality is equal or better than current process. |
| Operating trial | One recurring meeting, report, pipeline review, or release cycle | Users can invoke and review the skill without special support. |
| Pack rollout | One skill pack for a function such as executive ops or engineering ops | Validation passes and usage guidance is documented. |
| Governance | Skills become part of an internal enablement or operating standard | Owners, review requirements, and update process are clear. |

## 7. Adoption Risks

Watch for:

- teams treating skill output as approved facts without review;
- unclear ownership of maintained skills;
- requests to connect tools before workflow quality is understood;
- excessive skill proliferation;
- stale references that encode outdated process;
- sensitive data being pasted into inappropriate environments.

These risks are manageable when the workflow is narrow, the review bar is explicit, and validation remains part of every change.
