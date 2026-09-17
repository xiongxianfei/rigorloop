# Retire historical-path compatibility

## Purpose / big picture

Finish all selected historical-path retirement with canonical current routing, concise useful tests and consistent published guidance. Preserve the merged Release, Skill and Authoring test-design scope.

## Current Handoff Summary

- Owning change record: [historical-path retirement](../changes/2026-09-17-retire-historical-path-compatibility/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [complete retirement direction](../proposals/2026-09-17-retire-historical-path-compatibility.md).
- Spec: [Validation](../design/engineering/validation.md#current-path-support-and-retirement), [Design](../design/skill/authoring/design.md), [Workflow](../design/skill/workflow.md), [System](../design/system.md) and [Engineering](../design/engineering/engineering.md); no feature specification.
- Architecture: those owners' existing views; catalog, selector and executor remain the current pipeline.
- Prior-contract test spec: none; [System rules](../design/test-design/rules.md) and Validation's current test design govern proof.
- Exact upstream package: `historical-path-design-review-r2`, including the resolved `historical-support-consumer-reconciliation` finding and canonical model-authoring guidance.

## Context and orientation

Baseline `ddb7eb9e0d4669d360483eac080f8f05fedd5641` includes merged testing and feature-format retirement. Work uses the primary checkout on `codex/finish-compatibility-retirement`; the saved stash remains preserved. Do not restore it wholesale or create worktrees. Source history retains retired material; no historic record is retargeted.

`validation_selection.py` currently maps canonical tools back to predecessors before classifying them. Replace every consumer with direct current paths before deleting that machinery. Preserve both the current `scripts/release_evidence.py` wrapper and its internal module, plus live `validate-release.py` and `release-verify.sh`; `validate-release-ci.py` and both former `project_yaml.py` locations are obsolete. Exact model declarations retain the flat System root. Generic examples use their portable owner, never a historical-name substitution. Current record classification is an independent retained responsibility.

## Non-goals

- No additional model catalogs, new test framework, compatibility registry, runtime record migration, release redesign, publication or customer file conversion.
- No test-count target; deletion follows withdrawn obligations or established retained protection.

## Requirements covered

| Requirement basis | Allocation |
| --- | --- |
| VAL-SR-24/27/28/30/35 | M1, TG-PATHS and TG-MODELS: supported ownership, rejection, exact subject and retained detail safety. |
| ENG-SR-10/14/16, System TEST-SR-05/07/08/09/10/19/20/22 | M1, TG-PATHS and TG-MAINTENANCE: canonical consumer continuity and useful independent test oracles. |
| DES-SR-12/14/18, WF-SR-07/08, SYS-SR-05/13 | M1, TG-GUIDANCE: portable current targets, no implicit adoption or source mutation. |
| Complete approved all-family scope and cross-component failure hazards | TG-FINAL-1: actual branch routing, trusted executor and current committed records. |

## Milestones

### M1. Remove historical routing and prove current ownership

- Milestone kind: implementation.
- Engineering purpose: one coherent selector/validator/guidance slice avoids an intermediate state that loses current checks or advertises withdrawn input.
- Requirements: all rows above.
- Architecture responsibility: existing catalog construction, path classification, model admission and published authoring guidance.
- Dependencies: current independent Design Review and Delivery Review of this plan.
- Implementation scope: all six named retirement families, generic flat format, corresponding alternate trigger readers, exclusive tests/fixtures and required surviving consumers.
- Files/components likely touched: `scripts/lib/validation/{validation_selection,model_layout,boundary_first_validation}.py`, existing selection/model/catalog behavior modules, canonical Design guidance and generated candidate resources when required by current packaging.
- Required verification: TG-PATHS, TG-MODELS, TG-MAINTENANCE, TG-GUIDANCE and integrated TG-FINAL-1.
- Evidence expectations: observed fail-before/pass-after proof where feasible; independent canonical expected commands; group-level removal rationale and before/after discovery; actual validation results and limits.
- Implementation steps: establish new rejection and current canonical positive proof first; rewrite current paths and remove predecessor normalization; remove archive/examples, flat/relocation, retired tool and old document routes together; port shared safety fixtures to supported models; remove exclusive old compatibility cases; inspect remaining callers, resource generation and actual Git selection; run focused then required selected checks.
- Validation commands: the commands below, with targeted method filters for initial reproduction.
- Expected observable result: current inputs select their actual checks; unknown/unsupported inputs stay visibly unsuccessful, including mixed changes; current required-file failures and customer source bytes remain protected.
- Completion criteria: every selected family is retired, surviving proof is reachable and meaningful, required checks pass, and independent milestone Code Review is clean with concerns dispositioned by their reporter.
- Required evidence: registered M1 implementation evidence and exact-subject independent review.
- Review handoff: M1 complete diff against the approved package, then a separate fresh final whole-change review.
- Optional commit boundary: `M1: Retire historical-path compatibility`.
- Risks: canonical paths can lose checks hidden by predecessor normalization; broad fixture edits can discard shared safety; old-source substitution can survive in example or trigger helpers.
- Rollback/recovery: restore the coherent source/test/guidance slice from the baseline or implementation commit, preserve unrelated work and saved stash, and reassess changed evidence. Never recover by ignoring unknown paths or synthesizing successful checks.

### TG-PATHS. Current routing and unsupported inputs

Prove independent expected checks/commands for current validation, packaging and release modules, operational wrappers, test entrypoints, package initializers and resources. Include boundary/reference helpers and broad-smoke context consumers, not only the main classifier. Remove all selected historical maps/categories and exclusive paths: Skill archives, old examples, model aliases/move pairing, tool predecessors and obsolete commands/fixtures, legacy document deletion exceptions and fixed isolated evidence names. Representative unknown input with a known input must remain blocked, with no check launch through the public wrapper. Use real private Git trees for unstaged, staged and committed current deletion/rename endpoints and unknown companions. Current proposals/plans, release evidence and record-owned subjects retain their supported protection.

### TG-MODELS. Exact supported model admission

Through the public validator and selected command, prove a valid portable same-name model and explicit System model pass; a structurally valid generic flat model fails; absence, symlink and mixed valid/invalid inputs cannot be hidden by receiver substitution. Retain current marker/table/privacy checks and required catalog-detail failures. Use a supported portable path for shared symlink/read safety. Remove former Release-move replay tests while retaining current endpoint and trusted-command failure observations; indexed group deletion remains a failure until ownership is reconciled.

### TG-MAINTENANCE. Protection-based cleanup

Compare native test discovery and inspect changed methods/parameter rows. Retire old positive acceptance and per-filename deletion-routing obligations; map retained current command, containment, unknown input, record and release safety to concrete remaining assertions. Record removals, replacements and fixture disposition by coherent family, not a permanent per-method ledger. Keep old-looking literals when they independently exercise a current record/parser contract. Audit actual imports, catalog IDs, generated resources and copied-repository callers; no removed test may survive only as an undiscoverable link.

### TG-GUIDANCE. Supported authoring and preserved source authority

Inspect the exact canonical model-authoring method and its clean generated/installed consumer: an explicit project layout can select its declared target, the portable default uses a same-name directory, and a generic flat target cannot claim supported validation or automatic relocation. Preserve source interpretation and original customer bytes and review identities. Automated packaging/resource integrity checks establish actual inclusion; independent review assesses method meaning, since phrase matching cannot prove agent behavior. No published repository-specific retirement registry is introduced.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1 and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered change and its composed failure/consumer boundaries.
- Evidence: exact final subjects, independent reviewer basis, judgment and reporter-owned concern dispositions.
- Successor: distinct final Verify; corrections return to their owner for reassessment.

## Change-level verification

### TG-FINAL-1. Current branch through selector, executor and records

- Covers: all M1 requirements and canonical selection → trusted command → model/package boundary → actual result, including current record snapshot.
- Demonstrate: real local changes and the exact baseline-to-head PR range route without historical exceptions; a representative current model change executes successfully through the trusted CI command boundary, while a mixed unsupported input cannot produce a subset pass; current required missing detail remains unsuccessful. A prior-layout range is intentionally unsupported rather than silently repaired.
- Evidence expectations: actual selected local CI and exact committed PR-range CI after implementation, current source/package integrity and registered review/evidence validation. Record command exits, meaningful row counts and limitations. Reuse unchanged focused evidence only with an explicit current basis; required committed snapshot runs freshly.
- Non-applicability: no external deployment, publication, new concurrency mechanism or retry/state format, so those unchanged owner contracts require no new exhaustive scenario matrix.

## Validation plan

```bash
python tests/engineering/validation/test-boundary-first-validation.py
python tests/engineering/validation/test-select-validation.py
python scripts/validate-boundary-first.py --check
python scripts/validate-skills.py
bash scripts/ci.sh --mode local
bash scripts/ci.sh --mode pr --base ddb7eb9e0d4669d360483eac080f8f05fedd5641 --head HEAD
```

Use narrow method filters before full affected suites. The local selected run supplies remaining required executor, package, skill and current-record checks; do not repeat unchanged full suites merely for another gate. Exact committed PR-range CI is required before a PR-readiness claim. New authoritative proposal/plan/record files must be added to Git for tracking preflight; staging is preparation for the authorized scoped commit, not stash restoration or approval. Record actual results in evidence, not this plan. A source mutation after a pass requires affected fresh proof and reassessment.

## Risks and recovery

A retired path may share a broad current owner such as schemas or package sources; remove special historical treatment without imposing a blacklist on legitimate current namespaces. Current record-format rejection/exclusion, live release evidence, current publication authorization and CLI factual architecture/ADR discovery are unaffected. Unknown protection is investigated before removal. Preserve original history and the saved stash through the complete change.

## Dependencies

Use existing tools and fixtures. No new runtime dependency or worktree is required. Keep one actor writing records at a time. Commit the reviewed engineering result before final exact-head validation; recording-only closeout changes do not retarget engineering approvals.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-17 | Deliver the narrowed support boundary as one M1 with separate final review and Verify. | Canonical routing, model rejection and guidance form one small coupled pipeline. | Removing normalization before canonical routing or retaining a later historical-family cleanup would leave an incomplete contract. |
| 2026-09-17 | Keep merged test-design scope and preserve the saved stash. | User explicitly selected compatibility-only completion; saved records largely describe merged/superseded work. | Wholesale stash restoration and broader catalogs would overwrite reviewed outcomes or expand scope. |

## Readiness

- See the owning change record for current workflow state.
