# Code Review M3 R1: Discovery Adapter and Candidate Parity

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M3 implementation commit db9ff546
Reviewed artifact: M3 implementation b7d89f0d..db9ff546
Reviewed milestone: M3
Review date: 2026-09-03
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/reviews/code-review-m3-r1.md`; `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-log.md`; `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-resolution.md`
- Open blockers: none
- Next stage: final holistic code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-log.md`
- Review resolution: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: closed
- Remaining implementation milestones: none after workflow closeout
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Scope and authority

R1 independently inspected the committed M3 diff against ER-R1, ER-R3, ER-R27 through ER-R38, TG-11 through TG-14, the approved design package, and Delivery Review `delivery-review-r1`. Review covered generated candidates and metadata evidence; it did not publish, install into a user project, or edit canonical discovery behavior.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Separate Explore and Research packages, complete mapped resources, standalone paths, and authority semantics survive all three adapters. |
| Test coverage | pass | The new test inspects exact archive resources, shared bytes, public text, and clean installs; the existing suite covers missing, stale, malformed, escaped, unknown, and interrupted cases. |
| Edge cases | pass | Unknown selections, stale hashes, extra resources, bad archives, non-installing runners, and mixed packages fail closed. |
| Error handling | pass | Generation and install validation use temporary roots and reject partial or stale candidates before a current claim. |
| Architecture boundaries | pass | Canonical `skills/` remains authored source; archives are temporary output; only current unpublished CLI candidate metadata changed. |
| Compatibility | pass | Skill names remain stable, current v0.5.1 candidate metadata matches generation, and v0.5.0 historical metadata retains its exact hash. |
| Security/privacy | pass | Discovery archive entries exclude maintainer-only paths; mapped resources remain contained within each installed skill root. |
| Derived artifact currency | pass | Candidate archive/tree identities and release-index hash are synchronized and independently exercised by Python and npm tests. |
| Unrelated changes | pass | No archive body or `dist/adapters` package output is tracked; manifest and install README remain unchanged because their generic contract is sufficient. |
| Validation evidence | pass | 157 adapter tests, 8 build-skill tests, 362 skill tests, 25 token-cost tests, 373 npm tests, v0.4.0 generation/clean-install smoke, and 12-check broad smoke pass. |

## No-finding rationale and residual risk

The implementation proves exact canonical-to-archive-to-install parity and repairs the only stale current-candidate identity exposed by the full suite. The fixed v0.4.0 validation version differs from the package's unpublished v0.5.1 candidate identity by approved plan design; both are generated from the same canonical tree and are tested independently. No release was published and hosted download behavior remains outside this milestone.

## Handoff

M3 is clean for workflow closeout. Workflow may complete the final implementation milestone with this exact review evidence and proceed to final holistic Code Review; final verification remains unclaimed.
