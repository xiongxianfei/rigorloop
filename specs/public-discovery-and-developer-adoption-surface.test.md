# Public Discovery and Developer Adoption Surface Test Spec

## Status

active

## Related spec and plan

- Spec: `specs/public-discovery-and-developer-adoption-surface.md`
- Plan: `docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md`
- Architecture/ADRs: not applicable; the approved plan records no runtime architecture boundary change.

## Testing strategy

This change is documentation, external repository metadata, package metadata,
and evidence-surface work. The proof strategy therefore combines repository
validators, bounded scans, package smoke tests, and manual evidence records.

- Unit: no new product unit tests are expected unless implementation adds a small helper script for adoption-surface checks.
- Integration: run repository lifecycle/change metadata validators over the touched lifecycle artifacts and proof files.
- End-to-end: run the npm package test suite to preserve CLI behavior when package metadata or package README changes.
- Smoke: run README/package stale-version scans, Mermaid/link-presence scans, package metadata checks, and `git diff --check --`.
- Manual: record external GitHub metadata proof, README ownership proof, cold-read/link review, visual accuracy, unsupported-claim sweep, and behavior-preservation proof.
- Contract: verify every required proof artifact has the fields required by the approved spec and active plan.
- Migration: verify current-use `@0.1.5` pinned examples migrate to the current stable baseline unless explicitly historical.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `DXA-R1`, `DXA-R1a`, `DXA-R1b` | `DXA-T001`, `DXA-T008` | manual | Target and after-state metadata proof verify approved description or owner-approved shorter fallback and reject vague descriptions. |
| `DXA-R2`, `DXA-R2a`, `DXA-R2b` | `DXA-T001`, `DXA-T008` | manual | Metadata proof verifies topic count, topic syntax, approved set or smaller-positioning-preserving set. |
| `DXA-R3`, `DXA-R3a` | `DXA-T001`, `DXA-T008` | manual | Metadata proof records blank website decision or owner-approved stable landing page; temporary destinations are rejected. |
| `DXA-R4`, `DXA-R4a` | `DXA-T003` | contract | README ordering is checked against `specs/readme-user-value-positioning.md`. |
| `DXA-R5` | `DXA-T003`, `DXA-T005` | manual | README review and cold-read evidence verify what, who, why, try, proof, contribution, feedback, and security discovery. |
| `DXA-R6`, `DXA-R6a`, `DXA-R6d` | `DXA-T002`, `DXA-T003`, `DXA-T006` | smoke | Version proof and scans verify `@latest`, `@0.2.0`, and no stale current-use `@0.1.5` examples. |
| `DXA-R6b`, `DXA-R6c` | `DXA-T002` | manual | Version proof records GitHub release source, npm source when available, and owner-decision blocker on disagreement. |
| `DXA-R7`, `DXA-R7a`, `DXA-R7b`, `DXA-R7c` | `DXA-T004`, `DXA-T005` | manual | README scan and visual accuracy review verify Mermaid lifecycle, caption honesty, and no first-slice GIF/video requirement. |
| `DXA-R8`, `DXA-R8a` | `DXA-T004`, `DXA-T005` | manual | Link audit checks required links and active targets. |
| `DXA-R9`, `DXA-R9a`, `DXA-R9b` | `DXA-T003` | contract | README ownership proof verifies generated-region handling and contradiction checks. |
| `DXA-R10`, `DXA-R10a`, `DXA-R10b`, `DXA-R10c`, `DXA-R10d` | `DXA-T006` | smoke | Package metadata/README review verifies npm positioning, keywords when supported, version alignment, and no unsupported CLI claims. |
| `DXA-R11` | `DXA-T005`, `DXA-T006`, `DXA-T007` | manual | Unsupported-claim sweeps cover README, npm-facing copy, and behavior-preservation proof. |
| `DXA-R12`, `DXA-R12a`, `DXA-R12b` | `DXA-T001`, `DXA-T008` | contract | Repository metadata proof shape, before/after evidence, permission context, and secret exclusion are verified. |
| `DXA-R13`, `DXA-R13a` | `DXA-T002`, `DXA-T006` | contract | Version-sync proof verifies release sources, pinned version, stale sweep, and disagreement decision. |
| `DXA-R14`, `DXA-R14a` | `DXA-T003` | contract | README ownership proof verifies generated region inspection and owning-source updates when applicable. |
| `DXA-R15`, `DXA-R15a` | `DXA-T005` | manual | Adoption-surface review records cold-read, links, command checks, unsupported claims, stale versions, and visual accuracy. |
| `DXA-R16`, `DXA-R16a` | `DXA-T007` | contract | Behavior-preservation proof covers all listed surfaces. |
| `DXA-R17` | `DXA-T007`, `DXA-T009` | smoke | Diff review and package tests verify no runtime, skill, adapter, validator, release archive, or workflow semantic changes. |
| `DXA-R18`, `DXA-R18a` | `DXA-T005` | manual | Existing link checker is used if available; otherwise manual link review is recorded. |
| `AC-DXA-001` through `AC-DXA-003` | `DXA-T008` | manual | Metadata acceptance requires live after-state proof or explicit stop without claiming completion. |
| `AC-DXA-004` through `AC-DXA-008` | `DXA-T003`, `DXA-T004`, `DXA-T005` | manual | README first-contact, Quick Start, lifecycle visual, stale version, and required links. |
| `AC-DXA-009`, `AC-DXA-010` | `DXA-T006` | smoke | Package metadata and package README alignment when touched. |
| `AC-DXA-011` through `AC-DXA-015` | `DXA-T001`, `DXA-T002`, `DXA-T003`, `DXA-T005`, `DXA-T007` | contract | Required proof artifacts exist and satisfy their field contracts. |
| `AC-DXA-016`, `AC-DXA-017` | `DXA-T007`, `DXA-T009` | smoke | Unsupported claims and runtime-surface diff boundaries are checked. |
| `AC-DXA-018` | `DXA-T005` | manual | Link validation evidence is recorded. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1: GitHub visitor understands the project quickly | `DXA-T001`, `DXA-T003`, `DXA-T005` | Metadata target, README first-contact review, and cold-read evidence cover this flow. |
| E2: Quick Start stays reproducible | `DXA-T002`, `DXA-T003`, `DXA-T006` | Version proof plus README/package scans verify `@latest`, `@0.2.0`, and no stale current-use `@0.1.5`. |
| E3: release sources disagree | `DXA-T002` | Version-sync proof must block for owner decision when GitHub and npm disagree. |
| E4: generated README ownership is respected | `DXA-T003` | README ownership proof verifies generated-region source updates or direct-edit boundaries. |
| E5: lifecycle visual stays honest | `DXA-T004`, `DXA-T005` | Mermaid scan and visual accuracy review verify caption and manual invocation boundary. |
| E6: external GitHub metadata is reviewable | `DXA-T001`, `DXA-T008` | Repository metadata proof records before/after external state without secrets. |

## Edge case coverage

| Edge case | Covered by | Level | Notes |
| --- | --- | --- | --- |
| EC1: long description truncates poorly | `DXA-T001`, `DXA-T008` | manual | Owner-approved shorter fallback must be recorded before use. |
| EC2: no stable docs landing page | `DXA-T001`, `DXA-T008` | manual | Website remains blank and proof records the blank decision. |
| EC3: package metadata lacks keyword support | `DXA-T006` | manual | Package metadata review records the limitation instead of inventing unsupported format. |
| EC4: stale pinned version is historical | `DXA-T002`, `DXA-T006` | smoke | Stale sweep may allow clearly historical examples only when labeled. |
| EC5: no link checker exists | `DXA-T005` | manual | Manual link review is sufficient when checked targets and results are recorded. |
| EC6: maintainer performs cold-read | `DXA-T005` | manual | Evidence must label reviewer role. |
| EC7: metadata changed through GitHub UI | `DXA-T008` | manual | UI evidence may be summarized without recording session data. |
| EC8: generated vision block answers first-contact questions | `DXA-T003` | contract | README may rely on it only while respecting generated-region ownership. |

## Test cases

### DXA-T001. Repository metadata baseline proof

- Covers: `DXA-R1`, `DXA-R2`, `DXA-R3`, `DXA-R12`, `DXA-R12a`, `DXA-R12b`, `AC-DXA-011`, E6, EC1, EC2
- Level: manual
- Fixture/setup: `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/repository-metadata-proof.md`
- Steps: Record approved target description, topics, website decision, current before-state, evidence source, permission status, owner/action needed, after-state placeholders, and metadata acceptance status.
- Expected result: The proof artifact contains all required fields, records no secrets or session details, and does not claim `AC-DXA-001` through `AC-DXA-003` complete before after-state proof exists.
- Failure proves: External metadata is not reviewable or metadata acceptance can be claimed without durable proof.
- Automation location: manual artifact review plus `gh repo view xiongxianfei/rigorloop --json description,homepageUrl,repositoryTopics` when available.

### DXA-T002. Version source and stale pinned-version proof

- Covers: `DXA-R6`, `DXA-R6a`, `DXA-R6b`, `DXA-R6c`, `DXA-R6d`, `DXA-R13`, `DXA-R13a`, `AC-DXA-005`, `AC-DXA-006`, `AC-DXA-012`, E2, E3, EC4
- Level: smoke
- Fixture/setup: `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/version-sync-proof.md`
- Steps: Record GitHub latest stable release source, npm package version source or unavailability, chosen pinned version, stale-version sweep result, and owner decision if sources disagree.
- Expected result: Current Quick Start and npm landing examples use `@latest` and current pinned `@0.2.0` unless source disagreement blocks for owner decision; current-use `@0.1.5` examples are absent or clearly historical.
- Failure proves: Quick Start freshness is unproven or stale current-use version examples remain.
- Automation location: `gh release view --repo xiongxianfei/rigorloop --json tagName,isLatest`; `npm view @xiongxianfei/rigorloop version`; `rg -n "@xiongxianfei/rigorloop@0\\.1\\.5" README.md packages/rigorloop/README.md packages/rigorloop/package.json docs/ || true`

### DXA-T003. README ownership, ordering, and first-contact contract

- Covers: `DXA-R4`, `DXA-R4a`, `DXA-R5`, `DXA-R6`, `DXA-R8`, `DXA-R9`, `DXA-R9a`, `DXA-R9b`, `DXA-R14`, `DXA-R14a`, `AC-DXA-004`, `AC-DXA-005`, `AC-DXA-008`, `AC-DXA-013`, E1, E4, EC8
- Level: contract
- Fixture/setup: `README.md`, `VISION.md`, `specs/readme-user-value-positioning.md`, `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/readme-ownership-proof.md`
- Steps: Inspect edited README regions, generated markers, section ordering, first-contact answers, Quick Start placement, and contradiction checks against `VISION.md` and source-of-truth sections.
- Expected result: README preserves the approved value-first ordering, generated regions are not hand-edited unless the owning source is updated, and first-contact questions are answered directly or through a near-top link group.
- Failure proves: README adoption copy violates source ownership, approved positioning, or first-contact comprehension requirements.
- Automation location: `python scripts/validate-readme.py README.md --vision-markers`; manual README ordering review against `specs/readme-user-value-positioning.md`

### DXA-T004. README Mermaid lifecycle visual and required link presence

- Covers: `DXA-R7`, `DXA-R7a`, `DXA-R7b`, `DXA-R7c`, `DXA-R8`, `DXA-R8a`, `AC-DXA-007`, `AC-DXA-008`, E5
- Level: smoke
- Fixture/setup: `README.md`
- Steps: Search README for a Mermaid `flowchart LR`, the lifecycle stages from idea to PR, caption text that preserves manual invocation boundaries, and required link targets.
- Expected result: README includes the approved static Mermaid diagram and caption, required link surfaces are visible, and no first-slice GIF/video/screenshot-gallery dependency is introduced.
- Failure proves: The visual is missing, misleading, or maintenance-heavy beyond the approved first slice.
- Automation location: `rg -n "```mermaid|flowchart LR|Idea|Proposal|Spec|Test spec|Plan|Implement|Code review|Explain change|Verify|PR|manual skill" README.md`; `rg -n "docs/workflows.md|docs/changes/0001-skill-validator|CONTRIBUTING.md|SECURITY.md|ISSUE_TEMPLATE" README.md`

### DXA-T005. Cold-read, link-check, command-check, and unsupported-claim review

- Covers: `DXA-R5`, `DXA-R8`, `DXA-R11`, `DXA-R15`, `DXA-R15a`, `DXA-R18`, `DXA-R18a`, `AC-DXA-014`, `AC-DXA-016`, `AC-DXA-018`, E1, E5, EC5, EC6
- Level: manual
- Fixture/setup: `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/adoption-surface-review.md`
- Steps: Record reviewer role, identified first command, one-sentence value proposition, target audience, links checked, Quick Start commands checked, unsupported-claim sweep, stale-version sweep, and visual accuracy result.
- Expected result: A reviewer can identify value, audience, and first command without deep specs; required links resolve to active repository surfaces; unsupported hosted-platform, autonomous-merge, fake adoption, and runtime claims are absent.
- Failure proves: First-contact comprehension or adoption-surface trust is not established.
- Automation location: manual evidence; existing link checker if discovered; otherwise recorded manual link review.

### DXA-T006. npm package landing alignment

- Covers: `DXA-R10`, `DXA-R10a`, `DXA-R10b`, `DXA-R10c`, `DXA-R10d`, `DXA-R11`, `DXA-R13`, `AC-DXA-009`, `AC-DXA-010`, `AC-DXA-016`, E2, EC3, EC4
- Level: smoke
- Fixture/setup: `packages/rigorloop/package.json`, `packages/rigorloop/README.md`
- Steps: Review package description and keywords when touched, compare package README Quick Start with root README and version proof, and scan npm-facing copy for unsupported CLI or source-of-truth claims.
- Expected result: npm package metadata and package README align with repository positioning, current stable version, and npm-as-delivery-channel boundary.
- Failure proves: npm landing copy drifts from approved positioning or claims unsupported behavior.
- Automation location: `node -e "const p=require('./packages/rigorloop/package.json'); if (!p.description) process.exit(1)"`; `npm test --prefix packages/rigorloop`; stale-version `rg` sweep from `DXA-T002`

### DXA-T007. Behavior preservation and runtime-surface diff proof

- Covers: `DXA-R11`, `DXA-R16`, `DXA-R16a`, `DXA-R17`, `AC-DXA-015`, `AC-DXA-016`, `AC-DXA-017`
- Level: smoke
- Fixture/setup: `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/behavior-preservation.md`
- Steps: Record preservation matrix for CLI behavior, adapter behavior, skill behavior, README Quick Start, repository metadata, npm metadata when touched, and contribution routing. Inspect diff for forbidden runtime/workflow surfaces.
- Expected result: Behavior-preservation proof states runtime, skill, adapter, validator, release archive, and workflow semantic behavior are unchanged; package tests pass when package surfaces are touched.
- Failure proves: The documentation/metadata slice silently changed behavior or unsupported behavior claims.
- Automation location: `npm test --prefix packages/rigorloop`; `git diff --name-only -- . ':!README.md' ':!packages/rigorloop/README.md' ':!packages/rigorloop/package.json' ':!docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface' ':!docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md' ':!docs/plan.md' ':!specs/public-discovery-and-developer-adoption-surface.test.md'`

### DXA-T008. Live repository metadata after-state proof

- Covers: `DXA-R1`, `DXA-R2`, `DXA-R3`, `DXA-R12`, `DXA-R12a`, `DXA-R12b`, `AC-DXA-001`, `AC-DXA-002`, `AC-DXA-003`, `AC-DXA-011`, E6, EC1, EC2, EC7
- Level: manual
- Fixture/setup: `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/repository-metadata-proof.md`
- Steps: After a maintainer applies live settings, record after-state description, topics, website, evidence source, verifier, verification time/stage, mutation status, and acceptance criteria status.
- Expected result: After-state proof matches approved target values. If permission is unavailable, the milestone remains blocked and `AC-DXA-001` through `AC-DXA-003` remain incomplete.
- Failure proves: External metadata completion is claimed without live evidence or permission blocker handling.
- Automation location: `gh repo view xiongxianfei/rigorloop --json description,homepageUrl,repositoryTopics` or summarized GitHub UI evidence.

### DXA-T009. Lifecycle closeout validation

- Covers: `DXA-R17`, `AC-DXA-001` through `AC-DXA-018`
- Level: integration
- Fixture/setup: completed proof artifacts, touched README/package files, active plan, change metadata, and review records
- Steps: Run final lifecycle and review validators, package tests, stale-version sweep, selector validation, and whitespace checks after implementation and code-review complete.
- Expected result: Required proof artifacts, plan state, change metadata, and review records are synchronized; no metadata acceptance criterion is claimed before after-state proof; no runtime behavior changes are present.
- Failure proves: The branch is not ready for explain-change, final verify, or PR handoff.
- Automation location: active plan M5 validation commands, including `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface`, `python scripts/validate-change-metadata.py docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `npm test --prefix packages/rigorloop`, `python scripts/test-select-validation.py`, and `git diff --check --`

## Fixtures and data

- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/repository-metadata-proof.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/version-sync-proof.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/readme-ownership-proof.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/adoption-surface-review.md`
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/behavior-preservation.md`
- `README.md`
- `VISION.md`
- `specs/readme-user-value-positioning.md`
- `packages/rigorloop/package.json`
- `packages/rigorloop/README.md`

No synthetic fixtures are required unless implementation adds an automated
adoption-surface checker.

## Mocking/stubbing policy

Do not mock repository file checks. Inspect the real README, package README,
package metadata, proof artifacts, and lifecycle artifacts.

External metadata checks may use either live `gh`/npm commands or recorded
maintainer-visible UI evidence when command access is unavailable. Such evidence
must summarize observable metadata only and must not include tokens, cookies,
credentials, browser session data, or private account details.

## Migration or compatibility tests

- `DXA-T002` and `DXA-T006` verify migration from stale current-use `@0.1.5`
  examples to the current stable baseline `@0.2.0`, while allowing explicitly
  historical examples.
- `DXA-T007` verifies no CLI, adapter, skill, validator, release archive, or
  workflow semantic behavior changes occur.
- `DXA-T009` verifies lifecycle artifact compatibility and plan/change metadata
  synchronization before PR handoff.

## Observability verification

Reviewers must be able to reconstruct the decision and proof trail from:

- repository metadata proof for external settings;
- version-sync proof for release version selection;
- README ownership proof for generated-region boundaries;
- adoption-surface review for cold-read, links, commands, unsupported claims,
  stale versions, and visual accuracy;
- behavior-preservation proof for no-runtime-change claims;
- plan validation notes and change metadata for commands actually run.

## Security/privacy verification

- Metadata proof must not include tokens, cookies, credentials, browser session
  details, private keys, proxy credentials, or private account details.
- README and npm-facing copy must not fake adoption, maturity, CI status,
  sponsorship, hosted capabilities, autonomous merge behavior, or replacement of
  Git, CI, pull requests, security review, or human review.
- Link review must not direct users to unofficial or untrusted install sources.

## Performance checks

No runtime performance checks are required. The change must not add heavyweight
media assets, external runtime dependencies, or a heavy measurement dashboard.

The README remains performance-relevant only in a UX sense: manual cold-read
review checks that visitors can identify category, value, first command, proof
path, and contribution/security paths without reading deep mechanics first.

## Manual QA checklist

- Repository metadata proof includes approved target values, before state,
  permission status, after-state fields, mutation status, and metadata
  acceptance status.
- Version-sync proof records GitHub release source, npm version source or
  unavailability, chosen pinned version, and stale-version sweep.
- README ownership proof identifies generated regions and confirms whether any
  owning source artifact or generator changed.
- README first-contact surface answers what, who, why, how to try, proof, and
  contribution/security routing.
- Mermaid lifecycle diagram and caption do not imply mandatory full workflow
  completion for every manual skill invocation.
- Required README links resolve to active repository surfaces.
- Package metadata and package README align with approved positioning when
  touched.
- Behavior-preservation proof and diff review show no forbidden runtime or
  workflow semantic changes.
- Live metadata after-state proof exists before claiming `AC-DXA-001` through
  `AC-DXA-003`.

## What not to test and why

- Do not test new CLI behavior; this slice must not change CLI behavior.
- Do not test adapter generation, adapter archive contents, or skill behavior
  beyond diff/preservation checks; those are out of scope.
- Do not test hosted website behavior, analytics, launch posts, GIF/video
  rendering, or marketing screenshots; they are non-goals.
- Do not require broad social-proof metrics such as stars, forks, downloads, or
  traffic; the spec forbids unsupported adoption claims.
- Do not create browser automation for GitHub repository settings; durable
  proof may be recorded from `gh` or safe UI evidence.

## Uncovered gaps

None. All approved requirements and examples have a proof surface. Most checks
are manual or contract checks because the approved scope centers on external
settings and subjective first-contact evidence rather than runtime behavior.

## Next artifacts

- implementation
- code-review
- explain-change
- verify
- pr

## Follow-on artifacts

None yet.

## Readiness

This test spec is active and ready to guide M1 baseline proof work. Use the
`DXA-T*` cases above as the proof checklist for each milestone.
