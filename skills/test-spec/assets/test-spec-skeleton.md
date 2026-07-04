<!-- Template: test-spec-skeleton-v1 -->
<!-- Skill: test-spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/test-spec/SKILL.md -->

# <Test spec title>

## Status

<test spec status>

## Related spec and plan

- Spec: <path or reference>
- Plan: <path or reference>
- Architecture/ADRs: <paths or not applicable>

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| <input kind> | <path or not applicable> | <status or review state> | <commit, review ID, version, or rationale> |

## Testing strategy

<unit, integration, end-to-end, smoke, manual, contract, and migration strategy>

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| <requirement ID> | <test IDs or manual verification> | <level> | <notes> |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| <example> | <test IDs or manual verification> | <notes> |

## Edge case coverage

<edge case rows>

## Validation commands

<validation-command rows, or "No validation commands are part of this proof map" with rationale>

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <command ID> | `<command>` | <classification> | <owner> | <milestone or not applicable> | <milestone, gate, or not applicable> | <failure behavior> | <zero-test behavior or not applicable> | <artifact path> | <safe-mode or side-effect boundary> |

## Milestone proof map

<milestone proof rows, or "Not applicable" with rationale>

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| <milestone> | <test IDs or not applicable> | <manual proof IDs or none> | <command IDs or none> | <artifact paths or not applicable> | <gate or stage> | <notes> |

## Test cases

<test case blocks>

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
