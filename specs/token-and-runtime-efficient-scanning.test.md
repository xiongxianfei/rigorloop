# Token and Runtime Efficient Scanning Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/token-and-runtime-efficient-scanning.md`
- Plan: `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`
- Proposal: `docs/proposals/2026-04-27-token-and-runtime-efficient-scanning.md`
- Architecture: not required for this first slice; helper behavior remains in-process, adapter-family scoped, dependency-free, and non-persistent.
- Spec-review findings: approved on 2026-04-28 after failure taxonomy and lifecycle-readiness corrections.
- Plan-review findings: approved after validation command type and manifest-error milestone-boundary revisions.

## Testing strategy

- Contract tests inspect `docs/workflows.md` and the first-slice canonical `skills/*/SKILL.md` files to prove bounded extraction, stable ID reasoning, output budgets, verbose escape hatches, and full-file-read escalation guidance are present without expanding workflow order.
- Skill and adapter sync tests use existing skill validation, skill regression, generated skill drift, adapter drift, and adapter validation commands after canonical skill edits.
- Unit tests in `scripts/test-adapter-distribution.py` exercise structured adapter drift entries, failure categories, output formatting, output budgets, manifest parsing, manifest-first helper behavior, and no-persistent-cache boundaries.
- Integration tests run the `scripts/build-adapters.py` CLI and selected validation wrapper paths to prove normal and verbose output, exit-code compatibility, check identity, and CI wrapper behavior.
- Selector tests use `scripts/test-select-validation.py` to prove supported selected checks are stable and that `scripts/test-adapter-distribution.py` remains an expected manual-routing path when selector v1 reports it as unsupported.
- Smoke and release checks remain repository-owned pass gates from the approved plan; they are not substitutes for targeted unit and integration tests.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R4`, `R34` | `T1`, `T2`, `T16` | Workflow guidance plus skill escalation guidance and final contract validation. |
| `R5`-`R6`, `R35` | `T2`, `T16` | Every first-slice scan-sensitive skill gets summary or stable ID reasoning plus full-file-read guidance. |
| `R7` | `T4`, `T5`, `T6`, `T8` | Normal output is summary-first, failure-focused, diff-focused, and verbose-expandable. |
| `R8`-`R13` | `T1`, `T5`, `T8`, `T9` | Output budget targets, hard warning thresholds, excerpt limits, multi-file summaries, and default omissions. |
| `R14`, `R20` | `T7`, `T14`, `T16` | Output shaping must not alter validation semantics, selected coverage, or exit behavior. |
| `R15` | `T5`, `T8` | Omitted detail and over-budget output name the verbose expansion path. |
| `R16`-`R18` | `T4`, `T6`, `T14` | First output-shaped command, verbose form, and clean success behavior. |
| `R19`, `R19a`-`R19c` | `T5`, `T10` | Generated-output and canonical-source failures are collected and classified before manifest-error work. |
| `R19d` | `T12` | Manifest failure entries are classified as `manifest-error`. |
| `R21` | `T4` | Clean normal output includes check ID, version, output root, and concise success status. |
| `R22` | `T5`, `T12` | Failure normal output includes check ID, version, output root, category counts, displayed paths, detail, and verbose rerun instruction. |
| `R23` | `T5`, `T8` | Normal drift output avoids listing every entry beyond budget. |
| `R24`-`R25` | `T6`, `T12` | Verbose output includes every collected entry and is deterministic. |
| `R26` | `T9` | Tests or verification evidence record before-and-after output line or byte counts. |
| `R27`-`R29` | `T11`, `T12` | Manifest-first inventory precedes filesystem confirmation without making the manifest authoritative. |
| `R30`-`R33` | `T13` | Shared helpers are optional, in-process, adapter-family scoped, and no persistent cache is introduced. |
| `R36` | `T3`, `T16` | Generated `.codex/skills/` and public adapters are refreshed only through existing commands. |
| `R37` | `T13`, `T15`, `T16` | No new external dependency for output shaping, manifest-first scanning, or bounded extraction guidance. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T4` | Clean adapter drift check stays concise. |
| `E2` | `T5`, `T8` | Many drift failures are summarized before details and provide verbose expansion. |
| `E3` | `T6` | Verbose adapter drift output exposes complete deterministic detail. |
| `E4` | `T11`, `T12` | Manifest inventory is read before filesystem confirmation. |
| `E5` | `T1`, `T2` | Guidance escalates from bounded extraction to full-file read when needed. |
| `E6` | `T2` | Scan-sensitive skills prefer stable IDs and state full-file-read conditions. |

## Edge case coverage

- EC1, clean generated adapter output: `T4`
- EC2, one stale generated adapter file: `T5`
- EC3, many missing/stale/unexpected files: `T5`, `T8`
- EC4, verbose output for many failures: `T6`
- EC5, malformed adapter manifest: `T12`
- EC6, package coverage uses manifest inventory: `T11`
- EC7, drift proof still checks filesystem: `T11`, `T12`
- EC8, targeted search requires broader context: `T1`, `T2`
- EC9, whole artifact is review target: `T1`, `T2`
- EC10, unavoidable over-budget normal output warns: `T8`
- EC11, `scripts/ci.sh` wrapper preserves pass/fail status: `T7`
- EC12, canonical skill guidance changes regenerate derived outputs: `T3`, `T16`
- EC13, invalid canonical source reports `canonical-source-error`: `T10`
- EC14, manifest missing/malformed/inconsistent/mismatched reports `manifest-error`: `T12`

## Acceptance criteria coverage map

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T1`, `T16` | Workflow guidance documents bounded extraction, output budgets, verbose expansion, and full-file-read escalation. |
| `AC2` | `T2`, `T3`, `T16` | First-slice scan-sensitive canonical skills include stable ID reasoning and full-file-read escalation guidance, then generated outputs are synchronized. |
| `AC3` | `T4`, `T5`, `T7`, `T14` | Normal `build-adapters.py --check` output is shaped and preserves success and failure exit behavior. |
| `AC4` | `T6`, `T12` | Verbose adapter drift output exposes complete generated-output, canonical-source, and manifest diagnostics. |
| `AC5` | `T5`, `T9`, `T16` | Before-and-after line or byte counts are recorded for representative clean and drift cases. |
| `AC6` | `T11`, `T12` | Adapter generated-output inspection reads manifest evidence before filesystem confirmation. |
| `AC7` | `T5`, `T10`, `T12` | Concise failure output preserves check ID, affected path, category, and actionable detail. |
| `AC8` | `T6`, `T12` | Verbose output preserves complete diagnostic detail deterministically. |
| `AC9` | `T7`, `T14`, `T16` | Selected check coverage, CI wrapper behavior, and command exit behavior are unchanged. |
| `AC10` | `T10`, `T12` | Generated-output, canonical-source, and manifest failures are classified into the required taxonomy. |
| `AC11` | `T16` | Artifact lifecycle validation covers the proposal, spec, test spec, plan, and plan index. |

## Test cases

### T1. Workflow guidance defines bounded extraction and output budgets

- Covers: `R1`-`R4`, `R8`-`R15`, `R34`, `E5`, EC8, EC9, EC10
- Level: contract
- Fixture/setup:
  - `docs/workflows.md`
  - existing selector and workflow regression tests
- Steps:
  - Inspect workflow guidance for bounded extraction as the default first evidence-collection behavior for large files, repeated scans, generated output, and validation logs.
  - Assert guidance starts with inventories, headings, stable IDs, path lists, counts, or matching line numbers.
  - Assert guidance broadens from exact ranges to neighboring sections or full files only under the spec's full-file-read escalation conditions.
  - Assert guidance defines normal-mode budgets: routine output target 40 lines, hard warning threshold 80 lines, single excerpt target 12 lines, hard warning threshold 20 lines, and one summary line per file unless changed/failing/requested.
  - Assert guidance keeps verbose expansion available and does not treat budgets as validation failures.
- Expected result:
  - Contributors and agents have an authoritative bounded-extraction and output-budget workflow.
- Failure proves:
  - Repository guidance can still drive broad reads or noisy output by default.
- Automation location:
  - `python scripts/test-select-validation.py` or a focused workflow contract test added beside it

### T2. Scan-sensitive skills require stable ID reasoning and full-file-read escalation

- Covers: `R2`-`R6`, `R35`, `E5`, `E6`, EC8, EC9
- Level: contract
- Fixture/setup:
  - canonical `skills/architecture/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/bugfix/SKILL.md`
  - `skills/ci/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/project-map/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/research/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/test-spec/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/workflow/SKILL.md`
- Steps:
  - For every listed skill, assert guidance prefers check IDs, requirement IDs, file paths, counts, line citations, and concise summaries before raw excerpts.
  - Assert every listed skill includes explicit "when full-file read is required" guidance covering the spec's escalation conditions or a stage-specific equivalent.
  - Assert no listed skill says bounded extraction can replace a full contract review when the whole source-of-truth artifact is needed.
- Expected result:
  - All first-slice scan-sensitive skills carry consistent, stage-appropriate efficiency guidance.
- Failure proves:
  - A stage skill can still instruct broad raw reads or omit full-file-read escalation conditions.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`

### T3. Generated skill and adapter output stays derived

- Covers: `R36`, `R37`, EC12
- Level: integration, smoke
- Fixture/setup:
  - canonical skill changes from `T2`
  - generated `.codex/skills/`
  - generated `dist/adapters/`
- Steps:
  - Run skill validation and skill regression after canonical skill edits.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Assert no test or implementation requires hand-editing generated `.codex/skills/` or `dist/adapters/`.
- Expected result:
  - Generated surfaces are synchronized from canonical sources through existing repository commands.
- Failure proves:
  - Canonical skill guidance can drift from generated Codex mirrors or public adapters.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-adapter-distribution.py`
  - repository pass-gate commands named above

### T4. Clean adapter drift check has concise normal output

- Covers: `R7`, `R13`, `R16`, `R18`, `R20`, `R21`, `E1`, EC1, `AC3`
- Level: integration
- Fixture/setup:
  - repository generated adapters in sync for version `0.1.1`
  - temporary adapter output roots generated by `sync_adapter_output` where helper-level testing is needed
- Steps:
  - Run or invoke the check path for `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Assert return code is `0`.
  - Assert normal output includes check ID `adapters.drift`, requested version, generated adapter output root, and concise success status.
  - Assert normal output does not list unchanged generated files.
  - Assert output remains within routine normal-mode target.
- Expected result:
  - Clean checks are short, stable, and preserve success behavior.
- Failure proves:
  - Output shaping either changed success semantics or still emits noisy unchanged-file detail.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`

### T5. Normal drift output is categorized, actionable, and bounded

- Covers: `R7`-`R15`, `R16`, `R19`-`R19b`, `R20`, `R22`, `R23`, `E2`, EC2, EC3, EC10, `AC3`, `AC5`, `AC7`, generated-output portion of `AC10`
- Level: unit, integration
- Fixture/setup:
  - temporary adapter output root generated from fixture skills
  - one stale file fixture
  - many-drift fixture with missing, stale, and unexpected generated files
- Steps:
  - Create one stale generated file and collect drift.
  - Assert normal failure output includes `adapters.drift`, version, output root, category counts, category `stale`, affected path, and actionable detail.
  - Create many missing/stale/unexpected entries.
  - Assert normal output displays a bounded deterministic subset and does not print every failure when that would exceed the budget.
  - Assert omitted detail is counted or otherwise made clear and a `--verbose` rerun instruction appears.
  - Assert generated-output entries are classified as `missing`, `stale`, or `unexpected`.
- Expected result:
  - Normal failure output is useful first and concise by default.
- Failure proves:
  - Output shaping hides the actionable failure or still dumps unbounded drift lists.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T6. Verbose adapter drift output preserves complete deterministic detail

- Covers: `R17`, `R20`, `R24`, `R25`, `E3`, EC4, `AC4`, `AC8`
- Level: unit, integration
- Fixture/setup:
  - same many-drift fixture used by `T5`
  - generated-output and canonical-source drift entries
- Steps:
  - Run or invoke `python scripts/build-adapters.py --version <version> --check --verbose` against the fixture state.
  - Assert exit status matches normal check mode for the same state.
  - Assert verbose output includes every collected failure entry exactly once.
  - Run the same verbose invocation twice and assert deterministic ordering and content.
- Expected result:
  - Verbose output is a complete diagnostic escape hatch without changing pass/fail status.
- Failure proves:
  - Normal-mode omissions cannot be recovered reliably.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T7. Exit behavior and selected check coverage remain unchanged

- Covers: `R14`, `R18`-`R20`, `EC11`, `AC9`
- Level: integration
- Fixture/setup:
  - clean generated adapter state
  - drifted generated adapter state
  - invalid input or malformed canonical skill fixture
  - selector command catalog
- Steps:
  - Assert clean `--check` exits `0`.
  - Assert drift `--check` exits non-zero as before.
  - Assert invalid canonical source input still fails check mode.
  - Assert `scripts/validation_selection.py` still selects check ID `adapters.drift` with command `python scripts/build-adapters.py --version <adapter-version> --check`.
  - Run `scripts/ci.sh --mode explicit` for supported adapter paths or record the expected selector manual route for `scripts/test-adapter-distribution.py`.
- Expected result:
  - Output formatting does not alter selected coverage, wrapper pass/fail reporting, or command exit semantics.
- Failure proves:
  - A display-only change changed validation behavior.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/test-select-validation.py`

### T8. Output budget warnings are explicit when normal output exceeds thresholds

- Covers: `R8`-`R15`, `R22`, `R23`, EC10
- Level: unit
- Fixture/setup:
  - formatter-level fixture where every displayed failure is required for actionable diagnosis and normal output exceeds 80 lines
  - single-excerpt fixture exceeding 20 lines only if the implementation introduces excerpt rendering
- Steps:
  - Render normal output for an over-budget failure set.
  - Assert an over-budget warning is emitted.
  - Assert the warning does not change return code or validation result.
  - Assert the output names the verbose expansion path.
  - If a single excerpt is rendered, assert excerpts over 20 lines emit the single-excerpt warning.
- Expected result:
  - Normal output remains correctness-preserving when budget targets cannot be met.
- Failure proves:
  - Contributors cannot distinguish concise normal output from accidentally truncated diagnostics.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T9. Output-size evidence records before-and-after normal output size

- Covers: `R26`, `AC5`, observability, performance expectations
- Level: unit, manual
- Fixture/setup:
  - representative clean case
  - representative many-drift failure case
  - legacy one-line-per-entry baseline computed in the test or recorded in change-local evidence
- Steps:
  - Compute or record pre-change normal output line or byte count for the representative clean case.
  - Compute or record post-change normal output line or byte count for the same clean case.
  - Compute or record pre-change normal output line or byte count for representative drift output.
  - Compute or record post-change normal output line or byte count for the same drift state.
  - Store the evidence in assertions, plan validation notes, or change-local evidence.
- Expected result:
  - Reviewers can see that the first output-shaped script reduces or bounds normal output for representative cases.
- Failure proves:
  - Token reduction is asserted without measurable evidence.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - active plan validation notes or `docs/changes/token-and-runtime-efficient-scanning/explain-change.md`

### T10. Generated-output and canonical-source failures use structured categories

- Covers: `R19`, `R19a`-`R19c`, `R22`, `R24`, EC13, generated-output and canonical-source portions of `AC10`
- Level: unit, integration
- Fixture/setup:
  - missing generated file fixture
  - stale generated file fixture
  - unexpected generated file fixture
  - invalid canonical skill fixture such as `tests/fixtures/adapters/invalid-body/`
  - missing canonical skills root fixture
- Steps:
  - Collect adapter drift for each generated-output state.
  - Assert each entry has exactly one category: `missing`, `stale`, or `unexpected`.
  - Collect drift for invalid, incomplete, or unparsable canonical source input.
  - Assert each canonical-source failure entry is categorized as `canonical-source-error`.
  - Assert normal output includes affected path and actionable detail for displayed canonical-source failures.
  - Assert verbose output includes complete canonical-source failure entries.
- Expected result:
  - Non-manifest adapter drift entries are structured and category complete.
- Failure proves:
  - Failure output cannot support category counts or stable failure reasoning.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T11. Manifest-first inspection reads manifest inventory before filesystem confirmation

- Covers: `R27`-`R29`, `R31`, `R37`, `E4`, EC5, EC6, EC7, `AC6`
- Level: unit, integration
- Fixture/setup:
  - generated adapter output root with `manifest.yaml`
  - helper or spy fixture that can prove manifest read occurs before broad filesystem coverage traversal
  - filesystem states with missing, stale, and unexpected files
- Steps:
  - Invoke the adapter generated-output coverage or drift helper on an output root with a manifest.
  - Assert manifest inventory is parsed before filesystem confirmation.
  - Assert filesystem confirmation still detects missing, stale, unexpected, and drifted files.
  - Assert the manifest is not treated as authoritative over canonical skills, templates, and generator output.
- Expected result:
  - Manifest data is used as the first inventory but does not weaken drift correctness.
- Failure proves:
  - Generated-output scanning either ignores the manifest or trusts it too much.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T12. Manifest errors are classified and displayed completely

- Covers: `R19a`, `R19d`, `R22`, `R24`, `R25`, `R27`-`R29`, EC14, manifest-error portion of `AC10`
- Level: unit, integration
- Fixture/setup:
  - missing manifest fixture
  - malformed manifest fixture
  - inconsistent manifest fixture
  - version mismatch or generated-output contract mismatch fixture
- Steps:
  - Collect adapter drift or manifest-first coverage entries for each manifest failure state.
  - Assert every manifest failure entry is categorized as `manifest-error`.
  - Assert normal output includes `manifest-error`, affected manifest path, and actionable detail.
  - Assert verbose output includes complete manifest failure entries.
  - Assert canonical expected-file generation and filesystem confirmation still run where required for drift correctness.
- Expected result:
  - Manifest failures participate in the same failure taxonomy and complete-detail path as other adapter drift failures.
- Failure proves:
  - Manifest-first behavior lacks a reviewable failure category or hides manifest diagnostics.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T13. Parser helpers remain in-process and no persistent cache or dependency is added

- Covers: `R30`-`R33`, `R37`, performance expectations
- Level: unit, contract
- Fixture/setup:
  - `scripts/adapter_distribution.py`
  - temporary adapter output root
  - repository dependency metadata, if any
- Steps:
  - Inspect or test any shared parser helper introduced for the adapter drift family.
  - Assert helper state is scoped to one command invocation and discarded afterward.
  - Assert no persistent cache files, database files, or long-running index state are created in the repository or temp output root.
  - Assert no new external dependency is required to run output shaping or manifest-first scanning.
  - If no helper is introduced, record "not needed" in implementation evidence and assert no cache/dependency was added.
- Expected result:
  - The implementation keeps reuse lightweight and local to the selected script family.
- Failure proves:
  - The first slice exceeded the approved architecture and cache boundary.
- Automation location:
  - `python scripts/test-adapter-distribution.py`
  - artifact/code review checklist

### T14. CLI error and compatibility behavior stays clear

- Covers: `R14`, `R17`, `R20`, compatibility and error behavior
- Level: integration
- Fixture/setup:
  - `scripts/build-adapters.py`
  - normal repository environment
- Steps:
  - Run existing `python scripts/build-adapters.py --version 0.1.1 --check` and assert it remains valid.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check --verbose` and assert it is accepted.
  - Run `python scripts/build-adapters.py --version 0.1.1 --verbose` without `--check` and assert it fails non-zero with a clear message, or document the implemented no-op behavior only if the CLI explicitly supports it.
  - Run invalid arguments and assert argparse-style non-zero failure remains clear.
- Expected result:
  - New verbose support is backward-compatible and invalid command forms remain clear.
- Failure proves:
  - CLI compatibility or error reporting regressed while shaping output.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T15. Output shaping does not expose secrets or outside-repository data

- Covers: `R37`, security/privacy expectations
- Level: unit, integration
- Fixture/setup:
  - temporary adapter output roots under repository-owned or test temporary directories
  - environment variables containing sentinel values that must not appear in output
- Steps:
  - Run normal and verbose adapter drift output with sentinel environment values present.
  - Assert output includes only inspected repository or fixture paths and deterministic failure details.
  - Assert output does not include environment variable values, credentials, tokens, private keys, or unrelated machine-local debug paths.
- Expected result:
  - Concise and verbose output stay within the command's existing inspected data scope.
- Failure proves:
  - Output shaping introduced a privacy leak.
- Automation location:
  - `python scripts/test-adapter-distribution.py`

### T16. Final validation gates prove lifecycle and generated-output alignment

- Covers: `R14`, `R20`, `R25`, `R34`-`R37`, EC11, EC12, `AC1`-`AC11`
- Level: smoke, contract, manual-routing proof
- Fixture/setup:
  - completed implementation for M1-M4
  - active plan and this test spec
- Steps:
  - Run `python scripts/select-validation.py --mode explicit` with the concrete changed paths from the plan.
  - Confirm any `scripts/test-adapter-distribution.py` selector block is the expected manual route and run `python scripts/test-adapter-distribution.py` directly.
  - Run `bash scripts/ci.sh --mode explicit` for supported selected paths where the selector produces no manual-routing block.
  - Run all pass-gate commands named by M4.
  - Run `bash scripts/ci.sh --mode broad-smoke` before final PR readiness.
  - Run artifact lifecycle validation for the proposal, spec, this test spec, plan, and plan index.
- Expected result:
  - Repository-owned proof confirms generated outputs, selectors, lifecycle artifacts, release metadata, and broad smoke are aligned.
- Failure proves:
  - The completed slice is not ready for code-review, verify, or PR handoff.
- Automation location:
  - commands named in `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`

## Fixtures and data

- Existing adapter fixture skills under `tests/fixtures/adapters/`, including `portable-basic`, `transformable-frontmatter`, `invalid-body`, `invalid-description`, and `invalid-name`.
- Temporary adapter output roots generated with `sync_adapter_output`.
- Drift fixtures created inside tests by deleting expected files, editing generated files, and adding unexpected files.
- Manifest fixtures created inside tests by deleting `manifest.yaml`, writing malformed YAML, changing manifest version, removing expected manifest entries, or adding inconsistent entries.
- Output-size fixtures should use deterministic generated failure sets so line and byte counts do not depend on filesystem ordering.
- No committed fixture should contain secrets, machine-local absolute paths, or tool-specific local state.

## Mocking/stubbing policy

- Prefer real temporary filesystem fixtures and existing adapter generators over mocks for drift, manifest, and CLI behavior.
- Formatter-only unit tests may construct structured drift entries directly when filesystem setup would obscure the output contract being tested.
- Selector behavior should be tested through `scripts/test-select-validation.py`; do not mock selector output for final proof.
- Do not mock `scripts/build-adapters.py` exit codes in integration tests that assert compatibility.

## Migration or compatibility tests

- Existing `python scripts/build-adapters.py --version <version> --check` invocations remain valid and keep success/failure exit behavior: `T4`, `T7`, `T14`.
- Existing selector check ID `adapters.drift` and command template remain stable: `T7`, `T16`.
- CI wrapper behavior does not misreport child command status: `T7`, `T16`.
- Contributors do not need new external tools or dependencies: `T13`, `T16`.
- Rollback by restoring prior output formatting while preserving drift detection remains possible and reviewable through `T7`, `T10`, `T11`, and `T12`.

## Observability verification

- Normal output exposes check ID, status, version, output root, affected scope, and category counts: `T4`, `T5`, `T12`.
- Over-budget output reports the warning and verbose expansion path: `T8`.
- Output-size evidence records line or byte counts before and after shaping: `T9`.
- Change-local artifacts, plan validation notes, and final PR text must cite stable requirement IDs and command names rather than pasting large logs: `T9`, `T16`.

## Security/privacy verification

- No test should require network access, hosted CI, credentials, or installed Codex, Claude Code, or opencode tools.
- Normal and verbose output must not expose secrets, tokens, private keys, environment values, or unrelated machine-local debug paths: `T15`.
- Verbose output must stay limited to repository or temporary fixture paths already inspected by the command: `T15`.
- Bounded extraction guidance must not summarize away security-sensitive actionable failure details: `T1`, `T2`, `T5`.

## Performance checks

- Output-size reduction is measured through line or byte counts for representative clean and drift cases: `T9`.
- The first output-shaped script should derive normal and verbose output from the same collected drift result where practical: `T6`, `T13`.
- Manifest-first behavior should avoid unnecessary filesystem traversal for inventory-only coverage when the manifest is sufficient, while still confirming filesystem state for drift proof: `T11`.
- Runtime timing is not required for this first slice unless implementation changes a script with a measured runtime concern beyond output shaping.

## Manual QA checklist

- Confirm plan and test spec validation notes record the commands actually run.
- Confirm selector inspection blocks only on the expected `scripts/test-adapter-distribution.py` manual route when that path is included.
- Confirm before-and-after output-size evidence is present before code-review.
- Confirm any unchanged governance surface is recorded as `unaffected with rationale`.
- Confirm generated `.codex/skills/` and `dist/adapters/` changes, if any, came from generator commands.
- Confirm final broad smoke is run before PR readiness, not used as a substitute for targeted tests.

## What not to test

- Do not test persistent cache invalidation because persistent cache behavior is explicitly out of scope for this first slice.
- Do not test hosted CI status; local repository-owned commands are the proof surface.
- Do not test external Codex, Claude Code, or opencode tool execution.
- Do not add broad parser-helper tests outside the adapter drift family unless a later architecture artifact approves that boundary.
- Do not use snapshots as the only assertion for normal or verbose output; assert the behavioral fields, categories, counts, and omitted-detail semantics directly.

## Uncovered gaps

- None. Every spec MUST has automated test coverage, command-gate coverage, or explicit manual-routing proof coverage in this test spec.

## Next artifacts

- `implement` for M1-M4 in `docs/plans/2026-04-28-token-and-runtime-efficient-scanning.md`.
- `code-review` after implementation completes and plan validation notes are updated.
- `verify` after code-review is clean or findings are resolved.
- `explain-change` and `pr` after verify reports branch readiness.

## Follow-on artifacts

- None yet.

## Readiness

This test spec remains active as the proof map for the implemented slice.

M1-M4 implementation and first-pass `code-review` are complete. The next repository stage is `verify`.
