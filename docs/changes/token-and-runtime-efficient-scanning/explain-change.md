# Token and Runtime Efficient Scanning Explain Change

## Summary

M1 adds the bounded extraction guidance required by the approved token and runtime efficient scanning spec. It updates contributor workflow guidance, aligns every first-slice scan-sensitive canonical skill with summary and stable-ID first reasoning, regenerates derived skill surfaces, and records this change-local proof pack.

## Decision trail

- Proposal: `docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md`
- Spec: `specs/token-and-runtime-efficient-scanning.md`
- Test spec: `specs/token-and-runtime-efficient-scanning.test.md`
- Plan: `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`
- Milestone: M1, add bounded extraction and skill guidance
- Requirements covered in this milestone: `R1`-`R6`, `R10`-`R15`, `R34`-`R36`

## Diff rationale by area

| Area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `docs/workflows.md` | Adds bounded extraction, normal output budgets, verbose expansion, and full-file read escalation guidance. | Satisfies `R1`-`R4`, `R10`-`R15`, and `R34` for contributor-visible workflow guidance. | `T1`, `python scripts/test-skill-validator.py` |
| `skills/` | Adds concise summary and stable-ID first evidence guidance plus full-file read rules to the 19 scan-sensitive canonical skills. | Satisfies `R5`, `R6`, and `R35` without changing stage order or skill trigger behavior. | `T2`, `python scripts/test-skill-validator.py` |
| `.codex/skills/` | Regenerated from canonical `skills/`. | Keeps the local Codex runtime mirror derived instead of hand-edited. | `python scripts/build-skills.py`, `python scripts/build-skills.py --check` |
| `dist/adapters/` | Regenerated from canonical skills and adapter templates. | Keeps public adapter packages aligned after canonical skill wording changed. | `python scripts/build-adapters.py --version 0.1.1`, `python scripts/build-adapters.py --version 0.1.1 --check` |
| `scripts/test-skill-validator.py` | Adds focused M1 contract tests. | Proves workflow and first-slice skill guidance carry the required efficiency rules. | Initial failing run, then passing targeted test |

## Aligned-surface audit

| Surface | Decision | Rationale |
| --- | --- | --- |
| `AGENTS.md` | unaffected with rationale | It already points to `CONSTITUTION.md`, specs, active plans, and workflow docs; M1 updates those lower-level workflow surfaces without changing repository instruction precedence. |
| `CONSTITUTION.md` | unaffected with rationale | M1 changes operational evidence-collection guidance, not the repository's source-of-truth order, lifecycle policy, or governing principles. |
| `specs/rigorloop-workflow.md` | unaffected with rationale | The approved M1 scope names contributor workflow guidance and scan-sensitive skills; durable workflow-spec changes are not required for this first milestone. |
| `scripts/build-adapters.py` and adapter drift logic | unaffected with rationale | Output shaping, verbose mode, and failure taxonomy are owned by M2 and M3, not M1. |

## Tests added or changed

- `scripts/test-skill-validator.py`
  - `test_workflow_guidance_defines_bounded_extraction_and_output_budgets`
  - `test_scan_sensitive_skills_include_summary_id_reasoning_and_full_file_rules`

## Validation evidence

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py`
- `python scripts/build-adapters.py --version 0.1.1`
- `python scripts/test-select-validation.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/validate-change-metadata.py docs/changes/token-and-runtime-efficient-scanning/change.yaml`
- `python scripts/select-validation.py --mode explicit` with the M1 authored path set selected `skills.validate`, `skills.regression`, `skills.drift`, `adapters.drift`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, and `selector.regression`; broad smoke was not required.
- `bash scripts/ci.sh --mode explicit` with the same M1 authored path set executed the selected checks successfully.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/token-and-runtime-efficient-scanning/change.yaml --path docs/changes/token-and-runtime-efficient-scanning/explain-change.md --path docs/plan.md --path docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md --path docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.md --path specs/token-and-runtime-efficient-scanning.test.md`
- `git diff --check -- .`

Additional validation results are recorded in the active plan.

## Scope control

- M1 does not change adapter drift output, `--verbose` support, failure taxonomy, manifest-first collection, selected check coverage, or command exit behavior.
- Generated `.codex/skills/` and `dist/adapters/` were produced through existing generator commands.
- No new external dependency, parser boundary, persistent cache, or hosted CI behavior change is introduced.

## Readiness

M1 is complete and ready for `code-review` as a reviewable milestone slice. M2-M4 remain open for the full initiative.
