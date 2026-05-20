---
name: invalid-schema-version
description: >
  Invalid skill readability fixture.
version: 0.0.0-test
schema-version: skill-readability-v2
---

# Invalid schema version fixture

## Workflow role

- role_name: invalid-schema-version
- stage: authoring
- upstream: user request
- downstream: review
- summary: Creates a test artifact.

## Expected output

- The validator rejects this skill fixture.

## Output skeleton

```md
<artifact>
```
