# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1 review gate evidence model and validators implementation diff at commit `2685ae4c`
Reviewed artifact: M1 implementation diff at commit `2685ae4c`
Review date: 2026-06-25
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m1-r1.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md`, `docs/plans/2026-06-25-independent-adversarial-review-gates.md`, `docs/plan.md`, `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Open blockers: CR1-F1, CR1-F2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR1-F1, CR1-F2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md
- Review resolution: docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md
- Reviewed milestone: M1. Review gate evidence model and validators
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution, M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: CR1-F1, CR1-F2
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `HEAD^..HEAD` for commit `2685ae4c`, especially `scripts/review_artifact_validation.py`, `scripts/change_metadata_semantics.py`, `scripts/validate-change-metadata.py`, `scripts/test-review-artifact-validator.py`, `scripts/test-change-metadata-validator.py`, `tests/fixtures/review-artifacts/valid-automated-review-gate/`, `tests/fixtures/review-artifacts/invalid-automated-review-gate-l0/`, active plan and change metadata updates.
- Tracked governing branch state: branch `proposal/independent-adversarial-review-gates`; M1 implementation commit is tracked at `2685ae4c`. One unrelated untracked learn-session file exists and was excluded from the implementation review surface.
- Governing artifacts: `specs/review-independence-and-criticality.md` R1-R7, R13, R17, AC1-AC5, AC12; `specs/review-independence-and-criticality.test.md` T1-T4, T9, T12, T16, T19; `docs/plans/2026-06-25-independent-adversarial-review-gates.md` M1.
- Validation evidence reviewed: focused automated review gate tests, full review artifact validator suite, full change metadata validator suite, active change review artifact validation, active change metadata validation, lifecycle explicit-path validation, `git diff --check`, and whitespace scan as recorded in the active plan and rerun during review.

## Diff summary

M1 adds parser-owned automated review gate validation to `scripts/review_artifact_validation.py`, change-metadata semantic validation for optional `review.review_gate` records, targeted unit tests, and durable valid/fail-closed review artifact fixtures. It also records the accepted proposal/spec/architecture/plan/test-spec artifact package and updates the active plan to request `code-review M1`.

## Findings

### CR1-F1 - Automated review gates can advance without recording the native review result

Finding ID: CR1-F1
Severity: major
Location: `scripts/review_artifact_validation.py:66`
Evidence: `specs/review-independence-and-criticality.md:146`-`153` requires the review invocation manifest to record the native review status when known and the derived `review_gate_outcome`. The observability contract at `specs/review-independence-and-criticality.md:431`-`433` also says manifests expose the native review result and `review_gate_outcome`. The validator's `REVIEW_GATE_REQUIRED_FIELDS` includes `Review gate outcome` but does not include `Native review status`, and the checked-in valid fixture at `tests/fixtures/review-artifacts/valid-automated-review-gate/reviews/code-review-r1.md:8`-`12` passes without any native review result field. A temporary review proof deleted or omitted `Native review status` and `python scripts/validate-review-artifacts.py --mode structure <tmpdir>` still passed with `findings=0`.
Required outcome: Automated review gate records that can advance must fail closed when the native review result is absent from the manifest evidence.
Safe resolution path: Add `Native review status` to the automated review gate required-field set, add it to the valid fixtures, and add a negative validator test that removes it and expects a missing-required-field failure. Rerun `python scripts/test-review-artifact-validator.py` and the active change review artifact validation.
needs-decision rationale: none
auto_fix_class: none

### CR1-F2 - Independence-level matrix proof is incomplete for named T1 cases

Finding ID: CR1-F2
Severity: major
Location: `scripts/test-review-artifact-validator.py:768`
Evidence: `specs/review-independence-and-criticality.test.md:99`-`113` requires T1 to create valid automated review fixtures for standard `L1`, elevated `L2`, and critical internal `L3`, plus invalid fixtures for missing context separation mechanism, unsupported independence level, and missing reviewer context identity on an unverifiable platform. The current automated gate tests cover a generated valid `L1` record, a checked-in valid `L2` fixture, `L0`, same-context IDs, missing packet inventory, missing packet hash, attestation-only context exclusion, forbidden context labels, bad phase order, long free-form fields, and incomplete clean receipts. Repository search found no valid `L3` fixture or negative direct proof for missing context separation mechanism, unsupported independence level, or missing reviewer context identity. The code may reject some of these by generic required-field or enum checks, but the named T1 edge cases lack direct proof.
Required outcome: T1's named independence-level and invalid-manifest cases must have direct validator proof before M1 can close.
Safe resolution path: Extend the automated review gate tests and/or durable fixtures to cover valid `L3`, missing `Context separation mechanism`, unsupported `Independence level`, and missing `Reviewer context ID`. Keep the existing L1/L2/L0 coverage. Rerun `python scripts/test-review-artifact-validator.py` and `python scripts/test-change-metadata-validator.py` if change-metadata fixtures are extended.
needs-decision rationale: none
auto_fix_class: none

## Checklist coverage

1. Spec alignment: block. CR1-F1 violates the manifest and observability requirements for native review result evidence.
2. Test coverage: block. CR1-F2 leaves named T1 independence matrix and invalid-manifest cases without direct proof.
3. Edge cases: block. Missing native review result, valid L3, missing context separation, unsupported independence, and missing reviewer context identity are named or implied fail-closed cases.
4. Error handling: concern. The validator fails closed for several invalid states, but not for absent native result evidence.
5. Architecture boundaries: pass. The implementation stays inside review artifact validation, change metadata validation, fixtures, and lifecycle handoff artifacts; no hosted service or external control plane is introduced.
6. Compatibility: pass. Existing manual/profile-off review artifact validator tests continue to pass in the rerun suites.
7. Security/privacy: pass. The new validators reject several forbidden reasoning/context labels and do not introduce secret, credential, or network handling.
8. Derived artifact currency: pass. M1 does not edit canonical `skills/` files, so generated skill and adapter proof is not triggered in this milestone.
9. Unrelated changes: concern. The M1 commit includes upstream lifecycle artifacts plus implementation changes as expected for this branch. A separate untracked learn session exists in the working tree but is outside the reviewed M1 commit.
10. Validation evidence: concern. The named validation commands are relevant and pass, but they miss CR1-F1 and CR1-F2.

## No-finding rationale

Not applicable. Material findings were found.

## Residual risks

M2-M5 routing, skill guidance, calibration, generated adapter proof, and final holistic review behavior remain planned future milestones and were not reviewed as implemented behavior here.

## Milestone handoff state

- Reviewed milestone: M1. Review gate evidence model and validators
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining implementation milestones: M1 resolution, M2, M3, M4, M5
- Next stage: review-resolution M1
- Final closeout readiness: not ready
