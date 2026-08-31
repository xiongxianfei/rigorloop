# ADR-20260831-verification-ownership-without-test-spec-stage: Co-locate Verification Ownership

## Owning change record

`docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml`

## Context

RigorLoop currently requires a feature specification, an execution plan, and a separate test specification before implementation. The Lightweight Requirement-to-Delivery Model made the specification the owner of observable system requirements and the plan the owner of requirement allocation and work decomposition. A mandatory test-spec artifact now repeats scenarios and traceability already owned at those two boundaries.

Removing the artifact affects more than prose. The stage appears in governed lifecycle vocabularies, review-package membership, CLI transition rules, validators, skill packages, generated adapters, templates, examples, and historical records. The replacement must preserve pre-implementation verification planning, fail-closed lifecycle behavior, and the authority of existing governed records without introducing a renamed verification artifact.

## Decision

For newly governed changes after activation, verification responsibility is co-located with the requirements and allocated delivery work it validates:

- the specification owns observable behavior, failure behavior, boundaries, compatibility expectations, and important scenarios;
- the architecture explains how system requirements are realized and identifies verification-relevant technical boundaries;
- the plan owns milestone allocation, safe implementation order, milestone verification groups, change-level verification, and required evidence expectations;
- Delivery Review approves one exact plan-centered delivery package by jointly assessing implementation readiness and verification adequacy;
- implementation creates the concrete tests and checks and records evidence, while Verify evaluates evidence closure.

The active lifecycle vocabulary and routing graph remove `test-spec` authoring, `test-spec-review`, test-spec settlement, and test-spec membership in Delivery Review. Unknown stage, artifact, review, and outcome vocabulary continues to fail closed before consistency checks.

Historical test-spec artifacts, review records, and settled lifecycle evidence remain valid read-only records. A change already governed under the prior contract continues that registered contract unless Workflow performs an explicit, validated migration. Activation updates canonical skills, workflow rules, schemas, validators, templates, documentation, tests, and generated adapter packages as one coherent compatibility boundary; mixed old and new packages are invalid.

Use `lifecycle_contract: stage-owned-change-local-v2` as the durable discriminator for the no-test-spec graph. Activation creates one tracked, schema-validated compatibility manifest containing the activating source revision and the complete sorted set of pre-activation change IDs, each bound to its observed contract class (`stage-owned-change-local-v1` or `legacy-unversioned`). The manifest is immutable activation evidence, not mutable lifecycle state. `new-change` writes v2 after activation.

A reader classifies a record by its explicit contract value and the manifest. V2 selects the new graph. V1 or an absent contract is accepted only for a change ID whose manifest entry has the same class; that record continues the prior graph whether it is in flight or completed. A non-manifest v1 or unversioned record, an unknown contract value, a class mismatch, or v2 state containing an active test-spec stage or package member fails before consistency interpretation. No creation date, current stage, artifact presence, Git reachability, or network lookup is a discriminator.

An optional workflow-owned contract migration atomically changes an eligible manifest-listed record from its prior class to v2 and writes an identity-bound migration receipt in the existing lifecycle coordination state. It requires current artifact identities, a v2-valid target state, verification content already absorbed by the plan, and explicit invalidation or preservation of affected review authority. Failure leaves the prior bytes and authority unchanged. The first implementation may omit this optional operation; omission means prior-contract changes finish their registered graph.

Before activation produces any v2 record, rollback restores the complete prior authoring and routing package while retaining the manifest as unused evidence. After a v2 record exists, recovery is a forward compatibility release; restoring v1 as the default would require a separately approved contract migration design because rewriting v2 records or silently reintroducing test-spec obligations is unsafe.

Verification groups are lightweight plan-local identities connecting requirements and allocated work to later tests and evidence. They are not a new governed artifact, lifecycle stage, or requirement hierarchy.

## Alternatives considered

- Keep the standalone test-spec stage and reduce its template: rejected because ownership and synchronization remain duplicated even with a shorter document.
- Rename test-spec as proof obligations or verification plan: rejected because it recreates the same mandatory lifecycle surface under another name.
- Merge specification and plan: rejected because system behavior and delivery sequencing have different owners, audiences, and change cadence.
- Remove all test-design guidance: rejected because the goal is to preserve rigor while relocating ownership; specialist methods remain conditionally loaded plan references.
- Hard-delete all test-spec vocabulary and records: rejected because historical evidence and already-governed changes must remain interpretable and authoritative.

## Consequences

New changes have fewer artifacts, review rounds, settlement states, and overlapping context loads. Plans become more substantial where delivery risk requires migration, concurrency, compatibility, recovery, security, or cross-system verification. Delivery Review assumes explicit responsibility for challenging both sequence and proof adequacy.

The lifecycle engine and validators need separate treatment of v2 active vocabulary and manifest-bound prior compatibility. Removal work must inventory every active and generated surface and prove that unknown values do not fall through. Release and adapter validation must reject mixed packages. The tracked activation manifest adds bounded generated inventory and baseline maintenance, but avoids runtime Git-history or date inference.

This change does not define concrete test mechanics in the specification, make milestone order primarily test-driven, require one test per SR, or alter the downstream Code Review and Verify responsibilities.

## Follow-up

- Reconcile the feature specification with this boundary.
- Design Review must approve the exact architecture, ADR, and specification package.
- Delivery planning must define the atomic activation, compatibility fixtures, validation proof, and rollback sequence.
