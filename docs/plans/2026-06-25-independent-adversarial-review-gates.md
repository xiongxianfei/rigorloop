# Independent Adversarial Review Gates Execution Plan

## Status

Plan lifecycle state: active
Terminal disposition: none

- Change ID: 2026-06-25-independent-adversarial-review-gates-for-automated-workflows
- Owner: maintainer
- Start date: 2026-06-25
- Last updated: 2026-06-25
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the first slice of independent adversarial review gates for workflow-managed automated reviews. The work should make automated review handoff depend on verifiable fresh context, neutral initial packets, blind-first phase receipts, risk-tier gates, clean-review sufficiency receipts, second-review disagreement handling, final holistic code review evidence, and calibration signals.

The first implementation slice pilots the full contract in automated `code-review`, records manifest-only evidence for earlier review stages during rollout, preserves manual and profile-off behavior, and keeps clean reviews valid when the independent evidence supports them.

## Source artifacts

- Proposal: [Independent Adversarial Review Gates for Automated Workflows](../proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md)
- Proposal-review: [proposal-review-r2](../changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/proposal-review-r2.md)
- Spec: [Review Independence and Criticality](../../specs/review-independence-and-criticality.md)
- Spec-review: [spec-review-r2](../changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/spec-review-r2.md)
- Architecture: [canonical system architecture](../architecture/system/architecture.md)
- ADR: [ADR-20260625-independent-adversarial-review-gates](../adr/ADR-20260625-independent-adversarial-review-gates.md)
- Architecture-review: [architecture-review-r1](../changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/architecture-review-r1.md)
- Test spec: [Review Independence and Criticality Test Spec](../../specs/review-independence-and-criticality.test.md)
- Change metadata: [change.yaml](../changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml)

## Context and orientation

This change is workflow-governance and validation work inside the repository-local RigorLoop system. There is no hosted service, persistent database, or deployment target to add.

Important implementation surfaces:

- `scripts/review_artifact_validation.py` and `scripts/test-review-artifact-validator.py` own review-record and closeout shape checks.
- `scripts/change_metadata_semantics.py`, `scripts/validate-change-metadata.py`, `schemas/change.schema.json`, and `scripts/test-change-metadata-validator.py` own change metadata shape and semantic checks.
- `scripts/lifecycle_state_sync.py`, `scripts/artifact_lifecycle_validation.py`, `scripts/validate-artifact-lifecycle.py`, and `scripts/test-artifact-lifecycle-validator.py` own workflow-state and profile-routing assertions.
- `scripts/validation_selection.py`, `scripts/select-validation.py`, `scripts/ci.sh`, and `scripts/test-select-validation.py` own changed-path routing and selected validation.
- Canonical stage guidance lives under `skills/`; generated adapter output must be refreshed from canonical sources when skill text changes.
- Existing formal review recording and implementation autoprogression behavior must remain compatible, especially `changes-requested -> review-resolution` routing when an active profile authorizes it.

## Non-goals

- Do not require every review to produce a finding.
- Do not implement a hosted review service, database, external control plane, or network dependency.
- Do not make heterogeneous models mandatory for standard-risk automated review.
- Do not expose private chain-of-thought or hidden model reasoning in records.
- Do not make this first slice a full review-family migration; `code-review` is the full pilot, while `spec-review` and `plan-review` collect manifest evidence first.
- Do not change PR opening, publishing, deployment, or external-boundary authority.
- Do not proceed to implementation until `plan-review` and the matching test spec are complete.

## Requirements covered

- `R1`-`R2`: M1, M2, M3
- `R3`-`R7`: M1
- `R8`-`R9`: M3
- `R10`: M2
- `R11`: M2, M3
- `R12`: M2
- `R13`: M1, M3
- `R14`-`R16`: M4
- `R17`: M1, M4
- `R18`: M2, M3, M5
- `R19`: M3, M5
- `R20`: M2, M3, M5
- `AC1`-`AC5`: M1
- `AC6`-`AC9`, `AC-RAI-018`, `RAI-021`-`RAI-023`: M2
- `AC10`-`AC14`: M4
- `AC15`: M5

## Current Handoff Summary

- Current milestone: M3. Code-review pilot and review-family guidance
- Current milestone state: review-requested
- Latest review evidence: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m3-r1.md
- Last reviewed milestone: M3. Code-review pilot and review-family guidance
- Review status: review-requested; stage=code-review; round=r2
- Remaining in-scope implementation milestones: M4, M5
- Next stage: code-review M3
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation-milestones-open, milestone-review-pending, explain-change-pending, verify-pending, pr-handoff-pending — M3 review-resolution is complete and awaiting code-review-m3-r2; M4-M5 remain incomplete.

## Milestones

### M1. Review gate evidence model and validators

- Milestone state: closed
- Goal: Add structured review-gate evidence records for manifests, initial packets, phase receipts, clean-review sufficiency receipts, and private-reasoning-safe record fields.
- Requirements: `R1`-`R7`, `R13`, `R17`, `AC1`-`AC5`, `AC12`
- Files/components likely touched:
  - `schemas/change.schema.json`
  - `scripts/review_artifact_validation.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/review-artifacts/`
  - `tests/fixtures/change-metadata/`
- Dependencies:
  - Approved matching test spec must define concrete fixture expectations before implementation.
- Tests to add/update:
  - Valid manifest with L1/L2/L3, packet inventory, packet hash, reviewer context identity, phase receipts, and native verdict.
  - Invalid L0 handoff, missing packet inventory, missing packet hash, mutable manifest after later evidence release, early evidence release, unbounded free-form manifest field, and private-reasoning field rejection.
  - Clean-review sufficiency receipt valid and invalid fixtures.
- Implementation steps:
  - Define the smallest structured record shape that satisfies the spec without turning clean receipts into broad prose.
  - Add parser and semantic checks for manifest, initial packet, phase receipts, and clean-review receipt.
  - Add fixtures covering valid and fail-closed outcomes.
  - Keep existing clean review receipt and material finding validation compatible for manual/profile-off reviews.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Expected observable result: Automated review gate evidence can be validated structurally, and incomplete or contaminated evidence fails closed without changing manual/profile-off review behavior.
- Commit message: `M1: add independent review gate evidence validation`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: yes
  - validation notes updated: yes
  - milestone committed: yes
- Risks:
  - Record formats could become too prose-heavy for validators to enforce.
- Rollback/recovery:
  - Revert the new evidence validation paths and fixtures while leaving existing review artifact validation untouched.

### M2. Orchestration semantics and workflow-state gates

- Milestone state: closed
- Goal: Enforce normalized `review_gate_outcome`, fail-closed risk-tier classification, `changes-requested` routing semantics, second-review disagreement stops, and final holistic code-review preconditions in workflow-state evaluation.
- Requirements: `R10`-`R12`, `R14`, `R18`, `R20`, `AC6`-`AC11`, `AC13`, `AC15`, `AC-RAI-018`, `RAI-021`-`RAI-023`
- Files/components likely touched:
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `tests/fixtures/artifact-lifecycle/`
  - `specs/workflow-stage-autoprogression.md` only if implementation exposes a true approved-spec gap
- Dependencies:
  - M1 evidence parsing should exist before routing gates rely on manifest and receipt state.
- Tests to add/update:
  - Native `approved` and `clean-with-notes` advance only with valid independence and evidence gates.
  - Native `changes-requested` routes to `review-resolution` only when an active profile authorizes it and policy gates allow another round.
  - Native `blocked` and `inconclusive` pause regardless of profile authorization.
  - Ambiguous risk tier escalates or becomes inconclusive.
  - Second-review disagreement blocks automatic continuation.
  - Missing final holistic code review blocks `explain-change` and `verify` under implementation autoprogression.
- Implementation steps:
  - Add derived gate-outcome evaluation helpers.
  - Connect manifest, phase receipt, risk tier, clean receipt, unresolved finding, and second-review state into workflow-state checks.
  - Preserve existing implementation-profile correction-loop behavior when `changes-requested` is routable.
  - Add fixture coverage for Examples E8-E10 and RAI-021 through RAI-023.
- Validation commands:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Expected observable result: Workflow-state validation distinguishes clean advance, routable `changes-requested`, blocked, and inconclusive states without string-only review status comparisons.
- Commit message: `M2: enforce automated review gate routing`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: yes
  - validation notes updated: yes
  - milestone committed: yes
- Risks:
  - Routing checks could accidentally pause existing authorized correction loops.
- Rollback/recovery:
  - Revert the new gate-outcome evaluator and fixtures while preserving prior implementation-profile guards.

### M3. Code-review pilot and review-family guidance

- Milestone state: review-requested
- Goal: Update canonical review and workflow skills so automated `code-review` uses the full blind-first independent gate, while automated `spec-review` and `plan-review` record minimal manifest evidence during the pilot.
- Requirements: `R6`, `R8`, `R9`, `R18`-`R20`, `AC12`, `AC13`, `AC15`
- Files/components likely touched:
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/review-resolution/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/architecture-review/SKILL.md` if final review-family wording needs manifest compatibility
  - `scripts/test-skill-validator.py`
  - `scripts/test-build-skills.py`
- Dependencies:
  - M1 and M2 should define the evidence and routing vocabulary before skill text relies on it.
- Tests to add/update:
  - Skill validation for required guidance, no generated-output source edits, no reviewer edit authority, no finding quota, and deferred prior-finding/evidence-menu language.
  - Generated local skill build checks after canonical skill updates.
- Implementation steps:
  - Add code-review pilot guidance for initial packet, risk map, evidence challenge, prior-finding reconciliation, clean sufficiency receipt, and final holistic review.
  - Add workflow/implement routing guidance so profile-managed automated reviews invoke the independent gate.
  - Add minimal manifest collection language for automated spec-review and plan-review during Phase 1.
  - Keep direct isolated review behavior unchanged.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
- Expected observable result: Canonical skill guidance matches the approved review-independence contract and remains valid for generated adapters.
- Commit message: `M3: pilot independent gates in review skills`
- Milestone closeout:
  - validation passed: yes
  - progress updated: yes
  - decision log updated if needed: yes
  - validation notes updated: yes
  - milestone committed: yes
- Risks:
  - Skill text could become too long or expose maintainer-only implementation details.
- Rollback/recovery:
  - Revert skill text changes for the affected skills and regenerate from the last valid canonical skill state.

### M4. Calibration fixtures and measurement evidence

- Milestone state: planned
- Goal: Add public defect-class fixtures, calibration record validation, sampling-floor evidence, downstream escape recording, and metric separation by review skill and risk tier.
- Requirements: `R14`-`R17`, `AC10`-`AC14`
- Files/components likely touched:
  - `tests/fixtures/review-artifacts/`
  - `tests/fixtures/artifact-lifecycle/`
  - `scripts/review_artifact_validation.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/behavior-preservation.md`
- Dependencies:
  - M1 and M2 must define the calibration record inputs that validators can inspect.
- Tests to add/update:
  - Standard-risk rollout sampling below 20% fails.
  - Standard-risk sample-rate reduction before 10 independently reviewed clean outcomes fails.
  - Elevated-risk clean review without second review fails.
  - Second-review material finding, blocked result, or inconclusive result blocks continuation.
  - Calibration records distinguish recurrence detection, novel-defect detection, disagreement, escapes, false positives, inconclusive rate, receipt quality, and review duration by skill and tier.
- Implementation steps:
  - Add representative public seeded-defect class fixtures without implying the whole calibration corpus is public.
  - Add validation for calibration record shape and sampling floors.
  - Add downstream escape record examples and validation.
  - Record behavior-preservation evidence for manual/profile-off review compatibility and no finding quota.
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows`
- Expected observable result: Calibration and second-review evidence can be tested without treating public fixtures as the only measured defect corpus.
- Commit message: `M4: add review gate calibration evidence`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Public fixtures could be mistaken for the complete private calibration corpus.
- Rollback/recovery:
  - Revert fixture and calibration validation changes while keeping the core gate fail-closed behavior.

### M5. Generated guidance, docs alignment, and final proof

- Milestone state: planned
- Goal: Align contributor-facing workflow guidance, generated skill/adapters checks, behavior-preservation evidence, and final validation selection for the first slice.
- Requirements: `R19`, `R20`, all acceptance criteria
- Files/components likely touched:
  - `docs/workflows.md`
  - `AGENTS.md` or `CONSTITUTION.md` only if implementation changes their summarized guidance
  - `skills/`
  - generated adapter validation surfaces
  - `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/behavior-preservation.md`
  - `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Dependencies:
  - M1-M4 must be complete.
  - Matching test spec must name final validation expectations before implementation begins.
- Tests to add/update:
  - Build and validation checks for canonical skill source and generated adapter output.
  - Changed-path selection confirms new deterministic evidence paths route to the intended checks or record explicit routing debt.
  - Behavior-preservation evidence covers manual/profile-off compatibility, no finding quota, and existing authorized `changes-requested -> review-resolution` routing.
- Implementation steps:
  - Update workflow docs or record them unaffected with rationale.
  - Refresh generated skill/adapters evidence using repository-owned scripts.
  - Add behavior-preservation matrix.
  - Run selected validation for all touched source, test, skill, schema, and evidence files.
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`
  - `python scripts/select-validation.py --mode explicit --path <changed-path>`
  - `bash scripts/ci.sh --mode explicit --path <changed-path>`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path specs/review-independence-and-criticality.md --path specs/review-independence-and-criticality.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260625-independent-adversarial-review-gates.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Expected observable result: All first-slice artifacts, guidance, fixtures, validators, and generated checks are coherent and ready for final explain-change and verify after implementation review closes.
- Commit message: `M5: align review gate guidance and proof`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Validation selection may expose unregistered deterministic evidence paths late in the slice.
- Rollback/recovery:
  - Resolve selector routing debt before verify, or remove unsupported deterministic evidence and record an explicit deferral if authorized.

## Validation plan

- `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md --path specs/review-independence-and-criticality.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260625-independent-adversarial-review-gates.md --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/architecture-review-r1.md`
- `git diff --check -- docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows`
- When any change touches files under `skills/`, the validation plan MUST include public adapter archive proof in addition to local skill validation: `python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir"` followed by `python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`. If `v0.1.5` is not the current adapter manifest version at implementation time, use the version from `dist/adapters/manifest.yaml` in both commands. Local-skill checks alone do not prove the public adapter archive boundary required by the architecture.
- Milestone-specific test commands listed under M1-M5 after the matching test spec is active.

## Generated skill and adapter proof boundary

`scripts/build-skills.py --check` proves local-skill output: canonical skill files are well formed and generated local skill output is current.

`scripts/build-adapters.py --output-dir <tmpdir>` followed by `scripts/validate-adapters.py --root <tmpdir>` proves public adapter archive output: the `v0.1.3` and later release-archive form built from current canonical skill content remains generable and valid.

Both proofs are required for canonical-skill changes. Neither proof subsumes the other.

## Risks and recovery

- Risk: The gate could become an attestation-only layer.
  - Recovery: Keep validator-owned closed fields and phase-order checks in M1/M2, then use second-review and calibration fixtures in M4 for evidence quality.
- Risk: Existing implementation-profile correction loops could regress.
  - Recovery: Preserve `changes-requested` routing only under active profile authority and include regression fixtures for `correction-finding-unclassified`.
- Risk: Skill guidance could leak repository-maintainer implementation detail into published skills.
  - Recovery: Keep maintainer detail in specs, validators, and docs; published skill text should describe user-facing review behavior and evidence requirements.
- Risk: Public seeded fixtures could be overfit.
  - Recovery: Keep public fixtures at the defect-class level and record that measured private rotating fixtures remain a separate calibration responsibility.
- Risk: Plan could imply implementation readiness before test-spec.
  - Recovery: Current Handoff Summary and Readiness keep next stage as `plan-review`; implementation milestones remain planned until plan-review and test-spec are complete.

## Dependencies

- Approved proposal, spec, architecture package, and ADR listed in Source artifacts.
- Approved architecture-review evidence with no material findings.
- Matching active test spec before implementation.
- Existing review artifact, change metadata, lifecycle, skill, build, and selector validation scripts.
- No new runtime dependency is planned.

## Progress

- 2026-06-25: Proposal accepted; spec approved after resolving `SR1-F1`; architecture package and ADR approved by architecture-review; execution plan created.
- 2026-06-25: Plan-review R1 requested `PR1-F1`; accepted and revised M3, M5, and the top-level validation plan to require adapter archive proof for canonical skill changes. This was discovered under isolated formal plan-review; manual review discipline continues for this change pending independence-gates landing.
- 2026-06-25: Plan-review R2 approved the revised plan; matching active test spec authored.
- 2026-06-25: M1 implemented structured automated review-gate evidence validation for review records and change metadata, including manifest fields, initial-packet inventory and hash checks, blind-first phase receipts, clean-review sufficiency receipt fields, forbidden context indicators, bounded prose fields, and durable valid/fail-closed fixtures.
- 2026-06-25: Code-review M1 R1 requested changes: `CR1-F1` requires native review result evidence in automated review gate manifests, and `CR1-F2` requires direct T1 proof for valid L3 and missing/unsupported context identity cases.
- 2026-06-25: M1 review-resolution addressed `CR1-F1` and `CR1-F2`; added native review status required-field and R12 mapping validation; added T1 L1/L2/L3 and invalid independence fixtures; returned M1 to `code-review-m1-r2`.
- 2026-06-25: Code-review M1 R2 requested changes: `CR2-F1` requires unsupported native review status values to fail closed instead of silently advancing with `review_gate_outcome: advance`.
- 2026-06-25: M1 review-resolution addressed `CR2-F1`; converted native review status validation to fail-closed closed-vocabulary gating, added unknown native status regression tests and fixture coverage, added closed-vocabulary guidance to `AGENTS.md`, and returned M1 to `code-review-m1-r3`.
- 2026-06-25: Code-review M1 R3 approved the M1 review-resolution with no material findings; M1 is closed and the next implementation milestone is M2.
- 2026-06-25: M2 implemented normalized automated review-gate routing in lifecycle state helpers, including clean advance gates, routable `changes-requested`, blocked/inconclusive pauses, second-review disagreement stops, and final holistic review preconditions before `explain-change`.
- 2026-06-25: Code-review M2 R1 requested changes: `CR3-F1` requires clean native statuses to derive `review_gate_outcome: inconclusive` when clean/evidence gates fail instead of treating that outcome as a native/derived mismatch.
- 2026-06-25: M2 review-resolution addressed `CR3-F1`; split determinate native outcome mapping from clean native gate-derived outcome logic, added `CLEAN_ADVANCE_GATES`, added conditional mismatch handling, and returned M2 to `code-review-m2-r2`.
- 2026-06-25: Code-review M2 R2 approved the CR3-F1 resolution with no material findings; M2 is closed and the next implementation milestone is M3.
- 2026-06-25: M3 implemented code-review pilot guidance for workflow-managed independent adversarial review, workflow and implement routing guidance, and Phase 1 manifest-only guidance for automated spec-review and plan-review while preserving direct isolated review behavior.
- 2026-06-25: Code-review M3 R1 requested changes: `CR4-F1` requires operational `failed-remediation` guidance and test coverage, and `CR4-F2` requires `auto-fix eligibility` to be excluded from implement handoff packets and tested.
- 2026-06-25: M3 review-resolution addressed `CR4-F1` and `CR4-F2`; added R8d/R5 phrase constants for skill guidance assertions, updated code-review and implement guidance, reran local skill and adapter archive proof, and returned M3 to `code-review-m3-r2`.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-25 | Split implementation into five milestones | Separates evidence schema, routing semantics, skill pilot guidance, calibration, and final generated/doc proof so each can receive focused test-spec coverage and code-review. | One broad implementation slice; review-family migration before the code-review pilot proves the contract. |
| 2026-06-25 | Require test-spec before implementation M1 | The spec has many normative gates and RAI checks; implementation without a traceable test spec would hide coverage gaps. | Start coding directly from the architecture and retroactively document tests. |
| 2026-06-25 | Require adapter archive proof in M3 and M5 when canonical skills change | M3 changes canonical stage-skill guidance and M5 performs final generated proof; public adapter archive validation must be proven at the milestone-local boundary and again at final closeout. | Defer all adapter proof to M5; treat local skill validation as sufficient for public adapter archives. |
| 2026-06-25 | Keep M1 review-gate evidence validation in semantic validators instead of changing `schemas/change.schema.json` | Existing schema structure already permits optional nested review metadata; semantic validators can enforce closed independence levels, phase order, hashes, and fail-closed review evidence without broad schema churn. | Add schema-only fields that would not enforce the M1 behavioral gates. |
| 2026-06-25 | Treat repository-wide required-field enumeration drift as a process follow-up before M2 | `CR1-F1` and `CR1-F2` repeat a cross-initiative pattern where hand-listed validator or fixture subsets drift from spec enumerations; resolving the M1 findings is necessary but not sufficient to prevent recurrence. | Hide the broader audit inside the M1 fix; defer it silently. |
| 2026-06-25 | Add closed-vocabulary validator discipline before M2 | `CR2-F1` confirmed that guard-style membership checks can silently pass unknown values in the same resolution path that fixed a required-field omission. | Rely on future code review to catch each instance manually. |
| 2026-06-25 | Implement M2 review-gate routing as a lifecycle-state helper | The current lifecycle validator already owns implementation-profile route projection, so adding a focused `evaluate_automated_review_gate_route` keeps orchestration semantics testable without adding schema churn. | Encode M2 routing only in prose or in review artifact validation. |
| 2026-06-25 | Split determinate and conditional review status constants | `CR3-F1` showed that clean native statuses derive outcomes from gate state, while `changes-requested`, `blocked`, and `inconclusive` have determinate mappings. | Reuse one native-status mapping constant for both unconditional consistency checks and conditional derivation. |
| 2026-06-25 | Keep M3 scoped to existing canonical skills | The plan listed `skills/review-resolution/SKILL.md`, but no such canonical skill exists in this repository; creating a new skill would exceed the approved M3 scope and conflict with the repository rule against one-off skills. | Create a new review-resolution skill during M3. |
| 2026-06-25 | Drive M3 review-independence skill assertions from R-cited phrase constants | `CR4-F1` and `CR4-F2` showed that hand-listed skill assertions can mirror missing spec-required guidance. | Keep the M3 assertions as independent hand-written phrase subsets. |

## Surprises and discoveries

- Existing review-artifact validation expects review-log entries to use `review-resolution.md#<Review ID>` in this change root, so the architecture-review clean receipt is indexed through the existing resolution ledger.
- Plan-review R1 showed that local skill validation can be mentally substituted for adapter validation unless the plan names both boundaries explicitly.
- M1 fixture-backed review-log entries needed the existing block-style `Resolution` field even for no-material automated review examples; this preserves compatibility with the current review-log parser.
- Code-review M1 R1 found the same structural required-field drift pattern seen in the implementation-autoprogression initiative. Before M2 starts, perform a focused audit of review artifact, change metadata, and lifecycle/state validators for spec-required field lists, T-ID coverage enumerations, and fail-open unknown-value handling.
- Code-review M1 R2 confirmed the fail-open unknown-value variant exists for native review status; include unknown-value handling in the pre-M2 validator audit, not only required-field coverage.
- The M1 guard-style audit found `scripts/review_artifact_validation.py:824` as the native-status fail-open defect. Other inspected uppercase-vocabulary occurrences in `scripts/review_artifact_validation.py`, `scripts/change_metadata_semantics.py`, `scripts/validate-change-metadata.py`, and `scripts/lifecycle_state_sync.py` were already fail-closed gates or routing/forbidden-key membership checks; no additional M1-surface findings were opened.
- M2 reuses `ImplementationAutoprogressionRoute` for normalized review-gate routing results so lifecycle tests can assert the same `profile_state`, `next_stage`, and `stop_reason` shape already used by implementation autoprogression.
- CR3-F1 is an evaluation-order defect rather than the earlier unknown-value fall-through family. Future validator audits should also flag constants that mix unconditional mapping and conditional gate-derived outcome roles.
- The plan listed `skills/review-resolution/SKILL.md`, but the repository has no canonical review-resolution skill. M3 therefore updated the existing canonical skills that own automated review invocation, review execution, and authoring review guidance without creating a new skill.
- Code-review M3 R1 showed the same hand-listed-subset drift pattern in skill guidance assertions. M3 now uses `scripts/review_independence_skill_phrases.py` for R5 and R8d phrase checks so future spec additions have one test-side update point.

## Validation notes

- 2026-06-25: `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed.
- 2026-06-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md --path specs/review-independence-and-criticality.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260625-independent-adversarial-review-gates.md --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/architecture-review-r1.md` passed.
- 2026-06-25: `git diff --check -- docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed.
- 2026-06-25: Plan revised for `PR1-F1`; rerun target is `plan-review-r2`.
- 2026-06-25: Test spec authored at `specs/review-independence-and-criticality.test.md`; implementation can begin with M1 after validation passes.
- 2026-06-25: `python scripts/test-review-artifact-validator.py` passed after M1.
- 2026-06-25: `python scripts/test-change-metadata-validator.py` passed after M1.
- 2026-06-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed after M1.
- 2026-06-25: `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after M1.
- 2026-06-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md --path specs/review-independence-and-criticality.md --path specs/review-independence-and-criticality.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260625-independent-adversarial-review-gates.md --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/plan-review-r2.md` passed after M1 handoff sync.
- 2026-06-25: `git diff --check -- scripts/review_artifact_validation.py scripts/change_metadata_semantics.py scripts/validate-change-metadata.py scripts/test-review-artifact-validator.py scripts/test-change-metadata-validator.py tests/fixtures/review-artifacts docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after M1.
- 2026-06-25: `rg -n '[[:blank:]]$|\t' scripts/review_artifact_validation.py scripts/change_metadata_semantics.py scripts/validate-change-metadata.py scripts/test-review-artifact-validator.py scripts/test-change-metadata-validator.py tests/fixtures/review-artifacts docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` returned no matches after M1.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k native_review_status` passed after `CR1-F1` with 2 tests.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k mismatched_native` passed after `CR1-F1` with 1 test.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k t1_` passed after `CR1-F2` with 2 parameterized tests covering 3 valid cases and 3 invalid cases.
- 2026-06-25: `python scripts/test-review-artifact-validator.py` passed after M1 review-resolution with 62 tests, up from 57 in the M1 handoff commit.
- 2026-06-25: `python scripts/test-change-metadata-validator.py` passed after M1 review-resolution with 41 tests.
- 2026-06-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed after M1 review-resolution.
- 2026-06-25: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed after M1 review-resolution.
- 2026-06-25: Direct T1 fixture validation passed for valid L1/L2/L3 fixtures and expected-failed for missing context separation, unsupported independence level, and missing reviewer context ID on an unverifiable platform.
- 2026-06-25: `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after M1 review-resolution.
- 2026-06-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md --path specs/review-independence-and-criticality.md --path specs/review-independence-and-criticality.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260625-independent-adversarial-review-gates.md --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m1-r1.md` passed after M1 review-resolution.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k native_review_status` passed during code-review M1 R2 with 2 tests.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k mismatched_native` passed during code-review M1 R2 with 1 test.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k t1_` passed during code-review M1 R2 with 2 parameterized tests covering 3 valid and 3 invalid cases.
- 2026-06-25: `python scripts/test-review-artifact-validator.py` passed during code-review M1 R2 with 62 tests.
- 2026-06-25: Temporary adversarial fixture changed `Native review status: clean-with-notes` to `Native review status: rubber-stamp` while keeping `Review gate outcome: advance`; `python scripts/validate-review-artifacts.py --mode structure <tmpdir>/fixture` passed with zero findings, producing `CR2-F1`.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k unknown_native` failed before the `CR2-F1` fix and passed afterward with 2 tests covering three unknown values plus allowed-value error text.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k t1_` failed before the `CR2-F1` fix on `unknown-native-review-status` and passed afterward with 2 parameterized tests covering 3 valid cases and 4 invalid cases.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k native_review_status` passed after `CR2-F1` with 3 tests.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k mismatched_native` passed after `CR2-F1` with 1 test.
- 2026-06-25: `python scripts/test-review-artifact-validator.py` passed after `CR2-F1` with 64 tests.
- 2026-06-25: Direct validation of `tests/fixtures/review-artifacts/invalid-unknown-native-review-status` failed with `unsupported native review status 'rubber-stamp'` and listed the allowed native statuses.
- 2026-06-25: `rg -n "if .* in [A-Z][A-Z0-9_]+| if .* not in [A-Z][A-Z0-9_]+|\\.value in [A-Z][A-Z0-9_]+" scripts/review_artifact_validation.py scripts/change_metadata_semantics.py scripts/validate-change-metadata.py scripts/lifecycle_state_sync.py` completed the M1 closed-vocabulary audit; no additional fail-open validator findings were opened.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k unknown_native` passed during code-review M1 R3 with 2 tests.
- 2026-06-25: `python scripts/test-review-artifact-validator.py -k t1_` passed during code-review M1 R3 with 2 parameterized tests covering 3 valid and 4 invalid cases.
- 2026-06-25: `python scripts/test-review-artifact-validator.py` passed during code-review M1 R3 with 64 tests.
- 2026-06-25: `python scripts/test-change-metadata-validator.py` passed during code-review M1 R3 with 41 tests.
- 2026-06-25: Temporary adversarial fixture changed `Native review status: clean-with-notes` to `Native review status: rubber-stamp` while keeping `Review gate outcome: advance`; `python scripts/validate-review-artifacts.py --mode structure <tmpdir>/fixture` failed with `unsupported native review status 'rubber-stamp'`.
- 2026-06-25: `python scripts/test-artifact-lifecycle-validator.py -k review_gate` passed after M2 with 4 tests.
- 2026-06-25: `python scripts/test-artifact-lifecycle-validator.py -k phase_boundaries` passed after M2 with 1 test covering the final holistic review precondition.
- 2026-06-25: `python scripts/test-artifact-lifecycle-validator.py` passed after M2 with 132 tests.
- 2026-06-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after M2 before handoff.
- 2026-06-25: `python scripts/test-artifact-lifecycle-validator.py -k review_gate` failed before the `CR3-F1` fix because `CLEAN_ADVANCE_GATES` was missing, then passed after the fix with 6 tests, including 11 routing subcases and every clean-advance gate covered.
- 2026-06-25: `python scripts/test-artifact-lifecycle-validator.py -k phase_boundaries` passed after `CR3-F1` with 1 test.
- 2026-06-25: `python scripts/test-artifact-lifecycle-validator.py` passed after `CR3-F1` with 134 tests.
- 2026-06-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m2-r1.md` passed after `CR3-F1`.
- 2026-06-25: `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after `CR3-F1`.
- 2026-06-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed after `CR3-F1`.
- 2026-06-25: `git diff --check -- scripts/lifecycle_state_sync.py scripts/test-artifact-lifecycle-validator.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m2-r1.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after `CR3-F1`.
- 2026-06-25: `rg -n '[[:blank:]]$|\t' scripts/lifecycle_state_sync.py scripts/test-artifact-lifecycle-validator.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m2-r1.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` returned no matches after `CR3-F1`.
- 2026-06-25: `python scripts/test-skill-validator.py -k review_independence_m3` failed before M3 skill guidance was added, then passed after implementation with 3 tests.
- 2026-06-25: `python scripts/test-skill-validator.py` passed after M3 with 237 tests.
- 2026-06-25: `python scripts/validate-skills.py` passed after M3, validating 23 skill files.
- 2026-06-25: `python scripts/test-build-skills.py` passed after M3 with 7 tests.
- 2026-06-25: `python scripts/build-skills.py --check` passed after M3.
- 2026-06-25: `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` passed after M3, building and validating Codex, Claude, and OpenCode adapter archives.
- 2026-06-25: `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after M3 handoff sync.
- 2026-06-25: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after M3 handoff sync.
- 2026-06-25: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed after M3 handoff sync.
- 2026-06-25: `git diff --check -- scripts/test-skill-validator.py skills/code-review/SKILL.md skills/workflow/SKILL.md skills/implement/SKILL.md skills/spec-review/SKILL.md skills/plan-review/SKILL.md docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed after M3.
- 2026-06-25: `rg -n '[[:blank:]]$|\t' scripts/test-skill-validator.py skills/code-review/SKILL.md skills/workflow/SKILL.md skills/implement/SKILL.md skills/spec-review/SKILL.md skills/plan-review/SKILL.md docs/plans/2026-06-25-independent-adversarial-review-gates.md docs/plan.md docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` returned no matches after M3.
- 2026-06-25: `python scripts/test-skill-validator.py -k review_independence_m3` passed after M3 review-resolution with 3 tests and enumeration-driven R5/R8d phrase checks.
- 2026-06-25: `python scripts/test-skill-validator.py` passed after M3 review-resolution with 237 tests.
- 2026-06-25: `python scripts/validate-skills.py` passed after M3 review-resolution, validating 23 skill files.
- 2026-06-25: `python scripts/test-build-skills.py` passed after M3 review-resolution with 7 tests.
- 2026-06-25: `python scripts/build-skills.py --check` passed after M3 review-resolution.
- 2026-06-25: `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` passed after M3 review-resolution, building and validating Codex, Claude, and OpenCode adapter archives.

## Outcome and retrospective

- Not started. Fill after implementation, review-resolution if any, explain-change, verify, and PR handoff complete.

## Readiness

- See `Current Handoff Summary`.
