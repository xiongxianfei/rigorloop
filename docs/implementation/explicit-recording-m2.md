# Explicit Recording M2 — Isolated Implementation Evidence

## Authority and scope

The user requested M2 implementation followed by independent review after the clean advisory M1 rereview. This is an isolated M2 request, not ordinary contract adoption or permission to begin M3. The current CLI lookup (`node packages/rigorloop/dist/bin/rigorloop.js workflow-context --change 2026-09-05-explicit-recording-and-model-centered-design --format json`) reports `RL_CONTEXT_CHANGE_NOT_FOUND`; no formal change state or gate identity is inferred.

The reviewed [CLI model](../design/cli.md), [Workflow model](../design/workflow.md), [delivery plan M2](../plans/2026-09-05-explicit-recording-and-model-centered-design.md) and [M1 rereview](../reviews/explicit-recording-m1-code-review.md) are the explicit basis. No project-map inference is needed: the selected package entrypoint, M1 validator and historical transaction implementation are inspected directly.

## Same-slice completeness

TG-03 requires the four command interfaces in text and JSON, byte-preserving recording, coherent inspection including absence/missing sidecars, read-only checking, closed arguments/limits, observations distinct from errors and containment. TG-04 requires exact revision/read/write preconditions, competing writers, interrupted publication/recovery, complete/restore, third-state and tampered-evidence stops, and protection of acknowledged commitment. Public subprocess proof and helper proof are both required; neither substitutes for the other.

Existing historical engines, schemas and unrelated dirty files are not modification targets. Governance, skills and ordinary activation stay unchanged because they belong to later milestones. Existing compact transaction code is a reuse candidate, not proof that the new storage contract is implemented.

## Initial preflight (historical)

Test preparation began with five command cases: read-only absent inspection/checking, exact-byte creation/inspection, stale retry versus refreshed unchanged replacement, unknown-argument safe rejection, and refusal to claim an existing root without a manifest. `node --test packages/rigorloop/test/record-store-cli.test.js` produced the expected initial red result, `ERR_MODULE_NOT_FOUND` for the not-yet-implemented command module. The new draft test file was removed after the preflight blocker below was confirmed; it is not left as an unresolved import that breaks the package suite. No preexisting file was removed or reverted.

Before command implementation, independent preflight identified an unrepresentable input-error case. CLI Design requires rejection of unknown subcommands, missing selectors and invalid change IDs, but the result definition and M1 schema require one of four known operations and a valid change ID in every JSON result. There is no defined representation for an unavailable selector. Neither fabricating an ID nor silently selecting the legacy usage envelope is justified by the reviewed contract.

The recommended owner decision is to permit null only for unavailable `operation` or `change_id` selectors in rejected input-error results, with explicit conditional validation. Successful and other command-scoped results retain their existing identity requirements. A separately defined pre-dispatch usage envelope is an alternative. The CLI Design owner must select and independently review the bounded clarification before implementation adopts it; this evidence does not change the Design or schema.

## Implementation and current handoff

The user explicitly authorized the bounded CLI rule refinement, independent Design rereview, M2 implementation and Code Review. The [advisory Design rereview](../reviews/explicit-recording-and-model-centered-design.md) approved the two-model package with the new selector-error rule and resolved ER-M2-001 at Design. No formal registration or ordinary activation is inferred.

Implementation adds `record-store-cli.js` (argument parsing, bounded stdin, safe text/JSON output), `record-store.js` (explicit candidates, coherent reads, preconditions, journaling and recovery), and `record-store-files.js` (shared filesystem checks, streaming reads/hashes and synchronized writes). The canonical and packaged result schemas and M1 validator now admit unavailable selectors only in the specified rejection partition. Request/record identities remain strict. Schema bundling uses the existing M1 generator.

The existing dispatcher has dependency-injected fixture access and an import-safe exported `main`; ordinary CLI invocation still rejects the namespace. The test-only launcher under `packages/rigorloop/test/helpers/` is not shipped package data and exercises that same dispatcher/parser/renderer/storage path in real subprocesses. No environment variable or flag enables the ordinary entrypoint. Existing CLI observability, command vocabularies, semantic engines and release behavior are unchanged; new ordinary integration remains M4-owned. The entrypoint guard preserves invocation through a bin symlink.

Private recovery contains one bounded before/candidate journal, a writer lock and an epoch marker for detecting overlapping completed writers. It is not a workflow record, request ledger or lifecycle decision source. Restore validates known before/candidate bytes and preserves unrelated files; completion rechecks declared decision-basis inputs. A committed journal cannot be restored. Fault hooks are dependency-injected test controls, not shipped CLI flags. No separate OS investigation, platform matrix, native dependency or platform-support claim was introduced.

### Proof trace

| Allocation | Direct cases |
| --- | --- |
| ER-M2-001 / TG-03 | Missing/unknown/invalid/repeated selectors, format fallback, no stdin access on argument rejection, null-selector schema partitions, public JSON safe errors |
| CLI-SR-01/02/03/07 / TG-03 | Read-only inspect/check; exact explicit bytes; terminal-status recording with separate observations; missing sidecar visibility/repair; no registry removal or unrelated-file overwrite |
| CLI-SR-04/08 / TG-04 | Revision/write/read identity conflict; stale lost-response retry; refreshed identical unchanged result; live competing subprocess; post-replacement read-set drift and exact restoration |
| CLI-SR-05/06 / TG-04 | Pre-journal failure; prepared/partially published/committed interruption; multi-record mixed bytes withheld from inspection; actual process exit followed by public complete/restore in text/JSON; repeatable interrupted recovery; third-state and stale/missing/tampered/unknown-phase recovery stops |
| CLI-SR-09/11 / TG-03/04 | Public/helper safe rejection, symlink/hard-link rejection, injected ancestor substitution without escaped bytes, overlapping completed writer detection, precise unsupported-contract and IO errors without payload echoes, ordinary namespace remains disabled |

### Commands and results

The selector-schema test was written first and failed against the M1 validator, then passed after the bounded schema/runtime change. New command tests initially failed with the missing command module. Additional diagnostic tests reproduced two misclassified errors before correction.

`node --test packages/rigorloop/test/record-store-cli.test.js packages/rigorloop/test/record-store-contract.test.js` passed all 38 tests on the review-requested revision. `npm --prefix packages/rigorloop test` passed 511 of 513 tests, with two existing skips and zero failures. `node scripts/build-record-store-schema.mjs --check` and `git diff --check` passed. These are local checks, not hosted CI or final Verify.

`npm pack --dry-run --json` from `packages/rigorloop` exited 0: all four record-store modules and the schema bundle are included, while no `test/` files or fixture launcher are included. No archive was published or installed.

## Core result

- Skill: implement
- Status: blocked
- Completed scope: M2 command/storage implementation, three review-driven corrections and independent rereview; milestone closeout withheld
- Artifacts changed: the explicitly named implementation, tests, schema bundle and this evidence; Design and review evidence remain separately owned
- Tests added or updated: command/public-subprocess/failure tests and bounded M1 result-schema extension
- Validation performed: commands and revision-specific results above
- Validation result: all 48 focused tests pass; full package has 521 passes, two skips and zero failures
- Open blockers: independent rereview reproduced a later external target-edit window; the exact guarantee needs a CLI Design owner decision
- Next stage: resolve the external-writer guarantee at CLI Design; no automatic downstream handoff
- Claim limitations: no clean-review, ordinary activation, M3, formal settlement, final Verify, commit or push

## Independent Code Review outcome

### Authorized safety correction proof

The user explicitly authorized fixing ER-M2-002/003/004 in this repository's isolated M2 scope. Operation: `fix`; command authority: `current-bounded`; write authority: `governed-scope-bound` under that explicit exception, limited to the two storage modules, existing CLI tests and this evidence. No lifecycle registration, Design change or activation is authorized. Each finding is a separately reproduced `race-or-timing` defect with `settled` CLI-SR-04/05/06/09 basis, `supported` cause, `feasible` tests and `failing-automated-test` proof.

Before production correction, `node --test --test-name-pattern='ER-M2-00[234]' packages/rigorloop/test/record-store-cli.test.js` exited 1: all ten new checks failed. Inputs use the existing explicit-recording fixture and disposable local directories. Controlled synchronous interposition schedules a competing journal before lock acquisition, a third-state edit at publication's actual expected-hash read, and ancestor substitution at each mutation syscall. Expected outcomes are preserved journal identity, preserved third-state bytes, and untouched outside targets. Observed outcomes included saved/recovered over third states, replaced prepared journal, and escaped writes/removals/creation. The committed-journal case returned conflict rather than recovery-required. Proof file SHA-256 before and after correction: `07ea8596dd05b1d28628a27155580a05f598a7ab4555528cf0b8a6a19d5e53b7`; environment: Node v24.14.1. The identical command and tests passed all ten after correction.

The two storage modules now recheck pending journals under writer exclusion, validate the exact publication precondition against recorded before/candidate identities, and share a synchronous verified-parent mutation boundary. The last boundary temporarily pins the working directory to the verified parent inode, uses only single relative basenames for mutations, and restores the caller's working directory in `finally`. It never yields or calls injected workflow hooks inside that section. Inputs still resolve only against explicit root. This adds no dependency, OS investigation, public command or platform certification claim.

Post-correction validation: `node --test packages/rigorloop/test/record-store-cli.test.js packages/rigorloop/test/record-store-contract.test.js` passed all 48; `npm --prefix packages/rigorloop test` passed 521 of 523 tests, with two existing skips and zero failures; `node scripts/build-record-store-schema.mjs --check` and `git diff --check` exited 0. These are local checks, not hosted CI or final Verify.

Independent rereview confirmed the three original corrections but reproduced a distinct final-target window: a non-cooperating external writer changes the target after its final hash check, before the actual rename, and the recorder overwrites that edit. Parent anchoring does not make content comparison and rename indivisible. Passing current checks therefore does not close M2. Bugfix terminal result: `blocked`, not `fix-applied`; current action: `route-owner` for an explicit CLI Design guarantee decision. The recommended simple boundary is full exclusion for cooperating CLI writers and freshness at the observed check for non-cooperating external edits. That recommendation is not adopted by this evidence. No additional dependency, speculative precheck or implementation expansion was attempted; the reviewer owns its durable finding and disposition.

The [M2 advisory implementation review](../reviews/explicit-recording-m2-code-review.md) recorded `changes-requested` after independently reproducing three interleavings not covered by the green suite: a pending journal can appear between initial inspection and lock acquisition and be replaced (ER-M2-002); a new third-state hash can be promoted into an accepted replacement precondition (ER-M2-003); and late ancestor substitution can redirect pathname mutation outside the selected root before the post-write check detects it (ER-M2-004).

These were required safety corrections, not deferred acceptance criteria or new workflow rules. Corrections and regression proof are now recorded above; independent disposition remains review-owned. Public activation remains disabled, and M3 has not begun.
