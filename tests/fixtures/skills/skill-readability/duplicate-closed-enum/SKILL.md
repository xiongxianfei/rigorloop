---
name: duplicate-closed-enum
description: >
  Invalid skill readability fixture.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Duplicate closed enum fixture

## Workflow role

- role_name: duplicate-closed-enum
- stage: authoring
- upstream: user request
- downstream: review
- summary: Creates a test artifact.

## Contract

Closed enum: status

```text
draft
accepted
```

Closed enum: status

```text
draft
accepted
```

## Expected output

- The validator rejects this skill fixture.

## Output skeleton

```md
<artifact>
```
