# Proposal Review R2: Code-Review Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: external user-supplied proposal reviewer
Target: docs/proposals/2026-08-10-code-review-skill-simplification.md
Reviewed artifact: docs/proposals/2026-08-10-code-review-skill-simplification.md
Review date: 2026-08-10
Status: changes-requested
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: CRSIM-PR1, CRSIM-PR2, CRSIM-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-10-code-review-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-10-code-review-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-10-code-review-skill-simplification/review-resolution.md`
- Open blockers: proposal direction is not closed on conditional-reference ownership, runtime acceptance, or success measurement
- Immediate next stage: proposal revision; no automatic downstream handoff

## Overall assessment

The proposal identifies the correct problem and selects the correct broad direction: deduplicate the common review contract, keep universal safety rules inline, use assets as the sole structural output source, conditionally load automation-only procedure, and report common-path and total-package size separately.

The proposal is not ready for specification because three proposal-level decisions remain unresolved.

## Material Findings

### Finding CRSIM-PR1

Finding ID: CRSIM-PR1
Severity: major
Location: `Recommended Direction`, conditional automation-reference paragraphs
Evidence: The proposal chooses progressive disclosure but leaves two materially different package designs open: a mapped conditional reference or compressed inline automation policy. The unresolved fallback defers the mechanism responsible for most expected common-path reduction to specification.
Required outcome: Select one package-level ownership model and define which universal rules remain inline versus which automation-only procedure moves to the reference.
Safe resolution path: Select `skills/code-review/references/workflow-managed-automated-review.md`; define the governing published skill as `SKILL.md` plus explicitly mapped references and structural assets while keeping ownership at `code-review`; keep universal purpose, authority, checklist, finding/status vocabulary, recording, proof, stop, claim, handoff, milestone, and resource-load rules inline; move only workflow-managed automation phases, packet handling, risk and auto-fix classification, bounded correction, receipts, and automation-specific pause handling.
needs-decision rationale: none; the review supplies the proposal-level decision.

### Finding CRSIM-PR2

Finding ID: CRSIM-PR2
Severity: major
Location: `Testing and Verification Strategy` and `Non-goals`
Evidence: Scenario testing is named without distinguishing deterministic fixtures and semantic review from live Codex, Claude Code, opencode, or other target-runtime execution. That ambiguity could recreate the runtime behavior-certification system rejected by the governing repository-simplification direction.
Required outcome: Explicitly exclude target-agent execution, prompt journeys, transcript grading, and runtime-version evidence from acceptance.
Safe resolution path: Define exactly three proof classes: deterministic structural proof, fixture-based contract proof, and independent semantic review of the final skill package and rule-disposition ledger. State that no target agent runtime is used for implementation, verification, release, or acceptance.
needs-decision rationale: none; the higher-priority published-skill-first contract already assigns runtime behavior evaluation outside repository acceptance.

### Finding CRSIM-PR3

Finding ID: CRSIM-PR3
Severity: major
Location: `Recommended Direction`, reduction target; `Open Questions`; success and measurement model
Evidence: The proposal introduces a 35–45 percent target but does not decide whether it is normative. A hard percentage could encourage unsafe compression, while no closed success model could permit a rewrite that leaves duplication materially unchanged.
Required outcome: Define success through complete rule ownership and material common-path reduction, with numeric size measurements as supporting evidence rather than the semantic gate.
Safe resolution path: Require a change-local `code-review-rule-disposition.yaml` with stable rule IDs and closed dispositions `retained-inline`, `retained-conditional-reference`, `asset-owned`, `removed-duplicate`, or `removed-obsolete-with-approved-contract-change`; account for every behaviorally significant rule; report main-file, conditional-reference, total-package, duplication-cluster, template, and resource metrics; keep 35–45 percent as a planning target; prohibit a new permanent token, line-count, or prose-quality validator.
needs-decision rationale: none; the review supplies the proposal-level acceptance model.

## Review Dimensions

- Problem clarity: pass
- User value: pass
- Option diversity: pass
- Decision rationale: concern; O3 is sound but its package mechanism is not selected definitively
- Scope control: pass
- Architecture awareness: pass with revision; the package boundary requires an architecture assessment
- Testability: block; target-runtime execution is not yet explicitly excluded
- Risk honesty: pass
- Rollout realism: pass
- Readiness for spec: block until CRSIM-PR1 through CRSIM-PR3 are resolved and rereviewed

## Scope Preservation Review

- Scope-preservation result: pass.
- The requested simplification, behavior preservation, branch, proposal, and review outcomes remain visible.
- The required revisions clarify mechanism and proof without broadening into cross-skill rewriting or unrelated validator retirement.

## Recommended Proposal Edits

- Select the conditional-reference model without an inline fallback.
- Add an exact inline-versus-reference ownership table and package-level governing-skill definition.
- Exclude every target-agent runtime and model-output proof path from acceptance.
- Require deterministic scenario fixtures, independent semantic review, and a rule-disposition ledger.
- Make 35–45 percent a non-normative target and prohibit a permanent simplicity validator.
- Add architecture assessment as the next required artifact after proposal approval.

## Recommendation

- Recommendation: changes-requested. Revise the proposal to close CRSIM-PR1, CRSIM-PR2, and CRSIM-PR3, then run proposal-review again.
- This review is isolated and performs no automatic downstream handoff.
