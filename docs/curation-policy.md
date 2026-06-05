# Curation Policy

Codex Skills for Enterprise is a curated enterprise skill pack, not a bulk prompt catalog. A skill belongs here only when it makes a recurring business workflow more repeatable, reviewable, and useful.

## What Belongs

Accepted skills should have:

- a specific enterprise workflow with clear users;
- repeatable input artifacts such as notes, logs, CSVs, reports, tickets, policies, or drafts;
- a concrete output standard that a reviewer can evaluate;
- explicit handling of missing context, uncertainty, sensitive data, and human review;
- evidence from at least one realistic enterprise prompt or fixture;
- a maintenance path through validation, references, scripts, or documented limitations.

## What Does Not Belong

Reject or rework submissions that are:

- generic prompt wrappers around broad advice;
- tool-specific demos without a durable workflow;
- vendor-auth integrations embedded directly in core skill instructions;
- untested ideas with no realistic prompt evidence;
- large generated catalogs of shallow skills;
- skills that require inventing facts, owners, dates, financial values, customer commitments, or legal conclusions.

## Skill Tiers

Use maturity levels to set expectations:

- **Level 1**: prompted workflow with one reviewed output.
- **Level 2**: structured references, rubrics, or examples.
- **Level 3**: deterministic helper scripts with smoke-testable interfaces.
- **Level 4**: approved tool or system-of-record adapters.
- **Level 5**: audited pack with owner review and recurring validation.

See [Maturity Levels](maturity-levels.md) for the full model.

## Submission Evidence

Every new or materially changed skill should include:

- workflow improved;
- target audience and input artifacts;
- realistic prompt or fixture used for testing;
- expected output standard;
- validation command and result;
- known limitations and human-review requirements;
- reason the workflow should be a skill instead of a one-off prompt.

## Naming And Description

Skill names must use clear lowercase hyphen-case. Descriptions should be short enough to scan, but specific enough to trigger reliably. Include artifact types and "Use when" language in `SKILL.md` frontmatter.

## Review Criteria

Reviewers should ask:

- Does this skill reduce ambiguity in a recurring workflow?
- Would a user understand exactly when to invoke it?
- Are outputs actionable, structured, and honest about uncertainty?
- Is sensitive or revenue-critical data treated prudently?
- Does validation catch likely structural regressions?
- Is the skill compact enough to load without crowding out the user's real context?

Prefer a smaller catalog of high-trust skills over a larger catalog of thin prompt wrappers.
