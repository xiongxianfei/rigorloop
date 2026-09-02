<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Simplify Final Verification and Retire Explain Change

Stage: explain-change
Status: current
Final diff identity: `f4cc4570d4492665b5f2a8315b80b06bfd0ed6e6..9c364d6162a32a03ac63d81093e728fd0e41b0bc`, binary diff SHA-256 `5aa61b918d81bb232997c91918457c85a88a66372968981b9a4214e30f79786d`
Final review identity: `code-review-final-r1` plus targeted PR-preflight rereviews `code-review-pr-preflight-r2`, `r4`, `r6`, and `r8`; latest reviewed correction `2365031f`, recording revision `b77057b1e5be548b7012aa4c94ac6b221fd62599`

## Summary

This change assembles a non-authoritative v3 RigorLoop candidate in which final Code Review routes directly to Verify, Verify selects evidence according to actual impact and freshness, and only a successful Verify result contains the durable final explanation consumed by PR preparation. It removes the standalone current `explain-change` skill and standalone test-spec path, keeps historical v1/v2 records readable without progression authority, and leaves activation, publication, release, and migration outside this change.

The implementing change itself remains registered under v2 until this M6 closeout finishes. This document is therefore the required historical-v2 explanation of the reviewed v3 candidate; it is not a v3 explanation artifact and does not grant verification or PR readiness.

## Problem

The previous final path produced an explanation before final verification, so a verification finding could immediately make that explanation stale. It also treated revision identity too broadly when deciding whether earlier evidence remained applicable, which could cause product checks to rerun after a final change that could not affect the surface those checks proved.

The approved direction moves explanation generation into successful final Verify and makes evidence selection depend on impact, applicability, and explicit freshness policy. Unknown impact broadens verification, and Verify remains read-only with respect to implementation repair.

## Decision trail

- The accepted proposal approved removing the governed standalone explanation stage, generating the final explanation only after successful verification, allowing conservative impact-based evidence reuse, preserving explicit freshness overrides, and keeping Verify independent from repair.
- Design Review `design-review-r2` approved the exact architecture, specification, and ADR package. The architecture makes `verify-report.md` the v3 success artifact; the specification defines FV-R1 through FV-R38, eight boundary classes, four selected interactions, and FV-AC1 through FV-AC14.
- Delivery Review `delivery-review-r3` approved the plan-only package and six milestones. It bound this change's closeout to immutable v2 source revision `585c2beecea0ddda0ae11ed8f0b1a53b24310052` before any later v3 activation.
- M1 established lifecycle classification, activation-manifest validation, and historical compatibility. M2 implemented impact, applicability, freshness, execution-proof, result, and evidence-tail contracts. M3 implemented correction ownership and PR consumption. M4 aligned canonical skills, governance, validators, templates, and generated candidates. M5 selected v3 as the sole current executable candidate, removed the standalone skill, and aligned public and adapter guidance.
- Code Reviews M1 through M5 resolved 18 material findings. Final holistic Code Review `code-review-final-r1` reviewed `f4cc4570..c93e3834`, found no material issue, and confirmed the candidate remains preactivation with no release or historical mutation. PR integration then exposed four clusters of stale current-behavior test fixtures. Findings FV-M6-CR1 through FV-M6-CR4 were corrected without changing production code and independently approved by targeted rereviews R2, R4, R6, and R8.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| Lifecycle runtime, CLI readers, schemas, and metadata validators | Add parsed v3 classification and validation; make v3 the sole current executable contract while v1/v2 remain readable history with no progression. | A single current contract avoids permanent multi-version progression logic and fails closed on unknown or mixed state. | FV-R4-FV-R7, FV-R37-FV-R38; Design Review R2. | M1 and M5 evidence; Node, conformance, metadata, lifecycle, and boundary suites. |
| Verify protocol and report model | Add closed impact surfaces, applicability decisions, freshness classes, execution proofs, always-current checks, normalized basis, and closed report-tail validation. | Evidence should rerun only when impact or policy can invalidate it; uncertainty must broaden proof. | FV-R8-FV-R34; BND-INPUT-001 through BND-ENV-001. | M2 evidence; JavaScript/Python conformance, cache-separation, tail, and unknown-value regressions. |
| Workflow correction and PR handoff | Route seven Verify finding kinds to exact owners and required rereview boundaries; require PR to consume the exact successful Verify basis and explanation. | Verify must identify defects without repairing them, and PR must not author a competing rationale. | FV-R23-FV-R30; INT-002-INT-003. | M3 evidence; public route/return matrices and PR-consumption tests. |
| Canonical `verify`, `workflow`, `pr`, and sibling stage skills | Remove current pre-Verify explanation dependencies and add progressive final-impact, applicability, and success-only explanation resources. | The final explanation belongs to the exact evidence basis that established readiness. | FV-R1-FV-R3, FV-R26-FV-R30, FV-R35-FV-R37. | M4 package-parity evidence and skill/build validation. |
| `skills/explain-change/` and current inventories | Remove the standalone authored package and its current adapter manifest entry. | V3 must have no governed explanation stage or separately settled explanation artifact. | FV-R1-FV-R3, FV-R28, FV-R35. | Absence and mixed-package regressions; historical archive audit. |
| Adapter generation and public guidance | Generate the OpenCode alias declaration from the canonical tuple, package complete Verify resources, and describe candidate metadata separately from immutable releases. | Human and generated entrypoints must expose the same non-authoritative candidate graph. | FV-R35, FV-R37; FV-AC11, FV-AC14. | M5 R2 direct generated probe; 155 adapter tests; root README route regression. |
| Current workflow test fixtures | Select v3 for current query/state fixtures, use the current Verify completion rule, accept the review-only pre-Verify tail, reject retired policy selectors, and preserve separately identified historical-read cases. | Tests must exercise the sole current contract instead of requiring production to retain retired v1/v2 stages or selectors. | FV-R1-FV-R7, FV-R28, FV-R35, FV-R37-FV-R38. | PR-preflight reviews R2/R4/R6/R8; focused suites 26, 19, 20, and 70 tests; PR gate 28/28. |
| Change-local reviews, resolutions, and evidence | Record milestone reviews, two Design/Delivery revisions, 22 resolved findings, final holistic review, targeted correction rereviews, and immutable-v2 closeout constraints. | The implementing v2 change must finish coherently before v3 can ever be activated. | FV-R7, TG-24-TG-27. | Closed review validation; final holistic review and PR-preflight rereviews. |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| TG-01-TG-05 | Parsed lifecycle identity, manifest integrity, normalized basis identity, and unknown-value-first rejection. | Unit and cross-language conformance. |
| TG-06-TG-09 | Complete impact mapping, evidence applicability, freshness, execution proof, successful-result shape, and exact evidence tail. | Unit, integration, and repository-backed protocol tests. |
| TG-10-TG-14 | V3 route without explanation, exact correction ownership, failed-attempt behavior, PR consumption, and cache/result separation. | Workflow and lifecycle integration. |
| TG-15-TG-18 | Canonical and generated skill parity, progressive resource loading, historical compatibility, and mixed-package rejection. | Skill, build, and adapter package validation. |
| TG-19-TG-23 | Current v3 scaffold and public route, historical read-only behavior, package retirement, complete candidate scenarios, and preactivation inventory. | Public CLI, documentation, adapter, and broad-smoke validation. |
| TG-24-TG-27 | Complete requirement trace, cross-milestone validation, immutable-v2 bootstrap hashes, review closeout, and release-isolation checks. | Final holistic Code Review and M6 closeout evidence. |
| FV-M6-CR1-FV-M6-CR4 | Current query, evidence-tail, policy, and state fixtures agree with the v3-only runtime while explicit historical cases remain bounded. | PR integration and focused regression suites. |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `bash scripts/ci.sh --mode broad-smoke` | Final holistic review passed 12 of 12 checks in 730 seconds. | `0409d0c54b054f61312e2c70b94103053637c35b` |
| `npm test --prefix packages/rigorloop` | 333 passed, 2 intentional historical skips, 0 failed. | `0409d0c54b054f61312e2c70b94103053637c35b` |
| Lifecycle CLI conformance and governed validation | Passed; no activation, final-activation, or legacy-progression error. | `0409d0c54b054f61312e2c70b94103053637c35b` |
| Metadata, Workflow, cache, and boundary suites | 107 metadata, 78 Workflow, 25 cache, and 69 boundary tests passed. | `0409d0c54b054f61312e2c70b94103053637c35b` |
| Skill, generated-skill, and adapter validation | 376 skill tests, 8 build tests, generated drift check, and 155 adapter tests passed during M5 review; final broad smoke revalidated selected current surfaces. | `0409d0c54b054f61312e2c70b94103053637c35b` |
| Review closeout and artifact lifecycle | 28 reviews, 22 resolved findings, no open finding; change metadata and review closeout validation passed. | `9c364d6162a32a03ac63d81093e728fd0e41b0bc` |
| Bound v2 archive, skill, and CLI hashes | Exact plan-bound archive and three file hashes passed. | `0409d0c54b054f61312e2c70b94103053637c35b` |
| Activation/release/history audit | Activation manifest remains preactivation; no release archive, tag, publication record, release note, or historical explanation changed. | `0409d0c54b054f61312e2c70b94103053637c35b` |
| `bash scripts/ci.sh --mode pr --base 066d973c4e230639aefda753d1f52dea4d730d28 --head HEAD --jobs 4` | Passed all 28 selected direct product and governance checks; merge simulation was conflict-free. | `9c364d6162a32a03ac63d81093e728fd0e41b0bc` |

## Review resolution summary

All 22 material findings are accepted and resolved, with no `needs-decision` disposition or open review-log finding. The findings tightened parsed lifecycle classification, manifest ordering, evidence-surface closure, execution proof, report identity and tail shape, cross-language conformance, v3 route ownership, public package parity, the M6 immutable-v2 closeout boundary, and the separation of current-v3 fixtures from historical compatibility coverage. See `review-resolution.md` for the durable dispositions and validation evidence.

## Alternatives rejected

- Keeping standalone explain-change preserves a stale-artifact cycle and cannot bind the rationale to the evidence that actually established readiness.
- Treating every new revision as invalidating every earlier result is safe but needlessly broad and ignores what each result proves.
- Treating particular filenames as inherently harmless is unsafe; impact must be established from the actual changed surface and governing evidence.
- Maintaining executable v1/v2/v3 progression indefinitely adds compatibility machinery without user value. Historical records remain readable, but only the newest activated contract should execute.
- Letting Verify repair implementation would merge evidence judgment with change ownership and weaken rereview boundaries.

## Scope control

This change does not activate or release v3, publish packages, create tags, migrate historical explanations, modify completed historical records, define a complete dependency graph, infer safety from filenames, make evidence permanently valid, weaken explicit freshness policy, remove Code Review, or authorize Verify to repair implementation. The candidate manifest and generated packages remain non-authoritative until a separately governed post-M6 activation and release action.

## Risks and follow-ups

Impact classification can be wrong, so unknown or ambiguous impact always broadens verification and explicit freshness requirements always override reuse. The staged protocol increases Verify's responsibilities; progressive resources and cross-language conformance reduce the chance of contradictory implementations. Historical-v2 closeout remains intentionally separate from the new v3 success-only explanation model.

M6 still requires final Verify, dual read-back through the bound archived CLI and current read-only validators, and PR handoff. Universal zero-nonterminal-pre-v3 proof, activation, publication, tagging, and release remain future separately authorized work.

## Workflow handback

Explanation status: current
Explanation basis: final diff `f4cc4570d4492665b5f2a8315b80b06bfd0ed6e6..9c364d6162a32a03ac63d81093e728fd0e41b0bc`, final holistic review `code-review-final-r1`, targeted correction rereviews through `code-review-pr-preflight-r8`
Validation-evidence cutoff: `9c364d6162a32a03ac63d81093e728fd0e41b0bc`
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
