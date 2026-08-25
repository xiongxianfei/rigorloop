# Review Resolution: Local CLI Observability and Token-Efficient Results

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: proposal-review-r4

- Reviews covered: `proposal-review-r1`
- Findings resolved: 3
- Unresolved findings: 0
- Current result: CLI review registration synchronized the compatibility summary, settlement derived `revision-required`, and the proposal revision addresses CLIOBS-PR6 through CLIOBS-PR8. Same-stage governed rereview remains required before specification.
- Validation evidence: revised proposal `sha256:70652f4e5afb34bb3272f73be339a43661a14ef6d4c69bf02585091a6592f47c`; review log has no open findings; focused lifecycle regressions and package tests pass.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CLIOBS-PR6 | accepted | resolved | Remove request fingerprints from the first release and use invocation IDs plus allowlisted semantic identities. |
| CLIOBS-PR7 | accepted | resolved | Add an `invalid-input` family and define the minimum logger-initialization boundary. |
| CLIOBS-PR8 | accepted | resolved | Assign hosted CI retention and forwarding to a separate roadmap-owned proposal. |

## Finding Details

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
