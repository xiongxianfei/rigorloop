# Published Skill Design Spec Family Behavior Preservation Notes

## Scope

Changed rollout skills:

- `skills/spec/SKILL.md`
- `skills/spec-review/SKILL.md`

M1 records the preservation template and baseline protected behavior. M3 must fill the final rows after any behavior-significant wording is removed, moved, or rewritten.

## Preservation Template

| Skill | Removed or rewritten wording | Why safe | Essential rule preserved where |
| --- | --- | --- | --- |
| `spec` | Description routing was rewritten; project-local evidence and inputs were compacted; required section descriptions, workflow handoff wording, and expected output prose were compressed; an output skeleton was added. | Safe because the rewrite moves routing into frontmatter, adds workflow-role claim boundaries, keeps all required section names, keeps upstream settlement/output-path/artifact-placement/rules/evidence behavior, and adds a compact normative skeleton without deleting required behavior. | `skills/spec/SKILL.md` frontmatter `description`, `## Workflow role`, `## Project-local evidence`, `## Required sections`, `## Workflow handoff behavior`, `## Output skeleton`, and `## Expected output`. |
| `spec-review` | Description routing was rewritten; input and review-dimension prose was compacted; workflow role and output skeleton were added; expected-output prose was compressed. | Safe because the rewrite preserves the review gate, finding severity, material finding requirements, isolation/recording block, rules, workflow handoff boundaries, and expected result fields while adding portable routing and explicit claim boundaries. | `skills/spec-review/SKILL.md` frontmatter `description`, `## Workflow role`, `## Review dimensions`, `## Finding severity`, `## Material findings`, `## Isolation and Recording`, `## Rules`, `## Workflow handoff behavior`, `## Output skeleton`, and `## Expected output`. |

## `spec` Protected Behavior

M3 must preserve these behavior groups:

- write a behavioral contract before execution planning or implementation;
- define what the system must do and how behavior will be observed, without unnecessary internal implementation detail;
- use project-local artifacts when present and relevant, including `AGENTS.md`, `CONSTITUTION.md`, accepted proposals, issues, exploration and research artifacts, `docs/project-map.md`, `docs/workflows.md`, related local specs, architecture records, ADRs, interfaces, schemas, APIs, UI flows, config, and data contracts;
- avoid requiring RigorLoop repository-internal specs, docs, reports, follow-up files, or governance files in customer projects;
- preserve upstream status settlement behavior for workflow-managed downstream execution and keep review-only/manual inspection requests isolated;
- preserve output-path guidance under `specs/slug.md` and no-overwrite behavior for unrelated specs;
- preserve artifact-placement lookup order and source-rank subordination;
- preserve required spec sections, stable requirement-ID format, example format, and testability expectations for every `MUST`;
- preserve rules against vague requirements, buried requirements, skipped failure behavior, skipped compatibility expectations, invented requirements, and durable `reviewed` status;
- preserve workflow handoff behavior to `spec-review` when the spec has no blockers;
- preserve bounded evidence and full-file read escape conditions;
- preserve expected output: spec file path, examples first, requirement IDs, edge cases, non-goals, acceptance criteria, ambiguities, and readiness statement.

## `spec-review` Protected Behavior

M3 must preserve these behavior groups:

- independently review a feature spec before architecture, test planning, execution planning, or implementation;
- challenge requirement clarity, normative language, completeness, testability, examples, compatibility, observability, security/privacy, non-goals, and acceptance criteria;
- preserve finding severity semantics for `blocking`, `major`, and `minor`;
- preserve material finding completeness: finding ID, severity, location, evidence, required outcome, and safe resolution or needs-decision rationale;
- preserve formal review recording behavior, including recording status, blocker reporting, clean review receipts, detailed records for material findings, review log updates, and review-resolution when required;
- preserve direct/review-only isolation and avoid automatic downstream handoff;
- preserve rules against approving vague or untestable `MUST` requirements, collapsing spec review into plan/code review, editing the spec without request, or approving without eventual `test-spec` readiness;
- preserve immediate-next-stage rules, including not naming `test-spec` while architecture or plan still remains;
- preserve workflow handoff behavior: report outcome, immediate next repository stage, eventual test-spec readiness, and stop condition, then stop unless the user explicitly requests a later stage;
- preserve bounded evidence and full-file read escape conditions;
- preserve expected result output fields and review findings shape.

## M3 Closeout Rule

M3 must not close on structural validation alone if either rollout skill changes behavior-significant wording.

Closeout evidence must show:

- what wording moved or changed;
- why the change is safe;
- where the essential rule now lives;
- behavior-parity evidence did not weaken lifecycle rules.

## M3 Preservation Result

M3 changed behavior-significant wording, so closeout relies on the preservation
table above plus behavior-parity evidence. The rewrite did not remove protected
rules; it compressed duplicate prose, moved routing into `description`, added
workflow-role blocks, and added compact fenced output skeletons.
