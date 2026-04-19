---
name: valid-sibling
description: >
  Valid sibling skill used to prove the validator still catches a neighboring missing SKILL.md.
---

# Valid sibling fixture

This fixture is valid on its own but shares a parent directory with a missing skill file case.

## Expected output

- The validator rejects the sibling directory that lacks SKILL.md.
