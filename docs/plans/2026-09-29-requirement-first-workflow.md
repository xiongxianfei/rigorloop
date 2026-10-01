# Requirement-first workflow delivery plan

## Purpose / big picture

Coordinate replacement of the Proposal-first workflow with the accepted requirement-first responsibilities and one mandatory whole-change Code Review gate. This draft collects delivery intent after the system-wide ownership design; it does not authorize implementation or claim reviewed delivery readiness.

## Current Handoff Summary

This is a document-based refactor under the [Constitution exception](../../CONSTITUTION.md#workflow-and-review). No governed Change record is selected. Mutable progress and assessments belong in separate operational evidence, not this plan. The exception does not waive implementation completion or external-action requirements.

## Source artifacts

- Requirement basis: [analysis](../../design/requirements/workflow-refactor.md) and its [workflow assessment provenance](../../design/requirements/sources.md#src-workflow-requirement-review).
- Architecture: [composition and owning records](../../design/architecture/README.md#requirement-first-workflow-composition), including parent contracts and Module realization decisions.
- Verification intent: [Operations](../../design/architecture/modules/MOD-018-engineering-operations/test-design.md) and [Governance](../../design/architecture/modules/MOD-017-engineering-governance/test-design.md) test designs, under the [shared test rules](../design/test-design/rules.md).

## Context and orientation

The owning [v4 record contract](../../design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md), [v2 command contract](../../design/architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/README.md), [package contract](../../design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/README.md) and [replacement contract](../../design/architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/README.md) define the detailed design input. Delivery must allocate their implementation and proof after applicable integrated Design assessment. Requirement acceptance does not establish either readiness claim.

The existing v3 stages and Proposal subject retain their historical meanings. The target uses separate requirement/design bases and gate attempts. Package installation supplies facts to adoption; it cannot silently activate policy or approve work. Canonical sources, generated consumers, validators and selected active-work state must agree before activation.

## Non-goals

- SQLite implementation, bulk historical cleanup, and deleting `docs/changes/` belong to the separate operational-store initiative.
- No new Module per skill, duplicated REM manual, mandatory milestone review, invented CLI command or automatic PR authorization.

## Requirements covered

SR-079–081 allocate primarily to M1; SR-082 spans M1–M3; SR-083 spans M1–M3. The boundary refinement of existing SR-042–044 allocates immutable assessment correction and truthful commit behavior to M2; refined SR-065/SCN-063 allocates separately authorized obsolete-unit retirement to M3. Shared SR-027–029 and SR-053–055 retain their authority, provenance and portable-invocation limits. AR-029–042 constrain the responsible Modules; this plan does not author substitute architectural obligations.

## Milestones

### M1. Reconcile methods and specialist contracts

- Kind and purpose: implementation checkpoint establishing one coherent authored workflow.
- Owners and scope: MOD-008 methods and MOD-012 guidance; replace `skills/proposal`, `skills/proposal-review`, and combined `skills/design`; reconcile `route`, `plan`, `delivery-review`, `implement`, `code-review`, `verify`, conditional resources, examples and templates.
- Dependencies: applicable integrated design and Delivery Review; no implicit execution permission from this draft.
- Steps: reconcile owning Workflow, Assessment and authoring contracts and Constitution adoption; author replacement responsibilities from canonical REM; update handoffs and remove obsolete active paths with their consumers.
- Required proof TG-M1: prepared-task walkthroughs for SCN-075–081, including unchanged requirement reuse, incomplete Function/AR design after requirement approval, wrong-owner corrections, advisory feedback and a one-milestone Change.
- Observable completion: coherent source contracts and required checks complete, with exact walkthrough subjects and actual findings retained. No review ID is needed merely to finish this milestone.
- Validation allocation: `bash scripts/ci.sh --mode explicit --path skills/route/SKILL.md`; expand the explicit path set to all actual changed owning files and use the selected repository checks. Semantic walkthroughs supplement structural checks.
- Recovery: retain exact earlier sources before replacement; stop affected dependent work when the authored contract is mixed. Do not claim installed adoption from source edits.

### M2. Realize successor recording and guarded workflow state

- Kind and purpose: implementation checkpoint preserving truthful history and current applicability.
- Owners and scope: MOD-010/011 admission, persistence and recovery; MOD-006/007 semantic work/assessment support. Reconcile records, workflow and targeted-recording schemas, command adapters, validators and tests using the approved detailed contract.
- Dependencies: the reviewed v4/v2 specifications, M1 semantics and a supported adapter satisfying atomicity, identity and recovery. The specified initial v4 adapter reuses the existing filesystem transaction engine and private local mapping, so SQLite migration is not a prerequisite. SQLite remains the target under the separate store initiative. Portable guidance may proceed before governed recording is available, but M2 cannot claim completion without its actual adapter and proof.
- Steps: implement scoped operations and unknown-value rejection; separate milestone progress from formal gate attempts; adapt the existing file transaction engine to the v4 private mapping and its declared capacity limits; implement verified content-addressed payload publication before metadata commit; implement explicit selected-work migration with provenance; remove obsolete internal active paths while preserving agreed external compatibility.
- Required proof TG-M2: missing and stale approval, repeated correction attempts in one gate, contradictory evidence, unknown stage/scope rejection before consistency checks, stale concurrent writes, interrupted publication and failure reported after commit. Verify preserved historical bytes and unrelated facts independently.
- Observable completion: current-subject reliance and actual publication outcomes follow the accepted contract; old Proposal/milestone judgments are not promoted to new approvals. Record exact fixture subjects, observed state and command outcomes.
- Validation allocation: use `bash scripts/ci.sh --mode explicit --path docs/design/cli/cli.md --path docs/design/cli/records.md` plus the actual new schema, dispatch, adapter and test paths allocated before Delivery Review. Validate new v4 schema definitions and v2 dispatch with unknown values for every new closed vocabulary, and real adapter commit/race/recovery outcomes. The documented successor commands must not be used as if already installed.
- Recovery: retain the current supported contract and original records; expose unavailable affected workflow if compatibility is incomplete. Do not automatically replay stale intent or infer successful rollback.

### M3. Integrate packaging, installation and selected adoption

- Kind and purpose: implementation checkpoint proving coherent replacement at the consumer boundary.
- Owners and scope: MOD-013 production, MOD-014 installation, MOD-006 adoption and MOD-012 consumers; public catalogs, adapters, navigation, validation selectors and installed resources.
- Dependencies: compatible M1/M2 outputs and a reviewed bounded replacement/recovery contract.
- Steps: generate the target inventory and checksum-bound workflow descriptor under a new release identity; qualify that candidate and old-client rejection; implement the explicit replacement-profile flag and union preflight; retain obsolete units outside discovery and publish only authorized candidate units; reconcile selected active work and confirm compatibility before explicit activation per Change.
- Required proof TG-M3: SCN-082 with partial replacement, unavailable conditional references, unknown or mixed contracts, competing adoption actors and unrelated active Changes. Compare actual installed bytes, original historical bytes, current contract identity and explicit activation disposition.
- Observable completion: consumer parity and selected adoption/recovery proof, preserving unrelated user work. Installation success alone cannot establish activation. Preserve candidate identity and actual installation effects in evidence.
- Validation allocation: owning [Packaging](../design/engineering/packaging.md) and [Release](../design/engineering/release/release.md) candidate checks, plus `bash scripts/ci.sh --mode local` for the complete changed scope; manual/operational observations must identify subjects and limitations.
- Recovery: stop affected dependent work after partial replacement; resume the earlier contract only if all required components remain compatible and intact, otherwise recover explicitly. No atomic whole-project rollback is promised.

## Final review checkpoint

All implementation and required checks precede one mandatory independent whole-change Code Review gate. Optional explicitly requested interim advice is not a milestone prerequisite or whole-change approval. Corrections return to the responsible owner; renewed assessments remain within the same gate and preserve earlier attempts. Applicable approval precedes distinct final Verify; a PR requires separate authority.

## Change-level verification

TG-FINAL-1 covers SR-079–083 and the shared assurance/guidance obligations across M1–M3. Exercise request reuse through accepted requirements, composed design, checked milestones, optional advice, whole-change correction and distinct Verify using the actual selected candidate. Include stale review/adoption races, missing installed resources and committed-write reporting failure: child checks can pass while these interactions fail. Inspect complete current-subject coverage, independently expected routing, preserved history and actual adoption state. Reuse applicable local evidence rather than rerunning unaffected checks without cause.

## Risks and recovery

The main risks are mixed contract activation, loss of historic judgment meaning, false approval from storage success and unintended deletion of installed user content. The owning designs supply failure containment and explicit recovery. Keep recoverable original identities before replacement; neither a package backup nor a later successful retry alone proves safe restoration.

## Dependencies

Applicable integrated Design assessment and Delivery Review precede implementation reliance. Exact implementation path/check allocation, qualification of the specified initial adapter and explicit ordering for any later operational-store migration must be completed before this draft is accepted. Storage and workflow retain separate acceptance claims; an absent backend cannot be hidden by source-only workflow completion.

## Decision log

| Decision | Reason | Alternative rejected |
| --- | --- | --- |
| Keep sequencing here and meaning with model owners | A completed migration does not retire current design | Standalone workflow design doubling as plan and evidence |
| One whole-change review gate, with reassessment | Milestones organize implementation and proof | Mandatory approval per milestone |

## Readiness

This is draft delivery intent. It is not a completed detailed plan, a Delivery Review outcome or implementation authorization. Actual assessments and progress remain separately recorded under the applicable project contract.
