# Code Review Independence Under Autoprogression

## Status

- approved

## Related proposal

- [Code Review Independence Under Autoprogression](../docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md)

## Goal and context

This spec defines how `code-review` behaves when it is entered automatically after `implement` in a workflow-managed full-feature run.

The approved autoprogression contract already requires `implement -> code-review` and permits `code-review -> review-resolution -> code-review` for fixable findings. This follow-up does not change that stage order. It makes the first `code-review` pass independently credible by requiring independent-review mode, a first-pass review record before review-driven fixes begin, evidence-backed clean outcomes, and explicit `inconclusive` behavior when the reviewer cannot inspect enough evidence.

The goal is credible review outcomes, not a higher comment count. A clean result remains valid when it is grounded in the actual diff, upstream artifacts, checklist coverage, and validation evidence.

## Glossary

- `independent-review mode`: a `code-review` mode that grounds the review in the actual diff, upstream artifacts, checklist coverage, and validation evidence rather than implementation intent or chat memory alone.
- `first-pass review record`: the initial `code-review` result emitted before any review-driven fixes are applied.
- `workflow-managed run`: a full-feature execution flow where the agent is carrying the change through its normal downstream stages toward completion.
- `isolated code-review request`: a direct request for `code-review` output only, without downstream continuation.
- `review-only request`: a request whose goal is critique, audit, or readiness assessment rather than downstream execution.
- `no-finding rationale`: the explicit explanation of why a clean review found no blocking, major, or minor issues after checking the required review inputs and coverage.
- `sensitive change classes`: changes affecting security-sensitive behavior, workflow order or stage policy, CI behavior, schemas, architecture boundaries, or compatibility-sensitive contributor expectations.
- `clean-with-notes`: a passing first-pass review status that may still include positive notes, nits, or other non-blocking observations.
- `changes-requested`: a first-pass review status indicating one or more fixable findings within current approved scope and with sufficient evidence to act.
- `blocked`: a first-pass review status indicating the review cannot safely auto-enter `review-resolution` under current approved scope without a new decision.
- `inconclusive`: a first-pass review status indicating the reviewer cannot inspect enough evidence to produce a credible clean or actionable result.

## Examples first

### Example E1: workflow-managed clean review continues to verify

Given a full-feature change has completed `implement`
When `code-review` enters automatically and inspects the actual diff, upstream artifacts, checklist coverage, and validation evidence
Then it emits a first-pass review record with status `clean-with-notes`, includes a no-finding rationale, and continues to `verify` when no stop condition applies.

### Example E2: fixable findings become visible before review-resolution

Given a workflow-managed run reaches `code-review`
When the reviewer finds fixable issues within current approved scope
Then the first-pass review record lists those findings before fixes begin, and the workflow automatically enters `review-resolution` when no stop condition applies.

### Example E3: isolated code-review stops after the first-pass record

Given the user asks only for `code-review`
When the reviewer finds actionable issues
Then `code-review` emits the first-pass review record and stops instead of entering `review-resolution`.

### Example E4: missing evidence produces an inconclusive result only when no supported finding remains

Given `code-review` cannot inspect enough evidence to ground a clean result
And the available review surface does not independently support a fixable or blocking finding
When the review runs
Then the result is `inconclusive`, the missing evidence is reported explicitly, and the workflow does not enter `review-resolution`.

### Example E5: decision-requiring findings block instead of auto-fixing forward

Given `code-review` finds an issue that requires a product decision, spec approval, architecture approval, ADR approval, or scope expansion
When the first-pass review record is produced
Then the result is `blocked` and the workflow stops instead of auto-entering `review-resolution`.

### Example E6: sensitive change classes require stronger coverage

Given a change affects workflow stage policy or CI behavior
When the first-pass review record is emitted
Then the record includes explicit coverage of the relevant governing requirements or checklist items instead of only a generic clean summary.

## Requirements

R1. When `code-review` is entered from `implement` in a workflow-managed full-feature run, it MUST run in independent-review mode.

R1a. Independent-review mode MUST ground the review in the actual diff or changed files, approved upstream artifacts, checklist coverage, and available validation evidence rather than implementation intent or chat memory alone.

R1b. This feature MUST NOT require hard fresh-session enforcement as part of this slice.

R1c. When a fresh session, separate reviewer, or separate agent is available, `code-review` SHOULD prefer it.

R2. `code-review` MUST produce a first-pass review record before any review-driven fix is applied or `review-resolution` work begins.

R2a. The first-pass review record MUST include:
- review status;
- review inputs;
- diff summary;
- findings;
- checklist coverage;
- no-finding rationale when no findings exist; and
- recommended next stage.

R2b. Surfacing findings first MUST mean the findings are visible before fixes begin. It MUST NOT create a new user decision gate unless a stop condition applies.

R2c. This feature MUST NOT require a new standalone review artifact solely to preserve the first-pass review record. Existing workflow and docs-changes rules remain authoritative for when standalone `review-resolution.md` is required.

R3. The first-pass review status MUST be one of:
- `clean-with-notes`;
- `changes-requested`;
- `blocked`; or
- `inconclusive`.

R3a. `clean-with-notes` MUST mean the review passes and no unresolved accepted fix is required before `verify`.

R3b. `changes-requested` MUST mean the reviewer identified one or more fixable findings within current approved scope and with sufficient evidence to act.

R3c. `blocked` MUST mean the review cannot safely auto-enter `review-resolution` under current approved scope without a new decision.

R3d. Issues that are clearly fixable within current approved scope and with sufficient evidence to act MUST use `changes-requested`, not `blocked`.

R3e. `inconclusive` MUST mean the reviewer cannot inspect enough evidence to produce a credible clean or actionable result.

R4. In a workflow-managed full-feature run, `clean-with-notes` MUST continue to `verify` when no stop condition applies.

R4a. In a workflow-managed full-feature run, `changes-requested` MUST automatically continue to `review-resolution` when no stop condition applies.

R4b. In a workflow-managed full-feature run, `blocked` MUST stop and report the blocker.

R4c. In a workflow-managed full-feature run, `inconclusive` MUST stop and report the missing evidence. It MUST NOT enter `review-resolution`.

R4d. In an isolated or review-only request, `code-review` MUST stop after the first-pass review record.

R5. `code-review` MUST NOT automatically enter `review-resolution` when any of the following applies:
- the request is review-only;
- the request is an isolated `code-review` request;
- findings require a product decision;
- findings require spec approval;
- findings require architecture or ADR approval;
- findings require scope expansion;
- a higher-priority repository policy requires human review for the finding;
- the result is `inconclusive`;
- the reviewer cannot inspect the actual diff, relevant tests, or authoritative upstream artifacts; or
- the user explicitly asked to stop after review.

R6. A clean review outcome MUST be evidence-backed.

R6a. A `clean-with-notes` first-pass review record MUST identify the review inputs, checklist coverage, diff summary, and no-finding rationale grounding the result in the actual diff, upstream artifacts, and validation evidence.

R6b. A review MUST NOT claim a credible clean result when the reviewer cannot inspect the required evidence. It MUST use `inconclusive` when missing evidence prevents both a supported finding and a clean conclusion.

R6c. Passing tests alone or remembered implementation reasoning alone MUST NOT be treated as a sufficient basis for `clean-with-notes`.

R6d. A clean review MUST NOT require positive notes.

R6e. Positive notes in a clean review SHOULD appear only when they provide specific, evidence-backed information useful to future maintainers.

R6f. A review that says only "looks good" or uses generic praise without checklist coverage and no-finding rationale MUST be treated as invalid.

R7. For changes in the sensitive change classes, the first-pass review record MUST include explicit coverage of the relevant governing requirements, risks, or checklist items rather than only a generic clean summary.

R8. This feature MUST preserve the existing autoprogression boundaries from `specs/workflow-stage-autoprogression.md`.

R8a. This feature MUST preserve automatic `implement -> code-review` handoff in workflow-managed full-feature runs.

R8b. This feature MUST preserve the existing `code-review -> review-resolution -> code-review` loop for fixable findings in workflow-managed full-feature runs.

R8c. This feature MUST preserve isolated `code-review` behavior by default for review-only or direct isolated requests.

R8d. This feature MUST NOT require a human reviewer or mandatory second-pass reviewer for every non-trivial change.

## Inputs and outputs

Inputs:

- the actual diff or changed files for the review;
- the approved spec and related upstream artifacts such as test spec, plan, architecture document, or ADR when they exist and are relevant;
- available validation evidence;
- invocation context identifying workflow-managed, isolated, or review-only behavior;
- explicit user pause or stop instructions; and
- any higher-priority repository policy that requires human review for a finding class.

Outputs:

- a first-pass review record with status, inputs, diff summary, findings, checklist coverage, no-finding rationale when applicable, and recommended next stage;
- automatic continuation to `review-resolution` or `verify` when the workflow-managed status mapping allows it; or
- an explicit blocker or missing-evidence result when continuation stops.

## State and invariants

- No review-driven fix is applied before the first-pass review record exists.
- Independent-review mode is required for autoprogressed `code-review` after `implement`.
- A clean review outcome is not valid without evidence-backed checklist coverage and no-finding rationale.
- `inconclusive` never auto-enters `review-resolution`.
- Isolated or review-only `code-review` does not auto-continue.
- Existing standalone `review-resolution.md` trigger rules remain unchanged by this feature.

## Error and boundary behavior

- If `code-review` cannot inspect the actual diff, the result MUST be `inconclusive`.
- If authoritative upstream artifacts needed to ground a clean result are unavailable, `code-review` MUST NOT return `clean-with-notes`. It MAY still return `changes-requested` or `blocked` when the inspectable review surface independently supports a finding; otherwise the result MUST be `inconclusive`.
- If findings require a product, spec, architecture, ADR, or scope decision, the result MUST be `blocked`.
- If the user explicitly asks to stop after review, `code-review` MUST stop after the first-pass review record even when the findings are otherwise fixable.
- If a higher-priority repository policy requires human review for a sensitive finding, the workflow MUST stop instead of auto-entering `review-resolution`.
- If the first-pass review record omits required fields from `R2a`, the review result is incomplete.

## Compatibility and migration

- This feature is a workflow and skill-contract clarification, not a runtime product migration.
- It preserves the existing autoprogression stage order and stop-condition model from `specs/workflow-stage-autoprogression.md`.
- It does not expand autoprogression into fast-lane or bugfix execution.
- It does not require hard fresh-session enforcement.
- It does not require a new standalone `review-resolution.md` artifact by default.
- Existing `code-review` outputs that only say "approve, no findings" are no longer sufficient after this feature lands; clean outcomes must include the required evidence-backed fields.

## Observability

- `code-review` output MUST state the first-pass review status explicitly.
- `code-review` output MUST identify the review inputs, checklist coverage, and findings or no-finding rationale.
- When workflow-managed continuation occurs, the output SHOULD make clear whether the next stage is `review-resolution` or `verify`.
- When continuation stops, the output MUST identify whether the reason is blocker, missing evidence, isolated request, review-only mode, or explicit user pause.

### Recommended clean review template

```md
# Code Review

## Review status

clean-with-notes

## Review inputs

- Diff range:
- Spec:
- Test spec:
- Plan milestone:
- Architecture / ADR:
- Validation evidence:

## Diff summary

<What changed, based on the actual diff.>

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | pass | <evidence> |
| Test coverage | pass | <evidence> |
| Edge cases | pass | <evidence> |
| Error handling | pass | <evidence> |
| Architecture boundaries | pass | <evidence> |
| Compatibility | pass | <evidence> |
| Security/privacy | pass | <evidence> |
| Generated output drift | pass | <evidence> |
| Unrelated changes | pass | <evidence> |

## No-finding rationale

No blocking findings were found because:

- the diff matches the approved spec and plan scope
- tests cover the changed behavior
- no unrelated files are present in the reviewed diff
- validation evidence supports the implemented behavior

## Residual risks

- None identified.
```

## Security and privacy

- The first-pass review record MUST NOT expose secrets, credentials, or sensitive runtime values from the diff or validation outputs.
- This feature MUST NOT introduce any new network, secret, or credential dependency.
- When a higher-priority repository policy requires human review for a security-sensitive finding, that policy takes precedence over automatic entry into `review-resolution`.

## Performance expectations

- No product runtime performance change is expected.
- The feature may add one explicit first-pass review record before fix application, but it MUST NOT require duplicate manual confirmation or mandatory second-pass review for ordinary non-trivial work.

## Edge cases

1. A workflow-managed clean review continues to `verify` only when it includes checklist coverage and no-finding rationale.
2. Fixable findings become visible before `review-resolution` begins.
3. A review-only or isolated `code-review` request stops after the first-pass review record.
4. Missing diff produces `inconclusive`, and missing authoritative upstream artifacts prevent a clean result unless the review surface independently supports `changes-requested` or `blocked`.
5. Findings that require product, spec, architecture, ADR, or scope decisions produce `blocked`.
6. Sensitive change classes require stronger explicit coverage than a generic clean summary.
7. An explicit user request to stop after review overrides automatic entry into `review-resolution`.
8. This feature does not create a new standalone review artifact requirement by itself.
9. Positive notes remain optional in clean reviews; a clean review stays valid without them when checklist coverage and no-finding rationale are present.

## Non-goals

- Reverting `implement -> code-review` autoprogression.
- Requiring hard fresh-session enforcement.
- Requiring a human reviewer or mandatory second-pass reviewer for every non-trivial change.
- Expanding autoprogression into fast-lane or bugfix execution.
- Redefining when standalone `review-resolution.md` is required.
- Treating a higher review comment count as the success metric for this feature.
- Requiring generic praise or positive-note boilerplate in every clean review.

## Acceptance criteria

- A reviewer can see that autoprogressed `code-review` requires independent-review mode.
- A reviewer can see the required contents of the first-pass review record.
- A reviewer can see the status mapping for `clean-with-notes`, `changes-requested`, `blocked`, and `inconclusive`.
- A reviewer can see that workflow-managed fixable findings auto-enter `review-resolution` without adding a new user decision gate.
- A reviewer can see that clean outcomes require evidence-backed checklist coverage and no-finding rationale.
- A reviewer can see that positive notes are optional and that generic praise without checklist coverage is invalid.
- A reviewer can see that isolated or review-only `code-review` stops after the first-pass record.
- A reviewer can see that sensitive change classes require stronger explicit coverage.
- A reviewer can see that this feature does not require hard fresh-session enforcement or mandatory human review for every change.

## Open questions

- None.

## Next artifacts

- `plan`
- `plan-review`
- `test-spec`

## Follow-on artifacts

- `specs/code-review-independence-under-autoprogression.test.md`
- `docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`

## Readiness

- This spec is approved.
- No separate architecture artifact is expected for the first slice.
- The active plan and active test spec now exist.
- The next stage is `implement`.
