# Usability-First Boundary-First v0.4.0 Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex independent blind-first code-review peer
Target: d215c045..f6557066
Reviewed artifact: M1 usability semantic fixture and validator proof at commit f6557066
Reviewed milestone: M1
Review date: 2026-08-06
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-implementation
Reviewer context ID: m1-r1-independent-blind-first
Context separation mechanism: separate-agent-blind-first
Risk tier: medium
Risk-tier triggers: published-skill-semantics; ten-consumer-composition; stage-ownership; semantic-proof-fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: specs/usability-first-boundary-release.md; specs/usability-first-boundary-release.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md; docs/plans/2026-08-06-usability-first-boundary-release.md; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/usability-first-boundary-release.md@f6557066#sha256:1507c4f1a38fb01da5bace5a7c4e5f83fdd9468ed3355775444bb624c7ee6160; specs/usability-first-boundary-release.test.md@f6557066#sha256:2bbaf2f118928af45e46442e84753f23f92d00ceca99c40b1bd851ee9a6c19db; docs/architecture/system/architecture.md@f6557066#sha256:0495a510b37cdc2535390cebb25e0f5dbbfb093ae031853f48425e22ea53c1c2; docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md@f6557066#sha256:dcdecc94c62a4d55e108711b466976c2309cb6bf4cfc866110461e9c44d82cdf; docs/plans/2026-08-06-usability-first-boundary-release.md@f6557066#sha256:20dfdffbe57586be33ed111dad8b10e44d431e29a6af49caf4c1be097ddc90cd; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@f6557066#sha256:6cee88cd96627ee65d2f9b4e9b7dee158ca4fa743cff3530d0501cec79b7968d; range:d215c045..f6557066.diff@f6557066#sha256:7e67ea3e42e358adf140bfb9ea761fcf56a8947dccbe312844b2b1c4ede03872
Prompt template version: code-review-v1
Initial packet hash: sha256:7e67ea3e42e358adf140bfb9ea761fcf56a8947dccbe312844b2b1c4ede03872
Manifest owner: code-review
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: automatic concise boundary selection semantics; stage-owned artifact behavior; semantic journey proof; ten-skill generated-resource coherence
Highest-impact failure modes: self-fulfilling fixture proves only its own algorithm; tests bypass shipped skill text; a governed skill omits automatic behavior; deeper triggers expand unrelated scope; ordinary work becomes exhaustive; informal work creates formal artifacts; generated consumers diverge
Changed boundaries: BND-INPUT-001; BND-COMPOSE-001; INT-001
Evidence expected: direct semantic proof for ordinary, no-boundary, contract, risk, and explicit-depth cases; all ten canonical consumers; stage-ownership checks; mapped-resource and generated-output parity; negative closed-vocabulary fixtures
Areas requiring direct inspection: fixture authority; semantic selection helper; assertions against shipped skill content; ten-skill inventory; compact shared scan; owner-scoped resources; generated projection checks
Areas intentionally out of scope: M2 activation and custom-path retirement; M3 release payload; M4 active snapshot; public release actions; final verification
Risk classes considered: requirement-fidelity=applicable; semantic-proof-fidelity=applicable; composition-bypass=applicable; stage-ownership=applicable; compatibility=applicable; generated-parity=applicable; checked-revision-activation=not-applicable:out-of-scope-M2; public-release-mutation=not-applicable:out-of-scope-M3; registry-availability=not-applicable:out-of-scope-M3
Falsifiable review questions: Do tests exercise the actual ten governed skill instructions rather than only a fixture-owned selector? Can expected fixture output be changed together with candidate flags while tests still pass? Do ordinary and no-boundary cases avoid invented output while all three deeper triggers expand only one owned material topic? Do formal and informal journeys preserve stage-owned artifact behavior? Do canonical, mapped, and generated consumers remain coherent across every governed skill?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-m1-r1.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/fixtures/boundary-first/semantic/usability-cases.json; scripts/test-skill-validator.py
Requirement-fidelity matched path triggers: scripts/*validator*
Requirement-fidelity matched category triggers: spec-derived validators; multi-surface public skill guidance
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: finding IDs UBR-M1-CR1-001 and UBR-M1-CR1-002
Requirement-fidelity no-finding rationale: not applicable; material finding recorded.
Material findings: UBR-M1-CR1-001, UBR-M1-CR1-002
Immediate next stage: review-resolution
Automatic downstream handoff: none
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: review invocation, detailed review record, review log, and review resolution
- Open blockers: UBR-M1-CR1-001, UBR-M1-CR1-002
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: UBR-M1-CR1-001, UBR-M1-CR1-002
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md#code-review-m1-r1`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: UBR-M1-CR1-001, UBR-M1-CR1-002
- Verify readiness: not-claimed

## Review inputs

- Immutable implementation range: `d215c045..f6557066`
- Governing spec: `specs/usability-first-boundary-release.md`
- Governing test spec: `specs/usability-first-boundary-release.test.md`
- Governing architecture: `docs/architecture/system/architecture.md`
- Governing ADR: `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`
- Approved plan: `docs/plans/2026-08-06-usability-first-boundary-release.md`
- Owning change record: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
- Implementation evidence, released only after the blind-first risk map: `docs/changes/2026-08-06-usability-first-boundary-release/evidence/implementation-m1.md`

## Diff summary

The M1 slice adds one 11-case usability semantic fixture and three validator tests, records implementation evidence, and routes M1 to code review. It intentionally leaves the already-present shared compact scan and its ten canonical skill copies unchanged. M2 through M4 implementation and final verification are outside this review.

## Finding UBR-M1-CR1-001

Finding ID: UBR-M1-CR1-001
Severity: major
Location: `scripts/test-skill-validator.py:8235-8337`, `scripts/test-skill-validator.py:8351-8409`, and `scripts/fixtures/boundary-first/semantic/usability-cases.json:1-163`
Evidence: The fixture supplies candidate ownership, governing consequences, observed interfaces, stage, formal artifact, and `expected_selected`; the test helper derives output from those same fixture-owned flags and compares it back to `expected_selected`. Stable case IDs do not bind the approved E1-E3 stage or semantic inclusions/exclusions. Independent mutations removed E1's required `compatibility` topic and changed its expected selection, admitted the expressly irrelevant `release-tag` topic by flipping fixture flags and expected selection, and changed E1 from `spec`/`boundary-record` to `test-spec`/`proof-map`; `usability_fixture_errors()` returned an empty list for all three. The green suite therefore proves internal fixture consistency, not the approved journey oracle required by T1-T4, UBR-R001 through UBR-R005, UBR-R018, BND-INPUT-001, and INT-001.
Required outcome: Bind every required usability case ID to an independent contract-owned stage, formal-artifact outcome, required material topics, forbidden expansions, and depth relation so deleting a required topic, admitting an excluded topic, or moving a journey to another stage fails the test. The proof must continue to avoid exact prose, word-count, bullet-count, or method-name assertions.
Safe resolution path: Add an immutable expected-semantics mapping in test code or an independently validated contract fixture, assert E1-E3 required and forbidden topic sets plus stage/artifact ownership directly, and add negative mutations for required-topic deletion, forbidden-topic admission, stage reassignment, and coordinated candidate/expected edits. Retain the existing ten-skill compact-scan, resource, and generated-parity checks.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding UBR-M1-CR1-002

Finding ID: UBR-M1-CR1-002
Severity: major
Location: `scripts/test-skill-validator.py:8285-8291` and `scripts/test-skill-validator.py:8395-8404`
Evidence: Closed-vocabulary membership is attempted before the three case fields are proved to be strings. Mutating `stage`, `depth_trigger`, or `formal_artifact` to an array raises `TypeError: unhashable type: 'list'` instead of returning a bounded validation error. Existing regressions cover unknown strings only.
Required outcome: Validate the type of every closed-vocabulary field before membership or dependent semantic evaluation, return an explicit validation error for malformed JSON values, and add non-string regressions for stage, trigger, and artifact fields.
Safe resolution path: Add `isinstance(value, str)` guards, avoid dependent evaluation for malformed rows, and extend the mutation matrix without changing the fixture's public semantics.
needs-decision rationale: none
auto_fix_class: mechanical

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The selected fixture currently matches E1-E3, but its oracle can be rewritten without detection. |
| Test coverage | block | T1-T4 semantic outcomes are not independently anchored to the approved contract. |
| Edge cases | concern | Ordinary, no-boundary, contract, risk, and explicit cases exist, but coordinated semantic drift passes. |
| Error handling | block | UBR-M1-CR1-002 shows malformed closed-vocabulary value types can escape as `TypeError`. |
| Architecture boundaries | pass | No runtime checker, new stage, or generated behavior mechanism was introduced. |
| Compatibility | pass | Existing compact scan, ten canonical skills, resources, and projections remain unchanged. |
| Security/privacy | pass | M1 adds repository-local semantic metadata and emits no private runtime data. |
| Derived artifact currency | pass | Canonical skill validation, generated build check, and checked-revision boundary validation passed. |
| Unrelated changes | pass | The range is limited to M1 fixture/tests, evidence, and workflow routing. |
| Validation evidence | concern | All named commands pass, but passing CMD01 cannot establish requirement fidelity while its semantic oracle is self-authored. |

## Validation evidence

- `python scripts/test-skill-validator.py` passed 285 tests with 16 skipped.
- `python scripts/test-boundary-first-reference.py` passed 28 tests.
- `python scripts/validate-skills.py` passed for 24 skill files.
- `python scripts/build-skills.py --check` passed.
- `python scripts/validate-boundary-first.py --check` passed for the pending snapshot.
- `git diff --check d215c045..f6557066` passed.
- Independent semantic and malformed-type mutations reproduced UBR-M1-CR1-001 and UBR-M1-CR1-002.

## Handoff

M1 does not close. The isolated next stage is `review-resolution` for UBR-M1-CR1-001 and UBR-M1-CR1-002, followed by an M1 correction and independent rereview. No automatic downstream handoff occurs, no owner decision is needed, and M2-M4 remain out of scope and must not begin from this review result.
