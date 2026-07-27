# Boundary-First Proof Modeling Architecture Review R21

Review ID: architecture-review-r21
Stage: architecture-review
Round: 21
Reviewer: Codex architecture-review skill with context-separated independent reviewer
Target: canonical architecture, boundary-proof component diagram, architecture assessment, and capability-projected file-change ADR chain
Review surface: canonical-architecture-update plus proposed ADR
Reviewed artifact: R20 correction candidate at a46757fc
Status: changes-requested
Review status: changes-requested
Material findings: BFP-AR21-1
Recording status: recorded
Immediate next stage: architecture
Plan readiness: not-ready
Review date: 2026-07-27
Context separation mechanism: separate-agent

Reviewed commit: `a46757fc9912baa61116e000f3852ef37b0047a3`

## Result

Changes requested. Prior ownership and common-gate findings are resolved, but
one v3 attestation-assembly path still bypasses pure validation and depicts
failure diagnostics inside successful evidence.

## Material finding

### BFP-AR21-1 — The v3 attestation path bypasses canary-policy validation and depicts forbidden diagnostic content

Finding ID: BFP-AR21-1

Severity: material

Evidence:

The canary policy flows directly to the preflight attestation and has no
generation path. Both successful-attestation edges include diagnostics even
though the approved successful attestation has no diagnostic field.

Required outcome:

Validate every v3 attestation input through the pure model and keep failure
diagnostics outside successful attestation evidence.

Safe resolution:

Route canary policy object/identity into the pure validator, route its validated
identity into both attestations, remove the direct edge, and route validated
diagnostic decisions only to a separate failure-response/evidence node.

## Readiness

Not ready for plan revision. Resolve BFP-AR21-1 and rerun architecture review.
