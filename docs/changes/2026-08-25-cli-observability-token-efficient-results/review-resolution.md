# Review Resolution: Local CLI Observability and Token-Efficient Results

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: proposal-review-r4

- Reviews covered: `proposal-review-r1`, `spec-review-r1`
- Findings resolved: 3
- Unresolved findings: 3
- Current result: Proposal findings remain closed. CLIOBS-SR1 through CLIOBS-SR3 are accepted for bounded specification revision and require same-stage rereview.
- Validation evidence: revised proposal `sha256:70652f4e5afb34bb3272f73be339a43661a14ef6d4c69bf02585091a6592f47c`; review log has no open findings; focused lifecycle regressions and package tests pass.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CLIOBS-PR6 | accepted | resolved | Remove request fingerprints from the first release and use invocation IDs plus allowlisted semantic identities. |
| CLIOBS-PR7 | accepted | resolved | Add an `invalid-input` family and define the minimum logger-initialization boundary. |
| CLIOBS-PR8 | accepted | resolved | Assign hosted CI retention and forwarding to a separate roadmap-owned proposal. |
| CLIOBS-SR1 | accepted | open | Close the unprovable expired-ID outcome or define bounded expiry evidence. |
| CLIOBS-SR2 | accepted | open | Define path containment, permission refusal, and emergency stderr behavior. |
| CLIOBS-SR3 | accepted | open | Close concise-field applicability and benchmark/wrapper proof inputs. |

## Finding Details

### spec-review-r1

#### CLIOBS-SR1

Finding ID: CLIOBS-SR1
Disposition: accepted
Status: open
Owner: specification author
Owning stage: spec
Decision owner: none; the finding narrows ambiguity within the accepted proposal
Decision needed: none
Chosen action: remove `RL_LOG_EXPIRED` from the first release and use one absent-ID result until a bounded expiry index is separately specified.
Rationale: random IDs plus five retained files cannot prove that an absent ID previously existed.
Required outcome: retained lookup has one deterministic absent partition and no hidden or unbounded index.
Validation target: revised R19, EC5, state boundary, examples, and acceptance criteria.
Validation evidence: pending specification revision and spec-review-r2.

#### CLIOBS-SR2

Finding ID: CLIOBS-SR2
Disposition: accepted
Status: open
Owner: specification author
Owning stage: spec
Decision owner: none; safe local logging behavior is already in scope
Decision needed: none
Chosen action: make the selected absolute directory the containment root, refuse symlink or unsafe-permission entries without chmod, and let explicit `off` suppress the emergency stderr diagnostic.
Rationale: an explicit console-off choice should be honored while diagnostic degradation remains visible in new structured projections.
Required outcome: path and emergency-output behavior is closed and testable without changing semantic results.
Validation target: revised R11-R17, E4, EC3, EC6, EC9, and affected boundaries.
Validation evidence: pending specification revision and spec-review-r2.

#### CLIOBS-SR3

Finding ID: CLIOBS-SR3
Disposition: accepted
Status: open
Owner: specification author
Owning stage: spec
Decision owner: none; this operationalizes the accepted token-efficiency gate
Decision needed: none
Chosen action: add concise field applicability, exact line-budget exceptions, a versioned repository benchmark manifest and baseline, an unweighted named-profile median, and an enumerated wrapper surface.
Rationale: adoption proof must not depend on implementation-selected fields, profiles, or wrappers.
Required outcome: concise semantic completeness and adoption measurements are deterministic and regression-testable.
Validation target: revised R23-R31, E2, E7, INT-003, INT-005, and AC7-AC10.
Validation evidence: pending specification revision and spec-review-r2.

### proposal-review-r1

#### CLIOBS-PR6

Finding ID: CLIOBS-PR6
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: retain only a canonical allowlisted semantic fingerprint or remove request fingerprinting from the first release.
Chosen action: remove request digests and derived request fingerprints from the first release; retain only invocation IDs and allowlisted semantic identity fields.
Rationale: an unspecified digest of a request can preserve equality and low-entropy information derived from prohibited private fields.
Required outcome: persistent request correlation contains no raw or derived private request material and has an explicit user value.
Follow-up: run governed proposal rereview.
Validation target: revised event schema boundary and privacy scenarios.
Validation evidence: revised proposal `sha256:70652f4e5afb34bb3272f73be339a43661a14ef6d4c69bf02585091a6592f47c`, Recommended Direction and privacy risk table.

#### CLIOBS-PR7

Finding ID: CLIOBS-PR7
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: define the minimum initialization boundary and whether invalid-input events are included.
Chosen action: define minimum logger initialization before dispatch and parsing, route safely recognized malformed invocations through `invalid-input`, and explicitly exclude earlier startup failures from the file-observability claim.
Rationale: the current universal promise excludes invocations that never reach a supported command family.
Required outcome: every runtime path maps to guaranteed logging, best-effort logging, or an explicit unobservable precondition without raw argument capture.
Follow-up: run governed proposal rereview.
Validation target: applicability matrix and parser/startup failure scenarios.
Validation evidence: revised proposal `sha256:70652f4e5afb34bb3272f73be339a43661a14ef6d4c69bf02585091a6592f47c`, command-family table, applicability paragraph, and invalid-input test strategy.

#### CLIOBS-PR8

Finding ID: CLIOBS-PR8
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: assign hosted CI retention to the current architecture or a named separate proposal or follow-up.
Chosen action: make hosted CI retention and forwarding a separate proposal owned by `docs/roadmap.md#hosted-ci-log-retention-and-forwarding`; retain only local wrapper parity and a forward-compatible local schema here.
Rationale: CI forwarding is deferred in scope while remaining an obligation of the current architecture and next ADR.
Required outcome: one treatment and durable owner control CI retention, forwarding, privacy proof, and implementation.
Follow-up: run governed proposal rereview; initiate the CI proposal only if its roadmap item is selected.
Validation target: aligned scope budget, architecture impact, rollout, decision log, and follow-up ownership.
Validation evidence: revised proposal `sha256:70652f4e5afb34bb3272f73be339a43661a14ef6d4c69bf02585091a6592f47c`, aligned scope budget, architecture impact, test strategy, rollout, decision log, and follow-on link; durable roadmap entry.

### proposal-review-r2

Review closeout: proposal-review-r2

No material findings; no resolution entry required. This clean review was superseded only because its receipt required a structural correction after registration.

### proposal-review-r3

Review closeout: proposal-review-r3

No material findings; no resolution entry required. The fresh review confirms the final clarified proposal revision and closes proposal review.

### proposal-review-r4

Review closeout: proposal-review-r4

No material findings; no resolution entry required. The final rereview confirms that `FU-011` is an unapproved separate-proposal reservation and closes proposal review.
