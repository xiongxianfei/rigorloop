# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Target: docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md
Reviewed artifact: docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md
Review date: 2026-05-26
Reviewer: Codex proposal-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: CIM-PR1, CIM-PR2, CIM-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-log.md
- Review resolution: docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/review-resolution.md
- Open blockers: none
- Immediate next stage: proposal revision

## Outcome

- Review status: changes-requested
- Material findings: CIM-PR1, CIM-PR2, CIM-PR3
- No downstream handoff: do not proceed to spec, test-spec, or plan until the identity migration and public-skill boundary decisions are explicit.

## Material Findings

### CIM-PR1 - Compatibility alias policy must be resolved before spec

Finding ID: CIM-PR1
Severity: major
Location: Compatibility alias decision; acceptance criteria
Evidence: The proposal made compatibility handling for old `ci` references conditional: keep an alias if the adapter/install mechanism supports it safely, otherwise hard rename with migration guidance. Installed skill names are routing identifiers, and both paths affect generated adapter output and adopter expectations.
Required outcome: State that the first slice must not install two active skill directories. Make `ci-maintenance` the canonical installed skill. Allow legacy `ci` support only as a non-duplicating alias if the adapter, skill registry, or invocation layer supports aliases safely and tests prove no duplicate routing ambiguity. If no safe alias mechanism exists, use a hard rename and release-note migration guidance.
Safe resolution: Add an explicit compatibility alias decision and acceptance criteria proving no generated adapter exposes duplicate active `ci` and `ci-maintenance` skill bodies, alias resolution avoids duplicate routing, or release notes document the hard rename.

### CIM-PR2 - Command ownership boundary must be explicit

Finding ID: CIM-PR2
Severity: major
Location: Workflow skeleton placeholders; skill behavior contract
Evidence: The skeleton includes placeholders such as `<scoped validation command>` and `<comprehensive validation command>`, but the proposal did not state that `ci-maintenance` fills those only from project-owned sources.
Required outcome: Add a command ownership boundary stating that `ci-maintenance` may wire known project validation commands into CI but must not invent validation commands, design tests, execute validation, or claim readiness.
Safe resolution: List approved command sources: approved specs, approved or active test specs, plan validation sections, existing package scripts, existing project CI conventions, or explicit user-provided commands. Add acceptance criteria and fixtures proving missing command sources return a blocker instead of invented commands.

### CIM-PR3 - Risk-to-check map needs a portable/public boundary

Finding ID: CIM-PR3
Severity: major
Location: Risk-to-check map; public skill boundary
Evidence: The proposed map included rows such as `skills`, generated adapter validation, package/release metadata, and scripts/validators. These are valid for RigorLoop but not universal adopter-project surfaces.
Required outcome: Split the risk map into a portable core and project-specific extensions. Label RigorLoop-specific surfaces as project-specific examples, not universal public-skill requirements.
Safe resolution: Add a `Risk-map portability boundary` section, split `references/risk-to-check-map.md` into portable core rows and project-specific extension rows, and add acceptance criteria proving the public skill can be used in non-RigorLoop repositories.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | The rename inconsistency and workflow-output gap are clearly separated. |
| User value | pass | The proposal directly targets clearer skill identity and better CI workflow output. |
| Option diversity | pass | Four options compare rename-only, guidance-only, skeleton-only, and skeleton plus risk map. |
| Decision rationale | pass | Option 4 is directionally correct. |
| Scope control | concern | Alias behavior and public/private risk-map boundary needed sharper decisions. |
| Architecture awareness | pass | Generated adapters, validators, docs, and release notes are named. |
| Testability | concern | Test list was strong but needed command-ownership and alias/no-duplicate tests. |
| Risk honesty | pass | Duplicate routing, hidden policy assets, unsafe caches, and internal leakage are named. |
| Rollout realism | pass | Rename and enhancement are sequenced with migration guidance. |
| Readiness for spec | concern | The proposal needed revision before spec. |

## Scope Preservation Review

- Scope-preservation result: pass. The proposal preserved the initial goals to rename `ci`, fix mixed naming, improve concise and efficient workflows, mitigate common CI risk, avoid overcomplication, keep the skill portable, and avoid hidden repo-internal mechanisms.

## Recommended Proposal Edits

- Add a compatibility alias decision that forbids duplicate active installed skill directories and makes aliasing conditional on a safe non-duplicating alias mechanism.
- Add a command ownership boundary for validation commands.
- Split the risk-to-check map into portable core and project-specific extensions.
- Add acceptance criteria for alias behavior, command-source blocking, and public-skill portability.

## Recommendation

- Recommendation: changes requested. Revise CIM-PR1, CIM-PR2, and CIM-PR3 before downstream spec authoring relies on the proposal.
