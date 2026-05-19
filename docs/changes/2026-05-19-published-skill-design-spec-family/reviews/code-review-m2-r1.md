# Code Review M2 R1: Published Skill Design Spec Family

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `6ce542b` / M2 validator and fixture support
Status: changes-requested

Reviewed artifact: 6ce542b
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: SF-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-published-skill-design-spec-family/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-05-19-published-skill-design-spec-family/review-log.md
- Review resolution: docs/changes/2026-05-19-published-skill-design-spec-family/review-resolution.md#code-review-m2-r1
- Open blockers: SF-M2-CR1
- Immediate next stage: review-resolution for M2
- No automatic downstream handoff: this isolated review does not start fixes.

## Scope

Reviewed implementation surface:

- commit `6ce542b` (`M2: validate published skill design spec-family checks`)
- `scripts/test-skill-validator.py`
- `docs/plans/2026-05-19-published-skill-design-spec-family.md`
- `docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml`
- `docs/plan.md`

Governing artifacts checked:

- `specs/skill-contract.md`, R29, R32-R33, R35, R36
- `specs/skill-contract.test.md`, T21 through T24
- `docs/plans/2026-05-19-published-skill-design-spec-family.md`, M2

## Diff Summary

M2 adds deterministic regression checks in `scripts/test-skill-validator.py`
for spec-family routing coverage, audit classifications, preservation scaffold,
parity scaffold, and baseline token evidence. It does not change production
validator logic because the M1 audit found no new deterministic validator gap
beyond evidence-file coverage.

## Findings

### SF-M2-CR1 - Current handoff summary routes M2 back to implementation

Finding ID: SF-M2-CR1
Severity: major

Location:

- `docs/plans/2026-05-19-published-skill-design-spec-family.md`, Current Handoff Summary

Evidence:

The M2 implementation commit records:

```text
Current milestone state: review-requested
Next stage: implement M2
```

The same plan later states that it is ready for `code-review` of M2, and
`docs/plan.md` says the current next stage is code-review for M2. The stale
handoff value in the active plan body is the workflow-owned current next-stage
field for planned initiatives.

Problem:

The active plan's Current Handoff Summary is internally inconsistent. While M2
is in `review-requested`, the current next stage must be code-review, not
implementation. Leaving the stale value in the workflow-owned field can route
the next actor back into implementation and undermines the state-sync rule that
the active plan owns current milestone handoff state.

Required outcome:

Update the active plan's Current Handoff Summary so M2's next stage is
`code-review for M2` while the milestone is `review-requested`, or otherwise
make the handoff fields internally consistent.

Safe resolution path:

- Update `Next stage` in the Current Handoff Summary to `code-review for M2`.
- Rerun change metadata, artifact lifecycle, whitespace, and selected CI checks
  for the touched lifecycle artifacts.
- Return M2 to code-review after recording the resolution.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M2 adds deterministic checks matching T22 and keeps production validator scope bounded. |
| Test coverage | pass | `scripts/test-skill-validator.py` now covers the spec-family routing, audit, preservation, parity, and token evidence fixtures. |
| Edge cases | pass | The tests explicitly avoid runtime model-selection claims and broad semantic scoring. |
| Error handling | pass | No runtime error path or validator failure behavior changed in production logic. |
| Architecture boundaries | pass | No adapter roots, generated public skill bodies, or production architecture surfaces changed. |
| Compatibility | pass | Canonical skill validation passed after M2, and no skill body was rewritten in this milestone. |
| Security/privacy | pass | No secrets, credentials, or sensitive runtime values were introduced. |
| Derived artifact currency | pass | M2 does not modify generated adapter output or generated public skill bodies. |
| Unrelated changes | pass | The diff is limited to M2 tests and lifecycle state/evidence updates. |
| Validation evidence | concern | M2 validation is credible, but the active plan handoff summary contains a stale next-stage value. |

## No-Finding Rationale

Not applicable. One material finding remains open.

## Handoff

M2 requires review-resolution for SF-M2-CR1 before rerun code-review.

Next stage: `review-resolution` for M2.

Do not claim final verification, branch readiness, PR readiness, or final
closeout from this review. M2 remains open and M3 remains unimplemented.
