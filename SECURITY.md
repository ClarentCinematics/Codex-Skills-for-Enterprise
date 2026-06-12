# Security Policy

This repository contains Codex skill instructions, references, local helper scripts, and documentation. It does not intentionally store secrets, credentials, customer data, or private system exports.

## Reporting Sensitive Issues

Do not open public issues containing:

- API keys, passwords, tokens, or credentials;
- customer-identifying data;
- private logs or system exports;
- regulated personal data;
- confidential contract, revenue, or account details.

If a public issue would require sensitive evidence, sanitize the artifact first and include only the minimal excerpt needed to reproduce the issue.

## Supported Surfaces

Security-sensitive review should focus on:

- helper scripts under `skills/*/scripts/`;
- installer and validation scripts under `scripts/`;
- documentation that could encourage unsafe data handling;
- skill instructions that might invite unsupported legal, financial, or compliance conclusions.

## Data Handling Principle

Skills should mark missing or sensitive information explicitly. They should not invent facts, credentials, owners, legal conclusions, financial values, or customer commitments.

See [docs/security-model.md](docs/security-model.md) for the complete trust boundary, helper capability policy, registry declarations, and threat model.

## Private Reporting

Use GitHub private vulnerability reporting for security-sensitive findings. If that option is unavailable, open a minimal public issue requesting a private contact channel without including exploit details or sensitive evidence.
