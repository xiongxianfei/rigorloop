# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: M3 R1
Reviewer: Codex code-review skill
Target: commit ca68eeeb, M3 metadata and persistence slice
Status: changes-requested
Material findings: SLA-CR-M3-1
Reviewed milestone: M3. Minimal change-metadata state and consistency checks
Recording status: recorded

## First-pass risk map

| Risk | Verdict |
| --- | --- |
| Unknown values fall through consistency branches | pass |
| Historical reads mutate state | pass |
| Replacement is partial or non-atomic | pass |
| Review outcome and artifact settlement disagree | finding |
| A second validator family or policy engine appears | pass |

## Finding SLA-CR-M3-1

Severity: high
Location: `scripts/change_metadata_semantics.py`,
`validate_stage_owned_lifecycle_metadata`

Evidence: review outcome and artifact lifecycle state are each validated
against a closed vocabulary, but their required mapping is not checked.
For example, a proposal could carry `outcome: changes-requested` while its
entry says `accepted`.

Required outcome: enforce the review-outcome-to-state mapping, including ADR
approved settlement, and add a regression test.

Safe resolution: add the consistency check after all unknown-value checks;
keep validation in the existing metadata semantic path.

## Outcome

M3 remains in resolution until SLA-CR-M3-1 is fixed and focused validation
passes.
