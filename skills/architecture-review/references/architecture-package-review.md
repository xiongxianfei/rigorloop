# Architecture package review method

Use after the universal skill selects `canonical-architecture-update` or `ADR`. This method does not decide applicability, status, materiality, recording, settlement, or routing.

## Canonical package and arc42

Review the exact changed canonical architecture Markdown, linked diagram sources, related ADRs, governing specification, and legacy status as one package. Confirm current architecture truth has one canonical owner.

Check all 12 official arc42 sections for coherent current content. Pay particular attention to goals and constraints; context, solution strategy, and building blocks; Runtime View failure and recovery flows; Deployment View packaging, adapters, distribution, and environments; Crosscutting Concepts such as validation, security, portability, and observability; concise Architecture Decisions links; measurable Quality Requirements; material risks and debt; and ambiguous glossary terms.

## C4 and diagrams

Require reviewable context and container sources when those levels explain the change; require component or deployment views only when important responsibilities remain unclear. Check that people, the system, external systems, containers, technologies, responsibilities, and labeled relationships appear at the correct C4 level. Applicable Mermaid diagrams retain the project’s C4 role classes and one authored source rather than embedded or duplicated source.

## Building blocks and quality

Reject a Building Block View that is only a folder catalog for multi-responsibility architecture. Check ownership, interfaces, data boundaries, failures, migration, compatibility, security, operability, performance, and recovery. Quality scenarios identify stimulus, environment, response, and measure. Deployment content explains execution rather than repeating source layout.

## ADR quality

Review ADR ownership, context, decision, materially different alternatives, consequences, canonical compatibility, and follow-up. The ADR records a durable decision rather than duplicating current structure. For replacement or supersession, verify predecessor and replacement links, status intent, and canonical references; review approves the exact intended `accepted` or `active` state.

## Package consistency

Challenge silent failure, hidden coupling, irreversible migration, compatibility, trust boundaries, ownership, and bad integration assumptions. Confirm links resolve and canonical Markdown references no missing diagram or ADR. Record findings against exact paths, sections, lines, diagrams, or ADR IDs.
