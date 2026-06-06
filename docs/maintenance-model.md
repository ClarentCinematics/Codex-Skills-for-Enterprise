# Maintenance Model

This repository should look and behave like an actively maintained enterprise asset. Maintenance is intentionally lightweight, but explicit.

## Maintained Surfaces

The maintained surfaces are:

- `README.md`: public positioning, catalog, installation, and quality bar.
- `skills/`: skill instructions, references, scripts, and agent prompts.
- `docs/`: adoption, workflow, curation, maturity, and operating guidance.
- `scripts/`: local installer and validation tooling.
- `.github/`: validation workflow and contribution templates.

Internal planning notes, local artifacts, and OS metadata do not belong in the public root.

## Validation Standard

Run before every meaningful change:

```bash
python3 scripts/validate_skills.py
```

For script-assisted skills, also run syntax checks:

```bash
python3 -m py_compile scripts/validate_skills.py scripts/install_skill.py skills/*/scripts/*.py
```

When shell globbing does not match a script path, run explicit paths instead.

## Release Hygiene

For each release-quality update:

1. Keep the working tree clean before starting.
2. Pull or fetch remote changes before editing.
3. Keep unrelated changes in separate commits.
4. Update `CHANGELOG.md` for user-visible changes.
5. Run validation.
6. Push only after validation passes.

## Branch Policy

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

## Skill Lifecycle

Use this lifecycle:

1. **Candidate**: workflow mapped with audience, inputs, outputs, and quality risks.
2. **Draft**: `SKILL.md`, agent prompt, and at least one realistic example.
3. **Structured**: references or rubrics added for repeated variants.
4. **Script-assisted**: deterministic helpers added when repeated parsing or checking is costly.
5. **Adopted**: skill included in a pack and used in a real operating rhythm.

Retire or rewrite skills that are too broad, unused, hard to review, or dependent on unsupported assumptions.

## Documentation Review

Review docs for:

- current skill count;
- accurate installation commands;
- links to existing files;
- clear audience and business value;
- no copied third-party prose;
- no internal session notes.

## Current Maintained State

As of 2026-06-06:

- 15 skills are present.
- Validation passes with `python3 scripts/validate_skills.py`.
- Level 3 helper scripts exist for CI triage, CRM hygiene auditing, and KB metadata checks.
- `main` is the release branch.

