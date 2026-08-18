# Explain-Change Skill Simplification

## Owning change record

Portable authoring. No governed change record owns this proposal at creation time. Formal review evidence may use the recording-only fallback required by the review-recording contract; that fallback does not activate lifecycle settlement or workflow continuation.

## Problem

The published `explain-change` skill is a 1,175-word, 8,224-byte, approximately 2,056-token flat `SKILL.md`. Every invocation loads the complete durable-artifact placement hierarchy, change-local review-resolution closeout procedure, planned-initiative state rules, workflow-managed handoff prerequisites, ten-section document layout, and portable inline-explanation guidance.

The behavior is valuable, but the concerns do not all activate together. A developer asking why a small isolated diff changed should receive a truthful trace from the actual diff without loading RigorLoop-specific `change.yaml`, milestone, final-review, and review-resolution procedure. Conversely, workflow-managed final explanation must remain bound to the exact final reviewed diff, use the current change-local artifact, refuse stale or open review evidence, and hand back to workflow without claiming verification or PR readiness.

Repeated document structure is also embedded directly in procedure. The required section order, file-rationale table, validation-evidence layout, and conditional review-resolution summary have no copied structural owner. This makes the root file longer and encourages drift among durable explanations.

The optimization must reduce the real loaded workflow profile as well as the portable profile. Merely moving prose out of `SKILL.md` while making every normal invocation load an equal or larger reference-and-asset assembly would not be a successful simplification.

## Goals

- Reduce loaded procedure for portable inline, portable durable, governed inline, and governed durable explanation.
- Keep actual-diff grounding, truthful traceability, scope honesty, validation-gap disclosure, stop conditions, claim limits, and resource triggers in a compact universal `SKILL.md`.
- Move only change-local lifecycle eligibility, exact final-review and diff-basis validation, review-resolution closeout, governed artifact placement, staleness, and workflow handback into one conditional reference.
- Give durable explanation headings, ordering, repeated table shapes, metadata locations, and conditional groups one copied structural asset.
- Preserve the current workflow contract: final `explain-change` precedes `verify`; non-trivial changes require durable reasoning; PR text does not replace that artifact; `explain-change` never claims final verification or PR readiness.
- Bind governed explanations to the exact reviewed repository state and make stale evidence fail closed.
- Preserve portable customer-project behavior without requiring RigorLoop-internal lifecycle files.
- Measure every real loaded assembly, structural assets, complete package size, and canonical-through-installed parity separately.

## Non-goals

- Changing the standard lifecycle order, review-resolution contract, final code-review gate, verification ownership, PR contract, or lifecycle-state owner.
- Changing the meaning of trivial versus non-trivial work or deciding when a separate verify report is required.
- Turning `explain-change` into code review, verification, proposal/spec review, artifact settlement, milestone management, or workflow routing.
- Generating explanations automatically from Git history without judgment.
- Adding an executable explanation generator, semantic grader, model-runtime benchmark, transcript-scoring system, tokenizer dependency, or target-agent acceptance harness.
- Rewriting historical `docs/changes/**/explain-change.md` or approved legacy `docs/explain/*.md` artifacts merely to adopt a new skeleton.
- Performing section-level refresh, mixed owned/unowned body preservation, managed Markdown regions, or historical-layout parsing.
- Creating multiple narrow references, a second explanation artifact class, a new lifecycle state, a new persistence owner, or a new transaction record.
- Optimizing unrelated skills except directly coupled contract, validator, packaging, fixture, or architecture-document consumers.

## Vision fit

fits the current vision

The change makes a mandatory workflow stage easier to understand and cheaper to load while preserving durable reasoning, source-ranked evidence, human reviewability, explicit authority, and Git-tracked artifacts. It does not replace judgment with hidden runtime machinery or weaken the final verification boundary.

## Context

`specs/rigorloop-workflow.md` requires PR-summary explanation for every change and a standalone durable explanation for non-trivial changes. New non-trivial work defaults to `docs/changes/<change-id>/explain-change.md`; approved legacy top-level explanation artifacts remain compatible. Final `explain-change` runs after final holistic code review and before final `verify`, and may report only validation evidence available at authoring time.

`specs/skill-contract.md` classifies `explain-change` as an authoring skill, requires a reviewable output shape, permits packaged references and assets with explicit `READ` and `COPY` mappings, and requires changed packages to preserve resource integrity across generated, archived, release-candidate, and installed forms.

The current skill has no packaged resources. Its largest section is `Rules`, at roughly one quarter of the file by bytes. Several rules are universal truthfulness constraints, while others apply only to governed workflow closeout. Current validators also consume exact phrases such as `review-resolution.md`, concise linked summaries, upstream read-only behavior, and readiness boundaries. Those consumers must be inventoried before relocation so behavioral requirements and parser-sensitive literals are not confused.

The repository already supports the selected package pattern. No new loader or execution model is needed. The bounded architecture assessment should therefore expect `architecture-not-required` unless exact staleness or recovery requires a new durable schema or state owner.

## Options Considered

### Option 1: Keep the flat skill

This has the lowest migration risk and no package growth. It preserves unnecessary lifecycle procedure on portable explanation requests and leaves repeated durable-document structure embedded in the common file.

### Option 2: Editorially compress only `SKILL.md`

This can reduce total bytes with minimal packaging work. It cannot create a real portable/governed loading boundary, and aggressive compression risks obscuring the final-diff, review-closeout, and readiness safeguards that make the stage trustworthy.

### Option 3: Add only a structural asset

Moving the ten-section layout into a copied skeleton would clarify output ownership. Portable requests would still load governed artifact-placement, review-resolution, planned-work, and workflow-handoff procedure.

### Option 4: Add one governed workflow reference and one structural asset

Keep universal explanation quality and fail-closed resource selection inline. Load one reference only for a governed candidate, and copy one asset for every durable artifact creation or authorized refresh. This separates a genuine authority boundary while keeping the package small.

### Option 5: Split placement, review closeout, evidence identity, and handoff into several references

These concerns activate together for workflow-managed durable explanation. Multiple references would increase ordering, contradiction, and missing-resource states without reducing a real loaded assembly.

### Option 6: Add executable generation or semantic grading

A generator could standardize headings, and a model-based grader could score prose. Both introduce new runtime, portability, testing, and authority surfaces without proving that the explanation is true. Static contract scenarios and normal lifecycle review are sufficient for this refactor.

## Recommended Direction

Choose Option 4:

```text
compact skills/explain-change/SKILL.md
+ references/governed-workflow-explanation.md
+ assets/explain-change-skeleton.md
+ no scripts
```

### Classify output action independently from governance

Use three internal output actions:

```text
inline-explanation
create-durable-explanation
refresh-durable-explanation
```

The action is determined from the user request, the project workflow contract, target existence, and exact artifact identity. It is not lifecycle authority.

| Requested result | Target state | Result |
| --- | --- | --- |
| Inline explanation | No durable artifact required | Return an inline explanation; no repository write |
| Create durable explanation | Exact target absent | Create the artifact |
| Create durable explanation | Target already exists | Stop; require explicit refresh |
| Refresh durable explanation | Exact target exists and current identity is known | Refresh the artifact |
| Refresh durable explanation | Target absent | Stop; route to creation |
| Any durable action | Target path or identity ambiguous | Stop before writing |

A workflow-managed non-trivial change selects a durable action. A direct manual request remains isolated and may use inline output only when the governing project contract does not require durable reasoning. The skill never silently downgrades a required durable artifact to chat output.

Portable durable authoring requires either an explicit exact target path from the current user request or one exact portable path resolved by the project-local contract. When neither exists, durable output is blocked. Portable authoring never creates a change root, `change.yaml`, workflow state, or other governed state merely to obtain an output location.

Creation and refresh authority are separate. `create-durable-explanation` requires an absent exact target. `refresh-durable-explanation` requires an existing exact target plus either an explicit current user refresh request or a validated governed stale-artifact route. Target existence alone never grants replacement authority.

### Use tri-state governed-signal classification

Before loading conditional procedure, classify:

```text
no-governed-signal
single-governed-candidate
invalid-or-ambiguous-governed-signal
```

Governed signals include an explicit current change ID, a workflow-managed invocation naming an exact change, a target under a structured change-local location, or a valid structured owning-change pointer supplied by project metadata. Any present malformed, conflicting, escaped, duplicated, or stale governed signal is `invalid-or-ambiguous-governed-signal`; it stops and never falls through to portable writing.

`single-governed-candidate` loads `references/governed-workflow-explanation.md`. Loading does not grant write, lifecycle, routing, or readiness authority. The reference must validate the exact change, target, current workflow contract, final-review basis, and permitted output action before governed writing.

### Define four exhaustive loaded assemblies

| Assembly | Context | Loaded package content |
| --- | --- | --- |
| `EC0-portable-inline` | No governed signal and no durable artifact obligation | `SKILL.md` only |
| `EC1-portable-durable` | No governed signal and one exact portable durable target | `SKILL.md` plus copied skeleton |
| `EC2-governed-inline` | One valid governed candidate and no durable artifact obligation | `SKILL.md` plus governed reference |
| `EC3-governed-durable` | One valid governed candidate and one current durable artifact obligation | `SKILL.md`, governed reference, and copied skeleton |

Governance and output durability remain independent. A direct isolated request naming an exact change may use `EC2-governed-inline` only when the validated project contract permits inline output. A workflow-managed non-trivial change uses `EC3-governed-durable`. A governed candidate does not make durable output optional when the project contract requires it.

Late discovery of a governed signal changes `EC0` to `EC2` or `EC1` to `EC3` before any governed interpretation or write. Late discovery of a durable obligation changes `EC0` to `EC1` or `EC2` to `EC3` before output. Invalid or ambiguous governed signals stop before either form of output and never fall back to a portable assembly. A missing triggered resource blocks only its dependent assembly; an untriggered resource does not block another profile.

### Keep universal obligations inline

The compact root file remains responsible for:

- routing from the actual request and distinguishing `explain-change` from review, verify, and PR work;
- project-local evidence and portable defaults;
- output-action and tri-state governed-signal classification;
- exact diff or changed-file resolution;
- requirement, design, plan, test, review, and validation traceability only when supported by evidence;
- explicit treatment of observed facts, bounded inference, unknowns, unrelated changes, non-goals, risks, and validation gaps;
- sensitive-data and machine-local-data exclusion;
- resource selection and missing-resource behavior;
- universal write boundary, stop conditions, claims, and concise result fields.

The root file must remain capable of producing a safe inline explanation without the reference or asset. It must not reconstruct missing conditional procedure or document structure from memory.

### Give the governed reference one coherent responsibility

`references/governed-workflow-explanation.md` owns only procedure that activates after a single governed candidate is detected:

- exact change-root, target, and project-workflow validation;
- non-trivial durable-artifact requirement and approved legacy-path handling;
- final holistic code-review and complete final-diff eligibility;
- `review-log.md` and conditional `review-resolution.md` closeout checks;
- current milestone and workflow-stage interpretation from the owning state surface;
- exact explanation-basis construction and staleness comparison;
- governed create/refresh preconditions and bounded write/read-back procedure;
- workflow-managed completion result and return of control to workflow for `verify` routing.

It does not own explanation quality, semantic traceability, lifecycle mutation, artifact settlement, milestone transitions, final verification, PR readiness, or workflow continuation.

### Separate the reviewed subject from explanation recording

Before returning or writing a governed explanation, resolve a reviewed-change basis containing at least:

```text
change identity
repository identity
base revision
reviewed-subject revision
reviewed-diff identity from base to reviewed subject
final holistic code-review ID and reviewed-subject identity
governing proposal/spec/architecture/plan/test-spec identities when applicable
review-resolution identity or explicit not-required basis
validation-evidence cutoff
canonical explanation path and prior identity
```

The final reviewed diff is exactly the base revision to the reviewed-subject revision. It excludes the later explanation artifact and later verify-owned evidence. `EC3-governed-durable` records the complete successful reviewed-change basis in the explanation artifact. `EC2-governed-inline` reports it without manufacturing a durable artifact. The explanation describes one exact reviewed change, not an unbounded branch narrative.

Explanation recording is a separate identity group:

```text
explanation path
explanation content identity
recording revision
handoff revision
```

The artifact can record its own path, content basis, and reviewed subject without trying to embed a self-referential commit hash. The existing workflow or verify evidence resolves and checks the Git-derived recording and handoff revisions after the artifact is committed. This split does not grant `explain-change` authority to mutate workflow or verification evidence.

The handoff revision may equal the reviewed-subject revision when no durable write is required, or it may be one direct-child explain-change-owned evidence commit. In this first version that commit contains only the exact explanation artifact. It contains no product code, tests, specifications, architecture, plans, dependencies, configuration, generated output, unrelated documentation, change-record mutation, or another stage's evidence or state. A repository's already-approved equivalent closed evidence-tail contract may be used only when it provides the same subject, ownership, and content guarantees.

A broader change, multiple unexplained post-review commits, a changed governing identity, or a non-direct-child tail makes final-review reuse stale and requires a fresh final review. Later verify-owned evidence does not by itself stale the explanation because it falls after the recorded validation cutoff.

If the reviewed subject, final review, governing decision-bearing artifact, review closeout, or explanation content changes, the explanation is stale. `verify` checks that the reviewed subject still matches final review, the explanation matches its basis, the evidence tail is closed, and no decision-bearing or implementation change followed review. It routes stale artifacts back to `explain-change`; neither stage silently edits upstream artifacts.

### Use one atomic whole-file durable write protocol

For create or refresh:

1. Resolve the exact output action, target, current target identity, and complete evidence basis.
2. Confirm all required governed closeout evidence is current before writing.
3. Compose the complete intended artifact from the current structural asset before mutation, for both creation and refresh.
4. Include the complete successful explanation basis in the intended governed artifact.
5. Validate required sections, stable IDs, links, command claims, sensitive-data exclusions, and basis identities before mutation.
6. Re-read the target and every decision-bearing identity.
7. Perform one whole-file atomic replacement of the exact target using the current environment's supported safe replacement capability.
8. Read back the artifact and confirm its complete identity, metadata, and structural fields.
9. Report completion to workflow; do not mutate `change.yaml`, milestone state, review evidence, routing, verification, or PR state.

Every durable refresh is a complete whole-file composition and replacement. The first version does not perform section-level refresh, preserve mixed owned and unowned regions, parse historical layouts, or manage Markdown regions. Historical explanations remain unchanged until a genuine refresh is explicitly requested or required; refreshing one artifact is not bulk migration.

The first version does not claim resumable partial-write recovery. If atomic replacement is unavailable, fails, or leaves an uncertain result, report `blocked` and do not adopt partial output. A later invocation resolves the current bytes and all governing evidence afresh, then begins a new create or refresh operation. It may accept the target as complete only when read-back proves the entire intended artifact and successful basis; otherwise unrelated, partial, ambiguous, or concurrently changed content stops. No prepared transaction record, lifecycle state, or additional persistence owner is introduced.

### Make the asset the sole structural owner

`assets/explain-change-skeleton.md` owns only:

- title and stable section order;
- the mandatory governed explanation-basis metadata group and its location, plus the portable metadata insertion location when a project contract requires one;
- `Summary`, `Problem`, `Decision trail`, `Diff rationale by area`, `Tests added or changed`, `Validation evidence available before final verify`, `Alternatives rejected`, `Scope control`, and `Risks and follow-ups` headings;
- the file/area rationale table columns;
- validation-evidence table columns;
- insertion locations for conditional `Review resolution summary` and `Workflow handback` groups;
- visible placeholders and template metadata.

The skill and governed reference own applicability, evidence meaning, sufficiency, staleness, and claims. Inapplicable conditional groups are omitted. Applicable but unresolved content reports an explicit blocker rather than leaving placeholders.

Every durable creation and refresh uses the current skeleton to compose the complete artifact. Historical artifacts are not bulk-migrated; they adopt the current skeleton only when they are genuinely refreshed under current authority.

### Preserve current review-resolution semantics

When material findings exist, the explanation summarizes counts by final disposition and links the exact `review-resolution.md`; it does not reproduce review transcripts. `Closeout status: open`, any `needs-decision`, or any open finding blocks governed explanation completion. A stage-owned non-approval cannot be treated as resolved merely because `review-resolution.md` contains a disposition; the required later same-stage review or owner closeout must be part of the current basis.

No-material detailed review records may have `review-log.md` without an empty `review-resolution.md`. Clean review receipts remain valid evidence but do not by themselves establish lifecycle settlement beyond their governing contract.

### Keep readiness and routing ownership closed

An isolated direct invocation returns its explanation and stops. A governed workflow invocation may report that the explanation artifact is current for its exact basis and return control to workflow. Only workflow decides whether `verify` is next. `explain-change` never claims final verification, branch readiness, PR-body readiness, PR-open readiness, hosted CI completion, release readiness, deployment readiness, or final lifecycle completion.

The conditional `Workflow handback` group reports only:

```text
Explanation status: current | blocked
Explanation basis: <identity>
Validation evidence cutoff: <identity or timestamp>
Open explain-change blockers: <IDs or none>
Control returned to workflow: yes | no
Next-stage decision owner: workflow
```

Portable inline output omits the group. Portable durable output omits it unless a project contract explicitly requires neutral handback metadata. Governed inline output reports the same facts in its result rather than copying the durable skeleton. Governed durable output includes the group whether complete or blocked. An isolated invocation never claims workflow continuation.

The skeleton owns the labels and location only. `SKILL.md` and the governed reference own applicability, the meaning of `current`, blocker rules, and claim limits. The group must not contain or imply `verify-ready`, `verification-passed`, branch, PR, release, deployment, or lifecycle readiness. Any parser-sensitive migration from the old label must update all active consumers in the same reviewed slice.

### Preserve compatibility through separate inventories

Before editing, record:

1. a semantic-rule inventory for actual-diff grounding, required durable reasoning, path compatibility, final-review prerequisites, review closeout, traceability, validation wording, workflow order, stops, claims, and handoff; and
2. a literal-consumer inventory for parser-owned metadata labels, validator-required phrases, headings, paths, readiness terms, and package resource mappings.

Relocating a semantic rule requires proving that every applicable assembly still loads it. Relocating a consumed literal requires updating every active consumer in the same reviewed slice. Incidental tests should be changed to assert the correct package owner rather than forcing all text to remain in `SKILL.md`.

## Architecture Impact

The expected bounded result is `architecture-not-required`. The proposal reuses the accepted published-skill package model: one canonical `SKILL.md`, mapped `READ` references, mapped `COPY` assets, generated package parity, and ordinary change-local Markdown evidence. It adds no service, runtime, schema owner, lifecycle state, external integration, or executable synchronization mechanism.

A documentation-only architecture update is appropriate if the current architecture inventory presents `explain-change` as permanently flat or omits the resulting mapped resources.

Architecture becomes required if downstream specification or implementation discovers that safe basis binding, reviewed-subject/evidence-tail representation, or whole-file replacement needs a new persisted transaction record, new machine-readable schema, new lifecycle state, new routing owner, or new cross-stage write authority. The implementation must not weaken recovery claims merely to preserve the expected no-architecture result.

## Testing and Verification Strategy

Use deterministic contract and package proof:

- freeze the current word, byte, line, and estimated-token baseline;
- inventory semantic rules and exact literal consumers before edits;
- test the tri-state governed-signal classifier, three output actions, four loaded assemblies, and every late-trigger transition;
- prove `EC0` can explain safely without conditional resources;
- prove `EC2` loads governed procedure without manufacturing a durable artifact;
- prove `EC3` blocks on stale final diff, missing final review, open review resolution, conflicting target identity, or missing resources;
- prove create-versus-refresh target-state and authority behavior, current-skeleton whole-file composition, read-back, and fresh reclassification after uncertain failure;
- prove the asset owns structure without owning policy;
- prove historical artifacts remain untouched without a genuine refresh and every genuine refresh uses the current skeleton;
- prove the reviewed diff ends at the final-reviewed subject and excludes the closed explanation evidence tail;
- prove only one direct-child explanation-only evidence commit is accepted and every broader tail makes the final review stale;
- prove later verify evidence alone does not stale an otherwise current explanation;
- prove `Workflow handback` reports only explain-change-owned facts and never claims readiness;
- prove canonical, generated, archived, release-candidate, and installed resource path and raw-byte parity;
- run existing skill, workflow, review-artifact, lifecycle, adapter, and token-cost checks selected by the repository-owned validation system.

Acceptance does not execute Codex, Claude Code, opencode, or another target-agent runtime. It does not add a separate manual semantic-review gate or prose-grading stage. Ordinary proposal, spec, code, verification, and PR review remain the human judgment surfaces.

Report separately:

```text
EC0-portable-inline words and bytes
EC1-portable-durable words and bytes
EC2-governed-inline words and bytes
EC3-governed-durable words and bytes
SKILL.md size
reference size
asset size
complete package size
```

Use one closed formula: count each file loaded or copied by an assembly exactly once. Every supported assembly must decrease in both words and bytes from the current 1,175-word, 8,224-byte flat baseline. Estimated tokens may be reported through the existing measurement tool but do not replace the exact word and byte gate. A shorter root file alone is insufficient. Total package growth remains visible and requires rationale; inability to improve one assembly requires an explicit proposal amendment rather than a silent exemption.

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-EXCSIM-001` | Governance classification and output action remain independent. |
| `AC-EXCSIM-002` | Every valid governance/output combination has one named loaded assembly. |
| `AC-EXCSIM-003` | Governed inline explanation loads the reference but not the durable skeleton. |
| `AC-EXCSIM-004` | A governed durable obligation loads both the reference and skeleton. |
| `AC-EXCSIM-005` | Invalid or ambiguous governed signals stop without portable fallback. |
| `AC-EXCSIM-006` | Durable creation and refresh use one complete atomic whole-file replacement after revalidation. |
| `AC-EXCSIM-007` | No retry adopts partial content whose complete identity and basis were not proven. |
| `AC-EXCSIM-008` | A completed governed explanation stores the exact basis required for staleness checks. |
| `AC-EXCSIM-009` | Every supported loaded assembly is measured using one closed formula. |
| `AC-EXCSIM-010` | Every supported assembly decreases in words and bytes from the current flat baseline. |
| `AC-EXCSIM-011` | Complete package growth is reported independently from loaded-profile improvement. |
| `AC-EXCSIM-012` | No target-agent runtime or separate prose-grading acceptance stage is introduced. |
| `AC-EXCSIM-013` | Every durable create or refresh composes a complete artifact from the current skeleton. |
| `AC-EXCSIM-014` | The four loaded assemblies are exhaustive for every supported output action. |
| `AC-EXCSIM-015` | Refresh requires explicit current user authority or a validated governed stale-artifact route. |
| `AC-EXCSIM-016` | Portable durable authoring never creates governed state implicitly. |
| `AC-EXCSIM-017` | Reviewed-subject revision and explanation recording revision are represented separately. |
| `AC-EXCSIM-018` | The reviewed diff excludes the permitted explain-change-owned evidence tail. |
| `AC-EXCSIM-019` | A post-review evidence tail is limited to one exact direct-child explanation-only commit or an existing equivalent closed contract. |
| `AC-EXCSIM-020` | Any broader or unexplained post-review change invalidates the final-review basis. |
| `AC-EXCSIM-021` | The skeleton contains no field that claims verification, branch, PR, release, deployment, or lifecycle readiness. |
| `AC-EXCSIM-022` | `Workflow handback` reports only explain-change-owned state and names workflow as next-stage decision owner. |
| `AC-EXCSIM-023` | Later verify-owned evidence does not stale the explanation merely because it follows the recorded validation cutoff. |
| `AC-EXCSIM-024` | Architecture becomes required when existing evidence cannot safely represent reviewed-subject and evidence-tail identity. |

## Rollout and Rollback

Roll out as one package revision:

1. freeze rules, literals, consumers, profiles, and size baselines;
2. amend the focused explain-change contract and test specification;
3. perform the bounded architecture assessment and update architecture inventory only when required;
4. add the reference and asset, then compact the root skill;
5. update directly coupled validators, fixtures, packaging, and generated outputs;
6. prove loaded-profile reduction and package-chain parity;
7. complete ordinary lifecycle review and verification.

Do not migrate historical explanation artifacts merely to adopt the skeleton. New durable artifacts and every genuinely authorized refresh use the current skeleton for complete whole-file composition.

Rollback restores the previous flat `skills/explain-change/SKILL.md`, removes both mapped resources, regenerates packages from canonical source, and reverts only coupled consumers whose new behavior depends on the package split. Durable explanations authored during the rollout remain ordinary Markdown evidence and do not require deletion.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Universal truthfulness rules move behind a governed trigger | Maintain a closed universal-rule inventory and prove `EC0` without references |
| A loaded profile grows despite a shorter root file | Measure all four assemblies under one formula and reject root-only improvement |
| Governed signal detection becomes circular | Use tri-state signal presence for loading; keep complete authority validation in the reference |
| The skeleton becomes a policy owner | Limit it to labels, ordering, tables, metadata locations, and placeholders; test forbidden policy prose |
| Historical explanations are rewritten unnecessarily | Require genuine refresh authority; do not bulk-migrate untouched artifacts |
| Existing parser or validator literals disappear | Maintain a separate literal-consumer inventory and update all active consumers atomically |
| Explanation writing makes its own final review look stale | Separate the reviewed subject from the closed explanation-owned evidence tail |
| Handback language overclaims readiness | Use a closed `Workflow handback` group and reserve routing and verification conclusions for their owners |
| Replacement overwrites concurrent human edits | Re-read every identity immediately before one atomic whole-file replacement and stop on uncertainty |
| Conditional resource failure weakens safety | Fail closed before dependent judgment or writes; never reconstruct missing procedure from memory |
| Package size grows because structure becomes explicit | Report complete package size separately and require every real loaded assembly to improve |

## Open Questions

None at proposal level. Exact metadata field names, validator fixture names, selected commands, and the final compact wording belong to specification, planning, and implementation as long as they preserve the semantics decided here.

## Decision Log

- Select one governed workflow reference and one explanation skeleton.
- Keep universal actual-diff truthfulness and claim limits inline.
- Separate output action from governed authority.
- Use tri-state governed-signal classification with no malformed-signal fallback.
- Resolve `EXCSIM-PR1` with four exhaustive governance/output assemblies.
- Resolve `EXCSIM-PR2` with atomic whole-file replacement, no resumable partial-write claim, and fresh classification after uncertainty.
- Resolve `EXCSIM-PR3` with one measurement formula and reduction requirements for every assembly.
- Resolve `EXCSIM-PR4` by requiring current-skeleton whole-file composition for every durable create and refresh.
- Resolve `EXCSIM-PR5` by separating the final-reviewed subject from one closed explanation-owned evidence tail and later verify evidence.
- Resolve `EXCSIM-PR6` by replacing `Verify readiness` with an explain-change-owned `Workflow handback` group.
- Measure `EC0`, `EC1`, `EC2`, and `EC3`; require all four loaded assemblies to improve.
- Bind governed output to the exact base-to-reviewed-subject diff, final holistic review, governing artifacts, review closeout, and validation cutoff.
- Keep `explain-change` write authority limited to its own exact artifact.
- Apply the skeleton prospectively and avoid historical bulk migration.
- Use static contract/package proof and ordinary lifecycle review; add no target-agent or prose-grading acceptance stage.

## Next Artifacts

- Focused `explain-change` skill-simplification specification, followed by independent spec review.
- Bounded architecture assessment, with architecture authoring and architecture review only when required; otherwise record `architecture-not-required` and apply any bounded inventory correction.
- Execution plan followed by plan review when required by the final scope.
- Traceable test specification followed by independent test-spec review.
- Implementation, code review, explanation, final verification, and PR handoff under the standard workflow.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent proposal review. It is not yet ready for specification, implementation, verification, or PR claims until proposal-review settles the direction.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `explain-change` skill | in scope | Goals and Recommended Direction |
| Use a compact universal skill with conditional governed procedure | in scope | Recommended Direction and loaded assemblies |
| Give repeated explanation structure one owner | in scope | Structural asset decision |
| Preserve correctness and workflow safety while reducing tokens | in scope | Evidence basis, compatibility, testing, and measurement |
| Create the work on a new branch | in scope | Repository branch `proposal/explain-change-skill-simplification` |
| Run proposal review after authoring | in scope | Readiness and the separately recorded proposal-review result |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal `SKILL.md` | core to this proposal | Defines the common-path simplification |
| Governed workflow reference | core to this proposal | Owns the genuine lifecycle activation boundary |
| Explanation skeleton | core to this proposal | Owns repeated durable structure |
| Focused contract and test-spec changes | same-slice dependency | Public behavior and proof must remain aligned |
| Direct validator and fixture consumers | same-slice dependency | Exact active consumers must follow relocated ownership |
| Package generation and install parity | same-slice dependency | Mapped resources must ship together |
| Architecture inventory correction | first-slice candidate | Needed only if bounded assessment finds stale package documentation |
| New persisted recovery schema or state owner | separate proposal | Would materially expand architecture and authority |
| Executable generator or semantic grader | out of scope | Disproportionate to a Markdown package refactor |
| Optimization of another skill | separate proposal | Avoids silent multi-skill expansion |
