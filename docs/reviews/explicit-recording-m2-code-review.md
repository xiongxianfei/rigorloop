# Explicit Recording M2 — Pre-implementation Blocker

## Advisory result

- Skill: code-review
- Status: blocked
- Review status: blocked
- Recording status: recorded (advisory only)
- Material finding: ER-M2-001
- Scope: command/result contract preflight for isolated M2; no complete M2 implementation exists or has been reviewed
- Implementation checklist: not assessed; implementation review target is absent
- Next action: CLI Design owner resolves the selector-error representation, followed by affected independent review before implementation resumes
- Automatic downstream handoff: none
- Formal lifecycle settlement, milestone closeout and Verify readiness: not claimed

The independent reviewer inspected the CLI model, M2 delivery allocation, M1 result schema/validator and existing dispatcher. This is not approval or rejection of nonexistent M2 persistence code. The user authorized M2 implementation, but ordinary activation remains withheld until M4.

## ER-M2-001 — Selector failures lack a representable result identity

- Severity: major
- Owner: CLI model, Design stage
- Location: `docs/design/cli.md:94`, `docs/design/cli.md:101`; `schemas/explicit-recording-v1.schema.json:115`, `schemas/explicit-recording-v1.schema.json:802`, `schemas/explicit-recording-v1.schema.json:808`
- Evidence: The command contract rejects missing, malformed and contradictory selectors and unknown command arguments. Every JSON result nevertheless requires an operation from the four-command vocabulary and a Workflow change ID. The schema allows neither null nor unavailable selector identities. A missing/invalid `--change`, or unknown subcommand, cannot produce a faithful schema-valid result without fabricating a value or introducing an unspecified error envelope. The legacy dispatcher's `invalidUsage` at `packages/rigorloop/dist/bin/rigorloop.js:1749` returns another command envelope; that is not a defined exception to this new contract. M2 requires direct argument-error and JSON public-boundary proof at `docs/plans/2026-09-05-explicit-recording-and-model-centered-design.md:97`.
- Required outcome: Define the truthful machine-readable rejection shape when operation or change identity is unavailable, retaining safe diagnostics, closed vocabulary and no writes. Valid selectors must not be replaced by fabricated sentinel identities.
- Safe resolution path / needs-decision: The CLI Design owner must choose a bounded representation rule. Allowing null unavailable operation/change_id only for rejected input errors is a small option; a separately documented pre-dispatch usage-error envelope is an alternative. This reviewer does not select or implement that Design change. Update the affected contract and obtain the appropriate independent review before schema/parser implementation.

## Boundaries and evidence

M2's non-adopted fixture access is not itself a blocker: plan lines 93–103 explicitly require isolated roots, real CLI subprocess tests and no ordinary activation. Future proof must exercise the actual dispatcher/parser/rendering/storage boundary; helper-only tests cannot substitute. No OS investigation or extra engineering artifact split is required.

This preflight used read-only `sed` and `rg` inspection; no M2 execution proof was run. The implementation owner reports the retained M1 focused suite at 17 passed and `git diff --check` passing. These are not M2 proof. This record precedes correction. The reviewer changed only this advisory record, not Design, schema, implementation or lifecycle state.

## ER-M2-001 disposition — Design clarification resolved

The original blocked preflight above remains historical evidence. Following the user's authorization, the CLI Design owner selected the narrow nullable-unavailable-selector rule in `docs/design/cli.md`, Result schema and exit behavior. Independent rereview of both complete model members is recorded in [the advisory Design review](explicit-recording-and-model-centered-design.md), under Selector-error clarification.

Disposition: resolved at Design. Null operation/change_id now has a precise rejected invalid-input envelope, available selectors remain truthful, invalid/repeated format has a safe fallback, and argument errors access neither repository nor stdin. No fabricated identity or second unspecified usage envelope is needed.

Current preflight status: Design blocker cleared. M2 implementation Code Review remains not performed, and its checklist remains unassessed until the implementation target and proof exist. The schema/parser must implement the clarified contract and undergo independent Code Review. This disposition does not certify unchanged M1 schema compatibility with the new rule, grant execution authority, activate public writers or settle lifecycle state. Any M2 continuation relies on the user's separate explicit authorization.

## First implementation Code Review — current advisory result

The preflight and Design disposition above remain historical evidence. An M2 implementation now exists and was independently reviewed against both model documents, the advisory Design/Delivery basis and M1 rereview. The reviewer authored none of the implementation and made no fixes before recording this result. Review covers only the explicit M2 files below; unrelated dirty work is neither changed nor approved.

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: ER-M2-002, ER-M2-003, ER-M2-004
- Recording status: recorded (advisory only)
- Review record: `docs/reviews/explicit-recording-m2-code-review.md`
- Review log / separate resolution record: not applicable; dispositions remain here
- Reviewed milestone: M2, isolated user authorization
- Milestone closeout: withheld; required safety corrections remain
- Required review-resolution: all three findings require correction and independent rereview
- Remaining implementation milestones: M3–M5 remain outside this authorization
- Next owner: M2 implementation owner; no automatic downstream handoff
- Verify readiness: not-claimed
- Claim limits: no formal lifecycle settlement, ordinary activation, whole-branch review, M3 permission, hosted CI or PR readiness

### Exact reviewed implementation identities

| Path | SHA-256 |
| --- | --- |
| `packages/rigorloop/dist/lib/record-store-files.js` | `371b7483fc1994b1676f6cd7a017572886e4957c4e125574d32391e570ecb3d0` |
| `packages/rigorloop/dist/lib/record-store.js` | `c1320542b87c86e037eb7fd1c51f7e831f3533c9e1fccf5780902d17c273fb78` |
| `packages/rigorloop/dist/lib/record-store-cli.js` | `f66067a6f9b8d825e3427cd9119474357ceae0b30065cf95968e5352b4daf676` |
| `packages/rigorloop/dist/lib/record-store-contract.js` | `72a9813be174d2fdeb9dd8c552a5c23fda916befa8d2338107b130ea5f90f458` |
| `schemas/explicit-recording-v1.schema.json` | `3c5c78689dcd2fe31a43bf3b48c684c2c7dcaea3729b67b76b049e1531de38c2` |
| `packages/rigorloop/dist/schemas/explicit-recording-v1.schema.json` | `3c5c78689dcd2fe31a43bf3b48c684c2c7dcaea3729b67b76b049e1531de38c2` |
| `packages/rigorloop/dist/bin/rigorloop.js` | `0ed7599eb24ed50d238dfbf17a25218584c437444119d1ab078d7d4d44ab17ef` |
| `packages/rigorloop/test/record-store-cli.test.js` | `b34477eb621b8c5b324e67a609b74d0671b13b02206e9cff7307302799a799da` |
| `packages/rigorloop/test/helpers/record-store-launcher.mjs` | `74db14c1aa5f589addf1c9c1a7904ff56332b7010b389914fb92c7d2afbd3fac` |
| `packages/rigorloop/test/record-store-contract.test.js` | `a657757a9e749e3c92e84072f4804f93f293bad348d46ed2b18171e7cbeb3149` |
| `docs/implementation/explicit-recording-m2.md` | `e2ba3c7a635a8a7316d928d8adad2de3a4a4f48f8032cd665236a856c82f10b8` |

### ER-M2-002 — Recheck recovery exclusion after acquiring the writer lock

- Severity: major
- Owner: implementation, M2
- Location: `packages/rigorloop/dist/lib/record-store.js:207`, `:210`, and `acquire` at `:115`
- Evidence: `snapshot()` checks the recovery gate before lock acquisition, but after acquisition `record()` only rereads candidate bytes/preconditions. An intervening writer can prepare a journal and stop before publishing, leaving the original before-state unchanged. The waiting writer then passes its stale gate assumption, overwrites the prepared journal and removes it on success. A deterministic probe interposed at `RecordFiles.write` for the first writer's lock creation: a second writer ran the same valid request and stopped at `after-preparation`; it returned `recovery-required`. The original writer then returned `saved`, and the journal no longer existed. This violates CLI-SR-05/06 and the rule that unfinished transactions require explicit recovery rather than another record operation.
- Required outcome: Once writer exclusion is acquired, detect and preserve any pending journal before ordinary recording can prepare or publish another transaction. Losing a race must return busy/conflict/recovery-required without replacing recovery evidence.
- Safe resolution path: Add the interleaving regression and revalidate recovery ownership under the acquired exclusion boundary. Include pending prepared and committed journals and preserve their identities. No new workflow decision or OS policy is needed.

### ER-M2-003 — Never promote a newly observed third state into authorized replacement identity

- Severity: major
- Owner: implementation, M2
- Location: `packages/rigorloop/dist/lib/record-store.js:189`, especially `:194`
- Evidence: `publish()` first calls `known(j)`, then separately hashes each target and passes that fresh value as the expected identity to `write`/`remove`. A concurrent third-state edit between the known-state check and the fresh hash becomes the accepted compare-and-swap basis instead of a stop. The reviewer interposed at the direct `Store.publish` hash (after `Store.known`, before `RecordFiles.write`), wrote `external-third-state\n` to the manifest, then returned its actual digest. The operation returned `saved` and replaced those external bytes with its candidate. This is a lost update under CLI-SR-04 and violates CLI-SR-06's prohibition on overwriting a state matching neither before nor candidate. The shared method is used by recovery and restoration as well as ordinary save.
- Required outcome: The actual value used as the replacement precondition must itself be one of the exact authorized before/candidate identities, with committed-phase restrictions preserved. A newly observed external value must never acquire authorization merely because it was just read.
- Safe resolution path: Add a targeted third-state interleaving test at this exact boundary, then bind publication/removal preconditions to the journal's permitted identities. Rereview candidate, restore and committed cleanup paths together; this finding is distinct from pathname containment below.

### ER-M2-004 — Post-mutation ancestor checks cannot prevent escaped writes

- Severity: major
- Owner: implementation, M2
- Location: `packages/rigorloop/dist/lib/record-store-files.js:90` and the shared pathname-based mutation boundary
- Evidence: The last ancestor/hash validation precedes pathname-based rename. A parent substitution after that validation redirects rename before the post-rename assertion can stop it. A deterministic probe prepared an ordinary update, intercepted the second target hash inside `RecordFiles.write`, moved the prepared temporary file into a separate temporary directory outside the repository root, renamed the original change directory aside, and substituted a symlink to that outside directory. The ensuing rename overwrote the outside directory's preexisting `change.yaml` with candidate bytes. The CLI returned `recovery-required`, but the out-of-root overwrite had already occurred. The existing ancestor-substitution test acts at `before-replace:0`, before validation, and therefore misses this window. CLI-SR-09 expressly requires protection against concurrent substitution, not merely detection after damage.
- Required outcome: Publication, removal and exclusive creation must not resolve a substituted ancestor into an unauthorized target at the moment of mutation. Safe failure must preserve outside and unknown bytes, not only change the returned status.
- Safe resolution path: Add a direct late-substitution regression and repair the shared mutation boundary so target containment is maintained through the operation. Audit sibling recovery/removal/creation paths using the same primitive. This asks for the existing observable protection, not an OS selection or investigation. If the implementation cannot meet that contract within current execution assumptions, stop for an explicit owner decision rather than silently weaken it.

### Checklist

| Item | Assessment | Evidence |
| --- | --- | --- |
| Spec alignment | concern | ER-M2-002/003/004 contradict existing recovery, conflict and containment outcomes. |
| Test coverage | concern | All 38 focused tests pass, but the three narrower late interleavings above are uncovered. |
| Edge cases | concern | Pending-journal takeover and third-state mutation windows need direct proof; normal retry and interrupt cases are exercised. |
| Error handling | concern | Recovery-required after an escaped overwrite is not safe rejection. |
| Architecture boundaries | pass | Explicit recorder does not invoke lifecycle eligibility; fixture launcher uses the actual dispatcher/parser/renderer/storage modules. |
| Compatibility | pass within reviewed isolation | Ordinary entry remains unavailable, historical tests stay separate, and the bin symlink path has focused proof; ordinary observability/adoption remains unproved and deferred. |
| Security/privacy | concern | Containment fails at a late mutation window; selector diagnostics otherwise preserve the clarified safe rejection shape. |
| Derived artifact currency | pass | Canonical/package schema bytes match; parity command passes. |
| Unrelated changes | pass | Only named M2 surfaces assessed; no implementation or unrelated work edited by reviewer. |
| Validation evidence | concern | Passing focused and owner-reported broad checks do not establish the missing negative outcomes. |

### Commands, proof and limitations

Independently run: `node --test packages/rigorloop/test/record-store-contract.test.js packages/rigorloop/test/record-store-cli.test.js` (38 passed, zero failed), `node scripts/build-record-store-schema.mjs --check` (exit 0), `sha256sum` for the exact subjects, and read-only source/diff inspection. Three `node --input-type=module` manual probes used disposable temporary roots and runtime method interposition solely to schedule the documented concurrent filesystem/second-writer actions. No source monkeypatch was persisted. Their concrete results are recorded in each finding. The containment probe modified only reviewer-created temporary data, never real outside user files.

The implementation evidence reports full package regression at 513 total / 511 passed / two skipped / zero failed, whitespace checks and a package dry run excluding the test launcher. Those broader commands were not independently rerun by this reviewer. The fixture launcher intentionally does not prove ordinary activation or the future observability integration. No operating-system investigation or new Design sidecar was requested.

This implementation first-pass record was written before any correction. No automatic handoff occurs; required owner corrections and independent rereview remain visible here.

## Bounded correction rereview — current advisory judgment

- Skill: code-review
- Status: blocked
- Review status: blocked
- Recording status: recorded (advisory only)
- Original finding dispositions: ER-M2-002 resolved; ER-M2-003 resolved for its recorded promoted-hash defect; ER-M2-004 resolved for its recorded ancestor-redirection defect
- Open material finding: ER-M2-005, requiring a CLI Design-owner decision
- Milestone closeout / Verify readiness: not claimed
- Next owner: CLI Design owner and user for the bounded guarantee choice below; no automatic handoff, further implementation or M3 progression
- Scope: independent rereview of the two corrected storage modules and regression tests; no Design, schema, activation or formal lifecycle mutation

### Corrected subjects

Unchanged reviewed files retain the first implementation review identities above.

| Path | SHA-256 |
| --- | --- |
| `packages/rigorloop/dist/lib/record-store-files.js` | `5f83885b5198a8687942488887512344b9daa2ed77856072a9459996b3ed373d` |
| `packages/rigorloop/dist/lib/record-store.js` | `9c76928470276d8ebd1a8a2900cec9a016207b5fb5084f6d893cedf460c56405` |
| `packages/rigorloop/test/record-store-cli.test.js` | `07ea8596dd05b1d28628a27155580a05f598a7ab4555528cf0b8a6a19d5e53b7` |
| `docs/implementation/explicit-recording-m2.md` | `9d5330a3578164251de72345e7762333754f1d1bc69ab25a8f4f2ec0eff07530` |

The post-lock journal check preserves intervening prepared and committed journals; two focused regressions directly prove ER-M2-002's outcome. Publication now checks the actual expected hash against the journal's allowed identities before passing it to mutation; record, complete and restore regressions directly close ER-M2-003's recorded promotion window. `withParent` verifies the directory inode after synchronously entering it and performs mutation with single basenames, preventing the recorded substituted-ancestor redirection. Five late-substitution regressions cover replacement, exclusive creation, removal, directory creation and directory removal, including unchanged outside targets and restored caller cwd. This closes ER-M2-004's recorded reproduction, not every possible external-write race.

### ER-M2-005 — Decide the guarantee for non-cooperating edits after the final target check

- Severity: major
- Owner: CLI model, Design stage; user decision for any changed guarantee or expanded storage scope
- Location: `packages/rigorloop/dist/lib/record-store-files.js:108`–`:109`, against CLI-SR-04/06 and CLI Design Save safety and recovery boundary
- Evidence: The corrected parent anchoring protects ancestor identity, but target identity is still checked before a separate rename. A deterministic reviewer probe wrapped `fs.renameSync`; immediately before its actual call for `change.yaml`, another writer's action wrote `external-final-state\n` to that exact target. The normal rename then ran. The operation returned `saved`, and the external bytes were replaced by the candidate. The probe used a disposable root and restored the runtime wrapper afterward; no implementation edit was persisted. This is later than ER-M2-003's now-fixed hash-promotion window.
- Boundary distinction: Cooperating recorder writers are excluded by the lock. An arbitrary writer ignoring that lock can still modify the exact file after the final observed hash but before replacement. Pinning the parent prevents redirection to a different ancestor; it does not make checksum comparison and replacement one conditional operation. The existing Design's observed-check caveat explicitly describes decision-basis drift, while CLI-SR-04 requires concurrent replaced inputs to reject and recovery forbids overwriting unknown third states. The reviewer cannot silently extend that caveat to target overwrite.
- Required outcome: Resolve that contract/implementation boundary explicitly before M2 can claim its safety requirements. Do not present another pre/post pathname or hash check as unconditional protection through the mutation instant.
- Safe resolution path / needs-decision: The CLI Design owner and user must choose between (a) an explicit observed-check guarantee for non-cooperating exact-target edits in this final window, while preserving cooperating-writer exclusion, observed-third-state stops and ancestor containment, or (b) retaining the stronger target guarantee and separately scoping a storage mechanism capable of it. This review selects neither option, requests no OS investigation and authorizes no dependency, platform restriction or normative weakening. Any selected contract revision needs independent Design assessment and affected implementation proof/rereview.

### Rereview proof and limits

Independently run: `node --test packages/rigorloop/test/record-store-contract.test.js packages/rigorloop/test/record-store-cli.test.js` (48 passed, zero failed), schema bundle `--check` (exit 0), exact subject hashes, and the `node --input-type=module` final-target interleaving probe described above. The implementation owner's evidence reports the identical ten regression tests failed before correction and passed afterward, plus full package 523 total / 521 passed / two skipped / zero failed. The broader package command was not independently rerun by this reviewer.

Checklist reconsideration: the original targeted test, edge, error and containment concerns have direct correction proof; spec alignment and final-window data-safety remain blocked by ER-M2-005. Architecture ownership, historical isolation, derived parity and unrelated-change boundaries remain intact. No clean whole-M2 conclusion follows from the passing tests. This record preserves every first-pass finding and records the new supported issue before further correction. Ordinary activation remains disabled.

## Affected Code Review after approved external-edit refinement — current result

- Skill: code-review
- Status: completed
- Artifacts changed: this review only
- Open blockers: none in the isolated M2 review scope
- Next stage: isolated stop; no automatic downstream handoff
- Review status: clean-with-notes
- Material findings: none open under the current approved Design basis
- Recording status: recorded (advisory only)
- Recording blocker: none for this assigned advisory location
- Review record: `docs/reviews/explicit-recording-m2-code-review.md`
- Review log: not applicable
- Review resolution: dispositions preserved in this record
- Reviewed milestone: M2 under the user's isolated implementation/review exception
- Milestone closeout: not-applicable to formal lifecycle; advisory M2 review is clean
- Remaining implementation milestones: M3–M5, outside this invocation's authority
- Required review-resolution: no outstanding M2 finding
- Finding IDs: ER-M2-001–005 dispositioned below; historical evidence retained
- Verify readiness: not-claimed

### Basis, identities and finding disposition

The user selected an observed-check guarantee for non-cooperating external edits, and the [independent Design rereview](explicit-recording-and-model-centered-design.md), External-edit boundary section, approved both current model documents on that basis. This affected Code Review assesses implementation against that explicit refinement and the existing advisory M2 delivery allocation. No code or tests changed after the preceding correction rereview. The reviewer remains independent of their authorship.

The reviewer rehashed all eleven named M2 subjects. Every implementation, schema, dispatcher and test identity matches the first implementation identity table as updated by the corrected-subject table above. In particular, `record-store-files.js` remains `5f83885b5198a8687942488887512344b9daa2ed77856072a9459996b3ed373d`, `record-store.js` remains `9c76928470276d8ebd1a8a2900cec9a016207b5fb5084f6d893cedf460c56405`, and `record-store-cli.test.js` remains `07ea8596dd05b1d28628a27155580a05f598a7ab4555528cf0b8a6a19d5e53b7`. The implementation evidence as read has SHA-256 `c7af8821db15d8e8cd51d94ee1dccd831a8bb78e6b234c187413e2dd02801c0d`; its preceding blocked handoff is historical to this subsequent judgment, not an additional unresolved decision.

ER-M2-001 remains resolved by the reviewed selector rule and its schema/parser proof. ER-M2-002/003/004 remain resolved in their recorded scopes: fresh tests confirm pending-journal preservation under exclusion, rejection of observed third states on record/complete/restore, and ancestor-safe mutation through the shared verified-parent boundary, including sibling creation/removal paths. Live competing-CLI, interrupted recovery, read-set drift, mixed-snapshot rejection and committed-rollback tests also pass.

ER-M2-005 is dispositioned as resolved by the explicit user-approved scope change and this affected implementation assessment, **not by fixing the reproduced race**. The code still performs a target hash check and a later replacement. That is now consistent with CLI-SR-04/06's observed-check external boundary. The retained reproduction documents that an exact-target edit in the excluded final window may be overwritten. Users must not manually edit records or let other tools edit them while record/recover runs. The limitation does not waive competing-CLI exclusion, observed-conflict/third-state stops, ancestor containment or recovery protections. No unconditional external-writer guarantee is claimed.

### Current checklist

| Item | Assessment | Evidence and scope |
| --- | --- | --- |
| Spec alignment | pass | Current CLI-SR-04/06 explicitly own the remaining timing limit; retained guarantees match the reviewed paths. |
| Test coverage | pass for isolated M2 | All 48 focused cases pass, including the ten correction regressions and actual fixture-dispatch subprocess paths. |
| Edge cases | pass within stated boundary | Pending journals, observed third states, ancestor substitution, interrupted recovery and stale retry have direct proof; excluded final-window edit remains documented. |
| Error handling | pass | Safe selector errors, IO failures, busy/conflict/recovery-required outcomes and withheld mixed snapshots are exercised. |
| Architecture boundaries | pass | Storage accepts explicit decisions without lifecycle eligibility; no semantic owner transfer. |
| Compatibility | pass for unadopted slice | Historical rejection and ordinary namespace unavailability remain tested; M4 adoption is not certified. |
| Security/privacy | pass within stated boundary | Escaped-parent mutation and safe diagnostics have focused proof; no immunity to unsupported simultaneous manual/tool edits is claimed. |
| Derived artifact currency | pass | Canonical/package schema hashes match and bundle check passes; no installed-adapter or activation claim. |
| Unrelated changes | pass | Exact M2 subjects only; reviewer changed no source, model, plan or unrelated work. |
| Validation evidence | pass for scoped judgment | Independently rerun focused checks plus current coordinator-run broad regression, distinguished below. |

### Commands and handoff limits

Independently run: `node --test packages/rigorloop/test/record-store-cli.test.js packages/rigorloop/test/record-store-contract.test.js` (48 passed, zero failed); `node scripts/build-record-store-schema.mjs --check` (exit 0); subject `sha256sum` checks; and bounded source, Design-review, plan and evidence reads. The earlier final-target probe remains retained direct evidence of the limitation, not a newly passing regression. The coordinator reran `npm --prefix packages/rigorloop test` (523 total, 521 passed, two existing skips, zero failed), schema parity and `git diff --check` (exit 0); the reviewer did not rerun that full package command.

This is a clean advisory M2 assessment only. It neither settles a formal milestone nor approves the whole branch, ordinary observability/adoption integration, M3, final holistic Code Review, Verify, release or PR readiness. The direct invocation ends here; later work requires its own authority.
