# Code Review R5: Requirement-Fidelity Gate M4

Review ID: code-review-r5
Stage: code-review
Round: 5
Reviewer: Codex code-review skill
Target: M4 implementation diff
Reviewed artifact: M4 implementation at commit d1890647
Reviewed commit: d1890647 M4: add requirement-compression calibration fixtures
Reviewed milestone: M4. Compression calibration corpus and sampling records
Review date: 2026-06-26
Recording status: recorded
Status: changes-requested
Autoprogression profile: implementation-through-verify
Material findings: RFG-M4-CR1
Review status: changes-requested
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L1
Author context ID: m4-implementation-author-ctx
Reviewer context ID: m4-r5-reviewer-ctx
Context separation mechanism: fresh-context-same-model
Risk tier: standard
Risk-tier triggers: calibration validator and sampling record contract
Risk-tier classifier: deterministic-paths
Governing artifacts: specs/requirement-fidelity-gate.md; specs/requirement-fidelity-gate.test.md; docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md
Formal criteria: R17; R17a; R17b; R17c; R17d; R41; R42; R43; R44; R44a; R44b; R44c; R44d; R44e; R44f; R44g; R45; R45a; R45b; R45c; AC-RFG-012; AC-RFG-014; AC-RFG-015; AC-RFG-020
Initial packet inventory: specs/requirement-fidelity-gate.md@HEAD#sha256:1111111111111111111111111111111111111111111111111111111111111111; specs/requirement-fidelity-gate.test.md@HEAD#sha256:2222222222222222222222222222222222222222222222222222222222222222; docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md@HEAD#sha256:3333333333333333333333333333333333333333333333333333333333333333; git-show-d1890647@HEAD#sha256:4444444444444444444444444444444444444444444444444444444444444444
Prompt template version: code-review-template-v1
Initial packet hash: sha256:5555555555555555555555555555555555555555555555555555555555555555
Manifest owner: orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Affected behavior: requirement-compression calibration record validation; sampling floors; rotation trigger evidence; public calibration fixture routing
Highest-impact failure modes: misclassified not-applicable receipt lacks corrective action; corpus record omits canonical R26 seed; closed enum drift passes silently; public fixture mistaken for private measured corpus
Changed boundaries: review artifact validator, review-artifact validator tests, review-artifact fixtures, selector routing test, plan and change metadata
Evidence expected: negative fixtures for corpus completeness, sampling floors, closed calibration vocabularies, rotation fields, and corrective action on misclassification
Areas requiring direct inspection: `scripts/review_artifact_validation.py`; `scripts/test-review-artifact-validator.py`; `tests/fixtures/review-artifacts/valid-requirement-compression-calibration/reviews/code-review-r1.md`; M4 validation notes
Areas intentionally out of scope: M5 generated adapter refresh; final holistic code review; private rotating corpus contents
Risk classes considered: requirement-compression calibration=applicable; validation adequacy=applicable; historical compatibility=applicable; security/privacy=not-applicable:no secret or auth surface
Falsifiable review questions: Does every R42 seed type have accepted evidence? Does missing R26 canonical seed fail? Do Phase B floors fail below threshold? Does every R44g trigger stay closed? Does a misclassified not-applicable audit require corrective action?
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/review_artifact_validation.py; scripts/test-review-artifact-validator.py; scripts/test-select-validation.py; tests/fixtures/review-artifacts/valid-requirement-compression-calibration/
Requirement-fidelity matched path triggers: scripts/*validator*
Requirement-fidelity matched category triggers: review-recording contracts; closed enums; metadata validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence > prior findings
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: finding IDs RFG-M4-CR1
Requirement-fidelity no-finding rationale: not applicable; material finding recorded.

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r5.md; docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md; docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md; docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md; docs/plan.md; docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFG-M4-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/code-review-r5.md
- Review log: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-log.md
- Review resolution: docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/review-resolution.md#code-review-r5
- Reviewed milestone: M4
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M4, M5
- Required review-resolution: yes
- Finding IDs: RFG-M4-CR1
- Verify readiness: not-claimed

## Review Inputs

- Implementation diff: commit `d1890647`
- Approved spec: `specs/requirement-fidelity-gate.md`
- Test spec: `specs/requirement-fidelity-gate.test.md`
- Active plan: `docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md`
- Validation evidence: targeted M4 validator tests, public calibration fixture validation, focused selector routing test, full review-artifact/lifecycle/change-metadata regression suites, and change-local validators recorded in the plan and change metadata

## Diff Summary

M4 adds `requirement-compression` calibration fields to the review-artifact validator, including seed-type coverage, corpus iteration identifiers, R26 canonical seed evidence, sampling floor fields, rotation trigger fields, and closed vocabularies for sampling reasons, audit outcomes, and rotation triggers.

The implementation adds unit tests for incomplete corpus records, below-floor sampling rates, unknown closed values, missing iteration and rotation fields, a public valid calibration fixture, selector routing coverage for that fixture, and a soft-normative `MUST` wording scan for the requirement-fidelity spec.

## Requirement-Property Decomposition

| Spec clause | Requirement property | Required surfaces | Verified? | Evidence |
| --- | --- | --- | --- | --- |
| `R41`-`R43` | seeded family includes `requirement-compression`, all six seed types, and canonical R26 missing-`recorded` seed | validator constants; validator tests; public fixture | yes | `scripts/review_artifact_validation.py:226`; `scripts/test-review-artifact-validator.py:1607`; `tests/fixtures/review-artifacts/valid-requirement-compression-calibration/reviews/code-review-r1.md:76` |
| `R44`-`R44g` | named iteration ID and closed rotation trigger fields are recorded | validator required fields; closed trigger constants; tests | partial | Required fields and unknown trigger tests exist, but only one of three valid rotation triggers has positive fixture coverage. |
| `R17`-`R17d`, `R45`-`R45c` | Phase B floors, steady-state floors, sampling reason, audit outcome, and corrective action are recorded and validated | validator fields; sampling tests; direct probe | no | `scripts/review_artifact_validation.py:2078`; direct probe showed `Audit outcome: misclassified-should-have-applied` with `Corrective action: none` produces zero blocking findings. |
| `RFG-T022` | unquantified soft-normative `MUST` wording is rejected | review-artifact validator test | yes | `scripts/test-review-artifact-validator.py:1756` |

## Findings

### RFG-M4-CR1 - Misclassified not-applicable audits can omit corrective action

Finding ID: RFG-M4-CR1
Severity: major
Location: scripts/review_artifact_validation.py:2078
Evidence: `R45b` requires each sampled not-applicable receipt to record `corrective_action` when misclassified. The M4 validator only requires a `Corrective action` field and never checks its value against `Audit outcome`. I confirmed this with a direct validation probe: replacing `Audit outcome: correct` with `Audit outcome: misclassified-should-have-applied` while leaving `Corrective action: none` produced `blocking_findings=0`. That lets a sampled misclassification pass without any actual corrective action.
Required outcome: Requirement-compression calibration validation must fail when `Audit outcome: misclassified-should-have-applied` is paired with missing, empty, or `none` corrective action. Add a regression test for this exact negative case.
Safe resolution path: In `scripts/review_artifact_validation.py`, after parsing `Audit outcome` and `Corrective action`, add a check that rejects `Audit outcome: misclassified-should-have-applied` unless `Corrective action` is present and not `none`. In `scripts/test-review-artifact-validator.py`, add a case that changes the valid RFG calibration fixture to `Audit outcome: misclassified-should-have-applied` with `Corrective action: none` and expects a stable validation message such as `requirement-compression misclassified audit requires corrective action`.
needs-decision rationale: none
auto_fix_class: declared-safe
affected_paths: scripts/review_artifact_validation.py; scripts/test-review-artifact-validator.py
resolution_recipe: Add a targeted negative test for `Audit outcome: misclassified-should-have-applied` with `Corrective action: none`, then update the validator to reject missing, empty, or `none` corrective action for that audit outcome.
named_inputs: `R45b`; valid requirement-compression calibration fixture; direct probe showing `blocking_findings=0`
named_outputs: blocking validation finding for misclassified audit without corrective action
forbidden_paths: specs/; skills/; docs/architecture/; docs/adr/; generated output
acceptance_criteria: targeted negative test fails before the fix and passes after the validator rejects missing/no-op corrective action; existing valid requirement-compression calibration fixture remains valid
required_validation_commands: `python scripts/test-review-artifact-validator.py -k requirement_compression`; `python scripts/validate-review-artifacts.py --mode structure tests/fixtures/review-artifacts/valid-requirement-compression-calibration`; change-local metadata and lifecycle validators after resolution recording
scope_preservation_rule: change only the review-artifact validator branch and regression test needed for the conditional corrective-action requirement; do not revise the approved spec or broaden calibration semantics
production_code_change: no

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | `R45b` requires corrective action when misclassified; the validator accepts `misclassified-should-have-applied` with `Corrective action: none`. |
| Test coverage | concern | Tests cover unknown `audit_outcome` values, but no negative test covers the conditional corrective-action requirement. |
| Edge cases | block | The misclassified not-applicable receipt path is a named M4 calibration edge case and currently passes without action. |
| Error handling | concern | Closed enums fail for unknown audit outcomes, but a known audit outcome can still be semantically incomplete. |
| Architecture boundaries | pass | The diff stays inside review-artifact validation, tests, fixtures, selector routing, and lifecycle metadata. |
| Compatibility | pass | Existing full review-artifact, lifecycle, and change-metadata suites are recorded as passing; the new finding is localized to the new M4 RFG calibration branch. |
| Security/privacy | pass | The diff touches no secrets, auth, private corpus contents, network behavior, or side-effecting external systems. |
| Derived artifact currency | pass | No canonical skill or generated adapter output is changed in M4; M5 remains the generated-output milestone. |
| Unrelated changes | pass | The diff is scoped to M4 calibration validator behavior, tests, fixture, selector routing case, and plan/change metadata. |
| Validation evidence | concern | Targeted and full validator suites are relevant, but they miss the corrective-action conditional path. Full `test-select-validation.py` was also interrupted while waiting in preflight Git status; the targeted selector route did pass. |

## No-Finding Rationale

Not applicable. One material finding is recorded.

## Residual Risks

The review did not require a finding for the interrupted full selector suite because the touched selector behavior has direct targeted proof, but full selector validation remains useful during resolution or final closeout if it completes. M5 generated-output refresh and final holistic code-review remain pending.

## Milestone Handoff

M4 remains open and moves to `resolution-needed`. The next stage is `review-resolution` for `RFG-M4-CR1`. M5 remains open, so final closeout is not ready.
