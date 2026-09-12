# RigorLoop Canonical System Architecture

Current product composition and three-parent ownership are defined by [System](../../design/system.md). The former combined Distribution contract is split into [Engineering Packaging](../../design/engineering/packaging.md) and [CLI Installation](../../design/cli/installation.md); references below to its earlier combination retain their source-qualified historical scope. This notice does not transfer unmapped legacy obligations.


## Bounded Design and System replacement

[System](../../design/system.md#exact-mixed-architecture-migration-boundary) identifies the exact selected composition sections transferred here; [Design](../../design/skill/authoring/design.md#selected-replacement-map) owns the reconciled authoring method and decision mapping. This coordinated replacement covers only those selected paragraphs, bullets, tables and method decisions. Unselected Level 2, installation, distribution, validation and other responsibilities below retain their existing owners and amendments. Historical diagrams and approvals remain historical evidence; this mixed file is not wholly superseded.

[Release](../../design/engineering/release.md) contains the selected current release contract and exact source-disposition map. Its owning change records coordinated adoption through successful final Verify; the retained adapter and publication histories below preserve their original boundaries.

## Distribution replacement boundary

[Engineering Packaging](../../design/engineering/packaging.md) and [CLI Installation](../../design/cli/installation.md) receive the mapped generation and installation responsibilities respectively, including the five retired specification families and five ADRs. The preserved [source map](../../design/engineering/packaging.md#source-displacement-and-preservation) preserves original decisions and identifies superseded behavior. The [owning change](../../changes/2026-09-10-distribution-model-and-opencode-retirement/change.json) establishes adoption through reviewed implementation and successful Verify. Remaining named-version goals, quality scenarios, risks, glossary entries and Follow-on artifacts about three targets, local mirrors, state writing or managed replacement retain historical meaning only; current installation has two targets, destination conflicts and explicit `--force`, with no state interpretation or automatic upgrade. Unrelated architecture remains with its existing owner.

## V2-only runtime retirement

The [Record Format](../../design/cli/records.md), [CLI](../../design/cli/cli.md) and [Workflow](../../design/skill/workflow.md) models select `rigorloop-records-v2` as the only supported runtime stored format. Earlier compact/lifecycle and explicit-recording-v1 acceptance, activation, projection, mutation and recovery clauses below are historical design evidence, not current execution or compatibility obligations. Their stable IDs and recorded approvals keep their original meaning. Current consumers use scoped primary reads and targeted recording, with actor-owned decisions and applicability; the CLI does not select readiness. Preserve archival records unchanged, reject explicit retired input safely and preserve v2 safety. Unrelated document/configuration/transport version domains remain supported under their own contracts.

Specialist authoring and review responsibilities remain. Each governed change requires fresh independent whole-change Code Review after all implementation milestones and corrections, then distinct successful final Verify. Installed skills must contain usable v2 procedures and selective portable resources, without private internal requirement IDs or a dependency on this design repository.

## Selected unified Validation replacement

The [Validation model](../../design/engineering/validation.md#source-disposition-and-decision-preservation), selected by its [owning change](../../changes/2026-09-12-unified-validation-model/change.json), replaces only the exact validation execution/cache descriptions named in its source map at reviewed coherent implementation and successful Verify. This new-profile-only amendment preserves the mixed architecture's other responsibilities and the original historical evidence. The runtime cache, historical broad-smoke classification reader and duplicated scheduling implementation remain implementation cleanup targets; their existence does not require a separate current Test Design. Current product invariants, recording safety, release/publication and package generation keep their declared owners; this is not a whole-file retirement.

## Test criteria ownership

For this repository's explicitly adopted model work, [Validation](../../design/engineering/validation.md) preserves the adopted shared derivation, protective-value and maintenance criteria (TEST-SR-01–13) formerly owned by Test. The Test document is removed as a Design-stage consolidation; new VAL-SR execution behavior remains subject to independent review, implementation and successful Verify under the unified Validation change. Specialist reviewers and Verify judge actual plans, tests and evidence; Review and Closeout retains assessment authority policy, applicability and closeout consequences. Workflow retains coordination. Canonical consumers apply the criteria through selective quality and maintenance resources; those resources are application guidance, not another policy owner. This initiative's coordinated consumer adoption preserves historical contracts, required negative/regression proof and separately owned execution permissions. Installation does not adopt customer policy. Internal requirement mappings and package mechanics remain in contributor/governance surfaces rather than published skills.

Record Format profile boundary: for explicitly adopted model-driven work, [Workflow](../../design/skill/workflow.md) owns actor decisions, [Record Format](../../design/cli/records.md) owns v2 JSON records, and [CLI](../../design/cli/cli.md) owns bounded reads, targeted construction and shared recoverable persistence. New primary creation explicitly selects v2; existing contracts are not migrated. The lifecycle/compact eligibility architecture below remains historical-contract scope and is not called before recording a correction. Installation or a local adoption candidate does not authorize customer/release activation.

Current route amendment: `route` is the sole public semantic workflow router, `rigorloop workflow-context` supplies deterministic project-local facts, and `docs/workflows.md` and the former public `workflow` package have no current authority. Stable `stage_authority: workflow` and `workflow.automation` identifiers remain protocol state, not public skill names.

Historical compact current-state amendment (not executable): `compact-current-state-v1` replaces history-oriented active records prospectively after coherent activation. The authoritative set is `change.yaml`, stable current review records, conditional `material-decisions.md`, conditional `evidence.yaml`, and success-only `verify-report.md`, coordinated by one recoverable multi-file transaction boundary. The CLI derives eligibility and validates semantic operations; it is not a permission principal. Bounded projections identify current state and exact required paths. Correctness, recovery, review, resumption, and successful Verify work without Git history, without PR access, without network access, and without machine-local logs. Registered non-compact changes retain their contract and are never inferred or migrated from file shape. Compact writer authority remains withheld until package and supported-adapter parity is proven.

## Review and Closeout ownership

For explicitly adopted model work, [Review and Closeout](../../design/skill/assessment.md) owns shared assessment and final-closeout policy within Workflow (RC-SR-01–18). Workflow retains coordination; Record Format and CLI retain representation and mechanics. This change adopts that ownership for this repository's explicitly selected initiative; installation and distribution do not activate customer projects. The model's clause-level map identifies replacement ownership, while historical contracts and their stable IDs, judgments and stored procedures below retain their exact meaning. Specialized skills apply the owner through selectively packaged guidance; they do not define competing policy. Existing separately authorized release, PR, publication and destructive-action boundaries remain in force.

## Owning change record

`docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`

## Related artifacts

- Current generation contract and retired-source decisions: [Packaging](../../design/engineering/packaging.md); executable acquisition and destination writes: [Installation](../../design/cli/installation.md).

- Proposal: `docs/proposals/2026-04-28-architecture-skills-c4-arc42-adr.md`
- Proposal refinement: `docs/proposals/2026-04-29-c4-arc42-package-quality.md`
- Spec: `specs/architecture-package-method.md`
- Test spec: `specs/architecture-package-method.test.md`
- Legacy normalization plan: `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
- Method ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Method amendment ADR: `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`
- Change-local architecture delta: `docs/changes/2026-04-28-architecture-skills-c4-arc42-adr/architecture.md`
- Package-quality architecture delta: `docs/changes/2026-04-29-c4-arc42-package-quality/architecture.md`
- Legacy normalization delta: `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
- Architecture skill surface simplification proposal: `docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md`
- Workflow governance update: `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Workflow governance change metadata: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
- Release Token-Friendliness benchmark proposal: `docs/proposals/2026-05-10-release-token-friendliness-benchmark-for-skills.md`
- Release Token-Friendliness benchmark spec: `specs/release-token-friendliness-benchmark-for-skills.md`
- Release Token-Friendliness benchmark change metadata: `docs/changes/2026-05-10-release-token-friendliness-benchmark-for-skills/change.yaml`
- Expanded dynamic Token-Friendliness benchmark proposal: `docs/proposals/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Expanded dynamic Token-Friendliness benchmark spec: `specs/expand-dynamic-token-friendliness-benchmarks-for-core-skills.md`
- Expanded dynamic Token-Friendliness benchmark change metadata: `docs/changes/2026-05-11-expand-dynamic-token-friendliness-benchmarks-for-core-skills/change.yaml`
- Single Authored Skill Source proposal: `docs/proposals/2026-05-12-single-authored-skill-source-and-generated-adapter-output-cleanup.md`
- Single Authored Skill Source spec: `specs/single-authored-skill-source-generated-output.md`
- Generated output migration ADR: `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`
- Publish Next Release transition proposal: `docs/proposals/2026-05-12-publish-next-release-with-single-authored-skill-source.md`
- Publish Next Release transition spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Publish Next Release transition change metadata: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
- Public Adapter Artifact Migration proposal: `docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`
- Public Adapter Artifact Migration spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`
- Public Adapter Artifact Migration change metadata: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/change.yaml`
- Stop Tracking Generated Public Adapter Skill Bodies proposal: `docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
- Stop Tracking Generated Public Adapter Skill Bodies change metadata: `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/change.yaml`
- RigorLoop Scaffolding CLI proposal: `docs/proposals/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow.md`
- RigorLoop CLI Package and Codex Init spec: `specs/rigorloop-cli-package-and-codex-init.md`
- RigorLoop CLI Package and Codex Init ADR: `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`
- RigorLoop CLI Package and Codex Init change metadata: `docs/changes/2026-05-15-rigorloop-scaffolding-cli-and-machine-readable-workflow/change.yaml`
- RigorLoop CLI Lockfile change metadata: `docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`
- RigorLoop CLI New Change spec: `specs/rigorloop-cli-new-change.md`
- RigorLoop CLI New Change change metadata: `docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`
- RigorLoop npm Publication proposal: `docs/proposals/2026-05-16-first-public-npm-release.md`
- RigorLoop npm Publication spec: `specs/rigorloop-npm-publication.md`
- RigorLoop npm Publication ADR: `docs/adr/ADR-20260516-rigorloop-npm-publication.md`
- RigorLoop npm Publication change metadata: `docs/changes/2026-05-16-first-public-npm-release/change.yaml`
- Multi-Adapter Init and Proxy-Aware Adapter Download proposal: `docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- Multi-Adapter Init and Proxy-Aware Adapter Download change metadata: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- Script Output Optimization proposal: `docs/proposals/2026-05-21-script-output-optimization.md`
- Script Output Optimization spec: `specs/script-output-optimization.md`
- Change-Record Catalog Registration and Bounded Read Model proposal: `docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`
- Change-Record Catalog Registration and Bounded Read Model spec: `specs/change-record-catalog-registration-and-bounded-read-model.md`
- Change-Record Catalog Registration and Bounded Read Model ADR: `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`
- Change-Record Catalog Registration and Bounded Read Model change metadata: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`
- Validation Idempotency and Cache-Hit Safety proposal: `docs/proposals/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later.md`
- Validation Idempotency and Cache-Hit Safety spec: `specs/validation-idempotency-and-cache-hit-safety.md`
- Validation Idempotency and Cache-Hit Safety ADR: `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`
- Validation Idempotency and Cache-Hit Safety change metadata: `docs/changes/2026-05-23-validation-idempotency-first-conservative-edit-scoped-validation-later/change.yaml`
- Cache-Aware Inner-Loop Lifecycle Validation Helper proposal: `docs/proposals/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper.md`
- Cache-Aware Inner-Loop Lifecycle Validation Helper change metadata: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/change.yaml`
- Release Process Contract proposal: `docs/proposals/2026-05-23-release-process-contract.md`
- Release Process Contract change metadata: `docs/changes/2026-05-23-release-process-contract/change.yaml`
- Target-Native Init proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- Target-Native Init change metadata: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`
- Published Skill Resource Integrity proposal: `docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md`
- Published Skill Resource Integrity spec amendment: `specs/skill-contract.md` R46-R55
- Published Skill Resource Integrity spec-review: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/spec-review-r1.md`
- Published Skill Resource Integrity ADR: `docs/adr/ADR-20260623-published-skill-resource-integrity.md`
- Portable Boundary-First Capability proposal: `docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md`
- Boundary-First Proof Model spec: `specs/boundary-first-proof-model.md`
- Portable Boundary Reference Projection and Activation ADR: `docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md`
- Portable Boundary Release Manifest and Package Rollback ADR: `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md`
- Progressive Boundary-First Skill Guidance proposal: `docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Progressive Boundary-First Skill Guidance spec: `specs/progressive-boundary-first-skill-guidance.md`
- Progressive Boundary Guidance Resources ADR: `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Progressive Boundary-First Skill Guidance change metadata: `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/change.yaml`
- Superseded Boundary-First v1 Activation Release spec: `specs/boundary-first-v1-v0-3-7-activation-release.md`
- Superseded Boundary-First Activation Candidate and Atomic Publication ADR: `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`
- Historical Boundary-First v1 Activation Release change metadata: `docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/change.yaml`
- Usability-First Boundary-First v0.4.0 Release proposal: `docs/proposals/2026-08-06-usability-first-boundary-release.md`
- Usability-First Boundary-First v0.4.0 Release spec: `specs/usability-first-boundary-release.md`
- Checked-Revision Boundary Activation and Routine Release ADR: `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`
- Usability-First Boundary-First v0.4.0 Release change metadata: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
- Evidence-Bound and Incremental `project-map` proposal: `docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md`
- Evidence-Bound and Incremental `project-map` spec: `specs/project-map.md`
- Evidence-Bound and Incremental `project-map` proposal-review: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/proposal-review-r1.md`
- Evidence-Bound and Incremental `project-map` spec-review: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/spec-review-r1.md`
- Evidence-Bound and Incremental `project-map` change metadata: `docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml`
- Project-Map Skill Simplification proposal: `docs/proposals/2026-08-14-project-map-skill-simplification.md`
- Project-Map Skill Simplification spec amendment: `specs/project-map.md`
- Project-Map Skill Simplification spec-review: `docs/changes/2026-08-14-project-map-skill-simplification/reviews/spec-review-r1.md`
- Project-Map Skill Simplification change metadata: `docs/changes/2026-08-14-project-map-skill-simplification/change.yaml`
- Workflow-State Projection and Pre-Transition Synchronization Gate proposal: `docs/proposals/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate.md`
- Workflow-State Projection and Pre-Transition Synchronization Gate spec amendment: `specs/single-source-of-workflow-state.md`
- Workflow-State Projection and Pre-Transition Synchronization Gate spec-review: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/reviews/spec-review-r2.md`
- Workflow-State Projection and Pre-Transition Synchronization Gate change metadata: `docs/changes/2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate/change.yaml`
- Proposal-Gated Authoring Autoprogression proposal: `docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
- Proposal-Gated Authoring Autoprogression spec amendments: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`
- Proposal-Gated Authoring Autoprogression spec-review: `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/spec-review-r2.md`
- Proposal-Gated Authoring Autoprogression ADR: `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`
- Proposal-Gated Authoring Autoprogression change metadata: `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Implementation Autoprogression proposal: `docs/proposals/2026-06-24-separately-armed-implementation-autoprogression-through-verify.md`
- Implementation Autoprogression spec amendments: `specs/workflow-stage-autoprogression.md`, `specs/rigorloop-workflow.md`, `specs/review-finding-resolution-contract.md`
- Implementation Autoprogression spec-review: `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/reviews/spec-review-r1.md`
- Implementation Autoprogression ADR: `docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md`
- Implementation Autoprogression change metadata: `docs/changes/2026-06-24-separately-armed-implementation-autoprogression-through-verify/change.yaml`
- Independent Adversarial Review Gates proposal: `docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md`
- Review Independence and Criticality spec: `specs/review-independence-and-criticality.md`
- Independent Adversarial Review Gates spec-review: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/spec-review-r2.md`
- Independent Adversarial Review Gates ADR: `docs/adr/ADR-20260625-independent-adversarial-review-gates.md`
- Independent Adversarial Review Gates change metadata: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Requirement-Fidelity Gate proposal: `docs/proposals/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md`
- Requirement-Fidelity Gate spec: `specs/requirement-fidelity-gate.md`
- Requirement-Fidelity Gate spec-review: `docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/spec-review-r2.md`
- Requirement-Fidelity Gate ADR: `docs/adr/ADR-20260626-requirement-fidelity-gate.md`
- Requirement-Fidelity Gate change metadata: `docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/change.yaml`
- Release Transaction Automation proposal: `docs/proposals/2026-06-29-release-transaction-automation.md`
- Release Transaction Automation change metadata: `docs/changes/2026-06-29-release-transaction-automation/change.yaml`
- Bounded Review-Fix Autoprogression proposal: `docs/proposals/2026-06-30-bounded-review-fix-autoprogression-in-chat.md`
- Bounded Review-Fix Autoprogression spec: `specs/review-fix-autoprogression.md`
- Bounded Review-Fix Autoprogression spec-review: `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/reviews/spec-review-r2.md`
- Bounded Review-Fix Autoprogression ADR: `docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md`
- Bounded Review-Fix Autoprogression change metadata: `docs/changes/2026-06-30-bounded-review-fix-autoprogression-in-chat/change.yaml`
- Single Bounded Review-Fix Workflow Automation proposal: `docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md`
- Single Bounded Review-Fix Workflow Automation spec: `specs/single-bounded-review-fix-workflow-automation.md`
- Single Bounded Review-Fix Workflow Automation spec-review: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/spec-review-r5.md`
- Single Bounded Review-Fix Workflow Automation ADR: `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md`
- Single Bounded Review-Fix Workflow Automation change metadata: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/change.yaml`
- Stage-Owned Lifecycle Artifacts proposal: `docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md`
- Stage-Owned Lifecycle Artifacts spec: `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
- Stage-Owned Lifecycle Artifacts spec-review: `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/spec-review-r6.md`
- Stage-Owned Lifecycle Artifacts ADR: `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`
- Stage-Owned Lifecycle Artifacts change metadata: `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml`
- Record Every Formal Review proposal: `docs/proposals/2026-05-12-record-every-formal-review.md`
- Formal Review Recording spec: `specs/formal-review-recording.md`
- Record Every Formal Review change metadata: `docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml`
- C4 system context diagram: `diagrams/context.mmd`
- C4 container diagram: `diagrams/container.mmd`
- Published-Skill-First Repository Simplification proposal: `docs/proposals/2026-08-10-published-skill-first-repository-simplification.md`
- Published-Skill-First Repository Simplification spec: `specs/published-skill-first-repository-simplification.md`
- Validation responsibility and source dispositions: [System](../../design/system.md#necessary-design-consolidation-map); local contracts remain at their named owners.
- Necessary-source retention and scoped proof: [Design](../../design/skill/authoring/design.md#necessary-design-retention) and [Validation](../../design/engineering/validation.md#proof-quality-maintenance-and-evidence).
- Code-Review Skill Simplification proposal: `docs/proposals/2026-08-10-code-review-skill-simplification.md`
- Code-Review Skill Simplification spec: `specs/code-review-skill-simplification.md`
- Code-Review Skill Simplification change metadata: `docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`
- Workflow Skill Simplification proposal: `docs/proposals/2026-08-11-workflow-skill-simplification.md`
- Workflow Skill Simplification spec: `specs/workflow-skill-simplification.md`
- Workflow Skill Simplification change metadata: `docs/changes/2026-08-11-workflow-skill-simplification/change.yaml`

- Governed Lifecycle CLI proposal: `docs/proposals/2026-08-24-governed-lifecycle-cli.md`
- Governed Lifecycle CLI spec: `specs/governed-lifecycle-cli.md`
- Governed Lifecycle CLI ADR: `docs/adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md`
- Governed Lifecycle CLI change metadata: `docs/changes/2026-08-24-governed-lifecycle-cli/change.yaml`
- Compact Current-State proposal: `docs/proposals/2026-09-03-compact-current-state-change-record.md`
- Compact Current-State specification: `specs/compact-current-state-change-record.md`
- Compact Current-State architecture: `docs/architecture/2026-09-03-compact-current-state-change-record.md`
- Compact Current-State transaction ADR: `docs/adr/ADR-20260903-compact-current-state-transaction-boundary.md`

## Introduction and Goals

Current external boundaries, system responsibilities and composition goals are owned by [System](../../design/system.md). [Design](../../design/skill/authoring/design.md) owns the smallest justified living-model set, structural/runtime reasoning and embedded decision preservation.

Retained additional goals:

- preserve review, verification, and closeout evidence in repository artifacts;
- keep generated output reproducible from canonical sources;
- keep `skills/` as the only authored skill source while moving local and public generated skill copies out of ordinary authored Git state in staged releases;
- add a small CLI package boundary that scaffolds projects and installs verified Codex release archives without becoming a second source of truth;
- let the CLI record verified generated Codex adapter output in a downstream `rigorloop.lock` without making the lockfile canonical workflow, skill, schema, release, or adapter metadata;
- extend CLI adapter init through descriptors for Codex, Claude Code, and opencode while preserving Codex `.agents/skills`, strict release-archive verification, and local archive fallback;
- preserve schema-v1/v2 lockfile compatibility for mixed single-root and multi-root adapter state while current writes use target-oriented `rigorloop.lock` schema v3 without making downstream lockfiles canonical adapter metadata;
- retire public `--adapter` init syntax in favor of target-native `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode`;
- make default target-native init install-only while keeping explicit `--write-state` as the managed project-state path for target-oriented `rigorloop.yaml` and `rigorloop.lock` schemas;
- require release smoke for target-native init to use real non-dry-run packed-package and live-registry install paths rather than dry-run output alone;
- make published skill-local resource dependencies explicit, packageable, hash-verifiable, and present across canonical source, generated output, packed release candidates, and clean installed target trees;
- publish one portable boundary-first method through ten governed skills with
  an automatic four-question scan, one compact common core, two owner-scoped
  stage-family resources, artifact-sliced downstream reads, deterministic
  projections, checked-revision activation, and independent semantic review;
- make that method automatic and concise in all ten governed skills, prove
  activation from one coherent checked repository revision without Git
  history, tags, remote state, or network access, and publish `v0.4.0` through
  the existing routine release workflow;
- keep `project-map` as a current-state orientation reference with freshness metadata, cited material claims, visible inference, root/area registration, and downstream reliance boundaries;
- improve enterprise-network recovery through bounded proxy diagnostics while deferring programmatic proxy dispatcher support;
- let the CLI scaffold a draft change-local artifact pack for `docs/changes/<change-id>/change.yaml` without claiming lifecycle stage completion or creating durable-looking placeholder artifacts;
- publish the first public `@xiongxianfei/rigorloop` npm package only through a reviewable release-hardening boundary that preserves npm as delivery, not source of truth;
- make public release skill token-friendliness measurable through release reports, structured metadata, and fixture-backed runtime benchmarks;
- make dynamic token-friendliness coverage visible across the core delivery workflow without requiring every optional skill benchmark for every release;
- keep repository script output proportional to actionability: compact on success, specific on failure, and expandable through explicit verbose modes;
- treat change records as queried catalogs with registered deterministic evidence classes, selector routing, and bounded read paths for common stage-owned questions;
- reduce repeated validation work only through unchanged-input cache hits that preserve validator behavior and closeout actual-run gates, and make the safe inner-loop cached path easy through a named lifecycle validator helper mode;
- define the release process once as a standing contract, then execute routine publishes as operations with durable release evidence;
- make routine releases profile-driven typed transactions whose generated surfaces, cheap preflight, public evidence closeout, and timing evidence preserve the full release gate while reducing duplicated version state;
- keep first adoption and package-quality refinement review-based until real package usage proves which checks are worth automating.
- keep governed artifacts stable while `change.yaml` owns mutable artifact
  lifecycle, milestone, review, blocker, next-stage, and closeout state;
- use one target-driven `bounded-review-fix` automation mechanism whose target
  is sufficient repository-local continuation consent, while every stage keeps
  a fixed write boundary and external actions remain prohibited;
- make workflow-managed automated reviews structurally independent and adversarial through fresh review contexts, neutral initial packets, blind-first risk formation, staged evidence release, risk-tiered escalation, clean-review sufficiency receipts, and calibration evidence.
- make applicable automated reviews spec-canonical by requiring deterministic requirement-fidelity applicability, requirement-property decomposition, property-by-surface matrices, validator assertion comparison against the spec, and compression-defect calibration.
- make canonical skills and packaged resources the primary product boundary, compose deterministic adapter and release proof through three stable gates, keep semantic skill quality in review, and retire validation orchestration only through failure-preserving slices.

## Architecture Constraints

- [Design](../../design/skill/authoring/design.md) owns model layout, technical reasoning, decisions and scoped legacy authoring; [Workflow](../../design/skill/workflow.md) coordinates the handoff. Contributor scaffolds remain under `templates/`; required portable legacy aids are packaged inside `design`. Historical deltas cannot compete with a migrated current owner.
- `CONSTITUTION.md` is the highest-priority repository governance artifact below external runtime instructions.
- `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`
  owns governed artifact-state placement, transition authority, workflow
  routing state, planned-work state, automation-target semantics, and
  prospective migration.
- `skills/` is the only authored skill source.
- `.codex/skills/` is ignored local Codex runtime state and must not be hand-edited, required as tracked Git state, or treated as release evidence after its migration slice.
- Public adapter skill copies under `dist/adapters/**/skills` are generated adapter output and remain tracked only until the release-artifact compatibility window is satisfied.
- `dist/adapters/manifest.yaml`, `dist/adapters/README.md`, and `docs/reports/adapter-artifacts/releases/<version>.yaml` are tracked support and release evidence surfaces; generated adapter archives are release assets rather than committed repository files by default.
- The `v0.1.1` transition release validates canonical `skills/`, tracked public adapter output under `dist/adapters/`, release notes, adapter install guidance, and token-cost metadata; it does not build or validate `.codex/skills/` as release evidence.
- The `v0.1.2` archive-introduction release publishes per-adapter release archives for Codex, Claude Code, and opencode while keeping tracked public adapter skill bodies available for the stable compatibility window.
- The first public adapter untracking release occurs only after at least one stable release has shipped downloadable adapter archives and release-archive install documentation, unless an approved compatibility-window exception explicitly says otherwise.
- For `v0.1.3` and later, release archives are the active public adapter install surface. Generated adapter skill bodies, generated adapter instruction entrypoints, and generated opencode command wrappers are release or temporary output, not tracked package fragments under `dist/adapters/<adapter>/`.
- The first RigorLoop CLI package candidate is `@xiongxianfei/rigorloop` with one public binary, `rigorloop`.
- The completed first CLI slice was limited to help, version, and `init --adapter codex` with dry-run JSON, safe `rigorloop.yaml` generation, verified Codex adapter archive installation, and planned lockfile output only.
- The next CLI scaffolding slice adds `rigorloop new-change <change-id>` to create `docs/changes/<change-id>/change.yaml` only. It must not create `explain-change.md`, review artifacts, plans, specs, proposals, lockfiles, adapters, or any lifecycle artifact that would imply a later stage has completed.
- Change records under `docs/changes/<change-id>/` are queried catalogs, not append-only transcripts. Deterministic change-local evidence files require registered evidence-class routing or explicit registration debt.
- Evidence-class registry behavior belongs to the selector architecture. The first slice may centralize registry data when the selector supports it, or keep a selector-owned registry table with fixture-backed regression coverage.
- Bounded change-record reads belong to a new query-helper script rather than `validate-change-metadata.py`; validation remains proof work, while querying returns scoped metadata slices.
- Workstream A, evidence registration and selector routing, ships before Workstream B, bounded query helper and stage-skill guidance, so CI-routing risk and skill-behavior risk remain separately reviewable and rollbackable.
- Validation idempotency starts with the explicit-path lifecycle command family only: direct `validate-artifact-lifecycle.py --mode explicit-paths` and helper `validate-artifact-lifecycle.py --mode explicit-paths-inner-loop`.
- Direct `--mode explicit-paths` remains the actual-run command for closeout, verify, branch readiness, PR readiness, CI, and other first-slice final gates.
- `--mode explicit-paths-inner-loop` is a cache-aware inner-loop helper mode. It normalizes to canonical direct `--mode explicit-paths` argv for cache identity, prior passing event matching, and input-surface identity, while formal evidence records both displayed helper argv and canonical cache argv.
- Cache hits require a previous actual-run pass trace, identical canonical normalized command, identical input-surface hash, identical implementation manifest hash, and identical policy/config manifest hash.
- Validation cache execution state is untracked, branch-local, worktree-local, and change-local. It is not lifecycle evidence and must not be reused across branches, worktrees, machines, remote/shared caches, or CI jobs.
- Formal cache-hit evidence lives in `docs/changes/<change-id>/validation-cache-evidence.yaml`, while Workstream A measurement evidence lives in `docs/changes/<change-id>/validation-cache-measurement.yaml`.
- Helper cache-hit evidence is written or merged only when a safe change root or safe evidence path is supplied or inferable; local ad hoc helper use may print cache status without writing formal evidence.
- `cache-hit-inner-loop` evidence cannot satisfy stage or milestone closeout. First-slice closeout requires actual-run evidence, with primary rejection owned by `validate-artifact-lifecycle.py` and consistency checks owned by `validate-change-metadata.py`.
- Helper measurement keeps helper invocations, cache hits, cache misses, disabled evaluations, actual-run fallbacks, actual runs, and closeout actual runs distinct.
- Workstream B edit-scoped validation remains outside this architecture until Workstream A measurement is reviewed and a separate approved proposal or spec amendment authorizes it.
- The CLI package may contain CLI code, small scaffolds, and bundled official adapter metadata for the package's compatible Codex adapter release. It must not contain adapter archives as authored npm source or generated adapter skill bodies as canonical source.
- `rigorloop init --adapter codex --from-archive <path>` verifies local archives against bundled adapter metadata shipped with the installed CLI package version and does not require a separate user metadata path in the first slice.
- `rigorloop init` may write durable `rigorloop.lock` only for the approved Codex lockfile-writing surface after archive verification, extraction safety checks, generated-output mutation, installed-tree verification, and lockfile shape validation have succeeded.
- `rigorloop.lock` records verified generated Codex adapter output state in a downstream project. It is not canonical workflow content, canonical skill content, release metadata, adapter metadata, or validation authority.
- The first lockfile schema is strict: unknown top-level sections, unknown fields, unsupported schemas, unsupported adapters, unsupported source values, and unsupported tree hash algorithms block before mutation.
- The multi-adapter init slice extends the existing CLI package boundary to `init --adapter codex`, `init --adapter claude`, and `init --adapter opencode` through explicit adapter descriptors.
- Codex remains a single-root `.agents/skills` adapter; the CLI must not migrate Codex output to `.codex/skills`.
- Claude Code is a single-root `.claude/skills` adapter. opencode is a possible multi-root adapter with `.opencode/skills` and `.opencode/commands`.
- Trusted CLI-bundled metadata determines required opencode roots. Older compatible opencode archives without `command_aliases.opencode` may install skills only with warning code `opencode-command-aliases-not-declared`.
- Multi-adapter lockfiles use `schema_version: 2`; existing schema v1 Codex lockfiles remain readable and may be upgraded only after drift checks pass.
- For `0.3.0`, the public init surface is target-native: `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode`. `--adapter` is removed and fails before mutation with migration guidance.
- Default target-native init is install-only: it installs verified target support and must not create, update, delete, rename, or reformat `rigorloop.yaml` or `rigorloop.lock`.
- Managed project state is explicit through `rigorloop init <target> --write-state`. New state files use target-oriented schemas: `rigorloop.yaml` schema v2 with top-level `targets`, and `rigorloop.lock` schema v3 with `generated.targets`.
- Existing state files are byte-preserved by default, but byte preservation does not prevent safety reads. When default init plans target-root mutation, existing state is parsed enough to detect selected-target drift, overlapping roots, or conflicting root mappings. Malformed or ambiguous state blocks non-dry-run mutation.
- Historical archive filename values and non-user-visible `dist/adapters/` implementation names may continue to use adapter naming until a separate internal/archive rename is approved.
- Target-native release readiness requires real non-dry-run packed-package smoke before publish and live registry/download smoke after publish for every supported target. Dry-run output is not release install-smoke proof.
- Published skills declare required skill-local resources through `Resource map` entries. Untransformed mapped resources preserve skill-root relative path plus raw-byte SHA-256 from canonical source through generated output, packed release candidates, and installed target trees.
- Progressive boundary guidance keeps the established
  `boundary-first-method-v1.md` path as the compact core, adds feature-authoring
  guidance only to `spec` and `spec-review`, and adds proof guidance only to
  `test-spec` and `test-spec-review`.
- `specs/boundary-first-resources.yaml` is the sole declarative resource and
  consumer inventory. Projection, validation, measurement, and activation
  interpret that manifest rather than owning parallel inventories.
- The four compact-scan questions are copied from one checked contributor
  shared block directly into governed skill text. Deeper resources are loaded
  only for the owning stage family or after an approved artifact slice proves
  insufficient.
- Resource-integrity migration starts in audit mode for existing published skills, but new or changed skills cannot introduce unmapped skill-local resource references or missing mapped resources.
- `templates/` is not an implicit packaged skill resource class. Legacy `templates/...` references are migration lint input until removed, mapped to `assets/` or `references/`, or explicitly excepted.
- The `project-map` skill describes current repository orientation only. Project maps are living references and do not override source code, runtime configuration, schemas, build manifests, tests, CI, or governing workflow artifacts.
- Root project maps use `docs/project-map.md` by default. Area maps use `docs/project-map/<area>.md` only for durable boundaries and require registration from the root map when any area map exists.
- Project maps record their own baseline, coverage, exclusions, known gaps, status, and parent-map relationship. Dirty Git baselines use `<sha>+dirty` and list inspected uncommitted paths.
- Material current-state claims in project maps cite repository paths, inferences are labeled, unknowns are recorded as open questions, configured commands are distinct from executed commands, and executed commands include exit codes.
- The `project-map` skeleton is a packaged skill-local asset at `skills/project-map/assets/project-map-skeleton.md`, declared with `COPY` in the skill `Resource map`, carried through generated adapter output, and validated by the existing published skill resource-integrity path.
- The `project-map` package uses independent `create`, `refresh`, or `audit` operation and repository or area scope axes. Universal evidence and target-state classification remain in `SKILL.md`; `references/map-maintenance-and-area-coordination.md` owns refresh, audit, root/area coordination, and recoverable multi-map procedure; the skeleton owns structure only.
- Simple uncoordinated root creation may omit the conditional reference only after the bounded known-surface coordination preflight. Every maintenance operation, audit, area scope, or coordinated root creation loads the conditional reference before dependent judgment or writes, and a missing required resource stops rather than triggering remembered reconstruction.
- Existing project maps are not automatically migrated by this change; they satisfy the revised contract only when intentionally refreshed or recreated.
- First-slice proxy behavior uses Node built-in env-proxy support only when the runtime supports and enables it. Programmatic Undici proxy dispatcher support is out of scope until a later approved change.
- Public npm publication of `@xiongxianfei/rigorloop@0.1.4` is allowed only through the approved npm publication slice: package-content allowlist, lifecycle-script and dependency policy, exactly one publication mode, publication evidence, packed-package smoke, and real Codex adapter install proof.
- Normal npm publication uses trusted publishing through `.github/workflows/release.yml`. One-time bootstrap publication may be used only for `@xiongxianfei/rigorloop@0.1.4` if trusted publishing cannot be configured before package creation, and it may publish only the exact verified tarball recorded in publication evidence.
- After the `v0.1.3` adapter untracking migration, the tracked default adapter support surface under `dist/adapters/` is limited to `README.md` and `manifest.yaml` unless a later approved spec explicitly names more tracked metadata or templates.
- `docs/releases/<version>/release.yaml` and `docs/releases/<version>/release-notes.md` are authored release evidence, not generated release-note substitutes.
- Routine publish operations execute the standing release-process contract and record durable version-scoped evidence under `docs/releases/v<version>.md`; related change records link to that evidence when applicable.
- Routine release evidence does not update `docs/plan.md` unless the release is part of an active lifecycle plan; `docs/releases/` and the release index own routine publish records.
- Release-process changes, new package names or scopes, new adapter targets, changed authentication/provenance policy, and changed publish mechanics remain normal lifecycle-managed work before any publish operation uses them.
- Emergency release deferrals are narrow owner-approved exceptions to release gate timing, not an alternate normal release path. Release evidence creation, secret suppression, source/package/version/dist-tag recording, publish-path recording, registry verification, and recovery/follow-up recording are non-deferrable.
- Routine release profiles live at `docs/releases/profiles/<tag>.yaml` and are the source of truth for routine release version state, target set, publication requirements, required evidence classes, generated release-prep surfaces, and validator expectations. Release tooling may read the profile, but scripts are not the source of truth for routine release state.
- Release preflight owns cheap deterministic local/profile/schema checks. `scripts/release-verify.sh <tag>` remains the authoritative full release gate for generated outputs, archive integrity, package contents, adapter metadata, and full validation.
- For a governed change, `docs/changes/<change-id>/change.yaml` is the sole
  mutable state owner. `artifact_states` owns artifact lifecycle settlement,
  while `workflow_state` owns the current stage, milestone, blocker, next
  stage, and closeout readiness.
- Governed proposals, specs, architecture, ADRs, plans, and test specs retain
  stable intent and one change-record pointer; they do not carry mutable
  lifecycle, progress, review, blocker, or routing fields.
- Authoring and review skills are peers with transition-scoped writes to one
  matching artifact-state entry. A new primary plan reaches `review-required`
  without live planned work; after clean review evidence, `plan` initializes
  missing planned-work state exactly once from the reviewed revision, and the
  same review occurrence retries settlement. `workflow` coordinates those
  calls and selects routing and every later planned-work operation; the
  lifecycle CLI validates and persists each closed selected operation. Downstream
  skills write their own evidence and route upstream defects to the owner.
- `bounded-review-fix` remains the only writable workflow-automation
  mechanism. One structured target is the complete public consent boundary
  for repository-local prerequisite stages through that target.
- The mechanism does not require or persist a second public authorization,
  capability, activation selector, risk-class parameter, or selector ledger.
  It validates current prerequisites and fixed stage ownership before each
  invocation.
- Planned-work state is a bounded `workflow_state` projection of the stable
  plan milestone definitions. Repeated implementation and review occurrences
  bind the exact current milestone and never silently rebind on resume.
- Review evidence is durable before review settlement. Interrupted identical
  settlement is idempotently reconciled by the matching review peer;
  workflow pauses rather than manufacturing approval.
- Before governed lifecycle CLI activation, compatibility validators check closed values, legal transitions, evidence consistency, routing consistency, migration state, and generated-adapter parity without using content hashes or claiming which process physically wrote a file. After activation, the lifecycle engine uses exact content identities for freshness and revision calculation but still makes no actor-attribution claim.
- Proposal-side deterministic corrections remain driver-owned; implementation correction eligibility remains reviewer-owned; verification failure never authorizes automatic repair.
- Historical changes remain read-only. Resumed nonterminal work migrates once
  to the new state model before mutation, seeding exact current artifact and
  available authoring-evidence identities without changing settlement; no
  migration or rollback restores a retired artifact-local, plan-owned, or
  profile-owned writer.
- The mechanism cannot open PRs, push branches, publish, deploy, merge, perform destructive Git operations, or perform other external actions.
- The requirement-fidelity gate is an additive sibling to the independent adversarial review gate. When both apply, workflow-managed continuation requires both passing receipts.
- Requirement-fidelity applicability is determined before artifact comparison from affected-path and category triggers, with closed applicability results and justified reviewer override only.
- Requirement-fidelity review uses the governing spec clause as the canonical comparison point. Implementation and validator agreement is not proof of spec fidelity.
- Mandatory manual-review applicability classification is outside the first requirement-fidelity slice; manual reviews may voluntarily record fidelity receipts.
- Automation continuation requires a valid structured target, current settled
  prerequisites, unambiguous artifact or milestone identity, and no stop
  condition. The target never widens the invoked stage's fixed write boundary.
- Automation target state is change-local and subordinate to
  `workflow_state`; it does not own artifact settlement or another routing
  cursor.
- Architecture applicability is a closed routing result. Ambiguity pauses; a
  conditional target that is not applicable returns `target-not-applicable`
  rather than silently advancing.
- Implementation auto-fix authority belongs to code-review findings, not the coordinator. The coordinator enforces reviewer-declared classifications, affected paths, recipes, command boundaries, shrinking loops, and audit records.
- First implementation remains review-based for architecture package completeness; required package-shape, C4-file, and ADR-presence enforcement automation is deferred.
- Top-level legacy documents under `docs/architecture/*.md` are archived historical artifacts after accepted current content has been merged into this canonical package.
- Package diagrams live as separate authored source files under `diagrams/`; default Mermaid diagrams use `.mmd` files and are linked from `architecture.md` by relative path.
- Mermaid flowchart C4 diagrams use explicit person, system, external, and container styling; container labels include technology when relevant to review.
- Published-skill repository acceptance is deterministic: it does not start Codex, Claude Code, or opencode, send prompts, grade LLM output, or treat transcripts and model selection as product proof.
- Codex, Claude Code, and opencode receive equivalent generated-package inventory, mapped-resource, declared-transformation, archive, and byte-parity proof.
- Installer materialization is a conditional filesystem-only proof surface, not a fourth product gate and not a target-runtime behavior test.
- Existing selector, cache, scheduler, broad-smoke, benchmark, and validator-meta-test contracts remain transitional architecture until their retirement slice records exact contract disposition and replacement coverage.

## Context and Scope

[System Context and Scope](../../design/system.md#context-and-scope) owns the external actors, included responsibilities and target-agent interpretation boundary. The existing [context diagram](diagrams/context.mmd) remains historical structural evidence; it is not a second current composition contract.

## Solution Strategy

Use [Design](../../design/skill/authoring/design.md) for unified behavioral and technical authoring, scoped model selection, decision rationale, affected-consumer reconciliation and independent review. [System](../../design/system.md) owns the assembled responsibility view and integrated obligations. Retained local contracts below continue under their declared owners; the living models do not silently migrate them.

For published skills, use a one-way proof chain: Gate A validates canonical skill and resource integrity; Gate B generates and proves Codex, Claude Code, and opencode package parity; Gate C composes current A and B proof with release-only metadata and archive checks.
Lifecycle records flow to one bounded governance validation owner, while semantic skill questions flow to formal review.
No selector, cache, scheduler, benchmark, or target-runtime evidence layer is allowed between canonical skills and publication without an approved, measured exception.

For boundary-first guidance, use progressive disclosure without creating a
second semantic model. All governed skills carry a small compact core and the
same inline four-question scan. Only feature-contract stages carry formal
authoring guidance, only proof-map stages carry proof guidance, and downstream
stages begin with exact approved artifact rows. One declarative resource
manifest drives projection, parity, measurement, and activation identity.
The inline scan applies automatically when the task admits behavior boundaries;
users do not name the method, and stages expand beyond concise coverage only
for a governing requirement, material risk, or explicit request.

## Building Block View

The current system inventory and responsibility relationships are owned by [System](../../design/system.md#responsibility-inventory). The [container diagram](diagrams/container.mmd) is retained historical evidence. The following Level 2 details remain unmigrated under their existing contract amendments.

### Level 2 White-Box: Project-Map Skill Package

The published `project-map` capability is one governed package with three bounded parts:

- canonical `SKILL.md` owns purpose, routing, placement, target resolution, operation and scope classification, the bounded coordination preflight, evidence and freshness meanings, source rank, command truthfulness, universal map and reliance invariants, stops, claims, resource triggers, and next-stage behavior;
- `references/map-maintenance-and-area-coordination.md` owns detailed refresh comparison, affected-section selection, correction notes, audit, root registration, parent/child and overlap procedure, changed-path targeting, and interrupted maintenance or coordination recovery; and
- `assets/project-map-skeleton.md` owns metadata labels, required section order, root-registration and evidence-trail table shapes, placeholders, and insertion locations without owning evidence adequacy or policy.

Operation and scope are semantic classifications; loaded assembly is separate. `PMA0-simple-root-create` applies only to an absent repository target after the bounded coordination preflight finds no known coordination evidence. `PMA1-maintenance-or-coordinated` applies to every refresh, audit, area scope, and coordinated root creation. Late coordination discovery changes the assembly before dependent work without changing operation or scope.

Area creation is a recoverable two-artifact transaction against one existing valid root map. The attempt binds the root identity, area identity and normalized path, parent identity, evidence baseline, and expected registration. It validates and writes the area file first, revalidates the root, and writes the root registration last as the commit point. Retry completes only an exact matching missing registration; dangling, stale, conflicting, changed-root, or ambiguous state stops without implicit adoption.

### Level 2 White-Box: Progressive Boundary Guidance

See
[`diagrams/component-boundary-guidance.mmd`](diagrams/component-boundary-guidance.mmd)
for the focused component view.

The progressive boundary-guidance component separates four responsibilities:

- governed skill text owns the automatic compact scan, stage decision,
  mutation authority, stop conditions, review authority, and handoff;
- the compact core owns shared vocabulary, stable-ID meaning, interaction and
  example rules, non-Cartesian scenario selection, and upstream-gap routing;
- feature-authoring and proof resources own only their respective formal
  authoring and adequacy models; and
- one declarative projection manifest owns canonical paths, target paths, and
  consumer membership for projection, validation, measurement, and activation.

Approved feature and proof artifacts remain the downstream context carrier.
Plan, implementation, review, and verification stages read their cited rows
first and expand only on a missing, stale, unknown, ambiguous, conflicting, or
escaped identity. No per-stage context packet or runtime service is introduced.

Activation and release handling add three bounded responsibilities without a
new manifest, service, or publication path:

- activation authoring receives one exact reviewed pending-revision identity,
  calls the repository-internal pure
  `derive_grandfathered_specs(root, baseline_revision)` function once, and
  records the returned grandfathered path inventory with that identity in the
  existing activation record without introducing a CLI or activation writer;
- checked-revision validation reads only current repository files and verifies
  one coherent pending or active snapshot, canonical resources, projections,
  adapter support, and rollback metadata without Git history, tags, remote
  state, network access, or public-release claims; and
- routine release tooling retains profile-driven preparation, preflight, full
  verification, trusted tag publication, and rerunnable public closeout for
  the exact reviewed `v0.4.0` commit.

### Level 2 White-Box: RigorLoop CLI Package

The CLI package remains an additive executable delivery container. [Packaging](../../design/engineering/packaging.md#building-block-view) owns its target descriptors and trusted metadata; [Installation](../../design/cli/installation.md) owns acquisition, extraction and bounded destination mutation. The CLI retains command parsing and the shared output envelope for help, version, `init`, recording commands, JSON, human output, warnings, errors and exit codes.

### Level 2 White-Box: Governed Lifecycle CLI

The existing `rigorloop` package gains a `lifecycle` command family around one package-local lifecycle engine. The public CLI, skills, adapters, workflow, CI, and compatibility validators consume one versioned operation and result contract rather than independently interpreting lifecycle fields.

The component has four inward-facing responsibilities:

- repository snapshot: select one governed change and normalize `change.yaml`, exact referenced artifact and evidence identities, dependency edges, schema compatibility, and transient recovery state;
- pure interpretation: derive recorded state, evidence state, effective state, blockers, permitted operations, minimal stage context, lifecycle revision, and stable diagnostics without filesystem mutation;
- pure transition evaluation: validate a closed versioned semantic request and expected revision, enforce operation authority and preconditions, and return a rejected result or deterministic candidate `change.yaml`; and
- transaction adaptation: validate the candidate, serialize one same-directory writer, persist the recovery bundle, replace only `change.yaml`, verify the persisted result, restore prior bytes on failure, and admit only named interrupted-replace reconciliation when automatic recovery cannot finish.

The package pins the maintained `yaml` parser dependency. Parsing admits only the lifecycle schema's closed mapping, sequence, boolean, null, finite-number, and string domain; duplicate keys, aliases, anchors, merges, tags, multiple documents, and unsupported nodes fail before interpretation. Mutation serializes the normalized model through one schema-ordered UTF-8/LF block-YAML writer and does not promise source comment or formatting preservation.

Lifecycle revision uses a versioned canonical serialization of mutation-relevant state plus sorted repository-relative identities for every referenced artifact or evidence item that can affect the result. The versioned identity schema explicitly excludes provenance-only fields. The transient lock and recovery bundle coordinate one worktree but are not Git-tracked truth and are unnecessary for fresh-checkout reconstruction.

Skills retain semantic criteria, artifact authoring, findings, authority limits, stop behavior, and portable use. Governed skills ask the CLI for exact context, author their semantic file, then request registration or settlement. The closed `record-artifact-revision` operation verifies an already-written artifact and authoring evidence, binds creation or revision to the exact entry and optional prior identity, invalidates registrations for the replaced identity, and derives `review-required`; it never writes semantic content or routing state. The CLI validates stage-bound operations but never authors semantic content, selects whether or where workflow continues, invokes an agent, or infers approval. Workflow remains the only routing and continuation decision owner; after workflow selects a closed route-bearing operation such as `start-milestone`, the CLI may validate and atomically apply only that operation's deterministic routing projection.

Milestone completion and continuation are separate engine operations. `complete-milestone` closes only the reviewed milestone, advances the planned-work cursor to the next still-planned milestone, resets `latest_review`, and returns structural eligibility without changing workflow-stage projections. A later workflow-selected `start-milestone` marks the exact current implementation milestone `implementing` and synchronizes `workflow_state.current_stage`, `workflow_state.next_stage`, and an active `workflow.automation.current_stage` in the same candidate. A contradictory active automation projection rejects the candidate before persistence.

When completion consumes a review receipt directly, `lifecycle_cli.milestones.<milestone-id>` stores one normalized completion-evidence record. Its identity covers milestone proof path and digest, review receipt path and digest, the exact canonical review-log occurrence digest rather than the whole log file, the complete packet inventory and digest, normalized review facts, milestone identity, and stage authority. A derived fingerprint covers that normalized record. Current-revision completion replay reconstructs every constituent from repository bytes and compares the normalized record before returning `already-recorded`; omission or drift returns `RL_STALE_EVIDENCE` without mutation. Hashing the canonical occurrence permits unrelated review-log appends while preventing a changed authorizing occurrence from being reused.

Stage authority in a request is a structurally checked claim, not an authenticated identity. The engine matches it to the closed operation, current lifecycle state, exact artifact, and durable evidence. Filesystem authority, trusted CI, and branch protection remain the adversarial enforcement boundary.

During migration, existing Python validators consume the same versioned conformance fixtures and may run behind or beside `rigorloop lifecycle validate`. The Node engine is the mutation-time authority. A mismatch between implementations blocks enforcement; validator retirement follows the ledger-backed proof rule in ADR-20260810 rather than a big-bang rewrite.

### Level 2 White-Box: CLI Observability and Result Projection

One invocation controller surrounds every public command family after safe logging configuration and before dispatch. It owns invocation correlation, timing, diagnostic emission, single semantic-result rendering, and final exit mapping without acquiring semantic or lifecycle authority.

The component separates five package-local responsibilities: strict log configuration; allowlist-only event construction; a synchronous bounded JSON Lines sink; a shared internal command-result representation with compatibility, concise, and detailed renderers; and read-only path or exact-ID log inspection. Semantic handlers return normalized results and do not write diagnostic files or duplicate successful stdout.

The sink owns only `rigorloop.jsonl`, four numbered archives, and `.rigorloop-log.lock` beneath one validated user-state root. A fixed exclusive-create lock serializes each complete append and any rotation for at most 10 attempts and 1,000 milliseconds. Logging failures become `recorded`, `degraded`, or `disabled` diagnostic state and never change repository bytes, lifecycle evidence, semantic status, or exit behavior.

### Level 2 White-Box: Validation and Generation Scripts

The validation and generation container has these important internal responsibilities:

- direct hosted gates and compatibility selection: `scripts/ci.sh` invokes Gate A, Gate B, Gate C regression proof, public-package proof, and lifecycle governance directly for PR and main. `scripts/validation_selection.py` and `scripts/select-validation.py` remain compatibility owners for local, explicit, and release modes until their active contracts receive a separate retirement;
- evidence registration: the selector owns deterministic evidence-class matching for recurring change-local evidence files, rejects broad or ambiguous patterns through regression coverage, routes registered classes to declared checks, and surfaces stable `manual-routing-required` diagnostics for unregistered deterministic evidence;
- validation idempotency: cache helpers compute normalized argv, repository-relative explicit paths, input-surface hashes, implementation manifest hashes, and policy/config hashes for the eligible explicit-path lifecycle command family. Direct `--mode explicit-paths` remains actual-run for closeout and final gates, while helper `--mode explicit-paths-inner-loop` supplies inner-loop cache context, normalizes to canonical direct argv for cache identity, and records displayed-versus-canonical argv in formal helper evidence. Unsupported or uncertain manifests disable caching and run the validator;
- lifecycle and change validators: `scripts/validate-artifact-lifecycle.py`,
  `scripts/validate-change-metadata.py`, and
  `scripts/validate-review-artifacts.py` validate governed artifact-state and
  workflow-state shape, legal transitions, evidence consistency, change
  metadata, and material review closeout structure;
- requirement-fidelity validation: review artifact and skill validators protect the first-slice closed trigger lists, closed receipt vocabularies, packet-ordering evidence, applicability manifests, property-matrix receipt shape, and selected spec-derived property-list by surface-list assertions. Unknown closed-vocabulary values fail closed before consistency checks;
- lifecycle-state consistency: validators check the closed `artifact_states`,
  `workflow_state`, planned-work, blocker, closeout, automation-target, and
  linked-review shapes; reject mixed writable models; and treat plans and
  `docs/plan.md` as stable intent and navigation rather than live-state
  projections;
- change-record query helper: `scripts/query-change-record.py` exposes bounded `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>` reads over valid legacy and compact metadata shapes without executing validation commands;
- package generation: `scripts/build-adapters.py` and `scripts/adapter_distribution.py` implement Packaging’s canonical-to-package path; builds do not install runtime skills, and retained adapter regression owns complete resource and safe-output proof;
- release preparation, closeout, and validation: release tooling reads `docs/releases/profiles/<tag>.yaml` as the routine release transaction source of truth, generates profile-owned release-prep surfaces, checks human-authored surfaces for profile consistency, records timing evidence, and generates published evidence from public GitHub/npm/`npx` data after publication. `scripts/validate-adapters.py`, `scripts/validate-release.py`, and `scripts/release-verify.sh` check generated packages, manifests, release metadata, adapter artifact metadata, tracked release notes, package preview, registry verification, emergency deferral records, checksums, and smoke evidence. Release preflight owns cheap deterministic profile/schema/state checks before broad verification. For public releases, `release-verify.sh` is the maintainer-facing full gate and `validate-release.py` owns structured release validation delegated from that gate. For `v0.1.3` and later, these checks validate generated temporary or release-output adapter packages and release archives instead of tracked adapter package trees.
- published skill resource integrity: [Skill](../../design/skill/skill.md) owns common content/resource invariants; validation and generation consume SKL-SR-08–14. Installer smoke remains only when RigorLoop-owned materialization logic exceeds package copying and ends at filesystem inspection.
- checked-revision boundary activation: `scripts/boundary_first_validation.py` owns the repository-internal pure `derive_grandfathered_specs(root, baseline_revision)` authoring function. It accepts a repository root and an exact 40-character lowercase commit identity, performs read-only Git object inspection, and returns `(sorted_paths, issues)`, where `sorted_paths` is the complete raw-UTF-8-byte-sorted tuple of eligible top-level accepted, approved, or active feature-spec paths and `issues` is empty on success or contains bounded validation issues on failure. The function writes nothing, has no CLI surface, and is called only during the one-time activation implementation step and its regression fixtures. Separately, `scripts/validate-boundary-first.py --check` validates the current activation snapshot, canonical and projected resources, governed skill inventory, adapter support, and rollback metadata without inspecting Git history, tags, remote state, or network services; it never calls the derivation function and reads the frozen record directly.
- project-map contract validation: the first slice validates the normalized skill contract, resource-map entry, skeleton asset, generated adapter inclusion, and a small representative output set for required sections, material citations, inference labels, unknowns, configured/executed command separation, correction notes, and absence of unfilled placeholders. A dedicated project-map artifact validator remains deferred until concrete drift appears in at least two produced maps.
- measurement, benchmark, and reporting scripts: repository-local commands measure skill size, run token-cost benchmark prompts in disposable fixtures, analyze Codex JSONL session exports, summarize tool-output amplification, validate token-cost release metadata, and produce reviewable evidence for reports without requiring hosted telemetry.
- required-benchmark context: release validation determines the release-specific required dynamic benchmark set from core suite policy, transition carryover policy, changed public skills, and claimed optional coverage, then passes that context to token-cost validation in process or through a transient YAML file for CLI and debugging use.
- first-slice script-output shaping: `scripts/test-select-validation.py` is the first standalone runner surface for compact `[PASS]` success summaries, actionable `[FAIL]` details, explicit `--verbose`, silent successful `--quiet`, reliable-only rerun guidance, and behavior-preservation evidence.

See [System's responsibility inventory](../../design/system.md#responsibility-inventory) for the current skill, package, release, recording and assessment owners, and its [bounded consolidation map](../../design/system.md#necessary-design-consolidation-map) for the selected source dispositions.

### Level 2 White-Box: Code-Review Skill Package

The published `code-review` capability is one governed package with four bounded parts:

- canonical `SKILL.md` owns the universal direct, isolated, formal, and workflow-managed review contract, including authority, evidence, statuses, recording, stops, claims, milestone behavior, and handoff;
- `references/boundary-first-method-v1.md` owns shared boundary vocabulary and method detail already governed by the progressive boundary-guidance architecture;
- `references/workflow-managed-automated-review.md` owns only procedure that applies after a formally armed workflow-managed automated review or correction-loop trigger; and
- mapped result and finding assets own repeated copy-and-fill structure without owning policy.

The reference load is conditional disclosure, not delegation. `code-review` remains the only lifecycle, verdict, policy, recording, and readiness owner. Direct and isolated review must remain complete from `SKILL.md`; a missing or ambiguous automation trigger does not load the conditional procedure.

A change-local rule-disposition ledger maps every behaviorally significant current rule or duplication cluster to exactly one inline, conditional-reference, asset, duplicate-removal, or approved-obsolete destination. The ledger is implementation and semantic-review evidence, not another published runtime contract or permanent validation subsystem.

Existing Gate A proves package structure, closed resource mappings, containment, presence, placeholders, and narrow forbidden claims. Gate B proves the same complete package across supported generated and packed adapter targets, including relative paths and raw-byte identity for untransformed resources. For `code-review`, deterministic install proof also materializes every supported target into a temporary tree and compares mapped-resource inventory, relative paths, and raw-byte identity; additional installer logic may add bounded filesystem checks. Semantic review separately proves that relocated rules keep their owner and meaning; no target-agent execution or transcript grading participates in acceptance.

### Level 2 White-Box: Route Skill Package

The published `route` capability is one governed package with four bounded parts:

- canonical `SKILL.md` owns universal classification, source precedence, unknown-artifact behavior, lifecycle outline, isolation, high-level state ownership, stop and claim boundaries, resource triggers, and result or handoff policy;
- `references/governed-lifecycle-routing.md` owns governed identity interpretation, lifecycle and architecture-assessment applicability, settlement, stage transitions, milestone and review-resolution return, final review, closeout, and contradictory-state procedure;
- `references/bounded-workflow-automation.md` owns automation commands, target and occurrence, authorization identity, status, pause, resume, cancellation, packets, receipts, budgets, correction cycles, and automation-specific promotion procedure;
- `references/boundary-first-method-v1.md` retains its shared-method responsibility.

Conditional disclosure does not delegate workflow authority.
Automation consumes governed transition decisions and cannot redefine stage order, applicability, settlement, architecture assessment, final review, or closeout.
Any contradiction between the universal file and mapped references is a package defect rather than a local precedence choice.

Invocation assembly is authority-bound.
Generic, governed, governed-automated, guide-authoring, governed-guide, transient target-bootstrap, and stateless status-or-off commands have explicit resource sets.
Command context is not armed authority.
Target bootstrap persists nothing until governed identity is established and validated, while stateless status or off returns `no-active-run` without creating governed or automation state.
Active automation and guide authoring do not combine in one invocation.

Required conditional resources fail safe.
After classification and before dependent interpretation or action, the package checks that triggered references and assets are available and readable.
Missing, unreadable, contradictory, or mixed-version required resources stop the affected operation without remembered, invented, or partial reconstruction.
Resources whose triggers are false remain unloaded.

The complete workflow package is one canonical, generated, packed, archived, installed, and rollback unit.
Gate A and Gate B retain structural, containment, inventory, path, and raw-byte identity ownership.
Change-local fixtures and semantic review prove assembly selection, policy ownership, bootstrap ordering, failure behavior, and lifecycle preservation without executing or grading a target-agent runtime.

### Level 2 White-Box: Unified Workflow Automation

See [`diagrams/component-workflow-automation.mmd`](diagrams/component-workflow-automation.mmd) for the component view.

The published skills are the primary ownership surface.
Repository scripts validate their structured state and generated parity but do
not define another policy language.

The component has five responsibilities:

- target routing: `workflow` stores one structured target and advances only
  from current settled artifact state and stage-owned evidence;
- artifact-state transitions: each authoring or review peer changes only one
  matching `artifact_states` entry through the closed transition vocabulary;
- workflow-state selection: `workflow` alone selects current stage,
  milestone continuation, blocker disposition, next stage, and final-closeout
  intent; after lifecycle CLI activation, the CLI validates and atomically
  persists only the selected closed operation's derived fields;
- evidence linking: `change.yaml` points to authoring, review, resolution,
  validation, verification, and learn evidence without copying their bodies;
  and
- compatibility validation: historical records remain readable, while resumed
  nonterminal work must migrate to the new single-write model before mutation.

Authoring skills own governed content and the matching transitions into
`authoring` and `review-required`.
Review skills own formal review evidence and the matching settlement
transition.
Downstream stages own only their implementation or stage evidence.
They report upstream defects and stop instead of repairing upstream artifacts.

`workflow` coordinates these peers but cannot edit governed content, create a
review verdict, settle an artifact, or widen a stage's write boundary.
One automation target covers repository-local prerequisite stages through the
target without a second authorization, capability, selector, or risk-profile
layer.

Deterministic compatibility validators reject unknown values before consistency checks, illegal transitions, conflicting artifact and workflow state, stale review evidence, ambiguous milestone bindings, open blockers, mixed writable models, and adapter drift. Before CLI activation they do not hash governed content. The activated lifecycle engine adds content identities for freshness without claiming which skill process performed a write.

## Runtime View

### Design authoring flow

Follow [Design Runtime View](../../design/skill/authoring/design.md#runtime-view) for the reconciled engineering contract and exact review handoff. [System](../../design/system.md#integrated-authoring-change) explains the composition with planning, implementation and verification.

### Workflow and review flow

1. Non-trivial work records `change.yaml` plus durable Markdown reasoning under `docs/changes/<change-id>/`.
2. Workflow-managed delivery follows one recommended standard workflow, stage triggers, completed stage outcomes, and stop conditions.
3. Direct manual skill requests remain isolated unless the user explicitly asks to continue through the standard workflow.
4. Every supported formal lifecycle review records change-local review evidence or reports blocked recording. Clean no-finding reviews use lightweight receipts; material findings use detailed review records.
5. `review-log.md` indexes clean receipts and detailed review records so review events are discoverable without chat history.
6. `review-resolution.md` closes material findings only after final dispositions, actions, rationale, and validation evidence are recorded. Clean no-finding reviews do not create empty `review-resolution.md` solely because a receipt exists.
7. `$route auto: <target>` records one structured repository-local target.
   It does not pre-set future readiness or create another authorization layer.
8. Before each invocation, workflow reads the matching settled artifact state,
   current `workflow_state`, stage-owned evidence, and exact artifact or
   milestone binding.
9. Workflow validates that prerequisites are current and that the next stage's
   fixed write boundary can satisfy the route without modifying an upstream
   artifact.
10. The invoked authoring stage changes only its matching artifact entry to
    `authoring`, writes its artifact and authoring evidence, then changes that
    entry to `review-required`.
11. The matching review peer writes durable review evidence first and settles
    only that artifact entry. An isolated review stops without touching
    `workflow_state`.
12. In a workflow-managed run, workflow reads the settled result and updates
    only routing and planned-work state before invoking the next prerequisite
    stage.
13. If settlement is interrupted after evidence is durable, the same review
    occurrence reconciles idempotently. Workflow never settles on the review
    peer's behalf.
14. If a downstream stage discovers an upstream defect, it records the defect
    in its own evidence and pauses. Workflow routes to the upstream author,
    whose revision and fresh peer review precede conservative replay.
15. A target at `verify` remains sufficient consent for repository-local
    prerequisite stages, but future stages remain incomplete until their
    concrete prerequisites and evidence exist.
16. Verification failure pauses without automatic repair. Successful final
    verification completes the target and reports `pr` as the next stage
    without opening it.
17. `off` cancels the current run, preserves evidence, and stops scheduling;
    it does not restore retired writers or erase stage-owned history.
18. Historical status reads are side-effect free. The first resumed
    nonterminal mutation migrates to `stage-owned-change-local-v1`; historical
    embedded status and retired plan/profile state become read-only.
19. Workflow-managed automated reviews run through the independent adversarial review gate before their result may advance workflow routing. The orchestrator creates an immutable review invocation manifest from tracked artifacts, records a verifiable initial-packet inventory and hash, records the reviewer context identity, and fails closed when the context is `L0` or the required independence level cannot be proven.
20. The review gate releases evidence in phases. The reviewer first receives only the review target, governing artifacts, formal criteria, neutral routing metadata, and previous-round existence facts when applicable. After the reviewer records the risk map, the orchestrator records `risk-map-recorded`, releases the evidence menu, then records subsequent receipts for evidence-result release, prior-finding release, and verdict recording.
21. Risk-tier classification is orchestrator-owned and fail-closed. Standard risk requires L1, elevated risk requires L2 plus required direct proof and second-review policy, and critical risk requires L3 or human authority according to the trigger. Ambiguous trigger matches classify upward.

### Reviewed plan initialization and settlement flow

1. `plan` writes or revises the canonical stable-intent plan, registers the stable artifact tuple, and leaves the plan entry `review-required` without `planned_work`.
2. `plan-review` records a clean result for the exact reviewed repository revision. It leaves the entry `review-required` and reports `initialization-required` rather than claiming active settlement.
3. In workflow-managed execution, `workflow` invokes the plan-owned `initialize-approved-plan` operation. Isolated review stops after reporting the required operation.
4. `plan` validates the stable artifact tuple, clean review identity, unchanged reviewed revision, closed resolution state, milestone definitions, and absence of `planned_work`; it writes only the missing initial `planned_work` projection.
5. `workflow` invokes an identical settlement retry. `plan-review` reuses the existing judgment and durable review record, then moves only the plan entry to `active`.
6. Workflow routes onward only after initialization and settlement both succeed. Interruption preserves evidence and retries the owning operation; stale or conflicting identity, state, or evidence fails closed.

Legal temporary states are limited to authoring/revision/blocked without `planned_work`, review-required before review, review-required with clean evidence and no `planned_work`, review-required with clean evidence and matching `planned_work`, and active with settled clean review and matching `planned_work`. No content hash or new identity field participates in this flow.
22. The reviewer records the stage-native verdict, findings or clean-review sufficiency receipt, confidence, evidence challenge, and reconciliation results. The orchestrator derives `review_gate_outcome` only after manifest, phase-receipt, risk-tier, clean-receipt, second-review, and unresolved-finding gates are evaluated.
23. When the affected paths or changed content trigger requirement-fidelity applicability, the workflow or pre-review stage records an applicability manifest before the reviewer compares implementation wording or validator assertions.
24. Applicable review packets present the relevant spec clauses first, then accepted decompositions when present, expected surfaces, implementation diff, validator assertions, validation evidence, and prior findings. If no accepted decomposition exists, the reviewer records a reviewer-authored decomposition before artifact comparison.
25. For multi-surface contracts, the reviewer checks each requirement property against each required surface and compares validator assertions to the full spec-derived property list. A global substring match or implementation/validator agreement on a compressed subset is not clean-review evidence.
26. Applicable clean reviews require a requirement-fidelity receipt. Missing decomposition evidence, free-form `not-applicable` reasons, incomplete property matrices, or validator assertions accepted without spec comparison make automated continuation ineligible.
27. A derived `stop` from native `changes-requested` does not uniformly pause
    automation. Workflow may route to `review-resolution` only when the
    selected repository-local target still permits that prerequisite, the
    fixed stage ownership boundary is satisfied, and the independence,
    fidelity, evidence, and correction-loop gates pass; otherwise it pauses
    with a specific unroutable stop reason. Native `blocked` and
    `inconclusive` always pause.
28. Required or sampled second-review disagreement is not majority-voted away. A second reviewer material finding, blocked result, or inconclusive result prevents automatic continuation and routes to review-resolution, owner decision, or another authorized review.
29. Before `explain-change` and `verify`, workflow requires a final holistic
    code review over the complete final diff, governing artifacts, review
    resolutions, validation selection, generated artifacts, and
    cross-milestone scope.
30. Final closeout runs `ci-maintenance` when triggered, then
    `explain-change`, `verify`, and `pr`, subject to the selected target and
    the human-controlled PR boundary.
31. `explain-change`, `verify`, and `pr` use the change-local evidence pack, plan state, validation output, and review closeout state before claiming readiness.

### Final-review stage-evidence tail flow

1. Final holistic code review binds reviewed subject revision `S` and its base-to-subject diff.
2. The review peer records its exact review occurrence, invocation, log, conditional resolution, and matching settlement. Those changes form one non-merge direct-child revision `R`.
3. Workflow validates `R` by both path and field ownership. Shared `change.yaml` changes are admitted only for the closed final-review transition; path membership alone never establishes authority.
4. `explain-change` binds the unchanged reviewed subject and final-review identity, writes only the exact explanation artifact, and returns neutral handback facts.
5. Workflow records only the matching handback fields. The explanation and handback changes form one non-merge direct-child revision `E`, which is the pre-verify handoff revision.
6. Verify accepts final-review reuse only for exact linear ancestry `S -> R -> E`, exact content identities, and the closed per-revision path-and-field sets.
7. If execution stops after `R`, an identical retry may create only `E`. Any intervening revision, changed basis, merge, reordered evidence, unknown field, or unrelated path makes final-review reuse stale.
8. Verify-owned evidence written after `E` does not retroactively enter the pre-verify tail or redefine `S`, `R`, or `E`.

### Change-record catalog flow

1. A contributor or agent adds deterministic evidence under `docs/changes/<change-id>/`.
2. The changed-path selector matches the path against registered evidence classes before verify.
3. A registered evidence file routes to the evidence class's declared check IDs and governing change metadata context.
4. An unregistered deterministic evidence file receives a stable `manual-routing-required` diagnostic and becomes registration debt.
5. Registration debt is resolved before verify by adding a supported registry route, removing or renaming the unsupported evidence, or recording owner-approved deferral with validation impact and follow-up.
6. Workstream B adds `scripts/query-change-record.py` as the bounded read surface for common questions such as artifact paths, latest validation state, and stage-scoped validation evidence.
7. Query helper reads never execute validation bundle commands and never replace full forensic reads when evidence is disputed, ambiguous, unsupported, or the whole change record is the review target.
8. Stage-skill guidance may reference query helper commands only after those commands are stable and generated adapter output has been validated.

### Validation flow

1. Hosted PR and main acceptance invokes the stable product and governance owners directly through `scripts/ci.sh`; it does not invoke selector, cache, scheduler, or target-runtime evidence.
2. Local targeted compatibility remains available through `python scripts/select-validation.py --mode explicit --path ...` and `bash scripts/ci.sh --mode explicit --path ...`.
3. The selector emits stable check IDs such as `artifact_lifecycle.validate`, `change_metadata.validate`, `change_metadata.regression`, `review_artifacts.validate`, and generated-output checks.
4. Lifecycle-managed artifacts are checked with `scripts/validate-artifact-lifecycle.py`.
5. When governed lifecycle state is in scope,
   `scripts/validate-artifact-lifecycle.py` parses exact artifact, workflow,
   planned-work, blocker, target, and evidence fields; rejects unknown values
   before consistency checks; and blocks illegal transitions, mixed writers,
   stale evidence, or open blockers without scanning arbitrary historical
   prose.
6. Change metadata is checked with `scripts/validate-change-metadata.py`.
7. Review artifact closeout is checked with `scripts/validate-review-artifacts.py` when review files are in scope.
8. Architecture diagram source files and historical or exceptional change-local architecture evidence route only to existing non-enforcement lifecycle checks; C4 sufficiency, arc42 completeness, ADR need, and package shape remain architecture-review or code-review evidence.
9. Unclassified paths do not fail open; they require explicit manual routing or a later selector contract update.
10. Broad smoke remains an explicit legacy compatibility boundary and is not the hosted PR or main publication path.
11. Normal script and wrapper output is summary-first and failure-focused: passing checks collapse into counts and durations, failed checks expand with actionable details, and full passing detail remains available through `--verbose`.
12. `--quiet` is a script-local success-silencing mode, not a failure-hiding mode. Successful quiet runs produce no stdout or stderr, while usage errors, validation failures, test failures, and zero-test safety failures may emit bounded actionable diagnostics.
13. For branches adding deterministic change-local evidence, actual changed-path routing proof is required before verify. Supplemental fixtures and explicit-path validation do not replace routing the branch's own changed paths.

### Published skill resource-integrity flow

Common content/resource behavior is owned by [Skill](../../design/skill/skill.md), SKL-SR-08–14, under its coordinated adoption boundary. Canonical presence, verb classes, containment, bounded legacy lint, raw-byte parity and complete transformations are defined there rather than duplicated here. Validation and distribution consume those invariants through their existing gates.

8. Gate B proves Codex, Claude Code, and opencode package inventory, mapped-resource paths, declared transformations, archive contents, and untransformed raw-byte identities from local generated output or release candidates.
9. Installer inventory decides whether package parity is sufficient. A pure copy adds no smoke; meaningful RigorLoop-owned materialization receives only empty-temporary-directory invocation and filesystem inspection.
10. Target-agent runtime execution, prompts, transcripts, model selection, and LLM-output grading are not package proof and do not participate in repository acceptance.

### Code-review package loading and simplification flow

1. Every invocation enters canonical `skills/code-review/SKILL.md` and receives the complete universal review contract before any conditional resource decision.
2. Direct, isolated, and ordinary formal reviews continue from the common path without loading workflow-managed automation procedure.
3. Only a formally armed workflow-managed automated review or correction loop activates the exact `READ references/workflow-managed-automated-review.md` mapping.
4. The conditional reference supplies automated phases, packet handling, fidelity and risk procedure, correction classification, bounded correction and rereview, receipts, promotion, pause, and automation-specific failure handling without redefining native verdicts or handoff authority.
5. Repeated result and finding structures come from the mapped assets; policy remains inline or in the allowed conditional procedure according to its universal applicability.
6. Implementation records every current rule in the change-local disposition ledger before deleting or relocating prose. Unknown dispositions and missing destinations fail closed.
7. Deterministic fixtures prove required and forbidden outcomes for representative modes without running an agent. Independent semantic review checks the complete package and ledger.
8. Gate A and Gate B must both accept the complete resource move before publication. Each supported package is then materialized into a temporary installed tree whose mapped-resource inventory, relative paths, and raw-byte identities match the proved package. Partial canonical, generated, packed, or installed targets stop; rollback restores the prior canonical package and regenerates derived targets as one version.

### Workflow package loading and simplification flow

1. Every invocation enters canonical `skills/route/SKILL.md` and receives universal classification, authority, isolation, stop, claim, resource-trigger, and handoff policy.
2. Classification selects exactly one valid assembly or an explicit stop outcome from current governed, command, armed, and guide-authoring evidence.
3. Governed reads or transitions load `references/governed-lifecycle-routing.md`; read-only use does not imply mutation authority.
4. Stateless `status` or `off` loads only automation procedure and creates no state. A new target enters transient bootstrap, validates governed identity, reclassifies, loads governed procedure, and only then persists authorization or run state.
5. Armed automation loads governed and automation procedure. Automation asks governed procedure for each lifecycle transition and never becomes the stage-order owner.
6. Guide creation or substantial refresh loads guide procedure and the skeleton. Active automation combined with guide authoring stops until the run is inactive.
7. Before conditional interpretation or action, every triggered resource must be present and readable. Missing, contradictory, or mixed-version resources stop without fallback reconstruction.
8. Change-local semantic and literal inventories account for every moved, retained, or removed rule and genuine exact-text dependency. Static fixtures prove valid and invalid assemblies without running a model.
9. Gate A and Gate B accept the complete resource move before publication. Rollback restores the prior complete canonical package and regenerates all derived targets as one version.

### Progressive boundary-guidance projection and activation flow

1. A governed skill applies the four inline compact-scan questions before a
   qualifying stage-owned decision. Non-behavior work continues without a
   formal record or portable-resource read.
2. A feature-authoring or proof-owning stage loads the compact core and its one
   family resource. A downstream stage begins with the exact approved artifact
   rows cited for its decision and loads the compact core only when those rows
   cannot explain an observed outcome.
3. Maintainers edit the three canonical sources only:
   `specs/references/boundary-first-method-v1.md` for the compact core,
   `specs/references/boundary-first-feature-authoring-v1.md` for feature
   semantics, and `specs/references/boundary-first-proof-v1.md` for proof
   semantics.
4. `specs/boundary-first-resources.yaml` declares the closed resource IDs,
   canonical paths, skill-root-relative targets, and consumers. Its only
   top-level keys are `schema_version: 1`,
   `contract_version: boundary-first-v1`, and `resources`; its resources are
   exactly `compact-core`, `feature-authoring`, and `proof` in that order, with
   the exact paths and consumers defined by ADR-20260729. Entries contain only
   `id`, `source`, `target`, and `consumers`. The projection module rejects
   unknown or missing fields, IDs, consumers, unsafe paths, duplicates,
   missing sources, and unowned mappings before mutation.
5. Write mode preflights the complete matrix, then copies raw bytes to all
   expected skill-local targets. Check mode reports missing, additional, stale,
   mixed, path-divergent, or byte-divergent resources without mutation.
6. Projection identity uses raw-byte SHA-256 per file plus a sorted
   `<repository-target-path>\0<digest>\n` aggregate. The activation manifest
   binds the raw-byte resource-manifest identity and the aggregate projection
   identity.
7. Each governed `SKILL.md` maps the compact core with `READ` and a
   stage-specific load condition. Only `spec` and `spec-review` map
   feature-authoring guidance; only `test-spec` and `test-spec-review` map
   proof guidance.
8. Skill validation checks inline compact-scan drift, resource ownership,
   manifest closure, mapping shape, containment, canonical identity, and
   projection identity before dependent consistency checks.
9. Existing skill and adapter generators copy complete governed skill roots.
   Resource-integrity checks compare mapped paths and raw-byte SHA-256 through
   canonical, generated, packed, and clean installed target trees.
10. The changed-path selector assigns skill-only paths to purpose-built skill,
    boundary, projection, adapter, and prose checks. It assigns lifecycle
    validation only to actual governed artifacts and change records. Mixed
    changed sets retain both families with check-owned affected paths.
11. A tracked representative fixture records mapped, initially loaded, and
    permitted expansion resource IDs by stage family. Implementation evidence
    reports before-and-after canonical bytes, mapped-resource counts, and
    representative initial and expanded loaded-resource counts without making
    them release gates.
12. Activation authoring supplies one exact 40-character lowercase reviewed
    pending-revision identity and the repository root to the internal pure
    `derive_grandfathered_specs(root, baseline_revision)` function. The
    function performs read-only Git object inspection and returns the complete
    eligible accepted, approved, or active top-level feature-spec paths sorted
    by raw UTF-8 bytes plus an empty issue tuple, or no inventory plus bounded
    validation issues when the identity or baseline content is invalid or
    unavailable. The activation implementation step calls it once and records
    the supplied identity and returned paths directly in the existing
    activation record. Regression fixtures prove the recorded inventory and
    failure behavior. No CLI, public preparation command, or activation writer
    is introduced.
13. Every checked revision contains one independently valid `pending` or
    `active` snapshot. Pending uses sentinel release, rollback, and baseline
    values plus an empty inventory. Active uses release intent `v0.4.0`,
    rollback `v0.3.6`, the frozen baseline provenance, and the frozen inventory.
14. `python scripts/validate-boundary-first.py --check` reads current files
    only. It verifies the closed activation record, canonical resources,
    resource manifest, governed skills, projections, adapter support, and
    rollback metadata, and rejects missing, additional, stale, malformed,
    unknown, mixed, or divergent values.
15. Checked-revision validation does not inspect prior revisions, require the
    baseline to remain reachable, query a remote, require a release tag, or
    claim public availability. It reports the checked snapshot and release
    intent only.
16. Generated packages, archives, and installed target trees remain derived
    proof bound to canonical sources and release metadata; they are not tracked
    activation or rollback state.
17. New top-level feature specs absent from the frozen inventory require the
    standing boundary record. Edits to grandfathered specs continue to route
    to `spec-review` for substantive-revision classification.
18. Routine `v0.4.0` release preparation, preflight, full verification,
    trusted tag publication, and public closeout remain unchanged. The tag
    identifies the exact reviewed release commit, and public claims require
    GitHub, npm, and public `npx` evidence.
19. Before publication, validation failure leaves public state unchanged.
    After publication begins, partial state remains open and recovers through
    rerunnable closeout, dist-tag correction or deprecation when applicable,
    or a later patch. Immutable release identities are never rewritten.

### Project-map authoring and refresh flow

1. The `project-map` skill resolves exactly one operation (`create`, `refresh`, or `audit`) and one scope (`repository` or `area:<slug>`) before broad repository reading.
2. The skill resolves the exact target and current existence state. Create requires absence, refresh requires an existing target, and audit remains read-only whether the target exists or produces `missing-map`; no operation silently converts into another.
3. The skill resolves artifact placement from explicit user path, existing artifact metadata or active workflow context, project workflow guidance, and then portable defaults.
4. Before omitting conditional procedure for root creation, the skill checks the seven known coordination surfaces. It selects PMA0 only when no known coordination evidence exists; otherwise it loads PMA1 or stops if the required reference cannot be used.
5. For create or refresh, the map records metadata before the substantive sections: status, scope, baseline, last-reviewed date, coverage, exclusions, parent map, and known gaps.
6. When Git is available and inspected files include uncommitted changes, the baseline records `<sha>+dirty` and the inspected uncommitted paths so later readers can reconstruct what evidence was actually mapped.
7. The map writes current-state claims from source-ranked evidence. Material claims cite repository paths, inferences are labeled, and unknowns move to `Open questions` instead of being guessed.
8. Runtime and data-flow statements name their evidence mode: statically traced, demonstrated by tests, observed through execution, or partially inferred.
9. Configured commands and executed commands remain separate. Executed commands include exit codes; mutation, network, build, and test-suite commands require user go-ahead before execution.
10. Area maps are created only for durable repository boundaries and only when the root-map section would otherwise exceed roughly a screen of content, unless the area has its own deploy, release, ownership, package, domain, or data lifecycle.
11. Area creation requires an existing valid root and binds the complete root, area, parent, baseline, and registration identity before writing. It validates and writes the area file first, revalidates the root, and writes root registration last as the commit point.
12. An identical retry may complete only a missing registration for the exact matching area and transaction basis. Orphaned, dangling, stale, changed-root, conflicting, or ambiguous state stops without implicit adoption or overwrite.
13. When an area map exists, the root map remains the entry point. Overlap names one map as detail owner and makes the other link rather than duplicate.
14. If a refresh discovers a previous map claim was wrong at its recorded baseline, the result includes a correction note. Map status remains `current`, `partial`, or `stale`.
15. Risks and open questions remain orientation evidence. Any action routes through proposal, plan, learn, review resolution, release evidence, or other workflow-owned follow-up surfaces.
16. Downstream stages may use current maps for orientation, but inspect source directly when the relevant map is stale, partial, conflicting, missing cited paths, inferred, unknown, security-sensitive, or exact-behavior critical.

### Validation idempotency cache-hit flow

1. A contributor requests inner-loop lifecycle validation through `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop ...`, or a contributor, CI wrapper, or final gate requests actual lifecycle validation through direct `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.
2. Cache eligibility checks confirm the command surface is part of the first-slice explicit-path lifecycle command family and is not being used for a stage or milestone closeout full-bundle gate.
3. For helper invocations, the cache helper keeps the displayed helper argv for evidence but normalizes cache identity to the canonical direct `--mode explicit-paths` argv. For direct actual-run invocations, the canonical argv is the direct command.
4. The cache helper normalizes the command as an ordered argv vector, normalizes `--path` values as repository-relative POSIX paths, rejects unsafe or duplicate explicit paths, and computes the command hash.
5. The cache helper computes the input-surface hash from every explicit path's content hash or missing-file marker.
6. The cache helper computes the validator implementation manifest hash from the entrypoint, resolved repository-local imports/helpers, and manifest-generation logic, and computes the policy/config manifest hash from declared lifecycle policy/spec/config files.
7. If a matching local execution cache entry exists for the same branch, worktree, change ID, canonical command hash, input-surface hash, implementation hash, policy hash, and previous `pass` that traces to an actual run, the helper may emit bounded `[CACHE HIT]` output and write or merge formal cache-hit evidence when a safe change root or safe evidence path is supplied or inferable.
8. If any cache component is missing, malformed, unsupported, changed, unsafe, non-local, expired, non-passing, or not traceable to an actual run, the validator actually runs and preserves existing pass/fail behavior and exit semantics.
9. Formal cache-hit evidence in `validation-cache-evidence.yaml` is reviewable proof that a prior pass still applies. Helper-produced evidence records `displayed_command_argv`, `canonical_cache_argv`, `cache-hit-inner-loop`, `scope: inner-loop`, and `closeout_evidence: false`; it is not a new pass.
10. Closeout validation ignores cache hits as pass evidence. A closeout bundle is satisfied only by compact `schema_version: 2` validation events with `result: pass` and `evidence_kind: actual-run-pass` from the direct actual-run command or another approved actual-run bundle.
11. Workstream A measurement in `validation-cache-measurement.yaml` records eligible commands, helper invocations, cache hits, misses, disabled evaluations, helper actual-run fallbacks, actual runs, closeout actual runs, time saved, remaining cost, cache-hit rate, and Workstream B recommendation state.

### Token-cost measurement flow

1. Static skill measurement reads canonical skill files and reports byte size, line count, estimated token count, and largest sections where Markdown headings are available.
2. Codex JSONL session analysis reads a contributor-supplied exported session, reports token usage when present, and summarizes tool calls, command-output size, broad reads, high output caps, repeated reads, and top measured cost drivers.
3. Command-output amplification starts inside the JSONL analyzer because recorded sessions are the first evidence source for this workflow; live command wrapping remains a later optional surface.
4. The first baseline report is authored under `docs/reports/token-cost/`.
5. Change-local artifacts link to the durable baseline report when the report is produced by a change.
6. Token-cost thresholds are warning-only in the first slice and do not replace required validation, review, or workflow gates.

### Release Token-Friendliness benchmark flow

1. A maintainer preparing a public release runs static skill measurement and the tracked benchmark suite under `benchmarks/token-cost/`.
2. For `skill-token-runtime-v2`, release validation determines the effective required dynamic benchmark set from required core benchmarks, one-release transition carryover benchmarks, changed public skill benchmarks, and optional benchmarks that are explicitly claimed as release coverage.
3. Release validation passes that required benchmark context to token-cost validation in process. The standalone validator may receive the same context as YAML through `--required-benchmark-context`; that YAML is normally transient and tracked only when it becomes release decision evidence.
4. The benchmark runner copies the clean minimal downstream fixture into an isolated temporary directory outside the repository.
5. For Codex benchmarks, the runner installs current public Codex adapter skills from tracked public adapter output while that output remains tracked, or from generated temporary adapter output or release artifact output after public adapter skill copies move out of tracked Git. For `v0.1.3` and later, dynamic benchmark inputs use generated public adapter output or release archive output. The runner does not use repository-local `.codex/skills/` as the public benchmark source.
6. The runner executes prompt fixtures with `codex exec --json --ephemeral`, writes raw JSONL under `docs/reports/token-cost/runs/<release-version>/` when raw JSONL is tracked, and invokes the JSONL analyzer automatically.
7. Analyzer summaries are written beside run evidence and carry structured usage, tool-output, signal, verdict, and raw-or-sanitized evidence identity fields.
8. Maintainers manually review `skill-token-runtime-v2` benchmark result quality and record structured criteria for each dynamic run until stable expected-output checks justify automation.
9. Maintainers write a human-readable Markdown report and structured YAML metadata under `docs/reports/token-cost/releases/<release-version>.md` and `.yaml`.
10. `scripts/validate-token-cost-report.py` validates the token-cost metadata schema, waiver fields, run references, runner metadata, portability status, raw-or-sanitized evidence, result-quality evidence, required benchmark coverage, optional warning evidence, claimed optional coverage, and comparison shape.
11. Release validation delegates token-cost report validation before public release readiness is claimed.

### Generated guidance flow

1. Canonical skill sources under `skills/` are edited.
2. Adapter entrypoint templates under `scripts/adapter_templates/` provide thin authored package guidance.
3. Existing generators produce local runtime state and public adapter output from canonical skill guidance. After `.codex/skills/` is untracked, non-release local mirror validation uses temp-output generation rather than tracked-file drift comparison.
4. For local Codex use in the transition-release model, contributors use the public Codex adapter path and install or copy public Codex adapter skills into ignored `.codex/skills/` local runtime state.
5. OpenCode command aliases are generated prompt wrappers for a curated lifecycle command set and remain derived from canonical skill inclusion decisions.
6. While public adapter skill copies remain tracked, adapter validation and release verification keep checking tracked adapter drift.
7. For the `v0.1.1` transition release, release validation checks canonical `skills/`, tracked public adapter output under `dist/adapters/`, adapter manifest and install guidance, tracked release notes, token-cost metadata, and `.codex/skills/` tracked-state absence. It does not build or structurally validate `.codex/skills/` as release evidence.
8. For the `v0.1.2` archive-introduction release, release artifact preparation generates separate per-adapter archives for Codex, Claude Code, and opencode, may generate an optional combined archive, records tracked adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml`, and keeps tracked public adapter skill bodies available.
9. Release validation for the archive-introduction release checks canonical skills, tracked adapter output, generated adapter archives, adapter artifact metadata, checksums, token-cost evidence, tracked release notes, install guidance, and the retained compatibility path.
10. For the `v0.1.3` public adapter untracking release, repository-tree adapter package fragments under `dist/adapters/<adapter>/` are retired. Complete packages are generated into temporary or release-output directories and published as release archives.
11. Adapter validation checks generated temporary or release artifact output instead of tracked public skill-copy drift.
12. Release validation checks manifest shape, generated output structure, archive structure, artifact metadata, checksums, tracked release notes, root guidance alignment, token-cost evidence, smoke evidence, and security constraints. For `v0.1.3` and later, release validation fails if tracked generated public adapter skill bodies remain under `dist/adapters/**/skills`.

### CLI target-native installation and release smoke

[Installation’s Runtime View](../../design/cli/installation.md#runtime-and-deployment) owns `init codex` and `init claude`: verify the selected archive, preflight every candidate skill directory/file, report all existing units as conflicts, or replace complete conflicting units with explicit `--force`. Project state is neither inspected nor written. Shared command/result envelopes remain with CLI. [Release](../../design/engineering/release.md) requires actual packed and public installation proof and retains publication authority.

### CLI new-change flow

1. A user runs `rigorloop new-change <change-id> --title <title>` from the same `@xiongxianfei/rigorloop` CLI package boundary.
2. The CLI validates public option values before planning filesystem writes: `<change-id>` must be a single safe path segment, `--type` must be a lowercase classification token when supplied, `--risk` must be `low`, `medium`, or `high`, and unsupported profiles or missing required inputs fail as invalid usage.
3. The CLI builds a non-destructive write plan for `docs`, `docs/changes`, `docs/changes/<change-id>`, and `docs/changes/<change-id>/change.yaml`.
4. The write plan reports existing directories, planned directories, planned files, and blockers. It blocks before mutation on existing planned files, directory paths occupied by files or other non-directories, and symlinks at planned directory paths.
5. In dry-run mode, the CLI reports the plan using the stable JSON or human output contract and writes nothing.
6. In actual mode, the CLI creates directories before writing files and writes only `change.yaml` for this first slice.
7. If a mutation fails after earlier mutations, the CLI reports completed actions as `done`, the failed action as `failed`, names the failed path, does not claim artifact-pack creation success, and does not promise atomic rollback.
8. Generated `change.yaml` is deterministic UTF-8/LF YAML with the first-release required fields, empty `artifacts`, empty traceability arrays, and `review.status: pending`.
9. The command does not run validation, create durable Markdown reasoning placeholders, install adapters, mutate `rigorloop.yaml`, write `rigorloop.lock`, inspect Git or PR state, or claim lifecycle stage completion.

### Public npm publication flow

1. A maintainer prepares repository tag `v0.1.4` and release evidence for `@xiongxianfei/rigorloop@0.1.4`.
2. The release gate `bash scripts/release-verify.sh v0.1.4` owns release readiness and delegates to repository-owned checks.
3. Package-content validation inspects the packed npm tarball allowlist and forbidden paths before publication.
4. Packed-package smoke installs the generated `.tgz` into a temporary project and runs the installed `rigorloop` binary, not repository-local scripts.
5. Publication evidence selects exactly one mode: `trusted-publishing` or `bootstrap`.
6. In trusted-publishing mode, `.github/workflows/release.yml` publishes through npm trusted publishing/OIDC after release verification, package-content validation, and packed-package smoke.
7. In bootstrap mode, used only if trusted publishing cannot claim the unpublished package, `release.yml` or `release-verify.sh` still owns readiness but a maintainer manually publishes the exact tarball whose filename, SHA-256, source commit, pack command, package-content result, and smoke result are recorded.
8. The publication process records npm package URL, source commit, selected mode, trusted publishing or bootstrap details, provenance status when available, and rollback/deprecation notes.
9. FU-010 remains open until actual non-dry-run `init --adapter codex --json` succeeds from the packed or published package against the official `v0.1.4` Codex adapter archive. Dry-run smoke is not enough.

### Governed lifecycle CLI flow

1. A human, governed skill, workflow operation, adapter, or CI requests read-only status/context/validation or submits a versioned semantic mutation request.
2. The CLI resolves the repository and exact change, rejects unsafe paths or ambiguous selection, detects incomplete recovery state, and builds one immutable snapshot.
3. The pure engine checks compatibility, closed vocabularies, artifact and evidence identities, invalidation outcomes, current effective state, operation authority, and expected lifecycle revision.
4. Read-only commands render human and JSON views from the same result. A rejected mutation returns stable diagnostics without changing tracked bytes.
5. An accepted mutation produces a deterministic candidate and operation fingerprint. The transaction adapter validates the candidate before replacement.
6. The adapter atomically creates `.rigorloop-lifecycle.lock` beside the change record, then creates and syncs `.rigorloop-lifecycle-recovery.json` in `prepared` phase before replacing `change.yaml`; both transient files use mode `0600`.
7. After replacement, the adapter records `replaced` and verifies the persisted state. Verification failure restores and verifies prior bytes. Failed restoration leaves recovery blocked; only `validate` and named `reconcile-interrupted-replace` repair are admitted. Cleanup removes recovery before lock.
8. For milestone completion, the engine stores a normalized completion-evidence record and fingerprint under the milestone's lifecycle registration. Completion closes and reports successor eligibility but leaves every workflow-stage projection unchanged.
9. Workflow independently decides whether to continue. If it selects the successor, it submits a separate `start-milestone`; the engine validates the exact current planned milestone and atomically synchronizes every present authoritative routing projection without scheduling or invoking the stage.
10. A stale original request always fails. An equivalent completion request against the current revision returns `already-recorded` only after the engine rereads and revalidates the stored proof, receipt, canonical review-log occurrence, packet inventory, review facts, milestone, and authority. Omitted or drifted evidence fails unchanged.
11. No lifecycle command chooses a route, schedules another stage, or crosses the PR, push, release, deploy, or merge boundary.

### CLI observable invocation flow

1. The entrypoint resolves strict logging options and a random invocation ID without persisting raw argv or arbitrary environment values.
2. The invocation controller classifies one closed command family, records monotonic start state, and attempts one schema-v1 start event through the file and console thresholds.
3. The selected semantic handler runs independently and returns one normalized internal result. Logging availability cannot change its mutation, status, or exit class.
4. One selected renderer writes exactly one semantic stdout projection. Existing v0.4.x renderers preserve their compatibility contracts; new concise and detailed formats project the same result.
5. The controller derives an allowlisted completion event, attempts one terminal append, and returns the semantic exit code. Interruption may leave only the start event.
6. The sink acquires its fixed lock, revalidates owned paths, rotates within five files when required, writes one complete JSON line synchronously, and releases the lock. Failure or bound exhaustion degrades diagnostics without retrying the semantic command.
7. `logs show` scans the same five files for an exact validated invocation ID, ignores its own different invocation ID, returns only validated matching events, and never reconstructs or reruns the original operation.

## Deployment View

RigorLoop has no deployed service, database, or runtime infrastructure for this architecture method. The deployment boundary is repository packaging and publication.

Authored content is reviewed in Git and distributed as repository files. Generated guidance is produced from canonical sources by existing repository generators. Tracked generated surfaces are validated for drift while they remain tracked; untracked generated surfaces are validated through temporary output or release artifact output. GitHub Actions do not own validation behavior; they set up execution and delegate to repository-owned scripts.

### Published-skill target deployment boundary

Gate A runs against repository-owned canonical skill roots and packaged resources.
Gate B generates local temporary or release-output packages and archives for Codex, Claude Code, and opencode, then proves inventory, mapped paths, declared transformations, archive contents, and untransformed byte identity for each target.
Gate B does not install or start a target runtime.

Gate C consumes current Gate A and Gate B proof plus a local release candidate's version, package metadata, checksums, tracked release notes, archive inventory, generated-package freshness, and rollback consistency.
It may be a thin release composition command, but it does not copy canonical-skill or adapter-parity rules.

Installer materialization is outside the normal gate chain unless inspected installer branches perform RigorLoop-owned filesystem logic beyond copying Gate B-proved content.
When required, smoke runs against a local package in an empty temporary directory, inspects only filesystem results, and ends before Codex, Claude Code, or opencode starts or receives a prompt.

Existing all-target clean-install, live-registry smoke, Codex benchmark, selector, cache, scheduler, and broad-smoke paths remain transitional execution surfaces only while their active contracts and protected failures await slice-owned disposition.
No retirement slice may remove them until old-versus-replacement proof and rollback are recorded.

For `code-review`, `SKILL.md`, the boundary reference, the conditional automation reference, and both structural assets deploy as one package revision. Generated targets may not mix old inline procedure with a new reference or vice versa. Every supported target, including a pure-copy install, is materialized into a temporary tree and checked for mapped-resource inventory, relative paths, and raw-byte identity. The proof ends at filesystem identity and never invokes Codex, Claude Code, opencode, or another model runtime.

For `route`, `SKILL.md`, the boundary reference, the governed lifecycle reference, and the bounded automation reference deploy as one package revision. Generated, archived, and installed targets may not mix old inline procedure with new conditional references or combine resources from different package versions. Existing mapped-resource inventory, containment, relative-path, and raw-byte parity checks remain the deterministic deployment proof; semantic assembly and ownership remain review evidence. The proof ends before any target runtime starts or receives a prompt.

The main execution and publication boundaries are:

- local contributor shell: runs selector, CI wrapper, validation, change-record query helper, generation, and drift checks;
- CLI package execution: runs the additive `rigorloop` command from a local package artifact, local/global install, or future npm package; the package is a delivery mechanism and not a canonical workflow source;
- npm registry: public delivery boundary for `@xiongxianfei/rigorloop`; the registry serves the CLI package, but canonical workflow content, skills, schemas, templates, adapter definitions, and release evidence remain repository-owned;
- routine release evidence: `docs/releases/v<version>.md`, a version-scoped standing process record for release type, version decision, gate status, package contents, publish event, registry verification, emergency deferrals, recovery notes, and follow-up;
- release transaction profiles: `docs/releases/profiles/<tag>.yaml`, durable version-scoped transaction records that drive routine release version state, target support, publication requirements, evidence classes, generated prep surfaces, validator expectations, and timing requirements;
- downstream change metadata scaffold: `docs/changes/<change-id>/change.yaml` created by `rigorloop new-change`; it is draft traceability state and not proof that proposal, review, verification, or PR stages are complete;
- governed lifecycle state: `artifact_states` and `workflow_state` in
  `docs/changes/<change-id>/change.yaml`, plus one bounded automation target;
  this repository-local YAML is mutable workflow state, while linked Markdown
  artifacts remain stable intent or stage-owned evidence;
- legacy automation evidence: retired `workflow.autoprogression` records remain read-only compatibility inputs and historical audit evidence during migration;
- GitHub Actions: runs the same repository-owned scripts in hosted CI when configured;
- local validation execution cache: untracked branch-local, worktree-local, and change-local state that can speed eligible repeated local validation but is not portable and is not lifecycle evidence;
- local CLI diagnostic logs: user-scoped JSON Lines under the platform state/log directory or an explicit safe override, bounded to one active file and four archives; they are disposable observability state and never repository, review, lifecycle, CI, or release evidence;
- local Codex runtime state: `.codex/skills/`, ignored by Git and installed locally from public Codex adapter output when contributors need local Codex use;
- public adapter packages: tracked `dist/adapters/` output during the compatibility window through `v0.1.2`, then generated temporary or release-output packages and release archives for `v0.1.3` and later;
- mapped skill-local resource parity: canonical `skills/<skill>/` resources, generated adapter output, locally packed release candidates, and adapter archives preserve skill-root relative paths and raw-byte SHA-256 unless an explicit transformation contract applies; installed-tree inspection remains only for additional materialization behavior not proved by package parity;
- progressive boundary resource package: every governed target skill contains
  `references/boundary-first-method-v1.md`; only feature-contract targets also
  contain `references/boundary-first-feature-authoring-v1.md`; only proof-map
  targets also contain `references/boundary-first-proof-v1.md`;
- boundary resource and activation manifests:
  `specs/boundary-first-resources.yaml` owns the closed projection matrix, and
  `specs/boundary-first-activation.yaml` binds its raw-byte identity, the
  complete projection-set identity, activating release, rollback release, and
  frozen grandfathering baseline provenance and inventory;
- checked-revision activation snapshot: reviewed repository sources,
  mappings, projections, scripts, fixtures, selector policy, and one coherent
  pending or active activation record validated entirely from current files;
- activation authoring input: one exact full reviewed pending-revision commit
  identity, used during authoring only to derive and freeze the historical
  feature-spec inventory without becoming a recurring validation dependency;
- routine `v0.4.0` release transaction: the existing release profile,
  preparation, preflight, full release gate, trusted immutable-tag workflow,
  GitHub/npm publication, public target smoke, and rerunnable closeout;
- derived boundary proof set: temporary generated adapter trees, packed
  candidates, release archives, clean installed targets, and their identities;
  these prove the checked and reviewed package revision but remain generated
  or release output;
- adapter support metadata: `dist/adapters/manifest.yaml` and `dist/adapters/README.md`, tracked guidance and support surfaces rather than authored skill bodies;
- adapter artifact metadata: `docs/reports/adapter-artifacts/releases/<version>.yaml`, tracked release evidence with source commit, generator command, required per-adapter archive list, optional combined archive details, checksums, install roots, and validation result;
- adapter release artifacts: generated per-adapter archives, plus optional combined archive, uploaded as release assets rather than committed by default;
- bundled CLI adapter metadata: official adapter artifact metadata included in the CLI package for compatible supported adapter releases so local archive installation can verify one user-supplied archive without a separate metadata flag;
- downstream project manifest: `rigorloop.yaml` written at the target project root only when `rigorloop init <target> --write-state` is requested; schema v2 records target-oriented `targets` and does not claim workflow readiness;
- downstream project lockfile: `rigorloop.lock` written at the target project root only when `rigorloop init <target> --write-state` is requested after verified target installation; schema v3 records `generated.targets`, while legacy schema v1/v2 state remains compatibility input rather than canonical output;
- downstream runtime adapter roots: `.agents/skills`, `.claude/skills`, `.opencode/skills`, and `.opencode/commands` inside a user project; these are installed generated output, not authored RigorLoop source;
- durable reports: `docs/reports/`, authored from local measurement evidence and linked from change-local artifacts when produced by a change;
- validation cache evidence: `docs/changes/<change-id>/validation-cache-evidence.yaml` for formal cache-hit claims and `docs/changes/<change-id>/validation-cache-measurement.yaml` for Workstream A measurement;
- token-cost benchmark fixtures: `benchmarks/token-cost/`, authored prompt and fixture inputs used to exercise public skills in a downstream-style project;
- token-cost temporary runs: isolated directories under system temp or `$RUNNER_TEMP`, disposable and not durable release evidence;
- token-cost release evidence: `docs/reports/token-cost/releases/<version>.md`, `docs/reports/token-cost/releases/<version>.yaml`, and tracked raw or sanitized run summaries under `docs/reports/token-cost/runs/<version>/`;
- release evidence: tracked `docs/releases/profiles/<tag>.yaml`, `docs/releases/v<version>.md`, `docs/releases/<version>/release.yaml`, release notes, generated pending/publication evidence, timing evidence, and maintainer smoke evidence used by release verification.
- npm publication evidence: `docs/releases/v0.1.4/npm-publication.md`, recording selected publication mode, tarball identity, package-content checks, packed-package smoke, trusted publishing or bootstrap details, npm package URL, and real Codex install smoke.

Rollback before public adapter skill-copy untracking keeps `dist/adapters/**/skills` tracked and defers archive publication or fixes archive metadata, install docs, and validation before release. Rollback before `v0.1.3` publication may regenerate and restore tracked adapter output from `skills/` if the release cannot validate generated packages or archives. Rollback after public adapter skill-copy untracking preserves generation from `skills/` and either republishes release artifacts from last known good generated output or uses a later approved recovery release. No runtime data migration is required.

Rollback before public CLI publication removes or disables the package candidate and leaves existing release-archive install guidance and repository scripts unchanged. Rollback after public CLI publication uses a fixed patch release plus documentation or deprecation of the bad version; published npm versions are not mutated in place.

## Crosscutting Concepts

### Source of truth

[Design](../../design/skill/authoring/design.md) owns living-model conventions and their validation mapping. [System](../../design/system.md) owns system composition; [Workflow](../../design/skill/workflow.md) coordinates actors and [CLI](../../design/cli/cli.md) owns recording mechanics under [Record Format](../../design/cli/records.md). Unmigrated details retain their declared source contracts; historical package/ADR evidence grants no second current owner.

### Smallest sufficient Design scope

Use Design’s owner-selection and scoped legacy-source method. A change updates only its justified affected responsibilities and interactions; significant decisions belong to the owning model. Unsettled product direction returns to Proposal, and an unmigrated source retains its contract until explicitly consolidated.

### Lifecycle status

For governed changes, lifecycle status is stored in the matching
`change.yaml` artifact-state entry rather than in the governed artifact.
Authoring and review peers own only their closed matching transitions.
Historical pre-adoption artifacts may retain embedded status as read-only
evidence.
Terminal or superseded state preserves replacement and closeout evidence.

### Validation layering

The selector owns routing and stable check IDs. Validation scripts own proof work. Manual review owns C4 diagram sufficiency, arc42 completeness, ADR need, and architecture package shape until a later approved automation contract changes that. Architecture support paths may select lifecycle checks for deterministic CI routing, but that routing is not architecture-package enforcement.

Validation output is part of the proof surface. Default human-readable output should scale with actionability rather than work volume: success output records status, identity, counts, and duration; failure output records responsible checks, names, messages, locations when available, and reliable rerun guidance when available. `--verbose` is the explicit expansion path for full passing detail. `--quiet` suppresses successful script output only and must not hide failure reasons.

For change-record evidence, the selector's routing responsibility includes registered evidence-class matching. `manual-routing-required` is a diagnostic and registration-debt signal for deterministic in-repo evidence, not a durable CI workaround. The query helper belongs beside validation scripts but has a separate role: it reads bounded metadata slices and must not run proof commands.

Validation idempotency is a proof-preserving optimization layer inside validation execution. It may skip work only when the eligible validator's complete input surface, canonical normalized command, implementation manifest, policy/config manifest, and previous actual-run passing result trace are unchanged. It does not change selector routing, selected check IDs, validator semantics, failure detection, exit codes, or closeout requirements.

The helper mode is an adoption surface, not an expansion of cache power. It makes the safe inner-loop path short enough to use, while preserving direct actual-run validation for closeout and final gates. Formal helper evidence records both the user-visible helper command and the canonical direct command used for cache identity so reviewers can see what was invoked and what prior pass was reused.

The local execution cache is an optimization surface, not evidence. Formal cache-hit evidence is change-local YAML that explains why the prior pass still applies. Closeout gates require actual-run evidence and reject cache-only pass claims. Workstream B edit-scoped validation is a separate future architecture decision because it would reduce selected validators based on changed inputs rather than identical input surfaces.

Lifecycle-state consistency is a bounded validation responsibility.
Validation reads exact `artifact_states`, `workflow_state`, automation-target,
and linked-evidence fields rather than arbitrary prose.
Plans and `docs/plan.md` are stable intent and navigation, not projections of
mutable current state.
Review logs, review resolutions, implementation evidence, explain-change,
verify, and PR evidence retain their narrower stage ownership.
Unknown values fail before consistency checks, and contradictory or stale
evidence blocks downstream reliance.

### Unified workflow automation policy

Workflow automation is opt-in and change-local.
`bounded-review-fix` remains the only writable mechanism, and one structured
target records the requested stopping point.
That target is sufficient public consent for repository-local prerequisite
stages through the target; it is never authority for PR creation, push,
publication, deployment, merge, credentials, destructive Git, or another
external mutation.

The architecture has no parent-authorization, effective-capability,
activation-selector, risk-profile, or selector-ledger layer.
Before every invocation, workflow checks current prerequisites, exact
artifact or milestone identity, the target boundary, and the invoked stage's
fixed write ownership.
Future stages are not marked ready or complete early.

Review stages remain distinct peers.
They write durable formal evidence before settling only the matching artifact
entry.
Direct review-only requests remain isolated.
Workflow reads settlement and selects routing but cannot create a verdict. The lifecycle CLI applies only the selected closed routing operation after validating the current state.

Resume is evidence-first and transition-scoped.
An identical interrupted review settlement may reconcile idempotently;
conflicting review identity or evidence fails closed.
Legacy profile, plan-owned, and artifact-local state remains read-only
compatibility evidence after a one-way migration.

### Ordered final-review stage evidence

The canonical pre-verify identity is a four-part model:

```text
reviewed subject revision S
final-review recording revision R
explanation recording revision E
handoff revision E
```

Git derives `R` and `E` after their commits exist; no tracked artifact embeds its own commit identity. The final reviewed diff remains base-to-`S` and excludes later stage evidence.

`R` and `E` are composition boundaries, not new write owners. The review peer, explain-change, and workflow each retain their stage-owned writes. A commit may contain outputs from more than one existing owner only when each changed path and each changed field is in that stage transition's closed set. Validation compares the actual Git diff with the expected per-revision manifest and rejects whole-file allowlisting for shared lifecycle state.

The protocol permits one recoverable partial state: current exact `S -> R` with no competing change may continue by producing `E`. It does not permit rollback, adoption of an unrelated commit, reordered evidence, merge ancestry, or a broader evidence tail. Later verify evidence is downstream of `E` and does not make the explanation self-stale.

### Plan baseline and state ownership

The stable plan artifact owns ordered execution intent, completion criteria, required evidence, and review handoff. `change.yaml#workflow_state.planned_work` owns current milestone and closeout state. New writers emit no mutable milestone-state or progress fields in plan bodies. Readers may accept compatible historical plan structures, but historical embedded state never overrides or repairs governed live state.

Stable plan identity remains artifact ID, kind, role, and normalized path. Reviewed revision identity remains the durable review ID, round, record path, reviewed artifact path, and reviewed repository revision or commit. After governed lifecycle CLI activation, separate exact content identities participate in evidence freshness and lifecycle revision; they do not replace stable artifact identity or prove writer identity.

After initialization and settlement, changes to milestone ID, order, kind, completion criteria, or required evidence require a governed replan or explicit workflow-owned migration. Ordinary plan authoring cannot replace or update existing `planned_work`.

### Published skill resource integrity

[Skill](../../design/skill/skill.md) owns the common resource contract, including complete maps, raw-byte identity, explicit transformations, precise lint/enforcement populations and the distinction between runtime fallback and package validity. SKL-DEC-02 preserves the resource-integrity decision; [archive navigation](../../archive/skill-model/2026-09-08/README.md) preserves original ADR bytes and related history. Existing validation, distribution and installation owners consume this contract and retain their separate proof and execution authority.

### Code-review package composition

The `code-review` common path follows a universal-before-conditional rule. Anything needed to classify the invocation, resolve authority, produce native findings or statuses, record a formal review, stop safely, constrain claims, distinguish milestone and final review, or choose a downstream handoff remains in `SKILL.md`. Only procedure unique to an already-proved workflow-managed automation mode may live in the conditional reference.

Assets are structural leaves: the skill may copy and fill them, but they cannot determine policy, status, severity, recording, or routing. References are packaged procedure, not independent lifecycle owners. This keeps the governing published skill equal to the complete mapped package while retaining `code-review` as the sole semantic owner.

Simplification evidence has two distinct scopes. Common-path lines, words, and tokens estimate ordinary loading cost; total package words and tokens expose the true maintenance footprint. The 35–45 percent range is planning evidence only. Architectural acceptance depends on one owner per repeated rule, complete ledger disposition, material common-path reduction, canonical, generated, packed, and temporary installed-tree parity, and independent semantic preservation.

No new service, persistent state, selector, scheduler, cache, validator family, runtime journey, transcript grader, or model matrix is introduced. Existing deterministic owners may gain focused fixtures only for invariants they already own.

### Workflow package composition

The `workflow` package follows universal-before-conditional classification.
Anything needed to classify an invocation, apply source precedence, reject unknown artifacts or stages, preserve manual isolation, constrain mutation and claims, stop safely, select resources, or report the next handoff remains in `SKILL.md`.
Governed lifecycle, bounded automation, and guide-authoring references own only the detailed procedure activated by their exact evidence predicates.

Reference dependencies are one-way.
Automation consumes governed lifecycle applicability and transition decisions.
Guide authoring renders established policy into project guidance.
Neither may override its upstream owner, and contradiction stops as a package defect.
The skeleton remains a structural leaf.

Automation-command context is separate from armed authority.
New-target bootstrap is transient and persists state only after governed identity validation.
Stateless status and off commands return `no-active-run` without state creation.
These loading rules refine skill-package composition without changing the accepted `change.yaml` schema, automation persistence owner, lifecycle transition model, or stage write boundaries.

Required references are not convenience fallbacks.
When their trigger is true, absence, unreadability, contradiction, or mixed package identity stops the affected operation.
The common path cannot reconstruct intentionally disclosed procedure.
Existing resource-integrity and adapter parity owners prevent incomplete distribution, while the runtime stop rule contains an unexpected incomplete installation.

Simplification evidence separates loaded assembly size from total package size and separates semantic-rule disposition from literal compatibility.
The target percentage is advisory; architecture acceptance depends on material common-path improvement, preserved behavior, one policy owner per rule, deterministic complete-package parity, and independent semantic review.

### Progressive boundary-first guidance

Progressive boundary-first guidance specializes published skill resource
integrity without creating another semantic contract. The established
`specs/references/boundary-first-method-v1.md` path becomes the compact core.
Feature-authoring and proof semantics live in exactly one additional canonical
source each. Stage-specific workflow, mutation, review, stop, handoff, and
claim rules remain in the owning skill and approved specs.

`specs/boundary-first-resources.yaml` is the only resource-to-consumer
inventory. Its closed schema has exactly `schema_version`,
`contract_version`, and `resources` at the top level and exactly `id`,
`source`, `target`, and `consumers` per resource. ADR-20260729 fixes the three
resource IDs, paths, order, and consumer lists. Projection and validation code
interpret that schema and fail closed before consistency checks on unknown,
missing, or duplicate fields, entries, paths, or consumers. The projection-set
digest covers every expected skill-local target using sorted POSIX path and
raw-byte digest records. The activation manifest separately binds the raw-byte
manifest identity, retaining the established compact-core compatibility
fields.

The four compact questions live directly in each governed skill so a
non-behavior decision does not require a portable-resource read. Their
contributor source is one checked shared block; copied shipped text does not
expose repository-maintainer projection mechanics to users. Family resources
load only in their owning stages. Other stages consume exact stable-ID rows
from approved project artifacts and expand to the compact core only when the
cited slice is insufficient.

The approved usability-first release spec owns the closed `pending` and
`active` activation snapshots. The activation record is declarative: each
checked revision is judged independently, and validation makes no claim about
the state in earlier or later revisions. Active state binds release intent,
rollback, resource, projection, adapter, baseline-provenance, and frozen
grandfathered-inventory values without claiming public availability.

Activation authoring supplies the repository root and exact 40-character
lowercase reviewed pending revision to the repository-internal pure
`derive_grandfathered_specs(root, baseline_revision)` function in
`scripts/boundary_first_validation.py`. The function performs read-only Git
object inspection and returns `(sorted_paths, issues)` without writing files,
refs, or evidence. The activation implementation step records the successful
path tuple and supplied revision directly in the reviewed source change;
focused fixtures cover invalid, unavailable, malformed, unreadable, and
successful baselines. The function is not a public CLI and is never called by
normal `--check` validation. No activation writer, transition ledger,
candidate evidence, publication-readiness protocol, or remote-state cache is
introduced. Later checked-revision validation reads the frozen record and
current package identities only; it does not inspect history or require the
baseline to remain reachable.

Generated, packed, archived, and clean installed trees remain a derived proof
set bound to canonical resources and release metadata; they do not become
tracked activation or rollback state. Package rollback continues to use the
immutable `v0.3.6` adapter artifact metadata. Validation is read-only and does
not install, publish, write rollback state, retain a historical attestation
store, or treat external install trees as Git state.

Public `v0.4.0` availability remains a separate routine release claim. The
existing release profile, preparation, preflight, full gate, trusted tag
workflow, GitHub/npm publication, public target smoke, and rerunnable closeout
remain authoritative. The immutable tag identifies the exact reviewed release
commit; partial publication remains open and recovers through existing
closeout or fix-forward behavior rather than a custom atomic publisher.

Static resource and representative loading measurements are change evidence,
not runtime telemetry. A tracked fixture names the resources mapped, initially
loaded, and permitted for expansion by stage family. Reports record canonical
bytes, mapped counts, and representative loaded counts; hard context budgets
require a later approved contract.

### Project-map current-state orientation

Project maps are living orientation references. They are useful for locating likely modules, entry points, tests, CI surfaces, external boundaries, risks, and known gaps, but they do not outrank source, runtime configuration, schemas, build manifests, tests, CI workflows, or governing workflow artifacts.

The root map stays concise and remains the repository entry point whenever area maps exist. Area maps provide bounded depth only for durable repository boundaries and must be registered from the root map. Overlapping maps name the overlap and assign detailed ownership to one map to avoid contradictory parallel architecture descriptions.

Map trust is evidence-bound. Every map records freshness metadata, baseline, coverage, exclusions, and known gaps. Material current-state claims cite repository paths, observed and inferred claims remain distinguishable, and unknowns are recorded rather than silently filled. Intent artifacts such as proposals, specs, architecture plans, ADRs, and execution plans may explain expected or planned behavior, but they are not current-state proof.

Correction notes preserve downstream safety when a refresh finds the earlier map was wrong at its recorded baseline rather than merely stale. A correction note is result evidence, not a fourth map status.

The project-map skeleton owns reusable output structure only. Evidence ranking, inference policy, target-state classification, future-design prohibitions, handoff rules, and claim boundaries stay in `SKILL.md`; detailed refresh-trigger comparison, audit, and root/area coordination procedure stay in the mapped conditional reference. Neither packaged resource becomes an independent policy owner.

### Change-record catalog model

Change records are cataloged by evidence class and queried by bounded slices.
For governed changes, `change.yaml` is authoritative for artifact lifecycle,
workflow routing, planned-work state, blockers, closeout readiness, validation
inventory, summary metadata, and evidence links.
Durable rationale belongs to `explain-change.md`, and formal findings and
dispositions belong to review artifacts.
Full change-record reads remain valid for forensic reconstruction, disputed
evidence, selector debugging, migration checks, unsupported query shapes, and
whole-record review.

### Diagram source policy

[Design technical reasoning](../../design/skill/authoring/design.md#technical-reasoning-and-decisions) owns current text-source diagram selection and placement. Existing diagrams retain their historical identities and explanatory context; they do not impose a second current architecture layout.

### Generated output

Canonical skills and thin templates feed [Packaging](../../design/engineering/packaging.md). The retained package builder produces Codex and Claude Code archives in temporary or explicit safe output, never canonical or active skill roots. No separate local runtime mirror is generated. `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain the tracked support surfaces.

Historically, `v0.1.2` retained repository-tree packages for its archive compatibility window. From `v0.1.3`, public installation uses release archives and package validation uses temporary or release output. Historical release evidence keeps its original population and source basis.

### Release and adapter evidence

[Packaging](../../design/engineering/packaging.md) owns generated package identities and verification; [Release](../../design/engineering/release.md) owns candidate evidence, authorized publication and observed results. Current artifacts contain exactly the two supported target packages. Tracked metadata and checksums describe generated archives; builds and installation do not authorize publication.

The `v0.1.1` transition release does not require downloadable adapter archives. `dist/adapters/` remains the public adapter install path, and release notes or adapter docs state whether archives are absent or separately published. If a separate accepted plan publishes optional archives for `v0.1.1`, repository-tree installation from `dist/adapters/` remains the required public install path for that release and archive metadata becomes additional evidence rather than a replacement for tracked public adapter validation.

The `v0.1.2` archive-introduction release keeps repository-tree adapter packages for the compatibility window while publishing downloadable archives and metadata. For `v0.1.3` and later, release archives are the active install surface, `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain tracked, and generated adapter package contents are validated from temporary or release-output directories rather than tracked `dist/adapters/<adapter>/` package trees.

### CLI package and project scaffold boundary

The CLI package is an additive delivery surface. It can carry executable command code, small project scaffolds, and bundled official adapter metadata, but it does not own canonical workflow content, skill bodies, adapter generation rules, validation authority, or release readiness. Current installation and archive trust belong to [Installation](../../design/cli/installation.md); smoke and publication belong to [Release](../../design/engineering/release.md).

`rigorloop new-change` is also a scaffold command, but it scaffolds change-local traceability rather than project installation state. It creates only `docs/changes/<change-id>/change.yaml` in the first slice, with empty `artifacts`, `requirements`, `tests`, `validation`, and `changed_files` until later workflow stages produce real evidence. It deliberately omits `explain-change.md` and `artifacts.explain_change` so a placeholder file cannot be mistaken for durable reasoning.

The `new-change` mutation boundary is local and non-networked. It validates option domains and safe path segments before planning writes, blocks on symlinks and overwrite conflicts before mutation, reports every planned directory and file action, and uses the shared CLI JSON status and exit-code contract. Partial write failures are observable rather than atomic: already-completed actions are reported, the failed path is reported, and the command does not claim success.

Public npm publication is an approved deployment boundary for `@xiongxianfei/rigorloop@0.1.4` only when the npm publication spec is satisfied. The package may still be built and tested locally or from a packed artifact, but FU-010 closes only after public publication evidence and real Codex install proof exist. For the target-native `0.3.0` boundary, pre-publish release proof uses packed-package non-dry-run smoke for every supported target, and post-publish proof uses live registry/download smoke.

### Unified workflow automation boundary

The unified `bounded-review-fix` mechanism is a repository workflow component, not a new service, background worker, external scheduler, CLI deployment boundary, hosted PR actor, or release mechanism. It executes only inside an active workflow-managed interaction and composes existing stage skills, formal review surfaces, change-local lifecycle state, and repository validators.

Its persistence is change-local in
`docs/changes/<change-id>/change.yaml`.
The record separates `artifact_states`, `workflow_state`, and the selected
automation target.
Stage-owned Markdown evidence remains linked rather than copied into this
snapshot.

Authority is structural rather than selector-driven:

- authoring peers write their governed artifact, authoring evidence, and one
  matching authoring transition;
- review peers write review evidence and one matching settlement transition;
- plan initializes missing planned-work state once for a new primary plan;
- workflow selects routing and every later planned-work transition, and the
  lifecycle CLI validates and persists the selected closed operation;
- downstream stages write only their code or stage evidence; and
- every actor treats other governed artifacts and state entries as read-only.

One target is the complete repository-local continuation consent boundary.
The mechanism validates prerequisites and fixed ownership at each stage but
does not derive another capability, authorization class, risk profile, or
selector.
External actions remain prohibited.

Rollback is local and evidence preserving.
`off` cancels the run and retains artifact, review, transition, and stage
evidence.
Compatibility rollback may continue reading historical state, but no rollback
path restores retired plan, artifact, or profile writers.

### Governed lifecycle CLI boundary

`change.yaml` remains the sole Git-tracked mutable lifecycle snapshot. Semantic Markdown remains stage-owned. The lifecycle engine owns mechanical interpretation and transition calculation; the CLI transaction adapter owns local guarded replacement; workflow owns routing selection and continuation decisions; Git owns durable history and branch integration. The CLI may apply a route only as the deterministic result of a closed workflow-selected operation, never by choosing the operation or successor itself.

Completion and start therefore form a two-step protocol. Completion persists proof-bound settlement and reports eligibility while leaving routing unchanged. Start consumes workflow's explicit selection, validates the current planned implementation milestone and every present routing projection, then commits milestone and routing fields together or none of them. Completion replay is evidence-bound rather than status-bound: the stored normalized completion record and fingerprint are rederived from current repository bytes before idempotent success.

The lifecycle revision and artifact digests establish freshness, not actor attribution or cryptographic authorization. Exclusive local writing and optimistic revision checks cover ordinary same-worktree concurrency. Branch divergence remains visible as Git conflicts and requires normal integration policy.

Same-worktree serialization uses fixed transient siblings in the selected change directory. `.rigorloop-lifecycle.lock` is acquired by atomic exclusive create and is never stolen merely because time elapsed. `.rigorloop-lifecycle-recovery.json` has closed `prepared` and `replaced` phases and is reconciled under the lock before a new mutation. A live owner reports busy; an unverifiable orphan requires explicit dry-run plus named `clear-orphaned-lock` repair after recovery is settled.

Compatibility is gated in order: read-only interpretation, guarded mutation, canonical skill and adapter migration, CI parity, then mandatory enforcement. Until enforcement is activated, current validated direct mutation remains a compatibility path. After activation, rollback requires a coordinated compatible CLI, schema, skills, adapters, and CI release; repair never becomes an arbitrary setter.

This boundary amends ADR-20260729's no-hash and direct state-write mechanics for supported operations. It preserves one change-local state owner and the stage authority model: stages still own the semantic operation they may request, while the CLI alone derives and writes the lifecycle fields.

### Local CLI observability boundary

CLI diagnostics are machine-local, user-scoped, bounded, and non-authoritative. The invocation controller may observe only allowlisted normalized command and result facts. It cannot receive raw requests, arbitrary environment values, artifact contents, credentials, private network data, or absolute repository paths for event serialization.

The file sink validates one containment root and uses non-following inspection for its five log names and lock. New POSIX paths use restrictive modes; existing unsafe permissions or symlinks are refused without implicit repair. Rotation, corruption, contention, unavailable storage, and console configuration affect only diagnostic state. Explicit console level `off` suppresses even the guarded emergency diagnostic.

Result projection is downstream of semantic execution. Compatibility, concise, and detailed renderers consume one internal result and must agree on shared facts. The versioned benchmark corpus measures complete agent-facing interactions, including any follow-up lookup; it cannot become a substitute for semantic field-preservation tests.

### Independent adversarial review gate boundary

The independent adversarial review gate is a repository workflow and evidence contract, not a new service, background worker, database, hosted reviewer, or deployment boundary. It executes inside workflow-managed automation and uses existing formal review skills, change-local review artifacts, validation scripts, and the current `workflow_state`.

The orchestrator owns the review invocation manifest, initial-packet inventory, packet hash, prompt template version, reviewer context identity, risk-tier classification, phase receipts, normalized `review_gate_outcome`, second-review routing, and autoprogression handoff decision. These records are process evidence and must not contain private chain-of-thought or persuasive author self-assessment.

The reviewer owns independent defect discovery, severity, evidence, required outcome, confidence, stage-native verdict, clean-review sufficiency receipt, and prior-finding reconciliation. The reviewer does not see author hidden reasoning, desired approval outcome, validation-result summaries, evidence menus, implementation-stage safety narrative, prior finding content, or auto-fix budgets before recording the initial risk map.

Risk-tier classification is deterministic where possible from affected paths, review stage, configured triggers, and governing artifacts. Ambiguous matches fail closed to the higher tier. Author-provided classification may be input evidence only; it is not authoritative for handoff eligibility.

Review gate records use structured fields where possible, closed vocabularies for outcomes and phases, and bounded prose for evidence summaries and no-finding rationale. Structural validators can prove schema validity and phase ordering; sampled calibration audits remain responsible for detecting receipt boilerplate, prose misuse, and weak evidence quality.

Calibration is a separate evidence layer. Rollout samples at least 20% of standard-risk clean automated reviews with a minimum evidence floor, second-reviews all elevated-risk clean reviews, and records material disagreement, inconclusive outcomes, downstream escapes, seeded-defect recall, false positives, and clean-receipt quality by risk tier and review skill. Protected rotating fixtures are preferred for calibration runs when practical; public fixtures document defect classes without becoming the whole calibration corpus.

The gate preserves direct isolated and manual review compatibility. Direct
isolated reviews may still run under existing review recording rules without
changing workflow routing. Workflow-managed automated handoff cannot use
`L0`, missing manifests, missing phase receipts, insufficient clean receipts,
unresolved findings, failed second-review gates, or blocked/inconclusive
results as a clean advance.

### Requirement-fidelity gate boundary

The requirement-fidelity gate is a repository workflow and evidence contract, not a new service, background worker, database, hosted reviewer, or deployment boundary. It composes with workflow-managed automated reviews, formal review artifacts, skill guidance, validator scripts, and calibration evidence.

The workflow or pre-review stage owns applicability evidence: affected paths, matched path triggers, matched category triggers, `applicable` or `not-applicable` result, reviewer override direction, override justification, and review stage. Reviewer override is recorded evidence, not silent replacement of the computed result.

The reviewer owns spec-canonical judgment: relevant spec clauses, accepted or reviewer-authored decomposition, requirement properties, required surfaces, property-by-surface verification, validator assertion comparison, compressed-requirement risk, and either a requirement-fidelity receipt or material finding.

Applicable review packets order evidence from spec to artifacts: relevant spec clause, accepted decomposition if present, expected surfaces, implementation diff, validator assertions, validation evidence, then prior findings. This prevents implementation/validator agreement from becoming the implicit requirement source.

Validator pilots use shared property-list by surface-list matrices for selected changed contracts. The property and surface lists identify their normative source clause, protect closed lists from hand-compressed copies, and include missing-property negative fixtures or equivalent proof.

Requirement-compression calibration is distinct from independence calibration. Phase B uses quantified sampling for applicable receipts, reviewer-authored decompositions, and `not-applicable` receipts, and measures seeded compression-defect recall against named rotating corpus iterations. Public examples may document defect classes, but measured recall depends on rotating instances.

Rollback can disable the requirement-fidelity autoprogression gate while preserving the independent adversarial review gate, historical review evidence, and valid requirement-compression findings. Spec-derived constants that protect active validators should remain unless the governing spec changes.

### Public npm package boundary

The npm package is a delivery artifact for the CLI. It can include runtime CLI code, package metadata, package-local README and license files, and bundled official adapter metadata for the compatible Codex adapter release. It must not include adapter archives, generated public adapter skill bodies, repository lifecycle artifacts, tests, local fixtures, secrets, `.codex`, `.agents`, or generated adapter package trees.

Publication has one selected mode. Trusted-publishing mode uses `.github/workflows/release.yml` and npm OIDC. Bootstrap mode is a one-time manual publication path for `@xiongxianfei/rigorloop@0.1.4` only when trusted publishing cannot be configured before package creation. Bootstrap mode separates release readiness ownership from npm publish execution: `release.yml` or `release-verify.sh` owns readiness, and the maintainer publishes only the exact verified tarball recorded in publication evidence.

The npm package does not replace GitHub release assets for adapter archives. `rigorloop init codex`, `rigorloop init claude`, and `rigorloop init opencode` install generated target support from official GitHub release archives or verified local archives matched against package-bundled metadata.

### Release token-friendliness evidence

Public releases add a token-friendliness evidence layer beside adapter release evidence. Markdown reports are for reviewers; YAML metadata is for release gates. The first required runtime benchmark is Codex; Claude Code and opencode dynamic benchmarks remain optional until stable runners and comparable reports exist. Final public releases require `dynamic_runtime.status: pass` or a valid approved waiver. RC and draft reports may record `blocked` or `not-run` dynamic status only with structured incomplete-state metadata.

Raw Codex JSONL may be omitted when it is too large or sensitive, but durable evidence must remain structured through analyzer summaries or sanitized summaries. Release validation checks for raw JSONL or a valid sanitized substitute, not raw JSONL unconditionally.

`skill-token-runtime-v2` expands dynamic coverage with a required core suite, one-release transition carryover benchmarks, optional extended benchmarks, and changed-skill-required benchmarks. Optional benchmark problems remain warnings unless the benchmark is required by changed-skill policy or explicitly claimed as release coverage. Claimed optional coverage is gated coverage: missing, invalid, failed, not reviewed, or unwaived inconclusive claimed results block final release.

Release validation owns changed public skill detection and generated-adapter-to-canonical-skill tracing. Token-cost validation owns proving that the report satisfies the required benchmark context supplied by release validation.

Manual result-quality review is structured release evidence for v2. Required or claimed coverage must have passing result quality or a valid role-scoped waiver. Optional unclaimed failures and inconclusive results use stable warning codes and must not be summarized as passing coverage.

### Measurement reports

Reports under `docs/reports/` are durable authored evidence for longitudinal comparison. Token-cost reports live under `docs/reports/token-cost/` and summarize measured static skill cost, Codex session cost, tool-output amplification, top cost drivers, conclusions, and next actions. Release token-friendliness reports live under `docs/reports/token-cost/releases/` and compare against the previous public release report when one exists or declare the first report as the baseline. Change-local artifacts should link to these reports rather than duplicating their body.

Validation cache measurement lives under `docs/changes/<change-id>/validation-cache-measurement.yaml` for the implementing change. It records Workstream A cache-hit value, helper adoption, actual-run fallbacks, closeout actual runs, and remaining validation cost. That measurement is the required evidence gate before any future edit-scoped validation or broader cache-eligibility proposal can argue that riskier scope narrowing or expansion is worth pursuing.

### Review artifact closeout

Review records are authored change-local evidence. The review artifact validator checks structure, references, allowed dispositions, and closeout completeness; it does not decide whether a finding is substantively correct.

Clean formal review receipts are also authored change-local evidence. When no existing change root exists, an isolated or review-only clean formal review uses a minimal clean-receipt root containing `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`. That root omits `review-resolution.md` unless material findings, a blocking or revision outcome, or another approved review-resolution trigger requires it.

### Security and privacy

Architecture artifacts and diagrams must not include secrets, credentials, private keys, or machine-local debug-only data. When a change affects trust boundaries, permissions, data exposure, or secret handling, the relevant architecture section and diagrams should state that explicitly.

### Legacy architecture handling

The legacy normalization follow-on inventoried every current `docs/architecture/` file, merged accepted current content into this package, and archived the eight top-level legacy Markdown records. Those legacy records remain historical evidence only. That earlier eight-file normalization was not completion of living-Design consolidation; current method/composition ownership follows Design and System, while the unmigrated remainder stays explicit here.

## Architecture Decisions

- [Distribution decisions](../../design/engineering/packaging.md#architecture-decisions) preserve the five retired ADRs’ mapped rationale and current support boundary.
- [ADR-20260825: Local CLI Observability and Result Projection Boundary](../../adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md) establishes one invocation controller, allowlist event model, bounded synchronous local sink, shared result projection, and compatibility-gated concise-default decision.

- [ADR-20260824: Governed Lifecycle CLI Transaction Boundary](../../adr/ADR-20260824-governed-lifecycle-cli-transaction-boundary.md) establishes one lifecycle interpreter, versioned identity and operation contracts, guarded single-record replacement and recovery, validator convergence, skill-mechanics migration, and phased enforcement.

- [ADR-20260818: Ordered Final-Review Stage-Evidence Tail](../../adr/ADR-20260818-ordered-final-review-stage-evidence-tail.md) defines the exact `S -> R -> E` pre-verify revision protocol, path-and-field ownership, Git-derived identities, and interrupted-tail recovery.

- [ADR-20260813: Reviewed Plan Initialization and Settlement](../../adr/ADR-20260813-reviewed-plan-initialization-and-settlement.md) amended initialization timing while preserving the then-current single-state, stage-write, and no-hash boundaries; ADR-20260824 later revises hash and direct-write mechanics only for activated supported CLI operations.

- `docs/adr/ADR-20260428-architecture-package-method.md`: historical C4/arc42/ADR method; current reasoning and decision ownership is [Design](../../design/skill/authoring/design.md#material-decision-preservation).
- `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md`: historical surface-simplification decision; [Design](../../design/skill/authoring/design.md#material-decision-preservation) preserves its meaning and owns current model selection and scoped legacy treatment.
- `docs/adr/ADR-20260419-repository-source-layout.md`: repository source layout and canonical-source/generated-output separation.
- `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`: staged migration from tracked generated skill mirrors to untracked local mirrors and generated release artifacts.
- `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md`: one-package CLI boundary, bundled metadata for local Codex archive verification, planned lockfile-only behavior, and npm publication block.
- `docs/adr/ADR-20260516-rigorloop-npm-publication.md`: first public npm publication boundary, trusted-publishing/bootstrap modes, package-content proof, and real install closeout proof.
- `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`: change records as registered and queryable catalogs, with evidence-class selector routing and bounded query-helper reads.
- `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`: validation cache hits for unchanged explicit-path lifecycle inputs, with a cache-aware inner-loop helper mode, canonical direct-command cache identity, local-only cache state, formal cache-hit evidence, closeout actual-run gates, and Workstream B measurement gating.
- `docs/adr/ADR-20260623-published-skill-resource-integrity.md`: mapped skill-local resource integrity, bounded legacy-reference lint, raw-byte parity, packed clean-install proof, and runtime fallback/package-validity separation.
- `docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md`: superseded historical activation and rollback-transaction design.
- `docs/adr/ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md`: one reviewed release manifest, immutable source-control grandfathering baseline, existing adapter metadata, and read-only package rollback validation.
- `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`: compatibility-stable compact core, two owner-scoped family resources, declarative projection manifest, inline checked compact scan, representative loading evidence, path-owned selector routing, and one atomic rollback bundle. It revises only the resource-composition part of ADR-20260728.
- `docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`: superseded historical candidate and custom atomic-publication decision.
- `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`: active checked-revision snapshot validation, one-time explicit baseline derivation, automatic concise skill behavior, exact custom-path retirement, and reuse of the routine `v0.4.0` release workflow.
- `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`: superseded historical profile decision whose gate and review-independence rationale is retained through the unified mechanism.
- `docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md`: superseded historical profile decision whose risk separation, reviewer-owned correction, fresh verify, and stop-before-PR rules remain retained.
- `docs/adr/ADR-20260625-independent-adversarial-review-gates.md`: orchestrator-owned neutral review manifests, fresh-context enforcement, blind-first evidence staging, risk-tiered escalation, clean-review sufficiency receipts, second-review disagreement handling, and calibration for workflow-managed automated reviews.
- `docs/adr/ADR-20260626-requirement-fidelity-gate.md`: deterministic requirement-fidelity applicability, spec-canonical packet ordering, requirement-property decomposition, multi-surface property matrices, spec-derived validator assertion matrices, and compression-defect calibration for applicable automated reviews.
- `docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md`: superseded historical proposal-side profile decision whose nested writer is retired by the active stage-owned contract.
- `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md`: superseded historical consolidation decision whose one-target, review-independence, recovery, migration, and stop-before-PR constraints are retained without its capability and plan-owned-state layers.
- `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md`: active stage-owned lifecycle decision placing mutable artifact and workflow state in `change.yaml`, assigning peer transition ownership, keeping one target as sufficient repository-local consent, and removing capability, selector, hash, and write-interception layers.

No additional ADR is required for the 2026-04-29 package-quality refinement because it sharpens the accepted method without changing the durable architecture decision.

No additional ADR is required for `rigorloop new-change` because it is an additive command inside the existing CLI package boundary and does not introduce a new durable source-of-truth, packaging, release, validation, or persistence decision.

No additional ADR is required for the 2026-05-12 record-every-formal-review amendment because it refines the existing review artifact and workflow evidence architecture under the approved formal review recording spec. The durable rule is carried by `specs/formal-review-recording.md`, and this canonical package records the affected runtime and crosscutting architecture.

No additional ADR is required for the `v0.1.1` single-authored-source transition release because ADR-20260512 already records the durable generated-output and adapter release artifact migration. This package revision records the release-specific validation and packaging architecture for the transition window.

No additional ADR is required for script output optimization because it refines repository-owned validation output presentation inside the existing selector, test-runner, and CI-wrapper architecture. It does not introduce a new system boundary, persistence model, packaging model, release model, or durable source-of-truth decision.

No additional ADR is required for the evidence-bound `project-map` update because it applies existing published skill resource-integrity, generated-output, and living-reference workflow decisions to one skill and one packaged skeleton asset. The durable current behavior is carried by `specs/project-map.md` and this canonical package.

No additional ADR is required for project-map skill simplification because it applies the existing mapped-resource package and progressive-disclosure architecture to the current project-map capability. It changes no runtime, persistence owner, deployment topology, generated-output model, or independently governed policy surface; the amended `specs/project-map.md` and this canonical update carry the clarified operation, assembly, and transaction boundaries.

No additional ADR is required for workflow skill simplification because it applies the existing mapped-resource skill-package model to the current workflow component without changing the durable package model, `change.yaml` persistence, lifecycle ownership, runtime boundary, or deployment topology. The approved behavior is carried by `specs/workflow-skill-simplification.md` and this canonical package update.

No additional ADR is required for the milestone completion/start correction because ADR-20260824 already establishes workflow routing ownership, closed semantic CLI operations, exact evidence identities, deterministic replay, and single-record atomic mutation. This canonical update makes that existing decision operationally precise by separating completion from workflow-selected start and by defining the normalized milestone completion-evidence record; it introduces no new service, persistence owner, external authority, or deployment boundary.

ADR `docs/adr/ADR-20260729-stage-owned-change-local-lifecycle-state.md` is
required because this change replaces plan-owned live state and capability-
driven automation with one change-local lifecycle model and fixed peer-stage
write boundaries.
It supersedes the prior authority and state-placement decision
in ADR-20260721 while retaining that ADR's one-mechanism, structured-target,
review-independence, evidence-first recovery, migration, and stop-before-PR
constraints.

ADR `docs/adr/ADR-20260625-independent-adversarial-review-gates.md` is required because this change introduces a durable workflow orchestration and review-evidence decision: automated review handoff now depends on verifiable fresh context, orchestrator-owned neutral packets and phase receipts, risk-tiered review depth, second-review disagreement gates, and calibration evidence rather than same-context review prompts or finding quotas.

ADR `docs/adr/ADR-20260626-requirement-fidelity-gate.md` is required because this change introduces a durable workflow orchestration and review-evidence decision: applicable automated review handoff now depends on deterministic fidelity applicability, spec-first packet ordering, decomposed requirement properties, per-surface verification, validator assertion comparison against the spec, and compression-defect calibration rather than implementation/validator agreement.

ADR `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`
is required because this change revises durable validation and release
architecture. It replaces transition- and remote-dependent local activation
with independent checked-revision snapshots, makes one explicit reviewed
baseline an authoring-only input, removes the custom candidate and publisher
path, and restores the existing routine release workflow as the sole public
release authority. It supersedes ADR-20260805 while retaining the single
activation record, resource projection, package parity, and immutable rollback
decisions from ADR-20260728 and ADR-20260729.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Product-boundary determinism | A canonical skill or generated adapter package changes. | Gate A and Gate B decide acceptance from repository files, declared transformations, archives, and identities without a target runtime, prompt, transcript, model ID, or nondeterministic retry. |
| Cross-target package parity | A maintainer generates public adapters. | Codex, Claude Code, and opencode each have expected inventory, mapped resources, declared transformations, archive contents, and untransformed raw-byte identity proof. |
| Release composition | A local release candidate is verified. | Gate C requires current Gate A and Gate B proof, adds release-only checks, and reports the underlying failed owner without duplicating its semantic rules. |
| Retirement safety | A validation subsystem is proposed for removal. | Every protected fixture and failure has a recorded replacement or approved de-contracting, old and replacement proof are compared, unknown behavior pauses, and one recoverable rollback boundary is named. |
| Reviewability | A reviewer opens a PR that changes the canonical architecture package. | The affected arc42 sections, diagram source files, and ADR links are visible as repository text in the PR diff; no external binary diagram is required to review the change. |
| Traceability | A contributor changes architecture guidance for diagrams, skills, templates, or generated output. | The change links the accepted proposal, approved spec, canonical package update or explicit no-impact rationale, ADR decision if required, plan, test spec, and validation evidence. |
| Proportionality | A change needs architecture handling. | No-impact work records a rationale, clear current-architecture changes update this package directly, durable decisions create or update ADRs, and unsettled direction or behavior routes back to proposal or spec. |
| Determinism | Canonical skill guidance changes and generated guidance must be refreshed. | Generated local mirrors, public adapter output, and adapter release artifacts are produced from `skills/` through repository generators; tracked generated surfaces use drift checks and untracked generated surfaces use temp-output or release-artifact validation. |
| Adapter artifact reproducibility | A maintainer publishes generated adapter archives. | Tracked adapter artifact metadata records source commit, generator command, archive names, SHA-256 checksums, validation command, and validation result. |
| Transition release compatibility | A maintainer prepares `v0.1.1`. | `release-verify.sh` delegates structured checks to `validate-release.py`; release validation proves canonical skills and tracked public adapter output are current, release notes and adapter docs describe the transition, token-cost metadata uses public adapter output, and `.codex/skills/` is only checked for ignored/untracked state. |
| Public adapter untracking | A maintainer prepares `v0.1.3`. | Release validation proves no tracked generated adapter skill bodies remain, `dist/adapters/README.md` and `manifest.yaml` remain tracked, generated temporary or release-output packages validate, release archives validate, metadata and checksums validate, and root guidance no longer advertises retired repository-tree adapter skill bodies as the active install model. |
| CLI init safety | A user runs default `rigorloop init codex` in a project with existing files. | The CLI builds a write plan, refuses user-file overwrites by default, verifies bundled metadata and archive contents before extraction, preserves existing state files byte-for-byte, performs required safety reads before target-root mutation, and reports success/block/error through the stable command contract. |
| Multi-target init safety | A user runs `rigorloop init codex`, `rigorloop init claude`, or `rigorloop init opencode`. | The CLI selects an explicit internal descriptor, verifies a trusted release or local archive, installs only descriptor and metadata-selected roots, rejects unsupported targets and `--adapter` before mutation, and does not create state files by default. |
| Managed state opt-in | A user runs `rigorloop init codex --write-state`. | The CLI writes target-oriented `rigorloop.yaml` schema v2 and `rigorloop.lock` schema v3 only after verified install; new user-visible schema keys do not use `adapter` or `adapters`, and historical archive filename values may remain unchanged. |
| Release smoke fidelity | A maintainer prepares the target-native `0.3.0` release. | Packed-package pre-publish smoke and live registry/download post-publish smoke run real non-dry-run init for `codex`, `claude`, and `opencode`; dry-run output alone is not accepted as install proof. |
| Routine release transaction safety | A maintainer prepares a routine release. | `docs/releases/profiles/<tag>.yaml` owns release state; `prepare-release` generates only profile-owned surfaces, preflight catches cheap deterministic drift, `release-verify.sh <tag>` remains the full gate, closeout writes validator-compatible public evidence, and timing evidence is recorded without weakening release checks. |
| CLI diagnostic isolation | The log directory is unavailable, unsafe, full, corrupt, or contended while a semantic command completes. | Repository bytes, semantic stdout, and exit status match logging-disabled execution; the invocation records diagnostics when possible or reports bounded degraded state without recursive failure. |
| CLI diagnostic privacy | A command contains a synthetic credential, private path, request body, control character, or environment secret. | The value is absent from stdout, stderr, active logs, archives, and lookup output; only closed normalized fields appear. |
| Concise-result compatibility | A v0.4.x caller and an opt-in concise caller execute the same fixture. | Existing defaults retain their contract, concise and detailed projections agree on shared facts, and a default switch remains blocked unless all six complete-interaction profiles pass the adoption gates. |
| Skill resource self-containment | A published skill maps a skill-local resource. | The resource exists in canonical source, generated output, locally packed release candidates, and clean installed target skill roots with matching relative path and raw-byte SHA-256 unless a transformation contract applies. |
| Boundary-resource proportionality | A governed stage makes a decision after the compact scan. | Non-behavior work loads no formal family resource; feature-contract stages map only compact and feature-authoring resources; proof-map stages map only compact and proof resources; other stages begin with cited approved rows and expand only when the slice is insufficient. |
| Boundary-resource parity | A maintainer changes a boundary resource or governed skill. | One declarative manifest projects exactly the owner-approved resources; canonical, skill-local, generated, packed, and installed Codex, Claude Code, and opencode trees retain the expected mapped path and raw-byte SHA-256 with no missing or additional layer. |
| Boundary activation safety | The repository records `boundary-first-v1` as pending or active. | Checked-revision validation accepts exactly one coherent snapshot and matching source, resource-manifest, projection-set, governed-skill, adapter, and rollback identities; missing, additional, malformed, unknown, mixed, or divergent values fail without history, tag, remote, or network requirements. |
| Activation baseline reproducibility | A maintainer authors the active snapshot. | The internal pure `derive_grandfathered_specs(root, baseline_revision)` function accepts the exact 40-character reviewed pending-revision identity, returns the complete raw-byte-sorted eligible inventory or bounded issues without writing, and the implementation freezes the successful input and output in the reviewed activation record. Normal `--check` validation never calls the function. |
| Checked-revision claim boundary | A reviewer evaluates active `v0.4.0` source before the tag exists. | Focused local validation reports active state and release intent while making no tagged, published, public, or publicly verified claim. |
| Routine release reproducibility | An authorized operator publishes the reviewed `v0.4.0` commit. | The existing profile, preparation, preflight, full gate, trusted tag workflow, package and adapter checks, public smoke, and rerunnable closeout remain authoritative; the immutable tag names the exact reviewed release commit. |
| Boundary rollback safety | A maintainer withdraws unpublished work or responds after public release. | Before publication, public state remains unchanged; afterward, read-only validation selects immutable `v0.3.6`, while partial publication uses existing closeout, dist-tag correction or deprecation when applicable, or a later patch without rewriting releases. |
| Boundary measurement usefulness | A contributor evaluates progressive loading before activation. | Evidence reports before-and-after canonical bytes, mapped-resource counts per governed skill, and representative initial and expanded loaded-resource counts by stage family; no hard budget is inferred from the baseline. |
| Project-map reliance safety | A downstream skill uses a project map to orient work. | The map exposes status, baseline, coverage, exclusions, known gaps, material path citations, inference labels, unknowns, correction notes when applicable, and configured-versus-executed command evidence; stale, partial, inferred, unknown, conflicting, or missing-path claims require direct source inspection before reliance. |
| Legacy resource migration safety | A skill contains legacy `templates/...` instructions outside the `Resource map`. | Bounded migration lint reports the unmapped skill-local resource reference without classifying ordinary artifact paths or examples as package dependencies. |
| opencode command alias integrity | A user installs opencode from an archive whose metadata declares command aliases. | The CLI installs `.opencode/skills` and `.opencode/commands` or fails verification; older compatible skills-only archives emit `opencode-command-aliases-not-declared` and record only installed roots. |
| CLI new-change safety | A user runs `rigorloop new-change <change-id> --title <title>` in a project with existing or missing `docs/changes/` paths. | The CLI validates the option domains, builds a write plan naming every affected path, blocks on unsafe change IDs, symlinks, existing planned files, and path-type conflicts, writes only `change.yaml`, and reports partial write failures without claiming success. |
| Lifecycle claim boundary | A user sees `docs/changes/<change-id>/change.yaml` created by `new-change`. | The generated metadata has empty artifact and evidence arrays, `review.status: pending`, and no `explain_change` artifact; file existence does not imply proposal acceptance, review completion, verification, or PR readiness. |
| Evidence routing determinism | A branch adds `docs/changes/<change-id>/behavior-preservation.md`. | The changed-path selector routes it through a registered evidence class before verify, or emits stable `manual-routing-required` registration debt. |
| Bounded readability | A stage needs the latest validation result or canonical artifact paths for a change. | `scripts/query-change-record.py` returns the requested slice without requiring full validation history or executing validation commands. |
| Cache-hit safety | A repeated explicit-path lifecycle validation command is requested after an unrelated edit. | Cache hit occurs only when previous result was `pass` and normalized command, input-surface hash, implementation hash, and policy/config hash all match; otherwise the validator runs. |
| Inner-loop helper adoption | A contributor repeats lifecycle validation after change-local evidence edits. | `--mode explicit-paths-inner-loop` supplies cache context by default, normalizes to canonical direct `--mode explicit-paths` cache identity, and records displayed helper argv separately from canonical cache argv in formal evidence. |
| Lifecycle-state consistency | A stage updates one artifact or workflow transition while its linked review, milestone, blocker, or closeout evidence is absent, stale, or contradictory. | Validation reports the exact entry and evidence mismatch and blocks downstream reliance; plans and governed artifacts remain unchanged. |
| Milestone continuation authority | A reviewed milestone completes while another implementation milestone is planned. | Completion closes and reports eligibility without changing routing; only a later workflow-selected `start-milestone` marks the successor implementing and atomically synchronizes every present authoritative routing projection. |
| Completion replay freshness | A caller retries completed milestone settlement after review evidence is omitted or an authorizing receipt, canonical review-log occurrence, milestone proof, or packet constituent changes. | Replay reconstructs the normalized completion record and returns `RL_STALE_EVIDENCE` without mutation; identity-equal facts return `already-recorded`, and unrelated review-log appends do not invalidate the canonical occurrence. |
| Unified automation single-write safety | A user starts or resumes workflow automation through a current or legacy command. | The command resolves to one structured target, writes routing only through `workflow_state`, and leaves retired artifact, plan, and profile state unchanged. |
| Published stage-ownership completeness | A maintainer adds or changes an automatable stage. | The canonical skill defines one fixed content, evidence, and lifecycle-state write boundary; workflow routing cannot widen it; generated adapters preserve it byte-for-byte or semantically as required by the adapter contract. |
| Artifact-state write isolation | Multiple peers participate in one lifecycle transition. | The author or review peer writes only the matching artifact entry; plan may initialize missing planned work once only from current clean review evidence; workflow coordinates and selects routing and later planned-work operations; the CLI validates and persists only those closed selected operations; any other cross-owner mutation blocks reliance. |
| Settlement-stable resume | Review evidence is durable but its matching settlement write is interrupted. | The same review identity reconciles idempotently; conflicting identity or evidence fails closed, and workflow never substitutes its own verdict. |
| Final-review tail integrity | Final review is recorded after reviewed subject `S`, followed by explanation and workflow handback. | Verify accepts only exact non-merge direct-child ancestry `S -> R -> E`; each revision matches its closed path-and-field set, and any broader or reordered state requires fresh final review. |
| Final-review tail recovery | Execution stops after exact final-review recording revision `R`. | Resume may create only the exact explanation-and-handback child `E`; changed basis, intervening commits, merges, or unowned fields stop without adoption or rewrite. |
| Reviewed plan activation | A clean primary-plan review precedes live work initialization. | Clean evidence leaves the plan `review-required`; plan initializes only the exact reviewed revision; identical review settlement retry activates it; no downstream route occurs earlier. |
| Target-bound execution | A run targets a later stage before its prerequisites exist. | The target remains sufficient repository-local consent, but workflow invokes only the current basis-complete stage and never widens that stage's fixed write boundary. |
| Interrupted-stage recovery | Execution stops after stage-owned output is partially or fully written. | Resume inspects the owning evidence, reconciles a complete idempotent transition, and pauses on contradiction or partial output rather than inventing completion. |
| Repeated-target identity | `code-review@M2` resumes after the active plan has advanced to M3. | The run remains bound to M2 and cannot silently reinterpret the target as M3. |
| External-action containment | Unified automation completes fresh verification. | The run stops at the verify target and performs no PR creation, push, publication, deployment, merge, destructive Git operation, or other external action. |
| Automated review independence | Workflow-managed automation invokes an automated review. | The review can advance only when the orchestrator records a valid manifest, verifiable initial packet, non-L0 independence level, phase receipts, risk-tier classification, stage-native verdict, and normalized `review_gate_outcome`. |
| Blind-first review safety | A rereview follows prior findings and existing validation output. | The reviewer records an independent risk map before validation-result summaries, evidence menus, implementation narrative, or prior finding content are released; later reconciliation may still record new, reopened, superseded, or failed-remediation findings. |
| Clean-review trustworthiness | An automated review reports no material findings. | A clean-review sufficiency receipt records inspected governing artifacts, risk classes, adversarial hypotheses, direct proofs or reproductions, evidence challenge, unreviewed surfaces, confidence, and no-finding rationale before handoff eligibility is considered. |
| Requirement-fidelity trustworthiness | An applicable automated review implements, validates, teaches, or preserves a normative spec clause. | The review records deterministic applicability, spec-first packet ordering, accepted or reviewer-authored decomposition, property-by-surface verification, validator assertion comparison against the governing spec, compressed-requirement risk, and a structurally valid requirement-fidelity receipt or material finding. |
| Requirement-compression calibration | A review-quality calibration run measures compression detection. | The run cites a named corpus iteration, seeded defect type, expected finding, observed finding, recall result, and rotation state; Phase B sampling meets the approved floor rates. |
| Second-review escalation | A sampled or required second reviewer disagrees with a first clean automated review. | Any material finding, blocked result, or inconclusive result prevents automatic continuation and routes to review-resolution, owner decision, or another authorized review without majority voting. |
| Closeout gate safety | A milestone closeout record cites only `cache-hit-inner-loop` evidence. | Lifecycle or change-metadata validation rejects the closeout because first-slice closeout requires `actual-run-pass`. |
| Local archive verification | A user runs `rigorloop init codex --from-archive <path>`. | The CLI verifies the archive against bundled official metadata for the installed package's compatible target release and blocks with `metadata-unavailable` if metadata is absent. |
| State determinism | A user reruns `rigorloop init codex --write-state` after a verified install with unchanged generated output. | The CLI computes the same normalized manifest hash and `rigorloop-tree-hash-v1`, preserves supported unrelated entries, and produces byte-identical target-oriented state content for identical state. |
| Lockfile schema compatibility | A user adds Claude Code or opencode to a project with a valid schema v1 or v2 lockfile. | The CLI verifies existing generated output against recorded hashes before migrating current state to schema v3; drift blocks before unrelated adapter mutation. |
| State drift safety | A user reruns `rigorloop init codex` after generated files under `.agents/skills` were modified while existing state records Codex. | The CLI reports drift with expected and actual tree hashes when available and blocks destructive replacement by default before target-root mutation. |
| Proxy diagnostic safety | A network archive download fails in a proxied environment. | JSON diagnostics expose only bounded fields and allowed enum values; human output recommends `--from-archive`; neither mode prints raw proxy values, credentials, private hostnames, request headers, or machine-local paths. |
| npm publication safety | A maintainer publishes `@xiongxianfei/rigorloop@0.1.4`. | Publication evidence records exactly one publication mode, package-content validation, packed-package smoke, trusted-publishing or bootstrap identity, npm package URL, and real Codex install smoke before FU-010 closes. |
| Standing release-process safety | A maintainer publishes a routine release after the release-process contract is active. | Release evidence under `docs/releases/v<version>.md` records release type, version decision, source commit, package identity, dist-tag, full gate, package preview, packed install smoke, publish path, provenance mode, registry verification, recovery notes, and follow-up without requiring a new proposal/spec/plan when no new decision is introduced. |
| Emergency deferral safety | A maintainer publishes an emergency release with a deferred gate item. | Evidence records owner approval, rationale, deferred item, validation impact, accepted risk, follow-up location, and deadline; non-deferrable evidence, secret suppression, package/source/version/dist-tag recording, publish-path recording, registry verification, and recovery/follow-up recording still pass. |
| Measurement usefulness | A contributor optimizes skill token cost. | Static skill measurement, JSONL analysis, and baseline reports identify measured cost drivers before hard token-budget gates are introduced. |
| Release token-friendliness | A maintainer prepares a public release. | Markdown and YAML token-friendliness reports exist under `docs/reports/token-cost/releases/`, Codex benchmark evidence or a valid waiver is recorded, portability passes, and release validation delegates to the token-cost report validator. |
| Dynamic benchmark coverage | A maintainer prepares a public release with `skill-token-runtime-v2`. | The report records required core coverage, transition carryover coverage when applicable, changed-skill-required coverage, claimed optional coverage, optional warnings, and per-run result-quality evidence. |
| Review closeout | Architecture-review records a material finding. | The finding includes evidence, required outcome, and a safe resolution path or `needs-decision` rationale before it drives fixes. |
| Script output actionability | A contributor runs `scripts/test-select-validation.py` or selected checks through `scripts/ci.sh`. | Successful default output is compact and count-bearing; failed output preserves actionable failure evidence; `--verbose` exposes suppressed passing detail; `--quiet` success is silent while non-success diagnostics remain visible. |
| Security | Architecture work touches trust boundaries, permissions, data exposure, or secret handling. | The relevant architecture prose or diagram states the boundary, and no artifact includes secrets, credentials, private keys, or machine-local debug-only data. |

## Risks and Technical Debt

| Risk or debt | Current handling |
| --- | --- |
| Existing contracts still require routing fixtures, runtime benchmarks, clean installs, selectors, caches, or schedulers | The approved simplification spec gives a narrow immediate disposition only for named skill-contract clauses; every other subsystem remains transitional until its slice records exact contract disposition. |
| Consolidation could move all complexity into one oversized validator | Gate ownership is separated by canonical skill, package, release, and lifecycle-governance invariants; semantic judgment is excluded and internal modules retain one parser owner per invariant. |
| A retired check may protect an undocumented failure | Retirement pauses on unknown fixtures or contradictory behavior and requires old-versus-replacement proof plus rollback before removal. |
| Review-owned semantic quality may vary by reviewer | Published-skill review uses one concise checklist for trigger clarity, ownership, prerequisites, procedure, resources, stops, claims, output, and handoff; material concerns use formal findings. |
| Shared `change.yaml` path allowance could conceal unrelated lifecycle mutation | Ordered-tail validation inspects the changed fields for `R` and `E`; path-only allowlisting is explicitly insufficient. |
| Completion could silently acquire workflow routing authority | Completion and start are separate operations; completion cannot change stage projections, while start requires workflow's explicit selection and validates all present projections before one atomic candidate is persisted. |
| Closed milestone replay could trust status while authorizing evidence drifted | The milestone registration stores a normalized complete evidence identity and fingerprint; every current-revision replay rereads proof, receipt, canonical log occurrence, packet inventory, review facts, milestone, and authority before idempotent success. |
| Evidence recording can become self-referential or self-stale | Git derives recording identities after commit, the explanation records content and reviewed-basis identities rather than its own commit hash, and verify keeps later evidence outside the pre-verify tail. |
| Target runtimes may interpret structurally valid skill text unexpectedly | Treat reported runtime behavior as a product defect to investigate without making routine LLM execution a repository acceptance oracle. |
| Archived legacy architecture documents can be mistaken for current architecture truth | Each archived record points to this canonical package, and final closeout validation covers every changed legacy document. |
| First implementation relies on review rather than structural package enforcement | Approved spec intentionally defers enforcement automation until a real package proves the shape. |
| C4 context and container views may be too coarse for future module-level changes | Add component diagrams only when container-level structure no longer explains affected responsibilities. |
| Architecture work can overproduce change-local deltas | Deltas are no longer a normal architecture authoring path; use no-impact rationale, direct canonical update, ADR, or proposal/spec routing instead. |
| Historical or exceptional change-local evidence could be mistaken for current truth | Architecture-review, code-review, and verify must treat durable current architecture truth outside the canonical package as incomplete. |
| Architecture-review finding format could be mistaken for a replacement of material-finding closeout | The focused spec and this package keep the simple finding fields separate from the repository-wide material-finding contract. |
| Token-cost reports could expose excessive transcript or command-output content | Measurement reports summarize cost drivers and avoid embedding unnecessary raw transcript content. |
| Raw Codex JSONL could expose sensitive local paths or output | Release metadata supports sanitized summaries, and analyzer summaries do not require private raw JSONL paths when raw evidence is intentionally omitted. |
| Local CLI diagnostic logs could expose private inputs or be mistaken for lifecycle evidence | Event construction is allowlist-only and cannot access raw requests or arbitrary environment data; logs remain outside the repository and are explicitly excluded from lifecycle, review, verification, and CI authority. |
| Synchronous diagnostic writes could delay routine commands under contention | Each event uses at most 10 lock attempts and 1,000 milliseconds total; exhaustion degrades diagnostics and preserves the semantic result. |
| Concise output could hide an actionable fact or shift cost into a second lookup | A closed field-applicability matrix and six versioned complete-interaction profiles gate adoption; detailed output remains available through the declared compatibility window. |
| Benchmark runners could accidentally measure the repository-local Codex mirror instead of public adapter output | The release benchmark installs public Codex skills from tracked public adapter output while available, generated temporary adapter output, or release artifact output, and rejects `.codex/skills/` as the public benchmark source. |
| Release metadata can become prose-only or unreproducible | Structured YAML records runner invocation, fixture source, public skill source, run evidence, waiver state, and comparison data; release validation reads YAML rather than Markdown prose. |
| Users rely on copying public adapter skills from the repository tree | Public adapter skill copies remain tracked for at least one stable public release after downloadable adapter artifacts and install docs are available; release notes announce the repository-tree install transition. |
| Root guidance could preserve the retired repository-tree install model | The `v0.1.3` spec requires `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` to be updated or explicitly recorded as unaffected, with ordinary contributors pointed to `dist/adapters/README.md` as the install-contract surface. |
| Partial tracked adapter package fragments could look installable | The `v0.1.3` architecture keeps only `dist/adapters/README.md` and `manifest.yaml` tracked by default; complete adapter packages are generated in temporary or release-output directories and attached as release archives. |
| CLI package contents could be mistaken for canonical workflow source | The CLI package is limited to command code, scaffolds, and bundled metadata. Canonical workflow content stays in repository-authored paths, and adapter archives remain release artifacts. |
| Bundled adapter metadata could drift from official release metadata | The first-slice package must include official metadata for the package's compatible adapter release, and tests should verify matching archive name, size, SHA-256, install root, tree hash, and validation result. Public publication requires package-content checks and real Codex install smoke. |
| Descriptor-driven adapter support could under-install a runtime surface | Adapter descriptors define possible roots, trusted metadata defines required roots, and opencode declared commands must install or fail verification. Skills-only older opencode archives emit a stable warning and record only installed roots. |
| Schema v2 lockfile upgrade could mask existing generated-output drift | The CLI must verify existing schema v1 Codex generated output before upgrading the lockfile wrapper or adding unrelated adapter entries. Drift blocks before mutation. |
| Proxy diagnostics could leak enterprise network details | Diagnostics expose only safe fields and enum values. Raw proxy URLs, credentials, request headers, raw environment values, private hostnames, usernames, and machine-local paths are forbidden. |
| Programmatic proxy dispatch could add dependency and credential-handling complexity | The first proxy-aware slice uses Node built-in env-proxy support only when available and defers Undici dispatcher support to a later approved proposal or spec. |
| npm package tarball could include unintended repository internals | The npm publication spec requires a package-content allowlist, forbidden-path checks, package-local license, no adapter archives, no generated adapter skill bodies, no lifecycle artifacts, and no secrets before publication. |
| Bootstrap publication could become a shadow release path | Bootstrap mode is limited to the first `0.1.4` publication when trusted publishing cannot be configured before package creation. It publishes only the exact verified tarball recorded in evidence, and trusted publishing must be configured before the next npm publication. |
| Routine publish could smuggle a release-process or package-surface change | Release evidence must classify the release type before publish. Process changes, new package names or scopes, new adapter targets, changed auth/provenance policy, and changed publish mechanics stay lifecycle-managed and cannot be treated as routine operations. |
| Emergency release deferrals could become generic gate bypasses | Deferrals require owner approval, reason, validation impact, accepted risk, follow-up location, and deadline. Non-deferrable release requirements remain mandatory, and failed gate evidence must be recorded rather than hidden. |
| Release evidence could leak credentials or machine details | The release evidence boundary records command families and bounded public facts only. Tokens, OTPs, credentials, private environment dumps, private hostnames, usernames, and machine-local absolute paths are forbidden. |
| Release profile could become another duplicated source | The profile is the routine release source of truth, generated surfaces derive from it, unauthorized current-version literals are audited, and manual generated-surface overrides must be explicit and preflight-checked. |
| Preflight could be mistaken for the release gate | Preflight is bounded to cheap deterministic local/profile/schema drift. `release-verify.sh <tag>` remains the authoritative full gate for generated outputs, archive integrity, package contents, adapter metadata, and full validation. |
| Generated publication evidence could encode invalid validator shapes | Pending and published evidence are generated from validator-compatible templates and checked by pre-publication or published validation; closeout writes expected `npx` command shapes and `sha256:<hex>` hashes rather than ad hoc manual strings. |
| Public evidence may not be observable immediately after publication | `close-release-publication` is rerunnable and fails with a clear pending external evidence diagnostic without marking the release published or modifying unrelated files. |
| Dry-run smoke could hide a broken real target install | Target-native `0.3.0` release readiness requires actual non-dry-run packed-package smoke before publish and live registry/download smoke after publish for `codex`, `claude`, and `opencode`. Historical FU-010 closeout still requires real Codex install proof for the `0.1.4` publication boundary. |
| Local archive extraction could overwrite or escape project boundaries | The CLI write plan refuses user-file overwrites by default, rejects absolute paths, parent traversal, symlinks, drive-letter paths, and paths outside `.agents/skills`, and maps expected verification failures to exit code `3`. |
| Lockfile could be mistaken for canonical source or release metadata | The lockfile records downstream generated-output state only. Canonical workflow, skill, schema, adapter metadata, and release evidence stay in repository-authored or release-evidence surfaces. |
| Unknown future lockfile shape could be silently erased by older CLIs | The first lockfile schema blocks on unknown top-level sections, unknown fields, unsupported schema versions, unsupported adapters, unsupported source values, and unsupported tree hash algorithms before mutation. |
| Target installation could succeed while state writing fails | The CLI reports state-write failure explicitly and must not claim durable manifest or lockfile state was recorded; later recovery or repair commands require a separate spec. |
| Users could rely on `latest` for reproducible setup | The public command model allows `latest` for quick starts but pinned package versions are the reproducible path. `latest` with incompatible local archives blocks unless a compatibility rule exists. |
| `new-change` scaffolds could be mistaken for completed workflow evidence | The first `new-change` slice writes only `change.yaml`, leaves `artifacts` and evidence arrays empty, sets review state to pending, and avoids durable-looking Markdown placeholders. Later status or validate commands must inspect actual artifacts rather than assuming scaffolded metadata means readiness. |
| Partial `new-change` filesystem writes could confuse users | The command preflights path conflicts, creates directories before files, reports completed and failed actions, and does not claim artifact-pack success after partial failure. It does not promise atomic rollback in the first slice. |
| Release validation could keep treating `.codex/skills/` as a privileged internal release path | The `v0.1.1` transition release gate validates public adapter output and only confirms `.codex/skills/` ignored/untracked state; optional local Codex smoke installs from the public Codex adapter path and stays outside required release evidence. |
| Generated adapter archives could create binary churn in Git | Generated archives are release assets by default; Git tracks artifact metadata and checksums instead of archive files. |
| Warning-only token budgets could be mistaken for CI gates | The first measurement slice treats budget thresholds as report warnings; hard gates require a later accepted proposal and spec. |
| Optional benchmark failures could be mistaken for passing release coverage | `skill-token-runtime-v2` separates optional warning evidence from claimed optional release coverage; claimed coverage follows required benchmark evidence and result-quality gates. |
| Shorter validation output could hide changed coverage or failure evidence | Script output optimization is presentation-only. Behavior-preservation evidence must prove selected checks, exit codes, failure detection, and failure evidence remain unchanged, and quiet mode must not hide non-success diagnostics. |
| Incomplete input surfaces could create stale validation cache hits | First-slice cache eligibility is limited to explicit-path lifecycle validation with deterministic input, implementation, and policy manifests; any unsupported or uncertain surface disables caching and runs the validator. |
| Helper mode could be mistaken for closeout proof | `explicit-paths-inner-loop` is explicitly inner-loop only, formal helper evidence uses `cache-hit-inner-loop` with `closeout_evidence: false`, and closeout validation rejects helper cache hits as sole proof. |
| Canonical helper cache identity could hide what command the user ran | Formal helper cache-hit evidence records both `displayed_command_argv` and `canonical_cache_argv`, so reviewers can distinguish the user-facing helper command from the direct command identity used for reuse. |
| Cache-hit evidence could be mistaken for closeout evidence | `cache-hit-inner-loop` is inner-loop evidence only. Closeout requires `actual-run-pass`, and lifecycle/change-metadata validators reject cache-only closeout claims. |
| Local cache state could leak machine details or become portable evidence | Local cache state remains untracked and may use local worktree identity only for invalidation. Tracked cache-hit evidence must use repository-relative paths and omit secrets, usernames, hostnames, credentials, machine-local absolute paths, and environment dumps. |
| Workstream B scope narrowing could be introduced without evidence | Workstream B remains out of scope until Workstream A measurement is recorded, reviewed, and a separate proposal or spec amendment authorizes the riskier behavior. |
| Evidence-class patterns could become too broad | Registry validation rejects broad catch-all patterns and ambiguous matches, and selector regression coverage proves registered recurring patterns route only their intended evidence classes. |
| `manual-routing-required` could become a permanent workaround | Deterministic in-repo evidence treats the diagnostic as registration debt, and verify readiness blocks unless debt is resolved or an owner-approved deferral records path, reason, validation impact, and follow-up. |
| Bounded query output could hide failures or blockers | Query helper outputs include blockers, unsupported-shape diagnostics, and detail pointers; full forensic reads remain required for disputed evidence, summary inconsistency, unsupported shapes, and whole-record review. |
| Stage-skill guidance could drift from query helper commands | Workstream B updates stage skills only after query helper commands are stable, and generated adapter validation is required whenever canonical stage-skill text changes. |
| Workflow-state validation could overreach into historical evidence | Lifecycle validation parses only governed change-local state and linked structured evidence; historical artifacts and ledgers remain read-only and are not rejected merely for retaining pre-adoption status prose. |
| Governed artifacts could regain mutable status | The architecture makes `change.yaml` the only mutable lifecycle and routing owner; skills and validators reject artifact-local or plan-owned current state for governed changes. |
| Unified automation could become blanket autopilot | One target covers only repository-local prerequisite stages; fixed stage ownership, current prerequisite checks, explicit stop conditions, and the external-action prohibition remain non-bypassable. |
| Shared change-local state could blur ownership | `artifact_states` uses transition-scoped author/reviewer ownership, `workflow_state` is workflow-owned, and all other entries are read-only to the current stage. |
| Interrupted writes could repeat or skip work | Review settlement is evidence-first and idempotent for the same identity; other incomplete or contradictory stage evidence pauses conservative recovery. |
| Clean plan review could be mistaken for active execution authority | Plan review reports `initialization-required`, workflow blocks onward routing, and only matching initialization plus settlement retry makes the plan active. |
| Historical plan state could regain authority | Readers use old plan fields only as historical stable intent; governed current state comes only from matching `planned_work`, and incomplete active legacy state requires explicit migration. |
| Consecutive stages could collapse review independence | Each automated review is a distinct formal invocation over tracked artifacts, governing sources, formal criteria, and recorded findings, with context reset when fresh context is unavailable. |
| Legacy and unified writers could diverge | Migration is dual-read and single-write; mutating resume records one migration event and unified state, while mixed writable legacy and unified state fails closed. |
| Typed stage policy could become a second normative source | Approved specs remain normative; the immutable Python registry is an executable projection with exhaustive conformance tests and policy-version checks. |
| Repeated stage targets could silently advance | `implement` and `code-review` bind a plan and milestone identity before persistence and never rebind on resume. |
| Orchestrator could infer auto-fix safety | Code-review owns `auto_fix_class`; missing or unsupported classifications fail closed to pause, and the orchestrator cannot upgrade findings. |
| Correction loops could oscillate or expand scope | The loop is capped per milestone, must shrink unresolved findings, pauses on new finding IDs or classes, stays path-local, and blocks new dependencies, components, interfaces, integrations, migrations, and generated artifact classes. |
| Automatic fixes could rewrite the governing authority | Substantive proposal, spec, test-spec, architecture, ADR, plan, constitution, workflow policy, release policy, and security policy edits are hard stops. |
| Final verify could reuse stale evidence | Verification prerequisites and completion require fresh actual-run evidence for correctness-bearing, security-sensitive, release-sensitive, lifecycle, review closeout, change metadata, generated-output, and required test-suite checks. |
| Unified automation could cross the PR boundary | Successful verify completion reports `pr` next and stops; external actions are prohibited and cannot be inferred from the target. |
| Automated review could collapse into author self-review | The review gate fails closed on `L0`, missing reviewer context identity, invalid initial-packet evidence, missing phase receipts, or early release of forbidden author context. |
| Requirement-fidelity applicability could be skipped by reviewer discretion | Applicability starts from deterministic affected-path and category triggers recorded before artifact comparison; overrides require closed direction and non-empty justification. |
| Reviewer-authored decomposition could itself be compressed | Accepted decompositions are preferred when available, reviewer-authored decompositions are marked as such, and Phase B samples reviewer-authored decompositions at the higher approved rate. |
| Implementation and validator could agree on the same compressed subset | Applicable reviews compare both implementation and validator assertions against decomposed spec properties and required surfaces; agreement between projections is not clean evidence. |
| Evidence staging could become ceremony | Structural validators enforce manifest, phase, outcome, and receipt shape, while sampled second reviews, downstream escape analysis, and calibration audits evaluate evidence quality and boilerplate risk. |
| Risk tier could be under-classified to preserve automation | The orchestrator owns classification from deterministic triggers and affected surfaces; ambiguous matches escalate to the higher tier, and author classification is not handoff authority. |
| Calibration fixtures could be memorized | Public fixtures document defect classes, while protected rotating calibration instances are preferred for measured recall and are separated from recurrence-detection metrics. |
| Second-review cost could erase automation value | Rollout sampling uses a 20% floor plus a minimum evidence count for standard-risk clean reviews, then adjusts standard-risk sampling from measured material-disagreement confidence; elevated-risk clean reviews remain second-reviewed. |
| Resource-integrity lint could over-classify examples as dependencies | Migration lint is bounded to recognized resource-loading instructions and approved skill-local prefixes; ordinary artifact paths, customer-project paths, and code examples stay outside the package contract unless used as load/copy/read/run instructions. |
| Runtime fallback could hide a broken package | Package validation remains failing for missing mapped resources, and fallback is allowed only for redundant convenience resources whose full contract already exists in `SKILL.md`. |
| Workflow bootstrap could persist authority before governed identity exists | Automation-command context is distinct from armed context; target bootstrap remains transient and persists only after governed validation and reclassification. |
| Workflow references could become competing policy owners | Universal, governed, automation, guide, and asset responsibilities are non-overlapping; automation and guide procedure consume upstream decisions, and contradiction stops as a package defect. |
| A shortened workflow common path could reconstruct missing procedure | Governed, automation, and guide resources are required when triggered; missing, unreadable, or mixed resources stop without fallback invention. |
| Progressive resource splitting could create competing semantic models | The contract version stays `boundary-first-v1`; the resource manifest assigns non-overlapping ownership, and semantic review checks compact, authoring, proof, and stage-local boundaries. |
| Inline compact-scan copies could drift | One contributor-owned shared block supplies the copied questions and skill validation checks exact block drift; generated packages derive from canonical skill text. |
| A declarative manifest could drift from executable projection behavior | Projection, validation, measurement, and activation all interpret the same closed manifest; unknown fields, resources, consumers, duplicates, unsafe paths, and missing or additional mappings fail closed. |
| Skill-only selector optimization could suppress lifecycle proof for mixed changes | Selector checks compose per changed path; mixed fixtures require purpose-built skill checks and lifecycle validation with independently scoped affected paths. |
| Resource measurements could be mistaken for actual model context use | Reports identify static bytes, mapped counts, and fixture-declared representative reads only; they make no runtime token claim and cannot become a hard gate without a later approved contract. |
| Interrupted projection could leave a mixed worktree | Projection preflights the complete matrix and checked-revision validation rejects mixed output; an active snapshot is not review-ready until the current source and derived proof set agree, and unpublished recovery restores tracked sources while discarding or regenerating derived output. |
| Checked-revision activation could be mistaken for public release | Local output names the snapshot and release intent but never claims tagged, published, public, or publicly verified status; public claims require routine release evidence. |
| A frozen baseline could be mistyped during one-time authoring | The internal derivation function accepts only one exact 40-character lowercase commit identity, returns bounded issues for invalid or unavailable input, derives the complete raw-byte-sorted inventory without writes, and regression fixtures compare the recorded inventory with its successful result. |
| Later validation could accidentally restore history dependence | The focused validator reads current files and the frozen inventory only; regression proof covers unreachable baseline provenance and absence of tag, remote, and network requirements. |
| Removing the custom publisher could remove normal release protection | The cleanup inventory is closed, while routine profile preparation, preflight, full verification, trusted publication, public smoke, closeout, and rollback checks remain separately owned and required. |
| Routine publication can expose partial cross-service state | Existing closeout remains rerunnable and records phase-specific failure; recovery uses closeout, dist-tag correction or deprecation when applicable, or a later patch without rewriting immutable releases. |
| Tracked projections could be hand-edited as if authored | The projection check binds every governed copy to one source and fails before dependent validation or packaging; contributor guidance identifies the copies as derived. |
| Grandfathering could become a blanket bypass | The manifest records the explicit reviewed pending-revision identity and a frozen sorted eligible path inventory derived only from that revision; later paths require the marker, while spec-review classifies substantive edits to grandfathered paths. |
| Draft specs could become accidental historical exemptions | Only `accepted`, `approved`, or `active` feature specs present at the explicit reviewed pending revision enter the inventory; in-flight opt-in is available only after activation is active. |
| Activation facts could be incomplete or mixed | The reviewed manifest uses only `pending` or `active`, validators check its closed fields and package identities, and no projection or state writer may repair incomplete evidence. |
| Digest implementations could disagree across platforms | One shared helper uses sorted POSIX paths, raw-byte SHA-256, fixed NUL/newline UTF-8 records, and lowercase hexadecimal output. |
| Shared method content could absorb stage policy | The method source has a closed content boundary; skill and workflow review reject stage-specific routing, authority, approval, or readiness semantics in the reference. |
| Project maps could be mistaken for source-of-truth behavior contracts | The `project-map` contract makes maps living references only, requires source-ranked evidence for material current-state claims, and forces direct source inspection when map evidence is stale, partial, inferred, unknown, conflicting, security-sensitive, or exact-behavior critical. |
| Area maps could fragment repository orientation | The root map remains the required entry point whenever area maps exist, area maps require durable boundaries and root registration, and overlap names one detail owner rather than duplicating descriptions. |
| Conditional project-map loading could omit known coordination | A bounded seven-surface preflight selects PMA0 only when no known coordination evidence exists; ambiguity loads reference-owned resolution or stops before dependent work. |
| Interrupted area creation could leave an orphan or overwrite a changed root | Area content is written first, registration is the commit point, the root is revalidated before commit, and retry adopts only exact matching transaction state. |
| Project-map validation could overfit natural language | The first slice validates contract structure, skeleton presence, resource-map mapping, generated adapter inclusion, and small representative outputs; a dedicated artifact validator stays deferred until repeated produced-map drift appears. |

## Glossary

- Gate A: deterministic canonical skill and packaged-resource integrity.
- Gate B: deterministic Codex, Claude Code, and opencode generation and package parity.
- Gate C: release-candidate integrity composed from Gate A, Gate B, and release-only proof.
- retirement ledger: the per-check record of protected failures, contract disposition, replacement evidence, dual-run result, and rollback.
- materialization smoke: filesystem-only invocation of RigorLoop-owned installer logic in an empty temporary directory; never target-runtime execution.
- ADR: architecture decision record that preserves a durable decision, alternatives, consequences, and follow-up.
- arc42: the 12-section architecture documentation model used by `architecture.md`.
- C4: context, container, component, and code-level structural diagram model.
- canonical architecture package: the long-lived current architecture source under `docs/architecture/system/`.
- change-local architecture delta: historical or explicitly exceptional evidence under `docs/changes/<change-id>/`; not part of the normal architecture authoring path.
- generated output: derived files under `.codex/skills/`, public adapter skill paths under `dist/adapters/`, generated adapter archives, and generated command aliases.
- mapped skill-local resource: a packaged resource under a skill root that is declared in that skill's `Resource map`.
- resource parity identity: the skill-root relative path plus raw-byte SHA-256 for an untransformed mapped resource.
- transformation contract: explicit ownership and expected identity for a resource intentionally changed between canonical source and generated, packed, or installed output.
- boundary-first compact core: the compatibility-stable
  `boundary-first-method-v1.md` resource containing portable vocabulary,
  compact routing, stable-ID, interaction, example, and non-Cartesian rules.
- boundary-first family resource: feature-authoring or proof guidance projected
  only to the governed stage family that owns those semantics.
- boundary-first resource manifest: closed declarative YAML inventory of
  resource IDs, canonical sources, skill-root-relative targets, and consumers.
- boundary-first projection-set identity: SHA-256 of sorted UTF-8
  `<repository-target-path>\0<lowercase-raw-byte-sha256>\n` records for every
  expected projected resource.
- boundary-first activation record: repository-local YAML binding contract
  snapshot, activating release intent, rollback release, compact-core compatibility
  identity, resource-manifest identity, projection-set identity, governed
  skills, reviewed pending-revision baseline provenance, and frozen grandfathered feature-spec
  paths.
- checked-revision activation: validation of boundary-first behavior from files
  in the current repository revision without requiring Git history, remote
  state, release tags, or network access; it is not public-release proof.
- activation baseline provenance: exact full reviewed pending-revision commit
  identity supplied during activation authoring and frozen with its derived
  grandfathered-spec inventory.
- routine boundary-first release: the existing profile-driven preparation,
  preflight, full verification, trusted tag publication, and public closeout
  flow used to publish the checked and reviewed `v0.4.0` package.
- boundary-first package rollback validation: read-only comparison of the
  selected immutable release's adapter archive identities with the current
  supported-adapter inventory.
- transition release: a stable release that preserves repository-tree adapter installation from `dist/adapters/` while `.codex/skills/` remains ignored local runtime state and adapter archives remain a follow-on migration by default.
- compatibility-window release: a stable release that preserves repository-tree adapter packages while also providing release archives and install guidance, giving downstream users one release to transition install models.
- adapter artifact metadata: tracked YAML under `docs/reports/adapter-artifacts/releases/<version>.yaml` that records source commit, generator command, archive paths, checksums, and validation evidence for generated adapter release artifacts.
- artifact-install path: installing adapter packages from downloadable release assets rather than copying generated skill bodies from the repository tree.
- release token-friendliness metadata: structured YAML under `docs/reports/token-cost/releases/` that gates public release token-cost evidence.
- required benchmark context: release-validation input that identifies required core, transition carryover, and changed-skill-required dynamic benchmarks for a release.
- result quality: structured manual or future automated evidence that a dynamic benchmark response followed the prompt and made correct readiness or handoff claims.
- token-cost benchmark fixture: prompt and minimal downstream-project inputs under `benchmarks/token-cost/` used by the benchmark runner.
- token-cost benchmark runner: repository-owned script that installs public adapter skills into a temporary fixture, runs prompt fixtures, and invokes the JSONL analyzer.
- lowest sufficient architecture surface: the smallest architecture evidence surface that truthfully handles a change: no-impact rationale, direct canonical update, ADR, or proposal/spec routing.
- material finding: review finding that must include evidence, required outcome, and safe resolution path or `needs-decision` rationale before it drives fixes.
- non-enforcement lifecycle routing: selector-selected validation that checks artifact lifecycle compatibility without proving C4 sufficiency, arc42 completeness, ADR need, or architecture package shape.
- report: durable authored evidence under `docs/reports/` used for longitudinal comparison, such as token-cost baselines.
- review artifact: authored change-local review evidence such as `reviews/*.md`, `review-log.md`, or `review-resolution.md`.
- project map: living Markdown repository orientation reference that records current-state evidence, inference, unknowns, freshness metadata, risks, and open questions without overriding source code or workflow authority.
- root map: repository-level project map, normally `docs/project-map.md`, that remains the entry point when area maps exist.
- area map: bounded project map under `docs/project-map/<area>.md` for a durable service, package group, application, data platform, infrastructure subsystem, ownership area, or domain.
- material project-map claim: current-state claim a downstream agent could use to choose a module, trust a boundary, select tests, assess runtime or data flow, or decide whether a map is safe to rely on.
- correction note: project-map refresh result note that says a previous map claim was wrong at its recorded baseline rather than merely stale because the repository later changed.
- CLI package: the repository package boundary published as `@xiongxianfei/rigorloop` and exposing the `rigorloop` binary through local, packed, or npm delivery.
- publication mode: the selected public npm publication path, either `trusted-publishing` through `release.yml` and npm OIDC or one-time `bootstrap` manual publication of an exact verified tarball.
- publication evidence: durable release evidence under `docs/releases/<version>/npm-publication.md` recording package identity, selected publication mode, tarball identity, smoke results, npm URL, trusted publishing or bootstrap details, and real Codex install proof.
- standing release-process contract: approved release architecture and spec that define how already-reviewed source is packaged, published, verified from the registry, and recorded without re-running proposal/spec/plan ceremony for routine publishes.
- routine publish: publish operation for already-reviewed work that introduces no new product, release-process, package-surface, authentication, provenance, adapter-target, or publish-mechanics decision.
- release transaction profile: durable release profile under `docs/releases/profiles/<tag>.yaml` that owns routine release version state, target support, publication requirements, evidence classes, generated release-prep surfaces, validator expectations, and timing requirements.
- profile-owned generated surface: release-prep surface that is generated from the active release transaction profile and should not be hand-edited except through an explicit review-visible override.
- human-authored profile-checked surface: release surface such as release-note narrative that humans author while tooling checks required fields and consistency with the active release profile.
- historical immutable release surface: prior release evidence, prior profile snapshots, or historical fixtures that routine release preparation must not rewrite.
- release preflight: cheap deterministic local/profile/schema release check that runs before `release-verify.sh <tag>` and catches drift that does not require full generated output or archive validation.
- published evidence closeout: rerunnable post-publication evidence generation that reads public GitHub/npm metadata, runs fresh public `npx` smoke, and writes validator-compatible published evidence.
- emergency deferral: owner-approved temporary release-gate exception that records rationale, validation impact, accepted risk, follow-up location, and deadline while preserving non-deferrable release requirements.
- bundled adapter metadata: official adapter artifact metadata included in the CLI package for the package's compatible adapter release.
- adapter descriptor: CLI-owned adapter install contract that maps an adapter name to archive filename pattern, possible roots, manifest shape, and lockfile shape.
- planned lockfile content: lockfile-shaped command output that previews generated-output hashes without writing durable `rigorloop.lock`.
- durable lockfile: downstream project `rigorloop.lock` written by the CLI after verified adapter install to record generated-output state.
- `rigorloop-tree-hash-v1`: normalized tree-hash algorithm for generated adapter output, based on sorted relative file paths and normalized file hashes.
- proxy-safe diagnostic: download failure diagnostic that reports bounded recovery facts without credentials, raw proxy URLs, request headers, private hostnames, raw environment values, usernames, or machine-local paths.
- change metadata scaffold: draft `docs/changes/<change-id>/change.yaml` produced by `rigorloop new-change` before downstream workflow stages fill in real requirements, tests, validation, changed files, reviews, and durable reasoning artifacts.
- evidence class registry: repository-owned selector contract that maps recurring deterministic change-local evidence filenames to allowed roots, routes, validators, lifecycle expectations, and allowed or required conditions.
- registration debt: required resolution work created when deterministic in-repo evidence produces `manual-routing-required`.
- bounded read: a query path that returns the authoritative slice needed for a common change-record question without loading unrelated history.
- query helper: repository-owned command that returns bounded change-record slices without running validation proof commands.
- validation cache hit: reuse of a previous passing validator result when the normalized command, input surface, implementation manifest, and policy/config manifest are unchanged.
- cache-aware inner-loop helper mode: `validate-artifact-lifecycle.py --mode explicit-paths-inner-loop`, the user-facing helper command that supplies approved cache context for repeated inner-loop lifecycle validation.
- canonical cache argv: the normalized direct `validate-artifact-lifecycle.py --mode explicit-paths` argv used for helper cache identity.
- lifecycle-state consistency gate: bounded validation of governed
  artifact-state, workflow-state, planned-work, blocker, target, and linked
  evidence fields before downstream reliance.
- workflow automation mechanism: the single writable target-driven
  `bounded-review-fix` flow whose target and routing state are persisted in
  the governed change record.
- structured target: a requested public stage plus occurrence identity and completion predicate, bound before persistence.
- artifact-state entry: change-local lifecycle record for one stable governed
  artifact ID, changed only by its matching authoring or review transition.
- workflow state: the sole change-local current routing and planned-work snapshot; `plan` initializes missing primary-plan state once from current clean review evidence, `plan-review` retries settlement, and workflow selects every later transition from settled artifacts and stage evidence while the activated CLI validates and atomically persists closed selected operations.
- completion-evidence fingerprint: SHA-256 over the versioned canonical normalized milestone-completion record covering proof, review receipt, canonical review-log occurrence, full packet inventory, normalized review facts, milestone identity, and operation authority; replay must reconstruct every constituent before idempotent success.
- stable plan identity: artifact ID, kind, role, and normalized path; it names the durable plan artifact without hashing its content.
- reviewed revision identity: review ID, round, record path, reviewed artifact path, and reviewed repository revision or commit used to prove which plan revision was judged.
- fixed stage write boundary: the published-skill rule that defines the
  artifact, evidence, or transition a stage may write regardless of manual or
  automated invocation.
- independent adversarial review gate: workflow-managed review handoff contract that requires a fresh review context, neutral initial packet, blind-first risk map, staged evidence release, risk-tiered escalation, and structured verdict evidence before automatic continuation.
- requirement-fidelity gate: workflow-managed review handoff contract that requires deterministic applicability, spec-canonical packet ordering, requirement-property decomposition, property-by-surface verification, validator assertion comparison against the spec, and requirement-compression calibration for applicable automated reviews.
- requirement compression: defect class where a multi-property, multi-surface, closed-list, or multi-verb requirement is projected as an incomplete subset in implementation, validation, skill guidance, or review evidence.
- requirement property: explicit property decomposed from a normative spec clause and checked against required surfaces.
- requirement-fidelity receipt: clean-review evidence that records decomposition, property matrix completeness, multi-surface identification, validator comparison against the spec, compressed-requirement risk, and no-finding rationale.
- applicability manifest: review evidence that records whether the requirement-fidelity gate applies to a review, the path and category triggers, result, override direction, justification, and review stage.
- review invocation manifest: orchestrator-owned process record for an automated review, including target identity, independence level, reviewer context identity, initial-packet inventory, risk tier, phase receipts, and handoff eligibility inputs.
- initial-packet inventory: immutable list of tracked artifacts, revisions, hashes, prompt template version, and neutral routing metadata released to the reviewer before blind-first risk formation.
- clean-review sufficiency receipt: structured evidence for an automated no-finding review that records what was inspected, challenged, tested, and left uncertain.
- second-review disagreement: material finding, blocked result, or inconclusive result from a required or sampled second independent review after a first review was clean.
- failed-remediation: reconciliation category for a prior finding claimed or expected to be fixed but rediscovered independently during a blind-first rereview.
- gate-ready proposal: proposal artifact and review state proving accepted direction and clean proposal-review evidence, independent of user authorization.
- automation metadata: change-local mechanism, target, status, current stage,
  stop reason, and evidence that remains subordinate to `workflow_state` and
  does not own artifact settlement.
- architecture assessment: recorded workflow-managed micro-stage after approved `spec-review` that routes to `architecture`, `plan`, or pause for ambiguity.
- auto-fix classification: reviewer-owned material-finding field that records
  `none`, `mechanical`, or `declared-safe` eligibility for bounded
  implementation correction.
- test-spec settlement: deterministic evidence that the test spec is active or settled, mapped, gap-free, synchronized with inputs, and ready to authorize implementation.
- live-state surface: the bounded `change.yaml` fields that own artifact
  lifecycle, workflow routing, planned work, blockers, next stage, and
  closeout readiness for a governed change.
- displayed command argv: the normalized helper argv the user invoked, recorded in formal helper cache-hit evidence separately from canonical cache argv.
- local execution cache: untracked branch-local, worktree-local, change-local cache state used only to avoid repeated local validation execution.
- formal cache-hit evidence: tracked change-local YAML that records why a previous validator pass still applies and remains inner-loop evidence only.
- `cache-hit-inner-loop`: evidence kind for unchanged-input reuse; not eligible to satisfy stage or milestone closeout.
- `actual-run-pass`: evidence kind that the required validator or bundle actually executed and passed; eligible for first-slice closeout when it covers the required bundle.
- validation cache measurement: change-local YAML evidence that records Workstream A cache hits, misses, disabled evaluations, actual runs, time saved, remaining cost, and Workstream B recommendation state.

## Next artifacts

- Architecture-review for the project-map skill package-composition and area-transaction update.

## Follow-on artifacts

- Code-Review Skill Simplification: the prior canonical package update and its architecture-review history remain recorded under `docs/changes/2026-08-10-code-review-skill-simplification/`; the current workflow change supersedes only the canonical owning-change pointer.
- Usability-First Boundary-First v0.4.0 Release: approved spec and this
  canonical update make stage-owned boundary behavior automatic and concise,
  replace transition-based activation with checked-revision snapshots, retire
  the custom candidate/publisher experiment, and preserve the routine release
  workflow; architecture review is owned by its change record.
- Legacy architecture lifecycle normalization: completed; top-level legacy architecture records are archived historical evidence.
- Architecture-review for the 2026-04-29 package-quality refinement: approved on 2026-04-29 with no findings.
- Architecture-review for the 2026-05-08 workflow-governance direct canonical package update: approved in `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/architecture-review-r1.md` with no material findings.
- Plan-review for the 2026-04-29 package-quality refinement: approved on 2026-04-29 after PR-F1 corrected M5 sequencing.
- Plan-review for the 2026-05-08 workflow-governance execution plan: approved in `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/plan-review-r2.md` with no material findings.
- Test spec update: `specs/architecture-package-method.test.md` active on 2026-04-29 for R76-R118 and AC14-AC20.
- Historical architecture skill surface simplification (current replacement: [Design decision preservation](../../design/skill/authoring/design.md#material-decision-preservation)): proposal accepted and spec amendment approved on 2026-05-09; canonical architecture and ADR update approved in this package revision.
- Architecture-review for the 2026-05-09 architecture skill surface simplification: approved in `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/architecture-review-r1.md` with no material findings.
- Plan-review for the 2026-05-09 architecture skill surface simplification: approved in `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/reviews/plan-review-r2.md` after PR-F1 corrected milestone review sequencing.
- Token-cost measurement baseline and proposal scope preservation: accepted proposal and approved spec add repository-local measurement scripts, token-cost baseline reports under `docs/reports/token-cost/`, and proposal/proposal-review scope-preservation guidance.
- Release Token-Friendliness benchmark for skills: accepted proposal and approved spec add fixture-backed release token-cost benchmarking, structured release metadata, public-skill-source benchmark installation, analyzer summaries, raw-or-sanitized run evidence, waiver handling, and token-cost release validation delegation.
- Expanded dynamic Token-Friendliness benchmarks for core skills: accepted proposal and approved spec define `skill-token-runtime-v2`, required core coverage, transition carryover coverage, optional extended coverage, changed-skill-required benchmarks, claimed optional coverage gates, required benchmark context, and structured result-quality evidence.
- Single Authored Skill Source and Generated Output: accepted proposal and approved spec define `skills/` as the only authored skill source, untracked `.codex/skills/` local mirror generation, staged public adapter artifact migration, adapter artifact metadata, and temp-output validation for untracked generated trees.
- Publish Next Release With Single Authored Skill Source: accepted proposal and approved spec define the `v0.1.1` transition-release architecture: validate canonical `skills/`, tracked public adapter output, release notes, adapter install guidance, and token-cost metadata; keep `.codex/skills/` out of required release evidence; retain `dist/adapters/` as the public install path; defer downloadable adapter archives unless separately planned.
- Stop Tracking Generated Public Adapter Skill Bodies: accepted proposal and approved spec define the `v0.1.3` public adapter untracking release architecture: retire tracked generated adapter package fragments under `dist/adapters/<adapter>/`, keep `dist/adapters/README.md` and `manifest.yaml`, validate generated temporary or release-output packages and release archives, update root guidance, and preserve `v0.1.2` as compatibility-window evidence.
- RigorLoop CLI Package and Codex Init: accepted proposal and approved spec define the first CLI slice: one package candidate, one `rigorloop` binary, help/version, `init --adapter codex`, dry-run JSON, non-destructive write planning, generated `rigorloop.yaml`, bundled metadata for Codex archive verification in both default and local archive modes, planned lockfile output only, and no public npm publication until release hardening.
- RigorLoop CLI Lockfile: approved spec and accepted ADR define durable `rigorloop.lock` writes for verified Codex init, strict lockfile shape handling, `rigorloop-tree-hash-v1`, drift blocking, local and network source recording, and partial-failure write ordering.
- Architecture-review for the RigorLoop CLI Lockfile architecture update: approved in `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/architecture-review-r1.md` with no material findings.
- RigorLoop CLI New Change: approved spec defines `rigorloop new-change <change-id>` as a change metadata scaffolding command that creates only `docs/changes/<change-id>/change.yaml`, preserves lifecycle claim boundaries, validates public option domains, reports complete write plans, blocks symlinks and overwrites, and exposes partial write failures.
- Architecture-review for the RigorLoop CLI New Change architecture update: approved in `docs/changes/2026-05-16-rigorloop-cli-new-change/reviews/architecture-review-r1.md` with no material findings.
- RigorLoop npm Publication: accepted proposal and approved spec define the first public `@xiongxianfei/rigorloop@0.1.4` npm release, package-content allowlist, dependency and lifecycle-script policy, trusted-publishing and bootstrap modes, publication evidence, packed-package smoke, real Codex install smoke, and FU-010 closeout boundary.
- Multi-Adapter Init and Proxy-Aware Adapter Download: accepted proposal, approved spec, and accepted ADR define descriptor-driven CLI init for Codex, Claude Code, and opencode; keep Codex on `.agents/skills`; define schema v2 mixed-root lockfile handling; preserve release-archive and local-archive verification; and add proxy-safe download diagnostics while deferring programmatic Undici dispatcher support.
- Script Output Optimization: accepted proposal and approved spec define first-slice `scripts/test-select-validation.py` output shaping, reliable-only rerun guidance, silent quiet success, behavior-preservation evidence, and minimal `scripts/ci.sh` wrapper adjustment only when needed to preserve quiet-success and loud-failure behavior.
- Change-Record Catalog Registration and Bounded Read Model: accepted proposal, approved spec, and accepted ADR define deterministic evidence-class registration, selector routing for recurring change-local evidence, registration-debt handling for `manual-routing-required`, and a bounded query-helper model for common stage-owned reads.
- Validation Idempotency and Cache-Hit Safety: accepted proposal, approved spec, and accepted ADR define first-slice explicit-path lifecycle validation cache hits, the cache-aware inner-loop helper mode, local-only execution cache state, formal cache-hit evidence, closeout actual-run gates, Workstream A measurement, and Workstream B deferral.
- Workflow-State Projection and Pre-Transition Synchronization Gate:
  historical pre-adoption design for active-plan live-state ownership and
  projections; governed changes use the stage-owned change-local model instead.
- Target-Native Init Commands and Adapter Terminology Retirement: accepted proposal, approved spec, and accepted ADR define the 0.3.0 target-native init boundary, full public removal of `--adapter`, install-only default behavior, explicit `--write-state`, target-oriented state schemas, default state byte preservation with safety reads, and real non-dry-run release smoke gates.
- Published Skill Resource Integrity with an Architecture-Skill Pilot: accepted proposal, approved spec amendment, and accepted ADR define mapped resource integrity, bounded legacy lint, raw-byte generated and installed parity, locally packed release-candidate clean-install proof, and architecture-skill pilot resource-chain evidence.
- Progressive Boundary-First Skill Guidance: accepted proposal and approved
  spec define prompt-independent compact scanning, owner-scoped progressive
  resources, artifact-sliced downstream reads, hazard-driven scenario
  selection, path-owned validation, checked-revision activation, and measured rather
  than budget-gated loading.
- Evidence-Bound and Incremental `project-map`: accepted proposal and approved spec define evidence-bound map metadata, freshness, root/area registration, source-ranked claims, skeleton asset packaging, generated adapter inclusion, correction notes, and downstream reliance boundaries.
- Proposal-Gated Authoring Autoprogression: historical profile design whose
  separate authorization and state ownership are superseded; its proposal
  gate and review-independence safeguards remain retained review requirements.
- Release Transaction Automation: accepted proposal and approved spec define a routine release transaction profile under `docs/releases/profiles/<tag>.yaml`, generated-surface ownership, Python-owned release preflight, full-gate preservation, rerunnable public evidence closeout, and timing evidence.
- Implementation Autoprogression Through Verify: historical profile design
  whose separate authorization and state ownership are superseded; its
  reviewer-owned correction, fresh verify, and stop-before-PR safeguards
  remain retained workflow requirements.
- Independent Adversarial Review Gates: accepted proposal and approved spec define verifiable automated review independence through orchestrator-owned neutral manifests, blind-first risk formation, staged evidence release, risk-tiered review depth, clean-review sufficiency receipts, second-review disagreement gates, final holistic code review, and calibration metrics.
- Requirement-Fidelity Gate: accepted proposal, approved spec, and accepted ADR define deterministic requirement-fidelity applicability, spec-canonical packet ordering, requirement-property decomposition, per-property and per-surface verification, spec-derived validator assertion matrices, clean-review fidelity receipts, and compression-defect calibration as an additive sibling to independent adversarial review gates.
- Bounded Review-Fix Autoprogression: historical proposal-side profile design
  whose nested state writer is superseded; driver-owned proposal correction,
  bounded rereview, direct-review isolation, and architecture applicability
  remain preserved.
- Single Bounded Review-Fix Workflow Automation: historical consolidation
  contract retained for one writable target-driven mechanism, structured
  targets from `proposal-review` through `verify`, review independence,
  evidence-first recovery, dual-read/single-write migration, and the
  stop-before-PR boundary. Its two-level authority, capability, typed-policy,
  receipt-state, plan-owned live-state, and canonical-position decisions are
  superseded by the stage-owned change-local lifecycle model.

## Readiness

The project-map skill package-composition and area-transaction update is authored under `specs/project-map.md` and is ready for architecture review.
No diagram or ADR changes are required because container boundaries, persistence, deployment topology, and durable package decisions remain unchanged; the update uses the existing mapped-resource package model and records the bounded two-artifact write inside the existing project-map container.
Planning must wait for matching architecture-review settlement.

The published-skill-first validation architecture is authored under its approved feature specification.
Reliance on the new gate composition, semantic-review boundary, conditional materialization smoke, or retirement flow requires matching architecture and ADR review settlement.

ADR `docs/adr/ADR-20260810-published-skill-first-validation-architecture.md` records the proposed durable validation and release-composition decision.
The current selector, cache, scheduler, runtime benchmark, and meta-validation architecture remains transitional until the execution plan sequences exact contract amendments, dual proof, and recoverable retirement slices.

ADR `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`
records the proposed durable checked-revision snapshot, one-time baseline,
custom-path retirement, automatic concise guidance, and routine release
decision. It supersedes ADR-20260805 and amends only the local activation
semantics of ADR-20260728; architecture review is still required.

ADR `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
records the accepted durable resource-composition, manifest, identity,
measurement, selector, activation, and rollback decision. It revises only the
resource-composition part of ADR-20260728 while retaining its
immutable release rollback and external-action boundaries.

References below to earlier authoring, implementation, and review-fix profile
ADRs are historical decision evidence. They do not restore profile-owned
lifecycle state, separate workflow authorization, capability, typed-policy,
or receipt-state layers. The stage-owned change-local lifecycle decision is an
accepted current dependency, not the candidate under this review.

ADR `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md` records the durable decision to move generated local and public skill copies out of ordinary authored Git state through staged temp-output and release-artifact validation. ADR `docs/adr/ADR-20260515-rigorloop-cli-package-and-codex-init.md` records the first CLI package boundary, bundled local-archive metadata decision, planned-lockfile boundary, and original publication block. ADR `docs/adr/ADR-20260516-rigorloop-npm-publication.md` records the first public npm publication boundary, package-content and publication-mode decisions, and real install closeout proof. ADR `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md` records the durable decision to treat change records as registered and queryable catalogs. ADR `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md` records the durable decision to add validation cache hits for unchanged explicit-path lifecycle inputs, including the cache-aware inner-loop helper mode, while preserving actual-run closeout gates.  [Skill SKL-DEC-02](../../design/skill/skill.md#architecture-decisions), with [original ADR provenance](../../archive/skill-model/2026-09-08/README.md), preserves mapped-resource identity and runtime-fallback/package-validity distinctions; the existing validation owner governs currently applicable proof. ADR `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md` records the durable proposal-gated authoring autoprogression profile, policy persistence, and review-independence decision. ADR `docs/adr/ADR-20260624-implementation-through-verify-autoprogression.md` records the durable separately armed implementation autoprogression profile, phase gating, reviewer-owned correction authority, fresh verify requirement, and stop-before-PR boundary. ADR `docs/adr/ADR-20260625-independent-adversarial-review-gates.md` records the durable automated review-independence gate, neutral-packet evidence model, blind-first phase protocol, risk-tiered escalation, second-review disagreement behavior, and calibration boundary. ADR `docs/adr/ADR-20260626-requirement-fidelity-gate.md` records the durable automated requirement-fidelity gate, deterministic applicability model, spec-canonical packet order, decomposition and property-matrix evidence, validator assertion matrix boundary, and compression-defect calibration. ADR `docs/adr/ADR-20260630-bounded-review-fix-autoprogression.md` records the durable bounded review-fix profile, nested review-fix state, driver-owned safe-fix classification, same-review rerun boundary, and architecture-assessment routing. No additional ADR is required for `rigorloop new-change` because it is an additive command inside the existing CLI package boundary and does not introduce a new durable source-of-truth, packaging, release, validation, or persistence decision. No new ADR is required for the cache-aware inner-loop helper because it amends the existing validation cache-hit safety decision rather than introducing a separate validation architecture. No additional ADR is required for the evidence-bound `project-map` update because it applies existing generated-output, skill resource-integrity, and living-reference workflow decisions to one published skill and one packaged skeleton asset. No new ADR is required for workflow-state synchronization because the accepted spec amends the existing single-source workflow-state contract and composes through the existing lifecycle-validation architecture instead of adding a new system boundary, storage boundary, parser authority, or service. No change-local architecture delta is produced because the canonical package carries the intended durable guidance directly.
