# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | https://github.com/xiongxianfei/rigorloop/pull/130 |
| PR state | open |
| Base branch | main |
| Head branch | release/activate-boundary-first-v0.3.7 |

## Title

feat: make boundary-first guidance automatic for v0.4.0

## Summary

- Make a concise boundary scan automatic in the governed spec, inspection, implementation, review, and verification skills without requiring users to name the method.
- Replace the unpublished custom activation publisher with a checked-revision activation record and the existing routine release workflow.
- Prepare coherent `v0.4.0` Codex, Claude, opencode, and npm release inputs while preserving immutable `v0.3.6` rollback metadata.
- Close the selector, lifecycle-marker, release-profile, and historical-fixture gaps exposed by the complete PR gate.

## Tests and verification

- [x] `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` — all 21 selected local checks passed.
- [x] Required `broad_smoke.repo` — passed in 493.92 seconds.
- [x] Boundary regression — 65 tests passed.
- [x] Review/lifecycle/change-metadata validation — 36 reviews and 35 findings validated with zero open findings.
- [x] CLI and npm publication tests — passed.
- [ ] Hosted CI — pending after PR creation.

## Review resolution summary

- Accepted: 35
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Open findings: 0
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`

## Reviewer notes

- Review the compact default behavior and stage-owned progressive expansion first.
- Review lifecycle authority parsing and reciprocal owner/status marker placement for fail-closed behavior.
- Review the checked-revision activation and routine release authority split.
- The branch intentionally preserves the superseded unpublished activation history before the accepted replacement; it is 190 commits ahead of `main` with the exact `origin/main` merge base.

## External handoff

This PR does not tag, publish, merge, or claim public availability.
After approval and merge, an authorized maintainer may separately tag the exact reviewed commit, run trusted GitHub/npm publication, execute fresh public smoke, and record public closeout.
