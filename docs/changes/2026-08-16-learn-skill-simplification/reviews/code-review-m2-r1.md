# Code Review M2 R1: Learn Skill Simplification

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: M2 range `861406c3..9a40379a`
Reviewed milestone: M2
Reviewed artifact: commit `9a40379a`
Review date: 2026-08-17
Status: changes-requested
Material findings: LRNSIM-CR-M2-R1-F1, LRNSIM-CR-M2-R1-F2, LRNSIM-CR-M2-R1-F3
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, its invocation manifest, `review-log.md`, and `review-resolution.md`
- Open blockers: three accepted M2 findings
- Next stage: implement automated correction
- Review status: changes-requested
- Material findings: LRNSIM-CR-M2-R1-F1, LRNSIM-CR-M2-R1-F2, LRNSIM-CR-M2-R1-F3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-16-learn-skill-simplification/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-16-learn-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-learn-skill-simplification/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: open
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: LRNSIM-CR-M2-R1-F1, LRNSIM-CR-M2-R1-F2, LRNSIM-CR-M2-R1-F3
- Verify readiness: not-claimed

## Blind-first risk map

The split could weaken operation selection, first-write durability, evidence distinctions, topic conflict handling, route-row identity, completion-kind immutability, or result-write authority while still satisfying phrase-presence tests. The review compared the implementation directly with R1-R47 and the M2 test cases before using prior review conclusions.

## Findings

## Finding LRNSIM-CR-M2-R1-F1

Finding ID: LRNSIM-CR-M2-R1-F1
Severity: major
Location: `skills/learn/SKILL.md`, operations and resource loading
Evidence: R8 permits `record-learn-route-result` when an explicit request identifies an exact session, route, and owner result, but the skill says every explicit direct `$learn` invocation selects `run-learn-session`. R6 also requires resource failure to stop before session creation, while the shortened wording says only to stop dependent work.
Required outcome: Express the exact R8 exception and the R6 pre-creation stop without weakening unknown-operation failure.
Safe resolution path: Replace the two sentences and add direct assertions for the exception and pre-creation boundary.
needs-decision rationale: none
auto_fix_class: declared-safe
allowed paths: `skills/learn/SKILL.md`, `scripts/test-skill-validator.py`
forbidden paths: lifecycle state outside workflow-owned routing and unrelated skills
required validation: CMD2-CMD4 and `git diff --check`

## Finding LRNSIM-CR-M2-R1-F2

Finding ID: LRNSIM-CR-M2-R1-F2
Severity: major
Location: `skills/learn/references/session-method.md`, preparation, Frame, Observe, and topic effects
Evidence: R14 requires session identity, trigger, scope, evidence basis, and complete Frame in the first write. R19 requires recorded evidence, bounded inference, unknowns, and sensitive/excluded evidence to remain distinct. R24 requires identical topic effects to be idempotent and conflicting or ambiguous content to stop. The reference does not state all of these conditions.
Required outcome: Make first-write contents, evidence distinctions, and exact topic-effect retry/conflict behavior explicit.
Safe resolution path: Tighten the relevant reference paragraphs and add focused assertions.
needs-decision rationale: none
auto_fix_class: declared-safe
allowed paths: `skills/learn/references/session-method.md`, `scripts/test-skill-validator.py`
forbidden paths: persistence models, lifecycle state outside workflow-owned routing, and unrelated skills
required validation: CMD3-CMD4 and `git diff --check`

## Finding LRNSIM-CR-M2-R1-F3

Finding ID: LRNSIM-CR-M2-R1-F3
Severity: major
Location: `skills/learn/references/session-method.md` route construction and `skills/learn/SKILL.md` route-result recording
Evidence: R26 requires source observation, requested action, destination, owner, basis, immutable required completion kind, settlement, optional result, and optional blocker. R26a fixes the completion kind at route creation, and R34 requires result-kind matching. The reference omits several fields and immutability; the result operation can be read as selecting a completion kind at settlement rather than validating the fixed one.
Required outcome: List the complete route schema, fix completion kind during route creation, and require exact kind matching before the only permitted backlink write.
Safe resolution path: Amend the root/reference and strengthen focused tests for every field and kind mismatch.
needs-decision rationale: none
auto_fix_class: declared-safe
allowed paths: `skills/learn/SKILL.md`, `skills/learn/references/session-method.md`, `scripts/test-skill-validator.py`
forbidden paths: route services, polling, destination artifacts, and lifecycle state outside workflow-owned routing
required validation: CMD2-CMD4 and `git diff --check`

## Validation evidence

The focused and broad tests passed before review, demonstrating that the current assertions were insufficient to catch these contract gaps. This is a semantic contract failure, not a command failure.

## Automated correction classification

All three findings are `declared-safe`: each has one exact resolution in the approved spec, touches only M2-owned files and tests, and requires no new architecture, scope, dependency, or user decision.

## Claim limitations

This review does not close M2 or claim package parity, final verification, branch, CI, or PR readiness.
