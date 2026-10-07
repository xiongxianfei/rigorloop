# REM guidance composition

Owner: [Engineering authoring](design-authoring.md).
This supporting design defines the portable guidance composition; it creates no new Module, Interface, public skill or runtime record format.

## Scope and authority

Use the existing REM semantics with three selected improvements: focused knowledge documents and Practices/examples/sources; explicit verification and intended-use validation methods; and concern-based architecture-view tailoring.
Document splitting preserves requirement parentage, Scenario ownership, seven-question analysis, bounded open questions, Function coverage, accountable allocation, subordinate realization and evidence applicability.
The canonical REM method metadata owns its edition and explicitly selected KPS basis. A based-on relationship identifies the knowledge foundation; it does not assert KPS conformance, product release or completed source inspection. Imported reconstruction metadata, alternative profiles and release/check claims gain no authority merely by being copied into the tree. Document identities and source-specific publication/inspection provenance remain separate from the method edition.

## Logical behavior and ownership

FUNC-032/033 continue to identify applicable guidance and guide bounded authoring; FUNC-034 supplies assessment intent rather than a claim that new examples have been empirically validated.
MOD-008 owns canonical guidance interpretation; MOD-012 owns specialist invocation procedures; MOD-013 projects selected versioned resources into distributions.
MOD-007 retains independent review and final Verify authority.
The new REM assessment methods explain engineering assessment and do not add or replace RigorLoop workflow gates.
No Function/AR allocation or Interface changes are required for this document composition.

## Knowledge and reading paths

Concept documents own meanings. Eleven Principles explain deeper engineering relationships and why they matter, with assumptions, limits, examples and claim-specific sources. Models own selected structures and invariants; Methods own individual procedures; Operational Support owns cross-entity authoring guidance.
The former 22 principle commitments remain applicable under those owners. Explanatory relationships do not uniquely entail REM's selected cardinalities, authority rules or workflow, and adopting this catalog does not relax them.
Each new principle has a distinct named identity. A concise migration map identifies the recoverable original identities and current semantic owners; current consumers refer directly to those owners. Git retains retired documents, without live compatibility shims.
Practices coordinate those owners into goal-oriented work with locally usable stage summaries, procedures, explanations, examples, checks and fallback actions. Concise inline summaries apply the current Model and Method rules; the owning definitions remain authoritative. Preserve the five operating routes: engineer a change, review an existing system, verify and validate a bounded slice, make an architecture decision, and improve REM through actual use. Supporting knowledge guides and worked examples supply depth without replacing executable stages.
Current requirement parentage, Scenario ownership, Function coverage and allocation rules apply within those stages. Rule changes require explicit revision at their governing owner; an imported methodology-only or deferred-specification label cannot suspend existing rules.
Indexes provide navigation rather than duplicate normative definitions.
One rich reference document per publication lives under `rem/references/`; chapter-specific contributions remain precise sections of that publication. `rem/SOURCES.md` preserves the existing source identifiers as claim-to-section navigation. References inherit the canonical REM method metadata, while retaining their own bibliographic identity, inspection dates, inspected passages and limits. Incoming inspection reports stay attributed until actually checked; source metadata does not establish approval or conformance. Source contributions support exact claims and do not suspend current Model or Method rules. Reconciliation updates live consumers and generated citations before retiring duplicate source notes.
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

Check every retired principle's commitments, rationale and application details against surviving owners, including clear definitions and public-entry traceability. Check protected invariants, direct links and anchors, projection freshness and actual isolated adapter resources.
Source notes distinguish inspected external support, REM-authored inference and illustrative examples; a citation or proposed-package review label does not establish approval or empirical effectiveness.
Walk through one example with one parent IR per SR, one parent SR per AR, one owning IR and primary Feature per Scenario, relevant Functions and accountable Modules.
Inspect negative cases: unrun/stale evidence, unsupported intended-use claims and view omission hiding a material concern.
Independent review judges semantic preservation and usefulness; structural checks alone cannot demonstrate observed stakeholder effectiveness.
