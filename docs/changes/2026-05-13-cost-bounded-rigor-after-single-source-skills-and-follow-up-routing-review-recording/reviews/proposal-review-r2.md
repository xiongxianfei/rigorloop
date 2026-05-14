# Proposal Review R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: Maintainer proposal-review
Target: docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md
Reviewed artifact: docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md
Review date: 2026-05-13
Recording status: recorded
Status: changes-requested

## Outcome

- Review status: changes-requested
- Material findings: CBR-1, CBR-2, CBR-3, CBR-4, CBR-5, CBR-6
- Blocking findings: none
- Isolation: direct proposal-review feedback stops before spec or plan

## Scope Checked

Reviewed the cost-bounded rigor proposal after the single-source skill and follow-up-routing context was incorporated. The review focused on readiness wording, first-slice scope, scope-budget trigger mechanics, bounded-evidence safety, validation-budget deferral, and deferred lifecycle token-cost reporting.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal identifies the right remaining waste source: workflow amplification rather than generated adapter duplication or hidden follow-ups. |
| User value | pass | The value is concrete: reduce proposal-to-implementation cost without weakening rigor. |
| Option diversity | pass | The proposal compares no change, hard token budgets, and cost-bounded rigor rules. |
| Decision rationale | pass | The recommended direction follows from preserving rigor while reducing waste. |
| Scope control | concern | First-slice and acceptance wording still risks pulling in too many surfaces. See CBR-2, CBR-5, and CBR-6. |
| Architecture awareness | pass | The proposal names workflow docs, skill surfaces, validation selectors, reports, and generated-output boundaries. |
| Testability | concern | Scope-budget and validation-budget guidance need clearer first-slice boundaries to be testable without brittle semantic validation. See CBR-3 and CBR-5. |
| Risk honesty | concern | The bounded-evidence rule needs an explicit do-not-under-read escape. See CBR-4. |
| Rollout realism | concern | Rollout should start with proposal/proposal-review guidance and concise workflow wording rather than a broader skill/validator slice. See CBR-2. |
| Readiness for spec | concern | Changes are requested before spec or plan. |

## Scope Preservation

Pass. The proposal preserves the user goals: account for PR #52, account for PR #53, reduce proposal-to-implementation token cost, keep rules concise, preserve rigor, avoid re-solving completed cleanup, and generate an updated proposal.

## Vision Fit

Pass. The proposal uses `fits the current vision`, and the direction aligns with `VISION.md` by making workflow evidence more inspectable without replacing durable artifacts with chat-only summaries.

## Standing Artifact Gate

Pass. `VISION.md` and `CONSTITUTION.md` exist. The proposal is workflow-governance direction but does not bypass either standing artifact gate.

## Material Findings

### CBR-1 - Readiness wording preclaims acceptance

Finding ID: CBR-1

Severity: major

Location: `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`, `Readiness`

Evidence: The proposal status is `draft`, but the readiness section says it is "Ready for proposal status normalization to `accepted`; after acceptance, ready for a focused first-slice spec."

Required outcome: Make the readiness statement stage-accurate for a draft proposal.

Safe resolution path: Replace the readiness wording with `Ready for proposal-review.` and state that, if proposal-review approves the direction, the next artifact is a focused first-slice spec for scope-budget and bounded-evidence guidance. If a proposal-review receipt is being relied on for acceptance, cite it explicitly and update the proposal status accordingly.

### CBR-2 - First slice is still too broad

Finding ID: CBR-2

Severity: major

Location: `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`, `First implementation slice` and `Rollout`

Evidence: The first implementation slice covers scope-budget guidance, bounded evidence/path-search guidance in `docs/workflows.md` and selected skill surfaces, proposal-review checks, and static skill-validator checks.

Required outcome: Split the first slice into a smaller authoring/review guidance slice and defer skill/validator work unless explicitly needed.

Safe resolution path: Define M1 as scope-budget guidance for proposal/proposal-review plus concise bounded-evidence wording in `docs/workflows.md`. Move selector or validation-budget behavior changes, lifecycle token-cost summary artifacts, dynamic benchmark changes, broad progressive-loading implementation, and edits to `implement` or `code-review` out of M1 unless a later plan explicitly scopes them.

### CBR-3 - Scope-budget trigger needs reviewer-judgment boundary

Finding ID: CBR-3

Severity: major

Location: `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`, `Scope-budget trigger`

Evidence: The proposal says a scope budget is required when several semantic trigger conditions are true, while also saying validators should not infer whether a proposal is broad.

Required outcome: Make scope-budget applicability operational as proposal/proposal-review judgment, not mechanical validator inference.

Safe resolution path: Add wording that validators may check table shape when a `Scope budget` table exists, but must not fail a proposal solely because they infer that the proposal is broad. Proposal-review may require a scope budget when silent narrowing, hidden follow-up risk, or multi-workstream scope is evident.

### CBR-4 - Evidence-budget wording needs do-not-under-read guardrail

Finding ID: CBR-4

Severity: major

Location: `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`, `Workstream B: Evidence budget`

Evidence: The proposal says to use bounded evidence before broad reads and lists full-file reads only when the whole file is the target or bounded evidence is insufficient, but the proposed skill-facing wording does not explicitly say not to under-read.

Required outcome: Add a concise escape rule to preserve correctness when bounded evidence is incomplete, contradictory, or insufficient.

Safe resolution path: Add wording such as: "Use bounded evidence before broad reads, but do not under-read. Expand to a broader section or full file when bounded evidence is incomplete, contradictory, or insufficient to support the claim being made."

### CBR-5 - Validation-budget work should be deferred more clearly

Finding ID: CBR-5

Severity: major

Location: `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`, `Acceptance criteria`

Evidence: The scope budget says validation-budget guidance belongs to a separate implementation slice, but acceptance criteria still say validation-budget ownership is explicit across `docs/workflows.md`, validation-selection behavior, and skill prose.

Required outcome: Move validation-budget acceptance to a later-slice scope or narrow first-slice acceptance to proposal-level direction.

Safe resolution path: Replace the first-slice acceptance criterion with wording that the proposal records validation-budget ownership as a later slice and does not change selector behavior in the first implementation. Add a later-slice acceptance criterion for distinguishing `docs/workflows.md`, selector behavior, and skill-local reminders when M2 is implemented.

### CBR-6 - Lifecycle token-cost summary section is too detailed for a deferred feature

Finding ID: CBR-6

Severity: major

Location: `docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`, `Workstream D: Lifecycle token-cost summary`

Evidence: Lifecycle token-cost summaries are out of first-slice scope, but the proposal defines a detailed report path and YAML shape.

Required outcome: Reduce the deferred lifecycle token-cost summary section to a lightweight design sketch.

Safe resolution path: Keep the conditional/deferred trigger guidance, but move exact report path and schema definition to a later proposal or spec. In this proposal, state only the intended field groups: identity, trigger, scope, observed cost drivers, largest observed event, and result/rationale.

## Non-Material Concerns

- `Selected skill surfaces` is ambiguous; name first-slice skill surfaces explicitly or defer skill edits entirely. Minimal first-slice surfaces should be `proposal`, `proposal-review`, and `workflow`.
- Public skill wording should not grow into another shared template. `docs/workflows.md` should own the full rule, and only directly affected skills should get short operational reminders.

## Readiness

Changes requested before spec/plan. This is an isolated proposal-review result with no automatic downstream handoff.
