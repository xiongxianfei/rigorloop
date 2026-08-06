# ADR-20260806: Checked-Revision Boundary Activation and Routine Release

## Owning change record

`docs/changes/2026-08-06-usability-first-boundary-release/change.yaml`

## Context

The unpublished `v0.4.0` activation design coupled local capability proof to a unique Git transition, remote-ref discovery, candidate evidence, publication readiness, and a custom atomic branch-and-tag publisher. That design made the release harder to prepare without improving the everyday experience of users who need boundary-first behavior to apply automatically and concisely.

The approved replacement specification separates two claims:

- checked-revision activation proves that the files in the current repository revision carry one coherent `boundary-first-v1` capability; and
- public release proves that the exact reviewed release commit was tagged and published through the standing routine release workflow.

The design must retain deterministic package parity, historical-spec compatibility, immutable `v0.3.6` rollback, and normal release verification while removing the unpublished candidate and publisher experiment.

## Decision

Keep `specs/boundary-first-activation.yaml` as the single activation record and keep its existing closed field set. Interpret it as one declarative snapshot in the current repository revision, not as a locally enforced state machine.

- A `pending` snapshot uses `-` for `activating_release`, `rollback_release`, and `grandfathering_baseline_revision`, and uses an empty `grandfathered_specs` inventory.
- An `active` snapshot uses `v0.4.0` as release intent, `v0.3.6` as rollback, one exact full reviewed pending-revision commit identity as baseline provenance, and the complete sorted grandfathered-spec inventory derived from that revision.
- Both snapshots are independently valid. Checked-revision validation makes no claim about earlier or later revisions and does not classify an `active` snapshot followed by a `pending` snapshot.

Activation preparation is an authoring operation, not a new public workflow or state writer. The activation implementation step supplies the repository root and exact 40-character lowercase reviewed pending-revision commit identity to the repository-internal pure `derive_grandfathered_specs(root, baseline_revision)` function in `scripts/boundary_first_validation.py`. The function performs read-only Git object inspection and returns `(sorted_paths, issues)`: `sorted_paths` is the complete tuple of eligible top-level accepted, approved, or active feature-spec paths sorted by raw UTF-8 bytes and `issues` is empty on success; invalid, unavailable, malformed, or unreadable baselines return no inventory and bounded validation issues. It writes no files, refs, activation state, or evidence. The implementation calls it once, records the successful input and output directly in the activation record, and proves them with focused regression fixtures. The function is not exposed through `scripts/validate-boundary-first.py` or another public CLI. The projection writer continues to own resource projection only; no activation writer, preparation command, candidate evidence file, or transition receipt is introduced.

After the active record is authored, `python scripts/validate-boundary-first.py --check` validates only the current checked revision. It reads the activation record, canonical resources, resource manifest, governed skill inventory, projected resources, adapter support inventory, and rollback metadata. It fails closed on missing, additional, stale, malformed, unknown, mixed, or divergent values. It does not inspect Git history, require the baseline revision to be reachable, query a remote, require a tag, or make a public-release claim.

Automatic boundary-first behavior remains instruction-owned. The ten governed skill bodies apply their stage-owned compact scan whenever the task admits behavior boundaries; the user does not name the method. Each stage covers material boundaries once at the owning layer, loads only its owner-scoped resource or an approved artifact slice, and expands only for a governing requirement, material risk, or explicit request. No runtime checker, global scenario matrix, or separate boundary stage is added.

Retire the unpublished custom activation-release path exactly as specified by UBR-R013:

- delete `scripts/boundary_activation_release.py`, `scripts/publish-boundary-activation.py`, and `scripts/test-boundary-activation-release.py`;
- remove candidate and publication-readiness behavior from `scripts/boundary_first_validation.py`, `scripts/validate-boundary-first.py`, and their tests; and
- remove the custom activation-release check and path dependencies from the validation selector and selector tests.

Public `v0.4.0` release remains owned by the existing routine release profile, `prepare-release`, `release-preflight`, `release-verify.sh`, trusted tag publication workflow, and rerunnable public closeout. The immutable tag points to the exact reviewed release commit. Existing package, adapter, archive, install-smoke, secret, release-note, registry, and public `npx` checks remain in force. Partial publication remains open and recovers through rerunnable closeout, dist-tag correction or deprecation when applicable, or a later patch; neither `v0.4.0` nor `v0.3.6` is rewritten.

This decision supersedes `ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md`. It amends the activation semantics in `ADR-20260728-portable-boundary-first-release-manifest-and-package-rollback.md` from transition/tag-derived local state to checked-revision snapshots, while retaining that ADR's single manifest, frozen historical inventory, read-only package rollback validation, and external release-operator boundary. It retains the resource composition and parity decisions in `ADR-20260729-progressive-boundary-guidance-resources.md`.

## Alternatives considered

### Keep the candidate validator and atomic publisher

Rejected because it introduces remote state, six Git identities, extra evidence, transition restrictions, and a second publication path before users receive the capability.

### Remove the activation record entirely

Rejected because the record is the small deterministic authority for pending or active capability, package identity, historical-spec compatibility, and rollback selection.

### Derive grandfathering from Git on every validation run

Rejected because checked-revision validation must work without history, reachability, remote state, or network access.

### Add a new activation-preparation CLI or writer

Rejected because activation happens once through an ordinary reviewed source edit. A new command would add a permanent public surface, and a writer would add a second mutation owner, without recurring user value. The named repository-internal pure function gives implementation and tests one exact repeatable derivation contract without either surface.

### Treat checked-revision activation as public release proof

Rejected because local package coherence and public availability have different authorities. Only the immutable tag, trusted publication workflow, registry/assets, public smoke, and closeout support a public-release claim.

## Consequences

- Local activation proof becomes fast, deterministic, read-only, and independent of Git history, tags, remote state, and network access.
- The activation record remains a small explicit compatibility and rollback authority instead of becoming a transition ledger.
- One-time baseline derivation still requires the reviewed pending revision to be available during authoring. Its exact internal function contract is testable without becoming a CLI; later validation uses the frozen record and inventory directly and never calls that function.
- Three custom scripts and their selector surface disappear, and the existing validator and routine release paths become the only supported paths.
- Public release can still fail partially across GitHub and npm; existing closeout and fix-forward recovery handle that operational state without a custom atomic publisher.
- Automatic boundary behavior is tested semantically through representative RigorLoop journeys rather than exact prose, fixed counts, or method-name output.
- No new dependency, service, schema, persistent state store, release mode, or network call is introduced.

## Follow-up

- Update the canonical architecture package and focused boundary-guidance component diagram.
- Revise validator, selector, skill guidance, semantic fixtures, generated packages, activation record, and routine `v0.4.0` release surfaces through the approved plan and test specification.
- Record architecture review before execution planning.
