# Spec Revision R2 Evidence

- Skill: `spec`
- Artifact: `specs/plan-skill-simplification.md`
- Reason: `plan-review` preflight exposed `BFR-EXAMPLE-OWNER-MISMATCH` errors in the example ownership table
- Change: each example now cites only requirements governed by every boundary ID it names and removes unrelated boundary citations
- Semantic effect: none; requirements, boundary definitions, interactions, examples, and observable outcomes are unchanged
- Expected remaining boundary result before test-spec authoring: `BFR-PROOF-MAP-MISSING` only
- Authoring result: `review-required`
- Next stage: `spec-review`
