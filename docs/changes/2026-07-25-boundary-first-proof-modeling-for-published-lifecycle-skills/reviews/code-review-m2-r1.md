# Boundary-First Proof Modeling M2 Code Review R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill with context-separated independent reviewer
Target: commit range 450bb65f..093a0677
Reviewed artifact: M2 implementation commit range `450bb65f..093a0677`
Reviewed milestone: M2
Status: changes-requested
Review status: changes-requested
Material findings: BFP-CR-M2-1, BFP-CR-M2-2, BFP-CR-M2-3, BFP-CR-M2-4, BFP-CR-M2-5, BFP-CR-M2-6
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

## Findings

### BFP-CR-M2-1 - Fresh workflow evidence is synthesized

Finding ID: BFP-CR-M2-1
Severity: blocker

The child returns profile labels, after which the harness injects the feature
and proof records, renders both authored artifacts, and fabricates approved
review records and events. The stage-owning skills do not produce the recorded
artifacts or independent formal reviews.

Required outcome: Capture actual stage-owned authoring and independent review
outputs from the isolated workflow. The harness may validate, snapshot, and
publish them, but may not author or approve them.

### BFP-CR-M2-2 - Invocation-profile literals contradict the spec

Finding ID: BFP-CR-M2-2
Severity: blocker

The implementation uses four profile values that differ from the exact R28y
literals, and its validator repeats those incorrect values.

Required outcome: Use the exact approved orchestration, instruction, tool, and
Python implementation literals and regenerate all transitive evidence.

### BFP-CR-M2-3 - Artifact inventories are curated, not complete

Finding ID: BFP-CR-M2-3
Severity: blocker

Generation does not require a clean pre-run HEAD. The before inventory is
empty and the after inventory contains only produced snapshots, so the zero
new-universal-artifact metric is not derived from the required closed
repository selector.

Required outcome: Require a clean baseline and implement the complete closed
before/after artifact classifier.

### BFP-CR-M2-4 - Publication has an unrecoverable crash window

Finding ID: BFP-CR-M2-4
Severity: blocker

The run is installed before the prepared receipt exists, concurrent publishers
are not serialized, and no direct crash/recovery test exercises the publisher
or reconciler.

Required outcome: Establish exclusive durable recovery authority before the
first irreversible installation and prove every T51 interruption state.

### BFP-CR-M2-5 - Credential-isolation pass results exceed direct proof

Finding ID: BFP-CR-M2-5
Severity: blocker

The attestation asserts argv, stdin, PATH, and process-metadata isolation that
the probes do not fully establish.

Required outcome: Derive every credential-isolation pass from a direct probe,
close child PATH to the approved minimal value, and cover all proxy contrasts.

### BFP-CR-M2-6 - Plan state is contradictory

Finding ID: BFP-CR-M2-6
Severity: major

The handoff summary and M2 body disagree, and neither records the required
post-review `resolution-needed` state.

Required outcome: Synchronize the plan body, handoff summary, index, and review
status before correction.

## Review result

M2 is not closed. The six findings require recorded resolution, implementation
correction, regenerated evidence, and same-milestone rereview. M3 remains
blocked.
