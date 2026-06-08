# Skill Packs

Skill packs install related Codex Skills together for a team workflow. Packs are defined in `skill-packs.json` and installed with the local repository installer.

## Install Commands

List available skills and packs:

```bash
python3 scripts/install_skill.py --list
```

Install one skill:

```bash
python3 scripts/install_skill.py ci-failure-triage
```

Install a pack:

```bash
python3 scripts/install_skill.py --pack engineering-ops
```

Preview an install:

```bash
python3 scripts/install_skill.py --dry-run --pack revenue-ops
```

Install to a custom destination:

```bash
python3 scripts/install_skill.py --dest /tmp/codex-skills --pack knowledge-ops
```

Existing skills are not overwritten unless `--force` is passed.

## Available Packs

| Pack | Skills | Best for |
| --- | --- | --- |
| `executive-ops` | `meeting-intelligence`, `weekly-executive-report`, `decision-memo`, `project-status-brief`, `automation-opportunity-map`, `cao-operating-pulse` | Leadership operating rhythm, executive productivity, and Chief AI Officer briefings |
| `engineering-ops` | `ci-failure-triage`, `pr-review-brief`, `release-notes-generator` | Software delivery, review quality, CI triage, release communication |
| `revenue-ops` | `crm-hygiene-auditor`, `account-research-brief`, `proposal-drafting-assistant` | Pipeline quality, account strategy, proposal workflows |
| `knowledge-ops` | `research-synthesis-brief`, `policy-impact-analysis`, `knowledge-base-capture` | Research, policy analysis, and institutional knowledge capture |
| `reliability-ops` | `incident-postmortem-assistant` | Incident learning, corrective actions, and reliability follow-through |
| `customer-ops` | `support-deflection-miner` | Repeated support issue mining, KB opportunities, and deflection planning |
| `data-ops` | `data-quality-triage` | CSV data-quality checks before reporting, automation, or analysis |
| `product-ops` | `requirements-to-acceptance-criteria` | Product requirement readiness, acceptance criteria, and test scenarios |
| `risk-governance` | `vendor-security-review` | Vendor security evidence gaps, procurement questions, and review packets |
| `all` | All skills in the repository | Full enterprise skills installation |

## Adoption Pattern

Start with one pack, one workflow owner, and real artifacts. Run a forward test, compare output against the current team standard, and only then roll the pack out more broadly.
