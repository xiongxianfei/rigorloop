# Learn Session: M2 Test-Spec-Review Evidence Review Miss

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why the review skill in autoprogression did not find the M2 `test-spec-review` evidence wording issue.
- Trigger type: maintainer request / review miss retrospective.
- Date: 2026-06-26
- Scope:
  - why `code-review-r2` approved M2 without finding the missing `recorded` requirement;
  - why later isolated M2 re-review found `CR4-F1`;
  - whether the miss indicates a reusable review or validation pattern.
- Evidence in scope:
  - `docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/code-review-r2.md`
  - `docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/code-review-r4.md`
  - `docs/changes/2026-06-25-independent-test-spec-review-gate/reviews/code-review-r5.md`
  - `specs/test-spec-review-gate.md` R26
  - `skills/implement/SKILL.md`
  - `scripts/test-skill-validator.py`
  - commits `5bc55694`, `d6fbf415`, and `df5b9f4e`
- Explicit exclusions:
  - no new workflow, spec, skill, validator, or code-review policy change is made by this learn session;
  - no topic entry is created without contributor confirmation;
  - no branch readiness, PR readiness, CI status, verify status, or review-resolution status is claimed by this session.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/topics/review-artifact-recording.md`
  - `docs/learn/topics/skill-asset-design.md`
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
  - `docs/learn/sessions/2026-05-12-clean-review-settlement-vs-chat-evidence.md`
  - `docs/learn/sessions/2026-06-23-m2-resource-lint-review-root-cause.md`
  - `docs/learn/sessions/2026-06-25-test-spec-review-ownership.md`
- Session record path: `docs/learn/sessions/2026-06-26-m2-test-spec-review-evidence-review-miss.md`

## Observe

### O1 - The original review compared against the implemented weaker invariant, not the full R26 obligation

Evidence:

- `specs/test-spec-review-gate.md` R26 says the `implement` skill must require "active test spec plus approved, current, recorded `test-spec-review` evidence before implementation eligibility."
- `code-review-r2` recorded the M2 test coverage as proving "implementation requires approved current review evidence."
- The M2 focused validator assertion checked only `approved current test-spec-review when required`.
- `CR4-F1` later found that the published implementation skill and validator assertion omitted the `recorded` requirement.

Observation:

The miss was not that the reviewer lacked the relevant files. `code-review-r2` listed the spec, M2 diff, adjacent skills, and validator evidence as inputs.

The miss was that review accepted the implementation's compressed phrase, "approved current review evidence," as equivalent to R26. That phrase preserved approval and currentness but dropped the separate durable-recording condition.

### O2 - Passing validation reinforced the omission because the regression encoded the same incomplete phrase

Evidence:

- `code-review-r2` cited focused and full skill-validator runs as passing evidence.
- The focused test asserted one global substring: `approved current test-spec-review when required`.
- It did not assert the workflow-role, inputs, default-evidence, and stop-condition surfaces independently.
- The `CR4-F1` fix in commit `d6fbf415` changed all four surfaces and tightened the test to assert each surface independently.

Observation:

The validator was aligned with the implementation, but both were under-specified relative to R26. The original review challenged whether a test existed, but it did not challenge whether the test was a faithful projection of the normative requirement.

This is the same broad pattern as prior validator/test learnings: tests can prove examples while missing the decision model or a required dimension.

### O3 - The issue lived in a repeated public prose surface, but review treated it as a single routing concept

Evidence:

- The user identified four `implement` skill surfaces that needed tightening:
  - workflow role upstream;
  - inputs;
  - default evidence;
  - pre-implementation stop condition.
- `code-review-r2` summarized adjacent routing as a single concept: "`implement` to require approved current review evidence when applicable."
- `code-review-r4` found the missing condition by checking the exact implement-skill eligibility wording against R26.

Observation:

The review collapsed four contributor-facing obligations into one semantic bucket. That was enough to notice that `implement` now mentioned `test-spec-review`, but not enough to verify that every operational surface carried the complete requirement.

For public skills, repeated prose surfaces are not just duplication. Different sections are read at different workflow moments, so each surface can independently weaken the contract.

### O4 - Autoprogression did not fail because no automated gate required requirement-word fidelity across public skill surfaces

Evidence:

- The autoprogression path had clean M2 code-review and passing skill-validator evidence.
- No M2 validator rejected missing `recorded` in the `implement` skill.
- The later fix had to add per-surface assertions to `scripts/test-skill-validator.py` before the gap became machine-checkable.

Observation:

This was a review execution and proof-design gap, not a hidden runtime failure. Autoprogression can only act on recorded review findings, stop conditions, and validators that exist. Because the first review and the focused validator both accepted the weaker invariant, the profile had no recorded reason to pause.

## Root Cause

The root cause was requirement compression during review.

R26 had three separable evidence properties:

```text
approved
current
recorded
```

The M2 implementation and test compressed that into:

```text
approved current
```

The original review then reviewed the compressed implementation concept instead of re-expanding the normative requirement and checking every public skill surface where implementation eligibility is taught.

## Classify

| Observation ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Session record only | `code-review-r2`, `code-review-r4`, R26 | Explains the concrete review miss without needing a new policy change. |
| O2 | process-follow-up | pending confirmation | Possible future code-review or skill-validator guidance for requirement-fidelity assertions | Not yet confirmed | Reusable pattern, but changing review or validator practice belongs in an action-owning artifact. |
| O3 | process-follow-up | pending confirmation | Possible checklist item for repeated public skill surfaces | Not yet confirmed | Public skill prose can weaken contracts section-by-section, but learn alone should not update policy. |
| O4 | observation | observation | Session record only | Autoprogression evidence and later validator fix | Explains why autoprogression did not stop: the necessary review finding and validator did not exist yet. |

Contributor confirmation status: explicit maintainer request confirms recording this retrospective and answering the root-cause question. It does not by itself confirm updating topic files, specs, skills, validators, or workflow policy.

## Route

No derivative routing performed.

Candidate follow-up, not routed here: consider an action-owning update that requires code-review of public skill routing changes to build a requirement-to-surface checklist when a spec says a skill "MUST require" a condition across multiple sections.

Candidate validation follow-up, not routed here: for focused skill-surface regressions, prefer per-surface assertions over one global substring whenever the requirement applies in multiple public skill sections.

## No Durable Route Rationale

No topic entry was created. The finding is concrete and reusable, but the behavior change has already been handled for this PR by `CR4-F1`, commit `d6fbf415`, and `code-review-r5`.

Broader review-process or validator-design guidance would change action-owning artifacts such as review skill guidance, workflow guidance, or validator tests. This session records the lesson and candidate follow-up, then stops before turning it into policy.

## Best-Practice Answer

The review skill in autoprogression did not catch the issue because the first M2 review verified that the new gate was mentioned and that validation passed, but it did not decompose R26 into all required evidence properties and all public skill surfaces.

The better review move would have been:

1. Restate R26 as a checklist: active test spec plus `approved`, `current`, and `recorded` review evidence.
2. Enumerate every M2 `implement` surface that teaches implementation eligibility.
3. Check each surface independently for all required properties.
4. Challenge the validator by asking whether it would fail if only one surface dropped `recorded`.

That is exactly what the `CR4-F1` fix now does for this case.
