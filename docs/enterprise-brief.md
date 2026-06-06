# Enterprise Brief

Codex Skills for Enterprise is a curated operating library for teams that want AI assistance to produce consistent business artifacts, not just plausible drafts.

The repository packages repeatable workflows as Codex skills: concise instructions, deeper references, optional deterministic scripts, validation rules, and adoption guidance. The goal is to help companies move from individual prompt craft to shared operating standards.

## Who This Is For

This repository is built for:

- AI transformation leaders building internal enablement programs;
- Chief AI Officers and operating teams managing AI adoption;
- executive operations teams that need cleaner decisions, reports, and follow-ups;
- engineering organizations that want faster triage and release communication;
- revenue operations teams improving CRM quality and account workflows;
- knowledge teams preserving institutional knowledge in reusable form.

## What A Company Gets

Companies can use this repository as:

- a starter catalog of enterprise-grade Codex skills;
- a reference implementation for skill quality standards;
- a local installation and validation flow for internal pilots;
- a practical model for moving skills from prompt-only workflows to script-assisted and tool-connected workflows;
- a governance artifact that explains what should and should not become a maintained skill.

## Positioning

This is not a marketplace scrape or a prompt dump. It is a maintained skill pack with a conservative quality bar:

- every skill has explicit trigger language;
- every skill has a defined output standard;
- sensitive, missing, or uncertain information must be marked rather than invented;
- broader details live in `references/` so skills stay compact;
- deterministic scripts are added only when they remove repeated manual parsing or validation;
- repository validation runs through `scripts/validate_skills.py`.

## Operating Philosophy

Good enterprise AI work has three properties:

- **Repeatability**: a team can invoke the same workflow against similar artifacts and get a comparable output shape.
- **Reviewability**: a human can inspect the output for evidence, assumptions, owners, dates, risks, and decisions.
- **Governability**: the organization can decide which workflows are safe to scale, which require review, and which should stay out of scope.

The skills in this repository encode those properties directly.

## Where To Start

Start with one narrow workflow where the current output quality is inconsistent:

- meeting notes to decisions and follow-ups;
- weekly updates to executive reports;
- CI logs to root-cause triage;
- CRM exports to hygiene findings;
- support or incident notes to KB articles;
- AI initiative updates to a CAO operating pulse.

Install one skill, run it on real sanitized artifacts, compare output quality against the current standard, and only then scale to a pack.

