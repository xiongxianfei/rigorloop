# Code Review M1 R1: Authoring Model Integration

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Review date: 2026-08-30
Target: implementation commit `c6e46c57` and workflow handoff commit `c6a48171`
Reviewed milestone: M1
Reviewed artifact: M1 authoring-model implementation at commit `c6e46c57`
Status: changes-requested
Review status: changes-requested
Material findings: RTD-M1-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/reviews/code-review-m1-r1.md`, `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-log.md`, and `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-resolution.md`
- Open blockers: RTD-M1-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RTD-M1-CR1
- Recording status: recorded
- Recording blocker: none for durable evidence; the lifecycle CLI has no operation that records a non-clean milestone review without closing the milestone
- Review record: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-log.md`
- Review resolution: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: RTD-M1-CR1
- Verify readiness: not-claimed

## Review inputs

- Exact implementation: commit `c6e46c57`
- Workflow handoff: commit `c6a48171`
- Approved Design package: `design-review-r2`
- Approved Delivery package: `delivery-review-r2`
- Stable plan milestone: M1 in `docs/plans/2026-08-30-lightweight-requirement-delivery-model.md`
- Test specification: RTD-T01 through RTD-T04 and M1 proof map in `specs/lightweight-requirement-delivery-model.test.md`
- Implementation evidence: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/evidence/m1-authoring-model.md`

## Actual-diff summary

M1 adds one canonical lightweight requirement-to-delivery reference, copies it into the proposal, specification, architecture, and plan skill packages, adds conditional resource-map entries and concise stage responsibilities, extends the existing packaged-reference allowlist where needed, and adds focused static tests. Existing artifact skeletons remain unchanged because they already carry requirement, architecture, dependency, and work fields without adding RR, IR, AR, or mandatory work-hierarchy entities.

## Finding RTD-M1-CR1

Finding ID: RTD-M1-CR1
Severity: major
Location: `templates/shared/requirement-to-delivery-model.md:24-26` and `scripts/test-skill-validator.py:8771-8790`
Evidence: RTD-AC4 requires a larger example that demonstrates optional many-to-many decomposition, the approved M1 plan requires “examples for a small change without empty hierarchy and a many-to-many SR/work allocation,” and RTD-T03/RTD-T04 name concrete many-to-many and proportional fixtures. The shipped reference only says the relationship “may be many-to-many” and gives a small-change sentence. The focused test asserts those phrases but never proves a concrete mapping such as one SR allocated to multiple work items and one work item realizing multiple SRs. Consequently all validation commands pass while the named M1 acceptance example is absent.
Required outcome: The canonical and four M1 packaged references must contain one concise, concrete many-to-many SR/work allocation example, and focused proof must fail if either direction of that example is lost while preserving optional hierarchy and existing artifact types.
Safe resolution path: Add a compact example to the canonical reference, copy it byte-for-byte to the four M1 consumers, extend `RequirementDeliveryModelM1Tests` to assert both mapping directions and the absence of mandatory hierarchy, then rerun CMD-001, CMD-002, CMD-003, and CMD-007 before independent M1 rereview.
needs-decision rationale: The implementation owner must record whether this bounded correction is accepted, rejected, deferred, or partially accepted; Code Review does not choose the disposition.

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The model, ownership, authority limits, and proportionality align, but RTD-AC4's larger many-to-many example is missing. |
| Test coverage | concern | The suite passes 364 tests, but RTD-T03/RTD-T04 are reduced to positive phrase checks and do not prove the named concrete example. |
| Edge cases | pass | Existing fields permit one-to-many, many-to-one, small-change omission, and explicit non-SR obligations without new entities. |
| Error handling | pass | M1 adds no runtime operation; missing mapped resources continue to fail existing structural validation. |
| Architecture boundaries | pass | One canonical source, skill-local copies, conditional loading, and stage-local authority match the approved design. |
| Compatibility | pass | Existing artifact skeletons and lifecycle behavior are unchanged; historical artifacts require no retrofit. |
| Security/privacy | pass | No secret, authorization, network, or private-data collection surface changed. |
| Derived artifact currency | pass for M1 | Canonical and four M1 copies are byte-identical and `build-skills.py --check` passes; all-consumer and adapter parity remain explicitly assigned to M3. |
| Unrelated changes | pass | The implementation commit is limited to the M1 authoring model, focused tests, allowlist adjustment, evidence, and lifecycle recording. |
| Validation evidence | concern | Every M1 command passes, but the commands cannot establish RTD-AC4 until the focused test asserts the concrete many-to-many example. |

## Validation rerun

- `python scripts/test-skill-validator.py` — passed, 364 tests.
- `python scripts/validate-skills.py skills/proposal/SKILL.md skills/spec/SKILL.md skills/architecture/SKILL.md skills/plan/SKILL.md` — passed for all four skills.
- `python scripts/build-skills.py --check` — passed using temporary output.
- `python scripts/validate-documentation-prose.py --mode audit --path templates/shared/requirement-to-delivery-model.md --path skills/proposal/SKILL.md --path skills/spec/SKILL.md --path skills/architecture/SKILL.md --path skills/plan/SKILL.md` — passed with zero errors and warnings.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-30-lightweight-requirement-delivery-model/change.yaml` — passed before review recording; after the open finding was recorded, it correctly reports that the unchanged lifecycle projection still says zero unresolved items.
- `git diff --check 251bea2d..c6a48171` — passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-30-lightweight-requirement-delivery-model` — passed after review recording with six reviews, four findings, six log entries, and four resolution entries.
- Lifecycle CLI dry run of `complete-milestone` with this review — correctly blocked with `RL_OPERATION_NOT_PERMITTED` because milestone completion requires a clean review; the CLI exposes no separate operation for projecting a non-clean milestone review.

## Direct-proof gap and residual risk

No runtime, retry, persistence, concurrency, security, or external-environment behavior is introduced by M1. The material residual risk is semantic: published guidance can claim many-to-many support without showing agents how both mapping directions look, while the static test continues to pass.

## Handoff

This independent review is review-only and creates no automatic downstream handoff. M1 remains `review-requested`; M2 must not start. Resolve RTD-M1-CR1 through the implementation owner, rerun the M1 proof, and perform a fresh independent Code Review over the corrected M1 implementation before workflow closes the milestone.
