---
name: support-deflection-miner
description: Analyze support tickets, helpdesk exports, issue subjects, customer questions, or support thread summaries to find repeated themes, duplicate-looking requests, documentation gaps, automation candidates, and support-deflection opportunities. Use when Codex needs to convert support noise into prioritized KB, product, or workflow improvements without inventing customer facts.
---

# Support Deflection Miner

## Workflow

1. Identify source type, date range, product area, customer segment, and support goal.
2. Group repeated questions, symptoms, ticket subjects, and workaround requests.
3. Separate documentation gaps, product friction, policy confusion, and automation opportunities.
4. Prioritize by repetition, customer impact, confidence, and actionability.
5. Produce proposed KB articles, product feedback, macros, automation candidates, and caveats.

## Script-Assisted Workflow

When given ticket subjects in CSV or text form, run `scripts/mine_support_themes.py --input <path>` first. Use `--json` when structured theme counts are needed. The helper surfaces repeated text patterns; Codex must still judge whether a theme is a KB gap, product issue, or workflow candidate.

## Output Standard

Use this structure by default:

- **Deflection Summary**: source scope, top repeated issues, and confidence.
- **Top Themes**: theme, evidence, count, likely category, and caveats.
- **Duplicate-Looking Requests**: repeated subjects or near-repeated issue language.
- **KB Opportunities**: proposed article titles, audience, source evidence, and missing facts.
- **Product / Process Signals**: friction points requiring product, policy, or workflow review.
- **Automation Candidates**: macro, bot, form, routing, or script opportunities.
- **Questions To Resolve**: missing context needed before publishing or automating.

## Rules

- Do not invent customer names, ticket counts beyond the provided input, root causes, SLA impact, or product commitments.
- Mark keyword clusters as heuristic, not definitive taxonomy.
- Keep customer-sensitive data out of examples unless already sanitized.
- Prefer small, reviewable deflection actions over broad automation claims.

## References

Read `references/deflection-rubric.md` when deciding whether a repeated support theme should become a KB article, product bug, macro, or automation candidate.
