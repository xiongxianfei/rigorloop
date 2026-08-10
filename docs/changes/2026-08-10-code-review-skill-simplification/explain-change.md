# Code-Review Skill Simplification Explain Change

## Summary

This change makes the published `code-review` skill materially smaller on the
ordinary review path while preserving its review, recording, status, stop,
claim-boundary, milestone, and handoff contract. Universal policy remains in
`SKILL.md`; workflow-managed automation procedure now lives in one explicitly
mapped conditional reference; and the existing assets remain the sole owners of
repeated output structure.

The completed implementation reduced `SKILL.md` from 4,514 to 2,647 words and
from 8,160 to 4,813 estimated tokens, a 41.4 percent word reduction and a 41.0
percent token reduction. The complete package also became smaller, from 5,569
to 4,588 words and from 10,116 to 8,518 estimated tokens. All seven identified
duplication clusters now have one owner, and the skill has no inline output
template duplication.

## Problem

The prior skill mixed universal review rules with repeated guidance, inline
output structures, shared boundary detail, and workflow-managed automation
procedure. A direct review therefore loaded and navigated content that applied
only to an armed automated correction loop. Simply deleting prose or enforcing
a size percentage would risk weakening the public review contract.

## Decision trail

- Proposal option O3 was selected: consolidate the core and progressively
  disclose conditional policy.
- Proposal review required three closures: choose the conditional-reference
  ownership model, exclude target-agent execution from acceptance, and judge
  success through rule ownership and semantic preservation rather than a hard
  percentage gate.
- Requirements `R1` through `R25` define package ownership, inline universal
  rules, conditional loading, deterministic packaging, fail-closed fixtures,
  measurements, compatibility, and non-runtime proof.
- The architecture amendment defines a published skill as its canonical
  `SKILL.md` plus explicitly mapped references and assets, with lifecycle and
  policy ownership remaining at the skill level.
- M1 froze rule ownership and acceptance fixtures; M2 performed the package
  refactor and focused validator changes; M3 proved package parity, semantic
  preservation, compatibility, and measured reduction.
- The M1, M2, M3, and final holistic code reviews were all approved with no
  material implementation findings.

## Diff rationale by area

| Area | Change | Reason | Source and proof |
| --- | --- | --- | --- |
| `skills/code-review/SKILL.md` | Reorganized the common path around purpose, authority, stops, review sequence, finding/status rules, recording, claims, handoff, and resource loading; removed repeated templates and conditional automation detail. | Keeps every direct or isolated review self-sufficient while eliminating common-path repetition. | `R1`-`R8`, `R10`, `R17`, `R19`; T2-T6, T8, T12; M2 and semantic-preservation evidence. |
| `skills/code-review/references/workflow-managed-automated-review.md` | Added the single conditional procedure for formally armed workflow-managed automated review or correction loops. | Automation phases, packets, correction classification, bounded rereview, promotion, pause, and failure behavior do not need to load for ordinary reviews. | `R5`-`R7`, `R23`-`R25`; T3-T5, T13-T14; CMD3 and CMD6. |
| Existing `skills/code-review/assets/` | Retained the mapped review-result and finding assets as the only repeated output structures. | Prevents inline and asset templates from drifting while leaving policy in `SKILL.md`. | `R4`, `R7`, `R11`, `R21`-`R22`; T4, T6-T8. |
| `scripts/skill_validation.py` | Added a narrow allowlist for the exact workflow-managed automation reference mapping. | The existing deterministic validator owns mapped-resource structure; the change extends that owner instead of creating a new validator family. | `R4`, `R8`-`R10`, `R15`-`R16`; CMD2 and CMD3. |
| `scripts/test-skill-validator.py` | Added focused package tests for inline ownership, the exact load trigger, reference contents, asset ownership, vocabulary preservation, and forbidden runtime machinery. | Proves the structural contract and routing without executing a model runtime. | T2-T6, T8-T10, T13-T14; 290 tests passed with 16 governed skips. |
| Rule ledger and fixtures | Added 22 stable rule dispositions, seven representative static scenarios, and an invalid unknown-disposition fixture. | Ensures no behaviorally significant rule silently disappears and unknown dispositions fail closed before consistency checks. | `R2`, `R9`, `R13`, `R15`-`R16`, `R18`, `R20`; T1, T9-T10; CMD1. |
| Measurement and semantic evidence | Recorded exact before/after common-path and total-package metrics and an independent semantic checklist. | Separates context reduction from maintenance footprint and keeps 35-45 percent as a planning target rather than an unsafe acceptance threshold. | `R12`-`R14`, `R17`; T11-T12; CMD10, CMD11, MP1. |
| Architecture, proposal, spec, test spec, plan, and review records | Recorded the package-boundary decision, executable contract, proof map, milestones, review revisions, and closeout evidence. | Makes the non-trivial published-contract change traceable and reviewable under the repository lifecycle. | Approved governing artifacts and change-local review records. |

## Tests added or changed

- The focused skill-validator tests prove direct-review sufficiency, exact
  conditional loading, universal-policy placement, asset-only output structure,
  closed vocabulary preservation, mapped-resource integrity, and absence of
  target-runtime acceptance machinery.
- The fixture contract proves the seven required scenarios with explicit
  required and forbidden outcomes. The invalid ledger fixture proves that an
  unknown disposition fails closed.
- Existing adapter-distribution tests and the trusted `v0.3.6` temporary archive
  command prove that Codex, Claude, and opencode packages include the canonical
  skill, conditional reference, and assets and install them into clean temporary
  trees. These checks execute no target agent.
- MP1 independently checked trigger clarity, ownership, prerequisites,
  operating sequence, evidence, stop conditions, claim boundaries, outputs,
  handoff, and the conditional load trigger.

## Validation evidence available before final verify

- CMD1 passed with 22 ledger rules, seven scenarios, and the unknown disposition
  rejected.
- `python scripts/validate-skills.py skills/code-review/SKILL.md` passed.
- `python scripts/test-skill-validator.py` passed 290 tests with 16 governed
  skips.
- `python scripts/build-skills.py --check` passed against a temporary generated
  tree.
- `python scripts/test-adapter-distribution.py` passed.
- Corrected CMD6 generated and validated trusted `v0.3.6` Codex, Claude, and
  opencode archives and clean installations for `code-review`.
- `python scripts/validate-boundary-first.py --check --path specs/code-review-skill-simplification.md`
  passed.
- CMD10 and CMD11 produced the recorded common-path and total-package metrics.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-10-code-review-skill-simplification`
  and `python scripts/validate-change-metadata.py docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`
  passed after the final holistic review.
- Final verification has not yet been claimed; the `verify` stage will rerun the
  required proof on the reviewed branch state.

## Review resolution summary

Earlier authoring reviews produced material findings and every finding has a
final disposition in `review-resolution.md`; none remains open or
`needs-decision`. The implementation reviews for M1, M2, M3, and the final full
diff were clean, so they introduced no implementation finding requiring a new
resolution entry.

## Alternatives rejected

- Keeping the skill unchanged would preserve unnecessary common-path loading.
- Deduplicating only inside `SKILL.md` would leave automation-only procedure on
  every direct review path.
- Replacing the skill with a generic checklist would remove lifecycle rigor and
  repository-specific claim boundaries.
- A normative 35-45 percent reduction gate was rejected because semantic
  preservation must override numeric optimization.
- A new token-budget, prose-quality, or code-review-specific permanent
  validator was rejected because these measurements are change evidence, not
  durable product invariants.
- Prompt journeys, transcript grading, and Codex, Claude, opencode, or other
  target-agent execution were rejected as acceptance proof.

## Scope control

- Review status, severity, formal recording, isolation, milestone settlement,
  rereview, and downstream authority semantics are unchanged.
- The change does not create a new lifecycle owner, runtime, selector,
  scheduler, persistent state, external dependency, or model-behavior test
  system.
- Existing boundary-first guidance and structural assets remain governed by
  their established owners.
- Generated adapter archives remain derived output; canonical authorship stays
  under `skills/`.

## Risks and follow-ups

- The main residual risk is future drift between universal and conditional
  policy. The exact resource mapping, package tests, rule ledger, and existing
  generated-package parity checks constrain that risk.
- Token estimates are approximate and intentionally remain evidence rather than
  a permanent gate.
- CMD6 originally used an untrusted synthetic version and correctly failed
  before installation. The test spec was revised and rereviewed to use immutable
  trusted fixture `v0.3.6`; no production behavior changed.
- PR preparation remains a separate downstream stage and is outside this
  workflow target.

## Readiness

All implementation milestones and the final holistic code review are closed.
This explanation is complete and the change is ready to enter final `verify`.
It does not claim branch readiness or PR readiness before that stage runs.
