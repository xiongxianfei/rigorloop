# Change rationale: Usability-First Boundary-First v0.4.0 Release

## Summary

This change makes boundary-first behavior automatic and concise in the ten governed lifecycle skills, replaces the unpublished custom activation publisher with a checked-revision snapshot, and prepares one routine `v0.4.0` release payload for Codex, Claude, and opencode.

The tracked snapshot is active and locally verified, but no tag, publication, push, merge, registry write, or public-availability claim has occurred.

## Problem

Users previously had to name the boundary-first method even though the relevant skills already owned the responsibility to cover material correctness boundaries.
The pending activation design also coupled local capability proof to remote Git identities and a custom publisher, making a thin project harder to release without improving normal user behavior.

## Decision trail

- The proposal selected the existing routine release workflow and rejected both the custom publisher and a second simple-versus-hardened release mode.
- `UBR-R001` through `UBR-R005` and `UBR-R018` make automatic coverage concise, stage-owned, and semantically tested.
- `UBR-R006` through `UBR-R008`, `UBR-R015`, and `UBR-R019` define independent checked-revision snapshots, frozen compatibility, and immutable rollback.
- `UBR-R009` through `UBR-R012`, `UBR-R016`, `UBR-R017`, and `UBR-R020` retain routine release identity, parity, evidence safety, recovery, and trusted publication authority.
- ADR-20260806 keeps one declarative activation record, one internal read-only derivation function for activation authoring, and no new public CLI or writer.
- The plan separated semantic usability proof (M1), activation cleanup (M2), routine release payload proof (M3), and active integrated proof (M4).

## Diff rationale by area

| Area | Files and change | Reason | Contract and evidence |
| --- | --- | --- | --- |
| User behavior | `scripts/fixtures/boundary-first/semantic/usability-cases.json` and `scripts/test-skill-validator.py` add representative spec, inspection, and review journeys. The already-authored compact skill guidance remains unchanged. | Prove automatic, concise behavior by meaning rather than prose, word, bullet, or method-name assertions. | `UBR-R001`-`UBR-R005`, `UBR-R018`; M1 evidence |
| Activation | `scripts/boundary_first_validation.py`, its CLI and tests, `specs/boundary-first-activation.yaml`, and the proof-model status now use exact pending/active checked snapshots. | Keep local validation deterministic and independent of history, tags, remotes, and networks while freezing historical compatibility once. | `UBR-R006`-`UBR-R008`, `UBR-R015`, `UBR-R019`; ADR-20260806; M2/M4 evidence |
| Custom-path retirement | Deleted `boundary_activation_release.py`, `publish-boundary-activation.py`, and their test; removed their selector registration and dependencies. | Remove the unpublished second activation and publication mechanism while preserving ordinary validation and release selection. | `UBR-R013`; M2 evidence |
| Routine release | Added the `v0.4.0` profile, tracked release notes and evidence, timing and npm-publication records; updated `release_transaction.py`, `release-verify.sh`, and trusted release workflow checks. | Use the established preparation, preflight, verification, tag, and rerunnable closeout path with one exact version and dist-tag authority. | `UBR-R009`-`UBR-R012`, `UBR-R016`, `UBR-R020`; M3 evidence |
| Package parity | Updated package version/README, bundled adapter metadata, adapter validation, release indexes, and three-target fixtures. | Bind canonical skills, generated adapters, archives, and the npm package to equivalent resources and exact archive identities. | `UBR-R010`, `UBR-R011`, `UBR-R015`; M3/M4 evidence |
| Fail-closed evidence | Tightened lifecycle and release validators plus regressions for unknown vocabulary, evidence cardinality, tag identity, deferral authority, private diagnostics, and ambient Git/npm authority. | Prevent malformed, incomplete, mixed, or externally redirected evidence from being accepted. | `UBR-R007`, `UBR-R011`, `UBR-R017`, `UBR-R020`; review resolutions |
| Architecture and lifecycle | Updated the canonical architecture, component diagram, ADR, proposal, spec, plan, test spec, superseded-change state, reviews, and change-local evidence. | Preserve the approved authority split and make the complete decision/review history reconstructable. | Accepted artifacts and all milestone receipts |

## Tests added or changed

| Test surface | What it proves | Why this level fits |
| --- | --- | --- |
| Semantic skill journeys (`T1`-`T5`, `T23`) | Automatic selection, concise stop rules, justified expansion, stage ownership, and fail-closed fixture vocabulary. | Static skill behavior and repository loaders are deterministic local contracts. |
| Boundary validation (`T6`-`T12`) | Exact pending/active tuples, one-time derivation, no-history normal validation, bounded diagnostics, retirement, grandfathering, and rollback. | Unit and temporary-repository fixtures directly isolate snapshot and Git-authority boundaries. |
| Release transaction and lifecycle (`T13`, `T15`-`T22`) | Profile identity, complete evidence rows, immutable tag binding, recovery, public-authority separation, and secret-safe evidence. | Repository release validators can prove pre-public behavior without external mutation. |
| Adapter and npm package (`T14`-`T17`) | Three-target archive parity, clean installation, package contents, pending and active full gates. | Temporary generated archives and packed installs exercise the shipped boundary. |
| Selector regression | Retired custom checks are absent while ordinary spec, lifecycle, boundary, and release paths still execute. | Component-level routing tests catch path-selection regressions without invoking publication. |

## Validation evidence available before final verify

The reviewed final implementation has the following local evidence:

| Command or gate | Result |
| --- | --- |
| `python scripts/test-boundary-first-validation.py` | 62 passed |
| `python scripts/validate-boundary-first.py --check` | active snapshot; `v0.4.0` intent; `v0.3.6` rollback |
| `python scripts/test-select-validation.py` | 147 passed after the M4 fixture correction |
| `python scripts/release-preflight.py v0.4.0 --skip-remote` | passed; one pre-existing report-only `v0.3.4` literal warning |
| `bash scripts/ci.sh --mode release --release-version v0.4.0` | passed; `release.validate` 2.34s, required broad smoke 493.99s |
| `bash scripts/release-verify.sh v0.4.0` | passed; 285 skill tests (16 skips), 149 adapter tests, 6 npm tests, and three rebuilt archives |
| Review-artifact and change-metadata validation after R4 | passed; 26 reviews, 27 resolved findings, no open findings |

These are local repository checks.
Hosted CI, public assets, npm registry state, and public `npx` smoke have not been observed and are not claimed.

## Review resolution summary

The durable [review resolution](review-resolution.md) closes 27 material findings, all accepted and resolved, with no `needs-decision` or open review-log entry.
Every milestone ended in a clean independent review.
M4 R4 additionally reconciled the historical M4 R2 count of 26 with the 27-row final inventory, whose extra row is the now-resolved count-consistency finding itself.

## Alternatives rejected

- Keeping or finishing the custom candidate/atomic publisher retained remote identities, transition evidence, and a second publication path without user value.
- Removing the activation record lost the small compatibility and rollback authority still needed after activation.
- Deriving the grandfathered inventory on every check made normal validation depend on history; a new derivation CLI or writer added permanent surface for a one-time authoring action.
- Adding simple and hardened release modes duplicated policy. The existing routine workflow already separates local proof from trusted publication.

## Scope control

This change does not add a runtime checker, global scenario matrix, separate boundary stage, new service, new dependency, second release mode, or generated adapter source tree.
It does not redefine `boundary-first-v1`, migrate accepted historical specs, rewrite `v0.3.6`, or perform public release operations.

## Risks and follow-ups

- PR-mode preflight exposed one selector omission for the canonical research
  artifact produced during release framing. The focused
  [PR-readiness bug-fix evidence](evidence/pr-readiness-research-selector-bugfix.md)
  records the failing reproduction, test-first correction, and scoped routing
  result. This does not change the release contract; it makes the existing
  research output path participate in its owned documentation checks.
  Independent PR-readiness code review R1 approved the correction with no
  material findings and confirmed that unsupported and mixed unknown paths
  remain fail-closed.
- The first complete PR-mode execution then exposed four stale integration
  assumptions after the release version and activation model changed. The
  [full-gate fix evidence](evidence/pr-readiness-full-gate-fixes.md) records the
  boundary-record normalization, single architecture owner, exact release
  profile parsing, and `v0.4.0` CLI fixture update. Broad smoke passed in that
  run; only the four named diff-scoped checks required correction.
- Activation is locally coherent but not public availability; immutable tag, hosted publication, registry/assets validation, and fresh public smoke remain explicit maintainer operations after review and merge.
- Release recovery remains phase-specific and fix-forward after immutable publication begins; neither `v0.4.0` nor `v0.3.6` may be rewritten.
- Final verification must confirm this rationale, lifecycle state, generated output, targeted proof, broad smoke evidence, and release metadata still agree with the final branch before claiming `branch-ready`.

The release implementation and first selector correction are reviewed. The
full-gate corrections require independent code review before final
verification can refresh branch readiness; none of this authorizes public
release.
