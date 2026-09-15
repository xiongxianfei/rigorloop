# Risk-driven contract testing: scoped Design Review

## Result

- Skill: design-review.
- Review ID and round: risk-driven-test-design-review, round 1.
- Review status: approved.
- Package member: Validation, `docs/design/engineering/validation.md`, exact identity below.
- Upstream direction: user's explicit design-only testing refinement; no new proposal or lifecycle identity selected.
- Material findings and correction targets: none.
- Recording status: recorded, advisory-durable/manual.
- Open blockers: none for this Design assessment.
- Immediate next stage: isolated stop and return design-only result.
- Claim limitations: no suite audit, case deletion, implementation, Delivery allocation, final Verify or future implementation approval.

## Scope and independence

Author `/root` revised the Validation Design. Independent reviewer `/root/validation_design_review` did not author or edit that member and writes only this review. Assessment compares `/tmp/risk-driven-validation-design-before.md` with the final current Design, including the author's final distinction between observation descriptions and executor phases and preservation of validation-result caching prohibitions. Earlier tooling and test-refactor reviews retain their original subjects and judgments; none is retargeted to this amendment.

The selected amendment adds the risk-driven principle, TEST-SR-18, the detailed observation/fixture/oracle/failure/maintenance method, the overview link, representative scenario refinements and VAL-DEC-09 wording. Remaining Validation execution and retirement contracts are retained dependencies, not newly selected implementation. Packaging, Release and Assessment remain unchanged contract owners; their relevant artifact/public observation, independence and freshness obligations were inspected for compatibility.

## Assessment rationale

The Design is coherent: start with an owned required outcome and plausible defect, then choose a boundary capable of exposing the defect. Small fixtures and narrow rules are useful when they preserve the mechanism. Broader proof remains necessary for additional interactions, actual artifact identity and independently mandated operational observations. The four overlapping descriptions explain observation scope without introducing required testing layers, ratios, directories, catalog values or executor phase changes. VAL-DEC-09 preserves its identity and records the rationale and alternative to indiscriminate per-requirement automation.

Independent expected outcomes and counterexamples address tests that repeat the implementation's mistake. Shared setup is permitted without becoming a circular oracle. The archive and installer example separates independent rule vectors, actual generated-member inspection and packed-consumer proof. Controlled provider responses establish orchestration decisions only; they cannot establish public provider behavior. The uncertain-publication retry example retains the real orchestration boundary and forbids a duplicate immutable-version write. These give credible representative acceptance intent without prescribing an exhaustive case inventory.

Existing obligations remain effective. TEST-SR-15 allocates every affected requirement and material hazard even when no dedicated automated case is justified. TEST-SR-16 retains independent semantic instruction review, applicable human PR review and focused manual investigation of unresolved material uncertainty; no universal agent-compliance claim or semantic gate is introduced. TEST-SR-07–10 require established, assessed retained protection before consolidation/removal and preserve unknown protection. Runtime cost and inability to parallelize cannot justify weakening the claim. VAL-SR-01/02/17 still require owned mutable state, actual isolation assessment and bounded cleanup; ordered steps within one independent scenario remain legitimate. Fresh execution and validation-result cache prohibitions remain explicit.

No cross-owner amendment is required for this direction. Packaging's actual tarball/archive/installed-consumer acceptance remains mandatory. Release REL-SR-13–15 retains fresh public metadata and installed smoke, explicit unavailable/failure results, observation before retry and immutable publication safety. Assessment RC-SR-01–06/15 retains scoped nonauthor judgment, exact applicability and freshness overrides. The new method defers to these owners rather than replacing their concrete acceptance obligations with cheaper helper tests. Selector/scheduler limitations do not decide sufficiency.

## Review criteria

| Criterion | Outcome and evidence |
| --- | --- |
| Realization and feasibility | Pass: existing test runners, fixtures and specialist assessment support the method; no new engine is required. |
| Authority and compatibility | Pass: domain obligations, mandatory proof and scope-specific freshness remain effective. |
| No weakened approved goal | Pass: narrower proof is sufficient only for the claimed boundary; required broader observations survive. |
| Ownership and boundaries | Pass: behavior owners, Delivery, implementation and assessors retain distinct duties. |
| Decisions | Pass: VAL-DEC-09 remains the current decision with concrete rationale and alternatives. |
| Shared-contract coherence | Pass: Validation owns the reusable method and references existing domain acceptance owners. |
| Acceptance intent and assumptions | Pass: meaningful oracle, archive/installer and uncertain-publication examples expose distinct hazards; scenarios are not a whitelist. |
| Migration or displacement | Not applicable: no source, case, check or obligation is selected for retirement by this amendment. |
| Architecture views | Pass: Criteria owns the method and the overview links its detail. Existing Context, Building Block, Runtime and Deployment views remain adequate because no actor, execution component or trust boundary changes. |

Structural/prose/diff checks were reported passed by the author. This judgment rests on semantic inspection of the Design and retained contracts, not structural success. Selected Design validation was still pending at recording and is not claimed passed here. No automated test suite was audited or rerun by the reviewer, and no conclusion about current suite efficiency or adequacy is inferred from this Design approval.

## Exact subjects and reliance

The amended package has one member: Validation. Other listed subjects are relevant unchanged dependencies, not newly approved component changes. CLI subject inspection produced these identities after the final author clarifications; reviewer checked the current bytes still match before recording.

| Role | Subject | SHA-256 identity |
| --- | --- | --- |
| Amended package member | `docs/design/engineering/validation.md` | `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14` |
| Unchanged dependency | `docs/design/engineering/release.md` | `sha256:1cae90f16d152c7811eec499036dc4e7f8f63f82acd62d6b71c58f131d5f19b8` |
| Unchanged dependency | `docs/design/engineering/packaging.md` | `sha256:0aec3cfc2bf73424bf08d8c4efb775e4f7b5051b8417e8ebf1c90ada91aedbfa` |
| Unchanged dependency | `docs/design/skill/assessment.md` | `sha256:af968c5583c27abb95e9a2b2ac0293deba30c522e72480c6f9aa05066659ae19` |

Approval applies only to the exact Design amendment above. It supports the requested design-only result and does not authorize a follow-on audit, plan or implementation. No formal lifecycle state, branch readiness, hosted CI result or external action is asserted.
