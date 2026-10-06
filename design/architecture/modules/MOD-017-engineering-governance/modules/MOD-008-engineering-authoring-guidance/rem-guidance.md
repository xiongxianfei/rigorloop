# REM guidance composition

Owner: [Engineering authoring](design-authoring.md).
This supporting design defines the portable guidance composition; it creates no new Module, Interface, public skill or runtime record format.

## Scope and authority

Use the existing REM semantics with three selected improvements: focused knowledge documents and Practices/examples/sources; explicit verification and intended-use validation methods; and concern-based architecture-view tailoring.
Document splitting preserves requirement parentage, Scenario ownership, seven-question analysis, bounded open questions, Function coverage, accountable allocation, subordinate realization and evidence applicability.
Imported reconstruction metadata, alternative profiles and release/check claims have no authority in this composition.

## Logical behavior and ownership

FUNC-032/033 continue to identify applicable guidance and guide bounded authoring; FUNC-034 supplies assessment intent rather than a claim that new examples have been empirically validated.
MOD-008 owns canonical guidance interpretation; MOD-012 owns specialist invocation procedures; MOD-013 projects selected versioned resources into distributions.
MOD-007 retains independent review and final Verify authority.
The new REM assessment methods explain engineering assessment and do not add or replace RigorLoop workflow gates.
No Function/AR allocation or Interface changes are required for this document composition.

## Knowledge and reading paths

Concept documents own meanings, Principles retain the existing 22 commitments, Models own structures and invariants, and Methods own individual procedures.
Practices link those owners into goal-oriented work, with inputs, iteration, exit conditions and examples.
Indexes provide navigation rather than duplicate normative definitions.
Source notes identify the exact external claim supported and distinguish REM's selected rules from external recommendations.
Examples are illustrative application records and keep plans, observations and judgments separate.

Split large architecture documents into cohesive boundary, allocation, realization and view concerns.
Preserve section meaning during relocation and resolve links directly to each new owner.
Current operation must not depend on retired files or private proposal archives.

## Assessment methods

Verification identifies an obligation and criteria, exact subject state, method, conditions, planned observations, actual observations, discrepancies, applicability and scoped judgment.
Intended-use validation identifies the stakeholder outcome and governed Scenario, representative participants/context, agreed success criteria, subject maturity, observed outcome, remaining uncertainty and corrective owner.
A product can meet specified criteria while intended-use success remains unestablished.
Unexecuted plans and fictional examples cannot establish either conclusion; a waiver is distinct from a passing result.
Projects select representations under existing Operational Support; these methods impose no schema or extra approval gate.

## Architecture-view selection

Retain Logical, Process, Development, Physical and Scenario as the standard concern vocabulary.
For each declared architecture scope, identify readers and questions, select useful views, and record the reason and coverage location for omission or combination.
Additional views require a named concern and authoritative sources; they create no new REM entity or authority.
Omitting a presentation cannot omit a material obligation, runtime/deployment concern, or a project-required view.
Retain source state, projection rules, provenance, semantic fidelity, reading-task assessment and maintenance rules.
Tailoring does not change current browser output contracts or remove generated browser views.

## Distribution and compatibility

Canonical authoring remains in `rem/` and `skills/`.
The existing projection script selects complete relevant methods and their needed local dependencies for each skill, rewrites packaged links, and removes obsolete generated REM resources from that skill's owned output set.
It must preserve unrelated resources and user-authored files.
Generated references retain canonical source identity and must work without the internal Design checkout.
Do not introduce network-dependent methodology lookups for required packaged reasoning.
Current repository consumers migrate together; historical records retain their original paths and meanings.

## Proof and limitations

Check transferred baseline sections, protected invariants, direct links and anchors, projection freshness and actual isolated adapter resources.
Walk through one example with one parent IR per SR, one parent SR per AR, one owning IR and primary Feature per Scenario, relevant Functions and accountable Modules.
Inspect negative cases: unrun/stale evidence, unsupported intended-use claims and view omission hiding a material concern.
Independent review judges semantic preservation and usefulness; structural checks alone cannot demonstrate observed stakeholder effectiveness.
