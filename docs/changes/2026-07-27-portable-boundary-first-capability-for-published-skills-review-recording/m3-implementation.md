# M3 implementation evidence

## Result

- Milestone: PBF-M3
- Status: review-requested after R3 correction
- Scope: structural boundary records, proof maps, activation baseline, and
  validation selection
- Next stage: code-review M3

## Implementation

The new deterministic validator checks the closed boundary-first-v1 record
shape without claiming semantic completeness. It validates exact headings,
contiguous feature records, columns, dimension and proof vocabularies, ASCII
sentinels, identifier grammars and prefixes, feature-local references,
boundary ownership, proof coverage, and the distinction between covered rows
and blocking gaps.

Activation validation reads the repository-local JSON-compatible YAML record,
fails unknown contract, state, consumer, and field values before consistency
checks, and then checks the authoritative spec state, canonical and projection
identities, governed skill order, grandfathered inventory identity, historical
file bytes, and activation-time rules. Changed grandfathered specs route to
`spec-review`; the validator does not decide whether their edits are
substantive.

Validation selection now includes the boundary validator for affected specs,
governed skills and reference projections, adapter surfaces, activation state,
fixtures, and validator code. The boundary validation evidence class is
registered explicitly rather than relying on a broad YAML pattern.

## Test-first evidence

The first focused run failed because the boundary validation module did not
exist. The implemented suite now includes durable minimal,
semantic-omission, complete-proof, proof-gap, and activation fixtures plus
isolated mutations for each new closed vocabulary. The semantic-omission
fixture passes structural validation by design; semantic ownership remains
with the stage review skills.

Code-review M3 R1 found eight issues. The correction makes Markdown parsing
fence-aware, requires the contract marker after the lifecycle value in
`## Status`, validates exact separators and every proof reference/gap ID,
short-circuits malformed governing records, compares every projection with
canonical bytes, compares active historical inventory membership, shares the
feature activation gate with changed test specs, contains changed paths,
and redacts serialized offending values. The separately authorized
coordinator repair is committed as `197d150b`, so CMD8 no longer depends on
hidden worktree state.

Code-review M3 R2 found five additional issues. The second correction
preserves the immutable activation inventory when a historical contract later
adopts the marker, retains accepted marked artifacts through rollback,
contains explicit and derived companion paths before any read, accepts valid
CommonMark alignment separators, treats deletion as a changed contract
surface, and rejects symlinked historical inventory roots and entries.

Code-review M3 R3 confirmed those five corrections and found two remaining
fail-open paths. The final correction adds a closed rollback-preservation
path-and-byte inventory so a new self-declared accepted marker cannot adopt
after rollback. It also contains the fixed activation record and authoritative
proof-model spec before any read. The governing spec, test spec, architecture,
ADR, and pending activation record now describe the same rollback inventory.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-boundary-first-validation.py` | pass; 47 tests after R3 |
| `python scripts/validate-boundary-first.py --check` | pass; pending activation baseline |
| `python scripts/test-select-validation.py` | pass; 134 tests |
| `python -m py_compile scripts/boundary_first_validation.py scripts/validate-boundary-first.py scripts/test-boundary-first-validation.py` | pass |
| `git diff --check -- <M3 implementation paths>` | pass |

## Handoff

M3 is ready for independent code-review R4 against the approved proof-model
spec, test spec, architecture decision, plan, implementation diff, fixtures,
and bounded validation evidence. M4 remains blocked until M3 review closes.
