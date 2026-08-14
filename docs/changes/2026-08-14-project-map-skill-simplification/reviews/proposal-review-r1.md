# Proposal Review R1: Project-Map Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-14-project-map-skill-simplification.md`
Reviewed artifact: commit `08b4389e`
Review date: 2026-08-14
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PMAPSIM-PR1, PMAPSIM-PR2, PMAPSIM-PR3
- Open blockers: coordination-trigger coverage, universal dirty-baseline ownership, and result compatibility require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal selects a sound simplification model: a compact universal `SKILL.md`, one conditional maintenance and area-coordination reference, and the existing structural skeleton. Independent operation and scope axes correct a real ambiguity in the current four-mode model, and the proposal appropriately requires amendments to the governing specification and bounded architecture text instead of presenting a contract change as editorial cleanup.

The direction is close, but three contracts need proposal-level closure. The reference trigger does not cover root creation that discovers multi-map coordination, dirty-baseline truthfulness is partly placed behind a resource that root creation does not load, and the replacement of the public `Mode` field lacks an exact compatibility and migration decision.

## What is strong

### Universal evidence safety remains inline

The proposal keeps evidence classes, source ranking, claim citations, command truthfulness, runtime-observation limits, freshness meanings, stops, and downstream reliance in the main file. Those rules must apply before optional procedure is selected.

### The classification redesign reflects the domain

`create`, `refresh`, and `audit` are operations, while repository and area are scopes. Separating these axes produces clearer valid combinations than retaining `area` as a peer mode.

### Structural output retains one owner

The existing skeleton remains the only structural asset and does not acquire evidence or lifecycle policy. Removing duplicate label and section inventories from the main file is the right ownership direction.

### Measurement and acceptance stay proportionate

The proposal measures each loaded profile and the total package separately, treats size as evidence rather than policy, and excludes target-agent runtime execution and a new permanent simplicity validator.

## Material findings

### PMAPSIM-PR1 — Major: the reference trigger does not cover root creation that discovers area coordination

Finding ID: PMAPSIM-PR1
Severity: major
Location: Closed classification model; Conditional-reference ownership; Expected Behavior Changes
Evidence: `PM0-root-create` loads only `SKILL.md` and the skeleton, while the conditional reference owns root registration, parent/child rules, overlap ownership, contradiction handling, and missing-area behavior. A root-map creation can discover existing area maps, an orphaned area map, overlapping ownership, or a registration obligation during repository inspection. The current trigger therefore permits dependent multi-map decisions without loading their owning procedure. The proposal also does not close the allowed write sets or interrupted-write behavior for area creation plus root registration.
Required outcome: Define a positive coordination predicate in addition to operation and scope, require late loading before any dependent judgment or write, and enumerate the write boundary for each operation.
Safe resolution path: Add `map_coordination_context`, which is true for every area scope and whenever repository-scoped work discovers existing or proposed area maps, root registration, parent/child identity, overlap, contradiction, or missing-area handling. Load the reference for refresh, audit, or `map_coordination_context`. Permit `PM0-root-create` without the reference only after bounded inspection finds no coordination evidence. Define root-only creation as one-map write, area creation as an identity-bound area-map plus root-registration transaction, refresh as writes only to explicitly affected maps, and audit as read-only. Late discovery loads the reference before continuing; missing or ambiguous resources stop.
needs-decision rationale: none; the proposed ownership boundary already assigns multi-map coordination to the reference.

### PMAPSIM-PR2 — Major: universal dirty-baseline truthfulness is placed behind conditional loading

Finding ID: PMAPSIM-PR2
Severity: major
Location: Universal ownership in `SKILL.md`; Conditional-reference ownership; Testing and Verification Strategy
Evidence: The proposal keeps “baseline truthfulness” inline but assigns “dirty-baseline reconciliation” to the conditional reference. The approved project-map contract applies dirty-baseline reporting to creation as well as refresh. `PM0-root-create` does not normally load the reference, yet it must still distinguish a clean commit from inspected uncommitted state and record the inspected dirty paths. The ownership split is therefore not executable without either weakening root-create evidence or duplicating procedure.
Required outcome: Keep the complete minimum dirty-baseline truthfulness rule available to every profile and reserve only maintenance-specific comparison for the reference.
Safe resolution path: Keep inline the rule that, when Git is available and inspected evidence includes uncommitted changes, the map records `<sha>+dirty` and the inspected uncommitted paths; when Git is unavailable, it records the actual evidence baseline without inventing a commit identity. Let the conditional reference own comparison of previous and current baselines, changed-path targeting, correction notes, and recovery across maintenance runs. Update ownership, scenarios, rule disposition, and acceptance criteria accordingly.
needs-decision rationale: none; truthful current-state evidence is universal under the existing contract.

### PMAPSIM-PR3 — Major: operation/scope output compatibility is not a closed migration contract

Finding ID: PMAPSIM-PR3
Severity: major
Location: Expected Behavior Changes; Testing and Verification Strategy; Open Questions
Evidence: The current published result contract and validator fixtures require `Mode: <create|refresh|area|audit>`. The proposal says results will report operation and scope separately, but it leaves the exact old-mode-to-new-profile mapping to the specification and does not select field labels, compatibility behavior, or treatment of existing literal consumers. A later specification could preserve the ambiguous `Mode` field, emit both contracts indefinitely, or remove parser-sensitive literals without an atomic migration.
Required outcome: Select one exact new result vocabulary and a read-old/write-new compatibility boundary at proposal level.
Safe resolution path: New results should emit `Operation: <create|refresh|audit>` and `Map scope: <repository|area:slug>` and should not emit the legacy `Mode` field. Existing map artifacts remain unchanged because this is an invocation-result migration, not a content migration. Define the old mapping as `create → create/repository`, `refresh → refresh/repository` unless an explicit area target exists, `audit → audit/repository` unless an explicit area target exists, and `area → the requested operation/area`, stopping when the operation cannot be resolved. Inventory literal consumers, preserve or atomically migrate normative and parser/package contracts, update incidental tests, and retain historical fixtures only where they prove old artifact readability.
needs-decision rationale: none; the proposal has already selected independent operation and scope axes.

## Architecture assessment

Architecture assessment is required because the current architecture explicitly records the four-mode classifier and says refresh triggers stay inline. The expected result is a bounded architecture documentation update with no ADR: the published-skill package model, canonical source, generated parity, artifact locations, and lifecycle authority remain unchanged. A new ADR is needed only if implementation introduces an independent policy owner, runtime, persistence mechanism, package transformation, or lifecycle responsibility.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-PMAPSIM-001` | Reference loading uses a positive `map_coordination_context` in addition to operation and scope. |
| `AC-PMAPSIM-002` | Root creation without coordination evidence remains self-sufficient from `SKILL.md` and the skeleton. |
| `AC-PMAPSIM-003` | Late discovery of area coordination loads the required reference before dependent judgment or writes. |
| `AC-PMAPSIM-004` | Root create, area create, refresh, and audit have explicit allowed write sets and recovery behavior. |
| `AC-PMAPSIM-005` | Every profile can report a dirty inspected baseline truthfully without depending on maintenance procedure. |
| `AC-PMAPSIM-006` | Maintenance-only baseline comparison and correction remain owned by the conditional reference. |
| `AC-PMAPSIM-007` | New invocation results use closed `Operation` and `Map scope` fields. |
| `AC-PMAPSIM-008` | New results do not preserve the ambiguous legacy `Mode` field. |
| `AC-PMAPSIM-009` | Every legacy mode has one deterministic mapping or an explicit ambiguity stop. |
| `AC-PMAPSIM-010` | Normative and parser-sensitive literal consumers migrate atomically; incidental tests do not own prose. |
| `AC-PMAPSIM-011` | Existing project-map artifacts remain readable and are not rewritten solely for this migration. |
| `AC-PMAPSIM-012` | Every loaded profile decreases unless a specific semantic-preservation exception is independently approved. |
| `AC-PMAPSIM-013` | No target-agent runtime executes during acceptance. |
| `AC-PMAPSIM-014` | Canonical, generated, archived, and installed resources retain required parity. |

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload, overlapping modes, and duplicated structural ownership are concrete and measured. |
| User value | pass | Root creation and bounded audits should become easier to classify and scan. |
| Option diversity | pass | Unchanged, inline compression, one-reference, fragmented, and executable-engine options are materially different. |
| Decision rationale | pass | One conditional reference plus one existing asset is proportionate. |
| Vision fit | pass | The direction improves reusable orientation while preserving evidence and traceability. |
| Scope control | pass | Runtime mapping, historical rewriting, adjacent skills, and permanent size policy remain excluded. |
| Trigger model | block | Root creation can discover coordination procedure that its declared profile does not load. |
| Evidence ownership | block | Dirty-baseline truthfulness is universal but partly assigned to the conditional reference. |
| Compatibility | block | The replacement result vocabulary and legacy mode migration are not closed. |
| Structural ownership | pass | The skeleton remains the sole layout owner and procedure remains policy-owning. |
| Testing boundary | pass | Static scenarios, package proof, and semantic review are proportionate; runtime execution is excluded. |
| Measurement | pass | Loaded profiles and total package size are reported separately. |
| Architecture awareness | pass | The proposal correctly requires a bounded update to current architecture text. |
| Readiness for spec | changes-requested | PMAPSIM-PR1 through PMAPSIM-PR3 require proposal revision. |

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; core, same-slice, and excluded work are explicitly classified with reasons
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Record path: `docs/changes/2026-08-14-project-map-skill-simplification/reviews/proposal-review-r1.md`
- Recording blocker: none
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review log: `docs/changes/2026-08-14-project-map-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-project-map-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-14-project-map-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

Revise the proposal to resolve PMAPSIM-PR1 through PMAPSIM-PR3, then rerun independent `proposal-review` against a frozen revision. No automatic downstream handoff follows this review.

