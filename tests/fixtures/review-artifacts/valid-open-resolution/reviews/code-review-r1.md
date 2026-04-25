# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: git diff main...HEAD
Status: changes-requested

## Scope

This fixture records one first-pass review event.

## Findings

### CR1-F1: Missing direct proof

Finding ID: CR1-F1

Evidence: Requirement `R5b` requires every material Finding ID to appear in review-resolution.

Required outcome: The finding must have a resolution entry before fixes rely on it.

Suggested resolution: Add a matching review-resolution entry with a validation target.
