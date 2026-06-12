# Contributing

Contributions should make enterprise workflows more repeatable, valuable, and trustworthy. Prefer fewer, higher-quality skills over a large catalog of shallow prompt wrappers.

Read [docs/curation-policy.md](docs/curation-policy.md) before proposing a new skill. The repository accepts curated enterprise workflows, not generic prompt collections.

For repository operating expectations, see the [maintenance model](docs/enterprise-handbook.md#maintenance-model).

## Before Creating A Skill

Use [templates/enterprise-workflow-map.md](templates/enterprise-workflow-map.md) to define the workflow, audience, inputs, outputs, quality risks, and acceptance criteria.

A good candidate skill has:

- a specific enterprise workflow;
- repeated use across teams or operating rhythms;
- clear input and output artifacts;
- quality standards that can be encoded;
- measurable productivity, speed, quality, or risk-reduction value.

Do not add a skill just because an instruction can be written. Add it when the workflow is repeated, reviewable, and important enough to maintain.

## Skill Requirements

Follow [docs/skill-quality-standard.md](docs/skill-quality-standard.md). At minimum, every skill must include:

- `SKILL.md` with only `name` and `description` frontmatter;
- explicit trigger language in the description;
- concise workflow instructions;
- `agents/openai.yaml` with a default prompt that mentions `$skill-name`;
- only necessary `references/`, `scripts/`, or `assets/`.

Do not place README files, changelogs, install guides, or process notes inside skill folders.

## Submission Format

For new skills or meaningful skill changes, include this information in the pull request:

- **Workflow**: the enterprise workflow improved.
- **Audience**: primary user or team.
- **Inputs**: realistic artifacts the skill expects.
- **Output standard**: the structure or decision the skill should produce.
- **Evidence**: prompt, fixture, or real sanitized artifact used for testing.
- **Validation**: command run and result.
- **Limitations**: human-review needs, missing context, or sensitive-data concerns.

## Review Workflow

1. Map the workflow using the enterprise workflow template.
2. Draft or update the skill.
3. Add repo-level examples in `docs/examples.md` if the use case is new.
4. Confirm the contribution passes [docs/curation-policy.md](docs/curation-policy.md).
5. Review the work with [templates/skill-review-checklist.md](templates/skill-review-checklist.md).
6. Run validation.

```bash
python3 scripts/generate_catalog.py
python3 scripts/validate_skills.py
python3 scripts/validate_evals.py
python3 scripts/scan_skill_security.py
python3 tests/run_smoke_tests.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

7. Run an optional Codex comparison for featured behavior changes:

```bash
python3 scripts/run_codex_evals.py --dry-run --skill <skill-name>
python3 scripts/run_codex_evals.py --skill <skill-name>
```

8. Test at least one realistic enterprise prompt before submitting.
9. Update [CHANGELOG.md](CHANGELOG.md) for user-visible repository changes.

## Pull Request Standard

In the pull request summary, include:

- workflow improved;
- skill added or changed;
- validation command and result;
- realistic prompt used for manual testing;
- known limitations or human-review requirements.

The repository includes a pull request template and issue templates for skill requests and documentation improvements. Use them instead of opening unstructured requests.
