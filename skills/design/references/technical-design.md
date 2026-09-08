# Technical realization and credible claims

Use architecture reasoning inside the owning Design. Cover relevant goals/constraints, context, solution strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality scenarios, risks and glossary. These arc42 concerns improve reasoning; they do not impose a second file or twelve empty headings. State bounded reasons for material non-applicability.

## Structure and flows

Choose the lowest detail that explains the responsibility and its relationships. C4 context shows users and external systems; container views show significant executable/data responsibilities and dependencies; component views explain a necessary internal partition; deployment views show mapping to environments and nodes. A container is a runtime/deployment responsibility, not automatically a Docker container. Code-level views are optional. Do not invent services, databases or layers for a documentation or CLI system.

Explain responsibility, inputs/outputs, significant dependencies and trust boundaries. Use runtime scenarios for normal operations, failures, recovery and cross-owner interactions; deployment reasoning covers packaging, installation, distribution, environment assumptions and compatibility when relevant. Cross-cutting concerns include validation, security, privacy, portability, generation, caching and observability as applicable.

Update the lowest affected view and reconcile relevant enclosing relationships. Use focused reviewable text or Mermaid when a visual clarifies them; preserve one source with valid relative links and meaningful labels. A diagram does not replace observable requirements. Prepare related text and diagram changes coherently and check their references before handoff.

## Choices and assessment

Trace important requirements to realization choices and expose constraints, alternatives and consequences. Behavioral and technical reasoning inform each other; a material approved-direction change returns to its owner. A small/no-impact correction may need a documented no-change disposition rather than an invented architecture artifact.

A quality scenario names the relevant condition, expected response and observation boundary. Give metrics only where justified; do not fabricate measurements. Assess uncertain material feasibility with targeted evidence, a walkthrough, counterexample, investigation or prototype as needed. Neither a prototype nor formal proof is mandatory for every Design. Record assumptions and residual risks without calling structural validity approval.

Embed important stable decisions in the owning model. For an unmigrated architecture/ADR source, use the separately triggered legacy procedure instead of silently imposing model packaging. Never make temporary change-local truth compete with a current owner.
