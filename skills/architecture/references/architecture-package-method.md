# Architecture package method

Load for portable or governed authoring. The parent skill owns applicability, routing, safety, claims, and handoff.

## Placement and surface

Resolve paths from target identity, metadata, workflow guidance, then defaults: `docs/architecture/system/architecture.md`, `diagrams/`, and `docs/adr/`. Conflict stops.

Update the canonical package directly and only affected arc42 sections or C4 views. Change-local architecture remains history, not a competing source.

## arc42 method

Use `architecture-skeleton.md` for the owning-change pointer and all 12 official arc42 sections. Keep headings, justify `Not applicable`, and exclude mutable state.

Cover goals, constraints, context, strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality scenarios, risks, and glossary. Runtime owns behavior and failures; Deployment owns packaging and environments; Crosscutting Concepts owns validation, security, portability, generation, caching, and observability. Architecture Decisions links ADRs or gives a no-ADR rationale.

## C4 and diagrams

Use separate Mermaid sources for system context and container views with relative links. Add component or deployment views only when the lower detail is necessary.

Update the lowest affected C4 level first. Keep diagrams focused and text-authored; images or external links are never sole truth. Flowcharts copy `diagram-styles.mmd` or equivalent styles.

Within one canonical target, prepare all Markdown and diagrams together, write subordinate diagram sources before canonical Markdown, validate relative links, and treat canonical Markdown as the target commit point.

## ADRs

Use an ADR for a durable system boundary, packaging or adapter rule, validation architecture, cache or indexing strategy, portability constraint, release architecture, security boundary, or major workflow architecture decision. Use `adr-skeleton.md`; record context, decision, meaningful alternatives, consequences, and follow-up.

ADRs are history. Author replacement and supersession/deprecation links instead of rewriting old decisions; all remain unapproved until architecture-review.

## Quality and completion

Map requirements to choices and expose tradeoffs, quality, deployment, security, compatibility, risk, and recovery. Exclude behavior absent from the spec and plan sequencing.

Remove all copied placeholders. Report changed arc42 sections, diagram paths, ADR paths, unaffected surfaces with rationale, and a truthful architecture-review handoff or blocker.
