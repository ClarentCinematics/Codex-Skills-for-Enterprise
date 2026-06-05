---
name: release-notes-generator
description: Convert commits, merged pull requests, tickets, changelog fragments, deployment notes, or issue lists into audience-specific release notes with user impact, internal context, breaking changes, migrations, and known issues. Use when Codex needs to prepare polished release communication from technical change history.
---

# Release Notes Generator

## Workflow

1. Identify release scope, audience, product area, date range, and source artifacts.
2. Group changes by user value, operational impact, bug fixes, breaking changes, and internal-only work.
3. Translate technical changes into outcome-focused language appropriate for the audience.
4. Preserve material caveats: migrations, feature flags, rollout limits, known issues, and support impact.
5. Produce notes that can be used for customers, internal teams, support, or executives.

## Output Standard

Use this structure by default:

- **Release Summary**: concise overview of the release.
- **Highlights**: highest-value user or business outcomes.
- **Improvements**: user-facing changes grouped by theme.
- **Fixes**: resolved issues with impact, not raw ticket noise.
- **Breaking Changes / Migrations**: required user or operator action.
- **Known Issues**: limitations, workarounds, and follow-up owner if known.
- **Internal Notes**: operational, support, rollout, or enablement details.

## Rules

- Do not expose internal implementation details in customer-facing notes unless useful.
- Do not invent features, dates, ticket status, or customer impact.
- Mark uncertain release scope as `Not stated`.
- Separate external release notes from internal enablement notes.

## References

Read `references/release-note-patterns.md` when the user asks for customer, executive, support, or developer-facing notes.
