# Bulk Invite Upload

## Problem

Workspace admins want to upload a CSV of users instead of inviting each person manually.

## Requirements

- Admin can upload a CSV with email and role columns.
- System rejects rows with invalid email format.
- Imported users receive the existing invite email.
- Duplicate emails should not create duplicate pending invites.

## Owner

Product owner: Maya.

## Dependencies

CSV parser service and existing invite email service.

Acceptance criteria and test scenarios are TBD. Launch constraints are not stated.
