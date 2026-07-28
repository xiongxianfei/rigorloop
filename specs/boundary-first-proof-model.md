<!-- Template: spec-skeleton-v1 -->
<!-- Skill: spec -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/spec/SKILL.md -->
<!-- Readability contract: use semantic source lines; keep stable IDs and tables for repeated proof or mapping structures. -->

# Boundary-First Proof Model

## Status

draft

Boundary-first contract activation: pending
Activation record identity: -

## Related proposal

[Portable Boundary-First Capability for Published Skills](../docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md)

## Goal and context

This spec defines a portable boundary-first contract for behavior-changing
feature specs, test specs, plans, implementation, review, and verification.

The contract makes examples subordinate to governed requirements and explicit
boundaries.
It gives published-skill users one method that works from installed skill
packages and project-local artifacts without a particular agent runtime,
network service, model identity, or RigorLoop repository checkout.

This spec owns the boundary vocabulary, normalized record relationships,
activation rules, and semantic-versus-deterministic claim boundary.
`specs/rigorloop-workflow.md` continues to own stage order and handoff
semantics.
`specs/skill-contract.md` continues to own packaged-resource mapping,
self-containment, generation, and adapter parity.

This is the bootstrap spec for `boundary-first-v1`.
It does not carry the activation marker that it defines because repository
activation remains pending until every governed skill and package surface is
current together.

## Glossary

- `boundary contract`: the versioned rules connecting requirements,
  applicable dimensions, boundary definitions, interactions, examples, and
  proof obligations.
- `core dimension`: one member of the closed first-version applicability
  inventory.
- `boundary`: one requirement-owned partition, transition, invariant, or
  outcome set within an applicable core dimension.
- `selected interaction`: a requirement-owned composed hazard involving at
  least two defined boundaries.
- `proof obligation`: a test-spec record mapping an approved boundary or
  selected interaction to concrete automated, manual, or hybrid proof.
- `governed skill`: one published lifecycle skill required to carry
  stage-local boundary-first behavior.
- `shared method reference`: the byte-identical
  `references/boundary-first-method-v1.md` file packaged with every governed
  skill.
- `structural validation`: deterministic validation of record shape, closed
  values, identifiers, references, fixtures, packaging, and byte parity.
- `semantic review`: independent judgment of applicability, completeness,
  ownership, interaction selection, sequencing, or proof adequacy.
- `substantive normative revision`: a change to governed behavior rather than
  spelling, formatting, links, lifecycle settlement, review references, or
  non-normative clarification.

## Examples first

Example E1: a simple documentation behavior has concise non-applicability

Given a new behavior-changing feature spec governs a documentation-only
rendering rule
When the author applies `boundary-first-v1`
Then `input-domain` and `compatibility-migration` may be applicable
And the remaining dimensions may be `not-applicable` with concise
requirement-grounded rationales
And no standalone boundary artifact or Cartesian interaction matrix is
created.

Classification: illustration.
Governing requirements: PBF-R004, PBF-R010, PBF-R018.

Example E2: an example cannot create behavior

Given a spec example describes retrying interrupted work
When no requirement owns retry, replay, or recovery behavior
Then the example is classified as a discovery
And spec review stops for an upstream contract decision
And neither the example nor a validator invents the missing outcome.

Classification: discovery.
Governing requirements: PBF-R021, PBF-R022, PBF-R038.

Example E3: helper proof does not establish a composed public path

Given an applicable `composition-path` boundary includes a public entry point,
a helper, and a sibling entry point
When the proof map cites only a helper unit test
Then test-spec review reports inadequate proof
And implementation does not proceed until the public and material sibling
paths have direct proof or an approved narrower boundary.

Classification: illustration.
Governing requirements: PBF-R026, PBF-R032, PBF-R041.

Example E4: a historical spec remains valid

Given an accepted feature spec predates repository activation
When `boundary-first-v1` becomes active
Then the historical spec remains accepted without migration
And it adopts the marker only if it later receives a substantive normative
revision.

Classification: illustration.
Governing requirements: PBF-R050, PBF-R051, PBF-R055.

Example E5: rollback uses an existing immutable release

Given the active release must be withdrawn
When maintainers select the immediately preceding published release
Then repository validation confirms that release's existing adapter metadata
contains one passing archive identity for every currently supported adapter
And an authorized release operator performs any installation or publication
outside this capability
And no activation writer, rollback receipt, or historical attestation is
created.

Classification: illustration.
Governing requirements: PBF-R057, PBF-R058.

## Requirements

### Contract activation and scope

PBF-R001. The closed boundary contract version MUST be
`boundary-first-v1`.

PBF-R002. An adopting feature spec MUST record the literal metadata line
`boundary_contract: boundary-first-v1` in its `## Status` section after the
lifecycle status value.

PBF-R003. A feature spec MUST NOT record the activation marker while the
published capability state is `pending`.
In-flight opt-in is available only after activation is `active`.

PBF-R004. An adopting feature spec MUST contain the boundary record in that
same feature spec and MUST NOT require a standalone boundary artifact.

PBF-R005. The published capability state MUST use exactly one of `pending` or
`active`.

PBF-R005a. Before activation becomes `active`, one small release-activation
manifest MUST identify the contract version, state, activating release,
rollback release, governed skills, canonical reference identity, projection
identity, grandfathering baseline revision, and sorted grandfathered
feature-spec paths.
The activating release MUST be `-` while pending and MUST be one immutable
release tag while active.
The rollback release MUST be `-` while pending and MUST be the immutable tag of
the immediately preceding published release while active.
The grandfathering baseline revision MUST be `-` while pending and MUST be the
full source-control commit identity of the activating reviewed change's parent
revision while active.
Source control and release archives own historical byte identity; the
activation manifest MUST NOT duplicate a historical attestation store.

PBF-R005b. Architecture MUST select the release-activation manifest path and
format.
The manifest MUST be repository-local, deterministic, validator-readable, and
available without chat history or a network service.
Maintainers MUST settle it through an ordinary reviewed source change; this
capability MUST NOT require a state-writing activation script.

PBF-R005c. The grandfathered inventory MUST be derived only from the
grandfathering baseline revision recorded by the reviewed change that activates
the contract.
It MUST contain each top-level `specs/*.md` feature spec present at that
revision whose lifecycle status is `accepted`, `approved`, or `active`, except
this bootstrap spec, `README.md`, and files ending in `.test.md`.
It MUST exclude specs that already carry the activation marker.
Any feature-spec path first introduced after the baseline revision, including
by the activating reviewed change, MUST NOT be grandfathered.
Entries MUST be unique repository-relative POSIX paths sorted by raw UTF-8
bytes.

PBF-R006. Activation MUST change from `pending` to `active` only when the
shared method, all governed skill mappings and projections, structural
validators, review fixtures, generated output, adapter packages, and installed
skill cold-read proof are current together.
The activating reviewed change MUST update the release-activation manifest
only after those checks pass.

PBF-R007. Activation MUST fail closed if any governed skill or required
package surface is missing, stale, mixed-version, or byte-divergent.

### Core applicability inventory

PBF-R008. `boundary-first-v1` MUST use exactly these core dimensions:

| Dimension ID | Boundary ID prefix | Meaning |
| --- | --- | --- |
| `input-domain` | `BND-INPUT-` | Inputs, values, presence, absence, malformed values, limits, and unknown values. |
| `state-lifecycle` | `BND-STATE-` | Valid states, stale states, terminal states, and legal or illegal transitions. |
| `identity-authority` | `BND-AUTH-` | Identity, ownership, permission, authority, scope, and freshness. |
| `composition-path` | `BND-COMPOSE-` | Public, helper, sibling, alternate-entry, bypass, and composed paths. |
| `temporal-retry` | `BND-TEMPORAL-` | Ordering, duplication, concurrency, retry, replay, and idempotency. |
| `failure-recovery` | `BND-RECOVERY-` | Failure, interruption, partial work, rollback, resume, reconciliation, and dependency failure. |
| `compatibility-migration` | `BND-COMPAT-` | Historical data, old clients, mixed versions, migration, retirement, and rollback. |
| `external-environment` | `BND-ENV-` | External systems, resources, filesystem, network, platform, and operating limits. |

PBF-R009. Each core dimension MUST appear exactly once in an adopting feature
spec's applicability table.

PBF-R010. Applicability MUST use exactly `applicable` or `not-applicable`.

PBF-R011. An `applicable` dimension MUST cite at least one governing
requirement and at least one boundary defined by the same feature spec.

PBF-R012. A `not-applicable` dimension MUST use `-` for governing requirement
and boundary IDs and MUST include a concise non-applicability rationale.

PBF-R013. Undecidable applicability MUST block spec review rather than create a
third durable applicability value.

PBF-R014. Feature-specific dimension extensions MUST NOT be added in
`boundary-first-v1`.
A feature-specific boundary MUST be owned under the applicable core dimension;
a new dimension requires a later contract-version amendment.

PBF-R014a. A table cell with no applicable value MUST contain the literal
ASCII `-`.
Blank cells, em dashes, and other Unicode dash sentinels are invalid.

PBF-R014b. A table cell containing multiple IDs MUST serialize them as unique
IDs separated by comma followed by one ASCII space.
Ordering MUST follow first governing use and MUST remain stable across
downstream records.

PBF-R014c. Contract-owned boundary, interaction, and proof IDs MUST use the
grammars in this spec.
Test case, command, regression, discovery-gap, evidence, and manual-procedure
IDs MUST use the adopting project's stable ID grammar and MUST be nonempty
when their field is required.

### Feature-spec boundary record

PBF-R015. An adopting feature spec MUST serialize one contiguous record using
these headings in order:

```text
## Boundary model
## Boundary definitions
## Selected interactions
## Example ownership
```

PBF-R016. `## Boundary model` MUST begin with:

```text
Boundary model version: boundary-first-v1
Boundary model scope: <governed requirement IDs>
```

PBF-R017. The applicability table MUST use these exact columns:

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |

PBF-R018. A simple change MAY use concise non-applicability rationales and a
small number of applicable boundaries.
The contract MUST NOT require partitions or interactions that the governing
requirements do not admit.

PBF-R019. The boundary-definition table MUST use these exact columns:

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |

PBF-R020. Each boundary ID MUST match
`^BND-(INPUT|STATE|AUTH|COMPOSE|TEMPORAL|RECOVERY|COMPAT|ENV)-[0-9]{3}$`,
MUST be unique within the feature spec, and MUST be defined exactly once.

PBF-R021. Every behavioral example MUST be classified as exactly one of
`illustration`, `regression`, or `discovery`.

PBF-R022. An illustration MUST cite governing requirement and boundary IDs.
A regression MUST additionally cite one stable defect or regression ID.
A discovery MUST cite one stable gap ID and MUST route upstream without
creating normative behavior.

PBF-R023. The example-ownership table MUST use these exact columns:

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |

PBF-R024. An example MUST cite only boundaries defined in the same feature
record and requirements governed by every cited boundary.

PBF-R025. A selected interaction MUST involve at least two defined boundaries,
cite governing requirements, name an actual composed hazard, and define the
required composed outcome.

PBF-R026. Interaction selection MUST consider stale authority, partial retry,
public or helper bypass, sibling drift, compatibility migration, and
incident-derived hazards when admitted by the governing requirements.

PBF-R027. An interaction MUST be selected whenever correctness depends on one
boundary changing the success, failure, stale, interrupted, recovery, or stop
outcome of another boundary.

PBF-R028. The selected-interaction table MUST use these exact columns:

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |

PBF-R029. Interaction IDs MUST match `^INT-[0-9]{3}$` and be unique within the
feature spec.

PBF-R030. If no interaction is selected, the feature spec MUST replace the
interaction table with `No interaction selected: <requirement-grounded
rationale>`.

PBF-R031. Authors and reviewers MUST NOT generate a full Cartesian product of
dimensions, boundaries, partitions, or interactions.

### Test-spec proof record

PBF-R032. A test spec for an adopting feature MUST map every applicable
boundary and every selected interaction to at least one stable proof
obligation.

PBF-R033. The proof map MUST begin with the same boundary model version and
scope as its governing feature spec and MUST use these exact columns:

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

PBF-R034. Proof obligation IDs MUST match `^PRF-[0-9]{3}$` and be unique within
the test spec.

PBF-R035. `Proof level` MUST use exactly `unit`, `integration`, `contract`,
`end-to-end`, `smoke`, or `manual`.

PBF-R036. `Automation mode` MUST use exactly `automated`, `manual`, or
`hybrid`.
Automated proof MUST use `-` for manual procedure IDs.
Manual and hybrid proof MUST cite at least one stable manual procedure ID and
an evidence artifact.

PBF-R036a. `Coverage state` MUST use exactly `covered` or `gap`.

PBF-R036b. A `covered` row MUST provide governing requirement, boundary or
interaction, test case, proof level, automation mode, evidence or command
fields required by that mode, and required milestone values and MUST use `-`
for `Uncovered gap ID`.

PBF-R036c. A `gap` row MUST provide governing requirement, boundary or
interaction, required milestone, and one stable uncovered-gap ID.
It MUST use `-` for test case, proof level, automation mode, command, evidence,
and manual-procedure fields.

PBF-R036d. A `gap` row MUST NOT count as proof coverage and MUST block
test-spec-review approval and implementation until the governing contract or
proof map is corrected and rereviewed.

PBF-R037. A proof map MUST use exact approved requirement, boundary, and
interaction IDs and MUST NOT define, rename, infer, or repair them.

PBF-R038. A missing required boundary, interaction, or outcome MUST be
recorded as a `gap` row and routed to the feature spec or upstream owner before
implementation.

PBF-R039. Where a boundary admits them, proof partitions MUST cover valid,
invalid, missing, additional, stale, substituted, unknown, and conflicting
states.

PBF-R040. Stateful, mutating, or composed behavior MUST include direct proof
for applicable legal and illegal transitions, commit and partial states,
retry and replay, reconciliation and conflict, and public and material sibling
paths.

### Lifecycle ownership

PBF-R041. The governed skill set MUST be exactly:

```text
workflow
spec
spec-review
plan
plan-review
test-spec
test-spec-review
implement
code-review
verify
```

PBF-R042. Each governed skill MUST map the shared method reference with the
literal verb `READ` and a stage-specific load condition.

PBF-R043. Stage-local responsibility MUST be assigned as follows:

| Skill | Required responsibility |
| --- | --- |
| `workflow` | Route the method, locate governing artifacts, and stop on missing applicable ownership. |
| `spec` | Author the normative applicability, boundary, interaction, and example-ownership record. |
| `spec-review` | Judge applicability, boundary completeness, interactions, invariants, outcomes, and example ownership. |
| `plan` | Map applicable boundaries to independently closeable milestones, dependencies, affected surfaces, rollback units, and proof timing. |
| `plan-review` | Reject coupled primary boundaries, omitted dependencies, unsafe rollback, and proof sequencing that cannot close independently. |
| `test-spec` | Map every applicable boundary and selected interaction to proof without inventing contract IDs. |
| `test-spec-review` | Judge proof adequacy, negative coverage, fixtures, command ownership, and manual-proof boundaries. |
| `implement` | Stop on missing boundary or proof ownership and implement against the approved model and proof map. |
| `code-review` | Inspect composed public, helper, sibling, failure, stale, recovery, and escaped-boundary paths. |
| `verify` | Confirm contract-to-proof-to-implementation coherence and unresolved-gap closure. |

PBF-R044. Stage-specific stop conditions, review approval semantics, artifact
placement, lifecycle routing, and readiness claims MUST remain in the owning
workflow contract or skill rather than the shared method reference.

PBF-R045. `proposal` and `proposal-review` MUST remain outside the normative
first-version boundary-record authoring contract.

### Shared reference and deterministic support

PBF-R046. Every governed canonical skill MUST package one skill-local file at
`references/boundary-first-method-v1.md`.

PBF-R047. All governed skill-local reference files MUST be deterministic
projections of one canonical source and MUST be byte-identical.

PBF-R048. Canonical, generated, locally packed, and installed skill surfaces
MUST preserve the reference's skill-root-relative path and raw-byte SHA-256.

PBF-R049. Structural validators MUST check record shape, exact headings and
columns, closed vocabularies, identifier grammar, uniqueness, cross-references,
fixtures, mapped-resource presence, and byte parity.

PBF-R049a. After activation, structural validation MUST reject new
behavior-changing feature specs without the marker and MUST validate marker
and record shape when present.

PBF-R049b. Structural validation MUST use the release-activation manifest to
distinguish grandfathered feature specs from new feature specs.
It MUST NOT infer whether an edit to a grandfathered spec is substantively
normative.

PBF-R050. Structural validators MUST NOT claim semantic completeness,
applicability correctness, interaction adequacy, milestone isolation, proof
adequacy, implementation fidelity, or final evidence coherence.

PBF-R051. Structurally valid but substantively incomplete fixtures MUST be
review-skill fixtures, not semantic validator pass/fail claims.

### Compatibility, migration, and rollback

PBF-R052. Once activation is `active`, new behavior-changing feature specs and
existing feature specs receiving a substantive normative revision MUST adopt
the marker and records.

PBF-R053. After activation is `active`, an in-flight feature spec MAY opt in
before test-spec approval only when every downstream governed skill available
to that change uses `boundary-first-v1`.

PBF-R054. A substantive normative revision includes changes to behavior,
state, inputs, errors, identity, authority, security, persistence, data shape,
compatibility, migration, external integration, concurrency, retry,
idempotency, failure, interruption, rollback, or recovery.

PBF-R055. Spelling, formatting, links, status settlement, review-record
references, and non-normative example clarification MUST NOT activate the
contract by themselves.

PBF-R055a. `spec-review` MUST classify whether a changed grandfathered feature
spec is substantively revised.
An undecidable classification blocks review rather than allowing an unmarked
substantive change.

PBF-R056. Existing accepted historical specs MUST remain valid until
substantively revised and MUST NOT require automatic migration.

PBF-R057. Rollback validation MUST select the activation manifest's rollback
release and MUST read that release's existing adapter artifact metadata at
`docs/reports/adapter-artifacts/releases/<version>.yaml`.
That metadata is the ordinary evidence owner for adapter name, archive name,
archive SHA-256, and validation result.
The capability MUST NOT install or publish the selected release.
Any external installation or publication is owned by an authorized release
operator.

PBF-R058. Rollback validation MUST require exactly one `pass` artifact entry
for every adapter in `dist/adapters/manifest.yaml` and MUST reject a missing,
additional, duplicated, failing, or mixed-version entry.
Its output MUST identify the selected release tag and the complete ordered
adapter, archive, and SHA-256 matrix sorted by adapter name as raw UTF-8 bytes.
Rollback MUST NOT rewrite accepted feature specs, proof maps, project-local
boundary records, or the current source activation manifest.
The selected release exposes only the capability state and skill behavior
packaged in that release; rollback does not create a new capability state.
No repository rollback state, transaction receipt, historical attestation
store, or custom rollback writer is part of this capability.

### Semantic review and stop behavior

PBF-R059. `spec-review` MUST own semantic approval of dimension applicability,
boundary completeness, interactions, invariants, outcomes, and example
ownership and substantive-revision classification for grandfathered specs.

PBF-R060. `plan-review` MUST own semantic approval of boundary sequencing,
milestone isolation, dependencies, rollback units, and proof timing.

PBF-R061. `test-spec-review` MUST own semantic approval of proof adequacy,
negative coverage, fixture design, command ownership, and manual-proof scope.

PBF-R062. `code-review` MUST own implementation-fidelity review across the
approved boundary and proof map.

PBF-R063. `verify` MUST own final coherence checking without reapproving
requirements, architecture, planning, or proof design.

PBF-R064. A governed stage MUST stop when required ownership is absent, an ID
is stale or unknown, an example is the only behavior owner, an applicable
boundary or interaction lacks proof, helper proof substitutes for an admitted
public or sibling path, evidence is missing or stale, or a discovery requires
an upstream decision.

PBF-R065. No part of this capability MAY require a specific agent runtime,
model identity, network connection, sandbox, process-isolation mechanism,
workspace mutation interceptor, repository-local attestation store, or
immutable runtime evidence publication.

## Inputs and outputs

Inputs:

- an accepted proposal or other approved direction;
- project-local governing requirements;
- applicable historical compatibility constraints;
- approved architecture and plan inputs when those stages apply;
- supported adapter package definitions.

Outputs:

- adopting feature-spec boundary records;
- exact test-spec proof maps;
- stage-local governed skill guidance;
- one shared method reference projected into every governed skill;
- deterministic structural, fixture, packaging, and parity validation;
- independent review evidence for semantic judgments;
- release-activation evidence and read-only package identity validation.

No runtime certification report is an output of this capability.

## State and invariants

- The published capability state is one of `pending` or `active`.
- Pending state records `-` as the activating release, rollback release, and
  grandfathering baseline revision.
- Active state has one reviewed release-activation manifest, one immutable
  activating release tag, one immutable rollback release tag, one full
  grandfathering baseline commit identity, and one sorted grandfathered-spec
  path inventory.
- The boundary contract version remains `boundary-first-v1`.
- The eight core dimensions and two applicability values are closed.
- A feature spec owns boundary and interaction definitions.
- A test spec consumes exact approved IDs and does not create behavior.
- Examples remain subordinate to requirements and boundaries.
- All governed skills use the same shared reference bytes.
- Published skill packages remain self-contained.
- Structural validation and semantic review make distinct claims.
- Historical accepted artifacts remain valid until substantively revised.

## Error and boundary behavior

- Unknown contract versions, dimensions, applicability values, record columns,
  coverage states, proof levels, automation modes, or ID forms fail structural
  validation.
- Closed-vocabulary validation fails before dependent consistency checks.
- Missing mapped reference files or byte drift fail packaging validation.
- Missing or ambiguous semantic ownership blocks the owning review stage.
- A missing public or sibling path cannot be satisfied by helper-only proof.
- A discovery routes upstream and cannot silently become a requirement.
- Mixed governed-skill versions block activation.
- Missing, additional, duplicated, failing, or mixed-version rollback package
  identities block rollback readiness.
- Runtime fallback cannot make a structurally broken skill package valid.

## Compatibility and migration

Activation is prospective and release-scoped.
Historical accepted feature specs remain valid without migration.
New or substantively revised behavior contracts adopt only after activation is
`active`.
In-flight opt-in is permitted only before test-spec approval and only with a
complete governed skill chain.

Rollback validation selects the manifest's rollback release and checks its
complete adapter bundle against existing release metadata.
An authorized release operator owns any external installation or publication.
Artifacts already approved under `boundary-first-v1` remain valid historical
contracts.
Rollback does not mutate project-local feature specs or proof maps.

## Observability

Structural validation output MUST identify the artifact, record surface,
stable check ID, offending value or reference, and expected closed contract.

Activation validation output MUST identify the capability state, activating
release, canonical and projection identities, grandfathered path
inventory, and any new or changed feature spec that cannot be classified
structurally.

Packaging and parity output MUST identify the skill, relative reference path,
expected raw-byte SHA-256, actual SHA-256, and first divergent package layer.

Rollback validation output MUST identify the selected release tag and the
ordered adapter, archive, and SHA-256 matrix or the exact missing or conflicting
entry that blocks readiness.

Review records MUST identify the reviewed artifact identity, applicable
semantic owner, finding IDs, required outcomes, and disposition state.

No structural validation output may state or imply that semantic completeness
was proved.

## Security and privacy

The method records identities and authority boundaries when behavior admits
them, but it does not require secrets, credentials, private user data, model
identity, or runtime attestation.

Boundary and proof records MUST NOT embed secrets or private evidence when a
stable redacted artifact identity is sufficient.

## Accessibility and UX

No graphical interface is introduced.
Published Markdown MUST remain readable as text, use stable headings and
tables, and avoid color-only or diagram-only meaning.

Simple changes MUST be able to complete the applicability inventory with
concise rationales and without a separate boundary artifact.

## Performance expectations

Canonical structural validation SHOULD complete within the existing
skill-validator validation tier.
Package and clean-install parity checks MAY remain in the existing adapter or
release validation tier.

The contract MUST NOT require a Cartesian product of dimensions or
interactions, live agent execution, or network access for ordinary authoring
and review.

## Edge cases

EC1. An applicable dimension with no boundary ID fails validation.

EC2. A not-applicable dimension with a boundary ID fails validation.

EC3. A boundary owned by requirements outside the declared model scope fails
validation.

EC4. A duplicated boundary, interaction, example, or proof ID fails
validation.

EC5. An interaction citing one boundary fails validation.

EC6. No selected interaction is valid only with a requirement-grounded
rationale.

EC7. A discovery example with no gap ID blocks review.

EC8. A proof map citing a boundary from another feature spec fails validation.
Cross-feature boundary imports are not supported in `boundary-first-v1`.

EC9. An automated proof row with a manual procedure ID fails validation.

EC10. A manual or hybrid proof row without a procedure and evidence artifact
fails validation.

EC10a. A `gap` row with test IDs or proof metadata fails validation and cannot
count as coverage.

EC11. A formatting-only historical spec edit does not activate the contract.

EC12. A substantive edit to an old spec after activation requires adoption.

EC13. One stale projected skill reference blocks activation and packaging
parity.

EC14. A validator accepts structural completeness but cannot settle whether a
missing semantic boundary exists.

EC15. A runtime can decline to load an optional reference for an invocation,
but the mapped reference must still be present in its installed package.

## Non-goals

- Do not certify an agent runtime or model.
- Do not create a new boundary-review lifecycle stage.
- Do not create a standalone boundary artifact for every change.
- Do not derive normative behavior from examples or validators.
- Do not generate a Cartesian product of interactions.
- Do not automatically generate tests from boundary records.
- Do not retroactively migrate accepted historical artifacts.
- Do not partially activate across governed skills.
- Do not add an activation writer, rollback writer, transaction receipt,
  historical attestation store, or repository mutation protocol.
- Do not install or publish a rollback release; external release operations
  remain operator-owned.
- Do not decide progressive-disclosure optimization beyond the required
  packaged reference.
- Do not open, publish, or mutate external systems as part of the capability.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `PBF-AC001` | The version, published capability state and release evidence, eight dimensions, prefix mapping, applicability values, sentinels, delimiters, record headings, columns, coverage states, and identifier grammars are closed. |
| `PBF-AC002` | Feature specs own normalized applicability, boundary, interaction, and example-ownership records. |
| `PBF-AC003` | Test specs consume exact approved IDs, distinguish covered proof from blocking gaps, and cover every applicable boundary and selected interaction before implementation. |
| `PBF-AC004` | Examples are illustrations, regressions, or discoveries and never become implicit normative owners. |
| `PBF-AC005` | The ten governed skills have distinct stage-local responsibilities. |
| `PBF-AC006` | Every governed skill maps the same versioned `READ` reference with a stage-specific load condition. |
| `PBF-AC007` | One canonical source deterministically produces byte-identical skill-local, generated, packed, and installed references. |
| `PBF-AC008` | Structural validators reject unknown closed values before consistency checks and do not claim semantic completeness. |
| `PBF-AC009` | Independent spec, plan, test-spec, code, and verify gates retain their named semantic responsibilities. |
| `PBF-AC010` | Simple changes can use concise non-applicability rationales without a standalone artifact or Cartesian interaction set. |
| `PBF-AC011` | Prospective release activation, active-only in-flight opt-in, exact historical grandfathering, and read-only previous-release package validation are deterministic. |
| `PBF-AC012` | Activation cannot become active while governed skills or package surfaces are mixed, missing, stale, or byte-divergent. |
| `PBF-AC013` | The capability requires no runtime, model, network, sandbox, workspace-interception, or attestation dependency. |
| `PBF-AC014` | Structurally valid but semantically incomplete fixtures are judged by the owning review skills rather than semantic validator assertions. |

## Open questions

None.

Architecture must select the exact canonical shared-reference path and
projection mechanism within the approved one-source, deterministic-projection
contract.

## Next artifacts

1. Amend `specs/rigorloop-workflow.md` with the governed stage
   responsibilities and activation handoff.
2. Amend `specs/skill-contract.md` with the shared `READ` reference and
   deterministic projection requirements.
3. Perform independent `spec-review` on the complete contract amendment.
4. Record the required architecture assessment.
5. Author and review the architecture package.
6. Create and review the execution plan.
7. Create and review the matching test spec.

## Follow-on artifacts

- Workflow contract amendment: [RigorLoop Workflow](rigorloop-workflow.md).
- Published-skill contract amendment: [Skill Contract](skill-contract.md).
- Spec-review R2: [approved](../docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/spec-review-r2.md).

## Readiness

Draft revision ready for independent spec-review.
Published activation remains `pending` until the complete governed skill and
package bundle passes the release-scoped activation contract.
