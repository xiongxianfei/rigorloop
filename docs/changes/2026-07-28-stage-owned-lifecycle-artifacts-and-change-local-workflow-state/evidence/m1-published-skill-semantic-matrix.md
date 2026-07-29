# M1 Published-Skill Semantic Review

Stage: implement
Milestone: M1
Result: passed

## Inventory and perspectives

| Surface | Writable output | Read-only boundary | Independent invocation | Route-back result |
| --- | --- | --- | --- | --- |
| proposal/spec/architecture/plan/test-spec | Matching governed artifact, authoring evidence, matching entry only | Other artifacts, review settlement, workflow routing | Authors content but never approve it | Requests matching peer review |
| proposal-review/spec-review/architecture-review/plan-review/test-spec-review | Own review evidence and matching settlement entry only | Reviewed content, other entries, workflow routing | Records settlement and stops | Returns findings to matching author |
| implement/code-review/explain-change/verify/learn/pr | Stage-owned implementation or evidence only | Governed artifacts, artifact settlement, workflow routing | Does not manufacture upstream completion | Records the defect or blocker and routes to its owner |
| Governed artifact assets | Stable intent and owning-change pointer | Mutable state, current milestone, blocker, review, next stage | Usable without workflow automation | Change-local metadata owns live state |

## Adversarial perspectives

- Ownership: no changed downstream skill instructs a write to an upstream
  governed artifact or another stage's state.
- Peer separation: authoring and matching review remain peers; neither
  combines content revision and settlement in one stage.
- Recovery: downstream discoveries become stage-owned evidence and a
  route-back, not silent repair.
- Portability: published text explains user-visible ownership without
  repository-maintainer implementation detail.
- Ambiguity: uncertain ownership stops at the matching owner rather than
  selecting a writer heuristically.

Generated adapter parity is deliberately deferred to M5.
