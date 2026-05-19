# Published Skill Design Implement And Code-Review Skill Audit

Change: `2026-05-19-published-skill-design-implement-code-review`

## Scope

Audit target skills:

- `skills/implement/SKILL.md`
- `skills/code-review/SKILL.md`

Out of scope:

- rewriting other skills;
- merging, retiring, renaming, removing, or changing ownership of any skill;
- changing workflow stage order, validator selector semantics, adapter roots, or generated-output trust boundaries.

## Existence Gate

| Skill | Keep? | Why it earns existence |
|---|---|---|
| `implement` | yes | Owns a repeatable, high-risk lifecycle procedure: test/proof-first implementation of one approved milestone, active-plan progress updates, validation evidence, milestone handoff, and no-review/no-PR-readiness claim boundaries. |
| `code-review` | yes | Owns independent implementation review against governing artifacts, actual diff, validation evidence, material finding shape, clean review receipt behavior, review-resolution routing, and milestone-aware next-stage decisions. |

No merge or retire candidate is approved in this slice. If future work proposes merging or retiring either skill, it needs a separate proposal or explicit spec amendment because both skills own distinct lifecycle gates.

## Contract Audit

| Check | `implement` baseline | `code-review` baseline | M3 action |
|---|---|---|---|
| Routing-focused `description` | Present but broad; names strict TDD and prerequisites, but near misses such as bugfix/review-resolution/pr are not explicit. | Present but broad; names implementation review and PR readiness context, but near misses such as plan/spec review, verify, and review-resolution are not explicit. | Tighten descriptions with capability, trigger context, and near-miss boundaries while staying under 1024 characters. |
| `Workflow role` | Missing as a named section. Role is spread across purpose, handoff, and plan update rules. | Missing as a named section. Role is spread across purpose, handoff, and review rules. | Add explicit lifecycle role, received input, produced output/status, and forbidden downstream claims. |
| Body execution guidance | Strong but long. Contains TDD loop, first-pass completeness, validation layering, milestone handoff, plan updates, and stop conditions. | Strong but long. Contains independent-review mode, checklist coverage, material findings, recording, and workflow handoff behavior. | Preserve high-value rules while making body routing boundaries and output expectations easier to locate. |
| Output skeleton | No compact fenced result/handoff skeleton near the common path. | Has detailed expected output near the end but no compact first-pass record skeleton near the common path. | Add or preserve compact fenced output skeletons that do not replace detailed obligations. |
| Resource map | No packaged resources. | No packaged resources. | No resource map required unless resources are added. |
| Self-containment | `Project-local evidence` already blocks requiring RigorLoop internals in customer projects. | Evidence guidance is project/gov-artifact oriented, but less explicit about customer-project mode than `implement`. | Preserve portable project-local behavior and avoid new maintainer-only dependencies. |
| Deterministic validation gap | Existing validators cover description length, optional `when_to_use`, resource maps, root-script dependencies, and readability opt-in. | Same. | M2 should add focused regression evidence only if M1/M3 needs it; no broad semantic scoring. |

## Behavior-Significant Baseline To Preserve

`implement` must preserve:

- approved-slice and test/proof-first implementation;
- active-plan `Current Handoff Summary` first handoff inspection;
- first-pass acceptable result completeness set;
- plan progress, decisions, discoveries, aligned-surface audit, and validation notes updates;
- milestone transition from `planned` to `implementing` to `review-requested`;
- no claims of review passed, branch-ready, PR-ready, final closeout readiness, or generated-output currency without evidence;
- stop conditions for missing scope, contradictory artifacts, failing validation, or real owner decisions.

`code-review` must preserve:

- independent-review mode grounded in actual diff, governing artifacts, tests, and validation evidence;
- first-pass review status taxonomy;
- material finding completeness: evidence, required outcome, safe resolution or `needs-decision`;
- clean review receipt recording and no empty review-resolution for clean reviews;
- detailed review record and review-resolution requirements for material findings;
- direct proof requirement for named edge cases;
- milestone-aware routing to next implementation milestone or final closeout only when all implementation milestones are closed;
- no claims of verification, CI, branch-ready, or PR-ready unless owned evidence exists.

## Baseline Token Estimates

Command: `python scripts/measure-skill-tokens.py --skills-root skills`

| Skill | Baseline estimated tokens | Notes |
|---|---:|---|
| `implement` | 4421 | High-token skill with dense implementation loop and handoff guidance. |
| `code-review` | 5054 | Highest-token review skill in this slice because it includes material finding recording and checklist rules. |

M3 should target no material regression. Any increase above `+5%` needs rationale, and any increase above `+10%` blocks the rewrite unless the spec changes.
