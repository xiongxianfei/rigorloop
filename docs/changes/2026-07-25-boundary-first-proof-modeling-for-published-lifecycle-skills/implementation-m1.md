# M1 Implementation Diff Evidence

Stage: implement
Milestone: M1
Status: review-requested

## Implemented surfaces

- `scripts/boundary_proof_model.py`
- `scripts/validate-boundary-proof.py`
- `scripts/test-boundary-proof.py`
- `tests/fixtures/boundary-proof/incident-registry.json`
- `tests/fixtures/boundary-proof/incidents/*.json`
- `tests/fixtures/boundary-proof/simple-change.json`

## Review-finding corrections

- `BFP-M1-CR1`: stable unique regression/discovery IDs and per-reference
  requirement ownership now fail closed.
- `BFP-M1-CR2`: one immutable registry binds each exact fixture ID to its
  omission, trigger, contrast, gate, and diagnostic.
- `BFP-M1-CR3`: marker presence and scope presence are symmetric for explicit
  legacy and v1 pairs; only the fully markerless legacy pair is grandfathered.
- `BFP-M1-CR4`: executed rows require current repository-relative
  path-and-SHA-256 evidence whose path is tracked or belongs to this change
  root; unsafe, untracked non-change-local, and symlink-ancestor references
  fail closed. Not-run rows require a closed blocker.
- `BFP-M1-CR5`: equivalent mappings serialize to canonical bytes.
- `BFP-M1-CR6`: all eight incidents are executable boundary-state envelopes
  evaluated independently of fixture labels.
- `BFP-M1-CR7`: simple-change observations are derived from exact
  identity-bearing snapshots, formal-review bundles, nine-field events,
  evidence unions, terminal branches, final-approved feature/proof models,
  and three-field artifact inventories. Universal-artifact subtraction uses
  only trace-produced outputs and review-bundle members.

## Contract boundary

M1 implements deterministic structure, vocabulary, traceability, fixture, and
aggregate proof only. Semantic applicability, partition quality, interaction
sufficiency, reviewer reasoning, public skill behavior, selector routing,
adapter parity, activation, and the canonical M4 report remain outside this
milestone.
