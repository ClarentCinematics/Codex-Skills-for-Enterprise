## Summary

- 

## Type Of Change

- [ ] New skill
- [ ] Existing skill update
- [ ] Documentation update
- [ ] Script or validation update
- [ ] Pack or installer update

## Enterprise Workflow

Describe the workflow improved, target audience, expected inputs, and output standard.

## Evidence

Include the realistic prompt, fixture, sanitized artifact, or manual test used to validate the change.

## Validation

```bash
python3 scripts/validate_skills.py
python3 tests/run_smoke_tests.py
PYTHONPYCACHEPREFIX=/tmp/cse-pycache-pr python3 -m py_compile scripts/validate_skills.py scripts/install_skill.py scripts/generate_catalog.py tests/run_smoke_tests.py
```

Result:

- [ ] Passed
- [ ] Not run

## Quality Gates

- [ ] `skill-registry.json` updated if skill metadata changed.
- [ ] `docs/catalog.md` regenerated if registry changed.
- [ ] Smoke fixture added or updated if a featured skill changed.
- [ ] Sample output updated if featured skill behavior changed.
- [ ] `CHANGELOG.md` updated for user-visible changes.

## Review Notes

List known limitations, human-review requirements, sensitive-data concerns, or follow-up work.
