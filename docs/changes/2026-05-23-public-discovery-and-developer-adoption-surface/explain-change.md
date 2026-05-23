# Explain Change: Public Discovery and Developer Adoption Surface

## Summary

This change improves RigorLoop's public discovery and first-contact adoption
surface without changing runtime behavior. It updates the GitHub repository
metadata, root README, npm package metadata, package README, and durable
change-local proof artifacts so a first-time visitor can quickly understand
what RigorLoop is, how to try it, where to inspect proof, and how to contribute
or report feedback.

The core implementation is documentation, metadata, and evidence only:

- live GitHub description/topics/blank website decision;
- README first-contact command, link group, Quick Start refresh, and Mermaid
  lifecycle visual;
- npm package description, keywords, and package README version alignment;
- durable proof artifacts for external metadata, version source, README
  ownership, cold-read/link checks, unsupported-claim checks, and behavior
  preservation;
- lifecycle state synchronized through M5 and clean code-review.

## Problem

The accepted proposal identified a mismatch between RigorLoop's internal rigor
and its external discovery surface. The repository already had workflow
artifacts, specs, skills, validation scripts, release assets, contribution
files, and an npm-delivered CLI, but a new visitor could still fail to answer
the basic adoption questions quickly:

- What is this?
- Who is it for?
- Why should I try it?
- How do I start?
- What proof exists that it works?
- How do I contribute or report feedback?

The proposal framed this as a public-surface and developer-experience problem,
not as a runtime, skill, adapter, validator, or release-mechanics problem. The
implementation keeps that boundary.

## Decision Trail

| Source | Decision | Impact |
| --- | --- | --- |
| Proposal | Choose metadata plus landing-page README pass, not a full launch campaign. | Scope stayed on repository metadata, README, npm landing, visuals, links, and proof. |
| Proposal review | Add durable proof for external GitHub metadata, version sync, README ownership, and cold-read/link checks. | Added change-local proof artifacts instead of relying on chat or a PR diff. |
| Spec `DXA-R1` through `DXA-R3` | Set approved GitHub description/topics and leave website blank unless a stable landing page exists. | Live metadata was updated and recorded in `repository-metadata-proof.md`. |
| Spec `DXA-R4` through `DXA-R9` | Preserve README positioning, Quick Start, Mermaid visual, required links, and generated-region boundaries. | README was updated outside generated regions and ownership proof was recorded. |
| Spec `DXA-R10` through `DXA-R13` | Align npm package metadata and package README with current stable release and source-of-truth boundaries. | Package description/keywords and package README examples now align with `0.2.0`. |
| Spec `DXA-R14` through `DXA-R18` | Record cold-read, behavior-preservation, no-runtime-change, and link evidence. | Added durable review artifacts and validation notes. |
| Plan review `DXA-PLAN1` | Isolate live GitHub metadata mutation in separate M4 permission-gated milestone. | M1 recorded baseline proof; M4 performed the external mutation after permission was confirmed. |
| Plan milestones | Implement M1 proof, M2 README, M3 npm landing, M4 metadata mutation, M5 lifecycle evidence. | Work stayed reviewable and each slice had validation and code-review. |
| Architecture decision | No architecture artifact required. | The change touches public docs, metadata, and proof surfaces only; no runtime data flow or long-lived design boundary changed. |

## Diff Rationale By Area

| File or surface | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| GitHub repository settings | Set approved description, approved 18 topics, and blank website field. | Make the repo discoverable and reviewable as external state. | `DXA-R1` through `DXA-R3`, M4 | `repository-metadata-proof.md`; `gh repo view ...` |
| `README.md` | Added first command, near-top adoption links, Mermaid lifecycle diagram, current Quick Start commands, and contribution/security routing. | Make the repository understandable within the first few seconds while preserving value-first ordering. | `DXA-R4` through `DXA-R9`, M2 | `readme-ownership-proof.md`; `adoption-surface-review.md`; README validation |
| `packages/rigorloop/package.json` | Updated description and added 18 keywords. | Align npm package metadata with approved repository positioning and topic set. | `DXA-R10`, `DXA-R10a`, M3 | package metadata check; package tests |
| `packages/rigorloop/README.md` | Updated current-use examples and archive names to `0.2.0`; preserved npm delivery-channel boundary. | Remove stale public CLI examples and avoid making npm the canonical workflow source. | `DXA-R10` through `DXA-R13`, M3 | stale-version sweep; unsupported-claim sweep |
| `repository-metadata-proof.md` | Recorded approved targets, before-state, permission status, mutation command, after-state, and acceptance status. | GitHub metadata is not tracked in Git, so review needs durable evidence. | `DXA-R12`, `DXA-T001`, `DXA-T008` | live metadata command output |
| `version-sync-proof.md` | Recorded GitHub release and npm package version sources and stale-version sweep. | Pinned examples need a deterministic current-stable source. | `DXA-R6`, `DXA-R13`, `DXA-T002` | `gh release view`; `npm view`; `rg` sweep |
| `readme-ownership-proof.md` | Recorded generated vision block boundaries and contradiction checks. | Prevent hand-editing generated README content or conflicting with `VISION.md`. | `DXA-R9`, `DXA-R14`, `DXA-T003` | `python scripts/validate-readme.py README.md --vision-markers` |
| `adoption-surface-review.md` | Recorded cold-read, links, commands, stale-version, visual, and unsupported-claim checks. | Subjective first-contact quality needs explicit evidence. | `DXA-R15`, `DXA-R18`, `DXA-T005` | manual link/cold-read evidence plus scans |
| `behavior-preservation.md` | Recorded no-runtime-change matrix across README, npm, metadata, CLI, adapters, skills, validators, release, and workflow surfaces. | Prove adoption-surface work did not silently change product behavior. | `DXA-R16`, `DXA-R17`, `DXA-T007` | package tests; no unexpected runtime-surface diff |
| `docs/proposals/...`, `specs/...`, `docs/plans/...`, `docs/plan.md`, `review-log.md`, `review-resolution.md`, review records, `change.yaml` | Recorded lifecycle state, review results, validation, and accepted plan-review finding closeout. | Preserve the trace from proposal through implementation review. | Constitution workflow rules, active plan | review artifact validators; lifecycle validation |

## Tests Added Or Changed

No product test files were added because the implementation did not add runtime
behavior. The test coverage for this change is proof-based and validation-based,
as approved in the test spec:

- `DXA-T001`: repository metadata baseline proof.
- `DXA-T002`: version source and stale pinned-version proof.
- `DXA-T003`: README ownership, ordering, and first-contact contract.
- `DXA-T004`: README Mermaid lifecycle visual and required link presence.
- `DXA-T005`: cold-read, link-check, command-check, and unsupported-claim review.
- `DXA-T006`: npm package landing alignment.
- `DXA-T007`: behavior preservation and runtime-surface diff proof.
- `DXA-T008`: live repository metadata after-state proof.
- `DXA-T009`: lifecycle closeout validation.

The package test suite was rerun because package metadata and package README
surfaces changed.

## Validation Evidence Available Before Final Verify

Validation evidence is recorded in the active plan and `change.yaml`. The
available evidence includes:

- `gh repo view xiongxianfei/rigorloop --json description,homepageUrl,repositoryTopics`
- `gh release view --repo xiongxianfei/rigorloop --json tagName,isDraft,isPrerelease,publishedAt,url`
- `npm view @xiongxianfei/rigorloop version`
- `python scripts/validate-readme.py README.md --vision-markers`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `npm test --prefix packages/rigorloop` with 107 passing tests
- `python scripts/test-select-validation.py` with 97 passing checks
- stale-version sweeps showing no current README/package `@0.1.5` examples
- unsupported-claim sweeps for hosted-platform, autonomous-merge, fake status,
  replacement, and unsupported source-of-truth claims
- no-unexpected-runtime-surface diff checks
- `git diff --check --`

Hosted CI and final `verify` have not been claimed here.

## Review Resolution Summary

One material finding was recorded during planning:

- `DXA-PLAN1`: accepted and closed. The plan was revised to separate baseline
  tracked proof from permission-sensitive live GitHub metadata mutation.

`review-resolution.md` has `Closeout status: closed`, no open findings, and no
remaining `needs-decision` disposition. Subsequent proposal/spec/plan/code
reviews for this change recorded no material findings. M1 through M5 are closed
after clean code-review.

## Alternatives Rejected

- Metadata-only update: rejected because discoverability would improve but
  first-contact README comprehension and Quick Start drift would remain.
- README-only rewrite: rejected because GitHub search/discovery metadata would
  remain blank.
- Full launch campaign: rejected for this slice because off-platform promotion
  should not send traffic to an unfinished landing page.
- PNG diagram or CLI GIF as first visual: deferred in favor of Mermaid because
  Mermaid is diffable, low-maintenance, and easier to review.
- Website field placeholder: rejected because no stable approved docs landing
  page was identified for this first slice.
- Runtime, skill, adapter, validator, release, or workflow behavior changes:
  rejected as out of scope.

## Scope Control

The implementation preserved the proposal and spec non-goals:

- no CLI behavior changes;
- no skill behavior changes;
- no adapter behavior changes;
- no validator behavior changes;
- no release archive or release automation changes;
- no workflow semantic changes;
- no hosted control-plane, autonomous-merge, fake adoption, or broad maturity
  claims;
- no off-platform promotion.

The README remains a landing surface and links to deeper governing documents
instead of replacing them.

## Risks And Follow-Ups

Remaining risks:

- Final `verify` has not run yet and may still find stale lifecycle state or
  validation gaps.
- Hosted CI has not been observed from this local stage.
- Future releases can make pinned version examples stale again unless release
  updates include a version-sync check.
- Off-platform promotion remains intentionally deferred until final verification
  and PR readiness are handled.

Follow-up candidates from the proposal remain out of scope for this slice:

- Dev.to, Hacker News, Reddit, or other launch posts;
- a docs landing page or GitHub Pages site;
- automated README/npx demo GIF generation;
- adoption metrics or repository traffic review.

## Current Readiness

The active plan now has all implementation milestones closed after code-review.
This explain-change artifact is the durable rationale for the change and hands
off to `verify`.

This artifact does not claim final verification, PR readiness, branch readiness,
hosted CI success, or Done.
