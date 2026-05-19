---
name: packaged-script-valid
description: Use when validating that skill-local packaged scripts are allowed with explicit resource map details.
---

# Packaged script valid

## Resource map

- Run `scripts/check.py` when deterministic validation is needed. Input: a skill directory path. Output: exit code 0 means pass and nonzero means failure. On failure, stop and report the script output.

## Expected output

- The validator accepts this skill.
