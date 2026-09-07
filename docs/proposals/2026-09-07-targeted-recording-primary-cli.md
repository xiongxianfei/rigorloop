# Make Targeted Recording the Primary CLI Interface

**Status:** Draft for review

## Challenge

RigorLoop’s CLI will be a published tool used by developers and coding agents. Its normal interface should reduce repetitive bookkeeping, prevent accidental record corruption, and avoid making agents repeatedly read and reproduce unrelated content.

The supplied [CLI model draft](../design/cli.md) correctly separates workflow judgment from storage. However, its proposed interface requires complete replacement file contents, while inspection returns every registered record’s complete content. The [Workflow model draft](../design/workflow.md) separately requires callers to preserve neighboring actors’ entries. A small recording operation can therefore require a large read-and-rewrite interaction. This leaves mechanical work with the agent: reconstructing records, preserving unrelated entries, handling serialization, and reproducing information that has not changed.

Returning to CLI-owned readiness enforcement is not the solution. The [earlier proposal](2026-09-05-explicit-recording-and-model-centered-design.md) documents correction cycles in which workflow eligibility prevents recording the updates needed to resolve the problem.

The missing middle ground is **targeted, actor-specified recording**: agents supply the decisions and intended edits; the CLI constructs and safely persists the corresponding record changes.

This proposal refines the supplied, unapproved model designs. It does not assume their interfaces have already shipped.

## Goals

- Reduce accidental changes to unrelated records and the effort required to construct valid updates.
- Reduce agent context and output consumed by routine recording, while preserving sufficient information for responsible decisions.
- Provide one supported public interface that skills and humans can use without reconstructing complete files.
- Preserve correction availability, explicit decision ownership, structural validation, conflict detection, and recoverability.

## Scope and non-goals

**In scope:** Targeted recording and bounded inspection as the normal agent-facing interface; CLI construction of complete candidate records; concise human and machine results; and coordinated updates to the CLI and Workflow model designs, relevant skills, references, examples, validation, and supported adapter packages.

**Out of scope:** CLI-owned readiness, automatic stage selection, semantic approval, automatic applicability decisions, inferred correction ownership, new lifecycle stages, a new authentication system, arbitrary repository editing, or redesign of installation and release infrastructure.

Exact command names, request schemas, serialization rules, selection syntax, and persistence implementation remain Design decisions. Historical contracts must not be silently reinterpreted or migrated through this interface.

### Initial intent treatment

| Goal or concern | Treatment | Destination |
| --- | --- | --- |
| Reduce bookkeeping and accidental changes to unrelated content | in scope | Targeted updates and CLI candidate construction |
| Reduce context and output without weakening decision context | in scope | Bounded, sufficient inspection and concise results |
| Establish one supported normal public recording interface | in scope | Coordinated CLI, skill, documentation, validation, and adapter adoption |
| Preserve actor decisions and correction availability | in scope | Explicit ownership and separation of observations from structural rejection |
| Preserve storage safety and truthful historical identities | in scope | Shared validation, conflict detection, coherent persistence, and recovery obligations |
| Return to CLI-owned readiness enforcement | rejected option | Responsible actors retain workflow meaning and downstream reliance |
| Migrate historical contracts or redesign installation and release infrastructure | out of scope | Existing contracts and infrastructure retain their boundaries |

### Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Targeted recording, bounded inspection, and concise results | core to this proposal | Establishes the intended normal public interaction |
| Coordinated refinement of the CLI and Workflow models | same-slice dependency | Construction and actor ownership must agree across both designs |
| Preservation, validation, stale-write rejection, retry safety, and recovery | same-slice dependency | A smaller request must retain the declared storage protections |
| Relevant skills, references, examples, validation, and supported adapter packages | same-slice dependency | Adoption is incomplete if ordinary consumers still reconstruct full files or invoke eligibility gates |
| Complete-interaction token measurement | same-slice dependency | The expected benefit needs evidence without asserting an unmeasured saving |
| Exact commands, schemas, selectors, serialization, and persistence mechanisms | first-slice candidate | Design must settle these within the approved responsibility boundary |
| Historical migration, new lifecycle stages, authentication, and installation or release infrastructure redesign | out of scope | These require distinct decisions and are not prerequisites for this direction |

The scope budget identifies adoption dependencies, not implementation milestones. Delivery may sequence them into reviewable slices, but the primary interface is not adopted until its required consumers and safety obligations agree. This drafting step changes only this proposal; it neither revises the model designs nor activates their contract.

## Governing principle

> **Responsible actors supply workflow decisions; the CLI handles the mechanical work of reading, constructing, validating, and safely recording their explicitly requested updates.**

## Proposed direction

### Make targeted updates the normal interface

Routine skill invocations should identify the exact record or entry to change and supply the intended content or field values, rather than constructing complete replacement files.

Examples include recording a fully specified blocker, updating a named work item’s status and reason, recording an evidence result, or submitting a reviewer’s explicit judgment.

The CLI should construct the complete candidate records from a coherent, identity-checked snapshot, apply only the requested changes, and preserve unrelated entries and narrative content. Agents should not have to copy other actors’ records merely to leave them unchanged.

Mechanical construction does not authorize semantic completion. If an update lacks a required decision—such as a disposition, applicability value, owner, or rationale—the CLI should request that missing input rather than invent it.

Whether full-record submission remains available as a lower-level interface can be decided during Design. **Ordinary skills must not depend on full-file reconstruction.**

### Provide bounded, sufficient inspection

Skills should be able to retrieve the selected records or entries needed for an operation, together with their identities, snapshot revision, and relevant observations.

A bounded response must make its scope clear. An omitted record is not evidence that no blocker or concern exists. More detailed or complete inspection must remain available when the actor needs it.

This reduces unnecessary copying without transferring the decision about sufficient engineering context to the CLI. The skill remains responsible for examining the basis necessary for its judgment.

### Keep construction separate from workflow decisions

The responsibility boundary should be explicit:

| Responsible actor supplies | CLI handles |
| --- | --- |
| Intended stage, status, owner, judgment, disposition, applicability, and rationale | Structurally valid representation of the supplied values |
| Exact entry or record being changed | Target resolution and preservation of unrelated content |
| Decision basis and expected identities | Identity computation and freshness checks |
| Explicit related updates | Coherent candidate construction and safe persistence |
| Interpretation of observations and next action | Factual observations and a clear storage result |

Adding evidence must not automatically complete a milestone. Recording a review must not automatically change applicability or select the next stage. Matching a subject hash must not restore an approval.

A caller’s role label remains attribution, not authentication. Skills, independent review, and the surrounding execution authority retain their responsibilities.

### Preserve recording during correction

Workflow inconsistency must remain separate from structural invalidity.

The CLI may report a recorded completion alongside failed evidence, but must not reject an otherwise structurally sound update solely because the workflow is incomplete, contradictory, or associated with previously completed work. This preserves the boundary already specified by the explicit-recording draft.

For example, Verify can explicitly record failed evidence and a blocker. Route can subsequently record the correction activity. Neither operation should require the correction to have succeeded first, and all responsible actors need not submit their decisions simultaneously.

A successful write means **the requested records were saved**, not that the work is ready. Downstream reliance remains an actor responsibility; missing or contradictory required evidence still prevents justified progression under the Workflow contract.

### Preserve storage safety

Targeted updates must use the same structural validation, containment, conflict checks, coherent publication, and recovery protections as every other supported recording path.

The CLI must not silently apply an outdated decision to newer records. A stale expected revision or changed declared decision basis requires rereading and reassessment, not automatic merging.

Historical reviewed-subject identities must remain truthful. Constructing a candidate must never rewrite an old review to claim it assessed new content.

This proposal preserves the declared storage-safety boundary; it does not expand the draft’s guarantees for simultaneous edits by external tools.

### Make results useful without echoing whole records

Routine results should identify the storage outcome, affected records or entries, resulting identities, and actionable errors or observations. They should not echo complete record bodies unless explicitly requested.

Human and machine output must communicate the same outcome. Neither a successful save nor an absence of reported observations should imply engineering approval.

Skills should use the published interface to inspect the relevant basis, make their decisions, submit targeted updates, and handle the returned storage result. They should not retain a parallel normal path that assembles complete records manually or invokes an older eligibility engine before recording.

## Feasibility

**Assessment: Conceptually feasible; implementation safety and token benefits require validation.**

The supplied CLI design already separates decoding, structural validation, observation, and persistence. That provides a basis for adding deterministic candidate construction without adding semantic workflow authority. Existing transaction machinery is identified only as a reuse candidate, not verified support for the proposed contract. This is nevertheless an intentional interface revision. The draft currently requires caller-supplied exact bytes and prohibits serialization rewriting. Targeted construction must replace those requirements coherently rather than being introduced as an undocumented helper.

Design and Delivery should demonstrate that representative operations preserve unrelated content, avoid duplicated effects on retry, reject stale submissions, and retain the existing recovery outcomes. They should also demonstrate that a new blocker and correction can be recorded after completed work without satisfying a readiness gate.

The anticipated token benefit should be measured across complete interactions—including loaded skill guidance, inspection responses, update requests, and required follow-up reads. No numerical saving is established by the supplied materials.

No factual blocker to further Design is identified from the supplied drafts. Safe construction and sufficient bounded context remain unresolved Design obligations; the proposed benefits are not implementation evidence. This assessment relies on the linked model drafts and earlier proposal, without inferring repository architecture from a project map or asserting that existing code satisfies the direction.

## Impact and major trade-offs

**More CLI responsibility, less agent bookkeeping.** Candidate construction and bounded inspection add implementation work to the published CLI. In exchange, skills need less serialization procedure and fewer full-record read-and-rewrite interactions.

**Smaller responses, greater need for explicit scope.** Targeted inspection can reduce context, but an incomplete view must not look like a complete assessment. Actors must expand their reading when necessary.

**Mechanical reliability does not guarantee sound judgment.** A targeted update can faithfully record an incorrect decision. Independent review, evidence assessment, and responsible downstream reliance remain essential.

Because this changes a public interaction contract, the CLI, consuming skills, documentation, and compatibility behavior must be adopted together. A package rename or optional helper alone would not establish the intended normal path.

## Decision requested

Approve targeted, actor-specified updates and bounded inspection as the **primary published CLI interface for routine workflow recording**, with the CLI constructing safe complete replacements and preserving unrelated content.

Approve coordinated refinement of the CLI and Workflow designs and their consuming skills around that boundary, while retaining actor-owned workflow meaning, non-blocking correction recording, and the existing storage-safety obligations.

**Approval authorizes further Design and Delivery work. It does not approve exact commands, schemas, implementation mechanisms, a CLI-owned readiness gate, historical migration, or release activation.**
