# Review Resolution: Local CLI Observability and Token-Efficient Results

## Summary

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: proposal-review-r4
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `plan-review-r1`, `test-spec-review-r1`
- Findings resolved: 10
- Unresolved findings: 6
- Current result: Code-review M1 R1 requested six implementation and proof corrections. M1 remains open and requires review-resolution, correction, workflow handoff, and same-stage rereview.
- Validation evidence: `evidence/test-spec-revision-r1.md`; revised test spec `sha256:2c407aeff91b44a7ee39b8eaed162f46755483f75b4cb54379abaec86b319c73`; boundary-first structural validation passed.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CLIOBS-PR6 | accepted | resolved | Remove request fingerprints from the first release and use invocation IDs plus allowlisted semantic identities. |
| CLIOBS-PR7 | accepted | resolved | Add an `invalid-input` family and define the minimum logger-initialization boundary. |
| CLIOBS-PR8 | accepted | resolved | Assign hosted CI retention and forwarding to a separate roadmap-owned proposal. |
| CLIOBS-SR1 | accepted | resolved | Removed the unprovable expired-ID outcome from the first release. |
| CLIOBS-SR2 | accepted | resolved | Defined path containment, permission refusal, bounded locks, and console-off behavior. |
| CLIOBS-SR3 | accepted | resolved | Added concise-field applicability and versioned benchmark/wrapper proof inputs. |
| CLIOBS-PLR1 | accepted | resolved | Made M1-M4 explicitly test-first. |
| CLIOBS-PLR2 | accepted | resolved | Added deterministic selector ownership and a passing exact command requirement. |
| CLIOBS-TSR1 | accepted | resolved | Added direct no-network, no-database, no-daemon, and bounded-resource proof for R34. |
| CLIOBS-TSR2 | accepted | resolved | Added benchmark harness tests and packed-package/documentation proof to M4. |
| CLIOBS-M1-CR1 | accepted | open | Make unsafe-path and event-construction failures diagnostic-only and preserve semantic dispatch. |
| CLIOBS-M1-CR2 | accepted | open | Make log inspection non-mutating for absent and existing stores. |
| CLIOBS-M1-CR3 | accepted | open | Return semantic results to one controller and finalize observability before new projection rendering. |
| CLIOBS-M1-CR4 | accepted | open | Preserve complete JSONL records across partial append, rotation, and interruption failures. |
| CLIOBS-M1-CR5 | accepted | open | Measure real complete CLI interactions instead of trusting asserted gate values. |
| CLIOBS-M1-CR6 | accepted | open | Implement and run the approved T01-T17 and C01-C10 proof surface truthfully. |

## Finding Details

### code-review-m1-r1

#### CLIOBS-M1-CR1

Finding ID: CLIOBS-M1-CR1
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: implement M1-M3
Decision owner: none
Decision needed: none
Chosen action: isolate unsafe-path and event-construction failures from semantic dispatch and add direct failure regressions.
Rationale: diagnostic availability cannot control semantic command behavior.
Required outcome: logging failures preserve command output, repository bytes, and semantic exit status.
Validation target: R15, R33, T02, T07, T12, PRF-002, PRF-006, PRF-009.
Validation evidence: pending correction and code-review-m1-r2.

#### CLIOBS-M1-CR2

Finding ID: CLIOBS-M1-CR2
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: implement M3
Decision owner: none
Decision needed: none
Chosen action: split read-only path validation from writer initialization.
Rationale: lookup cannot mutate the local diagnostic store.
Required outcome: every inspection outcome leaves the store byte/path inventory unchanged.
Validation target: R18-R20, T08, T14, PRF-002, PRF-012.
Validation evidence: pending correction and code-review-m1-r2.

#### CLIOBS-M1-CR3

Finding ID: CLIOBS-M1-CR3
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: implement M1-M3
Decision owner: none
Decision needed: none
Chosen action: return normalized semantic results to the invocation controller, finalize observability, and render once.
Rationale: a completion failure must be visible in a new projection without duplicate stdout.
Required outcome: new projections report final observability and all renderers share one semantic result.
Validation target: R15, R21-R28, T10-T12, BND-COMPOSE-001, INT-003.
Validation evidence: pending correction and code-review-m1-r2.

#### CLIOBS-M1-CR4

Finding ID: CLIOBS-M1-CR4
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: add recoverable append/rotation behavior and fault-injection proof.
Rationale: failed local diagnostics cannot leave corrupt retained JSONL.
Required outcome: every retained line remains complete under append, rotation, disk, and interruption faults.
Validation target: R13-R15, T05, PRF-005, PRF-006, PRF-010.
Validation evidence: pending correction and code-review-m1-r2.

#### CLIOBS-M1-CR5

Finding ID: CLIOBS-M1-CR5
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: implement M4
Decision owner: none
Decision needed: none
Chosen action: replace asserted byte/gate values with executable complete-interaction measurements.
Rationale: self-reported fixture booleans and byte counts cannot prove adoption eligibility.
Required outcome: all six profiles are measured from normalized CLI stdout, stderr, and required follow-ups.
Validation target: R29-R30, T15, C06, C10, PRF-013, INT-005.
Validation evidence: pending correction and code-review-m1-r2.

#### CLIOBS-M1-CR6

Finding ID: CLIOBS-M1-CR6
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: implement M1-M4
Decision owner: none
Decision needed: none
Chosen action: complete the approved test partitions and rerun every milestone command with truthful evidence.
Rationale: broad passing package tests do not substitute for named boundary, recovery, privacy, packaging, and measurement proof.
Required outcome: T01-T17 and applicable C01-C10 evidence are current and all milestone reports match actual results.
Validation target: complete approved proof map.
Validation evidence: pending correction and code-review-m1-r2.

### test-spec-review-r1

#### CLIOBS-TSR1

Finding ID: CLIOBS-TSR1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Decision owner: none; this is direct proof required by R34
Decision needed: none
Chosen action: extend T05 with network/process guards and open-handle assertions and map it to the affected proof rows.
Rationale: fixed file counts do not alone prove absence of prohibited external execution paths.
Required outcome: deterministic direct proof of the complete R34 resource boundary.
Validation target: R34, PRF-008, T05, and Performance checks.
Final action: Extended T05 and the affected R34, BND-ENV-001, and performance mappings with deterministic network/process guards, dependency inspection, open-handle proof, and bounded filesystem counts.
Validation evidence: `evidence/test-spec-revision-r1.md`; revised test spec `sha256:2c407aeff91b44a7ee39b8eaed162f46755483f75b4cb54379abaec86b319c73`.

#### CLIOBS-TSR2

Finding ID: CLIOBS-TSR2
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Decision owner: none; the approved plan already requires these M4 proofs
Decision needed: none
Chosen action: add the benchmark regression command and a packed-package/documentation T17 case to M4.
Rationale: named automation and plan proof do not count unless a milestone command executes them.
Required outcome: M4 directly executes benchmark-tool tests and proves the shipped package/documentation surface.
Validation target: validation command ledger, M4 milestone row, T15, and new T17.
Final action: Added C10 for benchmark-harness regressions, T17 for packed CLI and documented operations, and mapped both to the M4 gate.
Validation evidence: `evidence/test-spec-revision-r1.md`; revised test spec `sha256:2c407aeff91b44a7ee39b8eaed162f46755483f75b4cb54379abaec86b319c73`.

### plan-review-r1

#### CLIOBS-PLR1

Finding ID: CLIOBS-PLR1
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Decision owner: none; repository implementation guidance is explicit
Decision needed: none
Chosen action: add a focused failing or characterization-test-first step to M1-M4.
Rationale: milestone proof must fail for the intended reason before production behavior changes.
Required outcome: every implementation milestone has explicit test-first sequencing without scope or identity changes.
Validation target: revised M1-M4 implementation steps.
Final action: Added focused failing or characterization-test-first steps to M1-M4 without changing milestone identity or scope.
Validation evidence: `evidence/plan-revision-r1.md`; plan-review-r2 pending.

#### CLIOBS-PLR2

Finding ID: CLIOBS-PLR2
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Decision owner: none; the selector's deterministic ownership contract applies
Decision needed: none
Chosen action: add selector registry and regression ownership to M3 and require an exact file-based selector command with no manual-routing blocker in M4.
Rationale: a declared closeout command must not be predictably blocked by an unowned production path.
Required outcome: wrapper changes select focused validation deterministically and the exact post-implementation command passes.
Validation target: M3/M4 files, steps, command, and completion criteria.
Final action: Added selector registry/test ownership to M3 and an exact post-implementation file list plus no-manual-routing completion gate to M4.
Validation evidence: `evidence/plan-revision-r1.md`; plan-review-r2 pending.

### spec-review-r1

#### CLIOBS-SR1

Finding ID: CLIOBS-SR1
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: none; the finding narrows ambiguity within the accepted proposal
Decision needed: none
Chosen action: remove `RL_LOG_EXPIRED` from the first release and use one absent-ID result until a bounded expiry index is separately specified.
Rationale: random IDs plus five retained files cannot prove that an absent ID previously existed.
Required outcome: retained lookup has one deterministic absent partition and no hidden or unbounded index.
Validation target: revised R19, EC5, state boundary, examples, and acceptance criteria.
Final action: Replaced expiry claims with one absent-ID result across R19, EC5, BND-STATE-001, and AC5.
Validation evidence: `evidence/spec-revision-r1.md`; spec-review-r2 pending.

#### CLIOBS-SR2

Finding ID: CLIOBS-SR2
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: none; safe local logging behavior is already in scope
Decision needed: none
Chosen action: make the selected absolute directory the containment root, refuse symlink or unsafe-permission entries without chmod, and let explicit `off` suppress the emergency stderr diagnostic.
Rationale: an explicit console-off choice should be honored while diagnostic degradation remains visible in new structured projections.
Required outcome: path and emergency-output behavior is closed and testable without changing semantic results.
Validation target: revised R11-R17, E4, EC3, EC6, EC9, and affected boundaries.
Final action: Defined selected-root containment, symlink refusal, no chmod repair, `RL_LOG_UNSAFE_PATH`, a 10-attempt/1,000-millisecond lock bound, and explicit console-off suppression.
Validation evidence: `evidence/spec-revision-r1.md`; spec-review-r2 pending.

#### CLIOBS-SR3

Finding ID: CLIOBS-SR3
Disposition: accepted
Status: resolved
Owner: specification author
Owning stage: spec
Decision owner: none; this operationalizes the accepted token-efficiency gate
Decision needed: none
Chosen action: add concise field applicability, exact line-budget exceptions, a versioned repository benchmark manifest and baseline, an unweighted named-profile median, and an enumerated wrapper surface.
Rationale: adoption proof must not depend on implementation-selected fields, profiles, or wrappers.
Required outcome: concise semantic completeness and adoption measurements are deterministic and regression-testable.
Validation target: revised R23-R31, E2, E7, INT-003, INT-005, and AC7-AC10.
Final action: Added the exhaustive concise-field applicability table, closed the two-line scope, and fixed the six-profile manifest, v0.4.x baseline, unweighted median, versioning rule, and production wrapper surface.
Validation evidence: `evidence/spec-revision-r1.md`; spec-review-r2 pending.

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
