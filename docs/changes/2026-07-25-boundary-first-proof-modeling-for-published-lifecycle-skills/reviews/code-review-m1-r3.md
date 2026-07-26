# Boundary-First Proof Modeling Code Review M1 R3

Review ID: code-review-m1-r3
Stage: code-review
Round: M1 R3
Reviewer: Codex code-review skill with context-separated independent reviewer
Target: commit `15369140` against `fec5eb73`
Reviewed artifact: M1 evidence and synthetic-trace correction
Reviewed milestone: M1. Deterministic core correction
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-26
Recording status: recorded
Material findings: none new; BFP-M1-CR7 remains open
Immediate next stage: review-resolution M1
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: boundary-first-m1-r3-author
Reviewer context ID: boundary-first-m1-r3-independent-reviewer
Context separation mechanism: separate-agent
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: retained synthetic-trace and evidence-formula finding
Risk-tier classifier: changed-contract-and-evidence-surface
Governing artifacts: specs/rigorloop-workflow.md; specs/skill-contract.md; specs/rigorloop-workflow.test.md; specs/skill-contract.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Formal criteria: R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p, T40-T46, T55
Initial packet inventory: specs/rigorloop-workflow.md@15369140#sha256:cce7047761aaa99d81263cf226261e73de3de35e9064e93732274d3a3a8ae1f8; specs/skill-contract.md@15369140#sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc; specs/rigorloop-workflow.test.md@15369140#sha256:94fdf3da61d35647596d550eaa0527d130daf49ca3af2cf7ff933e330f860f91; specs/skill-contract.test.md@15369140#sha256:c940ddd626f26db9e7b2f01cc381b99f63347db45fea21a828dde19c4b74c1ac; docs/plans/2026-07-25-boundary-first-proof-modeling.md@15369140#sha256:1f040d4995895fd919b5a4031ce5bfef9e495038691944f44027b5cfd4e292b7
Prompt template version: review-gate/v1
Initial packet hash: sha256:b8ea14af63d632f1de054b7a31f845119f81fb8f4a96f2886254af1656da67cc
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Clean-review sufficiency receipt: no

Affected behavior: exact R28y inventory classification, completeness, identity uniqueness, and structural-diagnostic provenance.
Highest-impact failure modes: lifecycle artifacts can be mislabeled out of the universal count; captured outputs can disappear from the complete inventory; duplicate identities can conceal substitution; diagnostics can remain caller assertions.
Changed boundaries: artifact path to closed classification; snapshot capture to complete inventory; structural evaluation to event diagnostic.
Evidence expected: derived classifier contrasts, identity uniqueness, complete snapshot/inventory equality, and structural-result-bound diagnostics.
Areas requiring direct inspection: the synthetic trace evaluator, simple-change fixture, and focused negative tests.
Areas intentionally out of scope: M2 runtime execution, skill mutation, adapters, activation, publication, and external actions.
Risk classes considered: caller assertion, classification ambiguity, inventory completeness, identity substitution, diagnostic provenance, and scope containment.
Falsifiable review questions: can a plan or spec path claim non-lifecycle; can two paths share one identity; can a declared output evade inventory; can failure accept an unrelated stable diagnostic?

## Result

- Review status: changes-requested
- Retained finding: BFP-M1-CR7
- BFP-M1-CR4: resolved
- Milestone state: resolution-needed
- M2 handoff: blocked
- Verify readiness: not claimed

## Evidence challenge

The independent reviewer ran the 16 focused tests, compilation, CLI help, and
adversarial probes from an exact checkout of `15369140`. The exact event,
snapshot, bundle, evidence-union, sequencing, correction, terminal, mapping,
and produced-path subtraction behavior is substantially implemented.

Four escapes remain:

1. `docs/plans/*.md` and `specs/*.md` can be labeled `non-lifecycle`, causing
   new lifecycle artifacts to evade the universal count.
2. Distinct inventory paths may share one identity even though R28y requires
   identities to be unique.
3. A declared `behavior-output` snapshot may be absent from every event and
   the complete after inventory.
4. An arbitrary stable non-`none` diagnostic may accompany structural
   failure; the diagnostic is not bound to the deterministic structural
   result.

Correctly classified extra feature-spec, test-spec, review-evidence, and
other-lifecycle paths each count as one. The remaining gap is therefore
classifier and provenance enforcement, not the produced-path subtraction
formula itself.

## Retained finding reconciliation

### BFP-M1-CR7 — classifier and diagnostic provenance remain incomplete

Status: open
Severity: blocker

Required outcome:

- derive artifact kind from the closed ordered R28y path classifier and reject
  caller mismatches;
- enforce unique inventory identities as well as paths;
- require every behavior-output snapshot in the complete after inventory and
  reject orphan captured output;
- bind failure diagnostics to deterministic structural results;
- add a direct negative regression for each escape.

No spec, architecture, skill, or scope decision is required.

## Prior-finding reconciliation

| Finding | R3 result |
| --- | --- |
| BFP-M1-CR1 | Resolved; regression scan passed. |
| BFP-M1-CR2 | Resolved; regression scan passed. |
| BFP-M1-CR3 | Resolved; regression scan passed. |
| BFP-M1-CR4 | Resolved; provenance and symlink contrasts passed. |
| BFP-M1-CR5 | Resolved; canonical serialization remains green. |
| BFP-M1-CR6 | Resolved; eight-incident replay remains green. |
| BFP-M1-CR7 | Failed remediation for the four escapes above. |

## Milestone handoff

M1 remains `resolution-needed`. M2 must not start until BFP-M1-CR7 is
corrected and an independent M1 R4 review approves the milestone.
