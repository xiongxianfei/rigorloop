# Review Resolution: Local CLI Observability and Token-Efficient Results

## Summary

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 5
- Current result: proposal revision and same-stage rereview are required before specification.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CLIOBS-PR1 | needs-decision | open | Select lifecycle-only or universal CLI observability and classify every command family. |
| CLIOBS-PR2 | needs-decision | open | Select the versioned compatibility and migration contract for JSON and human output. |
| CLIOBS-PR3 | needs-decision | open | Make minimum invocation lookup a dependency or remove the first-release reliance on it. |
| CLIOBS-PR4 | needs-decision | open | Select a falsifiable token-value threshold and adoption rule. |
| CLIOBS-PR5 | accepted | open | Add the required proposal status section without claiming settlement. |

## Finding Details

### proposal-review-r1

#### CLIOBS-PR1

Finding ID: CLIOBS-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: choose lifecycle-only or universal CLI observability and classify every public command family.
Chosen action: pending proposal-author decision between lifecycle-only and universal CLI observability.
Rationale: the current proposal promises logging for every invocation but defines lifecycle-oriented events and evidence.
Required outcome: every current and future command family has one applicability result for logging, projections, references, and CI forwarding.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: exhaustive command-family applicability table and aligned acceptance scenarios.
Validation evidence: pending proposal revision.

#### CLIOBS-PR2

Finding ID: CLIOBS-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: choose the compatibility mechanism, transition window, and default-change boundary for machine and human output.
Chosen action: pending selection of the compatibility mechanism and default-transition boundary.
Rationale: `--detail`, format versioning, and transition aliases impose different public compatibility contracts.
Required outcome: one versioned machine and human output migration policy, including adapter behavior and deprecation timing.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: compatibility decision, rollout gate, and old/new projection conformance scenarios.
Validation evidence: pending proposal revision.

#### CLIOBS-PR3

Finding ID: CLIOBS-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: choose whether minimum correlation and single-invocation retrieval are mandatory in the concise-default slice.
Chosen action: pending classification of correlation, path discovery, and single-invocation lookup as mandatory or deferred.
Rationale: concise defaults promise detail recovery without rerunning mutations, which requires a deterministic retrieval surface.
Required outcome: the first concise-default slice either includes minimum lookup or provides another complete, non-mutating detail path.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: corrected scope budget, rollout dependency, and lookup acceptance scenarios.
Validation evidence: pending proposal revision.

#### CLIOBS-PR4

Finding ID: CLIOBS-PR4
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: choose a provisional measurable reduction threshold and the behavior when it is not met.
Chosen action: pending selection of a provisional token or byte threshold and default-adoption rule.
Rationale: “materially smaller” cannot determine whether the added logging and rotation complexity creates enough user value.
Required outcome: a baseline, representative profiles, complete-interaction accounting, semantic guardrails, and pass/fail adoption behavior.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: measurable objective and deterministic rollout decision.
Validation evidence: pending proposal revision.

#### CLIOBS-PR5

Finding ID: CLIOBS-PR5
Disposition: accepted
Status: open
Owner: proposal author
Owning stage: proposal
Chosen action: add the required status section during proposal revision.
Rationale: the current artifact fails lifecycle validation because it has no `## Status` section.
Required outcome: the proposal records an accurate draft or changes-requested status without claiming approval or settlement.
Follow-up: revise the proposal and run proposal-review-r2.
Validation target: `python scripts/validate-artifact-lifecycle.py` accepts the revised proposal structure.
Validation evidence: pending proposal revision; proposal-review-r1 validation reproduced the missing-status failure.
