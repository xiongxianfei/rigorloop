# Retire specs and stale tests: implementation plan

## Purpose / big picture

Remove the entire repository specs tree and all stale test/fixture material identified by a complete population audit, while keeping important current contracts in the existing Design hierarchy and preserving meaningful protection. One owning change covers every family and dependent consumer.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-14-retire-specs-and-stale-tests/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing and closeout readiness live only in this record.

## Source artifacts

- Proposal: [complete retirement](../proposals/2026-09-14-retire-specs-and-stale-tests.md).
- Spec: the [System Design](../design/system.md) and affected current Skill, Workflow, Design, Assessment, CLI, Engineering, Validation, Packaging and Release models; unchanged Records and Installation remain applicable owners. Exact reviewed subjects live in the owning change.
- Architecture: embedded in the same models, especially their approved resource/input, diagnostic and candidate boundaries.
- Prior-contract test spec: none as an independent future proof owner after adopted retirement; all 54 remaining test specifications are reconciled source inputs under the [source disposition](../changes/2026-09-14-retire-specs-and-stale-tests/source-disposition.md), including still-applicable unique acceptance intent.
- Exact source baseline: [source-inventory.tsv](../changes/2026-09-14-retire-specs-and-stale-tests/source-inventory.tsv), commit `7ad33e1b1827c84dfa4e9fbbfc8b52a204b5139e`.

## Context and orientation

The repository publishes skills from skills/ and a CLI from packages/rigorloop/. Current model owners separate capability behavior, storage/installation and engineering. Shared method projection and validation still have specs-hosted inputs; old test fixtures include both retired positive behavior and meaningful current negative inputs. Record these differences explicitly instead of deleting by age or name.

Do not rely on the stale project map for this change: inspect the actual source, runner/catalog/job entrypoints and fixture readers. The 116-source baseline, 235 root fixture files and 43 initial Python/CLI test entrypoints bound initial discovery, not all actual cases. Before modifying tests, enumerate the complete tracked test/fixture population and the runners or generators that produce additional cases. Capture explicit membership or complete family membership with exceptions in existing change-local evidence. This is a bounded audit, not a new permanent ledger or validation platform.

Use the checkout CLI for current recording and record the tool/candidate distinction. Preserve original historical records and approvals. The implementation must not use a draft Design, inventory alone, a passing reduced suite or a previous milestone judgment as whole-change authority.

## Non-goals

- No unrelated product redesign, new submodel, token metric, persistent inventory service or renamed legacy-spec collection.
- No customer-governance adoption or blanket prohibition of customer specs; no new legacy runtime reader or data migration.
- No installation into active user skill roots, target-agent acceptance task, publication, release, merge or external account mutation.

## Requirements covered

| Owning requirements / engineering obligation | Allocation | Concrete proof |
| --- | --- | --- |
| SYS-SR-13, ENG-SR-15 | M1–M6 | TG-01–08, TG-FINAL-01/02; full inventory/reliance and empty-tree evidence |
| DES-SR-23, VAL-SR-28, DIST-SR-24 | M1, M3, M6 | TG-01/02/04/07/08; explicit model/feature, projection and candidate boundaries |
| SKL-SR-28/29, WF-SR-19, RC-SR-22/23 | M2, M4, M6 | TG-03/05/07; exact specialist interfaces, authority, output, recovery and current policy proof |
| CLI-SR-29/30, DIST-SR-23, REL-SR-26 | M3, M6 | TG-04/07, TG-FINAL-01; actual CLI/package/qualification checks |
| VAL-SR-26, TEST-SR-01–14, VAL-SR-19–22 | M1–M5 | TG-01–06; case/fixture purpose, retained detection, isolated execution and full membership |
| VAL-SR-27, current evidence routing and original-byte retention | M1, M4, M6 | TG-05/08, TG-FINAL-02; local/range actual selection, unknown/mixed/deleted/renamed cases |
| Unchanged CLI-SR-01–28, RF-SR-01–14 and Installation DIST-SR-07–16 | M3, M4, M6 | Current v3 CLI/storage and real candidate installation regressions, privacy and no-side-effect failures |

The mapping is many-to-many. Concrete tests remain implementation-owned. Distinct newly discovered required failures join their affected group; they are not excluded because no scenario row listed them.

## Milestones

### M1. Remove historical activation dependencies and relocate portable resources

- Milestone kind: implementation
- Engineering purpose: Remove historical activation dependencies and relocate portable resources as one coherent contract/reader/proof slice.
- Requirements: SYS-SR-13, DES-SR-23, VAL-SR-28, DIST-SR-24
- Architecture responsibility: Design/Validation input classification and Packaging shared-source projection
- Dependencies: Approved exact Design and Delivery packages; complete baseline source identities available.
- Implementation scope: Move the three portable references and closed manifest to their approved maintained homes. Replace repository activation/rollback/grandfathering readers with current model validation and explicit feature/proof input handling; reconcile generator, validator, release and selector callers in the same slice. Retire activation YAML and its exclusive fixture machinery. Record the affected cases and fixture readers as the first portion of the whole-population audit.
- Files/components likely touched: scripts/boundary_first_reference.py, scripts/boundary_first_validation.py, scripts/validate-boundary-first.py, scripts/project-boundary-first-reference.py, scripts/boundary-first-resources.yaml, templates/shared/boundary-first-*.md, supported skill reference projections, relevant package/release callers and boundary fixtures
- Required verification: TG-01: exact resource bytes/consumers/paths and malformed/missing/escaped/drifted source rejection; TG-02: model discovery, explicit supported feature/proof grammar, unmarked adoption-decision need, empty/malformed model population and no historical activation/Git dependency.
- Evidence expectations: Exact changed subjects and case/fixture membership, current obligation/hazard, retained detection or explicit retirement, reader/catalog reconciliation, actual commands/results and limitations.
- Implementation steps: Inspect exact source and cases; establish required current proof before removing its predecessor; implement the bounded consumer/source correction; run focused then required selected checks; reconcile evidence and hand off to independent Code Review.
- Validation commands: See the exact commands below.
- Expected observable result: Generation and validation use only current sources; supported methods and meaningful negative fixtures remain. Ordinary validation reports actual scope with no historical activation/rollback claim.
- Completion criteria: Every relocated resource has old/new byte identity and exact projection proof; all callers of removed activation helpers are reconciled; no active skills or unrelated files are overwritten.
- Required evidence: Stage-owned implementation/test-maintenance rationale, actual validation output and independent milestone assessment.
- Review handoff: Independent Code Review of this complete milestone, retained protection and previous-milestone interactions; required corrections close before dependent work.
- Optional commit boundary: `M1: Remove historical activation dependencies and relocate portable resources` (one or more coherent commits without hiding remaining milestone work).
- Risks: Partial manifest/source transition or missed release reader.
- Rollback/recovery: Restore source, manifest, projections, validators and their callers as one slice; do not repair an installation or recover old approval state.

```bash
python scripts/project-boundary-first-reference.py --check
python scripts/validate-boundary-first.py --check
python scripts/test-boundary-first-reference.py
python scripts/test-boundary-first-validation.py
python scripts/test-select-validation.py
bash scripts/ci.sh --mode local
```

### M2. Reconcile specialist and workflow consumers with current owners

- Milestone kind: implementation
- Engineering purpose: Reconcile specialist and workflow consumers with current owners as one coherent contract/reader/proof slice.
- Requirements: SKL-SR-28/29, WF-SR-19, RC-SR-22/23; existing SKL-SR-04/07/08–14 and RC-SR-01–23
- Architecture responsibility: Skill capability realization, Workflow follow-up placement and Assessment interfaces
- Dependencies: M1 reviewed; current source disposition identifies all specialist and common consumer families.
- Implementation scope: Update canonical skills, selective resources, assets, validators and current guides only where they depend on retired specs or stale representations. Preserve exact public classifications/results, conditional loading, permitted mutations, recovery, bounded CI repair and Verify/PR distinctions. Remove obsolete ledger/measurement/rollout assertions and exclusive fixture data; retain parser-sensitive public contracts. Record unchanged surfaces with reasons and group membership.
- Files/components likely touched: skills/, templates/shared/, scripts/skill_validation.py, related literal/guide/review validators, scripts/test-skill-validator.py, tests/fixtures/skills/, support and invocation scenario data
- Required verification: TG-03: valid/invalid specialist operation and authority, unknown values, complete output groups, resource triggers/failure, no-mutation modes, exact proof/retry identity, PR preparation/refresh/transition and bounded CI-repair admission.
- Evidence expectations: Exact changed subjects and case/fixture membership, current obligation/hazard, retained detection or explicit retirement, reader/catalog reconciliation, actual commands/results and limitations.
- Implementation steps: Inspect exact source and cases; establish required current proof before removing its predecessor; implement the bounded consumer/source correction; run focused then required selected checks; reconcile evidence and hand off to independent Code Review.
- Validation commands: See the exact commands below.
- Expected observable result: Current specialist guidance and meaningful static scenarios agree with current owners, with no required local specs source or retired format procedure.
- Completion criteria: All specialist families in the disposition have current consumer reconciliation and current negative protection; no incidental literal claim overrides a preserved public vocabulary.
- Required evidence: Stage-owned implementation/test-maintenance rationale, actual validation output and independent milestone assessment.
- Review handoff: Independent Code Review of this complete milestone, retained protection and previous-milestone interactions; required corrections close before dependent work.
- Optional commit boundary: `M2: Reconcile specialist and workflow consumers with current owners` (one or more coherent commits without hiding remaining milestone work).
- Risks: Deleting a live classifier or broadening a specialist write/continuation boundary under a prose simplification.
- Rollback/recovery: Restore the coherent skill/resource/validator/fixture slice and repair the owning contract or proof before renewed reliance.

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/test-guide-system-validator.py
python scripts/project-boundary-first-reference.py --check
bash scripts/ci.sh --mode local
```

### M3. Reconcile CLI, package and release source consumers

- Milestone kind: implementation
- Engineering purpose: Reconcile CLI, package and release source consumers as one coherent contract/reader/proof slice.
- Requirements: CLI-SR-29/30, DIST-SR-23/24, REL-SR-26; existing CLI/Records/Installation safety
- Architecture responsibility: CLI generic/recording/discovery interface separation and Engineering candidate qualification
- Dependencies: M1 and M2 reviewed; current generic and recording contract domains identified.
- Implementation scope: Remove old spec/activation/named-release input dependencies while preserving actual supported generic output, private bounded logs, v3 storage, installation trust/conflicts, npm content and current candidate/profile qualification. Audit package-local tests, embedded fixtures and release data readers; remove metric/recipe-only cases and refine useful current boundaries. Preserve actual current release inputs and original records.
- Files/components likely touched: packages/rigorloop/dist/, packages/rigorloop/test/, packages/rigorloop/package.json, scripts/adapter_distribution.py, scripts/release*.py, scripts/validate-release.py, scripts/test-adapter-distribution.py, scripts/test-npm-package-publication.py, scripts/test-release-transaction.py, tests/fixtures/adapters/, tests/fixtures/release-transaction/
- Required verification: TG-04: generic projection parity vs recorder/discovery envelopes, logging disabled/degraded/unsafe/corrupt/contention/privacy, actual npm member policy, candidate resource/install parity and missing current evidence failing before side effects. Historical recipe absence is allowed; publication is not performed.
- Evidence expectations: Exact changed subjects and case/fixture membership, current obligation/hazard, retained detection or explicit retirement, reader/catalog reconciliation, actual commands/results and limitations.
- Implementation steps: Inspect exact source and cases; establish required current proof before removing its predecessor; implement the bounded consumer/source correction; run focused then required selected checks; reconcile evidence and hand off to independent Code Review.
- Validation commands: See the exact commands below.
- Expected observable result: Current CLI and supported packages work with maintained resources; obsolete release recipes no longer act as qualification or authorization.
- Completion criteria: Every selected CLI/package/release spec family has a complete current contract and consumer disposition; tests observe actual CLI/archive/tarball boundaries, including required negative cases.
- Required evidence: Stage-owned implementation/test-maintenance rationale, actual validation output and independent milestone assessment.
- Review handoff: Independent Code Review of this complete milestone, retained protection and previous-milestone interactions; required corrections close before dependent work.
- Optional commit boundary: `M3: Reconcile CLI, package and release source consumers` (one or more coherent commits without hiding remaining milestone work).
- Risks: Confusing generic schema versions with stored versions, deleting installer trust inputs, or replacing historical replay with a hardcoded newest-version list.
- Rollback/recovery: Restore affected runtime/package/qualification and fixture changes together; preserve customer state, public artifacts, historical judgments and independently owned release evidence.

```bash
npm test --prefix packages/rigorloop
python scripts/test-adapter-distribution.py
python scripts/test-npm-package-publication.py
python scripts/test-release-transaction.py
python scripts/build-adapters.py --check
bash scripts/ci.sh --mode local
```

### M4. Retire obsolete governance checks and fixtures

- Milestone kind: implementation
- Engineering purpose: Retire obsolete governance checks and fixtures as one coherent contract/reader/proof slice.
- Requirements: VAL-SR-26/27, ENG-SR-15; WF-SR-01–19, RC-SR-01–23, RF-SR-01–14
- Architecture responsibility: Validation legacy reader/case maintenance at current workflow and storage boundaries
- Dependencies: M1–M3 reviewed; their retained/refined/removed cases and reader changes available.
- Implementation scope: Assess the complete artifact-lifecycle, review-artifact, change-metadata, workflow-automation/state/policy, query and fidelity test populations, including fixture builders. Remove positive acceptance and exclusive readers for retired lifecycle runtimes/rollout state. Retain independent current v3, reference, authority, discovery, parser and negative/regression protection with meaningful fixtures. Reconcile catalog/direct/CI callers of every removed entrypoint.
- Files/components likely touched: scripts/test-artifact-lifecycle-validator.py, scripts/test-review-artifact-validator.py, scripts/test-change-metadata-validator.py, scripts/test-workflow-*.py, scripts/test-validate-workflow-automation.py, scripts/test-query-change-record.py, scripts/test-governed-lifecycle-cli-validator.py, their implementation helpers, tests/fixtures/artifact-lifecycle/, tests/fixtures/review-artifacts/, tests/fixtures/change-metadata/, tests/fixtures/rigorloop-records-v3/
- Required verification: TG-05: current recording/discovery/routing/authority failures remain detected independently of retired production packs; unknown/malformed current inputs remain errors, archives are not active stores, and deleted commands have no callers or fake pass.
- Evidence expectations: Exact changed subjects and case/fixture membership, current obligation/hazard, retained detection or explicit retirement, reader/catalog reconciliation, actual commands/results and limitations.
- Implementation steps: Inspect exact source and cases; establish required current proof before removing its predecessor; implement the bounded consumer/source correction; run focused then required selected checks; reconcile evidence and hand off to independent Code Review.
- Validation commands: See the exact commands below.
- Expected observable result: A smaller coherent validation surface protects present behavior and rejects current invalid inputs without executing retired state engines.
- Completion criteria: Every case/fixture in the named populations has explicit or complete grouped disposition and all removed check/fixture consumers are reconciled; current proof succeeds and independent review accepts its detection mechanism.
- Required evidence: Stage-owned implementation/test-maintenance rationale, actual validation output and independent milestone assessment.
- Review handoff: Independent Code Review of this complete milestone, retained protection and previous-milestone interactions; required corrections close before dependent work.
- Optional commit boundary: `M4: Retire obsolete governance checks and fixtures` (one or more coherent commits without hiding remaining milestone work).
- Risks: Mistaking any invalid old-format input for stale data, or retaining a compatibility engine merely to keep old tests green.
- Rollback/recovery: Restore lost case/proof and reader/catalog relationships, or correct current replacement proof; do not migrate historical records or silently weaken the current contract.

```bash
python scripts/test-select-validation.py
npm test --prefix packages/rigorloop
bash scripts/ci.sh --mode local --broad-smoke
```

### M5. Complete the repository-wide case and fixture audit

- Milestone kind: implementation
- Engineering purpose: Complete the repository-wide case and fixture audit as one coherent contract/reader/proof slice.
- Requirements: ENG-SR-15, VAL-SR-26; TEST-SR-01–14 and VAL-SR-19–22
- Architecture responsibility: Validation full population, fixtures, runner discovery and isolated execution
- Dependencies: M1–M4 reviewed; prior milestone case decisions retained as evidence, not assumed universal coverage.
- Implementation scope: Reconcile all remaining runners, tests, parameter tables and fixture builders across the tracked repository and CI/package entrypoints. Explicitly assess remaining documentation-prose, Markdown readability, guide-system, selector and validation-execution populations plus any newly discovered tests and fixture directories. Reuse reviewed current decisions from M1–M4 only where unchanged. Remove all remaining identified stale/redundant cases and orphaned exclusive data; refine useful cases.
- Files/components likely touched: All tracked test entrypoints/cases and fixtures; scripts/fixtures/; package-local fixtures; inline/generated cases; tests/fixtures/documentation-prose/; check catalog and hosted workflow callers
- Required verification: TG-06: complete discovered population accounted for; retained case groups distinguish plausible current violations and remain independently runnable with the shared budget. No unassessed generator, helper or direct-only suite is silently omitted.
- Evidence expectations: Exact changed subjects and case/fixture membership, current obligation/hazard, retained detection or explicit retirement, reader/catalog reconciliation, actual commands/results and limitations.
- Implementation steps: Inspect exact source and cases; establish required current proof before removing its predecessor; implement the bounded consumer/source correction; run focused then required selected checks; reconcile evidence and hand off to independent Code Review.
- Validation commands: See the exact commands below.
- Expected observable result: The complete test/fixture population has evidence-backed current-purpose disposition, with no identified stale remainder hidden outside tests/fixtures.
- Completion criteria: Membership reconciles baseline plus later additions/removals; every generator has its discovered domain and reader outcome accounted for; required protection and actual execution remain visible. A file/count inventory alone cannot close this milestone.
- Required evidence: Stage-owned implementation/test-maintenance rationale, actual validation output and independent milestone assessment.
- Review handoff: Independent Code Review of this complete milestone, retained protection and previous-milestone interactions; required corrections close before dependent work.
- Optional commit boundary: `M5: Complete the repository-wide case and fixture audit` (one or more coherent commits without hiding remaining milestone work).
- Risks: Incomplete test discovery or treating similar assertions as redundant despite distinct boundaries.
- Rollback/recovery: Retain uncertain cases while resolving purpose, restore deleted protection if equivalence fails, and route a normative ambiguity to Design without dropping it from scope.

```bash
python scripts/test-select-validation.py
python scripts/test-validation-execution.py
bash scripts/ci.sh --mode local --broad-smoke
```

### M6. Remove remaining specs and reconcile the whole current repository

- Milestone kind: implementation
- Engineering purpose: Remove remaining specs and reconcile the whole current repository as one coherent contract/reader/proof slice.
- Requirements: SYS-SR-13, ENG-SR-15, VAL-SR-27; all affected owner requirements above
- Architecture responsibility: System current authority, Engineering source retirement and complete integration
- Dependencies: M1–M5 reviewed; complete source knowledge, live readers and useful proof reconciled.
- Implementation scope: Recheck exact source bytes and uncommitted content; remove every remaining specs/ member and coupled superseded architecture/ADR sources whose selected authority/readers are resolved. Correct governance, current model maps, README/contributor/package text, navigation, templates and current claims to use self-contained current owners. Convert provenance to recoverable commit/path without rewriting historical judgments. Resolve all evidence and deleted/renamed selector routes and prove the actual complete branch scope.
- Files/components likely touched: specs/; coupled docs/architecture/ and docs/adr/ identified by source disposition; AGENTS.md, CONSTITUTION.md, README.md, CONTRIBUTING.md, current guides/models, package metadata/descriptions, templates, validation selection/catalog, owning change evidence
- Required verification: TG-07: empty specs tree and self-contained current owner/navigation/operational paths; TG-08: local/range deletion and rename routing, known-plus-unknown rejection, current Subjects vs unregistered siblings, and complete no-spec package/CLI/validation operation.
- Evidence expectations: Exact changed subjects and case/fixture membership, current obligation/hazard, retained detection or explicit retirement, reader/catalog reconciliation, actual commands/results and limitations.
- Implementation steps: Inspect exact source and cases; establish required current proof before removing its predecessor; implement the bounded consumer/source correction; run focused then required selected checks; reconcile evidence and hand off to independent Code Review.
- Validation commands: See the exact commands below.
- Expected observable result: No specs/ directory or identified stale test/fixture remains; current operations do not retrieve retired Git content and required negative behavior still fails correctly.
- Completion criteria: All 116 baseline sources and newly found dependencies have final dispositions, actual deletion/rename selection is complete, test audit closes across all milestones, current links/reliance are reconciled, and integrated required checks pass. No unresolved family is deferred as completion.
- Required evidence: Stage-owned implementation/test-maintenance rationale, actual validation output and independent milestone assessment.
- Review handoff: Independent Code Review of this complete milestone, retained protection and previous-milestone interactions; required corrections close before dependent work.
- Optional commit boundary: `M6: Remove remaining specs and reconcile the whole current repository` (one or more coherent commits without hiding remaining milestone work).
- Risks: A newly discovered live obligation or reader, changed source bytes, unknown deletion route or stale relied-on evidence.
- Rollback/recovery: Stop affected deletion, restore its coherent source/consumer/proof slice and obtain the required owner correction/reassessment. Preserve unrelated work and original historical record bytes.

```bash
python scripts/select-validation.py --mode local --json
python scripts/test-select-validation.py
python scripts/validate-boundary-first.py --check
python scripts/validate-documentation-prose.py --mode enforce
python scripts/build-adapters.py --check
bash scripts/ci.sh --mode local --broad-smoke
npm test --prefix packages/rigorloop
```

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all six implementation milestones and required corrections complete, with no remaining selected source or unassessed test/fixture family.
- Assessment: fresh independent whole-change Code Review of the complete delivered engineering diff and cross-milestone interactions against exact current Design and Delivery subjects.
- Evidence: exact final subjects, independent reviewer basis, findings and dispositions, full source/case reconciliation and actual integrated check results.
- Successor: distinct final Verify; corrections return to their owner and receive affected reassessment before renewed final reliance.

Earlier milestone approvals, structural checks and integrated test success do not substitute for this checkpoint.

## Change-level verification

### TG-FINAL-01. Operate the complete repository without specs

- Covers: M1–M6 and all affected shared boundaries.
- Demonstrate: current owner navigation and model validation, complete canonical/package resource generation, actual CLI generic and recorder/discovery behavior, npm member/installation safety and candidate qualification after specs and historical activation disappear. Invalid/missing current resources still fail before side effects; no ordinary Git retrieval supplies a retired input.
- Evidence expectations: `bash scripts/ci.sh --mode local --broad-smoke`, actual package-local CLI tests and candidate/archive/npm/installation regressions; retained release-transaction tests exercise the current prepared-candidate verifier and required negative boundaries. Observe actual retained candidate bytes and results, not a dry-run label. No live publication or remote configuration is required.
- Non-applicability: none; separate local passes cannot prove this assembled boundary.

### TG-FINAL-02. Complete retirement and actual change selection

- Covers: SYS-SR-13, ENG-SR-15, VAL-SR-26/27 and every baseline/new source/case family.
- Demonstrate: zero tracked/worktree specs members, all selected source identities accounted for, no stale current imports/links/manifests/readers, complete case/fixture audit including generated members, original historical judgments unchanged, meaningful retained failures and actual local/committed-range routing.
- Evidence expectations: compare final tree to the recorded baseline and change-local dispositions; inspect actual readers and generated dependencies; run the local selector and `python scripts/select-validation.py --mode pr --base 7ad33e1b1827c84dfa4e9fbbfc8b52a204b5139e --head HEAD --json` on the committed implementation. Also run `bash scripts/ci.sh --mode pr --base 7ad33e1b1827c84dfa4e9fbbfc8b52a204b5139e --head HEAD` for that exact range. Unknown or dropped deletions cannot count as selected proof. Review current evidence applicability separately from historical reference recovery.
- Non-applicability: none; a smaller file count or empty directory alone proves neither preserved knowledge nor complete test maintenance.

## Validation plan

Use the exact focused and repository-owned commands allocated per milestone. The recorded command must state actual options, target identities and outcomes. CI's shared budget and normal phase gates apply; do not introduce nested worker pools, cached success or skip required failures.

M1's explicit boundary scripts and M2's current skill/guide validation remain supported commands under this plan; their old activation or wording-only cases may retire while their current purposes remain. Other obsolete governance entrypoints in M4 may disappear; record their actual removed check IDs and preserved current replacement detection before relying on the reduced catalog. Do not execute absent commands as successful no-ops. A change to required public proof or command authority returns to the owning Design/Delivery decision.

Current no-spec integrated proof includes `python scripts/build-adapters.py --check`, `npm test --prefix packages/rigorloop`, candidate/package regressions and the selected-plus-broad invocation. Real prepared-candidate qualification uses the existing `bash scripts/release-verify.sh <matching-tag> --prepared-candidate <isolated-candidate-directory>` path inside release-owned regression proof, binding tag/source/profile/artifact identities. The old bare historical-tag verifier is not a valid substitute for the current prepared-candidate contract. No `execute` or public publish command is authorized.

Design and prose verification use `python scripts/validate-boundary-first.py --check` after M1 and `python scripts/validate-documentation-prose.py --mode enforce`; validate the current change store with `node scripts/validate-record-store.mjs docs/changes/2026-09-14-retire-specs-and-stale-tests/change.json`. Before PR readiness, `git diff --check` and actual committed PR-range selection supplement complete required verification. Run only new/relevant proof after evidence-only recording changes where Assessment permits reuse; record the basis rather than rerunning blindly.

## Risks and recovery

- A source has a still-unowned obligation: correct Design and its source map before dependent removal, then obtain affected review; do not narrow the target silently.
- A test or generated fixture has uncertain protective value: retain it while inspecting its oracle, readers and current contract; establish replacement detection or explicit retirement before reducing coverage.
- A local source differs from the recorded baseline: preserve uncommitted content, record the new exact basis and reassess before deletion.
- A current record/review/release depends on a removed input: retain or replace its complete necessary basis with the responsible assessor; do not retarget historical judgments.
- An operation is interrupted or a concurrent edit appears: restore or complete only the identified coherent source/reader/proof slice; preserve unrelated work, installed files and original historical records.

Git is recovery for retired material, not an operational input for current builds or customer policy. Obtain the known baseline if absent before relying on its recoverability. No destructive external action is part of rollback.

## Dependencies

- Exact approved Proposal, Design and Delivery packages precede implementation reliance; work initialization uses only the approved ordered milestones.
- M1 → M2 → M3 → M4 → M5 → M6; independent review/correction closes each slice before the next relies on it.
- Full source/case discovery starts before the first test change and is reconciled through every milestone; M5 is final population reconciliation, not the first audit.
- Final Code Review follows all implementation/corrections; final Verify remains distinct. PR preparation/opening is a later separately authorized handoff.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-14 | Reconcile current resources and consumers before final tree deletion. | Keeps each milestone testable and makes the final absence proof meaningful. | Delete all first and reconstruct obligations from failing tests; retain specs indefinitely. |
| 2026-09-14 | Audit test populations in their owning slices and reconcile the entire population before closeout. | Preserves distinct protection while exposing inline/generated and direct-only remainder. | File-count-only audit; removing every historical invalid input; unlimited later cleanup proposals. |
| 2026-09-14 | Reuse current shared sources, check catalog, executor and evidence records. | No new platform or competing normative/test-spec owner is needed. | Permanent retirement registry, replacement metric programme or renamed archive collection. |

## Readiness

See the owning change record for current workflow state. This plan's existence records execution intent; independent Delivery Review, implementation, milestone assessments, final whole-change Code Review and distinct Verify remain required before completion.
