# Project Artifact Location Guide and Fixture Ownership

## Status

approved

## Related proposal

- [Project Artifact Location Guide and Examples Surface](../docs/proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md)

## Goal and context

This spec defines the contract for the project-local artifact-location map, test-owned fixture handling, and skill lookup behavior.

Public RigorLoop skills are being simplified so they do not carry long duplicated path rules, example directories, review-root algorithms, generated-output details, or repository-maintainer internals. After that simplification, users and agents still need a project-local answer to where proposals, specs, plans, review records, change metadata, examples, reports, and generated outputs belong.

The contract is intentionally split:

- `docs/workflows.md` provides the user-facing project-local artifact-location map.
- Stage skills create or update their own artifacts using the map when placement matters.
- Specs, schemas, and references define exact artifact shape, lifecycle state, and validation rules.
- Reusable authoring shapes live in owning skill assets, while executable cases live in tests.

## Glossary

- `artifact-location map`: the `Artifact locations` section in `docs/workflows.md` that lists default artifact locations and owning skills for the current project.
- `project workflow guide`: the project-local `docs/workflows.md` operating guide.
- `stage skill`: a skill that creates, reviews, verifies, or hands off a workflow artifact, such as `proposal`, `spec`, `plan`, `proposal-review`, `verify`, or `pr`.
- `portable default path`: a built-in fallback path that a public skill can use when no project-specific location is configured.
- `exact shape`: required fields, schema, lifecycle status values, review-record structure, validation behavior, and other normative artifact details beyond default location.
- `test fixture`: temporary or tracked test-only input that must not become project lifecycle state.
- `retained fixture`: an active-looking path kept temporarily or permanently because validator tests, compatibility checks, or historical proof references still depend on it.

## Examples first

### Example E1: artifact map answers the common path question

Given a user asks where new proposals and review receipts go
When the project has a current `docs/workflows.md`
Then the user can find an `Artifact locations` section
And the section lists default locations for proposals and formal review records
And it points to the owning skill for each artifact type.

### Example E2: exact review shape stays in the formal review spec

Given the artifact map lists formal review records under `docs/changes/<change-id>/reviews/<stage>-r<n>.md`
When an agent needs the required clean receipt fields or review-log indexing rules
Then the agent uses `specs/formal-review-recording.md`
And the artifact map is not treated as the complete review-record schema.

### Example E3: customized project location outranks a portable default

Given `docs/workflows.md` configures proposals under a project-specific proposal directory
When the `proposal` skill creates a proposal and the user did not provide an explicit path
Then the skill uses the configured project location
And it does not fall back to `docs/proposals/YYYY-MM-DD-slug.md`.

### Example E4: explicit user path outranks the artifact map

Given a user explicitly asks to write a spec at `specs/custom-contract.md`
When the project artifact map lists `specs/slug.md`
Then the skill uses `specs/custom-contract.md`
Unless a higher-priority governance artifact or safety rule blocks that path.

### Example E5: examples are not active lifecycle state

Given a lifecycle edge case needs executable proof
When repository tests create a temporary plan-shaped fixture
Then the fixture remains isolated from the real repository lifecycle state.

### Example E6: formal review examples do not trigger closeout

Given review-recording behavior needs a fixture
When a repository test creates that fixture in a temporary root
Then the fixture is validated only within that test root.

### Example E7: skill-validator fixtures are test-owned

Given a skill-validator case is synthetic
When it is stored in the repository
Then it lives under `tests/fixtures/`
And it cannot be mistaken for an active or historical project change root.

### Example E8: workflow refreshes stale artifact placement

Given `docs/workflows.md` says reports live under an obsolete path
When the `workflow` skill audits current project routing
Then it refreshes the guide or reports the contradiction
And ordinary task routing uses the current guide without rewriting it when no placement change exists.

### Example E9: lookup uses the path index without broad authority scans

Given a stage skill needs the default location for a new artifact
And no explicit path, active metadata, known spec constraint, or conflict exists
When `docs/workflows.md` has a current artifact-location map
Then the skill uses that map as the concise path index
And it does not broad-search approved specs or schemas solely to discover the path.

## Requirements

R1. `docs/workflows.md` MUST provide the user-facing project-local artifact-location map when RigorLoop artifact placement matters.

R1a. The artifact-location map MUST be in a clearly labeled `Artifact locations` section or an equivalent section whose purpose is unambiguous.

R1b. The artifact-location map MUST define default locations and owning skills, not exact artifact schemas, required fields, lifecycle status values, or validation rules.

R1c. The artifact-location map MUST state that exact artifact shapes are owned by the governing spec, schema, or reference for the artifact type.

R1d. `docs/workflows.md` MUST NOT override `CONSTITUTION.md`, approved specs, approved architecture or ADR records, active plan state, matching test specs, schemas, or explicit user-provided paths.

R2. Artifact placement MUST use this source rank when sources conflict:

1. explicit user-provided path or change ID;
2. active artifact metadata, active plan metadata, or active change metadata;
3. approved project specs or schemas;
4. `docs/workflows.md` artifact-location map;
5. portable default path;
6. block on ambiguity.

R2a. An explicit user-provided path or change ID MUST NOT override a higher-priority governance, safety, schema, or security constraint.

R2b. If artifact placement remains ambiguous after applying the source rank, the skill MUST stop and report the missing or conflicting artifact-location evidence.

R2c. The source rank in `R2` is a precedence rule, not a mandatory read order.

R2d. A stage skill MUST NOT search or read every approved spec, schema, architecture record, or governance artifact solely to discover artifact locations.

R2e. When artifact placement matters, a stage skill SHOULD use the project artifact-location map as the concise path index, while still obeying known governing specs, schemas, active artifact metadata, explicit user paths, and safety constraints.

R2f. If a governing spec or schema is already known to constrain the artifact type, exact shape, or placement, the skill MUST apply that constraint before relying on the workflow guide or portable default path.

R2g. If a conflict is discovered between `docs/workflows.md` and a higher-priority source, the higher-priority source wins and the skill MUST report or resolve the stale artifact-location map.

R3. The `workflow` skill MUST create or refresh `docs/workflows.md` when any of these triggers apply:

- RigorLoop is adopted in a project and no workflow guide exists;
- artifact locations are added, removed, renamed, or customized;
- review-recording, examples, reports, or change-root placement changes;
- stage skill guidance starts relying on the artifact-location map;
- generated-output or adapter source-of-truth guidance changes;
- the existing guide contradicts current repository paths or governing specs.

R3a. For ordinary task routing where the guide is current, `workflow` SHOULD reference the guide rather than rewrite it.

R3b. `workflow` MUST NOT become responsible for authoring proposals, specs, plans, reviews, ADRs, or exact schemas solely because it owns the artifact-location map.

R4. The artifact-location map MUST include default locations for at least these artifact types when the project supports them:

- project vision;
- workflow guide;
- examples;
- proposals;
- specs;
- test specs;
- architecture records;
- ADRs;
- plans;
- plan index;
- change root;
- change metadata;
- formal review records;
- review log;
- review resolution;
- explain-change record;
- verify report;
- reports.

R4a. The formal review records row MUST indicate that it is a default location only and that exact receipt/root rules are owned by the formal review recording contract.

R4b. The review resolution row MUST indicate that `review-resolution.md` is conditional on findings, blocking outcomes, or another approved disposition trigger.

R4c. The verify report row MUST indicate that `verify-report.md` is conditional when the workflow or verification contract requires standalone report evidence.

R5. Public stage skills MUST use concise shared lookup wording when artifact placement matters.

R5a. The shared lookup wording MUST describe this discovery order:

1. explicit user path or change ID;
2. active plan, active change metadata, reviewed artifact path, or current artifact metadata;
3. known governing spec or schema constraint for this artifact type, when already identified or directly relevant;
4. `docs/workflows.md` artifact-location table;
5. the skill's portable default path;
6. block on ambiguity.

R5aa. The shared lookup wording MUST state that the discovery order remains subordinate to the `R2` source-rank rule when sources conflict.

R5b. Individual stage skills SHOULD keep only their own short portable default path in addition to shared lookup wording.

R5c. Public stage skills MUST NOT duplicate long artifact-location tables, long review-root algorithms, or long example path lists when the project workflow guide and governing specs already own that information.

R5d. Public skill wording MUST remain project-portable and MUST NOT hardcode RigorLoop repository-internal validator paths where the project workflow guide is sufficient.

R5e. Public stage skills SHOULD use token-efficient placement lookup.

R5f. Public stage skills SHOULD start from the current artifact, active metadata, and `docs/workflows.md` artifact-location map instead of broad-searching governing documents.

R5g. Public stage skills SHOULD read a governing spec or schema only when:

- the artifact type has a known governing spec;
- the workflow guide points to that spec;
- the current artifact or change metadata cites it;
- a placement conflict is detected;
- exact artifact shape is needed, not just default location.

R6. The repository MUST NOT maintain a parallel documentation examples surface for lifecycle artifacts.

R6a. Reusable authoring shapes MUST live in owning skill assets or normative specifications.

R6b. Selector routing MAY retain a bounded compatibility classification for deleted example paths until the deletion no longer appears in the comparison baseline.

R6c. Lifecycle validation tests MUST isolate temporary fixtures from the real repository root.

R6d. The packaged plan skeleton MUST remain the sole maintained plan-authoring scaffold.

R6e. Formal-review test fixtures MUST live in tests or temporary test roots rather than production documentation.

R7. Synthetic validator cases MUST live under `tests/fixtures/`, not `docs/changes/`.

R7a. Tests MUST NOT depend on a production documentation path solely to obtain synthetic validator input.

R7b. Deleted historical proof MUST remain recoverable through Git history rather than a live special-case directory.

R7c. Fixture paths and identifiers SHOULD describe the case they exercise.

R7d. Removing a production-path fixture MUST update its references, selectors, validators, tests, and current guidance in the same slice.

R8. When examples or fixtures move, references, tests, validators, selectors, and contributor-facing guidance that cite the moved paths MUST be updated in the same slice.

R8a. If a production-path fixture cannot be removed safely in one slice, the implementation MUST stop and define a bounded migration rather than make the exception permanent.

R9. The artifact-location map MUST preserve custom project paths.

R9a. If a project customizes artifact locations, skills MUST use the customized locations from `docs/workflows.md` before falling back to portable defaults.

R9b. A project-local customization MUST NOT require every public skill to embed the custom path table.

R10. Generated output and adapter guidance MUST remain source-of-truth aware.

R10a. If canonical skill source changes, generated skill mirrors and adapter output MUST be refreshed or checked according to the active plan and validation commands.

R10b. Public skill text MUST NOT expose repository-maintainer-only generated-output internals when project-portable wording is sufficient.

R11. The artifact-location map MUST be testable through repository-owned validation.

R11a. Validation MUST include bounded selector coverage for deleted example paths while deletion compatibility is required.

R11b. Lifecycle tests MUST use temporary repositories for plan-shaped negative fixtures.

R11c. Review-artifact tests MUST use temporary repositories or test-fixture paths for review-shaped negative cases.

R11d. Validation MUST prove that skill-validator fixtures and their references remain test-owned.

R12. This spec MUST NOT change the standard workflow order.

R12a. This spec MUST NOT redesign formal review recording, review-resolution disposition rules, or clean receipt schema.

R12b. This spec MUST NOT make `docs/workflows.md` a higher-priority source than approved specs, schemas, architecture artifacts, active plan metadata, or explicit user paths.

## Inputs and outputs

Inputs:

- user-provided artifact paths or change IDs;
- active proposal, spec, plan, review, change metadata, and reviewed artifact paths;
- approved specs and schemas that define exact artifact shape;
- project workflow guide content in `docs/workflows.md`;
- portable default paths built into public skills;
- selector and lifecycle validation inputs for changed paths;
- generated skill and adapter output when canonical skill source changes.

Outputs:

- an updated `docs/workflows.md` artifact-location map;
- concise stage-skill artifact lookup wording;
- updated owning skill assets or test fixtures when reusable shapes or executable cases change;
- test-owned fixtures for synthetic validator cases;
- selector, lifecycle, skill, and review-artifact validation evidence for changed behavior;
- refreshed generated skill or adapter output when canonical skills change.

## State and invariants

- `docs/workflows.md` tells users where artifacts go.
- Specs and schemas define exact shapes and validation rules.
- Stage skills own artifact content and handoff.
- `workflow` owns guide creation, refresh, routing, and state audit; it does not author every artifact type.
- Documentation does not own reusable lifecycle scaffolds or executable fixtures.
- Retained active-looking fixtures require visible rationale.
- Ambiguous artifact placement blocks instead of silently guessing.

## Error and boundary behavior

- If `docs/workflows.md` is missing during RigorLoop adoption, `workflow` creates it before relying on project-local artifact placement.
- If `docs/workflows.md` is stale or contradicts approved specs, schemas, or current paths, `workflow` refreshes it or reports the contradiction before downstream reliance.
- If a stage skill cannot determine artifact placement after applying the source rank, it stops and reports the missing location evidence.
- If an explicit user path conflicts with a higher-priority governance, schema, security, or safety rule, the skill reports the conflict instead of writing there.
- If a test fixture contributes active state to the real repository, validation must fail until fixture isolation is corrected.
- If a test relies on a synthetic record under `docs/changes/`, validation or review must block until the case moves to test-owned fixtures.

## Compatibility and migration

Existing downstream projects may already customize artifact paths. This spec preserves those customizations by making `docs/workflows.md` the project-local map and by requiring skills to use that map before portable defaults.

Existing active lifecycle artifacts remain valid. This spec does not require historical proposals, specs, plans, reviews, or change roots to move.

Historical references to the retired examples surface remain historical evidence and are not rewritten.

Deleted historical proof remains recoverable through Git history and does not require a live compatibility directory.

Rollback for implementation slices is documentation-first: revert artifact-map and skill lookup wording if they cause ambiguous routing, and restore moved fixtures only when validation coupling breaks.

## Observability

This behavior is observed through tracked artifacts and validation output:

- `docs/workflows.md` visibly contains the artifact-location map and source-rank disclaimer.
- Stage skill text visibly uses concise lookup wording.
- Owning skill assets contain reusable authoring shapes.
- Selector output handles deleted example paths only through bounded compatibility.
- Lifecycle tests isolate temporary fixtures from active project state.
- Review artifact validation does not require active closeout for formal-review examples.
- Synthetic validator inputs are visibly owned by `tests/fixtures/`.

## Security and privacy

This spec introduces no new secrets, credentials, tokens, private keys, user data, or runtime data collection.

Artifact-location guidance MUST NOT encourage committing machine-local paths, usernames, credentials, or host-specific debug artifacts except when a reviewed example intentionally includes a machine-local path with clear justification.

Public skill text MUST avoid repository-maintainer internals where project-portable wording is sufficient, reducing accidental leakage of local packaging or validation implementation details into downstream user guidance.

## Accessibility and UX

No UI is involved.

The user-facing artifact-location map should remain concise, scannable, and table-based so users can find default locations without reading every governing spec.

## Performance expectations

No runtime performance behavior is involved.

Validation should remain targeted to changed surfaces where possible. Broad validation is required only when the active plan, test spec, selector, release process, or another authoritative trigger requires it.

## Edge cases

EC1. `docs/workflows.md` exists but lacks artifact locations: `workflow` refreshes it before skills rely on the map.

EC2. A project customizes proposal paths: `proposal` uses the project map before its portable default.

EC3. A user provides an explicit path: the skill uses it unless higher-priority governance, schema, security, or safety constraints block it.

EC4. A temporary fixture looks like a plan: lifecycle validation remains scoped to the temporary repository.

EC5. A formal review example contains review-like headings: validation does not treat it as an active review record unless an explicit fixture opt-in exists.

EC6. A synthetic validator input is placed under `docs/changes/`: validation or review requires it to move under `tests/fixtures/`.

EC7. A deleted historical proof pack is needed for investigation: the contributor retrieves it from Git history without restoring it as maintained documentation.

EC8. A skill cannot determine a change root after source-rank lookup: it blocks on ambiguity instead of inventing an unrelated path.

EC9. A table row appears to define schema: the artifact map disclaimer and governing spec references take precedence.

EC10. Canonical skills change: generated public skill and adapter output is checked or regenerated according to the active plan and validation commands.

## Non-goals

- Do not change the standard workflow order.
- Do not redesign formal review recording.
- Do not redefine review-resolution dispositions or closeout rules.
- Do not make `workflow` write every artifact type.
- Do not make `docs/workflows.md` override higher-priority governance, specs, schemas, architecture artifacts, active plan state, or explicit user paths.
- Do not require every public skill to duplicate the full artifact-location table.
- Do not require immediate movement of retained fixtures when validator or compatibility coupling remains.
- Do not change generated adapter packaging behavior except where canonical skill changes require the normal generated-output refresh or check.

## Acceptance criteria

- `docs/workflows.md` contains an artifact-location map with source-rank and schema-disclaimer wording.
- `workflow` guidance states when it creates or refreshes the workflow guide and artifact-location map.
- Stage skills use concise project-guide lookup wording when artifact placement matters.
- The spec distinguishes artifact-location source rank from skill lookup and read order.
- Stage-skill shared lookup wording includes known governing spec/schema constraints without requiring broad spec/schema searches.
- Public skills are instructed to use `docs/workflows.md` as the concise artifact-location index.
- Public skills consult governing specs or schemas only when they are known to constrain the artifact, the guide points to them, a current artifact or metadata cites them, a conflict is detected, or exact shape is needed.
- Tests or static checks prove shared lookup wording does not bypass the `R2` source-rank rule.
- Tests or static checks prove public skill wording discourages broad authoritative-document path searches.
- The repository has no parallel documentation examples surface.
- Selector coverage handles deleted example paths only for transition compatibility.
- Lifecycle validation uses isolated temporary fixtures for plan-shaped cases.
- Formal review tests use temporary repositories or test fixtures.
- Synthetic validator cases live under `tests/fixtures/` and production-path special cases are removed.
- Formal review receipt/root shape remains governed by `specs/formal-review-recording.md`.
- No public skill hardcodes RigorLoop-only internal validator paths when project-local guide wording is sufficient.

## Open questions

None.

None.

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

- Spec review: [spec-review-r1](../docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/spec-review-r1.md), [spec-review-r2](../docs/changes/2026-05-13-project-artifact-location-guide-and-examples-surface-review-recording/reviews/spec-review-r2.md)
- Plan: [Project Artifact Location Guide and Examples Surface Plan](../docs/plans/2026-05-13-project-artifact-location-guide-and-examples-surface.md)
- Test spec: [Project Artifact Location Guide and Examples Surface Test Spec](project-artifact-location-guide-and-examples-surface.test.md)

## Readiness

Approved. Ready for planning and test-spec authoring.

## Prospective stage-owned lifecycle amendment notice

For a change declaring
`lifecycle_contract: stage-owned-change-local-v1`, this specification defers
active-plan metadata as current lifecycle authority or a higher-ranked mutable
path source to
[Stage-Owned Lifecycle Artifacts and Change-Local Workflow State](stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md).

Artifact-location guidance, example isolation, path lookup, and
generated-surface validation remain governed here.
