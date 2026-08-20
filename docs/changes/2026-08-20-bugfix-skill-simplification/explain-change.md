<!-- explain-change-skeleton-v1; normative -->

# Change explanation: Bugfix skill simplification

Stage: explain-change
Status: current
Final diff identity: `2b7346abf0f8798dd3b49313dee936b1865cc4a1..c2cc66b1a7056fc52c8820df05ae021f5a212dd7` (`sha256:b1d704a87f5ad68e9f96c3b7cf31d5dc41a7fbc4ed548428babe5d65d87cf9d7`)
Final review identity: `code-review-final-r3` recorded by revision `b2ea37ed80270a2999efbaeb2c4777e3d58d7c37`

## Summary

The bugfix skill remains a single, resource-free package, but its compact guidance is replaced by a complete deterministic contract. The new contract separates intent, command authority, write authority, proof authoring, production correction, validation, owner routing, and terminal results. It favors truthful and sufficient semantics over an arbitrary word, byte, or token reduction.

## Problem

The previous skill combined diagnosis and correction decisions, did not close command or repository-write authority, made its regression-proof prerequisite circular, and allowed evidence combinations to route nondeterministically. Those gaps could permit an unsupported production edit, prevent writing the failing test needed to establish proof, or produce inconsistent claims about an unknown cause or contract gap.

## Decision trail

- Proposal: `docs/proposals/2026-08-20-bugfix-skill-simplification.md`
- Specification: `specs/bugfix-skill-simplification.md`
- Architecture assessment: `docs/changes/2026-08-20-bugfix-skill-simplification/architecture-assessment.md`
- Plan: `docs/plans/2026-08-20-bugfix-skill-simplification.md`
- Test specification: `specs/bugfix-skill-simplification.test.md`
- Final review: `docs/changes/2026-08-20-bugfix-skill-simplification/reviews/code-review-final-r3.md`

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/bugfix/SKILL.md` | Replaced the underspecified workflow with closed vocabularies, ordered gates, matrices, retry rules, claim limits, and explicit handoff. | Make every authority, proof, routing, and terminal-result decision deterministic without adding runtime machinery. | Spec R1-R27; plan M2 | Focused contract tests; semantic-preservation review |
| `tests/test_bugfix_skill_contract.py` | Added deterministic static scenarios for operation selection, bounded commands and writes, proof-first mutation, restoration, routing, retries, governed-signal failure, and claims. | Prove the complete contract and its failure paths directly. | Test spec T1-T14 | CMD1 and CMD2 |
| Package and adapter fixtures | Updated expected package content and parity assertions for the canonical one-file skill. | Ensure generated, packed, archived, release-candidate, and installed projections reproduce the canonical source. | Spec R25; plan M3 | CMD3-CMD9 and M3 package proof |
| Change-local evidence and reviews | Recorded baselines, measurements, semantic preservation, package proof, review findings and resolutions, CI coverage, and final review. | Preserve traceability and independent lifecycle settlement. | Workflow and plan closeout | Review structure and metadata validators |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T1-T5 | Closed operation, authority, defect-scope, and command/write behavior | Contract/static |
| T6-T9 | Proof-authoring gate, identical proof identity, correction eligibility, and validation | Contract/static |
| T10-T13 | Restoration basis, cause/owner consistency, retries, governed signals, and claims | Contract/static |
| T14 | Complete-package words and bytes are measured truthfully and never used as a semantic pass/fail ceiling | Measurement |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| Focused bugfix contract tests | 14 passed | `c2cc66b1a7056fc52c8820df05ae021f5a212dd7` |
| Canonical skill validation | passed | `c2cc66b1a7056fc52c8820df05ae021f5a212dd7` |
| Full Python suite | 446 passed, 16 skipped | `c2cc66b1a7056fc52c8820df05ae021f5a212dd7` |
| Skill boundary and build tests | passed | `c2cc66b1a7056fc52c8820df05ae021f5a212dd7` |
| Adapter distribution tests | 150 passed | `c2cc66b1a7056fc52c8820df05ae021f5a212dd7` |
| Build, metadata, and prose checks | passed | `c2cc66b1a7056fc52c8820df05ae021f5a212dd7` |
| Review-artifact structure and change metadata | passed | `b2ea37ed80270a2999efbaeb2c4777e3d58d7c37` |

The final skill measures 1,228 words and 10,215 bytes, compared with the 586-word and 3,761-byte baseline. No token estimate is claimed. The increase is accepted because the authored contract requires the additional semantics and the governing decision makes size diagnostic rather than normative.

## Review resolution summary

Four material code-review findings were accepted and resolved: ambiguous operation edges, a lost restoration distinction, insufficient deterministic edge proof, and malformed formal-review evidence fields. The closeout is recorded in `docs/changes/2026-08-20-bugfix-skill-simplification/review-resolution.md`; no finding remains open.

## Alternatives rejected

- Enforcing a strict word, byte, or token reduction was rejected because it would make brevity override truthful required behavior.
- Splitting the small package into conditional references was rejected because no genuine recurring loading boundary justified the added package complexity.
- Adding scripts, a debugging runtime, a persistent bug transaction, or target-agent acceptance was rejected as disproportionate to a Markdown contract correction.

## Scope control

The change does not add a new skill, modify bugfix lifecycle ownership, automate downstream review, integrate an issue or incident system, introduce a runtime repair engine, or change product code. It does not bulk-migrate unrelated skill packages.

## Risks and follow-ups

The always-loaded skill is larger than its baseline, so future editorial work should remove only demonstrated duplication while preserving the closed semantics. Acceptance is static and package-oriented; it does not claim that a live target agent repaired a real defect. No follow-up is required for this change.

## Workflow handback

Explanation status: current
Explanation basis: `2b7346abf0f8798dd3b49313dee936b1865cc4a1..c2cc66b1a7056fc52c8820df05ae021f5a212dd7`; final review `code-review-final-r3`
Validation-evidence cutoff: `c2cc66b1a7056fc52c8820df05ae021f5a212dd7`
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
