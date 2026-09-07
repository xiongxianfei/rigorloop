# Explicit Recording M4 — Packaged CLI and Activation Proof

## Authority and bounded scope

The user approved M4's activation mechanism: enable the existing `record-store` namespace after integration checks and review; new roots require an explicit `explicit-recording-v1` record request. No new configuration layer, automatic status changes, migration, commit, push or release is implied. This records that approval, not completed adoption.

The governing basis is the two reviewed [Workflow](../design/workflow.md) and [CLI](../design/cli.md) models, the [delivery plan](../plans/2026-09-05-explicit-recording-and-model-centered-design.md), its advisory Delivery Review and the clean-with-notes [M3 rereview](../reviews/explicit-recording-m3-code-review.md). The existing isolated implementation exception continues; no formal root, review ID or lifecycle settlement is fabricated. The last exact `workflow-context` check reported `RL_CONTEXT_CHANGE_NOT_FOUND`. The plan's direct source inventory supplies orientation; no project-map inference is used.

The initial handoff covered M4 validation prerequisites under WF-SR-10, CLI-SR-02/07/10 and CLI-MAP-07. The later packaged adoption candidate below extends that scope under the user's explicit request. M4 proof and both required reviews are now complete within the isolated exception; no public distribution is changed.

## Exact implementation inventory

| Surface | Change and proof |
| --- | --- |
| `scripts/validation_selection.py` | Select existing plan-owned package, schema, model, boundary and metadata checks for new model and record-store surfaces. Preserve tracking preflight and fail-closed handling of other unclassified paths. |
| `scripts/test-select-validation.py` | Six-path selection regression plus updated exact catalog/parallel-safe inventory. Five original cases failed before implementation; focused and full tests pass after correction. |
| `scripts/validate-change-metadata.py` | Explicit JSON contract dispatch invokes bounded Node validation; historical YAML/compact paths retain their existing validators. Unknown or mixed contracts reject. |
| `scripts/validate-record-store.mjs` | Read-only coherent recorder inspection and existing complete-set structural validation. Missing records, malformed data and unsafe paths reject; stale subjects and recorded workflow decisions do not become eligibility checks. No new public command or schema. |
| `scripts/test-change-metadata-validator.py` | Four new tests cover incomplete/completed decisions, unknown and mixed contracts, duplicate keys, encoding, symlink rejection, missing/malformed supporting records and stale subjects. The two positive cases failed before dispatch support. Preexisting unrelated changes are preserved. |
| `scripts/test-npm-package-publication.py` | Pack/install smoke reads the actual package version instead of the intentionally older release-transaction fixture. Existing real installed-binary assertions remain unchanged. |
| `packages/rigorloop/test/cli.test.js` | Refresh the candidate tree-hash expectation from regenerated and parity-checked metadata; preserve the historical v0.5.0 byte-identity assertion. |
| `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json`, `packages/rigorloop/dist/metadata/releases.json` | Regenerated only local-candidate adapter identities through existing archive/candidate generation; refreshed that candidate's index digest. Historical entries and release metadata remain byte-unchanged. No publication or archive is committed. |

The selector uses commands already allocated by the plan or schema-generation evidence. CI maintenance supplies coverage placement; implementation owns tests and the actual runs. No CI workflow, permission, cache, installed skill mirror or generated public archive is edited. No whole-repository tracking exclusion or generic advisory-artifact exemption is introduced.

## Original-worktree commands and results

- `python scripts/test-change-metadata-validator.py`: 116 passed.
- `python scripts/test-select-validation.py`: final rerun 158 passed. The initial run found the newly added checks missing from the test's explicit parallel-safe expectation; the expectation was reconciled without weakening the assertion. Later correction proof is below.
- `npm --prefix packages/rigorloop test`: 525 total, 523 passed, two existing skips, zero failures.
- `python scripts/build-adapters.py --check`: passed for v0.5.1; this is parity of the still-prospective guidance, not activation or an integrated adapter walkthrough.
- `node scripts/build-record-store-schema.mjs --check`: passed.
- `python scripts/validate-boundary-first.py --check --path docs/design/workflow.md --path docs/design/cli.md`: passed, structure/reference-only.
- `git diff --check`: passed at prerequisite handoff.
- `python scripts/test-adapter-distribution.py`: 157 tests ran; 156 passed and the candidate-metadata parity test failed. That failure was corrected and its exact test separately rerun as described below; the full suite was not rerun after regeneration.
- `python scripts/test-npm-package-publication.py`: final rerun seven passed, including actual tarball installation and all three adapter target installations.
- `bash scripts/ci.sh --mode local`: preflight blocked before checks. New model/record-store path gaps were reproduced and corrected; authoritative tracking and isolated advisory-path handling remain unresolved.

## Activation blockers and remaining work

The actual worktree contains untracked authoritative artifacts from this initiative and unrelated earlier changes. Local CI requires them to be tracked before broad branch-readiness proof. It also does not classify the isolated `docs/implementation/` and `docs/reviews/` records authorized for this initiative. Staging unrelated work, disguising advisory evidence as formal lifecycle records, or treating skipped preflight as passed would not resolve those issues truthfully. These are integration/validation-basis constraints, not CLI status deadlocks.

Remaining M4 work includes a resolved validation basis, explicit public dispatch/help and historical command isolation, new-contract scaffolds and contributor rollback guidance, governing/skill cutover, generated adapter integration and independent semantic walkthrough, TG-07/TG-FINAL-01/02, M4 review and distinct final whole-change Code Review. No part of this prerequisite handoff substitutes for those gates. After new roots exist, preserve compatible readers and stop writes/fix forward; do not delete or reinterpret records for rollback.

## Correction and packaging handoff

Independent first-pass review recorded ER-M4-001 before correction: record-store package classification lost the existing tarball/installed-binary check. A new exact-selection test reproduced four failing package-path subcases. The corrected selector retains `npm_package_publication.test` and reuses `rigorloop_cli.test` rather than scheduling a duplicate npm suite. A separate tests-first correction retains the existing authoritative-tracking preflight for model files; draft model structural validation itself still needs no Git registration. Focused checks and the final full 158-test selector run pass. Finding disposition remains reviewer-owned.

Running the restored publication check first exposed a current-package/old-fixture mismatch (`0.5.1` versus `0.5.0`). Selecting the actual package version retained real version/compatibility assertions and exposed stale bundled candidate archive identities from before M3. The full adapter suite independently found the same candidate-metadata mismatch. Existing `build_adapter_archives` and `_prepare_local_cli_release_candidate` generated fresh temporary output; only the generated v0.5.1 local-candidate metadata was copied back, with its derived index digest mechanically refreshed after checking the previous identity and local-candidate markers. No historical release entry was rewritten and no archive-verification check was weakened.

After regeneration, `python scripts/test-npm-package-publication.py` passes all seven tests and `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_v0_5_1_bundled_candidate_metadata_matches_generated_route_only_archives` passes. `git diff --check` passes. These fixes and generated identities are part of the independent prerequisite rereview, not an adoption claim.

The package rerun then identified one old literal candidate tree hash in `TNP-005`. Its expected hash was refreshed from that generated, parity-checked candidate without changing the retained historical metadata assertion. The final original-worktree rerun passes all 523 tests with two existing skips (525 total).

## Isolated validation basis

The user explicitly approved a separate clean worktree. It starts at `d6770adfbbd835363d3b428acbd5a27a9485171b` with exactly 59 initiative files copied and staged for validation, without a commit. Unrelated compact-engine/schema/fixture changes and earlier proposals/change roots were not transferred. The one unrelated 22-line compact-review test addition was excluded from the copied metadata test file; its original remains untouched. Other copied bytes match the initiative inventory. Original worktree state is preserved; further work occurs only in this isolated worktree.

A tests-first selector amendment recognizes exactly this initiative's ten already-authorized advisory evidence files. It selects prose audit and underlying model/runtime checks, not formal review settlement, and leaves arbitrary `docs/reviews/unknown_value.md` unclassified. The regression initially failed and now passes. Model/source tracking checks remain enforced; no untracked-artifact exception was added.

`npm ci --prefix packages/rigorloop --ignore-scripts` succeeded in the isolated worktree. Its `bash scripts/ci.sh --mode local` preflight now passes and executes all 16 selected checks. Fifteen pass, including model validation, schema parity, skill and selector regressions, metadata, lifecycle, prose, CLI tests and installed-package proof. The remaining selected check is the legacy `boundary_first.validate` invocation:

`python scripts/validate-boundary-first.py --check --path specs/boundary-first-proof-model.md --path specs/compact-current-state-change-record.md --path specs/rigorloop-workflow.md --path specs/skill-contract.md`

It returns `BFR-GRANDFATHERED-REVIEW` for `specs/rigorloop-workflow.md` and `specs/skill-contract.md`, requiring “semantic spec-review”. In `validate_changed_spec`, an active grandfathered file without the historical boundary marker unconditionally returns this issue; no classification result is consumed. The recorder and new model validator are not failing. The current Design preserves historical validation and uses model-owned tables for the new profile, so silently inserting a historical boundary marker, skipping the files or inventing an approval would change the approved boundary. Route must obtain the Design owner's resolution and affected independent review before dependent activation. No new model file is necessary.

## Approved grandfathered-review handoff correction

The user authorized implementation after the independent Design rereview resolved ER-M4-002's owner decision. This bounded correction implements WF-SR-07/08/09/10's Model validation and proof mapping under TG-06/07; it is not complete M4. The existing advisory Design record independently classifies the exact two shared-authority additions as new-profile-only. No classification is inferred from an exit code or supplied by the validator.

Changed surfaces: `scripts/validate-boundary-first.py` separates only `BFR-GRANDFATHERED-REVIEW` into path-bearing `review_required` observations owned by Design Review, returns `review-required`/exit zero for structural success and preserves observations alongside structural or rollback failures. Every other diagnostic, including an unknown code, still fails. `scripts/boundary_first_validation.py` names the current review owner and rejects unknown grandfathered markers and partial malformed adoption rather than silently accepting them. `scripts/test-boundary-first-validation.py` adds seven focused tests. The approved owner-stage reconciliation in `specs/boundary-first-proof-model.md` retains feature-format/activation rules and binds the reporting and classification handoff to the existing Workflow model; it introduces no new Design truth or lifecycle transition.

Tests first: the initial five-test run reproduced review-only failure, missing mixed-result observations and silent acceptance of an unknown grandfathered marker. After correction, all seven focused tests pass. They exercise the real selected-file parser and command reporting with only activation/archive integrity stubbed; the actual repository command below independently covers those unstubbed checks. Cases include two review paths, byte preservation, mixed structural failure, missing/unknown markers, malformed existing content, rollback failure and an unknown diagnostic. Existing pending-activation, containment, historical and model tests remain in the full suite.

Commands: `python scripts/test-boundary-first-validation.py GrandfatheredReviewHandoffTests` (seven passed); `python scripts/test-boundary-first-validation.py -q` (85 passed); the exact four-spec command recorded above (exit zero, `status: review-required`, both paths explicitly reported, activation and rollback selection validated); `bash scripts/ci.sh --mode local` (preflight and all 16 selected checks passed); `git diff --check` (passed). Public dispatch, all canonical skill bodies, adapter identities, record-store schema/runtime, historical change records and plan allocation are unchanged by this correction. Their earlier proof is not retargeted to changed subjects. Required broader M4 walkthrough and adoption work remain outstanding.

Independent Code Review recorded ER-M4-003 before correction: PBF-R059 still assigned grandfathered classification to retired `spec-review`, contradicting the aligned PBF-R055a. This was a preventable same-slice reconciliation miss, not a new Design decision. The one-sentence correction explicitly routes current classification to PBF-R055a/Design Review and retains unrelated historical duties. Affected validation and independent rereview follow; disposition remains reviewer-owned. The successful CI run above preceded this wording correction and does not by itself prove the corrected text.

Final correction validation: a second `bash scripts/ci.sh --mode local` run after the PBF-R059 correction passed preflight and all 16 selected checks, including the boundary command/regression, model/schema, skills, adapter drift, lifecycle/guide/prose, metadata, selector, npm runtime and actual package-publication proof. `git diff --check` passed. The boundary command still explicitly reports the two Design Review obligations; CI success does not consume or replace their recorded independent classification. Final boundary-spec SHA-256: `a166b68a673d485c83a0b665446933c774406b03a4f464b205426ae9b8b315bb`. Runtime and test identities remain those in the first-pass correction review. This evidence update changes no tested behavior; its prose/whitespace checks are rerun separately before handoff.

## M4 packaged adoption candidate

The user explicitly requested completion of packaged CLI, adapter integration and activation proof. The candidate now exposes the existing four-command `record-store` family through the ordinary package entrypoint, with no fixture switch, extra configuration or semantic transition. This is an unpublished isolated-worktree candidate pending the required independent M4 and final whole-change reviews, not a release or a claim that an installed historical distribution changed. No existing change root is migrated or created in this repository. The advisory recording exception remains; refreshed CLI context still reports the initiative root absent.

### Exact adoption inventory

| Design allocation | Authored/aligned surfaces and disposition |
| --- | --- |
| WF-MAP-01/10 | `CONSTITUTION.md` and `AGENTS.md`: the scoped profile permits explicitly selected new records using the two models and recorder context. Permissions, independent judgment and historical remainder stay intact. No lifecycle state is placed in a plan. |
| WF-MAP-02/03/04/05/06 | `specs/rigorloop-workflow.md`, `specs/compact-current-state-change-record.md`: profile-specific entry paragraphs identify new selection and retained historical procedures. Explicit record representations remain the previously reviewed schema, not altered compact schemas. Existing findings, decisions and proof subjects are untouched. |
| WF-MAP-07, CLI-MAP-05 | `docs/architecture/system/architecture.md`: scoped entry names the contract-separated recorder, with no transition evaluator. Historical engine and unrelated architecture remain unchanged. The two model files retain their independently reviewed exact bytes; initial drafting prose is historical basis, not current adoption evidence. |
| WF-MAP-08/09 and skill support surface | `skills/architecture/SKILL.md`, `skills/spec/SKILL.md`, `skills/route/SKILL.md`, `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/design-review/SKILL.md`, `skills/plan/SKILL.md`, `skills/delivery-review/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`: explicit profile selection, executable recorder context/commands and no fallback to historical registration. `specs/skill-contract.md` preserves published quality and independent assessment. Existing conditional historical package/transition/output resources remain packaged for historical callers, explicitly not selected by the new profile. Shared reasoning references remain applicable for substantive duties; model-owned tables replace only feature serialization. No installed mirror is authored. |
| Remaining skills/resources | Unchanged: optional discovery, project orientation, learning, CI maintenance and PR do not own new-contract recording or select its lifecycle; their substantive scoped outputs remain consumed by the responsible actor. No automatic progression or new support-stage write authority is added. Existing `templates/compact/` records, feature/spec/architecture/ADR scaffolds and historical plan/proof resources remain historical assets; new recording uses the new package templates and model mapping instead. |
| CLI-MAP-01/02/03/04/06 | `packages/rigorloop/dist/bin/rigorloop.js`: public dispatch/help only; existing storage libraries, closed schema, safety and historical handlers remain unchanged. `templates/explicit-recording/records.json` supplies five record metadata examples; `scripts/build-record-store-schema.mjs` bundles it alongside the canonical schema into `packages/rigorloop/dist/templates/explicit-recording/records.json`. No automatic initialization/defaults; example Verify is never part of an initial request. `packages/rigorloop/README.md` owns usage, encoding, selectors, external-edit limit, adoption and rollback instructions. |
| CLI-MAP-07 and document/CI support | Prior metadata and model-validator integration remains. `scripts/validation_selection.py` adds exactly the two template paths to existing recording checks; `scripts/test-select-validation.py` proves canonical parity and retained package-publication selection. Other selectors and tracking preflight remain intact. No CI provider/permission/cache change or new validation command. |
| Supported adapter output | `dist/adapters/README.md` documents matching candidate guidance and rollback; `dist/adapters/manifest.yaml` is unchanged because adapters, roots and aliases are unchanged. Existing builders generate Codex, Claude and OpenCode archives. Only local-candidate `packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json` and its `releases.json` digest are refreshed; historical release entries remain byte-identical. No generated archive is tracked or published. |

### Activation and integration proof

The initial public-command regression failed at the disabled dispatcher before candidate dispatch was changed. The prior M1 disabled-entry assertion now proves that public recording still requires explicit selectors and supplies no default root. Existing TG-03 public text/JSON and TG-05 workflow tests now use the real binary. New template tests validate all five kinds and byte parity, pending/blocked examples and the absence of implicit initial sidecars. The installed-package smoke uses an actual npm tarball and installed executable, initializes all three generated adapters, then performs inspect/check/record, byte preservation, stale retry, a competing public writer, interrupted packed-dispatcher publication and public complete/restore recovery, write-stop/read-only preservation, historical/unknown-contract rejection and no-Git operation. It also reruns the actor workflow through the installed binary. Fault injection remains test-only through exported `main`; ordinary CLI has no fault flag or environment hook.

The first installation run correctly rejected stale adapter metadata after guidance changed. Existing archive/candidate generation regenerated the metadata; no assertion was weakened. A subsequent request fixture missed the required stdin final LF, was rejected, and was corrected to the approved encoding. Two template-routing regressions failed before selector amendment and now pass. Full isolated npm currently reports 516 tests, 514 passed and two existing skips; metadata reports 115 passed. Counts exclude unrelated compact tests left in the original worktree. Broader final results and the independent walkthrough are recorded below when complete.

The skill-creator generic `quick_validate.py skills/route` rejects the repository's existing `argument-hint` frontmatter extension. This is a tool/profile mismatch, not permission to strip the governed skill metadata. Repository-owned `validate-skills.py` and `test-skill-validator.py` remain the applicable normalized-contract checks. No new dependency or skill is introduced.

## Core result

### Current correction and validation checkpoint

The first full adoption CI run selected 18 checks: 17 passed, while `skills.regression` failed because route's Quick operating guide began at estimated token 885, beyond the existing 800-token limit. Skill-creator guidance led to moving that existing quick guide before the profiles and making its context instruction profile-aware; no threshold or substantive duty was weakened. The focused quick-guide regression now passes.

Independent first-pass Code Review recorded ER-M4-004 before correction: the executable's historical logging wrapper consumed recorder flags or replaced its rejected/exit-2 envelope with a logging error/exit 4. Seven actual-binary cases now cover historical flags with valid and unknown logging environment values, plus an otherwise valid recorder invocation with invalid historical logging environment. Four initial cases failed before correction; all seven now pass. The entrypoint sends raw first-token recorder calls directly to their own parser and renderer. Historical commands retain their logging wrapper; preprocessing cannot turn leading historical flags into an accepted recorder invocation. Installed-package tests additionally exercise otherwise-valid recorder requests with forbidden logging flags. CLI documentation states this namespace boundary. Storage, schemas and both Design model bytes are unchanged.

Commands at this checkpoint:

- `node --test --test-name-pattern ER-M4-004 packages/rigorloop/test/record-store-cli.test.js`: seven passed after correction.
- `python scripts/test-skill-validator.py SkillValidatorFixtureTests.test_progressive_loading_canonical_skills_satisfy_quick_guide_contract`: one passed after correction.
- Existing `build_adapter_archives` and `_prepare_local_cli_release_candidate` generation: all three adapter archives and matching local CLI candidate regenerated. Only the current candidate metadata and index digest were refreshed; historical entries are retained.
- `bash scripts/ci.sh --mode local`: correction rerun passed all 18 selected checks, including real package publication, npm tests, selected adapter regressions, canonical/generated drift, metadata compatibility, skill quick-guide checks and retained historical validation. This supersedes the prior failed candidate run without erasing it.
- `python scripts/build-adapters.py --check` and `git diff --check`: passed for the corrected candidate.
- Full `python scripts/test-adapter-distribution.py`: 157 passed in 470.036 seconds. Adapter/guidance subjects were unchanged throughout; the later text-only runtime correction has separate fresh installed-package and full CI proof. Selected adapter cases are not represented as this complete suite.

Current entrypoint SHA-256: `0e468cf3bbb9c030a8825015d3bc2d3b05e627f291f31f8cbd9147c43b52272b`; route guidance: `298ad4ec122811f3e3b6d759154eb5172a88910c4b47d3ec6dd7703bfe3150fe`; regenerated candidate metadata: `1c27e0767d018af9e15f0b5c0a16a55b4d542510b22ee82b8ada1afa131310c6`. Candidate archives are untracked temporary proof, not published releases.

The whole-chain review then recorded ER-M4-005 against the existing M2 text renderer: available record identities were present in JSON but absent from human-readable results, contrary to CLI-SR-11. A public text regression first needed its fixture's required applicability entry corrected, then reproduced the missing revision line before the implementation changed. The two-line renderer correction prints the existing revision and file identities, using `unavailable`/`absent` for null values. No schema, JSON result, snapshot boundary or semantic behavior changes. The regression passes for a successful save and a missing registered record. Installed-package smoke also compares text with JSON identities across all three adapters.

- `node --test --test-name-pattern ER-M4-005 packages/rigorloop/test/record-store-cli.test.js`: one passed after reproducing and correcting the missing text identity.
- `npm --prefix packages/rigorloop test`: final standalone renderer run passed 522 of 524 tests, with two existing skips and zero failures. The earlier ER-M4-004 run passed 521 of 523; the added text regression accounts for the increase.
- `python scripts/test-change-metadata-validator.py`: 115 passed on the corrected candidate.
- `bash scripts/ci.sh --mode local`: final renderer rerun passed all 18 selected checks, including package tests and actual installed-package smoke with text identity assertions. Prior ER-M4-004 candidate also passed all 18 checks.

Final renderer SHA-256: `5d27c3f20f57f770140c705fdad46c2286bb709ee158d4d5296cdb2d77a2a5cc`. The matching package candidate was rebuilt from the same generated adapter archives; their identities and guidance did not change. Independent walkthrough proof is refreshed against that package before reliance.

### Independent packaged semantic and rollback walkthrough

The independent forward-test used temporary fixture `/tmp/rigorloop-m4-forward-1XZEeL/project`. Actual model author `/root/m3_walkthrough/fixture_author` and actual reviewer/Verify actor `/root/m3_walkthrough` were separate participants. The reviewer authored neither the model nor its corrections. Published route, Design Review and Verify guidance was read from generated packages, not inferred from actor labels in a unit test.

Verify recorded `verify-ttl-zero` with failed evidence. Route explicitly reopened completed design work; the separate author corrected TTL behavior. Independent review then found two model-format errors, recorded `model-format`, and required another author correction. The reviewer independently disposed that finding and the specific Verify defect after correction. The retained synthetic self-author approval and its open finding stayed byte-identical. Overall fixture Design assessment correctly remains `inconclusive`: missing upstream approval, delivery/runtime proof and retained finding disposition prevent completion. No `verify-report.md` was created. This is genuine correction/rereview and withheld-completion evidence, not a fabricated successful lifecycle. The automated packed actor scenario supplies the separate positive explicit-completion path.

Fixture identities: corrected model `sha256:1802508e0a109eb010f36bb62021bd02efd562568206acfa9ef42321066b353f`; proposal `sha256:e1a57e43f088fca1e729ed1e02576583744d5468e0c47c65d0134ec07da44042`; retained review `sha256:d7be432f11481d94a4465ff8c726b96c90bdee6f98989dac6d222c46f92d0cde`; final record revision `sha256:77c9f870d8efa0273dd1db242244179da819ea30c25bae3502fa62d35f78e6c5`. These are proof-fixture subjects, not repository lifecycle approvals.

The independent participant ran:

```sh
npm pack --offline --ignore-scripts --pack-destination /tmp/rigorloop-m4-forward-1XZEeL/renderer-package
npm install --prefix /tmp/rigorloop-m4-forward-1XZEeL/renderer-installed --offline --ignore-scripts --no-audit --no-fund /tmp/rigorloop-m4-forward-1XZEeL/renderer-package/xiongxianfei-rigorloop-0.5.1.tgz
node /tmp/rigorloop-m4-forward-1XZEeL/text-json.mjs
node /tmp/rigorloop-m4-forward-1XZEeL/rollback-final.mjs
```

Pack ran in `/tmp/rigorloop-clean-install-cli-91_ydf17`; the executable was the installed `renderer-installed/node_modules/.bin/rigorloop`. The final tarball SHA-256 was `6804b200767203599fcd40facab320cdfe4a93a3a6ff719a70891261c3769e70`. Installed entrypoint, renderer, metadata and both governing model identities matched those recorded above. Actual public `inspect`, `check` and `record`, with explicit root/change/stdin selectors and both formats, returned `inspected`, `valid` and `unchanged`, exit zero. Both formats exposed the same revision and all four available path/hash identities, observations and storage-only claim, without changing semantic evidence or creating completion.

All three generated adapter skill bodies agreed byte-for-byte after their expected frontmatter differences, and documented public commands worked from each target. Codex route/Design Review/Verify full-file hashes were `298ad4ec122811f3e3b6d759154eb5172a88910c4b47d3ec6dd7703bfe3150fe`, `4d5805df40fcd54d711899fa88e20f0a25d073b796b3f707b277c09fa105d602`, `661bb3314b3f24cbb99f1179e593d8b21bd42eb80ddb127a9c655fe6f9a57f27`. Corresponding Claude/OpenCode hashes were `6dfafbbfd53387c5be0c89325dc43fcd6689f48a2e1c4409db234123786b51fb`, `d3f4c1d5d7f4c8347b4679adf0e8d3e90ff116ec9b8c0aaf59f960d0d7f7e631`, `3b08ff01357b2708c47cc2697c2fd0193c9f68c4daa99151dd67e0b14dda2eee`.

For pre-first-write rollback, three fresh `renderer-rollback-{codex,claude,opencode}` fixture roots first used the final distribution and matching guidance; inspection reported `absent-change`. The participant then physically switched both distribution and guidance to the matched prior prospective pair. The prior CLI rejected unknown `record-store` with exit 4. Neither phase created `docs/changes` or `.rigorloop`; no record/recover command was used in these roots. This proves distribution/guidance rollback, separately from transaction restore. Prior entrypoint SHA-256 was `0ed7599eb24ed50d238dfbf17a25218584c437444119d1ab078d7d4d44ab17ef`; prior Codex/Claude/OpenCode archive hashes were respectively `b173a9abbe8cb709a6aace7d0acca1164fc12bd628e21b3f9acbb55034129ed0`, `4f425c17bb74270bf1451d30da109c6c8801b67008f6b90604b930dc577d29ea`, `eb54bc06a52d2c8a2f986f70d2afda542bb08e566d7af0eec92d542b289efdfb`.

After writes, the installed-package suite separately proves write-stop/compatible inspection preserves records; reverting to an incompatible writer is not approved. Native Claude/OpenCode sessions, hosted CI and release publication were not performed or inferred. Transaction interruption/competition/recovery comes from the installed-package suite, not the semantic participant's claim. This walkthrough expires on changes to its executable or governing guidance subjects.

- Skill: implement
- Status: implemented
- Completed scope: M4 packaged CLI, adapter integration and activation proof, including independent slice and distinct final whole-change reviews
- Artifacts changed: the adoption inventory above, including the public entrypoint, guidance, package examples, integration proof and candidate metadata
- Tests added or updated: prerequisite, public entrypoint, templates, installed-package integration and selector regressions described above
- Validation performed: commands and results above
- Validation result: both focused corrections, final renderer CI (18 checks), complete adapter suite (157 tests), metadata (115 tests) and refreshed independent activation walkthrough pass
- Open blockers: no remaining M4 technical finding; M5 Verify requires separate user authorization under the approved plan
- Next stage: separately authorized M5 Verify
- Claim limitations: isolated M4 completion and local candidate activation proof only; no successful Verify, formal lifecycle settlement, public activation, commit, push or release

### M4 handoff closeout

The independent [M4 review](../reviews/explicit-recording-m4-code-review.md) records ER-M4-004/005 resolved, retaining all earlier finding dispositions, and a clean-with-notes M4 slice result. Its separately labeled final whole-change M1–M4 Code Review also records clean-with-notes against the complete implementation and cross-milestone basis. No technical finding remains open. The retained notes are the approved non-cooperating external-edit limit, storage-only/actor-provenance boundary, and absence of release/native-tool/final-Verify claims. This handoff wording follows those judgments and adds no new behavioral proof. The original worktree is preserved; M5, integration/commit and publication are not inferred from M4 completion.
