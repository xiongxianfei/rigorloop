---
name: missing-workflow-role-field
description: >
  Invalid skill readability fixture.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Missing workflow role field fixture

## Workflow role

- role_name: missing-workflow-role-field
- stage: authoring
- upstream: user request
- summary: Creates a test artifact.

## Expected output

- The validator rejects this skill fixture.

## Output skeleton

```md
<artifact>
```
