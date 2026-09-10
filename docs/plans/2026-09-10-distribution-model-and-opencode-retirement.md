# Distribution, Explicit Force Installation and OpenCode Retirement

## Purpose / big picture

Deliver one Distribution contract for Codex and Claude Code. Installation verifies the archive, checks all candidate destination units, stops on any default conflict and uses explicit `--force` for complete replacement. It preserves unrelated content and does not inspect or write project state. Retire the mirror producer and the exactly mapped old documents after their surviving responsibilities and protection have usable replacements.

## Current Handoff Summary

- Owning change record: [Distribution change](../changes/2026-09-10-distribution-model-and-opencode-retirement/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Selected direction](../proposals/2026-09-10-distribution-model-and-opencode-retirement.md); assessment basis: [Proposal Review r3](../changes/2026-09-10-distribution-model-and-opencode-retirement/reviews/proposal-review-r3.json).
- Spec: [Distribution](../design/distribution/distribution.md), DIST-SR-01–20 and its eight scenario dimensions. [Design Review r5](../changes/2026-09-10-distribution-model-and-opencode-retirement/reviews/design-review-r5.json) owns the exact ten-member package assessment.
- Architecture: Distribution's Building Block, Runtime, Partial failure and retry, and displacement views; reciprocal [System](../design/system/system.md), [Skill](../design/skill/skill.md), [Design](../design/design/design.md) and [Release](../design/release/release.md) amendments. Their original responsibilities remain bounded by the package map.
- Retained legacy members: `specs/single-authored-skill-source-generated-output.md`, `specs/multi-agent-adapters-first-public-release.md`, `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`, `specs/rigorloop-cli-package-and-codex-init.md`, and `specs/published-skill-first-repository-simplification.md`, with exactly their reviewed prospective notices and unmigrated remainders.
- Prior-contract test spec: none independently governs a retired state-writing, OpenCode-success or mirror-production path. The five selected test specs retain protective intent only through Distribution's explicit preservation/supersession map. Other release, recording and measurement proof remains with its current owner.
- Governance: `CONSTITUTION.md`, `AGENTS.md`, Test's shared criteria and Review and Closeout's independent assessment policy. Do not treat model/package availability as customer adoption or publication authority.

## Context and orientation

Canonical content is under `skills/`; Python adapter generation uses `scripts/adapter_distribution.py` and `scripts/adapter_templates/`. `dist/adapters/manifest.yaml` and its README are tracked support surfaces. The Node CLI implementation is tracked directly under `packages/rigorloop/dist/`; packaging that directory does not make it generated source. The installer and state handling are concentrated in `dist/bin/rigorloop.js`, descriptors in `dist/lib/adapters.js`, hashes/state readers in `dist/lib/lockfile.js`, and the prior filesystem helper in `dist/lib/managed-authoring-replacement.js`.

The existing managed helper establishes only single-parent anchoring and related preservation primitives. Force installation needs the reviewed two-parent move into retention outside skill discovery. M1 must prove that capability and its rejection boundary before public dispatch depends on it. Do not replace this proof with a mocked successful rename or infer it from the old helper's tests.

Release preparation, execution, metadata validation and public-smoke fixtures contain current three-target assumptions. Reconcile those in one M2 composition slice; never globally shrink historical evidence lists. No-map rationale: the project map predates these model adoptions, so this plan uses the reviewed owner map and direct named code/test/selector inspection. The unrelated `docs/design.zip` and installed runtime directories are outside this change.

## Non-goals

- No publication, npm version selection, remote configuration, PR, merge or actual customer installation. Local temporary fixture projects and isolated package installation supply implementation proof.
- No project-state schema, reader, admission marker, managed upgrade, automatic recovery scanner or whole-project rollback. No blanket deletion of historical records, reports, fixtures or mixed-source remainders.
- No new platform, proxy dispatcher, general filesystem framework, inventory-wide skill procedure changes or cleanup of this repository's installed skills.

## Requirements covered

| Governing requirements | Allocated milestone | Verification groups |
| --- | --- | --- |
| Retained published-skill-first R14–20/R22; T1/T14 admission, T13 retirement comparison, T10/T13 measurements | M1–M3 | TG-08, TG-05/06, TG-FINAL-02; E1–E3 |
| DIST-SR-01 | M2, M4 | TG-04, TG-07, TG-FINAL-02 |
| DIST-SR-02 | M2 | TG-03, TG-04 |
| DIST-SR-03, DIST-SR-04 | M2, M3 | TG-04, TG-05, TG-FINAL-01 |
| DIST-SR-05 | M3 | TG-05, TG-06 |
| DIST-SR-06, DIST-SR-07 | M2 | TG-03, TG-04, TG-FINAL-01 |
| DIST-SR-08, DIST-SR-09 | M1, M2 | TG-01, TG-02, TG-03 |
| DIST-SR-10, DIST-SR-11, DIST-SR-12 | M2 | TG-03, TG-FINAL-01 |
| DIST-SR-13, DIST-SR-14 | M1, M2 | TG-01, TG-02, TG-03 |
| DIST-SR-15, DIST-SR-16 | M2 | TG-03 |
| DIST-SR-17, DIST-SR-18 | M2, M3 | TG-04, TG-FINAL-01 |
| DIST-SR-19 | M3, M4 | TG-05, TG-06, TG-07, TG-FINAL-02 |
| DIST-SR-20 | M2, M4 | TG-04, TG-07, TG-FINAL-02 |
| System SYS-SR-02/04–09; Design DES-SR-13/15/17/21; Skill content/resource invariants; Release REL-SR-02/03/08/09/13/19/21–24 as amended | M2, M3, M4 | TG-04, TG-05, TG-07, TG-FINAL-01/02 |

## Milestones

### M1. Prove bounded destination replacement primitives

- Milestone kind: implementation.
- Engineering purpose: establish the new filesystem capability behind an internal boundary before public force installation can remove or move existing skills.
- Requirements: DIST-SR-08/09/13/14; Partial failure and retry; resolved review findings `dist-force-mutation-basis` and `dist-retained-original-discovery`.
- Architecture responsibility: candidate-unit snapshots, anchored parents, outside-discovery detachment, no-clobber publication and preservation.
- Dependencies: exact reviewed Design and Delivery Review of this plan; current CLI behavior stays unchanged in this slice.
- Implementation scope: extract/reuse only necessary low-level primitives, implement two-parent anchored same-filesystem relocation and safe capability rejection, preserve detached originals outside all supported/configured discovery roots, and report bounded per-unit effects. Do not introduce a state/recovery schema or wire public flags yet.
- Files/components likely touched: `packages/rigorloop/dist/lib/managed-authoring-replacement.js`, a narrowly scoped replacement helper if separation is necessary, and Node filesystem tests such as `packages/rigorloop/test/installer-replacement.test.js`. Preserve old consumers until M2 removes their capability.
- Required verification: TG-01 — real successful single-directory/file replacement, complete candidate bytes, old-extra-file removal from the active unit, unrelated-unit preservation and retained originals outside discovery; TG-02 — source/ancestor change, destination appearance after detach, open writer on old inode, cross-filesystem or unavailable anchored move, unsafe/inaccessible/symlink paths, interrupted/partial publication and explicit retry behavior.
- Evidence expectations: actual temporary filesystem objects and independently expected bytes/counts; deterministic barriers at inspected/detached/published points where needed, not timing sleeps. Demonstrate a real supported two-parent move and unavailable-capability rejection before detachment. A test double may inject a failure but must not stand in for the successful filesystem primitive.
- Implementation steps: first encode the critical success/rejection/failure contracts; establish capability/placement before any detach; implement the minimal helper; run direct tests and inspect open-handle preservation. If a supported success path cannot be implemented within the reviewed constraints, stop and return to Design; do not silently ship force that only rejects or broaden dependencies.
- Validation commands: C1 and C2 below. C2 protects existing consumers while extraction is shared; replace only tests whose capability is retired later.
- Expected observable result: safe replacement works in the real fixture environment, while unsupported capability or placement leaves every original unit in place. No runtime-discoverable backup is created at any checkpoint.
- Completion criteria: TG-08/E1 admission evidence covers affected new or retained checks; TG-01/02 evidence and independent Code Review establish the helper's actual mutation and failure boundaries.
- Required evidence: command results, fixture capability/filesystem facts, observed original/candidate/retained bytes, exact code/test subjects and partial-effect diagnostics.
- Review handoff: independent M1 Code Review of helper realization, proof and effects on still-active managed consumers.
- Risks: two-parent anchoring is new; blindly reusing pathname-based rename or treating hidden names as undiscoverable would violate the contract.
- Rollback/recovery: revert only the isolated helper/extraction slice on its exact baseline; preserve temporary evidence when a failure needs diagnosis. Do not clean user installations or reinterpret actual state.

### M2. Integrate conflict installation and the two-target delivery path

- Milestone kind: implementation.
- Engineering purpose: change the public installer, package producers and release consumers coherently so no current surface retains hidden OpenCode or state-managed success.
- Requirements: DIST-SR-01–04/06–18/20, with the shared-owner requirements in the coverage table.
- Architecture responsibility: Distribution dispatch/acquisition/installation and Release's population/identity/publication separation.
- Dependencies: clean M1 review; supported replacement capability demonstrated. Keep old source documents readable until M4.
- Implementation scope: add `--force`; preflight all verified candidate units; reject any default existing directory/file, including identical or empty units; force complete replacement only within candidate scope; ignore project state. Remove `--write-state`, state parsing/marker guards, managed authoring/workflow replacement and exclusive dead helpers. Limit current producer/installer/profile/smoke support to Codex/Claude, remove current OpenCode template/aliases, and retain independently needed historical readers. Update user guidance and package metadata together.
- Files/components likely touched: Node CLI/descriptors/helper callers/tests; `scripts/adapter_distribution.py`, adapter templates, `build-adapters.py`, `validate-adapters.py`; `dist/adapters/manifest.yaml` and README; package/root READMEs; release candidate/execution/transaction/validation/provider modules and schema/profile fixtures; current `.github/workflows/` consumers when affected.
- Required verification: TG-03 — both acquisition routes, actual dispatch, complete conflict set after verification, no writes to any unit on default preflight failure, force removal of obsolete files, preserved unrelated skill parents/state, malformed/unreadable/symlink state being irrelevant, dry-run limits, removed flags/targets, archive trust/path/hash/count failures and safe proxy diagnostics; TG-04 — real generated two-target archives, bundled metadata/index and an actual packed CLI agree, while historical three-target observations remain historical and materially changed candidates cannot reuse approval.
- Evidence expectations: use actual archives and packed executable; independently inspect installed and retained bytes. Exercise representative default/force behavior on both targets and route parity through network-fixture and local-archive acquisition. Observe acquisition not being skipped for ordinary conflict reporting, and no acquisition on invalid target/removed flag. No mock may turn a bad archive or validator into success.
- Implementation steps: update focused public tests first; wire proven helper; remove withdrawn state branches after caller analysis; reconcile current generation/support/profile domains and all closed-set unknown-value errors; update help and examples; adapt current release-smoke tests and keep historical source-bound checks explicitly separated.
- Validation commands: C2, C3, C4 and C8. C4 exercises the real prepared-candidate/release-verifier path in isolated fixture repositories without publication; dry-run release verification is not sufficient.
- Expected observable result: both targets follow the new conflict/force contract using actual packaged bytes; OpenCode and state-writing syntax fail early; old project state neither blocks nor authorizes installation.
- Completion criteria: TG-08/E1 covers affected checks and E2 precedes any check removal in this slice; all current target lists and installer interfaces agree, TG-03/04 pass, required old guards remain, and independent Code Review assesses the integrated support withdrawal.
- Required evidence: actual commands, package/archive identities, per-target conflict/replacement/retention results, removed-helper caller dispositions and historical/current profile distinction.
- Review handoff: independent M2 Code Review of complete producer-to-packed-installer and release-consumer interactions.
- Risks: broad search-and-replace can rewrite historical facts; state cleanup may delete shared hashing; helper success alone may hide packed metadata mismatch.
- Rollback/recovery: revert the complete coupled public-support slice to its preceding coherent baseline if integration fails; do not partially restore only a target list. Fixture failures retain detached originals as specified. No published version is rewritten.

### M3. Retire the standalone mirror and reconcile validation callers

- Milestone kind: implementation.
- Engineering purpose: remove duplicate production only after retained current package paths and replacement protection exist.
- Requirements: DIST-SR-03–05/17–19; retained published-skill-first R14–20/R22; Skill's resource completeness and raw-byte preservation.
- Architecture responsibility: canonical-to-adapter production, retained resource validation and actual CI/selector execution.
- Dependencies: clean M2 review; working two-target package pipeline.
- Implementation scope: transfer useful mirror-test protection into retained adapter/skill tests, then delete `scripts/build-skills.py` and `scripts/test-build-skills.py` without wrappers. Remove exclusive `skills.generation_regression`/`skills.drift` commands and all actual callers. Keep active runtime directories untouched.
- Files/components likely touched: retained adapter/skill tests; `scripts/validation_selection.py`, selector/cache tests, `scripts/ci.sh`, `scripts/release-verify.sh`, `scripts/validate-release.py`, README/contributor guidance and any actual scoped caller found during the audit.
- Required verification: TG-05 — independent complete inventory/raw-byte oracle, missing and stale mapped resources, structurally malformed generated skills and no generation into active/canonical roots; TG-06 — correct selected checks for changed canonical, package and deleted-script paths, no invocation of deleted scripts, retained full release verifier and useful independent builder/validator operations.
- Evidence expectations: record how the seven old mirror cases divide into capability-specific retirement versus retained detection. Demonstrate retained tests reject representative missing/stale/malformed candidates using real production paths before deleting their old protection. Do not use passing suite counts as equivalence evidence.
- Implementation steps: audit current executable consumers; transfer required protection first; remove mirror producer/test and exclusive selector entries; reconcile command-manifest/cache tests and guidance; execute retained suites and verify deleted-path selection.
- Validation commands: C3, C5, C6, C7 and C8, plus TG-08/E1–E3 below. Historical recorded-source tests may invoke the original scripts only in their original source context, never through a current wrapper.
- Expected observable result: builds/checks create packages in temporary or explicit safe output, never `.codex/skills` or another active installation, and CI keeps necessary resource/package protection without stale commands.
- Completion criteria: TG-08/E1–E3 admission, representative old/replacement comparison and measurements are recorded before retirement closes; useful protection is demonstrated on retained producers, exclusive callers are removed and independent Code Review accepts the maintenance rationale.
- Required evidence: caller audit, before/after negative-case detection, commands and affected selector outputs.
- Review handoff: independent M3 Code Review covering script removal and test/selector composition, not just deleted files.
- Risks: deleting mirror checks can remove the only independent resource oracle; old check IDs may survive in caches or command expectations.
- Rollback/recovery: restore the complete producer/check/selector slice if a required detector or consumer is lost; do not regenerate active runtime copies as recovery.

### M4. Retire mapped source documents and complete owner navigation

- Milestone kind: implementation.
- Engineering purpose: remove obsolete authority only after its replacement behavior and protection are implemented and reviewed.
- Requirements: DIST-SR-01/19/20, Design DES-SR-13/21 and System composition/adoption relationships.
- Architecture responsibility: Distribution's exact source/consumer displacement map and historical identity preservation.
- Dependencies: clean M1–M3 reviews; no unresolved consumer requiring the original live source.
- Implementation scope: delete exactly the five selected `.md`/`.test.md` pairs and five ADRs in Distribution's map; replace only its named mixed-architecture sections and current navigation/consumer links. Preserve historical reviews, plans, release evidence, mixed-source operational remainders and their IDs. Reconcile governance/README/install guidance and FU-013's selected responsibility without claiming successful Verify prematurely.
- Files/components likely touched: the fifteen mapped source files; `docs/architecture/system/architecture.md`; five retained source notices; current links in affected owner models, docs indexes, `AGENTS.md`, `CONSTITUTION.md`, `docs/follow-ups.md` and operational validators/readers named by the consumer audit. No additional deletion is inferred from a grep match.
- Required verification: TG-07 — every displaced obligation/decision has a current destination or explicit supersession, no live consumer needs a removed file, supported guidance matches executable behavior, historical bytes/identities remain intact, and new-profile legacy classification is preserved.
- Evidence expectations: distinguish current executable/navigation references from literal historical subject IDs. Check both Markdown targets and actual reader behavior; merely replacing links does not prove a validator no longer opens deleted sources. Preserve the earlier legacy prose limitation separately from introduced findings.
- Implementation steps: audit current readers against the exact map; replace current references; remove selected documents after meaning is accessible; reconcile conditional adoption language and navigation; run documentation and actual selected consumer checks. Unexpected required source scope returns to Design rather than expanding the deletion set silently.
- Validation commands: C7, C8, C9 and C10, with the complete intended changed-file set supplied to C8. Apply relevant reader tests discovered by the audit through the repository selector.
- Expected observable result: contributors can use one current Distribution model without reconstructing deleted sources, while historical judgments still refer to their original subjects.
- Completion criteria: exact deletion map and real consumers reconcile; independent M4 Code Review accepts source retention and adoption dependencies. Only distinct final Verify establishes final closeout.
- Required evidence: exact removed paths, retained-source classification, link/reader checks, command results, historical preservation and scoped ownership updates.
- Review handoff: independent M4 Code Review, followed by the fresh whole-change checkpoint below after all corrections.
- Risks: a historical directory may contain a live baseline; apparent documentation-only links may be validator inputs. Existing full-file legacy prose errors must not be mislabeled fixed or silently waived.
- Rollback/recovery: restore a removed source together with affected readers if necessary until a reviewed replacement exists. Do not reconstruct or rewrite original assessment records; keep correction ownership explicit.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all four implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-milestone interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment and concern dispositions.
- Successor: distinct final Verify; corrections return to their owner and require affected reassessment.

This checkpoint applies the selected review policy. Milestone approval or a verification-group non-applicability rationale does not waive it.

## TG-08. Retained check admission and retirement evidence

The retained published-skill-first R14–20/R22 obligations apply to checks added, changed, retained as replacement protection or removed by this initiative. The separate Test/Workflow exceptions do not waive this slice. Keep this evidence in the existing change-local implementation evidence surface; no new validator, per-test ledger system or repository-wide inventory rewrite is required. Unknown fixture behavior pauses the affected retirement.

- E1 — M1 and M2 record admission when adding or changing checks; M3 completes the affected retirement ledger. For each affected script/check, name its concrete protected failure and contract, why deterministic automation is appropriate, why an existing gate cannot own it more simply, execution trigger, reported repair and evidence permitting later retirement. Reuse an existing entry only with an explicit current-applicability basis. Map retained protection to the existing gate owner; preserve the zero-new-standalone-validator/selector/cache budget. Independent milestone review inspects these fields against actual commands and fixtures.
- E2 — Before each affected check is deleted, run its old proof and the replacement proof over representative fixtures for still-contractual accepted/rejected behavior. For M3, run `python3 scripts/test-build-skills.py` from an isolated copy of the exact pre-removal source and C3/C5 over the replacement source; include representative missing/stale/malformed resource fixtures in both applicable paths. Record exact source/fixture identities, expanded commands, results, protected-failure coverage differences, each retained/replaced/explicitly de-contracted disposition and a recoverable source rollback boundary. M2 applies the same procedure with C2/C3 to affected retired checks. Do not require successful old-state/OpenCode/mirror-only semantics in the replacement; cite the approved supersession for those differences. Isolated old-source execution must not write this repository's installed skills. Passing whole suites alone is insufficient comparison.
- E3 — Capture actual before/after command count and elapsed runtime for the affected command population using the same documented fixture/environment scope; record expanded commands, timing method, run count and limitations. Record changed-line totals using `git diff --numstat <recorded-baseline> -- <scoped-paths>` plus explicit counts for new untracked files when applicable, and record the before/after maintenance owner of each affected check. M1 captures its baseline before changes; M2/M3 extend the same evidence for their slices, and M3 records the combined simplification result. There is no savings threshold and these measurements never replace protected-failure proof. Final Verify reconciles the delivered scope and discloses any non-comparable measurements.

These are implementation-owned execution and manual-inspection procedures, not additional automated subsystems. E1/E2 close with the milestone that changes the check; E3 completes with M3 and is checked against final subjects in TG-FINAL-02. Required evidence unavailable at its checkpoint prevents that retirement from being called complete.

## Change-level verification

### TG-FINAL-01. Complete delivery and replacement path

- Covers: M1–M3; DIST-SR-02–18; all eight scenario dimensions where installer/package composition matters.
- Demonstrate: current canonical resources produce exactly two verified packages consumed by the packed CLI; default complete conflict preflight and explicit whole-skill replacement work; retained originals never enter runtime discovery; state stays untouched; removed syntax/targets and unsafe destinations reject through real public dispatch. Required proof still runs after mirror/check retirement.
- Evidence expectations: C3/C4 exercise actual archive/metadata/packed paths and release verifier; C2/C6/C8 establish integrated runtime and selector coverage. Reuse milestone evidence only with explicit unchanged-surface/identity rationale; repeat when later consumer changes defeat its scope. Do not substitute fixtures for the validator or claim actual public release success.
- Non-applicability: none; helper or milestone-local success cannot prove this composition.

### TG-FINAL-02. Source retirement, authority and historical preservation

- Covers: M2–M4; DIST-SR-01/17/19/20, reciprocal owner relationships and all exact removal/consumer maps.
- Demonstrate: current code/help/metadata/docs/tests agree, deleted source/script paths have no live dependency, retained historical evidence keeps its meaning, and successful implementation does not itself authorize publication or customer adoption.
- Evidence expectations: C7–C10, TG-08/E1–E3 retained admission/retirement evidence and measurements, source/reader audit and exact final whole-change review. Verify assesses actual chain completeness and the disclosed legacy prose baseline; new or contradictory errors require owner correction.
- Non-applicability: none; the retirement spans code, documentation, selectors and release consumers.

## Validation plan

Run commands from repository root. These are future implementation checks, not claimed executions from plan authorship. C1 names the proposed focused test file; implementation may select an equivalent retained runner with recorded mapping, without changing proof scope.

| ID | Command | Purpose and timing |
| --- | --- | --- |
| C1 | `node --test packages/rigorloop/test/installer-replacement.test.js` | M1 direct actual-filesystem capability, conflict/race and retention tests; retain through final integration. |
| C2 | `npm test --prefix packages/rigorloop` | M1 shared-consumer regression, M2 public CLI/packaging/recording non-regression, and final affected runtime proof. |
| C3 | `python3 scripts/test-adapter-distribution.py` | M2/M3 real packages, current support, historical metadata and archive/resource checks. |
| C4 | `python3 scripts/test-release-transaction.py` | M2/final candidate, executor, profile and packed-install composition. The real candidate fixture invokes `bash scripts/release-verify.sh <fixture-tag> --prepared-candidate <fixture-output>`; record its actual expanded command/result. No public publish or dry-run substitute. |
| C5 | `python3 scripts/test-skill-validator.py` and `python3 scripts/validate-skills.py` | M3 canonical/common-resource contract and replacement negative proof. |
| C6 | `python3 scripts/test-select-validation.py` and `python3 scripts/test-validation-cache.py` | M3 deleted-path selection, command inventory and cache/selector consistency. |
| C7 | `python3 scripts/test-boundary-first-validation.py` and `python3 scripts/test-artifact-lifecycle-validator.py` | M4 current model/source-owner recognition, source-retirement consumers and lifecycle handling. |
| C8 | `bash scripts/ci.sh --mode explicit --path <intended-changed-path> ...` | Execute actual repository-selected checks for every intended changed/deleted path. Implementation records the full expanded path list, including code/tests/owners/governance and selected deleted files, excluding unrelated user changes. No PR/base SHA or publication is invented for an uncommitted branch. |
| C9 | `python3 scripts/validate-boundary-first.py --check --path <affected-model-or-source> ...` and `python3 scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <affected-artifact> ...` | Exact affected Distribution/System/Design/Skill/Release members, retained sources, plan and current amended artifacts. Exit-zero grandfathered observations still require independent classification. |
| C10 | `python3 scripts/validate-documentation-prose.py --mode enforce --path <new-or-revised-model-or-plan> ...` and `git diff --check` | Current model/plan prose and whitespace. Audit retained historical sources with the same validator in `audit` mode and compare findings to their original identities; baseline findings are not a full-file pass. Any required selected enforcement failure remains visible to Verify and must be corrected or dispositioned by its owner. |

Use exact current identities and realistic fixture outcomes in evidence. State-marker/schema tests are not a replacement for destination-conflict/force proof. Positive old OpenCode, state-writer, managed-upgrade and mirror-only tests retire only under their explicit Design supersession; shared hash, trust, containment, resource and historical-evidence checks remain. New closed vocabularies need explicit unknown-value regression tests before consistency checks. Do not require all agent runtimes or actual public installation for ordinary contributor proof; safe retention placement is established outside their declared discovery roots and includes an unknown-placement rejection case.

## Risks and recovery

Force can remove local edits from active destinations, leaves originals for explicit cleanup, and cannot promise filesystem-wide atomicity. M1 proves actual primitives and limits; M2 keeps the warning and exact affected paths visible. Retained paths never grant state repair or automatic retry authority.

Current/historical target populations and source identities must remain distinct. Roll back a failed coupled source/consumer slice, not one target list, and never rewrite published bytes or old judgments. Failed proof stops milestone completion and routes to the responsible owner.

The five retained specs have known full-file prose debt. Preserve actual findings and compare against the prior basis rather than reformatting unrelated historical examples. Delivery and final Verify must assess required-check applicability; this plan grants no blanket waiver and does not call a failed command successful.

## Dependencies

- Exact approved proposal/Design package and Delivery Review precede implementation; the change record owns applicability.
- M1 → M2 → M3 → M4, with independent Code Review after each and owned corrections before downstream reliance.
- Final whole-change Code Review precedes distinct Verify. Route/Verify establish final adoption and FU-013 disposition only with the required evidence; no other follow-up is closed by inference.
- Any newly discovered semantic gap returns to Design. Any additional required source deletion returns to the selected scope owner before removal.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-10 | Prove force relocation before wiring public installation. | Two-parent anchoring and outside-discovery preservation are new material capabilities. | Relying on the prior single-parent helper or deferring platform failure proof until final integration. |
| 2026-09-10 | Reconcile current two-target producer/installer/release consumers together in M2. | A partial support withdrawal can leave hidden current OpenCode paths or false metadata. | Separate incompatible target-list changes presented as independently complete. |
| 2026-09-10 | Transfer mirror-test protection before script deletion; retire documents last. | Necessary behavior and evidence must exist before their former owner disappears. | Deleting by age/name or treating smaller suite/file counts as proof. |

## Readiness

- See the owning change record for current workflow state.
- Remaining completion gates: Delivery Review, four implementation/Code Review slices with required corrections, fresh final whole-change Code Review and distinct successful Verify. This plan does not authorize publication or claim implementation completion.
