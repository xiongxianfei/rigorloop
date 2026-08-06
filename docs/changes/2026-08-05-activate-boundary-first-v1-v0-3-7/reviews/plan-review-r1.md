# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: independent Codex plan-review peer
Target: `docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md`
Target revision: `c96e5b0066a90af3eb7bd1233c512fa5c8630b4c`
Status: changes-requested
Material findings: BFA-PLAN-R1-001, BFA-PLAN-R1-002, BFA-PLAN-R1-003, BFA-PLAN-R1-004
Immediate next stage: plan revision

## Result

- Skill: plan-review
- Review status: changes-requested
- Recording status: recorded
- Recording blocker: none
- Open blockers: BFA-PLAN-R1-001 through BFA-PLAN-R1-004
- Implementation readiness: not ready
- Test-spec handoff: blocked pending revision and clean rereview

## Findings

### BFA-PLAN-R1-001 - M3 lacks a realizable B to T commit sequence

Finding ID: BFA-PLAN-R1-001
Severity: major
Location: Context and orientation; M3; Decision log
Evidence: M3 requires committed payload baseline B and child transition T but defines only one milestone commit after candidate proof.
Required outcome: Define a committed, proved pre-transition baseline B, then a narrow T commit with exact changed paths and post-T replacement recovery.
Safe resolution path: Split M3 into pre-transition payload preparation and a transition-candidate milestone.

### BFA-PLAN-R1-002 - Candidate proof is conflated with strict tagged-tree proof

Finding ID: BFA-PLAN-R1-002
Severity: major
Location: M3; Lifecycle closeout; Validation plan
Evidence: M3 invokes `release-verify.sh` while tag creation is prohibited, but BFA-R018-R019 require local `v0.4.0 -> T`, strict validation at H, and full release verification from a detached T worktree.
Required outcome: Separate candidate-at-H proof, release-owned local tag plus strict-H proof, and release-owned detached-T full verification; define cleanup on failure.
Safe resolution path: Keep implementation milestones pre-tag and add exact strict/tagged-tree steps to the explicit release checkpoint.

### BFA-PLAN-R1-003 - Boundary ownership omits release and public closeout proof

Finding ID: BFA-PLAN-R1-003
Severity: major
Location: Boundary and interaction ownership; Lifecycle closeout
Evidence: State, environment, recovery, and partial-publication outcomes are assigned only to local implementation milestones.
Required outcome: Distinguish implementation, candidate, strict release, atomic publication, and post-publication closeout proof owners.
Safe resolution path: Extend the ownership table and map INT-002, INT-004, INT-005, and INT-007 across their actual proof phases.

### BFA-PLAN-R1-004 - Broader validation commands are placeholders

Finding ID: BFA-PLAN-R1-004
Severity: minor
Location: M3; Validation plan
Evidence: Commands contain `--path ...`, defer to unnamed test-spec commands, and omit exact detached-T execution.
Required outcome: Provide executable command rules and exact candidate-H, strict-H, detached-T, bare-remote, and closeout commands.
Safe resolution path: Enumerate stable commands and require test-spec to instantiate the changed-path list before M1 begins.

## Review Dimensions

| Dimension | Verdict |
| --- | --- |
| self-contained context | pass |
| source alignment | concern |
| milestone size | block |
| sequencing | block |
| scope discipline | pass |
| validation quality | block |
| TDD readiness | block |
| risk coverage | concern |
| architecture alignment | concern |
| operational readiness | block |
| plan maintainability | concern |

## Exact Validation Evidence

- Scoped `git diff --check` passed.
- Explicit artifact-lifecycle validation passed with eight artifacts.
- Change-metadata validation passed.
- Markdown readability passed with nonblocking warnings.
- Explicit validation selection found no unclassified paths or registration debt.
- `python scripts/test-change-metadata-validator.py` passed 61 tests.
