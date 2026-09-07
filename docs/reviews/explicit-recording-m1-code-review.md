# Explicit Recording M1 — Advisory Code Review

## Authority and reviewed scope

This is an independent, isolated first-pass Code Review under the user's explicit M1-only implementation exception. The reviewer authored none of the implementation. The basis is the [Workflow model](../design/workflow.md), [CLI model](../design/cli.md), [delivery plan](../plans/2026-09-05-explicit-recording-and-model-centered-design.md), their advisory Design and Delivery rereviews, and [implementation evidence](../implementation/explicit-recording-m1.md). The two unified model files and absence of OS investigation remain authorized scope choices.

There is no registered change root, formal upstream gate ID, or formal milestone settlement. This record provides advisory judgment only. M2 persistence, current filesystem freshness, public command implementation, activation, migration, and unrelated preexisting working-tree changes are outside review scope. Public writers must remain disabled. No implementation was corrected before recording these findings.

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: ER-M1-001, ER-M1-002, ER-M1-003
- Artifacts changed: this advisory review only
- Open blockers: three representation defects below; no additional owner decision needed
- Next stage: isolated M1 implementation correction and independent rereview, only under user authority; no automatic downstream handoff
- Recording status: recorded (advisory only)
- Recording blocker: none for this explicitly assigned advisory location; formal settlement remains unavailable
- Review record: `docs/reviews/explicit-recording-m1-code-review.md`
- Review log: not applicable
- Review resolution: finding disposition belongs in this advisory record
- Reviewed milestone: M1 foundations, isolated exception
- Milestone closeout: not claimed; corrections required
- Remaining implementation milestones: M2–M5 remain outside this authorization
- Required review-resolution: correct and rereview all three findings
- Finding IDs: ER-M1-001, ER-M1-002, ER-M1-003
- Verify readiness: not-claimed

## Exact reviewed implementation identities

SHA-256 identifies the complete new files, not the unrelated branch diff.

| Path | SHA-256 |
| --- | --- |
| `schemas/explicit-recording-v1.schema.json` | `5d5f163061ce656f9c9bd8a26a592d1537743915be1255c1b0d42c99ade92ce1` |
| `packages/rigorloop/dist/schemas/explicit-recording-v1.schema.json` | `5d5f163061ce656f9c9bd8a26a592d1537743915be1255c1b0d42c99ade92ce1` |
| `packages/rigorloop/dist/lib/record-store-contract.js` | `153aa226c1c34aacb3b61c78054d3d5f0a0470523b0b508853843e56690d9deb` |
| `packages/rigorloop/test/record-store-contract.test.js` | `cf94758b2b96728ec0b2dcbffac71ba833a308f69b2688d2745486be890e23cb` |
| `scripts/build-record-store-schema.mjs` | `9021467a9492d39d2491b6d39b9debfc70abda5ad261f8172571e675a39d417b` |
| `tests/fixtures/explicit-recording-v1/records.json` | `d26bcaf4b366160e55968f56e9c39d4d22e418689ee2b80ed12e215c803f856c` |
| `docs/implementation/explicit-recording-m1.md` | `009593beda36bde1843fa7ae12501cc20e32da9318ee1915d039289684e92c17` |

## First-pass material findings

### ER-M1-001 — Reject overlapping decision-basis and replacement paths

- Severity: major
- Owner: implementation, M1; CLI model
- Location: `packages/rigorloop/dist/lib/record-store-contract.js:107`
- Evidence: Request validation checks uniqueness separately within `writes` and `reads` but never across them. A valid fixture request with `reads` replaced by `[{path: request.writes[0].path, expected_identity: null}]` is accepted. CLI model line 72 rejects duplicate request paths; line 143 explicitly states decision-basis files are outside the recorder's write set. This is a request representation rule, not an M2 filesystem freshness test.
- Required outcome: Reject any request whose declared read set overlaps its write set, while retaining support for distinct external decision-basis paths.
- Safe resolution path: Add a focused otherwise-valid overlapping request regression, then enforce disjoint path membership during request validation. Rereview the bounded correction; do not add persistence or change the Design.

### ER-M1-002 — Do not collapse distinct diagnostics onto path identity

- Severity: major
- Owner: implementation, M1; CLI model
- Location: `packages/rigorloop/dist/lib/record-store-contract.js:66`
- Evidence: Generic array validation treats every object containing `path` as uniquely identified by that path. Appending a distinct `subject-drift` observation for the same path as the fixture's `failed-evidence` observation rejects the otherwise-valid result with `duplicate identity or path`. CLI model lines 101 and 109 permit diagnostic objects describing different factual conditions; neither assigns diagnostic identity to path. Multiple non-path-specific diagnostics also share null. The schema's whole-item uniqueness does not imply path-only uniqueness for diagnostics.
- Required outcome: Permit distinct diagnostics for the same path, including null, without weakening actual ID/path uniqueness requirements on registries, references, request targets or snapshot members.
- Safe resolution path: Scope uniqueness rules to their owning representations and add positive same-path and null-path diagnostic tests alongside negative identity/path tests. Rereview the correction.

### ER-M1-003 — Validate inspected snapshot content and membership

- Severity: major
- Owner: implementation, M1; CLI model
- Location: `packages/rigorloop/dist/lib/record-store-contract.js:119`
- Evidence: `validateResult` checks only snapshot/files length, path order, allowed path and content digest. An inspected result containing `change.yaml` content `not a manifest\n` and its correct digest is accepted. An empty inspected snapshot/files pair retaining a non-null revision and no absent-change observation is also accepted. CLI model line 103 requires valid encoded Workflow records, manifest-derived membership, explicit missing-sidecar representation, and the specific absent-root result; malformed manifests must instead be rejected with null snapshot. The fixture exercises only record/saved results, so the passing suite does not demonstrate these inspected cases. The current path/hash check also bypasses authoritative content parsing and its 1 MiB limit.
- Required outcome: Validate the representation of inspected snapshots against the parsed manifest and existing record encodings/limits, with exact registered membership and record identities, missing-supporting-file nulls accompanied by subject-drift, and the prescribed empty absent-root shape. Do not accept malformed manifests as usable inspected snapshots. Do not require live filesystem observation or semantic lifecycle eligibility in M1.
- Safe resolution path: Add valid inspected, absent-root and missing-sidecar fixtures, then otherwise-valid negative tests for malformed/oversized content, incorrect registry membership and absent-root fields. Reuse bounded representation validation while preserving the contract's allowance for absent referenced historical subjects. Rereview before M1 closeout.

## Checklist coverage

| Item | Assessment | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Three direct CLI representation mismatches above; no justification to alter approved model direction. |
| Test coverage | concern | Twelve focused tests pass, but saved-only result fixture misses inspected representation; targeted probes expose accepted invalid/rejected valid cases. |
| Edge cases | concern | Cross-array overlap and empty/missing snapshots require direct regressions; exact limits and ID/path boundaries otherwise have focused tests. |
| Error handling | concern | Distinct diagnostics are falsely rejected and malformed inspected content is accepted. |
| Architecture boundaries | pass | New representation-only module has no CLI dispatcher, writer, semantic eligibility or lifecycle mutation. |
| Compatibility | pass | New discriminator is isolated; historical/unknown discriminator rejection and unavailable public command have focused tests. |
| Security/privacy | concern | Snapshot file-size/encoding validation is bypassed; no public mutation or logging expansion in this slice. |
| Derived artifact currency | pass | Canonical and packaged schema hashes match; generator and focused parity test inspected. |
| Unrelated changes | pass | Review limited to the seven explicit new files; unrelated dirty work preserved and not approved. |
| Validation evidence | concern | Named regressions pass, but passing broad checks cannot cover the demonstrated representation gaps. |

## Commands and evidence actually examined

The reviewer ran `node --test packages/rigorloop/test/record-store-contract.test.js`: 12 passed, zero failed. The reviewer also ran read-only `node --input-type=module` fixture probes invoking `validateRecordStoreRecord`, which produced: overlapping read/write accepted; two distinct observations sharing a path rejected; malformed manifest inspected result accepted; empty inspected snapshot with non-null revision and no absent observation accepted. File inspection used `sed`, `rg`, and `nl`; `sha256sum` supplied the identities above.

The implementation owner's recorded evidence reports `npm --prefix packages/rigorloop test` (486 total, 484 passed, two skipped), `python scripts/test-change-metadata-validator.py` (112 passed), `node scripts/build-record-store-schema.mjs --check` and `git diff --check` (exit 0). Those broader checks were not independently rerun by this reviewer. Their success is not whole-branch approval. Some malformed-input tests use otherwise-invalid unknown-field payloads, so they do not independently isolate every parser failure; corrective tests should use otherwise-valid fixtures where possible.

This first-pass record precedes any fixes. No formal gate, branch readiness, Verify, PR readiness, M2 permission or automatic continuation is claimed.

## Independent bounded rereview — current advisory judgment

The first-pass findings and identities above remain historical evidence. This section records independent review of the subsequent M1-only corrections, not a formal gate or lifecycle settlement. Only the validator module and focused tests changed in the reviewed implementation; the unchanged schema, generator and fixture retain their first-pass identities. Implementation evidence may separately be updated by its owner with broader validation results.

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Material findings: none remain open in the reviewed M1 slice
- Finding disposition: ER-M1-001 resolved; ER-M1-002 resolved; ER-M1-003 resolved
- Recording status: recorded (advisory only, in this same record)
- Artifacts changed by reviewer: this review only
- Next stage: stop at the authorized M1 boundary; no automatic downstream handoff
- Milestone closeout: advisory M1 review is clean; formal milestone settlement not claimed
- Remaining implementation milestones: M2–M5 remain outside the M1 exception
- Required review-resolution: none outstanding for these three findings
- Verify readiness: not-claimed

### Corrected implementation identities

| Path | SHA-256 |
| --- | --- |
| `packages/rigorloop/dist/lib/record-store-contract.js` | `1006f2efc7c97765cde9a47e6b32d8b87adcb7c37c36b65aaa32479ad54fb0ab` |
| `packages/rigorloop/test/record-store-contract.test.js` | `42917b55f9e67739b987e978c87314b2f4986548cfb407c6cd0a3fd92022cc03` |
| `docs/implementation/explicit-recording-m1.md` | `3dfc7e53a04e49c3c91421c532500af8632610711e25d2c8af7c444c8c46f2c8` |

### Disposition and direct proof

| Finding | Independent assessment | Direct proof |
| --- | --- | --- |
| ER-M1-001 | Resolved. Request validation checks all read paths against the complete write-path set before parsing replacement content. This implements CLI model lines 72 and 143 without adding live freshness or persistence. | `ER-M1-001 decision-basis and write paths are disjoint` accepts the original request and rejects an otherwise-valid overlapping path with the specific overlap failure. |
| ER-M1-002 | Resolved. Diagnostic uniqueness now uses the complete code/path/message tuple, while ID/path uniqueness on other arrays remains unchanged. | `ER-M1-002 distinct diagnostics may share a path or no path` accepts both observation and error pairs sharing a concrete path or null. Existing duplicate registry/model/finding and candidate tests continue passing. |
| ER-M1-003 | Resolved. Inspected results parse the manifest and present supporting content using existing bounded encodings, enforce exact registry membership and change/review identities, preserve missing supporting records with null content/digest and subject-drift, and validate the byte-derived revision. Empty snapshots require null revision and absent-change. Inspection does not invoke complete-candidate foreign-key validation, so missing-support repair remains representable. | Two `ER-M1-003` tests accept complete, absent-root and missing-sidecar inspection and reject malformed/null/oversized manifests, extra/omitted members, incorrect record identities, missing observations and incorrect absent/current revisions. Positive cases also pass through the public parser helper. |

The additional `TG-01 duplicate keys are rejected in otherwise valid records` test directly isolates ordinary, escaped and nested duplicate-key rejection using an otherwise-valid manifest. This addresses the first-pass test-quality note without expanding the contract.

### Current checklist and limitations

All ten checklist items were reconsidered for the bounded correction. Spec alignment, test coverage, edge cases, error handling and security/privacy concerns identified in the first pass are addressed by the checks and targeted tests above. Architecture boundaries, compatibility, generated schema parity and unrelated-change isolation remain intact. Validation evidence supports this representation-only slice: it does not demonstrate filesystem transactions, live snapshot coherence, recovery, public command behavior beyond its continued unavailability, or final whole-change readiness.

Commands independently run for rereview: `node --test packages/rigorloop/test/record-store-contract.test.js` (17 passed, zero failed), `node scripts/build-record-store-schema.mjs --check` (exit 0), and `sha256sum` for both corrected files. The reviewer inspected the complete changed module/test content and compared revision calculation with CLI model line 76. Broader regression results remain implementation-owner evidence rather than a claim that this reviewer reran them. No implementation, Design, plan, registration, settlement or activation was changed by this rereview.

Before final handoff, the reviewer read and hashed the final implementation evidence. It records post-correction `npm --prefix packages/rigorloop test` (491 total, 489 passed, two skipped, zero failed), Python metadata validation (112 passed), schema parity and whitespace checks (exit 0). These are owner-run results, with skipped tests explicitly preserved. The review-only `git diff --check -- docs/reviews/explicit-recording-m1-code-review.md` also passed independently.
