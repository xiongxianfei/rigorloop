# Skill procedures

Responsibility and allocation are defined in [module.json](module.json).

## Common invocation and ownership

MOD-012 composes FUNC-050–055 for SR-050–056. The [capability contract](capability-contract.md) owns detailed selection, portability, resource, output and specialist rules. This composition explains how those existing rules cooperate; it introduces no agent service, public command or mandatory operational record. The actor supplies the request, decisions and actual observations. The selected specialist retains its method and mutation boundary.

An invocation carries its requested outcome, selected capability, project-local or supplied subject, exact target, applicable authority and supported output scope. Portable work uses sufficient local or supplied context without requiring RigorLoop internal documents, a Change or a database. When a project workflow applies, bind its explicitly selected contract and scope; a failed governed read never selects a portable fallback. An explicit project exception retains its attributable source and limits.

| Existing behavior | Accountable composition and supporting owner | Allocated-obligation rationale |
| --- | --- | --- |
| SR-050; FUNC-050 | MOD-012 matches capability descriptions to requested outcomes, using current behavioral owners, triggers and near misses. Ambiguous fit returns the missing distinction before work. | SKL-SR-02/24 already constrain this single common selection responsibility; another AR would repeat it without separating a lower responsibility. |
| SR-051; FUNC-051/026 | MOD-012 binds invocation scope and target; MOD-006 supplies action-bound authority through IF-009. Valid existing grants remain usable within their conditions. | SKL-SR-05/15 and existing MOD-006 authority allocation retain both duties. No new target authority or permission mechanism is introduced. |
| SR-052; FUNC-052 | MOD-012 resolves the triggered resource closure and script-use contract. Packaging owns package-wide source/copy integrity; model-authoring guidance selection uses IF-008 only where applicable. | SKL-SR-08–11/13 already constrain resource selection and containment. Invocation success cannot stand for package qualification; no additional resource owner is needed. |
| SR-053; FUNC-053/032/033 | MOD-012 guides the selected specialist and preserves its usable output, stops and local handoff. MOD-008 supplies adopted model-authoring methods through IF-008; other specialists retain their linked contracts. | SKL-SR-03/04/12/24/27/29 and existing authoring allocations define the composition. No common skill wrapper acquires the specialist's authority or requires a duplicate report. |
| SR-054; FUNC-054/025/026/029/031 | MOD-012 prepares the handoff; MOD-006 supplies context and authority through IF-011/009, and MOD-007 supplies support/applicability through IF-010. | Existing workflow and assurance allocations retain stage and judgment meaning; SKL-SR-04/27 governs the consumer's handoff. The SR-079–083 ARs remain children of their own SRs, not borrowed child obligations here. |
| SR-055; FUNC-051/052/055 | MOD-012 admits the recording trigger, loads its complete procedure and submits explicit actor decisions through IF-004. MOD-010/011 retain actual command and persistence outcomes. | SKL-SR-25/26 and the existing command/storage allocation already define this boundary. A second recording authority or automatic portable-to-governed conversion is unnecessary. |
| SR-056; FUNC-052/053 | MOD-012 preserves canonical rule meaning, complete required subjects, closed vocabulary and privacy across selected reading paths and outputs. | SKL-SR-06/07/13–15 constrains existing guidance behavior across paths. This quality obligation needs no separate Function, resource service or duplicated AR. |

These seven SRs retain their current child sets. The rationale depends on the complete named contracts and current Function/Interface allocation; it is not a general exemption from deriving an AR when a new lower-level obligation or accountable boundary appears. Review examines each SR criterion as well as the composed result. Module allocation alone establishes neither Design coverage nor executed behavior.

## Resource and context changes

Resolve the selected Resource map from the identified package and its applicable canonical projection. Distinguish packaged paths from customer inputs, output targets and negative examples. Load each triggered normative method, output structure and transitive procedure before dependent use, preserving COPY/assets, READ/references and RUN/scripts meaning. Required content must be readable, contained and compatible with the same selected contract; actual script use retains its declared input, result/exit and failure behavior. The package owner separately qualifies every claimed package member, including resources not triggered by this invocation.

A new scope, target, authority condition, resource dependency or recording trigger invalidates the affected prepared invocation. Pause dependent work, reclassify it and obtain the newly required complete procedure before proceeding. Keep earlier actual effects and limitations visible. Missing, escaped, stale, mixed-version or contradictory required content blocks that path; an unrelated untriggered absence does not. A disclosed convenience fallback is permitted only when the entire needed contract is already loaded. Neither examples nor memory replace a required method.

Changing project instructions or the selected source version also requires reconsidering affected outputs and handoff support. Obtain complete subjects when the decision requires them, even if an earlier bounded read was sufficient for navigation. An unknown closed value is rejected before consistency inference; no profile or portable mode is guessed. Preserve the owning rule spelling, meaning and privacy limits without copying policy into output aids.

## Portable result and governed handoff

For SCN-051, a participant can complete an authorized portable activity from local inputs and selected resources. FUNC-053 composes the specialist procedure and reports actual output, incomplete scope, blockers and claim limits. FUNC-054 identifies the receiving owner and prerequisites. An isolated invocation ends there; authorized broader work continues only when the applicable authority and assessment dependencies hold.

SCN-056/057 add governed recording or a late trigger. Before the affected action, FUNC-055 loads the complete supported procedure and obtains current selected facts through IF-004. Keep its exact revision, compared versus reported basis and actor-supplied decisions; current v2/v4 tasks are used only when supported by the executing package. A successful save establishes persistence. Conflict or uncertain commitment requires fresh inspection and reconciliation, without replay, guessed success or fallback to ungoverned mutation. Prepared assurance content uses IF-014 where required, and MOD-007 retains the supplied judgment and its applicability.

The diagram shows the portable control path and its late-trigger interruption. Governance denotes the existing project-policy interpretation, authority and support responsibilities, not a required deployed service or database. The package and project are input sources, not new Modules.

<!-- architecture-diagram: prepare-and-use-guidance -->

```d2
shape: sequence_diagram
actor: "Engineer or agent"
skill: "Skill procedures\nMOD-012"
sources: "Selected package and\nproject inputs"
governance: "Applicable project\nGovernance / MOD-017"
actor -> skill: "Requested outcome, subject, target and scope"
skill -> sources: "Read capability and triggered complete resources"
sources -> skill: "Applicable instructions and inputs or explicit gap"
skill -> governance: "Interpret applicable authority and required support"
governance -> skill: "Covered action and conditions or unmet prerequisite"
skill -> actor: "Guide the authorized specialist procedure"
actor -> skill: "Actual output, observations and any new trigger"
skill -> skill: "Pause affected work; reclassify and load late dependencies"
skill -> actor: "Scoped result and next owner; isolated work ends here"
```

A missing prerequisite exits before the affected step; the successful arrows do not promise an output on failure. When a late trigger requires recording, use the [existing recording sequence](../../README.md#record-a-handoff-update) after its prerequisites are satisfied. The [parent handoff protocol](../../README.md#authoring-assessment-and-handoff-protocol) and [Governance review/correction sequences](../../../MOD-017-engineering-governance/README.md#whole-change-review-and-correction) retain the requirement-first dependencies and one whole-change gate. Guidance completion cannot stand for independent approval, adoption or permission to publish.

## Composition acceptance intent

Use the existing [Skill test-design groups](test-design/test-design.md) and [parent integration scenarios](../../test-design.md). The following walkthroughs identify the additional composition observations; they are Design intent, not executed agent or runtime proof.

| Starting facts and variation | Independent observation and failure exposed |
| --- | --- |
| Customer project has sufficient local input and authority but no RigorLoop internal files, workflow adoption or CLI; contrast an ambiguous target. | Portable control produces the specialist's supported scoped result; ambiguous target stops dependent action. Requiring a database or inventing a target fails the outcome. |
| A complete portable path gains a durable recording, privilege or output-scope trigger; compare missing transitive method, incompatible source version and absent untriggered resource. | Only affected work pauses and reclassifies; required dependencies and authority are settled before use. The unrelated absence neither blocks portable output nor proves package integrity. |
| A summary supports navigation but a later assessment needs the complete subject; compare a copied stale rule, unknown value and private-data request. | Full required evidence remains obtainable, owner meaning and vocabulary remain intact, and private unrelated inputs are excluded. A short readable result cannot conceal missing basis. |
| Governed recording returns saved, conflict, busy or uncertain commitment; contrast a valid standing grant with expanded scope. | Actual persistence, judgment and authority stay separate. Fresh inspection precedes reconciliation; no replay, portable downgrade or redundant request for already-covered authority occurs. |
| Completed milestone, adverse advisory finding, materially changed review basis or interrupted adoption. | Existing Workflow/Assessment owners determine prerequisites and correction. No milestone approval is synthesized, open obligations remain, and incompatible partial adoption cannot become one valid active workflow. |

## Supporting contracts

These documents retain detailed clauses and proof under this Module; they are not additional REM entities.

- [Skill Model Design](capability-contract.md)

## Guided authoring-task assessment

For SCN-034, consume the identified task basis and actual comparison under [MOD-008 guidance](../../../MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/guidance.md). Keep expectations, observations, help and unassessed scope intact through IF-008, existing IF-014 assurance preparation and explicitly selected IF-004 recording. A changed semantic candidate returns to its responsible preparation before retention; neither a save nor procedure completion establishes participant success or a formal judgment.

## Guided lessons and improvements

Consume [MOD-009 improvement Design](../../../MOD-017-engineering-governance/modules/MOD-009-engineering-learning/improvement.md) through IF-017 for SCN-035–039. Preserve selected source/context, observations versus inferences, existing contributor confirmation and limited route-result effects. Give proposals to the actual authorized owner and carry supplied assurance content through existing IF-014; only the selected writer establishes saved state. An incomplete proposal, scheduled follow-up or passing reproduction is not adopted or effective practice.
