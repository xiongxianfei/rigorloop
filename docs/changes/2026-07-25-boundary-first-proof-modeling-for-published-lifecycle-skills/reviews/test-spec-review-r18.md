# Boundary-First Proof Modeling Test-Spec Review R18

Review ID: test-spec-review-r18
Stage: test-spec-review
Round: 18
Reviewer: Codex test-spec-review skill with context-separated independent reviewer
Target: specs/rigorloop-workflow.test.md and specs/skill-contract.test.md
Reviewed artifact: R48/R22/R17 v3 proof-map candidate at bc8815ff
Status: changes-requested
Review status: changes-requested
Material findings: BFP-TSR18-1
Immediate next stage: test-spec revision
Implementation readiness: not-ready
Implementation handoff: not-allowed
Recording status: recorded
Review date: 2026-07-27
Context separation mechanism: separate-agent

Reviewed commit: `bc8815ffdee5a55bf72ac45bb323790166d97b8e`

Reviewed workflow test-spec identity:
`sha256:cda843f37335e3c30655e283a19de30eff7f0fd065ed1d33b815f8d31b2858d0`

Reviewed skill-contract test-spec identity:
`sha256:94f8bec1f53a9807982d504764a4f5dd37c6f26aa42e9ea10c534287dae8b11c`

## Result

Changes requested. The runtime-projection, common-conformance,
capability-branch, v3 migration, rollback, and open-M2-finding proof surfaces
pass. One mandatory companion command cannot execute under the approved
change-root-bound preflight contract.

## Finding

### BFP-TSR18-1 — Companion preflight command omits the required change identity

Finding ID: BFP-TSR18-1
Severity: major
Location: `specs/skill-contract.test.md`, `CMD-SBFP-8`

Evidence: `CMD-SBFP-8` invokes
`boundary_proof_behavior.py check-environment --json`, while approved R48
requires `check-environment --change-id <change-id> --json` and rejects a
missing change ID before runtime discovery. The command is mandatory for M2
and is referenced by T57, T58, and the M2 proof map.

Required outcome: Add the exact boundary-first change ID and synchronize
failure, evidence, and safe-side-effect semantics with primary command
`CMD-BFP-8`.

Safe resolution: Use the exact command
`python scripts/boundary_proof_behavior.py check-environment --change-id
2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills
--json`; state that failure stops M2 before other harness or participating
skill mutation; name `validation-m2.md` and
`evidence/runtime-preflight-attestation.json`; and classify it as an
evidence-only, non-secret, parent-observed feasibility transaction.

## Coverage assessment

All other reviewed dimensions pass, including exact implementation-byte
selection, ten-field projection, 3/93 feature partition, common pre-branch
conformance, all eleven conformance cases, both capability states, diagnostic
routing, v3 success/failure separation, opaque-v1/unsupported-v2 handling,
phase-aware rollback, milestone mapping, and the three open M2 implementation
findings.
