---
name: missing-output-skeleton
description: >
  Invalid skill readability fixture.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Missing output skeleton fixture

## Workflow role

- role_name: missing-output-skeleton
- stage: authoring
- upstream: user request
- downstream: review
- summary: Creates a test artifact.

## Expected output

- The validator rejects this skill fixture.
