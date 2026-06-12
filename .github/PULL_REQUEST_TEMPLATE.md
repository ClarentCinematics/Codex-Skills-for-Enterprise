## Summary

- 

## Type Of Change

- [ ] New skill
- [ ] Existing skill update
- [ ] Documentation update
- [ ] Script or validation update
- [ ] Pack or installer update
- [ ] Plugin, security, or governance update

## Enterprise Workflow

Describe the workflow improved, target audience, expected inputs, and output standard.

## Evidence

Include the realistic prompt, fixture, sanitized artifact, or manual test used to validate the change.

## Validation

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_evals.py
python3 scripts/scan_skill_security.py
python3 tests/run_smoke_tests.py
python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONPYCACHEPREFIX=/tmp/cse-pycache-pr python3 -m py_compile scripts/*.py tests/*.py
```

Result:

- [ ] Passed
- [ ] Not run

## Quality Gates

- [ ] `skill-registry.json` updated if skill metadata changed.
- [ ] `docs/catalog.md` regenerated if registry changed.
- [ ] Smoke fixture added or updated if a featured skill changed.
- [ ] Three featured eval cases added or updated when featured behavior changed.
- [ ] Trigger cases updated when skill descriptions changed.
- [ ] Sample output updated if featured skill behavior changed.
- [ ] Trust metadata and security declarations match actual helper capabilities.
- [ ] Plugin manifest version updated when the installable surface changed.
- [ ] `CHANGELOG.md` updated for user-visible changes.

## Review Notes

List known limitations, human-review requirements, sensitive-data concerns, or follow-up work.
