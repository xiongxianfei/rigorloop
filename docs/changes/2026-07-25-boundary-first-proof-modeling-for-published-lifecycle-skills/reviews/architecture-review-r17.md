# Boundary-First Proof Modeling Architecture Review R17

Review ID: architecture-review-r17
Stage: architecture-review
Round: 17
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: architecture candidate at 5cce27cf
Reviewed artifact: canonical architecture, boundary-proof component diagram, architecture assessment, proposed stage-envelope ADR, accepted predecessor ADRs, and approved R45 workflow spec
Status: changes-requested
Review status: changes-requested
Material findings: BFP-AR17-1
Immediate next stage: architecture
Plan readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed commit: `5cce27cf2c9209f54cea291398f302a8b0b311cd`

Reviewed architecture identity: `sha256:aa082fda043bed871ca6675ea7e88f9029f482848dbafc90dc1b4458dd5c2b92`

Reviewed component-diagram identity: `sha256:d99bf113d27c3b742629ee93096bf4419593e272a1e9b5f849bdf73b8164668a`

Reviewed proposed envelope ADR identity: `sha256:d43a762ad21244b87fa35194b7db79cd3ec345f2d09d0f2a1d22128be1b1d1c6`

Reviewed accepted permission-profile ADR identity: `sha256:ed9e026797920dc4e2e24cdbec22a466498ea9eb2a2efdf0e28bc588b1c73f14`

Reviewed workflow-spec identity: `sha256:bd5956d3c8977d0df11069010eef8cdec8f43603cf140aba732ec244167e8f97`

## Result

Changes requested with one material finding.

The Runtime View now projects the complete approved R45 protocol, and the
runtime, component, evidence-version, and ADR-lifecycle decisions are coherent.
However, one Building Block responsibility still exposes a writable child
workspace root. Planning remains paused until that contradiction is removed
and independently rereviewed.

## Material findings

### BFP-AR17-1 — The Building Block View still exposes a writable child workspace root

Finding ID: BFP-AR17-1

Severity: material

Location: `docs/architecture/system/architecture.md`, Level 2 White-Box
Boundary-Proof Validation and Evaluation, `Isolated workspace assembler`

Evidence:

- The assembler responsibility says it exposes one writable
  behavior-output root.
- The Runtime View, component diagram, proposed transport ADR, and approved
  R45 spec require read-only child workspace access, no child writable root,
  and parent-only materialization after the unchanged-workspace gate.
- An implementation plan could rely on the stale component responsibility and
  reintroduce the exact write bypass that the amendment is intended to close.

Required outcome:

State unambiguously that the assembler provisions a parent-owned output root,
presents all scenario workspace roots read-only to the child with no writable
child root, and permits writes only through the parent exact-byte materializer
after the unchanged-workspace gate.

Safe resolution:

Correct the single Building Block responsibility and rerun architecture-review.
No spec or ADR reopening is required.

## Prior-finding assessment

| Finding | Result |
| --- | --- |
| `BFP-AR16-1` | Mostly resolved, but remains blocked by `BFP-AR17-1`. |
| `BFP-AR16-2` | Resolved; the numbered Runtime View now projects the complete R45 protocol. |

## Review dimensions

| Dimension | Result |
| --- | --- |
| Spec alignment | pass with one contradictory projection |
| Package shape | pass |
| Boundary clarity | block |
| Data ownership | pass |
| Interface safety | pass |
| Runtime and failure handling | pass |
| Deployment and execution boundaries | pass |
| Security and privacy | block on stale writable-root statement |
| Quality and operations | pass |
| Testing feasibility | pass |
| Complexity discipline | pass |
| ADR quality | pass |
| Plan readiness | block |

## Readiness

Not ready for plan or implementation. Correct the isolated-workspace assembler
responsibility and rerun architecture-review R18.
