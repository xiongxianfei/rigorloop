# Review Resolution: Project-Map Skill Simplification

## Summary

Closeout status: open

Review closeout: proposal-review-r1

- Reviews covered: `proposal-review-r1`
- Findings resolved: 0
- Unresolved findings: 3
- Current result: proposal revision required

## Resolution overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| `PMAPSIM-PR1` | needs-decision | open | Proposal author must close reference loading and write boundaries for discovered map coordination. |
| `PMAPSIM-PR2` | needs-decision | open | Proposal author must keep universal dirty-baseline truthfulness available to every profile. |
| `PMAPSIM-PR3` | needs-decision | open | Proposal author must define the new result vocabulary and legacy mode migration. |

## Finding details

### proposal-review-r1

#### PMAPSIM-PR1

Finding ID: PMAPSIM-PR1
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Close reference loading when root creation discovers multi-map coordination and define every operation's allowed write set.
Chosen action: pending proposal revision
Rationale: Root creation can encounter procedure owned only by a reference that its declared profile does not load.
Required outcome: Add an evidence-based coordination predicate, late-load behavior, explicit write boundaries, and interruption handling.
Safe resolution path: Adopt `map_coordination_context` and the operation-specific boundaries recommended by `proposal-review-r1`.
Validation target: revised classification, resource ownership, expected behavior, scenarios, risks, rollout, and acceptance criteria plus independent proposal rereview.
Validation evidence: pending

#### PMAPSIM-PR2

Finding ID: PMAPSIM-PR2
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Separate universal dirty-baseline truthfulness from maintenance-specific comparison.
Chosen action: pending proposal revision
Rationale: Root creation must describe inspected uncommitted evidence even when the maintenance reference is not loaded.
Required outcome: Keep the complete minimum baseline-reporting contract inline and move only maintenance comparison to the reference.
Safe resolution path: Adopt the ownership split recommended by `proposal-review-r1` and prove it for all profiles.
Validation target: revised ownership, scenarios, rule ledger, risks, and acceptance criteria plus independent proposal rereview.
Validation evidence: pending

#### PMAPSIM-PR3

Finding ID: PMAPSIM-PR3
Disposition: needs-decision
Status: open
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: Select the exact operation/scope result contract and compatibility migration.
Chosen action: pending proposal revision
Rationale: The current `Mode` literal is a published and validator-consumed contract, while the proposal selects a different classification without closing its emitted shape.
Required outcome: Define exact new fields, legacy mappings, ambiguity stops, and literal-consumer migration.
Safe resolution path: Adopt `Operation` and `Map scope` as the write-new result contract and migrate real consumers atomically as recommended by `proposal-review-r1`.
Validation target: revised expected behavior, compatibility, testing, rollout, and acceptance criteria plus independent proposal rereview.
Validation evidence: pending

