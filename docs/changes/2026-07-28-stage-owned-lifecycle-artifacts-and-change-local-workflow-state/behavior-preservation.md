# Behavior Preservation

## Published behavior matrix

| Surface | Preserved behavior | Revised behavior | Evidence |
| --- | --- | --- | --- |
| Proposal/spec/architecture/plan/test-spec authoring | Stage authors its own durable content | Mutable settlement moves to matching change-local entry | M1 semantic matrix |
| Formal peer review | Independent evidence and closed outcomes | Review settles only the matching artifact entry | M1 focused tests |
| Downstream execution and review | Reports upstream gaps instead of inventing contract | Upstream content and state are explicitly read-only | M1 focused tests |
| Workflow automation | One selected target and bounded repository-local continuation | Routing state is change-local and evidence-derived | M2 scenarios |
| Historical changes | Readable without forced migration | First resumed nonterminal mutation migrates once | M4 migration matrix |
| Status/off | Status is read-only; off preserves evidence | No capability or selector lookup | M2 and M4 tests |
| Verify/PR boundary | Verify proves readiness; PR remains separately invoked | Verify success completes target before PR | M2 scenarios |
| Generated adapters | Generated from canonical skills | Stage ownership and route-back text remain aligned | Adapter distribution suite |
| External actions | No implicit push, PR, publish, release, deploy, merge, credential, or destructive Git action | unchanged | Workflow contract and broad smoke |

## Boundary-first proof summary

All eight approved boundaries and seven selected interactions map to the
approved T1-T26 proof cases. Focused tests cover stage ownership, metadata
shape, state transitions, migration, recovery, and target containment.
Canonical build and adapter distribution cover generated surfaces. Broad
smoke is the cross-boundary integration gate.

Before M6, no tracked change record contains the
`stage-owned-change-local-v1` activation marker.
