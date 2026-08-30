# Change explanation: Simplify the RigorLoop Proposal Contract

Stage: explain-change
Status: current
Final diff identity: `origin/main...3ee81ed9bf2f65eab95da9c8e2ae89830481ed24`
Final review identity: `code-review-m4-r3` at `c18b2398acc5dabc9b9637052af1e94c01600c2b`

## Summary

This change makes a proposal a concise direction-approval artifact. It keeps seven required sections, makes impact analysis conditional, embeds proportionate feasibility, and prevents Proposal Review from demanding decisions owned by Design or Delivery. Canonical skills, templates, governance guidance, validators, tests, and temporary adapter projections now implement the same contract.

## Problem

Proposal authoring and review had accumulated architecture, behavioral requirements, delivery planning, proof design, rollout detail, and generic risk analysis. That obscured the direction-level decision, duplicated downstream work, and weakened the authority of Design Review and Delivery Review.

## Decision trail

- Proposal Review `proposal-review-r1` approved a lightweight direction-approval contract with feasibility inside the proposal and conditional material-impact analysis.
- Design Review `design-review-r2` approved `docs/architecture/2026-08-30-simplified-proposal-contract.md` and `specs/simplified-proposal-contract.md` as one package.
- Delivery Review `delivery-review-r3` approved `docs/plans/2026-08-30-simplify-rigorloop-proposal-contract.md` and `specs/simplified-proposal-contract.test.md` as one package, including the corrected current-versus-historical publication proof boundary.
- Final holistic Code Review `code-review-m4-r3` reviewed `origin/main...3ee81ed9bf2f65eab95da9c8e2ae89830481ed24` and found no material issue.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/proposal/`, proposal template, and references | Define seven required sections, conditional impact analysis, proportionate feasibility, and downstream deferral | Make proposal authoring match direction-level approval | SPC-R1-SPC-R10; BND-AUTHOR-001 | CMD-01, CMD-02, M1 evidence |
| `skills/proposal-review/` and review resources | Review decision sufficiency and Vision fit without requiring Design or Delivery detail | Keep review authority at the proposal boundary | SPC-R11-SPC-R16; BND-REVIEW-001 | CMD-01, CMD-02, proposal-review receipt |
| Governance and workflow references | Align handoff language and stage ownership with the simplified contract | Prevent maintainers and shipped skills from describing different rules | Approved design package | CMD-09, M1 evidence |
| Proposal and review validators | Enforce current section shape, conditional placement, governed ownership, historical compatibility, and closed review vocabularies | Make deterministic contract rules software-owned | SPC-R1-SPC-R16; BND-VALIDATE-001 | CMD-03-CMD-05, M2 evidence |
| Build and adapter parity tests | Select both proposal-stage packages and compare temporary generated and installed resources across supported adapters | Prove published package parity without committing generated bodies | SPC-R17-SPC-R18; BND-COMPOSE-001 | CMD-06-CMD-08, M3 evidence |
| Lifecycle CLI retry handling | Permit a replacement review after a blocked unchanged package while retaining fail-closed prior-evidence checks | Unblock the approved Design rereview without weakening evidence integrity | Existing lifecycle contract | Package tests and independent CLI review |
| Review closeout validator | Match rereviews by stable occurrence, stage, and numeric round rather than Markdown source order | Prevent false historical blockers without cross-closing milestones | Existing review closeout contract | 108 review-validator tests; `code-review-m4-r2` |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| SPC-T01-SPC-T08 | Proposal grammar, conditional impact, feasibility, ownership, compatibility, review criteria, and downstream deferral | Contract and integration |
| SPC-T09 | Canonical proposal-stage resources match temporary generated packages | Build integration |
| SPC-T10 | Proposal and Proposal Review clean-install correctly for Codex, Claude, and opencode | Adapter integration |
| SPC-M4-CR1 regression | Canonical review-log ordering works; same-round and cross-milestone reviews do not close another occurrence | Validator unit |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| CMD-01 through CMD-09, CMD-11, CMD-12 | Passed in their approved modes | `code-review-m4-r1` and milestone evidence |
| `npm test --prefix packages/rigorloop` | 298 passed, 2 intentional skips, 0 failed | `code-review-m4-r1` |
| `python scripts/test-review-artifact-validator.py` | 108 passed | `code-review-m4-r3` |
| Review structure and closeout validation | Passed with all ten findings resolved | `code-review-m4-r3` |
| Recorded-source `v0.4.1` validation | Passed; tracked historical surfaces unchanged | `code-review-m4-r1` and `code-review-m4-r3` |
| Generated-output inspection | No generated skill bodies or archives committed | `code-review-m4-r3` |

## Review resolution summary

All ten material findings have accepted, resolved dispositions in `review-resolution.md`. They cover Delivery wording, current-versus-historical proposal validation, governed path correlation, publication identity, M3 evidence attribution, and review closeout occurrence matching. `code-review-m4-r3` is the clean final holistic review.

## Alternatives rejected

- Keeping downstream architecture, detailed behavior, implementation sequencing, or verification design in proposals was rejected because those decisions belong to Design or Delivery.
- A fixed proposal length or token budget was rejected in favor of decision sufficiency and proportional depth.
- Per-document hashes, document version markers, and new compatibility documents were not introduced for the proposal contract.
- Published `v0.4.1` identities were not reused for current-branch output; current parity uses temporary artifacts while historical validation uses recorded source.

## Scope control

This change does not redesign Design Review, Delivery Review, Code Review, or Verify; merge authoring artifacts; add semantic proposal generation; rewrite settled historical proposals; commit generated adapter packages; or define new release behavior.

## Risks and follow-ups

The main residual risk is reviewer drift back toward requesting downstream detail. The updated Proposal Review criteria, examples, and deterministic shape checks reduce that risk. Final verification still owns current branch readiness, complete command reruns where required, and PR handoff eligibility.

## Workflow handback

Explanation status: current
Explanation basis: `origin/main...3ee81ed9bf2f65eab95da9c8e2ae89830481ed24`; final review `code-review-m4-r3`
Validation-evidence cutoff: `c18b2398acc5dabc9b9637052af1e94c01600c2b`
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
