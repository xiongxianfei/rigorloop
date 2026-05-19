# Published Skill Design Plan Family Behavior Preservation

Change: `2026-05-19-published-skill-design-plan-family`
Milestone: M3 final
Date: 2026-05-19
Scope: `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md`

## Purpose

Record behavior-significant wording preserved by the M3 plan-family skill-body
rewrite.

## Preservation table

| Skill | Behavior-significant wording or rule | Why it matters | M3 preservation requirement |
|---|---|---|---|
| `plan` | Plan after approved behavior and architecture are stable; do not decide product direction. | Prevents planning from replacing proposal/spec/architecture stages. | Preserve as workflow role, near-miss description language, or stop condition. |
| `plan` | Public skills use project-local artifacts when present and must not require RigorLoop internals in customer projects. | Preserves portability and self-containment. | Preserve project-local evidence guidance without maintainer-only required paths. |
| `plan` | Upstream status settlement is limited to known mappings and must block on missing/contradictory evidence. | Prevents silent lifecycle status guessing. | Preserve the settlement rule and output block or a reviewed equivalent. |
| `plan` | Concrete plan bodies live under `docs/plans/`; `docs/plan.md` is the lifecycle index. | Prevents duplicate plan-body surfaces. | Preserve plan/index ownership and create/replan update rules. |
| `plan` | Normal handoff is `plan-review`; `test-spec` follows only after plan-review when workflow allows it. | Prevents stage skipping. | Preserve immediate handoff and downstream-readiness distinction. |
| `plan` | Do not claim implementation, review, verification, branch-ready, PR-ready, or Done from planning. | Preserves claim boundaries. | Preserve in claims or workflow-role block. |
| `plan` | Readiness is not Done; final closeout requires remaining gates and owning evidence. | Prevents premature completion. | Preserve readiness/Done definitions and completion-gate language. |
| `plan` | Milestone state values are `planned`, `implementing`, `review-requested`, `resolution-needed`, and `closed`. | Keeps active plan state machine stable. | Preserve exact vocabulary. |
| `plan` | Active plan `Current Handoff Summary` owns live state. | Prevents scattered workflow state. | Preserve the summary fields and ownership rule. |
| `plan` | Do not proceed to implementation until `plan-review` and `test-spec` are ready unless explicitly isolated. | Protects proof-before-code sequencing. | Preserve stop condition or planning rule. |
| `plan-review` | Review the concrete plan body, not just `docs/plan.md`. | Prevents reviewing the index as if it were the plan. | Preserve in inputs/rules. |
| `plan-review` | Review dimensions cover self-contained context, source alignment, milestones, sequencing, scope, validation, TDD readiness, risk, architecture, operations, and maintainability. | Defines the formal review scope. | Preserve dimensions or a reviewed equivalent. |
| `plan-review` | Material findings require evidence, required outcome, and safe resolution or `needs-decision`. | Preserves finding quality. | Preserve exact material finding contract. |
| `plan-review` | Every formal lifecycle review must be recorded or explicitly blocked. | Preserves formal review recording. | Preserve recording requirement. |
| `plan-review` | Clean reviews create a lightweight receipt and `review-log.md`, not an empty `review-resolution.md`. | Preserves review artifact shape. | Preserve clean receipt behavior. |
| `plan-review` | Material or blocking outcomes require detailed review record and disposition artifacts. | Preserves downstream resolution workflow. | Preserve detailed-record and review-resolution triggers. |
| `plan-review` | Isolated material reviews still require durable records and state no automatic downstream handoff. | Preserves isolation/recording boundary. | Preserve isolation language and required final output fields. |
| `plan-review` | Do not require implementation code before approving a plan. | Keeps plan review at the planning stage. | Preserve as rule or workflow role claim boundary. |
| `plan-review` | Immediate next stage is `test-spec`; implementation readiness is downstream readiness only. | Prevents stage skipping. | Preserve in expected output and handoff guidance. |

## M3 Preservation Result

| Skill | Essential rule preserved | Preserved where |
|---|---|---|
| `plan` | Stage role after approved behavior/design sources, not product-direction selection. | Frontmatter `description`, `## Workflow role`, opening paragraphs, `## When not to use`, and `## Planning rules`. |
| `plan` | Published skill remains self-contained and does not require unavailable RigorLoop internals. | `## Project-local evidence`, `## Artifact placement`, and validated readability self-containment. |
| `plan` | Upstream status settlement stays evidence-bound and blocks on missing or contradictory evidence. | `## Upstream status settlement`. |
| `plan` | Concrete plan bodies and `docs/plan.md` index ownership remain distinct. | `## Output paths`, `## Outputs`, `## Required sections`, and `## Planning rules`. |
| `plan` | Handoff remains `plan-review`; `test-spec` follows only after review when workflow allows it. | `## Handoff`, `## Output skeleton`, and `## Expected output`. |
| `plan` | Planning must not claim implementation, review, verification, branch readiness, PR readiness, final closeout, or Done. | `## Workflow role`, `## Claims this skill must not make`, and `## Progress, readiness, closeout, and Done`. |
| `plan` | Milestone states and `Current Handoff Summary` ownership stay intact. | `## Milestone-aware plans`. |
| `plan` | Implementation must wait for plan-review and test-spec unless explicitly isolated. | `## Planning rules` and `## Stop conditions`. |
| `plan-review` | Review target is the concrete plan body, not only `docs/plan.md`. | `## Inputs to read` and `## Rules`. |
| `plan-review` | Formal review dimensions remain present. | `## Review dimensions`. |
| `plan-review` | Material findings require evidence, required outcome, and safe resolution or `needs-decision`. | `## Material findings`. |
| `plan-review` | Formal review recording, clean receipt behavior, detailed records, review-resolution triggers, and isolated material-review boundaries remain intact. | `## Isolation and Recording` and `## Output skeleton`. |
| `plan-review` | Plan review must not require implementation code, review code diffs, verify, prepare PRs, or claim downstream completion. | Frontmatter `description`, `## Workflow role`, and `## Rules`. |
| `plan-review` | Immediate next stage remains `test-spec` or plan revision, with implementation readiness kept downstream. | `## Workflow role`, `## Output skeleton`, and `## Expected output`. |

No behavior-significant rule from the M1 preservation table was removed or
weakened. The rewrite adds routing/frontmatter clarity, workflow-role fields,
and compact output skeletons while preserving the underlying lifecycle contract.
