# Proposal Review R2: Project-Map Skill Simplification

Review ID: proposal-review-r2
Stage: proposal-review
Round: r2
Reviewer: independent proposal-review context supplied by the user
Target: `docs/proposals/2026-08-14-project-map-skill-simplification.md`
Reviewed artifact: commit `3c31023a`
Review date: 2026-08-14
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PMAPSIM-R2-PR1, PMAPSIM-R2-PR2, PMAPSIM-R2-PR3
- Open blockers: target-state operation selection, coordination preflight and assembly accounting, and recoverable area creation require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, or continue the workflow

## Overall assessment

The proposal retains the correct simplification boundary: a compact universal `SKILL.md`, one conditional maintenance and coordination reference, one existing structural skeleton, and independent operation and scope axes. Universal evidence meanings, source ranking, command truthfulness, claim boundaries, and reliance safety remain inline, while detailed refresh and multi-map procedure move behind one genuine conditional boundary.

Three operational contracts remain insufficiently closed. Operations are not bound deterministically to target existence, the negative coordination decision lacks a bounded evidence contract and assembly model, and the proposed two-map area-creation transaction lacks complete prerequisites, commit order, and recovery semantics.

## Material findings

### PMAPSIM-R2-PR1 — Major: operation selection is not tied to target existence and current state

Finding ID: PMAPSIM-R2-PR1
Severity: major
Location: Closed classification model; write boundaries; Expected Behavior Changes
Evidence: Root `create` may “create or replace” an existing map, allowing refresh behavior to bypass baseline comparison, correction notes, affected-section analysis, and maintenance recovery. Audit can also be followed by correction without saying whether that mutation remains part of audit or becomes a new refresh operation.
Required outcome: Bind `create`, `refresh`, and `audit` to resolved target state and make audit permanently read-only.
Safe resolution path: Permit create only for an absent resolved target, require refresh for every existing target including full rewrites, permit refresh only for an existing resolvable target, treat audit of a missing target as a read-only `missing-map` finding, and require every post-audit correction to begin a separately classified refresh with fresh evidence resolution.
needs-decision rationale: none; these are closed operation semantics selected by the proposal.

### PMAPSIM-R2-PR2 — Major: no-coordination proof and loaded assemblies are underspecified

Finding ID: PMAPSIM-R2-PR2
Severity: major
Location: Closed classification model; coordination predicate; Testing and Verification Strategy
Evidence: `PM0-root-create` may omit the reference only when bounded inspection finds no coordination evidence, but the proposal does not name the minimum ownership surfaces that must be checked. The same semantic profile may load either the common package or the conditional reference, so profile measurement does not identify the actual loaded assembly.
Required outcome: Define a bounded coordination preflight and represent semantic operation/scope classifications separately from loaded-resource assemblies.
Safe resolution path: Inspect project-local workflow guidance, canonical and configured root and area-map locations, existing registration rows when present, known area-map files, request-supplied coordination evidence, and directly referenced active-change paths. Treat unavailable, conflicting, or ambiguous surfaces as requiring the reference or a stop. Retain six semantic classifications but define `PMA0-simple-root-create` and `PMA1-maintenance-or-coordinated` as the measured procedural assemblies.
needs-decision rationale: none; the proposal already separates evidence-based loading from operation and scope.

### PMAPSIM-R2-PR3 — Major: area creation lacks a recoverable two-map transaction

Finding ID: PMAPSIM-R2-PR3
Severity: major
Location: Closed write boundaries; Risks and Mitigations; Testing and Verification Strategy
Evidence: Area creation is described as an identity-bound area-map and root-registration transaction, but the proposal does not require an existing valid root, identify the full transaction basis, choose a write order or commit point, or distinguish recoverable matching partial state from orphaned, dangling, conflicting, stale, or ambiguous state.
Required outcome: Define area-creation prerequisites, identity basis, write ordering, commit point, and a complete partial-state recovery matrix.
Safe resolution path: Require one existing valid root map; bind root path and content identity, area slug and normalized path, parent identity, evidence baseline, and expected registration row; prepare and validate the area first; re-read the root before registering; write registration last as the commit point; reconcile only exact matching partial states; and stop on dangling, conflicting, changed-root, unrelated, or ambiguous states.
needs-decision rationale: none; the proposal already selected two-map coordination and must make it executable.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload, overlapping modes, and duplicated structure are concrete. |
| User value | pass | Simple root creation and bounded audits should become easier to scan. |
| Option diversity | pass | Inline compression, one reference, fragmented references, and executable mapping are materially distinct. |
| Decision rationale | pass | One conditional maintenance and coordination reference is appropriate. |
| Vision fit | pass | The direction improves trustworthy repository orientation without changing project vision. |
| Scope control | pass | Work remains limited to project-map and directly coupled contract, architecture, validation, and packaging surfaces. |
| Operation model | block | Create overlaps refresh, and audit correction is not isolated. |
| Coordination trigger | block | Negative coordination evidence and actual loaded assemblies are not closed. |
| Multi-map consistency | block | Area creation lacks complete transaction and recovery semantics. |
| Structural ownership | pass | The existing skeleton remains the correct sole structural owner. |
| Compatibility | pass with revisions | Operation and scope migration is sound after operation semantics are closed. |
| Measurement | concern | Coordinated root creation must be measured as a separate loaded assembly. |
| Testing boundary | pass | Static proof and package parity are proportionate; target-agent execution is excluded. |
| Architecture awareness | pass | A bounded architecture update is correctly required. |
| Readiness for spec | changes-requested | PMAPSIM-R2-PR1 through PMAPSIM-R2-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; all initial goals remain classified and the scope budget exposes same-slice dependencies without hidden follow-up work

## Recommended Proposal Edits

- Recommended edits: bind operations to target state, define the coordination preflight and two procedural assemblies, and close the area-creation transaction and recovery matrix

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass; core, same-slice, and excluded work remain explicitly classified
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-14-project-map-skill-simplification/reviews/proposal-review-r2.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r2
- Review record: `docs/changes/2026-08-14-project-map-skill-simplification/reviews/proposal-review-r2.md`
- Review log: `docs/changes/2026-08-14-project-map-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-project-map-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-14-project-map-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview

## Recommendation

Revise the proposal to resolve PMAPSIM-R2-PR1 through PMAPSIM-R2-PR3, then rerun independent proposal review against a frozen revision. No automatic downstream handoff follows this review.
