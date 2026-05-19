---
name: invalid-stage
description: >
  Invalid skill readability fixture.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Invalid stage fixture

## Workflow role

- role_name: invalid-stage
- stage: planningish
- upstream: user request
- downstream: review
- summary: Creates a test artifact.

## Expected output

- The validator rejects this skill fixture.

## Output skeleton

```md
<artifact>
```
