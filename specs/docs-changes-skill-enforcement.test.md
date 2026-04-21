# Docs Changes Skill Enforcement test spec

## Status

- active

## Related spec and plan

- Spec: `specs/docs-changes-skill-enforcement.md`
- Related proposal: `docs/proposals/2026-04-21-docs-changes-skill-enforcement.md`
- Plan: `docs/plans/2026-04-21-docs-changes-skill-enforcement.md`
- Related governing and proof surfaces:
  - `specs/rigorloop-workflow.md`
  - `specs/docs-changes-usage-policy.md`
  - `specs/docs-changes-usage-policy.test.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - canonical `skills/`
  - generated `.codex/skills/`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `bash scripts/ci.sh`

## Testing strategy

- Use manual contract review for the touched canonical skills because this feature aligns stage-local guidance rather than adding a new runtime subsystem.
- Use the existing docs-changes and workflow-stage test specs as relied-on proof surfaces where they already own the governing contract:
  - `specs/docs-changes-usage-policy.test.md` for baseline pack, fast-lane omission, and default durable reasoning
  - `specs/workflow-stage-autoprogression.test.md` for direct-`pr`, readiness blockers, and isolated-stage behavior
- Use generated-output drift checks as executable proof that canonical `skills/` and generated `.codex/skills/` stay synchronized.
- Use repo-owned smoke validation through `bash scripts/ci.sh` to confirm the touched skill guidance does not break the standard verification path.
- Keep validator-side missing-pack inference out of scope for this feature; this test spec proves skill alignment, not a new metadata inference engine.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R1a`, `R2`, `R2a`, `R2b` | `T1` | manual | Shared workflow skill and governing contract split |
| `R3`, `R3a`, `R3b`, `R9` | `T1` | manual | `implement` guidance and compatibility with the approved docs-changes policy |
| `R4`, `R4a`, `R5`, `R5a`, `R6`, `R6a`, `R9` | `T2` | manual | `verify`, `pr`, and `explain-change` blocker/readiness behavior |
| `R7` | `T3` | integration | Canonical/generated skill synchronization |
| `R8`, `R9` | `T1`, `T2`, `T4` | manual, smoke | Non-goal protection and repo-wide proof |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1` | Ordinary non-trivial implementation creates or updates the baseline pack |
| `E2` | `T1` | Fast-lane omission remains unchanged |
| `E3` | `T2` | `verify` blocks when the required baseline pack is missing |
| `E4` | `T2` | `pr` treats the missing baseline pack as a readiness blocker |
| `E5` | `T2` | `explain-change` aligns with the default change-local durable reasoning surface |

## Edge case coverage

- Edge case 1: fast-lane work must not accidentally gain a universal docs-changes requirement: `T1`
- Edge case 2: standalone `review-resolution.md` and `verify-report.md` remain conditional rather than universal: `T1`
- Edge case 3: `verify` must not silently accept a missing baseline pack for ordinary non-trivial work: `T2`
- Edge case 4: direct `pr` still opens when readiness passes, but missing baseline docs-changes artifacts block readiness: `T2`
- Edge case 5: PR text alone is not enough to satisfy durable reasoning for new ordinary non-trivial work: `T2`
- Edge case 6: generated `.codex/skills/` output must remain synchronized after canonical edits: `T3`
- Edge case 7: repo-owned smoke validation must still pass after the skill updates: `T4`

## Test cases

### T1. Workflow and implement skills require the baseline pack only for ordinary non-trivial work

- Covers: `R1`, `R1a`, `R2`, `R2a`, `R2b`, `R3`, `R3a`, `R3b`, `R8`, `R9`, `E1`, `E2`
- Level: manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `specs/docs-changes-usage-policy.test.md`
  - `specs/docs-changes-usage-policy.md`
  - `docs/workflows.md`
- Steps:
  - Review the touched workflow and implement skills against the approved docs-changes policy.
  - Confirm ordinary non-trivial work carries the baseline change-local pack.
  - Confirm approved fast-lane work remains exempt where the governing workflow contract allows omission.
  - Confirm the touched skills keep `review-resolution.md` and `verify-report.md` conditional.
  - Review and update `specs/docs-changes-usage-policy.test.md` where its existing proof cases for fast-lane omission, required `change.yaml`, and default durable reasoning surface would otherwise drift.
- Expected result:
  - The entrypoint and implementation skills operationalize the approved baseline pack without broadening fast-lane behavior or turning conditional artifacts into universal requirements.
- Failure proves:
  - Contributors could still omit the baseline pack for ordinary non-trivial work or misread fast-lane and conditional-artifact boundaries.
- Automation location:
  - Manual review during M1.

### T2. Verify, explain-change, and PR skills make missing baseline packs visible as blockers

- Covers: `R4`, `R4a`, `R5`, `R5a`, `R6`, `R6a`, `R8`, `R9`, `E3`, `E4`, `E5`
- Level: manual
- Fixture/setup:
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `specs/docs-changes-usage-policy.md`
- Steps:
  - Review the touched downstream gate skills against the approved docs-changes policy and workflow-stage autoprogression rules.
  - Confirm `verify` treats a missing required baseline pack as a blocker for ordinary non-trivial work.
  - Confirm `pr` includes required docs-changes artifacts in readiness and still opens directly when readiness passes.
  - Confirm `explain-change` aligns with `docs/changes/<change-id>/explain-change.md` as the default durable reasoning surface for new ordinary non-trivial work and does not imply PR text alone is enough.
  - Review and update `specs/workflow-stage-autoprogression.test.md` where its existing proof cases for direct-`pr`, readiness blockers, and isolated-stage behavior would otherwise drift.
- Expected result:
  - The downstream stage-local skills now surface missing required baseline packs as blockers and use the approved durable reasoning default consistently.
- Failure proves:
  - Ordinary non-trivial work could still reach `verify` or `pr` without the required baseline pack, or `explain-change` could drift from the approved durable reasoning surface.
- Automation location:
  - Manual review during M2.

### T3. Canonical and generated skills remain synchronized

- Covers: `R7`
- Level: integration
- Fixture/setup:
  - touched canonical `skills/`
  - generated `.codex/skills/`
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
- Expected result:
  - Canonical skills are valid and generated compatibility output stays synchronized with the canonical edits.
- Failure proves:
  - The skill updates changed canonical guidance without validating or regenerating the derived distribution surface.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`

### T4. Repo-owned smoke validation still passes after the skill alignment

- Covers: `R8`, `R9`
- Level: smoke
- Fixture/setup:
  - touched canonical skills
  - generated `.codex/skills/`
  - `docs/workflows.md` if touched
  - repo-owned validation wrapper
- Steps:
  - Run `bash scripts/ci.sh` after the skill changes land.
  - Confirm the standard repo-owned validation path still passes.
  - Confirm any touched summary surface remains truthful after the canonical skill edits.
- Expected result:
  - The repository's standard smoke validation remains green and no directly related summary surface still teaches the old behavior.
- Failure proves:
  - The skill-alignment change broke the normal validation path or left related guidance surfaces stale.
- Automation location:
  - `bash scripts/ci.sh`

## Fixtures and data

- Real repository guidance surfaces:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `docs/workflows.md`
- Real governing proof surfaces:
  - `specs/docs-changes-usage-policy.test.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `specs/rigorloop-workflow.md`
  - `specs/docs-changes-usage-policy.md`
- Repo-owned validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `bash scripts/ci.sh`

## Mocking/stubbing policy

- No mocking is required for this feature.
- Use real repository files and the repo-owned validation scripts rather than synthetic adapters.
- If a later follow-up adds executable missing-pack inference, that should define its own fixture strategy separately.

## Migration or compatibility tests

- Confirm fast-lane omission remains unchanged.
- Confirm legacy approved top-level `docs/explain/*.md` compatibility is not reopened or narrowed by the stage-local skill wording.
- Confirm the feature stays stacked cleanly on the docs-changes usage-policy branch until that base change merges or is restacked.

## Observability verification

- Reviewers should be able to inspect the touched skills and see when missing baseline packs block `verify` or `pr`.
- Generated-skill drift checks should surface canonical/generated mismatches explicitly.
- Any touched summary wording should make the updated docs-changes rule discoverable without reading chat history.

## Security/privacy verification

- Confirm the touched skills do not encourage putting secrets, credentials, or sensitive runtime data into `change.yaml`, `explain-change.md`, `review-resolution.md`, or `verify-report.md`.
- Confirm the skills do not imply that private chat can replace tracked durable reasoning for ordinary non-trivial work.

## Performance checks

- No dedicated performance test is required.
- Smoke validation should remain lightweight and file-based through the existing repo-owned scripts.

## Manual QA checklist

- Inspect the touched stage-local skills together and confirm they tell one coherent docs-changes story.
- Inspect `specs/docs-changes-usage-policy.test.md` and `specs/workflow-stage-autoprogression.test.md` after updates and confirm they still own the existing proof cases they were designed to cover.
- Confirm any touched summary surface does not overstate validator behavior beyond what the repository actually enforces today.

## What not to test

- Do not add new validator behavior that infers missing baseline packs when no `change.yaml` exists; that is out of scope for this feature.
- Do not retest the full docs-changes packaging contract exhaustively here; rely on `specs/docs-changes-usage-policy.test.md` where it already owns that proof.
- Do not introduce a new architecture-proof layer for this small skill-alignment change.

## Uncovered gaps

- The repository still lacks executable validator-side inference for missing required baseline packs when no `change.yaml` exists. This remains a separate possible follow-up and is not a blocker for this skill-alignment slice.

## Next artifacts

- `pr`

## Follow-on artifacts

- None yet

## Readiness

- This test spec remains the relied-on proof surface after final verification and explanation.
- The next stage is `pr`.
