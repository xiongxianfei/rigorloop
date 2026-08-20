# Code Review M2 R2: Corrected Compact Contract

Review ID: code-review-m2-r2
Stage: code-review
Round: r2
Reviewer: Codex independent code-review context
Target: corrected implementation milestone M2 range `204e9689..1a72a04e`
Reviewed milestone: M2
Reviewed artifact: commit `1a72a04e`
Review date: 2026-08-20
Status: changes-requested
Material findings: BUGSIM-CR2
Recording status: recorded

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: 1
- Recording status: recorded
- Review resolution: needs-decision
- Milestone closeout: open
- Next owner: proposal/spec
- Verify readiness: blocked

## Rereview result

`BUGSIM-CR1` is corrected: the canonical text and focused assertions now restore all R14 causes, all R15 actions, the exact post-fix phase, the unexpected-mutation stop, and R24 result fields. Focused, broad, boundary, build, prose, and metadata validation passed for that correction.

## BUGSIM-CR2 — Major: the approved inline contract and strict legacy-byte ceiling conflict

### Evidence

R7 requires the published skill to classify five axes using every closed value selected by the proposal. R12 requires the complete proof-action matrix. R21 requires exact portable/governed write tables. The corrected 3,754-byte file remains below the 3,761-byte ceiling only because those contracts are summarized rather than enumerated. For example, it names the evidence axes but omits the full reproduction, contract-basis, feasibility, proof, and support vocabularies.

Adding those required inline values and exact tables exceeds the approved ceiling before optional explanation is considered. Removing them passes R26's size assertion but violates R7, R12, and R21. Moving them to a reference violates R1's one-file/no-reference package and changes the approved package decision.

### Required outcome

The proposal/spec owner must choose and approve a coherent constraint set. Safe options are:

1. retain the flat package and replace the legacy-byte ceiling with a justified bounded budget or word-only reduction;
2. permit one conditional reference and define its loading/measurement contract; or
3. narrow the normative inline state model while preserving fail-closed authority and proof behavior.

Implementation must not silently relax R26, omit R7/R12/R21, or add a resource contrary to R1.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| BUGSIM-CR1 correction | pass | The specifically omitted values and behaviors are restored and tested. |
| Evidence vocabulary | block | Full R7 vocabularies are not published inline. |
| Proof matrix | block | R12's exhaustive matrix is summarized rather than closed. |
| Write boundary | block | R21's portable/governed phase table is not fully represented. |
| Size acceptance | pass in isolation | Current file is 412 words and 3,754 bytes, but semantic completion breaks the byte constraint. |
| Architecture | unchanged pending decision | A reference would require reassessment; a bounded flat-file budget change likely would not. |

## Claim limitations

M2 remains open. M3, final review, explanation, verification, CI, branch readiness, and PR readiness are not established.
