# Behavior Preservation: Test-Spec Contract Normalization

## Scope

This evidence covers M3 of [Test-Spec Contract Normalization](../../plans/2026-05-20-test-spec-contract-normalization.md): the canonical `skills/test-spec/SKILL.md` normalization.

The change adds contract-required structure:

- frontmatter `version: "1.0.0"`;
- frontmatter `schema-version: skill-readability-v1`;
- `Workflow role`;
- dedicated `Stop conditions`;
- fenced `Output skeleton`.

It does not change the frontmatter `description`, required section list, test-case format, coverage rules, durable state guidance, or produced artifact obligations.

## Preservation Matrix

| Source content | Existing location | New location | Change type | Preservation proof |
| --- | --- | --- | --- | --- |
| `Do not generate tests from an unreviewed or unstable spec unless the user explicitly requests isolated test-planning output and the limitation is recorded.` | `skills/test-spec/SKILL.md`, `Rules` | `Stop conditions` | moved | Same blocker, same exception, and same required limitation recording are preserved. The wording changed only from "Do not generate tests..." to "Stop and report the blocker instead of producing a test spec when..."; no new blocking state was added. |
| `Do not generate tests from a spec-review outcome that explicitly marked eventual test-spec readiness as not-ready or not-assessed.` | `skills/test-spec/SKILL.md`, `Rules` | `Stop conditions` | moved | Same spec-review outcomes, same explicit eventual readiness condition, and same prohibition on producing a test spec are preserved. |
| 19 required sections | `Required sections` numbered list | `Output skeleton` | skeletonized | The skeleton contains the same section set: Status; Related spec and plan; Testing strategy; Requirement coverage map; Example coverage map; Edge case coverage; Test cases; Fixtures and data; Mocking/stubbing policy; Migration or compatibility tests; Observability verification; Security/privacy verification; Performance checks; Manual QA checklist; What not to test and why; Uncovered gaps; Next artifacts; Follow-on artifacts; Readiness. |
| `T1. Title` test-case ID and title format | `Test case format` fenced block | `Output skeleton`, `Test cases` section | skeletonized | The skeleton keeps stable test-case IDs through `### T1. <Title>` and keeps the existing title requirement. |
| Test case fields: Covers, Level, Fixture/setup, Steps, Expected result, Failure proves, Automation location | `Test case format` fenced block | `Output skeleton`, `Test cases` section | skeletonized | The skeleton includes the same fields and does not add any field. |
| Requirement coverage map | `Required sections` item 4 and `Coverage rules` | `Output skeleton`, `Requirement coverage map` section | skeletonized | The skeleton includes a requirement coverage table and keeps the obligation that every requirement ID maps to one or more tests or explicit manual verification through the unchanged required-section text and coverage rules. |
| Example coverage map | `Required sections` item 5 | `Output skeleton`, `Example coverage map` section | skeletonized | The skeleton includes an example coverage table and does not add new example coverage rules. |
| Edge case coverage | `Required sections` item 6 and `Coverage rules` | `Output skeleton`, `Edge case coverage` section | skeletonized | The skeleton includes edge-case coverage and preserves the existing boundary/edge proof intent. |
| Coverage rules for `MUST`, error behavior, migration/compatibility, architectural boundaries, and bugs | `Coverage rules` | unchanged `Coverage rules`; reflected by skeleton sections | unchanged plus skeletonized | The rule text remains unchanged. The skeleton only provides locations for the already-required proof. |
| Durable state guidance for `draft`, `active`, `abandoned`, `superseded`, `archived` | `Required sections` item 1 and `Rules` | unchanged `Required sections` and `Rules`; reflected by skeleton `Status` | unchanged plus skeletonized | The durable state guidance remains unchanged and the skeleton uses the same state set. |
| Routing description | frontmatter `description` | frontmatter `description` | unchanged | The `description` text is unchanged. |
| Project artifact lookup behavior | `Artifact placement` | `Artifact placement` | portable wording adjustment | The lookup order remains the same. The wording now keeps the existing static phrase for this repository while adding "when present" to preserve published-skill portability under the readability contract. |

## Stop-Condition Result

The dedicated `Stop conditions` section contains only the two prior invocation blockers from `Rules`:

- unreviewed or unstable source spec, with the same isolated-output exception and limitation-recording requirement;
- spec-review outcome explicitly marking eventual `test-spec` readiness as `not-ready` or `not-assessed`.

No third blocker was added. No blocker was removed or weakened.

## Output-Skeleton Result

The output skeleton is a compact shape of the artifact already required by `test-spec`. It adds no new required section, test-case field, coverage map, coverage rule, durable state, generated artifact, or packaging resource.

## Scope Guard

Out of scope and unchanged:

- no tabulation of required-section prose;
- no enum fencing;
- no `spec` or `spec-review` skill-body edits;
- no packaged `assets/`, `references/`, or `scripts/`;
- no routing-description rewrite.
