# Skills and commands composition

[MOD-018](module.json) owns the cooperation of capability guidance, command admission and operational persistence. This is proposed composition for SR-079–083, not a new workflow submodel or adopted runtime contract. Direct entities and their realization facets retain their authority; [Governance](../MOD-017-engineering-governance/README.md) owns gate and adoption semantics.

## Authoring, assessment and handoff protocol

Each handoff identifies the requested scope, current subject set, governing requirement/design basis, unresolved findings, relevant evidence and responsible next owner. An absent item is either explicitly inapplicable or an identified gap. It is not synthesized from a stage label.

| Activity | Owned result | Reliance condition and next owner |
| --- | --- | --- |
| Requirement Analysis | RR interpretation; IR/SR reuse/refinement/creation; stakeholder Feature/Scenario analysis | Independent Requirement Review assesses the exact proposed basis, including justified reuse. |
| Requirement Review | Scoped requirement judgment and findings | Accepted basis permits authorized System/Architecture Design; Function/AR completion is not required here. |
| System Design | Logical behavior and Feature/SR–Function relationships | Work iterates with Architecture Design; changed stakeholder obligations return upstream. |
| Architecture Design | Accountable Modules, Interfaces, realization and ARs | One integrated Design Review assesses the complete affected design composition. |
| Design Review | Integrated judgment and correction ownership | Planning relies on the accepted design. Missing architectural responsibility cannot become a delivery task. |
| Plan and Delivery Review | Delivery intent, sequencing, dependencies and proof allocation; reviewed adequacy | Authorized implementation begins only with an applicable delivery basis. |
| Implement | Actual work, required checks, blockers and remaining scope | Eligible milestones continue; full implementation readiness requests one whole-change gate. |
| Code Review, advisory scope | Attributable feedback on explicitly selected interim subjects | No lifecycle approval. Material defects still require correction or disposition. |
| Code Review, whole-change scope | Exact complete candidate, governing basis, judgment and findings | Corrections return to owners and reassessment remains in the same gate. Applicable approval permits distinct Verify. |
| Verify | Current criterion support and scoped completion conclusion | Engineering defects return to their owners; evidence-only retries repeat affected verification without inventing a new review gate. Optional PR retains separate authority. |

Stage validity, artifact completeness, approval applicability, execution authority and recorded persistence outcome are separate predicates. FUNC-054 composes them; the CLI supplies observations and accepts explicit decisions without becoming a semantic router. Missing or unknown stage/scope values must reject before consistency inference. Concrete closed vocabularies and literal operation schemas belong to the replacement CLI/Records contract and require negative tests during implementation.

## Recording cooperation

Governance owns engineering meaning, including work context and supplied judgments; persistence owns coherent storage and recovery. This distinction does not create two authored copies. Governance responses reference the same operational facts and subject identities that the caller read. The participant doing a review makes the judgment; MOD-012 applies the review method, MOD-007 supplies common assurance interpretation, and MOD-011 persists the explicitly supplied result when required.

The successor [v4 record specification](modules/MOD-011-operational-record-persistence/README.md) is owned by MOD-011; MOD-010 owns the [v2 command interface](modules/MOD-010-engineering-command-interface/README.md). Their field and operation definitions are proposed contracts, not available runtime commands. Machine schema artifacts, dispatch and a qualified store adapter remain implementation dependencies. [Parent-owned test design](test-design.md) covers handoff and assurance interactions; actual execution results belong outside the current design.

## Process projection boundary

The [Process projection contract](../../../support/README.md#process-projection-refinement) maps this handoff protocol to a proposed activity detail beneath the runtime topology. Operations owns the composed handoff conditions; Governance retains gate meaning and the accountable Module/Interface facets retain execution facts. Actor roles and skills do not imply separate runtime processes. The structured projection extension is a deferred option, not a prerequisite for Architecture Design. The owning handoff and gate explanations may use Mermaid now. Customer generation and publication are addressed by the [proposed browser composition](../../README.md#customer-architecture-browser-composition); no generated activity or implemented workflow support is claimed.
