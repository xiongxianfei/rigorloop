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
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3
Review closeout: code-review-m1-r4
Review closeout: code-review-m1-r5
Review closeout: code-review-m1-r6
Review closeout: code-review-m1-r8
Review closeout: code-review-m1-r9
Review closeout: code-review-m1-r11
Review closeout: code-review-m1-r13
Review closeout: code-review-m1-r15
Review closeout: code-review-m1-r16
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m2-r3
Review closeout: code-review-m2-r4
Review closeout: code-review-m2-r5
Review closeout: code-review-m2-r8
Review closeout: code-review-m2-r9
Review closeout: code-review-m2-r10
Review closeout: code-review-m2-r11
Review closeout: code-review-m2-r12
Review closeout: code-review-m2-r13
Review closeout: code-review-m2-r14
Review closeout: code-review-m2-r15
Review closeout: code-review-m2-r6
Review closeout: code-review-m2-r7

- Reviews covered: `proposal-review-r1`, `spec-review-r1`, `plan-review-r1`, `test-spec-review-r1`
- Findings resolved: 51
- Unresolved findings: 4
- Current result: Isolated code-review M3 R1 returned `changes-requested` on bundle `sha256:b2ef0a7fb4d2cf548d06e636145d361d58c4ca8455ded0d1862b97834df28303`. `CLIOBS-M3-R1-F1` through `CLIOBS-M3-R1-F4` require implementation correction and fresh M3 rereview; no lifecycle state or routing changed.
- Validation evidence: Package C01 passed 256/256, the wrapper helper tests passed 3/3, selector tests passed 154/154, and repository lifecycle validation passed for 29 records with one declared baseline warning. Direct public/controller probes nevertheless returned an unapproved retained private field, reflected an invalid identity in JSON and human output, and downgraded lifecycle exit 3 to warning; inspection also proved the wrapper tests and selector do not execute T13.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| CLIOBS-M3-R1-F1 | accepted | unresolved | Validate retained events against the closed read-side schema before lookup returns them. |
| CLIOBS-M3-R1-F2 | accepted | unresolved | Reject invalid invocation identities without echoing the raw value. |
| CLIOBS-M3-R1-F3 | accepted | unresolved | Derive terminal severity from semantic failure class rather than numeric exit code alone. |
| CLIOBS-M3-R1-F4 | accepted | unresolved | Execute and select the complete production-wrapper T13 matrix. |
| CLIOBS-M2-R13-F1 | accepted | resolved | Capture trusted acquisition identity before injected inspection, preserve same-number replacements, and prove the corrected frozen M2 bundle. |
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
| CLIOBS-M1-CR1 | accepted | resolved | Unsafe-path and event-construction failures are diagnostic-only and preserve semantic dispatch. |
| CLIOBS-M1-CR2 | accepted | resolved | Log inspection validates existing state read-only and does not create an absent store. |
| CLIOBS-M1-CR3 | accepted | resolved | One controller finalizes observability before rendering one semantic result. |
| CLIOBS-M1-CR4 | accepted | resolved | Partial append rollback and concurrent-writer proof preserve complete JSONL records. |
| CLIOBS-M1-CR5 | accepted | resolved | The six-profile gate measures real complete CLI interactions and derives every gate. |
| CLIOBS-M1-CR6 | accepted | resolved | Direct proof, selector ownership, packed-package smoke, and corrected proof-command ownership cover the approved surface truthfully. |
| CLIOBS-M1-CR7 | accepted | resolved | Replaced unsubstantiated v0.4.x values with replayed, revision-bound detailed measurements. |
| CLIOBS-M1-CR8 | accepted | resolved | Added direct severity, failure-isolation, lifecycle equivalence, and copied-log non-authority proof. |
| CLIOBS-M1-CR9 | accepted | resolved | Normalized allowlisted string-list diagnostic fields and rejected unsupported shapes. |
| CLIOBS-M1-L1-F1 | accepted | resolved | Mutation results now provide the authoritative persisted-change fact. |
| CLIOBS-M1-L1-F2 | accepted | resolved | Projection omits ambiguous continuation choices. |
| CLIOBS-M1-L1-F3 | accepted | resolved | `new-change` now accepts all shared explicit formats. |
| CLIOBS-M1-L1-F4 | accepted | resolved | T10/T11 now cover result, mutation, continuation, and public compatibility partitions. |
| CLIOBS-M1-L1-F5 | accepted | resolved | Added the revision-bound 27-case T10 corpus and preserved detailed JSON compatibility. |
| CLIOBS-M1-L1-F6 | accepted | resolved | Repair state change now follows a closed persistence-status mapping. |
| CLIOBS-M1-L1-F7 | accepted | resolved | Post-evaluation transaction failures now report authoritative unchanged state. |
| CLIOBS-M1-L1-F8 | accepted | resolved | Lifecycle-owned before/after persistence determines caught failure mutation truth. |
| CLIOBS-M1-L1-F9 | accepted | resolved | Repair evaluation initializes the lifecycle-owned before snapshot. |
| CLIOBS-M1-L1-F10 | accepted | resolved | Explicit detailed projection retains authoritative mutation truth without changing legacy JSON. |
| CLIOBS-M1-L1-F11 | accepted | resolved | All new projections retain the finalized closed observability state. |
| CLIOBS-M1-L1-F12 | accepted | resolved | Log inspection rejects undocumented detailed output and retains its human/JSON contract. |
| CLIOBS-M2-L1-F1 | accepted | resolved | Event shapes, mandatory facts, clock failure, duration, and bounded fallback now fail closed. |
| CLIOBS-M2-L1-F2 | accepted | resolved | Candidate-based append failure preserves the prior complete active JSONL. |
| CLIOBS-M2-L1-F3 | accepted | resolved | Injected monotonic timing enforces ten attempts and the 1,000 ms budget. |
| CLIOBS-M2-L1-F4 | accepted | resolved | Completed the T02-T05 proof matrix and refreshed identity-bound M2 evidence. |
| M2-L1B-F1 | accepted | resolved | Closed scalar and list validators reject nested unsafe values. |
| M2-L1B-F2 | accepted | resolved | Bound destructive source operations to checked identities and removed unsafe failed-publication cleanup. |
| M2-L1B-F3 | accepted | resolved | Throwing diagnostic console sinks no longer abort semantic dispatch. |
| M2-L1B-F4 | accepted | resolved | Completed the distinct fault, path, privacy, timing, and resource proof partitions. |
| CLIOBS-M2-R3-F1 | accepted | resolved | Timestamp-source failure now produces degraded diagnostics without changing semantic execution. |
| CLIOBS-M2-R3-F2 | accepted | resolved | All post-open descriptors close; stale or unverifiable locks are retained under approved R14. |
| CLIOBS-M2-R3-F3 | accepted | resolved | Failed publication performs no pathname unlink cleanup, and the excluded adversarial race is explicit. |
| CLIOBS-M2-R3-F4 | accepted | resolved | Added direct retained-surface, interruption, rotation, recovery, and descriptor proof with truthful evidence. |
| CLIOBS-M2-R4-F1 | accepted | resolved | Revalidated root/components/owned paths and source identity adjacent to every destructive operation. |
| CLIOBS-M2-R4-F2 | accepted | resolved | Every tested post-open fault closes descriptors; approved R14 defines fail-safe stale-lock recovery. |
| CLIOBS-M2-R4-F3 | accepted | resolved | Event kind and sequence are validated as one closed pair. |
| CLIOBS-M2-R4-F4 | accepted | resolved | Added the exact reproduced boundary tests and restricted evidence to demonstrated results. |
| CLIOBS-M2-R5-F1 | accepted | resolved | Added one injected adjacent validator for root, components, source, and existing destination at every mutation. |
| CLIOBS-M2-R11-F1 | accepted | resolved | Centralized bounded descriptor release closes still-owned handles, avoids retry after `EBADF`, and refuses a known reused identity. |

## Finding Details

### code-review-m3-r1

#### CLIOBS-M3-R1-F1

Finding ID: CLIOBS-M3-R1-F1
Disposition: accepted
Status: unresolved
Owner: implementation author
Owning stage: implement M3
Decision owner: none
Decision needed: none
Chosen action: add closed read-side diagnostic-event validation and public lookup regressions before returning retained events.
Rationale: matching `schema_version` and `invocation_id` do not prove that a retained object is a valid allowlisted event.
Required outcome: lookup returns only complete closed-schema events and never returns unknown, malformed, wrong-type, or private fields.
Validation target: R5-R9, R19-R20, E5, T08, T09, public JSON/human lookup, and the M3 package suite.
Final action: pending implementation correction.
Validation evidence: code-review-m3-r1 direct public probe returned `M3_LOOKUP_PRIVATE_SENTINEL` from an unvalidated schema-1 object.

#### CLIOBS-M3-R1-F2

Finding ID: CLIOBS-M3-R1-F2
Disposition: accepted
Status: unresolved
Owner: implementation author
Owning stage: implement M3
Decision owner: none
Decision needed: none
Chosen action: validate the lookup identity before result construction and use constant rejection output.
Rationale: rejected caller text is not a validated invocation identity and has no diagnostic value in the stable error.
Required outcome: invalid identities return `RL_INVALID_INVOCATION_ID` without echoing or persisting the rejected value in JSON, human output, or logs.
Validation target: R8, R19, BND-INPUT-001, T08, T09, and both public lookup formats.
Final action: pending implementation correction.
Validation evidence: code-review-m3-r1 JSON and human probes each returned `M3_INVALID_PRIVATE_SENTINEL` with exit 4.

#### CLIOBS-M3-R1-F3

Finding ID: CLIOBS-M3-R1-F3
Disposition: accepted
Status: unresolved
Owner: implementation author
Owning stage: implement M3
Decision owner: none
Decision needed: none
Chosen action: propagate normalized semantic failure classification into the invocation controller and expand severity/console tests.
Rationale: one numeric exit code can represent outcomes with different required diagnostic severity, so exit-code-only mapping loses the R4 distinction.
Required outcome: internal, unsafe-recovery, and logging failures are error; expected policy/input failures are warning; semantic exits remain unchanged.
Validation target: R4, R15, T06, T07, lifecycle exit 3, logging failure, unsafe recovery, validation, usage, stale, and blocked partitions.
Final action: pending implementation correction.
Validation evidence: code-review-m3-r1 direct controller probe recorded lifecycle exit 3 as `severity: warning`, `status: error`, with no default-console error diagnostic.

#### CLIOBS-M3-R1-F4

Finding ID: CLIOBS-M3-R1-F4
Disposition: accepted
Status: unresolved
Owner: implementation author
Owning stage: implement M3
Decision owner: none
Decision needed: none
Chosen action: implement the executable T13 child-result matrix and add a dedicated selector check for the wrapper and its test.
Rationale: pure baseline-matching tests and generic package checks cannot prove production-wrapper structured-output consumption or exit-class parity.
Required outcome: wrapper changes deterministically select a focused check that executes success, blocked, usage, invalid-repository, stale, and internal detailed/concise child results, prevents duplicate success output, and preserves classifications.
Validation target: R31, T13, C03, C04, CLIOBS-PLR2, wrapper script/test, selector catalog, selector regressions, and exact changed-path selection.
Final action: pending implementation correction.
Validation evidence: code-review-m3-r1 inspection found only three in-process `baseline_matches()` tests and selector routing to package/publication checks; no selected command executes T13.

### code-review-m1-r1

#### CLIOBS-M1-CR1

Finding ID: CLIOBS-M1-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1-M3
Decision owner: none
Decision needed: none
Chosen action: isolate unsafe-path and event-construction failures from semantic dispatch and add direct failure regressions.
Rationale: diagnostic availability cannot control semantic command behavior.
Required outcome: logging failures preserve command output, repository bytes, and semantic exit status.
Validation target: R15, R33, T02, T07, T12, PRF-002, PRF-006, PRF-009.
Final action: Isolated configuration and event-construction failures behind diagnostic degradation; semantic dispatch, output, repository bytes, and exit classification remain authoritative.
Validation evidence: `evidence/code-review-m1-r1-correction.md`; 22 focused observability tests and 201 package tests passed.

#### CLIOBS-M1-CR2

Finding ID: CLIOBS-M1-CR2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M3
Decision owner: none
Decision needed: none
Chosen action: split read-only path validation from writer initialization.
Rationale: lookup cannot mutate the local diagnostic store.
Required outcome: every inspection outcome leaves the store byte/path inventory unchanged.
Validation target: R18-R20, T08, T14, PRF-002, PRF-012.
Final action: Split read-only validation from writer initialization and added absent-store and corrupt-store lookup regressions.
Validation evidence: `evidence/m3-invocation-integration.md`; focused lookup regressions and 201 package tests passed.

#### CLIOBS-M1-CR3

Finding ID: CLIOBS-M1-CR3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1-M3
Decision owner: none
Decision needed: none
Chosen action: return normalized semantic results to the invocation controller, finalize observability, and render once.
Rationale: a completion failure must be visible in a new projection without duplicate stdout.
Required outcome: new projections report final observability and all renderers share one semantic result.
Validation target: R15, R21-R28, T10-T12, BND-COMPOSE-001, INT-003.
Final action: Buffered semantic output behind one controller and rendered projections only after terminal observability is finalized with the semantic exit code.
Validation evidence: `evidence/m1-result-model.md`; completion-failure, exit-parity, and single-render focused regressions passed.

#### CLIOBS-M1-CR4

Finding ID: CLIOBS-M1-CR4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: add recoverable append/rotation behavior and fault-injection proof.
Rationale: failed local diagnostics cannot leave corrupt retained JSONL.
Required outcome: every retained line remains complete under append, rotation, disk, and interruption faults.
Validation target: R13-R15, T05, PRF-005, PRF-006, PRF-010.
Final action: Added full-write verification, sync, exact pre-append truncation on failure, and real concurrent-writer proof.
Validation evidence: `evidence/m2-logging-core.md`; partial-write, rotation, lock, and six-process JSONL regressions passed.

#### CLIOBS-M1-CR5

Finding ID: CLIOBS-M1-CR5
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M4
Decision owner: none
Decision needed: none
Chosen action: replace asserted byte/gate values with executable complete-interaction measurements.
Rationale: self-reported fixture booleans and byte counts cannot prove adoption eligibility.
Required outcome: all six profiles are measured from normalized CLI stdout, stderr, and required follow-ups.
Validation target: R29-R30, T15, C06, C10, PRF-013, INT-005.
Final action: Replaced asserted fixture results with subprocess execution, normalized stdout/stderr and follow-up accounting, field checks, exit checks, and immutable fixture identity.
Validation evidence: `evidence/m4-token-and-package-proof.md`; 3 measurement regressions and the six-profile gate passed with a 73.04% median reduction and no default change.

#### CLIOBS-M1-CR6

Finding ID: CLIOBS-M1-CR6
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1-M4
Decision owner: none
Decision needed: none
Chosen action: complete the approved test partitions and rerun every milestone command with truthful evidence.
Rationale: broad passing package tests do not substitute for named boundary, recovery, privacy, packaging, and measurement proof.
Required outcome: T01-T17 and applicable C01-C10 evidence are current and all milestone reports match actual results.
Validation target: complete approved proof map.
Final action: Added direct failure and boundary regressions, deterministic selector ownership, exact installed-package smoke, truthful milestone evidence, guarded duplicate-registration recovery, and approved plan/test-spec proof-command corrections.
Validation evidence: `evidence/code-review-m1-r1-correction.md`; C01-C04 and C06-C10 applicable implementation proof passed; C05 is rerun after this durable closeout and C11 remains final-verification proof.

### code-review-m1-r2

#### CLIOBS-M1-CR7

Finding ID: CLIOBS-M1-CR7
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M4
Decision owner: none
Decision needed: none
Chosen action: bind the baseline to the exact pre-feature v0.4.x implementation and correct its measured bytes.
Rationale: a real current measurement cannot establish a reduction against invented or irreproducible prior values.
Required outcome: reproducible baseline provenance and recalculated adoption evidence.
Validation target: R29-R30, T15, C06, C10.
Final action: Replayed the six detailed interactions at the exact pre-feature revision and bound the baseline to revision, package version, normalization, and command mapping.
Validation evidence: `evidence/code-review-m1-r2-correction.md`; C06/C10 passed with a 72.65% median and no default change.

#### CLIOBS-M1-CR8

Finding ID: CLIOBS-M1-CR8
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2-M3
Decision owner: none
Decision needed: none
Chosen action: add direct table-driven diagnostic matrix and lifecycle non-authority tests.
Rationale: broad package success cannot substitute for named cross-boundary proof.
Required outcome: current direct proof for T06, T07, T12, and T14 with truthful evidence.
Validation target: R1-R5, R15-R17, R27-R28, R32, T06, T07, T12, T14.
Final action: Added public family/severity tests, environment/console failure partitions, lifecycle semantic and repository-byte equivalence, and copied-log non-authority proof.
Validation evidence: `evidence/code-review-m1-r2-correction.md`; 27 focused and 206 package tests passed.

#### CLIOBS-M1-CR9

Finding ID: CLIOBS-M1-CR9
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: introduce typed normalization for allowlisted string-list event fields.
Rationale: privacy-bounded logging applies to every retained string, including collection members.
Required outcome: control characters cannot persist through any allowlisted string field and invalid shapes fail closed.
Validation target: R7-R9, T02, T03.
Final action: Added typed normalization for string-list event fields and fail-closed validation for unsupported member shapes.
Validation evidence: `evidence/code-review-m1-r2-correction.md`; focused event privacy regressions passed.

### code-review-m1-r3

The local L0 rereview found no new material implementation issue, but it is inconclusive for workflow promotion because automated reviews cannot advance at L0. No finding disposition is required. M1 remains review-requested pending an L1-or-higher review.

### code-review-m1-r4

#### CLIOBS-M1-L1-F1

Finding ID: CLIOBS-M1-L1-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: centralize an authoritative closed mapping for mutation state changes.
Rationale: projections cannot infer persistence from a broad negative list.
Required outcome: no-write outcomes report false and persisted transitions report true.
Validation target: R23, R27, T11.
Final action: Added authoritative mutation facts and removed renderer inference; dry-run and already-recorded outcomes are false while persisted revision changes are true.
Validation evidence: `evidence/code-review-m1-r4-correction.md`; T11 state-change table and 211 package tests passed.

#### CLIOBS-M1-L1-F2

Finding ID: CLIOBS-M1-L1-F2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: enforce exact-one continuation selection.
Rationale: list order is not deterministic continuation authority.
Required outcome: zero/multiple choices omit the field; one explicit or unique choice is retained.
Validation target: R23-R25, T11.
Final action: Added exact-one unique selection with explicit continuation precedence and omission for zero, multiple, or conflicting choices.
Validation evidence: `evidence/code-review-m1-r4-correction.md`; T11 continuation partition tests and 211 package tests passed.

#### CLIOBS-M1-L1-F3

Finding ID: CLIOBS-M1-L1-F3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: admit the shared format vocabulary in new-change parsing and preserve one renderer.
Rationale: public handlers cannot diverge after common top-level option parsing.
Required outcome: concise and detailed explicit formats work for new-change without changing legacy defaults.
Validation target: R21-R27, T10.
Final action: Added shared-format parsing to `new-change` and routed concise formats through the common renderer without changing legacy JSON.
Validation evidence: `evidence/code-review-m1-r4-correction.md`; public new-change format characterization and 211 package tests passed.

#### CLIOBS-M1-L1-F4

Finding ID: CLIOBS-M1-L1-F4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: add table-driven field and public compatibility characterization.
Rationale: the approved proof must fail for the defects the reviewer reproduced.
Required outcome: T10/T11 cover every named result and mutation partition.
Validation target: T10, T11, C01, C02.
Final action: Added table-driven result-class, mutation-state, continuation-cardinality, mandatory-field, and public compatibility coverage.
Validation evidence: `evidence/code-review-m1-r4-correction.md`; 14 exact C02 tests, 32 expanded focused tests, and 211 package tests passed.

### code-review-m1-r5

#### CLIOBS-M1-L1-F5

Finding ID: CLIOBS-M1-L1-F5
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: add the complete revision-bound compatibility characterization required by T10.
Rationale: renderer-unit equivalence and one public success case cannot prove compatibility across the applicable command surface.
Required outcome: legacy human/JSON results match the exact pre-feature baseline and every JSON case matches explicit detailed JSON.
Validation target: R21, R22, R26, T10, C01, C02.
Final action: Added 27 normalized cases bound to `fcbbfda44a89945ee06cfa0c1b16dcbd39984036`, fixed the detailed-JSON `state_changed` leak they exposed, and isolated non-observability tests from the shared local log store.
Validation evidence: `evidence/code-review-m1-r5-correction.md`; 15 exact C02 tests, 117 CLI tests, and 212 package tests passed.

### code-review-m1-r6

#### CLIOBS-M1-L1-F6

Finding ID: CLIOBS-M1-L1-F6
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: derive repair state change from a closed repair persistence outcome mapping.
Rationale: lifecycle-owned lock and recovery bytes can change without changing the `change.yaml` lifecycle revision.
Required outcome: persisted repair outcomes report true; dry-run and no-op outcomes report false; unknown statuses fail closed; detailed compatibility remains unchanged.
Validation target: R23, R27, T11, C01, C02.
Final action: Added exhaustive repair outcome mapping, a public orphan-lock/no-op regression, and an unknown-status regression.
Validation evidence: `evidence/code-review-m1-r6-correction.md`; 17 exact C02 tests and 214 package tests passed.

### code-review-m1-r8

#### CLIOBS-M1-L1-F7

Finding ID: CLIOBS-M1-L1-F7
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: carry transition-evaluation state into caught mutation results.
Rationale: a transaction can reject or roll back after semantic transition evaluation without persisting lifecycle bytes.
Required outcome: post-evaluation failures report false, pre-evaluation failures omit the field, and persisted outcomes remain true.
Validation target: R23, R27, T11, C01, C02.
Final action: Added evaluation-state tracking plus public busy, injected rollback, and pre-evaluation omission regressions.
Validation evidence: `evidence/code-review-m1-r8-correction.md`; 18 exact C02 tests and 215 package tests passed.

### code-review-m1-r9

#### CLIOBS-M1-L1-F8

Finding ID: CLIOBS-M1-L1-F8
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: compare lifecycle-owned repository bytes before and after caught post-evaluation transaction failures.
Rationale: a real transaction fault may persist recovery state even when `change.yaml` is restored or unchanged.
Required outcome: pre-evaluation failures omit `state_changed`; busy and verified rollback failures report false; retained recovery, candidate, lock, or changed `change.yaml` bytes report true.
Validation target: R23, R27, T11, C01, C02.
Final action: Added content-addressed lifecycle-owned snapshots plus real retained-recovery and verified-rollback transaction regressions.
Validation evidence: `evidence/code-review-m1-r9-correction.md`; 18 exact C02 tests and 215 package tests passed.

### code-review-m1-r11

#### CLIOBS-M1-L1-F9

Finding ID: CLIOBS-M1-L1-F9
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: initialize lifecycle-owned persistence identity before repair inspection and execution.
Rationale: repair failure paths share the catch projector and require the same authoritative invocation baseline.
Required outcome: unchanged live-lock repair rejection reports false; persisted repair changes remain true; pre-evaluation rejection remains omitted.
Validation target: R23, R27, T11, C01, C02.
Final action: Initialized the repair baseline before inspection/action and added a public live-lock repair-error regression.
Validation evidence: `evidence/code-review-m1-r11-correction.md`; 18 exact C02 tests and 215 package tests passed.

### code-review-m1-r13

#### CLIOBS-M1-L1-F10

Finding ID: CLIOBS-M1-L1-F10
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: separate explicit complete detailed projection from legacy JSON compatibility serialization.
Rationale: non-enumerable internal facts preserve legacy output but must be materialized in explicit detailed output.
Required outcome: legacy JSON stays exact; detailed and concise agree on applicable mutation truth across ordinary and repair partitions.
Validation target: R21, R22, R26, R27, T10, T11, C01, C02.
Final action: Split explicit complete detailed projection from legacy JSON serialization and added dual-projection mutation regressions.
Validation evidence: `evidence/code-review-m1-r13-correction.md`; 19 exact C02 tests and 216 package tests passed.

### code-review-m1-r15

#### CLIOBS-M1-L1-F11

Finding ID: CLIOBS-M1-L1-F11
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: materialize validated controller observability in every new projection while retaining legacy output.
Rationale: R28 applies to concise JSON, concise human, and explicit detailed JSON.
Required outcome: recorded, degraded, and disabled are preserved across new projections; unknown values fail closed; legacy JSON remains exact.
Validation target: R21, R22, R26, R27, R28, T10, T11, C01, C02.
Final action: Added shared closed observability validation, explicit detailed materialization, concise-human output, and recorded/degraded/disabled regressions.
Validation evidence: `evidence/code-review-m1-r15-correction.md`; 20 exact C02 tests and 217 package tests passed.

### code-review-m1-r16

#### CLIOBS-M1-L1-F12

Finding ID: CLIOBS-M1-L1-F12
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M1
Decision owner: none
Decision needed: none
Chosen action: enforce the documented R18 human/JSON-only log inspection contract.
Rationale: log inspection is a specialized event-list surface, not a common semantic-result projection.
Required outcome: logs path/show reject `detailed-json`; human and JSON remain unchanged.
Validation target: R18, R22, R26, R27, R28, T08, T11, C01, C02.
Final action: Removed undocumented logs detailed-format acceptance and added public path/show rejection regressions.
Validation evidence: `evidence/code-review-m1-r16-correction.md`; 39 focused tests and 218 package tests passed.

### code-review-m2-r1

#### CLIOBS-M2-L1-F1

Finding ID: CLIOBS-M2-L1-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Validate bounded event fields, mandatory completion facts, non-negative duration, clock failure, and privacy-safe fallback.
Rationale: Event construction violates size, privacy, mandatory-field, and clock contracts.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: R5, R7-R9, R33, T02.
Final action: Added closed mandatory event shapes, non-negative duration validation, fail-closed clock handling, and a fixed privacy-safe fallback bounded below 16 KiB.
Validation evidence: `evidence/m2-logging-core.md`; C02 37/37 and C01 238/238 passed; code-review-m2-r4 independently confirmed this scoped correction.

#### CLIOBS-M2-L1-F2

Finding ID: CLIOBS-M2-L1-F2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Adopt a recoverable append protocol that preserves complete JSONL through combined write and rollback faults.
Rationale: Partial append plus truncate failure leaves corrupt retained JSONL.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: R14-R15, T05.
Final action: Writes now use a candidate file so a partial candidate failure cannot corrupt the retained active JSONL.
Validation evidence: `evidence/m2-logging-core.md`; combined candidate write/failure regression passed; code-review-m2-r4 independently confirmed this scoped correction.

#### CLIOBS-M2-L1-F3

Finding ID: CLIOBS-M2-L1-F3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Inject monotonic time and wait adapters and enforce attempts plus the 1,000 ms deadline.
Rationale: Held-lock acquisition exceeded the explicit time bound.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: R14, T05.
Final action: Added injectable monotonic time and wait adapters with a maximum of ten attempts and an enforced 1,000 ms budget.
Validation evidence: `evidence/m2-logging-core.md`; deterministic bound tests passed and code-review-m2-r4 measured the real held-lock path at 978.011 ms.

#### CLIOBS-M2-L1-F4

Finding ID: CLIOBS-M2-L1-F4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Implement the complete T02-T05 proof matrix and refresh exact M2 evidence.
Rationale: Current tests and evidence omit named partitions and overclaim contradicted behavior.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: T02-T05, C01, C02.
Final action: Completed the approved T02-T05 matrix, including privacy, exact-size, permissions, concurrency, interruption, fault, recovery, and resource partitions, and refreshed the identity-bound M2 evidence.
Validation evidence: `evidence/m2-logging-core.md`; C02 passed 41/41 and C01 passed 242/242; code-review-m2-r6 found no contradictory correction evidence.

### code-review-m2-r2

#### M2-L1B-F1

Finding ID: M2-L1B-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Add exact closed validators for every admitted event field and nested shape.
Rationale: Unsafe scalar objects can persist synthetic private values.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: R7-R9, T02.
Final action: Added closed type and shape validators for admitted scalar and string-list event fields; nested unsafe values fail closed.
Validation evidence: `evidence/m2-logging-core.md`; focused privacy/shape regressions passed; code-review-m2-r4 confirmed the scoped correction.

#### M2-L1B-F2

Finding ID: M2-L1B-F2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Bind no-follow file and lock cleanup to invocation-owned handle, inode, and token identities.
Rationale: Replacement races can make cleanup delete an unowned lock.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: R11-R14, T05.
Final action: Opened owned files without following final symlinks, compared pre-open/post-open device and inode identities, rechecked destructive sources immediately before mutation, and removed failed-publication pathname cleanup.
Validation evidence: `evidence/m2-logging-core.md`; direct no-unlink, replacement-lock, descriptor-closure, and adjacent-mutation tests passed; code-review-m2-r6 found no new material defect.

#### M2-L1B-F3

Finding ID: M2-L1B-F3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Isolate every diagnostic console write from semantic dispatch and result authority.
Rationale: A throwing stderr sink can abort before semantic dispatch.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: R15, T05.
Final action: Guarded diagnostic console writes so throwing stderr sinks cannot replace semantic dispatch, output, or exit behavior.
Validation evidence: `evidence/m2-logging-core.md`; controller-level throwing-sink regressions passed; code-review-m2-r4 confirmed the correction.

#### M2-L1B-F4

Finding ID: M2-L1B-F4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: Complete the distinct review's missing fault, path, privacy, timing, and resource proofs and refresh evidence.
Rationale: The approved T02-T05 proof map is incomplete and evidence is stale.
Required outcome: The corrected implementation and tests satisfy the cited contract without weakening privacy, integrity, or semantic isolation.
Validation target: T02-T05, C01, C02.
Final action: Completed the distinct fault, path, privacy, clock, concurrency, interruption, and surviving-resource tests and refreshed exact evidence identities.
Validation evidence: `evidence/m2-logging-core.md`; focused T02-T05 passed 27/27, C02 passed 41/41, and C01 passed 242/242.

### code-review-m2-r3

#### CLIOBS-M2-R3-F1

Finding ID: CLIOBS-M2-R3-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: propagate timestamp-source failure into the controller's degraded diagnostic state.
Rationale: silently replacing the failed source reports ordinary recorded observability and contradicts R33.
Required outcome: timestamp failure degrades only diagnostics while semantic output and exit remain unchanged.
Validation target: R15, R33, T02, T07.
Final action: Timestamp-source and serialization-clock failures now raise a stable internal unavailable signal that the controller projects as degraded diagnostics without changing semantic execution.
Validation evidence: `evidence/m2-logging-core.md`; direct clock probe and controller regression passed; code-review-m2-r4 confirmed the correction.

#### CLIOBS-M2-R3-F2

Finding ID: CLIOBS-M2-R3-F2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: make exclusive-lock acquisition clean up every failure after open.
Rationale: post-open `fstat` failure strands the lock and descriptor and lacks the stable unavailable classification.
Required outcome: acquisition faults leave no owned lock or descriptor and do not suppress later event attempts.
Validation target: R14-R15, T05.
Final action: Guarded acquisition and `openOwned()` as resource transactions so every tested post-open failure closes its descriptor. Approved R14 and ADR-20260825 now require retaining an unverifiable lock and bounded degradation rather than unsafe removal.
Validation evidence: `evidence/m2-logging-core.md`; acquisition and active-file post-open regressions passed; C02 39/39 and C01 240/240 passed; code-review-m2-r5 confirmed the scoped correction.

#### CLIOBS-M2-R3-F3

Finding ID: CLIOBS-M2-R3-F3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: remove the final pathname check/use race from lock cleanup.
Rationale: a replacement introduced after the inode check is still deleted by the separate unlink.
Required outcome: cleanup never removes a lock object not owned by the current invocation.
Validation target: R11, R14, T05, INT-002.
Final action: Removed failed-publication pathname unlink cleanup. Approved R11 and ADR-20260825 explicitly exclude a same-user or privileged process that replaces pathnames after validation and prohibit race-proof-containment claims.
Validation evidence: `evidence/m2-logging-core.md`; no-unlink and replacement-lock preservation regressions passed; spec-review-r3 and architecture-review-r2 approved the exact boundary.

#### CLIOBS-M2-R3-F4

Finding ID: CLIOBS-M2-R3-F4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: complete the missing direct T02-T05 partitions and correct M2 evidence claims.
Rationale: in-memory privacy and ordinary-concurrency tests do not prove retained surfaces, interruption, concurrent rotation, acquisition recovery, destructive races, or descriptor cleanup.
Required outcome: every named M2 completion criterion has current identity-stable proof and evidence states only demonstrated outcomes.
Validation target: T02-T05, C01, C02, PRF-005, PRF-008, PRF-010.
Final action: Added direct retained-surface privacy, concurrent rotation, interruption, acquisition recovery, descriptor cleanup, and destructive-boundary proofs; revised evidence now names only demonstrated outcomes.
Validation evidence: `evidence/m2-logging-core.md`; T02-T05 passed 27/27; code-review-m2-r6 reconciled the current proof inventory without a new finding.

### code-review-m2-r4

#### CLIOBS-M2-R4-F1

Finding ID: CLIOBS-M2-R4-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: architecture owner if the approved invariant is not implementable with the selected Node filesystem interface
Decision needed: none unless bounded implementation cannot preserve R11/R14
Chosen action: bind validated root and owned identities through publication, archive deletion, and archive rename operations.
Rationale: deterministic replacement probes published or deleted unowned files and rotated a substituted external root.
Required outcome: destructive filesystem operations cannot target an object or root substituted after validation.
Validation target: R11, R14, T04, T05, INT-002.
Final action: Added a shared pre-mutation validator that rechecks the root, existing components, and every owned entry, then verifies the destructive source identity as the final operation before each unlink or rename. The approved R11/ADR boundary explicitly excludes a same-user or privileged replacement after that check.
Validation evidence: `evidence/m2-logging-core.md`; the six-site operation-order regression and fail-before-mutation fault regression passed; C02 passed 41/41 and C01 passed 242/242.

#### CLIOBS-M2-R4-F2

Finding ID: CLIOBS-M2-R4-F2
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: reconcile the accepted retry outcome with the safety-first stale-lock behavior before implementation closeout.
Chosen action: close every post-open descriptor and implement or formally revise usable-retry recovery.
Rationale: `openOwned()` leaks a descriptor after `fstatSync` failure, while retained acquisition locks suppress later attempts.
Required outcome: resource faults leave no leaked descriptor and recovery matches the approved disposition.
Validation target: R14-R15, T05.
Final action: Added close-on-failure to `openOwned()` and retained safety-first stale-lock behavior under the revised approved R14 contract.
Validation evidence: `evidence/m2-logging-core.md`; active-file `fstat` failure closes both opened descriptors; C02 39/39 and C01 240/240 passed.

#### CLIOBS-M2-R4-F3

Finding ID: CLIOBS-M2-R4-F3
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: validate event kind and sequence as one closed pair.
Rationale: start/complete events currently accept each other's fixed sequence.
Required outcome: start accepts only sequence 1 and completion accepts only sequence 2.
Validation target: R5, T02.
Final action: Added a closed event-to-sequence mapping: start requires 1 and completion requires 2.
Validation evidence: `evidence/m2-logging-core.md`; exact crossed-pair regression passed; C02 39/39 and C01 240/240 passed.

#### CLIOBS-M2-R4-F4

Finding ID: CLIOBS-M2-R4-F4
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: add exact regressions for every R4 reproduction and correct the M2 evidence inventory and claims.
Rationale: green focused and package suites do not cover the destructive races, descriptor leak, or fixed event ordering.
Required outcome: direct tests fail on the reviewed target, pass after correction, and evidence reports only demonstrated properties for all twelve prior findings plus R4.
Validation target: T02-T05, C01, C02, PRF-005, PRF-008, PRF-010.
Final action: Added exact crossed-sequence, descriptor-fault, adjacent pathname-validation, and validation-failure regressions and refreshed the M2 evidence identities and claims.
Validation evidence: `evidence/m2-logging-core.md`; focused T02-T05 passed 27/27, C02 passed 41/41, and C01 passed 242/242.

### code-review-m2-r5

#### CLIOBS-M2-R5-F1

Finding ID: CLIOBS-M2-R5-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: add one injected pre-mutation validator for root, components, affected source, and existing destination and call it immediately before every owned unlink or rename.
Rationale: the early whole-root check and source-only identity assertions do not implement the approved R11 check cadence.
Required outcome: every destructive pathname operation has adjacent deterministic validation and a direct operation-order/fault regression.
Validation target: R11, R13-R15, T04, T05, INT-002.
Final action: Added one injected validator immediately before all archive deletion, archive renames, active rotation, and lock publication. It checks the root, components, all owned entries including an existing destination, and the exact source identity before mutation.
Validation evidence: `packages/rigorloop/test/cli-observability.test.js` T05 operation-order and validation-fault regressions; `evidence/m2-logging-core.md`; C02 passed 41/41 and C01 passed 242/242.

### code-review-m2-r6

The local L0 rereview found no new material implementation issue and reconciled all seven formerly open M2 findings against current direct proof. It is inconclusive for workflow promotion because automated reviews cannot advance at L0. No new finding disposition is required. M2 remains review-requested pending an L1-or-higher review.

### code-review-m2-r7

The fresh L1 independent review returned `clean-with-notes` with no material findings on frozen M2 bundle `sha256:a8ccc19505fef9e6243859dba71da3ecfd803575d43db2170b71922cb9c3d3f8`. It directly challenged privacy, all six destructive R11 mutation intervals, no-follow and identity behavior, containment, unsafe and ordinary I/O failures, partial rotation at every rename/unlink position, concurrent writers, bounded locks, semantic isolation, and proof adequacy. C02 passed 41/41, C01 passed 242/242, and the additional six-position partial-rotation probe retained only complete bounded JSONL. No finding disposition is required. M2 remains review-requested and no lifecycle state advances until a distinct second clean independent review agrees.

### code-review-m2-r8

Finding ID: CLIOBS-M2-R8-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: reject existing non-directory intermediate components through the stable unsafe-path boundary and add direct T04 proof.
Rationale: the component walker rejects symlinks but allows a regular-file component to reach a child `lstat`, which leaks raw `ENOTDIR` instead of `RL_LOG_UNSAFE_PATH`.
Required outcome: an intermediate regular-file component fails before mutation with `RL_LOG_UNSAFE_PATH`, preserves the existing sentinel, and creates no owned log entry.
Validation target: R11, T04, C02, C01, and fresh M2 rereview.
Final action: The component walker now rejects an existing non-directory component with `RL_LOG_UNSAFE_PATH`; the identity-equal T04 fixture preserves the sentinel and proves no nested root is created.
Validation evidence: `packages/rigorloop/test/cli-observability.test.js` passed 27/27; C02 passed 41/41; C01 passed 242/242; code-review-m2-r9 independently reproduced the corrected result and found no adjacent R11/T05 regression.

### code-review-m2-r9

The fresh L1 correction rereview returned `clean-with-notes` with no material findings on corrected frozen M2 bundle `sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190`. `CLIOBS-M2-R8-F1` is resolved. This is the first clean review of the corrected bundle and does not advance lifecycle state; a distinct second clean review is still required.

### code-review-m2-r10

The distinct fresh L1 review returned `clean-with-notes` with no material findings on the identical corrected frozen M2 bundle `sha256:bcaca1334372260838357d8a4d3401886bfaa51a77e105de2fdd9b5453002190`. It independently reproduced intermediate-regular-file `RL_LOG_UNSAFE_PATH` classification with sentinel preservation and no creation; all six adjacent destructive mutation intervals; ordinary-I/O unavailable/no-mutation behavior; every partial-rotation unlink/rename fault position; post-open identity refusal; privacy; concurrency; resource bounds; and current evidence identities. R9 and R10 therefore establish the required distinct clean agreement on the identical hash. No finding disposition is required. This isolated review does not mutate lifecycle state; workflow owns M2 settlement and routing.

### code-review-m2-r11

#### CLIOBS-M2-R11-F1

Finding ID: CLIOBS-M2-R11-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: correct bounded descriptor release for close-before-release faults, add direct active-read, ordinary-validation, and rotation-handle regressions, and refresh M2 evidence and frozen identity before rereview.
Rationale: T05 and the M2 evidence require no descriptor to survive a faulted append. The existing close-failure test closes the descriptor before throwing, while the fresh probe throws before close and proves the active descriptor remains valid after the API returns.
Required outcome: every descriptor opened by the logging sink is invalid after the append attempt returns, including when the first close attempt fails; stable degraded observability and semantic isolation remain unchanged.
Validation target: R13-R15, R34, T05, C02, C01, corrected M2 evidence, new bundle identity, and fresh holistic M2 rereview.
Final action: Centralized every sink-owned release in `closeOwned`. After an injected close failure it uses trusted native `fstatSync`, treats `EBADF` as already closed, refuses a known device/inode mismatch, otherwise makes one trusted native cleanup close, and preserves stable diagnostic failure. Added active-read, ordinary-validation, and five rotation-held throw-before-close regressions with post-return `EBADF`.
Validation evidence: `evidence/m2-logging-core.md`; C02 passed 42/42; C01 passed 243/243; code-review-m2-r12 reproduced post-return `EBADF`, already-closed handling, and same-number different-inode mismatch refusal on bundle `sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff`.

### code-review-m2-r12

The fresh L1 correction rereview returned `clean-with-notes` with no material findings on corrected frozen M2 bundle `sha256:841c0e493c27f76981964a5a123b868846d86e8b9c716f03d9ba3f686d5bcfff`. `CLIOBS-M2-R11-F1` is resolved. This is the first clean review of the new corrected bundle and does not advance lifecycle state; a distinct second clean independent review of the identical hash is still required.

### code-review-m2-r13

#### CLIOBS-M2-R13-F1

Finding ID: CLIOBS-M2-R13-F1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: implement M2
Decision owner: none
Decision needed: none
Chosen action: correct identity-unknown acquisition cleanup so a close adapter cannot cause trusted cleanup to close a different inode that reused the same descriptor number.
Rationale: after acquisition `fstatSync` fails, `closeOwned(fd, null, io)` has no expected identity; a direct close/reopen/throw probe proved that trusted cleanup then closes the unowned replacement descriptor.
Required outcome: every post-open acquisition fault releases only the originally owned descriptor, never a same-number replacement, while preserving stable `RL_LOG_UNAVAILABLE`, fail-closed lock retention, and all existing known-identity cleanup guarantees.
Validation target: R13-R15, R34, T05, the acquisition-failure and descriptor-reuse probes, C02, C01, corrected M2 evidence, a new frozen identity, and fresh holistic independent review agreement.
Final action: `acquire()` now captures trusted device/inode identity immediately after opening the lock and before invoking the injected identity inspection. On later close failure, cleanup checks that identity and refuses a same-number different-inode replacement; trusted-capture failure uses native close on the still-owned descriptor.
Validation evidence: code-review-m2-r14 directly reproduced injected acquisition `fstatSync` failure plus close/reopen/throw and observed `RL_LOG_UNAVAILABLE`, retained fixed lock, valid replacement descriptor, and fail-closed subsequent attempt. The targeted four-test descriptor matrix, independent already-closed and known-identity mismatch probes, C02 43/43, and C01 244/244 passed on bundle `sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f`.

### code-review-m2-r14

The fresh L1 correction rereview returned `clean-with-notes` with no material findings on corrected frozen M2 bundle `sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f`. `CLIOBS-M2-R13-F1` is resolved. This is the first clean review of the new corrected bundle and does not advance lifecycle state; a distinct second clean independent review of the identical hash is still required.

### code-review-m2-r15

The distinct second fresh L1 holistic review returned `clean-with-notes` with no material findings on the identical corrected frozen M2 bundle `sha256:e6de92ecf6a84f9b20b05d28d0773d1b99b9c0c0060c4d882c05473e601c907f`. R14 and R15 establish distinct clean agreement on the identical hash, so the M2 code-review gate may be consumed by workflow. This review evidence does not itself mutate lifecycle state or routing.

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
