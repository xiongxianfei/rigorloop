# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1. Output-layer audit and baseline identity proof in working tree
Status: clean-with-notes

## Review inputs

- Review surface: M1 working-tree diff for `script-output-layer-audit.md`, `behavior-preservation.md`, `broad-smoke-child-commands-baseline.txt`, `change-metadata-validator-tests-baseline.txt`, the active plan, plan index, and change metadata.
- Governing artifacts: `specs/script-output-optimization.md` R36 through R38, R49 through R50, R53, R60 through R62, R64 through R65; `specs/script-output-optimization.test.md` TSRO-015, TSRO-016, TSRO-023, TSRO-024, and TSRO-026; M1 in `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`.
- Validation evidence: M1 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml` and the active plan, including broad-smoke, producer default, producer quiet compatibility, lifecycle, metadata, hash, selected explicit, and patch hygiene checks.
- Related code inspected: current `scripts/ci.sh` broad-smoke `run_check` and `run_broad_smoke` structure to compare the normalized command list with the current wrapper path.

## Diff summary

M1 adds the change-local output-layer audit, behavior-preservation baseline, normalized broad-smoke child-command identity list, and ordered `scripts/test-change-metadata-validator.py` selected-test identity list. The active plan, plan index, and change metadata are updated to record M1 implementation and validation evidence. No production script, selector, generated artifact, skill, adapter, JSON behavior, or validation selection code changes in M1.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. The audit satisfies R36 through R38 by recording producers, direct-run success/failure shape, orchestrators, capture policy, high-use status, and first-slice treatment, with selected-CI and broad-smoke split into separate paths.
- Test coverage/proof: pass. TSRO-015, TSRO-016, TSRO-023, and TSRO-024 are covered by the audit, normalized broad-smoke command hash, selected-test hash, and quiet compatibility proof.
- Edge cases: pass. Existing `--quiet` and `-q` compatibility is recorded as accepted unittest behavior, and the audit assigns broad-smoke compaction to wrapper capture rather than producer quiet flags.
- Error handling: pass. M1 does not alter runtime error handling; failure-evidence and fail-exit proof remain explicitly pending for M2/M3 where the behavior changes happen.
- Architecture boundaries: pass. The milestone records evidence only and does not introduce new helper architecture or broaden into generated outputs.
- Compatibility: pass. `scripts/test-change-metadata-validator.py` remains the first targeted producer, and quiet compatibility is preserved as a baseline contract.
- Security/privacy: pass. The artifacts record command identities, hashes, and validation summaries only; no secrets or sensitive runtime dumps were observed.
- Derived artifact currency: pass. No generated skills, adapters, or release outputs changed in M1.
- Unrelated changes: pass. The reviewed M1 diff is scoped to the approved lifecycle and evidence surfaces for this change.
- Validation evidence: pass. The recorded commands include exact broad-smoke after intent-to-add made new lifecycle artifacts visible to dirty-worktree selection, direct producer default and quiet checks, lifecycle/metadata validation, hash verification, selected explicit validation for supported artifacts, and manual patch-hygiene routing for unsupported change-local evidence files.

## No-finding rationale

The approved M1 milestone is evidence-first: it must enumerate the printing layers and record stable identity baselines before output changes. The audit names the structural broad-smoke gap, keeps selected-CI and broad-smoke distinct, locks `scripts/test-change-metadata-validator.py` as the first producer, and records quiet compatibility without taking on custom quiet formatting. The two baseline files provide ordered, hashable proof surfaces for the broad-smoke child commands and producer selected tests, avoiding the prior count-only proof failure pattern.

## Residual risks

M2 still must prove the broad-smoke command list remains unchanged after capture and must add failure/verbose output proof. M3 still must prove producer selected-test identity, default compact output, failure output, verbose detail, and quiet compatibility after producer formatting. This review closes M1 only and does not claim final verification, branch readiness, or PR readiness.

## Handoff

Reviewed milestone: M1. Output-layer audit and baseline identity proof
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M2. Broad-smoke capture and wrapper-mode consistency guard
Remaining implementation milestones: M2, M3, M4
Verify readiness: not-claimed
