# Code Review Independence Under Autoprogression test spec

## Status

- active

## Related spec and plan

- Spec: `specs/code-review-independence-under-autoprogression.md`
- Related proposal: `docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md`
- Plan: `docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`
- Related governing and proof surfaces:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - canonical `skills/`
  - generated `.codex/skills/`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/validate-artifact-lifecycle.py`
  - `bash scripts/ci.sh`

## Testing strategy

- Use manual contract review for the touched workflow and stage-local skills because this feature changes guidance and review output expectations, not a repo-owned workflow router.
- Keep proof ownership split with `specs/workflow-stage-autoprogression.test.md`:
  - this focused test spec owns first-pass review record contents, first-pass status semantics, evidence-backed clean-review validity, optional positive notes, and sensitive-change coverage;
  - `specs/workflow-stage-autoprogression.test.md` continues to own the broader `implement -> code-review -> review-resolution/code-review -> verify` chain, isolated-stage defaults, and bounded v1 autoprogression.
- Use generated-output drift and skill-validator checks as executable proof that canonical `skills/` and generated `.codex/skills/` stay synchronized and structurally valid.
- Use explicit-path artifact lifecycle validation to confirm the touched authoritative artifacts remain internally consistent as the new proof surface is introduced.
- Use repo-owned smoke validation through `bash scripts/ci.sh` after implementation to confirm the workflow and skill updates still pass the standard validation path.
- Use real repository artifacts rather than synthetic mocks. The risk here is contract drift across workflow docs and stage skills, not runtime algorithm correctness in a new subsystem.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R1c` | `T1` | manual | Independent-review mode, evidence grounding, and no hard fresh-session enforcement |
| `R2`, `R2a`, `R2b`, `R2c` | `T2` | manual | First-pass review record contents, visibility-before-fix, and no new standalone artifact requirement |
| `R3`, `R3a`, `R3b`, `R3d`, `R4`, `R4a`, `R8`, `R8a`, `R8b`, `R8d` | `T3` | manual | Workflow-managed clean/fixable status mapping and preserved autoprogression boundary |
| `R3c`, `R3e`, `R4b`, `R4c`, `R4d`, `R5`, `R8c` | `T4` | manual | `blocked`, `inconclusive`, stop conditions, and isolated/review-only behavior |
| `R6`, `R6a`, `R6b`, `R6c`, `R6d`, `R6e`, `R6f` | `T5` | manual | Evidence-backed clean reviews and optional positive notes |
| `R7` | `T6` | manual | Sensitive change classes require explicit governing coverage |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T3`, `T5` | Workflow-managed clean review continues to `verify` only when the clean result is evidence-backed |
| `E2` | `T2`, `T3` | First-pass findings appear before any `review-resolution` work begins |
| `E3` | `T4` | Isolated or review-only `code-review` stops after the first-pass record |
| `E4` | `T4` | Missing diff/tests/upstream artifacts force `inconclusive` |
| `E5` | `T4` | Decision-requiring findings use `blocked` and stop |
| `E6` | `T6` | Sensitive change classes require stronger explicit coverage |

## Edge case coverage

- Edge case 1: workflow-managed clean review continues to `verify` only when checklist coverage and no-finding rationale are present: `T3`, `T5`
- Edge case 2: fixable findings become visible before `review-resolution` begins: `T2`, `T3`
- Edge case 3: isolated or review-only `code-review` stops after the first-pass review record: `T4`
- Edge case 4: missing diff, tests, or authoritative upstream artifacts produces `inconclusive`: `T4`
- Edge case 5: product/spec/architecture/ADR/scope decisions produce `blocked`: `T4`
- Edge case 6: sensitive change classes require stronger explicit coverage than a generic clean summary: `T6`
- Edge case 7: explicit user stop-after-review instructions override automatic entry into `review-resolution`: `T4`
- Edge case 8: this feature does not create a new standalone review artifact requirement by itself: `T2`
- Edge case 9: positive notes remain optional in clean reviews: `T5`

## Test cases

### T1. Autoprogressed `code-review` runs in independent-review mode

- Covers: `R1`, `R1a`, `R1b`, `R1c`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched `code-review` and shared workflow guidance.
  - Confirm autoprogressed `code-review` is explicitly required to ground itself in the actual diff or changed files, approved upstream artifacts, checklist coverage, and available validation evidence.
  - Confirm remembered implementation intent or chat memory alone is not treated as sufficient review grounding.
  - Confirm hard fresh-session enforcement is not introduced.
  - Confirm a fresh session, separate reviewer, or separate agent remains preferred when available.
- Expected result:
  - Independent-review mode is explicit, evidence-grounded, and compatible with the approved no-hard-session-enforcement scope.
- Failure proves:
  - `code-review` could still behave like implementation continuation or the change expanded beyond the approved session-boundary scope.
- Automation location:
  - Manual review during M1.

### T2. `code-review` records a first-pass review before any review-driven fixes

- Covers: `R2`, `R2a`, `R2b`, `R2c`, `E2`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md` if touched
  - `docs/workflows.md`
- Steps:
  - Review the touched workflow and review-stage guidance.
  - Confirm `code-review` requires a first-pass review record before any review-driven fix or `review-resolution` work begins.
  - Confirm the first-pass record includes: review status, review inputs, diff summary, findings, checklist coverage, no-finding rationale when no findings exist, and recommended next stage.
  - Confirm “surface findings first” means the findings are visible before fixes begin and does not add a new user decision gate unless a stop condition applies.
  - Confirm the change does not create a new standalone review artifact requirement solely to preserve the first-pass record.
- Expected result:
  - The repository guidance makes first-pass review output durable and visible before any automatic fix loop begins.
- Failure proves:
  - Review output could still be overwritten by fixes, hidden until after `review-resolution`, or widened into an unapproved standalone artifact requirement.
- Automation location:
  - Manual review during M1.

### T3. Workflow-managed status mapping preserves the approved autoprogression boundary

- Covers: `R3`, `R3a`, `R3b`, `R3d`, `R4`, `R4a`, `R8`, `R8a`, `R8b`, `R8d`, `E1`, `E2`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md` if touched
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched `code-review`, workflow, and adjacent execution-stage guidance.
  - Confirm the first-pass review statuses include `clean-with-notes` and `changes-requested` with the approved meanings.
  - Confirm workflow-managed `clean-with-notes` continues to `verify` when no stop condition applies.
  - Confirm workflow-managed `changes-requested` automatically enters `review-resolution` and reruns `code-review` when no stop condition applies.
  - Confirm automatic `implement -> code-review` handoff remains in place.
  - Confirm no mandatory human reviewer or mandatory second-pass reviewer is added for every non-trivial change.
  - Confirm `specs/workflow-stage-autoprogression.test.md` still owns the broader loop and isolated-stage proof surface rather than being silently replaced.
- Expected result:
  - The focused code-review change strengthens the first pass without altering the approved stage order or adding unapproved human-review requirements.
- Failure proves:
  - The feature weakened or broadened the autoprogression contract instead of refining the existing boundary.
- Automation location:
  - Manual review during M1.

### T4. Stop conditions force `blocked` or `inconclusive` and keep isolated review isolated

- Covers: `R3c`, `R3e`, `R4b`, `R4c`, `R4d`, `R5`, `R8c`, `E3`, `E4`, `E5`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched `code-review` and workflow guidance for stop conditions and isolated-stage behavior.
  - Confirm `blocked` is used when findings require a product decision, spec approval, architecture or ADR approval, scope expansion, or a higher-priority repository policy that requires human review.
  - Confirm `inconclusive` is used when the reviewer cannot inspect the actual diff, relevant tests, or authoritative upstream artifacts.
  - Confirm `blocked` and `inconclusive` do not auto-enter `review-resolution`.
  - Confirm direct isolated or review-only `code-review` stops after the first-pass record.
  - Confirm an explicit user request to stop after review overrides otherwise-fixable automatic continuation.
- Expected result:
  - The workflow now distinguishes fixable review findings from real blockers or missing evidence without surprise continuation.
- Failure proves:
  - The repository could still fix forward when it should stop, or it could blur `blocked`, `inconclusive`, and isolated-review behavior.
- Automation location:
  - Manual review during M1.

### T5. Clean reviews require evidence-backed checklist coverage and optional positive notes only

- Covers: `R6`, `R6a`, `R6b`, `R6c`, `R6d`, `R6e`, `R6f`, `E1`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `docs/workflows.md` if touched
  - `specs/code-review-independence-under-autoprogression.md`
- Steps:
  - Review the clean-review guidance and any clean-review template added to the canonical skill surfaces.
  - Confirm a clean review requires review inputs, checklist coverage, diff summary, and no-finding rationale grounded in the actual diff, upstream artifacts, and validation evidence.
  - Confirm passing tests alone or remembered implementation reasoning alone are not treated as sufficient for `clean-with-notes`.
  - Confirm positive notes are optional and, when present, are limited to specific evidence-backed information useful to future maintainers.
  - Confirm generic praise such as “looks good” without checklist coverage and no-finding rationale is explicitly invalid.
- Expected result:
  - Clean reviews become credible without requiring positive-note boilerplate.
- Failure proves:
  - Unsupported clean reviews could still pass, or the implementation reintroduces the wrong success metric by requiring praise instead of evidence.
- Automation location:
  - Manual review during M1.

### T6. Sensitive change classes require explicit governing coverage

- Covers: `R7`, `E6`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `docs/workflows.md` if touched
  - `AGENTS.md`
  - `CONSTITUTION.md`
- Steps:
  - Review the review-stage guidance for changes affecting security-sensitive behavior, workflow stage policy, CI behavior, schemas, architecture boundaries, and compatibility-sensitive contributor expectations.
  - Confirm those change classes require explicit governing-requirement, risk, or checklist coverage rather than only a generic clean summary.
  - Confirm the guidance does not encourage exposing secrets, credentials, or sensitive runtime values from diffs or validation output in the first-pass review record.
  - Confirm higher-priority policies requiring human review for sensitive findings still stop automatic continuation.
- Expected result:
  - Sensitive changes receive visibly stronger review coverage without overriding higher-priority safety policies.
- Failure proves:
  - The implementation would still allow generic clean output for high-sensitivity changes or could weaken security/privacy handling in review output.
- Automation location:
  - Manual review during M1.

### T7. Canonical and generated skill surfaces remain synchronized and structurally valid

- Covers: supporting proof for `T1`-`T6`
- Level: integration
- Fixture/setup:
  - touched canonical `skills/`
  - generated `.codex/skills/`
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
- Expected result:
  - Canonical skills are valid, the skill validator still passes, and generated compatibility output stays synchronized with the canonical edits.
- Failure proves:
  - The feature changed skill guidance without keeping the derived distribution surface valid and in sync.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`

### T8. Artifact lifecycle and repo smoke validation stay green after the workflow guidance changes

- Covers: supporting proof for touched authoritative artifacts and repo-wide smoke
- Level: integration, smoke
- Fixture/setup:
  - `docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md`
  - `specs/code-review-independence-under-autoprogression.md`
  - `specs/code-review-independence-under-autoprogression.test.md`
  - `docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`
  - touched workflow and skill surfaces
  - repo-owned validation wrapper
- Steps:
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md --path docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`.
  - Run `bash scripts/ci.sh` after the implementation lands.
  - Confirm the standard validation wrapper completes successfully and the touched lifecycle-managed artifacts remain internally consistent.
- Expected result:
  - The authoritative artifacts stay lifecycle-valid and the repository smoke path still passes after the code-review guidance changes.
- Failure proves:
  - The initiative left stale lifecycle state behind or broke the standard validation path.
- Automation location:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md --path docs/plans/2026-04-22-code-review-independence-under-autoprogression.md`
  - `bash scripts/ci.sh`

## Fixtures and data

- Real repository workflow and review surfaces:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md` if touched
  - `docs/workflows.md`
- Real governing and overlapping proof surfaces:
  - `specs/code-review-independence-under-autoprogression.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
- Repo-owned validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `bash scripts/ci.sh`

## Mocking/stubbing policy

- No mocks or stubs are required for this feature.
- Use real repository artifacts and repo-owned validation scripts rather than synthetic reviewers, diff fixtures, or a fake workflow router.
- If a later follow-up adds executable orchestration or stronger reviewer isolation, that follow-up should define its own fixture strategy separately.

## Migration or compatibility tests

- Confirm the change preserves automatic `implement -> code-review` handoff and the existing `code-review -> review-resolution -> code-review` loop for fixable findings: `T3`
- Confirm isolated and review-only `code-review` behavior remains isolated by default: `T4`
- Confirm the feature does not add hard fresh-session enforcement, mandatory human review, or a universal second-pass reviewer requirement: `T1`, `T3`
- Confirm the feature does not create a new standalone `review-resolution.md` requirement solely to preserve first-pass review output: `T2`
- Confirm generic “approve, no findings” or “looks good” outputs are no longer sufficient for clean reviews: `T5`

## Observability verification

- Confirm first-pass review output is expected to state review status, review inputs, diff summary, findings, checklist coverage, and no-finding rationale when applicable: `T2`, `T5`
- Confirm first-pass review output is expected to announce the recommended next stage or stop reason: `T2`, `T3`, `T4`
- Confirm workflow-managed continuation versus isolated stop behavior is visible in the guidance: `T3`, `T4`
- Confirm sensitive change classes require explicit visible coverage instead of a generic clean closeout: `T6`

## Security/privacy verification

- Confirm first-pass review guidance does not encourage exposing secrets, credentials, or sensitive runtime values from diffs or validation outputs: `T6`
- Confirm higher-priority human-review requirements for sensitive findings still override automatic continuation: `T4`, `T6`
- Confirm the feature adds no new network, secret, or credential dependency: `T1`, `T6`

## Performance checks

- No dedicated benchmark suite is required. The approved feature changes workflow guidance and review output shape rather than product runtime behavior.
- Manual architectural confirmation is sufficient:
  - no new workflow router;
  - no mandatory second-pass reviewer loop for ordinary non-trivial work; and
  - no duplicate user confirmation gate before fixable findings can enter `review-resolution`.
- Supporting checks: `T1`, `T3`

## Manual QA checklist

- Inspect `skills/code-review/SKILL.md` and `skills/workflow/SKILL.md` together and confirm they teach the same first-pass review contract.
- Inspect any touched `docs/workflows.md` wording and confirm it summarizes the focused spec without widening v1 autoprogression scope.
- Inspect `specs/workflow-stage-autoprogression.test.md` after its narrow update and confirm it still owns the broader loop/isolation proof surface.
- Inspect the clean-review guidance and confirm generic praise without checklist coverage is invalid while positive notes remain optional.
- Inspect stop-condition wording and confirm isolated review, explicit user stop, missing evidence, and decision blockers all stop continuation as approved.
- Run the skill-validation, lifecycle-validation, and smoke commands named in `T7` and `T8`.

## What not to test

- Do not add end-to-end runtime tests for a workflow router or session-isolation subsystem. No such subsystem exists in this slice.
- Do not retest the entire broader autoprogression feature here. Rely on `specs/workflow-stage-autoprogression.test.md` where it already owns direct-`pr`, broader stage-order, and isolated-stage-default proof.
- Do not require positive-note content generation quality beyond the approved evidence-backed optionality rule.
- Do not use snapshot-only assertions as the sole proof for behavioral review requirements.

## Uncovered gaps

- None blocking. The approved spec is testable as written.
- Intentional limitation: because this slice is guidance- and skill-driven, end-to-end behavior is proved mainly through manual contract review plus repo-owned validation rather than a dedicated runtime harness.

## Next artifacts

- `implement`
- `code-review`
- `verify`

## Follow-on artifacts

- None yet

## Readiness

- This test spec is active.
- The tracked-source prerequisite is satisfied for the accepted proposal, approved spec, active plan, and this active test spec.
- Implementation, first-pass `code-review`, and `verify` are complete for M1.
- The next stage is `explain-change`.
