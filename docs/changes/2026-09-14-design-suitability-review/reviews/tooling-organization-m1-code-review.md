# Tooling organization M1 independent Code Review

## Result

- Skill: code-review.
- Status: completed correction review.
- Artifacts changed: this review only.
- Review status: approved.
- Open blockers/material findings: none; TCR-01, TCR-02 and TCR-03 resolved.
- Next stage: fresh independent final whole-change Code Review, then distinct scoped Verify.
- Recording status: recorded, advisory-durable/manual.
- Reviewed milestone: M1 of tooling-organization plan.
- Milestone closeout: complete for this scope; remaining implementation: none.
- Verify readiness: not-claimed.

## Finding TCR-01

- Finding ID: TCR-01.
- Severity: major.
- Location: `scripts/lib/validation/validation_selection.py`, catalog and dependent selectors; corresponding changed test expectations.
- Evidence: source relocation changes the externally reported canonical IDs `release_evidence.validate`, `release_transaction.regression` and `validation_execution.regression` to names prefixed with `lib.release.` or `lib.validation.`. These are serialized check identities, not Python module imports. Baseline-relative comparison shows test expected IDs changed in parallel, which can conceal the regression despite passing fixtures.
- Governing requirement: ENG-SR-16 and Validation Tooling placement explicitly preserve canonical check identities, results and command behavior; no ID migration is approved.
- Required outcome: restore original catalog/check/result IDs and all callers/assertions expecting those IDs; retain qualified imports and mock targets where those actually denote modules.
- Safe resolution: inspect every changed string, distinguish module reference from protocol/check identity, restore original IDs and add an independent baseline literal identity assertion or equivalent focused proof. Re-run selected/catalog/executor protection and current routing.
- Owner: implementation.

## Finding TCR-02

- Finding ID: TCR-02.
- Severity: major.
- Location: `scripts/lib/release/release_candidate.py`, recursive `script_identity` enumeration.
- Evidence: `Path.rglob('*')` does not traverse symlink directories, and the `p.is_file()` filter drops those directories before `file_identity` can reject them. In an owned temporary fixture, reviewer created `scripts/lib/validation` as a symlink to a directory containing helper.py. Changing that helper's bytes left `script_identity(scripts)` unchanged, with no rejection. Thus a loadable nested authored subtree can escape the newly required identity guard.
- Governing requirement: Engineering's complete authored scripts identity and Release's loaded/candidate integrity boundary; moving code cannot remove it from the checked identity. Delivery requires missing/unsafe inputs not silently shrink protection.
- Required outcome: unsupported symlinked maintained code/resource subtrees reject explicitly rather than silently disappear from identity. Generated-bytecode exclusions remain intentional.
- Safe resolution: inspect directory and file entries before filtering maintained source, reject unsafe symlinked authored inputs (including directory links), and preserve regular nested source/resource hashing with relative keys. Add a negative symlink-directory regression and rerun actual candidate mismatch checks; do not follow arbitrary external roots.
- Owner: implementation; no new release-policy decision required.

## Scope and independence

Author `/root` implemented the slice. Separate reviewer `/root/validation_design_review` edits only review evidence. The review compares the original tooling baseline tar to the explicit twenty-one-file move map and current consumers. Previous test relocation remains baseline. Findings were recorded before author corrections. The narrow Validation unknown-path wording correction has separate explicit Design/Delivery applicability records; it does not authorize check-ID changes or weakening source identity.

Full source/test review and required full execution remain in progress. This first-pass record preserves actionable findings without claiming pending tests passed or approving the entire accumulated branch.

## Finding TCR-03

- Finding ID: TCR-03.
- Severity: major.
- Location: `scripts/lib/validation/validation_selection.py`, four initializer entries in `_TOOL_PATH_PREDECESSORS`.
- Evidence: new package initializers are assigned a representative old module as a synthetic predecessor. Root `lib/__init__.py` runs before all Python descendant imports, but maps only to the selector. Packaging initializer runs before both adapter and npm helpers, but maps only to adapter distribution. Passing representative checks does not cover all actual import consumers. These files have no old deployment predecessor.
- Governing requirement: ENG-SR-16 and Validation owning responsibility require supported new tooling paths to retain meaningful affected-reader selection; Delivery TG1 includes the complete routing and consumer map.
- Required outcome: select the finite union of existing descendant consumer protection for each package initializer, including npm qualification for Packaging and all three owner groups for the root initializer. Preserve unknown-path rejection and original serialized check IDs.
- Safe resolution: explicit package initializer responsibility mapping, separate from actual relocation predecessors, with focused assertions for required existing check sets. No synthetic broad directory acceptance or new catalog identities are needed.
- Owner: implementation.

## Correction inspection in progress

TCR-01 source now restores the three original check IDs. Author's isolated baseline/current catalog comparison reports all forty-one keys and command templates identical. TCR-02 now checks symlinks before file filtering, including directory links and root links, while intentionally excluding bytecode. The focused nested code/resource, symlink-directory rejection and actual candidate-boundary cases pass. These corrections are suitable on inspected source; complete current selected proof remains pending. TCR-03 was recorded before its correction.

## Exact corrected review subjects

The CLI inspected these sixty-three subjects after the initializer correction. The twenty-one-source move map is compared against `/tmp/tooling-organization-baseline/sources.tar`; removed old internal/resource paths are part of scope, except the intentionally retained thin release-evidence command. Earlier branch changes form baseline and are not approved here.

| Subject | SHA-256 identity |
| --- | --- |
| `CONTRIBUTING.md` | `sha256:fa259933a9f5a0237bcd9cf6afc26d424f6bb5515873e5303c0437dfdaa1e4f0` |
| `docs/design/engineering/engineering.md` | `sha256:cadf64631c82db8341bb3d67b892582dee5f0670f827c36b62968e59a395f64c` |
| `docs/design/engineering/packaging.md` | `sha256:0aec3cfc2bf73424bf08d8c4efb775e4f7b5051b8417e8ebf1c90ada91aedbfa` |
| `docs/design/engineering/release.md` | `sha256:1cae90f16d152c7811eec499036dc4e7f8f63f82acd62d6b71c58f131d5f19b8` |
| `docs/design/engineering/validation.md` | `sha256:96139f158cf9f2097afebf1ed6dd72729a64c8610fe71fd37bb17ee49dcf90d8` |
| `docs/design/system.md` | `sha256:4eedbac3ea4702f50c84ebafec521663759debe48b183496272e9d420e1b1f86` |
| `docs/plans/2026-09-14-tooling-organization.md` | `sha256:120d4d3bc980a7831663d3e8905aa3c19858d483fe6ed242d880d8481e137072` |
| `docs/project-map.md` | `sha256:57fba62f2bcf11d3f74bab801a4c78f6828581a9746d34228b1c69943019acee` |
| `scripts/build-adapters.py` | `sha256:05f4689343582213f51e320ee84b69f3301cd8440fa41a9fbc1b02b3a632b48f` |
| `scripts/ci.sh` | `sha256:9f03477a3dc5da070181ed4bc973c5ba4de620c5519510afb541bf25503f63c0` |
| `scripts/classify-record-store.mjs` | `sha256:4f5bc31f7f0b96b77ac95df60aab63ba428a29ed7acddef39919cb2d46dfd00a` |
| `scripts/close-release-publication.py` | `sha256:f5dcf960c963116b146b25f2354c16d1417bcf7cb8c53d37f0cbda8c9a80b231` |
| `scripts/lib/__init__.py` | `sha256:a475fe529b9464273e1cf43cf390decb9b7073a0a7aafe10ed7c134a1255d244` |
| `scripts/lib/packaging/__init__.py` | `sha256:26483913fed28d1d1e2a96f9fd0fe5b6086664163f1a84ba483184867a49a1ea` |
| `scripts/lib/packaging/adapter_distribution.py` | `sha256:e8ea363bdae9191cabf683df0b6fa7f5d01a361cbd3c13b5f77efd3792932124` |
| `scripts/lib/packaging/npm_package_validation.py` | `sha256:88265d284dc554c8f73b64df1309c54493f2e3ad27ce5248942c34b6bc37474a` |
| `scripts/lib/release/__init__.py` | `sha256:0474ba4eaf4c7e5cbe085189f35242ef2697f8ab8e1215d0a1ed6d9649f3d827` |
| `scripts/lib/release/release_candidate.py` | `sha256:e6ccfe19fc3fe7c101b3900d9b2f36debb5f3c62acaf79b5721b1ecd6c43d162` |
| `scripts/lib/release/release_coordination.py` | `sha256:2375f4e50b8f49bdef84fdee3715a7487c0a72d0a1c13aa87411ca1db71086ba` |
| `scripts/lib/release/release_evidence.py` | `sha256:780c388366ddd39d601792d38723e281ba0c0248ee73f64c9e53fea5f301fb63` |
| `scripts/lib/release/release_execution.py` | `sha256:b72520ed6e1f7b7244533dce6856a114def501c19fdb96525365453301ae4e4f` |
| `scripts/lib/release/release_provider.py` | `sha256:4d6b854ce2a1f8f9911ecf48765c196a8e2971f5ae7ae80d90d07b56b9017d2e` |
| `scripts/lib/release/release_transaction.py` | `sha256:779e86f05bf64da7f9eb91aa01abeb2e13ddb5f51d4413b6b13c3dbfc8625dbc` |
| `scripts/lib/validation/__init__.py` | `sha256:c5e7f5224503ad3831c673814967d35154554f2ffd74e21e71c0e498c7f7d281` |
| `scripts/lib/validation/boundary_first_reference.py` | `sha256:d2e536f938312d4ac2ba06b40477be58b706c28162b8592881d792333af9d9a5` |
| `scripts/lib/validation/boundary_first_validation.py` | `sha256:b55874a5f7d9c3af9cb9cbd66fbc7939f7aba30c3ba54931d8f251f923bf5426` |
| `scripts/lib/validation/model_layout.py` | `sha256:8b518a76baf1d9b8e1aa1e44c64b7419053d18df4c7ea775f2eaccc62fe6062f` |
| `scripts/lib/validation/project_yaml.py` | `sha256:19f6578eeca9e5bef371500710477034e550b57297e18cbf4eb22fcc51d4c9d7` |
| `scripts/lib/validation/record_snapshot_git.mjs` | `sha256:8c6bedfcc75f7a3c1df262c7a720d0b0d3326901c76f98b055aa7ee8e0a9e3ce` |
| `scripts/lib/validation/record_store_classification.py` | `sha256:9ec9b7cee1d8aac02df56aff79f63fc8a97a264a09c970ffee9f0dba5d921495` |
| `scripts/lib/validation/skill_validation.py` | `sha256:ff05600fd3cd81584a7eac99105e9802c00c5813d995bddc1dea013371d8fbb4` |
| `scripts/lib/validation/validation_execution.py` | `sha256:132a133c71cef31f4aefbb49835c4269c9cd80ba492686e9988b4573e776b9f3` |
| `scripts/lib/validation/validation_node_adapter.mjs` | `sha256:4ff0c3964282dcd004ff906dfdfacb9e5c9c4ef0ede5a2bda9be1e7c71381da4` |
| `scripts/lib/validation/validation_selection.py` | `sha256:312ab4bc594e58593135b8395dff0f9b7cb55c7a40e39eca92c39decf03999c5` |
| `scripts/prepare-release.py` | `sha256:0b017e0ab48898083dd0b6579de1a5e8fe3a35c7d6c5de95262412bfd99af65a` |
| `scripts/project-boundary-first-reference.py` | `sha256:c0d4ea281726275b5c5f929ea686179b6ff8f31ec0e5927d0df0a48b31aa9508` |
| `scripts/release-coordinator.py` | `sha256:5235bf6e07ad9e57858c15574009a9c39c5d8dc10932d8aba52b9a545c3d98b8` |
| `scripts/release-preflight.py` | `sha256:4fafb659d62f530be1ccc88900a0881eb0cf0dcb79729307c7862bf37a5ec9df` |
| `scripts/release-verify.sh` | `sha256:379e14ae9c190a6293eeb0a9cd78b79e0ed9d91ede88441b23808aad2a312513` |
| `scripts/release_evidence.py` | `sha256:ce6640b6a4f29a0841d46de174ece31444b7fbad010f0073663bb227368aac44` |
| `scripts/resources/adapter-templates/claude/CLAUDE.md` | `sha256:9252777761edc382999710a0f4fa8cc221eaca00e43abca7448387d4783ce94a` |
| `scripts/resources/adapter-templates/codex/AGENTS.md` | `sha256:3c395fbf2c82aa3372a040e521375ff79a904f7397cdc792c29a28d8564c7db7` |
| `scripts/resources/boundary-first/boundary-first-resources.yaml` | `sha256:d7806a57f7cf4d4b6329da679d8b1e96189908833d8fa8337d5be45ae9a8cb18` |
| `scripts/select-validation.py` | `sha256:4eeb52c295358ab195c8a139ccd71d6b33b068ddeb29845e6e16af40a4aee56c` |
| `scripts/validate-adapters.py` | `sha256:c312233283f2fb2b175d29f59edfb46da3dd0f990152f366428f061ec6761689` |
| `scripts/validate-boundary-first.py` | `sha256:caa4bc96e3f7af566bf8d96d5cf63409b5903ac25de8f268740abfd4ed05b2f7` |
| `scripts/validate-guide-system.py` | `sha256:fe2934d930187290fb016138f203f7eef4a6b11714f6bc62eac9e73f7e3f15bf` |
| `scripts/validate-npm-package.py` | `sha256:699a652ad29f15fddbebd1f1273ef178253ec535eae823ddf084545684edcc61` |
| `scripts/validate-record-store.mjs` | `sha256:95728e886a0f8b91ba828b3fe38691686065f2b1dd6c47dbb07f775d4e9b6dc2` |
| `scripts/validate-release.py` | `sha256:8d4591a5b7683425eb237dc667d02d1e362c256ec19e2cb04ec7eb67f66b2116` |
| `scripts/validate-skills.py` | `sha256:3711d0996eab2b5f079a06c91d29960b65377c2fb860db7b27674ed4f64d7ac8` |
| `tests/engineering/packaging/test-adapter-distribution.py` | `sha256:41464128d1ae09979f90f06bdbe4cde6d44960c324beae05eba217fe928017bd` |
| `tests/engineering/packaging/test-npm-package-publication.py` | `sha256:ea822eb2304e6bf4584ff36a1680bb2d28d12fa7489f522f9a71141a248fd922` |
| `tests/engineering/release/release_candidate_tests.py` | `sha256:b4d96a8cbeb90c265d3359a6f0d47443fd2d534de06dd4fade42dc009201c1a2` |
| `tests/engineering/release/release_coordination_tests.py` | `sha256:1ef60b0ebff61f4834c5a092ba00bb926686defa90d836da75a2c95bd06a3390` |
| `tests/engineering/release/release_evidence_tests.py` | `sha256:a32097648ca5d66e788092872f51e416d9e11ca50b87c96d3263a8e206942809` |
| `tests/engineering/release/release_execution_tests.py` | `sha256:69fb000f68ef0926534cbb29ae95dd4d38866bfc5a21acf66b128e35a517d921` |
| `tests/engineering/release/test-release-transaction.py` | `sha256:5353fa1165740406a99d813836977a11c553ee1b92b639fc31d30f685df7397b` |
| `tests/engineering/validation/test-boundary-first-reference.py` | `sha256:9d13e5af2fdff369007a13d63c180960e9fe11910be2047c0bead0470991b74d` |
| `tests/engineering/validation/test-boundary-first-validation.py` | `sha256:c77947b6b9de79ee781ae84bb6a97664f7439f8b837c7cb7702e065de88e2989` |
| `tests/engineering/validation/test-select-validation.py` | `sha256:886f4c5b6e342f3edce8a228e7b72997b1cb26ff4f5ed73e1ce87d99dde46a22` |
| `tests/engineering/validation/test-validation-execution.py` | `sha256:9f7e3f5a9ae5173c375523900577ca60e11c82f775ceb5433c67d8454141d341` |
| `tests/skill/test-skill-validator.py` | `sha256:c71ccf44471be322b9334fe374ba53ea1d34bc0e7307b6f938ebf328f33550ee` |

TCR-03 correction independently inspected: the four exact initializer paths now select explicit unions of existing descendant checks, separately from actual predecessor paths. The regression failed for Validation, Packaging and root scope before correction and passes afterward; unknown initializer paths remain blocked. No further material source finding remains. Final judgment still awaits applicable execution.

## Applicable execution and checklist assessment

The author ran `bash scripts/ci.sh --mode local --broad-smoke --jobs 4`: exit 0, 1,364 passed check/case rows and no other row statuses. Reviewer inspected the completed log, including actual candidate build and packed metadata chain (81.56 seconds), actual npm package/installed smoke, current record snapshot boundaries, and archive build/validation. The original selector loaded before the initializer correction; this run does not establish final initializer selection by itself. Current focused initializer/move tests pass, current local selection reports no unknown paths or blockers, and an additional complete current selector run is pending to remove timing ambiguity. The candidate case launched after source freeze, so its exact source identity observation applies to the corrected code. Earlier pre-correction candidate success is not substituted for this current observation.

Reviewer independently compared baseline and current discovery: all 929 baseline cases retained among 934 current cases, with exactly five new routing/source-identity methods. All three relocated authored resources retain identical bytes. All sixty-three recorded subjects still matched the current files when checked. The forty-one canonical catalog IDs and command templates match baseline after TCR-01 correction. Author direct archive suite passed 96 cases; direct absolute skill validation from another working directory passed 19 skills. These supplement, rather than replace, relevant selected execution.

| Checklist item | Assessment and evidence |
| --- | --- |
| Spec alignment | Pass: stable commands, owner directories, explicit imports and complete nested release identity implement ENG-SR-16 and exact approved five-model package. |
| Test coverage | Pass subject to pending complete selector closeout: preserved case population, meaningful new move/initializer routing and real candidate identity regressions; no test deletions or semantic skill harness. |
| Edge cases | Pass: copied repositories, worker subprocesses, bytecode exclusion, symlink rejection, missing source root and nested authored resource changes assessed. |
| Error handling | Pass: unknown tooling paths still block; source identity rejects unsafe inputs; thin release-evidence command preserves main return/exception behavior. |
| Architecture boundaries | Pass: finite capability package imports, colocated Node worker/helper and authored resources; no duplicate moved implementation. |
| Compatibility | Pass: all original catalog identities/templates and supported command paths retained; consumers and fixture copies updated together. |
| Security/privacy | Pass for relocation scope: no new credentials/publication actions, no arbitrary external symlink traversal, loaded/source guard extended. |
| Derived artifact currency | Pass: actual archive validation, npm packed/installed smoke and candidate build/metadata chain completed; no generated adapter source edited. |
| Unrelated changes | Pass: original working-tree tar is comparison baseline; earlier design/test work is excluded from this judgment. |
| Validation evidence | Pending final complete selector run; completed full run and focused corrected evidence are explicitly bounded above. |

No current engineering finding remains unresolved on source. Final milestone approval is withheld until the pending complete selector observation is available. This review does not assert hosted CI status, external release safety, branch readiness or scoped Verify completion.

## Final correction judgment

Approved for the scoped M1 implementation on the exact subjects above. The final current selector command `python tests/engineering/validation/test-select-validation.py` completed successfully: 181 passed in 119.33 seconds, exit 0. This replaces uncertainty about the original full-run selector load timing. Together with the completed 1,364-row selected local/broad execution, focused failed-before/passed-after regressions and current local selection, the required milestone proof is adequate. Reviewer rechecked all sixty-three subject hashes after this result; none changed.

TCR-01 is resolved by restoration of every original catalog identity and independent full catalog/template parity. TCR-02 is resolved by pre-filter symlink rejection and real candidate-boundary proof covering moved code and authored resources. TCR-03 is resolved by finite initializer consumer unions, original catalog IDs, and independent required-descendant scope assertions. Earlier findings and failed observations above retain their historical meaning; the final correction judgment supersedes their open status.

All ten checklist items pass for the bounded implementation scope, including validation evidence and complete selector coverage. No material finding remains. This is independent advisory-durable milestone approval by nonauthor reviewer `/root/validation_design_review`; it invents no governed lifecycle state. A separate fresh final whole-change Code Review remains required before the root assessor performs scoped Verify. No hosted CI, branch-wide readiness, PR, deployment or publication claim is made.
