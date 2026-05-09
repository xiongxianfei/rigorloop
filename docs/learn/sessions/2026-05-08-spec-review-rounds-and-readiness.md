# Learn Session: Spec Review Rounds and Readiness Wording

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation with questions: why the safe-resolution path produced many spec-review rounds, why `spec-review` reports eventual `test-spec` readiness instead of plan readiness, and why the latest `spec-review` record concluded `Immediate next repository stage: none`.
- Trigger type: explicit maintainer request / contributor observation.
- Scope:
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r1.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r2.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r3.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r4.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r5.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`
  - `specs/rigorloop-workflow.md`
  - `specs/test-spec-readiness-and-skill-workflow-alignment.md`
  - `.codex/skills/spec-review/SKILL.md`
- Explicit exclusions:
  - no topic-file update without contributor confirmation;
  - no workflow, skill, or spec policy update from this learn session;
  - no architecture, plan, verify, or PR readiness claim.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-05-review-record-placement.md`
  - `docs/learn/sessions/2026-05-06-isolated-review-material-finding-records.md`
- Session record path: `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`

## Observe

### O1 - Safe resolutions were applied too narrowly

Evidence:

- `spec-review-r1` found broad ambiguity around proportional-evidence/tiny-change wording, direct final-milestone-to-`verify` routing, and stale next-artifact sections.
- `spec-review-r2` found remaining retired route vocabulary, direct-verify closeout wording, autoprogression vocabulary, and test-spec assertions.
- `spec-review-r3` found additional direct-`verify` closeout wording in milestone-aware surfaces and public skill guidance.
- `spec-review-r4` found residual `Proportional-evidence` and `Fast-lane exceptions` wording after earlier fixes.
- `spec-review-r5` approved after the final pass added broader public-surface and workflow-spec static checks.

Observation:

The safe-resolution path reduced risk per edit, but each review fixed the latest visible defect class in a bounded surface set. Because the first fixes did not include a same-class sweep across all affected public/spec/test/skill/generated surfaces, later reviews discovered adjacent stale wording variants.

Practical answer:

The many rounds were not caused by `spec-review` itself being inherently too heavy. They were caused by using each safe resolution as a local patch instead of treating it as the minimum fix plus a required same-class search. The better pattern is:

1. record the material finding before fixing;
2. apply the safe resolution;
3. run a same-class sweep across canonical specs, matching test specs, public docs, canonical skills, generated copies, and static checks;
4. only then ask for the next review.

### O2 - `test-spec` readiness is a downstream proof-design signal, not the immediate handoff

Evidence:

- `.codex/skills/spec-review/SKILL.md` requires `spec-review` output to report review outcome, immediate next repository stage, eventual `test-spec` readiness, and stop condition.
- `specs/rigorloop-workflow.md` requires `spec-review` to distinguish immediate next repository stage from eventual `test-spec` readiness.
- `specs/rigorloop-workflow.md` says immediate next repository stage can be `architecture`, `plan`, `spec`, or empty for inconclusive review.
- `specs/rigorloop-workflow.md` says `test-spec` authoring still requires approved feature spec, spec-review findings, concrete execution plan, and approved architecture or ADR inputs when relevant.

Observation:

`spec-review` reports eventual `test-spec` readiness because its core question is whether the spec is clear and testable enough for proof design after required intermediate artifacts exist. That does not replace plan readiness. The immediate next repository stage is the slot that names `architecture` or `plan` when those are next.

Practical answer:

After `spec-review`, plan can still be the immediate next stage. `eventual test-spec readiness` answers a different question: "Once architecture and plan dependencies are handled, is this spec testable enough for a test spec?" The wording is useful for preventing a common mistake: jumping to `test-spec` when architecture or plan still remains. It is also confusing because the label can sound like the next stage is `test-spec`. A clearer output style would emphasize:

- immediate next repository stage: `architecture`, `plan`, `spec`, or none;
- eventual proof-design readiness: `ready`, `conditionally-ready`, `not-ready`, or `not-assessed`.

### O3 - `Immediate next repository stage: none` conflated isolation with routing

Evidence:

- `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/spec-review-r5.md` says: "No automatic downstream handoff is performed because this was a direct `spec-review` request" and then says `Immediate next repository stage: none`.
- `.codex/skills/spec-review/SKILL.md` says direct or review-only `spec-review` requests remain isolated by default, but still report review outcome, immediate next repository stage, eventual `test-spec` readiness, and stop condition.
- `specs/test-spec-readiness-and-skill-workflow-alignment.md` says direct or review-only `spec-review` remains isolated even when its output names the immediate next stage and eventual downstream readiness.
- `docs/workflows.md` says after `spec-review`, the immediate next stage is `architecture` when needed, otherwise `plan`.

Observation:

The `none` conclusion came from treating "no automatic downstream handoff" as if it also meant "no immediate next repository stage." That collapses two different fields:

- isolation: whether the agent should automatically continue after the direct review request;
- immediate next repository stage: the next lifecycle stage if the user or workflow continues.

Practical answer:

For a direct `$spec-review`, the handoff should say no automatic downstream handoff, but the immediate next repository stage should still be named when known. `none` is appropriate only when the review is inconclusive, required inputs are missing, or no repository-stage continuation is applicable.

For this workflow-governance change, the better conclusion would have been:

- automatic downstream handoff: none, because the invocation was isolated;
- immediate next repository stage if continuing: `architecture`, because the change is broad-impact, cross-component, generated-output-affecting, and workflow-boundary-changing;
- eventual proof-design readiness: `ready`, assuming the spec stays approved.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | process-follow-up | pending confirmation | Possible spec-review skill guidance or workflow guidance update requiring same-class sweep after material wording findings. | Not yet confirmed | The pattern is reusable, but changing review behavior belongs in an authoritative artifact. |
| O2 | artifact-update | pending confirmation | Possible spec-review skill wording update to rename or explain `eventual test-spec readiness` as downstream proof-design readiness. | Not yet confirmed | The current contract is internally coherent, but the label confused a maintainer during use. |
| O3 | artifact-update | pending confirmation | Possible correction to affected spec-review records and/or output guidance clarifying that isolation stops autoprogression, not the immediate-next-stage field. | Not yet confirmed | The current `spec-review-r5` wording is misleading because it conflates isolated invocation with the next lifecycle stage if continuing. |

## Route

No routing performed.

Contributor confirmation is unavailable for derivative updates. This session therefore records the observations and stops before topic-file, skill, spec, or workflow changes.

## No Durable Lesson Rationale

No topic entry was created. The session produced useful observations, but durable guidance would change review behavior or output wording and should be confirmed before being routed to an owning artifact.
