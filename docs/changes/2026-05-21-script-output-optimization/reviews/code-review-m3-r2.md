# Code Review M3 R2

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M3 resolution for `SRO-M3-CR1` at commit `a16ddb9`
Status: clean-with-notes

## Review inputs

- Review surface: commit `a16ddb9` (`M3: resolve output contract validation routing`).
- Governing artifacts: `specs/script-output-optimization.md`, `specs/script-output-optimization.test.md`, and M3 in `docs/plans/2026-05-21-script-output-optimization.md`.
- Resolution evidence: `scripts/test-select-validation.py`, `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`, `selected-tests-m3.txt`, `output-contract-red-test.md`, `review-resolution.md`, and `change.yaml`.
- Validation evidence recorded for `SRO-M3-CR1`: ordinary validation, focused output-contract command, selected-test hash proof, lifecycle validation, review-artifact validation, change metadata validation, diff check, selector inspection, and selected CI.

## Diff summary

The M3 resolution removes the `load_tests` filter that excluded `ScriptOutputContractTests` from ordinary discovery after the formatter was implemented. Ordinary `python scripts/test-select-validation.py` validation now runs `73` tests, including the `10` output-contract acceptance tests. The explicit `ScriptOutputContractTests` command remains available as a focused diagnostic rerun. Evidence artifacts now record the updated ordinary selected-test list and SHA-256 hash.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. R32 and R35 require the presentation change to preserve validation behavior and output-shape coverage; ordinary validation now includes the required output-contract cases.
- Test coverage: pass. `python scripts/test-select-validation.py` now exercises `ScriptOutputContractTests` by default, and `python scripts/test-select-validation.py ScriptOutputContractTests` remains a focused rerun.
- Edge cases: pass. Recorded validation directly covers quiet success, conflicting flags, JSON deferral, zero-test failure, quiet failure evidence, unreliable rerun omission, and reliable rerun output.
- Error handling: pass. The resolution does not change formatter semantics; recorded validation still proves conflicting flags, zero tests, unsupported `--json`, and loader failure behavior.
- Architecture boundaries: pass. The change stays within `scripts/test-select-validation.py` and change-local evidence. `scripts/ci.sh` remains untouched for the conditional M4 decision.
- Compatibility: pass. The explicit output-contract command remains available while ordinary validation now covers the post-M3 acceptance contract.
- Security/privacy: pass. No new secrets, environment dumps, or sensitive output are introduced.
- Derived artifact currency: pass. No generated artifacts changed.
- Unrelated changes: pass. The diff is scoped to the M3 review finding resolution, evidence, and lifecycle state.
- Validation evidence: pass. The plan and change metadata record ordinary validation with `73` tests, focused output-contract validation, selected-test hash `sha256:878bd8dfce24e987ee50ab36d686f54e8d821bf4a5b11fe831d381c57d164047`, lifecycle validation, metadata validation, review-artifact validation, diff check, selector inspection with manual routing for unsupported evidence files, and selected CI.

## No-finding rationale

`SRO-M3-CR1` required ordinary post-M3 validation to execute the required output-contract acceptance cases or an equivalent guard. Removing the `load_tests` exclusion makes those cases part of default discovery, and the updated selected-test evidence records `73` ordinary tests including all `10` `ScriptOutputContractTests`. The default selected CI path runs `selector.regression`, which now includes those acceptance tests.

## Residual risks

M4 and M5 remain open. This review closes M3 only and does not decide whether `scripts/ci.sh` needs a no-code closeout or patch, does not perform final verification, and does not claim branch or PR readiness.

## Handoff

Reviewed milestone: M3. Test-select-validation output shaping
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M4 conditional CI wrapper preservation
Remaining implementation milestones: M4 when triggered, M5
Verify readiness: not-claimed
