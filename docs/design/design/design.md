# Design Model Design

Model validation contract: model-document-v1

## Introduction and Goals

Design owns the method for authoring coherent engineering contracts: required behavior, technical realization, boundaries, important decisions and representative acceptance intent. It also owns the living-model document convention and the method for describing relationships among models. The [System model](../system/system.md) applies that method to RigorLoop's assembled system; it does not define it again.

The direction is [Unified Design Authoring and Bounded Model Consolidation](../../proposals/2026-09-08-unified-design-authoring-and-bounded-model-consolidation.md). This package defines the replacement for the selected responsibility, not a declaration that every old document has been migrated. Its adoption boundary below governs reliance. Current activity, reviews and exact subjects are registered in the [owning change](../../changes/2026-09-08-unified-design-authoring-and-bounded-model-consolidation/change.json).

## Architecture Constraints

The Constitution retains precedence. Product direction belongs to the proposal's decision owner; Workflow owns coordination; Review and Closeout owns shared assessment and applicability policy; Test owns shared test derivation, protective-value and maintenance criteria; Record Format owns stored representation; CLI owns recording mechanics. Design supplies engineering intent and identifies its assessment basis, not approval, work allocation or execution permission.

The adopted model profile permits this combined living Design. The unified `design` skill supplies technical and behavioral authoring at coordinated adoption. This document does not activate the replacement public skill or amend governance merely by existing. It introduces no lifecycle gate, runtime record schema, model-management service, mandatory prototype, per-test ledger or target-agent correctness claim.

## Context and Scope

| Responsibility | Design owns | Separate owner or boundary |
| --- | --- | --- |
| Engineering contract | Intended outcomes, structure, invariants, shared interfaces, constraints and decisions | Proposal owns material product direction |
| Model organization | Coherent responsibility, document identity, references, supporting examples and scoped consolidation | System owns the actual system inventory and composition obligations |
| Assessment intent | Important claims, assumptions, representative conditions, observable outcomes and needed feasibility evidence | Review and Closeout governs actual assessments; specialists judge their subjects |
| Verification intent | What an implementation must demonstrate and where its violation can be observed | Test supplies adequacy criteria; Delivery allocates checks and evidence; implementation supplies fixtures/assertions |
| Authoring integration | One public authoring contract, sufficient conditional methods and exact review handoff | Workflow selects activities; installation/publication and local runtime permissions remain separate |

Input is an approved direction or an explicitly scoped authorized correction, affected model identities and relevant current contracts. Output is the smallest reconciled set of model changes, preserved decisions/references, declared consumer impacts and reviewable acceptance intent. An unmigrated source may be a scoped output under its existing document contract; changing it does not automatically migrate its responsibility.

## Solution Strategy

Replace the normal `spec` and `architecture` entrypoints with `design` in one coordinated package adoption. Do not retain redirect skills, parallel manuals or separate normal authoring decisions under those old names. Preserve architecture reasoning and behavioral precision as conditional methods within the one skill. Old documents and old released packages retain their historical meaning; withdrawing an invocation is distinct from superseding a document obligation.

One author reconciles behavior and realization iteratively. The author first selects affected responsibility owners, then makes observable behavior and constraints explicit, tests the credibility of important choices, and reconciles dependencies. A material reduction of an approved product goal returns to the direction owner with its constraint and alternatives. A local realization choice within the approved bounds belongs here. The independent reviewer assesses the resulting exact package.

## Requirements

| ID | Required behavior |
| --- | --- |
| DES-SR-01 | Normal authoring MUST expose one `design` contract covering behavioral requirements, technical realization, important decisions and acceptance intent; old `spec` and `architecture` invocations MUST NOT remain competing authoring contracts after coordinated adoption. |
| DES-SR-02 | The author MUST select the smallest justified set of coherent responsibility owners. One model has one current normative Design; a shared contract has one named owner and references from consumers. A feature, folder, class, team or size threshold alone MUST NOT define a new model. |
| DES-SR-03 | Each changed model MUST define observable required outcomes, applicable invariants, inputs/outputs, boundaries, compatibility and failure/recovery behavior with stable model-local requirement identities. Conditions under which side effects must not occur MUST be explicit where material. |
| DES-SR-04 | Behavior and technical realization MUST be reconciled. A material feasibility constraint that changes approved product direction MUST return to its decision owner with evidence and alternatives; the author MUST NOT silently weaken the approved goal or present implementation convenience as authority. |
| DES-SR-05 | A model MUST explain responsibility structure, significant dependencies, runtime or operational flows, applicable deployment/trust boundaries, quality constraints and risks to the depth needed to assess its claims. Irrelevant concerns need a bounded rationale; methods MUST NOT demand fictitious services, components or metrics. |
| DES-SR-06 | Important decisions MUST retain stable identity, context, chosen outcome, meaningful alternatives, consequences and still-applicable constraints in the owning model. Normal model work MUST NOT require an additional ADR with duplicate current authority. Historical ADR identities and judgments MUST retain their original meaning. |
| DES-SR-07 | The system-level Design MUST describe external boundaries, responsibility inventory, significant relationships, end-to-end flows and genuinely system-wide quality/failure obligations. It MUST reference component/shared-contract owners without copying their local rules or overriding governance or component authority. |
| DES-SR-08 | An interface or shared-assumption change MUST identify affected producers/consumers and required reconciliation or an evidence-backed unaffected disposition. Review scope MUST include relevant interactions and exact changed subjects; it MUST NOT require every repository model for every invocation or rely on a CLI-inferred semantic dependency graph. |
| DES-SR-09 | Important design claims MUST have an explicit assessment basis: representative walkthrough, counterexample analysis, inspection or targeted feasibility evidence proportional to the uncertainty. Material assumptions and unresolved decisions MUST remain visible. Structural validity alone MUST NOT establish credibility or approval. |
| DES-SR-10 | Design MUST identify representative conditions and observable expected outcomes for realization, including integrated outcomes that local model checks cannot establish. Scenarios MUST NOT be an exhaustive test whitelist or a basis for deleting unlisted regression protection; shared adequacy and maintenance criteria remain Test-owned. |
| DES-SR-11 | The document layout and structural mapping below MUST use the `model-document-v1` document contract, preserving the existing structural rules independently of runtime record versions. Stable requirement/decision references MUST survive revision or have explicit replacement mappings; no old review may be retargeted to revised content. |
| DES-SR-12 | Each owning model MUST index its examples with purpose, governing requirements, excerpt/complete scope and material synthetic identities or starting assumptions. Examples MUST illustrate existing obligations and satisfy the model-owned example contract below: JSON validity and available-schema conformance, before/after invariant preservation, and independent review alongside the owner with exact identities when relied upon. Examples MUST load on demand and remain distinct from normative model subjects; selectors MUST retain model/example validation pairing. |
| DES-SR-13 | Every displaced obligation and material decision in the selected migration MUST have a destination, explicit supersession or justified retention, including obligations expressed in unnumbered prose. Grouped mappings MUST expose each material obligation's disposition; section names or source-ID enumeration alone MUST NOT establish preservation. Mixed sources MUST retain identifiable unmigrated authority. No adoption or removal may rely on unresolved contradictions, anonymous follow-up or a filename-only mapping. |
| DES-SR-14 | Scoped work on an unmigrated document MUST retain its applicable contract and historical reference identities unless separately approved for migration. New features MUST update existing responsibility owners where appropriate; repository-wide conversion MUST NOT become a prerequisite for a small change. |
| DES-SR-15 | Published `design` guidance MUST work without the RigorLoop internal Design checkout or private requirement IDs. The common contract MUST be compact; specialist methods MUST load conditionally from complete packaged resources, with no full loading of both retired manuals. Missing or inconsistent required resources MUST stop dependent authoring rather than reconstruct the method. |
| DES-SR-16 | Authoring MUST hand independent Design Review the exact affected model set, relevant interactions, material decisions, evidence/assumptions and changed-subject applicability impacts. Review and Closeout remains the assessment owner. Delivery MUST receive stable requirements, representative outcomes and integrated obligations; concrete commands, milestones, proof groups and actual results remain downstream. |
| DES-SR-17 | Public invocation withdrawal MUST follow the compatibility contract below across source skills, supported adapters, invocation examples and installer boundaries. A current package or installation with retired authoring entries MUST NOT be represented as a coherent replacement. Detection MUST preserve unrelated/user-modified files and existing project state. |
| DES-SR-18 | Coherent adoption MUST reconcile governance, Workflow references, directly affected consumers, validation selection and packaged resources together. Historical records and released evidence MUST NOT be rewritten to claim approval of new subjects; publication and customer adoption remain separately authorized. |
| DES-SR-19 | Required structural checks MUST fail closed on unknown contract markers, closed values and malformed references while retaining semantic review ownership. This change MUST preserve required negative/regression protection and existing Test criteria when relocating or retiring checks. No test-count, document-count or token-saving target substitutes for evidence. |
| DES-SR-20 | The first slice MUST deliver the selected Design/System responsibilities and their shared relationship, dispose their superseded current sources as mapped, and assign remaining consolidation to named later work. Completion MUST NOT claim whole-repository consolidation. |
| DES-SR-21 | For an explicitly approved necessary-design consolidation, surviving requirements, applicability, constraints, technical realization, material decisions and failure knowledge MUST have usable current owners before source removal. Retain an original only for a named remaining need and owner; no automatic archive, redirect, index or duplicate is required. Historical judgments and records MUST retain their original subjects and meaning; current reliance MUST not require reconstruction from version history. This policy applies only to the selected sources and does not cancel a different initiative's retention commitment. |

## Building Block View

Design is a method responsibility, not a new service. Its public implementation is one authored skill with a small common procedure and conditionally loaded methods. The same model requirements govern repository use and portable installed guidance; repository-specific mappings below remain contributor content.

| Public resource | Trigger and responsibility | What stays out |
| --- | --- | --- |
| `skills/design/SKILL.md` | Always: scope/authority, owner selection, reconciliation loop, stable references, boundary scan, assessment/verification distinction and handoff | Detailed migration inventory, repository paths for maintainers, exhaustive method manuals |
| `references/model-authoring.md` | Creating/revising a living model: requirements, decisions, model layout and the complete DES-SR-12 example contract, including parent indexing, validity, invariant preservation and review handoff | Lifecycle mutation and approval |
| `references/technical-design.md` | Significant structure, interfaces, runtime, deployment, trust or quality choices | A mandatory second architecture file or ADR |
| `references/system-composition.md` | Multiple affected owners, shared contract or system-wide claim | Whole-repository loading or inferred ownership by folder |
| `references/legacy-source-reconciliation.md` | Scoped unmigrated-source work: select the project authority, retain its format/IDs, classify the amendment and load the applicable feature or legacy technical procedure below; invocation coexistence or explicit authority migration | Automatic conversion, blanket deletion or historical approval rewriting |
| `references/boundary-first-method-v1.md` | Interpret or author a retained feature-format boundary record: complete compact vocabulary, IDs, examples and interaction rules | A second policy owner or mandatory feature records for living models |
| `references/boundary-first-feature-authoring-v1.md` | Substantive amendment remaining under the retained feature format: complete four-section procedure, tables and semantic checks; loads the compact method above | The retired spec manual or automatic migration |
| `references/legacy-technical-authoring.md` | Scoped unmigrated architecture/ADR amendment: retain applicable concerns, decision history, source ownership and project-prescribed packaging; load the applicable scaffold below when creating or rebuilding such an artifact | A competing normal authoring skill or mandatory ADR for model work |
| `assets/legacy-architecture-skeleton.md`, `assets/legacy-adr-skeleton.md`, `assets/diagram-styles.mmd` | Conditional installed aids for a retained architecture/ADR contract or a diagram needing the shared styles; use only the matching aid | Internal checkout dependencies or mandatory scaffolds for simple amendments |
| `references/governed-design-authoring.md` | Explicitly selected governed change: v2 context, subject inspection and targeted author-owned recording | Portable lifecycle creation, semantic readiness engines or retired recording fallback |
| `references/test-quality.md` | Authoring or assessing verification intent under adopted Test policy | A new definition of test adequacy or a per-test ledger |
| `assets/design-skeleton.md` | Creating a model: stable engineering sections and existing required tables | Mutable status, prescribed tests/commands, second spec/architecture scaffold |

The resource names are the selected package decomposition. Delivery may divide implementation work but may not silently replace the loading responsibilities with eager concatenation. Existing portable boundary vocabulary supports the common compact scan. The named feature-format resource and its compact-method dependency are packaged together and loaded only when that retained format is triggered; neither retired authoring manual is shipped in full. The legacy reconciliation resource owns selection and the named specialist resources supply the complete procedure. Any transitive required method or scaffold must be contained in the installed package and covered by the same trigger/integrity checks. The current published resource-integrity owner retains contained-path, projection and parity mechanics.

The customer project supplies its authoritative legacy requirements, approved decisions, local format/version and any mandatory project-specific template or schema. Packaged methods explain how to amend that source; they cannot invent its authority. A missing packaged method is a distribution defect that stops the dependent invocation. Missing or contradictory project authority instead requires the project owner to resolve that bounded gap; installing more generic guidance or migrating the document does not settle it. The author may proceed with independently authorized unaffected work. A project-specific required scaffold must come from that project; the bundled generic aid is used only when its declared contract permits it.

## Runtime View

1. Read the approved direction or authorized correction and select exact affected owners. For governed work, inspect current model references and applicable assessments through existing primary CLI reads. For portable work, resolve an explicit target or the model layout below; do not infer governance adoption.
2. Explain observable outcomes and constraints, then reconcile technical choices and dependencies. Escalate a material product-direction conflict; retain unaffected independent work.
3. Identify important claims and uncertainty. Use a scenario walkthrough or counterexample for ordinary claims and targeted feasibility evidence for a material uncertain claim. Record assumptions and any owned unresolved question.
4. Update model-local requirements, realization, decision rationale and representative outcomes together. Include affected shared-contract consumers, missing reconciliation and justified unaffected paths.
5. Preserve references and current ownership. For a selected migration, use the exact displacement map; for an unmigrated amendment, preserve its declared contract and boundary format.
6. Inspect completed subject identities and record only author-owned references, decisions and impact restrictions. Independent Design Review evaluates that package. A successful write does not approve it; a missing resource or uncertain authority remains a scoped stop.

## Deployment View

### Public invocation compatibility

The first adopting package supplies `design` for Codex, Claude Code and OpenCode and removes the authored `skills/spec/` and `skills/architecture/` packages after their material content is reconciled. Generated packages omit both old skill directories and old command aliases. OpenCode replaces its two authoring aliases with one `design` alias. No redirect wrapper is shipped: it would either duplicate the contract or require a cross-skill dependency outside the established resource boundary.

Previously released archives and historical install examples remain byte-preserved release evidence, not proof of the current skill inventory. Current install guidance identifies the withdrawal and the replacement invocation. A user of an older release can retain that older coherent release under its own contract, but cannot claim it supplies this capability.

The verified candidate archive must contain `design` and omit both retired authoring entries and their target command aliases. A candidate violating that inventory is rejected before target/state writes. Ordinary init also rejects an installed old or mixed inventory with a diagnostic identifying the target, offending paths and the appropriate managed or unmanaged transition. Detection itself grants no removal authority.

The prior installation profile defined its executable transition in the [preserved Target-native init amendment](../distribution/distribution.md#source-displacement-and-preservation), TNI-DES-01–06. For a managed target, retain the complete old tree, inspect the exact selected roots and recorded hashes, and back up those roots and both state files outside the installation. After explicit operator authorization, `init TARGET --write-state` narrowly replaces an eligible, unchanged lockfile-managed old installation with the verified candidate. It checks the original hash before removal and writes the new basis only after verification. Manual pre-deletion is not this managed procedure, and `--write-state` does not override drift. The amendment extends the existing workflow-to-route replacement pattern; the implementation must preserve that same original-basis authority for the authoring transition.

Modified old entries, unrecorded additions, missing roots, unsafe symlinks, mixed ownership or ambiguous state block before mutation. Operators preserve local changes and restore the original recorded basis under the installation owner's recovery procedure before retry. A caught failure restores prior target/state bytes or reports incomplete recovery; process interruption requires inspection and restoration from the retained backup when the pair is partial. Neither retry nor recovery may silently reset hashes, delete lock state or overwrite intervening unrelated changes. Other targets and unrelated valid state/content remain protected. Candidate checks, dry-run and ordinary init do not remove old files.

For genuinely unmanaged targets, diagnostics direct explicit operator inspection, backup and removal of only the obsolete entries/aliases, followed by normal conflict-checked installation. A state-implicated target cannot use that path to escape drift protection. No automatic cleanup on detection, broad force operation or document migration is introduced. Existing workflow-to-route behavior retains its separate scope. Manual archive installation documents the same inventory condition, and managed targets use the managed procedure rather than manual overlay; the CLI cannot police direct invocation of manually retained skills.

This is a bounded consumer of Design's invocation policy. [Target-native init](../distribution/distribution.md#source-displacement-and-preservation), [multi-adapter installation](../distribution/distribution.md#source-displacement-and-preservation) and the [lockfile contract](../distribution/distribution.md#source-displacement-and-preservation) retain installation, trust, filesystem, hash and state ownership. TNI-DES-01–06 supplies the smallest selected installer amendment; lockfile R46–R51 and hashing semantics remain unchanged. Package validity ends at observable source/archive/install boundaries; model behavior in a target agent is not a deterministic acceptance claim.

### Coordinated adoption boundary

The exact reviewed Design package consists of Design and System, the scoped Workflow convention amendment and the TNI-DES-01–06 installation-owner amendment in Target-native init. The installer remains an unmigrated source; inclusion in this package does not consolidate its other responsibilities. Approval permits authorized Delivery planning, not immediate replacement of current authorities. Until coordinated implementation and its required reviews/Verify, the pre-adoption governing text and entrypoints remain effective. Draft ownership destinations below are not a second active contract.

At adoption, current navigation and instructions resolve the mapped responsibilities to these owners. The old architecture-method spec remains at its stable path with an explicit historical-contract notice and replacement links; its existing text and IDs remain historical evidence below that notice. The two selected method ADRs remain byte-identical, including their historical status; current ADR navigation labels their relevant decisions as superseded by the mappings below. Mixed system architecture retains unmigrated sections and gains a bounded authority notice and links at displaced sections. No historical `docs/changes/` record, review identity, release archive or grandfathering snapshot is rewritten.

Rollback before adoption discards the unadopted candidate under normal source control authority. After adoption, rollback requires an explicitly authorized coherent package/governance reversal or forward correction, with reassessment of affected subjects; it never reassigns old approvals or converts project records. Restoring one old skill directory beside `design` is not a valid rollback.

## Crosscutting Concepts

### Model document and structural contract

The convention transferred from Workflow WF-SR-07/08/09 uses one `docs/design/M/M.md` per coherent responsibility, where `M` is the matching stable directory/filename model ID. Model-owned examples live under that directory's `examples/`. Examples may be Markdown, JSON, Mermaid or a suitable format; no shared cross-model example root or mandatory wrapper is introduced. A shared example has one owner and is referenced by its consumers. Cross-model contract references use the owner's path and stable requirement/decision identity.

Each model declares exactly once `Model validation contract: model-document-v1`. Its level-two `Requirements` heading introduces a table with exactly `ID` and `Required behavior` columns, unique nonempty IDs beginning with a letter and containing only letters, digits and hyphens, and nonempty normative text. Its level-three `Boundary scan and acceptance scenarios` heading introduces a table with exactly `Dimension`, `Requirement basis` and `Distinct outcome to demonstrate` columns. Each of the eight dimensions in this document's scenario table occurs exactly once. Applicable rows cite unique IDs from that model separated by comma and one space and give a nonempty outcome; non-applicable rows use `-` and an outcome starting `Not applicable:` with a reason. Required headings/tables occur once. Unknown markers/dimensions, duplicates, undeclared IDs, malformed tables and missing required cells reject.

The marker replaces the ambiguous document identifier `explicit-recording-v1`; it does not version or convert stored workflow records. Current model validation accepts exactly `model-document-v1` and rejects the retired document marker, unknown values, missing declarations and duplicates before table checks. Adopt the rename together across current living models, the validator, authoring guidance, skeleton and generated candidate metadata. Existing customer models require an explicit project-owner-authorized marker edit; installation does not rewrite their documents. Historical record bytes and original review identities remain unchanged. A rollback restores the matching document/validator/guidance set together, without changing the v2-only runtime contract.

#### Example: a small model document

| Example | Purpose and governing requirements | Scope and assumptions |
| --- | --- | --- |
| The fenced label-normalization model below | Illustrates DES-SR-09/11/12: the marker, model-owned requirements, all eight scenario dimensions and observable outcomes | Complete illustrative structural record for hypothetical `docs/design/label-normalization/label-normalization.md`; not an adopted RigorLoop component or a stored workflow record. Synthetic LAB-SR identifiers belong only to this example. |

The function accepts a label and returns a normalized value. For example, `"  green  room  "` becomes `"green  room"`; an all-space string becomes `""`; a non-string input produces an error and no normalized value. The scenarios describe intended observations, not an exhaustive test list or evidence that an implementation passed.

```markdown
# Label Normalization Design

Model validation contract: model-document-v1

## Responsibility

Normalize labels with a pure function. The caller owns storage, authorization and presentation; this model owns only the input-to-output transformation.

## Requirements

| ID | Required behavior |
| --- | --- |
| LAB-SR-01 | For a string input, return it with leading and trailing ASCII spaces removed; preserve every interior character and return an empty string for an all-space input. |
| LAB-SR-02 | Reject a non-string input with an input error and no normalized value. |
| LAB-SR-03 | Do not read or write external state; repeated normalization of an already normalized string returns the same value. |

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | LAB-SR-01, LAB-SR-02 | Leading/trailing spaces disappear, interior spaces remain, empty/all-space inputs return an empty string, and non-string inputs reject. |
| State/lifecycle | LAB-SR-03 | Calls leave external state unchanged; earlier calls cannot affect a later result. |
| Identity/authority | - | Not applicable: this pure transformation has no principals or permission decisions; callers own access control. |
| Composition/path | LAB-SR-01, LAB-SR-03 | Passing the result through normalization again preserves the result. |
| Temporal/retry | LAB-SR-03 | Repeating the same call yields the same result without accumulated side effects. |
| Failure/recovery | LAB-SR-02, LAB-SR-03 | Invalid input produces no normalized value or state changes; a following valid call succeeds normally. |
| Compatibility/migration | - | Not applicable: this example owns no persisted records, versions or migration. |
| External/environment | LAB-SR-01, LAB-SR-03 | The ASCII-space rule produces the same result regardless of locale and without filesystem or network access. |
```

Extract the fenced content to the hypothetical model path to check its structure. The fence is illustrative content, so its declaration and tables must not count as additional live declarations in this owning Design. Structural validation checks shape and references; independent assessment judges the requirements and scenarios, and implementation tests establish actual behavior. Changing this relied-on example requires reassessment with its owning Design and exact subject under DES-SR-12/16.

Path selection continues to accept explicitly supplied historical flat `docs/design/M.md` regular files when present, without maintaining flat copies, relocating subjects or retargeting approvals. Mismatched IDs, model paths pointing into examples, extra normative nesting and symlink paths reject. A known historical flat deletion maps to its current model for validation selection only. Model/example selection preserves the owning-model check. Existing historical `specs/` formats and adoption rules remain valid for their own responsibilities; the document marker is independent of runtime record formats.

References to scenario rows use the model path and exact dimension label; material combined hazards are concise requirement-linked prose alongside them. No additional boundary/proof ID series is required for model documents. Every affected requirement, scenario row and material integrated hazard is allocated to concrete proof by Delivery. Actual observations stay in existing evidence records. Design and Delivery reviewers assess semantic adequacy under Review and Closeout and Test, not document syntax.

The existing grandfathered-spec handoff is retained: changed unmarked grandfathered specs receive a separate `review_required` observation. Structural success reports `review-required` with exit zero; structural errors still fail. Missing/unknown markers on non-grandfathered specs and malformed existing boundary content cannot become review observations. Independent Design Review records whether an exact amendment is non-substantive historical, substantive historical requiring existing feature-format adoption, or new-profile-only preserving the historical remainder. Unknown or stale classification prevents reliance. No new classification artifact, schema or CLI state is introduced.

### Model-owned example contract

DES-SR-12 retains the example obligations transferred from Workflow's Model-centered layout and examples section. The owning model MUST index each example with its purpose, governing requirement references, complete-artifact or excerpt scope, and any material synthetic identities or starting assumptions. An example illustrates its cited contract; it MUST NOT introduce a new normative rule or leave its owner implicit.

JSON examples MUST parse without explanatory extra keys. A complete record example MUST conform to its selected schema when that schema is available. Explanations belong in the model's index or accompanying prose rather than invented record fields; declaring an example complete is not evidence of schema conformance. If the schema is unavailable, that limit must be visible and no schema-conformance result may be claimed.

Before/after example pairs MUST preserve the invariants they demonstrate. Syntactic validity alone does not establish that an illustrated transition retains its required state, authority or identity constraints. Independent review MUST cover affected examples alongside their owning model and include the exact example identities when relying on them, under Review and Closeout's assessment/applicability policy. The author supplies those subjects in the DES-SR-16 handoff; the reviewer retains judgment ownership. On-demand loading does not excuse omitting an affected or relied-on example from the assessment.

These are retained content and assessment obligations, not a new schema, automatic semantic validator or requirement to implement every representative test during Design. Delivery allocates suitable concrete checks and evidence; specialists assess whether the example actually demonstrates its claim.

### Technical reasoning and decisions

The arc42 concern set remains a useful completeness guide: goals, constraints, external context, strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality, risks and glossary. New model documents need not repeat twelve headings when the same concerns are clearly covered in a smaller structure; retaining a heading is not evidence that its concern was assessed. This first package keeps familiar headings to ease comparison without making them a universal schema.

C4-style context and structural views are conditional on explanatory value. A system context shows the whole system and its external actors; a container view shows actual execution/storage or distribution boundaries, not every policy model as a fake deployed container. Component/deployment detail is added when a coarser view cannot explain a material relationship. Text-source diagrams have one authored source and intent-labeled relationships. Inline Mermaid is permitted for a small model-local view; reused/larger views use one model-owned source file and relative links. Binary exports and external diagrams are never the sole authority. C4 flowcharts retain distinguishable roles and relevant technology labels; color is not the only distinction.

Model decisions replace mandatory new standalone ADRs for adopted responsibilities. A historical decision may remain applicable, be narrowed or be superseded; its old judgment never applies to a changed model automatically. Repository-level `templates/architecture.md`, `templates/adr.md` and `templates/diagram-styles.mmd` remain contributor source aids. Installed invocations use the named skill-local legacy assets and `legacy-technical-authoring.md`, never repository paths. Delivery reconciles their content and validates packaged completeness under existing asset/source governance. These conditional legacy assets do not establish a second normal authoring contract or require standalone ADRs for living models.

### Necessary-design retention

The [necessary-design consolidation direction](../../proposals/2026-09-09-consolidate-necessary-design-and-retire-superseded-sources.md) selects the validation-related source boundary in System's necessary-design consolidation map. DES-SR-21 applies at that package's coordinated adoption; approval of this draft alone does not remove a source. Existing owners are sufficient: Design owns preservation and source disposition, Test owns protective-value criteria, and System owns their composition. No Validation model is selected.

The separately approved [Release consolidation](../../proposals/2026-09-09-release-model-source-consolidation.md) also selects DES-SR-21 for the six specification/test-specification/ADR sources and exact architecture paragraphs in [Release's displacement map](../release/release.md#source-displacement-and-retirement). This applicability extension takes effect at that package's reviewed coherent implementation and successful Verify. Necessary representation rules and proof intent move to Release; historical release evidence, transaction profiles, schemas, templates, fixtures and the literal-audit baseline remain operational/evidentiary inputs. No other archive commitment or Release-adjacent source is waived by this extension.

The [Distribution direction](../../proposals/2026-09-10-distribution-model-and-opencode-retirement.md) selects DES-SR-21 for the ten spec/test-spec files, five ADRs and exact mixed-architecture sections in [Distribution's map](../distribution/distribution.md#source-displacement-and-preservation), under its [owning change](../../changes/2026-09-10-distribution-model-and-opencode-retirement/change.json). The transfer takes effect only at reviewed implementation and successful Verify. After adoption, Distribution's DIST-SR-10–15 explicitly supersede the managed replacement and state-write requirements referenced here in TNI-DES-02–05, DES-SR-15/17's realization and scenarios, the consumer map and DES-DEC-04. Candidate/installed inventory guards in supported projects, no-overwrite conflicts, preservation and unmanaged inspection/backup remain; automatic authoring and workflow-to-route upgrades do not. The installation compatibility section above and related upgrade examples describe the prior adopted profile only. Current init rejects `--write-state`, ignores project state and preflights actual candidate destination units after archive verification. Existing units conflict even when identical; explicit `--force` permits complete replacement only within candidate units, preserving unrelated skills and shared parents. Archive, containment, symlink and concurrent-change safeguards remain mandatory. The earlier no-force, identical-no-op and state-marker rejection choices are superseded; force does not remove noncandidate retired entries or restore managed-basis interpretation and state updates. The original decisions and review identities remain historical evidence, not requirements to preserve withdrawn replacement transactions. Installation is part of Distribution, not an additional model. Unselected retention commitments and historical subjects stay unchanged.

Preserve an actionable rule, its applicable population and approved exceptions, rather than a generic promise to preserve behavior. Preserve enough decision context, alternatives, consequences, implementation relationships and failure knowledge for future changes. Completed rollout instructions and redundant descriptions need an explicit disposition, not a new normative home. Use the existing displacement tables; no parallel migration catalogue is introduced.

| Remaining use | Required treatment |
| --- | --- |
| Current obligation or operational reader | Transfer completely with its consumers, or retain the exact remainder and its owner. A resource manifest, schema, fixture or recovery input is not archival prose. |
| Material rationale or regression knowledge | Preserve the necessary explanation at its owner; retain the original only if that explanation cannot supply the needed basis. |
| Exact original still needed for current assessment reliance | Retain the needed original, or explicitly stop relying on that assessment for the new claim. Never relabel the original judgment as an assessment of replacement text. |
| Incidental historical citation, completed procedure or duplicate with no remaining use | Remove the selected source after reviewed disposition; version history may preserve it, but current rules remain available in the checkout. Do not rewrite historical citations merely to point old judgments at new content. |

Existing byte-preservation decisions for the earlier architecture-method and Skill pilot remain scoped to their own selected files; this initiative does not purge those archives. Constitution's record/release preservation requirements remain unchanged because no historical record or release artifact is selected for deletion. Its requirement to identify a superseded artifact's replacement is satisfied by the explicit source-qualified displacement map and current change evidence, not by a compulsory file at the old path.

For this consolidation, observe three distinct outcomes under DES-SR-13/18/21: a removed duplicate has a complete accessible owner; a mixed source retains a precise current remainder; a historical citation does not become current approval of replacement content. If a supposed prose source has an operational reader or an unresolved finding, stop that removal and reconcile the need. Recovery restores only the affected source/consumer slice with current review applicability; it does not restore old approval for new bytes. These outcomes supplement the Compatibility/migration and Identity/authority scenarios and require semantic review plus focused reference/reader checks, not an automatic runtime benchmark.

### Selected replacement map

The following rows select all R1–R124 of [Architecture Package Method](../../../specs/architecture-package-method.md) for method-authority reconciliation. Ranges are inclusive and each R appears once. Original IDs are source-qualified historical references, never renamed Design IDs. Acceptance criteria AC1–AC22 remain historical acceptance of the old method; their ongoing protective obligations resolve through the corresponding R rows, rather than becoming an independent second current contract. Examples E1–E10 retain historical illustration meaning; the corresponding current outcomes are owned by DES-SR-02/04/05/06/11/13/14/19 and the scenarios below. Completed rollout requirements are explicitly retired as completed historical requirements, not reapplied to this initiative.

| Displaced source IDs | Selected disposition and destination | Retained meaning or deliberate replacement |
| --- | --- | --- |
| R1–R6 | Replace with DES-SR-01/02/07/11 | One owning Design and System composition view replace a separate canonical architecture-method/spec authority and fixed package paths. |
| R7–R13 | Replace with DES-SR-05/11 and technical reasoning above | Preserve concern coverage and non-applicability rationale; retire mandatory twelve-heading serialization and old mutable-state representation. |
| R14–R16 | Retain substance in DES-SR-03/05/08 | Runtime, deployment and cross-cutting impacts remain material authoring concerns. |
| R17 | Replace with DES-SR-06 | Embedded stable decisions replace a mandatory ADR-link section. |
| R18–R20 | Retain substance in DES-SR-05/09 | Quality, risks and necessary terminology remain assessable; no empty-heading ritual. |
| R21–R25 | Replace with DES-SR-05/07 | Context/container/component/deployment views follow explanatory need; code-level diagrams remain optional. |
| R26–R29 | Retain source/authority protection in DES-SR-05/12 | Reviewable text remains primary; initial Mermaid rollout requirement is historical. |
| R30–R39 | Replace with DES-SR-02/04/06/08/13/14 | Small direct owner updates and no competing temporary truth survive; normal output is a living Design, scoped legacy amendment or justified no-change result. |
| R40–R43 | Retain scoped coherence in DES-SR-05/16/18 | Required design reconciles with delivered behavior before reliance; no-impact changes need no invented architecture. Approved Design/Delivery and current review policy govern sequencing, not historical post-code exceptions. |
| R44–R48 | Replace with DES-SR-06/11/13 | Preserve decision context, alternatives and old judgments; retire mandatory new ADR and retired writable lifecycle rules. |
| R49–R54 | Split: DES-SR-15/18; retain templates source governance | New normal scaffold is design-owned; legacy architecture/ADR templates remain conditional. Completed introduction of templates is historical. |
| R55–R58 | Replace with DES-SR-01/15/16/18 | Current route/review/adapter consumers replace retired workflow and review entrypoints; generation remains source-derived. |
| R59–R66 | Replace with DES-SR-13/20 | This actual method/System slice demonstrates consolidation; no full legacy conversion claim. Earlier first example and normalization rollout remain historical. |
| R67–R72 | Retain non-semantic validation boundary in DES-SR-09/11/19 | Existing model structural validation is retained; earlier ban on first-rollout architecture enforcement is historical, not a ban on these already adopted checks. No new architecture-sufficiency validator. |
| R73–R75 | Retain in DES-SR-05/12/15 and security/usability below | Preserve confidentiality, relevant trust reasoning and navigable text. |
| R76–R86 | Replace with DES-SR-05/11/12 | One text-source diagram and parent-model identity remain; fixed package directory and universal inline prohibition retire. Historical diagrams stay historical. |
| R87–R97 | Retain semantic substance in DES-SR-05/07 | C4 roles, intent and hierarchy remain useful; a sentence-count trigger and obligatory styling file are replaced by explanatory sufficiency. |
| R98–R99 | Replace with DES-SR-06 | Decision rationale lives once in the model; historical ADR links retain context without competing current authority. |
| R100–R104 | Retain in DES-SR-05/09/10 | Quality conditions and observable outcomes, relevant deployment boundaries and concise non-duplication remain. |
| R105–R107 | Split: DES-SR-05/15; conditional legacy templates | Shared style/old scaffolds remain reusable; new scaffold follows the model contract and embedded decisions. |
| R108–R111 | Replace with DES-SR-01/15 | Compact common method, conditional examples and smallest justified output survive; mandatory inline C4 snippets/old surface selector retire. |
| R112–R118 | Reference DES-SR-16/19 and Review and Closeout | Material finding protection survives through the current reviewer contract; no revival of architecture-review, new finding category or C4 classification. |
| R119–R124 | Replace with DES-SR-08/14/16 | Review selects exact changed owners, legacy amendments and interactions; proposal gaps remain with the direction owner. |

| Selected Workflow source | Destination | Workflow remainder |
| --- | --- | --- |
| WF-SR-07; Model documentation and traceability; Model-centered layout and examples | DES-SR-02/06/08/11/12; document contract and explicit example-obligation mapping below | Coordinate the required owning-model updates; preserve WF-SR-07 as a reference to Design. |
| WF-SR-08; WF-DEC-02 | DES-SR-06/11/13 and DES-DEC-01 | Stable old IDs remain; applicability/independence still resolve to Review and Closeout. |
| WF-SR-09's document/proof-mapping clause; Model validation and proof mapping | DES-SR-10/11/16/19 | Workflow coordinates Delivery allocation and closeout under Review and Closeout; Test owns adequacy. |
| Responsibility-specific updates opening paragraph; Building Block View model-truth row | DES-SR-01/02/16 | Workflow owns author/reviewer/route activity boundaries and stored work coordination. |
| WF-MAP-01/07/08 and retirement-only statements excluding a skill refactor | DES-SR-13/18/20 for this later selected initiative only | Preserve prior retirement initiative scope/history; its exclusion does not exclude this separately approved direction. |

The unnumbered example obligations in Workflow's pre-transfer Model-centered layout and examples section have the following individual destinations. Every row is retained; none is superseded or deferred. These rows supplement the section-level map and preserve source meaning without creating another normative owner.

| Displaced Workflow obligation | Exact Design destination | Preserved assessment consequence |
| --- | --- | --- |
| Owning document indexes each example's purpose, governing requirements, complete/excerpt scope, synthetic identities and starting assumptions | DES-SR-12; Model-owned example contract, first paragraph | A standalone example with no parent-model index does not satisfy the authoring contract. |
| JSON examples parse without explanatory extra keys | DES-SR-12; Model-owned example contract, second paragraph | A malformed JSON example or explanation encoded as an invented record field cannot be accepted as a valid example. |
| Complete records conform to their selected schema when available | DES-SR-12; Model-owned example contract, second paragraph | Parse success does not excuse a complete record's schema violation; unavailable-schema limits remain explicit. |
| Before/after pairs preserve the invariants they demonstrate | DES-SR-12; Model-owned example contract, third paragraph | Two individually valid artifacts do not establish a valid illustrated transition if its claimed invariant is violated. |
| Independent review covers affected examples with their owner and exact identities when relied upon | DES-SR-12/16; Model-owned example contract, third paragraph | A model-only reviewed identity cannot establish review of a changed, relied-on example; on-demand loading does not waive the required subject. |

### Material decision preservation

| Source decision | Treatment | Preserved rationale and changed consequence |
| --- | --- | --- |
| ADR-20260428-architecture-package-method: C4/arc42/ADR choice and fixed canonical package | Superseded for selected model-authoring responsibility by DES-DEC-01/02/03 | Ad hoc prose loses consistency; C4 alone loses runtime/rationale; arc42 alone lacks relationships; ADR alone lacks system structure. Preserve all these concern categories. Replace fixed separate packaging with model ownership. |
| Same ADR: normal temporary architecture deltas | Historical narrowing retained by DES-DEC-01/04 | Temporary truth attracts unresolved direction and duplicate authority; use direct owner updates and return material direction gaps. |
| Same ADR: templates source boundary, review-based first rollout, deferred normalization | Retain source governance and historical rollout meaning through DES-SR-18/19/20 | No source-boundary change or retrospective rollout claim; existing model checks remain structural. |
| ADR-20260509-architecture-skill-surface-simplification: no normal deltas, four normal surfaces and reviewer surface selector | Split: preserve no-delta principle; replace output/review selector by DES-DEC-01/04 and DES-SR-16 | The old decision deliberately left C4/arc42/ADR packaging intact. This later approved direction changes that packaging explicitly, while preserving alternatives/consequences and historical evidence. |

### Required consumer reconciliation

This is the exact source-family boundary for Delivery expansion, not a claim of completed edits. Every directly affected file requires a concrete allocated edit or an evidence-backed unaffected disposition; an otherwise deferred subsystem cannot retain a broken required caller. Skill resources are selected transitively from the actual mapped references. Historical records and release archives are excluded from bulk substitution.

| Surface | Selected change or retained owner |
| --- | --- |
| `CONSTITUTION.md`, `AGENTS.md` | At adoption amend separate authorship/fixed package rules and source-of-truth/required-reading guidance for selected model responsibilities; retain governance precedence, independent review, stage authority and external permissions. |
| `docs/design/workflow/workflow.md` | Reference Design for the mapped convention; retain coordination and old stable IDs. Its prior retirement drafting evidence is historical basis, not the current work state. |
| `docs/architecture/system/architecture.md` and two method ADR navigation entries | Apply System's exact mixed-document map; retain unrelated source authority and historical decisions. |
| `specs/architecture-package-method.md` and `.test.md` | Add bounded historical/replacement notices; preserve old IDs and historical acceptance text. Retain or replace protective checks by obligation; do not run retired gate/record procedures. |
| `specs/skill-contract.md`, `specs/rigorloop-workflow.md`, `specs/skill-invocation-commands-for-adapters.md` | Amend current selected-profile authoring name, model/review subject and handoff references. Preserve unrelated normalized structure, historical clause IDs and separate proof owners. |
| `skills/spec/**`, `skills/architecture/**` | Reconcile material methods into the selected `skills/design/` resources, then remove old canonical packages. Do not delete a method solely because its old filename is retired. |
| `skills/design-review/**` | Assess exact affected models, scoped legacy members, important decisions and interactions; replace fixed tuple and correction routing. Keep independent recording and actual assessment duties. |
| `skills/proposal/**`, `skills/proposal-review/**`, `skills/route/**`, `skills/plan/**`, `skills/delivery-review/**`, `skills/implement/**`, `skills/code-review/**`, `skills/verify/**` | Reconcile normal authoring names, requirement-to-realization references and model/review/verification handoff. Preserve all distinct stage boundaries, isolation, correction and final review requirements. |
| `skills/bugfix/**`, `skills/ci-maintenance/**`, `skills/explore/**`, `skills/research/**`, `skills/learn/**`, `skills/project-map/**`, `skills/constitution/**`, `skills/vision/**`, `skills/pr/**` | Update current normal author/correction references where present; preserve scope-specific methods, advisory behavior and external boundaries. A mention of a historical spec is not automatically an obsolete invocation. |
| `templates/architecture.md`, `templates/adr.md`, `templates/diagram-styles.mmd` | Retain contributor aids; reconcile the named conditional installed legacy assets and technical procedure without a public dependency on these repository paths. New normal model scaffold is `skills/design/assets/design-skeleton.md`. |
| `scripts/skill_validation.py`, `scripts/validate-skills.py`, `scripts/test-skill-validator.py`, current resource projection owners | Replace old normal-skill inventories and mapped-resource expectations; retain unknown-value rejection, claim boundaries and normalized skill quality. Internal mappings never become public skill instructions. |
| `scripts/boundary_first_validation.py`, `scripts/boundary_first_reference.py`, `scripts/validation_selection.py` and their existing entrypoints/tests | Preserve the model marker/tables and model/example pairing; revise authoring consumers and source-owner references. No semantic dependency/readiness engine or historical format rewrite. |
| `scripts/build-adapters.py`, `scripts/adapter_distribution.py`, `scripts/validate-adapters.py`, `scripts/adapter_templates/*`, `dist/adapters/manifest.yaml`, `dist/adapters/README.md` | Generate the coherent new inventory/aliases and verify source/archive/install parity using existing mechanisms. Do not hand-edit generated bodies or fabricate release metadata. |
| `packages/rigorloop/dist/bin/rigorloop.js`, existing init tests, `specs/target-native-init.md`, `specs/multi-adapter-init-and-proxy-aware-download.md` | Implement the candidate/installed guards and TNI-DES-01–06 authorized managed replacement/recovery; retain installer/lockfile ownership, hashing, drift protection and unrelated content. No broad force, automatic cleanup on detection or new schema. |
| `packages/rigorloop/dist/lib/workflow-context.js` and its current contract/configuration consumers | Inspect existing `model` references through primary context for exact governed subjects. Existing spec/architecture/ADR location keys remain legacy artifact-placement metadata, not independent public actor instructions; current guidance routes their authoring to design. No new discovery kind/API is required. |
| `README.md` outside generated vision front-matter, `docs/project-map.md`, `docs/follow-ups.md`, current contributor/install indexes | Update current navigation, the bounded system view and durable follow-up ownership. Do not rewrite vision or unrelated follow-ups, historical plans, approvals or releases. |

### Security, observability and usability

Requirements, rationale and evidence references must not expose secrets, credentials or machine-local debug data. Trust/permission and data-exposure boundaries are described when affected, with local runtime and human authority unchanged. Prose, tables and text diagrams support ordinary repository navigation without color-only semantics. Observations identify actual claims, assumptions, owners and replacement references; no new telemetry or metrics service is needed. No quantitative token/runtime target is selected.

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | DES-SR-02, DES-SR-03, DES-SR-11, DES-SR-12, DES-SR-14, DES-SR-19 | A new model, scoped existing model and unmigrated-spec amendment resolve different valid targets. Unknown marker, malformed requirement reference or unresolved owner rejects; an unmarked historical amendment gets its retained semantic classification rather than silent model conversion. An unindexed example, malformed JSON, explanatory extra record keys or a complete record violating an available schema cannot satisfy the example contract. |
| State/lifecycle | DES-SR-04, DES-SR-13, DES-SR-16, DES-SR-18 | A saved draft or approved proposal does not activate the new skill or replacement authority. An unresolved direction conflict returns to its owner without presenting the weakened behavior as approved. |
| Identity/authority | DES-SR-06, DES-SR-08, DES-SR-11, DES-SR-12, DES-SR-16, DES-SR-21 | A decision/requirement move preserves its replacement reference, while the review remains attached to its original subject. The author cannot self-approve or change another actor's judgment. An affected example is assessed with its owning model and its exact identity is included when relied upon; an unchanged parent identity does not make an edited example's old assessment current. |
| Composition/path | DES-SR-07, DES-SR-08, DES-SR-10, DES-SR-15, DES-SR-16 | A shared-authoring-contract change reaches routing, Design Review and planning consumers with one owner and consistent integrated outcome. A locally coherent model whose consumer expects the old contract remains unreconciled. |
| Temporal/retry | DES-SR-08, DES-SR-11, DES-SR-13, DES-SR-16 | Concurrent edits to a shared model require current subject inspection and impact/reassessment under Review and Closeout; a failed recording retry cannot replay a stale approval or overwrite a neighbor. |
| Failure/recovery | DES-SR-04, DES-SR-09, DES-SR-15, DES-SR-17, DES-SR-18 | Missing required packaged guidance stops dependent authoring. A failed guard leaves files/state unchanged; an authorized managed replacement follows TNI-DES-05 rollback/interruption recovery, never an automatic document conversion or lockfile reset. |
| Compatibility/migration | DES-SR-01, DES-SR-06, DES-SR-13, DES-SR-14, DES-SR-17, DES-SR-20, DES-SR-21 | New packages supply design alone; old/mixed selected-target entrypoints produce a safe actionable rejection of ordinary init, with the eligible managed replacement path defined by TNI-DES-01–06. A small unmigrated-source amendment preserves its owner/format, while selected migrated clauses have exactly one replacement and old approvals remain unchanged. |
| External/environment | DES-SR-05, DES-SR-12, DES-SR-15, DES-SR-17 | A clean installed package contains every triggered method without the internal repository checkout, including substantive unmigrated feature-format authoring, its compact dependency and applicable legacy technical scaffolds. Other target roots and user files remain untouched; context/structure checks make no target-agent performance or publication claim. |

Material integrated hazards include a public rename with stale routing/installer entries (DES-SR-01/15/17/18), a shared-method extraction with two surviving current definitions (DES-SR-02/08/13), and a historical reference preserved while its old approval is incorrectly reused (DES-SR-06/11/16). Delivery must allocate proof at those composed boundaries. Representative outcomes do not enumerate every legitimate concrete test.

For DES-SR-12/16, a before/after example pair may contain two parseable, schema-conforming records while violating the invariant it claims to demonstrate. Assessment must expose that violation rather than accept the pair on local syntax checks. Similarly, a changed relied-on example must not disappear from review merely because its parent model text is unchanged. These representative outcomes retain the transferred safeguards without prescribing test fixtures or expanding them into an exhaustive catalogue.

Before Distribution adoption, for DES-SR-15/17, the integrated installer outcomes are TNI-DES-01–06 and the installation owner's clean managed, locally modified, interrupted/retried and already-clean cases. Delivery must demonstrate the complete documented upgrade sequence, including failure recovery and preservation of other targets/state, rather than testing only rejection.

For DES-SR-14/15, install the package without RigorLoop's internal checkout and substantively amend a customer-owned unmigrated specification under its declared feature-format contract. The reconciliation resource must select both packaged boundary resources, preserve IDs/authority and supply the full procedure without forcing model migration. A retained architecture/ADR amendment that requires a scaffold resolves the matching installed asset or explicitly required customer template. Missing packaged guidance and missing project authority produce distinguishable scoped stops. This is a required triggered-method path, not an exhaustive list of permitted tests.

## Architecture Decisions

| ID | Context and decision | Alternatives and consequences |
| --- | --- | --- |
| DES-DEC-06 | The selected consolidation retains necessary engineering knowledge, not historical files by default. DES-SR-21 permits removal once meaning, current reliance and consumers are resolved. | Automatic snapshots preserve duplicate reading burden; indiscriminate deletion loses constraints and evidence. Earlier separately scoped retention commitments remain intact. |
| DES-DEC-01 | Separate normal authors duplicate responsibility despite the living-model profile. Use one design authoring contract and embedded decisions. | Renaming without reconciliation preserves contradiction; concatenating manuals increases load and retains dual authority. One contract needs disciplined boundaries and independent review. |
| DES-DEC-02 | Model-local clarity is insufficient for composed claims. Design owns the composition method; System owns the actual RigorLoop composition and shared outcomes. | Making Workflow or system prose own every component rule duplicates contracts; one giant Design makes every change require broad reading. Explicit owners and scoped relationships add reconciliation work where it matters. |
| DES-DEC-03 | Keep the reasoning value of arc42/C4 without mandatory separate files or twelve-section schema. Preserve existing model structural format and on-demand examples. | Mandatory full architecture packaging retains the inconsistency; no method loses trust/runtime/quality reasoning. Conditional depth requires semantic review rather than word/diagram-count checks. |
| DES-DEC-04 | Withdraw old public authoring entries together. Use safe detection, installer-owned authorized replacement of an exact managed tree, and scoped manual cleanup only for unmanaged targets. Retain portable legacy-document authoring with complete conditional resources. | Forwarding wrappers retain a competing contract; unconditional manual pre-deletion breaks the managed hash basis. Broad deletion risks local edits. The bounded replacement checks the original basis before removal and requires backup/recovery; it deliberately replaces the earlier draft's universal cleanup instruction without relaxing drift checks. |
| DES-DEC-05 | Migrate the whole architecture-method responsibility, Workflow's document convention and a bounded system-composition slice; retain historical artifacts and unmigrated current owners. | Whole-repository consolidation delays delivery; copying everything creates conflicting authority. Explicit mappings and deferred owners make the temporary coexistence inspectable. |

No new standalone ADR is required for this adopted model-profile draft. The material decision table and source-decision mapping carry its rationale; the old ADRs remain separate historical evidence.

## Quality Requirements

| Quality | Reviewable outcome | Basis |
| --- | --- | --- |
| Coherence | A reader resolves an obligation and each shared interaction to one current owner after adoption. | DES-SR-02, DES-SR-07, DES-SR-13 |
| Credibility | Important claims expose assumptions, plausible violations and sufficient feasibility basis without universal prototype requirements. | DES-SR-04, DES-SR-09 |
| Testability | Delivery can derive local and integrated proof from observable outcomes without rebuilding old spec/architecture pairs. | DES-SR-03, DES-SR-10, DES-SR-16 |
| Portability | Installed triggered resources are complete, and the public method does not depend on contributor-only model files. | DES-SR-15, DES-SR-17 |
| Historical fidelity | Source identities, old decisions and review judgments are not retargeted or erased during migration. | DES-SR-06, DES-SR-11, DES-SR-18 |

## Risks and Technical Debt

Conditional loading can omit a needed technical method; semantic review must assess actual triggers and integrated examples. A general-purpose Design can become oversized; split only a coherent responsibility with an explicit reference map. Installer guards cover supported CLI publication, not arbitrary manually retained agent files. Mixed documents remain a navigation cost until their named follow-ups complete. None of these risks authorizes weakening the first slice's single-owner, evidence or compatibility obligations.

## Glossary

Model: a coherent engineering responsibility with owned concepts and rules. Design: its living normative engineering document, and the authoring method named here. System view: composition-owned obligations and references across models. Consolidation: reconciled authority and decision meaning, not merely a move or rename. Representative scenario: a requirement-grounded condition/outcome from which further justified tests may derive.

## Next artifacts

Independent Design Review of Design, System, the Workflow amendment and the scoped Target-native init amendment, including exact adoption maps and relevant unchanged dependencies. Authorized Delivery planning allocates the concrete edits and proof only after that package is approved.

## Follow-on artifacts

None yet.
