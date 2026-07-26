# Boundary-First Proof Modeling Spec Review R29

Review ID: spec-review-r29
Stage: spec-review
Round: 29
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: R28 resolution candidate at 9a5cbe2b
Reviewed artifact: `specs/rigorloop-workflow.md` and `specs/rigorloop-workflow.test.md`
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR-R29-1, BFP-SR-R29-2, BFP-SR-R29-3
Immediate next stage: spec revision
Architecture assessment: architecture-required-after-approval
Eventual test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent
Manifest owner: workflow orchestrator

Reviewed spec identity: `sha256:635fd6776f4237895e870990041b508148917431d0f563f92edd2e0822185d31`

Reviewed test-spec identity: `sha256:d87da1704f4d9671c52dc02e77cedb49f91049f61d620c2611c5128015bfcfaf`

Reviewed plan identity: `sha256:6da7d59c219a26807e83c650ceef09001f6b0feaaaca9885aac4e60b42aafc7f`

## Findings

### BFP-SR-R29-1 - Compound transport failures lack deterministic diagnostics

Finding ID: BFP-SR-R29-1
Severity: major
Location: `specs/rigorloop-workflow.md` R28y transport record and `specs/rigorloop-workflow.test.md` T52
Evidence: A transport row stores one diagnostic while output and protocol,
security, or runtime-identity failures can be observed together. The tuple
matrix does not define which condition owns routing or how all detected
conditions remain visible.
Required outcome: Define a closed diagnostic derivation order or a bounded
ordered diagnostic set with one primary routing diagnostic; cover compound
conditions while preserving output state independently; clarify prospective
event identity; and add compound cases to T52.
Safe resolution: Add `diagnostic_ids` plus `primary_diagnostic_id`, derive them
with closed precedence `liveness -> protocol/security/runtime identity ->
output integrity -> timeout -> none`, and reject inconsistent rows.

### BFP-SR-R29-2 - Candidate-scoped publication can bypass global in-flight state

Finding ID: BFP-SR-R29-2
Severity: blocking
Location: `specs/rigorloop-workflow.md` R28y publication state machine and `specs/rigorloop-workflow.test.md` T51
Evidence: Candidate-local observation can classify run B as clean while the
single global receipt, orphan staging, or temporary pointer belongs to run A.
The staged current reference also becomes nonexistent after rename, and
current input identity is not explicitly revalidated before installation.
Required outcome: Discover global recovery state before run allocation or skill
invocation; reconcile the receipt-owned run exclusively; block unrelated
in-flight state; use a historical staged snapshot or state-relative identity;
validate current inputs before installation; and test cross-run discovery.
Safe resolution: Add a global pre-generation discovery pass, bind the only
candidate from global state, replace the staged current reference with a
historical snapshot plus state-relative validation, and reject every unrelated
publication object before generation.

### BFP-SR-R29-3 - Manual recovery is not bound to the orphan publisher

Finding ID: BFP-SR-R29-3
Severity: blocking
Location: `specs/rigorloop-workflow.md` R28y orphan-staging recovery and `specs/rigorloop-workflow.test.md` T51
Evidence: The recovery record cites a terminated transport-stage process, but
staging does not identify its publisher. A later maintainer generally cannot
reap the crashed publisher, and interrupted authorized recovery states are not
exhaustively routed.
Required outcome: Bind staging to a publication-specific publisher identity,
use publisher-specific liveness proof safe across PID reuse/restart, and define
a closed recovery-resume table across authorization, staging presence,
deletion, directory fsync, and completion recording.
Safe resolution: Persist a publisher-instance lease before staging, bind the
staged manifest to it, require a lease-specific non-live proof rather than
child reaping, and model recovery as a closed write-ahead state machine with
idempotent deletion and fsync completion.

## Prior-finding assessment

| Prior finding | Assessment |
| --- | --- |
| `BFP-SR-R28-1` | Partially resolved; tuple and retry closure pass, compound diagnostic derivation remains. |
| `BFP-SR-R28-2` | Partially resolved; named candidate states pass, global discovery and publisher-bound recovery remain. |
| `BFP-SR-R28-3` | Resolved. |

## Review result

The spec remains blocked until R29-1 through R29-3 are resolved and
independently rereviewed.
Architecture remains required after approval.
