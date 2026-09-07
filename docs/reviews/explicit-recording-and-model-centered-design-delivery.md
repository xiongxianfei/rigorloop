# Explicit Recording and Model-Centered Design — Advisory Delivery Review

## Recording basis

The user requested a delivery plan followed by independent Delivery Review. This record reviews the portable plan against the two user-authorized model Design drafts and their independent advisory rereview. It is not a registered lifecycle review or an implementation authorization. The descriptive IDs below do not invent registered artifact identities. The reviewer `review_compact_fix` authored neither the plan nor the model documents and did not change them during review.

## Result

- Skill: delivery-review
- Review status: changes-requested
- Package members: `plan` → [Delivery plan](../plans/2026-09-05-explicit-recording-and-model-centered-design.md).
- Upstream review ID: None; [the advisory Design rereview](explicit-recording-and-model-centered-design.md) supplies the reviewed draft basis, not a formal Design Review ID.
- Review ID and round: No formal identity assigned; independent advisory first pass.
- Traceability result: All 21 model requirements have architectural-boundary, milestone and proof-group allocation. One required closeout review is absent from the explicit sequence.
- Material findings: DELIVERY-001.
- Correction targets: `plan`, plan authoring.
- Recording status: recorded.
- Settlement status: not-applicable.
- Open blockers: Allocate final holistic Code Review before Verify. Separately, formal implementation authority remains unresolved as the plan already states.
- Immediate next stage: Isolated stop; plan-owner correction and independent rereview if authorized.
- Claim limitations: No registration, formal Delivery approval, implementation permission, lifecycle progression, code correctness, Verify result or release readiness.

## Finding DELIVERY-001

- Finding ID: DELIVERY-001
- Severity: major
- Location: Delivery plan M4 Review handoff and M5 Dependencies, contrasted with Non-goals and the Workflow model's retained final-Code-Review boundary.
- Evidence: The plan explicitly excludes removing final Code Review. However, M4 hands its adoption-and-compatibility slice review directly to Verify; M5 requires only M1–M4 independent reviews, finding resolution and triggered CI maintenance. Neither allocates the required final holistic Code Review of the complete change. Current code-review guidance explicitly distinguishes milestone review from final holistic review. TG-FINAL-01/02 are integrated proof groups, not an independent Code Review judgment.
- Required outcome: Explicitly include final holistic Code Review of the complete implementation and cross-milestone interactions before Verify, with current reviewed subjects, unresolved-finding handling and rereview after corrections. Preserve the distinction between the M4 slice review and final complete-change review. This need not introduce another implementation milestone.
- Safe resolution path: The plan author updates closeout sequencing, dependencies and evidence expectations consistently, retaining the separately stated formal-authority prerequisite. Independently rereview the revised plan before reliance. Removing the gate would instead require a separately authorized direction change, which this plan expressly excludes.
- needs-decision rationale: None for preserving the existing gate; correction is within plan ownership.
- Finding scope: artifact-local.
- Affected artifact IDs: `plan` (descriptive portable-plan identity).
- Owning stages: plan.

## Sequence and verification assessment

M1 isolates representation and historical-contract compatibility before a writer exists. M2 deliberately implements reading, validation, writing and recovery together while ordinary adoption remains disabled. M3 integrates actor responsibility, canonical skills and model-document guidance. M4 brings those boundaries together before enabling explicit new-contract creation. Those intermediate states are appropriately constrained. The final handoff needs the correction above; milestone completion and green integration checks must not substitute for the retained independent whole-change judgment.

The requirement table maps WF-SR-01–10 and CLI-SR-01–11 to named boundaries, M1–M4 and TG-01–07/TG-FINAL-01–02. The proof groups cover closed vocabularies and unknown-value regressions, explicit supplied semantics, inspection content and missing records, rejection versus observations, declared-basis conflicts, lost-response retry, competing writers, interrupted save/recovery, third-state external edits, historical non-mutation and new-change-only adoption. Public CLI subprocess checks are required in addition to helper tests. These allocations are meaningful and do not defer every failure path to Verify.

Semantic responsibility and actual reviewer independence are assigned to a scoped independent walkthrough as well as structural fixtures. The plan explicitly rejects role-string fixtures as proof of independence, and binds walkthrough currency to the changed guidance and executable subjects. The two change-level groups cover the agent/storage interaction and generated-adapter compatibility. No OS selection, platform matrix or OS feasibility task is required; observable save/conflict/recovery proof remains in scope.

The plan retains one Design file per model and treats boundary-format mapping as a constrained allocation/recognition task. It explicitly routes a discovered new normative outcome back to Design before dependent implementation. The previously disclosed mapping and adoption obligations remain visible; this review does not silently approve new behavior through a validator change.

## Authority and evidence limits

No owning change root or formal Design Review ID exists for this portable package. The parent reports current context returns RL_CONTEXT_CHANGE_NOT_FOUND. The plan correctly withholds M1 implementation until the governing authority is established. That administrative limitation is distinct from DELIVERY-001 and cannot be repaired by assigning a fictional review identity here.

The reviewer read the complete primary plan, the current complete model drafts in the preceding independent Design rereview, the preserved advisory Design record, the Delivery Review skill and required method/recording resources. This package does not claim to consume an adopted boundary-first-v1 proof map, so no retired test-spec artifact or proof-map substitute was required. Current code-review guidance was inspected specifically to resolve the closeout sequence.

Commands inspected rather than executed as implementation proof: `npm --prefix packages/rigorloop test` resolves to the existing `node --test` script; the named adapter, CI and boundary command options exist. Review used `cat` for the plan/resources/package metadata and `rg` for closeout obligations and command options. `git diff --check -- docs/reviews/explicit-recording-and-model-centered-design-delivery.md` checks the review record's whitespace only. No future tests, adoption, generation, full CI or final verification were run or claimed.

The first-pass finding is recorded before any review-driven correction. No plan, model document, implementation or lifecycle state was changed by this review.

## Independent correction rereview

The first-pass result and finding above remain preserved. The user subsequently authorized plan refinement and independent rereview. The same independent reviewer reread the complete corrected plan and this record without editing the plan or its Design basis.

### Result

- Skill: delivery-review
- Review status: approved within the isolated advisory delivery-review scope.
- Package members: `plan` → [Delivery plan](../plans/2026-09-05-explicit-recording-and-model-centered-design.md).
- Upstream review ID: None; the linked advisory Design rereview remains the draft basis.
- Review ID and round: No formal identity assigned; independent correction rereview.
- Traceability result: All 21 model requirements retain milestone and proof allocation; complete-change review now has an explicit place before Verify.
- Material findings: None open; DELIVERY-001 resolved.
- Correction targets: None for this review.
- Recording status: recorded.
- Settlement status: not-applicable.
- Open blockers: No substantive delivery finding remains in this advisory scope. Formal implementation authority is still an explicit prerequisite outside this portable plan.
- Immediate next stage: Isolated stop; no automatic implementation handoff.
- Claim limitations: Advisory adequacy only, not formal package approval, registration, implementation permission, adoption, code correctness or final verification.

### DELIVERY-001 disposition

Disposition: accepted and resolved through plan refinement and independent rereview.

M4 now distinguishes its adoption-slice review from a subsequent independent final whole-change Code Review covering M1–M4, cross-milestone interactions and the current Design/Delivery basis. Its handoff requires finding resolution and affected rereview; integrated tests cannot substitute for the judgment. M5 requires the clean current final review before Verify, explicitly refreshes it when correction or CI changes its basis, and includes reviewed subjects and disposition/rereview evidence in its closeout evidence. Verify retry retains those dependencies. This satisfies the original finding without adding an implementation milestone or changing the approved user scope.

The complete-plan rereview found no further material sequencing or proof-allocation issue. Representation, full storage safety, actor/guidance integration and coherent adoption remain separated into reviewable slices. Public-path negative proof, historical non-mutation, explicit actor decisions, independent walkthroughs and recovery coverage remain allocated. No OS investigation, separate model Design sidecar or historical migration was added. Future behavioral gaps remain routed to their Design owner instead of silently becoming test-defined behavior.

Commands actually run for this rereview: `cat docs/plans/2026-09-05-explicit-recording-and-model-centered-design.md`, `cat docs/reviews/explicit-recording-and-model-centered-design-delivery.md`, and `git diff --check -- docs/reviews/explicit-recording-and-model-centered-design-delivery.md`. The last command is a whitespace check only; no implementation tests, generation, CI or lifecycle commands were run.
