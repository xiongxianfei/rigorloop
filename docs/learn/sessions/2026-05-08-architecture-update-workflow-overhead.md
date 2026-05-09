# Learn Session: Architecture Update Workflow Overhead

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking whether the delta architecture -> architecture-review -> merge-back path is too complicated and what best practices should be.
- Trigger type: explicit maintainer request / contributor observation.
- Scope:
  - `CONSTITUTION.md`
  - `specs/architecture-package-method.md`
  - `docs/architecture/system/architecture.md`
  - `.codex/skills/architecture/SKILL.md`
  - `.codex/skills/architecture-review/SKILL.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/architecture.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r5.md`
  - `docs/learn/README.md`
  - `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`
  - `docs/learn/sessions/2026-05-08-public-skill-surface-boundary.md`
- Explicit exclusions:
  - no architecture, skill, workflow, spec, ADR, or topic-file update from this learn session;
  - no change to architecture-review approval or merge-back status;
  - no plan, verify, PR, CI, or generated-output readiness claim.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`
  - `docs/learn/sessions/2026-05-08-public-skill-surface-boundary.md`
- Session record path: `docs/learn/sessions/2026-05-08-architecture-update-workflow-overhead.md`

## Observe

### O1 - The current contract does not require a delta for every architecture update

Evidence:

- `specs/architecture-package-method.md` says the goal is to make architecture work consistent without making every feature rewrite the architecture baseline.
- `specs/architecture-package-method.md` says a feature-specific architecture delta is used only when a change is architecture-significant enough to need reviewable working design reasoning before accepted content is merged into the canonical package.
- `specs/architecture-package-method.md` says small changes whose architecture impact is clear only after implementation may update the canonical package after implementation and before final verification.
- `.codex/skills/architecture/SKILL.md` says to use a change-local delta only when the change is architecture-significant enough to need reviewable working design reasoning before merge-back.
- `CONSTITUTION.md` says architecture-affecting changes must update the relevant architecture document or ADR, not that every such change must first create a delta.

Observation:

The expensive path is not meant to be universal. The current architecture contract already permits direct canonical updates or no-architecture-impact rationale when that is the lowest sufficient architecture surface.

Practical answer:

Best practice is a decision tree:

1. No architecture impact: record a short no-impact rationale in plan, test-spec, change metadata, or PR evidence.
2. Clear current architecture truth update: edit the smallest affected canonical architecture section or diagram directly.
3. Working design needed before committing current truth: create a change-local architecture delta, review it, then merge durable content back only if it changes current architecture truth.
4. Durable decision introduced or revised: create or supersede an ADR.

### O2 - The recent workflow made the change-local delta path feel like the default

Evidence:

- The 2026-05-08 workflow-governance change used a change-local delta and then direct `architecture-review`.
- The delta's readiness text says merge-back is not merged and describes conditional merge-back before final closeout.
- The direct architecture-review approved the delta and then said the next stage is `plan`, after normalizing the architecture delta status to `approved`.
- The maintainer observed that this path feels too complicated.

Observation:

The latest workflow run exposed a usability gap: even though the written contract says deltas are conditional, the visible handoff pattern can teach contributors that every architecture update needs a temporary delta, a review, and a merge-back decision.

Practical answer:

Architecture guidance should make the simpler path obvious first. A delta should be introduced only when it reduces review risk by separating exploratory design from current architecture truth.

### O3 - Merge-back should be conditional, not automatic ceremony

Evidence:

- `specs/architecture-package-method.md` requires merge-back from a change-local delta when durable content changes current architecture truth.
- `docs/architecture/system/architecture.md` says change-local deltas are supported only for architecture-significant work that needs temporary design reasoning and that accepted durable content is merged before completion.
- The 2026-05-08 architecture delta says merge-back is required only if architecture-review identifies durable canonical content; otherwise the delta can remain change-local evidence.

Observation:

Merge-back is a correctness rule for avoiding competing sources of truth. It should not be a default extra task when the delta only records change-local reasoning and the existing canonical architecture already covers the durable structure.

Practical answer:

When a delta is used, final closeout should record exactly one of:

- merge-back completed, with canonical paths;
- no merge-back required, because the delta did not change current architecture truth;
- merge-back deferred, with owner, reason, and blocking status if downstream work would rely on the missing canonical truth.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | pending confirmation | Possible architecture skill or architecture-package-method wording clarification. | Not yet confirmed | Existing authoritative artifacts already support the simpler paths, so this is mainly an interpretation and guidance problem. |
| O2 | artifact-update | pending confirmation | Possible update to architecture skill, workflow guide, or architecture-package method examples to show the decision tree before the delta path. | Not yet confirmed | The maintainer experienced the current output as too complicated, and clearer guidance belongs in the owning artifacts. |
| O3 | artifact-update | pending confirmation | Possible update to architecture-review/readiness wording to require explicit merge-back disposition rather than imply merge-back ceremony. | Not yet confirmed | Merge-back behavior is correct but should be presented as conditional on current architecture truth changing. |

## Route

No routing performed.

Contributor confirmation is unavailable for derivative updates. This session records the observations and stops before topic-file, skill, spec, workflow, architecture, or ADR changes.

## No Durable Lesson Rationale

No topic entry was created. The session contains a useful best-practice interpretation and candidate artifact updates, but changing architecture guidance belongs in the architecture skill, architecture package method spec, workflow guide, or architecture-review wording after confirmation.
