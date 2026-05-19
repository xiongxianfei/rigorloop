# Proposal Review R2

Review ID: proposal-review-r2
Stage: proposal-review
Round: 2
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-18-skill-readability-self-containment.md
Reviewed artifact: docs/proposals/2026-05-18-skill-readability-self-containment.md
Review date: 2026-05-18
Recording status: recorded
Status: approved

## Review inputs

- Proposal: `docs/proposals/2026-05-18-skill-readability-self-containment.md`
- Related accepted proposal: `docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md`
- Governance: `CONSTITUTION.md`, `AGENTS.md`
- Vision: `VISION.md`
- Workflow guidance and review-recording guidance: `docs/workflows.md`
- Project orientation: `docs/project-map.md`

## Findings

No material findings.

## Outcome

- Review status: approved
- Material findings: none
- Blocking findings: none
- Recording: clean review receipt recorded
- Isolation: direct proposal-review request stops here and does not automatically continue into spec

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The proposal states a concrete user-facing problem: installed skills are the user's full contract, but current skill text is harder to scan, repeats rules, narrates enums, lacks skeletons, and can rely on unavailable repository context. |
| User value | pass | The value is concrete and priority-ordered: preserve output quality first, improve clarity and concision second, and treat token cost as a tertiary constraint. |
| Option diversity | pass | The proposal compares no change, moving shared rules to specs, build-time composition, and in-skill restructure. The rejected options are meaningfully different. |
| Decision rationale | pass | Option 4 follows from the core constraint that installed skills must be self-contained without new tooling or dangling references. |
| Scope control | pass | Non-goals exclude normative rule changes, build-time partials, adapter packaging changes, legacy archive rewrites, and spec/schema/workflow-doc edits in this proposal. |
| Architecture awareness | pass | The proposal names canonical skill source, generated adapter output, repository-internal guidance, project-local guidance, and the generated-output validation boundary. |
| Testability | pass | Quality floors, clarity floors, behavior parity, cold-read verification, structural checks, self-containment checks, and token measurement are concrete enough for a focused spec and test spec. |
| Risk honesty | pass | Risks cover normative drift, token optimization eroding quality or clarity, cold-read ceremony, front-matter confusion, token increases, divergence across skills, and build-time-composition scope creep. |
| Rollout realism | pass | The pilot on `proposal` and `proposal-review`, cold-read verification, token measurement, and per-skill follow-on rollout are realistic and reversible. |
| Readiness for spec | pass | Remaining open questions are correctly scoped to spec or plan: full rollout subset, workflow-role block shape, lint enforcement mode, and token budget thresholds. |

## Vision fit review

Pass. Root `VISION.md` exists, and the proposal uses the allowed first
non-empty value `fits the current vision`. The rationale ties the change
to inspectability, reasoning, validation, maintenance, and reconstructing
quality from tracked artifacts. The added falsifier gives the quality
claim an observable failure condition.

## Standing artifact gate review

Pass. Root `VISION.md` and `CONSTITUTION.md` exist. The proposal is not a
bootstrap exception and does not bypass a required standing artifact gate.

## Scope preservation

Pass. The proposal visibly classifies the user's initial goals and
priorities:

- High-quality skill output is in scope and recorded as the primary
  success criterion.
- Clear and concise skills are in scope and recorded as the secondary
  criterion.
- Token cost is in scope as a tertiary constraint, not a driver.
- Tables, fenced enums, workflow-wide versus skill-local distinction,
  fillable skeletons, cold-read verification, deferred build-time
  composition, and rejected spec-only rule extraction are all traceable.

## Prior feedback closeout

The proposal resolves the prior review feedback that could block spec:

- Priority inversion is resolved by making quality, clarity, then token
  cost explicit in the Problem, Goals, risks, and core invariant.
- The missing quality falsifier is resolved in Vision fit and Testing and
  verification strategy.
- Relationship to the accepted customer-portable public skills proposal
  is resolved by declaring this proposal a follow-on, not a replacement.
- Quality and clarity floors are added before token-cost acceptance.
- Terminology now distinguishes installed skills, canonical skill source,
  generated adapter output, repository-internal guidance, and project-local
  guidance.
- Local guidance boundaries are explicit enough for spec.

## Adversarial checks

- Bad investment trigger: the work would be a bad investment if it became
  broad aesthetic churn or allowed token savings to degrade output quality.
  The proposal mitigates this with quality and clarity floors plus a pilot.
- Simpler option considered: doing nothing was considered and rejected
  because it leaves adopter-facing friction and drift risk in the skill
  surface.
- Deferred architecture cost: build-time partials are intentionally
  deferred; the proposal keeps this separate from the readability and
  self-containment decision.
- User segment at risk: adopters who only see installed skills are the
  main affected segment; cold-read verification directly tests that view.
- Behavior that should not change: normative skill behavior, lifecycle
  stage boundaries, review verdict meanings, adapter packaging, and
  release archive contracts remain out of scope.
- Test proving value: behavior-parity fixtures and cold-read verification
  should prove that rewritten skills preserve output quality while making
  rules, enums, skeletons, handoffs, and scope boundaries easier to find.

## No-finding statement

Clean formal proposal review completed with no material findings.

## Recommended next stage

Normalize the proposal status to `accepted` before downstream focused
spec work relies on it. This review remains isolated and does not
automatically start `spec`.
