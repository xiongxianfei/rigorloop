# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3 reviewer-owned finding classification and correction guardrails implementation diff
Status: changes-requested
Autoprogression profile: implementation-through-verify

## Review inputs

- Diff/review surface: `scripts/review_artifact_validation.py`, `scripts/test-review-artifact-validator.py`, `scripts/lifecycle_state_sync.py`, `scripts/test-artifact-lifecycle-validator.py`, active plan, plan index, and change metadata state updates.
- Tracked governing branch state: local branch `proposal/implementation-autoprogression-through-verify`; governing artifacts are present in the working tree for this change.
- Governing artifacts: `specs/workflow-stage-autoprogression.md` R2be-R2bu, `specs/review-finding-resolution-contract.md` R1e-R1l and R11, `specs/implementation-autoprogression-through-verify.test.md` T7-T11, and `docs/plans/2026-06-24-implementation-autoprogression-through-verify.md` M3.
- Validation evidence reviewed: `python scripts/test-review-artifact-validator.py -k auto_fix`, `python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails`, full `test-review-artifact-validator.py`, full `test-artifact-lifecycle-validator.py`, change metadata validation, review artifact validation, artifact lifecycle explicit-path validation, and `git diff --check`.

## Diff summary

M3 adds implementation-profile finding classification validation to the review artifact parser and adds a fixture-driven automatic correction guardrail evaluator. The parser enforces `auto_fix_class`, closed mechanical kinds, required mechanical fields, complete declared-safe recipes, and production-code behavior proof labels for review files that identify `implementation-through-verify`. The correction evaluator enforces class presence, round caps, shrinking finding sets, no-new-finding sets, path locality, governing-artifact stops, scope-budget stops, command approval, CI scope and deny-list checks, and audit presence.

## Findings

### CR-M3-R1-F1: Correction path locality can bypass reviewer-declared affected paths

Finding ID: CR-M3-R1-F1
Severity: major
Location: `scripts/lifecycle_state_sync.py:758`
Evidence: `evaluate_implementation_correction_guardrails()` builds `allowed_paths` from top-level `data.get("affected_paths")` and never cross-checks it against each finding's reviewer-declared `affected_paths`. The fixture shows findings carry their own affected paths at `scripts/test-artifact-lifecycle-validator.py:1488`, but the evaluator would allow a caller to set `findings[0].affected_paths=["scripts/example.py"]`, top-level `affected_paths=["scripts/other.py"]`, and `changed_paths=["scripts/other.py"]`; that would pass path locality even though the reviewer did not declare `scripts/other.py` for the finding. This violates `workflow-stage-autoprogression` R2bp, which limits automatic correction diffs to reviewer-declared affected paths plus explicitly approved generated/projection/evidence paths.
Required outcome: The correction guardrail must derive the ordinary correction path set from the unresolved findings' reviewer-declared `affected_paths`, or validate that any top-level path allowance exactly matches that reviewer-declared union before allowing a correction.
Safe resolution: Add a regression where finding-level `affected_paths` and top-level/changed paths diverge, expect `correction-path-out-of-scope`, then change the evaluator to use or verify the finding-level affected path union. Keep approved generated outputs, workflow projections, and evidence records as explicit extra allowlists.
auto_fix_class: declared-safe
affected_paths: scripts/lifecycle_state_sync.py, scripts/test-artifact-lifecycle-validator.py
resolution_recipe: Add a failing correction-guardrail fixture with mismatched finding-level and top-level affected paths; implement reviewer-declared affected-path union enforcement before evaluating changed paths.
named_inputs: workflow-stage-autoprogression R2bp; implementation-autoprogression-through-verify.test.md T10
named_outputs: correction guardrail route result and focused fixture test
forbidden_paths: docs/proposals/, specs/, docs/architecture/, docs/adr/, docs/plans/
acceptance_criteria: A changed path outside every finding-level affected path pauses unless it is an approved generated output, workflow projection, or evidence record.
required_validation_commands: python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails; python scripts/test-artifact-lifecycle-validator.py
scope_preservation_rule: No new runtime dependency, public interface, external integration, or governing artifact change.
production_code_change: yes
behavior_test: scripts/test-artifact-lifecycle-validator.py::test_implementation_correction_guardrails_enforce_path_scope_and_commands

### CR-M3-R1-F2: Mechanical correction eligibility does not require deterministic authority

Finding ID: CR-M3-R1-F2
Severity: major
Location: `scripts/lifecycle_state_sync.py:807`
Evidence: `_correction_findings_stop_reason()` accepts `auto_fix_class=mechanical` after checking only `auto_fix_kind`, `affected_paths`, and `required_validation`; it never requires `deterministic_authority`. The default correction fixture at `scripts/test-artifact-lifecycle-validator.py:1484`-`1490` omits `deterministic_authority` and still reaches `code-review M3`. This violates `workflow-stage-autoprogression` R2bj and `review-finding-resolution-contract` R1h, both of which require mechanical findings to name deterministic authority before automatic correction eligibility.
Required outcome: Mechanical correction eligibility must pause when `deterministic_authority` is missing or empty, and focused tests must prove the missing-authority path.
Safe resolution: Add a correction-guardrail regression for a mechanical finding without deterministic authority, expect a dedicated stop reason, then require `deterministic_authority` in `_correction_findings_stop_reason()` and add it to the valid fixture.
auto_fix_class: declared-safe
affected_paths: scripts/lifecycle_state_sync.py, scripts/test-artifact-lifecycle-validator.py
resolution_recipe: Add a failing mechanical correction fixture without deterministic authority; require nonempty deterministic_authority for mechanical findings; update valid fixture data to include the deterministic authority.
named_inputs: workflow-stage-autoprogression R2bj; review-finding-resolution-contract R1h; implementation-autoprogression-through-verify.test.md T8
named_outputs: correction guardrail route result and focused fixture test
forbidden_paths: docs/proposals/, specs/, docs/architecture/, docs/adr/, docs/plans/
acceptance_criteria: Mechanical findings without deterministic authority pause before automatic correction eligibility is granted.
required_validation_commands: python scripts/test-artifact-lifecycle-validator.py -k correction_guardrails; python scripts/test-artifact-lifecycle-validator.py
scope_preservation_rule: No new runtime dependency, public interface, external integration, or governing artifact change.
production_code_change: yes
behavior_test: scripts/test-artifact-lifecycle-validator.py::test_implementation_correction_guardrails_pause_on_unclassified_or_invalid_findings

## Checklist coverage

1. Spec alignment: block. CR-M3-R1-F1 violates R2bp path-locality authority; CR-M3-R1-F2 violates R2bj/R1h deterministic-authority eligibility.
2. Test coverage: block. Current tests prove some M3 paths, but they do not cover mismatched finding-level affected paths or missing mechanical deterministic authority.
3. Edge cases: block. T8 and T10 include deterministic authority and reviewer-declared path locality; both have direct proof gaps.
4. Error handling: concern. Existing stop reasons are deterministic, but two required invalid states currently route as eligible.
5. Architecture boundaries: pass. The slice stays inside existing validators and fixture evaluators.
6. Compatibility: pass. Existing full validator suites pass, and the added fields are scoped to implementation-profile review records.
7. Security/privacy: pass. No secrets, credentials, network, or external-action behavior added.
8. Derived artifact currency: pass. M3 does not edit generated adapters or generated skill output.
9. Unrelated changes: pass. The reviewed diff is scoped to review artifact validation, correction guardrails, tests, and lifecycle handoff metadata.
10. Validation evidence: concern. The named commands passed, but they miss the two contract-required negative cases above.

## No-finding rationale

Not applicable. Material findings were found.

## Residual risks

The review did not evaluate M4 skill/adapters or Phase C behavior, which remain planned future milestones. The current findings are limited to M3 correction eligibility and guardrail proof.

## Milestone handoff state

- Reviewed milestone: M3. Reviewer-owned finding classification and correction guardrails
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M3, M4, M5
- Next stage: review-resolution M3
- Final closeout readiness: not ready
- Verify readiness: not-claimed
