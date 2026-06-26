# Independent Test-Spec-Review Gate Review Resolution

## Scope

This record tracks material findings for the independent test-spec-review gate change after the isolated M2 re-review.

Closeout status: open

Review closeout: code-review-r4
Review closeout: proposal-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: architecture-review-r1
Review closeout: spec-review-r1
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3

- Reviews covered: `proposal-review-r1`, `plan-review-r1`, `plan-review-r2`, `architecture-review-r1`, `spec-review-r1`, `code-review-r1`, `code-review-r2`, `code-review-r3`, `code-review-r4`
- Findings resolved: 0
- Unresolved findings: 1
- Current result: `code-review-r4` found that M2 does not fully carry the spec requirement that implementation eligibility depends on recorded, approved, current `test-spec-review` evidence.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CR4-F1 | needs-decision | open | Needs owner disposition before implementation can fix and re-review the M2 skill wording. |

## Finding Details

### code-review-r4

#### CR4-F1 - Implement skill omits recorded test-spec-review evidence from eligibility wording

Finding ID: CR4-F1
Disposition: needs-decision
Decision owner: maintainer
Decision needed: Decide whether to accept the M2 wording fix as in-scope for this PR or defer it to a follow-up with explicit owner authorization.
Status: open
Owner: maintainers
Owning stage: review-resolution
Chosen action: pending
Rationale: `specs/test-spec-review-gate.md` R26 requires the `implement` skill to require active test spec plus approved, current, recorded `test-spec-review` evidence before implementation eligibility. The M2 implementation added approved/current wording but omitted recorded evidence in the implementation skill and its focused validator assertion.
Required outcome: Update `skills/implement/SKILL.md` and `scripts/test-skill-validator.py` so formal workflow-managed implementation eligibility explicitly requires recorded, approved, current `test-spec-review` evidence.
Safe resolution path: Add `recorded` to the relevant `implement` skill eligibility/input/default-evidence/stop-condition wording; update the focused skill-validator assertion; run targeted and full skill validation; rerun code-review for the fix.
Validation target: `python scripts/test-skill-validator.py -k test_test_spec_review_canonical_skill_assets_and_adjacent_routing`; `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.
Validation evidence: pending

### proposal-review-r1

No material findings; no resolution entry required.

### plan-review-r1

No material findings; no resolution entry required.

### plan-review-r2

No material findings; no resolution entry required.

### architecture-review-r1

No material findings; no resolution entry required.

### spec-review-r1

No material findings; no resolution entry required.

### code-review-r1

No material findings; no resolution entry required.

### code-review-r2

No material findings; no resolution entry required.

### code-review-r3

No material findings; no resolution entry required.
