---
name: packaged-script-missing-failure
description: Use when validating that packaged script resource maps include input, output, and failure behavior.
---

# Packaged script missing failure

## Resource map

- Run `scripts/check.py` when deterministic validation is needed. Input: a skill directory path. Output: exit code 0 means pass.

## Expected output

- The validator rejects this skill.
