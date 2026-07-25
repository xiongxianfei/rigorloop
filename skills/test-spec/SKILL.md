---
name: test-spec
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Generate a traceable test specification from an approved feature spec and execution plan before writing test code or production code. Use to map requirements, examples, edge cases, architecture boundaries, and milestones into concrete tests.
argument-hint: [feature spec path, plan path, or feature name]
---

# Test spec authoring

You are designing the proof before implementation.

The test spec defines how the team will know the implementation satisfies the behavioral contract.

## Workflow role

- role_name: test-spec
- stage: authoring
- upstream: approved spec, spec-review findings, approved plan, and relevant architecture or ADR records when present
- downstream: test-spec-review
- summary: Design the proof mapping requirements, examples, edge cases, architecture boundaries, and milestones to tests before implementation.
- must_not_claim: implementation completion, code-review approval, verification, branch readiness, or PR readiness.

## Stop conditions

Stop and report the blocker instead of producing a test spec when:

- the source spec is unreviewed or unstable, unless the user explicitly requests isolated test-planning output and the limitation is recorded;
- the relevant spec-review outcome explicitly marked eventual `test-spec` readiness as `not-ready`.

## Inputs to read

Read:

- approved feature spec;
- spec-review findings;
- architecture doc and ADRs when relevant;
- concrete execution plan;
- `AGENTS.md` and `CONSTITUTION.md` if present;
- existing test conventions, fixtures, helpers, and CI commands;
- related tests for similar behavior.

## Output path

Prefer:

```text
specs/slug.test.md
```

## Artifact placement

Use the project workflow guide for artifact locations when placement matters.

Lookup order:

1. explicit user path or change ID;
2. active plan, change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint when directly relevant;
4. project workflow guide artifact-location table, such as the `docs/workflows.md` artifact-location table when present;
5. this skill's portable default path;
6. block on ambiguity.

This discovery order is subordinate to the source-rank rule in the project workflow guide when sources conflict.

Do not broad-search authoritative documents just to find paths. Use `docs/workflows.md` as the path index when present in this project, and consult specs or schemas only when they govern exact shape, placement, or a detected conflict.

## Resource map

- COPY `assets/test-spec-skeleton.md` when creating or fully rewriting a test spec.
  Fill: title, sections, coverage maps, test cases, artifacts, and readiness.
  Do not emit unfilled placeholders.
- COPY `assets/test-case.md` when adding each test case.
  Fill: test ID, title, covers, level, command IDs, setup, steps, expected result, failure proof, evidence artifact, automation location, and required milestone.
  Do not emit unfilled placeholders.
- COPY `assets/coverage-map-row.md` when adding requirement or example coverage-map rows.
  Use the `Requirement coverage row` variant for the requirement coverage map.
  Use the `Example coverage row` variant for the example coverage map.
  Fill: fields exactly as shown by the selected variant.
  Do not add a `Level` column to the example coverage map.
  Do not emit unfilled placeholders.
- COPY `assets/validation-command-row.md` when adding each validation-command ledger row.
  Fill: command ID, command, classification, owner, owning milestone, first required milestone, failure behavior, zero-test behavior, evidence artifact, and safe-mode or side-effect boundary.
  Do not emit unfilled placeholders.
- COPY `assets/milestone-proof-row.md` when adding each milestone proof-map row.
  Fill: milestone, required test IDs, manual proof IDs or none, command IDs or none, evidence artifacts, required-before gate, and notes.
  Do not emit unfilled placeholders.

## Generated Markdown readability

When this skill creates or updates generated or generator-shaped Markdown:

- Use semantic source lines for human-facing prose; one sentence or natural clause per source line when practical.
- Preserve stable IDs for requirements, findings, commands, milestones, and evidence; use tables for repeated mappings.
- Keep commands fenced or table-owned when they carry proof.
- Diagrams are optional. Use them only when they reduce cognitive load and map to real artifacts, stages, components, actors, or states.
- Do not require manual-proof contracts from this readability guidance alone; use governing project rules when manual proof is otherwise required.

## Required sections

| Section | Requirement |
| --- | --- |
| Status | Use `<test spec status>`. |
| Related spec and plan | Include the related spec and plan. |
| Input artifact identities | Include when implementation or code-review will rely on the test spec. Record input kind, path, status or review state, and identity for the feature spec, relevant review records, plan, plan review, and architecture or ADR inputs when applicable. |
| Testing strategy | Cover unit, integration, end-to-end, smoke, manual, contract, and migration strategy. |
| Requirement coverage map | Every requirement ID maps to one or more tests or explicit manual verification. |
| Example coverage map | Every example maps to a test when feasible. |
| Edge case coverage | Include edge case coverage. |
| Validation commands | Required whenever the test spec names, references, or depends on validation commands. If no commands are part of the proof map, say so explicitly with rationale. |
| Milestone proof map | Required when the approved plan has milestones, staged validation, staged commands, or milestone-specific code-review boundaries. If not applicable, state `Not applicable` or equivalent rationale. |
| Test cases | Include test cases with stable IDs. |
| Fixtures and data | Include fixtures and data. |
| Mocking/stubbing policy | Include mocking/stubbing policy. |
| Migration or compatibility tests | Include when relevant. |
| Observability verification | Include when logs, metrics, traces, or audit events are required. |
| Security/privacy verification | Include when relevant. |
| Performance checks | Include when relevant. |
| Manual QA checklist | Include when automation is insufficient. |
| What not to test | Include what not to test and why. |
| Uncovered gaps | Include gaps that must return to spec or architecture. |
| Next artifacts | Include planned next steps while the test spec remains draft or active. |
| Follow-on artifacts | Include actual downstream artifacts or terminal disposition. If present before any real follow-ons exist, say `None yet`. |
| Readiness | Include truthful next-stage or active-proof-surface wording. |

## Test case format

Use:

```text
T1. Title
- Covers: R1, R3, E2
- Level: <test case level>
- Command IDs: <command IDs or none>
- Fixture/setup:
- Steps:
- Expected result:
- Failure proves:
- Evidence artifact:
- Automation location:
- Required by milestone:
```

If a test case uses or depends on a validation command, reference at least one Command ID from `Validation commands`. Do not rely only on raw command strings.

## Validation command ledger

Use `Validation commands` whenever the test spec names, references, or depends on validation commands. The section is optional only when no commands are part of the proof map, and then it must state that no validation commands are part of the proof map with rationale.

Use stable Command IDs such as `CMD1`, `CMD2`, and `CMD3`. Reference those IDs from test cases, milestone proof-map rows, and evidence notes.

Command classification is a closed enum:

```text
existing/configured
planned-for-implementation
release-owned
ci-owned
external-owned
not-applicable
```

Each validation-command row must record:

- Command ID;
- command;
- classification;
- owner;
- owning milestone;
- first required milestone;
- failure behavior;
- zero-test behavior;
- evidence artifact;
- safe-mode or side-effect boundary.

Command rules:

- Every named, referenced, or depended-on validation command gets a stable Command ID.
- A planned command must use `planned-for-implementation` and name an owner, owning milestone, and first required milestone.
- A planned command is not required before its first required milestone.
- A command expected to run tests must define zero-test behavior.
- Commands with network, publication, destructive, or external side effects must state the safe-mode or side-effect boundary.
- Missing required commands block implementation or milestone closeout according to the milestone proof map.
- During authoring, inspect known manifests and existing scripts when feasible, but do not execute validation commands.

## Milestone proof map

Use `Milestone proof map` when the approved plan has milestones, staged validation, staged commands, or milestone-specific code-review boundaries.

Each implementation milestone must map to test IDs, manual proof IDs or `none`, command IDs or `none`, evidence artifacts, and the gate where proof is required. A milestone may use an explicit not-applicable rationale only when no proof entry applies.

Milestone proof-map rules:

- Identify which proof is required before milestone code-review.
- Identify proof deferred to later milestones, verify, release-owned evidence, or another explicitly named stage.
- Do not let a milestone rely on a command whose ownership starts in a later milestone unless the row explicitly marks the command as planned and not yet required.

## Coverage rules

| Coverage target | Rule |
| --- | --- |
| `MUST` requirements | Every `MUST` requirement needs coverage. |
| Error behavior | Every error behavior needs coverage. |
| Migration or compatibility claims | Every migration or compatibility claim needs coverage or explicit manual verification. |
| Architectural boundaries that could break wiring | Every architectural boundary that could break wiring needs an integration or contract test. |
| Bugs | Bugs require a regression test that fails before the fix when feasible. |

## Closed enums

Test spec status:

```text
draft
active
abandoned
superseded
archived
```

Test case level:

```text
unit
integration
e2e
smoke
manual
```

Coverage map level:

```text
unit
integration
e2e
smoke
manual
contract
migration
```

## Output skeleton

```md
# <Test spec title>

COPY `assets/test-spec-skeleton.md` for the full test-spec structure. Use
`assets/test-case.md`, `assets/coverage-map-row.md`,
`assets/validation-command-row.md`, and `assets/milestone-proof-row.md`
for repeated structures.
```

Required sections are listed above. Do not emit unfilled placeholders.

## Rules

- Do not invent behavior not specified.
- Do not mark a requirement covered by a test that does not assert it.
- Do not rely only on snapshots for behavioral requirements.
- Do not skip integration tests where the risk is at a boundary.
- Do not use `reviewed` or long-lived `complete` as durable test-spec states. Move from `draft` to `active` when implementation or review is relying on the test spec, then close out to `archived`, `superseded`, or `abandoned` when it is no longer the active proof-planning surface.
- Preserve `Next artifacts` as planning history. Use `Follow-on artifacts` for actual downstream artifacts, replacement, or terminal closeout.
- Do not hide untestable requirements; send them back to `spec-review`.
- Do not treat downstream implementation readiness as a substitute for approved spec-review findings and concrete plan context.
- When changed boundaries still require approved architecture or ADR input, return the work to the appropriate upstream gate instead of guessing.
- Formal workflow-managed test specs route to `test-spec-review` before implementation.
- Under a unified run with valid implementation authority, the workflow may run deterministic test-spec settlement after authoring. Settlement records coverage, uncovered gaps, validation commands, and input artifact identities; it does not replace required `test-spec-review`.
- If settlement or `test-spec-review` reveals upstream ambiguity or stale inputs, pause instead of authorizing implementation. The first milestone's code-review rechecks the recorded input artifact identities before accepting the implementation review surface.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- test spec path;
- grouped test cases;
- requirement-to-test coverage map;
- fixtures and commands;
- explicit exclusions;
- uncovered gaps, if any;
- readiness statement for `test-spec-review`.
