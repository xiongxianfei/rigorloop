# Boundary-First Proof Modeling Code Review M1 R2

Review ID: code-review-m1-r2
Stage: code-review
Round: M1 R2
Reviewer: Codex code-review skill with context-separated independent reviewer
Target: commit `fec5eb73` against approved test-spec baseline `dc1a3baf`
Reviewed artifact: M1 correction implementation
Reviewed milestone: M1. Deterministic core correction
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-26
Recording status: recorded
Material findings: none new; BFP-M1-CR4 and BFP-M1-CR7 remain open
Immediate next stage: review-resolution M1
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: boundary-first-m1-r2-author
Reviewer context ID: boundary-first-m1-r2-independent-reviewer
Context separation mechanism: separate-agent
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: retained fail-closed evidence and synthetic-trace contract findings
Risk-tier classifier: changed-contract-and-evidence-surface
Governing artifacts: specs/rigorloop-workflow.md; specs/skill-contract.md; specs/rigorloop-workflow.test.md; specs/skill-contract.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Formal criteria: R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p, T40-T46, T55
Initial packet inventory: specs/rigorloop-workflow.md@fec5eb73#sha256:cce7047761aaa99d81263cf226261e73de3de35e9064e93732274d3a3a8ae1f8; specs/skill-contract.md@fec5eb73#sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc; specs/rigorloop-workflow.test.md@fec5eb73#sha256:94fdf3da61d35647596d550eaa0527d130daf49ca3af2cf7ff933e330f860f91; specs/skill-contract.test.md@fec5eb73#sha256:c940ddd626f26db9e7b2f01cc381b99f63347db45fea21a828dde19c4b74c1ac; docs/plans/2026-07-25-boundary-first-proof-modeling.md@fec5eb73#sha256:b9402c16929211fdac78f7981e5a8d3d3ed49ee0d2e95859c1fc55cd95909f3b
Prompt template version: review-gate/v1
Initial packet hash: sha256:a908a58a595847198085451206aebaa1721cd146d9d9c08fd9adc6eb8d680767
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Clean-review sufficiency receipt: no

Affected behavior: M1 evidence provenance, exact synthetic trace grammar, and derived simple-change observations.
Highest-impact failure modes: detached evidence can support a report; compressed event records can conceal invalid linkage; overbroad subtraction can hide a new universal lifecycle artifact.
Changed boundaries: repository files to accepted evidence references; synthetic event records to R28y trace proof; event-produced paths to universal-artifact calculation.
Evidence expected: tracked-or-change-local provenance; exact nine-field events; identity-bearing snapshots and inventories; review-bundle and evidence-union checks; exact branch and subtraction contrasts.
Areas requiring direct inspection: the M1 model, focused tests, simple-change fixture, and current R28y grammar.
Areas intentionally out of scope: M2 runtime execution, skill mutation, adapters, activation, publication, and external actions.
Risk classes considered: evidence identity, provenance, trace linkage, closed outcomes, recovery branch shape, artifact classification, and scope containment.
Falsifiable review questions: can untracked scratch evidence pass; can diagnostics contradict structural results; can unproduced outputs enter inventory; can an extra lifecycle artifact be subtracted without trace ownership?

## Result

- Review status: changes-requested
- Retained findings: BFP-M1-CR4 and BFP-M1-CR7
- Resolved findings confirmed: BFP-M1-CR1, BFP-M1-CR2, BFP-M1-CR3, BFP-M1-CR5, and BFP-M1-CR6
- Milestone state: resolution-needed
- M2 handoff: blocked
- Verify readiness: not claimed

## Evidence challenge

The independent reviewer ran the focused suite, compilation, CLI help, and
direct adversarial probes against an archive of exact commit `fec5eb73`.

Passed validation:

- `python3 scripts/test-boundary-proof.py` — 13 tests passed.
- `python3 -m py_compile scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py` — passed.
- `python3 scripts/validate-boundary-proof.py --help` — passed.

The implementation remains synthetic and contains no `skills/` changes.
However, direct probes reproduced two retained contract escapes.

## Retained finding reconciliation

### BFP-M1-CR4 — evidence provenance remains incomplete

Status: open
Severity: blocker
Location: `scripts/boundary_proof_model.py`

The correction now rejects missing, stale, escaping, non-regular, leaf or
ancestor symlink, and hash-mismatched evidence, and it enforces the closed
`not-run` blocker. It still accepts an arbitrary untracked regular file outside
the current change-local root when the caller supplies its current hash.
R28y requires every evidence path to be tracked repository state or an allowed
change-local file.

Required outcome: classify each evidence path as tracked or current
change-local and reject every other repository file. Add direct untracked
non-change-local and symlink-ancestor regressions.

### BFP-M1-CR7 — synthetic trace grammar and formulas remain compressed

Status: open
Severity: blocker
Locations: `scripts/boundary_proof_model.py`;
`tests/fixtures/boundary-proof/simple-change.json`

The evaluator computes counters, but its five-field events and two-field
inventories omit the approved R28y snapshot identities, exact input/output
links, reviewed snapshot, evidence unions, review-bundle grammar, distinct
attempt-two output, and identity-bearing inventory.

Direct probes were accepted for:

- passing authoring with a non-`none` diagnostic;
- structurally passing blocked review with diagnostic `none`;
- authoring structural failure with diagnostic `none`;
- a blocked prefix paired with inventory for stages that never ran; and
- an unrelated extra feature spec that did not increase the universal-artifact
  count.

The last escape occurs because the evaluator subtracts every newly classified
feature spec, test spec, and review-evidence file instead of only exact
trace-produced outputs and review-bundle references.

Required outcome: implement the exact R28y event, snapshot, review-bundle,
evidence, and inventory grammar; derive applicable-only mapping from terminal
approved snapshots; subtract only exact trace-produced outputs and formal
review-bundle references; and add negative proof for every consistency row,
terminal branch, broken or ambiguous link, same-path correction, invalid
evidence union, unproduced inventory artifact, and extra lifecycle artifact.

## Prior-finding reconciliation

| Finding | R2 result |
| --- | --- |
| BFP-M1-CR1 | Resolved: stable and unique identities plus per-reference requirement ownership are enforced. |
| BFP-M1-CR2 | Resolved: exact omission, trigger, contrast, gate, and diagnostic rules are frozen. |
| BFP-M1-CR3 | Resolved: marker presence and explicit legacy/v1 scope parity fail closed. |
| BFP-M1-CR4 | Retained: byte identity is enforced but tracked/change-local provenance is not. |
| BFP-M1-CR5 | Resolved at M1 scope: semantic mapping permutations serialize identically. |
| BFP-M1-CR6 | Resolved: all eight incident files replay through state-derived evaluation. |
| BFP-M1-CR7 | Retained: aggregate counters exist but the governing trace grammar and formulas remain incomplete. |

## Milestone handoff

M1 remains `resolution-needed`. M2 must not start until both retained findings
are resolved, focused validation passes, and an independent M1 R3 review
approves the corrected milestone.
