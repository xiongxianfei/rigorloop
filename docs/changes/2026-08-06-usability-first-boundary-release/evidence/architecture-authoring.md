# Architecture Authoring Evidence: Usability-First Boundary-First v0.4.0 Release

Stage: architecture
Date: 2026-08-06
Owning change: `docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`
Approved spec: `specs/usability-first-boundary-release.md`
Canonical architecture: `docs/architecture/system/architecture.md`
ADR: `docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md`

## Result

- Architecture surface: canonical-update and ADR.
- Canonical architecture changed: yes.
- Diagrams changed: `docs/architecture/system/diagrams/component-boundary-guidance.mmd`.
- ADRs created or updated: created `ADR-20260806`; it supersedes the unpublished candidate/atomic-publication decision in `ADR-20260805` without rewriting that historical ADR.
- Direction/spec blockers: none.
- Next stage: `architecture-review`.

## Architecture decision

The architecture uses the smallest recurring mechanism that satisfies the approved contract:

- the existing activation record carries one independently valid pending or active checked-revision snapshot;
- one explicit reviewed pending-revision identity is passed with the repository root to the internal pure `derive_grandfathered_specs(root, baseline_revision)` function only during authoring to derive and freeze the historical-spec inventory;
- the existing focused `validate-boundary-first.py --check` path validates current files without Git history, tags, remote state, network access, or public-release claims;
- automatic concise boundary behavior remains owned by the ten published skill bodies and their existing resource model, not a new runtime checker; and
- the existing routine release profile, preparation, preflight, full gate, trusted tag workflow, and rerunnable closeout remain the sole public `v0.4.0` release path.

The internal function returns a raw-byte-sorted path tuple plus bounded validation issues, performs no writes, and is not called by normal `--check` validation. No activation writer, preparation CLI, candidate evidence, publication-readiness protocol, custom publisher, service, dependency, schema, state store, or release mode is introduced.

## Changed architecture surfaces

| Surface | Change |
| --- | --- |
| Section 1, Introduction and Goals | Adds the usability-first release artifacts and replaces the candidate/atomic-publication goal with automatic concise behavior, checked-revision activation, and routine release. |
| Section 4, Solution Strategy | Makes the inline boundary scan automatic for behavior-bearing tasks and limits expansion to contract, risk, or explicit user need. |
| Section 5, Building Block View | Replaces the five candidate/publication components with activation authoring, the exact internal pure derivation function, checked-revision validation, and routine release responsibilities. |
| Section 6, Runtime View | Defines the function's exact input, output, failure, no-write, and one-time invocation contract plus independent snapshot validation, current-file-only checks, exact custom-path retirement boundary, and routine public release/recovery flow. |
| Section 7, Deployment View | Removes candidate evidence, tagged-tree split execution, and atomic ref transaction boundaries; retains derived package proof and the standard release transaction. |
| Section 8, Crosscutting Concepts | Defines declarative snapshot semantics, the claim boundary, no-writer authoring, history-independent validation, automatic skill ownership, package parity, and immutable recovery. |
| Section 9, Architecture Decisions | Adds ADR-20260806 and classifies ADR-20260805 as superseded historical design. |
| Section 10, Quality Requirements | Replaces candidate, tagged-tree, and atomic-publisher scenarios with snapshot coherence, baseline reproducibility, claim separation, routine release, and rollback scenarios. |
| Section 11, Risks and Technical Debt | Replaces custom-publication risks with baseline authoring, accidental history dependence, routine-release preservation, partial-publication recovery, and local/public claim separation. |
| Section 12, Glossary | Replaces six-role candidate vocabulary with checked-revision activation, baseline provenance, and routine boundary-first release. |
| Component diagram | Shows explicit baseline input, the read-only inventory helper, activation authoring, activation record, checked-revision validator, routine release, public services, and evidence flow. |

The C4 system context and container views remain unchanged because the repository, boundary-guidance container, release-evidence container, external GitHub/npm systems, and supported users do not change. The component view is the lowest affected level and is sufficient; no deployment diagram is needed because the change removes a custom publication component and reuses the already documented release deployment boundary.

## Requirement-to-architecture mapping

| Spec requirements | Architecture owner |
| --- | --- |
| UBR-R001 through UBR-R005, UBR-R018 | Governed skill bodies, compact scan, owner-scoped resources, approved artifact slices, and semantic journey tests; no separate runtime checker or scenario matrix. |
| UBR-R006 through UBR-R008 | Existing activation record, explicit authoring-only baseline input, frozen inventory derivation, and current-file-only checked-revision validator. |
| UBR-R009 through UBR-R012, UBR-R020 | Existing routine release profile, preparation, preflight, full verification, trusted immutable tag workflow, package/adapter proof, public smoke, and closeout. |
| UBR-R013 | Exact three-script deletion and five-surface candidate/publication behavior removal; ordinary selector, checked-revision validation, and routine release remain. |
| UBR-R014, UBR-R017 | Repository-local lifecycle stages perform no external publication and store only privacy-bounded evidence; trusted publication retains its existing credential boundary. |
| UBR-R015, UBR-R016 | Read-only `v0.3.6` rollback package selection plus existing phase-specific closeout, dist-tag correction/deprecation, and fix-forward recovery. |
| UBR-R019 | Frozen grandfathered-spec inventory controls historical exemption; new or substantively revised specs continue prospective adoption. |

## Alternatives and consequences

- Keeping candidate validation and the atomic publisher was rejected because it preserves remote state, six Git identities, extra evidence, transition restrictions, and a second publication path.
- Removing the activation record was rejected because the record remains the smallest deterministic authority for capability, compatibility, package identity, and rollback selection.
- Recomputing grandfathering on every validation was rejected because it restores history and reachability dependence.
- Adding a preparation CLI or writer was rejected because activation is a one-time reviewed source edit and the permanent command or extra mutation surface has no recurring user value; the named internal pure function is sufficient for implementation and regression proof.

The main tradeoff is that the one-time baseline must be available and supplied correctly during authoring. The exact internal function contract, reviewable provenance, deterministic inventory derivation, and regression fixtures cover that narrow risk without a user-facing command. Routine publication may expose partial cross-service state, but the standing release contract already owns rerunnable closeout and immutable fix-forward recovery.

## Architecture-review R1 resolution

`UBR-AR1-001` is addressed by naming the repository owner and exact callable contract: `scripts/boundary_first_validation.py` owns `derive_grandfathered_specs(root, baseline_revision)`, which accepts a repository root and exact 40-character lowercase commit identity and returns `(sorted_paths, issues)` without writes. The activation implementation step calls it once; focused regression fixtures prove successful and bounded-failure behavior; normal `scripts/validate-boundary-first.py --check` never calls it. No owner decision or new public CLI is required.

## Quality, deployment, and security

- Usability: ordinary users receive automatic concise boundary behavior without naming the method or seeing an extra stage.
- Determinism: checked-revision validation uses closed record fields and current canonical, projection, adapter, and rollback identities.
- Performance: ordinary skill use adds no network call; focused validation adds no Git-history or remote query.
- Deployment: no new infrastructure or runtime is introduced; the existing GitHub/npm release boundary is reused.
- Security/privacy: local validation needs no credentials and emits bounded repository identities; public credentials remain inside the existing trusted release workflow; evidence excludes secrets, private environment values, usernames, hostnames, and machine-local paths.
- Compatibility: historical accepted specs and immutable `v0.3.6` rollback remain valid; the unpublished custom mechanism has no supported compatibility obligation.

## Evidence scope

`docs/project-map.md` was used only for repository orientation. Because its boundary-activation detail predates this approved change, the design relies on direct inspection of the canonical architecture, activation and resource ADRs, activation record, validator/CLI interfaces, selector surfaces, routine release tooling, and approved spec instead of treating the map as exact behavior authority.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-06-usability-first-boundary-release/change.yaml` — pass after the R1 revision.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-06-usability-first-boundary-release` — pass with five recorded reviews and six findings; R1 remains open pending R2 review.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/component-boundary-guidance.mmd --path docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md --path docs/changes/2026-08-06-usability-first-boundary-release/change.yaml --path docs/changes/2026-08-06-usability-first-boundary-release/evidence/architecture-authoring.md` — pass with only the already classified merge-language warnings in the approved proposal and spec.
- `python scripts/validate-markdown-readability.py docs/architecture/system/architecture.md docs/adr/ADR-20260806-checked-revision-boundary-activation-and-routine-release.md docs/changes/2026-08-06-usability-first-boundary-release/evidence/architecture-authoring.md` — pass with advisory readability warnings.
- `python scripts/validate-boundary-first.py --path specs/usability-first-boundary-release.md` — pass.
- Arc42 heading audit — all 12 required headings remain present in order.
- `git diff --check` over the revised architecture, diagram, ADR, change record, and authoring evidence — pass.

## Handoff

The R1 finding is addressed without a new public surface. The architecture and ADR have no open design questions and are ready for architecture-review R2. No planning, implementation, publication, or architecture-review approval is claimed here.
