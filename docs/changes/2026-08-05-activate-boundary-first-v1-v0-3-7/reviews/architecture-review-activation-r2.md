# Architecture Review: Boundary Activation Release R2

Review ID: architecture-review-activation-r2
Stage: architecture-review
Round: 2
Reviewer: independent Codex architecture-review peer
Target: canonical architecture package and activation-publication ADR
Reviewed commit: `419797397d7fad0c53c0599958938295a54fda78`
Review surfaces: canonical-architecture-update and ADR
Status: changes-requested
Material findings: BFA-AR2-001
Automatic downstream handoff: none

## Result

- Review status: changes-requested
- Recording status: recorded
- Recording blocker: none
- Open blocker: BFA-AR2-001
- Required ADR updates: none
- Required canonical updates: focused component diagram and Architecture Decisions summary
- Next stage: architecture revision, then architecture-review R3

The amended ADR is sound: `R -> C ... H` is non-circular, candidate evidence
does not become a new mutable state owner, publication readiness owns fresh
`H`, and the publisher consumes that exact SHA. The canonical package still
contains two superseded descriptions.

## Material Finding

### Finding BFA-AR2-001

Finding ID: BFA-AR2-001
Severity: material
Location: `docs/architecture/system/diagrams/component-boundary-guidance.mmd`; Architecture Decisions summary in `docs/architecture/system/architecture.md`
Evidence: The component diagram still labels candidate validation as direct
`P/B/T/H` proof and shows neither immediate evidence commit `C` nor publication
readiness deriving and passing exact `H`. The Architecture Decisions summary
still calls the model four Git identities. Both contradict BFA-R017 through
BFA-R020 and the amended ADR.
Required outcome: Consistently show candidate `P/B/T/R`, immediate `R -> C`
provenance, live-`H` readiness, strict `H`, detached `T`, and exact
readiness-to-publisher SHA binding.
Safe resolution path: Update the focused component diagram and Architecture
Decisions summary, correct the duplicated conjunction in the responsibility
list, and preserve the no-new-manifest/state-owner decision.
needs-decision rationale: none; the settled spec and ADR determine the model.

## Review Dimensions

| Dimension | Verdict |
| --- | --- |
| Spec alignment | block |
| Package shape | concern |
| Boundary clarity | block |
| Data ownership | concern |
| Interface safety | pass |
| Runtime and failure handling | pass |
| Deployment and execution boundaries | pass |
| Security/privacy | pass |
| Quality and operations | pass |
| Testing feasibility | pass |
| Complexity discipline | pass |
| ADR quality | pass |
| Plan readiness | block |

## Validation Evidence

- `git diff --check e964ad63..41979739 -- <architecture> <ADR>` passed.
- Change metadata and explicit artifact-lifecycle validation passed.
- Explicit validation selection reported no unclassified paths or blockers.
- Markdown readability passed with baseline nonblocking warnings.

## Recommendation

Correct the two stale canonical projections and rereview; do not revise the ADR decision.
