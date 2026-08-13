# Architecture Assessment R1: Plan-Review Skill Simplification

Assessment date: 2026-08-13
Result: blocked-on-spec-correction
Owner: workflow
Change: `2026-08-13-plan-review-skill-simplification`
Finding ID: PLRSIM-ARCH-001

The proposed package split reuses the existing published-skill resource-integrity architecture, and the reviewed-plan operation otherwise reuses `ADR-20260813-reviewed-plan-initialization-and-settlement.md`. The approved specification's glossary defines the plan tuple with a “plan content identity,” however, while the ADR and `specs/plan-skill-simplification.md` define stable artifact identity as artifact ID, kind, role, and normalized path plus durable review identity and explicitly forbid a governed-document hash or `content_identity` field.

Required outcome: the specification must use the existing stable artifact and reviewed-revision identities and explicitly preserve the no-hash, no-`content_identity` architecture before architecture applicability can be settled.

Safe correction: revise only the identity wording and corresponding requirement, preserve every transaction outcome and authority boundary, then run a fresh formal `spec-review`. This correction introduces no product choice or new architecture decision.
