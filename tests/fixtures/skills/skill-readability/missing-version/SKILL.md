---
name: missing-version
description: >
  Invalid skill readability fixture.
schema-version: skill-readability-v1
---

# Missing version fixture

## Workflow role

- role_name: missing-version
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
