# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: fresh isolated Codex code-review agent
Target: M2 implementation commit e96791be
Reviewed artifact: commit e96791be
Reviewed milestone: M2
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-28
Recording status: recorded
Recording blocker: none
Material findings: PBF-M2-CR1
Immediate next stage: review-resolution M2
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: M2 review manifest, detailed review, review log, review resolution, active plan, plan index, and change metadata
- Open blockers: PBF-M2-CR1
- Next stage: review-resolution M2
- Review status: changes-requested
- Material findings: PBF-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: PBF-M2-CR1
- Verify readiness: not-claimed

## Review inputs

- Diff surface: commit range `425cad4a..e96791be`.
- Tracked governing state: approved spec, test spec, ADR, active plan, and the M2 implementation commit.
- Governing clauses: PBF-R041 through PBF-R051, PBF-R059 through PBF-R064, and test cases T3, T6, T10, T16, and T17.
- Invocation evidence: `review-invocation-code-review-m2-r1.yaml`.

## Risk map

- Affected behavior: ten published lifecycle skills, packaged-reference validation, and semantic fixture proof.
- Highest-impact failures: responsibility compression, phrase-only semantic proof, an overbroad resource exception, generated drift, or proposal-stage inclusion.
- Expected evidence: a ten-skill property matrix, closed membership, structured lifecycle packets, stage outcomes and handoffs, negative resource rejection, and generated parity.
- Applicable risks: requirement fidelity, published compatibility, negative proof, generated currency, resource integrity, and test validity.
- Non-applicable risks: network APIs, credentials, concurrency, active activation, rollback, and release publication.

## Diff summary

All ten governed skills map the shared reference and contain the required
stage responsibility and stop guidance. The validator admits the exact
projected reference for the closed governed set. The new semantic fixture and
test, however, model expected prose rather than semantic lifecycle behavior.

## Finding PBF-M2-CR1

Finding ID: PBF-M2-CR1
Severity: major
Location: `scripts/test-skill-validator.py:7697`; `scripts/fixtures/boundary-first/semantic/review-cases.json:1`
Evidence: The fixture contains only an owner, required substring, and forbidden sentence. The test checks text presence and absence, but supplies no structurally valid record or lifecycle packet, expected outcome, or handoff. It allows at least seven cases and omits `plan`, so passing CMD4 cannot support T10 or T16.
Required outcome: Provide direct stage-specific proof for all ten governed skills using structured boundary/proof records or lifecycle packets with expected semantic owner, stop or review outcome, and handoff.
Safe resolution path: Extend the semantic fixture with exact ten-skill packets, structured inputs, expected outcomes and handoffs; require closed coverage and add a negative mutation proving phrase-only data fails. Keep semantic judgment out of `skill_validation.py`; do not change the governing spec, ADR, canonical reference, activation, or M3/M4 surfaces. Rerun CMD3, CMD4, CMD5, and focused lifecycle tests.
needs-decision rationale: none
auto_fix_class: declared-safe

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Skill prose aligns, but the required semantic proof is compressed. |
| Test coverage | block | T10 and T16 behavior is not directly exercised. |
| Edge cases | block | Named gaps exist only as string expectations. |
| Error handling | pass | The resource exception is closed to the governed set and exact path. |
| Architecture boundaries | pass | Canonical projection and stage-local policy remain separated. |
| Compatibility | concern | Published behavior lacks direct semantic regression proof. |
| Security/privacy | pass | No secret, network, credential, or private-data surface is added. |
| Derived artifact currency | pass | Canonical projections and generated output were checked for M2. |
| Unrelated changes | pass | The commit is scoped to M2 and lifecycle evidence. |
| Validation evidence | concern | Commands pass, but the focused test proves text shape rather than semantic behavior. |

## Requirement-fidelity receipt

The literal `READ` mapping, PBF-R043 responsibility, and applicable PBF-R064
guidance pass on all ten skill surfaces. Proposal stages remain excluded and
the shared method remains stage-neutral. Direct semantic fixture and handoff
proof is missing for all ten stages, with no fixture at all for `plan`.

## Validation evidence challenged

The independent reviewer ran the canonical skill validator, all 261
skill-validator tests, generated build checking, the two focused tests, and a
scoped diff check from a clean archive of `e96791be`; all passed. These
commands prove structure, mapping, byte equality, and generated build parity,
but not the T10/T16 semantic behavior claim.

## Second-review evidence

- Second reviewer: isolated fresh M2 code-review agent.
- Second-review result: changes-requested.
- Reconciliation: PBF-M2-CR1 independently confirmed with the same scope, severity, evidence, and declared-safe correction; no additional material finding.
- Independent checks: focused lifecycle tests, all skill-validator tests, skill validation, generated build check, scoped diff check, fixture inventory, and validator-exception containment all passed.
- Confidence: high.

## Milestone handoff

- Reviewed milestone: M2
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M2, M3, M4
- Next stage: review-resolution M2
- Final closeout readiness: not ready; PBF-M2-CR1 and later milestones remain open.
