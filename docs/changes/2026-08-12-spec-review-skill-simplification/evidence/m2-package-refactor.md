# M2 Package Refactor Evidence

Milestone: M2
Date: 2026-08-12
Profile: `IP2-planned-armed`

## Implemented boundary

`skills/spec-review/SKILL.md` remains self-sufficient for formal classification, isolated recording, review judgment, routing, boundary activation, stops, claims, and result applicability. `references/governed-spec-review-settlement.md` loads only after exact governed authority exists and universal recording succeeds; it owns matching-entry settlement and workflow-managed automation procedure.

The shared `## Isolation and Recording` block and both projected boundary references remain byte-identical. The result asset now has one formal core, one required recording group, and governed, boundary, and automation conditional groups. Inapplicable groups are omitted by procedure, not decided by the asset.

## Profile evidence

Measurements use canonical LF-normalized bytes and whitespace-separated words and count each unique loaded resource once.

| Profile or resource | Baseline words | Current words | Baseline bytes | Current bytes | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `SKILL.md` | 2174 | 1949 | 16304 | 14821 | lower |
| `SR1-isolated-formal` | 2328 | 2143 | 17407 | 16248 | lower |
| governed reference | 0 | 447 | 0 | 3498 | conditionally added |
| `SR2-governed-formal` | 2328 | 2590 | 17407 | 19746 | explained growth |
| total package | 3590 | 3852 | 26522 | 28861 | explained growth |

The isolated formal profile decreases by 185 words (7.9 percent) and 1159 bytes (6.7 percent). Governed and total-package growth is explicit: the new reference makes exact settlement, automation, authorization, retry, pause, and missing-resource behavior independently loadable and package-valid instead of relying on compressed mixed common-path prose. No percentage target overrides preservation.

## Validation

- `python scripts/validate-skills.py skills/spec-review/SKILL.md`: passed.
- `python scripts/test-skill-validator.py`: 313 tests passed, 16 skipped.
- `python scripts/test-build-skills.py`: 7 tests passed.
- `python scripts/build-skills.py --check`: passed.
- `python scripts/test-skill-validator.py MarkdownReadabilityGuidanceTests`: 4 tests passed.
- `git diff --check`: passed.

No target-agent runtime, network service, publication action, or generated-output hand edit was used.
