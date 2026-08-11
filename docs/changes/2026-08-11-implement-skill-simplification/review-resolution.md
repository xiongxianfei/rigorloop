# Review Resolution: Implement Skill Simplification

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: proposal-review-r4
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: test-spec-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `proposal-review-r4`, `spec-review-r1`, `plan-review-r1`, `plan-review-r2`, `test-spec-review-r1`, `code-review-m1-r1`, `code-review-m2-r1`, `code-review-m2-r2`
- Findings resolved: 7
- Unresolved findings: 0
- Current result: code-review M2 R1 findings were corrected and are ready for independent rereview.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| IMPSIM-PR1 | accepted | resolved | The proposal defines isolated, planned, and armed profiles with profile-specific loaded-context evidence and success interpretation. |
| IMPSIM-PR2 | accepted | resolved | The proposal selects distinct planned-milestone and automated-review/correction references with separate triggers. |
| IMPSIM-PR3 | accepted | resolved | Armed automation is valid only within the same current planned milestone and requires durable identity-bound evidence. |
| IMPSIM-PR4 | accepted | resolved | The result asset uses one core and two omitted-when-inapplicable conditional groups without owning policy. |
| IMPSIM-PR5 | accepted | resolved | Semantic rules and literal dependencies use separate ledgers, closed vocabularies, and preservation treatments. |

## Finding Details

### proposal-review-r1

#### IMPSIM-PR1

Finding ID: IMPSIM-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Choose the required optimization profiles and their loaded-context success evidence.
Chosen action: Define `IP0-isolated`, `IP1-planned`, and `IP2-armed`; record loaded resources and deterministic before/after context for each; require material improvement for isolated and planned profiles and justified non-regression for the armed profile.
Rationale: Static `SKILL.md` reduction does not establish reduced loaded context for planned or armed implementation journeys.
Safe resolution path: Define isolated, planned, and armed profiles; record exact before/after loaded resources and context for each; name which profiles must materially improve.
Validation target: proposal-review-r2
Validation evidence: Proposal revision completed; focused artifact validation passed; proposal-review R2 approved the revision.
Implementation evidence: not applicable at proposal stage

#### IMPSIM-PR2

Finding ID: IMPSIM-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Choose one combined conditional reference or separate planned-milestone and automation-only references.
Chosen action: Use `references/planned-milestone-implementation.md` for ordinary workflow-managed milestone procedure and `references/automated-review-correction.md` only for formally armed automated review or correction.
Rationale: One reference currently makes ordinary planned milestones load automation-only review and correction procedure.
Safe resolution path: Prefer separate planned-milestone and armed-automation references, or record evidence that the single-reference coupling is necessary; update exact triggers and package rationale.
Validation target: proposal-review-r2
Validation evidence: Proposal revision completed; focused artifact validation passed; proposal-review R2 approved the revision.
Implementation evidence: not applicable at proposal stage

### proposal-review-r2

Review closeout: proposal-review-r2

No material findings.

### spec-review-r1

Review closeout: spec-review-r1

No material findings.

### proposal-review-r3

Review closeout: proposal-review-r3

#### IMPSIM-PR3

Finding ID: IMPSIM-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Choose the valid invocation profiles and authoritative trigger evidence.
Chosen action: Support only `IP0-isolated`, `IP1-planned`, and `IP2-planned-armed`; require current matching plan, milestone, and automation evidence; stop on unplanned armed automation or missing, stale, mismatched, or ambiguous authority.
Rationale: The current automation trigger appears independent even though the armed profile loads planned procedure.
Safe resolution path: Make armed automation valid only within a current planned milestone and stop on missing, stale, mismatched, or ambiguous authority.
Validation target: proposal-review-r4
Validation evidence: Proposal revision completed; focused artifact validation passed; proposal-review R4 approved the revision.
Implementation evidence: not applicable at proposal stage

#### IMPSIM-PR4

Finding ID: IMPSIM-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Choose the profile-applicability model for the single result asset.
Chosen action: Use one core group for every profile, one planned group for `IP1-planned` and `IP2-planned-armed`, and one automation group only for `IP2-planned-armed`; omit inapplicable groups and keep policy outside the asset.
Rationale: One undifferentiated result shape cannot represent all profiles without placeholders or policy leakage.
Safe resolution path: Define one core group plus planned and automation conditional groups; omit inapplicable groups and keep policy outside the asset.
Validation target: proposal-review-r4
Validation evidence: Proposal revision completed; focused artifact validation passed; proposal-review R4 approved the revision.
Implementation evidence: not applicable at proposal stage

#### IMPSIM-PR5

Finding ID: IMPSIM-PR5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Choose separate preservation contracts for semantic rules and literal dependencies.
Chosen action: Create separate semantic-rule and literal-compatibility ledgers with closed dispositions and classifications; preserve contract literals, migrate parser contracts atomically, update incidental tests, and remove obsolete literals with evidence.
Rationale: Incidental test wording must not become a permanent public contract.
Safe resolution path: Use separate change-local ledgers with closed semantic dispositions and literal classifications.
Validation target: proposal-review-r4
Validation evidence: Proposal revision completed; focused artifact validation passed; proposal-review R4 approved the revision.
Implementation evidence: not applicable at proposal stage

### proposal-review-r4

Review closeout: proposal-review-r4

No material findings.

### plan-review-r1

Review closeout: plan-review-r1

No material findings.

### plan-review-r2

Review closeout: plan-review-r2

No material findings.

### test-spec-review-r1

Review closeout: test-spec-review-r1

No material findings.

### code-review-m1-r1

Review closeout: code-review-m1-r1

No material findings.

### code-review-m2-r1

#### IMPSIM-CR1

Finding ID: IMPSIM-CR1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implement
Chosen action: Remove the two trailing-whitespace defects and rerun `git diff --check`.
Rationale: Required reviewability proof must agree with the committed diff.
Validation target: `git diff --check cd2b2dae..HEAD`
Validation evidence: `git diff --check` passed after correction.
Implementation evidence: removed trailing whitespace from the two named evidence lines and from the review record without changing prose semantics.

#### IMPSIM-CR2

Finding ID: IMPSIM-CR2
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implement
Chosen action: Restore the unrelated code-review heading assertion and rerun the full skill-validator suite.
Rationale: M2 must not modify tests for the already-settled code-review package.
Validation target: `python scripts/test-skill-validator.py`
Validation evidence: `python scripts/test-skill-validator.py` passed 291 tests with 16 skips.
Implementation evidence: restored `## Boundary-first bridge` only in the pre-existing code-review package assertion; retained the implement package's `## Boundary-first method` assertion.

### code-review-m2-r2

Review closeout: code-review-m2-r2

No material findings.
