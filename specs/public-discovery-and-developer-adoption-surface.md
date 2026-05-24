# Public Discovery and Developer Adoption Surface

## Status

approved

## Related proposal

- [Public Discovery and Developer Adoption Surface](../docs/proposals/2026-05-23-public-discovery-and-developer-adoption-surface.md)
- Proposal review: [proposal-review-r1](../docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/reviews/proposal-review-r1.md)
- Related approved README contract: [README User Value Positioning](readme-user-value-positioning.md)

## Goal and context

This spec defines the public discovery and first-contact developer adoption
contract for RigorLoop's repository metadata, root README, npm-facing package
surface, and reviewable evidence for those external or subjective checks.

The goal is to make RigorLoop easier to discover and easier to evaluate within a
few seconds while preserving the existing project truth: RigorLoop is a
Git-first workflow for AI coding agents and human reviewers, not a hosted
runtime, autonomous code-merging system, replacement for pull requests, or
replacement for CI and human review.

This spec extends the approved README positioning contract. It does not change
workflow semantics, CLI behavior, skill behavior, adapter behavior, validator
behavior, release archive trust boundaries, or the repository source-of-truth
order.

## Glossary

- `adoption surface`: public surfaces a first-time visitor or package consumer
  sees before deep repository inspection, including GitHub repository metadata,
  root README, npm package metadata, and package README.
- `repository metadata`: GitHub repository description, topics, and website
  field.
- `first-contact README surface`: the top portion of `README.md` that a GitHub
  visitor sees before reaching detailed mechanics or reference content.
- `current stable release`: the latest stable GitHub release tag at
  implementation time, cross-checked against the npm package version when npm
  metadata is available.
- `pinned CLI example`: an example command using an explicit
  `@x.y.z` npm package version instead of `@latest`.
- `generated README region`: README content whose owning source is another
  artifact or generator, including the `<!-- vision:start -->` to
  `<!-- vision:end -->` region generated from `VISION.md`.
- `cold-read reviewer`: a reviewer or role that reads the public adoption
  surface as a first-time visitor and records what they can identify without
  deep repository inspection.

## Examples first

Example E1: GitHub visitor understands the project quickly
Given a first-time visitor lands on the GitHub repository page
When they read the repository description, topics, and first-contact README surface
Then they can identify that RigorLoop is a Git-first workflow for AI coding agents and human reviewers, see a first command to try, and find deeper workflow, example, contribution, and security links without reading deep specs.

Example E2: Quick Start stays reproducible
Given the latest stable GitHub release and npm package version both resolve to `0.2.0`
When the README and npm package README show Quick Start commands
Then quick-trial commands use `@latest`, reproducible onboarding commands use `@0.2.0`, and no current Quick Start surface still pins `@0.1.5`.

Example E3: release sources disagree
Given the latest stable GitHub release says `v0.2.0`
And npm package metadata says `0.1.5`
When implementation prepares pinned Quick Start examples
Then implementation blocks for an owner decision instead of choosing one source silently.

Example E4: generated README ownership is respected
Given target README text is inside `<!-- vision:start -->` and `<!-- vision:end -->`
When implementation changes that text
Then it updates the owning source artifact or generator rather than hand-editing only `README.md`.

Example E5: lifecycle visual stays honest
Given the README includes a Mermaid lifecycle diagram from idea to PR
When a reader inspects the caption
Then the caption says the full chain is recommended for complete AI-assisted delivery and manual skill invocations may use only relevant stages without implying the full workflow is complete.

Example E6: external GitHub metadata is reviewable
Given repository description and topics are external GitHub settings
When implementation changes those settings
Then the change records before/after metadata proof in a durable change-local artifact without storing tokens, cookies, or browser session details.

## Requirements

DXA-R1. The GitHub repository description MUST be set to:

```text
Git-first workflow for AI coding agents: proposals, specs, tests, review gates, and durable validation evidence from idea to PR.
```

DXA-R1a. If implementation evidence shows the GitHub UI truncates or displays
the approved description poorly, the owner MAY choose this shorter description
instead:

```text
Traceable Git-first workflow for AI coding agents, from proposal to verified PR.
```

DXA-R1b. The repository description MUST NOT use a vague category-only
description such as `A tool for AI agents`.

DXA-R2. GitHub repository topics MUST be set to a relevant list of no more than
20 lowercase, number, or hyphen topic names.

DXA-R2a. The first approved topic set SHOULD be:

```text
ai-agents
ai-coding
coding-agent
agentic-workflow
llm
developer-tools
software-engineering
code-review
git-workflow
cli
npm-package
claude-code
codex
opencode
workflow
testing
validation
pull-requests
```

DXA-R2b. If implementation uses a smaller topic set, it MUST preserve the
RigorLoop positioning around AI coding, developer tooling, code review, Git
workflow, CLI/npm delivery, and supported agent adapters.

DXA-R3. The GitHub repository website field MUST remain blank for this slice
unless implementation identifies and records an owner-approved stable docs
landing page.

DXA-R3a. The website field MUST NOT point to a temporary release page, raw README
anchor, or npm package page unless that surface is approved as the public landing
page.

DXA-R4. The root README MUST continue to satisfy
`specs/readme-user-value-positioning.md`.

DXA-R4a. This spec MUST NOT be used to reorder the README in a way that violates
the approved value-first README contract, including the required near-top
`When to use / When not to use` section before mechanics/reference content.

DXA-R5. The first-contact README surface MUST answer, directly or through a
near-top scannable link group, all of the following:

- what RigorLoop is;
- who it is for;
- why it matters;
- how to try it;
- where to see proof or deeper workflow evidence;
- where to contribute, report feedback, or find security guidance.

DXA-R6. The README MUST include a first-contact Quick Start path with both:

- `@latest` commands for quick trials;
- pinned current-stable-release commands for reproducible onboarding.

DXA-R6a. The current implementation baseline pinned version is `@0.2.0`.

DXA-R6b. Before implementation uses any pinned version, it MUST record the
GitHub latest stable release source and npm package version source when npm
metadata is available.

DXA-R6c. If the GitHub latest stable release and npm package version disagree,
implementation MUST block for an owner decision.

DXA-R6d. Current Quick Start and npm landing surfaces MUST NOT retain stale
pinned public CLI examples such as `@0.1.5` unless those examples are explicitly
marked as historical.

DXA-R7. The README MUST include a static Mermaid lifecycle diagram for the first
slice.

DXA-R7a. The diagram SHOULD show:

```text
Idea -> Proposal -> Spec -> Test spec -> Plan -> Implement -> Code review -> Explain change -> Verify -> PR
```

DXA-R7b. The diagram caption MUST communicate that RigorLoop recommends the full
chain for complete AI-assisted delivery and that manual skill invocations may
use only relevant stages without implying full workflow completion.

DXA-R7c. The first slice MUST NOT require a CLI GIF, long product video, or
marketing screenshot gallery.

DXA-R8. The README MUST include visible links or a near-top link group for:

- Quick Start;
- workflow guidance;
- proof-of-value example;
- contribution guidance;
- bug report path;
- feature request path;
- security policy.

DXA-R8a. Links MUST point to active repository surfaces and MUST NOT point to
stale, missing, or contradictory documents.

DXA-R9. Implementation MUST identify whether edited README text is inside or
outside generated/owned regions.

DXA-R9a. If edited README text is inside a generated/owned region, implementation
MUST update the owning source artifact or generator and not only `README.md`.

DXA-R9b. If edited README text is outside generated/owned regions,
implementation MUST verify it does not contradict `VISION.md`, source-of-truth
sections, or `specs/readme-user-value-positioning.md`.

DXA-R10. The npm package description SHOULD closely mirror the approved GitHub
repository description when package metadata is touched.

DXA-R10a. npm package keywords SHOULD mirror relevant GitHub topics when package
metadata is touched and the package metadata format supports keywords.

DXA-R10b. The package README Quick Start and current command examples MUST align
with the root README Quick Start and current stable release version.

DXA-R10c. npm-facing content MUST NOT claim behavior unsupported by the current
CLI.

DXA-R10d. npm-facing content MUST keep npm positioned as a delivery channel, not
the canonical source for workflow rules, skills, schemas, templates, or adapter
archives.

DXA-R11. Public adoption copy MUST NOT claim unsupported broad adoption,
production maturity, hosted-platform capabilities, autonomous code merging,
replacement of Git-based review, replacement of CI, or replacement of human
review.

DXA-R12. Implementation MUST record durable repository metadata proof at:

```text
docs/changes/<change-id>/repository-metadata-proof.md
```

DXA-R12a. Repository metadata proof MUST include approved description, approved
topic list, website field value or explicit blank decision, command or UI
evidence used to set values, before/after metadata evidence, permission context,
and confirmation that no runtime/package behavior changed.

DXA-R12b. Repository metadata proof MUST NOT record tokens, cookies, credentials,
or browser session details.

DXA-R13. Implementation MUST record durable version-sync proof at:

```text
docs/changes/<change-id>/version-sync-proof.md
```

DXA-R13a. Version-sync proof MUST include the GitHub latest stable release
source, npm package version source or reason npm metadata was unavailable, chosen
pinned version, stale-version sweep result, and any owner decision if version
sources disagreed.

DXA-R14. Implementation MUST record durable README ownership proof at:

```text
docs/changes/<change-id>/readme-ownership-proof.md
```

DXA-R14a. README ownership proof MUST identify generated or owned README regions
inspected, whether any generated region was changed, owning source artifacts or
generators updated when applicable, and contradiction checks against `VISION.md`
and README source-of-truth sections.

DXA-R15. Implementation MUST record cold-read and link-check evidence at:

```text
docs/changes/<change-id>/adoption-surface-review.md
```

DXA-R15a. Adoption-surface review evidence MUST include reviewer or role, first
command identified, one-sentence value proposition identified, target audience
identified, links checked, Quick Start commands checked, unsupported-claim sweep
result, stale-version sweep result, and visual accuracy check result.

DXA-R16. Implementation MUST record behavior-preservation proof at:

```text
docs/changes/<change-id>/behavior-preservation.md
```

DXA-R16a. Behavior-preservation proof MUST cover CLI behavior, adapter behavior,
skill behavior, README Quick Start, repository metadata, npm metadata when
touched, and contribution routing.

DXA-R17. This slice MUST NOT change runtime CLI behavior, adapter behavior, skill
behavior, validator behavior, release archive trust boundaries, or core workflow
semantics.

DXA-R18. If a link checker exists in the repository, implementation MUST run it
for touched adoption surfaces or record why it is not applicable.

DXA-R18a. If no link checker exists, implementation MUST record manual link
review for all links required by this spec.

## Inputs and outputs

Inputs:

- GitHub repository metadata for `xiongxianfei/rigorloop`
- root `README.md`
- `VISION.md`
- `specs/readme-user-value-positioning.md`
- package metadata for `@xiongxianfei/rigorloop`
- package README for `@xiongxianfei/rigorloop`
- GitHub latest release metadata
- npm package version metadata when available
- contribution, issue-template, code-of-conduct, security, workflow, and
  proof-of-value repository surfaces

Outputs:

- updated GitHub repository description, topics, and website field decision
- updated root README first-contact adoption surface
- updated npm package metadata and package README when touched
- Mermaid lifecycle diagram in README
- durable change-local proof artifacts for metadata, version sync, README
  ownership, cold-read/link checks, and behavior preservation

## State and invariants

- `VISION.md` remains the canonical project-vision artifact.
- README content between `<!-- vision:start -->` and `<!-- vision:end -->`
  remains generated from `VISION.md`.
- `README.md` remains a public project overview, not the canonical workflow
  source of truth.
- npm remains a CLI delivery channel, not a canonical workflow source.
- GitHub repository metadata is external state and requires durable proof.
- Documentation and metadata changes do not imply runtime behavior changes.
- The approved README positioning contract remains active.

## Error and boundary behavior

- If the repository description or topic list cannot be changed because the
  implementer lacks permission, implementation must record the blocker and stop
  before claiming `DXA-R1` or `DXA-R2` complete.
- If GitHub release metadata and npm package metadata disagree for the current
  stable version, implementation must block for owner decision before updating
  pinned version examples.
- If a required README, contribution, issue-template, security, workflow, or
  proof link does not exist, implementation must either correct the target within
  scope or record a blocker before claiming adoption-surface readiness.
- If README text inside a generated region needs to change and the owning source
  or generator is unclear, implementation must block instead of hand-editing the
  generated region.
- If cold-read evidence shows the reviewer cannot identify value proposition,
  audience, or first command, implementation must revise the adoption surface
  before claiming acceptance criteria complete.
- If a proposed README or npm-package claim exceeds current CLI, adapter, or
  workflow behavior, implementation must remove the claim or return to proposal
  for a behavior-changing scope decision.

## Compatibility and migration

- Existing runtime CLI commands and adapter install behavior remain unchanged.
- Existing workflow rules, review gates, source-of-truth order, validation
  semantics, and release archive trust boundaries remain unchanged.
- Existing deep README mechanics may be moved, shortened, or linked as long as
  the README still satisfies this spec and `specs/readme-user-value-positioning.md`.
- Stale pinned `@0.1.5` examples in current adoption surfaces migrate to
  `@0.2.0` for this baseline unless they are intentionally historical.
- Rollback for tracked file changes is a revert of README/package wording and
  proof artifacts. Rollback for GitHub metadata is restoring the prior
  description, topics, or website value recorded in repository metadata proof.

## Observability

- Reviewers must be able to inspect durable proof artifacts to verify external
  GitHub metadata changes that do not appear in the Git diff.
- Reviewers must be able to inspect version-sync proof to determine why the
  pinned release version was selected.
- Reviewers must be able to inspect README ownership proof to confirm generated
  regions were respected.
- Reviewers must be able to inspect adoption-surface review evidence to confirm
  cold-read, link-check, command-check, unsupported-claim, stale-version, and
  visual-accuracy checks.
- Diff review must be able to confirm no runtime, skill, adapter, validator, or
  release archive changes are included in this slice.

## Security and privacy

- Repository metadata proof must not include tokens, cookies, credentials,
  browser session details, private keys, or private account data.
- Adoption copy must not fake stars, forks, production usage, security status,
  CI status, sponsorship, or broad adoption.
- npm-facing and README-facing claims must not encourage bypassing code review,
  CI, security review, or human release judgment.
- Link updates must not direct users to untrusted or unofficial install sources.

## Accessibility and UX

- The README adoption surface must remain text-readable without relying on
  images or video.
- The Mermaid diagram must have adjacent text or caption that communicates the
  lifecycle meaning and manual-invocation boundary.
- Link text must be descriptive enough for skimming readers to understand the
  target.
- Quick Start commands must be copy-pasteable shell commands.

## Performance expectations

- The first slice must not add heavyweight media assets or external runtime
  dependencies.
- The README adoption surface should remain scannable on GitHub without forcing
  a visitor to read full workflow mechanics before seeing the project category,
  value, first command, and next links.
- Validation for this slice should use repository-owned scripts and bounded
  manual evidence rather than introducing a new heavy measurement system.

## Edge cases

EC1. If GitHub UI display truncates the approved long description poorly, the
shorter approved description may be used with owner approval.

EC2. If no stable docs landing page exists, the website field remains blank even
though a blank field is less visually complete than a filled field.

EC3. If package metadata lacks keyword support or a publish surface does not
consume keywords, implementation records that limit instead of inventing a new
metadata format.

EC4. If a stale pinned version appears only in release notes or historical
examples that intentionally document prior versions, it may remain if clearly
marked historical and excluded from current Quick Start or npm landing surfaces.

EC5. If no link checker exists, manual link review is sufficient when recorded
with checked targets and results.

EC6. If cold-read review is performed by a project maintainer rather than a new
external user, the evidence must label that reviewer role so later reviewers can
judge the limitation.

EC7. If repository metadata changes are made through the GitHub UI instead of
the GitHub CLI, proof may summarize UI evidence without recording secrets,
cookies, or session details.

EC8. If the README generated vision block already answers part of the
first-contact questions, implementation may rely on it, but must still respect
the generated-region ownership rule.

## Non-goals

- Changing CLI behavior.
- Changing adapter behavior.
- Changing skill behavior.
- Changing validator behavior.
- Changing release archive trust boundaries.
- Changing core workflow semantics, workflow stage order, or source-of-truth
  ordering.
- Creating a product website or GitHub Pages docs site.
- Creating a CLI GIF, long product video, or marketing screenshot gallery.
- Launching Dev.to, Hacker News, Reddit, social, or other off-platform
  promotion.
- Adding analytics dashboards or paid growth tactics.
- Claiming broad adoption before evidence exists.
- Replacing detailed docs, specs, or examples with README prose.

## Acceptance criteria

- AC-DXA-001. GitHub repository description matches `DXA-R1` or the approved
  shorter fallback in `DXA-R1a`.
- AC-DXA-002. GitHub topics satisfy `DXA-R2` and are no more than 20 valid topic
  names.
- AC-DXA-003. GitHub website field is blank or has owner-approved stable docs
  landing proof.
- AC-DXA-004. README first-contact surface answers the questions in `DXA-R5`
  while continuing to satisfy `specs/readme-user-value-positioning.md`.
- AC-DXA-005. README Quick Start includes `@latest` and the current pinned
  stable version, with `@0.2.0` as the current baseline unless source evidence
  requires owner decision.
- AC-DXA-006. No current Quick Start or npm landing surface retains stale
  `@0.1.5` pinned examples unless clearly historical.
- AC-DXA-007. README includes the approved Mermaid lifecycle diagram and caption.
- AC-DXA-008. README links include workflow guidance, proof-of-value example,
  contribution guide, bug report path, feature request path, and security policy.
- AC-DXA-009. Package metadata description and keywords align with repository
  positioning when package metadata is touched.
- AC-DXA-010. Package README Quick Start and command examples align with the root
  README and current stable release when package README is touched.
- AC-DXA-011. Repository metadata proof exists and satisfies `DXA-R12`.
- AC-DXA-012. Version-sync proof exists and satisfies `DXA-R13`.
- AC-DXA-013. README ownership proof exists and satisfies `DXA-R14`.
- AC-DXA-014. Adoption-surface review evidence exists and satisfies `DXA-R15`.
- AC-DXA-015. Behavior-preservation proof exists and satisfies `DXA-R16`.
- AC-DXA-016. Documentation and metadata changes do not claim unsupported CLI,
  adapter, workflow, hosted-platform, autonomous-merge, or release behavior.
- AC-DXA-017. The implementation diff does not include runtime CLI, adapter,
  skill, validator, release archive, or workflow semantic changes.
- AC-DXA-018. Link validation evidence is recorded through an existing link
  checker or manual link review.

## Open questions

None.

## Next artifacts

- spec-review
- plan
- plan-review
- test-spec only if spec-review or plan-review decides automated metadata,
  README, link, or package checks should be formalized before implementation
- implementation
- code-review
- explain-change
- verify
- pr

## Follow-on artifacts

- Spec review: [docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/reviews/spec-review-r2.md](../docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/reviews/spec-review-r2.md)
- Plan: [docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md](../docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md)

## Readiness

Approved after clean `spec-review`. Downstream planning has begun.
