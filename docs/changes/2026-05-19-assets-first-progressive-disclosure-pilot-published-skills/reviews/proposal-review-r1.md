# Proposal Review R1: Assets-First Progressive Disclosure Pilot for Published Skills

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: external proposal-review result provided in chat
Target: docs/proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md
Status: changes-requested
Record mode: reconstructed
Original review source: chat result provided after proposal drafting
Original review evidence: user-provided proposal-review result with material findings APD-PR1 through APD-PR4
Created after fixes began: yes
Loss of fidelity: none known; finding IDs, severity, evidence, required outcomes, and safe resolution paths were preserved in summarized form

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: APD-PR1, APD-PR2, APD-PR3, APD-PR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md
- Review resolution: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-resolution.md
- Open blockers: spec-slice dependency, handoff asset risk, output-skeleton source boundary, asset validation oracle precision
- Immediate next stage: proposal revision, then spec amendment after proposal-review approval
- No automatic downstream handoff: this review does not start spec or implementation work.

## Overall Verdict

Good direction, changes requested before spec amendment.

The proposal has a strong core: use a narrow `assets/`-only pilot, choose `plan` rather than high-risk review skills, keep rules in `SKILL.md`, package assets through adapters, and require behavior parity before claiming success. The requested changes tighten source-of-truth boundaries and testability before the proposal advances.

## Material Findings

### APD-PR1 - Proposal needs explicit dependency on existing skill-contract slice

Finding ID: APD-PR1
Severity: major
Location: `Recommended direction`, `First-slice boundary`, `Next artifacts`
Evidence: The proposal chooses `plan` as the first asset pilot and names `spec amendment: specs/skill-contract.md`, but does not explicitly say whether this is a new follow-on slice or a revision to current skill-contract first-slice scope.
Required outcome: State that this proposal is a new follow-on asset pilot, not part of the existing published-skill design first slice, unless the governing spec is explicitly amended.
Safe resolution path: Add a spec-slice dependency section and rename `first implementation slice` to `asset pilot implementation slice`.

### APD-PR2 - Handoff summary asset is lifecycle-sensitive

Finding ID: APD-PR2
Severity: major
Location: `Recommended pilot asset layout`, `Resource map contract`, `Behavior-parity requirements`
Evidence: The proposal includes `assets/current-handoff-summary.md` for the active plan handoff section, while current handoff state is workflow-sensitive.
Required outcome: Clarify that the handoff asset may contain only structure and placeholders, while handoff semantics, state consistency requirements, and claim boundaries remain in `SKILL.md` or governing workflow/spec artifacts.
Safe resolution path: Add a handoff asset boundary and acceptance criteria for no lifecycle transition rules in the asset and retained handoff consistency rules in `SKILL.md`.

### APD-PR3 - Output skeleton source boundary is unclear

Finding ID: APD-PR3
Severity: major
Location: `Recommended pilot asset layout`, `Asset contract`, `Expected behavior changes`
Evidence: The proposal adds `assets/plan-skeleton.md` as a full plan skeleton and says `SKILL.md` remains the execution contract, but prior readability work expects artifact-producing skills to expose a fillable output skeleton or reviewed equivalent.
Required outcome: Define the source-of-truth relationship between the inline output expectation and the asset.
Safe resolution path: State that `assets/plan-skeleton.md` may serve as the reviewed equivalent output template only if `SKILL.md` includes a compact output expectation summary and Resource map entry, and avoid duplicating the full section layout in both places.

### APD-PR4 - Asset validation checks need deterministic oracle boundaries

Finding ID: APD-PR4
Severity: major
Location: `Testing and verification strategy`
Evidence: The proposal says validators should prove assets contain structural markup and placeholders, not paragraph-length procedure text, and says behavior-parity fixtures should preserve plan shape and handoff semantics.
Required outcome: Define which checks are static, which are review-only, and which are fixture-based.
Safe resolution path: Add an asset validation oracle boundary that limits static validation to deterministic checks and routes qualitative prose or behavior-parity judgments to bounded heuristics, fixtures, or code review.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The problem is concrete: progressive disclosure exists as guidance but has no packaged-resource pilot. |
| User value | pass | The pilot improves published-skill maintainability and adapter confidence without broad disruption. |
| Option diversity | pass | The proposal compares do-nothing, broad resource pilot, settled-skill retrofit, and `plan` asset pilot. |
| Decision rationale | pass | `plan` is a defensible pilot because it has repeated milestone structure and lower review-recording risk. |
| Scope control | concern | Needs explicit relationship to the existing skill-contract first slice. |
| Architecture awareness | concern | Output-template and handoff-rule ownership need tightening. |
| Testability | concern | Validator oracles need deterministic boundaries. |
| Risk honesty | pass | Risks around hidden behavior, packaging, placeholders, semantics, and token-cost overclaim are named. |
| Rollout realism | pass with concern | The rollout is incremental, but depends on resolving spec-slice sequencing. |
| Readiness for spec | changes-requested | Direction is ready, but four material clarifications should be added before spec amendment. |

## Scope Preservation

Scope preservation result: pass.

The proposal preserves the requested intent to prove progressive disclosure with a small, assets-only `plan` pilot while preserving self-containment, behavior parity, adapter packaging validation, and avoidance of references, scripts, and build-time partials.

## Blocking Questions

1. Is the `plan` asset pilot a new follow-on slice after the current published-skill design-contract slice, or does it amend the current slice?
2. Should `current-handoff-summary.md` remain an asset, or is it too lifecycle-sensitive for the first asset pilot?
3. Will `assets/plan-skeleton.md` be the reviewed equivalent output template, or will `SKILL.md` retain the full output skeleton?
4. Which asset checks are static validator checks, and which are code-review or behavior-parity checks?

## Readiness

Not ready for spec amendment as written. The direction is worth keeping. After APD-PR1 through APD-PR4 are resolved, the proposal can be rerun through proposal review and then proceed to spec amendment if approved.
