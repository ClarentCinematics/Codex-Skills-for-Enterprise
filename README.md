# Codex Skills for Enterprise

Premium, practical Codex Skills for teams that want to accelerate executive work, automate repeatable workflows, and raise the quality of day-to-day knowledge operations.

This repository is designed for enterprise AI leaders, transformation teams, and internal builders who need more than generic prompts. Each skill packages a repeatable workflow into concise instructions, reusable references, and validation standards that help Codex produce consistent, high-value work.

## Why This Exists

Enterprises do not need more scattered prompt snippets. They need reliable operating patterns that help teams:

- turn messy inputs into decision-ready outputs;
- standardize reporting, follow-ups, and escalation paths;
- identify automation opportunities with measurable business value;
- preserve institutional quality standards across teams;
- move from one-off AI usage to repeatable AI-enabled workflows.

Codex Skills make that possible by giving Codex targeted procedural knowledge for specific work.

## Skill Catalog

### Executive Ops

| Skill | Enterprise outcome | Use when |
| --- | --- | --- |
| `meeting-intelligence` | Convert meetings into decisions, owners, risks, and follow-ups | Raw meeting notes, transcripts, or recap drafts need executive-ready structure |
| `weekly-executive-report` | Create concise weekly leadership reports | Multiple team updates need to become one clear status narrative |
| `decision-memo` | Frame options, tradeoffs, risks, and a recommendation | A team needs a documented decision path, not just a recommendation |
| `project-status-brief` | Standardize project health, blockers, milestones, and escalations | Project updates are inconsistent, scattered, or too verbose |
| `automation-opportunity-map` | Identify and prioritize workflows for automation | A process needs evaluation for Codex, scripts, tools, or integration automation |

### Engineering Ops

| Skill | Enterprise outcome | Use when |
| --- | --- | --- |
| `ci-failure-triage` | Diagnose failed builds, tests, checks, and release-blocking automation | CI logs or pipeline summaries need root cause, owner, reproduction, and fix path |
| `pr-review-brief` | Prepare focused, risk-aware pull request reviews | PRs or merge requests need review focus, blockers, missing tests, and suggested comments |
| `release-notes-generator` | Produce audience-specific release communication | Commits, PRs, tickets, or changelog fragments need polished release notes |

### Revenue Ops

| Skill | Enterprise outcome | Use when |
| --- | --- | --- |
| `crm-hygiene-auditor` | Improve pipeline hygiene, ownership clarity, and forecast confidence | CRM records or opportunity exports need data-quality inspection |
| `account-research-brief` | Turn account context into sales-ready research and outreach angles | Account notes, research, and signals need synthesis for discovery or strategy |
| `proposal-drafting-assistant` | Draft tailored, reviewable enterprise proposals | Customer needs and solution context need a proposal or SOW-style draft |

### Knowledge Ops

| Skill | Enterprise outcome | Use when |
| --- | --- | --- |
| `research-synthesis-brief` | Create source-grounded research and decision briefs | Multiple sources need claims, evidence, caveats, contradictions, and actions |
| `policy-impact-analysis` | Translate policy changes into business impact and action plans | Policies, regulations, or internal guidance need gap analysis and rollout guidance |
| `knowledge-base-capture` | Preserve institutional knowledge as maintainable KB articles | Meetings, support threads, SOPs, or learnings need reusable documentation |

## Repository Structure

```text
.
|-- README.md
|-- CONTRIBUTING.md
|-- docs/
|   |-- adoption-guide.md
|   |-- examples.md
|   |-- forward-test-playbook.md
|   |-- skill-quality-standard.md
|   `-- v2-skill-examples.md
|-- skills/
|   `-- <skill-name>/
|       |-- SKILL.md
|       |-- agents/openai.yaml
|       `-- references/
|-- templates/
|   |-- enterprise-workflow-map.md
|   |-- skill-review-checklist.md
|   `-- trigger-examples.md
|-- scripts/
|   `-- validate_skills.py
`-- .github/workflows/validate-skills.yml
```

## Quickstart

1. Clone the repository.

   ```bash
   git clone https://github.com/ClarentCinematics/Codex-Skills-for-Enterprise.git
   cd Codex-Skills-for-Enterprise
   ```

2. Review the catalog in `skills/` and select the skill that matches the workflow.

3. Copy or install the selected skill into the Codex skills directory used by your environment.

   ```bash
   mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
   cp -R skills/meeting-intelligence "${CODEX_HOME:-$HOME/.codex}/skills/"
   ```

4. Invoke the skill in Codex with a concrete business artifact.

   ```text
   Use $meeting-intelligence to turn these notes into decisions, actions, risks, and follow-ups.
   ```

5. Validate the repository before contributing changes.

   ```bash
   python3 scripts/validate_skills.py
   ```

## Quality Bar

Every skill in this repository must meet a strict v1 standard:

- clear trigger language in `SKILL.md` frontmatter;
- concise procedural instructions that assume Codex is already capable;
- one-level `references/` files for deeper frameworks or examples;
- no auxiliary README, changelog, or installation files inside skill folders;
- realistic enterprise use cases documented at the repo level;
- validation through `scripts/validate_skills.py` and manual review.

See [Skill Quality Standard](docs/skill-quality-standard.md) for the full checklist.

For the v2 skill expansion, see [V2 Skill Examples](docs/v2-skill-examples.md) and [Forward-Test Playbook](docs/forward-test-playbook.md) for realistic prompts, quality criteria, and smoke-test guidance.

## Enterprise Adoption Path

Start with a narrow workflow where quality and consistency matter: executive reporting, meeting follow-up, decision documentation, project status, or automation intake. Install one skill, run it against real artifacts, compare outputs against the current operating standard, then tune the skill or reference material before broader rollout.

See [Enterprise Adoption Guide](docs/adoption-guide.md) for a practical rollout model.

## Contributing

Use the templates in `templates/` before adding or changing a skill. A contribution should improve repeatability, reduce ambiguity, or encode a valuable enterprise workflow that Codex would otherwise have to rediscover.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

Before opening a pull request:

```bash
python3 scripts/validate_skills.py
```

Then review the contribution against [templates/skill-review-checklist.md](templates/skill-review-checklist.md).
