# Tooling organization independent Design Review

## Result

- Skill: design-review.
- Review ID: tooling-organization-design-review, round 1, 2026-09-14.
- Review status: approved after TDR-01 correction assessment.
- Recording: advisory-durable/manual; no governed lifecycle identity selected.
- Scope: System and Engineering, Validation, Packaging and Release models for ENG-SR-16 and coordinated tooling organization; separate from the preceding test relocation.
- Material findings: TDR-01, resolved below.
- Next owner: Plan author for concrete scoped delivery allocation and independent Delivery Review.
- Claim limits: suitable engineering basis for authorized scoped planning; no formal lifecycle settlement, implementation approval, release or branch readiness.

## Finding TDR-01

- Finding ID: TDR-01.
- Severity: minor, required before planning reliance.
- Finding scope: cross-artifact.
- Affected subjects: `docs/design/engineering/packaging.md`, `docs/design/engineering/validation.md`, `docs/design/engineering/release.md`, coordinated through Engineering.
- Owning stage: design.
- Location/evidence: Packaging's new Building Block section declares `scripts/resources/boundary-first/boundary-first-resources.yaml`, but its retained Boundary resources section still says the manifest moves to `scripts/boundary-first-resources.yaml`. Validation's current realization text and Release's Existing block table also name internal old paths while new sections declare new directories. The new destination and legacy/current placement are not explicitly distinguished at these normative references.
- Required outcome: one unambiguous prospective target and adoption boundary, with prior placements clearly current-until-migration or superseded. A planner should not need to guess which 'moves to' instruction governs.
- Safe resolution: reconcile affected current references now, or add an explicit cross-owner transition statement declaring ENG-SR-16 target paths authoritative for this migration and older internal/resource paths current only until their coordinated move. Preserve supported command paths and historical identities. No broad historical replacement is required.
- Decision need: none; user already selected the target organization.

The author is `/root`; reviewer `/root/validation_design_review` is a separately delegated agent and has edited no engineering member. This finding was recorded before correction. Existing test-refactor reviews do not approve these new subjects.


## Exact approved package and correction disposition

The author reconciled the current internal code paths and Packaging's conflicting manifest destination. TDR-01 is resolved: the boundary manifest has one target under `scripts/resources/boundary-first/`, while supported command entrypoints retain their existing paths. Filename-only module labels identify responsibilities, not competing deployment roots. The separate dual-use `scripts/release_evidence.py` command is explicitly retained as a thin entrypoint.

CLI subject inspection returned these exact complete members after correction:

| Member | Identity |
| --- | --- |
| `docs/design/system.md` | `sha256:4eedbac3ea4702f50c84ebafec521663759debe48b183496272e9d420e1b1f86` |
| `docs/design/engineering/engineering.md` | `sha256:cadf64631c82db8341bb3d67b892582dee5f0670f827c36b62968e59a395f64c` |
| `docs/design/engineering/validation.md` | `sha256:4d668122366066044b50e81f2223618280351d1dba8a6fed8c6d87a2039cb626` |
| `docs/design/engineering/packaging.md` | `sha256:0aec3cfc2bf73424bf08d8c4efb775e4f7b5051b8417e8ebf1c90ada91aedbfa` |
| `docs/design/engineering/release.md` | `sha256:1cae90f16d152c7811eec499036dc4e7f8f63f82acd62d6b71c58f131d5f19b8` |

## Assessment rationale

ENG-SR-16 supplies a bounded implementation organization, not a new public product: stable commands, explicit capability-owned packages, grouped authored resources and coherent consumer migration. System delegates detailed ownership to Engineering; Validation, Packaging and Release preserve their respective behavior and external-action boundaries. The scope does not authorize unrelated helper cleanup or wildcard compatibility exports. Unknown consumers remain an investigation obligation before removal.

The complete Engineering, Packaging and Release members were read, alongside the complete previously read System/Validation basis and their current full baseline-relative changes. Existing review policy, stable-plan allocation and Constitution remain unchanged dependencies. Current model views continue to explain their real actors, artifacts, processes and permissions; the new Engineering building-block diagram adds internal placement without inventing runtime services. Existing model-local requirements and important legacy/retirement scopes remain intact. This assessment does not approve historical initiatives or every referenced child contract anew.

Source feasibility inspection confirms material consumers that Delivery must address: Python supervisor/discovery bootstraps embed `validation_execution` imports and its directory; Node worker lookup uses sibling location; `validate-record-store.mjs` imports a snapshot helper; candidate code derives both loaded and candidate source identity from current script placement. `release_evidence.py` has a real `__main__` entrypoint. The chosen explicit imports, stable dual-use command wrapper, root-aware worker/resource resolution and whole-source fixture copying can support those paths without a new service or dependency.

The author corrected the initially inaccurate statement that release identity already covered nested files. The source currently hashes only top-level `.py` and `.sh`. The reviewed contract now explicitly extends that loaded/candidate guard to authored nested implementation and resources before and after preparation, excluding generated bytecode. This is necessary to prevent relocated code escaping the existing guard. Delivery must allocate meaningful changed nested code/resource rejection, ordinary import-created bytecode non-interference, complete source enumeration and unsupported unsafe input handling; merely checking a new hash string is inadequate.

Package representations, canonical skill bytes, closed manifest semantics, archive/installed resource populations and publication authority remain unchanged. Resource paths and source identities necessarily change, so preserved outcomes require actual generated archive/candidate/installed-consumer observations. Command arguments, results, exit codes, working-directory behavior, direct workers and old/new deletion routing are explicit compatibility requirements. Existing representative success/failure scenarios and coherent rollback give Plan enough basis to allocate proof without treating structural validity as implementation success.

## Evidence and handoff

Reviewer independently ran exact CLI subject inspection and:

```bash
python scripts/validate-boundary-first.py --check --path docs/design/system.md --path docs/design/engineering/engineering.md --path docs/design/engineering/validation.md --path docs/design/engineering/packaging.md --path docs/design/engineering/release.md
```

All five members passed structure/reference validation; the tool explicitly limits that result to structure and references. Source inspection and the semantic assessment above supply the engineering judgment; no migrated implementation or package output is claimed to have passed.

This exact five-member package is suitable for the user's authorized scoped planning. The plan must enumerate actual module/resource moves, dual-use entrypoints, worker/import and fixture consumers, recursive source-identity coverage, stable command compatibility and integrated proof, with independent Delivery Review before implementation reliance. No new proposal or governed change identity is inferred. Original test-relocation approvals retain their original subjects and do not supply this new approval. Subsequent material member changes require appropriate independent reassessment.

Before handoff the author added Engineering’s explicit current-until-migration transition sentence. The reviewer inspected and accepted that final refinement and refreshed its Engineering identity above; it clarifies TDR-01 without broadening scope. The structural pass cited above preceded this final prose sentence and is not claimed as a rerun against it.

## Narrow applicability reassessment: unknown path terminology

Validation's tooling-placement clause now says unknown paths remain rejected by existing unsupported/unclassified handling, replacing the narrower statement that all remain unclassified. The exact revised Validation subject is `sha256:96139f158cf9f2097afebf1ed6dd72729a64c8610fe71fd37bb17ee49dcf90d8`, obtained through CLI subject inspection. The reviewer inspected the clause and existing selector handling: unknown scripts already use `script-unsupported` and block; other unknown inputs remain unclassified. This correction preserves fail-closed behavior and avoids introducing a new classification promise. It changes no command, scope, permission, observation or evidence requirement. The other four approved subjects remain unchanged by this correction.

The reviewer approves the package with this revised Validation identity for the same scoped reliance. Original identities above retain their original judgments; this explicit reassessment, not automatic hash matching, supplies renewed applicability.
