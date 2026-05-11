# Review Skill Recording Output Guardrail Review Resolution

## Scope

This record resolves material findings from formal lifecycle reviews for the review skill recording output guardrail change.

Closeout status: closed

## Resolution Entries

### proposal-review-r1

Review closeout: proposal-review-r1

#### RSG1

Finding ID: RSG1
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Revise the proposal so `recorded` means every artifact required by the active recording trigger exists or was updated, and distinguish material findings from no-material detailed-record triggers.
Rationale: The finding is correct. The proposal must preserve the approved boundary that `review-resolution.md` is required for material findings or another approved trigger, not every detailed review record.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to define `recorded` by the active recording trigger and distinguish material findings from no-material detailed-record triggers. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.

#### RSG2

Finding ID: RSG2
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Add a change ID selection rule for required review recording artifacts.
Rationale: The finding is correct. Review skills need a deterministic path before they can record material findings without blocking unnecessarily.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to add deterministic change ID selection before blocking. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.

#### RSG3

Finding ID: RSG3
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Define valid `Location` forms for file, section, line, missing artifact, requirement, milestone, and absence-based findings.
Rationale: The finding is correct. `Location` must be required but flexible enough for absent evidence or missing artifact findings.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to define flexible valid `Location` forms. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.

#### RSG4

Finding ID: RSG4
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Choose an explicit first-slice shared wording strategy for all formal review skills.
Rationale: The finding is correct. Five hand-written variants would invite drift in a contract whose value depends on consistency.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to choose the first-slice shared wording strategy and remove it as an unresolved open question. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.

#### RSG5

Finding ID: RSG5
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Clarify that recording status is separate from the stage-specific review verdict or review status.
Rationale: The finding is correct. `recorded` is artifact-recording state, not a review approval outcome.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to include a result shape with separate `Review status` and `Recording status` fields and to state that recording status is not the review verdict. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.

#### RSG6

Finding ID: RSG6
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Add a later automation trigger if formal reviews again report material findings without `Recording status: recorded` or `Recording status: blocked`.
Rationale: The finding is correct. Static checks are a reasonable first slice, but recurrence should trigger stronger runtime or output validation.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to add a later runtime/output validation trigger if the lapse recurs. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.

### proposal-review-r2

Review closeout: proposal-review-r2

#### RSG-F2

Finding ID: RSG-F2
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Revise `Next Artifacts` so a focused spec amendment for formal review output recording and artifact-status sync is required.
Rationale: The finding is correct. Artifact-status sync changes cross-review lifecycle behavior and should be owned by the workflow/review contract, not only by skill wording.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` so `Next Artifacts` requires a focused spec amendment for formal review output recording and artifact-status sync. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md docs/changes/2026-05-12-review-skill-recording-output-guardrail docs/learn/sessions/2026-05-12-review-approval-status-sync.md` passed after revision.

#### RSG-F3

Finding ID: RSG-F3
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Add an explicit edit-permission rule for isolated and review-only requests.
Rationale: The finding is correct. Status sync is not downstream continuation, but it is still an artifact edit and must respect explicit no-edit user instructions.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to state that workflow-managed and isolated reviews may update status surfaces unless the user explicitly forbids edits; explicit no-edit instructions produce `Status sync: blocked`. Validation commands listed under RSG-F2 passed after revision.

#### RSG-F4

Finding ID: RSG-F4
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Tighten the artifact-specific status table and add a block condition when the next status cannot be chosen from the table or an artifact-local lifecycle field.
Rationale: The finding is correct. Broad phrases such as "according to artifact vocabulary" or "plan-owned state" need narrower targets so implementers do not guess.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to replace the broad status table with stricter targets and a `Status sync: blocked` rule when the next status cannot be chosen. Validation commands listed under RSG-F2 passed after revision.

#### RSG-F5

Finding ID: RSG-F5
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Add separate `Recording blocker` and `Status sync blocker` output fields and define when each is required.
Rationale: The finding is correct. Recording and status sync can fail independently, so final output must not collapse both into a generic blocker.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to add `Recording blocker` and `Status sync blocker` fields and require each when its corresponding status is blocked. Validation commands listed under RSG-F2 passed after revision.

#### RSG-F6

Finding ID: RSG-F6
Disposition: accepted
Owner: implementer
Owning stage: proposal
Chosen action: Split implementation planning into two milestones: recording-status guardrail first, artifact-status sync second.
Rationale: The finding is correct. The proposal can keep both behaviors, but the execution plan should avoid making the first implementation slice too broad.
Validation target: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md`
Validation evidence: Proposal revised in `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` to require execution planning milestones M1 recording-status guardrail and M2 artifact-status sync guardrail. Validation commands listed under RSG-F2 passed after revision.

### spec-review-r1

Review closeout: spec-review-r1

#### SR1

Finding ID: SR1
Disposition: accepted
Owner: implementer
Owning stage: spec
Chosen action: Revise `R30` so status sync is required for clean or approving formal review results when the status target is clear and edits are allowed, while preserving `Status sync: blocked` for explicit no-edit instructions, unavailable repository state, ambiguous ownership, or missing status surfaces.
Rationale: The finding is correct. The accepted proposal requires clean or approving review results to synchronize the reviewed artifact to its next artifact-specific lifecycle status when the status surface is clear. A `MAY update` requirement makes the core status-sync behavior optional and weakens the contract.
Validation target: `specs/formal-review-recording.md`
Validation evidence: `R30` in `specs/formal-review-recording.md` was revised to require update-or-block behavior for clean or approving formal review results. `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-12-review-skill-recording-output-guardrail`, and `git diff --check -- specs/formal-review-recording.md docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.
