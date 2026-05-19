---
name: required-root-script-command
description: Use this fixture to prove root script command dependencies are blocked.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Required root script command

## Workflow role

- role_name: required-root-script-command
- stage: support
- upstream: user request
- downstream: validation
- summary: Validates root script command detection.

## Contract

Run `scripts/validate-internal.py` for validation.

## Expected output

- The validator rejects this skill.

## Output skeleton

```md
Result: <result>
```
