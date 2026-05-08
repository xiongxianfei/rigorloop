# Review Resolution: Skill Contract Optimization

## Summary

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: code-review-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `code-review-r1`, `code-review-r2`
- Findings resolved: 8
- Unresolved findings: 0
- Final result: proposal-review identified five major findings and two concerns in R1. The proposal findings are closed. `code-review-r1` found one M1 validator-scaffolding issue, `CR1-F1`; the fix was applied and `code-review-r2` returned clean-with-notes for M1.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SCO1 | accepted | resolved | Added an explicit first implementation slice and removed the contradictory open question. |
| SCO2 | accepted | resolved | Made `specs/skill-contract.md` the normative skill-contract source and defined the ownership split. |
| SCO3 | accepted | resolved | Replaced the one-size section shape with required core, conditional sections, and skill-type variants. |
| SCO4 | accepted | resolved | Added shared-block source-of-truth rules under `templates/shared/<block-name>.md`. |
| SCO6 | accepted | resolved | Renamed the claim-ownership row to `review-resolution artifact/guidance`. |
| SCO7 | accepted | resolved | Changed the result block to a minimal common core plus optional type-specific fields. |
| SCO8 | accepted | resolved | Made examples optional, bounded, and routed long examples outside skill files. |
| CR1-F1 | accepted | resolved | Tightened the first-slice test-spec assertion so short skill names cannot pass from unrelated words. |

## Resolution Entries

### proposal-review-r1

#### SCO1 - First implementation slice is still not settled

Finding ID: SCO1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `First implementation slice`, listing only `skills/workflow/SKILL.md`, `skills/plan/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, and `skills/learn/SKILL.md`, plus the allowed first-slice changes.
Rationale: The proposal should choose the first implementation slice before spec and plan authors rely on it.
Validation target: Proposal text no longer contains an open question asking which skills are first.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed; `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md` passed.

#### SCO2 - Normative source is ambiguous

Finding ID: SCO2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Normative ownership`, making `specs/skill-contract.md` the normative source for skill-contract behavior and defining the ownership split with workflow spec, workflow docs, and local skills.
Rationale: Validator-enforced skill behavior needs a clear source of truth instead of conditional spec ownership.
Validation target: Proposal names `specs/skill-contract.md` as normative and updates architecture impact accordingly.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed; `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md` passed.

#### SCO3 - Standard section shape should not be one-size-fits-all

Finding ID: SCO3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Replaced the full standard section list with required core sections, conditional sections, and variants for authoring, review, execution, and periodic skills.
Rationale: Skills need consistent scanning anchors without flattening useful domain-specific guidance.
Validation target: Proposal distinguishes required core sections from conditional and skill-type-specific sections.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed; `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md` passed.

#### SCO4 - Shared-block source boundary needs a governance decision

Finding ID: SCO4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Shared-block source of truth`, naming `templates/shared/<block-name>.md` as canonical authored source for copied skill subsections and defining verbatim-copy, validator-comparison, generated-output, and non-replacement rules.
Rationale: Shared blocks need one canonical source so copied skill sections can be compared without inventing another policy authority.
Validation target: Proposal defines shared-block authority and notes that `templates/` is already listed as a canonical authored source in governance.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed; `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md` passed.

#### SCO6 - `review-resolution guidance` is not a skill but appears as a skill row

Finding ID: SCO6
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Renamed the claim-ownership table row from `review-resolution guidance` to `review-resolution artifact/guidance`.
Rationale: The proposal explicitly does not introduce a standalone review-resolution skill, so the table should not imply one.
Validation target: Proposal uses `review-resolution artifact/guidance` in the ownership table.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed; `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md` passed.

#### SCO7 - Output result block should be adapted by skill type

Finding ID: SCO7
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Replaced the result block with a minimal common core and optional fields for validation, review, milestones, readiness, follow-ups, authoring skills, and learn.
Rationale: A result block should make common handoff data predictable while allowing skill-specific evidence fields.
Validation target: Proposal defines core result fields and optional type-specific fields.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed; `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md` passed.

#### SCO8 - Examples may bloat skills

Finding ID: SCO8
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added an `Examples` subsection making examples optional, short, and bounded to one minimal valid and one invalid example when they prevent recurring errors.
Rationale: Examples can prevent recurring errors, but long examples would conflict with the proposal's goal of smaller skills.
Validation target: Proposal states that long examples belong in `examples/` or templates, not skill files.
Validation evidence: `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-08-skill-contract-optimization` passed; `bash scripts/ci.sh --mode explicit --path docs/proposals/2026-05-08-skill-contract-optimization.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/proposal-review-r1.md` passed.

### proposal-review-r2

No material findings.

### code-review-r1

#### CR1-F1 - First-slice test-spec coverage check is too weak for short skill names

Finding ID: CR1-F1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implement
Chosen action: Tightened the `scripts/test-skill-validator.py` first-slice test-spec assertion so it checks exact bounded evidence from the T3 first-slice list instead of bare skill-name substrings. Also tightened the plan assertion to use canonical `skills/<skill>/SKILL.md` paths instead of bare skill-name substrings.
Rationale: M1's static proof should not allow `pr` or other short skill names to pass from unrelated words in the test spec.
Validation target: `python scripts/test-skill-validator.py` and the M1 selector/CI commands pass after the assertion is tightened.
Validation evidence: `python scripts/test-skill-validator.py` passed after the bounded assertion change; `bash scripts/ci.sh --mode explicit --path scripts/test-skill-validator.py --path docs/changes/2026-05-08-skill-contract-optimization/review-log.md --path docs/changes/2026-05-08-skill-contract-optimization/review-resolution.md --path docs/changes/2026-05-08-skill-contract-optimization/reviews/code-review-r1.md --path docs/changes/2026-05-08-skill-contract-optimization/change.yaml --path docs/plans/2026-05-08-skill-contract-optimization.md` passed selected checks after the fix; `code-review-r2` returned clean-with-notes.

### code-review-r2

No material findings.
