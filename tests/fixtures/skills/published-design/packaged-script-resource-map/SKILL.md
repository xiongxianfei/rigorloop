---
name: packaged-script-resource-map
description: Use this fixture to prove mapped skill-local packaged scripts are allowed.
version: 0.0.0-test
schema-version: skill-readability-v1
---

# Packaged script resource map

## Workflow role

- role_name: packaged-script-resource-map
- stage: support
- upstream: user request
- downstream: validation
- summary: Validates packaged script resource maps.

## Resource map

- Use `scripts/validate_output.py` when validating this skill's generated output.
  Input: generated output file.
  Output: exit code 0 means valid; nonzero means fix the output and rerun.

## Expected output

- The validator accepts this skill.

## Output skeleton

```md
Result: <result>
```
