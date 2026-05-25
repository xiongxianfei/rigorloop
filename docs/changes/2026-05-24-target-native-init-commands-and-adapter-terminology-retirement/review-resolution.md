# Target-Native Init Commands and Adapter Terminology Retirement Review Resolution

## Scope

This record tracks formal lifecycle review findings for the target-native init commands and adapter terminology retirement change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: proposal-review-r3
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4
Review closeout: code-review-r5
Review closeout: code-review-r6
Review closeout: code-review-r7

## Resolution Entries

### proposal-review-r1

#### TINIT-PR1-F1

Finding ID: TINIT-PR1-F1
Disposition: accepted
Status: resolved and confirmed by proposal-review-r2
Owner: proposal owner
Owning stage: proposal revision
Required outcome: The proposal must consistently state whether user-visible `rigorloop.yaml` and `rigorloop.lock` keys are renamed away from `adapter` in 0.3.0, and must distinguish that decision from deferred non-user-visible internal implementation names.
Safe resolution path: Revise `Public Terminology Boundary`, `Non-goals`, and any related scope text so user-visible state-file schema keys are explicitly in scope for target-oriented rename under `--write-state`, while non-user-visible `dist/adapters/`, archive filenames, and package-bundled release metadata fields remain deferred unless later approved.
Rationale: The current proposal contains both the owner decision to rename user-visible state-file keys now and wording that says lockfile keys may keep `adapter` until a separate migration. A spec cannot safely derive one contract from both statements.
Chosen action: Revised the proposal so public CLI/docs and user-visible `rigorloop.yaml` and `rigorloop.lock` content written by `--write-state` must use target/tool terminology. The deferred internal list now covers only non-user-visible or historical internals such as `dist/adapters/`, archive filenames, package-bundled metadata field names, internal code names, historical release evidence, and existing state files preserved unchanged by default init. Added a dedicated state-file schema boundary and acceptance criteria for legacy state-file behavior and deferred internal names.
Stop state: closed
Validation target: Rerun proposal-review and focused artifact validation after the proposal language is made consistent.
Validation evidence: Proposal-review R2 approved the revised proposal with no material findings. Focused validation is recorded in `change.yaml`.

### proposal-review-r2

No material findings.

### proposal-review-r3

No material findings.

### spec-review-r1

#### TNI-SR1

Finding ID: TNI-SR1
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec revision
Required outcome: Make the dry-run state-file planning requirements internally consistent for default init and `--write-state`.
Safe resolution path: Revise TNI-R65 so it says dry-run reports planned state-file writes only when state-file writes are in scope for the requested command, such as `--write-state`. Keep TNI-R66 requiring default dry-run to omit planned state-file creation/update, and keep TNI-R67 requiring `--write-state --dry-run --json` to report planned target-oriented state-file content.
Rationale: The current wording makes all dry-runs report planned state-file writes while also requiring default dry-run not to report planned state-file creation or update.
Chosen action: Revised dry-run requirements so dry-run always reports planned target-root writes without mutation, but planned state-file writes are reported only when state-file writes are in scope for the requested command. Default `init <target> --dry-run` is explicitly install-only and does not report planned `rigorloop.yaml` or `rigorloop.lock` creation or update. `--write-state --dry-run --json` reports planned target-oriented state-file content.
Stop state: closed
Validation target: Rerun spec-review and focused artifact validation after the dry-run requirements agree.
Validation evidence: Spec-review R2 approved the revised dry-run contract with no material findings. Focused validation is recorded in `change.yaml`.

#### TNI-SR2

Finding ID: TNI-SR2
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec revision
Required outcome: Clarify that target-oriented state-file requirements prohibit user-visible schema keys named `adapter` or `adapters`, while allowing explicitly permitted historical archive filename values such as `rigorloop-adapter-codex-v0.3.0.zip`.
Safe resolution path: Revise TNI-R43, TNI-R44, AC-TNI-008, and any related examples to distinguish schema keys from values. State that new state-file schemas must not use `adapter` or `adapters` as user-visible keys, while archive filename values may retain historical names until a separate internal archive rename is approved.
Rationale: TNI-R43 and TNI-R44 currently say new state-file content must not use `adapter` or `adapters`, but the lockfile example in TNI-R57 records archive filenames containing `rigorloop-adapter-*`, which the proposal explicitly defers as a non-user-visible internal/archive naming concern.
Chosen action: Revised state-file requirements to prohibit adapter-oriented schema keys while allowing historical archive filename values. The lockfile example keeps historical archive filename values under target-oriented keys, and AC-TNI-008 now distinguishes schema keys from archive filename values.
Stop state: closed
Validation target: Rerun spec-review and focused artifact validation after state-file key terminology and archive filename values are distinguished.
Validation evidence: Spec-review R2 approved the revised schema-key and archive-value distinction with no material findings. Focused validation is recorded in `change.yaml`.

#### TNI-SR3

Finding ID: TNI-SR3
Disposition: accepted
Status: resolved and confirmed by spec-review-r2
Owner: spec author
Owning stage: spec revision
Required outcome: Define when default install-only init must parse existing state files for mutation safety, and how malformed or ambiguous state affects default init.
Safe resolution path: Add requirements that separate byte preservation from safety checks. For example, default init must not write state files, but when an existing state file records the selected target or an install root that would be mutated, the CLI must parse enough valid state to detect drift/conflicts before replacement. Define whether malformed state blocks only when the selected target/root is implicated, or always blocks when any target root mutation is planned. Keep the chosen rule testable for malformed manifest, malformed lockfile, selected target drift, unrelated target entries, and no existing target root.
Rationale: TNI-R15 through TNI-R17 require default init to preserve state files byte-for-byte, while error behavior item 11 says malformed state is preserved unless needed for a safe mutation decision. The spec does not define when state is needed, so tests and implementation would have to guess whether default init ignores malformed legacy state or blocks before mutating target roots.
Chosen action: Added default-init state safety requirements separating byte preservation from safety reads. Default init preserves existing state files but must parse enough valid state when target-root mutation is planned to detect selected-target drift, overlapping roots, or conflicting target-root mappings. Malformed or ambiguous existing state blocks default non-dry-run init before target-root mutation; default dry-run may report planned target-root writes but must report that non-dry-run would block.
Stop state: closed
Validation target: Rerun spec-review and focused artifact validation after default-init state parsing and malformed-state behavior are explicit.
Validation evidence: Spec-review R2 approved the revised default-init state safety contract with no material findings. Focused validation is recorded in `change.yaml`.

### spec-review-r2

No material findings.

### spec-review-r3

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

#### TNI-PLR1-F1

Finding ID: TNI-PLR1-F1
Disposition: accepted
Status: resolved after plan revision
Owner: plan owner
Owning stage: plan revision
Required outcome: Make the release verification command in the plan match the supported or explicitly planned `release-verify.sh` interface before test-spec or implementation relies on it.
Safe resolution path: Either revise the plan to use the existing environment-variable interface, for example `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`, or add an explicit M3 implementation step and tests that extend `release-verify.sh` to support `--release-output-dir` and `--release-commit` before listing that syntax as a validation command.
Rationale: The current plan lists `bash scripts/release-verify.sh v0.3.0 --release-output-dir <release-output-dir> --release-commit <commit>`, but `scripts/release-verify.sh` currently accepts only a release-tag positional argument and reads release output and commit values from `RELEASE_OUTPUT_DIR` and `RELEASE_COMMIT`. Extra long-option arguments would not bind to the intended release artifacts.
Chosen action: Updated the M3 release verification command and the global validation plan to use the current `scripts/release-verify.sh` interface. The plan no longer lists unsupported `--release-output-dir` or `--release-commit` arguments. Release verification now uses `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`.
Stop state: closed
Validation target: Rerun plan-review after the release verification invocation is corrected.
Validation evidence: Plan revision validation is recorded in `change.yaml`; plan-review R2 is still required before test-spec or implementation readiness is claimed.

### plan-review-r2

No material findings.

### code-review-r1

#### TNI-CR1-F1

Finding ID: TNI-CR1-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: review-resolution
Required outcome: Add durable package CLI tests for the named alias targets and mixed `--adapter` forms required by `TTNI-CLI-002`, `TTNI-CLI-003`, and the M1 plan, proving each fails before mutation and reports the required guidance.
Safe resolution path: Extend `packages/rigorloop/test/cli.test.js` with table-driven cases for `claude-code`, `open-code`, `openai`, `codex-cli`, `init --adapter codex claude`, and `init codex --adapter claude`. Assert exit class/status, diagnostic code where stable, target-native migration or allowed-target guidance, and unchanged temporary project contents. Rerun `npm test --prefix packages/rigorloop` plus M1 metadata/lifecycle/diff checks, then rerun code-review.
Rationale: The implementation appears to reject the forms through the shared parser path, but the approved test spec names these parser edge cases explicitly and M1 cannot close from broad package-test success without durable direct proof.
Chosen action: Added package CLI tests for rejected alias targets `claude-code`, `open-code`, `openai`, and `codex-cli`, plus mixed removed syntax forms `init --adapter codex claude` and `init codex --adapter claude`. Each case asserts the expected error status/diagnostic guidance and unchanged temporary project contents.
Stop state: closed
Validation target: `npm test --prefix packages/rigorloop`; `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`; `git diff --check -- packages/rigorloop docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement docs/plans/2026-05-24-target-native-init-commands.md docs/plan.md`.
Validation evidence: `npm test --prefix packages/rigorloop` passed with 110 tests after the parser-edge tests were added. Focused metadata, lifecycle, review-artifact, and patch-hygiene validation is recorded in `change.yaml`.

### code-review-r2

No material findings.

### code-review-r3

#### TNI-CR3-F1

Finding ID: TNI-CR3-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: review-resolution
Required outcome: Add durable direct M2 package CLI tests for default opencode no-state install, default implicated drift/conflict state blocking, and default legacy adapter state preservation before M2 can close.
Safe resolution path: Extend `packages/rigorloop/test/cli.test.js` with focused default-init tests for opencode declared skills/commands that assert `.opencode/skills` and `.opencode/commands` install and `rigorloop.yaml` / `rigorloop.lock` are absent. Add default-init tests for selected-target or overlapping-root state drift/conflict that assert blocked status, bounded blocker code, unchanged state files, and no target-root mutation. Add at least one default legacy `adapter`/`adapters` state preservation test covering compatibility input and byte preservation. If these tests expose a parser or safety-ordering bug, fix the minimal runtime path and rerun the M2 validation set.
Rationale: The M2 implementation records passing broad validation, but the approved plan and test spec name default-init and migration edge cases that require direct proof. Current tests exercise related `--write-state` paths, which is insufficient for default install-only state-safety closeout.
Chosen action: Added package CLI tests for default `init opencode` installing `.opencode/skills` and `.opencode/commands` without writing `rigorloop.yaml` or `rigorloop.lock`; default `init codex` blocking selected-target drift before mutation; default `init codex` blocking an overlapping managed-root conflict before mutation; and default `init codex` preserving valid legacy `adapter` / `adapters` state byte-for-byte while treating it as compatibility input. The tests passed without production runtime changes.
Stop state: resolved; pending confirmation by code-review-r4
Validation target: `npm test --prefix packages/rigorloop`; `python scripts/test-npm-package-publication.py`; `python scripts/test-adapter-distribution.py`; `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`; `git diff --check --`.
Validation evidence: `npm test --prefix packages/rigorloop -- --test-name-pattern "TTNI-INST-002|TTNI-STATE-005|TTNI-MIG-001"` passed. `npm test --prefix packages/rigorloop` passed with 117 tests. `python scripts/test-npm-package-publication.py` passed. `python scripts/test-adapter-distribution.py` passed with 103 tests. Focused metadata, lifecycle, review-artifact, and patch-hygiene validation is recorded in `change.yaml`.

### code-review-r4

No material findings.

### code-review-r5

#### TNI-CR5-F1

Finding ID: TNI-CR5-F1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: review-resolution
Required outcome: Extend the v0.3.0 post-publish live-smoke evidence contract and tests so recorded evidence for each target includes the fields required by `TTNI-SMOKE-003` and release evidence validation enforces them before published evidence can pass.
Safe resolution path: Add target-smoke evidence fields for installed root(s), tree hash value(s), file count(s), and command output summary in `docs/releases/v0.3.0/npm-publication.md`, using pending placeholders before publication and real values after live smoke. Update `_validate_npm_publication_evidence` so `published` v0.3.0 evidence fails when any target row omits those fields, and consider requiring pending placeholders while status is `pending-publication` so the execution contract is visible before publish. Add direct release validation tests in `scripts/test-adapter-distribution.py` for missing target-smoke detail fields and for complete published target-smoke evidence. Keep pre-publish packed-package smoke and target-native docs validation unchanged.
Rationale: M3 records live post-publish smoke rows, but the current evidence schema and validator only require thin pass/pending rows. The approved test spec requires evidence to name installed roots, tree hashes, file counts, and command output summary, so a future published evidence row could pass without the durable proof needed to validate real public asset delivery.
Chosen action: Extended `docs/releases/v0.3.0/npm-publication.md` target-smoke evidence with npm version, installed root(s), tree hash value(s), file count(s), command output summary, explicit pending placeholders, and a visible table. Updated `_validate_npm_publication_evidence` to enforce those fields for v0.3.0 target-smoke rows, reject pending placeholders in published evidence, require real tree hash and file count values for published rows, and require opencode to name both `.opencode/skills` and `.opencode/commands`. Added positive and negative tests for pending placeholders, complete published target-smoke evidence, missing roots, missing hashes, missing counts, missing command summaries, incomplete opencode roots, and published placeholder leakage.
Stop state: resolved; pending confirmation by next code-review
Validation target: `python scripts/test-adapter-distribution.py`; `python scripts/validate-release.py --version v0.3.0 --release-output-dir <release-output-dir> --release-commit <commit>`; `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`; `python scripts/validate-change-metadata.py docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement`; `git diff --check --`.
Validation evidence: Focused target-smoke evidence tests passed. `python scripts/test-adapter-distribution.py` passed with 112 tests. `python scripts/test-npm-package-publication.py` passed with 6 tests. `npm test --prefix packages/rigorloop` passed with 117 tests. `python scripts/validate-release.py --version v0.3.0 --release-output-dir /tmp/tmp.cWJYJ5cs7M --release-commit 02a9d7d6d514fc99908abf32898494dbbbae00c9` passed. `RELEASE_OUTPUT_DIR=/tmp/tmp.cWJYJ5cs7M RELEASE_COMMIT=02a9d7d6d514fc99908abf32898494dbbbae00c9 bash scripts/release-verify.sh v0.3.0` passed.

### code-review-r6

No material findings.

### code-review-r7

No material findings.
