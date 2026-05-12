# Downstream Status Settlement Before Reliance

## Status

approved

## Related proposal

[Downstream Status Settlement Before Reliance](../docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md), accepted.

## Goal and context

This spec defines the first downstream status-settlement slice for `spec`, `architecture`, and `plan`.

The goal is to prevent downstream skills from relying on stale upstream lifecycle status when durable review evidence clearly supports a deterministic status update. Formal review skills remain focused on review evidence and material-finding recording. Downstream authoring skills settle only minimal upstream lifecycle metadata before relying on upstream artifacts.

This first slice implements the chain:

```text
proposal -> spec
spec -> architecture
spec/architecture -> plan
```

Later slices may extend the model to `test-spec`, `implement`, `explain-change`, `verify`, and `pr`, but this spec does not authorize those skills to perform downstream settlement.

## Glossary

- **Downstream skill**: a workflow-managed skill that is about to rely on a prior lifecycle artifact.
- **Upstream artifact**: a lifecycle artifact used as governing input by the downstream skill.
- **Settlement**: a minimal update to an upstream artifact's lifecycle/status/readiness/follow-on/closeout metadata so the artifact matches clear review evidence.
- **Clear review evidence**: durable review evidence that satisfies the requirements in this spec and supports exactly one settlement result.
- **Stale status**: an upstream artifact status that contradicts clear review evidence.
- **Substantive content**: artifact body content that changes requirements, design, plan scope, rationale, or implementation behavior rather than lifecycle metadata.

## Examples first

### Example E1: `spec` settles an approved proposal

Given:

- `docs/proposals/example.md` says `Status: draft`;
- durable proposal-review evidence says `approved`;
- no later proposal-review record contradicts approval;
- no open material findings remain.

When:

- `spec` relies on `docs/proposals/example.md`;

Then:

- `spec` updates the proposal status to `accepted`;
- `spec` reports `Upstream status settlement` with `Settlement result: updated`;
- `spec` may continue.

### Example E2: `architecture` settles an approved spec

Given:

- `specs/example.md` says `Status: draft`;
- durable spec-review evidence says `approved`;
- no unresolved material findings remain.

When:

- `architecture` relies on `specs/example.md`;

Then:

- `architecture` updates the spec status to `approved`;
- `architecture` reports `Settlement result: updated`;
- `architecture` may continue.

### Example E3: unresolved findings block settlement

Given:

- `specs/example.md` has spec-review approval in one record;
- `review-log.md` lists an open finding for the same spec;

When:

- `plan` relies on `specs/example.md`;

Then:

- `plan` does not update the spec status;
- `plan` reports `Settlement result: blocked`;
- `plan` reports `New status: approved` because the deterministic target is known;
- `plan` names unresolved findings as the blocker.

### Example E4: unmapped artifact blocks settlement

Given:

- `plan` relies on an upstream artifact whose status vocabulary is not listed in this spec;

When:

- `plan` detects stale or ambiguous lifecycle status;

Then:

- `plan` does not guess the settlement;
- `plan` reports `Settlement result: blocked`;
- `plan` reports `New status: not-applicable`;
- `plan` names the missing mapping.

### Example E5: already settled input needs no output

Given:

- a proposal already says `Status: accepted`;
- proposal-review approval has no unresolved findings;

When:

- `spec` relies on the proposal;

Then:

- `spec` may omit `Upstream status settlement`, or report `Settlement result: not-needed` if useful.

## Requirements

### Scope

R1. The first implementation slice MUST apply only to workflow-managed executions of `spec`, `architecture`, and `plan`.

R2. The first implementation slice MUST NOT authorize downstream settlement by `test-spec`, `implement`, `explain-change`, `verify`, or `pr`.

R3. The first implementation slice MUST NOT add artifact-status sync ownership to formal review skills.

R4. Review-only, no-edit, or manual inspection requests MUST remain isolated and MUST NOT enter downstream settlement behavior.

### Settlement permission and edit boundary

R5. In workflow-managed downstream execution, `spec`, `architecture`, and `plan` MAY perform minimal upstream lifecycle/status settlement before relying on an upstream artifact.

R6. Downstream settlement MUST edit only lifecycle/status/readiness/follow-on/closeout metadata.

R7. Downstream settlement MUST NOT rewrite substantive proposal, spec, architecture, ADR, plan, test, implementation, or review content.

R8. Downstream settlement MUST NOT ask whether edits are allowed during normal workflow-managed downstream execution.

### Clear review evidence

R9. A downstream skill MUST treat review evidence as clear only when all of the following are true:

- durable formal review evidence exists for the relevant upstream artifact;
- the review outcome is approving or clean for the relevant artifact;
- no later durable review record contradicts that outcome;
- `review-log.md`, when present for the change, lists no open findings for the relevant artifact;
- `review-resolution.md`, when required, has closed all material findings for the relevant artifact;
- the artifact-status mapping is explicitly defined by this spec.

R10. If any clear-review-evidence condition is not met, the downstream skill MUST NOT settle the upstream artifact and MUST report `Settlement result: blocked` when settlement is relevant to reliance.

### Initial settlement mappings

R11. When `spec` relies on a proposal with clear proposal-review approval and no unresolved material findings, `spec` MUST settle stale proposal status to `accepted`.

R12. When `architecture` relies on a spec with clear spec-review approval and no unresolved material findings, `architecture` MUST settle stale spec status to `approved`.

R13. When `plan` relies on a spec with clear spec-review approval and no unresolved material findings, `plan` MUST settle stale spec status to `approved`.

R14. When `plan` relies on an architecture package with clear architecture-review approval and no unresolved material findings, `plan` MUST settle stale architecture status to `approved`.

R15. When `plan` relies on an ADR with clear architecture-review approval and no unresolved material findings, `plan` MAY settle the ADR only when the ADR already exposes a lifecycle/status field with a known target status of `accepted` or `active`.

R16. If an ADR's lifecycle/status field is absent, ambiguous, or uses a vocabulary that does not clearly support `accepted` or `active`, `plan` MUST report `Settlement result: blocked` and name the missing mapping.

R17. If an artifact type, lifecycle field, or next status is not listed in this spec, the downstream skill MUST NOT infer a settlement and MUST report `Settlement result: blocked` when settlement is relevant to reliance.

R17a. When blocked settlement occurs because no deterministic target status exists, the settlement output MUST set `New status` to `not-applicable`.

### Settlement output

R18. A downstream skill MUST report an `Upstream status settlement` block when status was updated.

R19. A downstream skill MUST report an `Upstream status settlement` block when settlement was blocked.

R20. A downstream skill MUST report an `Upstream status settlement` block when stale upstream status was detected.

R21. A downstream skill MAY omit the settlement block when no upstream lifecycle artifact is relied on, all relied-on upstream artifacts are already settled, or settlement is irrelevant to the task.

R22. When the settlement block is reported, it MUST include:

- upstream artifact;
- review evidence;
- previous status;
- new status;
- settlement result;
- settlement blocker.

R23. `Settlement result` MUST be one of `updated`, `blocked`, or `not-needed`.

R23a. When `Settlement result: updated`, `New status` MUST be the status value written to the upstream artifact.

R23b. When `Settlement result: blocked` and the intended target status is deterministic, `New status` MUST be the intended target status.

R23c. When `Settlement result: blocked` because the artifact type, lifecycle field, status vocabulary, or target status is unknown or unmapped, `New status` MUST be `not-applicable`.

R23d. When `Settlement result: not-needed`, `New status` MAY be the already-settled current status or `not-applicable`, depending on whether a status check was performed.

R24. When `Settlement result: blocked`, `Settlement blocker` MUST name the missing, contradictory, unresolved, or unmapped condition.

R24a. For blocked settlement, `Settlement blocker` MUST distinguish between a known target blocked by evidence or state and an unknown target blocked by missing mapping or lifecycle vocabulary.

### Later slices and validation

R25. The spec MAY include later-slice notes for `test-spec`, `implement`, `explain-change`, `verify`, and `pr`, but those notes MUST NOT define operational requirements for those skills.

R26. Lifecycle-validator stale-status detection MUST NOT be required in the first implementation slice.

R27. A later lifecycle validator MAY detect stale upstream artifact status when clear review evidence exists and a downstream artifact relies on the upstream artifact.

## Inputs and outputs

Inputs:

- upstream proposal, spec, architecture package, or ADR;
- durable formal review evidence;
- `review-log.md` when present;
- `review-resolution.md` when material findings or another trigger require it;
- downstream skill invocation context.

Outputs:

- optionally updated upstream lifecycle/status metadata;
- `Upstream status settlement` output when required by this spec;
- downstream continuation only when settlement is not blocked.

Required settlement output shape when reported:

```md
## Upstream status settlement

- Upstream artifact:
- Review evidence:
- Previous status:
- New status:
- Settlement result: updated | blocked | not-needed
- Settlement blocker:
```

`New status` is either the settled or intended target status, or `not-applicable` when no deterministic target exists.

`Settlement blocker` is required when `Settlement result: blocked`; otherwise it may be `none`.

## State and invariants

- Artifacts remain the durable source of truth.
- Review skills record evidence; downstream skills settle status before reliance.
- Settlement must be deterministic.
- Unknown mappings block settlement.
- Unresolved material findings block settlement.
- Review-only isolation blocks downstream settlement because downstream execution has not started.

## Error and boundary behavior

E1. Missing review evidence: settlement blocks.

E2. Contradictory review evidence: settlement blocks.

E3. Later review contradicts earlier approval: settlement blocks.

E4. Open material findings: settlement blocks.

E5. Required `review-resolution.md` missing or open: settlement blocks.

E6. Missing upstream status surface: settlement blocks.

E7. Unknown artifact type, lifecycle field, or next status: settlement blocks.

E8. ADR lifecycle vocabulary absent or ambiguous: settlement blocks.

E9. Already settled upstream artifact: settlement output is optional or `not-needed`.

E10. Direct review-only or no-edit invocation: no downstream settlement occurs.

E11. Blocked proposal settlement with known target and unresolved findings: settlement output uses `New status: accepted`.

E12. Blocked ADR settlement with unknown target: settlement output uses `New status: not-applicable`.

## Compatibility and migration

Existing reviewed artifacts do not need bulk migration. Settlement occurs only when a first-slice downstream skill runs and relies on a touched upstream artifact.

Existing formal review records remain valid. This spec does not change review-recording requirements or review-result vocabulary.

Generated skills and adapter output must be refreshed after canonical skill changes.

## Observability

Settlement is observable through:

- the upstream artifact metadata diff when a status is updated;
- `Upstream status settlement` output when settlement is updated, blocked, or stale status is detected;
- validation evidence in the active plan or change-local metadata when this behavior is implemented.

Lifecycle-validator stale-status detection is deferred. If added later, initial validation should be explicit-path or warning mode until settlement mappings are stable.

## Security and privacy

This change does not introduce new secrets, authentication, authorization, or private-data handling.

The main safety boundary is preventing downstream skills from rewriting substantive upstream content under the guise of status settlement.

## Accessibility and UX

No UI behavior is involved.

## Performance expectations

Settlement checks should use targeted upstream artifact and review evidence reads. They should not require broad repository searches when the upstream artifact and change-local review records are already known.

## Edge cases

EC1. A proposal has proposal-review approval but also later proposal-review changes-requested: settlement blocks.

EC2. A spec has spec-review approval, but `review-log.md` still lists an open finding for that spec: settlement blocks.

EC3. An architecture package has architecture-review approval, but no status field exists: settlement blocks.

EC4. An ADR has architecture-review approval, but no lifecycle vocabulary: settlement blocks.

EC5. `plan` relies on both spec and architecture; spec is settled but architecture is blocked: `plan` reports the architecture blocker and does not claim full upstream settlement.

EC6. `spec` is invoked as manual review-only/no-edit inspection rather than workflow-managed downstream execution: settlement does not run.

EC7. Upstream artifact is already settled and no stale status is detected: settlement output may be omitted.

## Non-goals

- No review-side artifact-status sync.
- No implementation for `test-spec`, `implement`, `explain-change`, `verify`, or `pr` in the first slice.
- No lifecycle-validator stale-status enforcement in the first slice.
- No bulk migration of historical artifact statuses.
- No substantive artifact rewrites during settlement.
- No change to formal review recording rules.

## Acceptance criteria

AC1. The spec defines first-slice settlement for `spec`, `architecture`, and `plan`.

AC2. The spec excludes `test-spec`, `implement`, `explain-change`, `verify`, and `pr` from first-slice operational settlement.

AC3. The spec defines clear review evidence.

AC4. The spec defines deterministic mappings for proposal, spec, architecture package, and ADR handling in the first slice.

AC5. Unknown lifecycle vocabulary blocks settlement.

AC6. Settlement output is required for updated, blocked, or stale-status-detected cases.

AC7. Already settled or irrelevant cases may omit settlement output or report `not-needed`.

AC8. The spec preserves review-skill independence and does not move artifact-status sync back into review skills.

AC9. The spec defers lifecycle-validator stale-status detection.

AC10. Blocked settlement output supports both known-target blockers and unknown-target blockers without inventing a target status.

## Open questions

None.

## Next artifacts

- spec-review
- plan
- test-spec
- implementation slice for `spec`, `architecture`, and `plan`

## Follow-on artifacts

- Spec-review R2: `docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/reviews/spec-review-r2.md`.

## Readiness

Approved. Ready for execution planning before test-spec and implementation.
