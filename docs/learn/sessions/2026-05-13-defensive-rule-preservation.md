# Learn Session: Defensive Rule Preservation

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why the agent tends to add defensive wording such as "Local Codex runtime state under `.codex/skills/` MUST NOT be hand-edited or tracked" instead of deleting obsolete rules to keep descriptions clear and concise.
- Trigger type: explicit maintainer request / contributor observation.
- Scope:
  - M2 documentation changes in the publish-next-release transition release plan.
  - Current contributor-facing guidance in `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and `README.md`.
  - Existing learn sessions and topic guidance related to concise guidance, public/internal boundaries, and stale instruction cleanup.
- Evidence in scope:
  - `CONSTITUTION.md` line containing local Codex runtime-state wording.
  - `AGENTS.md`, `docs/workflows.md`, and `README.md` local Codex setup wording.
  - Active plan notes for M2 documenting that stale local Codex setup wording was replaced.
  - `CONSTITUTION.md` and `AGENTS.md` rules saying stale instructions should be removed or challenged when wrong.
  - Prior learn sessions `2026-05-08-public-skill-surface-boundary.md` and `2026-05-09-review-finding-volume-root-cause.md`.
  - Topic `docs/learn/topics/token-cost-measurement.md`, which recommends concision but warns not to weaken safety-critical guidance without evidence.
- Explicit exclusions:
  - No direct edit to M2 documentation in this learn session.
  - No curated topic update from this single observation.
  - No new workflow policy, spec, ADR, skill behavior, release-readiness, branch-readiness, or PR-readiness claim.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-08-public-skill-surface-boundary.md`
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
  - `docs/learn/topics/token-cost-measurement.md`
- Session record path: `docs/learn/sessions/2026-05-13-defensive-rule-preservation.md`

## Observe

### O1 - The agent preserved a stale rule shape instead of asking whether the rule should disappear

Evidence:

- The M2 change rewrote local Codex setup wording across contributor surfaces.
- The resulting `CONSTITUTION.md` wording still says local Codex runtime state under `.codex/skills/` "MUST NOT be hand-edited or tracked" before describing the public adapter install path.
- The maintainer challenged that wording as defensive and asked why the rule was not simply deleted.

Observation:

The agent treated the existing local-runtime warning as a safety invariant that needed to survive in rewritten form. That preserved a defensive prohibition even though the approved transition-release direction was trying to reduce `.codex/skills/` prominence.

### O2 - The root cause is over-applying preservation rules to obsolete instructions

Evidence:

- Repository guidance says to preserve user changes and avoid unrelated refactors.
- Repository guidance also says agents must remove or challenge stale instructions when they are demonstrably wrong.
- The approved transition-release spec says local Codex setup should use public Codex adapter output and `.codex/skills/` should not become release evidence.

Observation:

The agent gave more weight to "do not remove safety guidance casually" than to "delete stale instructions when the approved contract supersedes them." That creates wordy replacement rules where a clean deletion or narrower install instruction would be clearer.

### O3 - The active M2 review should judge whether the current wording is still too defensive

Evidence:

- M2 has been implemented and handed to `code-review`.
- The maintainer observation is specifically about wording introduced by M2.

Observation:

This is actionable during M2 review, but it is not yet a durable repository-wide lesson by itself. The next review should check whether the current contributor-facing wording can be simplified without losing the approved source-boundary behavior.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | M2 review context | Maintainer observation | The event is concrete and evidenced, but one example does not by itself prove a durable general rule. |
| O2 | direction | direction | Candidate M2 review follow-up | Maintainer observation | The maintainer is giving style and authoring direction: delete or simplify obsolete rules instead of preserving defensive wording. This should be evaluated in the owning implementation/review flow. |
| O3 | process-follow-up | process-follow-up | M2 code-review checklist note | Maintainer observation | The current active milestone is at code-review handoff, so review is the correct next owner for deciding whether the wording should change. |

Contributor confirmation status: confirmed for recording this session and routing the observation to M2 review context. Not confirmed for creating curated topic guidance or changing authoritative policy in this learn session.

## Route

- Session record: created.
- Topic update: not routed.
- Action-owning artifact update: not routed from learn.
- Process follow-up: M2 code-review should explicitly evaluate whether the local Codex setup wording is unnecessarily defensive and whether obsolete `.codex/skills/` rules should be deleted rather than restated.

## Practical Answer

The immediate reason was conservative editing: the agent saw an existing governance rule, recognized part of it was stale, and rewrote it to preserve the perceived safety boundary. That was too defensive for this case.

The better practice for this kind of change is:

- If an approved contract supersedes an old rule, delete the old rule shape instead of restating it with extra prohibitions.
- Keep only the active behavior users need to follow.
- Put validation and release-evidence constraints in validators, specs, or release docs, not in every contributor-facing sentence.
- Use review to decide whether any remaining prohibition is necessary.

## No Durable Topic Rationale

This session records a useful maintainer observation, but it does not create a curated topic entry. The evidence is one current wording issue plus related prior concision guidance, not repeated confirmed failures of the same exact pattern. If M2 code-review or later reviews find the same defensive-preservation pattern again, that accumulated evidence may justify durable topic guidance or an authoring-rule update.
