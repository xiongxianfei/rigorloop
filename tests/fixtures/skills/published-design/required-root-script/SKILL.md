---
name: required-root-script
description: Use when validating that repository-root scripts are not required customer-project dependencies.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Required root script

## Workflow role

- role_name: required-root-script
- stage: support
- upstream: user request
- downstream: validation
- summary: Validates a fixture.

## Contract

Before proceeding, run `scripts/validate-internal.py`.

## Expected output

- The validator rejects this skill.

## Output skeleton

```md
Result: <result>
```
