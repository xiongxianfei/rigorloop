# Implement First-Attempt Correctness test spec

## Status

- active

## Related spec and plan

- Spec: `specs/implement-first-attempt-correctness.md`
- Related proposal: `docs/proposals/2026-04-23-implement-first-attempt-correctness.md`
- Plan: `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
- Architecture: none. The approved spec and active plan both state that no separate architecture artifact is expected for this slice.
- Related workflow and proof surfaces:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md` only if implementation updates it under the aligned-surface audit
  - `AGENTS.md` only if implementation proves real practical-summary drift
  - `CONSTITUTION.md` only if implementation proves a principle-level contract change
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md`
  - generated `.codex/skills/`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/validate-artifact-lifecycle.py`
  - `python scripts/validate-change-metadata.py`
  - `bash scripts/ci.sh`

## Testing strategy

- Use manual contract review as the primary proof method because this feature changes workflow-facing guidance, first-pass completeness rules, and contributor-visible proof surfaces rather than a runtime subsystem.
- This focused test spec owns proof for:
  - `implement` first-pass acceptable-result wording and pre-handoff boundaries
  - required edge-case sources and the touched-failure-path rule
  - the distinction between the smallest scope-complete change and the smallest diff
  - the distinction between preventable first-pass misses and ordinary later review comments
  - the same-slice completeness set, authoritative unaffected-rationale handling, and blocker behavior
  - aligned `workflow` wording without routing or ownership drift
  - targeted pre-`code-review` proof versus optional broad smoke or later PR proof
  - conditional aligned-surface updates for `docs/workflows.md`, generated `.codex/skills/`, and any no-change decisions for `AGENTS.md` or `CONSTITUTION.md`
- Use real repository surfaces rather than mocks. The risk here is contract drift across canonical skills, workflow summary, generated adapter output, the active plan audit, and change-local artifacts.
- Use targeted repo-owned validation commands as the minimum pre-`code-review` proof path. Treat `bash scripts/ci.sh` as optional broad smoke during implementation and later PR proof when downstream policy requires it.
- Keep `specs/rigorloop-workflow.md` out of this first slice. If implementation reveals that the durable workflow invariant must move there now, stop and return to the appropriate upstream gate instead of guessing past the approved boundary.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R1c` | `T1` | manual | `implement` defines the first-pass acceptable-result gate and blocks incomplete handoff |
| `R2`, `R2a`, `R2b` | `T2` | manual | Required edge cases come from governing sources and touched failure paths |
| `R3`, `R3a`, `R3b`, `R4`, `R4a`, `R4b` | `T3` | manual | Smallest scope-complete change and preventable miss semantics stay explicit |
| `R5`, `R5a`, `R5b`, `R5ba`, `R5c` | `T4` | manual | Same-slice completeness set, authoritative unaffected rationale, aligned-surface audit, and blocker behavior |
| `R6`, `R6a`, `R6b`, `R6c`, `R6d`, `R8c` | `T5` | manual | `workflow` stays aligned without routing or ownership drift and is updated together with `implement` |
| `R7`, `R7a`, `R7b`, `R7c` | `T6`, `T9`, `T10` | manual, integration, smoke | Targeted proof is the M1 handoff gate; broader smoke remains separate |
| `R8`, `R8a`, `R8b`, `R8d`, `R8e` | `T4`, `T5`, `T7`, `T9` | manual, integration | Required aligned surfaces stay truthful and generated output stays in sync |
| `R9`, `R9a`, `R9b`, `R9c`, `R10`, `R10a`, `R10b` | `T8` | manual | Tests-first and scope-control remain intact, and the first slice stays focused on `implement` plus aligned `workflow` |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1`, `T5` | The first pass updates both primary and aligned workflow guidance before handoff |
| `E2` | `T4` | A locally correct wording fix still fails if required plan or change-local surfaces are stale |
| `E3` | `T2` | Touched failure-path behavior creates a required edge case |
| `E4` | `T3` | Later non-required review comments do not automatically prove first-pass failure |
| `E5` | `T5` | `workflow` wording aligns without changing routing behavior |
| `E6` | `T1`, `T6` | Missing targeted validation blocks handoff |

## Edge case coverage

- A required authored surface may remain unchanged only when it is explicitly marked unaffected with rationale in an acceptable authoritative surface: `T4`
- A required aligned surface may remain unchanged only when it is explicitly marked unaffected with rationale in an acceptable authoritative surface: `T4`, `T7`
- A locally correct fix still fails if it leaves the active plan audit, change-local metadata, or another required surface stale: `T4`
- A later review comment does not automatically prove first-pass failure when it was not required by governing sources or targeted validation: `T3`
- A touched failure path can create a required edge case even if the summary prose did not name it separately: `T2`
- Updating `skills/workflow/SKILL.md` must not alter stage order, routing behavior, or claim ownership split: `T5`
- Narrow targeted validation is sufficient for M1 handoff when it satisfies the slice contract; broader smoke remains optional at that point: `T6`, `T10`
- If approved artifacts are too ambiguous to determine required surfaces or edge cases, the correct behavior is to stop with a blocker instead of handing off to `code-review`: `T4`

## Test cases

### T1. `implement` defines first-pass acceptability and blocks incomplete handoff

- Covers: `R1`, `R1a`, `R1b`, `R1c`, `E1`, `E6`
- Level: manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Review the touched implementation-stage and companion workflow guidance.
  - Confirm `implement` defines `first-pass acceptable result` in observable terms before handoff to `code-review`.
  - Confirm the guidance includes all `R1a` completeness conditions:
    - all in-scope requirements are addressed
    - required authored surfaces are updated or explicitly marked unaffected with rationale
    - required aligned surfaces are updated or explicitly marked unaffected with rationale
    - no known in-scope defect remains
    - required targeted validation passes
    - no required same-slice fix is deferred
    - no later cleanup is required to become contract-complete
  - Confirm the guidance explicitly says this is not a zero-review-comment guarantee.
  - Confirm `implement` must not report readiness for `code-review` when any `R1a` condition is unsatisfied.
- Expected result:
  - The implementation stage has a concrete pre-handoff completeness gate instead of an implicit quality preference.
- Failure proves:
  - The slice still permits incomplete first passes or implies a perfection guarantee rather than an observable readiness contract.
- Automation location:
  - Manual review during M1.

### T2. Required edge cases come from governing sources and touched failure paths

- Covers: `R2`, `R2a`, `R2b`, `E3`
- Level: manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/implement-first-attempt-correctness.md`
- Steps:
  - Review the touched implementation guidance and the approved feature spec together.
  - Confirm `required edge case` is the contract term and that vague wording such as `obvious edge cases` is not used as the standard.
  - Confirm required edge-case sources include:
    - approved spec requirements
    - approved test-spec items
    - named regression cases from the motivating incident
    - changed branch conditions or touched failure paths
    - existing repository tests or fixtures that govern touched behavior
    - required aligned workflow or skill wording distinctions
  - Confirm touched failure paths or changed branch conditions must be handled or evidenced in the first pass.
- Expected result:
  - Edge-case selection is grounded in approved sources rather than intuition alone.
- Failure proves:
  - The implementation could still skip required edge cases or rely on subjective judgment language.
- Automation location:
  - Manual review during M1.

### T3. Smallest scope-complete change and preventable misses stay distinct from smaller diffs and ordinary later comments

- Covers: `R3`, `R3a`, `R3b`, `R4`, `R4a`, `R4b`, `E4`
- Level: manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/implement-first-attempt-correctness.md`
- Steps:
  - Review the touched guidance for `smallest scope-complete change` and `preventable first-pass miss`.
  - Confirm the guidance says completeness targets the smallest change set that satisfies all in-scope requirements and required aligned surfaces, not merely the smallest diff.
  - Confirm a smaller diff that leaves a stale required surface, known in-scope defect, or missing required edge case behind is explicitly disallowed.
  - Confirm later review findings are divided between:
    - preventable first-pass misses that should have been caught by governing sources, required edge cases, or targeted validation
    - ordinary later comments that do not automatically invalidate the first-pass contract
- Expected result:
  - The slice draws a stable boundary between incomplete first passes and normal later review feedback.
- Failure proves:
  - The contract still rewards minimal-but-incomplete diffs or overreacts to any later review comment as proof of failure.
- Automation location:
  - Manual review during M1.

### T4. Same-slice completeness, unaffected rationale, and blocker behavior are contributor-visible

- Covers: `R5`, `R5a`, `R5b`, `R5ba`, `R5c`, edge cases 1, 2, 3, 8, `E2`
- Level: manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md`
- Steps:
  - Review `skills/implement/SKILL.md` and the active plan together.
  - Confirm the same-slice completeness set includes:
    - in-scope requirements
    - required authored surfaces
    - required aligned surfaces
    - required edge cases
    - the targeted validation set
  - Confirm the active plan acts as the authoritative pre-`code-review` aligned-surface audit and that each audited surface carries one decision from:
    - `update`
    - `no-change`
    - `out-of-scope`
    - `not-applicable`
  - Confirm every `no-change` decision requires rationale.
  - Confirm the plan or change-local artifacts are used as `R5ba`-acceptable authoritative surfaces when unchanged required surfaces stay unaffected.
  - Confirm missing inputs, contradictions, or unresolved scope ambiguity require a blocker instead of incomplete handoff.
  - Confirm M1 closeout re-reads the audit, resolves all `TBD` entries, adds newly affected surfaces to scope, adds changed surfaces to targeted validation, and mirrors final decisions in `explain-change.md` at handoff.
- Expected result:
  - A reviewer can see exactly how unchanged required surfaces were assessed and why handoff was or was not allowed.
- Failure proves:
  - The slice could still leave required surfaces stale or hide unaffected-rationale decisions in chat-only reasoning.
- Automation location:
  - Manual review during M1.

### T5. `workflow` stays aligned without changing routing or ownership

- Covers: `R6`, `R6a`, `R6b`, `R6c`, `R6d`, `R8c`, `E5`, edge case 6
- Level: manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md` when touched
- Steps:
  - Review the touched canonical skill surfaces together.
  - Confirm `skills/workflow/SKILL.md` reflects the same first-pass acceptability and `smallest scope-complete change` concepts that govern `skills/implement/SKILL.md`.
  - Confirm `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` are both updated in this first slice.
  - Confirm the wording preserves:
    - canonical stage order
    - lane selection rules
    - autoprogression rules and stop conditions
    - stage ownership
    - review-only behavior
    - fast-lane behavior
    - bugfix behavior
  - Confirm the ownership split remains:
    - `implement` owns implementation completion and readiness for review
    - `code-review` owns review findings
    - `verify` owns `branch-ready`
    - `pr` owns PR-body and PR-opening readiness
- Expected result:
  - The workflow entrypoint mirrors the implementation-stage contract without silently changing repository routing behavior.
- Failure proves:
  - The slice widened into workflow-routing changes or left canonical skill guidance misaligned.
- Automation location:
  - Manual review during M1.

### T6. Targeted proof is the pre-`code-review` gate and broader smoke remains separate

- Covers: `R7`, `R7a`, `R7b`, `R7c`, edge case 7
- Level: manual
- Fixture/setup:
  - `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `specs/implement-first-attempt-correctness.md`
  - `specs/implement-first-attempt-correctness.test.md`
- Steps:
  - Review the active plan’s validation table and M1 validation commands.
  - Confirm the plan distinguishes:
    - targeted proof before `code-review`
    - optional broad smoke during implementation
    - final CI or PR proof before PR handoff when downstream policy requires it
  - Confirm the targeted validation set comes from the approved spec, active plan, this test spec, or existing repo-owned validation surfaces governing the touched behavior.
  - Confirm missing targeted validation makes the first pass unacceptable.
  - Confirm `bash scripts/ci.sh` is not required for M1 handoff when narrower targeted proof is sufficient.
- Expected result:
  - Pre-handoff proof remains narrow and slice-specific, while broader smoke and final PR proof stay distinct downstream activities.
- Failure proves:
  - The plan still collapses first-pass handoff proof with repo-wide smoke or leaves targeted proof under-specified.
- Automation location:
  - Manual review during M1.

### T7. Required aligned surfaces stay truthful and conditional no-change decisions are explicit

- Covers: `R8`, `R8a`, `R8b`, `R8d`, `R8e`, edge cases 2 and 3
- Level: manual
- Fixture/setup:
  - `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - generated `.codex/skills/`
- Steps:
  - Review the aligned-surface audit in the active plan and the final implementation diff.
  - Confirm `docs/workflows.md` is updated only if changed canonical skill wording would otherwise leave the short workflow summary stale.
  - Confirm generated `.codex/skills/` output is regenerated when canonical `skills/` wording changes would otherwise leave adapter guidance stale.
  - Confirm any untouched audited surface that remains `no-change` records rationale in the active plan and is mirrored in `explain-change.md` at handoff.
  - Confirm `AGENTS.md` and `CONSTITUTION.md` either:
    - remain unchanged with explicit audit rationale; or
    - are added to implementation scope and targeted validation if implementation proves they are affected.
- Expected result:
  - All required aligned surfaces are either updated or explicitly kept truthful with rationale in a contributor-visible authoritative surface.
- Failure proves:
  - The slice still allows conditional aligned surfaces to drift or relies on implicit no-change decisions.
- Automation location:
  - Manual review during M1.

### T8. Tests-first, scope-control, and first-slice boundaries remain intact

- Covers: `R9`, `R9a`, `R9b`, `R9c`, `R10`, `R10a`, `R10b`
- Level: manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - final implementation diff
- Steps:
  - Review the final implementation diff against the approved spec and active plan.
  - Confirm tests or other proof surfaces are written or updated first when feasible for the slice.
  - Confirm no unrelated refactors are introduced in the name of completeness.
  - Confirm `implement` is not turned into `code-review`, architecture design, or broad exploration.
  - Confirm this first slice stays focused on `implement` plus aligned `workflow` wording.
  - Confirm `bugfix` and other implementation-adjacent skills remain untouched and are deferred as later approved follow-up work.
  - Confirm `specs/rigorloop-workflow.md` is not silently edited as part of M1; if implementation reveals that a durable fold-in is required now, the work must stop and return to the appropriate upstream gate.
- Expected result:
  - The implementation remains within the approved first slice and preserves existing tests-first and scope-control rules.
- Failure proves:
  - The change widened into deferred follow-up work or weakened the repository’s existing implementation discipline.
- Automation location:
  - Manual review during M1.

### T9. Targeted structural proof passes for canonical skills, generated output, lifecycle, and metadata

- Covers: supporting proof for `T1`-`T8`
- Level: integration
- Fixture/setup:
  - touched canonical `skills/`
  - generated `.codex/skills/`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - touched lifecycle-managed artifacts
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`.
  - Run `git diff --check -- skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md specs/implement-first-attempt-correctness.test.md docs/changes/2026-04-23-implement-first-attempt-correctness .codex/skills docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/plan.md AGENTS.md CONSTITUTION.md`.
- Expected result:
  - The targeted pre-`code-review` proof path stays green for canonical skills, generated output, change metadata, lifecycle-managed artifacts, and patch hygiene.
- Failure proves:
  - The slice changed workflow-facing guidance without keeping the targeted structural proof surfaces valid and synchronized.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/implement-first-attempt-correctness.md --path specs/implement-first-attempt-correctness.test.md --path docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `git diff --check -- skills/implement/SKILL.md skills/workflow/SKILL.md docs/workflows.md specs/implement-first-attempt-correctness.test.md docs/changes/2026-04-23-implement-first-attempt-correctness .codex/skills docs/plans/2026-04-23-implement-first-attempt-correctness.md docs/plan.md AGENTS.md CONSTITUTION.md`

### T10. Optional broad smoke and final CI proof remain later-stage validation

- Covers: supporting smoke proof for `T6`
- Level: smoke
- Fixture/setup:
  - repo-owned validation wrapper
  - downstream review-resolution or PR-readiness context when available
- Steps:
  - Run `bash scripts/ci.sh` only as optional broad smoke during implementation or as final PR proof when downstream readiness requires it.
  - Confirm later-stage documentation does not retroactively treat this command as the minimum M1 pre-`code-review` gate.
- Expected result:
  - The repo-wide smoke wrapper remains available and useful without overriding the narrower handoff-proof boundary approved for M1.
- Failure proves:
  - The change reintroduced broad smoke as a mandatory pre-`code-review` requirement or blurred handoff versus PR-ready proof.
- Automation location:
  - `bash scripts/ci.sh`

## Fixtures and data

- Real repository workflow and proof surfaces:
  - `specs/implement-first-attempt-correctness.md`
  - `docs/plans/2026-04-23-implement-first-attempt-correctness.md`
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md` when touched
  - `AGENTS.md` when touched
  - `CONSTITUTION.md` when touched
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/change.yaml`
  - `docs/changes/2026-04-23-implement-first-attempt-correctness/explain-change.md`
  - generated `.codex/skills/`
- The active plan acts as a proof fixture for:
  - the required aligned-surface audit
  - the M1 aligned-surface closeout checklist
  - targeted versus broad validation levels
  - the authoritative-surface choice for unaffected rationale during this slice

## Mocking/stubbing policy

- No mocks or stubs are needed.
- Use real repository files and repo-owned validation scripts because this feature is about contributor-visible workflow behavior and proof surfaces, not isolated runtime logic.
- If a later follow-up adds validator-backed enforcement or a broader workflow subsystem, that later change should define its own fixture strategy separately.

## Migration or compatibility tests

- Manual verification that the implementation preserves compatibility with the current workflow baseline:
  - canonical stage order remains unchanged
  - lane selection, autoprogression, stop conditions, and stage ownership remain unchanged
  - `bugfix` behavior remains unchanged in this slice
  - `implement` continues to hand off to `code-review`, not to `verify` or `pr`
  - `specs/rigorloop-workflow.md` remains untouched in this first slice unless work is intentionally returned upstream for a broader approved follow-up
  - `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` remain unchanged unless the aligned-surface audit proves they are affected

## Observability verification

- Manual review must be able to tell from touched workflow-facing outputs:
  - what counts as a first-pass acceptable result
  - which required authored surfaces and required aligned surfaces were updated or explicitly marked unaffected with rationale
  - which edge-case sources govern the slice
  - when a touched failure path created a required edge case
  - which targeted validation commands formed the pre-`code-review` proof path
  - when a blocker prevented handoff
  - the final aligned-surface audit decisions and where they were mirrored

## Security/privacy verification

- Confirm the wording change introduces no new network, secret, or credential dependency.
- Confirm aligned-surface rationale and change-local explanation do not expose secrets, tokens, credentials, or private runtime data while describing blockers or unaffected decisions.
- Confirm the feature does not weaken higher-priority repository rules for security-sensitive workflow decisions.

## Performance checks

- Not applicable for product runtime performance.
- Manual review must confirm the slice does not require broader-than-needed validation before `code-review` when narrower targeted proof already satisfies the approved contract.

## Manual QA checklist

- [ ] `implement` defines `first-pass acceptable result` and blocks incomplete handoff to `code-review`.
- [ ] `implement` states that first-pass acceptability is not a zero-review-comment guarantee.
- [ ] Required edge-case sources are explicit, and touched failure paths are included when they create required edge cases.
- [ ] `smallest scope-complete change` is distinct from the smallest diff.
- [ ] Preventable first-pass misses are distinguished from ordinary later review comments.
- [ ] The active plan carries a required aligned-surface audit with final `update`, `no-change`, `out-of-scope`, or `not-applicable` decisions and rationale for every `no-change`.
- [ ] `skills/implement/SKILL.md` and `skills/workflow/SKILL.md` are both updated in this first slice.
- [ ] `workflow` wording remains alignment-only and does not change routing or stage ownership.
- [ ] `docs/workflows.md`, generated `.codex/skills/`, `AGENTS.md`, and `CONSTITUTION.md` are either updated or explicitly kept unchanged with rationale through the aligned-surface audit.
- [ ] Targeted proof is the minimum pre-`code-review` gate, and `bash scripts/ci.sh` remains optional broad smoke or later PR proof.
- [ ] `bugfix` and other implementation-adjacent skills remain untouched in this first slice.
- [ ] The targeted structural validation commands named in the active plan all remain on the implementation proof path.

## What not to test

- Do not invent executable product unit, integration, or end-to-end tests for runtime code; this feature is intentionally workflow-contract driven.
- Do not treat validator-backed completeness scoring or enforcement as part of v1 proof.
- Do not broaden the proof surface into `bugfix` or other implementation-adjacent skills outside the approved first slice.
- Do not require `bash scripts/ci.sh` before `code-review` when the approved targeted proof path is already sufficient for M1 handoff.
- Do not test a durable workflow-spec fold-in for `specs/rigorloop-workflow.md` in this slice; that remains a separate approved follow-up if the repository later chooses it.

## Uncovered gaps

- None. The approved spec and active plan are specific enough to support focused manual and repo-owned structural proof without returning to spec or architecture.

## Next artifacts

- `implement`
- `code-review`
- `verify`

## Follow-on artifacts

- None yet

## Readiness

- This test spec is active.
- The tracked-source prerequisite is satisfied for the accepted proposal, approved spec, active plan, and this active test spec.
- No separate architecture artifact is expected for this slice.
- It remains the current proof-planning surface for this initiative until lifecycle closeout moves it to a terminal state.
- Implementation is complete for `M1`, the targeted pre-`code-review` proof is recorded in the active plan and change-local artifacts, first-pass `code-review` completed with `clean-with-notes`, and `verify` completed with verdict `ready`.
- The next stage is `explain-change`.
