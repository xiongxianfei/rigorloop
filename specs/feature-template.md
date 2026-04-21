# <feature-name>

## Status
- draft | approved | abandoned | superseded | archived

If the status is `superseded`, also record:

- `superseded_at: YYYY-MM-DD`
- `superseded_by: specs/replacement-spec.md`
- `superseded_reason: short explanation`

## Related proposal

- proposal path or issue link

## Goal and context

Describe the user-visible behavior in one short paragraph.

## Glossary

- term: definition

## Examples first

### Example E1: happy path

Given ...
When ...
Then ...

### Example E2: edge or failure path

Given ...
When ...
Then ...

## Requirements

R1. The system MUST ...
R2. The system MUST ...

## Inputs and outputs

- inputs:
- outputs:

## State and invariants

- invariant:

## Error and boundary behavior

- invalid input:
- empty state:
- partial failure:

## Non-goals

- item

## Compatibility and migration

- note any compatibility constraints, rollout rules, or migration requirements

## Observability

- logs, metrics, traces, audit events, or user-visible confirmations

## Security and privacy

- auth, permissions, data exposure, abuse, or secret handling notes

## Accessibility and UX

- only when the feature changes user-visible interaction

## Performance expectations

- only when user-visible behavior depends on performance

## Edge cases

1. edge or empty case
2. failure or compatibility case

## Acceptance criteria

- criterion

## Open questions

- only include questions that do not invalidate the spec

## Next artifacts

- planned next steps while this spec remains active

## Follow-on artifacts

- `None yet`

This section is optional until actual downstream artifacts or terminal closeout exist. If it is present before real follow-ons exist, it must explicitly say `None yet`.

## Readiness

- Draft example: ready for `spec-review`.
- Approved example: spec review is complete and the spec may be relied on by downstream stages.
- Historical example: terminal or archived specs should describe actual closeout rather than pending review work.
