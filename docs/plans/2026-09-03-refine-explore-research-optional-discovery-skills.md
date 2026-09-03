# Execution Plan: Refine Explore and Research as Optional Discovery Skills

## Purpose / big picture

Refine the existing `explore` and `research` public skills into two small, optional discovery modes: Explore expands a decision's materially different options, while Research establishes bounded decision-relevant facts with explicit confidence. Explicit invocations produce standalone supporting artifacts, but the owning Proposal, Design, Delivery, Implementation, Verify, or other decision stage retains approval and lifecycle authority.

## Current Handoff Summary

- Owning change record: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/change.yaml`

Mutable lifecycle state, current milestone state, review status, blockers, routing, and closeout readiness live only in this record.

## Source artifacts

- Proposal: `docs/proposals/2026-09-03-refine-explore-research-optional-discovery-skills.md`
- Spec: `specs/refine-explore-research-optional-discovery-skills.md`
- Architecture: `docs/architecture/2026-09-03-refine-explore-research-optional-discovery-skills.md`
- Approved Design package: `design-review-r2`
- Prior-contract test spec: none; v3 uses this plan's verification allocation.

## Context and orientation

Canonical public skills live under `skills/`. Explore and Research currently have large core instructions and different artifact behavior: Explore carries a fixed five-option method and proposal-adjacent output, while Research permits either standalone or inline output. Their package structure, metadata, conditional resources, shared-block parity, forbidden authority claims, and public wording are validated primarily by `scripts/skill_validation.py` and `scripts/test-skill-validator.py`.

Stable shared public policy is authored under `templates/shared/` and copied verbatim into each self-contained consuming skill package. `specs/skill-contract.md` owns the approved shared-block inventory and package rules. `specs/rigorloop-workflow.md`, `skills/route/SKILL.md`, `AGENTS.md`, `README.md`, and applicable examples and fixtures describe on-demand support and semantic routing. `docs/project-map.md` is current enough for orientation but lacks the new `docs/explorations/` artifact root, so its affected rows require a bounded refresh.

Supported Codex, Claude Code, and opencode packages derive from canonical `skills/` through `scripts/build-skills.py`, `scripts/build-adapters.py`, and adapter-distribution validation. Only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are tracked adapter support surfaces; generated public adapter skill bodies and release archives are validation output and must not be hand edited.

This plan separates the work at reviewable integrity boundaries. M1 establishes the complete self-contained skill packages and validator-enforced shared contract. M2 changes semantic routing and all current repository-owned explanatory surfaces after the packages are valid. M3 proves canonical-to-generated and installed-adapter parity without publishing a release.

## Non-goals

- Merge Explore and Research, rename either public skill, or create a new discovery skill.
- Add lifecycle stages, review gates, settlement states, artifact kinds in `change.yaml`, CLI transitions, or automatic progression.
- Give either support artifact authority to approve or mutate an owning stage's decision.
- Require discovery work before Proposal, Design, Delivery, Implementation, or Verify when direction and facts are already sufficiently clear.
- Require a fixed number of options, sources, pages, or tokens.
- Build a research database, knowledge base, telemetry system, or external evidence service.
- Rewrite historical discovery artifacts, completed change records, or immutable release archives.
- Publish a release or hand-edit generated adapter skill bodies.

## Requirements covered

| Requirement and boundary scope | Owning milestone or evidence |
| --- | --- |
| ER-R1-ER-R22, ER-R27-ER-R34, ER-R37-ER-R38; all eight boundary IDs; INT-001-INT-005 | M1 self-contained Explore and Research contracts, artifacts, methods, authority, failure behavior, and validator enforcement |
| ER-R2, ER-R4, ER-R9, ER-R15, ER-R20-ER-R28, ER-R34, ER-R36-ER-R38; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-001, INT-002, INT-005 | M2 Route selection and current governance, workflow, documentation, examples, fixtures, and map coherence |
| ER-R1, ER-R3, ER-R27-ER-R38; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-003 | M3 generated candidates, adapter support metadata, release-oriented parity, and historical preservation |
| ER-R1-ER-R38; BND-INPUT-001-BND-ENV-001; INT-001-INT-005 | TG-FINAL-01 through TG-FINAL-03 complete-change proof |

## Milestones

### M1. Build the canonical optional discovery packages

- Milestone kind: implementation
- Engineering purpose: Establish both complete self-contained packages, their standalone artifact contracts, and fail-closed validation before changing repository-wide routing guidance.
- Requirements: ER-R1-ER-R22, ER-R27-ER-R34, ER-R37-ER-R38; all eight boundary IDs; INT-001-INT-005.
- Architecture responsibility: canonical shared discovery policy; Explore package; Research package; artifact boundary; authority and ownership; evidence semantics; progressive disclosure; package validation.
- Dependencies:
  - approved Design package `design-review-r2`;
  - existing shared-block, Resource map, package-containment, and skill-validation mechanisms;
  - canonical `skills/` source ownership.
- Implementation scope: Add the approved shared discovery block and both verbatim package-local copies; replace the core Explore and Research instructions; add one artifact skeleton and two conditionally loaded method references to each package; update the skill-contract shared-block inventory; and extend focused validation for required clauses, resources, parity, paths, proportional options, standalone output, authority exclusions, secrets, and unknown closed values. Do not yet change Route or broad workflow documentation.
- Files/components likely touched:
  - `templates/shared/discovery-support.md`;
  - `skills/explore/SKILL.md`, `skills/explore/assets/`, and `skills/explore/references/`;
  - `skills/research/SKILL.md`, `skills/research/assets/`, and `skills/research/references/`;
  - `specs/skill-contract.md`;
  - `scripts/skill_validation.py` and `scripts/test-skill-validator.py`;
  - focused skill fixtures under `scripts/fixtures/` when existing fixture structure requires them.
- Required verification:
  - TG-01 — An explicit Explore invocation resolves one absent `docs/explorations/YYYY-MM-DD-slug.md` artifact, records the required decision-space sections, permits a proportional two-option case, includes status quo only when credible, and never claims approval or lifecycle progression.
  - TG-02 — An explicit Research invocation defines bounded questions and stopping evidence, examines repository evidence first when applicable, writes one `docs/research/YYYY-MM-DD-slug.md` artifact, distinguishes evidence/inference/assumption and confidence, and never collapses into an inline completion.
  - TG-03 — New targets, exact explicit revisions, collisions, ambiguous or escaped paths, unrelated existing artifacts, missing or unreadable resources, unavailable evidence, contradiction, scope expansion, and retry preserve owner authority and unrelated bytes.
  - TG-04 — Core files stay focused, required resources are mapped and contained, specialized methods load conditionally, the canonical shared block and both local copies are byte-identical, and any missing, drifted, mixed-version, escaped, contradictory, or unknown closed value fails before a package-current claim.
  - TG-05 — Supporting Implementation or Verify, encountering an approved contradiction, or recording a leading option/bounded answer hands the artifact to the named owner without mutating that owner's artifact or lifecycle state and without recording secrets or machine-local paths.
- Evidence expectations: Focused validator tests use representative valid packages and mutations for fixed quotas, inline Research output, authority overreach, missing and escaped resources, shared-copy drift, unsafe paths, collisions and exact revisions, conditional loading, unknown vocabulary values, private data, and historical artifacts.
- Implementation steps:
  - Add failing focused validator and package-fixture tests for the new structure and each fail-closed invariant.
  - Add the approved shared block to the skill-contract inventory and create both exact package-local copies.
  - Replace each core skill with its narrow purpose, routing boundary, authority exclusions, artifact result, stop conditions, Resource map, and handoff.
  - Add concise copy-and-fill artifact skeletons and only the conditionally triggered methods named by the architecture.
  - Run focused validation and inspect public text for maintainer-only implementation leakage.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
- Expected observable result: Canonical Explore and Research are independently installable, visibly distinct, optional support skills with concise standalone outputs, proportional work, bounded authority, and validator-enforced resource integrity.
- Completion criteria: Every M1 test group passes; both local shared copies match the admitted canonical block; neither core contract retains the five-option quota or inline Research completion; all failure cases preserve unrelated artifacts and owner authority.
- Required evidence: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m1-canonical-discovery-packages.md`
- Review handoff: Code Review of public distinction, artifact safety, shared-resource integrity, progressive disclosure, evidence semantics, authority exclusions, and negative validator coverage.
- Optional commit boundary: `M1: refine canonical explore and research packages`
- Risks:
  - A copied shared block may drift or make installed packages depend on repository-root files.
  - Static clause checks may accept wording that semantically grants approval authority.
- Rollback/recovery:
  - Revert the shared-block admission, both complete skill packages, and their focused validation as one unit; do not leave either package on a mixed contract.

### M2. Align routing and current repository guidance

- Milestone kind: implementation
- Engineering purpose: Make selection of Explore, Research, both, or neither predictable across current workflow and documentation surfaces after the canonical packages are internally valid.
- Requirements: ER-R2, ER-R4, ER-R9, ER-R15, ER-R20-ER-R28, ER-R34, ER-R36-ER-R38; all eight boundary IDs; INT-001, INT-002, INT-004, INT-005.
- Architecture responsibility: Route guidance; Explore-only, Research-only, combined, contradiction, and stopping runtime flows; current governance and workflow coherence; affected project-map orientation.
- Dependencies:
  - accepted M1 implementation and Code Review;
  - complete current-surface search distinguishing public/current guidance from historical evidence;
  - existing Route support-selection and stage-authority boundaries.
- Implementation scope: Update Route's on-demand support guidance and current workflow, contributor, public, example, fixture, and benchmark surfaces that materially describe Explore or Research. Add selection and handoff regressions for one, both, or neither. Refresh only affected project-map rows. Preserve lifecycle graphs, stage authority, incidental local fact checks, and historical records.
- Files/components likely touched:
  - `skills/route/SKILL.md` and its on-demand support reference if the existing Resource map requires one;
  - `specs/rigorloop-workflow.md` and applicable current examples or fixtures;
  - `AGENTS.md`, `README.md`, and `docs/project-map.md`;
  - `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, selection fixtures, and benchmark inventories only where they encode the old distinction;
  - current architecture or documentation indexes only where an existing statement becomes false.
- Required verification:
  - TG-06 — Route selects Explore for material option-space uncertainty, Research for a material uncertain fact, Explore then bounded Research when evidence can change the option comparison, and neither when the owner can proceed with settled direction and facts.
  - TG-07 — Route does not auto-run discovery without explicit invocation or higher authority; an incidental fact check or option consideration produces no support artifact and no discovery-completion claim.
  - TG-08 — Proposal, Design, Delivery, Implementation, Verify, and another named owner can receive a support artifact, while the support skill cannot edit the owner's artifact, grant approval, settle a package, or advance lifecycle state; contradictions return to the affected owner.
  - TG-09 — Current governance, workflow specification, public documentation, examples, fixtures, benchmarks when affected, and project map agree on optionality, standalone artifacts, default paths, one/both/neither routing, and owner adoption without rewriting history.
  - TG-10 — Repeated, stale, unavailable, unsafe, or out-of-scope support work stops or qualifies its result; fresh evidence and explicit exact revisions remain attributable, bounded, and safe to retry.
- Evidence expectations: Route selection matrix, explicit-versus-incidental cases, solution-biased and volatile-fact scenarios, cross-stage authority negatives, contradiction handoffs, direct current-reference inventory, and reviewed exclusions for historical artifacts and release archives.
- Implementation steps:
  - Add failing route and current-surface coherence tests for Explore, Research, both, neither, explicit invocation, incidental checks, and owner authority.
  - Update Route and the normative workflow contract without altering lifecycle stages or transition operations.
  - Reconcile current contributor and public documentation, examples, fixtures, and affected benchmark inventory entries.
  - Refresh affected `docs/project-map.md` rows from direct source inspection and classify remaining old-contract matches as current defects or preserved history.
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-boundary-first.py --check --path specs/refine-explore-research-optional-discovery-skills.md`
- Expected observable result: A developer or agent can consistently choose Explore, Research, both, or neither, and every current explanatory surface preserves optionality and the decision owner's authority.
- Completion criteria: The routing matrix and cross-stage negative cases pass; current source contains no conflicting fixed quota, inline explicit-Research result, proposal-only restriction, or discovery approval claim; preserved historical matches are explicitly outside current authority.
- Required evidence: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m2-routing-and-guidance.md`
- Review handoff: Code Review of semantic routing, explicit invocation boundary, owner adoption, lifecycle non-mutation, current-versus-historical classification, and documentation coherence.
- Optional commit boundary: `M2: align optional discovery routing and guidance`
- Risks:
  - Broad wording edits could accidentally rewrite historical evidence or make discovery appear mandatory.
  - Supporting Implementation or Verify could be confused with permission to repair or approve those stages.
- Rollback/recovery:
  - Revert the Route and current-guidance slice together; retain the already reviewed M1 packages as internally valid but do not claim repository-wide routing coherence until M2 is restored.

### M3. Prove generated adapter and release-candidate parity

- Milestone kind: implementation
- Engineering purpose: Propagate and verify the reviewed canonical packages through every supported adapter boundary without treating derived output or publication as authored work.
- Requirements: ER-R1, ER-R3, ER-R27-ER-R38; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-003.
- Architecture responsibility: deployment view; canonical-to-generated package boundary; adapter support metadata; compatibility, security, rollback, and raw-byte resource parity.
- Dependencies:
  - accepted M2 implementation and Code Review;
  - stable canonical skill packages and current routing guidance;
  - repository-owned adapter generator, manifest, validation, and temporary release-output path.
- Implementation scope: Update tracked adapter support metadata and generator or release checks only where the new resources and contract require it; generate temporary supported-adapter candidates and archives from canonical skills; validate invocation names, contained resources, public text, and shared-copy bytes; prove interrupted or failed generation cannot create a partially authoritative package; preserve historical release archives. Do not publish or hand edit generated bodies.
- Files/components likely touched:
  - `dist/adapters/manifest.yaml` and `dist/adapters/README.md` when their current contract or inventory changes;
  - `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`, and adapter templates only where new resources expose a missing generic rule;
  - `scripts/build-adapters.py`, release validation, and token-cost inventory tests only when affected by the resource additions;
  - temporary Codex, Claude Code, and opencode output outside tracked authored skill source.
- Required verification:
  - TG-11 — All supported adapters retain separate Explore and Research invocations with their complete mapped local resources, standalone artifact wording, and identical public authority semantics.
  - TG-12 — Canonical, generated, archived-candidate, and clean-installed inventories agree; each discovery-support copy is the expected raw bytes; no package reaches outside its installed skill root or contains maintainer-only source and adapter mechanics.
  - TG-13 — Unknown adapter/resource inventory values, missing resources, path escapes, mixed versions, generator interruption, stale output, or failed validation block package-current claims and leave no partially authoritative tracked output.
  - TG-14 — Prior discovery artifacts and immutable release archives remain unchanged; the current package keeps the public skill names while adopting proportional Explore and standalone Research behavior.
- Evidence expectations: Adapter-distribution tests, temporary archive inventories, clean-install checks for Codex, Claude Code, and opencode, resource-byte comparisons, interruption/stale-output regressions, historical hash or exclusion evidence, and a current-versus-historical match audit.
- Implementation steps:
  - Add or update failing adapter inventory, resource, public-text, path-containment, stale-output, and interruption tests before distribution changes.
  - Update only the generic generator, metadata, or templates proven necessary by those tests.
  - Generate candidates and archives into a temporary output directory through repository tooling; never edit their skill bodies.
  - Run complete canonical and adapter validation, inspect remaining contract matches, and preserve generated output only as validation evidence where the repository contract permits it.
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-token-cost-measurement.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.4.0 --output-dir /tmp/rigorloop-discovery-adapters`
  - `bash scripts/ci.sh --mode broad-smoke`
- Expected observable result: Every supported generated and installed adapter exposes the same refined Explore and Research packages and failure semantics, while tracked source and historical archives retain their correct ownership.
- Completion criteria: All adapter inventories, resources, bytes, and invocation surfaces agree with canonical source; failure and stale-output cases fail closed; broad smoke passes; no release is published and no generated skill body is tracked as authored source.
- Required evidence: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m3-adapter-parity.md`
- Review handoff: Code Review of generated parity, containment, public-text hygiene, failure recovery, historical preservation, and absence of hand-edited derived output.
- Optional commit boundary: `M3: propagate optional discovery packages to adapters`
- Risks:
  - A new mapped resource may be omitted by one adapter or transformed inconsistently.
  - A fixed `/tmp` validation target may contain stale output from an earlier run.
- Rollback/recovery:
  - Remove the exact temporary output directory before generation and on failure; revert tracked adapter metadata or generic generator changes with M3. After a later publication, use a corrective release rather than rewriting immutable archives.

## Change-level verification

### TG-FINAL-01. Optional discovery routing and owner authority

- Covers: ER-R2-ER-R26, ER-R34, ER-R38; M1-M2; BND-INPUT-001, BND-STATE-001, BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001; INT-001, INT-002, INT-004, INT-005.
- Demonstrate: Across explicit Explore, explicit Research, combined support, incidental local reasoning, and neither-needed scenarios, exactly the requested supporting artifact is created or revised, owner and lifecycle state remain unchanged, unsafe or contradictory work stops correctly, and the named decision owner alone adopts conclusions.
- Evidence expectations: Selection matrix, representative artifact outputs, exact target and collision/revision cases, before/after owner-artifact and `change.yaml` identities, unavailable/stale evidence cases, contradiction routing, and private-data inspection.
- Non-applicability: Milestone-local proof is insufficient because the claim crosses Route selection, both skill packages, filesystem effects, and downstream stage authority.

### TG-FINAL-02. Canonical, generated, and installed package coherence

- Covers: ER-R1, ER-R27-ER-R38; M1-M3; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-003.
- Demonstrate: Canonical skills, shared policy, conditionally mapped resources, current docs and validation, generated archives, and clean-installed adapters expose the same two independent contracts, while drift, missing resources, unknown inventories, path escape, mixed versions, or maintainer-only leakage fails closed.
- Evidence expectations: Closed resource inventories, raw-byte shared-copy comparison, validator mutation matrix, clean-install trees for every supported adapter, adapter command/resource inspection, and historical archive exclusions.
- Non-applicability: Milestone-local proof is insufficient because package-current confidence spans canonical, generated, archived, installed, and public-documentation boundaries.

### TG-FINAL-03. Compatibility, failure, and recovery integrity

- Covers: ER-R3, ER-R7, ER-R10, ER-R12-ER-R21, ER-R30, ER-R33, ER-R35-ER-R38; M1-M3; all eight boundary IDs; INT-001-INT-005.
- Demonstrate: Historical artifacts remain readable, current explicit invocations use proportional and standalone contracts, exact revision preserves identity, collisions and partial failures preserve unrelated bytes, volatile evidence is qualified, interrupted generation is recoverable, and all repository-owned validation passes without granting lifecycle authority or publishing a release.
- Evidence expectations: Historical/current fixtures, filesystem identity checks, repeated and failed invocation cases, confidence/freshness examples, generator interruption cleanup, full lifecycle/review validation, and fresh broad-smoke output.
- Non-applicability: Milestone-local proof is insufficient because compatibility and recovery cross artifact creation, stage handoff, validation, generation, and repository governance.

## Validation plan

- `scripts/test-skill-validator.py` owns focused public-contract, Resource map, shared-copy, path, progressive-disclosure, authority, routing, and unknown-value regressions.
- `scripts/validate-skills.py` and `scripts/build-skills.py --check` own canonical package structure and local generated-skill coherence.
- `scripts/test-select-validation.py` proves repository validation selection still includes affected discovery, shared-template, Route, workflow, and adapter surfaces.
- `scripts/test-adapter-distribution.py`, build-skill tests, token-cost tests, and temporary adapter generation own supported adapter inventories, transformations, resource containment, archive bytes, and clean-install parity.
- Boundary-first validation preserves the approved eight-dimension specification proof map. Milestone-focused commands run before `bash scripts/ci.sh --mode broad-smoke` on the complete M3 candidate.
- Final explicit-path lifecycle validation includes this plan, proposal, architecture, specification, owning change root, both canonical skill packages, Route, the shared template, changed governance/docs, adapter metadata, and review evidence.
- Hosted CI, release publication, deployment, and post-adoption usage metrics are not Delivery Review or implementation claims. Verify records any later required hosted observation.

## Risks and recovery

- Risk: Explore and Research remain semantically interchangeable despite structural changes.
  - Recovery: Keep one central question per package and require selection-matrix and representative-output review before distribution work.
- Risk: The shared policy or a conditional resource drifts across self-contained packages.
  - Recovery: Admit one canonical block, enforce verbatim copies and closed Resource maps, and fail before generation on any mismatch.
- Risk: Standalone artifacts become mandatory workflow overhead.
  - Recovery: Preserve explicit-invocation and incidental-work negatives in Route, workflow, and validator fixtures.
- Risk: Support work silently mutates an approved decision or lifecycle state.
  - Recovery: Test owner-artifact and `change.yaml` identity around creation, collision, contradiction, and handoff cases; route correction to the owner.
- Risk: Adapter generation produces a mixed or partial public package.
  - Recovery: Generate to an exact clean temporary directory, validate all supported adapters before any later publication, and use a corrective release after publication rather than rewriting history.

## Dependencies

- Accepted proposal, approved exact Design package `design-review-r2`, and approval of this exact primary plan by Delivery Review.
- M1 precedes routing reconciliation; M2 consumes the reviewed canonical packages; M3 consumes the reviewed current repository contract.
- Each implementation milestone receives direct proof and Code Review before its dependent milestone starts.
- No standalone test-spec is created. The TG groups in this plan are the v3 Delivery evidence map.
- Generated adapters and archives derive from canonical `skills/`; generated bodies are not hand edited or committed as authored source.
- External research is not required to implement this repository-owned contract. Release publication and post-adoption usefulness measurement remain separately authorized future work.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-03 | Use three implementation milestones for packages, routing coherence, and adapter parity. | Each slice has a distinct integrity boundary, reviewer focus, and rollback path. | One repository-wide milestone; one milestone per file family. |
| 2026-09-03 | Put the shared-block admission and both consuming packages in M1. | A reviewed state must not admit a block without its required copies or ship either package with mixed common policy. | Separate shared-template and per-skill milestones. |
| 2026-09-03 | Change Route only after both canonical packages validate. | Routing should not direct users to a partially refined support mode. | Route-first cutover; independent Explore and Research cutovers. |
| 2026-09-03 | Treat adapter candidates as generated validation output, not authored deliverables. | Repository governance makes `skills/` canonical and tracks only adapter support metadata after v0.1.3. | Hand-edit adapter bodies; track temporary release archives. |

## Readiness

- See the owning change record for current workflow state.
- Readiness is not Done. Delivery Review must approve this exact primary plan before implementation begins.
