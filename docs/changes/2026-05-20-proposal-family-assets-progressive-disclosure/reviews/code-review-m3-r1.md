# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3. Proposal-Review Structural Assets
Reviewed artifact: commit `1d344e7` (`M3: extract proposal-review structural assets`)
Review date: 2026-05-20
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Review status: changes-requested
- Material findings: PFA-M3-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-log.md
- Review resolution: docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/review-resolution.md
- Reviewed milestone: M3. Proposal-Review Structural Assets
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: PFA-M3-CR1
- Verify readiness: not-claimed

## Scope

Reviewed the M3 `proposal-review` structural asset extraction against the
actual commit diff, approved proposal-family asset spec and test spec, active
plan, pinned baseline, M3 behavior-preservation evidence, and recorded
validation evidence.

## Review inputs

- Diff/review surface: commit `1d344e7`
- Tracked governing branch state: commit `1d344e7` on `proposal/proposal-family-assets-progressive-disclosure`
- Governing artifacts:
  - `specs/proposal-family-assets-progressive-disclosure.md`
  - `specs/proposal-family-assets-progressive-disclosure.test.md`
  - `docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md`
  - `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`
  - `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md`
- Validation evidence:
  - `python scripts/validate-skills.py skills/proposal-review/SKILL.md` - pass, 1 skill file
  - `python scripts/test-skill-validator.py` - pass, 151 tests
  - `python scripts/validate-skills.py` - pass, 23 skill files
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass before this review record was added
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` - pass, 3 artifact files
  - `git diff --check --` - pass

## Diff summary

- Added `skills/proposal-review/assets/review-result-skeleton.md` and
  `skills/proposal-review/assets/material-finding.md`.
- Added `COPY` resource-map entries to `skills/proposal-review/SKILL.md`.
- Replaced the full inline proposal-review output skeleton with compact
  asset-copy guidance.
- Recorded M3 preservation, behavior parity, and review-class asset boundary
  evidence in `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/behavior-preservation.md`.
- Updated the active plan, plan index, and change metadata to hand M3 to code
  review.

## Findings

### PFA-M3-CR1

Finding ID: PFA-M3-CR1
Severity: major
Location: `skills/proposal-review/assets/review-result-skeleton.md:6`, `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md:119`, `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md:146`
Evidence: The pinned baseline lists `Skill` as a `review-result-skeleton.md` field and says the asset must preserve the same `## Result` field set and placeholders. The previous inline skeleton started `## Result` and included `- Skill: proposal-review`. The new asset starts `# Result` and begins with `- Review status: <review status>`, so it omits the `Skill` field and changes the top result heading shape.
Required outcome: `review-result-skeleton.md` must preserve the pinned `## Result` block shape and same result field set, including the `Skill` field, without weakening the `proposal-review` review-class asset boundary.
Safe resolution path: Change the asset heading to `## Result`, restore `- Skill: proposal-review` as a structural field, update the `proposal-review` asset structural-label allowlist and positive fixture coverage if needed so the restored field validates as an approved structural label, then rerun the M3 validation commands and return M3 for code-review rerun.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `PFA-R36` and `PFA-R37` require source-to-asset parity and unchanged field obligations. The new review-result asset omits the baseline `Skill` field and changes the previous `## Result` heading shape. |
| Test coverage | concern | The recorded validator tests passed, including proposal-review asset checks, but they did not catch the missing baseline `Skill` field because the allowlist does not currently include it. |
| Edge cases | concern | The named preservation edge case for result field parity is not fully covered; the asset is otherwise limited to approved structural fields and placeholders. |
| Error handling | pass | Asset metadata, visible placeholders, `COPY` mapping, fill-field wording, and no-placeholder guidance are present and validated. |
| Architecture boundaries | pass | The diff does not change adapter roots, lockfiles, CLI behavior, generated output, build-time partials, references, or scripts. |
| Compatibility | concern | Published proposal-review output shape changes by dropping `Skill: proposal-review` from the copied result skeleton. |
| Security/privacy | pass | The asset and skill text introduce no secrets, credentials, private data, unsafe logging, or security-sensitive runtime behavior. |
| Derived artifact currency | pass | M3 intentionally does not edit generated outputs; generated mirror and temporary adapter proof remain assigned to M4. |
| Unrelated changes | pass | The diff is scoped to `proposal-review` asset extraction plus required lifecycle and preservation evidence. |
| Validation evidence | concern | Validation evidence is relevant and credible for deterministic checks, but direct preservation proof fails against the pinned baseline for the result field set. |

## No-finding rationale

Not applicable. M3 has one material finding.

## Residual risks

M4 still needs generated skill mirror proof, temporary adapter output proof,
token-cost/P evidence, cold-read evidence, and final lifecycle evidence. The
two untracked learn artifacts present in the worktree were not part of this
review surface.

## Handoff

- Reviewed milestone: M3. Proposal-Review Structural Assets
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Recommended next stage: review-resolution for `PFA-M3-CR1`
- Final closeout readiness: not ready; M3 requires review-resolution and re-review, M4 remains open, and explain-change, verify, and PR handoff remain open.
- Automatic downstream handoff: none from this isolated code-review invocation.
