# Boundary-First Proof Modeling Spec Review R32

Review ID: spec-review-r32
Stage: spec-review
Round: 32
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R31 resolution candidate at e03ff747
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R32-1, BFP-SR-R32-2, BFP-SR-R32-3, BFP-SR-R32-4
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:728b5252fd81560232058473260a50f62f8f6d580706ed640fe8468e1a4e7387`

Reviewed test-spec identity: `sha256:7b8fb2a115733b9cbe401320d3f3bb48940a30902e6f1d56924816f912558a0d`

Reviewed plan identity: `sha256:9908925fb7c5d4d384a76da62cb7a0518665fd5bfd724bc83fd1c8d28ac1f0fe`

## Findings

### BFP-SR-R32-1 - Unknown protocol events lack evidence

Finding ID: BFP-SR-R32-1
Severity: blocking
Location: R28y diagnostic vocabulary/evidence and T52
Evidence: An unknown event may have no bound schema and cannot truthfully use
the schema-incompatibility evidence shape.
Required outcome: Add a closed classification-invalid diagnostic with exact
unknown-lookup evidence and non-output routing.
Safe resolution: Add `protocol-item-classification-invalid` with the bound
classification identity, unknown lookup result, and event-shape identity.

### BFP-SR-R32-2 - Output duplicate detection conflicts with set normalization

Finding ID: BFP-SR-R32-2
Severity: major
Location: R28y output evaluator and T52
Evidence: Set normalization can erase duplicates, empty required output
overlaps absent/complete, and mixed missing-plus-extra output is not classified.
Required outcome: Preserve raw lists, require nonempty unique requirements,
classify every duplicate and mixed observation deterministically, and test all
contrasts.
Safe resolution: Validate required-list uniqueness before invocation and use a
disjoint contradiction-first list comparison.

### BFP-SR-R32-3 - Temporary recovery basis can become permanently malformed

Finding ID: BFP-SR-R32-3
Severity: blocking
Location: R28y recovery-basis installation and T51
Evidence: A crash during direct temporary-file write can leave a malformed
discoverable file with no authorized cleanup route.
Required outcome: Use an unpublished temporary object or add locked,
lease/basis-bound discard, fsync, and reconstruction for malformed
noncanonical temp state.
Safe resolution: Under the global lock, discard only a deterministically named
malformed temp after validating canonical/lease/orphan context, fsync, and
reconstruct; never discard canonical basis.

### BFP-SR-R32-4 - Publisher lock pollutes artifact inventories

Finding ID: BFP-SR-R32-4
Severity: blocking
Location: R28y inventory selector and T51/T52
Evidence: Persistent `publisher.lock` is outside transient discovery and is not
explicitly excluded from before/after inventories.
Required outcome: Exclude the exact lock path while validating it separately
and prove lock persistence does not change counts or canonical evidence.
Safe resolution: Add an exact selector exclusion and focused count/parity
fixtures.

## Review result

The spec remains blocked until R32-1 through R32-4 are resolved and
independently rereviewed.
