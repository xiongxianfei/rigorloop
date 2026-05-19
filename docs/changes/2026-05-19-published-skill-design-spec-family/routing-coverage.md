# Published Skill Design Spec Family Routing Coverage

## Scope

Changed rollout skills:

- `spec`
- `spec-review`

This evidence is a fixture and transcript-review input. It does not claim deterministic runtime skill auto-selection.

## Coverage Table

| Skill | Positive triggers | Near misses | Competing skills | Should-not-trigger prompt classes |
| --- | --- | --- | --- | --- |
| `spec` | write a contract-level feature spec; amend an existing feature spec; define observable behavior, APIs, UI, config, data contracts, error behavior, compatibility, security, or safety-sensitive logic before planning or implementation | brainstorm options; write or review a proposal; review a feature spec; create architecture; create execution plan; create test spec; implement code; verify branch; prepare PR | `explore`, `research`, `proposal`, `proposal-review`, `spec-review`, `architecture`, `plan`, `test-spec`, `implement`, `verify`, `pr` | generic explanation of specifications; summarize text; edit grammar only; review code diff; run tests; final release readiness |
| `spec-review` | review a feature spec before architecture, test planning, execution planning, or implementation; challenge requirement clarity, completeness, testability, compatibility, edge cases, observability, security/privacy, non-goals, and acceptance criteria | write the spec; review a proposal; review architecture; review an execution plan; review implementation diff; verify final branch; create PR handoff | `spec`, `proposal-review`, `architecture-review`, `plan-review`, `code-review`, `verify`, `pr` | summarize a spec without judgment; explain spec format; edit wording only; implement requirements; run tests; route final release readiness |

## Prompt Fixtures

### `spec`

| Fixture type | Prompt class | Expected coverage |
| --- | --- | --- |
| Obvious positive | "Write the feature spec for this accepted proposal." | `description` should trigger spec authoring from an approved upstream artifact. |
| Casual positive | "Can you turn this behavior into requirements before we plan it?" | `description` should trigger contract-level spec authoring before planning. |
| Edge positive | "We need to define config, compatibility, error behavior, and rollback before implementation." | `description` should trigger spec authoring because the request defines observable behavior and boundaries. |
| Near negative | "Explain what a feature spec is." | `description` should not imply generic explanation is the spec skill's job. |
| Competing skill | "Review this feature spec and tell me if it is ready for planning." | `description` should route toward `spec-review`. |
| Should not trigger | "Implement M1 from the approved plan." | `description` should route toward `implement`. |

### `spec-review`

| Fixture type | Prompt class | Expected coverage |
| --- | --- | --- |
| Obvious positive | "Review this feature spec before architecture and planning." | `description` should trigger spec review. |
| Casual positive | "Can you sanity-check whether this spec is testable?" | `description` should trigger spec review. |
| Edge positive | "This spec may miss compatibility, observability, and error behavior; challenge it." | `description` should trigger spec review. |
| Near negative | "Write the feature specification from this accepted proposal." | `description` should route toward `spec`. |
| Competing skill | "Review this implementation diff against the spec." | `description` should route toward `code-review`. |
| Should not trigger | "Run final verification and say whether this branch is ready." | `description` should route toward `verify`. |

## Static Coverage Expectations

M2 may validate:

- coverage-table existence for each changed rollout skill;
- positive trigger phrase coverage;
- near-miss or competing-skill phrase coverage;
- should-not-trigger prompt class presence;
- description length and frontmatter routing source checks already required by the skill contract.

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
