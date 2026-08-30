# Final Holistic Code Review R3: Lifecycle Request Selector Routing

Review ID: code-review-final-r3
Stage: code-review
Round: r3
Reviewer: Codex independent code-review context `/root/cli_fix_review`
Review date: 2026-08-30
Review scope: post-verify final-holistic correction
Target: selector correction commit `523762d789bf1cece8b865f8a55ea028ba2f760d`
Reviewed artifact: `scripts/validation_selection.py` and `scripts/test-select-validation.py`
Reviewed milestone: none
Reviewed revision: `523762d789bf1cece8b865f8a55ea028ba2f760d`

Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: CRG-SEL-CR1

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this final review record, the review log, and matching review resolution
- Open blockers: CRG-SEL-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CRG-SEL-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-final-r3.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md#code-review-final-r3`
- Reviewed milestone: none
- Milestone closeout: resolution-needed
- Remaining implementation milestones: none
- Required review-resolution: yes
- Finding IDs: CRG-SEL-CR1
- Verify readiness: not-claimed

## Review inputs

- Commit range: `79700526f2dda91e081ca97733005085e9579652..523762d789bf1cece8b865f8a55ea028ba2f760d`.
- Governing authority: `specs/test-layering-and-change-scoped-validation.md` R13 through R15, `specs/change-record-catalog-registration-and-bounded-read-model.md` CRM-R7 through CRM-R15 and CRM-R50, accepted `ADR-20260522-change-record-catalog-registration-and-bounded-read-model`, and `specs/governed-lifecycle-cli.md` request-input contract.
- Direct inspection: request-path classification, selected lifecycle check, selector fixture, artifact-lifecycle scope resolution, and the current change's request inputs.
- Review mode: explicit independent read-only review requested as a stop gate for the final review basis.

## Actual-diff summary

The commit classified every exact-depth `docs/changes/<change-id>/requests/*.json` path as `change-local-lifecycle` and added a selector test that asserted an `ok` result plus selection of `artifact_lifecycle.validate`. The path predicate was bounded, but the selected validator did not parse or validate JSON request content.

## Finding CRG-SEL-CR1

Finding ID: CRG-SEL-CR1

Severity: major

Location: `scripts/validation_selection.py:2433`; `scripts/test-select-validation.py:1347`; `scripts/artifact_lifecycle_validation.py:1771`

Evidence: The new rule classified any JSON filename directly under `requests/`, including `requests/arbitrary.json`, as a lifecycle artifact. The selected `artifact_lifecycle.validate` check reads content only for Markdown and YAML paths and has no request-schema branch, so it accepted the request path without parsing its JSON, validating its operation vocabulary, or associating it with its owning change record. The new test asserted check selection but did not execute the selected command or prove request validation. Direct execution of the selected lifecycle command passed while reporting only the lifecycle artifacts it recognized, not the JSON request.

Required outcome: A changed lifecycle request must receive meaningful validation or remain a transient, non-durable input that does not enter the governed diff. Selector classification must not suppress `manual-routing-required` while its selected check ignores the changed file.

Safe resolution path: Either introduce a distinct request-input category with a validator for JSON syntax, schema version, closed operation and field vocabularies, repository-relative paths, and change ID without requiring historical revisions to remain current, or keep request files transient, remove them from the governed diff, and revert the selector exception and its fixture.

needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | The selector reports safe targeted proof for a path that its selected validator does not inspect, conflicting with R14 and CRM-R50. |
| Test coverage | block | The added fixture proves only selection; malformed, arbitrary, unknown-field, and selected-command execution paths are absent. |
| Edge cases | block | Any exact-depth JSON name is admitted, whether or not it is a lifecycle request. |
| Error handling | block | Invalid request content cannot produce a selector or validation failure through the selected route. |
| Architecture boundaries | concern | The route bypasses the registered-evidence architecture without defining a distinct transient-input contract. |
| Compatibility | pass | No existing runtime CLI operation or result shape changes in this commit. |
| Security/privacy | pass | The selector change adds no external, secret-bearing, permission, or network surface. |
| Derived artifact currency | pass | No generated adapter or published skill changes. |
| Unrelated changes | pass | The commit is bounded to the selector exception and its fixture. |
| Validation evidence | block | Selector regression passes, but direct execution shows the selected lifecycle validator ignores JSON content. |

## Direct proof

```text
python scripts/test-select-validation.py ValidationSelectionTests.test_change_local_cli_request_uses_lifecycle_validation
=> passed

python scripts/test-select-validation.py
=> passed

python scripts/select-validation.py --mode explicit --path docs/changes/2026-08-28-consolidate-rigorloop-review-gates/requests/start-m2.json
=> status ok; artifact_lifecycle.validate selected

python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml --path docs/changes/2026-08-28-consolidate-rigorloop-review-gates/requests/start-m2.json
=> passed while validating recognized lifecycle artifacts rather than the JSON request content
```

## Handoff

Final closeout is paused. Record an accepted disposition, correct the selector or remove the transient request inputs, rerun selector proof against the actual branch diff, and submit the correction for final holistic rereview. The earlier explanation and Verify evidence cannot establish readiness for a later correction.
