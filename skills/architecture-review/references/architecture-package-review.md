# Architecture package review method

Use this reviewer-focused method only after the universal skill selects `canonical-architecture-update` or `ADR`. It specializes the approved architecture method; it does not decide applicability, semantic status, materiality, recording, settlement, or routing.

## Canonical package

Review the exact changed canonical Markdown, linked diagram sources, related ADRs, and governing specification as one package. Confirm current architecture truth has one canonical owner and that legacy documents are not implied to be normalized without explicit evidence.

Check arc42 completeness and coherence across all 12 official sections. Require useful current content in Introduction and Goals, Architecture Constraints, Context and Scope, Solution Strategy, and Building Block View. Review Runtime View for orchestration, failure, retry, command, and generated-output flows; Deployment View for environments, packaging, adapters, distribution, and release boundaries; Crosscutting Concepts for validation, security, caching, portability, generation, and observability; Architecture Decisions for concise ADR links; Quality Requirements for measurable quality scenarios; Risks and Technical Debt for material residual risk; and Glossary for ambiguous domain terms.

## C4 and diagrams

Require reviewable source text for context and container views when those levels explain the change. Add component or deployment views only when important internal responsibilities or execution boundaries remain unclear.

Check that context diagrams distinguish people, the system under review, and external systems; container diagrams show relevant technologies and responsibilities; relationships are labeled; and the chosen C4 level does not mix container, component, runtime, or dependency semantics without explanation. For Mermaid flowcharts or graphs, require the project’s applicable C4 role classes. Keep one authored diagram source rather than embedding or duplicating it in canonical Markdown.

## Building blocks and quality

Reject a Building Block View that is only a folder catalog when multiple responsibilities or containers are involved. Test whether ownership, interfaces, data boundaries, failure modes, migrations, compatibility, security, observability, performance, scalability, and recovery are explicit enough to plan and verify.

Quality scenarios should identify stimulus, environment, response, and measure. Deployment content should explain real packaging and execution boundaries rather than repeat source layout. Diagrams support decisions; they do not substitute for them.

## ADR quality

For each ADR, review stable ownership, context, the decision, materially different alternatives, consequences, compatibility with canonical architecture, and follow-up. Confirm the ADR records a durable decision rather than duplicating current structure that belongs in the canonical package.

For replacement or supersession, verify predecessor and replacement links, status intent, and canonical references are coherent. Architecture authoring may propose ADR status changes, but architecture review owns approval of the exact intended `accepted` or `active` settlement state.

## Package consistency and failure prompts

Challenge silent failure, hidden coupling, irreversible migration, old-client and old-data compatibility, trust boundaries, operational ownership, bad integration assumptions, and decisions that would be unrecoverable without an ADR. Confirm links resolve and that canonical Markdown does not reference missing diagrams or ADRs.

Record findings against exact paths, sections, lines, diagram names, or ADR IDs. Do not restate universal status, recording, settlement, or handoff policy here.
