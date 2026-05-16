# Plan Review R1 - RigorLoop npm Publication

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Target: docs/plans/2026-05-16-rigorloop-npm-publication.md
Reviewed artifact: docs/plans/2026-05-16-rigorloop-npm-publication.md
Review date: 2026-05-16
Reviewer: Codex plan-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: PR1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/plan-review-r1.md
- Review log: ../review-log.md
- Review resolution: ../review-resolution.md
- Open blockers: PR1-F1
- Immediate next stage: plan revision

## Scope

Reviewed the active execution plan for the first public `@xiongxianfei/rigorloop@0.1.4` npm publication against the approved proposal, spec, architecture package, ADR, and current repository release/package surfaces.

## Reviewed Inputs

- Plan: `docs/plans/2026-05-16-rigorloop-npm-publication.md`
- Proposal: `docs/proposals/2026-05-16-first-public-npm-release.md`
- Spec: `specs/rigorloop-npm-publication.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260516-rigorloop-npm-publication.md`
- Change metadata: `docs/changes/2026-05-16-first-public-npm-release/change.yaml`
- Existing release workflow: `.github/workflows/release.yml`
- Existing release gate: `scripts/release-verify.sh`

## Dimension Review

| Dimension | Result | Notes |
| --- | --- | --- |
| Self-contained context | pass | The plan identifies current package metadata, release workflow state, release gate state, publication evidence path, FU-010 closeout rule, and deferred follow-ups. |
| Source alignment | concern | The plan traces requirements broadly, but the publication/evidence sequencing does not fully operationalize the spec's before-publication versus after-publication evidence boundaries. See PR1-F1. |
| Milestone size | pass | M1 through M5 are reviewable implementation slices. M6 is correctly marked lifecycle-closeout, but needs a clearer merge/tag/evidence boundary. |
| Sequencing | block | The plan does not explicitly separate repository implementation PR/merge from release-tag publication and post-publication evidence closeout. See PR1-F1. |
| Scope discipline | pass | The plan keeps `status`, `validate`, workflow YAML, generated workflow docs, new adapter behavior, and bundled adapter archives out of scope. |
| Validation quality | concern | The command set is strong, but post-publication validation needs a named repository evidence update path after publication. See PR1-F1. |
| TDD readiness | pass | Tests to add or update are identified for package metadata, tarball validation, packed smoke, release verification, publication modes, and evidence shape. |
| Risk coverage | concern | Risks cover duplicate publish paths, version mismatch, bootstrap, bad package versions, and asset ordering, but recovery needs an explicit post-publication evidence PR or equivalent tracked repository update path. |
| Architecture alignment | pass | The plan preserves npm as CLI delivery, GitHub release archives as adapter artifacts, one package/binary, trusted publishing as normal path, and bootstrap as one-time first-publish path. |
| Operational readiness | concern | Release and publication operational checks are identified, but operational handoff between merged release workflow, tag creation, publication, and evidence recording is underdefined. |
| Plan maintainability | pass | Progress, decisions, surprises, validation notes, and milestone state fields are present and updateable. |

## Findings

### PR1-F1 - Publication execution and repository closeout sequencing is underdefined

Finding ID: PR1-F1
Severity: blocking

Location:

- `docs/plans/2026-05-16-rigorloop-npm-publication.md:264`
- `docs/plans/2026-05-16-rigorloop-npm-publication.md:307`
- `docs/plans/2026-05-16-rigorloop-npm-publication.md:315`
- `docs/plans/2026-05-16-rigorloop-npm-publication.md:321`
- `docs/plans/2026-05-16-rigorloop-npm-publication.md:338`
- `specs/rigorloop-npm-publication.md:411`
- `specs/rigorloop-npm-publication.md:438`
- `specs/rigorloop-npm-publication.md:525`
- `specs/rigorloop-npm-publication.md:533`

Evidence:

- M5 is described as "Documentation, Follow-Up State, And Final Local Readiness" and says the expected result is that "the repository is ready for the publication execution gate" while publication evidence may still be pending.
- M6 then depends on M1-M5 being closed and performs publication, records npm evidence, runs post-publication checks, runs real Codex install smoke, and updates `docs/follow-ups.md` to close FU-010.
- M6 closeout also says "explain-change, verify, and PR handoff completed for repository updates."
- The spec requires `docs/releases/v0.1.4/release.yaml` and release notes before publication, but requires publication evidence with npm URL and real install smoke before FU-010 closes. It also requires post-publication `npm view`/npx checks.

Problem:

The plan does not explicitly define the repository-state transition between pre-publication implementation and post-publication evidence. Release workflow/package changes must be merged before a `v0.1.4` tag can safely run, while final publication evidence and FU-010 closeout can only be completed after npm publication and, in many cases, after the GitHub release assets are externally observable. Without a named boundary, implementation could either:

- try to publish from an unmerged branch;
- tag before the release workflow and release evidence surfaces are merged;
- treat pending `npm-publication.md` as closeout evidence;
- or claim PR handoff after external publication without defining how the post-publication evidence and FU-010 update enter the repository.

Required outcome:

Revise the plan to explicitly model the release execution boundary and repository evidence update path.

Safe resolution path:

Update the plan with one of these equivalent structures:

- Split M6 into two lifecycle-closeout milestones:
  - pre-publication PR/merge readiness: all implementation milestones closed, explain-change/verify/PR handoff completed, PR merged, and `v0.1.4` tag creation allowed only after merge;
  - publication/evidence closeout: run selected publication mode, record npm publication evidence, run post-publication checks and real Codex install smoke, then update `docs/releases/v0.1.4/npm-publication.md`, `docs/follow-ups.md`, this plan, and `docs/plan.md` in a follow-up evidence PR or explicitly named tracked commit path.
- Or keep M6 as one lifecycle-closeout milestone but add explicit ordered gates:
  1. implementation PR merged before tag;
  2. release tag created from the merged commit;
  3. publication runs from that tag or bootstrap publishes the exact verified tarball from that commit;
  4. post-publication evidence is committed through a named evidence-update path;
  5. FU-010 closes only after that evidence update passes validation.

The revised plan should name the validation commands for the evidence-update path and state whether that path is a second PR, a release-evidence commit, or another repository-owned mechanism. It should not proceed to test-spec until this boundary is clear.

## Missing Milestones Or Dependencies

One lifecycle boundary is missing: the transition from implementation PR merge to tag publication and then to post-publication repository evidence. No new product milestone is required, but the plan must name this gate before test-spec.

## Suggested Edits

- In `Current Handoff Summary`, distinguish implementation milestones from publication/evidence closeout and state that test-spec follows only after the plan revision is reviewed.
- In M5, make the expected result "implementation PR ready for review/merge before release tag" rather than only "ready for publication execution."
- In M6, name the precondition that the implementation PR has merged before `v0.1.4` is tagged.
- Add an explicit post-publication evidence update path for `docs/releases/v0.1.4/npm-publication.md`, `docs/follow-ups.md`, `docs/plans/2026-05-16-rigorloop-npm-publication.md`, and `docs/plan.md`.
- Add validation commands for that evidence update path, including change metadata, artifact lifecycle, selected CI for evidence paths, and `git diff --check`.

## Immediate Next Stage

Plan revision. Do not proceed to test-spec until PR1-F1 is resolved and plan-review reruns cleanly.

## Isolation

This was an isolated formal plan-review request. There is no automatic downstream handoff.
