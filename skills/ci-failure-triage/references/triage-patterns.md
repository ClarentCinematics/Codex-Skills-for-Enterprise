# CI Failure Triage Patterns

## Failure Classes

| Class | Signals | First checks |
| --- | --- | --- |
| Test regression | assertion failure, snapshot diff, changed behavior | changed files, failing test scope, recent related commits |
| Build/config | compiler error, missing module, invalid config | dependency lockfiles, env vars, build scripts |
| Infrastructure | timeout, runner failure, network error, service unavailable | retry history, provider status, parallel job failures |
| Secret/access | unauthorized, forbidden, missing token | secret rotation, permissions, environment scope |
| Flaky test | intermittent pass/fail, timing, order dependence | recent flakes, isolation, retries, timeouts |

## Triage Heuristics

- Prefer the earliest deterministic error over later cascading failures.
- Compare failing and passing jobs when both are provided.
- Treat broad failures after dependency or image changes as environment/config candidates.
- Treat one isolated test failure after feature changes as a code or test expectation candidate.

## Escalation Triggers

- Release or deployment is blocked.
- Failure affects multiple unrelated jobs.
- Secret, credential, compliance, or customer data exposure is possible.
- Root cause requires access to systems not present in the prompt.
