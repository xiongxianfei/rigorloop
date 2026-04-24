# Code Review Branch Reality And Traceability test spec

## Status

- active

## Related spec and plan

- Spec: `specs/code-review-branch-reality-and-traceability.md`
- Related proposal: `docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md`
- Plan: `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
- Architecture: none. The approved spec and active plan both state that no separate architecture artifact is expected for this slice.
- Related workflow and proof surfaces:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/explain-change/SKILL.md` only if implementation touches it for readiness-term alignment
  - `specs/code-review-independence-under-autoprogression.md`
  - `specs/code-review-independence-under-autoprogression.test.md`
  - generated `.codex/skills/`
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/validate-artifact-lifecycle.py`
  - `python scripts/validate-change-metadata.py`
  - `bash scripts/ci.sh`

## Testing strategy

- Use manual contract review as the primary proof method because this feature changes workflow-facing guidance, vocabulary, and review-evidence expectations rather than a runtime subsystem.
- This focused test spec owns proof for:
  - stage-owned language across `implement`, `code-review`, `verify`, and `pr`
  - the distinction between review surface and tracked governing branch state
  - mixed-evidence review outcomes when tracked governing authority is missing
  - direct-proof requirements for named edge cases
  - qualified readiness terminology using `branch-ready`, `pr-body-ready`, and `pr-open-ready`
  - compatibility with the earlier `code-review` independence contract
- Keep ownership split with `specs/code-review-independence-under-autoprogression.test.md`:
  - that earlier test spec continues to own the main first-pass review-record contract and broader independent-review semantics
  - this focused test spec must prove the new branch-reality and traceability rules add evidence requirements without weakening those earlier guarantees
- Use generated-output drift checks, artifact-lifecycle validation, and the repo-owned CI wrapper as executable proof that the workflow-facing contract remains structurally valid after implementation.
- Use real repository surfaces rather than mocks. The risk here is drift across authoritative docs and skills, not isolated function behavior.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b` | `T1` | manual | `implement` stays inside implementation ownership and does not claim review outcomes |
| `R1c`, `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R2e` | `T2` | manual | `code-review` distinguishes review surface from tracked governing branch state |
| `R2f`, `R2g`, `R2h`, `R2i`, `R2j`, `R2k` | `T3` | manual | Missing tracked authority blocks clean results without suppressing supported findings |
| `R1d`, `R1e`, `R1f`, `R2l`, `R2m`, `R2n` | `T4` | manual | `verify` owns `branch-ready`; `pr` owns qualified PR-opening terms; residual `PR-ready` hits are manually classified |
| `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f` | `T5` | manual | Named edge cases require direct proof and unresolved gaps block clean outcomes or readiness |
| `R4`, `R4a`, `R4b` | `T6` | manual | Earlier `code-review` independence guarantees remain intact |
| `R4c`, `R4d`, `R4e` | `T7` | manual | Durable invariant lands in `specs/rigorloop-workflow.md`; v1 scope remains wording-first |
| supporting structural proof for touched workflow and skill surfaces | `T8`, `T9` | integration, smoke | Canonical/generated sync, artifact lifecycle, metadata, and repo smoke validation |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1` | `implement` reports completion and readiness for `code-review` without claiming review findings |
| `E2` | `T2` | `code-review` may inspect an uncommitted diff when cited governing artifacts are tracked |
| `E3` | `T3` | Local-only governing inputs force `inconclusive` when no independently supported finding exists |
| `E4` | `T3` | Missing tracked authority does not suppress a supported `changes-requested` result |
| `E5` | `T4` | `verify` blocks `branch-ready` when authoritative artifacts are missing from tracked governing branch state |
| `E6` | `T5` | Named edge cases need direct proof rather than code-shape inference |
| `E7` | `T2` | Local-only artifacts may inform background but cannot support branch-scoped authority |

## Edge case coverage

- `implement` may report milestone completion or readiness for `code-review`, but not review-clean or branch-ready status: `T1`
- `code-review` may inspect staged or unstaged changes without requiring all reviewed code to be committed: `T2`
- Local-only governing artifacts may inform background understanding but cannot support clean branch-scoped conclusions: `T2`, `T3`
- Missing tracked governing authority blocks `clean-with-notes`, but supported `changes-requested` or `blocked` findings remain valid: `T3`
- `inconclusive` is allowed only when missing evidence prevents both a supported finding and a clean conclusion: `T3`, `T6`
- `verify` may block `branch-ready` even after a non-blocking implementation sanity check because those stages own different claims: `T4`
- Remaining unqualified `PR-ready` hits may survive only as negative guidance, forbidden examples, historical context, or quoted term definitions: `T4`
- A named edge case may be implemented correctly in code, but without direct proof it cannot support a clean branch-scoped review conclusion: `T5`
- This slice must preserve the earlier first-pass review record, status mapping, and review-resolution handoff contract: `T6`
- The first implementation slice must not introduce committed-only review, a review router, or validator-backed wording enforcement: `T7`

## Test cases

### T1. `implement` uses stage-owned language and does not claim review outcomes

- Covers: `R1`, `R1a`, `R1b`, `E1`
- Level: manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched implementation-stage and shared workflow guidance.
  - Confirm `implement` may report implementation completion, milestone validation, blockers, readiness for `code-review`, or the next milestone.
  - Confirm `implement` does not claim completed review findings, review-clean status, or `branch-ready`.
  - Confirm examples or templates do not say “post-implementation review found no required fixes” or equivalent review-owned conclusions.
- Expected result:
  - Implementation-stage wording stays inside implementation ownership and hands off cleanly to `code-review`.
- Failure proves:
  - The implementation stage can still masquerade as review completion or pre-claim readiness owned by later stages.
- Automation location:
  - Manual review during M1.

### T2. `code-review` distinguishes review surface from tracked governing branch state

- Covers: `R1c`, `R2`, `R2a`, `R2b`, `R2c`, `R2d`, `R2e`, `E2`, `E7`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched `code-review`, workflow, and durable workflow-spec wording.
  - Confirm the glossary and operative guidance distinguish the review surface from tracked governing branch state.
  - Confirm `code-review` may inspect changed files, staged changes, unstaged diffs, PR diffs, or commit ranges.
  - Confirm cited governing artifacts must be confirmed in tracked governing branch state before they support a clean branch-scoped conclusion.
  - Confirm local-only governing artifacts are background only and cannot support clean branch-scoped authority.
- Expected result:
  - The reviewed code surface and the tracked authority supporting branch-scoped conclusions are distinct and both are explained consistently across touched surfaces.
- Failure proves:
  - The implementation still blurs filesystem visibility with tracked governing authority or silently reintroduces a committed-only review rule.
- Automation location:
  - Manual review during M1.

### T3. Missing tracked authority blocks clean results without suppressing supported findings

- Covers: `R2f`, `R2g`, `R2h`, `R2i`, `R2j`, `R2k`, `E3`, `E4`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
- Steps:
  - Review the mixed-evidence rule in touched review and workflow guidance.
  - Confirm missing tracked governing authority prevents `clean-with-notes`.
  - Confirm a directly supported fixable defect still yields `changes-requested` even when tracked authority for a clean result is incomplete.
  - Confirm a directly supported blocking defect still yields `blocked` even when tracked authority for a clean result is incomplete.
  - Confirm `inconclusive` is reserved for cases where missing evidence prevents both a supported finding and a clean conclusion.
  - Confirm `inconclusive` output identifies the missing tracked governing artifacts when that missing authority contributed to the outcome.
- Expected result:
  - The mixed-evidence rule prevents unsupported clean outcomes without erasing real findings the review surface supports directly.
- Failure proves:
  - Missing governing authority can still produce unsupported clean outcomes, or it incorrectly suppresses supported review findings.
- Automation location:
  - Manual review during M1.

### T4. `verify` owns `branch-ready` and residual unqualified `PR-ready` hits are manually classified

- Covers: `R1d`, `R1e`, `R1f`, `R2l`, `R2m`, `R2n`, `E5`
- Level: manual
- Fixture/setup:
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/explain-change/SKILL.md` when touched
  - `skills/workflow/SKILL.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched `verify`, `pr`, and shared workflow guidance.
  - Confirm `verify` owns `branch-ready` and treats missing authoritative tracked artifacts as `blocked`, not `ready` or `concerns`.
  - Confirm `pr` guidance uses `pr-body-ready` and `pr-open-ready` where the approved contract applies.
  - Run the targeted `rg` path named in the active plan for `PR-ready`.
  - Manually classify every remaining unqualified `PR-ready` hit in touched workflow-facing surfaces.
  - Confirm any surviving unqualified hits are only negative guidance, forbidden examples, historical context, or quoted term definitions, and not live output guidance or status language.
- Expected result:
  - Readiness ownership is explicit and any remaining unqualified `PR-ready` usage is intentionally non-operative.
- Failure proves:
  - Earlier stages can still pre-claim `branch-ready`, or touched surfaces still use unqualified `PR-ready` as live guidance.
- Automation location:
  - Manual review during M1 plus the targeted `rg` command from the active plan.

### T5. Named edge cases require direct proof and unresolved gaps block clean outcomes

- Covers: `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `E6`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched review and verification guidance for named edge-case proof handling.
  - Confirm clean `code-review` results must cite direct proof for named edge cases from the approved spec or active test spec.
  - Confirm acceptable proof is limited to targeted automated tests, targeted validation output, or an explicit manual verification note when allowed.
  - Confirm code-shape inference alone is explicitly insufficient.
  - Confirm actionable proof gaps become findings and unresolved proof gaps block clean review or `branch-ready`.
- Expected result:
  - Named edge cases require real evidence rather than inferential confidence.
- Failure proves:
  - The implementation still permits unsupported clean conclusions for named test-spec paths.
- Automation location:
  - Manual review during M1.

### T6. Earlier `code-review` independence guarantees remain intact

- Covers: `R4`, `R4a`, `R4b`
- Level: manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/code-review-independence-under-autoprogression.md`
  - `specs/code-review-independence-under-autoprogression.test.md`
  - `docs/workflows.md`
- Steps:
  - Compare the touched workflow-facing guidance against the earlier `code-review` independence spec and active test spec.
  - Confirm `code-review` still produces a first-pass review record before any review fixes are applied.
  - Confirm the approved review statuses remain `blocked`, `changes-requested`, `clean-with-notes`, and `inconclusive`.
  - Confirm a clean review cannot be a bare “looks good” result and still requires checklist coverage plus no-finding rationale.
  - Confirm missing required review evidence still yields `inconclusive` unless the review surface independently supports a finding.
  - Confirm fixable findings still flow to `review-resolution` in workflow-managed mode when no stop condition applies.
  - Confirm isolated `code-review` and review-only requests still stop after the first-pass review record.
  - Confirm the new branch-reality and traceability requirements add evidence constraints without weakening the earlier independence contract.
- Expected result:
  - The feature supplements the earlier independence contract instead of silently replacing or narrowing it.
- Failure proves:
  - The new contract regressed first-pass review behavior or invalidated previously approved status and stop-condition semantics.
- Automation location:
  - Manual review during M1.

### T7. The enduring invariant lands in the durable workflow spec and v1 scope remains narrow

- Covers: `R4c`, `R4d`, `R4e`
- Level: manual
- Fixture/setup:
  - `specs/code-review-branch-reality-and-traceability.md`
  - `specs/rigorloop-workflow.md`
  - `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - touched workflow-facing skills and docs
- Steps:
  - Review the final implementation diff against the approved spec and active plan.
  - Confirm the enduring invariant is folded into `specs/rigorloop-workflow.md` and the focused spec remains the change vehicle rather than the only durable home.
  - Confirm the implementation stays inside the approved first slice: contract updates, skill wording, test-spec coverage, and manual or document review.
  - Confirm the implementation does not introduce committed-only review, a review router, or validator-backed enforcement for forbidden implement-stage wording.
- Expected result:
  - The durable workflow rule is updated and the v1 slice remains wording-first and narrowly scoped.
- Failure proves:
  - The implementation either left the invariant stranded in the focused spec or widened the slice beyond the approved contract.
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
- Expected result:
  - Canonical skills are valid and generated compatibility output remains synchronized with the authored changes.
- Failure proves:
  - The feature changed workflow-facing skills without keeping the derived distribution surface valid and in sync.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`

### T9. Lifecycle-managed artifacts, metadata, and repo smoke validation stay green

- Covers: supporting proof for touched authoritative artifacts and repo-owned smoke validation
- Level: integration, smoke
- Fixture/setup:
  - `docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md`
  - `specs/code-review-branch-reality-and-traceability.md`
  - `specs/code-review-branch-reality-and-traceability.test.md`
  - `specs/rigorloop-workflow.md`
  - `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml` once created
  - repo-owned validation wrapper
- Steps:
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml` once the baseline change-local pack exists.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`.
  - Run `git diff --check -- specs/code-review-branch-reality-and-traceability.test.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md docs/changes/2026-04-22-code-review-branch-reality-and-traceability .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md docs/plan.md`.
  - Run `bash scripts/ci.sh` after implementation lands.
  - Confirm the touched lifecycle-managed artifacts remain internally consistent and the repo-owned smoke path passes.
- Expected result:
  - The authoritative artifacts stay lifecycle-valid, metadata stays valid once created, and the repository smoke path still passes after the workflow-contract changes.
- Failure proves:
  - The feature left stale lifecycle state behind or broke a required repo-owned validation surface.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - `git diff --check -- specs/code-review-branch-reality-and-traceability.test.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md docs/changes/2026-04-22-code-review-branch-reality-and-traceability .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md docs/plan.md`
  - `bash scripts/ci.sh`

## Fixtures and data

- Real repository workflow and proof surfaces:
  - `specs/code-review-branch-reality-and-traceability.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/explain-change/SKILL.md` when touched
  - generated `.codex/skills/`
- Overlapping proof and compatibility fixtures:
  - `specs/code-review-independence-under-autoprogression.md`
  - `specs/code-review-independence-under-autoprogression.test.md`
- The active plan acts as a proof fixture for first-pass scope, validation commands, and the manual classification rule for residual `PR-ready` hits:
  - `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`

## Mocking/stubbing policy

- No mocks or stubs are needed.
- Use real repository files and repo-owned validation scripts because this feature is about contributor-visible workflow behavior, not isolated runtime logic.
- If a later follow-up adds validator-backed wording enforcement or another executable subsystem, that later change should define its own fixture strategy separately.

## Migration or compatibility tests

- Manual verification that the implementation preserves compatibility with the earlier workflow baseline:
  - `implement -> code-review -> review-resolution when needed -> verify` stage order remains unchanged
  - the first-pass review record and review-status rules from the earlier independence contract remain intact
  - the feature does not introduce committed-only review
  - the feature does not add a review router, readiness registry, or validator-backed wording enforcement in v1
  - broad `PR-ready` wording is replaced where it remains live guidance, while quoted negative guidance may survive intentionally

## Observability verification

- Manual review must be able to tell from touched workflow-facing outputs:
  - when a stage is reporting implementation completion versus review findings
  - which cited governing artifacts were confirmed in tracked governing branch state
  - when missing tracked governing authority blocked `clean-with-notes` but did not suppress supported findings
  - when `branch-ready` is blocked by missing authoritative tracked artifacts
  - when named edge-case coverage is backed by direct proof rather than inference
  - when any remaining unqualified `PR-ready` term is only a forbidden example or negative guidance

## Security/privacy verification

- Confirm the wording change introduces no new network, secret, or credential dependency.
- Confirm examples and output guidance do not encourage exposing credentials, secrets, or sensitive local-only paths while reporting missing governing artifacts or proof gaps.
- Confirm the feature does not weaken higher-priority security or human-review requirements for sensitive changes.

## Performance checks

- Not applicable. This feature changes workflow guidance and proof surfaces, not product runtime behavior.

## Manual QA checklist

- [ ] `implement` guidance reports completion and readiness for `code-review` without claiming review outcomes.
- [ ] `code-review` guidance distinguishes review surface from tracked governing branch state.
- [ ] Missing tracked governing authority blocks `clean-with-notes` but does not suppress directly supported `changes-requested` or `blocked` findings.
- [ ] `inconclusive` appears only when missing evidence prevents both a supported finding and a clean conclusion.
- [ ] `verify` owns `branch-ready` and blocks missing authoritative tracked artifacts.
- [ ] `pr` guidance uses `pr-body-ready` and `pr-open-ready` where the approved contract applies.
- [ ] Every remaining unqualified `PR-ready` hit in touched workflow-facing surfaces has been manually classified and any live guidance usage has been replaced.
- [ ] Named edge cases require direct proof and do not rely on code-shape inference alone.
- [ ] The earlier `code-review` independence guarantees still hold, including first-pass review record shape, approved statuses, clean-review evidence requirements, `review-resolution` handoff, and isolated-review stop behavior.
- [ ] The enduring invariant is folded into `specs/rigorloop-workflow.md` and the v1 slice remains validator-free and narrowly scoped.
- [ ] Skill, lifecycle, metadata, and smoke validation commands named in the active plan all remain on the implementation proof path.

## What not to test

- Do not invent executable runtime unit or end-to-end tests for product behavior; this feature is intentionally workflow-contract driven.
- Do not treat validator-backed enforcement for forbidden implement-stage wording as part of v1 proof.
- Do not broaden the proof surface into a general rewrite of all workflow-facing skills outside the approved first slice.
- Do not require all remaining historical references to the unqualified term `PR-ready` to disappear when they are intentionally negative guidance or quoted terminology.

## Uncovered gaps

- None. The approved spec and active plan are specific enough to support focused manual and repo-owned structural proof without returning to spec or architecture.

## Next artifacts

- `explain-change`
- `pr`

## Follow-on artifacts

None yet.

## Readiness

This test spec is active.

It remained aligned through implementation, first-pass `code-review`, and `verify` for `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`.

It also remained aligned through the 2026-04-23 mixed-evidence follow-up and the later local overlap-spec cleanup for `specs/plan-index-lifecycle-ownership.md` and `specs/rigorloop-workflow.md`.

PR #14 merged into `main` at `c06a3cd7e0ae422c0f14a9bd1047d84e592534c0`.

No separate architecture artifact is expected for this slice.

No further workflow stage is pending.

If implementation reveals a need for architecture or a broader workflow redesign, stop and return to the appropriate upstream gate instead of proceeding on this test spec alone.
