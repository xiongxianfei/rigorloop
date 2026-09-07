# Explicit Recording M4 — Advisory Prerequisite Code Review

## First-pass result (historical)

- Skill: code-review
- Status: completed
- Artifacts changed: this review only
- Open blockers: ER-M4-001 requires selector correction; actual CI preflight remains separately blocked
- Next stage: bounded correction and independent rereview; no automatic downstream handoff
- Review status: changes-requested
- Material findings: ER-M4-001
- Recording status: recorded (advisory only)
- Recording blocker: none for the explicitly assigned review location
- Review record: `docs/reviews/explicit-recording-m4-code-review.md`
- Review log: not applicable to this isolated advisory review
- Review resolution: finding disposition belongs in this record
- Reviewed milestone: M4 validation prerequisites only, not complete M4
- Milestone closeout: resolution-needed; M4 remains incomplete
- Remaining implementation milestones: remaining M4 integration/adoption and M5
- Required review-resolution: yes
- Finding IDs: ER-M4-001
- Verify readiness: not-claimed

## Scope, basis and independence

The reviewer authored none of the implementation. The exact target is the new Node validation bridge, explicit-contract Python dispatch and its four new tests, and explicit-recording selection/catalog changes with matching tests. The earlier compact-review test addition in the same Python test file and all unrelated dirty changes are excluded. Basis: current Workflow and CLI models (WF-SR-10; CLI-SR-02/07/10), reviewed M4 delivery allocation including package/adapter compatibility proof, prior advisory Design/Delivery and M3 review, and [M4 prerequisite evidence](../implementation/explicit-recording-m4.md).

The user's isolated implementation authority permits this partial review without inventing a registered root or formal gate ID. Public activation, final governance cutover, integrated adapter proof and whole-change review are not this target. Tracking and advisory-path preflight blockers are preserved, not bypassed or counted as successful CI.

## Finding ER-M4-001

- Finding ID: ER-M4-001
- Severity: minor
- Location: `scripts/validation_selection.py:2313` (new package-path classification), `scripts/validation_selection.py:1782` (early-return selection)
- Evidence: The new `explicit-recording` category shadows the existing `rigorloop-cli` category for record-store modules, packaged schema and package tests. Its selection returns without retaining `npm_package_publication.test`. A direct `select_validation` probe for `packages/rigorloop/dist/lib/record-store.js` and `packages/rigorloop/dist/schemas/explicit-recording-v1.schema.json` selects only `boundary_first.regression`, `change_metadata.regression`, `model.validate`, `record_store.regression` and `record_store.schema`. The sibling `packages/rigorloop/dist/lib/compact-contract.js` still selects `npm_package_publication.test` and `rigorloop_cli.test`. Package publication tests include actual tarball contents and installed-binary execution; the newly selected npm suite does not replace this boundary. M4 requires supported package/distribution compatibility, and the new classification silently removes existing coverage for the very package surfaces being adopted. The new regression checks only that three added IDs are present, so misses this subtraction.
- Required outcome: Package paths receiving explicit-recording checks must retain the existing applicable package publication proof. Non-package model/schema-source paths need not acquire unrelated publication obligations solely for this correction.
- Safe resolution path: Add an exact package-path selection regression and retain `npm_package_publication.test` alongside the new checks for those package paths. Keep fail-closed preflight and existing historical classification intact; independently rereview the bounded correction.
- needs-decision rationale: None; this restores existing package coverage rather than introducing a new adoption mechanism or expanding Design.

## Checklist

| Item | Assessment | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Structural recording dispatch preserves semantics, but ER-M4-001 weakens adoption compatibility proof. |
| Test coverage | concern | Four metadata and six-path selection cases pass; selected package-path coverage lacks the retained-publication assertion. |
| Edge cases | pass within partial scope | Unknown/mixed contracts, duplicate JSON keys, encoding, symlinks and missing/malformed registered support records have focused rejection tests; stale subjects do not become eligibility. |
| Error handling | pass within partial scope | Node bridge rejects malformed/unavailable sets with generic errors; subprocess failure/timeout fails closed. No repair or mutation is introduced. |
| Architecture boundaries | pass | Existing recorder inspection and complete-set validation are reused; no new lifecycle engine, config layer or public command. |
| Compatibility | concern | Historical metadata handlers remain selected; package-check subtraction is ER-M4-001. |
| Security/privacy | pass within partial scope | Inspection applies existing containment and coherent-set checks; failures do not print record bodies; no writer enabled. |
| Derived artifact currency | concern | Reported parity applies to prospective output only; dropped tarball/installed-package routing requires correction. Activation and integrated-adapter proof remain unperformed. |
| Unrelated changes | pass | Only the named prerequisite diff is assessed; unrelated compact work and preflight blockers remain untouched. |
| Validation evidence | concern | Focused checks pass but direct selection probe exposes omitted proof; no actual local CI success claimed. |

## Exact reviewed subjects

SHA-256 identifies complete files; review ownership is only the bounded changes described above.

| Path | SHA-256 |
| --- | --- |
| `scripts/validate-record-store.mjs` | `339baf0fdcae22d77bc427c11ee483f275720b91a6d89d2254efae355eda16c6` |
| `scripts/validate-change-metadata.py` | `5d3829970b9695841f132bea7d6c61e56d0f45a512ec9057482b5f5f7c2de399` |
| `scripts/test-change-metadata-validator.py` | `e114fc81d9f2aad5396d9d8c8c8ac4f240e4c0a3a1d433d8d830811136bb4420` |
| `scripts/validation_selection.py` | `b42add0a6927c1ab440bf0f953935663d58565433f120f14e852480a19cdb4b3` |
| `scripts/test-select-validation.py` | `a9227e2391fd74126e41ef490c14a04bf80f91dcf41dd18077f32ac5f52ae12e` |
| `docs/implementation/explicit-recording-m4.md` | `ff622de02774e99c742f7f438fdab1c023be702db6975cd879687c7649e06adc` |

## Commands and limitations

Independently run: `python scripts/test-change-metadata-validator.py ExplicitRecordingMetadataTests` (4 passed), `python scripts/test-select-validation.py ValidationSelectionTests.test_explicit_recording_adoption_surfaces_select_real_proof` (1 passed), `git diff --check` (passed), and a read-only `PYTHONPATH=scripts python` probe invoking `select_validation` with explicit individual package paths and current repository preflight context (results recorded in ER-M4-001). Source inspection and SHA-256 checks establish the subjects above.

Coordinator evidence reports metadata 116 passed, selector 156 passed, npm 525 total / 523 passed / two existing skips / zero failures, adapter/schema parity and model validation passing. These are coordinator-run results, not independently rerun broad proof. The evidence records adapter-distribution tests as still running; no outcome is inferred. Actual local CI stops at preflight; untracked authority and advisory-path handling remain unresolved. This finding is recorded before fixes, requires no owner decision, and does not authorize activation or claim complete M4, branch readiness, final holistic review or Verify.

## Current prerequisite correction rereview

- Skill: code-review
- Status: completed
- Artifacts changed by reviewer: this review only
- Review status: clean-with-notes
- Material findings / required review-resolution: none remaining in this partial target
- Finding disposition: ER-M4-001 resolved by independently reviewed correction
- Recording status: recorded, advisory only
- Open blockers: actual CI preflight and remaining M4 integration/adoption work, not waived
- Reviewed milestone: M4 validation prerequisites and the bounded packaging corrections they exposed
- Milestone closeout: not-applicable to this partial review; M4 remains incomplete
- Next stage: stop at this isolated review boundary; resolve validation basis before further adoption
- Remaining implementation milestones: remaining M4 and M5
- Verify readiness: not-claimed

The selector now retains `npm_package_publication.test` for explicit-recording package paths. Its exact six-check regression covers runtime, packaged schema, test and launcher paths. Reusing `rigorloop_cli.test` avoids scheduling the same npm suite under two IDs without subtracting proof. ER-M4-001 is resolved. The added model-path tracking test preserves existing authoritative-document CI preflight; it does not impose Git on the separate structural model checker or recorder.

The publication fixture now takes its expected version from the actual package being packed, instead of the release-transaction fixture's older version. Installed version, real target initialization and archive checks remain intact. Generated v0.5.1 metadata still explicitly identifies a local release candidate; only its current archive/tree identities and the corresponding release-index digest changed. Historical entries are unchanged. Independent generation parity and installed-package tests support this correction; neither proves a published release nor completed workflow adoption.

No additional material finding was identified. Current checklist: spec alignment, test coverage, edge cases, error handling, architecture boundaries, compatibility, security/privacy, derived artifact currency, unrelated changes and validation evidence all **pass within this partial target and the limits below**. The former concerns about omitted package coverage are closed, not the separate whole-M4 obligations.

### Current changed and additional subjects

These SHA-256 identities supersede the corresponding first-pass subjects or add the newly reviewed packaging corrections. The bridge, Python dispatch and metadata-test subjects retain their first-pass identities.

| Path | SHA-256 |
| --- | --- |
| `scripts/validation_selection.py` | `3dbd23dac0b83ec80e508b78100cdbde40ed54ea539ad50ab2bb9016abac73cb` |
| `scripts/test-select-validation.py` | `49fce64a7b8b5a800c1d6504d627efbdf2e5babdda7900cc5627dde016f91912` |
| `scripts/test-npm-package-publication.py` | `ec51daedbe0dcca4baa36aa59fa95f2f748d145cd7de254d192baad940560583` |
| `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json` | `ee148c15f8410114a349a9a06c102dac3a802784daad15e15c27ae56d7092b22` |
| `packages/rigorloop/dist/metadata/releases.json` | `58165e370e033f9ae85c9ef96268c2b7568d8db049077e4c8300c9cacf80f21e` |
| `docs/implementation/explicit-recording-m4.md` | `5c4f03fcbc77850c2cccc408b2138e0d13c269ab6971a2f74198e0f4d5397b15` |

Independently run for this rereview:

- `python scripts/test-select-validation.py ValidationSelectionTests.test_explicit_recording_package_paths_retain_publication_proof ValidationSelectionTests.test_model_selection_retains_authoritative_tracking_preflight ValidationSelectionTests.test_explicit_recording_adoption_surfaces_select_real_proof`: three passed.
- `python scripts/test-npm-package-publication.py`: seven passed, including tarball/installed-binary and all three adapter target installations.
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_v0_5_1_bundled_candidate_metadata_matches_generated_route_only_archives`: one passed; generated candidate metadata equals the complete bundled metadata.
- `git diff --check`: passed.

Coordinator evidence reports the current full selector suite at 158 passed and metadata at 116 passed. The earlier adapter run had 156 passes and one candidate-parity failure; that exact failure now passes independently, but the complete adapter suite has not been rerun after regeneration. The npm runtime suite remains 523 passed plus two existing skips on unchanged runtime subjects. Actual CI preflight remains blocked. This record preserves the first-pass finding, owns its disposition and stops without activation, formal lifecycle settlement, complete M4 approval or final whole-change review.

## Current isolated-worktree prerequisite review

- Skill: code-review
- Status: blocked
- Review status: blocked
- Artifacts changed by reviewer: this isolated review file only
- Material findings / required review-resolution: ER-M4-002; yes
- Prior disposition: ER-M4-001 remains resolved
- Recording status: recorded, advisory only
- Open blocker: grandfathered-authority classification and validation handoff require Design-owner resolution
- Reviewed milestone: bounded M4 prerequisites, not complete M4
- Milestone closeout: blocked; no formal settlement
- Next stage: Design-owner decision and affected independent review; no automatic downstream handoff
- Remaining implementation milestones: remaining M4 and M5
- Verify readiness: not-claimed

This assessment is bound to `/home/xiongxianfei/data/20260419-rigorloop.worktrees/explicit-recording-m4-IYKgvb`, based on `d6770adfbbd835363d3b428acbd5a27a9485171b`. The reviewed 59-path initiative diff excludes the unrelated compact engine/schema/fixture edits. The metadata-test diff contains only the explicit-recording test class, not the earlier 22-line compact-review test. The reviewer made no writes to the original worktree. This is not a new review of all 59 files: it retains prior scoped assessments and reviews the isolation delta below.

The refreshed TNP-005 literal matches the already independently parity-checked candidate metadata; its remaining assertions are preserved. The selector recognizes exactly ten named, previously user-authorized advisory files, selects prose and underlying model/runtime proof and does not assert formal settlement. The unknown review-path regression remains unclassified, and the previous package-publication coverage fix is retained. No additional implementation defect was identified in those deltas.

## Finding ER-M4-002

- Finding ID: ER-M4-002
- Severity: major
- Location: `scripts/boundary_first_validation.py:1957`–grandfathered-feature branch; affected authority `specs/rigorloop-workflow.md` and `specs/skill-contract.md`; inherited obligations `specs/boundary-first-proof-model.md` PBF-R049b/PBF-R055a/PBF-R056
- Evidence: The exact selected boundary command independently returns exit 1 with `BFR-GRANDFATHERED-REVIEW` for both affected files, expecting “semantic spec-review”. When activation is active, a selected grandfathered feature with no marker unconditionally receives this issue; the branch consumes no semantic classification result. The inherited contract forbids the validator from inferring substantive revision, requires review classification and preserves non-substantively revised historical specs. Current prospective adoption changes these shared authorities while preserving historical validation and using model-owned structure for the new profile. The implementation has no reviewed decision/validation handoff resolving that boundary. This is an exposed inherited adoption gap, not a regression caused by the advisory-file selector or recorder.
- Required outcome: The Design owner must settle how these shared-authority amendments are classified and how the appropriate independent assessment is supplied to validation, preserving historical obligations and fail-closed treatment of unknown classification. Selected CI must be able to assess the approved outcome without inventing approval, silently skipping the files or treating a marker as an exemption.
- Safe resolution path: Record the bounded decision in the existing affected model Design, obtain independent Design rereview, then implement only the resulting approved validation/handoff change with targeted proof and affected Code Review. No extra model file or automatic migration is required by this finding.
- needs-decision rationale: Owner is Design for the Workflow/CLI adoption boundary. Code Review cannot choose a substantive classification, reassign the inherited review obligation or waive it through selector changes. No classification or exemption is supplied by this record.

### Current checklist and validation basis

Spec alignment, compatibility and validation evidence are **block** for continuation because ER-M4-002 remains unresolved. Test coverage, edge cases, error handling, architecture boundaries, security/privacy, derived artifact currency and unrelated-change scope **pass within the narrow deltas and prior stated limits**. The exact allowlist does not excuse arbitrary advisory paths or authoritative tracking; no runtime or activation behavior changed.

The coordinator reports isolated local CI preflight passed and 15 of 16 selected checks passed, with only the boundary check failing. This reviewer independently reproduced that failure, not the complete CI run. The author updated the evidence to distinguish original-worktree results from the isolated result; its current Core result correctly identifies an executed validation failure, not blocked tracking preflight. No CI-pass claim is supported.

### Current isolated subject identities

These identities supersede the matching prior subjects. The metadata-test identity changes only because unrelated earlier work was excluded. Other previously reviewed prerequisite identities remain unchanged.

| Path | SHA-256 |
| --- | --- |
| `scripts/validation_selection.py` | `d040c90c9356b086f2532fb418eea4864fa3d5c8cf9cbc3c66f284463011689d` |
| `scripts/test-select-validation.py` | `5af88a8d31de55a4674038d6c3e681fd322cbae0af7cb8aa2cad6cdf31f0429c` |
| `packages/rigorloop/test/cli.test.js` | `a4464a3117c74d0875fe52965ef6f20af40bfc0086fede3a2a426b0b351e7125` |
| `scripts/test-change-metadata-validator.py` | `44d5ab15486006f90fd156a11021e823377eacc5614616cdd570b3c40a89100d` |
| `docs/implementation/explicit-recording-m4.md` | `3c31681be7fc2d093a7f8de56471b9a613d28dc3d8968a7ff605b639b5cc7206` |

ER-M4-002 was reproduced against unchanged parser identity `2faf8ec25f599168e7751801f9c92876a67d4d414db4d0f72e42ffb1da91bd3b`; affected Workflow spec identity is `af9ec40714a995e1e4faffafbdf77b8763d66da9eb295ce8a1fcc93baf0d4956` and skill contract identity is `85d9f928eb4bfcf1d89c186848011524d01aab97a1fba40ccac39cb763ac65fe`.

Independently run in the isolated worktree: `python scripts/test-select-validation.py ValidationSelectionTests.test_isolated_recording_evidence_selects_proof_without_formal_settlement ValidationSelectionTests.test_explicit_recording_package_paths_retain_publication_proof` (two passed); `node --test --test-name-pattern='TNP-005 package version' packages/rigorloop/test/cli.test.js` (one passed); `python scripts/validate-boundary-first.py --check --path specs/boundary-first-proof-model.md --path specs/compact-current-state-change-record.md --path specs/rigorloop-workflow.md --path specs/skill-contract.md` (exit 1, exact two findings above); source/diff and SHA-256 inspection. The finding is recorded before any correction. Stop for the named Design decision; no source fix, activation, complete M4, final whole-change review or Verify is claimed.

## Grandfathered-handoff implementation — first-pass correction review

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Artifacts changed by reviewer: this isolated review only
- Material findings / required review-resolution: ER-M4-003; yes
- Prior findings: ER-M4-001 resolved; ER-M4-002 Design decision resolved, final implementation disposition awaits the reconciliation below
- Recording status: recorded, advisory only
- Open blocker: remaining contradictory classification owner in governing reconciliation
- Reviewed milestone: bounded M4 grandfathered-review handoff correction
- Milestone closeout: resolution-needed, not complete M4
- Next stage: narrow reconciliation and independent rereview; no automatic downstream handoff
- Remaining implementation milestones: remaining M4 and M5
- Verify readiness: not-claimed

The reviewer authored none of these changes. Basis is the approved two-model handoff refinement and its independent classification of the two exact shared-authority amendments. The implementation separates only `BFR-GRANDFATHERED-REVIEW` into review observations; unknown diagnostics remain errors. Review-only results identify Design Review and return structural success, mixed structural/rollback failures retain observations and fail, and unknown markers or partial malformed boundary adoption reject. No classification or approval is inferred by the validator. The independently executed real four-spec command returns exit zero with `review-required`, both exact paths and validated activation/rollback selection.

## Finding ER-M4-003

- Finding ID: ER-M4-003
- Severity: minor
- Location: `specs/boundary-first-proof-model.md:511`, PBF-R059
- Evidence: The correction changes PBF-R055a to require Design Review classification, but PBF-R059 still requires `spec-review` to own “substantive-revision classification for grandfathered specs”. Both clauses govern the same classification. The approved model explicitly replaces that retired owner; the remaining unconditional duplicate makes the required governing reconciliation incomplete even though the new command emits `design-review`.
- Required outcome: The grandfathered classification owner must agree with PBF-R055a and the approved Workflow mapping throughout the affected governing rule. Preserve unrelated historical review responsibilities.
- Safe resolution path: Narrowly qualify PBF-R059's grandfathered-classification responsibility by the current PBF-R055a handoff, then independently rereview the exact correction. No new format, owner decision or broader historical cleanup is necessary.
- needs-decision rationale: None; the Design owner already chose the required classification responsibility.

Current checklist: spec alignment and compatibility **concern** because of ER-M4-003. Test coverage, edge cases, error handling, architecture boundaries, security/privacy, derived-artifact scope, unrelated changes and validation evidence **pass within this bounded correction**. The seven focused tests use the actual parser/command while stubbing activation/archive integrity; the real repository invocation separately exercises those unstubbed checks. New unknown-marker and unknown-diagnostic regressions support fail-closed handling. No broader adoption claim follows.

| Current correction subject | SHA-256 |
| --- | --- |
| `scripts/validate-boundary-first.py` | `3d12bb1991e923ae9a409ecde67e49fe1c73a63c461f05a1e16510cd20b65288` |
| `scripts/boundary_first_validation.py` | `403d9c77f2c8fe3a99a532157c2b5ad639b23ca6a405f20757d92b969f5e04af` |
| `scripts/test-boundary-first-validation.py` | `832b6f0754f89350bd1cdb11fa8ba80fb16f3530461f93c551d55f1e055cf997` |
| `specs/boundary-first-proof-model.md` | `71888ff2dfc0ff8e6a0e6a12e84b0907141cf056e2d21317741a64af60c58ccf` |
| `docs/implementation/explicit-recording-m4.md` | `deb59bff4e70a58a9b3e4c8e7284889b4f956d3fddb0df03e743a299ada330ae` |

Independently run: `python scripts/test-boundary-first-validation.py GrandfatheredReviewHandoffTests` (seven passed), `python scripts/test-boundary-first-validation.py` (85 passed), and the exact four-spec command printed in the preceding review (exit zero, `review-required`, both paths). Current selected CI is still running at first-pass recording; no result is inferred. This supported finding is recorded before its correction. The reviewer stops without source edits, public activation, complete M4 approval or final whole-change review.

## Current bounded handoff rereview

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Artifacts changed by reviewer: this isolated review only
- Finding dispositions: ER-M4-001 remains resolved; ER-M4-002 and ER-M4-003 resolved for this implemented prerequisite handoff
- Material findings / required review-resolution: none remaining in reviewed prerequisite scope
- Recording status: recorded, advisory only
- Open blockers: no blocker in this bounded correction; remaining M4 integration/adoption obligations are not completed
- Reviewed milestone: M4 prerequisites and grandfathered-review handoff only
- Milestone closeout: not-applicable to partial review; M4 remains incomplete
- Next stage: isolated stop and return judgment to coordinator; no automatic lifecycle handoff
- Remaining implementation milestones: remaining M4 and M5
- Verify readiness: not-claimed

PBF-R059 now retains its unrelated historical duties and explicitly assigns current grandfathered-spec classification to Design Review under PBF-R055a. That removes the evidenced duplicate-owner contradiction and completes the approved governing reconciliation. This is the selected reporting/classification handoff, not a blanket historical exemption or a new retrospective approval. The two shared-authority classifications remain owned by the preceding independent Design Review; the validator still reports their review obligation without authenticating or inferring approval.

The independently reviewed implementation and direct proof from the preceding pass remain unchanged. Combined with this exact wording correction, they resolve ER-M4-002's implemented handoff and ER-M4-003's reconciliation omission. Current checklist: spec alignment, test coverage, edge cases, error handling, architecture boundaries, compatibility, security/privacy, derived-artifact scope, unrelated changes and validation evidence all **pass within the stated prerequisite limits**. No further material issue was identified.

Only these subject identities supersede the preceding implementation pass; both scripts and the 85-test suite retain their recorded identities:

| Path | SHA-256 |
| --- | --- |
| `specs/boundary-first-proof-model.md` | `a166b68a673d485c83a0b665446933c774406b03a4f464b205426ae9b8b315bb` |
| `docs/implementation/explicit-recording-m4.md` | `aed833f4ddda5855df21f4e946e5c9c2c0db23c61b7e562281dd6d46a7a7ecca` |

Independently rerun after the wording correction: the exact four-spec `python scripts/validate-boundary-first.py --check` invocation above (exit zero, `review-required`, both paths and Design Review owner preserved) and `git diff --check` (passed). Coordinator evidence reports a second `bash scripts/ci.sh --mode local` run after the correction with preflight and all 16 selected checks passing; the final evidence prose audit reports zero errors/warnings. These are actual selected-check results, not an inferred whole-repository or final Verify result.

First-pass findings and timing remain preserved. The original worktree was not modified. Public activation, generated-adapter semantic integration, complete M4, final holistic Code Review, formal settlement and Verify remain outside this judgment.

## M4 adoption candidate — finding recorded before correction

## Finding ER-M4-004

- Finding ID: ER-M4-004
- Severity: major
- Location: `packages/rigorloop/dist/bin/rigorloop.js:2435`, public `runObservedCli` entry; `packages/rigorloop/dist/lib/log-config.js:33`, outer argument preprocessing
- Evidence: The newly exposed public recorder goes through the historical logging parser before its own closed selector validation. Independently run from the isolated worktree, `node packages/rigorloop/dist/bin/rigorloop.js record-store inspect --root . --change no-such-review-fixture --format json --no-file-log` returns an inspected/exit-zero result, although that flag is not admitted by the approved recorder command grammar. Replacing the final flag with `--console-log-level unknown_value` returns exit 4 and only `RL_INVALID_LOG_LEVEL: logging configuration rejected` on stderr, with no JSON result. CLI's Result schema and exit behavior requires argument errors to return the empty rejected/exit-2 envelope, retaining independently available selectors and honoring one valid JSON format. Exit 4 instead means busy. The actual installed-binary path adds this outer parser; calling exported `main` alone does not test it. This is the observability integration dependency explicitly identified by the CLI Design, not evidence that record-store's inner parser accepts the bad value.
- Required outcome: Actual public/installed recorder calls must preserve the approved closed selectors and result/exit contract through outer command integration. Invalid argument paths must not disappear into historical logging preprocessing or return a different command's error contract. Keep raw rejected values and payloads out of diagnostics.
- Safe resolution path: Add otherwise-valid real-binary regressions for these outer-parser cases, implement a contract-separated handling that retains the approved recorder rejection envelope, and prove historical command logging behavior remains intact. Do not silently expand the recorder's flags or change its exit meanings; any intended expansion requires an explicit Design decision. Independently rereview the correction.
- needs-decision rationale: None for restoring the already approved closed-selector and result guarantees; a proposed departure from them would belong to CLI Design.

This finding is recorded before any implementation correction. M4 cannot receive a clean result while it remains open. The supported finding is independent of still-running broader validation; complete review evidence and current subject inventory follow at handoff. Prior ER-M4-001/002/003 dispositions remain intact. No source, model, plan or lifecycle state was changed by this reviewer.

### M4 adoption first-pass subject inventory

Exact complete-file identities bind the current adoption deltas; previously reviewed unchanged prerequisite/storage subjects retain their earlier identities. This inventory does not confer final whole-change approval.

| Path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `52d4ff2dde00cc5d478726155be41c2322115d67bfde3786901a1d0a961eb993` |
| `CONSTITUTION.md` | `ba13fbf7bbce39f8257f91ca07c657f06b3e22658da89807acb3be9512b38a92` |
| `docs/architecture/system/architecture.md` | `f1d2ea08a55eaa99ac849f37ee9b17d5a470be26671b16b179f72de30d277975` |
| `specs/rigorloop-workflow.md` | `b755687df0f75199dbab35438895bb23fe26a2e150d75b9407f7cdc589355dde` |
| `specs/compact-current-state-change-record.md` | `a07cbbe6e7b9c703c779ba905d3e6c521a10eb0215db30ff7734206e17b758fc` |
| `specs/skill-contract.md` | `02efe372f358bce68a1d1e85e4dcd4ca6a8686c652f0cb1258d2563884215408` |
| `skills/architecture/SKILL.md` | `3d19519808911916552ba4b841f680ce82f34dbd5e4154dfa7eef4cc6409fa27` |
| `skills/spec/SKILL.md` | `b313228b5a0c4575e63427d183b2da3a7651d1c195fa159b3e3a0ad6ff2edebf` |
| `skills/route/SKILL.md` | `5c9118bb6a389371a19253e83b45310e31bcf080d1d1c1a03a140b7ee70512a9` |
| `skills/proposal/SKILL.md` | `181484512c300a3a1c89af42f289d3986e47aece0973382b0d5bec92dfc586cc` |
| `skills/proposal-review/SKILL.md` | `2f229d90510e45e63e25c228f65f8fe85261214f68e7fa4ed8c979d0ca6dd677` |
| `skills/design-review/SKILL.md` | `4d5805df40fcd54d711899fa88e20f0a25d073b796b3f707b277c09fa105d602` |
| `skills/plan/SKILL.md` | `df0ae5c1fdbd03b15c7d3dffe81e43d01877f70b2b1faca7b0c719c4ad00adad` |
| `skills/delivery-review/SKILL.md` | `527e3f722f8f607ab26f5a7629d6242bfb458d881e6a6448d8d77b6f6f361987` |
| `skills/implement/SKILL.md` | `682196d731cd9a3d91598bcf0b76cbc93c2354712bc67581fa940cc28f50bbbe` |
| `skills/code-review/SKILL.md` | `6879564a4a577113bec5ed02af6dd677fe2d275e7b6ec362384884e7634f30a7` |
| `skills/verify/SKILL.md` | `661bb3314b3f24cbb99f1179e593d8b21bd42eb80ddb127a9c655fe6f9a57f27` |
| `packages/rigorloop/README.md` | `1213b1f7315ee0cc8cdb999de81cec6380cfdd35c3d8d4409c2382f1935a545d` |
| `dist/adapters/README.md` | `947e75b4c9348b98eaac61d36cc5b8844b8a0f6a41452f680fbfa0a895edb5eb` |
| `packages/rigorloop/dist/bin/rigorloop.js` | `9a0422927e0e6b8b2ee6ef7ff6b45482808ff473060f3be178a3a5b157627710` |
| `templates/explicit-recording/records.json` | `f32fc683953f7b6eadbd6c4a34454b716547187ab509970a1557d0b43c049675` |
| `packages/rigorloop/dist/templates/explicit-recording/records.json` | `f32fc683953f7b6eadbd6c4a34454b716547187ab509970a1557d0b43c049675` |
| `scripts/build-record-store-schema.mjs` | `69fd13f1530dc31cccf9f12de035509723fb2188d9ab6512ae04dc4204a98b32` |
| `scripts/validation_selection.py` | `c4b75e7358ebe8b514efa0b8622de015783ee7c5ff2d6914fba5680d51d915a5` |
| `scripts/test-select-validation.py` | `d66d6503a7e1bba1aab19333ece93547a49696682bd84624d3deb2bdf693d409` |
| `scripts/test-skill-validator.py` | `08422daaa2ba9cbfeae0d51a76a58a138fea98cf7692810bfe6bf753329f870d` |
| `packages/rigorloop/test/cli.test.js` | `e1163ebbc40689b46ed2f2663967ac7b41db2c8b35820fd2877b2ef2a2eec452` |
| `packages/rigorloop/test/record-store-cli.test.js` | `4424eb5e1dadcf2df254280d0228d3628b67bb6e9b08f0fca6fcc456e1bc7e03` |
| `packages/rigorloop/test/record-store-contract.test.js` | `55b718c66e918ea3921639d2875d5ee582cbcbc5e1a31ce58b1f77b85aa49ef3` |
| `packages/rigorloop/test/record-store-workflow.test.js` | `35c3d134bd03c014fb9d86c873a88e816ce8b2df0323dc4d177de049d3504d18` |
| `packages/rigorloop/test/helpers/record-store-launcher.mjs` | `54c35e54cfb6b71f9680bcc3a4ba4d133d5fa5949cf33d88f76cbfab1c193fa8` |
| `scripts/test-npm-package-publication.py` | `53daa329a350ed2e79ecad00438a3f4859047009c4a403a31ea3845df03953cd` |
| `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json` | `f5ee6135e446cf6666be0e0dd9b58d4e1879a9a3f20c293baf9122f757093c7a` |
| `packages/rigorloop/dist/metadata/releases.json` | `5eb106135e18db41482c90df775f3663efb8d6bfe511adeecc8e9c9bba758a51` |

The outer-wrapper evidence for ER-M4-004 additionally relies on unchanged `packages/rigorloop/dist/lib/cli-observability.js` (`d7fbd479f574772c842a23e1e9f37432fe5d6b7db06f4dfb8198183ccd8160ab`) and `packages/rigorloop/dist/lib/log-config.js` (`6b6d8fb56077b3359ae47b21bc9aab401e2510beb985ffe5fc5d43a6da070b9a`).

### Adoption checklist and proof assessment

| Item | Assessment | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Four commands and explicit records align with the models; ER-M4-004 breaks the composed selector/result contract. |
| Test coverage | concern | Installed-package seven-test suite passes independently, including all adapters, competing writer, crash/recovery and packed actor scenario; outer logging argument composition is missing. |
| Edge cases | concern | Transaction interruption, stale retry, old/unknown rejection and missing root are exercised; the outer-parser edge is reproduced separately. |
| Error handling | concern | The wrapper can emit a historical error instead of the required recorder envelope. |
| Architecture boundaries | concern | Contract-separated dispatcher is present, but its outer observability dependency is not reconciled completely. |
| Compatibility | pass within observed scope | Historical handlers remain and old-root bytes are preserved by package tests; shared-spec amendments receive a fresh independent Design classification, not the older prospective approval. |
| Security/privacy | pass within observed scope | No payload disclosure was reproduced; storage protections are unchanged. Valid role labels still are not authenticated provenance. |
| Derived artifact currency | pass on named evidence | Canonical/template parity independently passes; installed target initialization checks generated archive identities. Only local-candidate metadata/index entries change. No publication claim. |
| Unrelated changes | pass | Adoption inventory identifies scoped governance, eleven stage profiles, package data, dispatcher and proof changes; original worktree and unrelated compact work remain excluded. |
| Validation evidence | concern | Passing automated proof does not close ER-M4-004; final coordinator CI and independent semantic/rollback proof were pending at this assessment. |

The eleven changed profiles consistently direct new-contract callers to the recorder snapshot and explicit requests, replace historical package/transition/output procedures including their conditional resources, and retain substantive duties. They preserve independent review and final whole-change review, not just stage labels. Their historical resources remain distributed for historical selection; shared reasoning remains applicable, with the model-specific serialization explicitly substituted. The inventory's unchanged support surfaces do not acquire new recording or lifecycle authority. No broader source cleanup or extra Design sidecar is required by this assessment.

Templates are examples, not generated approvals or complete initial requests. The change example starts pending with no registered sidecars; the review example is blocked. Successful Verify metadata is clearly labeled as a shape example and is never included automatically. Contributor documentation explains byte encoding, explicit root creation, stale/conflict handling, the approved external-edit limit and before/after-write rollback boundaries. The new namespace does not call historical transition evaluators.

Independently run for this adoption pass: `python scripts/test-npm-package-publication.py` (seven passed); `node scripts/build-record-store-schema.mjs --check` (passed); `python scripts/test-select-validation.py ValidationSelectionTests.test_explicit_recording_adoption_surfaces_select_real_proof ValidationSelectionTests.test_explicit_recording_package_paths_retain_publication_proof` (two passed); `git diff --check` (passed); and the exact read-only public-command probes recorded in ER-M4-004. Automated actor labels are simulated data; any independent walkthrough is separately attributable evidence, not inferred from the test passing.

## Finding ER-M4-005

- Finding ID: ER-M4-005
- Severity: minor
- Location: `packages/rigorloop/dist/lib/record-store-cli.js:41`, `render`; integrated public text-output path
- Evidence: CLI-SR-11 requires results to name affected identities where available. The text renderer emits status, snapshot content, observations and recovery information, but never emits `revision` or `files` identities. An independently executed real public `record --format text` in a fresh temporary fixture saved the manifest successfully, yet printed only `Record store: saved (storage-only)` and subject-drift diagnostics. Subsequent JSON inspect exposed revision `sha256:f63e4bb434e61308af5351c56b0519bed416054c81f65ba6f7265c719300a1c9` and manifest identity `sha256:27bced182f1ce2e7d7df54e3ce81e4b395391f78ea1745e8b5431054effd5cec`; neither affected manifest path/identity nor revision was present in the text save result. These are disposable fixture identities, not repository approval subjects. The public text/JSON test currently asserts only nonempty text output.
- Required outcome: Human-readable results must identify affected record paths and available identities, with explicit absence/unavailability where relevant, without exposing payloads in errors or implying semantic approval. Preserve the existing JSON envelope and snapshot-content boundaries.
- Safe resolution path: Add targeted public text assertions against the exact JSON/result identities and narrowly render that existing information. Include success and missing-identity representation; do not introduce a new schema or infer decisions. Rereview the affected M2 renderer and integrated M4 proof before closeout.
- needs-decision rationale: None; CLI-SR-11 already owns this output obligation.

This is an existing M2 renderer gap discovered through whole-chain inspection at M4's public boundary, not a change to the approved Design. It is recorded before correction. The temporary fixture was removed after the reproduction; no authoritative repository record was written. Renderer subject remains `packages/rigorloop/dist/lib/record-store-cli.js` SHA-256 `f66067a6f9b8d825e3427cd9119474357ceae0b30065cf95968e5352b4daf676`. ER-M4-004's seven corrected real-binary regressions and the route quick-guide regression independently pass, but M4 and the distinct final whole-change judgment remain unclosed pending this finding and remaining proof.

## Current M4 adoption rereview

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Reviewed milestone: M4, including packaged adoption and preceding prerequisites
- Finding dispositions: ER-M4-004 and ER-M4-005 resolved; ER-M4-001/002/003 remain resolved
- Material findings / required review-resolution: none remaining in this reviewed scope
- Recording status: recorded, advisory only under the explicit isolated-worktree exception
- Milestone closeout: M4 implementation review complete within that exception; no formal settlement
- Artifacts changed by reviewer: this existing review record only
- Open blockers: none for this scoped review
- Next stage: distinct final whole-change Code Review below, not inferred from this result
- Verify readiness: not claimed

ER-M4-004 is resolved by the actual executable's contract-separated raw recorder dispatch. Historical logging flags now reach the closed recorder grammar and produce its rejected envelope; leading historical flags cannot be normalized into an accepted recorder call. Historical commands retain their own wrapper. The seven real-binary regressions and installed-package assertions test the integration boundary that exported-main coverage previously missed.

ER-M4-005 is resolved by rendering the existing revision and affected path identities in text, including unavailable/absent values. The JSON contract and snapshot/error payload boundaries are unchanged. The new actual-public regression checks successful recording and a missing registered record, and installed smoke compares the identities across all three adapters. This is restoration of CLI-SR-11, not a new Design decision. First-pass findings remain above.

Independently run on the corrected subjects: `node --test --test-name-pattern='ER-M4-00[45]' packages/rigorloop/test/record-store-cli.test.js` (eight passed); `python scripts/test-skill-validator.py SkillValidatorFixtureTests.test_progressive_loading_canonical_skills_satisfy_quick_guide_contract` (one passed); `python scripts/test-npm-package-publication.py` (seven passed, actual packed/installed executable); and `git diff --check` (passed). A read-only actual public text inspect of an absent fixture change returned inspected/exit zero and explicitly unavailable revision. Earlier independently run schema parity, selector, boundary and storage-focused results remain attributable to their recorded subjects.

Coordinator-run final evidence reports `bash scripts/ci.sh --mode local` with preflight and all 18 selected checks passing, standalone npm 524 total / 522 passed / two existing skips / zero failures, metadata 115 passed, full adapter suite 157 passed, adapter generation parity and whitespace passing. The full adapter suite binds unchanged guidance/archive subjects; the later renderer additionally has fresh installed-package and final CI coverage. These are reported coordinator results, not commands performed by this reviewer.

The refreshed independent packaged walkthrough is attributable to separate model author and reviewer participants. It proves real correction, independent rereview and proper refusal of unsupported completion. Its overall fixture remains inconclusive, with retained self-author review/open finding byte-identical and no Verify report. The automated installed actor scenario separately covers positive explicit-completion semantics. Together these satisfy TG-FINAL-01's implementation/provenance proof allocation without treating synthetic actor labels as independence or claiming the genuine fixture completed. The actual final installed text/JSON inspect/check/record results agree on revision and all four identities. The three-target rollback physically switches distribution and matching guidance before the first write; post-write write-stop/compatible inspection is separately proven. Neither is confused with transaction restore.

The current adoption classification in the existing independent Design review covers the exact new-profile shared-spec amendments, not the older prospective wording. Historical contracts and release entries remain preserved. No native Claude/OpenCode session, hosted CI, release publication, or repository lifecycle activation is claimed.

## Distinct final whole-change M1–M4 Code Review

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Scope: entire isolated initiative diff against HEAD `d6770adfbbd835363d3b428acbd5a27a9485171b`, M1 through M4, with current proposal, both models, Delivery allocation and evidence
- Review independence: reviewer authored no implementation, Design or plan; prior reviewer-owned judgments are evidence, not implementation authored by the reviewer
- Material findings / required review-resolution: none open against the current reviewed implementation and approved Design
- Recording status: recorded advisory judgment; no fabricated formal root or review identity
- Milestone closeout: M1–M4 implementation and separate final Code Review complete within the user-authorized exception
- Remaining planned work: M5 final verification; not performed or approved by this review
- Next stage: return scoped judgment to coordinator; no automatic Verify, PR or lifecycle mutation
- Verify / PR / release readiness: not claimed

This is a fresh holistic assessment, not aggregation of milestone statuses. I inspected the full isolated HEAD diff and complete recorder schema/runtime, followed the composed public dispatcher, persistence and recovery boundaries, and reconciled the validation, generated package, governing profiles and plan proof allocation. The final whole-chain scrutiny produced ER-M4-005 before its correction. The original worktree's unrelated compact changes are excluded. Current complete-file subject identities below bind both the M4 rereview and this distinct final assessment; this review's own hash is omitted to avoid circular identity.

| Checklist item | Current judgment and whole-chain basis |
| --- | --- |
| Spec alignment | pass — all ten Workflow and eleven CLI requirements are represented across explicit record shapes, actor-owned decisions, one file per model, snapshot interpretation and public storage operations; CLI-SR-11 now holds in both formats. |
| Test coverage | pass within scope — contract, storage, model parsing, selector and actual installed-binary tests cover the plan's proof groups; attributable independent semantic proof is distinguished from automated positive fixtures. |
| Edge cases | pass within approved limits — null/empty values, malformed encoding/selectors, unknown vocabulary, missing members, stale identities, competing writers, interruption and explicit recovery have direct checks. |
| Error handling | pass — public rejected/busy/recovery outcomes retain their contract; observed third states stop, failed structural checks remain failures, and review-required is not approval. |
| Architecture boundaries | pass — the CLI stores explicit actor decisions without lifecycle transitions; model checking owns structure, review owns semantics, and historical handlers are separated. |
| Compatibility | pass — historical roots and procedures are retained without migration; matching generated guidance, candidate identities and before/after-write rollback duties are covered. |
| Security/privacy | pass within approved limits — containment, cooperating-writer exclusion and observed identity checks remain; no payload diagnostics or automatic authentication of role labels is introduced. |
| Derived artifact currency | pass — canonical/packaged schema and template parity, generated adapter/candidate checks and real package installation cover affected outputs without treating the candidate as a publication. |
| Unrelated changes | pass — exact isolated initiative inventory includes required governing reconciliation and proof; no unrelated compact fixes or broader OS/design work is imported. |
| Validation evidence | pass within scope — fresh focused and installed checks, final selected CI, full named regressions and attributable walkthrough support this result; no success-only Verify artifact is fabricated. |

The approved ER-M2-005 limitation remains material to reliance: do not edit records simultaneously through manual or other non-cooperating tools during record/recover. Identity protection applies at observed checks; the final exact-target replacement race is excluded, not repaired. Ancestor containment and cooperating CLI writer exclusion remain mandatory and reviewed. This is not an unconditional external-writer CAS or platform certification.

Model validators and the grandfathered review-required exit-zero handoff validate/report structure, never semantic acceptance. The independent Design classification supplies the separately required assessment for the current shared-spec amendments. Actor decisions and review provenance remain substantive duties; valid record labels alone do not establish them. Completion in the real walkthrough was correctly withheld when its basis was incomplete.

No additional material defect was identified. The final implementation evidence is reviewed at its exact hash below; a subsequent handoff-only wording update must not be represented as new behavioral proof. Changes to implementation, governing guidance or relied-on subjects require affected reassessment. M5/Verify, formal lifecycle settlement, commit, push and release remain outside this completed Code Review.

### Current exact whole-change subjects

| Subject | SHA-256 |
| --- | --- |
| `AGENTS.md` | `52d4ff2dde00cc5d478726155be41c2322115d67bfde3786901a1d0a961eb993` |
| `CONSTITUTION.md` | `ba13fbf7bbce39f8257f91ca07c657f06b3e22658da89807acb3be9512b38a92` |
| `dist/adapters/README.md` | `947e75b4c9348b98eaac61d36cc5b8844b8a0f6a41452f680fbfa0a895edb5eb` |
| `docs/architecture/system/architecture.md` | `f1d2ea08a55eaa99ac849f37ee9b17d5a470be26671b16b179f72de30d277975` |
| `docs/design/cli.md` | `f0bde78dcdd9bd9daaaaf4639df42f712ea9b9a90184f09ad062244558d535a5` |
| `docs/design/workflow.md` | `29f9c0994e6468ee630516198d2e7d0f6a28ebcaae81ab1ea5b9b43d55b3094e` |
| `docs/implementation/explicit-recording-m1.md` | `3dfc7e53a04e49c3c91421c532500af8632610711e25d2c8af7c444c8c46f2c8` |
| `docs/implementation/explicit-recording-m2.md` | `c7af8821db15d8e8cd51d94ee1dccd831a8bb78e6b234c187413e2dd02801c0d` |
| `docs/implementation/explicit-recording-m3.md` | `4a4b6b9a34ae19c1d67ceb87237f578ae2574a33c549b60fca9fb9105626b0f1` |
| `docs/implementation/explicit-recording-m4.md` | `60270373566df89df4ae12994ed4ba12281fe4fb4e40cb2306807d9d50802db4` |
| `docs/plan.md` | `d59116249ec8d288e95c04c2371c231ddacfecbfc8e377abd2f2aa667e1fea16` |
| `docs/plans/2026-09-05-explicit-recording-and-model-centered-design.md` | `2058ebf122e130f7d92f0c5d6dfa464200927ad85f99d4c754893d4ddd4904f4` |
| `docs/proposals/2026-09-05-explicit-recording-and-model-centered-design.md` | `b4efd7fd9010fa0e9af32207afc68abbc847f12f707047c2f640ec7f6e9e44a9` |
| `docs/reviews/explicit-recording-and-model-centered-design-delivery.md` | `a41728e98c4018a3ee9b47c7d0757d8dbf5e95c71e9bc1fcc3232b3b813b9273` |
| `docs/reviews/explicit-recording-and-model-centered-design.md` | `56e21a1a7d0cda7e38516de99347ddc6c95f59c5e256bcf56e3d3bc9f0a04d6d` |
| `docs/reviews/explicit-recording-m1-code-review.md` | `94d54108699b64e2466f1d6bb211b3cdeb9eb9864562993c35e6720a74812349` |
| `docs/reviews/explicit-recording-m2-code-review.md` | `1787d5e21b82ef7599db76020f0b3f2d996ed30c2d33386fa6f1db41bfc3b9e1` |
| `docs/reviews/explicit-recording-m3-code-review.md` | `694bdec6f994f655252d4839cebbdf022f955c11c2b81ac1f8ca06c08b14c984` |
| `packages/rigorloop/README.md` | `71d506c1036aef9b13296364ce59fa041fff7a3a324e3dcefcd8bca1af2e5a5e` |
| `packages/rigorloop/dist/bin/rigorloop.js` | `0e468cf3bbb9c030a8825015d3bc2d3b05e627f291f31f8cbd9147c43b52272b` |
| `packages/rigorloop/dist/lib/record-store-cli.js` | `5d27c3f20f57f770140c705fdad46c2286bb709ee158d4d5296cdb2d77a2a5cc` |
| `packages/rigorloop/dist/lib/record-store-contract.js` | `72a9813be174d2fdeb9dd8c552a5c23fda916befa8d2338107b130ea5f90f458` |
| `packages/rigorloop/dist/lib/record-store-files.js` | `5f83885b5198a8687942488887512344b9daa2ed77856072a9459996b3ed373d` |
| `packages/rigorloop/dist/lib/record-store.js` | `9c76928470276d8ebd1a8a2900cec9a016207b5fb5084f6d893cedf460c56405` |
| `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json` | `1c27e0767d018af9e15f0b5c0a16a55b4d542510b22ee82b8ada1afa131310c6` |
| `packages/rigorloop/dist/metadata/releases.json` | `69ea4ebaf432c328355f2693033e79c03dfebd95a98da82e1facc6a01bbadf31` |
| `packages/rigorloop/dist/schemas/explicit-recording-v1.schema.json` | `3c5c78689dcd2fe31a43bf3b48c684c2c7dcaea3729b67b76b049e1531de38c2` |
| `packages/rigorloop/dist/templates/explicit-recording/records.json` | `f32fc683953f7b6eadbd6c4a34454b716547187ab509970a1557d0b43c049675` |
| `packages/rigorloop/test/cli.test.js` | `c44203eb4495b3c77d238bf96a969b0829746b5dd66ab62547a2771167a59c56` |
| `packages/rigorloop/test/helpers/record-store-launcher.mjs` | `54c35e54cfb6b71f9680bcc3a4ba4d133d5fa5949cf33d88f76cbfab1c193fa8` |
| `packages/rigorloop/test/record-store-cli.test.js` | `feb09e6a639d83eef4e1895421376ffec7ec8ec9e72a5381ccb3b1bd38b973be` |
| `packages/rigorloop/test/record-store-contract.test.js` | `55b718c66e918ea3921639d2875d5ee582cbcbc5e1a31ce58b1f77b85aa49ef3` |
| `packages/rigorloop/test/record-store-workflow.test.js` | `35c3d134bd03c014fb9d86c873a88e816ce8b2df0323dc4d177de049d3504d18` |
| `schemas/explicit-recording-v1.schema.json` | `3c5c78689dcd2fe31a43bf3b48c684c2c7dcaea3729b67b76b049e1531de38c2` |
| `scripts/boundary_first_validation.py` | `403d9c77f2c8fe3a99a532157c2b5ad639b23ca6a405f20757d92b969f5e04af` |
| `scripts/build-record-store-schema.mjs` | `69fd13f1530dc31cccf9f12de035509723fb2188d9ab6512ae04dc4204a98b32` |
| `scripts/test-boundary-first-validation.py` | `832b6f0754f89350bd1cdb11fa8ba80fb16f3530461f93c551d55f1e055cf997` |
| `scripts/test-change-metadata-validator.py` | `44d5ab15486006f90fd156a11021e823377eacc5614616cdd570b3c40a89100d` |
| `scripts/test-npm-package-publication.py` | `b369e63983d4456a9f1a4ae1108040b3b593006358ff47ab64c20e66b81ffc44` |
| `scripts/test-select-validation.py` | `d66d6503a7e1bba1aab19333ece93547a49696682bd84624d3deb2bdf693d409` |
| `scripts/test-skill-validator.py` | `08422daaa2ba9cbfeae0d51a76a58a138fea98cf7692810bfe6bf753329f870d` |
| `scripts/validate-boundary-first.py` | `3d12bb1991e923ae9a409ecde67e49fe1c73a63c461f05a1e16510cd20b65288` |
| `scripts/validate-change-metadata.py` | `5d3829970b9695841f132bea7d6c61e56d0f45a512ec9057482b5f5f7c2de399` |
| `scripts/validate-record-store.mjs` | `339baf0fdcae22d77bc427c11ee483f275720b91a6d89d2254efae355eda16c6` |
| `scripts/validation_selection.py` | `c4b75e7358ebe8b514efa0b8622de015783ee7c5ff2d6914fba5680d51d915a5` |
| `skills/architecture/SKILL.md` | `3d19519808911916552ba4b841f680ce82f34dbd5e4154dfa7eef4cc6409fa27` |
| `skills/code-review/SKILL.md` | `6879564a4a577113bec5ed02af6dd677fe2d275e7b6ec362384884e7634f30a7` |
| `skills/delivery-review/SKILL.md` | `527e3f722f8f607ab26f5a7629d6242bfb458d881e6a6448d8d77b6f6f361987` |
| `skills/design-review/SKILL.md` | `4d5805df40fcd54d711899fa88e20f0a25d073b796b3f707b277c09fa105d602` |
| `skills/implement/SKILL.md` | `682196d731cd9a3d91598bcf0b76cbc93c2354712bc67581fa940cc28f50bbbe` |
| `skills/plan/SKILL.md` | `df0ae5c1fdbd03b15c7d3dffe81e43d01877f70b2b1faca7b0c719c4ad00adad` |
| `skills/proposal-review/SKILL.md` | `2f229d90510e45e63e25c228f65f8fe85261214f68e7fa4ed8c979d0ca6dd677` |
| `skills/proposal/SKILL.md` | `181484512c300a3a1c89af42f289d3986e47aece0973382b0d5bec92dfc586cc` |
| `skills/route/SKILL.md` | `298ad4ec122811f3e3b6d759154eb5172a88910c4b47d3ec6dd7703bfe3150fe` |
| `skills/spec/SKILL.md` | `b313228b5a0c4575e63427d183b2da3a7651d1c195fa159b3e3a0ad6ff2edebf` |
| `skills/verify/SKILL.md` | `661bb3314b3f24cbb99f1179e593d8b21bd42eb80ddb127a9c655fe6f9a57f27` |
| `specs/boundary-first-proof-model.md` | `a166b68a673d485c83a0b665446933c774406b03a4f464b205426ae9b8b315bb` |
| `specs/compact-current-state-change-record.md` | `a07cbbe6e7b9c703c779ba905d3e6c521a10eb0215db30ff7734206e17b758fc` |
| `specs/rigorloop-workflow.md` | `b755687df0f75199dbab35438895bb23fe26a2e150d75b9407f7cdc589355dde` |
| `specs/skill-contract.md` | `02efe372f358bce68a1d1e85e4dcd4ca6a8686c652f0cb1258d2563884215408` |
| `templates/explicit-recording/records.json` | `f32fc683953f7b6eadbd6c4a34454b716547187ab509970a1557d0b43c049675` |
| `tests/fixtures/explicit-recording-v1/records.json` | `d26bcaf4b366160e55968f56e9c39d4d22e418689ee2b80ed12e215c803f856c` |

### Evidence handoff freshness acknowledgment

Independently inspected the subsequent M4 evidence title, opening, core-result and handoff-closeout wording. It accurately references the completed M4 and distinct final whole-change judgments, preserves their limitations, and leaves M5 separately authorized. No new behavioral proof or implementation approval is introduced. The current `docs/implementation/explicit-recording-m4.md` SHA-256 is `8a94a65a1ea390f5917393d5eaa21aa78daf42da15d235e6e89e5d6e68c6830b`, superseding only its earlier evidence identity above. Tested-subject identities, finding dispositions and both clean-with-notes judgments remain unchanged. Independently checked the file hash and ran `git diff --check`; both passed. This acknowledgment adds no lifecycle settlement or downstream execution.
