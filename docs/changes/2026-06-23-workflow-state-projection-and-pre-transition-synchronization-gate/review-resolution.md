# Workflow-State Projection and Pre-Transition Synchronization Gate Review Resolution

## Scope

This record tracks formal lifecycle review findings for the workflow-state
projection and pre-transition synchronization gate change.

Closeout status: open

Review closeout: code-review-m1-r2
Review closeout: code-review-m3-r3

## Resolution Entries

### spec-review-r1

#### WSS-SR1

Finding ID: WSS-SR1
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec revision
Decision owner: spec author
Decision needed: Choose the exact allowed `Review status` syntax and final-closeout reason-code vocabulary.
Chosen action: Define exact structured `Review status` syntax plus closed review status, review-stage, round-token, and final-closeout reason-code vocabularies.
Rationale: Deterministic validation requires owner fields with one parseable grammar and closed accepted values.
Required outcome: Define exact allowed values and parseable syntax for `Review status` and final-closeout reason codes, including how review stage and round are represented when present.
Validation target: Revised spec includes closed value tables or equivalent normative requirements and acceptance criteria for valid and invalid bounded owner-field fixtures.
Resolution: Defined exact parseable syntax for the `Current Handoff Summary` `Review status` field: `<status>; stage=<review-stage>; round=<round-token>`. The spec now defines closed status and review-stage vocabularies and an `r<n>` or `none` round token. It also defines closed final-closeout reason-code syntax: `<reason-code-list> — <bounded detail>`, including readiness cross-field consistency rules.
Validation evidence: Spec revision validation passed with diff cleanliness, change metadata validation, review artifact validation, and explicit-path lifecycle validation. Spec-review-r2 approved the revised contract with no material findings.

#### WSS-SR2

Finding ID: WSS-SR2
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec revision
Decision owner: spec author
Decision needed: Choose the authoritative source for each `docs/plan.md` projection cell.
Chosen action: Define an authoritative source for every `docs/plan.md` projection cell and add exact plan-body owner fields.
Rationale: Deterministic projection validation requires each table cell to name exactly one owner or parse source.
Required outcome: Define the authoritative source for each `docs/plan.md` projection cell, especially `State` and `Change ID`.
Validation target: Revised spec maps `Plan`, `State`, `Next stage`, and `Change ID` to exact owner fields or artifact sources and adds acceptance criteria for projection-source validation.
Resolution: Defined `Plan` as the actual plan-file link target, `State` as the plan-body `Plan lifecycle state`, `Next stage` as `Current Handoff Summary` `Next stage`, and `Change ID` as the plan-body `Change ID`. The spec clarifies that plan lifecycle state is distinct from current milestone state and that `change.yaml.change_id` is a consistency check rather than the owner.
Validation evidence: Spec revision validation passed with diff cleanliness, change metadata validation, review artifact validation, and explicit-path lifecycle validation. Spec-review-r2 approved the revised contract with no material findings.

### spec-review-r2

No material findings. Spec-review-r2 confirmed WSS-SR1 and WSS-SR2 are resolved and closed this review-resolution record.

### architecture-review-r1

No material findings. Architecture-review-r1 approved the canonical architecture update and introduced no additional resolution obligations.

### plan-review-r1

#### WSS-PLAN1

Finding ID: WSS-PLAN1
Disposition: accepted
Status: resolved and confirmed by plan-review-r2
Owner: plan author
Owning stage: plan revision
Decision owner: plan author
Decision needed: none
Chosen action: Revise the plan to separate the mandatory `test-spec` lifecycle stage from implementation milestones.
Rationale: The governing workflow chain routes clean plan-review to `test-spec`, then implementation. Treating test-spec authoring as an implementation milestone creates a stage-order contradiction before implementation begins.
Required outcome: The plan routes clean plan-review to `test-spec`, and its first implementation milestone consumes the completed matching test spec instead of authoring it as code-reviewed implementation work.
Validation target: Revised plan no longer lists `specs/single-source-of-workflow-state.test.md` authoring or `TWSS-*` requirement mapping as an implementation milestone deliverable; plan-review rerun approves the corrected sequencing.
Resolution: Revised the plan so M1 no longer authors the matching test spec. The revised M1 consumes the completed test spec and starts implementation with fixture-backed validator tests and parser scaffolding. M2 now depends on the completed test spec and M1 parser fixture harness.
Validation evidence: Plan revision validation passed with diff cleanliness, change metadata validation, and explicit-path artifact lifecycle validation. Plan-review-r2 approved the revised plan with no material findings.

### plan-review-r2

No material findings. Plan-review-r2 confirmed WSS-PLAN1 is resolved and closed this review-resolution record.

### code-review-m1-r1

#### WSS-CR1

Finding ID: WSS-CR1
Disposition: accepted
Status: resolved and confirmed by code-review-m1-r2
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: none
Chosen action: Resolve plan-index owners from `docs/plan.md` through the shared workflow-state parser and union those owner paths into artifact-lifecycle state-sync validation.
Rationale: `docs/plan.md` is the live projection surface and must fail when its projected values drift from the active plan owner, even when the index is the only explicit validation input.
Required outcome: `docs/plan.md` projection validation runs when the plan index is in scope and compares linked structured active/blocked plan bodies against their table rows.
Validation target: Add a regression test where `validate_repository(..., paths=["docs/plan.md"])` fails on a stale `Next stage` projection, then update the artifact-lifecycle hook so the test passes.
Resolution: Added `resolve_owners_from_index()` to `scripts/lifecycle_state_sync.py` so the shared parser resolves active and blocked `docs/plan.md` rows to structured owner plan bodies, reports missing linked plans as projection errors, skips legacy plans without the structured handoff marker, and deduplicates explicit owner paths. Updated `scripts/artifact_lifecycle_validation.py` to call that resolver whenever the plan index is in scope before running `validate_workflow_state_sync()`.
Validation evidence: `python scripts/test-artifact-lifecycle-validator.py -k workflow_state` passed with the WSS-CR1 regression cases. `python scripts/test-artifact-lifecycle-validator.py` passed. Direct drift-fixture validation with `paths=["docs/plan.md"]` produced one blocker on `docs/plan.md Next stage`. `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md` passed against the actual repository state. Code-review-m1-r2 confirmed the resolution with no material findings.

### code-review-m1-r2

No material findings. Code-review-m1-r2 confirmed WSS-CR1 is resolved and closed this review-resolution record.

### code-review-m2-r1

No material findings. Code-review-m2-r1 approved the M2 parser and lifecycle state-sync validator slice and introduced no additional resolution obligations.

### code-review-m3-r1

#### WSS-CR2

Finding ID: WSS-CR2
Disposition: accepted
Status: resolved and confirmed by code-review-m3-r2
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: none
Chosen action: Revise review evidence summary derivation so closed/open finding counts require review-artifact closeout semantics, not only `Closeout status: closed`.
Rationale: R65 requires material findings to stay open until final disposition, required action or accepted exception, validation evidence, and no later reopening are all satisfied.
Required outcome: Derived `change.yaml` review counts and workflow owner-state blocking must still treat a finding as open when `review-resolution.md` lacks required closeout evidence, even if the file says `Closeout status: closed`.
Validation target: Add failing fixtures where a closed-status resolution entry without required validation evidence is still counted open for change metadata and lifecycle owner-state checks, plus a positive fixture only after closeout validation succeeds.
Resolution: Added `finding_closure_state()` in `scripts/review_artifact_validation.py` and routed `summarize_review_evidence()` plus closeout-mode review-artifact validation through the shared predicate. The predicate fails closed for unresolved review-log open findings, missing or duplicate resolution entries, missing accepted-action evidence, missing validation evidence, and later reopen records.
Validation evidence: `python scripts/test-review-artifact-validator.py` passed with predicate parity and missing-validation fixtures. `python scripts/test-change-metadata-validator.py` passed with closed-status missing-validation count checks. `python scripts/test-artifact-lifecycle-validator.py` passed with owner-state blocking for the same summary-open case.

### code-review-m3-r2

#### WSS-CR3

Finding ID: WSS-CR3
Disposition: accepted
Status: resolved and confirmed by code-review-m3-r3
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: none
Chosen action: Make the shared finding closure predicate fail closed when a review-resolution entry has a missing, unsupported, or otherwise unparseable disposition.
Rationale: R65 requires final disposition before a material finding can close, and R65a requires every shared derived open/closed predicate consumer to observe that same failure state.
Required outcome: `finding_closure_state()` reports `open` for missing or unsupported disposition values, and the summary, change metadata, lifecycle, and closeout-mode paths all agree on that open verdict.
Validation target: Add regression coverage where `summarize_review_evidence()` reports one open finding for a missing or unsupported disposition and where change metadata and lifecycle validation reject downstream-ready state for the same fixture.
Resolution: Reworked the closure predicate to require positive evidence for parseable disposition state, exactly one disposition field, valid closeout status, and validation evidence. Added regression coverage for missing, unsupported, and duplicate dispositions; missing closeout status; all-blockers reporting; parity with closeout-mode review validation; change metadata count blocking; and lifecycle owner-state blocking.
Validation evidence: `python scripts/test-review-artifact-validator.py`, `python scripts/test-change-metadata-validator.py`, and `python scripts/test-artifact-lifecycle-validator.py` passed after the WSS-CR3 resolution.

### code-review-m3-r3

No material findings. Code-review-m3-r3 confirmed WSS-CR3 is resolved and closed the M3 review-resolution loop.

### code-review-m4-r1

#### WSS-CR4

Finding ID: WSS-CR4
Disposition: accepted
Status: resolved pending code-review-m4-r2
Owner: implementation author
Owning stage: review-resolution
Decision owner: implementation author
Decision needed: none
Chosen action: Replace cross-product change metadata association with keyed pairing by `change_id` and explicit `artifacts.plan`, add multi-active-plan regression coverage, and remove the plan-level deferral by rerunning the all-active audit cleanly.
Rationale: M4 must either make active/blocked enforcement pass for the active index scope or record a valid blocker before handoff; the current implementation records the failing all-active audit as outside the slice.
Required outcome: Active and blocked enforcement scope must satisfy R81/T19, including multi-active-plan validation, or the governing spec/plan must be revised before bypassing that scope.
Validation target: Add or update regression coverage for the multi-active-plan active/blocked audit path, rerun the all-active audit command, and rerun M4 state-sync validation after owner/projection surfaces are updated.
Resolution: The root cause was code, not plan data. The Evidence-Bound Project Map plan body and its `change.yaml` already used the same `Change ID`; `validate_workflow_state_sync()` incorrectly compared each in-scope `change.yaml` against every structured plan body. The validator now keys plan/change associations by `change_id`, uses `artifacts.plan` to report explicit plan-linked mismatches, applies review-summary owner-state blocking only to the associated plan, and keeps linked legacy plans under the existing structured-marker grandfather rule. Added multi-active-plan fixtures for correct pairings, misassigned plan IDs, missing plan IDs, unmatched metadata, and order-independent keyed pairing.
Validation evidence: `python scripts/test-artifact-lifecycle-validator.py -k multi_active`, `python scripts/test-artifact-lifecycle-validator.py -k audit_pairs`, and `python scripts/test-artifact-lifecycle-validator.py -k workflow_state` passed. The all-active audit command from code-review M4 R1 passed after the fix: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md`.

## Validation Evidence

Spec revision completed for WSS-SR1 and WSS-SR2. Spec-review-r2 approved the revised contract with no material findings. Architecture-review-r1 approved the canonical architecture update with no material findings. Plan-review-r2 approved the revised plan and confirmed WSS-PLAN1 is resolved. Code-review-m1-r2 confirmed WSS-CR1 is resolved and closed. Code-review-m2-r1 approved M2 with no material findings. Code-review-m3-r1 requested changes for WSS-CR2; code-review-m3-r2 confirmed WSS-CR2 is resolved and requested changes for WSS-CR3. Code-review-m3-r3 confirmed WSS-CR3 is resolved and closed M3.
