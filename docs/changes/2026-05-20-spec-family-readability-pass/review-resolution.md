# Review Resolution: Spec-Family Readability Pass

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `plan-review-r1`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`
- Findings resolved: 5
- Unresolved findings: 1
- Final result: proposal-review requested changes in R1 for dependency-baseline proof, section-ordering boundary, enum authority, behavior-parity proof, and produced-artifact readability scope. The proposal was revised to add those controls before downstream plan reliance. Proposal-review R2 approved the proposal with no material findings. Spec-review R1 approved the focused spec with no material findings. Plan-review R1 approved the execution plan with no material findings. Code-review M1 R1 requested changes for a validation fixture coverage regression; the fixture was corrected and M1 returned to code-review. Code-review M2 R1 requested changes for a presentation-only preservation issue in the `spec-review` review-dimension table.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SFRP-PR1 | accepted | resolved | Added a normalized baseline gate requiring the plan to confirm the post-normalization `test-spec` baseline before readability edits. |
| SFRP-PR2 | accepted | resolved | Added a section-ordering boundary that treats family ordering as a readability convention, not a behavior override. |
| SFRP-PR3 | accepted | resolved | Added an enum authority map requirement and duplicate-handling acceptance criteria. |
| SFRP-PR4 | accepted | resolved | Added a mandatory content-preservation proof matrix and clarified that representative behavior parity supplements it. |
| SFRP-PR5 | accepted | resolved | Reclassified produced-artifact readability as deferred follow-up and kept this proposal scoped to published skill readability. |
| SFRP-M1-CR1 | accepted | resolved | Preserved exact settlement-result value coverage for unaffected first-slice skills while allowing `spec` to use the new enum-authority shape. |
| SFRP-M2-CR1 | accepted | open | The `spec-review` review-dimension table adds review-focus examples that are not source-preserving tabulation of the baseline dimension list. |

## Resolution Entries

### proposal-review-r1

#### SFRP-PR1 - Dependency baseline needs durable proof, not only PR status

Finding ID: SFRP-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Normalized baseline gate` requiring the plan to confirm `test-spec` front matter, Workflow role, surfaced stop conditions, fenced output skeleton, and closed or accepted normalization behavior-preservation evidence.
Rationale: Downstream reviewers need a concrete baseline gate for the predecessor dependency, not only a PR number.
Validation target: Proposal contains a checklist that blocks readability implementation if the normalized baseline is absent.
Validation evidence: Pending validation after proposal revision.

#### SFRP-PR2 - Section-ordering alignment needs a safe boundary

Finding ID: SFRP-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Section-ordering boundary` defining allowable alignment surfaces and requiring stop conditions, must-not-claim boundaries, and validation obligations to remain visible before normal output procedure.
Rationale: Section order can affect practical behavior even when wording is preserved.
Validation target: Proposal states that behavior clarity wins over strict family ordering and exceptions must be recorded.
Validation evidence: Pending validation after proposal revision.

#### SFRP-PR3 - Enum fencing needs an authoritative enum map to prevent duplication

Finding ID: SFRP-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Enum authority map` requiring each changed skill to identify enum source, authoritative destination, values, and duplicate handling.
Rationale: Fencing narrated enums should not create duplicate full value lists in the same skill.
Validation target: Proposal requires before/after value-set proof and no duplicate closed enum value-set lists.
Validation evidence: Pending validation after proposal revision.

#### SFRP-PR4 - Behavior-parity oracle is too subjective as written

Finding ID: SFRP-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Content-preservation proof` requiring a per-skill source-to-destination matrix for moved, tabulated, fenced, or reordered content.
Rationale: Representative-input behavior parity is useful but not deterministic enough by itself for a presentation-only change.
Validation target: Proposal states that behavior parity supplements source-content preservation and does not replace it.
Validation evidence: Pending validation after proposal revision.

#### SFRP-PR5 - Produced-artifact readability should be classified as deferred, not left open

Finding ID: SFRP-PR5
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Reclassified produced-artifact readability from open question to deferred follow-up in the initial intent table, open questions, decision log, and follow-on candidate text.
Rationale: This proposal is moving forward as a published skill readability pass; produced artifact readability changes output expectations and requires separate proposal treatment.
Validation target: Proposal scopes produced-artifact readability out of this change and names it as a deferred follow-up candidate.
Validation evidence: Pending validation after proposal revision.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

#### SFRP-M1-CR1 - Validation fixture weakens settlement-result coverage for unaffected skills

Finding ID: SFRP-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement M1 fix
Chosen action: Update `scripts/test-skill-validator.py` so `spec` can use the new settlement-result enum authority while unaffected `architecture` and `plan` skills retain exact inline settlement-result value coverage.
Rationale: The approved M1 scope permits presentation-only changes to `spec`; it does not justify weakening regression coverage for unaffected first-slice skills.
Validation target: `python scripts/test-skill-validator.py` and M1 selected CI pass with the narrower fixture expectation.
Validation evidence: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `git diff --check -- ...`; `bash scripts/ci.sh --mode explicit ...`.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

#### SFRP-M2-CR1 - Review-focus cells introduce unproven guidance beyond the baseline prose

Finding ID: SFRP-M2-CR1
Disposition: accepted
Status: open
Owner: implementer or spec owner
Owning stage: review-resolution / implement M2 fix
Chosen action: pending source-preserving M2 fix or approved spec/owner change
Rationale: The approved M2 scope permits presentation-only tabulation and enum authority for review-dimension verdict values. The current table adds richer review-focus examples that may be useful, but they are not directly source-mapped to the baseline `spec-review` text and can be read as new review obligations.
Validation target: M2 returns to code-review with either a source-preserving table that removes non-baseline focus examples or an approved spec/owner change that explicitly accepts the richer review-focus guidance as behavior.
Validation evidence: pending
