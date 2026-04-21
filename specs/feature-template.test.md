# <feature-name> test spec

## Status
- draft | active | abandoned | superseded | archived

If the status is `superseded`, also record:

- `superseded_at: YYYY-MM-DD`
- `superseded_by: specs/replacement-feature.test.md`
- `superseded_reason: short explanation`

## Related spec and plan

- Spec: `specs/<feature-name>.md`
- Plan: `docs/plans/YYYY-MM-DD-<slug>.md` or `not needed`

## Testing strategy

- unit:
- integration:
- smoke/manual:

## Requirement coverage map

| Requirement | Test IDs | Notes |
| --- | --- | --- |
| `R1` | `T1` | note |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T1` | note |

## Edge case coverage

- edge case -> `T2`

## Test cases

### T1. Title
- Covers: `R1`, `E1`
- Level: unit | integration | smoke | manual
- Fixture/setup:
- Steps:
- Expected result:
- Failure proves:
- Automation location:

## Fixtures and data

- fixture, seed data, or helper notes

## Mocking/stubbing policy

- what may be mocked and what must stay real

## Migration or compatibility tests

- only when relevant

## Observability verification

- logs, metrics, traces, or audit checks when relevant

## Security/privacy verification

- auth, permission, or exposure checks when relevant

## Performance checks

- only when performance is part of the contract

## Manual QA checklist

- manual proof items when automation is insufficient

## What not to test

- explicit exclusions and why

## Uncovered gaps

- spec or architecture gaps that block safe proof

## Next artifacts

- planned next steps while this test spec is still draft or active

## Follow-on artifacts

- `None yet`

This section is optional until actual downstream artifacts or terminal closeout exist. If it is present before real follow-ons exist, it must explicitly say `None yet`.

## Readiness

- Draft example: ready for implementation use or the next repository-defined review surface.
- Active example: this test spec is the current proof-planning surface.
- Historical example: terminal or archived test specs should describe actual closeout and should not claim long-lived `complete` status.
