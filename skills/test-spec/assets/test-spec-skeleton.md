<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/test-spec/SKILL.md -->
<!-- Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# <Test spec title>

## Owning change record

<docs/changes/change-id/change.yaml>

## Related spec and plan

- Spec: <path or reference>
- Plan: <path or reference>
- Architecture/ADRs: <paths or not applicable>

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| <input kind> | <path or not applicable> | <artifact ID> | <review ID and record path> |

## Testing strategy

<unit, integration, end-to-end, smoke, manual, contract, and migration strategy>

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |

<insert requirement coverage rows>

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |

<insert example coverage rows>

## Edge case coverage

<edge case rows>

## Validation commands

<validation-command rows, or "No validation commands are part of this proof map" with rationale>

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

<insert validation command rows, or replace the table with the approved no-command rationale>

## Milestone proof map

<milestone proof rows, or "Not applicable" with rationale>

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |

<insert milestone proof rows, or replace the table with an explicit non-applicability rationale>

## Test cases

<insert test case blocks>

## Fixtures and data

<fixtures, data, or none>

## Mocking/stubbing policy

<policy>

## Migration or compatibility tests

<tests or not applicable>

## Observability verification

<logs, metrics, traces, audit events, or not applicable>

## Security/privacy verification

<checks or not applicable>

## Performance checks

<checks or not applicable>

## Manual QA checklist

<manual checks or not applicable>

## What not to test and why

<explicit exclusions and rationale>

## Uncovered gaps

<gaps that must return to spec or architecture, or none>

## Next artifacts

<planned next steps while draft or active>

## Follow-on artifacts

<actual downstream artifacts, terminal disposition, or None yet>

## Readiness

<truthful next-stage or active-proof-surface wording>
