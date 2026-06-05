# PR Review Rubric

## Risk Areas

| Area | Look for |
| --- | --- |
| Correctness | changed control flow, edge cases, invalid assumptions |
| Security/privacy | auth, permissions, secrets, logging sensitive data |
| Data | migrations, schema changes, backfills, destructive updates |
| Compatibility | API contracts, config, clients, serialization, versioning |
| Performance | new loops, queries, blocking calls, resource pressure |
| Operability | logs, metrics, alerts, failure modes, rollback |
| Maintainability | unclear abstractions, duplicated logic, testability |

## Review Comment Pattern

Use concise comments:

```text
Blocking: <issue>. Evidence: <file/behavior/source>. Impact: <risk>. Suggested fix: <specific action>.
```

Use non-blocking comments:

```text
Non-blocking: <suggestion>. This would improve <clarity/testability/operability>.
```

## Approval Guidance

- **Ready**: risk is low and coverage matches impact.
- **Ready with nits**: only minor comments remain.
- **Needs changes**: correctness, security, data, compatibility, or rollout risk remains.
- **Unclear**: insufficient diff, context, or test evidence.
