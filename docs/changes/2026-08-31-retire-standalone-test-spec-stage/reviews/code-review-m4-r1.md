# Code Review M4 R1

Review ID: code-review-m4-r1
Stage: code-review
Round: r1
Reviewer: Codex code-review skill
Target: M4. Assemble governance, validation, and adapter parity before activation
Reviewed artifact: implementation commit `376a8e17` (`M4: stage no-test-spec publication parity`)
Reviewed milestone: M4
Review date: 2026-08-31
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-log.md`, and `review-resolution.md`
- Open blockers: none
- Next stage: implement next milestone
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-log.md`
- Review resolution: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md#code-review-m4-r1`
- Reviewed milestone: M4
- Milestone closeout: closed
- Remaining implementation milestones: M5
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Scope

Reviewed M4 against approved Design package `design-review-r2`, Delivery package `delivery-review-r3`, the exact plan at sha256 `727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`, implementation commit `376a8e17`, and the recorded M4 validation evidence.

## Actual-diff summary

- Governing and workflow surfaces now state the contract-keyed preactivation boundary: registered v1 retains plan plus test specification, inactive v2 uses plan only, and M5 owns activation.
- Shared boundary guidance routes v2 verification-allocation gaps to plan while retaining the registered-v1 test-spec route.
- Activation-prerequisite validation rejects unknown lifecycle and stage values before readiness checks and reports exact sorted blocking change IDs.
- Temporary Codex, Claude Code, and opencode candidates omit standalone test-spec, carry all eight plan specialist references, reject mixed archives, and install cleanly.
- Released adapter metadata, the active v1 default, new-change scaffolding, and historical records remain unchanged.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The diff stages RTS-R17 through RTS-R20 and RTS-R22 through RTS-R25 without activating v2 or introducing a replacement artifact. |
| Test coverage | pass | Activation, governance, archive exactness, resource inclusion, mixed-package rejection, and clean-install regressions passed. |
| Edge cases | pass | Unknown lifecycle/stage values, pre-gate blockers, terminal records, post-gate v1 records, extra retired entries, and escaped resource ownership are represented. |
| Error handling | pass | Closed vocabularies fail before readiness checks; archive validation reports missing, unexpected, stale, and invalid content. |
| Architecture boundaries | pass | Semantic adequacy stays review-owned, activation stays M5-owned, and M4 uses existing lifecycle and adapter mechanisms. |
| Compatibility | pass | Released/default v1 behavior and historical records are unchanged; v2 output is temporary and explicit. |
| Security/privacy | pass | Exact archive entry and byte comparison rejects unexpected or escaped package content; no data or privilege surface changes. |
| Derived artifact currency | pass | Canonical skill resources generate deterministic staged archives for all supported adapters and pass clean-install validation. |
| Unrelated changes | pass | The implementation is limited to M4 governance, validation, packaging, tests, and evidence. |
| Validation evidence | pass | All M4 commands passed; focused independent review checks also passed. |

## No-finding rationale

M4 forms a coherent inactive publication candidate without changing the active contract. The activation prerequisite is executable and directly tested; invoking it through the public activation path remains properly assigned to M5, where the manifest is frozen and activation occurs. Exact archive comparison plus clean-install proof prevents a mixed adapter from passing, while the explicit inventory explains every intentionally unchanged active or historical surface.

## Validation performed

- `python scripts/test-change-metadata-validator.py LifecycleContractClassificationTests.test_activation_prerequisites_report_exact_blocking_change_ids LifecycleContractClassificationTests.test_activation_prerequisites_accept_post_delivery_and_terminal_records LifecycleContractClassificationTests.test_activation_prerequisites_reject_unknown_state_before_readiness LifecycleContractClassificationTests.test_activation_prerequisites_reject_unknown_stage_before_readiness`: 4 passed.
- `python scripts/test-skill-validator.py RetireStandaloneTestSpecM4Tests`: 3 passed.
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_staged_v2_archives_omit_test_spec_and_package_plan_methods AdapterDistributionTests.test_staged_v2_archive_validation_rejects_extra_retired_entrypoint`: 2 passed, including supported-adapter clean installs.
- `git show --check 376a8e17`: passed.
- `git diff --check 376a8e17^..376a8e17`: passed.
- Reviewed implementation evidence reports the complete required M4 suites passing: 81 change-metadata, 166 artifact-lifecycle, 110 review-artifact, 379 skill, 8 build-skill, and 154 adapter-distribution tests, plus build, prose, lifecycle, compilation, and whitespace checks.

## Residual risks

- M5 still must freeze the exact prior-contract inventory, wire the prerequisite into activation, switch the public graph and package selectors atomically, and prove post-gate v1 continuation.
- The canonical standalone entrypoints and released v1 adapter inventory remain present by design until M5.
- The existing untracked `packages/rigorloop/node_modules/` directory was not reviewed or modified.

## Handoff

- Reviewed milestone: M4
- Review status: clean-with-notes
- Milestone closeout: closed
- Remaining implementation milestones: M5
- Required review-resolution: no
- Recommended next stage: Workflow settles M4; M5 is the next implementation milestone.
- Final closeout readiness: not ready; M5 and lifecycle closeout remain open.
