---
name: knowledge-base-capture
description: Convert meetings, support threads, incident learnings, project notes, SOP drafts, process explanations, or expert knowledge into clean knowledge-base articles with audience, steps, ownership, freshness metadata, related links, and review needs. Use when Codex needs to preserve institutional knowledge in a reusable article.
---

# Knowledge Base Capture

## Workflow

1. Identify audience, knowledge type, source material, owner, and intended knowledge base location if provided.
2. Extract reusable knowledge: purpose, prerequisites, steps, decisions, troubleshooting, examples, and limits.
3. Remove transient discussion, duplicated context, and unresolved claims unless they are marked for review.
4. Structure the article for reuse, searchability, ownership, and future maintenance.
5. Produce a clean KB draft with metadata and review questions.

## Script-Assisted Workflow

When reviewing a markdown KB draft, run `scripts/check_kb_metadata.py --input <draft.md>` to check required sections, metadata completeness, review freshness, owner gaps, and unresolved assumptions. Adjust `--required-sections` and `--today` for the target knowledge-base standard. Use the output to decide publishing readiness; do not use the script to rewrite the article.

## Output Standard

Use this structure by default:

- **Title**: searchable, specific, and outcome-oriented.
- **Audience**: who should use the article.
- **Summary**: what the article helps the reader do.
- **Prerequisites**: access, tools, context, or permissions needed.
- **Procedure / Guidance**: steps, decision rules, or reference content.
- **Troubleshooting / Exceptions**: known issues, limits, and escalation path.
- **Ownership And Freshness**: owner, review date, source, and confidence.
- **Related Links**: source artifacts or related docs when provided.
- **Review Questions**: unresolved items before publishing.

## Rules

- Do not publish unresolved assumptions as facts.
- Preserve source provenance when available.
- Flag stale, sensitive, incomplete, or ownerless knowledge for review.
- Make the article useful to someone who was not present for the original discussion.

## References

Read `references/kb-patterns.md` when the user asks for SOPs, troubleshooting articles, incident learnings, onboarding docs, or support knowledge.
