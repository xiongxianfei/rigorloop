# Explain Change: Independent Adversarial Review Gates

Change ID: 2026-06-25-independent-adversarial-review-gates-for-automated-workflows
Status: active explanation
Explained after: code-review-m5-r2
Next stage: verify

## Summary

This change turns the accepted independent-adversarial-review-gates proposal into repository-enforced workflow behavior for the first implementation slice.

The implementation adds:

- structured automated review-gate evidence validation;
- normalized review-gate routing and fail-closed lifecycle checks;
- canonical skill guidance for the automated `code-review` pilot and Phase 1 manifest evidence for authoring reviews;
- calibration and sampling evidence for clean automated reviews;
- contributor workflow guidance and behavior-preservation evidence;
- durable review, resolution, validation, and lifecycle state records.

The core reason for the change is the proposal's finding that automated reviews can inherit the author's assumptions when the same workflow context authors, validates, and reviews a change. The implementation moves that safety claim from guidance into checkable evidence, state transitions, and review records.

## Problem

Autoprogression made review stages cheaper to invoke, but it also made author-context leakage, validation-result anchoring, prior-finding anchoring, and continuation incentives more likely. The approved proposal reframed the issue away from "not enough findings" and toward review sensitivity:

```text
the review process has low sensitivity to defects that share the author's assumptions.
```

The chosen response was not a finding quota. It was a structural gate: fresh review context, neutral initial packet, blind-first risk formation, evidence challenge, prior-finding reconciliation, risk-tier escalation, clean-review sufficiency receipts, and calibration.

## Decision Trail

| Stage | Decision | Resulting implementation |
| --- | --- | --- |
| Proposal | Adopt independent adversarial review gates and preserve clean reviews when evidence supports them. | Added validators, routing checks, skill guidance, calibration records, and final holistic review evidence. |
| Proposal-review | Approved with directives for normalized gate outcome, immutable packet evidence, L1/L2/L3 rules, second-review disagreement, and sampling floors. | Spec and plan carried these into R12, R14, R17, R18-R20, and M1-M5. |
| Spec | Define review-context levels, packet/phase evidence, clean receipts, risk tiers, stop semantics, calibration, and compatibility. | Implemented evidence fields and fail-closed checks in review-artifact, change-metadata, and lifecycle validators. |
| Architecture/ADR | Keep orchestrator-owned process evidence separate from reviewer-owned judgment. No new service or persistence. | Changes stay in repository scripts, docs, skills, fixtures, and change-local evidence. |
| Plan | Split into M1-M5: evidence validators, routing, skill pilot, calibration, generated/docs proof. | Each milestone added focused tests and review records before final holistic code-review. |
| Test spec | Map requirements to T1-T20, including critical-risk gates, calibration, skill guidance, generated adapters, synchronization, and cost visibility. | Test additions cite these surfaces through validator, lifecycle, skill, fixture, and manual evidence. |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `specs/review-independence-and-criticality.md` | Added critical-authority detail to R14d and closed yes/no calibration parsing to R17a. | Code-review found the downstream contract needed explicit L3/human authority and fail-closed control fields. | R14d, R17a, CR5-F1, CR5-F2, CR6-F1 | `test_review_gate_critical_authority_gates_clean_handoff`, calibration validator tests |
| `specs/review-independence-and-criticality.test.md` | Added T10c-T10g variants and T11d-T11g. | Named edge cases had to map to executable proof, including parser-order diagnostics. | T10, T11 | Lifecycle and review-artifact validator suites |
| `scripts/lifecycle_state_sync.py` | Added critical-authority vocabularies, parser-first checks, tier-specific authority requirements, and clean-gate integration. | Clean automated reviews must not advance for critical tiers without explicit authority; malformed authority input must fail before outcome mismatch. | R14d, T10, CR5-F1, CR6-F1 | `python scripts/test-artifact-lifecycle-validator.py` |
| `scripts/review_artifact_validation.py` | Added critical-authority calibration fields, shared yes/no parsing, authority validation, and sampling consumers that read parsed booleans. | Calibration records are process evidence and must reject ambiguous control values. | R17a, T11, CR5-F1, CR5-F2 | `python scripts/test-review-artifact-validator.py` |
| `scripts/test-artifact-lifecycle-validator.py` | Added critical authority route cases, invalid-kind parser-order proof, and non-bool authority proof. | Tests directly exercise the high-risk routing edge cases the reviewer reproduced. | T10c-T10g | Targeted `critical_authority` and `authority_kind_invalid` runs |
| `scripts/test-review-artifact-validator.py` | Added calibration authority, unsupported boolean, public fixture, and invalid-kind noise-regression tests. | Prevents authority gaps, unknown control values, and parse-order regressions in review records. | T11d-T11g | Full review-artifact validator suite |
| `tests/fixtures/review-artifacts/*calibration*` | Added valid and invalid critical-internal and irreversible-external calibration fixtures. | Public fixtures document defect classes and record shape without claiming to be the private measured corpus. | R16, R17, T11, T12 | Fixture-driven validator tests |
| `skills/code-review/SKILL.md`, `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/plan-review/SKILL.md` | Added independent review gate guidance, forbidden initial-packet guidance, failed-remediation condition, and manifest-only authoring-review rollout guidance. | The code-review pilot and workflow handoff needed user-facing stage guidance. | R5, R8d, R19, R20, T14, T15 | `python scripts/test-skill-validator.py -k review_independence_m3` |
| `scripts/review_independence_skill_phrases.py` and `scripts/test-skill-validator.py` | Centralized R5/R8d phrase expectations and added docs workflow assertions. | Avoids hand-listed skill assertions drifting from spec-required guidance. | CR4-F1, CR4-F2, T14 | Skill validator suite |
| `docs/workflows.md` | Added the independent automated `code-review` gate, clean handoff gates, and final holistic review precondition. | Contributor workflow guidance must reflect the new workflow-managed review boundary. | R18-R20, T14, T15 | `test_review_independence_m3_workflow_and_implement_route_automated_gate` |
| `docs/changes/.../behavior-preservation.md` | Records M4 and M5 preservation matrices, including manual/profile-off compatibility, no finding quota, sampling/cost visibility, and final holistic precondition. | Shows what behavior was preserved or strengthened across calibration and final proof milestones. | Behavior-preservation proof, T15, T20, CR7-F1 | Artifact lifecycle and review-artifact validation |
| Review records and `review-resolution.md` | Recorded proposal/spec/architecture/plan/code reviews, 12 material findings, dispositions, validation evidence, and final clean holistic review. | Formal review evidence is part of the workflow contract and must be durable before verify. | Formal review recording rules, R18, T19 | `validate-review-artifacts --mode structure` and `--mode closeout` |
| `docs/plans/...`, `docs/plan.md`, `change.yaml` | Kept active handoff state, milestone status, review status, changed files, and validation ledger synchronized. | The active plan owns current state; change metadata and index must not drift. | T19, CONSTITUTION plan-state rules | `validate-change-metadata`, `validate-artifact-lifecycle` |

## Tests Added Or Changed

| Test area | What it proves | Why this level is appropriate |
| --- | --- | --- |
| Lifecycle route tests | `critical-internal` requires L3/human authority, irreversible external action requires human authority, invalid authority kinds and non-bool authority satisfaction fail closed before downstream checks. | Routing semantics are owned by lifecycle helpers, so integration-style route tests exercise the orchestration boundary directly. |
| Review artifact validator tests | Calibration records reject missing/insufficient authority, unsupported authority kind, unsupported yes/no controls, and multiple invalid controls. | Review records are durable process evidence; fixture and parser tests prove accepted records are trustworthy. |
| Fixture tests | Valid critical-internal L3 and irreversible-human fixtures pass; missing authority, L3-only irreversible, and invalid-kind fixtures fail. | Fixtures preserve named edge cases as reviewable examples. |
| Skill validator tests | Canonical skills contain the pilot guidance, forbidden initial-packet items, failed-remediation condition, no finding quota, and direct/profile-off compatibility. | Skill text is user-facing behavior, so phrase-level assertions protect required guidance from drift. |
| Workflow doc assertion | `docs/workflows.md` names the independent gate, clean automated handoff gates, and final holistic review precondition. | Contributor guidance is an operational surface and needed direct proof after M5 edited it. |
| Adapter proof | Canonical skill changes build local generated skills and public adapter archives. | Architecture and plan require local skill proof plus public adapter archive proof; one does not subsume the other. |

## Validation Evidence Available Before Final Verify

The active plan and change metadata record the detailed command ledger. Key evidence available before final verify includes:

- `python scripts/test-review-artifact-validator.py` passed after M4 R2 review-resolution with 78 tests.
- `python scripts/test-artifact-lifecycle-validator.py` passed after M4 R2 review-resolution with 137 tests.
- `python scripts/test-skill-validator.py` passed after M5 with 237 tests.
- `python scripts/validate-skills.py` validated 23 skill files.
- `python scripts/test-build-skills.py` passed with 7 tests.
- `python scripts/build-skills.py --check` passed.
- `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` passed for Codex, Claude, and OpenCode adapter archives.
- `python scripts/select-validation.py --mode explicit --path <M5 changed paths>` selected the expected checks with no unclassified paths or broad-smoke requirement.
- `bash scripts/ci.sh --mode explicit --jobs 1 --timeout 300 --path <M5 changed paths>` passed all selected checks after M5.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed after code-review M5 R2 with 19 reviews, 12 findings, 19 log entries, and 12 resolution entries.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows` passed after code-review M5 R2 with the same counts.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed after code-review M5 R2.
- `git diff --check` passed, and whitespace scans over changed files returned no matches.

One earlier selected-CI attempt with a 120-second timeout timed out only on `selector.regression`; the direct selector test then passed, and the same selected CI command passed with a 300-second timeout.

## Review Resolution Summary

Material findings are closed in `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-resolution.md`.

Summary:

- Total material findings: 12.
- Dispositions: 12 accepted.
- Status: 12 resolved.
- Open findings: 0.
- Final code review: `code-review-m5-r2` returned `clean-with-notes` for the final holistic implementation diff.

Finding groups:

- `SR1-F1`: clarified stop semantics for routable `changes-requested`.
- `PR1-F1`: added adapter archive proof to plan validation.
- `CR1-F1` through `CR3-F1`: corrected review-gate evidence and native/derived outcome routing.
- `CR4-F1` and `CR4-F2`: completed skill guidance for `failed-remediation` and initial-packet exclusions.
- `CR5-F1` through `CR6-F1`: added critical-authority and calibration parser-order enforcement.
- `CR7-F1`: corrected behavior-preservation metadata scope for M5 evidence.

## Alternatives Rejected

These alternatives were explicitly considered and rejected in the proposal, plan, or review-resolution trail:

- Requiring at least one finding per review. Rejected because it creates noise and punishes genuinely clean work.
- Strengthening prompts only. Rejected because it does not prevent biased evidence packets or author-context leakage.
- Requiring a different model for every ordinary review. Rejected as the base rule because model diversity is not independence if the evidence packet is biased.
- Requiring human review for every automated clean outcome. Rejected as the default because it removes most automation value; retained for irreversible external authority.
- Creating a new `review-resolution` skill during M3. Rejected because no canonical skill exists and creating one would exceed the approved M3 scope.
- Hand-editing generated adapter output. Rejected by repository policy and architecture; adapter proof uses temporary archive generation and validation instead.

## Scope Control

The change preserved the approved non-goals:

- It does not require every review to produce a finding.
- It does not introduce a hosted review service, database, persistent external control plane, or network dependency.
- It does not make heterogeneous models mandatory for standard-risk automated reviews.
- It does not expose private chain-of-thought or private author reasoning in records.
- It does not migrate the entire review family to the full blind-first protocol in this first slice.
- It does not claim final `verify`, PR readiness, hosted CI status, or branch readiness.

## Risks And Follow-Ups

Remaining risks before PR handoff:

- Final `verify` has not run yet and may find stale lifecycle, metadata, validation, or documentation issues.
- The public calibration fixtures are examples of defect classes and record shapes, not the private measured seeded-defect corpus.
- The review-family rollout beyond the code-review pilot remains a follow-on slice.
- Sampling-rate adjustment policy depends on future observed disagreement data.

Current lifecycle state:

- All implementation milestones are closed.
- Required review-resolution loops are closed.
- Explain-change is now recorded.
- Next stage is `verify`.
