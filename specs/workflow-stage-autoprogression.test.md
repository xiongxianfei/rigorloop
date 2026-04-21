# Workflow stage autoprogression test spec

## Status

- active

## Related spec and plan

- Spec: `specs/workflow-stage-autoprogression.md`
- Related proposal: `docs/proposals/2026-04-21-workflow-stage-autoprogression.md`
- Architecture: `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
- ADR: `docs/adr/ADR-20260419-repository-source-layout.md`
- Plan: `docs/plans/2026-04-21-workflow-stage-autoprogression.md`
- Related workflow and guidance surfaces:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - canonical `skills/`
  - generated `.codex/skills/`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `bash scripts/ci.sh`

## Testing strategy

- Use manual contract review for the normative workflow docs and canonical stage skills because v1 is guidance- and skill-driven rather than backed by a repo-owned workflow router.
- Use generated-output drift checks as the executable proof that canonical `skills/` and `.codex/skills/` remain aligned after each milestone.
- Use repo-owned smoke validation through `bash scripts/ci.sh` to confirm the changed workflow/skill guidance still passes the repository's standard checks.
- Use real repository artifacts rather than synthetic mocks for workflow and skill coverage. The main risk is contract drift across authored surfaces, not algorithmic logic in a new runtime subsystem.
- Treat PR-opening prerequisites, isolated-stage behavior, and stop conditions as contract/manual scenarios asserted through stage-skill wording and readiness guidance until a later approved change adds executable orchestration.
- Treat compatibility and migration coverage as manual plus smoke: confirm stage order and lane definitions remain intact while the new continuation policy lands only in the approved v1 scope.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R1c`, `R2`, `R2a`, `R2b`, `R2ba`, `R10`, `R10a` | `T1`, `T5`, `T9` | manual | Core scope boundary, isolated-stage behavior, and preservation of existing lane/stage structure |
| `R1d`, `R6`, `R6a`, `R6b`, `R6c` | `T4`, `T8` | manual, smoke | Direct-`pr` behavior, readiness blockers, and truthful hosted-CI wording |
| `R2c`, `R2d`, `R2e`, `R2f`, `R2g`, `R7`, `R7a` | `T3` | manual | Authoring-to-review handoffs and explicit non-expansion into review-to-authoring transitions |
| `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `R7`, `R7a` | `T2`, `T8` | manual, smoke | Full-feature execution flow from `implement` through `pr`, including conditional `ci` |
| `R5`, `R5a`, `R8`, `R8a`, `R8b` | `T4`, `T5` | manual | Stop conditions, pause handling, and non-expansion into stronger external actions |
| `R8c`, `R8d`, `R9`, `R9a` | `T6` | manual | Advice-only `learn`, truthful readiness wording, and blocker/pause reporting |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T2` | Full-feature `implement -> code-review` handoff |
| `E2` | `T3` | `spec -> spec-review` in workflow-managed context |
| `E3` | `T5` | Review-only request stops after the requested stage |
| `E4` | `T2` | `code-review <-> review-resolution` loop |
| `E5` | `T4` | PR creation opens directly when readiness passes |
| `E6` | `T4` | PR creation blocks on base/scope problems |
| `E7` | `T5` | Explicit pause overrides continuation |
| `E8` | `T4` | Direct `pr` still opens when ready |
| `E9` | `T5` | Direct `verify` stays isolated by default |
| `E10` | `T9` | Fast-lane and bugfix execution stay outside v1 scope |

## Edge case coverage

- `EC1`: direct `verify` request stays isolated: `T5`
- `EC2`: workflow-managed `spec -> spec-review`: `T3`
- `EC3`: full-feature `implement -> code-review`: `T2`
- `EC4`: fixable `code-review` findings loop through review-resolution: `T2`
- `EC5`: design-choice review findings stop instead of auto-looping: `T5`
- `EC6`: unrelated tracked changes block `pr`: `T4`
- `EC7`: unrelated untracked drafts may remain local but stay out of PR scope: `T4`
- `EC8`: hosted CI may be pending when the PR opens, without false success claims: `T4`
- `EC9`: explicit `stop after code-review` pause is honored: `T5`
- `EC10`: `verify -> ci/explain-change -> pr` in full-feature flow: `T2`
- `EC11`: direct `pr` opens when ready and then stops: `T4`
- `EC12`: directly invoked `verify` without workflow-managed context stops after verify: `T5`
- `EC13`: lifecycle-closeout or upstream-stage blockers prevent PR opening: `T4`
- `EC14`: fast-lane and bugfix execution do not gain v1 autoprogression: `T9`

## Test cases

### T1. Workflow contract surfaces expose the bounded v1 scope

- Covers: `R1`, `R2`, `R2a`, `R2b`, `R2ba`, `R10`, `R10a`
- Level: manual
- Fixture/setup:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
- Steps:
  - Review the approved spec and the updated workflow/governance surfaces.
  - Confirm v1 applies only to full-feature execution from `implement` through `pr` plus `proposal/spec/architecture -> matching review`.
  - Confirm stage order, enforcement model, and lane definitions are preserved.
  - Confirm fast-lane and bugfix execution are explicitly excluded from v1 autoprogression.
- Expected result:
  - The normative and summary workflow surfaces agree on the same bounded v1 scope.
- Failure proves:
  - Contributors could infer a broader or different automation model than the approved spec allows.
- Automation location:
  - Manual review during M1.

### T2. Full-feature execution skills express the required downstream chain

- Covers: `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `R7`, `R7a`, `E1`, `E4`, `EC3`, `EC4`, `EC10`
- Level: manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/ci/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
- Steps:
  - Review the canonical execution-stage skills and shared workflow skill.
  - Confirm the full-feature path is expressed as `implement -> code-review -> verify -> ci when triggered / explain-change otherwise -> pr`.
  - Confirm accepted review findings enter `review-resolution` and rerun `code-review`.
  - Confirm execution stages no longer imply redundant user confirmation between already-known downstream gates.
- Expected result:
  - Full-feature execution skills reflect the exact downstream chain defined by the approved spec.
- Failure proves:
  - The repository would still pause incorrectly or skip required handoffs in the full-feature lane.
- Automation location:
  - Manual review during M2.

### T3. Authoring stages hand off into matching review gates only

- Covers: `R2c`, `R2d`, `R2e`, `R2f`, `R2g`, `R7`, `R7a`, `E2`, `EC2`
- Level: manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - Review authoring and paired review skills.
  - Confirm successful `proposal`, `spec`, and `architecture` hand off into the matching review stage when that review is the next required or default downstream stage.
  - Confirm review-to-next-authoring transitions such as `proposal-review -> spec` remain explicitly out of scope.
- Expected result:
  - Upstream handoffs are automatic only where the approved spec allows them.
- Failure proves:
  - The implementation would either miss required authoring-review transitions or expand v1 past its approved boundary.
- Automation location:
  - Manual review during M3.

### T4. PR-opening behavior uses existing readiness rules and reports blockers clearly

- Covers: `R1d`, `R5`, `R6`, `R6a`, `R6b`, `R6c`, `E5`, `E6`, `E8`, `EC6`, `EC7`, `EC8`, `EC11`, `EC13`
- Level: manual
- Fixture/setup:
  - `skills/pr/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `specs/docs-changes-usage-policy.md`
  - `docs/workflows.md`
  - the active plan and other lifecycle-managed artifacts for readiness wording
- Steps:
  - Review direct-`pr` and workflow-managed `pr` guidance.
  - Confirm `pr` opens directly when readiness passes.
  - Confirm blocker wording covers: unknown base branch, missing review branch, unrelated tracked changes, missing required baseline docs-changes artifacts for ordinary non-trivial work, stale lifecycle closeout, and unavailable network/tooling.
  - Confirm unrelated untracked drafts are excluded from PR scope rather than treated as automatic blockers.
  - Confirm pending hosted CI is described truthfully rather than reported as passed.
- Expected result:
  - `pr` remains a submit/open stage, and readiness blockers including missing required docs-changes artifacts are explicit and reviewable.
- Failure proves:
  - PR opening semantics, docs-changes readiness checks, scope safety, or CI honesty drifted from the approved contract.
- Automation location:
  - Manual review during M2 and M3.

### T5. Isolated requests and stop conditions prevent surprise continuation

- Covers: `R1a`, `R1b`, `R1c`, `R5`, `R5a`, `R8`, `R8a`, `R8b`, `E3`, `E7`, `E9`, `EC1`, `EC5`, `EC9`, `EC12`
- Level: manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `specs/docs-changes-usage-policy.md`
- Steps:
  - Review isolated-stage and stop-condition wording across shared and stage-local skills.
  - Confirm direct `code-review`, `verify`, and `explain-change` remain isolated by default.
  - Confirm direct `verify` still reports a missing required baseline docs-changes pack as a blocker for ordinary non-trivial work instead of treating the omission as acceptable silence.
  - Confirm explicit pause instructions and decision-requiring review findings stop the workflow instead of auto-continuing.
  - Confirm stronger external actions such as merge, release, deploy, and destructive Git remain outside default autoprogression.
- Expected result:
  - The workflow remains safe and unsurprising when the request is isolated or a real blocker such as a missing required docs-changes pack exists.
- Failure proves:
  - The implementation would continue when it should pause or block, or it could hide a required docs-changes blocker during isolated verification.
- Automation location:
  - Manual review during M2 and M3.

### T6. Advice-only `learn` stays non-automatic and readiness wording is truthful

- Covers: `R8c`, `R8d`, `R9`, `R9a`
- Level: manual
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - active plan/readiness text touched during implementation
- Steps:
  - Review `learn` and shared workflow guidance.
  - Confirm `learn` stays advice-only and does not become automatic by implication.
  - Confirm stage outputs/readiness wording are expected to name the actual next stage or the blocker/pause reason.
- Expected result:
  - Advice-only behavior and truthful readiness wording remain explicit after the change.
- Failure proves:
  - Contributors could misread `learn` as automatic or miss why continuation stopped.
- Automation location:
  - Manual review during M2 and M3.

### T7. Generated skill output remains synchronized with canonical skills

- Covers: `R1`-`R10a`
- Level: integration
- Fixture/setup:
  - touched canonical `skills/`
  - generated `.codex/skills/`
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
- Expected result:
  - Canonical skills are valid and generated compatibility output is in sync.
- Failure proves:
  - Skill guidance changed without regenerating or validating the derived distribution surface.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`

### T8. Repository-wide smoke validation still passes after guidance and skill updates

- Covers: `R3`, `R6`, `R7`, `R8`, `R9`, `R10`
- Level: smoke
- Fixture/setup:
  - canonical workflow docs and skills
  - generated `.codex/skills/`
  - repo-owned validation wrapper
- Steps:
  - Run `bash scripts/ci.sh` after the autoprogression guidance and skill changes land.
  - Confirm the wrapper completes successfully without generated-output drift.
- Expected result:
  - The repository's standard smoke validation still passes after the workflow and skill changes.
- Failure proves:
  - The initiative broke the repo-owned validation path or left generated surfaces stale.
- Automation location:
  - `bash scripts/ci.sh`

### T9. Fast-lane and bugfix execution remain unchanged in v1

- Covers: `R2b`, `R10`, `R10a`, `E10`, `EC14`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/bugfix/SKILL.md`
- Steps:
  - Review fast-lane and bugfix guidance after implementation.
  - Confirm neither lane inherits the full-feature autoprogression chain by implication.
  - Confirm bugfix keeps its existing explicit-step blast-radius flow.
- Expected result:
  - Out-of-scope lanes remain behaviorally unchanged in v1.
- Failure proves:
  - The change silently broadened beyond the approved feature boundary.
- Automation location:
  - Manual review during M1 and M3.

## Fixtures and data

- Use the real repository workflow artifacts as the main proof surface:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - canonical `skills/`
  - generated `.codex/skills/`
- Use the current active plan and lifecycle-managed source artifacts as readiness/continuation examples.
- Use local branch/worktree state only for manual PR-readiness scenario review. Do not bake machine-local branch names or unrelated drafts into tracked fixtures.

## Mocking/stubbing policy

- Do not add mocks or stubs for v1 proof. The feature is guidance- and skill-driven, so real repository artifacts are the authoritative test inputs.
- Do not simulate a repo-owned workflow router because the approved architecture explicitly keeps such a router out of scope.
- When manual PR-opening scenarios are reviewed, use documented prerequisite matrices rather than fake network responses.

## Migration or compatibility tests

- Confirm the change preserves stage order and lane definitions while changing only default continuation behavior: `T1`, `T9`.
- Confirm fast-lane and bugfix execution remain unchanged in v1: `T9`.
- Confirm direct `pr` reuses existing readiness rules instead of introducing a second readiness registry: `T4`.
- Confirm generated output remains reproducible from canonical skills: `T7`.

## Observability verification

- Confirm stage outputs are expected to announce automatic continuation and name the next stage: `T2`, `T6`.
- Confirm blocker/pause outputs identify the blocked or paused stage and reason: `T4`, `T5`, `T6`.
- Confirm isolated-stage classification is surfaced when it changes behavior: `T5`.
- Confirm `pr` output distinguishes opened PRs from blockers and pending hosted CI: `T4`.

## Security/privacy verification

- Confirm the change does not authorize merge, release, deploy, or destructive Git actions by default: `T5`.
- Confirm `pr` guidance excludes unrelated tracked changes and keeps unrelated untracked drafts out of scope: `T4`.
- Confirm hosted CI wording remains truthful and does not claim success without an observed hosted run: `T4`.

## Performance checks

- No benchmark suite is required for v1 because the approved architecture adds no long-running subsystem, persistent state, or external service.
- Manual architectural confirmation is sufficient:
  - no new workflow router;
  - no new queue or daemon;
  - no new network dependency beyond the existing `pr` stage behavior.

## Manual QA checklist

- Review the full-feature execution chain in canonical skills and confirm every downstream handoff is present and lane-aware.
- Review direct `pr` wording and confirm it opens when ready instead of drafting-only.
- Review isolated direct `verify`, `code-review`, and `explain-change` requests and confirm they stop after the requested stage unless continuation is explicitly requested.
- Review pause and blocker wording and confirm product/design decision points stop the workflow.
- Review fast-lane and bugfix guidance and confirm no new automatic continuation was introduced.
- Run the generated-skill drift checks and `bash scripts/ci.sh`.

## What not to test

- Do not write end-to-end runtime tests for a workflow router. No repo-owned router exists in v1, and adding one is explicitly out of scope.
- Do not test merge, release, deploy, or destructive Git automation. Those behaviors remain outside the approved feature boundary.
- Do not claim hosted GitHub Actions passed from local-only execution. Hosted CI observation belongs to later verify/PR stages.
- Do not add snapshot-only tests for stage behavior wording; use targeted manual assertions and generated-output drift checks instead.

## Uncovered gaps

- None blocking. The approved spec and architecture are testable as written.
- Intentional limitation: because v1 is guidance- and skill-driven, end-to-end continuation behavior is proved mainly through manual contract review plus repo-owned smoke validation rather than a dedicated runtime test harness.

## Next artifacts

- `implement`
- `code-review`
- `verify`

## Follow-on artifacts

- None yet

## Readiness

- This test spec is active.
- The tracked-source prerequisite is satisfied for the accepted proposal, approved spec, approved architecture, active plan, and this test spec.
- It remains the current proof-planning surface for this initiative until lifecycle closeout moves it to a terminal state.
