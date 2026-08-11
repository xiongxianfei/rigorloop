# Proposal Review R2: Workflow Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-08-11-workflow-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-workflow-skill-simplification.md`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: WFSIM-PR3, WFSIM-PR4, WFSIM-PR5
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-workflow-skill-simplification/reviews/proposal-review-r2.md
- Review log: docs/changes/2026-08-11-workflow-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-workflow-skill-simplification/review-resolution.md
- Open blockers: automation bootstrap, reference ownership, and required-resource failure behavior are not closed
- Immediate next stage: proposal revision

## Material Findings

### Finding WFSIM-PR3

Finding ID: WFSIM-PR3
Severity: major
Location: Recommended direction, Bounded automation reference; Trigger model and representative assemblies
Evidence: The proposal says `armed_automation_context` implies an existing `governed_change_context`, but its new-target row loads both references before a governed record exists and then establishes that identity. It therefore uses governed context to mean both an already valid record and a record that may be created during bootstrap. The assembly table also says guide authoring is independently additive without deciding the governed-plus-automation-plus-guide combination.
Required outcome: Define a non-circular automation-command bootstrap state, distinguish command context from durable armed context, and close every supported predicate combination.
Safe resolution path: Add `automation_command_context`; reserve `armed_automation_context` for current durable authorization bound to an existing governed record; introduce transient `WPB-automation-bootstrap`; load automation command/bootstrap procedure first, establish and validate governed identity, then load governed procedure and persist authorization. Make workflow-guide authoring and active automation mutually exclusive within one first-version invocation.
needs-decision rationale: The proposal owner must choose the bootstrap and combined-context contract because it determines when durable authority exists and which resource assemblies are valid.

### Finding WFSIM-PR4

Finding ID: WFSIM-PR4
Severity: major
Location: Universal `SKILL.md` contract; Governed lifecycle reference; Bounded automation reference; Workflow-guide authoring reference; Ownership and duplication rules
Evidence: The automation reference owns architecture-assessment routing, gate promotion, and target completion while the governed reference owns stage transitions, final review, settlement, and closeout. Those lists can produce competing answers about applicability and the next stage. The guide-authoring reference owns source rank, unknown-artifact handling, and general customer-project fallback even though ordinary routing requires those safeguards before guide authoring is triggered.
Required outcome: Establish one non-overlapping ownership table, keep universal routing safeguards inline, and define a strict dependency direction among references.
Safe resolution path: Keep source rank, evidence precedence, unknown-artifact behavior, isolation, and universal stops inline. Give the governed reference exclusive ownership of lifecycle applicability, architecture assessment, stage transition, settlement, milestone, final-review, and closeout routing. Limit automation to commands, authorization, target identity, receipts, budgets, correction cycles, pause/cancel/resume, and asking governed procedure for the next valid transition. Limit guide authoring to creating or refreshing the guide, using the skeleton, recording customizations, and migration notes. Add a contradiction-is-package-defect stop rule.
needs-decision rationale: The proposal owner must settle the policy-owner boundaries; downstream specification cannot safely infer precedence between potentially competing references.

### Finding WFSIM-PR5

Finding ID: WFSIM-PR5
Severity: major
Location: Goals; Universal `SKILL.md` contract; Testing and verification strategy; Rollout and rollback; Stop conditions not yet proposed
Evidence: Governed mutation, automation, and guide authoring intentionally depend on mapped references and the guide skeleton, but the proposal defines only build-time parity and atomic rollout. It does not define invocation-time behavior when a required resource is missing, unreadable, or from a mixed package version. The shortened main file could otherwise invite remembered or partially reconstructed procedure.
Required outcome: Make unavailable required packaged resources an explicit package-integrity stop condition and prohibit fallback invention.
Safe resolution path: Continue from `SKILL.md` only when no conditional trigger applies. Stop before governed interpretation or mutation when the governed reference is unavailable; before any target, status, resume, or cancellation action when automation procedure is unavailable; and before guide writes when the guide reference or skeleton is unavailable. Treat unreadable or mixed-version resources as package-integrity blockers and prohibit reconstructing procedure from memory. Do not add runtime hash verification.
needs-decision rationale: The proposal owner must choose the runtime fail-safe boundary because progressive disclosure is unsafe if required procedure can be silently reconstructed or skipped.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and repeated policy ownership remain concrete. |
| User value | pass | Generic routing and audit should become easier without weakening governed behavior. |
| Option diversity | pass | The proposal compares deferral, inline editing, limited extraction, bounded disclosure, and an executable engine. |
| Decision rationale | pass | O3 remains the strongest direction. |
| Scope control | pass | Runtime engines, permanent simplicity validation, other skills, and target-agent testing remain excluded. |
| Architecture awareness | concern | The expected no-architecture outcome is plausible, but reference dependency and ownership must be closed first. |
| Testability | concern | Static scenarios and package proof are appropriate, but bootstrap and missing-resource cases are not fully specified. |
| Risk honesty | pass | Semantic drift, package growth, authority, validator scope, and architecture expansion are visible. |
| Rollout realism | concern | Atomic packaging is covered; incomplete-install runtime behavior is not. |
| Readiness for spec | block | WFSIM-PR3 through WFSIM-PR5 require proposal-owned decisions. |

## Scope Preservation Review

- Scope-preservation result: pass. Every initial user goal remains classified and the architecture-ownership condition is retained.
- Scope-budget result: pass. Core resources, package proof, change-local evidence, architecture assessment, and exclusions are explicitly classified.
- Vision-fit result: pass. `fits the current vision` remains consistent with traceability, resumability, and reduced ceremony.

## Recommended Proposal Edits

- Recommended edits: add automation-command context and transient bootstrap; close every predicate combination and disallow active automation plus guide authoring; replace overlapping responsibility lists with one ownership table and dependency direction; keep source-rank and unknown-artifact safeguards inline; and add required-resource package-integrity stops with no fallback reconstruction.

## Recommendation

- Recommendation: revise the proposal to close WFSIM-PR3, WFSIM-PR4, and WFSIM-PR5, then run proposal-review R3. Do not proceed to specification until the trigger lattice, ownership boundaries, and missing-resource behavior are definitive. No automatic downstream handoff follows this isolated review.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-11-workflow-skill-simplification/change.yaml` — passed.
- `python scripts/validate-review-artifacts.py docs/changes/2026-08-11-workflow-skill-simplification` — passed with two reviews and five recorded findings.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` — passed for the proposal and R2 review surfaces.
- Whitespace checks for the proposal and change-local artifacts — passed.
