# Proposal Review R1: Workflow Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-08-11-workflow-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-workflow-skill-simplification.md`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: WFSIM-PR1, WFSIM-PR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-workflow-skill-simplification/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-08-11-workflow-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-workflow-skill-simplification/review-resolution.md
- Open blockers: governed read-only routing and validation ownership are not closed
- Immediate next stage: proposal revision

## Material Findings

### Finding WFSIM-PR1

Finding ID: WFSIM-PR1
Severity: major
Location: Recommended direction, Governed lifecycle reference; Trigger model and representative assemblies; Expected behavior changes
Evidence: The governed reference is loaded exactly when an invocation must “advance, resume, settle, or mutate” a governed record, while the reference also owns complete record inspection, identity resolution, and stale or contradictory state handling. A read-only audit, status explanation, or routing decision can depend on current `change.yaml` state without performing any of those four actions. The `WP0-route-audit` label and the statement that direct audits omit lifecycle procedure make it unclear whether such a governed read must load `governed-lifecycle-routing.md`. This ambiguity can either hide required evidence rules from a governed audit or load the reference more broadly than the reported profile model.
Required outcome: Define the governed predicate by evidence dependency, not mutation alone. Close the treatment of read-only audits, status requests, and route decisions that rely on current governed state, and update the representative assemblies and success measurements accordingly.
Safe resolution path: Load the governed reference whenever routing, audit, status, resume, settlement, or mutation depends on a current governed record. Reserve `WP0` for requests that can be answered without governed record semantics; rename it if necessary. State whether `$workflow auto: status` with no active run loads only automation command procedure or also governed lifecycle procedure, and add representative required and forbidden load cases.
needs-decision rationale: The proposal-owning stage must decide the resource boundary for governed read-only operations because it directly controls the claimed common-path reduction and safe evidence handling.

### Finding WFSIM-PR2

Finding ID: WFSIM-PR2
Severity: major
Location: Scope budget; Testing and verification strategy; Open questions
Evidence: The proposal says semantic ledgers fail closed, requires static scenario fixtures, proposes focused validators, and leaves the exact validator ownership split as an open question. It excludes a permanent simplicity validator but does not decide whether rule-disposition vocabularies, literal classifications, scenario fixtures, profile assembly, or duplication counts become permanent repository validation. That decision affects implementation scope, selector registration, long-term maintenance, and whether one-change evidence becomes a new validator family.
Required outcome: Separate permanent contract and package validation from change-local simplification evidence at proposal level.
Safe resolution path: Keep existing permanent owners for frontmatter, required sections, closed public vocabulary, Resource-map integrity, packaged-resource existence, and generated/archive/install parity. Keep semantic and literal ledgers, scenario fixtures, profile measurements, duplicate-cluster counts, and independent semantic review change-local. Explicitly prohibit a new workflow-simplicity validator, permanent profile-size gate, generic fixture framework, selector evidence class, or target-runtime journey.
needs-decision rationale: The proposal-owning stage must choose the durable validation boundary; downstream specification should not infer whether temporary simplification evidence becomes permanent infrastructure.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal identifies concrete common-path loading and duplicated ownership rather than treating size alone as the problem. |
| User value | pass | Faster, clearer routing and audit journeys are explicit. |
| Option diversity | pass | O0 through O4 cover defer, editorial, incremental extraction, packaged disclosure, and a state-engine alternative. |
| Decision rationale | pass | O3 follows three real authority boundaries and rejects unnecessary runtime architecture. |
| Scope control | concern | Product scope is bounded, but validation infrastructure scope remains open under WFSIM-PR2. |
| Architecture awareness | pass | The proposal reuses the package model and makes this change own architecture if `change.yaml` architecture later changes. |
| Testability | concern | Proof classes are strong, but the governed read-only profile and durable validation owner are ambiguous. |
| Risk honesty | pass | Authority, duplication, package drift, hidden profile growth, and architecture expansion are addressed. |
| Rollout realism | pass | Atomic package rollout and complete rollback are credible. |
| Readiness for spec | block | WFSIM-PR1 and WFSIM-PR2 require proposal-level decisions before requirements can define exact loading and proof ownership. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal is classified, including branch creation, proposal review, workflow rigor, and architecture ownership when `change.yaml` architecture changes.
- Scope-budget result: concern. Core package and architecture work are classified, but permanent versus change-local validation remains unresolved.
- Vision-fit result: pass. `fits the current vision` is valid and supported by reduced ceremony with preserved evidence and resumability.

## Recommended Proposal Edits

- Recommended edits: redefine `governed_change_context` to include any route, audit, status, settlement, resume, or mutation that depends on current governed state; narrow and rename `WP0` accordingly; add explicit no-active-run status behavior; and define permanent validation versus change-local evidence with a prohibition on new simplicity, profile, fixture-family, selector-evidence, and runtime-journey infrastructure.

## Recommendation

- Recommendation: revise the proposal to close WFSIM-PR1 and WFSIM-PR2, then run proposal-review R2. Do not proceed to specification until read-only governed loading and validation ownership are definitive. No automatic downstream handoff follows this review.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-11-workflow-skill-simplification/change.yaml` — passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-11-workflow-skill-simplification` — passed with one review and two recorded findings.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` — passed for the change-local proposal and review surfaces.
- `git diff --check` — passed.
