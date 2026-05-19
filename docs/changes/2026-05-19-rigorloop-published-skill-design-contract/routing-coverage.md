# Published Skill Design Pilot Routing Coverage

## Scope

Changed pilot skills:

- `proposal`
- `proposal-review`

This evidence is a fixture and transcript-review input. It does not claim deterministic runtime skill auto-selection.

## Coverage Table

| Skill | Positive triggers | Near misses | Competing skills | Should-not-trigger prompt classes |
| --- | --- | --- | --- | --- |
| `proposal` | create a RigorLoop proposal; turn a selected direction into a reviewable proposal; record problem, goals, non-goals, options, recommendation, risk, rollout, readiness | early brainstorming without selected direction; write requirements; create execution plan; review an existing proposal; implement code; verify branch | `explore`, `research`, `spec`, `plan`, `proposal-review`, `implement`, `verify` | generic explanation of proposals; summarize text; edit grammar only; review code diff; run tests |
| `proposal-review` | review a RigorLoop proposal before spec; challenge problem framing, option quality, scope, risk, vision fit, decision rationale, readiness for spec | write the proposal; review a feature spec; review an execution plan; review implementation diff; verify final branch; create PR handoff | `proposal`, `spec-review`, `plan-review`, `code-review`, `verify`, `pr` | summarize proposal without judgment; explain proposal format; edit wording only; implement requested direction; route final release readiness |

## Prompt Fixtures

### `proposal`

| Fixture type | Prompt class | Expected coverage |
| --- | --- | --- |
| Obvious positive | "Create a RigorLoop proposal for this skill design contract direction." | `description` should trigger proposal authoring. |
| Casual positive | "Can you turn this direction into a proposal before we spec it?" | `description` should trigger proposal authoring from a selected direction. |
| Edge positive | "We have options and risks but no requirements yet; draft the proposal artifact." | `description` should trigger proposal because the stage is pre-spec authoring. |
| Near negative | "Explain what a RigorLoop proposal is." | `description` should not imply generic explanation is the proposal skill's job. |
| Competing skill | "Review this proposal and tell me whether it is ready for spec." | `description` should route toward `proposal-review`. |
| Should not trigger | "Implement this approved plan milestone." | `description` should route toward `implement`. |

### `proposal-review`

| Fixture type | Prompt class | Expected coverage |
| --- | --- | --- |
| Obvious positive | "Review this RigorLoop proposal before spec." | `description` should trigger proposal review. |
| Casual positive | "Can you sanity-check whether this proposal is ready?" | `description` should trigger proposal review. |
| Edge positive | "This proposal has open questions and a possible vision conflict; challenge it." | `description` should trigger proposal review. |
| Near negative | "Explain what a proposal review is." | `description` should not imply generic explanation is the review skill's job. |
| Competing skill | "Review this implementation diff against the plan." | `description` should route toward `code-review`. |
| Should not trigger | "Write the feature specification from the accepted proposal." | `description` should route toward `spec`. |

## Static Coverage Expectations

M2 may validate:

- table existence for each changed pilot skill;
- positive trigger phrase coverage;
- near-miss or competing-skill phrase coverage;
- should-not-trigger prompt class presence.

M2 must not validate:

- broad semantic quality of skill prose;
- deterministic model auto-selection;
- runtime routing behavior without an approved harness.

## Transcript Review Expectations

When transcripts are available, record whether:

- the skill under-triggered;
- the skill over-triggered;
- the skill opened unnecessary resources;
- near-miss wording should be tightened;
- no change is needed, with rationale.
