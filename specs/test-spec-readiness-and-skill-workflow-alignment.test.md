# Test-Spec Readiness And Skill Workflow Alignment test spec

## Status

- active

## Related spec and plan

- Spec: `specs/test-spec-readiness-and-skill-workflow-alignment.md`
- Related proposal: `docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- Plan: `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
- Architecture: none. The approved spec and active plan both state that no separate architecture artifact is expected for this slice.
- Related workflow and proof surfaces:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `skills/spec-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan-review/SKILL.md` only if implementation finds a real wording conflict
  - generated `.codex/skills/`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/validate-artifact-lifecycle.py`
  - `python scripts/validate-change-metadata.py`
  - `bash scripts/ci.sh`

## Testing strategy

- Use manual contract review as the primary proof method because this feature changes workflow-facing guidance, handoff wording, and repository-visible proof expectations rather than a runtime subsystem.
- This focused test spec owns proof for:
  - `spec-review` immediate next stage versus eventual `test-spec` readiness
  - negative readiness output shapes for `not-ready` and `not-assessed`
  - preserved stage-order and isolation boundaries
  - `plan-review` preserving `test-spec` as the immediate next handoff when its wording is in scope
  - `test-spec` preserving approved spec, spec-review findings, concrete plan, and relevant architecture or ADR inputs when needed
- Keep `specs/rigorloop-workflow.test.md` archived unless implementation finds genuine overlap that requires an explicit follow-up update; do not revive it by default for this slice.
- Use skill validation, generated-output drift checks, artifact-lifecycle validator fixtures, explicit-path artifact validation, and the repo-owned CI wrapper as executable proof that the contract remains structurally valid after implementation.
- Prefer real repository surfaces over mocks or synthetic fixtures. The risk here is contract drift across workflow spec, workflow summary, and workflow-facing skills.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R1c`, `R1d`, `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R2e`, `R3`, `R3a`, `R3b`, `R3c`, `R3k` | `T1` | manual | Successful `spec-review` outputs distinguish repository-stage handoff from eventual readiness |
| `R2f`, `R2g`, `R3d`, `R3f`, `R3g`, `R3h`, `R3i` | `T2` | manual | `changes-requested` and `blocked` deny approval and route back to `spec` with explicit defect framing |
| `R2h`, `R3e`, `R3j` | `T3` | manual | `inconclusive` uses `not-assessed`, records the stop condition, and leaves immediate next stage empty |
| `R4`, `R4a`, `R4b`, `R4c` | `T4`, `T5` | manual | Preserved stage order, no broadened autoprogression, and isolated-stage behavior |
| `R5`, `R5a`, `R5b` | `T5` | manual | `plan-review` preserves `test-spec` as the immediate next handoff when in scope |
| `R6`, `R6a`, `R6b` | `T6` | manual | `test-spec` prerequisites remain intact and reject unready upstream review states |
| `R7`, `R7a` | `T7` | manual | First-pass implementation scope stays limited to directly affected workflow-facing surfaces |
| `R8`, `R8a` | `T7`, `T8`, `T9` | manual, integration, smoke | Validator deferral remains in place and proof comes from touched wording plus repo-owned validation |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1` | Successful `spec-review` with no architecture step names `plan` next and marks eventual readiness `ready` |
| `E2` | `T1` | Successful `spec-review` with architecture dependency uses `architecture` next plus `conditionally-ready` |
| `E3` | `T2` | Missing eventual readiness becomes a review failure rather than a successful handoff |
| `E4` | `T5` | Approved `plan-review` keeps `test-spec` as the immediate next stage |
| `E5` | `T6` | `test-spec` authoring still requires approved spec and plan context |
| `E6` | `T3` | Missing reviewer input produces `inconclusive` and no immediate-next-stage value |

## Edge case coverage

- Approved `spec-review` with remaining architecture work uses immediate next stage `architecture` and eventual readiness `conditionally-ready`: `T1`
- Approved `spec-review` with no architecture dependency uses immediate next stage `plan` and eventual readiness `ready`: `T1`
- `changes-requested` and `blocked` never pair with `ready` or `conditionally-ready`: `T2`
- `inconclusive` never invents a pseudo-stage such as blocker handling or missing-context resolution: `T3`
- Direct or review-only `spec-review` remains isolated even when outputs name the next stage and downstream readiness: `T4`
- `plan-review` may already satisfy the approved handoff wording; in that case implementation must leave it unchanged: `T5`, `T7`
- `test-spec` authoring must still reject missing relevant architecture or ADR input when changed boundaries require it: `T6`
- The archived `specs/rigorloop-workflow.test.md` surface stays archived unless later implementation proves a real overlap that must be updated explicitly: `T7`
- Canonical `skills/` and generated `.codex/skills/` may drift independently, so both need proof: `T8`, `T9`

## Test cases

### T1. Successful `spec-review` outputs distinguish immediate next stage from eventual `test-spec` readiness

- Covers: `R1`, `R1a`, `R1b`, `R1c`, `R1d`, `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R2e`, `R3`, `R3a`, `R3b`, `R3c`, `R3k`, `E1`, `E2`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/spec-review/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Review the touched workflow spec, workflow summary, and `spec-review` guidance.
  - Confirm successful `spec-review` output reports both:
    - the immediate next repository stage
    - eventual `test-spec` readiness
  - Confirm approved output uses repository stages only for the immediate next stage.
  - Confirm approved output with required architecture uses immediate next stage `architecture` and eventual readiness `conditionally-ready` with a named dependency.
  - Confirm approved output without required architecture uses immediate next stage `plan` and eventual readiness `ready`.
  - Confirm successful `spec-review` never names `test-spec` as the immediate next stage when `architecture` or `plan` still remains.
- Expected result:
  - Successful review output makes the handoff/readiness distinction explicit without skipping required intermediate stages.
- Failure proves:
  - The implementation still blurs later-stage fitness with immediate stage routing, or it leaves the enduring invariant outside the durable workflow rule.
- Automation location:
  - Manual review during M1.

### T2. `not-ready` output denies approval and routes upstream to `spec`

- Covers: `R2f`, `R2g`, `R3d`, `R3f`, `R3g`, `R3h`, `R3i`, `E3`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `skills/spec-review/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Review the negative `spec-review` output contract in the touched workflow and review guidance.
  - Confirm `changes-requested` pairs with immediate next stage `spec` and eventual readiness `not-ready`.
  - Confirm `blocked` pairs with immediate next stage `spec` and eventual readiness `not-ready`.
  - Confirm `not-ready` output states that the spec is not approved for downstream planning.
  - Confirm `not-ready` output names `spec` as the required upstream fix surface.
  - Confirm `not-ready` output identifies a blocking defect category such as missing testable requirements or contradictory requirements.
- Expected result:
  - Missing or contradictory testable requirements stop approval and downstream planning instead of being treated as a soft warning.
- Failure proves:
  - The repository could still approve or continue from a spec that is not credible enough for later proof design.
- Automation location:
  - Manual review during M1.

### T3. `not-assessed` output records the stop condition and no immediate next stage

- Covers: `R2h`, `R3e`, `R3j`, `E6`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `skills/spec-review/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Review the missing-input path in the touched workflow and `spec-review` guidance.
  - Confirm `inconclusive` pairs with eventual readiness `not-assessed`.
  - Confirm the immediate next repository stage field is omitted or explicitly empty.
  - Confirm the output records the stop condition and identifies the missing required input.
  - Confirm no pseudo-routing states such as `blocker handling` or `missing-context resolution` appear in the immediate-next-stage field.
- Expected result:
  - Missing reviewer inputs stop the workflow cleanly without inventing a non-stage route.
- Failure proves:
  - The implementation still allows ambiguous stop behavior or pseudo-stage leakage in contributor-facing outputs.
- Automation location:
  - Manual review during M1.

### T4. Stage order, autoprogression boundaries, and isolated `spec-review` behavior remain unchanged

- Covers: `R4`, `R4a`, `R4c`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/spec-review/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Compare the touched workflow surfaces against the approved focused spec.
  - Confirm the feature preserves the existing stage order of `spec-review -> architecture when needed -> plan -> plan-review -> test-spec`.
  - Confirm the feature does not broaden autoprogression from `spec-review` into `architecture`, `plan`, or `test-spec`.
  - Confirm direct or review-only `spec-review` remains isolated unless a higher-priority approved workflow rule changes that behavior.
- Expected result:
  - The change clarifies wording without changing the repository’s approved routing and continuation boundaries.
- Failure proves:
  - The implementation widened the workflow instead of clarifying contributor-visible output semantics.
- Automation location:
  - Manual review during M1.

### T5. `plan-review` preserves `test-spec` as the immediate next handoff when its wording is in scope

- Covers: `R4b`, `R5`, `R5a`, `R5b`, `E4`
- Level: manual
- Fixture/setup:
  - `skills/plan-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
- Steps:
  - Inspect `skills/plan-review/SKILL.md` only if implementation touches it.
  - If it is touched, confirm approved `plan-review` continues to name `test-spec` as the immediate next stage and treats any implementation-readiness wording as downstream readiness only.
  - If it is not touched, confirm the existing wording already satisfies the approved contract and that implementation did not widen scope by editing it unnecessarily.
- Expected result:
  - `plan-review` either stays unchanged because it is already compliant or is aligned without obscuring `test-spec` as the immediate handoff.
- Failure proves:
  - The repository still blurs immediate handoff with later implementation readiness, or the slice widened without a real defect.
- Automation location:
  - Manual review during M1.

### T6. `test-spec` authoring preserves approved upstream prerequisites

- Covers: `R6`, `R6a`, `R6b`, `E5`
- Level: manual
- Fixture/setup:
  - `skills/test-spec/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/test-spec-readiness-and-skill-workflow-alignment.md`
- Steps:
  - Review the touched `test-spec` guidance.
  - Confirm `test-spec` authoring still requires:
    - an approved feature spec
    - spec-review findings
    - a concrete execution plan
    - approved architecture or ADR inputs when relevant to changed boundaries
  - Confirm `test-spec` does not proceed from upstream `not-ready` or `not-assessed` review outcomes.
  - Confirm missing approved inputs return work to the appropriate upstream gate instead of silently continuing.
- Expected result:
  - The proof-authoring stage stays gated by the same upstream rigor the approved spec requires.
- Failure proves:
  - The implementation weakened prerequisites or allowed proof authoring from an unready upstream artifact.
- Automation location:
  - Manual review during M1.

### T7. First-pass implementation scope stays narrow and validator enforcement remains deferred

- Covers: `R7`, `R7a`, `R8`, `R8a`
- Level: manual
- Fixture/setup:
  - `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - touched workflow and skill surfaces
- Steps:
  - Review the final implementation diff against the active plan and approved spec.
  - Confirm first-pass implementation stays limited to:
    - `specs/rigorloop-workflow.md`
    - `docs/workflows.md`
    - `skills/spec-review/SKILL.md`
    - `skills/test-spec/SKILL.md`
    - `skills/workflow/SKILL.md`
    - `skills/plan-review/SKILL.md` only if a real wording conflict existed
  - Confirm no dedicated readiness-wording validator, router, or new persistence layer is introduced in v1.
  - Confirm proof continues to rely on wording review plus the named validation surfaces rather than a new enforcement subsystem.
- Expected result:
  - The implementation remains inside the approved first slice and keeps validator enforcement deferred.
- Failure proves:
  - The slice widened into broad review-skill normalization or premature automation.
- Automation location:
  - Manual review during M1.

### T8. Canonical and generated skill surfaces remain synchronized and structurally valid

- Covers: supporting proof for `T1`-`T7`
- Level: integration
- Fixture/setup:
  - touched canonical `skills/`
  - generated `.codex/skills/`
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Confirm the touched canonical skills and generated compatibility output stay synchronized.
- Expected result:
  - Canonical skill guidance remains valid and generated `.codex/skills/` output stays in sync with the authored changes.
- Failure proves:
  - The feature changed workflow-facing skills without keeping the derived distribution surface structurally valid.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`

### T9. Artifact-lifecycle fixtures, explicit-path validation, and repo smoke stay green

- Covers: supporting proof for touched authoritative artifacts and repo-owned smoke validation
- Level: integration, smoke
- Fixture/setup:
  - `docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `specs/test-spec-readiness-and-skill-workflow-alignment.md`
  - `specs/test-spec-readiness-and-skill-workflow-alignment.test.md`
  - `specs/rigorloop-workflow.md`
  - `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml` once created
  - repo-owned validation wrapper
- Steps:
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml` once the baseline change-local pack exists.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/rigorloop-workflow.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`.
  - Run `bash scripts/ci.sh` after implementation lands.
  - Confirm the touched lifecycle-managed artifacts stay internally consistent and the standard smoke path still passes.
- Expected result:
  - The authoritative artifacts remain lifecycle-valid, the validator fixtures stay green, and the repository smoke path continues to pass after the workflow-contract changes.
- Failure proves:
  - The feature left stale lifecycle state behind or broke a required repo-owned validation surface.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-test-spec-readiness-and-skill-workflow-alignment/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md --path specs/test-spec-readiness-and-skill-workflow-alignment.md --path specs/rigorloop-workflow.md --path specs/test-spec-readiness-and-skill-workflow-alignment.test.md --path docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`
  - `bash scripts/ci.sh`

## Fixtures and data

- Real repository workflow and proof surfaces:
  - `specs/test-spec-readiness-and-skill-workflow-alignment.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `skills/spec-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/plan-review/SKILL.md` when touched
  - generated `.codex/skills/`
- The active plan acts as a proof fixture for first-pass scope, validation commands, and the conditional `plan-review` touch rule:
  - `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`

## Mocking/stubbing policy

- No mocks or stubs are needed.
- Use real repository files and repo-owned validation scripts because the contract is about contributor-visible workflow behavior and proof surfaces, not isolated function logic.

## Migration or compatibility tests

- Manual verification that the implementation preserves compatibility with the current workflow baseline:
  - the canonical stage order remains unchanged
  - no new autoprogression is implied from `spec-review`
  - the archived `specs/rigorloop-workflow.test.md` surface is not silently reopened
  - older wording that treated `test-spec` as the immediate next stage after `spec-review` is replaced or removed where touched

## Observability verification

- Manual review must be able to determine from touched workflow-facing outputs:
  - the immediate next repository stage
  - eventual `test-spec` readiness
  - when approval is denied for downstream planning
  - when a stop condition prevented readiness assessment
- Manual review must be able to tell whether `plan-review` preserved `test-spec` as the immediate next handoff when its wording is in scope.

## Security/privacy verification

- Confirm the wording change does not introduce any new network dependency, secret handling path, or destructive workflow action.
- Confirm examples and review-output wording do not encourage exposing credentials, secrets, or sensitive runtime values while naming missing inputs or blockers.
- Confirm the change does not weaken higher-priority repository policies for sensitive workflow decisions.

## Performance checks

- Not applicable. This feature changes workflow wording and proof surfaces, not runtime performance.

## Manual QA checklist

- [ ] Successful `spec-review` output distinguishes immediate next stage from eventual `test-spec` readiness.
- [ ] Approved `spec-review` with architecture dependency uses immediate next stage `architecture` and eventual readiness `conditionally-ready` with a named dependency.
- [ ] Approved `spec-review` without architecture dependency uses immediate next stage `plan` and eventual readiness `ready`.
- [ ] Approved `spec-review` never pairs with `not-ready` or `not-assessed`.
- [ ] `changes-requested` and `blocked` pair with `not-ready`, immediate next stage `spec`, and explicit upstream-fix wording.
- [ ] `inconclusive` pairs with `not-assessed`, records the stop condition and missing input, and leaves the immediate-next-stage field empty.
- [ ] Direct or review-only `spec-review` remains isolated.
- [ ] `plan-review` preserves `test-spec` as the immediate next handoff when in scope, or remains untouched because it was already compliant.
- [ ] `test-spec` guidance still requires approved spec, spec-review findings, concrete plan, and relevant architecture or ADR inputs when needed.
- [ ] No validator or routing subsystem is introduced in v1.
- [ ] Skill, lifecycle, and smoke validation commands named in the active plan are all represented on the implementation proof path.

## What not to test

- Do not invent executable product or unit tests for runtime code; this feature is intentionally workflow-contract driven.
- Do not treat a dedicated readiness-wording validator as part of v1 proof.
- Do not revive or expand the archived `specs/rigorloop-workflow.test.md` surface unless implementation reveals genuine overlap that requires a separate explicit update.
- Do not test broader review-stage normalization outside the approved first-pass scope.

## Uncovered gaps

- None. The approved spec and active plan are specific enough to support focused manual and repo-owned structural proof without returning to spec or architecture.

## Next artifacts

- `pr`
- downstream merge-closeout lifecycle updates if later stages continue

## Follow-on artifacts

None yet.

## Readiness

This test spec is active.

It remained aligned through implementation, first-pass `code-review`, `verify`, and `explain-change` for `docs/plans/2026-04-22-test-spec-readiness-and-skill-workflow-alignment.md`.

The next stage is `pr`.
