# Boundary-First Proof Modeling Spec Review R41

Review ID: spec-review-r41
Stage: spec-review
Round: 41
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: focused workspace-integrity candidate at b4daa372, including 4646e808
Reviewed artifact: specs/rigorloop-workflow.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR41-1, BFP-SR41-2, BFP-SR41-3
Immediate next stage: spec
Architecture assessment: architecture-required
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed spec identity: `sha256:afd2b510154bab406340bf0f799ca1ac4eee1f553daaf682cc19a3fc11baf36a`

## Result

The candidate correctly closes complete-but-fail-closed identity and evidence
handling, but the mutation proof is not yet safe or total. It does not prove
that shell-spawned descendants are unable to write during scanning and
materialization, cannot represent unstable or failed filesystem inspection,
and has no numeric work/evidence bounds or privacy-safe representation for
unexpected child-authored paths.

## Material findings

### BFP-SR41-1 — Terminal turn state does not prove writer quiescence

Finding ID: BFP-SR41-1

Severity: blocking

Location: `specs/rigorloop-workflow.md`, transport termination and completed
quiescence contract; accepted permission-profile ADR

Evidence:

Terminal turn/tool-call state and reaping the identified app-server process do
not prove that a permitted shell command left no background or detached
descendant. Such a writer can race post-turn scan or adapter materialization.
The accepted permission profile permits sandboxed commands and file changes in
the isolated workspace.

Required outcome:

Establish an observable boundary in which neither the runtime nor any process
or writer created through child authority can mutate the workspace before scan
or materialization.

Safe resolution:

Prefer a stage-turn permission profile that independently proves workspace read
success and write denial for commands, file-change events, and descendants,
while keeping parent materialization outside child authority. Otherwise close
or terminate a complete enumerable sandbox execution boundary and prove all
writers stopped. Apply the same rule to the canary. Failure to prove the
boundary is environment-unavailable or liveness-uncertain with no scan,
materialization, or retry.

### BFP-SR41-2 — Workspace scanning lacks closed race-safe failure behavior

Finding ID: BFP-SR41-2

Severity: blocking

Location: `specs/rigorloop-workflow.md`, workspace integrity observation

Evidence:

The `complete`/`overflow` scan vocabulary cannot represent unreadable entries,
invalid path encoding, enumeration or `lstat` failure, replacement between
inspection and open, symlink substitution, failed reads, or filesystem
instability. Baseline symlink/non-regular rejection also lacks a named result
and route. A pathname-based `lstat` followed by ordinary open can follow a
replacement symlink.

Required outcome:

Make baseline capture and post-turn scanning total, race-resistant, and
exhaustively routed, with inspection inability distinct from confirmed
mutation.

Safe resolution:

Add a closed invalid/error scan state and reason vocabulary, deterministic
baseline failure, post-turn failure diagnostics, root-anchored no-follow open,
`fstat` agreement, descriptor hashing, stability verification, normalized path
encoding, and canary parity. Inspection failure must prohibit materialization
and retry.

### BFP-SR41-3 — Integrity work and evidence are unbounded and can persist child-authored path strings

Finding ID: BFP-SR41-3

Severity: major

Location: `specs/rigorloop-workflow.md`, workspace integrity observation,
diagnostic evidence, and RLW-AC-B10

Evidence:

The durable observation has no parent-owned entry, path-byte, aggregate-byte,
serialized-size, or scan-time limits. A relative `baseline + 1` growth bound
does not bound an already unbounded baseline, and deterministic sorting can
require enumerating attacker-expanded directories. Unexpected child-created
paths are persisted verbatim, contradicting the value-free/no-child-prose
claim.

Required outcome:

Bound scan work and durable evidence through immutable parent-owned limits and
prevent unexpected child-authored filenames from entering durable evidence.

Safe resolution:

Bind positive limits for baseline and encountered entries, per-path and
aggregate path bytes, serialized observation bytes, and scan duration. Stop at
the first deterministic limit. Persist trusted baseline paths only; represent
unexpected paths by identity, byte/component counts, and safe structural
classification. Keep raw unexpected paths transient. Give the canary separate,
smaller bound values.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Requirement clarity | block |
| Normative language | block |
| Completeness | block |
| Testability | block |
| Compatibility | pass |
| Observability | block |
| Security and privacy | block |
| Non-goals | pass |
| Acceptance criteria | block |

## Readiness

Not ready for architecture or test-spec reliance. Resolve BFP-SR41-1 through
BFP-SR41-3 and obtain an approved spec rereview.
