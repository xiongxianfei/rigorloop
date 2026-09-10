<!-- Template: plan-skeleton-v3 -->

<!-- Skill: plan -->

<!-- Template status: normative -->

<!-- Structural-fingerprint: sha256:41e5a53fc9626de70a61c8506ea7fd8b4de125eb1c1d35e0d65831f0c7cbff35 -->

# Approval-Driven Release and Source Consolidation Delivery Plan

## Purpose / big picture

Implement the reviewed Release contract so that supported routine work reaches a complete candidate automatically, the maintainer approves that exact candidate once, and tooling publishes, observes and reports the authorized result. Transfer the selected source definitions and remove six superseded documents after their consumers are coherent. Preparation, execution and CI integration precede source retirement; no intermediate milestone alone establishes the complete operation.

## Current Handoff Summary

- Owning change record: [release-model-source-consolidation](../changes/2026-09-09-release-model-source-consolidation/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Approval-driven Release direction](../proposals/2026-09-09-release-model-source-consolidation.md), independently assessed by `proposal-review-r4`.
- Spec: [Release](../design/release/release.md), REL-SR-01–24, including its retained formats, population boundaries and complete displacement map.
- Architecture: the exact `design-review-r4` package contains Release; [System](../design/system/system.md), scoped Release composition; [Design](../design/design/design.md), scoped DES-SR-21 retention extension; and [published-skill-first](../../specs/published-skill-first-repository-simplification.md), scoped R7/R8 amendment. It includes the approved S → C → archive → bundled metadata → npm pack → outer evidence sequence.
- Prior-contract test spec: `specs/release-process-contract.test.md` and `specs/release-transaction-automation.test.md` remain inspected sources of retained protection until their mapped retirement. They impose no new standalone test-spec or historical rehearsal programme. Release's explicit timing and lifecycle supersessions control this slice.
- Assessment and test owners: [Review and Closeout](../design/review-closeout/review-closeout.md) and [Test](../design/test/test.md). Original judgments and resolved findings keep their original subjects.

## Context and orientation

The inspected baseline has `release_transaction.py` preparation/preflight/public-closeout helpers, a tag-triggered `.github/workflows/release.yml`, full verification in `release-verify.sh`, and release/package validators. The workflow publishes a package directory; it does not yet supply the new candidate approval path. Preparation expects a profile, some generated evidence contains declared passes, timing validation can block release composition, and supported-version selectors need inspection rather than an assumed v0.5.1 release pass.

Candidate construction must respect real installer consumption: adapter archives supply facts for `packages/rigorloop/dist/metadata/adapter-artifacts-<tag>.json`; `releases.json` binds those metadata bytes; npm packing follows. C is sealed source, the generated overlay is a separately declared build input, and final tarball identity belongs in outer evidence. Metadata or reporting produced after packing cannot repair an invalid package.

Use the model and current script/consumer inspection for change placement. The project map is orientation only: its historical recording and release descriptions do not establish the new operation or current authority. No project-map claim replaces direct inspection. The literal-audit baseline under `docs/changes/2026-06-29-release-transaction-automation/` is a live input and stays.

## Non-goals

No real publication, tag push, remote release creation, customer installation, credential change or remote environment configuration is authorized by this plan. Implement and safely test the capability; one-time external setup remains a separately authorized deployment prerequisite. No version bump is selected for the development checkout. Temporary candidate versions are fixture inputs, not a real release decision.

Do not create a hosted service, general workflow engine, cache, standalone test specification, permanent per-test ledger or adoption registry. Do not generalize prerelease/special-release support, redesign Distribution/Installation, repeat Skill adoption, remove unrelated tests or delete whole directories. Current aliases and retained runtime safeguards remain compatible unless the Design explicitly amends them.

## Requirements covered

| Governing obligations | Existing allocation |
| --- | --- |
| REL-SR-01–07 | M1 / TG-01–02: eligible reviewed input, version/profile derivation, generated ownership, idempotency, preflight and literal protection; M3 / TG-06: real entry path. |
| REL-SR-08–09 | M1 / TG-02: candidate proof and same command composition; M3 / TG-06 and TG-FINAL-01: complete orchestration and final evidence applicability. |
| REL-SR-10–17 | M2 / TG-03–04: exact authorization, trusted path, public observation, durable facts, partial/uncertain outcome, recovery, deferrals and confidentiality; M3 / TG-05–06: hosted boundary and exceptional paths. |
| REL-SR-18–19 | M1 / TG-02: explicit diagnostic timing consequence and retained format rejection; M2 / TG-04: required public facts despite telemetry loss; M3 / TG-06: real composition and compatibility. |
| REL-SR-06/08/09/14/19/21/22, scoped standalone-command refinement | M5 / TG-09: redundant alias retirement, retained canonical/standalone protection and detached-checkout fixture; renewed TG-FINAL-01 and final assessments. |
| REL-SR-20–21 | M4 / TG-07–08: exact source/consumer retirement and proportionate proof; TG-FINAL-01 plus final Code Review and Verify. |
| REL-SR-22 | M1 / TG-01, M2 / TG-04, M3 / TG-05–06: automatic complete operator path with one normal approval, no duplicated entry and explicit exceptions. |
| REL-SR-23–24 | M1 / TG-01–02: sealed candidate and factual projections; M2 / TG-03–04: approval, invalidation, deduplication and persistence; M3 / TG-05–06: actual CI composition. |
| SYS-SR-02/04/06/07/08/09, scoped Release interaction | M1–M3 / TG-01–06 for source/artifact/evidence/authority consumers; M4 / TG-07–08 for one owner, history and remaining follow-ups; TG-FINAL-01 for the composed result. |
| DES-SR-13/18/19/21, selected source transfer and retention | M4 / TG-07–08: complete disposition and coordinated removal. No unrelated retention rule is amended. |
| Published-skill-first R7/R8 scoped transfer; applicable Test and Review/Closeout criteria | M1 / TG-02, M3 / TG-06 and TG-FINAL-01 retain product protection, assess actual detection and honor evidence/freshness policy; final independent Code Review precedes distinct Verify. |

## Milestones

### M1. Prepare and verify an immutable routine candidate

- Milestone kind: implementation.
- Engineering purpose: establish correct input, artifact and proof identities before any new publication entrypoint can depend on them.
- Requirements: REL-SR-01–09/18/19/22–24; SYS-SR-02/04/08.
- Architecture responsibility: Release routine coordination, S/C and build-overlay sequence, authoritative facts; REL-DEC-03/06–08.
- Dependencies: exact approved Design and Delivery package. Existing live/tag route remains unchanged; new candidate functionality has no external write authority.
- Implementation scope: derive the supported profile/notes from the reviewed next version, version rationale and change summaries under established policy. Handle ambiguous/missing decisions and already-published no-op distinctly. Produce deterministic C with an allowlisted generated diff, then archives, bundled metadata/index, npm tarball and outer binding. Integrate preflight/full checks without manufacturing pass assertions. Select the new-path nonblocking timing consequence explicitly while retaining diagnostic format validation and historical/special applicability.
- Files/components likely touched: `scripts/release_transaction.py`, `prepare-release.py`, `release-preflight.py`, `release-verify.sh`, `validate-release.py`, `validate-release-ci.py`, existing metadata builders, release/profile/evidence templates and relevant schema readers; `scripts/test-release-transaction.py`, `scripts/test-npm-package-publication.py` and `tests/fixtures/release-transaction/`. A bounded coordinator module may separate orchestration from helpers; it must reuse their contracts rather than create a parallel validation definition.
- Required verification: TG-01 — complete supported inputs produce a stable candidate; unknown profile/target values, absent version authority, unexplained C/overlay edits and unsupported special handling reject without publication or an approval request. TG-02 — actual archives → metadata/index → packed-install chain, stale digest and post-pack substitution rejection, generated pending versus observed pass, cheap preflight versus full verification, and timing-only diagnostic consequences with required evidence still blocking.
- Evidence expectations: run the existing focused release regression entrypoint against isolated repositories and actual validators. Include deterministic repeat/interruption of preparation, preserved narrative/history, metadata digest mismatch despite valid outer archive evidence, malformed timing versus absent timing and missing required correctness facts. Use external state fixtures for read-only registry resolution; do not give preparation publishing credentials.
- Implementation steps: add counterexample fixtures first; implement reviewed input resolution and C/overlay identity; connect existing builders in the approved order; derive metadata and evidence from actual outputs; amend timing composition and affected profile/check consumers together; inspect release supported-version selectors without rewriting historical cases.
- Validation commands: `python scripts/test-release-transaction.py`; `python scripts/test-npm-package-publication.py`; candidate archive/package commands in the Validation plan when those producers change. Run `python scripts/test-adapter-distribution.py` if shared generation or metadata code changes. New proof must be discovered by these existing test entrypoints or explicitly added to the affected selector under its owner.
- Expected observable result: a verified retained candidate or an actionable preapproval exception, with no remote write and no manual generated-data task.
- Completion criteria: TG-01–02 pass at actual source/package boundaries; required validators execute and retain negative detection; legacy behavior outside the selected new path is supported. Candidate metadata and dependent assertions have an inspected affected/unaffected disposition.
- Required evidence: exact source/generator/configuration and candidate identities, concrete commands/results, meaningful failure observations, timing-policy before/after and compatibility limits in stage-owned v2 evidence.
- Review handoff: independent Code Review of the complete candidate/preflight/timing slice and its producer/consumer interactions.
- Optional commit boundary: `M1: prepare verified immutable release candidates`.
- Risks: generic generated passes may masquerade as proof; packing before bundled metadata gives an unusable installer; an old supported-version constant may reject new eligible input.
- Rollback/recovery: restore changed candidate/preflight/validator consumers together. Keep the new path unavailable until corrected; preserve existing profiles, source and historical metadata. No public operation or tag is undone.

### M2. Execute the approved identity and persist observed outcomes

- Milestone kind: implementation.
- Engineering purpose: implement the irreversible-operation boundary and durable evidence while it remains disconnected from an automatic hosted trigger.
- Requirements: REL-SR-10–19/22–24; SYS-SR-04/06/09.
- Architecture responsibility: protected executor, authoritative observations, configured evidence ref, Runtime steps 3–5; REL-DEC-02/04/06/08.
- Dependencies: M1 and its independent milestone assessment. M2 accepts only the sealed candidate basis and verified approval-provider input, never an arbitrary branch tip or generic boolean approval.
- Implementation scope: validate exact candidate, destinations/path, provider approval and evidence applicability; publish retained artifacts through bounded adapters around existing GitHub/npm mechanisms; observe registry/assets/fresh smoke; generate standing/companion records and update the configured evidence ref with compare-and-swap. Keep public side effects substitutable at the external boundary. No automatic workflow activation in this milestone.
- Files/components likely touched: release coordinator/shared helper modules, `close-release-publication.py`, evidence templates/validation/readers, `scripts/test-release-transaction.py` and its fixtures. Reconcile real tarball publishing and trusted provenance arguments; do not preserve directory repacking as equivalent.
- Required verification: TG-03 — missing/stale/mismatched/rejected approval, changed source/overlay/tarball/channel/destination, duplicate approval and competing execution; denial has no external write. Unchanged adequate rechecking may continue under the original authorization. TG-04 — matching public state resumes observation; definite absence permits only the authorized missing write; lost response/delayed visibility, partial GitHub/npm outcomes, public mismatch, failed smoke and failed evidence persistence preserve actual identities and failure meaning.
- Evidence expectations: deterministic simulated registry/GitHub and local Git remotes, actual executor dispatch/persistence/validators, captured write counts and preserved bytes. Test evidence-ref CAS conflict without overwriting unrelated version or failed-attempt records; reporting retry cannot republish. Check secret suppression and emergency/non-deferred boundaries. Missing timing must not remove mandatory publish-event facts.
- Implementation steps: write authority/retry/persistence failures first; implement candidate-bound execution and external-state inspection; generate all projections from common observations; persist pending/approval facts before publication and outcomes after each boundary; provide actionable bounded exceptions without silently choosing new versions, authentication, deprecation or channel changes.
- Validation commands: `python scripts/test-release-transaction.py`; `python scripts/test-npm-package-publication.py` for changed tarball/publication argument behavior. Run shell syntax checks for changed shell helpers. Tests substitute external services, not validators, authorization policy or persistence implementation.
- Expected observable result: one authorized exact execution produces truthful durable outcome; exceptional attempts stop safely or resume only the still-authorized missing operation.
- Completion criteria: TG-03–04 demonstrate winner/duplicate/uncertain/partial/failed outcomes with actual executor and evidence-store boundaries. No new publication inference arises from duplicate events or a successful report repair.
- Required evidence: approved-candidate binding, test authority origin, before/after local remote state, public-operation event counts, non-leaking diagnostics and recovery results; explicitly identify substituted services and unexecuted real publication.
- Review handoff: independent Code Review of execution authority, uncertain-write recovery, immutable artifact use and durable reporting as a complete slice.
- Optional commit boundary: `M2: execute approved candidates with durable outcomes`.
- Risks: lost response can prompt a duplicate write; replacing checks with pass stubs hides incorrect publication; evidence failure can conceal a completed write.
- Rollback/recovery: keep hosted invocation disconnected; restore executor and evidence readers together. Preserve observed outcomes and immutable artifacts. For any separately authorized real operation, inspect public state and apply Release recovery rather than reverting a public version.

### M3. Compose the single-approval CI path and prove it end to end

- Milestone kind: implementation.
- Engineering purpose: join reviewed candidate and execution boundaries without leaving a legacy trigger that bypasses authorization or requiring extra normal approvals.
- Requirements: REL-SR-01–03/08–19/22–24; SYS-SR-02/04/06/08/09; scoped R7/R8.
- Architecture responsibility: default-branch preparation and one protected executor, Deployment prerequisites, local/CI command parity and evidence-ref readers.
- Dependencies: M1–M2 and their independent milestone assessments. Remote environment/reviewer, OIDC, evidence-ref permission and retention configuration are explicit setup requirements, not inferred from a workflow file or changed during this engineering task.
- Implementation scope: wire automatic eligible preparation, required checks and concise summary to one protected approval job; publish/observe/report within that boundary. Validate missing/misconfigured protection and unsupported inputs fail closed. Reconcile the old tag-triggered route so it consumes matching authorization or cannot publish this new routine candidate independently. Document setup, ordinary operation, supported legacy/special entrypoints and exceptional intervention separately. Adopt the evidence-ref lookup in actual release guidance/validators.
- Files/components likely touched: `.github/workflows/release.yml`, repository-owned coordinator, `release-verify.sh`, `validate-release.py`, `validate-release-ci.py`, scoped CI selectors/assertions, `docs/releases/README.md`, relevant contributor guidance and `scripts/test-release-transaction.py`. Inspect `scripts/ci.sh` consumers rather than introducing another correctness definition.
- Required verification: TG-05 — actual workflow/dispatcher composition requires one authorized candidate approval; absent environment protection/approval, altered artifact provider identity, bypassing tag trigger and unavailable credentials cannot publish. TG-06 — full operator path from reviewed merged fixture inputs plus established configuration through preparation, checks, one substituted approval, publication, public observation and durable report, with no manual profile/hash/timing/result entry.
- Evidence expectations: invoke the actual coordinator from the same entry boundary used by the workflow; model the provider approval/external services only. Run real candidate/package validators and packed-install proof at least once in the complete path. Assert one approval, published bytes equal approved bytes and the durable report reads through the configured evidence-ref consumer. Include prerequisite failure before approval, postapproval candidate change, duplicate/lost publication response, public verification failure, unavailable timing and evidence persistence recovery without multiplying every local case.
- Implementation steps: integrate thin CI wiring after testable lower boundaries; make legacy/new route exclusion explicit; implement fail-closed setup checks and recorded configured destinations; connect public closeout and durable reporting without a second human step; run complete-path proof and inspect parity with actual YAML/job dependencies.
- Validation commands: `python scripts/test-release-transaction.py`; `python scripts/test-npm-package-publication.py`; `bash -n scripts/release-verify.sh scripts/ci.sh`; change-selected `ci.sh --mode explicit` as specified below. Full-path tests must execute the repository-owned verification composition against a temporary prepared candidate, with real required checks and safe external substitutes. Do not run the production publisher for proof.
- Expected observable result: the supported configured path requires only one approval and completes or reports the exact exception. Unconfigured deployment is explicitly unavailable; local proof is not a claim that hosted setup or public publishing succeeded.
- Completion criteria: TG-05–06 and TG-FINAL-01's integrated behavior pass; actual workflow paths and legacy consumers are reconciled, with setup and real-publication limits stated. Candidate metadata and any changed projections are current under the owning builders.
- Required evidence: complete-path command traces/results and approval/action counts, retained candidate/report identities, YAML-to-dispatch inspection, setup-negative proof, and a bounded CI-maintenance assessment of triggers, permissions, serialization and parity. Local validation does not claim hosted green status.
- Review handoff: independent Code Review of the composed path and CI-maintenance assessment for the material workflow change. A CI-maintenance correction needs affected reassessment before M4.
- Optional commit boundary: `M3: compose one-approval release execution in CI`.
- Risks: a tag route races the new executor; a newly created unprotected environment silently runs; a workflow artifact expires; a second job approval restores manual coordination.
- Rollback/recovery: fail closed or disable the affected new entry path before restoring its coherent wiring and consumers. Do not fall back to an unguarded publisher or claim the failed candidate was released. Restore pending evidence and inspect external state before any separately authorized retry.

### M4. Adopt current ownership and retire the selected prose

- Milestone kind: implementation.
- Engineering purpose: remove obsolete definitions only after their surviving contract and actual operational readers are supported.
- Requirements: REL-SR-20–21; SYS-SR-02/04/06/07/08/09; DES-SR-13/18/19/21; scoped R7/R8.
- Architecture responsibility: Release exact file/architecture disposition and consumer map; System ownership/follow-up boundary; Design retention extension.
- Dependencies: M1–M3 and required reviews/corrections. Complete candidate/execution consumers must exist before their old source definitions are removed. Final adoption remains subject to final independent review and successful Verify.
- Implementation scope: remove exactly the four Release process/transaction spec and test-spec documents and their two ADRs named by the Design. Apply the exact architecture paragraph/subsection/bullet map; retain mixed Distribution/Installation/version histories. Reconcile current navigation and necessary consumers; preserve operational profiles, schemas, fixtures, records and the literal baseline. Reconcile FU-013's Release portion while leaving its Distribution/Installation remainders and other follow-ups open under their owners.
- Files/components likely touched: the six selected source files; `docs/architecture/system/architecture.md`; `docs/releases/README.md`; necessary navigation; the existing follow-up register. Review `AGENTS.md`, `CONSTITUTION.md`, project map, skill references, selectors, package resources and archive copies for actual dependence; change only directly affected current guidance or record inspected unaffected/retained dispositions.
- Required verification: TG-07 — every selected surviving clause, meaningful decision and representative acceptance intent has one usable current owner; a reviewer can apply the rule without reconstructing removed prose. TG-08 — removed-source references are classified by real use, retained operational/historical bytes remain valid, and current readers use the replacement. No automatic archive/redirect, whole-directory deletion or rewritten old judgment.
- Evidence expectations: grouped baseline-to-final source and consumer disposition in existing change evidence, exact removal diff, local current-link/reader checks and retained baseline digest. For old assessments whose input source is removed, obtain the responsible assessor's current-reliance disposition where still needed; preserve old subjects/judgments and use current adoption evidence rather than declaring those judgments now about replacement content. A historical citation alone does not require an original-path copy.
- Implementation steps: confirm the Design map against the then-current source and reader graph; reconcile remaining current readers; remove the six mapped files and only mapped architecture prose; update navigation and follow-ups through their owning mechanisms; assess final proof applicability after cleanup. A newly inseparable unowned responsibility returns to Design/scope decision, not a seventh implicit deletion.
- Validation commands: model/prose/readability checks and scoped `ci.sh --mode explicit` below; actual touched reader regressions if any. Reuse M3 integrated evidence only after recording that C/build/check/configuration and relevant dependencies remain applicable; rerun affected proof when they change.
- Expected observable result: one accessible Release contract with the selected old sources absent, useful operational/history remainders intact, and no stale current reader.
- Completion criteria: TG-07–08 pass, each retained exception has a need/owner, mapped cleanup is complete, actual follow-ups distinguish remaining work, and TG-FINAL-01 has an adequate final basis. An unresolved selected removal prevents a false completed-cleanup claim.
- Required evidence: semantic displacement assessment, removed/retained identities, consumer disposition, follow-up references and exact final check results/limitations.
- Review handoff: independent milestone Code Review of the full ownership/removal/consumer slice; this does not substitute for the final whole-change checkpoint.
- Optional commit boundary: `M4: adopt Release ownership and retire superseded sources`.
- Risks: historical-path resources can be operational; a blanket link replacement can retarget an old judgment; cleanup can affect selectors or bundled resources.
- Rollback/recovery: restore the affected source/owner/consumer slice together pending correction and reassessment. Preserve unrelated work, operational identities and historical records; do not migrate histories or revert a public version.

### M5. Retire the redundant validation alias and correct detached-fixture setup

- Milestone kind: implementation.
- Engineering purpose: complete the user-requested stale-script disposition and restore the actual CI fixture path without changing publication behavior.
- Requirements: REL-SR-06/08/09/14/19/21/22; the Release Standalone command disposition and Compatibility/migration scenario; Test protective-value criteria.
- Architecture responsibility: canonical recorded-source validation remains in `validate-release.py`; standalone preparation, preflight and public closeout retain their distinct uses.
- Dependencies: M1–M4 and their recorded reviews; current independent Design approval of the bounded alias retirement and Delivery approval of this additional allocation. Earlier final assessments preserve their original basis; renewed final review and Verify follow this refinement.
- Implementation scope: remove only `scripts/validate-release-ci.py` and its exclusive wrapper-delegation test. Preserve actual canonical recorded-source validation and all distinct negative/integrity protection. Keep deleted-path selector recognition for deletion-aware proof, with an explicit explanation that it grants no command support. Fix the release candidate integration fixture to establish its `main` branch from a detached checkout, matching the hosted PR environment. Do not change production authorization, versioning, generated evidence or workflow permissions.
- Files/components likely touched: `scripts/validate-release-ci.py`, `scripts/test-adapter-distribution.py`, `scripts/validation_selection.py`, `scripts/release_candidate_tests.py`. No other script retirement is selected. Historical commands/evidence retain original meaning; current model disposition supplies the replacement command.
- Required verification: TG-09 — canonical recorded-source validation still checks the recorded commit and rejects invalid metadata/resources after alias removal; the real candidate/CLI proof starts from detached Git state and reaches the same protected full validation and public-service-substituted recovery outcomes. Existing retained standalone functions/CLIs continue to pass their release regression tests.
- Evidence expectations: preserve the exact hosted failure and a local failing-before detached-branch reproduction; execute the corrected actual fixture, not a success stub. Explain removal of the delegation-only test using adjacent retained canonical and negative cases. Observe changed-path selection including the deleted script. The new final engineering range must rebuild candidate proof because script inventory and tests changed.
- Implementation steps: reproduce detached setup; strengthen the existing integration fixture to select that input and correct its branch creation; remove the alias and exclusive test; inspect remaining callers and selector behavior; run focused and full selected proof on a committed snapshot containing the deletion.
- Validation commands: `python scripts/test-adapter-distribution.py`; `python scripts/test-release-transaction.py`; `python scripts/test-select-validation.py`; the existing final PR-range `bash scripts/ci.sh --mode pr --base "$release_change_base" --head "$release_change_head"`, with inspected immutable revisions. The full selected run may supply these suites without repeating them separately. Model/prose/record and diff checks cover the changed governance surfaces. Observe replacement hosted PR CI after the authorized push; no live release is required.
- Expected observable result: one canonical recorded-source command, no redundant executable alias, retained protective checks and a portable actual release fixture in local and hosted PR checkouts.
- Completion criteria: TG-09 and affected TG-FINAL-01 proof pass, exact caller/test removal is independently assessed, and the observed CI failure has a supported correction. No stale prior final pass establishes new readiness.
- Required evidence: removal/caller disposition, before/after detached behavior, actual selected commands/results and hosted outcome with exact head identity.
- Review handoff: independent M5 Code Review, then fresh final whole-change Code Review and distinct Verify. Hosted CI observation supplements local proof after the PR update.
- Optional commit boundary: `M5: retire redundant release validator and fix detached fixture`.
- Risks and recovery: retiring shared functionality instead of the wrapper would weaken historical validation; preserve the canonical implementation/tests. Restore the bounded alias/test/selector slice if its claimed equivalence fails. Branch creation is restricted to temporary test repositories; no real branch or publication is replaced.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-milestone interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment and concern dispositions.
- Successor: final Verify; corrections return to their owner and require affected reassessment.

This checkpoint applies the selected review policy. A verification-group non-applicability rationale does not waive it. Final Verify separately assesses the current Proposal/Design/Delivery, all milestone and integrated evidence, current findings, source dispositions and required CI evidence. Neither stage authorizes an external release, push or PR.

## Change-level verification

### TG-FINAL-01. One approved candidate through current consumers to truthful closeout

- Covers: REL-SR-01–24, scoped SYS-SR-02/04/06/07/08/09, DES-SR-13/18/19/21 and R7/R8 across M1–M5.
- Demonstrate: reviewed inputs automatically yield archives, bundled metadata/index, packed npm and immutable approval basis; the real coordinator publishes those exact outputs under one substituted approval, observes public identity and fresh smoke, persists a truthful report, and its current readers work after the selected source removals. Changes after approval, preapproval failure, lost/duplicate external response, failed public verification, diagnostic loss and reporting recovery have their required outcomes. No old tag path bypasses authority and no helper-generated pass replaces an observation.
- Evidence expectations: M3 first supplies complete-path proof using real protected validation around substituted external services and local Git evidence persistence. M4/final assessment explicitly checks its applicability against final subjects, dependencies and current guidance. Rerun affected integrated proof when invalidated; preserve valid unchanged observations without mandatory blind repetition. Supplement with semantic source-transfer assessment and final selected CI results.
- Non-applicability: none for the complete-path and ownership claims. Isolated helper passes cannot establish the outcome. Real hosted publication and environment configuration are not required fixtures and cannot be inferred from them.

## Validation plan

The following commands are allocations for implementation and final verification, not claims already executed by plan authorship. Concrete new fixtures/assertions remain implementation-owned. Extend existing entrypoints/discovery to include the new required groups; require nonzero discovered cases for each intended group, and preserve failure exit status. No new permanent test catalogue is selected.

| Command / proof | Scope and purpose |
| --- | --- |
| `python scripts/test-release-transaction.py` | TG-01–06: extend existing suite to cover the actual candidate/executor/full-path boundaries, timing amendment, compatibility and failure behavior. Re-run after relevant milestone changes; preserve valid unchanged observations at final assessment. |
| `python scripts/test-npm-package-publication.py` | Changed package/publication contract and content proof; its existing version-specific checks are not proof that a new candidate is packed correctly. TG-02/06 also inspect the actual candidate tarball. |
| `python scripts/test-adapter-distribution.py` | Required when shared archive/metadata/installer-consumption helpers or fixtures change. Retain all-target negative and integrity protection; avoid inventory-wide improvement. |
| `bash -n scripts/release-verify.sh scripts/ci.sh` | Syntax only for changed shell composition; cannot prove workflow authority or actual invocation parity. |
| `bash scripts/ci.sh --mode explicit --path scripts/release_transaction.py --path scripts/release-verify.sh --path scripts/validate-release.py --path .github/workflows/release.yml` | M3 direct selected-check wrapper basis. Include every additional actual changed behavior-bearing path via repeated `--path` or use the final PR range. Inspect selection and execute any required TG not included by the selector; do not equate selection with proof sufficiency. |
| `python scripts/validate-boundary-first.py --path docs/design/release/release.md --path docs/design/system/system.md --path docs/design/design/design.md --path specs/published-skill-first-repository-simplification.md` | Model and scoped-source structure/references, not semantic transfer or runtime correctness. |
| `python scripts/validate-documentation-prose.py --mode enforce --path docs/design/release/release.md --path docs/plans/2026-09-09-release-model-source-consolidation.md` | New/changed owned prose. Inspect baseline-only issues in retained legacy files without unrelated cleanup. |
| `python scripts/validate-markdown-readability.py docs/plans/2026-09-09-release-model-source-consolidation.md docs/design/release/release.md docs/releases/README.md` | Readability and generated-region mistakes; warnings are reported, not a semantic or numeric savings gate. |
| `node scripts/validate-record-store.mjs docs/changes/2026-09-09-release-model-source-consolidation/change.json` and `git diff --check` | Exact record structure/references and patch whitespace; neither derives readiness. |
| `bash scripts/ci.sh --mode pr --base "$release_change_base" --head "$release_change_head"` | Final repository-required selected checks on the actual complete engineering range. Set both variables to inspected immutable commit IDs; include uncommitted changes through explicit selection before relying on range-only evidence. Record actual selected commands, scope and failures. |

For a temporary prepared candidate, use the existing builders and validators with resolved candidate inputs. The concrete shell pattern below uses an isolated candidate checkout/overlay and a temporary output root, never the maintainer's real release destination. `release_candidate_tag` is derived from the test profile; v0.5.1 is the inspected current development candidate, not a promised supported public release. The harness resolves and records exact C, overlay, tarball and output paths; variables are not a substitute for captured command arguments.

```bash
python scripts/build-adapters.py --version "$release_candidate_tag" --output-dir "$release_candidate_output"
python scripts/validate-adapters.py --version "$release_candidate_tag" --adapter-root "$release_candidate_output" --clean-install-smoke
npm pack "$release_candidate_package_root" --pack-destination "$release_candidate_output"
python scripts/validate-npm-package.py --package-root "$release_candidate_package_root" --tarball "$release_candidate_tarball"
python scripts/validate-release.py --version "$release_candidate_tag" --release-output-dir "$release_candidate_output" --release-commit "$release_candidate_commit"
```

Run the declared archive-to-bundled-metadata/index generation between archive validation and `npm pack`, through its existing owning builder adapted for actual C and archive bytes. The source-only `_prepare_local_cli_release_candidate` fixture with placeholder publication facts is not the production approval candidate. The test harness must run real packed-install proof against the resulting tarball and local archive/public-service substitutes. `release-verify.sh` and hosted checks must consume this exact candidate basis; if the baseline full verifier regenerates inputs, adapt it to validate the sealed outputs without substituting a new candidate. The successful composed fixture executes the actual full command set; production network/publication adapters are replaced only at their external-service boundaries. Do not simply call `bash scripts/release-verify.sh v0.5.1` in the development checkout and treat an unsupported tag or missing record as the selected proof.

When canonical or package inputs change, inspect whether current candidate metadata and its dependent assertions are affected. Regenerate affected current projections with the existing owning builder and run direct consumer checks, or record an inspected unaffected disposition before the owning milestone closes. Never invent hashes, preserve stale current identities or rewrite historical release metadata. A source-only cleanup needs semantic/reference/reader proof; it does not automatically repeat every package suite. Broad smoke remains required where the actual existing selector/governing contract requires it, with affected-scope evidence rather than historical command repetition.

Independent reviews judge semantic preservation and sufficient protection. Fixture tests cannot prove remote protection is configured, a registry accepted a release or hosted CI passed. Setup validation is exercised deterministically, and any actual read-only hosted inspection is reported separately with its limits. No remote configuration write or real publication is required for engineering completion.

## Risks and recovery

- Approval without stable bytes can authorize a different package. Restore candidate binding and deny execution until it is rechecked; changed material subjects need new approval.
- Shared validators can accidentally turn nonblocking timing into required work again, or demote missing event facts with it. Restore required safety checks and amend only the reviewed telemetry consequence with regression proof.
- Partial external success must survive rollback of code or evidence generation. Preserve identity/outcome records, inspect public state and use separately authorized recovery; never blindly republish or overwrite.
- Source cleanup can break an operational baseline or invalidate evidence reliance. Restore/reconcile the exact owner/consumer slice and obtain the responsible assessment; retain narrowly necessary original evidence if its current use cannot yet be resolved.
- Unavailable platform setup must fail closed. Deliver and verify setup detection and explicit guidance; do not replace missing authorization with an unprotected route or claim hosted activation.

## Dependencies

M1 → M2 → M3 → M4 → M5 is the engineering order, with independent milestone assessment and required corrections between slices. Add no new model to satisfy it. Shared package/installation behavior remains with its existing owners; an inseparable new requirement returns to Design before implementation.

Fresh final whole-change Code Review follows all implementation and required corrections; distinct Verify follows that review. The primary-plan work entries are initialized once only after current independent Delivery approval, through the plan-owned governed operation. Route owns subsequent activity/work transitions. No implementation work may be hidden as lifecycle-closeout or left only in chat.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-09 | Separate candidate construction, safe execution, CI composition and source retirement. | Each boundary has an independently reviewable safe predecessor; deletion waits for working current consumers. | One large automation-and-deletion commit; source retirement before implementation. |
| 2026-09-09 | Prove the full path using real validators and substituted external services, then assess reuse after cleanup. | Establish the one-approval outcome without publishing or repeating unrelated historical experiments. | Helper-only success; success stubs for protected validators; real publication as mandatory engineering proof. |
| 2026-09-09 | Keep remote setup and actual publication as explicit deployment prerequisites outside engineering execution. | Approved Design selects the capability and fail-closed setup contract, not remote administration authority. | Claiming a workflow file configures protection; leaving an unguarded fallback. |

The M5 refinement adds the inspected redundant-alias retirement and detached-checkout proof after the initial four-milestone delivery. Earlier milestone and final judgments retain their original subjects; current progression is governed by renewed assessments in the owning change.

## Readiness

- See the owning change record for current workflow state.
