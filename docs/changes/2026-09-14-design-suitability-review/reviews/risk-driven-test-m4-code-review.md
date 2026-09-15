# Risk-driven test redesign M4 Code Review

## Initial result

- Skill: code-review.
- Review status: approved; no material findings.
- Scope: seven-file M4 diff against `/tmp/risk-driven-m4-before`; earlier dirty changes excluded.
- Recording status: recorded, advisory-durable/manual.
- Nonauthor reviewer: `/root/validation_design_review`; author: `/root`.
- Artifacts edited by reviewer: this review only.
- Next stage: distinct final whole-change Code Review, then root-owned scoped Verify.

## Source assessment

The original aggregate retains its public TestCase, normal/custom runner and script-output checks. Contract, Git and CLI cases become non-TestCase mixins and setup becomes a plain helper mixin, preserving method selection and avoiding duplicate test registration. Four exact new module paths select existing Selector/Executor protection; the independently specified expected check set rejects accidental coverage loss without introducing a catch-all directory policy.

Reviewer independently compared method ASTs across the baseline and split modules. No original function is lost; EXPECTED_CATALOG is identical, including command arguments. Apart from the declared rendezvous changes, differences are the explicit aggregate-source path required after relocation and four duplicate assertion removals. For each of those four methods, reviewer confirmed exactly one expression removed and the set of expressions unchanged: the duplicate's assertion remains. No tested boundary is removed by those deletions.

The synthetic two-case execution fixture now uses per-invocation marker rendezvous, enabled only when the allocated budget permits two workers. Normal/sequential execution disables the gate. Existing discovered/started/completed identity and actual receipt interval assertions remain, and focused execution reports sequential non-overlap and concurrent overlap for the same two IDs. Markers belong to one owned test scenario; no cross-test mutable state is introduced.

Counter-script scenarios use an exclusive lock to record active processes and maximum observed overlap. Relevant concurrent callers request their allocated overlap and wait for that actual observation. Other serial/barrier cases preserve their delay. A deadline bounds a broken handshake; successful termination still requires existing cap, output and return-status assertions. The separate real bounded-worker overlap test remains unchanged. A cached synthetic peak does not prove unrelated invocations: each scenario uses its own isolated directory. No scheduler implementation or new timing threshold is introduced.

The split keeps the existing independently authored catalog oracle and uses actual Git/public command observations where claimed. Exact source inspection checks point back to the aggregate file rather than silently inspecting the new mixin file. Owned setup, copied workspaces, environment use and cleanup remain the original helpers, except the bounded handshake change above.

Full direct suites and combined selected execution remain pending. Focused output-contract and rendezvous results are promising but cannot substitute for complete consumer/discovery proof. No implementation edit or approval of later work is made by this first assessment.

## Exact subjects

Seven implementation paths and the approved Design/plan dependencies were inspected through CLI subject inspection.

| Subject | SHA-256 identity |
| --- | --- |
| `tests/engineering/validation/test-select-validation.py` | `sha256:bdffcfb1966d0952d9536763e913886270233ec631cd9a2c4c249240e547f11e` |
| `tests/engineering/validation/test-validation-execution.py` | `sha256:b3bfb43b260bdb22ed6ec01a44259f0adf963b4da85a94f36fb425f8e0c6eb24` |
| `scripts/lib/validation/validation_selection.py` | `sha256:e0239dc403a6a9f0ea0a2905c8268ebf0d015bd5767cbb7961ed35e5bd883c21` |
| `tests/engineering/validation/selection_contract_tests.py` | `sha256:b55487e8d28dd38374029f8b86c4a2017e81373ff84aa8d5f8e0f89bc606dcdd` |
| `tests/engineering/validation/selection_git_tests.py` | `sha256:8fb30b8fc9e969389dc5a8c37a3831dd925a54a8720836562aa6ed1114267b10` |
| `tests/engineering/validation/selection_cli_tests.py` | `sha256:585e25286619503f1e13c8d40516823f060bd16659e894fb98b3739c5ba6e56b` |
| `tests/engineering/validation/selection_test_helpers.py` | `sha256:4abe103954d342dd7436f6cde797d6cb882418fada02a1ac941f76199d3a16b7` |
| `docs/plans/2026-09-15-risk-driven-test-redesign.md` | `sha256:687849e708b45cdf80e42ca3f12d7dbf168a64fd47a695bdffdb8dddc7a938e5` |
| `docs/design/engineering/validation.md` | `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14` |

## Final M4 judgment

Approved on the recorded current subjects, all rechecked unchanged. Direct Selector passed 184 cases in 123.12 seconds; direct Executor passed 52 in 66.205 seconds. Focused output-contract eleven cases, two executor rendezvous cases and five counter scenarios passed. Reviewer independently confirmed selector discovery 183→184 and executor 52→52 with no removed baseline ID.

Final local selected execution exited 0 with all 1,296 result rows passed and boundary scope passed. Reviewer inspected the log and found no failed, unstarted or cancelled row. Actual local and explicit whole-redesign path-union selections both report ok, without unclassified inputs or blockers. Existing local selection also includes earlier dirty surfaces; their execution is not approval of unrelated engineering. This establishes complete current consumers and M4 integration alongside the direct full suites.

All ten checklist criteria pass for M4: Design alignment through bounded groups; preserved detection and discovery; real sequential/concurrent observations; truthful error/cleanup behavior; unchanged executor ownership; stable aggregate/case compatibility; owned temporary state and no expanded authority; actual affected product consumers in final execution; baseline-isolated scope; and complete current evidence. No material concern was found and no correction is required.

Durable commands/counts and source applicability are in `../contract-refinement.md`; detailed logs include `/tmp/risk-driven-m4-selector.log`, `/tmp/risk-driven-m4-executor.log`, `/tmp/risk-driven-m4-rendezvous.log`, `/tmp/risk-driven-m4-counter-rendezvous.log` and `/tmp/risk-driven-final-ci.log`. This milestone approval does not substitute for the separately requested fresh whole-change review or distinct Verify and asserts no performance improvement, hosted CI or branch-wide readiness.
