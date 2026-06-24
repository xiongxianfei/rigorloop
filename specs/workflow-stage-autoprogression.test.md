# Workflow stage autoprogression test spec

## Status

- active

## Related spec and plan

- Spec: `specs/workflow-stage-autoprogression.md`
- Related proposal: `docs/proposals/2026-04-21-workflow-stage-autoprogression.md`
- Current proposal-gated authoring autoprogression proposal: `docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
- Current proposal-gated authoring autoprogression plan: `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
- Current proposal-gated authoring autoprogression plan-review: `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/plan-review-r1.md`
- Current proposal-gated authoring autoprogression architecture: `docs/architecture/system/architecture.md`
- Current proposal-gated authoring autoprogression ADR: `docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md`
- Related amendment spec: `specs/milestone-aware-review-handoff.md`
- Related amendment test spec: `specs/milestone-aware-review-handoff.test.md`
- Completed amendment plan: `docs/plans/2026-05-07-milestone-aware-review-handoff.md`
- Current workflow-governance amendment proposal: `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Current workflow-governance amendment plan: `docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md`
- Architecture: `docs/architecture/2026-04-21-workflow-stage-autoprogression.md`
- ADR: `docs/adr/ADR-20260419-repository-source-layout.md`
- Plan: `docs/plans/2026-04-21-workflow-stage-autoprogression.md`
- Related workflow and guidance surfaces:
  - `specs/rigorloop-workflow.md`
  - `specs/code-review-independence-under-autoprogression.test.md`
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
- Use `specs/code-review-independence-under-autoprogression.test.md` as the focused proof surface for first-pass review record contents, first-pass status semantics, clean-review validity, optional positive notes, and sensitive-change coverage. This test spec retains ownership of the broader execution-chain and isolated-stage-default proof.
- Treat PR-opening prerequisites, isolated-stage behavior, and stop conditions as contract/manual scenarios asserted through stage-skill wording and readiness guidance until a later approved change adds executable orchestration.
- Treat compatibility and migration coverage as manual plus smoke: confirm stage order, one standard workflow, and isolated manual skill invocation remain intact while the continuation policy lands only in the approved v1 scope.
- Treat the milestone-aware review handoff amendment as a qualification of final closeout routing: non-final planned implementation milestones route to the next in-scope implementation milestone, while final clean implementation milestones route to final closeout.
- Treat the single-workflow-lane amendment as the current consumer of this proof surface: manual skill invocation remains isolated, while workflow-managed final closeout proceeds through `ci-maintenance` when triggered, `explain-change`, `verify`, and `pr`.
- For the proposal-gated authoring autoprogression first implementation slice, use layered proof tied to the approved plan:
  - M1 uses unit and fixture-backed integration tests for change metadata policy persistence and `authorization-not-persisted` behavior.
  - M2 uses lifecycle/state-sync fixture tests for profile state, gate readiness, architecture assessment routing, stop conditions, transition budget, and idempotent resume.
  - M3 uses skill-validator assertions and manual contract review for stage-skill alignment and review independence.
  - M4 uses generated-skill and adapter validation as integration proof that canonical guidance remains distributable.
  - M5 uses cross-surface fixture and contract checks for default-off behavior, architecture-required and architecture-not-required paths, stop paths, and behavior preservation.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R1b`, `R1c`, `R2`, `R2a`, `R2b`, `R2ba`, `R10`, `R10a` | `T1`, `T5`, `T9` | manual | Core scope boundary, isolated-stage behavior, and preservation of standard workflow structure |
| `R1d`, `R6`, `R6a`, `R6b`, `R6c` | `T4`, `T8` | manual, smoke | Direct-`pr` behavior, readiness blockers, and truthful hosted-CI wording |
| `R2c`, `R2d`, `R2e`, `R2f`, `R2g`, `R7`, `R7a` | `T3` | manual | Authoring-to-review handoffs and explicit non-expansion into review-to-authoring transitions |
| `R2h`-`R2q` | `T11`, `T13`, `T14`, `T15`, `T17` | manual, integration | Closed profile values, user-facing mapping, activation, bounded sequence, completion boundary, and no-test-spec/no-implementation rule |
| `R2r`-`R2t` | `T12`, `T13`, `T17` | unit, integration, manual | Mandatory durable authorization persistence, canonical/fallback policy surfaces, malformed-record handling, and `authorization-not-persisted` |
| `R2u`-`R2w` | `T11`, `T14`, `T17` | integration, manual | Explicit resume requirement and future-profile expansion boundary |
| `R2x`-`R2aa` | `T11`, `T14`, `T15`, `T17` | integration, manual | Architecture assessment outcomes, ambiguity pause, and architecture-required routing |
| `R2ab`-`R2ad` | `T11`, `T15`, `T17` | integration, manual | Separate review invocations, tracked-artifact review target, formal criteria, and recorded review evidence |
| `R2ae`-`R2ah` | `T11`, `T12`, `T14`, `T17` | integration, manual | Stop conditions, stop-result reporting, contradictory state, unreliable partial completion, and safe resumption |
| `R2ai`-`R2aj` | `T11`, `T14`, `T17` | integration, manual | Six-slot transition budget, skipped architecture slots, explicit rereview events, and unexpected-cycle pause |
| `R2ak`-`R2al` | `T16`, `T17` | integration, smoke | Audit trail, generated guidance alignment, and behavior preservation |
| `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `R7`, `R7a` | `T2`, `T8` | manual, smoke | Standard workflow execution flow from `implement` through `pr`, including conditional `ci-maintenance` |
| Milestone-aware review handoff amendment `R1`-`R11b` | `T10` | manual, integration | Qualifies clean `code-review` routing for milestone-based standard workflow plans |
| `R5`, `R5a`, `R8`, `R8a`, `R8b` | `T4`, `T5` | manual | Stop conditions, pause handling, and non-expansion into stronger external actions |
| `R8c`, `R8d`, `R9`, `R9a` | `T6` | manual | Advice-only `learn`, truthful readiness wording, and blocker/pause reporting |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T2` | Standard workflow `implement -> code-review` handoff |
| `E2` | `T3` | `spec -> spec-review` in workflow-managed context |
| `E3` | `T5` | Review-only request stops after the requested stage |
| `E4` | `T2` | `code-review <-> review-resolution` loop |
| `E5` | `T4` | PR creation opens directly when readiness passes |
| `E6` | `T4` | PR creation blocks on base/scope problems |
| `E7` | `T5` | Explicit pause overrides continuation |
| `E8` | `T4` | Direct `pr` still opens when ready |
| `E9` | `T5` | Direct `verify` stays isolated by default |
| `E10` | `T9` | Manual skill and bugfix execution stay outside v1 autoprogression scope |
| `E17`-`E20` | `T11`, `T12` | `authoring-through-plan-review` activation, stop-after-plan-review, direct-review isolation, and architecture ambiguity |
| `E17`-`E20` implementation proof | `T13`-`T17` | Durable authorization, profile routing, stage independence, generated guidance alignment, and integrated behavior-preservation proof |
| Milestone-aware amendment `E1`-`E6` | `T10` | Non-final/final clean review split, same-milestone findings, ambiguous plan state, plan revision, and lifecycle-closeout distinction |

## Edge case coverage

- `EC1`: direct `verify` request stays isolated: `T5`
- `EC2`: workflow-managed `spec -> spec-review`: `T3`
- `EC3`: standard workflow `implement -> code-review`: `T2`
- `EC4`: fixable `code-review` findings loop through review-resolution: `T2`
- `EC5`: design-choice review findings stop instead of auto-looping: `T5`
- `EC6`: unrelated tracked changes block `pr`: `T4`
- `EC7`: unrelated untracked drafts may remain local but stay out of PR scope: `T4`
- `EC8`: hosted CI may be pending when the PR opens, without false success claims: `T4`
- `EC9`: explicit `stop after code-review` pause is honored: `T5`
- `EC10`: `ci-maintenance` when triggered, then `explain-change`, `verify`, and `pr` in standard workflow flow: `T2`
- `EC11`: direct `pr` opens when ready and then stops: `T4`
- `EC12`: directly invoked `verify` without workflow-managed context stops after verify: `T5`
- `EC13`: lifecycle-closeout or upstream-stage blockers prevent PR opening: `T4`
- `EC14`: manual skill and bugfix execution do not gain v1 autoprogression: `T9`
- `EC20`-`EC27`: authoring profile activation, architecture assessment, review stops, direct-review isolation, explicit resume, and completion boundary: `T11`
- `EC28`-`EC31`: durable authorization persistence, pre-pack arming, cancellation persistence, and fallback audit behavior: `T12`
- APGA implementation edge cases:
  - default profile is `off`, unknown profile fails closed, and legacy changes without durable profile policy do not activate: `T13`, `T14`, `T17`
  - proposal gate missing status, review approval, recording evidence, settled scope, or unambiguous placement pauses before `spec`: `T14`, `T17`
  - architecture-required, architecture-not-required, and architecture-ambiguous assessment outcomes are recorded and routed or paused correctly: `T14`, `T17`
  - review stages run independently and record evidence before downstream action: `T15`, `T17`
  - direct reviews remain isolated even when profile policy exists: `T15`, `T16`, `T17`
  - clean `plan-review` completes the profile and reports `test-spec` without invoking it: `T14`, `T15`, `T17`
- Milestone-aware amendment `EC1`-`EC14`: `T10`

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
  - Confirm v1 applies only to standard workflow execution from `implement` through `pr` plus `proposal/spec/architecture -> matching review`.
  - Confirm stage order, enforcement model, one standard workflow, and isolated manual skill invocation are preserved.
  - Confirm manual skill and bugfix execution are explicitly excluded from v1 autoprogression unless the user asks to continue through the standard workflow.
- Expected result:
  - The normative and summary workflow surfaces agree on the same bounded v1 scope.
- Failure proves:
  - Contributors could infer a broader or different automation model than the approved spec allows.
- Automation location:
  - Manual review during M1.

### T2. Standard workflow execution skills express the required downstream chain

- Covers: `R3`, `R3a`, `R3b`, `R3c`, `R3d`, `R3e`, `R3f`, `R7`, `R7a`, `E1`, `E4`, `EC3`, `EC4`, `EC10`
- Level: manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/ci-maintenance/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
- Steps:
  - Review the canonical execution-stage skills and shared workflow skill.
  - Confirm the standard workflow path is expressed as `implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`.
  - Confirm accepted review findings enter `review-resolution` and rerun `code-review`.
  - Confirm execution stages no longer imply redundant user confirmation between already-known downstream gates.
- Expected result:
  - Standard workflow execution skills reflect the exact downstream chain defined by the approved spec.
- Failure proves:
  - The repository would still pause incorrectly or skip required handoffs in the standard workflow.
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
  - Confirm successful `proposal`, `spec`, and `architecture` hand off into the matching review stage when that review is the next mandatory or triggered downstream stage.
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

### T9. Manual skill and bugfix execution remain isolated in v1

- Covers: `R2b`, `R10`, `R10a`, `E10`, `EC14`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/bugfix/SKILL.md`
- Steps:
  - Review manual skill invocation and bugfix guidance after implementation.
  - Confirm neither invocation model inherits the standard workflow autoprogression chain by implication.
  - Confirm bugfix keeps its existing explicit-step blast-radius flow.
- Expected result:
  - Out-of-scope invocation models remain behaviorally unchanged in v1.
- Failure proves:
  - The change silently broadened beyond the approved feature boundary.
- Automation location:
  - Manual review during M1 and M3.

### T10. Milestone-based clean review routing is qualified by amendment

- Covers: milestone-aware review handoff amendment `R1`-`R11b`, amendment `E1`-`E6`, amendment `EC1`-`EC14`
- Level: manual, integration
- Fixture/setup:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/milestone-aware-review-handoff.md`
  - `specs/milestone-aware-review-handoff.test.md`
  - `docs/workflows.md`
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Confirm final closeout routing is qualified for milestone-based plans.
  - Confirm clean non-final implementation milestone reviews close the reviewed milestone and route to the next in-scope implementation milestone.
  - Confirm clean final implementation milestone reviews close the reviewed milestone and route to `ci-maintenance` when triggered; otherwise `explain-change`.
  - Confirm findings, inconclusive review, ambiguous remaining milestones, and user stop conditions do not route to final closeout.
- Expected result:
  - The autoprogression contract no longer implies that a clean review of one non-final milestone makes the whole plan ready for final closeout.
- Failure proves:
  - The original milestone-aware handoff bug remains in the autoprogression proof surface.
- Automation location:
  - `scripts/test-skill-validator.py`
  - `specs/milestone-aware-review-handoff.test.md`

### T11. Authoring-through-plan-review profile follows the bounded stage chain

- Covers: `R2h`-`R2q`, `R2u`-`R2al`, `E17`-`E20`, `EC20`-`EC27`, `APGA-001`-`APGA-030`, `APGA-037`
- Level: manual
- Fixture/setup:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/rigorloop-workflow.md`
  - `docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/proposal-review-r1.md`
  - `skills/workflow/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
- Steps:
  - Confirm the closed profile values are only `off` and `authoring-through-plan-review`, and unknown values fail closed.
  - Confirm `auto-through: plan-review` maps to `autoprogression.profile: authoring-through-plan-review`.
  - Confirm activation requires `armed && gate-ready`, with user authorization separate from proposal-gate readiness.
  - Confirm the active profile sequence is `spec`, `spec-review`, recorded architecture assessment, conditional `architecture`, conditional `architecture-review`, `plan`, `plan-review`, then stop.
  - Confirm `test-spec`, implementation, code-review, explain-change, verify, PR, release, deploy, merge, and review-fix loops are excluded.
  - Confirm architecture assessment records exactly one allowed outcome and ambiguity pauses.
  - Confirm review stages are independent formal review invocations and are recorded before downstream routing.
  - Confirm non-clean reviews, material findings, `needs-decision`, contradictory workflow state, unreliable partial completion, and transition-budget exhaustion pause the profile.
  - Confirm direct review requests remain isolated even when the profile is armed.
  - Confirm clean `plan-review` completes the profile and reports `test-spec` next without invoking it.
- Expected result:
  - The authoring profile is a bounded, explicitly armed workflow-managed continuation path that preserves review independence, architecture routing, stop conditions, idempotent resume, and off-by-default behavior.
- Failure proves:
  - The profile could bypass a gate, start an out-of-scope stage, skip architecture, collapse review independence, or change default behavior when off.
- Automation location:
  - Manual contract review before implementation.

### T12. Profile authorization persistence is mandatory before activation

- Covers: `R2r`, `R2s`, `R2t`, `R2ae`, `R2ag`, `R9a`, `E17`, `EC28`-`EC31`, `APGA-031`-`APGA-036`
- Level: manual
- Fixture/setup:
  - `specs/workflow-stage-autoprogression.md`
  - `specs/rigorloop-workflow.md`
  - `docs/changes/<change-id>/change.yaml`
  - `docs/changes/<change-id>/workflow-policy.yaml`
  - activation audit trail or profile-managed output for the candidate change
- Steps:
  - Confirm activation pauses with stop reason `authorization-not-persisted` when no durable authorization record exists.
  - Confirm activation pauses when the durable authorization record is malformed, partially written, or missing profile name, `authorized_by`, authorization timestamp, or change ID.
  - Confirm activation pauses when the authorization persistence write fails.
  - Confirm pre-pack arming is session intent only and cannot activate the profile until the user re-asserts authorization after change-pack creation and the workflow records it durably.
  - Confirm cancellation changes the profile to `off` only after cancellation is durably recorded; if persistence fails, the prior durable profile state remains and the workflow pauses.
  - Confirm `workflow-policy.yaml` is used only when the change-metadata contract rejects policy data in `change.yaml`.
  - Confirm the fallback decision and fallback path appear in the same audit-trail entry as activation.
  - Confirm profile policy metadata records authorization only and does not own current stage, next stage, review status, branch readiness, or PR readiness.
- Expected result:
  - No profile-driven transition can start from in-memory, implicit, malformed, partially written, missing, or failed authorization evidence.
- Failure proves:
  - The implementation could run the authoring chain without durable user authorization or without enough audit evidence to explain why the stage ran.
- Automation location:
  - Manual contract review before implementation.

### T13. Profile policy metadata validates durable authorization

- Covers: `R2h`-`R2t`, `R2ae`, `R2ag`, `R7ea`-`R7eg`, `R7er`, `E17`, `EC28`-`EC31`, `APGA-001`-`APGA-006`, `APGA-031`-`APGA-036`
- Level: unit, integration
- Fixture/setup:
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `scripts/change_metadata_semantics.py`
  - `scripts/query-change-record.py`
  - `scripts/test-change-metadata-validator.py`
  - `tests/fixtures/change-metadata/`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
- Steps:
  - Add a passing fixture for `workflow.autoprogression.profile: authoring-through-plan-review` with `authorized_by`, authorization timestamp, and matching change ID.
  - Add failing fixtures for unknown profile values, missing profile, missing `authorized_by`, missing timestamp, mismatched change ID, malformed policy shape, and partial records.
  - Add a fixture or semantic assertion that pre-pack arming without durable policy remains session intent only and cannot satisfy activation.
  - Add a fixture or semantic assertion that cancellation cannot be treated as `off` unless the cancellation record persists durably.
  - Add fallback coverage proving `workflow-policy.yaml` is valid only when the change metadata contract rejects policy data and the fallback decision is auditable.
  - Confirm `scripts/query-change-record.py` exposes profile policy as evidence only and does not project live next-stage state.
- Expected result:
  - Valid durable authorization passes; absent, malformed, partial, failed, fallback-invalid, or unknown policy fails closed before activation.
- Failure proves:
  - The profile can activate without durable user authorization or can let policy metadata become a live workflow-state owner.
- Automation location:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`

### T14. Workflow routing enforces gate readiness, architecture assessment, stops, and resume

- Covers: `R2h`-`R2q`, `R2u`-`R2aa`, `R2ae`-`R2aj`, `R7ea`-`R7el`, `R7en`-`R7ep`, `APGA-001`-`APGA-021`, `APGA-025`-`APGA-030`, `APGA-037`
- Level: integration, manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - `scripts/lifecycle_state_sync.py`
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - workflow-state fixtures under `tests/fixtures/artifact-lifecycle/`
  - accepted proposal, review log, review records, and change metadata for this change
- Steps:
  - Add fixture-backed checks that `off` preserves existing behavior and unknown profile values fail closed.
  - Add fixture-backed checks that activation requires `armed && gate-ready && durable authorization persisted`.
  - Add negative gate-readiness fixtures for missing accepted proposal status, missing approved recorded proposal-review, material findings, open blockers, unsettled scope, missing standing gate evidence, ambiguous change ID, and ambiguous artifact placement.
  - Add route fixtures for `architecture-required`, `architecture-not-required`, and `architecture-ambiguous`.
  - Add stop fixtures for non-clean reviews, material findings, open `needs-decision`, user pause/cancellation, contradictory workflow state, unreliable partial completion, and exhausted transition budget.
  - Add resume fixtures proving completed stages are not duplicated, clean reviews are not rerun without a rereview event, and file existence alone does not prove completion.
  - Add assertions that clean `plan-review` completes the profile and reports `test-spec` next without invoking it.
- Expected result:
  - Workflow-managed routing can prove why each profile transition starts, skips, pauses, resumes, completes, or remains off.
- Failure proves:
  - The workflow can skip a gate, duplicate a stage, continue after ambiguity, or begin an out-of-scope downstream stage.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path skills/workflow/SKILL.md --path docs/workflows.md --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md`

### T15. Stage skills preserve independent reviews and direct-review isolation

- Covers: `R2l`-`R2q`, `R2x`-`R2ae`, `R2ak`, `R7eh`-`R7em`, `R7eq`, `APGA-007`-`APGA-018`, `APGA-023`, `APGA-024`
- Level: integration, manual
- Fixture/setup:
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Confirm each affected skill names `authoring-through-plan-review` only as an explicitly armed workflow-managed profile, not as default direct-review behavior.
  - Confirm proposal-review can expose deterministic gate result and immediate next stage without making isolated proposal-review auto-continue.
  - Confirm spec-review either records or routes to recorded architecture assessment before profile-driven downstream action.
  - Confirm review skills require tracked artifact input, governing sources, formal criteria, and recorded results before downstream action.
  - Confirm review skills do not edit the reviewed artifact as part of review.
  - Confirm plan-review completion reports profile completion and `test-spec` next without invoking `test-spec`.
- Expected result:
  - Consecutive authoring/review stages remain distinct, recorded, and independent, and direct review requests remain isolated.
- Failure proves:
  - The profile collapses review independence or treats a direct review request as authorization for workflow-managed continuation.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - manual contract review during M3

### T16. Generated and adapter-facing guidance stays aligned with canonical skills

- Covers: `R2ak`, `R7eq`, `APGA-018`, `APGA-019`, `APGA-029`, `APGA-030`
- Level: integration, smoke
- Fixture/setup:
  - canonical `skills/`
  - `scripts/build-skills.py`
  - `scripts/test-build-skills.py`
  - `scripts/test-adapter-distribution.py`
  - `dist/adapters/README.md`
  - `dist/adapters/manifest.yaml`
  - adapter templates under `scripts/adapter_templates/`
- Steps:
  - Run canonical skill validation after M3 skill edits.
  - Run generated-skill drift checks.
  - Run adapter distribution tests.
  - Confirm adapter support surfaces do not imply broader autoprogression, direct-review auto-continuation, or generated public adapter body edits.
  - Record unaffected-with-rationale when adapter surfaces need no content change.
- Expected result:
  - Generated and adapter-facing guidance remains reproducible from canonical sources and preserves direct-review isolation.
- Failure proves:
  - The public adapter surface can drift from the canonical profile contract or silently broaden workflow behavior.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`

### T17. Integrated APGA behavior-preservation proof covers first-slice boundaries

- Covers: all `authoring-through-plan-review` requirements and `APGA-001`-`APGA-037`
- Level: integration, smoke, manual
- Fixture/setup:
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/behavior-preservation.md`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - review records, review log, review resolution, active plan, and touched specs/skills/scripts/fixtures
- Steps:
  - Prove default-off behavior remains unchanged.
  - Prove an armed clean gate path with `architecture-not-required` runs through `plan-review` and stops with `test-spec` next.
  - Prove an armed clean gate path with `architecture-required` runs architecture and architecture-review before plan.
  - Prove `architecture-ambiguous`, non-clean review status, material finding, open owner decision, missing persistence, direct-review invocation, user pause/cancel, duplicate resume, unreliable partial completion, and transition-budget exhaustion stop the profile.
  - Prove every automatically run review has formal recorded evidence before downstream action.
  - Update behavior-preservation evidence with preserved default behavior, direct-review isolation, fast-lane and bugfix explicit-step behavior, review recording, and no implementation start.
  - Run the selected final validation commands named by the active plan.
- Expected result:
  - The first slice is auditable, preserves existing default behavior, stops at clean `plan-review`, and cannot start `test-spec` or implementation through this profile.
- Failure proves:
  - The implementation violates the proposal's core safety boundary or lacks enough evidence to reconstruct why a stage ran.
- Automation location:
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path specs/workflow-stage-autoprogression.md --path specs/workflow-stage-autoprogression.test.md --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260624-proposal-gated-authoring-autoprogression.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/plan.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path specs/workflow-stage-autoprogression.md --path specs/rigorloop-workflow.md --path skills/workflow/SKILL.md --path docs/workflows.md --path docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md --path docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/change.yaml`

## Fixtures and data

- Use the real repository workflow artifacts as the main proof surface:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - canonical `skills/`
  - generated `.codex/skills/`
- Use the current active plan and lifecycle-managed source artifacts as readiness/continuation examples.
- Use the approved proposal-gated authoring autoprogression plan and plan-review as the milestone-to-test mapping source:
  - `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`
  - `docs/changes/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review/reviews/plan-review-r1.md`
- Use local branch/worktree state only for manual PR-readiness scenario review. Do not bake machine-local branch names or unrelated drafts into tracked fixtures.

## Mocking/stubbing policy

- Do not add mocks or stubs for v1 proof. The feature is guidance- and skill-driven, so real repository artifacts are the authoritative test inputs.
- Do not simulate a repo-owned workflow router because the approved architecture explicitly keeps such a router out of scope.
- When manual PR-opening scenarios are reviewed, use documented prerequisite matrices rather than fake network responses.

## Migration or compatibility tests

- Confirm the change preserves stage order, one standard workflow, and isolated manual skill invocation while changing only default continuation behavior: `T1`, `T9`.
- Confirm manual skill and bugfix execution remain unchanged in v1: `T9`.
- Confirm direct `pr` reuses existing readiness rules instead of introducing a second readiness registry: `T4`.
- Confirm generated output remains reproducible from canonical skills: `T7`.
- Confirm existing v1 autoprogression behavior is preserved when `authoring-through-plan-review` is `off`: `T11`.
- Confirm profile authorization persistence is intentionally tightened from optional/advisory to mandatory durable evidence: `T12`.
- Confirm legacy change records without durable profile policy remain `off` until the user re-asserts authorization and the workflow records it durably: `T13`, `T17`.
- Confirm future profile expansion requires separate proposal and spec amendments rather than widening `authoring-through-plan-review`: `T14`, `T17`.

## Observability verification

- Confirm stage outputs are expected to announce automatic continuation and name the next stage: `T2`, `T6`.
- Confirm blocker/pause outputs identify the blocked or paused stage and reason: `T4`, `T5`, `T6`.
- Confirm authoring profile activation failures report `authorization-not-persisted` when durable authorization is absent, malformed, partial, or cannot be written: `T12`.
- Confirm isolated-stage classification is surfaced when it changes behavior: `T5`.
- Confirm `pr` output distinguishes opened PRs from blockers and pending hosted CI: `T4`.

## Security/privacy verification

- Confirm the change does not authorize merge, release, deploy, or destructive Git actions by default: `T5`.
- Confirm `pr` guidance excludes unrelated tracked changes and keeps unrelated untracked drafts out of scope: `T4`.
- Confirm hosted CI wording remains truthful and does not claim success without an observed hosted run: `T4`.
- Confirm profile authorization metadata excludes secrets and owns no live workflow-state fields: `T12`.
- Confirm profile activation, pause, completion, fallback, and stop results leave reconstructable audit evidence: `T13`, `T14`, `T17`.

## Performance checks

- No benchmark suite is required for v1 because the approved architecture adds no long-running subsystem, persistent state, or external service.
- Manual architectural confirmation is sufficient:
  - no new workflow router;
  - no new queue or daemon;
  - no new network dependency beyond the existing `pr` stage behavior.

## Manual QA checklist

- Review the standard workflow execution chain in canonical skills and confirm every downstream handoff is present and trigger-aware.
- Review direct `pr` wording and confirm it opens when ready instead of drafting-only.
- Review isolated direct `verify`, `code-review`, and `explain-change` requests and confirm they stop after the requested stage unless continuation is explicitly requested.
- Review pause and blocker wording and confirm product/design decision points stop the workflow.
- Review profile authorization persistence wording and confirm missing, malformed, partial, or failed durable records stop before activation with `authorization-not-persisted`.
- Review implementation fixtures for default-off, architecture-required, architecture-not-required, architecture-ambiguous, direct-review isolation, duplicate resume, and transition-budget exhaustion.
- Review manual skill and bugfix guidance and confirm no new automatic continuation was introduced.
- Run the generated-skill drift checks and `bash scripts/ci.sh`.

## What not to test

- Do not write end-to-end runtime tests for a workflow router. No repo-owned router exists in v1, and adding one is explicitly out of scope.
- Do not implement or test automatic review-fix loops, implementation profiles, `authoring-through-test-spec`, PR publication automation, merge, release, deploy, or destructive Git automation as part of this profile.
- Do not test merge, release, deploy, or destructive Git automation. Those behaviors remain outside the approved feature boundary.
- Do not claim hosted GitHub Actions passed from local-only execution. Hosted CI observation belongs to later verify/PR stages.
- Do not add snapshot-only tests for stage behavior wording; use targeted manual assertions and generated-output drift checks instead.

## Uncovered gaps

- None blocking. The approved spec and architecture are testable as written.
- Intentional limitation: because v1 is guidance- and skill-driven, end-to-end continuation behavior is proved mainly through manual contract review plus repo-owned smoke validation rather than a dedicated runtime test harness.
- Implementation may decide the exact fixture shape for persisted profile policy and architecture-assessment records, but it must preserve the approved fields, stop reasons, and ownership boundaries.

## Next artifacts

- `implement M1` under `docs/plans/2026-06-24-proposal-gated-authoring-autoprogression-through-plan-review.md`.
- `code-review M1` after M1 implementation and targeted validation.
- Continue the approved milestone loop with M2 through M5 until all in-scope implementation milestones are closed.
- `explain-change`, `verify`, and `pr` only after all implementation milestones and required review-resolution are closed.

## Follow-on artifacts

- None yet

## Readiness

- This test spec is active.
- The tracked-source prerequisite is satisfied for the accepted proposal, approved specs, approved architecture, accepted ADR, approved active plan, clean plan-review, and this test spec.
- Implementation handoff: M1.
- It remains the autoprogression proof surface for the proposal-gated authoring autoprogression initiative until lifecycle closeout moves the initiative to a terminal state.
