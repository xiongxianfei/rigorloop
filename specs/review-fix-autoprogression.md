# Review-Fix Autoprogression

## Status

approved

## Related proposal

- [Bounded Review-Fix Autoprogression in Chat](../docs/proposals/2026-06-30-bounded-review-fix-autoprogression-in-chat.md)

## Goal and context

This spec defines an explicitly armed workflow mode that can run proposal-side lifecycle stages, apply only deterministic review fixes, rerun the same review, and continue until a requested target stage is complete.

The goal is to reduce repeated manual chat routing without weakening RigorLoop's review gates. Direct review requests remain isolated by default. Review evidence remains durable. The driver stops on judgment, ambiguity, unsafe edits, stale evidence, or exhausted budgets.

## Glossary

- `review-fix autoprogression`: the explicitly armed workflow-managed mode defined by this spec.
- `review-fix driver`: the workflow-owned orchestrator that runs preflight, invokes existing stage skills, classifies findings, applies eligible fixes, reruns review, and stops or continues toward the target stage.
- `target_stage`: the closed stage value where the armed loop must stop after successful completion.
- `stage pair`: an authoring stage and its matching review stage, such as `spec` and `spec-review`.
- `auto-safe finding`: a review finding that satisfies the closed criteria for deterministic automatic repair.
- `bounded safe fix`: a small edit applied by the driver after review evidence exists and before the same review is rerun.
- `profile-local cursor`: review-fix state fields that describe the current stage and review for safe resume and audit.

## Examples first

Example E1: direct review stays isolated
Given the user invokes `proposal-review`
When the review is approved
Then the system records the review result and does not create `workflow.autoprogression.review_fix` state or continue into `spec`.

Example E2: target-stage command arms the loop
Given the user invokes `$workflow auto: spec-review`
When the proposal gate is clean and the target stage is allowed
Then the system records `workflow.autoprogression.review_fix` authorization with `target_stage: spec-review` and continues only along the standard path toward `spec-review`.

Example E3: safe finding is fixed and rereviewed
Given an armed review-fix loop reaches `spec-review`
And the review records only deterministic `mechanical` findings within budget
When review evidence is recorded
Then the driver records planned disposition, applies the bounded fixes, records changed files and actual disposition, and reruns `spec-review`.

Example E4: owner decision stops the loop
Given an armed review-fix loop reaches `architecture-review`
When a finding requires choosing between two architecture boundaries
Then the driver does not edit the artifact, records the stop reason, and asks for owner decision.

Example E5: target boundary stops continuation
Given the user invokes `$workflow auto: plan-review`
When `plan-review` is approved and recorded
Then the driver marks the profile terminal and does not invoke `test-spec`.

Example E6: budget exhaustion stops continuation
Given a review records six material findings
When the per-cycle auto-applied finding budget is five
Then the driver does not apply a partial hidden set of fixes and stops with the remaining findings and budget reason.

Example E7: stale review blocks fixing
Given the reviewed artifact changed after the review record was created
When the driver prepares to apply an otherwise auto-safe fix
Then the driver stops and requires a fresh review before mutation.

## Requirements

R1. The system MUST support the user-facing command shape `$workflow auto: <target-stage>` for review-fix autoprogression.

R2. The system MUST support `$workflow auto: status` to report current review-fix state without mutating artifacts.

R3. The system MUST support `$workflow auto: off` to clear or terminally cancel armed review-fix autoprogression.

R4. The system MUST persist review-fix authorization under `workflow.autoprogression.review_fix`.

R5. The `review_fix.profile` value MUST be the closed value `bounded-review-fix`.

R6. The `review_fix.status` value MUST be one of `off`, `armed`, `active`, `paused`, `completed`, or `cancelled`.

R7. The durable `review_fix.target_stage` value MUST be one of `proposal-review`, `spec`, `spec-review`, `architecture`, `architecture-review`, `plan`, `plan-review`, `test-spec`, or `test-spec-review`.

R8. The system MUST NOT persist raw arbitrary stage names as review-fix authority.

R9. The review-fix state MUST record `target_stage`, `profile`, `status`, `armed_by`, `armed_at`, `current_stage`, `current_review`, `stop_reason`, and `last_updated_evidence` when those values are known.

R9a. Review-fix activation MUST require durable user authorization plus a clean current gate for the current stage.

R9b. Proposal-start review-fix activation MUST require an accepted proposal, approved recorded proposal-review, no open proposal-review findings, closed proposal-review resolution when material findings existed, and unambiguous change ID and artifact placement.

R9c. An armed review-fix profile MUST become active only when its durable authorization exists and the current stage gate passes from tracked artifacts.

R9d. Direct review invocations MUST NOT activate, resume, or advance review-fix autoprogression even when review-fix state already exists.

R9e. Unknown, malformed, missing, or contradictory persisted review-fix state MUST pause the profile or stop before mutation and downstream continuation.

R9f. `$workflow auto: off`, target completion, cancellation, and completed terminal transitions MUST update `workflow.autoprogression.review_fix` deterministically in `change.yaml` or in the approved fallback policy surface when change metadata cannot carry the policy data.

R10. Direct manual invocations of `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `test-spec-review`, or `code-review` MUST NOT create review-fix authorization state.

R11. The review-fix loop MUST be limited to the proposal-side path `proposal -> proposal-review -> spec -> spec-review -> architecture when required -> architecture-review when required -> plan -> plan-review -> test-spec -> test-spec-review`.

R12. The review-fix loop MUST NOT invoke `implement`, `code-review`, `verify`, `pr`, release, publication, network, destructive, or external-state operations.

R13. The driver MUST run preflight before authoring, review, fix application, or downstream continuation.

R14. Preflight MUST resolve the change ID, target artifact path, review state, requested target stage, review-fix state, current artifact freshness, and next transition.

R15. Preflight MUST stop when artifact placement, change ID, review evidence, profile state, or next transition is ambiguous.

R16. The driver MUST use existing authoring and review skills for their owned stages rather than replacing their artifact or review authority.

R17. Review skills MUST remain independent review gates and MUST NOT edit the reviewed artifact during the review pass as part of this profile.

R18. The driver MUST record formal review evidence before applying review-driven fixes.

R19. The driver MUST rerun the same review after every applied fix cycle.

R20. The driver MUST NOT continue to the next stage until the current review is approved, recorded, current, and has no open material findings.

R21. The driver MUST stop when the target stage is reached.

R22. The driver MUST NOT continue past the armed target stage.

R22a. After approved recorded `spec-review`, the driver MUST record exactly one architecture assessment value before routing to `architecture`, `architecture-review`, or `plan`.

R22b. Architecture assessment values MUST be closed to `architecture-required`, `architecture-not-required`, and `architecture-ambiguous`.

R22c. `architecture-required` MUST route through `architecture` and `architecture-review` unless another stop condition applies.

R22d. `architecture-not-required` MUST skip `architecture` and `architecture-review`.

R22e. When `architecture-not-required` skips conditional stages, the driver MUST continue toward the next applicable target only when doing so does not exceed the user's target intent.

R22f. When the requested target stage is `architecture` or `architecture-review` and architecture assessment records `architecture-not-required`, the driver MUST stop with `target-not-applicable` rather than claiming the skipped target stage was reached.

R22g. `architecture-ambiguous` MUST stop for owner decision and MUST NOT choose between `architecture` and `plan`.

R23. The driver MUST classify every material finding before applying any fix in that cycle.

R24. The authoritative auto-fix classification MUST be computed by the driver, even when the review finding includes a hint.

R25. Auto-fix classifications MUST be closed to `mechanical`, `format-preserving`, `exact-reviewer-wording`, `status-normalization-with-evidence`, `recording-repair`, `cross-reference-repair`, `validation-command-shape-repair`, and `not-auto-safe`.

R26. A finding MUST be auto-safe only when it has a stable finding ID, evidence, deterministic required outcome, deterministic patch target, small diff, current reviewed artifact, and a same-review rerun path.

R27. A finding MUST NOT be auto-safe when it changes product direction, scope, requirements, architecture decisions, milestone sequencing, validation ownership, public behavior, release policy, external state, or generated output ownership.

R28. A finding with `needs-decision`, ambiguous alternatives, missing evidence, missing deterministic patch target, or reviewer-declared downstream block MUST stop the loop.

R29. `exact-reviewer-wording` MUST require target artifact, target section or line range, exact quoted replacement text, no owner-decision rationale, and no semantic scope change.

R30. The driver MUST apply at most 2 auto-fix and rereview cycles per review gate.

R31. The driver MUST auto-apply at most 5 material findings per cycle.

R32. The driver MUST change at most 3 files per cycle.

R33. The driver MUST change at most 10 files per chat invocation.

R34. Budget exhaustion MUST stop the loop and report the exhausted budget, remaining findings, changed files, review state, and required owner action.

R35. The driver MUST record planned and actual disposition for every auto-applied material finding in `review-resolution.md`.

R36. Auto-applied disposition records MUST include finding ID, driver classification, rationale, files changed, validation evidence, and rereview linkage.

R37. The driver MUST stop before applying fixes when the reviewed artifact changed after the review evidence being used.

R38. Generated or marker-owned artifacts MUST be changed only through their owning generator or canonical source; otherwise the driver MUST stop.

R39. The driver MUST mark review-fix state terminal or clear it when the target stage is reached, the user runs `$workflow auto: off`, a non-auto-safe blocker is encountered, or authorization is cancelled.

R40. A paused review-fix profile MUST NOT resume from manual fixes unless the user explicitly resumes and the tracked artifact and review evidence still match the profile-local cursor.

R41. The chat result for each run MUST report mode, target stage, current stage, review status, auto-applied fixes, human decisions required, artifacts changed, review rerun status, next stage run, and stop reason.

R42. Validators MUST fail closed on unknown review-fix profile values, target stages, status values, auto-fix classes, review statuses, and disposition values.

R43. Validators MUST reject state combinations that claim continuation past target stage, open findings with approved continuation, auto-applied fixes without rereview, stale review authorization, or closed closeout with unresolved findings.

R44. Existing `authoring-through-plan-review` and `implementation-through-verify` behavior MUST remain unchanged unless a later approved spec explicitly changes those profiles.

R45. The feature MUST NOT expose partial user-visible review-fix autoprogression before the full proposal-side contract through `test-spec-review` passes its acceptance criteria.

## Inputs and outputs

Inputs:

- User command: `$workflow auto: <target-stage>`, `$workflow auto: status`, or `$workflow auto: off`.
- Existing proposal-side artifacts and review records.
- Change-local metadata under `docs/changes/<change-id>/`.
- Existing authoring and review skill outputs.
- Review findings with IDs, evidence, required outcomes, and safe resolution paths or `needs-decision` rationale.

Outputs:

- Updated `workflow.autoprogression.review_fix` state.
- Authored or reviewed proposal-side lifecycle artifacts.
- Review records and `review-log.md` entries.
- `review-resolution.md` disposition entries for auto-applied material findings.
- Chat-visible run summary with changed artifacts, rerun status, stop reason, and next action.

## State and invariants

- Review-fix authorization lives only under `workflow.autoprogression.review_fix`.
- Review-fix state is profile-local evidence and does not own active plan state, branch readiness, PR readiness, or final workflow completion.
- Review gates remain authoritative. The driver cannot treat a fix as approved until the same review reruns cleanly.
- Direct review invocation isolation is preserved.
- The armed target stage is an upper bound, not permission to skip prerequisites.
- Arming the profile authorizes only auto-safe, budget-bounded fixes; unsafe findings always stop.
- No dry-run or apply-mode state exists in this first contract.

## Error and boundary behavior

- Unknown command target: reject with allowed `target_stage` values.
- Missing change ID or artifact path: stop without guessing.
- Missing review evidence: run the required review or stop if the review cannot be recorded.
- Blocked recording: stop and report the recording blocker.
- Architecture assessment records `architecture-ambiguous`: stop for owner decision.
- Architecture assessment records `architecture-not-required` while the target is `architecture` or `architecture-review`: stop with `target-not-applicable`.
- Stale review evidence: stop and require fresh review.
- Non-auto-safe finding: stop and report finding ID plus owner action.
- Budget exhaustion: stop with the exhausted budget and remaining work.
- Target reached: mark the profile `completed` or clear it according to the metadata contract.
- User cancellation: mark `cancelled` or clear state and do not resume without a new command.
- Contradictory profile or lifecycle state: stop and require state repair.

## Compatibility and migration

This is an additive workflow profile. Existing manual skill invocations remain isolated by default. Existing `authoring-through-plan-review` and `implementation-through-verify` profiles keep their current semantics.

Existing change records without `workflow.autoprogression.review_fix` state are treated as unarmed. No migration is required for historical reviews or proposals.

When the feature is disabled or rolled back, review records and review-resolution history remain valid evidence. Disabling the feature removes automatic continuation and automatic safe-fix application, not recorded lifecycle artifacts.

## Observability

Each run reports:

- command interpreted;
- target stage;
- current stage and review;
- profile status;
- review result;
- applied finding IDs and classifications;
- files changed;
- review rerun status;
- human-decision blockers;
- stop reason;
- next action.

Durable observability comes from review records, `review-log.md`, `review-resolution.md`, and review-fix metadata.

## Security and privacy

The driver must not run network, publication, release, destructive, credential-accessing, or external state-mutating commands under this profile. It must not expose secrets or rely on untracked private chat state as durable authorization.

Authorization must be explicit and durable. Session-only intent is not enough to resume after the active chat state is lost.

## Accessibility and UX

The command surface is text-only. User-visible output must be concise and scannable, with exact stop reasons and allowed targets. Error messages should name the invalid value and the allowed closed values.

## Performance expectations

Preflight should run before expensive authoring, review, or validation work. The loop budgets in R30 through R33 bound repeated review-fix cycles and file churn in one chat invocation.

## Edge cases

EC1. Direct `spec-review` after arming was not recorded in profile state; the review remains isolated unless the workflow command created durable review-fix authorization first.

EC2. A review includes four auto-safe findings and one `needs-decision` finding; the driver stops without applying fixes in that cycle.

EC3. A reviewer provides exact replacement text but no target section; the finding is `not-auto-safe`.

EC4. A safe resolution path would update generated adapter output directly; the driver stops unless the generator or canonical source owns that edit.

EC5. `architecture` is target stage but architecture is not required; the driver stops at the deterministic next applicable stage and reports that `architecture` was not reached because the architecture assessment did not require it.

EC6. `$workflow auto: verify` is rejected because `verify` is outside the review-fix target-stage enum.

EC7. A paused profile is resumed after manual edits; the driver reruns preflight and stops if the review evidence no longer matches the artifact.

EC8. A clean review exists but `review-log.md` still lists open findings; the driver stops for state repair.

## Non-goals

- No implementation, code-review, verify, PR, release, publication, network, or external-state automation.
- No dry-run mode.
- No separate apply-mode state or `apply safe fixes` command.
- No default auto-continuation for direct review invocations.
- No review skill self-editing during the review pass.
- No auto-application of product, requirement, architecture, validation-ownership, release, or owner decisions.
- No hidden background work.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | `$workflow auto: <target-stage>` accepts only the closed proposal-side target-stage enum. |
| AC2 | `$workflow auto: status` reports state without mutation. |
| AC3 | `$workflow auto: off` clears or terminally cancels review-fix authorization. |
| AC4 | Direct review-only invocations remain isolated and do not create review-fix state. |
| AC5 | Review-fix state is persisted only under `workflow.autoprogression.review_fix`. |
| AC6 | Unknown profile, status, target-stage, auto-fix class, review status, and disposition values fail validation. |
| AC7 | Review evidence is recorded before auto-fix disposition or downstream continuation. |
| AC8 | Auto-applied findings record driver classification, rationale, changed files, validation evidence, and rereview linkage. |
| AC9 | Same-stage rereview is mandatory after every auto-fix cycle. |
| AC10 | Needs-decision, ambiguous, scope-changing, requirement-changing, architecture-changing, validation-ownership-changing, or generated-output-owner findings stop the loop. |
| AC11 | The loop enforces cycle, finding, per-cycle file, per-invocation file, and target-stage budgets. |
| AC12 | Budget exhaustion stops with a clear reported reason. |
| AC13 | Stale review evidence cannot authorize fixes or continuation. |
| AC14 | The driver never continues past the armed target stage. |
| AC15 | Review-fix activation requires durable authorization plus a clean current stage gate. |
| AC16 | Proposal-start activation requires accepted proposal, approved recorded proposal-review, no open proposal-review findings, and unambiguous change ID and artifact placement. |
| AC17 | Direct review invocation does not activate, resume, or advance review-fix state even when state exists. |
| AC18 | Unknown, malformed, missing, or contradictory persisted review-fix state pauses or stops before mutation and continuation. |
| AC19 | Off, cancelled, completed, and target-reached transitions update `workflow.autoprogression.review_fix` deterministically. |
| AC20 | After approved recorded `spec-review`, architecture assessment records exactly one of `architecture-required`, `architecture-not-required`, or `architecture-ambiguous`. |
| AC21 | `architecture-required` routes through `architecture` and `architecture-review`. |
| AC22 | `architecture-not-required` skips conditional architecture stages and either continues to the next applicable in-bound target or stops with `target-not-applicable` when the requested target was skipped. |
| AC23 | `architecture-ambiguous` stops for owner decision. |
| AC24 | Existing `authoring-through-plan-review` and `implementation-through-verify` semantics are unchanged. |
| AC25 | No partial user-visible review-fix mode is enabled before the full proposal-side path through `test-spec-review` passes. |
| AC26 | Chat output lists applied fixes, stopped findings, changed artifacts, review rerun status, next action, and stop reason. |

## Open questions

None.

## Next artifacts

- Architecture assessment, with architecture and ADR updates if reusable orchestration or persistent state changes are introduced
- Execution plan
- Plan review
- Test spec
- Test-spec review

## Follow-on artifacts

- Approved spec-review: `../docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/spec-review-r2.md`

## Readiness

Approved and ready for architecture.
