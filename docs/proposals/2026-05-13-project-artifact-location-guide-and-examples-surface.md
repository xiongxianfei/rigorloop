# Project Artifact Location Guide and Examples Surface

## Status

accepted

## Problem

RigorLoop skills are being simplified so they do not carry long duplicated path rules, review-recording examples, change-root algorithms, and generated-output details. That simplification is correct, but it creates a practical question for users and agents:

```text
If public skills no longer contain detailed path rules,
how does a skill know where to put proposals, specs, plans, reviews,
examples, change metadata, reports, and generated outputs?
```

The repository has also been moving examples out of active-looking lifecycle locations and into `docs/examples/`. That direction is already partially implemented: `docs/examples/README.md` exists, `docs/examples/plans/example-plan.md` is the illustrative plan, and `docs/changes/0001-skill-validator/` is retained as a rich validator fixture and historical proof pack. The remaining problem is to make the artifact-location model explicit enough that public skills can stay concise without leaving artifact placement ambiguous.

Recent formal review work makes placement more important. Every supported formal lifecycle review now creates durable review evidence or reports blocked recording, with clean reviews using lightweight receipts and material findings using detailed review records plus disposition tracking. Users and agents need one user-facing place that answers:

```text
Where do RigorLoop artifacts go in this project?
```

## Goals

- Make `docs/workflows.md` the user-facing artifact location guide.
- Make the `workflow` skill responsible for creating or refreshing that guide.
- Keep public stage skills concise by having them consult the project artifact map instead of embedding long path rules.
- Keep examples under `docs/examples/`.
- Clarify that examples are non-normative and not active lifecycle state.
- Keep exact review receipt and review-root shape in the formal review recording spec or reference.
- Preserve stage ownership: each skill still owns its own artifact content.
- Preserve validator ability to enforce artifact shape when validators exist.
- Avoid making every public skill duplicate the same artifact location table.

## Non-goals

- Do not change the standard workflow order.
- Do not redesign review recording.
- Do not make `workflow` write every artifact type.
- Do not make `docs/workflows.md` override higher-priority governance or specs.
- Do not move example or fixture paths unless references, tests, and validators can be updated in the same change.
- Do not remove support for existing projects with custom artifact paths.
- Do not hardcode RigorLoop repository-internal validator paths into public skills.
- Do not change generated adapter packaging in this proposal.

## Vision fit

fits the current vision

This proposal supports RigorLoop's goal of making AI-assisted software delivery traceable and reviewable from durable artifacts, while keeping public skills concise and portable.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Let users know where RigorLoop documents go | in scope | Goals, Recommended direction |
| Use `workflow` to guide where changes, examples, and review output go | in scope | Goals, Workflow skill responsibility |
| Keep skills concise after removing detailed path rules | in scope | Goals, Skill artifact lookup rule, Stage skill responsibility |
| Move examples to `docs/examples/` | in scope, partially already done | Goals, Examples surface, Rollout and rollback |
| Handle `docs/plans/0000-00-00-example-plan.md` | in scope, already moved in current repo state | Context, Examples surface |
| Handle `docs/changes/0001-skill-validator/` carefully | in scope, conditional | Examples surface, Retained fixture contract |
| Avoid making workflow own all artifact content | in scope | Non-goals, Recommended direction |
| Preserve specs/references as exact shape owners | in scope | Goals, Formal review recording responsibility |

## Context

RigorLoop is moving toward concise public skills. Long path rules, examples, and generated-output internals should not be duplicated across every skill.

Recent review-recording work also increases the need for discoverable artifact placement. The formal-review direction says every formal lifecycle review creates a durable review file or reports blocked recording, with clean reviews using lightweight receipts and material-finding reviews using detailed records and disposition tracking.

The clean-review learning reinforces that durable artifact state matters: chat approval is not enough when the tracked artifact remains stale.

The single-authored-skill-source direction identifies generated output as derived and reinforces clear source-of-truth boundaries.

Current repository state already reflects part of the desired examples surface:

- `docs/examples/README.md` states that examples are non-normative.
- `docs/examples/plans/example-plan.md` is the illustrative plan structure.
- `docs/examples/formal-review-recording/` contains formal review recording examples.
- `docs/changes/0001-skill-validator/` remains a validator fixture and historical proof pack, not the universal minimum for every non-trivial change.

## Options considered

### Option 1: Keep detailed path rules inside every skill

This keeps each skill self-contained and avoids requiring agents to read `docs/workflows.md`.

The cost is duplicated path rules across many skills, larger public skill text, drift when artifact locations change, and conflict with token-friendly skill simplification.

### Option 2: Put all artifact placement rules in specs only

This is normative and testable, and it keeps skills shorter.

The weakness is usability: downstream projects may not carry every RigorLoop spec, and specs are not the easiest day-to-day place for users to find artifact locations. Public skills still need a lightweight project-local guide.

### Option 3: Use `docs/workflows.md` as the project artifact map

This gives users and agents one visible project-local guide. It lets public skills stay concise, points to specs for exact shapes, and can be created or refreshed by the `workflow` skill.

The cost is that `docs/workflows.md` must stay current and stage skills need a simple lookup rule before falling back to portable defaults.

## Recommended direction

Choose Option 3.

## Project artifact map

`docs/workflows.md` owns the project-local artifact-location map.

The map defines default locations and owning skills. It does not define full artifact schemas, required fields, lifecycle status values, or validation rules.

Skills use this lookup order when artifact placement matters:

```text
1. explicit user-provided path or change ID;
2. active plan, change metadata, or reviewed artifact path;
3. docs/workflows.md artifact-location table;
4. portable default path;
5. block on ambiguity.
```

`workflow` creates or refreshes the map when artifact placement changes or when the project adopts RigorLoop.

## Artifact-location source rank

`docs/workflows.md` is the project-local user-facing artifact map. It does not override higher-priority governance, accepted specs, schemas, or explicit user-provided paths.

When artifact placement conflicts, use this source rank:

```text
1. explicit user-provided path or change ID
2. active artifact metadata or active change metadata
3. accepted project specs or schemas
4. docs/workflows.md artifact-location table
5. built-in RigorLoop default path
6. block on ambiguity
```

Use this ownership model:

```text
workflow skill:
  creates or refreshes docs/workflows.md

docs/workflows.md:
  project-local workflow and artifact location guide

stage skills:
  create their own artifacts using docs/workflows.md locations

specs/references:
  define exact artifact shapes and validation rules

docs/examples:
  stores non-normative examples
```

`docs/workflows.md` should contain an `Artifact locations` section with the common project defaults:

The table defines default locations and owning skills. It does not define the full artifact schema, required fields, lifecycle status values, or validation rules. For exact shapes, use the governing spec, schema, or reference for that artifact type.

| Artifact type | Default location | Owning skill |
|---|---|---|
| Project vision | `VISION.md` | `vision` |
| Workflow guide | `docs/workflows.md` | `workflow` |
| Examples | `docs/examples/` | none; examples are non-normative |
| Proposals | `docs/proposals/YYYY-MM-DD-slug.md` | `proposal` |
| Specs | `specs/slug.md` | `spec` |
| Test specs | `specs/slug.test.md` | `test-spec` |
| Architecture | `docs/architecture/` or project-configured architecture path | `architecture` |
| ADRs | `docs/adr/ADR-YYYYMMDD-slug.md` | `architecture` |
| Plans | `docs/plans/YYYY-MM-DD-slug.md` | `plan` |
| Plan index | `docs/plan.md` | `plan` / workflow bookkeeping |
| Change root | `docs/changes/<change-id>/` | current change lifecycle |
| Change metadata | `docs/changes/<change-id>/change.yaml` | relevant stage / workflow |
| Formal review records | `docs/changes/<change-id>/reviews/<stage>-r<n>.md`; default location only, exact receipt/root rules are owned by `specs/formal-review-recording.md` | review skills |
| Review log | `docs/changes/<change-id>/review-log.md` | review skills |
| Review resolution | `docs/changes/<change-id>/review-resolution.md` when findings or blocking outcomes require disposition | `review-resolution` |
| Explain change | `docs/changes/<change-id>/explain-change.md` | `explain-change` |
| Verify report | `docs/changes/<change-id>/verify-report.md` when required | `verify` |
| Reports | `docs/reports/` | release / verify / measurement workflows |

If a project customizes artifact locations, it should update this table. Skills should use the table before falling back to default paths.

## Skill artifact lookup rule

Public skills should use this lookup order when artifact placement matters:

```text
Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, or reviewed artifact path;
3. docs/workflows.md artifact-location table;
4. this skill's portable default path;
5. block on ambiguity.
```

Each skill should keep only its own short default. For example, `proposal` can say:

```text
Default proposal path: docs/proposals/YYYY-MM-DD-slug.md.
Use the project workflow guide if it customizes proposal locations.
```

Review skills can say:

```text
Default review path: docs/changes/<change-id>/reviews/<stage>-r<n>.md.
Use the project workflow guide and formal review recording rules for exact placement.
```

## Workflow skill responsibility

Update `workflow` so it owns the guide, not every artifact.

`workflow` should be responsible for:

- routing work through the standard workflow;
- auditing current workflow state;
- creating or refreshing `docs/workflows.md`;
- keeping the artifact location table visible;
- pointing users to the owning stage skill.

`workflow` should not be responsible for:

- writing proposals, specs, plans, reviews, or ADRs;
- inventing detailed schemas;
- replacing stage skills;
- replacing formal review recording rules.

## Workflow guide refresh triggers

The `workflow` skill should create or refresh `docs/workflows.md` when:

- RigorLoop is adopted in a project and no workflow guide exists;
- artifact locations are added, removed, renamed, or customized;
- review-recording, examples, reports, or change-root placement changes;
- stage skill guidance starts relying on the artifact-location table;
- generated-output or adapter source-of-truth guidance changes;
- the existing guide contradicts current repository paths or governing specs.

For ordinary task routing where the guide is current, `workflow` should reference the guide rather than rewrite it.

## Stage skill responsibility

Each stage skill should:

- read the project workflow guide when artifact placement matters;
- use the location table when present;
- fall back to portable default paths;
- stop when the location is ambiguous;
- own only its artifact content and handoff.

Review skills should not duplicate the full change-ID selection algorithm or receipt template. They should use the formal review recording rule and the project artifact map.

## Formal review recording responsibility

Exact review receipt and review-root shape should live in:

```text
specs/formal-review-recording.md
```

Filled examples should live in:

```text
docs/examples/formal-review-recording/
```

The formal review recording spec should own clean receipt root and metadata requirements. Validators need precise rules for `change.yaml.review` fields such as `status: clean`, reviewed artifact, review log, and zero unresolved items.

## Examples surface

`docs/examples/` should remain the non-normative examples surface.

Recommended layout:

```text
docs/examples/
  README.md
  plans/
    example-plan.md
  changes/
    skill-validator/
  formal-review-recording/
    clean-review-receipt.md
    clean-review-log-entry.md
    blocked-clean-review-recording.md
    material-finding-review-record.md
    material-finding-location-examples.md
    change-id-selection-examples.md
```

`docs/examples/README.md` should continue to say that examples are non-normative, illustrate artifact shape and common patterns, and are not active lifecycle state.

The current repository already has the examples root, the plan example, and formal review examples. The skill-validator proof pack should move to `docs/examples/changes/skill-validator/` only if references, tests, validators, and selector routing can be updated in the same change. If it is still needed as a live validator fixture, retain it with explicit rationale and schedule a follow-up.

## Examples validation and routing

`docs/examples/**` is non-normative example content.

Selector routing should classify it as documentation or example content, not as active lifecycle state.

Lifecycle validators should not treat `docs/examples/**` as active proposals, active plans, active change roots, active review records, or active reports unless a specific test fixture explicitly opts in.

Acceptance for this policy should include:

- explicit selector coverage for `docs/examples/**`;
- lifecycle validation does not treat `docs/examples/plans/example-plan.md` as an active plan;
- `docs/examples/formal-review-recording/**` examples do not trigger review-record closeout requirements.

## Retained fixture contract

`docs/changes/0001-skill-validator/` is an active-looking path retained only as a validator fixture and historical proof pack.

If it stays in `docs/changes/`, implementation should add a durable retained-fixture marker or rationale in a visible local surface such as the fixture README, change metadata, workflow guide, or validator documentation. That marker should say:

- the fixture is not an active change root;
- it is not the universal template or minimum artifact pack for non-trivial work;
- it remains only because tests, validators, or compatibility references still rely on that path;
- the move target is `docs/examples/changes/skill-validator/` once references can be updated safely.

If those references can be updated in the same implementation slice, move it to `docs/examples/changes/skill-validator/` instead.

## Expected behavior changes

Before this change, each skill may carry its own path rules, examples, and fallback logic.

After this change, `docs/workflows.md` provides the project artifact map and skills consult it while staying concise.

Before this change, examples could look like active lifecycle artifacts.

After this change, examples live under `docs/examples/` where practical and are explicitly non-normative. Any retained fixture in an active-looking path has a visible rationale.

Before this change, users may not know where review receipts, change metadata, examples, and reports go.

After this change, `docs/workflows.md` answers where artifacts go and points to specs or references for exact shapes.

## Architecture impact

No runtime architecture change is expected.

This is a workflow-guide and artifact-placement clarity change. Affected surfaces may include:

- `docs/workflows.md`;
- `skills/workflow/SKILL.md`;
- stage skills that need concise lookup wording;
- `docs/examples/`;
- `docs/changes/0001-skill-validator/` if it can move safely;
- selector routing;
- artifact lifecycle validation;
- change metadata tests;
- review artifact tests.

## Testing and verification strategy

Likely validation includes:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/validate-review-artifacts.py
python scripts/validate-change-metadata.py <affected change.yaml>
git diff --check --
```

If examples move and selectors are affected:

```bash
python scripts/select-validation.py --mode explicit --path docs/examples/plans/example-plan.md
python scripts/select-validation.py --mode explicit --path docs/examples/changes/skill-validator/change.yaml
```

If canonical skills change:

```bash
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
```

## Rollout and rollback

Roll out the change in small reviewable slices:

- add or update the `docs/workflows.md` artifact location table and `workflow` skill guide ownership wording;
- update stage skills with concise project-guide lookup wording where artifact placement matters;
- complete the examples surface by keeping examples under `docs/examples/` and deciding whether `docs/changes/0001-skill-validator/` remains a fixture or moves with updated references;
- update selector, lifecycle, review, and change-metadata validation for the final placement choices;
- refresh generated skills and adapters when canonical skills change.

Rollback is documentation-first: revert the artifact map and skill lookup wording if it causes ambiguous routing, restore moved fixtures if validation coupling breaks, and keep any already-moved examples under `docs/examples/` only when selectors and validators still classify them consistently as non-lifecycle examples.

No new spec is expected for changes limited to `docs/workflows.md`, workflow skill guide ownership wording, concise stage-skill lookup wording, and examples README or placement cleanup.

A spec or test-spec update is expected if implementation changes selector routing policy for `docs/examples/**`, lifecycle validation behavior, formal review root/schema rules, or makes the artifact-location table normative beyond default locations.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| `docs/workflows.md` becomes too large | Keep only the artifact location map and concise summaries; details stay in specs or references |
| Skills cannot find paths in a customized project | Use the lookup order and block on ambiguity |
| Example movement breaks tests | Move only with reference updates, or defer deeply coupled fixtures |
| Review receipt rules get duplicated in skills | Keep exact shape in spec/reference; skills use concise pointer wording |
| Downstream users lack specs | Ensure `docs/workflows.md` has enough default locations to operate |
| Selector blocks `docs/examples/**` | Add routing or explicit ignore behavior |

## Open questions

No open question blocks proposal review.

Implementation planning should still make two scoped decisions:

- whether `docs/changes/0001-skill-validator/` can move to `docs/examples/changes/skill-validator/` in the same slice as its reference, test, validator, and selector updates; if not, retain it with the retained-fixture marker described above;
- whether artifact-location table generation from a template is worth scheduling as a later follow-up, or should remain out of scope until repeated drift appears.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-13 | Use `docs/workflows.md` as the project artifact location guide. | Public skills need one project-local path source after detailed path rules are removed. | Duplicating path rules in every skill; spec-only placement guidance |
| 2026-05-13 | Make `workflow` responsible for creating or refreshing the guide. | Workflow owns routing and guide generation, not every artifact's content. | Making `workflow` write all lifecycle artifacts |
| 2026-05-13 | Keep examples under `docs/examples/` where practical. | Examples should not look like active lifecycle state. | Keeping illustrative examples in active lifecycle directories |
| 2026-05-13 | Keep exact shapes in specs or references. | Skills should stay concise and portable. | Copying exact review and artifact shapes into every public skill |
| 2026-05-13 | Classify `docs/examples/**` as non-lifecycle example content. | Examples should not trigger active lifecycle state, review closeout, or plan validation requirements unless a fixture explicitly opts in. | Leaving selector/lifecycle behavior open through implementation |

## Next artifacts

```text
spec-review
architecture if needed
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Proposal review: [proposal-review-r1](../changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/proposal-review-r1.md)
- Spec: [Project Artifact Location Guide and Examples Surface](../../specs/project-artifact-location-guide-and-examples-surface.md)

## Readiness

Accepted. Follow-on spec drafted; see Follow-on artifacts for review evidence and downstream contract.

## Core invariant

```text
workflow maintains the artifact map.
docs/workflows.md tells skills where artifacts go.
stage skills own artifact content.
specs own exact shapes.
docs/examples owns examples.
```
