# Security Model

Codex Skills for Enterprise contains instructions, references, and local advisory helpers. It does not include external service authentication, remote execution, or autonomous business decisions.

## Trust Boundary

Skill inputs may contain internal or confidential business information. Users remain responsible for deciding whether an artifact may be processed in their Codex environment.

Repository fixtures are fictional. Contributors must not commit:

- credentials, tokens, or secrets;
- customer-identifying records;
- private production logs;
- regulated personal data;
- confidential contracts, revenue records, or security reports.

## Helper Capabilities

Current Level 3 helpers:

- read only the input path supplied by the user;
- write results to standard output only;
- use the Python standard library;
- make no network calls;
- launch no subprocesses;
- access no credentials or environment variables;
- perform no destructive or source-file operations.

`scripts/scan_skill_security.py` checks helper abstract syntax trees against the declared registry profile. A capability must be explicitly reviewed and declared before it can be introduced.

## Registry Trust Metadata

Every skill declares:

- owner and semantic version;
- last review date;
- expected data classification;
- network and filesystem effects;
- human-review level;
- evaluation status.

High-risk skills require human review. Registry metadata describes the repository workflow and does not override an organization's own data, legal, security, or compliance policies.

## Output Safety

Skills must not invent missing owners, dates, metrics, approvals, customer commitments, legal conclusions, financial values, incident impact, or security evidence.

Outputs should:

- separate evidence from inference;
- mark missing facts explicitly;
- preserve unresolved assumptions;
- redact obvious secret-like values when a helper processes logs;
- require qualified review for legal, compliance, security, financial, executive, or customer-impacting decisions.

## Threats In Scope

- malicious or accidental helper capabilities;
- prompt instructions that pressure Codex to fabricate evidence;
- secret-like values echoed from logs;
- stale or undeclared ownership and review metadata;
- supply-chain risk in GitHub Actions;
- catalog, fixture, and generated-document drift.

## Threats Out Of Scope

- security of the user's Codex installation or connected services;
- authorization decisions in external business systems;
- malware scanning of arbitrary user inputs;
- guarantees that model output is correct;
- automated approval of vendors, releases, policies, incidents, forecasts, or executive decisions.

Report sensitive findings through GitHub private vulnerability reporting. Do not include sensitive evidence in a public issue.
