# Engineering Model Design

Model validation contract: model-document-v1

Owning change: [three-model reconciliation](../../changes/2026-09-12-unified-validation-model/change.json).

## Introduction and Goals

Engineering owns how this repository builds, proves and delivers high-quality published skills and the CLI. It uses RigorLoop's published behaviors as development tools while retaining an independent assessment of the candidate. System defines the product composition; Skill and CLI define what the delivered products must do.

## Context and Scope

Inputs are authorized product direction, exact affected contracts, the selected development tool basis and repository sources. Outputs are implemented candidates, attributable validation and assessment evidence, distributable packages and authorized public release observations. No hosted agent runtime, third customer executor product or automatic external action is introduced.

| Submodel | Owner | Product contribution |
| --- | --- | --- |
| Development | [Development](#development) | Plan and implement the product using its behaviors, obtain independent assessment and maintain a resumable basis. |
| Validation | [Validation](validation.md) | Useful proof, isolated execution, bounded concurrency and truthful results without a validation cache. |
| Packaging | [Packaging](packaging.md) | Reproducible skill archives, CLI package composition and installer metadata. |
| Release | [Release](release.md) | Candidate qualification, publication authority, observed public identity and recovery. |

## Architecture Constraints

Canonical skill content remains in `skills/`; executable source remains under `packages/rigorloop/`. Repository scripts implement development validation and package production; hosted CI delegates to them. Shared criteria can be referenced by published capabilities, but repository-specific operations are not a customer prerequisite. Original adoption and historical review identities remain scoped to their actual subjects.

## Requirements

| ID | Required behavior |
| --- | --- |
| ENG-SR-01 | Engineering MUST realize and assess the Skill and CLI product contracts using the Development, Validation, Packaging and Release submodels; it MUST reference product behavior rather than redefine it. |
| ENG-SR-02 | Development MUST identify the approved product subjects, active work and required reviews before implementation, use bounded milestones and route a behavioral gap to its owning Design. |
| ENG-SR-03 | When developing RigorLoop with RigorLoop, Development MUST distinguish the tools and skill versions used to perform work from the candidate under assessment. Candidate self-use alone MUST NOT establish correctness or independent approval. |
| ENG-SR-04 | Repository work MUST retain actual implementation evidence, required milestone reviews, fresh independent whole-change Code Review and distinct final Verify under the Skill Assessment contract before governed closeout is claimed. |
| ENG-SR-05 | Validation MUST derive protective checks from product contracts, execute isolated cases with bounded shared parallelism, report actual results and limitations, and remove validation-result caching under its exact cleanup map. |
| ENG-SR-06 | Packaging MUST produce the supported skill archives and CLI npm candidate from canonical sources in isolated output, preserving their declared contents, identities and common interface without mutating active skill installations. |
| ENG-SR-07 | Integrated proof MUST assess generated/packed skills and the actual candidate CLI at their documented command, resource, record and installation boundaries; independent local passes MUST NOT substitute for compatibility evidence. |
| ENG-SR-08 | Release MUST qualify an exact candidate, obtain required external authorization, publish only that candidate and record observed public outcomes and recovery limitations. Local validation and engineering closeout MUST NOT supply publication authority. |
| ENG-SR-09 | A failed check, inconsistent contract, changed evidence basis or interrupted operation MUST return to the affected owner with its actual state preserved. Corrections MUST receive affected reassessment before renewed reliance. |
| ENG-SR-10 | Source retirement MUST preserve stable requirements, decisions, useful negative/regression proof and historical record identities, reconcile actual readers and remove superseded sources and exclusive machinery. Unknown live consumers MUST block their affected removal. |
| ENG-SR-11 | Repository engineering procedures MUST remain contributor/governance content. Published skills MUST NOT require this repository’s executor, paths or internal record identities for ordinary customer use. |
| ENG-SR-12 | The three-model transfer MUST include coherent Skill/CLI instructions, recording and package consumers, and the selected no-cache/source cleanup before adoption. Design authoring MUST NOT claim implementation, final Verify or customer activation. |

## Development

Development applies Skill Workflow, Authoring, Implementation and Assessment. It records which installed or checkout tools performed work and which source/package identities are the candidate. For this repository, `node packages/rigorloop/dist/bin/rigorloop.js` is a checkout entrypoint; its use is not evidence that the candidate CLI is correct. Candidate tests exercise the actual relevant package/record/installation boundary with independent assertions.

The approved proposal and exact affected Designs feed a stable delivery plan and independent Delivery Review. Implementation proceeds through bounded milestones, recording commands actually run and outcomes. A non-final milestone review can permit the next allocated milestone; final whole-change Code Review remains fresh and distinct from Verify. A specification gap returns to Authoring, a test defect to its implementation owner, and an assessor's finding remains with that assessor for disposition.

## Validation

[Validation](validation.md) is the sole owner of reusable proof criteria and repository check execution. Skill capabilities consume the reusable criteria under their applicability; this repository's plan allocates the concrete tests. All workers, nested invocations and independent cases share the declared budget; deterministic summaries expose missing, skipped, failed and interrupted work. No cache restores prior execution as a current pass.

## Packaging

[Packaging](packaging.md) owns canonical-to-artifact generation and the installer-consumed metadata/hash representation. Skill owns content and capability behavior. CLI Installation owns target writes and safe replacement. Their shared package boundary is explicit: producing an archive never installs it, and local archive installation never supplies an alternate trust root.

## Release

[Release](release.md) consumes exact package identities, applicable engineering assessments and actual validation. Its preparation and public-observation work is distinct from the implementation candidate used during development. Required external authorization remains separate from Code Review, Verify and any saved status. An uncertain public write is inspected under Release recovery rather than blindly repeated.

## Integrated operation and failure

A Skill or CLI requirement change identifies both affected consumers before implementation. After the reviewed work is implemented, generated skill resources and documented requests are checked against the actual CLI candidate. Negative cases demonstrate missing resources, unknown input, stale revisions, unsafe installation destinations and mismatched artifact identity where applicable. A passing checker with an unmet requirement remains inadequate evidence; independent assessment returns the work to its owner.

If the development CLI cannot safely persist a decision, stop that write and preserve the actual outcome. Do not use the candidate's success label to manufacture a review or bypass conflict recovery. A failed validation/package/release operation reports partial work and limits under its own contract. Existing governing records, installed customer files and unrelated source changes are not cleanup targets.

## Deployment and maintenance

Development tools operate in the repository under its existing permissions. Package output uses temporary or explicitly selected non-installation locations. Publication uses the exact Release-owned authorization and public endpoints. Individual skills remain independently usable by customers; choosing governed recording or CLI installation introduces the corresponding CLI dependency, not a dependency on this repository's engineering environment.

## Acceptance and boundaries

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | ENG-SR-02, ENG-SR-05 | An authorized Skill or CLI change has a named product contract and bounded proof; missing authority is surfaced before dependent implementation. |
| State/lifecycle | ENG-SR-02, ENG-SR-04 | Progress through milestones retains required reviews; a local pass or non-final review cannot close the whole change. |
| Identity/authority | ENG-SR-03, ENG-SR-08 | The development tool basis and candidate identities remain distinguishable; independent assessment and publication authority are not inferred from self-use. |
| Composition/path | ENG-SR-01, ENG-SR-07 | Generated skills and the packed CLI agree on resources, commands and records; a helper-only pass cannot hide incompatible products. |
| Temporal/retry | ENG-SR-05, ENG-SR-09 | Concurrent cases share one budget; changed subjects trigger affected proof and reassessment rather than cached success. |
| Failure/recovery | ENG-SR-09, ENG-SR-10 | Failed or interrupted operations preserve actual partial state and route correction without deleting unrelated sources or historical records. |
| Compatibility/migration | ENG-SR-10, ENG-SR-12 | Every retired source has a resolved consumer/meaning disposition; the hierarchy does not silently revive retired runtime formats or remove required proof. |
| External/environment | ENG-SR-08, ENG-SR-11 | Customer individual skills work without this repository executor; public release claims require real Release observations and authorization. |

## Decisions and assessment basis

The development process is a consumer of published capability behavior, not a second copy of it. Separate Development from Skill Implementation because one defines this repository's allocation and tooling basis while the other defines reusable agent behavior. Separate Packaging from CLI Installation because artifact production and user filesystem mutation have different inputs, authority and failure recovery. Release keeps publication ownership. The integrated counterexamples above justify these boundaries without claiming executed candidate tests.

## Source disposition and follow-through

The [reconciliation map](../../changes/2026-09-12-unified-validation-model/design-reconciliation.md) identifies exact source identities, retained contracts, Distribution's split and current consumers. The mapped Validation cache/source/script retirement remains required implementation work. Detailed retained specifications remain named authorities for unmigrated obligations. Source changes do not establish reviewed implementation or successful Verify.

## Next artifacts

Independent Design Review of System, Skill, CLI, Engineering and the affected child/legacy contracts, followed by Delivery allocation. Required candidate tests, reviews and distinct final Verify establish coherent implementation; publication retains separate authority.
