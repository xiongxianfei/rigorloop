# Simplified Proposal Contract Specification

## Owning change record

`docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

[Simplify the RigorLoop Proposal Contract](../docs/proposals/2026-08-30-simplify-rigorloop-proposal-contract.md)

## Goal and context

This specification defines the observable authoring, review, lifecycle-ownership, compatibility, and publication contract for concise RigorLoop proposals. A proposal approves a direction; Design owns detailed behavior and architecture, and Delivery owns implementation and proof planning.

The contract removes proposal-owned lifecycle metadata and routine vision-alignment metadata while retaining proportional feasibility, independent Proposal Review, durable review evidence, and governed ownership in `change.yaml`.

## Glossary

- **proposal content contract**: the required level-two sections and their decision responsibilities.
- **portable proposal**: a proposal not referenced by a governed change record.
- **governed proposal**: a proposal referenced by the primary proposal entry in `docs/changes/<change-id>/change.yaml`.
- **routine vision alignment**: a Proposal Review judgment that the direction fits current `VISION.md` and requires no proposal-level exception decision.
- **material vision issue**: a conflict, revision request, or bootstrap exception that could affect approval.
- **cutover**: the coordinated activation point after which current proposal authoring and review use this contract.

## Examples first

Example E1: ordinary concise proposal
Given a developer proposes a bounded workflow improvement that fits current vision
When the proposal is authored
Then it contains the seven required sections, proportional feasibility, no routine impact section, and no proposal-owned lifecycle or vision metadata.

Example E2: material impact
Given a direction has significant compatibility consequences
When the proposal is authored
Then `Impact and major trade-offs` appears between `Feasibility` and `Decision requested` and contains the consequences that could change approval.

Example E3: governed ownership
Given a portable proposal is accepted into governed work
When workflow creates or updates its change record
Then `change.yaml` references the proposal and owns its lifecycle state without rewriting the proposal to add status or a reverse pointer.

Example E4: routine vision review
Given a proposal contains no material vision conflict
When Proposal Review compares it with `VISION.md`
Then review evidence records `aligned`, and the reviewer does not request a `Vision fit` section merely to repeat that judgment.

Example E5: vision conflict
Given a direction conflicts materially with current vision
When the conflict is absent from the proposal
Then Proposal Review withholds approval and routes the conflict to proposal ownership for explicit impact disclosure and decision.

Example E6: historical proposal
Given a settled proposal predates cutover and remains unchanged
When repository compatibility validation encounters it
Then it remains readable evidence and is not rewritten into the simplified structure.

## Requirements

| ID | Requirement |
| --- | --- |
| SPC-R1 | A simplified proposal MUST contain exactly these required level-two sections in order: `Challenge`, `Goals`, `Scope and non-goals`, `Governing principle`, `Proposed direction`, `Feasibility`, and `Decision requested`. |
| SPC-R2 | A simplified proposal MAY contain `Impact and major trade-offs` only when its content could materially influence approval; when present, it MUST be the only additional level-two section and MUST appear between `Feasibility` and `Decision requested`. |
| SPC-R3 | A proposal MAY use level-three and deeper headings inside an allowed level-two section, and structure validation MUST NOT treat those nested headings as additional proposal sections. |
| SPC-R4 | A simplified proposal MUST NOT contain proposal-owned `Status`, `Owning change record`, or routine `Vision fit` sections or equivalent mutable lifecycle, reverse-ownership, or routine-alignment metadata. |
| SPC-R5 | Every simplified proposal MUST contain exactly one non-empty `Feasibility` section with an explicit assessment, a credible basis or bounded assumptions, material constraints, and any blocker that would prevent responsible Design work. Its depth MUST be proportional to uncertainty. |
| SPC-R6 | A portable proposal MUST be valid without `change.yaml`, lifecycle status, an ownership pointer, or a lifecycle command. Portable authoring and review MUST NOT claim governed settlement. |
| SPC-R7 | For a governed proposal, the matching `change.yaml` primary proposal entry MUST identify the proposal path and MUST remain the sole owner of proposal lifecycle state and governed ownership. The proposal MUST NOT duplicate that information. |
| SPC-R8 | This change MUST NOT add a proposal lifecycle field, proposal document-version marker, per-document content hash requirement, compatibility interpreter, or new CLI command. Existing lifecycle operations MAY reference the proposal through `change.yaml`. |
| SPC-R9 | Proposal Review MUST decide whether the challenge is material, goals address it, scope is bounded, the governing principle is sound, direction is concrete and justified, feasibility is proportionate, material impacts are disclosed, vision alignment is responsible, downstream decisions remain downstream, and the requested decision is explicit. |
| SPC-R10 | Proposal Review evidence MUST record exactly one vision-alignment outcome: `aligned`, `material-conflict`, `vision-revision-requested`, or `no-vision-bootstrap`. Ordinary alignment MUST be review evidence rather than required proposal content. |
| SPC-R11 | A material vision issue MUST be disclosed in `Impact and major trade-offs` and made explicit in `Decision requested`. Proposal Review MUST withhold approval when a material issue is undisclosed or lacks the required owner decision. |
| SPC-R12 | Proposal approval MUST lock the challenge, goals, scope and non-goals, governing principle, high-level direction, feasibility sufficient to proceed, and material proposal-level impacts. It MUST authorize architecture and specification authoring only. |
| SPC-R13 | Proposal approval MUST NOT lock or require detailed behavioral requirements, architecture, APIs, commands, schemas, component design, implementation sequencing, verification design, test cases, or rollout mechanics. |
| SPC-R14 | Proposal Review MUST create a material finding when the direction is too vague to approve or when proposal content prematurely settles a downstream Design or Delivery decision. It MUST NOT create a finding solely because downstream detail or a routine impact section is absent. |
| SPC-R15 | A proposal settled before cutover MUST remain valid under its settled contract. A proposal created before cutover MUST continue under the prior contract unless explicitly migrated at cutover. A proposal created after cutover, and any proposal still unsettled at cutover, MUST use this contract before later settlement. |
| SPC-R16 | Compatibility validation MUST keep untouched settled historical proposals readable while current authoring, review, and changed-proposal validation paths enforce the simplified contract after cutover. Compatibility MUST NOT require rewriting historical proposal evidence or adding a per-proposal version marker. |
| SPC-R17 | `CONSTITUTION.md`, `AGENTS.md`, workflow guidance, proposal and proposal-review skills, templates, references, validators, tests, examples, and supported adapter generation and release-validation surfaces MUST be updated together before cutover or explicitly reported as blocking drift. |
| SPC-R18 | Canonical authored skills MUST remain under `skills/`. Generated release archives and repository-local installed skill copies MUST NOT become authored truth or be hand-edited as the implementation of this contract. |
| SPC-R19 | The contract MUST NOT impose a fixed proposal length, word count, or token budget. Review MUST judge decision sufficiency and proportionality. |
| SPC-R20 | Direct Proposal Review MUST remain independent and isolated by default. Recording or settlement MUST NOT automatically start Design work. |

## Inputs and outputs

Inputs are the developer’s selected direction, current `VISION.md`, applicable governance, and any bounded feasibility evidence relied on by the proposal.

The proposal output is ordinary Markdown with one title, the required level-two sections, and the conditional impact section only when applicable. Proposal Review outputs an approval status, findings when material, the vision-alignment outcome, review evidence, and the authority or correction owner implied by that status.

For governed work, `change.yaml` maps the primary proposal artifact ID to its repository-relative path and owns its lifecycle state. No reverse mapping is serialized in the proposal.

## State and invariants

- A portable proposal can become governed without changing its content solely to add lifecycle metadata.
- Proposal content remains stage-owned; review evidence remains reviewer-owned; lifecycle state remains change-record-owned.
- Exactly one current proposal contract is used for new authoring after cutover.
- Historical settled evidence remains immutable unless a separately authorized substantive revision reopens it.
- Approval never grants Design Review, Delivery Review, implementation, verification, or PR authority.
- Review evidence records vision judgment; examples and validators never create semantic approval.

## Error and boundary behavior

- A missing, duplicated, misordered, or unknown level-two proposal section fails simplified-structure validation.
- An empty or non-credible Feasibility section fails Proposal Review even when its heading exists.
- An embedded `Status`, reverse owning-change pointer, or routine `Vision fit` section fails the simplified contract after cutover.
- A missing change record does not invalidate portable proposal authoring, but it prevents governed lifecycle settlement claims.
- A governed proposal path that does not match its `change.yaml` entry blocks lifecycle reliance without rewriting the proposal.
- Undisclosed material vision conflict, missing vision-revision authority, or unsafe no-vision bootstrap blocks approval.
- Partial cutover across canonical skills, governance, validation, or supported publication surfaces blocks release activation.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: SPC-R1, SPC-R2, SPC-R3, SPC-R4, SPC-R5, SPC-R6, SPC-R7, SPC-R8, SPC-R9, SPC-R10, SPC-R11, SPC-R12, SPC-R13, SPC-R14, SPC-R15, SPC-R16, SPC-R17, SPC-R18, SPC-R19, SPC-R20

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | SPC-R1, SPC-R2, SPC-R3, SPC-R4, SPC-R5 | BND-INPUT-001 | - |
| state-lifecycle | applicable | SPC-R6, SPC-R7, SPC-R12, SPC-R15, SPC-R20 | BND-STATE-001 | - |
| identity-authority | applicable | SPC-R7, SPC-R9, SPC-R10, SPC-R11, SPC-R12, SPC-R20 | BND-AUTH-001 | - |
| composition-path | applicable | SPC-R6, SPC-R7, SPC-R17, SPC-R18 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | SPC-R15, SPC-R16, SPC-R20 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | SPC-R11, SPC-R16, SPC-R17 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | SPC-R8, SPC-R15, SPC-R16, SPC-R17 | BND-COMPAT-001 | - |
| external-environment | not-applicable | - | - | The contract operates on repository Markdown and existing local lifecycle surfaces; it adds no network, hosted service, platform, or external dependency behavior. |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | SPC-R1, SPC-R2, SPC-R3, SPC-R4, SPC-R5 | exact required sections, optional material impact, missing, duplicate, misordered, unknown, forbidden legacy metadata, inadequate feasibility | Level-two headings define the proposal contract; nested headings do not. | Valid structure proceeds to semantic review; invalid structure routes to proposal correction. | SPC-R1 |
| BND-STATE-001 | state-lifecycle | SPC-R6, SPC-R7, SPC-R12, SPC-R15, SPC-R20 | portable draft, governed review-required, accepted, rejected, historical settled, isolated review | Proposal content does not own mutable lifecycle state. | Portable work remains isolated; governed authority comes only from `change.yaml` and matching review evidence. | SPC-R7 |
| BND-AUTH-001 | identity-authority | SPC-R7, SPC-R9, SPC-R10, SPC-R11, SPC-R12, SPC-R20 | authoring, review judgment, lifecycle ownership, workflow continuation, vision-owner decision | Each owner writes only its surface; approval authority is bounded. | Valid authority records its decision; cross-owner mutation or undisclosed owner decision blocks. | SPC-R12 |
| BND-COMPOSE-001 | composition-path | SPC-R6, SPC-R7, SPC-R17, SPC-R18 | portable skill, governed workflow, canonical skill, generated adapter, repository validator | Every path projects the same proposal contract from canonical sources. | Consistent paths proceed; drift blocks cutover or release. | SPC-R17 |
| BND-TEMPORAL-001 | temporal-retry | SPC-R15, SPC-R16, SPC-R20 | pre-cutover settled, pre-cutover unsettled, post-cutover new, identical rereview, revised proposal | Cutover does not rewrite settled history, and rereview uses current proposal evidence. | Historical settled remains valid; unsettled or revised current work adopts the current contract and requires current review. | SPC-R15 |
| BND-RECOVERY-001 | failure-recovery | SPC-R11, SPC-R16, SPC-R17 | undisclosed conflict, partial cutover, failed generation, corrected proposal, corrected canonical surface | Failure never grants approval or partial activation. | Correct forward and rereview or revalidate; historical evidence remains intact. | SPC-R17 |
| BND-COMPAT-001 | compatibility-migration | SPC-R8, SPC-R15, SPC-R16, SPC-R17 | untouched historical, explicitly migrated unsettled, post-cutover simplified, mixed surface | No per-document version marker, compatibility interpreter, or historical rewrite is required. | Supported history remains readable; current work uses the simplified contract; mixed cutover blocks. | SPC-R16 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | SPC-R6, SPC-R7, SPC-R12 | BND-STATE-001, BND-AUTH-001 | A portable proposal becomes governed and is rewritten merely to add status or reverse ownership. | Workflow records the path and state in `change.yaml`; proposal content remains unchanged and approval authority stays review-owned. |
| INT-002 | SPC-R9, SPC-R10, SPC-R11 | BND-INPUT-001, BND-AUTH-001, BND-RECOVERY-001 | Routine alignment is duplicated in proposals, or a material vision conflict is hidden as routine. | Review records ordinary alignment; material issues are disclosed in proposal impact and decision content before owner resolution and approval. |
| INT-003 | SPC-R15, SPC-R16, SPC-R17, SPC-R18 | BND-COMPOSE-001, BND-TEMPORAL-001, BND-COMPAT-001 | Skills, validators, governance, and adapters activate different proposal contracts. | Cutover remains blocked until canonical and supported published surfaces agree; settled historical evidence is not rewritten. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | SPC-R1, SPC-R2, SPC-R4, SPC-R5 | BND-INPUT-001 | - | - |
| E2 | illustration | SPC-R11 | BND-AUTH-001 | - | - |
| E3 | illustration | SPC-R7 | BND-STATE-001, BND-AUTH-001 | - | - |
| E4 | illustration | SPC-R9, SPC-R10 | BND-AUTH-001 | - | - |
| E5 | illustration | SPC-R11 | BND-AUTH-001, BND-RECOVERY-001 | - | - |
| E6 | illustration | SPC-R15, SPC-R16 | BND-TEMPORAL-001, BND-COMPAT-001 | - | - |

## Compatibility and migration

Cutover is coordinated across canonical skills, templates, review evidence, governance, validators, tests, and supported adapter release surfaces. It introduces no document version field or compatibility command.

Settled historical proposals remain readable under their settled contract. New proposals after cutover use this contract. Proposals still unsettled at cutover adopt this contract before later settlement. Existing historical proposal files are not rewritten solely for structural consistency.

## Observability

Proposal structural diagnostics identify the exact missing, duplicated, misordered, unknown, or forbidden level-two section. Proposal Review output states its decision, material findings, vision-alignment outcome, authority granted or withheld, and next owner.

Public skill output remains concise and does not expose repository-maintainer details about canonical paths, generator mechanics, or release archives.

## Security and privacy

The change adds no credentials, network access, private data, authorization capability, or external trust boundary. Proposal and review evidence must continue to avoid secrets and unnecessary private context.

## Accessibility and UX

No graphical interface is introduced. Markdown headings and review results must use plain, stable language that is readable in text-only tools and screen-reader navigation.

## Performance expectations

Proposal authoring and review should require less prompt and document context than the prior contract. Validation must remain bounded to the selected proposal, governing change record when applicable, canonical skill surfaces, and existing generated-package checks; no repository-wide content hashing or compatibility inventory is introduced.

## Edge cases

EC1. A proposal contains all seven names but places `Decision requested` before `Feasibility`; simplified-structure validation fails and names the ordering defect.

EC2. A proposal contains an `Impact and major trade-offs` section with only routine implementation cost; Proposal Review requests removal only when the content obscures the decision, not merely because the optional section exists.

EC3. A portable proposal has no change record; authoring and isolated review remain valid, but governed settlement is unavailable.

EC4. A governed `change.yaml` references the wrong proposal path; lifecycle reliance blocks without inserting a corrective pointer into proposal Markdown.

EC5. `VISION.md` is absent for a first substantive proposal; Proposal Review records `no-vision-bootstrap` and blocks unless the proposal explicitly owns the vision bootstrap decision.

EC6. An untouched historical proposal contains legacy `Status`, ownership, and `Vision fit` sections; compatibility validation keeps it readable and does not treat it as a current authoring example.

EC7. An unsettled legacy proposal reaches cutover; it is revised to the simplified contract and rereviewed before settlement.

EC8. Canonical proposal skills are updated but one supported adapter release projection still contains the previous contract; cutover and release validation block until regeneration succeeds.

## Non-goals

- Redesigning Design Review, Delivery Review, Code Review, or Verify.
- Changing ownership or lifecycle metadata for non-proposal governed artifacts.
- Defining implementation milestones or complete test cases.
- Adding proposal document versions, hashes, reverse pointers, new lifecycle fields, or CLI commands.
- Rewriting settled historical proposals.
- Imposing a fixed proposal length or token budget.

## Acceptance criteria

| ID | Acceptance criterion |
| --- | --- |
| SPC-AC1 | A new ordinary proposal contains only the seven required level-two sections and passes current proposal authoring and review conformance. |
| SPC-AC2 | A material-impact proposal adds the optional section in the defined position and remains reviewable without downstream design detail. |
| SPC-AC3 | A portable proposal requires no status, reverse pointer, change record, or routine vision field. |
| SPC-AC4 | A governed change references its proposal and owns lifecycle state solely through `change.yaml`. |
| SPC-AC5 | Proposal Review records one vision-alignment outcome and blocks undisclosed material conflicts. |
| SPC-AC6 | Current validators reject malformed simplified proposals while leaving untouched settled historical proposals readable. |
| SPC-AC7 | Canonical skills, templates, governance, validators, tests, and supported generated release surfaces agree at cutover. |
| SPC-AC8 | No new CLI command, proposal lifecycle field, proposal version marker, reverse pointer, or per-document hash requirement is introduced. |

## Open questions

None. Delivery planning may choose exact file groupings and validation commands without changing this contract.

## Next artifacts

- Design Review over this specification and `docs/architecture/2026-08-30-simplified-proposal-contract.md`.
- Execution plan and test specification after Design Review approval.

## Follow-on artifacts

None yet.

## Readiness

Ready for Design Review after governed registration and final cross-artifact validation.
