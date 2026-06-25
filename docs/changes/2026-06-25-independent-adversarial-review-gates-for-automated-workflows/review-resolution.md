# Independent Adversarial Review Gates Review Resolution

## Scope

This record closes formal proposal-review, spec-review, architecture-review, and plan-review evidence for the independent adversarial review gates change.

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `plan-review-r2`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m1-r3`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m3-r1`
- Findings resolved: 6
- Unresolved findings: 2
- Current result: proposal-review rounds approved the proposal with no material findings. Spec-review R1 requested `SR1-F1`; the spec was revised, and spec-review R2 approved the revised contract. Architecture-review R1 approved the canonical architecture update and ADR with no material findings. Plan-review R1 requested `PR1-F1`; the plan was revised, and plan-review R2 approved it with no material findings. Code-review M1 R1 requested `CR1-F1` and `CR1-F2`; both findings are resolved. Code-review M1 R2 requested `CR2-F1`; it is resolved. Code-review M1 R3 approved the M1 resolution with no material findings. Code-review M2 R1 requested `CR3-F1`; it is resolved. Code-review M2 R2 approved the M2 resolution with no material findings. Code-review M3 R1 requested `CR4-F1` and `CR4-F2`; both require review-resolution.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| SR1-F1 | accepted | resolved | Added `R12f` stop semantics, examples, acceptance criterion, and test IDs; `spec-review-r2` approved the revised contract. |
| PR1-F1 | accepted | resolved | Added adapter archive generation and validation commands to M3 and M5; added a top-level validation invariant for `skills/` changes; added a boundary statement distinguishing local skill proof from public adapter archive proof. |
| CR1-F1 | accepted | resolved | Added native review status as required manifest evidence, mapping validation, valid fixture updates, and missing/empty/mismatched regression tests. |
| CR1-F2 | accepted | resolved | Added T1 valid L1/L2/L3 fixture enumeration and invalid direct proof for missing context separation, unsupported independence level, and missing reviewer context ID on an unverifiable platform. |
| CR2-F1 | accepted | resolved | Converted native review status validation from guard-style to fail-closed gate-style; added unknown-value regression tests, T1 fixture coverage, allowed-values error proof, and closed-vocabulary discipline guidance. |
| CR3-F1 | accepted | resolved | Split determinate native outcome mapping from clean native gate-derived outcome logic and added clean-gate routing coverage. |
| CR4-F1 | accepted | open | Code-review guidance must define the required `failed-remediation` rediscovery condition and test it. |
| CR4-F2 | accepted | open | Implement handoff guidance must exclude `auto-fix eligibility` from the initial review packet and test it. |

## Finding Details

### proposal-review-r1

No material findings; no resolution entry required. The review approved the proposal and directed downstream specification details.

### proposal-review-r2

No material findings; no resolution entry required. The isolated formal proposal-review confirmed the accepted proposal remains ready for downstream specification work.

### spec-review-r1

#### SR1-F1 - Normalized `stop` outcome is ambiguous for changes-requested reviews

Finding ID: SR1-F1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Added `R12f` and sub-requirements defining `review_gate_outcome: stop` semantics for native `changes-requested`; clarified `R14g` as second-review disagreement only; added Examples E8-E10; added `AC-RAI-018`; added test IDs `RAI-021`, `RAI-022`, and `RAI-023`.
Rationale: Without this clarification, architecture, tests, and implementation could reasonably choose incompatible behaviors: pausing all automation on `changes-requested` or routing into review-resolution under existing approved authority.
Validation target: Rerun `spec-review-r2`.
Validation evidence: `specs/review-independence-and-criticality.md` now preserves `code-review changes-requested -> review-resolution` routing when the active profile's existing gates pass, and supersedes implicit-route behavior for other review stages by requiring explicit active-profile authorization. `spec-review-r2` approved the revised contract with no material findings.

### spec-review-r2

No material findings; no resolution entry required. This same-stage rereview approved the revised spec and closed `SR1-F1`.

### architecture-review-r1

No material findings; no resolution entry required. The review approved the canonical architecture package update and ADR for planning.

### plan-review-r1

#### PR1-F1 - Generated adapter proof is in scope but lacks runnable validation commands

Finding ID: PR1-F1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Added temporary adapter archive generation and validation commands to M3 for canonical skill changes and to M5 as final cross-milestone proof; added a top-level validation-plan invariant binding `skills/` changes to public adapter archive proof; added a generated skill and adapter proof boundary statement distinguishing `build-skills.py --check` from `build-adapters.py --output-dir` plus `validate-adapters.py --root`.
Rationale: Canonical stage-skill changes must prove both local generated skill output and public adapter archive output. Architecture sections at `docs/architecture/system/architecture.md:315`, `docs/architecture/system/architecture.md:316`, and `docs/architecture/system/architecture.md:913` require adapter generation and validation for stage-skill changes; `AGENTS.md:34` and `AGENTS.md:36` establish that public adapter skill bodies are release archives, not tracked source, and generated public adapter package output must not be hand-edited.
Validation target: Rerun `plan-review-r2`.
Validation evidence: `docs/plans/2026-06-25-independent-adversarial-review-gates.md` now names adapter archive proof in M3, M5, and the top-level validation plan. The plan records that `build-skills.py --check` proves local-skill output, while `build-adapters.py --output-dir <tmpdir>` followed by `validate-adapters.py --root <tmpdir>` proves public adapter archive output. This resolution was discovered under isolated formal plan-review; manual review discipline continues for this change pending independence-gates landing.

### plan-review-r2

No material findings; no resolution entry required. This same-stage rereview approved the revised execution plan and closed `PR1-F1`.

### code-review-m1-r1

#### CR1-F1 - Automated review gates can advance without recording the native review result

Finding ID: CR1-F1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implement M1 review-resolution
Chosen action: Added `Native review status` to the spec-cited `REVIEW_GATE_REQUIRED_FIELDS` constant; added R12 native-status to `review_gate_outcome` consistency validation; updated valid automated review gate fixtures to include native status; added regression tests for missing, empty, and mismatched native review status.
Rationale: The validator's automated review gate required-field set omits native review result evidence even though the spec and observability contract require it.
Validation target: Rerun `code-review-m1-r2`.
Validation evidence: `python scripts/test-review-artifact-validator.py -k native_review_status` ran 2 tests and passed; `python scripts/test-review-artifact-validator.py -k mismatched_native` ran 1 test and passed; `python scripts/test-review-artifact-validator.py` passed with 62 tests, up from 57 in the M1 handoff commit.

#### CR1-F2 - Independence-level matrix proof is incomplete for named T1 cases

Finding ID: CR1-F2
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implement M1 review-resolution
Chosen action: Added durable T1 fixtures for valid L1, existing valid L2, valid L3 critical-internal heterogeneous review, missing context separation, unsupported independence level, and missing reviewer context ID on an unverifiable platform; converted T1 validation to `T1_VALID_CASES` and `T1_INVALID_CASES` enumeration-driven tests.
Rationale: T1 names valid L1/L2/L3 proof and invalid manifest proof for missing context separation, unsupported independence level, and missing reviewer context identity; the M1 tests do not directly cover several of those named cases.
Validation target: Rerun `code-review-m1-r2`.
Validation evidence: `python scripts/test-review-artifact-validator.py -k t1_` ran 2 parameterized tests covering 3 valid cases and 3 invalid cases and passed; `python scripts/test-review-artifact-validator.py` passed with 62 tests, up from 57 in the M1 handoff commit.

Platform-verifiability note: M1 now recognizes `Platform verifiability: unverifiable` as review-gate process evidence and emits `reviewer-context-id-required-on-unverifiable-platform` when reviewer context identity is missing. No separate finding is needed for the M1 surface.

Meta-resolution note: `CR1-F1` is the M1 meta-self-check for the manifest contract M1 defines. The fix keeps the required-field enumeration in a named constant with an explicit spec-source comment. The broader repository-wide required-field and T-ID enumeration audit remains a process follow-up before M2 rather than a hidden M1 expansion.

### code-review-m1-r2

#### CR2-F1 - Unknown native review statuses can still advance as clean automated review gates

Finding ID: CR2-F1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implement M1 review-resolution
Chosen action: Converted native review status validation from `if value in NATIVE_STATUS_GATE_OUTCOMES` guard-style checking to fail-closed gate-style checking. Unsupported values now emit `unsupported native review status '<value>'; allowed values are ... per specs/review-independence-and-criticality.md R12` before known-value mismatch validation runs. Added regression tests parameterized across `rubber-stamp`, `lgtm`, and `bogus`; added an allowed-values error test; added `tests/fixtures/review-artifacts/invalid-unknown-native-review-status/`; added the case to the T1 invalid fixture enumeration and to `specs/review-independence-and-criticality.test.md`; added closed-vocabulary validator discipline to `AGENTS.md`.
Rationale: Code-review M1 R2 found that `Native review status` values outside the supported stage-native vocabulary are not rejected. A temporary fixture with `Native review status: rubber-stamp` and `Review gate outcome: advance` validated with zero findings.
Validation target: Rerun `code-review-m1-r3`.
Validation evidence: `python scripts/test-review-artifact-validator.py -k unknown_native` failed before the implementation change and passed afterward with 2 tests; `python scripts/test-review-artifact-validator.py -k t1_` failed before the implementation change on `unknown-native-review-status` and passed afterward with 2 parameterized tests covering 3 valid cases and 4 invalid cases; `python scripts/test-review-artifact-validator.py` passed with 64 tests; direct validation of `tests/fixtures/review-artifacts/invalid-unknown-native-review-status` failed with `unsupported native review status 'rubber-stamp'` and listed the allowed values. The scoped audit command `rg -n "if .* in [A-Z][A-Z0-9_]+| if .* not in [A-Z][A-Z0-9_]+|\\.value in [A-Z][A-Z0-9_]+" scripts/review_artifact_validation.py scripts/change_metadata_semantics.py scripts/validate-change-metadata.py scripts/lifecycle_state_sync.py` identified `scripts/review_artifact_validation.py:824` as the M1 guard-style defect; other reviewed uppercase-vocabulary validation occurrences were already fail-closed gates or documented routing/forbidden-key membership checks.

Structural prevention note: `AGENTS.md` now requires validator closed-vocabulary checks against constants such as `*_OUTCOMES`, `*_FIELDS`, and `*_KINDS` to fail closed on unknown values before consistency checks, and says new closed-vocabulary validator constants should include unknown-value regression tests.

### code-review-m1-r3

No material findings; no resolution entry required. This same-stage rereview approved the revised M1 review-gate evidence validator and closed the M1 review-resolution loop.

### code-review-m2-r1

#### CR3-F1 - Clean-status evidence failures cannot produce the required inconclusive gate outcome

Finding ID: CR3-F1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implement M2 review-resolution
Chosen action: Split native verdict handling into `DETERMINATE_NATIVE_OUTCOMES` for unconditional `changes-requested`, `blocked`, and `inconclusive` mappings and `CLEAN_NATIVE_STATUSES` for gate-derived clean verdicts. Added `CLEAN_ADVANCE_GATES` with an explicit R12c/R12d/R13c source comment, reordered evaluation so clean verdicts derive the expected outcome from independence/evidence/recording/clean-receipt/escalation gates before consistency checking, and added `review-gate-outcome-mismatch-given-gate-state` for supplied `advance` when gate state requires `inconclusive`.
Rationale: Code-review M2 R1 found that `evaluate_automated_review_gate_route` rejects `clean-with-notes` plus `review_gate_outcome: inconclusive` as a native/derived mismatch before evaluating clean/evidence gates, even though the spec requires materially insufficient clean evidence to produce `review_gate_outcome: inconclusive`.
Validation target: Rerun `code-review-m2-r2`.
Validation evidence: `python scripts/test-artifact-lifecycle-validator.py -k review_gate` passed with 6 tests, including 11 routing subcases and a property-style check covering every `CLEAN_ADVANCE_GATES` entry; `python scripts/test-artifact-lifecycle-validator.py -k phase_boundaries` passed with 1 test; `python scripts/test-artifact-lifecycle-validator.py` passed with 134 tests, up from 132 in the M2 handoff commit; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m2-r1.md` passed; `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed.
Required outcome: Adjust the routing helper and tests so clean native statuses advance only when required gates pass and missing or insufficient clean/evidence gates can produce the required inconclusive gate outcome instead of a mismatch stop.

Audit note: This finding expands the validator audit pattern beyond guard-style unknown-value fall-through. Constants that are used both for unconditional supplied-value consistency checking and conditional gate-derived outcome computation should be split so each constant has one role.

### code-review-m2-r2

No material findings; no resolution entry required. This same-stage rereview approved the `CR3-F1` resolution and closed the M2 review-resolution loop.

### code-review-m3-r1

#### CR4-F1 - `failed-remediation` is named but not operationally defined in code-review guidance

Finding ID: CR4-F1
Disposition: accepted
Status: open
Owner: implement
Owning stage: implement M3 review-resolution
Chosen action: Add the required `failed-remediation` condition to `skills/code-review/SKILL.md` and add a matching assertion to `test_review_independence_m3_code_review_pilot_guidance`.
Rationale: The spec requires `failed-remediation` when a prior finding was claimed or expected to be fixed but is independently rediscovered during the blind-first pass. Naming the category without the condition leaves reviewer behavior under-specified.
Expected proof: `python scripts/test-skill-validator.py -k review_independence_m3`; full `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; generated skill and adapter proof commands.

#### CR4-F2 - Implement handoff guidance still permits `auto-fix eligibility` in the initial packet

Finding ID: CR4-F2
Disposition: accepted
Status: open
Owner: implement
Owning stage: implement M3 review-resolution
Chosen action: Add `auto-fix eligibility` to the forbidden initial packet list in `skills/implement/SKILL.md` and update `test_review_independence_m3_workflow_and_implement_route_automated_gate` to require it.
Rationale: The initial review packet must not include fixability signals before independent review discovery. `code-review` excludes `auto-fix eligibility`, but `implement` owns the handoff and currently omits that prohibited item.
Expected proof: `python scripts/test-skill-validator.py -k review_independence_m3`; full `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; generated skill and adapter proof commands.
