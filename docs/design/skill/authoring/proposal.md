# Request and proposal intake

Model validation contract: model-document-v1

A request, proposal, issue or incident supplies RR input to Requirement Analysis. It is not an IR merely because its proposed direction was approved, and it does not introduce a separate Proposal Review gate. Preserve its source, intended outcome, constraints and open questions without requiring an extra document or record solely to begin analysis.

[Engineering authoring](design.md#authoring-responsibilities) and the canonical [Requirement Analysis method](../../../../rem/methods/requirement-analysis.md) own interpretation against existing requirements. Reuse without modification, refinement, creation, deferral and an explicit conflict are valid dispositions when justified. Proposed technology remains a candidate solution unless the caller establishes it as a genuine constraint.

[Workflow](../workflow.md) owns the first mandatory Requirement Review, followed by System/Architecture Design and one integrated Design Review. Optional Explore and Research can resolve material uncertainty without supplying approval or expanding execution authority.

## Historical disposition

The former Proposal authoring capability, its preliminary approval semantics and exclusive presentation pilot are retired from the successor. Applicable intent, scope, feasibility, uncertainty and authority duties move to Requirement Analysis and its supporting REM methods. Earlier proposal bytes and judgments retain their original meaning; they are not rewritten as accepted IR/SR assessments. The prior contract is recoverable at commit `39be9c81` under this path and `skills/proposal/`.

## Requirements

These stable local references reconcile the prior document contract with the current REM and Module owners linked above. They do not retain the superseded workflow or filesystem interface.

| ID | Required behavior |
| --- | --- |
| PROP-SR-01 | RR intake MUST preserve the request’s outcome, constraints, source and proposed solution without treating a proposal as approved IR. |
| PROP-SR-02 | Analysis MUST inspect existing IR/SRs and decide justified reuse, refinement or creation, keeping material uncertainty visible. |
| PROP-SR-03 | Authoring MUST respect exact requested scope, authority and existing work; ambiguous authority does not justify fallback or implicit expansion. |
| PROP-SR-04 | Requirement Analysis MUST load the relevant REM methods and enough current model context to assess stakeholder need and supporting Feature/Scenario coverage. |
| PROP-SR-05 | Operational recording MUST use current CLI tasks and revisions; recorded source material does not grant engineering acceptance. |
| PROP-SR-06 | The first mandatory review MUST assess the requirement basis, including reuse. No separate Proposal approval gate or mandatory RR document is required. |

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | PROP-SR-01 | Unknown contracts, malformed references or unsupported scope stop the affected operation without inferred defaults. |
| State/lifecycle | PROP-SR-01 | Progress, accepted basis, review judgment, final Verify and historical completion remain distinct; saved state alone advances none. |
| Identity/authority | PROP-SR-01 | The actual responsible actor, declared scope and current support govern reliance; an identifier or role label does not establish authority. |
| Composition/path | PROP-SR-01 | Changed producer and consumer contracts are reconciled together, including packaged conditional resources and referenced engineering definitions. |
| Temporal/retry | PROP-SR-01 | A changed basis requires rereading and proportionate reassessment; an old submission does not acquire current authority on retry. |
| Failure/recovery | PROP-SR-01 | Interrupted work exposes its actual outcome and an owned next step without erasing unresolved issues or inventing success. |
| Compatibility/migration | PROP-SR-01 | Retired procedures remain historical; successor behavior requires explicit applicable adoption/import and cannot relabel old approval. |
| External/environment | PROP-SR-01 | Local engineering results remain separate from installed, published or hosted outcomes; required observations must actually be made. |

## Test design

Inspect the current responsibilities and boundary scenarios against the owning REM model and Module contract. Structural checks establish format only; independent review judges semantic coverage. Runtime record behavior is exercised by the package’s operational store, update, reliance, review and maintenance tests; skill guidance is assessed in actual generated archives with the resource validator and independent scenario inspection. Required combined and negative proof is allocated in the adoption plan.
