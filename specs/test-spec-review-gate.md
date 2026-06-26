# Test-Spec-Review Gate

## Status

approved

## Related proposal

- [Independent Test-Spec-Review Gate for Proof-Map Adequacy](../docs/proposals/2026-06-25-independent-test-spec-review-gate.md)

## Goal and context

RigorLoop needs an independent pre-implementation review gate for active test specs. The gate verifies whether the active test spec is a complete, executable, and traceable proof map for the approved feature spec, required architecture, approved plan, and clean plan-review before implementation consumes that proof map.

The change adds a `test-spec-review` stage between `test-spec` and `implement`. It preserves the test-spec artifact state as `active`; approval is recorded in a separate formal review artifact.

## Glossary

- `test-spec-review`: the formal review stage that assesses proof-map adequacy before implementation.
- `proof map`: the active test spec's mapping from requirements, examples, edge cases, architecture decisions, and plan milestones to tests, manual proofs, validation commands, fixtures, and evidence.
- `implementation handoff`: a deterministic routing field that says whether implementation may rely on the reviewed proof map.
- `substantive test-spec change`: a change that affects proof obligations, mapping, commands, fixtures, manual proof, milestone alignment, automation level, pass/fail criteria, or non-goal treatment.
- `non-substantive test-spec change`: a formatting, typo, link-only, heading-fix, or list-reordering edit that does not alter proof obligations.

## Examples first

Example E1: complete proof map is approved
Given an active test spec maps every in-scope requirement, example, edge case, and milestone to automated tests or explicit manual proof
When `test-spec-review` runs with the approved spec, required architecture, approved plan, and clean plan-review evidence
Then the review may return `Review status: approved`
And `Implementation handoff: allowed`.

Example E2: missing failure proof blocks implementation
Given the approved feature spec defines an error behavior
And the active test spec only covers the happy path
When `test-spec-review` runs
Then the review returns `changes-requested`
And `Implementation handoff: not-allowed`.

Example E3: upstream ambiguity routes upstream
Given the active test spec cannot map a proof because the approved spec and plan contradict each other
When `test-spec-review` runs
Then the review returns `blocked`
And the immediate next stage is the owning upstream revision stage, not implementation.

Example E4: isolated advisory review does not authorize implementation
Given a user manually invokes `test-spec-review` outside workflow-managed lifecycle recording
When the review is clean
Then the output may be advisory
But it does not establish formal implementation eligibility.

Example E5: low-risk command check stays bounded
Given the test spec references a current command
When the reviewer needs to validate the command name or shape
Then the reviewer may run only low-risk resolvability, help-text, or dry-run checks with no fixture setup, side effects, or network dependence.

## Requirements

R1. The standard workflow MUST place `test-spec-review` after `test-spec` and before `implement`.

R2. Formal workflow-managed implementation MUST NOT begin until the active test spec has a latest applicable `test-spec-review` with `Review status: approved`, `Implementation handoff: allowed`, no open material findings, and no later substantive test-spec change.

R3. Test specs MUST retain the durable artifact state `active`; `approved` and `changes-requested` MUST NOT become test-spec artifact states.

R4. `test-spec-review` approval MUST be recorded in a separate formal review artifact for workflow-managed reviews.

R5. The review status enum MUST be closed to `approved`, `changes-requested`, `blocked`, and `inconclusive`.

R6. The implementation-handoff enum MUST be closed to `allowed` and `not-allowed`.

R7. `Review status: approved` MUST map to `Implementation handoff: allowed`; all other review statuses MUST map to `Implementation handoff: not-allowed`.

R8. The immediate-next-stage enum MUST be closed to `test-spec revision`, `spec revision`, `architecture revision`, `plan revision`, `review-resolution`, `implement`, and `none`.

R9. `Immediate next stage: implement` MUST be used only with `Review status: approved`.

R10. A `changes-requested` review MUST identify proof-map defects in the test spec itself and route to `test-spec revision` or `review-resolution` as appropriate.

R11. A `blocked` review MUST identify the upstream missing or contradictory contract and route to `spec revision`, `architecture revision`, `plan revision`, or `none`.

R12. An `inconclusive` review MUST identify the specific evidence gap, explain why it prevents a proof-map adequacy judgment, and name the smallest evidence needed to make a later review conclusive.

R13. The review MUST assess traceability from requirements, acceptance criteria, examples, edge cases, architecture decisions, and plan milestones to test IDs, manual proof IDs, validation commands, fixtures, and evidence.

R14. The review MUST treat happy-path-only proof as a material defect when the approved contract defines failure, permission, compatibility, migration, rollback, security, or error behavior.

R15. Manual proof entries MUST name a stable ID, automation rationale, exact steps, required environment, evidence artifact, pass condition, failure condition, and owning stage.

R16. Validation commands referenced by the test spec MUST be classified as existing and configured, planned with owner and milestone, manual only, or external/release-owned.

R17. Review-time command execution MUST be optional and bounded to low-risk resolvability, help-text, or dry-run checks with no fixture setup, side effects, secrets, or network dependence.

R18. Fixtures and test data described by the test spec MUST be deterministic, isolated, safe, representative, and cleaned up when relevant.

R19. An approved review MUST become stale after a substantive test-spec change.

R20. Formatting, typo, link-only, heading-fix, or list-reordering edits MUST NOT automatically stale an approved review when a reviewer or workflow check confirms proof obligations are unchanged.

R21. If upstream `spec revision`, `architecture revision`, or `plan revision` is required, the current test spec MUST NOT be considered implementation-eligible until the upstream artifact is settled and the proof map is revised or explicitly confirmed current by a later review.

R22. Formal `test-spec-review` records MUST live under `docs/changes/<change-id>/reviews/test-spec-review-r<n>.md` and update `docs/changes/<change-id>/review-log.md`.

R23. A clean formal review MUST NOT require an empty `review-resolution.md`; material findings or blocking outcomes that require disposition MUST create or update `review-resolution.md`.

R24. The `test-spec-review` skill MUST NOT claim test implementation, production implementation, code-review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout.

R25. The `test-spec` skill MUST route formal workflow-managed output to `test-spec-review`, not directly to `implement`.

R26. The `implement` skill MUST require an active test spec plus approved, current, recorded `test-spec-review` evidence before implementation eligibility.

R27. Review validators MUST reject unknown review statuses, immediate-next-stage values, implementation-handoff values, and inconsistent status/handoff/stage combinations before consistency checks.

R28. Generated and installed skill packages MUST include the new `test-spec-review` skill and mapped assets through normal generation, not hand-edited generated output.

## Inputs and outputs

Inputs:

- active test spec;
- approved feature spec;
- approving spec-review evidence;
- approved plan;
- clean plan-review evidence;
- approved architecture and architecture-review when required;
- project workflow guide when routing or artifact placement matters;
- command manifests, CI configuration, fixtures, schemas, migrations, or source seams only when the test spec relies on them.

Outputs:

- formal review result with review status, material findings, recording status, review record, review log, review resolution status, open blockers, immediate next stage, implementation handoff, and stop condition;
- material findings with finding ID, severity, location, evidence, required outcome, safe resolution path, and `needs-decision` rationale when applicable;
- review-log entry for formal workflow-managed reviews.

## State and invariants

- Test-spec artifact state remains `active`.
- Review approval lives in formal review evidence, not in the test-spec artifact state.
- Implementation eligibility depends on the latest applicable review and staleness state.
- A stale review is not implementation-eligible.
- Formal review records are durable lifecycle evidence; isolated advisory reviews do not imply workflow eligibility.

## Error and boundary behavior

- Missing target test spec returns `blocked` or `inconclusive`.
- Non-active target test spec returns `blocked`.
- Missing approved feature spec, required architecture approval, approved plan, or clean plan-review returns `blocked`.
- Missing evidence needed to judge adequacy returns `inconclusive`.
- Defects inside an otherwise reviewable test spec return `changes-requested`.
- Unknown enum values fail validation before handoff consistency is evaluated.
- Upstream contradictions route to the owning upstream artifact stage instead of being repaired inside the test spec.

## Compatibility and migration

The change applies forward to formal workflow-managed test specs. Existing historical test specs are not retroactively migrated in the first slice.

Workflow guidance, `specs/rigorloop-workflow.md`, `specs/skill-contract.md` when needed, canonical skills, validators, and generated adapter support surfaces must be updated together. Generated public adapter skill bodies must be produced through normal generation.

Rollback restores `test-spec -> implement`, removes `test-spec-review` from workflow routing and generated packages, restores `test-spec` and `implement` skill wording together, and preserves already-created review evidence as historical.

## Observability

Review results expose the reviewed target, review status, material finding IDs, recording status, review record path, review log path, review-resolution path or not-required status, immediate next stage, implementation handoff, and stop condition.

Failures must identify the requirement, example, edge case, command, fixture, milestone, or upstream artifact that made the proof map inadequate or unreviewable.

## Security and privacy

The review must not require secrets, credentials, private network access, or side-effecting external systems. Manual proof and fixture guidance must avoid exposing sensitive data and must identify safe evidence artifacts.

## Accessibility and UX

Not applicable for end-user UI. Contributor-facing skill output must be concise, scan-first, and explicit about whether implementation is allowed.

## Performance expectations

Review should start from bounded evidence and inspect the smallest sufficient surfaces. It should distinguish fast focused proof checks from expensive release or boundary checks without weakening coverage.

## Edge cases

EC1. A test spec with complete happy-path tests but missing required error behavior returns `changes-requested`.

EC2. A test spec that references a nonexistent command with no owner or milestone returns `changes-requested` when the test spec can be revised, or `blocked` when command ownership depends on an upstream contract.

EC3. A manual proof that says only "verify manually" returns `changes-requested`.

EC4. A typo-only test-spec edit after approval does not stale the review when proof obligations are unchanged.

EC5. A plan revision after review makes implementation handoff unavailable until review confirms the proof map still applies or a revised test spec is reviewed.

EC6. An isolated advisory review with `approved` status does not satisfy formal workflow-managed implementation eligibility.

## Non-goals

- Do not make `test-spec-review` author the test spec.
- Do not reapprove product requirements or architecture.
- Do not implement tests or production code.
- Do not execute final validation or claim validation success.
- Do not replace `code-review`, `verify`, or downstream review backstops.
- Do not require a different model or vendor for this stage.
- Do not retroactively review historical test specs in the first slice.
- Do not add numeric proof-map scoring.

## Acceptance criteria

AC-TSR-001. A reviewer can tell that the standard workflow places `test-spec-review` between `test-spec` and `implement`.

AC-TSR-002. A reviewer can tell that test specs retain `Status: active` and review approval is recorded separately.

AC-TSR-003. A validator can reject unsupported review status, immediate-next-stage, and implementation-handoff values.

AC-TSR-004. A validator can reject `changes-requested` with `Implementation handoff: allowed`.

AC-TSR-005. A complete proof-map fixture can receive `approved` and `Implementation handoff: allowed`.

AC-TSR-006. Missing requirement, negative-case, command, fixture, or vague-manual-proof coverage produces non-approval.

AC-TSR-007. A substantive test-spec edit after approval makes implementation handoff unavailable until re-review.

AC-TSR-008. Generated packages include `test-spec-review` and its assets.

AC-TSR-009. Code-review and verify remain required backstops and do not become weaker because this gate exists.

## Open questions

None. The proposal's candidate decisions are settled by this spec.

## Next artifacts

```text
spec-review
architecture assessment
architecture, if required
architecture-review, if required
plan
plan-review
test-spec
```

## Follow-on artifacts

None yet

## Readiness

Approved after clean recorded `spec-review`. Current workflow state is owned by the active plan.
