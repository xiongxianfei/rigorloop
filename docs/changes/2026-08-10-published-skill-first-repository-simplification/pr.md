# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | https://github.com/xiongxianfei/rigorloop/pull/131 |
| PR state | open |
| Base branch | main |
| Head branch | proposal/published-skill-first-repository-simplification |

## Result

- Skill: pr
- Status: submitted
- Open blockers: none
- Next stage: none
- Readiness: PR body ready and PR open ready

## Title

refactor: simplify published skill validation

## Summary

- Make canonical skills, packaged resources, generated adapter archives, and
  releases the deterministic product proof chain.
- Consolidate validation under Gate A, Gate B, Gate C, and one separate
  lifecycle-governance entry point.
- Run 26 named product and governance checks directly on PR/main while retaining
  selector, cache, and broad-smoke code only for active compatibility contracts.
- Exclude target-agent execution, prompts, transcripts, model matrices, and LLM
  grading from repository acceptance; installation proof ends at filesystem
  materialization.

## Tests and verification

- [x] Current committed PR range passed all 26 direct local checks.
- [x] Review closeout passed with 20 reviews, nine resolved findings, and no
  open findings.
- [x] Change metadata, lifecycle composition, generated-skill currency, and
  boundary snapshot passed.
- [x] Recorded-source Gate C rebuilt and validated Codex, Claude Code, and
  opencode archives.
- [x] Fixture-safe Gate C wrapper dry-run selected the real command sequence and
  published nothing.
- [x] Final holistic review was clean-with-notes with no material findings.
- [x] Hosted CI run `31385108670` passed the complete direct graph on the clean
  GitHub Python 3.11 runner in 1m43s.

The direct historical `v0.4.0` replay against the current unreleased tree
failed closed as expected because current archives do not match historical
package metadata and that profile retains its historical benchmark requirement.
The approved recorded-source and fixture-safe release checks passed.

## Review resolution summary

- Accepted: 9
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Open findings: 0
- Review resolution:
  `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-resolution.md`

## Risks and rollback

- The direct graph favors transparency over changed-path optimization and takes
  several minutes locally.
- Selector, cache, and broad-smoke compatibility code remains until separate
  contract amendments and retirement proof permit deletion.
- Historical releases require recorded-source proof or a matching candidate;
  mismatched current-tree replay must continue to fail closed.
- Rollback reverts the affected gate milestone or restores the prior PR/main
  dispatch without rewriting canonical skills or historical evidence.

## Reviewer notes

- Review the spec/ADR ownership split, then `scripts/ci.sh` and the retirement
  ledger.
- Confirm equivalent deterministic package proof for Codex, Claude Code, and
  opencode without runtime execution.
- Confirm Gate C composes current product owners and lifecycle governance stays
  separate from semantic review.
- Review the dependency-free retirement-ledger correction at `3dffeca0`: JSON
  is semantically equal to the former YAML object and loads under `python -S`.

## External handoff

This PR does not tag, publish, deploy, merge, execute target runtimes, or claim
model-behavior certification.
