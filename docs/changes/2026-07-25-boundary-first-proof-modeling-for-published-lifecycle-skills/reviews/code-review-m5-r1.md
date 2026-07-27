# Code Review M5 R1

Review ID: code-review-m5-r1

Stage: code-review

Round: 1

Reviewer: Codex code-review skill

Target: M5 correction through `c6253bb1`

Reviewed artifact: implementation diff `f5136d14..c6253bb1`

Reviewed milestone: M5

Status: approved

Review status: clean-with-notes

Material findings: None

Immediate next stage: final holistic code review

Milestone closeout: closed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: clean-with-notes

Review gate outcome: advance

Independence level: L1

Author context ID: boundary-m5-implementation

Reviewer context ID: boundary-m5-review-r1-reset

Context separation mechanism: blind-first inspection of the matcher, registry,
changed-path behavior, and negative tests before accepting validation summaries

Risk tier: elevated

Risk-tier triggers: validation selection, fail-closed evidence registration,
actual PR-range routing, and lifecycle handoff state

Risk-tier classifier: validation, fail-closed routing, lifecycle, and requirement-fidelity triggers

Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md` CRM-R1-R19; `specs/rigorloop-workflow.md` R28p; `docs/plans/2026-07-25-boundary-first-proof-modeling.md` M5

Formal criteria: bounded root and pattern registration, exactly-one matching, fail-closed unknown and ambiguous handling, declared semantic routes, selector regression, actual changed-path proof, and synchronized lifecycle handoff

Initial packet inventory: specs/change-record-catalog-registration-and-bounded-read-model.md@c6253bb1#sha256:ec49d110c272ae5b7dfd189724dd0ee37cfcd35e490ba7badb041dee29711601; specs/rigorloop-workflow.md@c6253bb1#sha256:c339ceed9592ec069cb94efd4774ad60ab9829983320fab1a3f22ea128e06ced; scripts/validation_selection.py@c6253bb1#sha256:c8de622a5111d196b9e7c6ea3b4e6fa76917012638d03eabc80595c0a94e60f1; scripts/test-select-validation.py@c6253bb1#sha256:6570d79b9a58ef25e2ee65375bb0747e3c77c79886ca64d3ef0edb7331156e0e; docs/plans/2026-07-25-boundary-first-proof-modeling.md@c6253bb1#sha256:ba171ac753534a5c145c6e8944f5e3865aeadaaaf597376ce9156701b7a76a86; validation-m5.md@c6253bb1#sha256:fc9df9d7ad160f05423b1f8ae864b384a0203c9a6346c89abd8363f7f4db168d

Prompt template version: code-review-template-v1

Initial packet hash: sha256:a1ae23f26996809b0f4ef4f7a0ca222cef1081b11972de113121a895a909d1ca

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: evidence-class root validation, complete-path matching,
nested evidence classification, selected-check routing, registration debt,
and active-plan handoff.

Highest-impact failure modes: a broad pattern silently accepting unrelated
evidence; a nested path bypassing registration; one change's registration
capturing another change; an ambiguous match being treated as valid; or
fixture-only proof replacing the branch's actual changed-path proof.

Changed boundaries: filename matching versus full repository-path matching;
generic change-root registration versus exact initiative-root registration;
supplemental fixtures versus PR-range evidence.

Evidence expected: safe-root rejection, immediate-versus-descendant pattern
contrasts, unknown-sibling rejection, cross-change isolation, complete tracked
inventory routing, preserved existing routes, and actual
`origin/main..HEAD` selection.

Areas requiring direct inspection: `CHANGE_EVIDENCE_CLASSES`,
`validate_evidence_class_registry`, `_path_category`,
`_matching_evidence_classes`, root-relative matching helpers, selector tests,
M5 validation evidence, and plan/index state.

Areas intentionally out of scope: boundary-model behavior, runtime generation,
skill text, adapter generation, release activation, publication, deployment,
and PR creation.

Risk classes considered: validation=applicable; requirement-fidelity=applicable; lifecycle=applicable; generated-evidence=applicable only to routing; authorization=not-applicable; security/privacy=not-applicable beyond repository-relative path containment

Falsifiable review questions: Can a path outside the registered root match only because its basename matches?

- Can a path outside the registered root match only because its basename
  matches?
- Can `*.json` recurse below its registered root without an explicit
  descendant pattern?
- Can another change inherit this initiative's semantic routes?
- Does the branch's actual PR range still contain registration debt?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, plan body, plan index, and change metadata
- Open blockers: none at the M5 milestone gate
- Next stage: final holistic code review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `reviews/code-review-m5-r1.md`
- Review log: `review-log.md`
- Review resolution: not-required
- Reviewed milestone: M5
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Diff summary

The correction makes `allowed_root` operational instead of descriptive.
Registered evidence is matched relative to a safe change-local root; immediate
patterns remain immediate, slash-bearing patterns may describe descendants,
and the boundary evidence families are registered only under this initiative's
exact dated root. The plan records the verification-discovered correction as
M5 and synchronizes the plan index.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The central registry retains stable IDs, roots, bounded patterns, routes, validators, lifecycle stages, and conditions. Unknown and ambiguous evidence still fail closed under CRM-R1-R19. |
| Test coverage | pass | Eight focused contrasts cover safe and unsafe roots, representative families, unknown siblings, cross-change isolation, the tracked inventory, and route preservation; the complete 142-test selector suite passes. |
| Edge cases | pass | Missing roots, traversal, non-change roots, absent trailing slash, descendants without descendant patterns, unknown families, cross-change paths, and ambiguous matches are rejected or blocked. |
| Error handling | pass | Unsupported paths continue to emit `manual-routing-required`; ambiguous matches remain blocking; invalid registry entries produce explicit validation errors. |
| Architecture boundaries | pass | The centralized selector registry remains the sole routing surface; semantic checks are reused rather than duplicated in evidence handling. |
| Compatibility | pass | Existing root-level evidence calls retain basename compatibility, and the preservation-surface selector test remains green. |
| Security/privacy | pass | Matching is repository-relative and root-bounded; no runtime evidence content or secret material is read by the selector. |
| Derived artifact currency | concern | The capability report must be regenerated once after review metadata settles; this is an owned post-review step, not a code defect. |
| Unrelated changes | pass | The diff is limited to selector routing, its direct tests, M5 evidence, and required lifecycle synchronization. |
| Validation evidence | pass | Selector regression passes 142 tests, lifecycle and metadata validation pass, and PR selection at `c015ff96` reports `ok`, no blockers, no registration debt, and no broad-smoke trigger. |

## Requirement-fidelity receipt

Applicability: applicable.

CRM-R1-R19 were decomposed into registry field closure, safe and bounded
matching, exactly-one classification, fail-closed unknown and ambiguous
handling, declared route selection, governing change context, registry
regression, actual changed-path proof, and registration-debt closure. The
implementation and tests directly cover each property affected by M5.
Supplemental fixtures do not replace the recorded PR-range selector result.

## Clean-review sufficiency receipt

Review target identity: `c6253bb1c2d6ce43229cd6bb58903370937c09b3`

Independence level: L1 tracked-artifact context reset.

Governing artifacts inspected: CRM-R1-R19, R28p, M5, the selector registry and
matcher diff, focused tests, full selector result, actual PR-range result,
validation-m5, and plan/index state.

Adversarial hypotheses tested: basename escape, descendant overmatch,
cross-change capture, unknown-family acceptance, ambiguous matching, unsafe
root acceptance, incomplete tracked inventory, and fixture-only proof.

Direct proofs performed: inspected the full changed matcher and registrations;
ran focused contrast tests; ran the complete selector regression; and selected
the actual `origin/main..c015ff96` PR range.

Validation evidence challenged: the clean conclusion relies on both negative
fixtures and actual changed-path proof. Unaffected boundary, skill, adapter,
preservation, and release suites were not treated as proof of the changed
matcher and were intentionally reused only outside this review surface.

Risk classes considered: validation, requirement fidelity, lifecycle state,
generated-evidence routing, path containment, compatibility, and
security/privacy.

Unreviewed surfaces: no external CI, publication, deployment, release
activation, or PR operation was performed.

Confidence: high for M5 milestone closure.

No-finding rationale: full-path matching is bounded by an exact or safely
templated root, descendants require explicit patterns, every current evidence
path routes exactly once, adversarial siblings remain blocked, and the actual
PR range closes the verification-discovered registration debt without
widening broad-smoke or lifecycle authority.

## Handoff

M5 may close. Because final holistic review R2 predates M5, the next stage is a
new final holistic code review. The M5 correction also makes the prior
explanation stale; `explain-change` follows only after that final review.
