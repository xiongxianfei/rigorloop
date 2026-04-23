# Code review branch reality and traceability plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-22
- Last updated: 2026-04-22
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved workflow-contract follow-up that closes the remaining review-credibility gap after the earlier `code-review` independence work.

This initiative should make the repository's durable workflow spec, short workflow summary, and directly affected workflow-facing skills say the same thing about:

- stage-owned language for `implement`, `code-review`, `verify`, and `pr`;
- the distinction between review surface and tracked governing branch state;
- mixed-evidence review behavior, where missing tracked governing authority blocks `clean-with-notes` but does not suppress supported findings;
- `branch-ready`, `pr-body-ready`, and `pr-open-ready` as qualified readiness terms instead of broad `PR-ready`; and
- direct proof expectations for named edge cases.

The implementation must stay inside the approved first slice:

- no new workflow stage;
- no committed-only review requirement;
- no full review-orchestration subsystem;
- no validator-backed wording enforcement in v1; and
- no separate architecture artifact unless the work expands beyond workflow guidance and skill alignment.

## Source artifacts

- Proposal: `docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md`
- Spec: `specs/code-review-branch-reality-and-traceability.md`
- Spec-review findings carried into this plan: none pending. The approved spec already incorporates the glossary split between review surface and tracked governing branch state, the mixed-evidence status rule, and the qualified readiness terms.
- Architecture: none. The approved spec says no separate architecture artifact is expected for this slice.
- Architecture-review findings: none.
- Test spec: `specs/code-review-branch-reality-and-traceability.test.md`
- Related workflow and proof surfaces:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/explain-change/SKILL.md` only if its current wording still uses broad `PR-ready`
  - generated `.codex/skills/`

## Context and orientation

- This is workflow-governance work, not runtime product behavior, but it is compatibility-sensitive because it changes contributor-visible workflow guidance and the durable workflow spec.
- The focused approved spec is the change vehicle. Implementation must also fold the enduring invariant into `specs/rigorloop-workflow.md` without leaving the focused spec as a second long-term normative home.
- The main authored surfaces likely to change are:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/explain-change/SKILL.md` only if wording drift is still present there
  - `AGENTS.md` if the approved workflow wording materially changes the practical agent summary
  - `CONSTITUTION.md` only if the work rises to a governance or principle change instead of lower-level workflow guidance
  - `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
  - `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/explain-change.md`
  - generated `.codex/skills/`
- Generated `.codex/skills/` output remains derived. Regenerate it; do not hand-edit it.
- The repository currently has no `docs/project-map.md`. The change is narrow enough that a project map is not required for planning.
- This is ordinary non-trivial work. Implementation must carry the baseline change-local pack:
  - `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
  - `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/explain-change.md`
- Current wording drift already matters for planning:
  - `skills/verify/SKILL.md` still says `PR-ready`
  - `skills/explain-change/SKILL.md` still says `PR-ready summary bullets`
  - `skills/pr/SKILL.md` still says “PR ready” in rules
  These surfaces should be updated only as needed to align with the approved qualified readiness terms, not widened into a broader PR-surface rewrite.

## Non-goals

- Requiring a human reviewer for every change.
- Restricting `code-review` to committed code only.
- Replacing `code-review` with `verify`, tests, or validators alone.
- Redesigning workflow stage order or autoprogression.
- Solving every review-quality problem across every workflow-facing skill in one pass.
- Adding validator enforcement for forbidden implement-stage review language in the same v1 slice.
- Creating a new readiness registry or orchestration subsystem.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R1f`, observability, acceptance criteria about stage-owned language and qualified readiness terms | `skills/implement/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/explain-change/SKILL.md` if needed, `skills/workflow/SKILL.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, generated `.codex/skills/` |
| `R2`-`R2n`, error/boundary behavior, acceptance criteria about review surface, tracked governing branch state, mixed-evidence outcomes, and `branch-ready` blocking | `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/workflow/SKILL.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, generated `.codex/skills/` |
| `R3`-`R3f`, observability and acceptance criteria about direct proof for named edge cases | `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/workflow/SKILL.md`, focused future test spec, generated `.codex/skills/` |
| `R4`-`R4e`, compatibility/migration, non-goals, and v1 scope control | `specs/rigorloop-workflow.md`, `docs/workflows.md`, `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/`, generated `.codex/skills/` |

## Milestones

### M1. Implement branch-reality and traceability alignment

- Goal:
  - Align the durable workflow spec, short workflow summary, directly affected workflow-facing skills, qualified PR-surface terms, and generated output with the approved contract without broadening stage order or v1 automation scope.
- Requirements:
  - `R1`-`R4e`
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/explain-change/SKILL.md` only if wording drift is still present
  - `AGENTS.md` if the guidance-impact check shows practical workflow guidance changed
  - `CONSTITUTION.md` only if the same check shows a governance or principle change rather than lower-level workflow guidance
  - `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
  - `docs/changes/2026-04-22-code-review-branch-reality-and-traceability/explain-change.md`
  - generated `.codex/skills/`
- Dependencies:
  - accepted proposal
  - approved focused spec
  - `plan-review`
  - active focused test spec created after `plan-review`
  - no separate architecture artifact unless scope expands beyond the approved slice
- Tests to add/update:
  - create `specs/code-review-branch-reality-and-traceability.test.md` as the focused proof surface for M1
  - require the focused test spec to prove `implement` does not claim review findings or review-clean status
  - require the focused test spec to prove `code-review` distinguishes review surface from tracked governing branch state
  - require the focused test spec to prove missing tracked governing authority blocks `clean-with-notes` but does not suppress independently supported `changes-requested` or `blocked` findings
  - require the focused test spec to prove `inconclusive` is used only when missing evidence prevents both a supported finding and a clean conclusion
  - require the focused test spec to prove `verify` blocks `branch-ready` when required authoritative artifacts are missing from tracked governing branch state
  - require the focused test spec to prove workflow-facing outputs use `branch-ready`, `pr-body-ready`, and `pr-open-ready` instead of broad `PR-ready` where the approved contract applies
  - require the focused test spec to prove named edge cases need direct proof and cannot rely on code-shape inference alone
  - require the focused test spec to prove compatibility with `specs/code-review-independence-under-autoprogression.md`, specifically that this change preserves:
    - first-pass review records before any review fixes are applied
    - the approved `blocked`, `changes-requested`, `clean-with-notes`, and `inconclusive` review statuses
    - the rule that a clean review cannot be a bare "looks good" result
    - the requirement that `clean-with-notes` includes checklist coverage plus no-finding rationale
    - the rule that missing required review evidence yields `inconclusive` unless the review surface independently supports a finding
    - workflow-managed `review-resolution` handoff for fixable findings when no stop condition applies
    - isolated `code-review` and review-only requests stopping after the first-pass review record
    - the invariant that branch-reality and traceability rules add evidence requirements without weakening the earlier independence contract
  - require the focused test spec to prove the touched workflow-facing skill surfaces, workflow summary, durable workflow spec, and generated `.codex/skills/` output stay aligned
  - update any currently active broader proof surface only if implementation reveals genuine overlap that would otherwise drift
- Implementation steps:
  - update `specs/rigorloop-workflow.md` to record the enduring invariant for:
    - stage-owned language across `implement`, `code-review`, `verify`, and `pr`
    - review surface versus tracked governing branch state
    - mixed-evidence handling for `clean-with-notes`, `changes-requested`, `blocked`, and `inconclusive`
    - `branch-ready`, `pr-body-ready`, and `pr-open-ready` as qualified readiness terms where the workflow spec needs them
    - direct proof expectations for named edge cases
  - update `skills/implement/SKILL.md` so its closeout language stays inside implementation ownership and does not imply review conclusions
  - update `skills/code-review/SKILL.md` so it reflects the glossary split, mixed-evidence rule, and direct-proof expectations for named edge cases
  - update `skills/verify/SKILL.md` so it owns `branch-ready`, blocks missing tracked authoritative support, and removes broad `PR-ready` wording
  - update `skills/pr/SKILL.md` so its readiness wording uses the approved qualified terms where relevant instead of broad `PR ready`
  - inspect `skills/explain-change/SKILL.md` and update it only where its expected-output wording still conflicts with the approved readiness terminology
  - update `skills/workflow/SKILL.md` and `docs/workflows.md` only where the shared workflow summary must mention the new invariant to avoid stale contributor guidance
  - explicitly assess whether the approved contract affects `AGENTS.md` or `CONSTITUTION.md`
  - if `AGENTS.md` is affected because practical workflow guidance changed, update it in this milestone
  - if `CONSTITUTION.md` is affected because the change rises to a governance or principle change, update it in this milestone
  - if neither file is affected, record that no-change decision in the plan validation notes instead of leaving the omission implicit
  - create the baseline change-local pack for this initiative
  - regenerate `.codex/skills/` after canonical skill changes
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - `rg -n 'review surface|tracked governing branch state|branch-ready|pr-body-ready|pr-open-ready|clean-with-notes|changes-requested|blocked|inconclusive|direct proof|PR-ready' skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md .codex/skills`
  - `rg -n 'workflow|review|verify|pr-ready|branch-ready|pr-body-ready|pr-open-ready' AGENTS.md CONSTITUTION.md docs/workflows.md specs/rigorloop-workflow.md`
  - `git diff --check -- specs/code-review-branch-reality-and-traceability.test.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md docs/changes/2026-04-22-code-review-branch-reality-and-traceability .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md docs/plan.md`
  - `bash scripts/ci.sh`
- Expected observable result:
  - the durable workflow spec, workflow summary, directly affected workflow-facing skills, and generated output all use the approved contract for stage-owned language, review surface versus tracked governing branch state, mixed-evidence status handling, qualified readiness terms, and direct proof for named edge cases.
- Commit message: `M1: implement branch reality and traceability alignment`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] lifecycle state updated in `docs/plan.md` and this plan body if the milestone changed it
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - `specs/code-review-branch-reality-and-traceability.md` and `specs/rigorloop-workflow.md` may drift if the implementation duplicates rather than folds the durable invariant cleanly
  - unqualified `PR-ready` wording may persist in a touched workflow-facing surface if the search scope is too narrow
  - `AGENTS.md` or `CONSTITUTION.md` may be over-edited when no practical or principle-level guidance change actually occurred
  - the absence of a v1 validator means wording drift must be caught through the focused test spec and review surfaces
- Rollback/recovery:
  - revert canonical and generated workflow-facing skill changes together
  - revert `specs/rigorloop-workflow.md` together with the focused skill updates if the invariant lands inconsistently
  - if implementation shows a broader workflow or architecture problem than approved, stop and create a separate proposal or architecture track instead of widening M1 silently

## Validation plan

- Before implementation:
  - `plan-review` is complete
  - the active focused test spec `specs/code-review-branch-reality-and-traceability.test.md` now owns proof for:
    - stage-owned language in `implement`
    - review surface versus tracked governing branch state
    - mixed-evidence handling across `clean-with-notes`, `changes-requested`, `blocked`, and `inconclusive`
    - `branch-ready` blocked on missing tracked authoritative artifacts
    - qualified `branch-ready`, `pr-body-ready`, and `pr-open-ready` terminology
    - direct proof requirements for named edge cases
    - touched workflow-facing skills, workflow summary, durable workflow spec, and generated output staying aligned
  - confirm whether any currently active broader proof surface needs overlap updates; do not widen proof ownership unless implementation reveals genuine drift risk
- During implementation:
  - run the narrow skill and generation checks first:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/test-artifact-lifecycle-validator.py`
    - `python scripts/build-skills.py`
    - `python scripts/build-skills.py --check`
  - run `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml` once the change-local pack exists
  - run explicit-path artifact validation once the focused test spec exists and `specs/rigorloop-workflow.md` is touched
  - record the explicit `AGENTS.md` / `CONSTITUTION.md` impact decision in validation notes
  - use targeted `rg` and `git diff --check` commands before the repo-wide smoke pass
  - manually classify every remaining unqualified `PR-ready` hit in touched workflow-facing surfaces after the targeted `rg` pass
  - allow remaining unqualified `PR-ready` hits only when they are negative guidance, forbidden examples, historical context, or quoted term definitions
  - replace any live output guidance or status language that still uses unqualified `PR-ready`
- Final milestone proof:
  - run `bash scripts/ci.sh`
  - record the exact commands and results in this plan body's validation notes

## Risks and recovery

- Risk: the focused spec and `specs/rigorloop-workflow.md` diverge.
  - Recovery: treat the focused spec as the change vehicle only, fold the enduring invariant into `specs/rigorloop-workflow.md`, and verify both artifacts together.
- Risk: stage-owned language changes land in `implement`, `verify`, `pr`, and `explain-change` inconsistently.
  - Recovery: keep the review surface versus tracked-governing-state vocabulary and qualified readiness terms synchronized across all touched guidance surfaces and rerun targeted `rg` plus lifecycle proof.
- Risk: the work expands into a broader review-skill normalization effort.
  - Recovery: keep the first implementation pass limited to the approved contract surfaces and stop for re-planning if new workflow classes need redesign.
- Risk: the absence of a validator leaves wording drift possible.
  - Recovery: make the future focused test spec and manual/document review surfaces explicit enough to catch the drift in v1.

## Dependencies

- `plan-review` is complete.
- the active focused test spec now exists and must remain the proof surface before production guidance changes begin.
- no separate architecture artifact is planned; if implementation expands beyond workflow guidance and skill alignment, stop and create architecture before implementation.
- the baseline change-local pack for this ordinary non-trivial change is required during implementation.
- generated `.codex/skills/` output must stay synchronized with canonical `skills/`.

## Progress

- [x] 2026-04-22: proposal accepted and focused spec approved.
- [x] 2026-04-22: plan created and indexed in `docs/plan.md`.
- [x] 2026-04-22: focused active test spec created for this initiative.
- [x] 2026-04-22: M1 implementation completed with canonical and generated workflow guidance aligned; first-pass `code-review` is the next stage.
- [x] 2026-04-22: first-pass `code-review` completed with `clean-with-notes` and `verify` completed with verdict `ready`; the next stage is `explain-change`.

## Decision log

- 2026-04-22: No separate architecture artifact is planned for the first slice. Rationale: the approved spec limits the implementation to workflow guidance, workflow summary, and directly affected workflow-facing skills.
- 2026-04-22: Start with one implementation milestone. Rationale: the expected authored surfaces are narrow enough for one coherent review loop and one coherent commit; split later only if implementation expands.
- 2026-04-22: Include `skills/pr/SKILL.md` and conditionally `skills/explain-change/SKILL.md` in the first-pass plan. Rationale: current repo wording already contains broad `PR-ready` references that conflict with the approved qualified terms, but the fix should stay as narrow as possible.
- 2026-04-22: `AGENTS.md` and `CONSTITUTION.md` require an explicit impact decision rather than an implicit omission. Rationale: workflow guidance changes can affect practical agent behavior or governance expectations even when the likely implementation stays below that threshold.
- 2026-04-22: `AGENTS.md` and `CONSTITUTION.md` stay unchanged in M1. Rationale: the implementation changes workflow contract wording and operational guidance in `specs/rigorloop-workflow.md`, `docs/workflows.md`, and the directly affected skills, but it does not change the concise repository summary or governing principles enough to justify edits in this slice.

## Surprises and discoveries

- 2026-04-22: The repository currently has no `docs/project-map.md`. The feature is still narrow enough that a project map is not required.
- 2026-04-22: Unqualified `PR-ready` wording already exists in `skills/verify/SKILL.md` and `skills/explain-change/SKILL.md`, and `skills/pr/SKILL.md` still says “PR ready” in rules.
- 2026-04-22: `docs/plan.md` currently has no active initiatives, so this plan becomes the sole active entry when created.
- 2026-04-22: Running `python scripts/build-skills.py` and `python scripts/build-skills.py --check` in parallel produced a false drift failure. The stable proof path is sequential generation followed by the drift check.
- 2026-04-23: An isolated code-review found one remaining mixed-evidence contradiction between `skills/code-review/SKILL.md` and the older approved `code-review` independence spec/test surfaces. Resolving it required touching those overlapping authoritative surfaces, which M1 had explicitly allowed when real overlap drift appeared.

## Validation notes

- 2026-04-22: plan creation validation passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - `git diff --check -- docs/plan.md docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md specs/code-review-branch-reality-and-traceability.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - Result: passed.
- 2026-04-22: plan-review feedback incorporated:
  - added explicit focused-test-spec proof requirements for compatibility with the earlier `code-review` independence contract
  - added manual classification requirements for any remaining unqualified `PR-ready` hits in touched workflow-facing surfaces
- 2026-04-22: focused test spec creation validation passed with:
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - `git diff --check -- docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md specs/code-review-branch-reality-and-traceability.md specs/code-review-branch-reality-and-traceability.test.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - Result: passed.
- 2026-04-22: implementation validation passed with:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
  - `rg -n 'review surface|tracked governing branch state|branch-ready|pr-body-ready|pr-open-ready|clean-with-notes|changes-requested|blocked|inconclusive|direct proof|PR-ready' skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md .codex/skills`
  - `rg -n 'workflow|review|verify|pr-ready|branch-ready|pr-body-ready|pr-open-ready' AGENTS.md CONSTITUTION.md docs/workflows.md specs/rigorloop-workflow.md`
  - `git diff --check -- specs/code-review-branch-reality-and-traceability.test.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md docs/changes/2026-04-22-code-review-branch-reality-and-traceability .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md docs/plan.md`
  - `bash scripts/ci.sh`
  - Result: passed.
- 2026-04-22: `AGENTS.md` / `CONSTITUTION.md` impact decision:
  - `AGENTS.md`: no change required in M1 because the practical workflow summary remains accurate once `docs/workflows.md` is updated.
  - `CONSTITUTION.md`: no change required in M1 because the slice refines workflow contract wording without changing governing principles.
- 2026-04-22: residual unqualified `PR-ready` hits were manually classified:
  - allowed survivors are negative guidance or quoted term definitions in `skills/workflow/SKILL.md`, `specs/rigorloop-workflow.md`, and the focused spec and test spec.
  - no touched workflow-facing live guidance or output template still uses unqualified `PR-ready` in `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/explain-change/SKILL.md`, or `docs/workflows.md`.
- 2026-04-22: no `docs/plan.md` lifecycle update was needed after M1 implementation or the first-pass review. The initiative remains active, so the existing `## Active` entry stays truthful while the plan body moves from `implement` readiness into downstream review readiness.
- 2026-04-22: first-pass `code-review` record for `297a010^..297a010`.
  - Review status: `clean-with-notes`
  - Review inputs:
    - Diff range: `297a010^..297a010`
    - Review surface: committed diff for `297a010^..297a010`
    - Tracked governing branch state: `HEAD` at `297a0104a50f9797870b8c424598b568517acfbe`, with the proposal, focused spec, focused test spec, active plan, and `specs/rigorloop-workflow.md` confirmed in tracked state via `git ls-files`
    - Spec: `specs/code-review-branch-reality-and-traceability.md`
    - Test spec: `specs/code-review-branch-reality-and-traceability.test.md`
    - Plan milestone: `M1`
    - Architecture / ADR: none for this approved first slice
    - Validation evidence: `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/test-artifact-lifecycle-validator.py`, `python scripts/build-skills.py`, `python scripts/build-skills.py --check`, `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`, `bash scripts/ci.sh`
  - Diff summary: the committed range adds the approved proposal/spec/test-spec/plan stack, folds the durable branch-reality and traceability invariant into `specs/rigorloop-workflow.md`, aligns the directly affected workflow-facing skills and `docs/workflows.md` with the new stage-owned language and evidence rules, regenerates `.codex/skills/`, and records the implementation proof path in the active plan and change-local pack.
  - Findings: no blocking or required-change findings.
  - Checklist coverage:
    - Spec alignment: pass (`specs/rigorloop-workflow.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/workflow/SKILL.md`, `skills/pr/SKILL.md`, and `docs/workflows.md` implement the approved contract without widening the slice.)
    - Test coverage: pass (the focused test spec names the exact proof surface and the implementation validation followed the repo-owned commands named in the plan.)
    - Edge cases: pass (`skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, and `specs/rigorloop-workflow.md` explicitly require direct proof for named edge cases and block unsupported clean conclusions.)
    - Error handling: pass (`code-review` now uses `inconclusive` only when missing evidence prevents both a supported finding and a clean conclusion; `verify` blocks missing authoritative tracked artifacts for `branch-ready`.)
    - Architecture boundaries: pass (the change stayed within the approved workflow-guidance slice and did not introduce validators, routers, or stage-order redesign.)
    - Compatibility: pass (`specs/rigorloop-workflow.md` preserves the earlier `code-review` independence contract and `docs/workflows.md` keeps `implement -> code-review -> verify` intact.)
    - Security/privacy: pass (the wording changes add no new secret-bearing path and preserve the rule against exposing sensitive values in review or verification outputs.)
    - Generated output drift: pass (`python scripts/build-skills.py` plus `python scripts/build-skills.py --check` kept `.codex/skills/` synchronized with canonical `skills/`.)
    - Unrelated changes: pass (the diff is limited to this initiative's workflow artifacts, directly affected skills, summary docs, generated mirrors, and change-local pack.)
    - Validation evidence: pass (the plan and change metadata name the actual repo-owned commands and they passed on the touched scope.)
  - No-finding rationale: no blocking findings were found because the diff matches the approved spec and plan scope, the focused test spec covers the changed contract, the governing artifacts cited in the review are tracked in the reviewed branch state, and the recorded validation evidence supports the implementation.
  - Recommended next stage: `verify`
- 2026-04-22: `verify` passed on the implementation plus the post-review lifecycle bookkeeping.
  - Verification verdict: `ready`
  - Traceability:
    - `R1`-`R1f` -> `T1`, `T4` -> `specs/rigorloop-workflow.md`, `skills/implement/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/explain-change/SKILL.md`, `docs/workflows.md` -> committed diff plus clean review record and verify validation commands -> pass
    - `R2`-`R2n` -> `T2`, `T3`, `T4` -> `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `specs/rigorloop-workflow.md`, active plan review record -> tracked-governing-state proof, mixed-evidence handling, and `branch-ready` blocking rules -> pass
    - `R3`-`R3f` -> `T5` -> `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `specs/rigorloop-workflow.md`, `docs/workflows.md` -> direct-proof wording and named-edge-case blocking behavior -> pass
    - `R4`-`R4e` -> `T6`, `T7`, `T8`, `T9` -> `specs/rigorloop-workflow.md`, active test spec, active plan, `.codex/skills/`, and change-local pack -> preserved earlier `code-review` independence contract, narrow v1 scope, generated-output sync, lifecycle validity, and smoke proof -> pass
  - Validation commands:
    - `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
    - `rg -n '^## (Active|Blocked|Done|Superseded)$|2026-04-22-code-review-branch-reality-and-traceability' docs/plan.md`
    - `git diff --check -- docs/plan.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md specs/code-review-branch-reality-and-traceability.test.md docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml docs/changes/2026-04-22-code-review-branch-reality-and-traceability/explain-change.md`
    - `bash scripts/ci.sh`
  - CI status: local repo-owned CI wrapper passed via `bash scripts/ci.sh`; hosted CI remains unobserved from this environment.
  - Artifact drift: none blocking. The active plan, active test spec, and change metadata now reflect the clean first-pass review result and ready verify outcome.
  - Remaining risks: hosted CI and eventual PR/base-branch readiness remain downstream concerns for later stages.
  - Recommended next stage: `explain-change`
- 2026-04-23: isolated code-review found a mixed-evidence contract contradiction after the earlier clean review.
  - Findings:
    - `major`: `skills/code-review/SKILL.md` still said missing authoritative upstream artifacts force `inconclusive`, which conflicted with the approved mixed-evidence rule.
    - `major`: `specs/code-review-independence-under-autoprogression.md` and `.test.md` still encoded the older absolute `inconclusive` rule, leaving two authoritative review contracts that could be read differently.
  - Resolution:
    - `Review-resolution: align mixed-evidence review contract` (`5a15a5c`) updated the canonical/generated `code-review` skill and the overlapping older approved spec/test surfaces so missing authoritative upstream artifacts prevent `clean-with-notes` but do not suppress independently supported `changes-requested` or `blocked` findings.
  - Validation commands:
    - `python scripts/validate-skills.py`
    - `python scripts/test-skill-validator.py`
    - `python scripts/build-skills.py`
    - `python scripts/build-skills.py --check`
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md`
    - `git diff --check -- skills/code-review/SKILL.md .codex/skills/code-review/SKILL.md specs/code-review-independence-under-autoprogression.md specs/code-review-independence-under-autoprogression.test.md`
    - `bash scripts/ci.sh`
  - Result: passed.
- 2026-04-23: rerun first-pass `code-review` for `5a15a5c^..5a15a5c`.
  - Review status: `clean-with-notes`
  - Review inputs:
    - Diff range: `5a15a5c^..5a15a5c`
    - Review surface: committed diff for `5a15a5c^..5a15a5c`
    - Tracked governing branch state: `HEAD` at `5a15a5cc84e7401778f56ce9eab68a471cc0a582`, with the canonical `code-review` skill, generated mirror, older approved `code-review` independence spec/test surfaces, and the current branch-reality spec all confirmed in tracked state
    - Spec: `specs/code-review-branch-reality-and-traceability.md`
    - Test spec: `specs/code-review-branch-reality-and-traceability.test.md`
    - Plan milestone: `M1`
    - Architecture / ADR: none for this approved slice
    - Validation evidence: `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, `python scripts/build-skills.py`, `python scripts/build-skills.py --check`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md`, `git diff --check -- skills/code-review/SKILL.md .codex/skills/code-review/SKILL.md specs/code-review-independence-under-autoprogression.md specs/code-review-independence-under-autoprogression.test.md`, `bash scripts/ci.sh`
  - Diff summary: the committed follow-up narrows one canonical `code-review` skill sentence and aligns the older approved `code-review` independence spec/test surfaces with the mixed-evidence rule already defined by the current branch-reality contract.
  - Findings: no blocking or required-change findings.
  - Checklist coverage:
    - Spec alignment: pass (the follow-up now matches the approved mixed-evidence rule instead of contradicting it.)
    - Test coverage: pass (the overlapping older test spec now proves the same mixed-evidence behavior rather than the superseded absolute `inconclusive` rule.)
    - Edge cases: pass (missing authoritative upstream artifacts now block `clean-with-notes` without erasing supported findings.)
    - Error handling: pass (the rerun preserves `inconclusive` only for cases where missing evidence prevents both a clean result and a supported finding.)
    - Architecture boundaries: pass (the follow-up stays inside the plan-approved overlap update for genuine proof-surface drift.)
    - Compatibility: pass (the repo no longer retains two contradictory authoritative review contracts for this rule.)
    - Security/privacy: pass (the wording-only fix adds no new sensitive-output path.)
    - Generated output drift: pass (`python scripts/build-skills.py` and `python scripts/build-skills.py --check` kept the generated mirror aligned.)
    - Unrelated changes: pass (the follow-up diff is limited to the single canonical/generated skill and the overlapping older spec/test surfaces.)
    - Validation evidence: pass (the rerun uses repo-owned validation plus the explicit overlap proof commands.)
  - No-finding rationale: no blocking findings were found because the committed follow-up removes the mixed-evidence contradiction without widening the feature scope, and the overlapping authoritative surfaces now agree on when `inconclusive` is required.
  - Recommended next stage: `verify`
- 2026-04-23: targeted `verify` rerun passed on the review-resolution follow-up.
  - Verification verdict: `ready`
  - Validation commands:
    - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md`
    - `git diff --check -- skills/code-review/SKILL.md .codex/skills/code-review/SKILL.md specs/code-review-independence-under-autoprogression.md specs/code-review-independence-under-autoprogression.test.md`
    - `bash scripts/ci.sh`
  - CI status: local repo-owned CI wrapper passed via `bash scripts/ci.sh`; hosted CI remains unobserved from this environment.
  - Artifact drift: none blocking for the follow-up diff.
  - Recommended next stage: `explain-change`

## Outcome and retrospective

- While the plan is still active, say so plainly instead of implying `Done`, `Blocked`, or `Superseded`.
- When the real lifecycle decision is known, update both this plan body and the single `docs/plan.md` entry in the same change.

## Readiness

- This plan is active.
- Plan-review feedback is incorporated.
- The focused active test spec now exists.
- M1 implementation is complete and recorded.
- First-pass `code-review` is recorded as `clean-with-notes`.
- `verify` is recorded as `ready`.
- The immediate next stage is `explain-change`.

## Risks and follow-ups

- Risk: the plan may still be too narrow if implementation reveals more workflow-facing surfaces with conflicting readiness language.
- Follow-up: add validator-backed enforcement only in a later approved initiative after the wording contract has stabilized.
