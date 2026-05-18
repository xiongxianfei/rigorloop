# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md
Reviewed artifact: docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Review Inputs

- Proposal: `docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`
- Vision: `VISION.md`
- Workflow guidance and review-recording guidance: `docs/workflows.md`
- Related accepted proposal context: `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`, `docs/proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md`
- Existing proposal-review record patterns under `docs/changes/`

## Findings

### CPS-PR1

Finding ID: CPS-PR1
Severity: major
Location: `docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md:717`

Evidence: The revised proposal includes the previously requested first-slice boundary, repository mode boundary, missing-guidance behavior, static-check precision, safety-preservation checklist, mandatory generated-adapter validation for public skill changes, `project-map` caveat, and focused spec path. The `Readiness` section still says `Changes requested before spec/plan.` and line 719 says the draft is ready for proposal-review re-check after those additions.

Required outcome: Align the `Readiness` section with the current proposal state before downstream spec or planning relies on the proposal.

Safe resolution path: Update `Readiness` to state readiness for focused spec after proposal acceptance, or intentionally keep the proposal blocked and record the remaining blocker. Then rerun proposal-review.

## Outcome

- Review status: changes-requested
- Material findings: CPS-PR1
- Blocking findings: none
- Recording: detailed review record, review log, and open review-resolution entry recorded
- Isolation: direct proposal-review request stops here and does not automatically continue into spec

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal states the real product boundary: public skills cannot require RigorLoop repository-internal docs in customer projects. |
| User value | pass | The benefit is concrete: installed skills become usable, cheaper to operate, and less brittle outside this repository. |
| Option diversity | pass | The proposal compares no change, copying internal docs into customer projects, and embedding a concise portable operating contract. |
| Decision rationale | pass | The recommended portable contract follows from the need to preserve rigor without runtime dependence on absent internal artifacts. |
| Scope control | pass | The first slice is now audit-first, updates only required or misleading internal-document dependencies, and forbids broad uniform rewrites. |
| Architecture awareness | pass | The proposal identifies the public skill surface, workflow guidance, validator checks, token reports, and generated adapter validation boundary without claiming runtime architecture changes. |
| Testability | pass | The behavior can be specified through mode rules, missing-guidance behavior, static-check boundaries, migration notes, token measurement, and adapter temp-output validation. |
| Risk honesty | pass | The proposal names vague skill wording, deleted safety rules, brittle static checks, missing local workflow docs, and overbroad skill changes. |
| Rollout realism | pass | Audit, selected wording changes, static checks, measurement, review, and release consideration form a realistic staged rollout. |
| Readiness for spec | concern | The direction is ready for a focused spec, but the proposal's own readiness text still records changes requested before spec/plan. |

## Scope Preservation

Pass. The proposal visibly classifies the user's initial goals: customer-project portability, avoiding internal-doc reliance, token-cost simplification, concise public skills, rigor preservation, and avoiding unrelated product features are all in scope or explicitly out of scope.

## Vision Fit Review

Pass. Root `VISION.md` exists and the proposal uses the allowed value `fits the current vision`. The direction supports RigorLoop's vision by keeping AI-assisted changes traceable while making installed skill behavior practical in real customer projects.

## Standing Artifact Gate Review

Pass. Root `VISION.md` and `CONSTITUTION.md` exist. The proposal changes public skill contract behavior and correctly routes next work through a focused spec rather than bypassing standing artifact gates.

## Adversarial Checks

- Bad investment trigger: the proposal would be a poor investment if it became a broad rewrite of every skill. The first-slice boundary mitigates this with audit-first selection.
- Simpler option considered: no change was considered and rejected because it leaves customer-installed skills brittle.
- Deferred architecture cost: runtime architecture is unaffected; validator and adapter-output validation remain the main implementation boundaries.
- User confusion risk: customers could confuse local `specs/` with RigorLoop internal specs. The repository mode boundary and static-check precision address this.
- Behavior that should not change: safety-critical review, verification, material-finding, mutation-safety, release-boundary rules, generated adapter source boundaries, and unrelated CLI features remain out of scope.
- Test proving value: a focused spec can require static checks plus audit evidence proving touched skills no longer require RigorLoop repository-internal docs as customer-project evidence.

## Evidence Expansion

Read review-recording guidance and existing review artifacts to satisfy the formal review recording requirement. A broad review-artifact search produced more output than needed; review then narrowed to `docs/workflows.md` review-recording lines and existing proposal-review record patterns.

## Recommended Next Stage

Revise the proposal to resolve `CPS-PR1`, then rerun proposal-review. This review remains isolated and does not automatically start `spec`.
