---
name: valid-pilot
description: >
  Valid skill readability fixture.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Valid pilot fixture

## Workflow role

- role_name: valid-pilot
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

Workflow-wide rule: keep review evidence recorded.

Skill-local rule: emit this fixture's artifact.

## Expected output

- The validator accepts this skill fixture.

## Output skeleton

```md
Title: <title>

## Status

<draft|accepted>
```
