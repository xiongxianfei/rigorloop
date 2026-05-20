# Learn Session: Spec-Family Asset Formalism

## Frame

- Trigger: explicit maintainer request after M6 removed trivial spec-family row assets.
- Trigger type: maintainer request / contributor observation / implementation retrospective.
- Scope: the spec-family assets progressive-disclosure change, especially M2 through M6.
- Session path: `docs/learn/sessions/2026-05-20-spec-family-asset-formalism.md`
- Evidence in scope:
  - `docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md`
  - `specs/spec-family-assets-progressive-disclosure.md`
  - `specs/spec-family-assets-progressive-disclosure.test.md`
  - `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`
  - `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/generated-output-proof.md`
  - commit `4053415` (`M6: remove trivial spec-family row assets`)
- Explicit exclusions:
  - This session does not reopen the earlier `plan` assets pilot.
  - This session does not create new packaged-resource policy outside the active spec-family change.
  - This session does not claim M6 code-review, verify, branch readiness, or PR readiness.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/topics/token-cost-measurement.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`

## Observe

### O1: Multi-instance row assets can still be formalism

M2 originally created `spec` row assets for requirements, acceptance criteria,
and decision-log rows. These were multi-instance structures, but their bodies
were one-line templates already governed by inline format guidance in
`skills/spec/SKILL.md`.

Evidence:

- M6 removed `skills/spec/assets/requirement-row.md`,
  `skills/spec/assets/acceptance-criterion-row.md`, and
  `skills/spec/assets/decision-log-row.md`.
- `specs/spec-family-assets-progressive-disclosure.md` now records `SFA-R3A`
  through `SFA-R3C`, including the substantial-template and
  metadata-to-content checks.
- The active plan records that the `spec` row assets had a poor
  metadata-to-content ratio and duplicated inline format guidance.

### O2: The useful asset boundary is substantial structure, not asset count

The assets that remain after M6 are full skeletons or multi-field blocks where
field order or table shape is easy to get wrong: `spec-skeleton.md`,
`review-result-skeleton.md`, `review-finding.md`, `test-spec-skeleton.md`,
`test-case.md`, and `coverage-map-row.md`.

Evidence:

- `scripts/skill_validation.py` now approves only the reduced spec-family asset
  inventory.
- `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/generated-output-proof.md`
  records refreshed generated-output proof for the reduced six-asset set.
- Temporary adapter archive inspection confirmed the removed row assets are
  absent while the current mapped assets are present.

### O3: The best fix was an authoritative artifact update, not a topic-only lesson

The maintainer observation changes the current spec-family contract. M6 routed
the lesson into the owning proposal, spec, test spec, plan, validator, skills,
fixtures, and generated-output evidence before this learn session captured it.

Evidence:

- `specs/spec-family-assets-progressive-disclosure.md` owns the normative
  substantial-template rule.
- `specs/spec-family-assets-progressive-disclosure.test.md` maps the rule to
  proof.
- The active plan records M6 as review-requested and routes the next stage to
  code-review.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | artifact-update | Maintainer request plus M2/M4/M6 evidence | The pattern recurred across row assets and has an authoritative spec update. |
| O2 | durable-lesson | durable-lesson | topic entry | Maintainer request plus M6 generated-output proof | The remaining inventory shows the reusable boundary: substantial skeletons and multi-field blocks. |
| O3 | artifact-update | artifact-update | none | Commit `4053415` and active plan M6 | Behavior-changing guidance belongs in the spec, test spec, plan, validators, and skills; learn records the lesson and links the authoritative route. |

## Route

- Added topic entry: `docs/learn/topics/skill-asset-design.md`.
- Authoritative artifact route already completed in M6:
  - `docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md`
  - `specs/spec-family-assets-progressive-disclosure.md`
  - `specs/spec-family-assets-progressive-disclosure.test.md`
  - `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`
  - `skills/spec/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`

## Result

The durable lesson is that assets need an existence gate. Repetition alone does
not justify a packaged template. Use assets for substantial copy-and-fill
structures such as full skeletons, multi-field blocks, and error-prone table
variants. Keep trivial one-line rows inline when the skill already carries the
format rule.

## Follow-Ups

- No separate follow-up is needed from this learn session.
- M6 remains review-requested; code-review owns the next workflow gate.
