# Published Skill Design Plan Family Behavior Preservation

Change: `2026-05-19-published-skill-design-plan-family`
Milestone: M1 scaffold
Date: 2026-05-19
Scope: `skills/plan/SKILL.md`, `skills/plan-review/SKILL.md`

## Purpose

Record behavior-significant wording that must be preserved when M3 rewrites the
plan-family skill bodies. M1 records the preservation targets; M3 must update
this file with final "preserved where" citations after edits.

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

## M1 conclusion

The M3 rewrite may reorganize or compact wording, but it must not weaken the
rules above. M3 must replace this scaffold with final preservation evidence
showing where each essential rule is preserved.
