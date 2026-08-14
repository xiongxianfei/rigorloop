# Code Review M2 R1: Proposal Package Simplification

Review ID: code-review-M2-r1

Stage: code-review

Round: r1

Reviewer: Codex independent code-review context

Target: implementation milestone M2 diff `fc7ec210..b08bea8b`

Reviewed milestone: M2

Reviewed artifact: commit `b08bea8b`

Reviewed revision: `b08bea8b`

Review date: 2026-08-14

Recording status: recorded

Status: changes-requested

Review status: changes-requested

Material findings: PRSIM-M2-CR1

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, review resolution, and workflow review state
- Open blockers: none; the finding is mechanically correctable within M2
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PRSIM-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-14-proposal-skill-simplification/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-14-proposal-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-14-proposal-skill-simplification/review-resolution.md#code-review-M2-r1`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: PRSIM-M2-CR1
- Verify readiness: not-claimed

## Actual diff summary

M2 adds two conditionally mapped proposal references, expands the existing skeleton to four independently applicable groups, shortens the universal skill, allows the approved packaged resources, migrates directly coupled assertions, and adds six focused tests. Contract and package validators pass.

## Finding PRSIM-M2-CR1

Finding ID: PRSIM-M2-CR1

Severity: major

Location: `skills/proposal/SKILL.md`, both new references, and `evidence/m2-package-implementation.md`

Evidence: The baseline for every pre-refactor assembly is 2,122 words and 14,796 bytes. The current `PA1G-governed-gated` procedural assembly is 2,062 words but 15,913 bytes. M2 evidence says every real assembly is smaller while reporting only words, so R47 is not satisfied and the evidence overstates acceptance.

Required outcome: Reduce the combined `SKILL.md` plus governed and strategic reference assembly below both baseline metrics without removing any rule, exact contract literal, failure case, or owner boundary, then correct the evidence to report both metrics.

Safe resolution path: Tighten repeated wording only in the three procedural owners, preserve the skeleton and validators, rerun CMD2-CMD4, remeasure all profiles, update M2 evidence, and return M2 for context-reset rereview.

needs-decision rationale: none

auto_fix_class: mechanical

auto_fix_kind: semantic-preserving-prose-compression

deterministic_authority: R47 and the approved plan require both portable primary metrics to decrease for every real loaded assembly.

affected_paths: `skills/proposal/SKILL.md`, `skills/proposal/references/governed-proposal-authoring.md`, `skills/proposal/references/strategic-and-scope-gates.md`, and `evidence/m2-package-implementation.md`

required_validation: CMD2, CMD3, CMD4, exact profile byte/word recomputation, and `git diff --check`

## Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | R1-R46 and R48-R49 are represented, but R47 byte reduction fails for PA1G. |
| Test coverage | pass | Six focused and 342 broad tests pass. |
| Edge cases | pass | Candidate authority, operations, retry, reset, predicates, group composition, and missing resources are covered. |
| Error handling | pass | Governed and resource failures stop without portable fallback or reconstruction. |
| Architecture boundaries | pass | Existing package and stage ownership remain unchanged. |
| Compatibility | pass | Exact literals remain and directly coupled consumers migrated atomically. |
| Security/privacy | pass | Repository-local static procedure introduces no external access. |
| Derived artifact currency | pass with M3 pending | Generated skill checks pass; full adapter parity belongs to M3. |
| Unrelated changes | pass | The diff is limited to planned package, validator, test, and evidence surfaces. |
| Validation evidence | concern | Commands pass, but M2 evidence omits the failing byte total. |

## Requirement-fidelity receipt

The package implements the approved ownership and behavior model, but acceptance explicitly requires both UTF-8 bytes and words. The combined profile's word reduction cannot substitute for its byte growth.

## Handoff

M2 requires correction and rereview of `PRSIM-M2-CR1`. This review does not claim M2 closure, M3 parity, final review, verification, branch readiness, or PR readiness.
