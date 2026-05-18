---
name: required-internal-reference
description: >
  Invalid skill readability fixture.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Required internal reference fixture

## Workflow role

- role_name: required-internal-reference
- stage: authoring
- upstream: user request
- downstream: review
- summary: Creates a test artifact.

## Expected output

- The validator rejects this skill fixture.

Before proceeding, read specs/skill-contract.md from the RigorLoop repository.

## Output skeleton

```md
<artifact>
```
