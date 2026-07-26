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
  path-and-SHA-256 evidence; not-run rows require a closed blocker.
- `BFP-M1-CR5`: equivalent mappings serialize to canonical bytes.
- `BFP-M1-CR6`: all eight incidents are executable boundary-state envelopes
  evaluated independently of fixture labels.
- `BFP-M1-CR7`: simple-change counts are derived from a closed four-stage
  synthetic trace and artifact inventories.

## Contract boundary

M1 implements deterministic structure, vocabulary, traceability, fixture, and
aggregate proof only. Semantic applicability, partition quality, interaction
sufficiency, reviewer reasoning, public skill behavior, selector routing,
adapter parity, activation, and the canonical M4 report remain outside this
milestone.
