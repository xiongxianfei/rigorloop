# Test Layering and Change-Scoped Validation

## Status

- accepted

## Problem

RigorLoop intentionally uses many validation surfaces because the project values reviewability, traceability, generated-output correctness, and release safety. The cost is that contributors and agents can spend too much time running broad checks before cheaper, change-relevant checks have proven the slice is even structurally sound.

The problem is not too many tests. The problem is that the project does not yet make test layering explicit enough for daily development. Full-repo validation is useful near handoff, but it is inefficient as the first proof step for every small workflow, skill, documentation, or generated-output slice.

## Goals

- Preserve current correctness and release-safety expectations.
- Make cheap, local, change-scoped checks the default first proof step.
- Separate targeted proof before review from broader smoke before merge or release.
- Prefer contract-oriented tests over prose or implementation-string checks.
- Reduce duplicate validation of the same invariant at multiple layers.
- Make fixture tests smaller, faster, and easier to diagnose.
- Give contributors and agents a clear way to choose the smallest valid verification scope.

## Non-goals

- Reducing required proof for non-trivial changes.
- Removing full-repo CI, release checks, generated-output drift checks, or manual adapter smoke.
- Replacing human code review or workflow review.
- Optimizing hosted CI infrastructure before the validation contract is clear.
- Converting every documentation rule into machine enforcement in the first slice.
- Adding heavy dependency-based test selection infrastructure before simpler path-based selection is proven.

## Context

`CONSTITUTION.md` says RigorLoop optimizes for reviewability, traceability, and trustworthy automation over speed-by-default. It also says contributors should run repository-owned validation commands before PR and name the commands actually run.

`docs/workflows.md` already points contributors toward structural checks, generated-output drift checks, adapter validation, release validation, review artifact validation, and artifact lifecycle validation. It also notes that `scripts/ci.sh` can derive validation scope from tracked changes.

The current validation surface is broad:

- skill validators and skill regression fixtures;
- generated skill drift checks;
- adapter distribution fixtures;
- generated adapter drift checks;
- adapter validation;
- release metadata validation;
- change metadata validation;
- artifact lifecycle validation;
- review artifact validation;
- full `scripts/ci.sh` wrapper behavior.

Recent implementation work showed that broad checks are valuable, but running them too early creates avoidable iteration cost. Examples include review artifact closeout changes, adapter command alias changes, and workflow wording changes where a focused contract fixture would catch the issue faster than the whole wrapper.

## Options considered

### Option 1: Keep the current broad-check-first habit

Advantages:

- Simple contributor guidance.
- Low risk of missing cross-surface drift before PR.
- Reuses existing `scripts/ci.sh` behavior without new selection rules.

Disadvantages:

- Slow feedback for small changes.
- Encourages agents to wait on broad validation before fixing obvious local failures.
- Makes contributors treat full CI as the first debugging tool instead of the final confidence layer.

### Option 2: Reduce the number of tests and validators

Advantages:

- Shorter validation time.
- Less fixture maintenance.
- Lower immediate complexity.

Disadvantages:

- Conflicts with the project value of trustworthy automation.
- Increases risk around generated adapters, review gates, release metadata, and lifecycle artifacts.
- Solves runtime cost by weakening proof rather than improving proof order.

### Option 3: Add manual checklists instead of more validation structure

Advantages:

- Lightweight to author.
- Useful for rules that are hard to automate.
- Can improve contributor understanding quickly.

Disadvantages:

- Does not reduce repeated command cost.
- Leaves change-scope selection inconsistent between agents.
- Makes review depend more on human memory and less on repository-owned proof.

### Option 4: Formalize layered validation with change-scoped selection

Advantages:

- Keeps coverage while improving feedback speed.
- Lets structural and contract failures surface before broad smoke.
- Gives agents a defensible proof scope for pre-review work.
- Keeps full CI, release checks, and manual smoke as later confidence gates.
- Encourages tests that prove behavior and contracts rather than brittle implementation text.

Disadvantages:

- Requires a clear mapping from changed surfaces to required checks.
- Needs focused selector tests so the optimization does not silently skip required validation.
- Adds a small amount of workflow and documentation surface area.

## Recommended direction

Choose Option 4.

RigorLoop should formalize a layered validation strategy:

```text
1. Fast structural tests
2. Contract tests
3. Change-scoped integration tests
4. Full-repo smoke
5. Release-only manual smoke
```

The first proof step should be the cheapest check that can catch the likely failure. If a failure can be detected without running the whole repository, it should be detected in a structural or contract test.

The workflow should distinguish two validation categories:

- Targeted proof before review: touched contract validation, directly affected regression tests, changed-root selection tests, skill validation when skills change, generated-output drift checks when canonical generated sources change, and adapter validation when adapter generation changes.
- Broad smoke before handoff: full `scripts/ci.sh`, repo-wide regression sweep, release packaging checks, and cross-adapter or manual smoke when the release contract requires it.

For RigorLoop, the practical direction is a standalone repository-owned change-scope selector that maps changed paths to the smallest valid command set:

```text
python scripts/select-validation.py
```

`scripts/select-validation.py` should be the selection engine. `scripts/ci.sh` should be the wrapper and orchestration layer that calls the selector and executes the selected checks. This gives local development, hosted PR CI, push-to-main CI, and future tooling one testable source of truth for validation routing.

The selector can start simple and path-based. It does not need a full dependency graph in the first version. The strongest principle is:

```text
One selector, many modes.
```

Recommended first-slice categories:

- skills;
- generated adapters;
- review artifacts;
- lifecycle artifacts;
- release metadata;
- workflow specs;
- workflow summaries;
- templates;
- schemas;
- validation, generation, selector, and release scripts.

Concrete first-slice paths should include:

- `skills/**`;
- `dist/adapters/**`;
- `docs/changes/**`;
- `specs/**`;
- `docs/workflows.md`;
- `AGENTS.md` and `CONSTITUTION.md` when touched or declared affected;
- `templates/**`;
- `schemas/**`;
- `scripts/**` for validators, selectors, generation, and release checks.

The first slice should remain repository-governance and artifact-centric. It should not broaden to arbitrary app or runtime code unless this repository later gains such code and the selector contract is extended.

Examples:

- Changes under `skills/` run skill validation, skill regression fixtures, generated skill drift checks, and adapter drift or validation when public adapters are affected.
- Changes under `scripts/adapter_*`, `scripts/build-adapters.py`, or `dist/adapters/` run adapter distribution fixtures, adapter drift checks, and adapter validation.
- Changes under `docs/changes/<change-id>/reviews/`, `review-log.md`, or `review-resolution.md` run review artifact validation for that changed root.
- Changes under lifecycle-managed proposal, spec, test-spec, architecture, ADR, or plan paths run artifact lifecycle validation for the touched paths.
- Changes under release metadata or release notes run release validation for the affected version.

The selector should produce structured selected checks, affected roots, and rationale, not hide decisions. Contributors and agents should be able to see why a command was selected and when broader smoke is still needed.

The selector must not fail open. If any changed path is unclassified, the selector must either return an explicit `unclassified-path` blocking result requiring manual routing or select a repository-defined conservative fallback validation set. It must never return empty targeted proof for unknown changed paths.

`verify` should not require both targeted proof and broad smoke for every non-trivial change. The gate split should be:

- Targeted proof is required for all non-trivial changes before review or review handoff.
- Broad smoke is required before PR or merge for planned initiatives.
- Broad smoke is required before PR or merge for ordinary non-trivial changes only when repository policy, risk, or handoff requirements trigger it.

Manual proof should be represented as durable structured evidence instead of free-form prose only. A manual proof record should include a check ID, result, why the check is manual, performer, evidence location, and date. If a check is intentionally not automatable, the record should say `manual by design`, not merely `not tested`.

Hosted CI should consume the same selector output through `scripts/ci.sh`. Different CI contexts should use different modes, not separate selection logic:

```text
PR mode = targeted + required PR-scope checks
main mode = broader smoke + required main checks
release mode = full release validation
```

`scripts/ci.sh` remains the wrapper for selected validation. It is not synonymous with broad smoke. The wrapper may execute targeted proof, broad-smoke mode, or release validation. Broad-smoke mode is required only when planned, policy, risk, handoff, main, or release context triggers it. The wrapper alone does not imply that broad-smoke validation is required for every PR.

## Expected behavior changes

- Contributors start with targeted proof instead of full `scripts/ci.sh` for every iteration.
- `implement` and `code-review` can cite focused validation that matches the changed surfaces.
- `verify` requires targeted proof for non-trivial changes and broad smoke when the workflow, plan, test spec, risk level, or handoff context calls for it.
- Test specs can name the targeted proof set separately from broad smoke.
- `scripts/ci.sh` remains the validation wrapper; broad-smoke mode is used only when planned, policy, risk, handoff, main, or release context triggers it.
- Planned initiatives record both targeted proof and broad smoke before final handoff.
- Ordinary non-trivial changes record targeted proof and add broad smoke only when triggered by repository policy or risk.
- Manual proof records use stable structured fields instead of unstructured "not tested" notes.
- Hosted CI and local CI use the same selector output through `scripts/ci.sh`, with mode-specific breadth.
- Release-only manual smoke remains reserved for release readiness and adapter behavior that cannot be proven structurally.
- Tests increasingly parse stable fields, IDs, enums, manifest entries, and canonical record formats instead of grepping for prose.
- Duplicate tests for the same invariant are reduced to one normative contract test plus only the alignment checks that add real risk coverage.

## Architecture impact

This change affects repository workflow and validation orchestration. It does not require runtime services, storage, networked infrastructure, or a new generated adapter layout.

Likely touched surfaces in a follow-on implementation:

- `specs/rigorloop-workflow.md` for the validation-layering contract.
- A focused `specs/test-layering-and-change-scoped-validation.md` and matching test spec for selector behavior.
- `docs/workflows.md` for contributor-facing validation guidance.
- `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, and `skills/pr/SKILL.md` if their stage guidance needs to distinguish targeted proof from broad smoke.
- `scripts/select-validation.py` as the standalone selection engine.
- `scripts/ci.sh` as the wrapper that consumes selector output and executes selected checks.
- `.github/workflows/ci.yml` if hosted PR, main, or release CI needs explicit selector modes.
- Fixture tests under `tests/fixtures/` and regression tests under `scripts/` for path-to-command selection.

Generated `.codex/skills/` and public adapter output are affected only if canonical skills change. If they do, generated output should be rebuilt or checked through the existing drift commands.

## Testing and verification strategy

The follow-on spec should turn the proposal into concrete, testable requirements. The test strategy should use small fixtures and behavior-level assertions.

Recommended proof surfaces:

- Structural selector tests for path-to-command mapping.
- Contract tests proving selected commands include the required validator categories for changed surfaces.
- Negative tests proving required checks are not skipped for generated-output, release, review-artifact, lifecycle, and skill changes.
- Mode tests proving PR, main, and release modes use the same selector logic with different breadth.
- Manual-proof validation tests for required structured fields when a check is manual by design.
- Regression fixtures for small changed-path sets rather than large golden repositories.
- Alignment checks proving workflow docs and stage skills describe targeted proof and broad smoke consistently.
- Drift checks for generated skill and adapter output only when canonical generated sources change.
- Full `bash scripts/ci.sh` as broad smoke after targeted proof passes.

Avoid overusing tests that only assert script text contains a phrase. Use those only when the literal phrase is itself the contract. Prefer parsing command selection output or invoking validators against fixtures.

## Rollout and rollback

Rollout should be incremental:

- First, add the contract and contributor-facing guidance.
- Next, add `python scripts/select-validation.py` for the first-slice categories.
- Then update `scripts/ci.sh` to call the selector instead of owning selection logic directly.
- Then update stage skills to request targeted proof before broad smoke.
- Finally, expand selector coverage only when repeated validation waste or missed proof justifies it.

Rollback is straightforward because the change should only affect validation guidance and command selection. If the selector is wrong or too broad, contributors can fall back to existing explicit validation commands and `bash scripts/ci.sh` while the selector rules are repaired.

## Risks and mitigations

- Risk: targeted validation skips a required check.
  Mitigation: keep full CI as broad smoke before handoff and add selector regression fixtures for every supported changed-surface category.

- Risk: the selector becomes another complex system to maintain.
  Mitigation: start with path-based categories and explicit rationale output; avoid dependency graph inference until there is evidence it is needed.

- Risk: contributors treat targeted proof as final proof.
  Mitigation: document targeted proof and broad smoke as separate gates, and keep `verify` responsible for branch-ready claims.

- Risk: docs and skills diverge on validation expectations.
  Mitigation: use one normative spec plus focused alignment checks for the short workflow summary and stage skills.

- Risk: brittle tests move from prose greps to giant golden files.
  Mitigation: prefer small single-purpose fixtures and structured assertions; reserve golden files for stable generated outputs and canonical record formats.

## Open questions

None blocking for proposal review.

Resolved direction for the follow-on spec:

- Add `python scripts/select-validation.py` in the first implementation slice.
- First-slice categories are skills, generated adapters, review artifacts, lifecycle artifacts, release metadata, workflow specs, workflow summaries, templates, schemas, and validation-related scripts.
- Targeted proof is required for all non-trivial changes; broad smoke is required for planned initiatives and for ordinary non-trivial changes when policy, risk, or handoff context triggers it.
- Manual proof is recorded as durable structured evidence with check ID, result, manual rationale, performer, evidence location, and date.
- Hosted CI consumes the same selector output through `scripts/ci.sh`, using separate PR, main, and release modes rather than separate selection logic.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-04-25 | Draft proposal recommends layered validation with change-scoped selection. | It preserves proof while reducing avoidable local iteration cost. | Broad-check-first habit, fewer tests, manual checklists only. |
| 2026-04-25 | Use one standalone selector with local, PR, main, and release modes. | One selector gives a testable source of truth while allowing different validation breadth by context. | Keeping selection only in `scripts/ci.sh`; separate CI-specific selection logic. |
| 2026-04-25 | Keep the first selector slice repository-governance and artifact-centric. | These surfaces change contract meaning, generated output, or required validation routing. | Broadening to arbitrary app/runtime code before the repository has such code. |
| 2026-04-25 | Require targeted proof for all non-trivial work and broad smoke only for planned, risk-triggered, policy-triggered, or handoff-triggered cases. | This keeps proof proportional while preserving final confidence gates. | Requiring full broad smoke for every non-trivial change; treating targeted proof as final proof in all cases. |

## Next artifacts

- `specs/test-layering-and-change-scoped-validation.md`.
- `specs/test-layering-and-change-scoped-validation.test.md`.
- Architecture or ADR only if the selector changes CI boundaries, generated-output ownership, or hosted workflow behavior.
- Execution plan after the spec and test spec settle.

## Follow-on artifacts

- `proposal-review`: approved with no material findings after second review pass.
- `specs/test-layering-and-change-scoped-validation.md`.

## Readiness

Accepted and ready for the follow-on spec. The earlier open questions are resolved into proposal-level decisions and should be made normative in the spec.
