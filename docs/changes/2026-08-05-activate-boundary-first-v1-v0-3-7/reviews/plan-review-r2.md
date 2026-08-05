# Plan Review R2

Review ID: plan-review-r2
Stage: plan-review
Round: 2
Reviewer: independent Codex plan-review peer
Target: `docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md`
Target revision: `78d46d6d0284dc689e312712e5b7cd1f2d6c765b`
Status: changes-requested
Material findings: BFA-PLAN-R2-001, BFA-PLAN-R2-002
Immediate next stage: plan revision

## Result

- R1 closure: BFA-PLAN-R1-002 and BFA-PLAN-R1-003 closed; BFA-PLAN-R1-001 and BFA-PLAN-R1-004 remain open.
- Test-spec handoff: blocked pending revision and clean rereview.
- Packet integrity: all five declared hashes matched at review HEAD `5a7b5e52aac4cce9b2e7845b6cebf5a14661ed43`.

## Findings

### BFA-PLAN-R2-001 - B is designated before M3 can close

Finding ID: BFA-PLAN-R2-001
Severity: major
Location: M3; M4 dependencies
Evidence: M3 calls its payload commit B, but required review and resolution evidence is committed after that payload commit; T therefore cannot be both the immediate child of B and start only after M3 closes.
Required outcome: Designate B only after all M3 implementation, review, resolution, and closeout evidence settles, then begin M4 immediately from that exact head.
Safe resolution path: Name the payload commit as a preparation identity; after any review fixes and repeated validation, let workflow designate the final M3 closeout head as B.

### BFA-PLAN-R2-002 - Release-checkpoint commands are not fully executable

Finding ID: BFA-PLAN-R2-002
Severity: major
Location: Lifecycle closeout; Validation plan
Evidence: `python scripts/validate-release.py v0.4.0` exits 2 because `--version` is required; the tagged-tree rule describes variable assignment and cleanup instead of providing executable failure-safe shell.
Required outcome: Provide directly executable release-checkpoint commands whose cleanup runs after every pre-publication failure.
Safe resolution path: Use `python scripts/validate-release.py --version v0.4.0` and a literal shell block with assignments, command substitution, a temporary worktree, and an EXIT trap that conditionally removes the worktree and local tag.

## Review Dimensions

| Dimension | Verdict |
| --- | --- |
| self-contained context | pass |
| source alignment | concern |
| milestone size | pass |
| sequencing | block |
| scope discipline | pass |
| validation quality | block |
| TDD readiness | block |
| risk coverage | pass |
| architecture alignment | concern |
| operational readiness | block |
| plan maintainability | pass |

## Exact Validation Evidence

- Packet hashes and revisions matched.
- Scoped diff check passed.
- Artifact lifecycle validated eight artifacts.
- Change metadata passed.
- Markdown readability passed with nonblocking warnings.
- Explicit validation selection passed with no unclassified paths, blockers, or registration debt.
- Review artifacts passed with eight reviews and ten findings before R2 recording.
- Change-metadata regression passed 61 tests.
- Release-mode validation selection passed.
- `python scripts/validate-release.py v0.4.0` exited 2, confirming the invalid planned command.
