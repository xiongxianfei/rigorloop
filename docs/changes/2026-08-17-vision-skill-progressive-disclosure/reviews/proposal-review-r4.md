# Proposal Review: Vision Skill Progressive Disclosure

Review ID: proposal-review-r4
Stage: proposal-review
Round: r4
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-17-vision-skill-progressive-disclosure.md`

Reviewed artifact: `docs/proposals/2026-08-17-vision-skill-progressive-disclosure.md` at commit `1536dddd`
Review date: 2026-08-17
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: VISSIM-R4-PR1
- Open blockers: the no-reference skip path must be reconciled with README applicability, marker ownership, and manifest identity
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, mutate vision artifacts, or continue workflow

## Overall assessment

The proposal now closes the round-3 findings: README authority binds the prior-to-intended vision transition, `VA0S` represents explicit sync skip, structural assets are selected independently, all six assemblies are measured, and the source-first recovery model remains bounded.

One consolidated skip-path contract remains inconsistent. The earlier README applicability table still says `sync-readme` always requires the README reference, while `VA0S` explicitly omits it. In addition, every skip is required to bind an observed marker state and manifest identity, but marker parsing belongs to the omitted reference and the target-manifest rule applies only to mutating invocations. The proposal therefore cannot yet explain how a pre-resolved skip obtains its evidence without loading the reference or how a zero-write skip gets the manifest identity required by its authority.

## Finding VISSIM-R4-PR1

Finding ID: VISSIM-R4-PR1
Severity: major
Location: README synchronization applicability, README action authority, loaded assemblies, and target-manifest scope
Evidence: the applicability table maps all `sync-readme` to a required README reference, but `VA0S-readme-skip` maps exact pre-resolved skip to `SKILL.md` only. Skip authority also binds observed marker state and manifest identity, while exact marker classification belongs to the README reference and only “mutating invocations” are guaranteed a manifest. `VA0S`, `VA1S`, and `VA2S` can therefore lack evidence their own authority contract requires.
Required outcome: define one evidence-complete pre-resolved skip path that genuinely omits README procedure, and distinguish it from a skip decided after README procedure loads.
Safe resolution path: update the applicability table with explicit pre-resolved sync skip; require every mutation-capable or skip-settled operation to create an operation manifest, including no-write skip targets whose prior and intended identities match; let pre-resolved skip bind exact current owner authority and README content identity without semantically classifying markers, using `marker_state: not-evaluated-under-exact-skip` or an equivalent closed value. If skip depends on marker evaluation or is authorized only after the reference loads, retain the loaded sync assembly even when the final action is skip. Add scenarios and criteria for both paths.
needs-decision rationale: none.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The flat package and conditional boundaries remain well motivated. |
| User value | pass | Real sync, editorial, and strategic paths become smaller. |
| Option diversity | pass | Alternatives remain materially distinct. |
| Decision rationale | pass | Two references and two assets remain appropriate. |
| Vision fit | pass | The direction preserves durable human-authorized vision work. |
| Scope control | pass | Scope and non-goals remain explicit. |
| Operation and assembly model | pass with revisions | Six assemblies are present, but skip selection conflicts with an earlier trigger table. |
| Multi-artifact consistency | pass | Source-first ordering, read-back, and partial recovery are now closed. |
| Authority binding | pass with revisions | Planned transitions are correct; zero-write skip evidence is incomplete. |
| Resource ownership | block | Pre-resolved skip requires marker evidence owned by the reference it omits. |
| Structural ownership | pass | Asset selection is independent and exhaustive. |
| Measurement | pass | Primary and secondary profiles are represented separately. |
| Testing boundary | pass | Static contract and package proof remain proportionate. |
| Architecture awareness | pass with condition | No architecture is needed if the operation manifest remains existing in-memory or change-local evidence. |
| Readiness for spec | changes-requested | VISSIM-R4-PR1 requires proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; all initial goals remain represented without hidden follow-up.

## Recommended Proposal Edits

- Reconcile pre-resolved and late-loaded skip behavior, extend manifest scope to zero-write skip settlement, and remove the no-reference path's dependency on semantic marker parsing.

## Recommendation

- Recommendation: revise VISSIM-R4-PR1 and run another independent proposal rereview. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: pass
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/reviews/proposal-review-r4.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r4
- Review record: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/reviews/proposal-review-r4.md`
- Review log: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/review-log.md`
- Review resolution: `docs/changes/2026-08-17-vision-skill-progressive-disclosure/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-17-vision-skill-progressive-disclosure`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
