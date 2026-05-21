# RigorLoop Script Output Optimization

## Status

accepted

## Problem

RigorLoop's repository scripts provide essential validation, selection, packaging, and lifecycle checks. However, some scripts produce output volume proportional to the amount of work performed rather than the amount of information a maintainer needs to act.

The clearest failure mode is a successful test or validation run that prints dozens of individual `ok` lines. A passing run communicates one actionable fact: the suite passed. A long list of passing test names consumes maintainer attention without changing the decision.

The design principle is:

```text
Output volume should scale with the information the reader needs to act on,
not with the amount of work the program did.
```

A successful run should be quiet and summarized. A failed run should be loud, specific, and actionable. The user-provided guidance identifies the current anti-pattern directly: a 62-line all-`ok` pass list communicates one bit of information in 62 lines, while a useful success line would be closer to `[PASS] test-select-validation: 62 passed in 7.77s`.

This is also consistent with RigorLoop's own evidence-efficiency discipline: prefer stable IDs, summaries, targeted excerpts, and failure-focused evidence; output caps should not change failure detection or required validation evidence.

The problem is not that scripts are wrong. The problem is that their default output is not consistently optimized for the maintainer's next action.

## Goals

- Make script output quiet on success and specific on failure.
- Preserve all validation behavior, exit codes, failure detection, and evidence quality.
- Keep success output compact while retaining suite name, pass count, and duration.
- Suppress passing-test detail by default when there are no failures.
- On failure, show the failed check or test name, error or assertion, file location, and rerun command when reliable.
- Add explicit verbosity tiers: default, `--verbose`, and `--quiet`.
- Keep existing full pass-list behavior available behind `--verbose`.
- Ensure `--quiet` never hides failure reasons.
- Start with a narrow first slice around the noisiest validation and test scripts.
- Avoid broad rewrites of all scripts before an audit identifies output pain.

## Non-goals

- Do not change what any script validates.
- Do not change script exit codes.
- Do not change failure detection.
- Do not remove required validation evidence.
- Do not truncate failure details needed for repair.
- Do not make CI logs silent when failures occur.
- Do not require all scripts to emit identical output formats if their jobs differ.
- Do not change generated adapter output, skill files, workflow specs, or validation selection logic.
- Do not replace existing test frameworks unless a later proposal justifies it.
- Do not make `--verbose` unavailable.
- Do not rewrite every script in the first slice.

## Vision fit

fits the current vision

RigorLoop's vision is artifact-first and evidence-first. Script output is part of the evidence surface maintainers rely on to decide whether a change is ready for review, verification, or PR handoff.

This proposal supports that vision by making passing evidence compact and failure evidence actionable. It reduces log noise without weakening validation. It is falsified if output becomes shorter but maintainers need extra reruns to understand failures, if pass counts disappear, or if failure evidence is hidden behind a verbosity flag.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize RigorLoop scripts | in scope | Goals, Recommended direction |
| Make success output one summary line | in scope | Output contract |
| Make failure output detailed and actionable | in scope | Output contract |
| Preserve failure evidence | in scope | Non-goals, Testing and verification strategy |
| Keep verbose output available | in scope | Verbosity tiers |
| Avoid suppressing useful failure details | in scope | Non-goals, Risks and mitigations |
| Apply to CI wrapper behavior | in scope | First-slice boundary, Rollout and rollback |
| Avoid broad noisy rewrites | in scope | First-slice boundary, Scope budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Script-output audit | core to this proposal | The first slice needs an evidence-based boundary before changing multiple scripts. |
| `scripts/test-select-validation.py` output shaping | first-slice candidate | It is the clearest reported noisy success-output source. |
| `scripts/ci.sh` wrapper behavior | same-slice dependency | It is touched only if the audit or runner change shows the wrapper must change to preserve quiet-success and loud-failure behavior. |
| Common script-output helper library | deferable follow-up | A shared helper is useful only after multiple scripts prove the pattern repeats. |
| JSON output across validation scripts | deferable follow-up | Stable machine-readable output is valuable but not needed for the first success-noise reduction. |
| Broad CI log standardization | separate proposal | Repository-wide CI output policy is broader than the first script UX slice. |
| Generated adapter output and public skill files | out of scope | The proposal targets repository script presentation, not generated release artifacts or user-facing skill bodies. |

## Context

RigorLoop has many scripts used by contributors and CI. Some are user-facing enough that their output shape matters almost as much as their validation behavior.

The user-provided guidance identifies two output layers:

```text
1. Python validation/test scripts such as test-select-validation.py
2. CI wrapper behavior such as ci.sh --mode pr
```

The CI wrapper may already intend to hide successful command output, while the underlying test runner can still print noisy pass lists. The practical fix is therefore both local and layered: make noisy scripts summarize success, then ensure wrappers show one line per passing check and expand only failing checks.

This proposal treats output optimization as a script UX improvement, not a validation behavior change.

## Options considered

### Option 1: Do nothing

Keep current script output unchanged.

Pros:

- No implementation risk.
- Existing logs remain familiar.
- No test updates required.

Cons:

- Passing logs stay noisy.
- Maintainers spend attention on non-actionable `ok` lines.
- CI logs are harder to scan.
- The repository's script output remains inconsistent with its own evidence-efficiency discipline.

### Option 2: Suppress all output on success and show only exit codes

Make passing scripts print nothing.

Pros:

- Very quiet.
- Easy to implement for wrappers.

Cons:

- Hides pass count.
- Hides duration.
- Can mask silent test collapse, such as a suite shrinking from 62 tests to 3.
- Makes CI logs less informative.

This option is rejected. A success line should include at least suite name, pass count, and duration.

### Option 3: Keep current verbose output but make CI hide it

Only change `ci.sh` to suppress successful script logs.

Pros:

- Improves CI immediately.
- Leaves scripts unchanged.
- Smaller implementation.

Cons:

- Running scripts locally remains noisy.
- CI wrapper must compensate for every noisy script.
- Scripts do not become better standalone tools.
- Failure formatting still depends on each script's raw output.

This is useful but incomplete.

### Option 4: Add outcome-aware output to noisy scripts and preserve verbose mode

Make scripts default to:

```text
success: one summary line
failure: summary plus actionable failures
verbose: current full detail
quiet: minimal but never hides failure reasons
```

Pros:

- Improves local and CI use.
- Preserves full output behind `--verbose`.
- Keeps pass count and duration.
- Makes failure output more actionable.
- Aligns scripts with RigorLoop evidence-efficiency principles.

Cons:

- Requires changes to test runners or result formatting.
- Requires fixture tests for output shape.
- Some scripts may need individual handling.

## Recommended direction

Choose Option 4.

Adopt an outcome-aware output contract for user-facing RigorLoop scripts:

```text
Default:
  quiet on success
  loud and specific on failure

--verbose:
  include full pass/check detail

--quiet:
  suppress nonessential success output
  still show failure reasons
```

The first implementation should be audit-first and target the noisiest scripts, beginning with the validation or test runner that emits long all-pass lists.

## Output contract

### Default success output

A successful run should print one summary line:

```text
[PASS] test-select-validation: 62 passed in 7.77s
```

Required fields:

| Field | Reason |
| --- | --- |
| ASCII status word | Scannable pass/fail state that remains portable in CI logs. |
| Suite/check name | Identifies which script ran. |
| Count | Prevents silent test collapse. |
| Duration | Helps detect performance regressions. |

First-slice summary output uses ASCII status words:

```text
[PASS] test-select-validation: 62 passed in 7.77s
[FAIL] test-select-validation: 2 failed, 60 passed in 7.81s
[SKIP] test-select-validation: no matching paths
```

Do not print every passing test or check by default.

### Default failure output

A failed run should print:

```text
[FAIL] test-select-validation: 2 failed, 60 passed in 7.81s

FAILED test_pr_mode_routes_adapter_fixture_to_adapter_checks
  AssertionError: expected ['adapter.distribution'] but got ['skills.drift']
  scripts/test-select-validation.py:412

FAILED test_unclassified_path_blocks_without_fail_open
  AssertionError: selector returned status 'ok', expected 'blocked'
  scripts/test-select-validation.py:588

Re-run: python scripts/test-select-validation.py -k "test_pr_mode_routes_adapter_fixture or test_unclassified_path_blocks"
```

Required fields:

| Field | Reason |
| --- | --- |
| Summary line | Shows scale of failure. |
| Failed test/check names | Identifies what broke. |
| Assertion or error message | Explains why. |
| File and line when available | Tells where to inspect. |
| Rerun command when reliable | Helps iterate quickly without risking misleading instructions. |

Passing checks collapse into the summary count.

### Rerun-command decision

Rerun commands are an affordance, not a required field. A missing rerun command is acceptable. A wrong rerun command is a defect.

Generate scoped rerun commands only when:

- the runner supports a stable name filter;
- the failed check ID maps exactly to that filter;
- the filter is known to select the intended check;
- quoting can be generated safely.

If those conditions are not met, omit the scoped rerun command or provide a safe broader command:

```text
Re-run: python scripts/test-select-validation.py
```

For first-slice tests, require a scoped rerun for `scripts/test-select-validation.py` only if its filter is reliable. Runners without reliable filters must not show misleading partial commands.

### Verbosity tiers

| Mode | Success output | Failure output |
| --- | --- | --- |
| Default | One summary line | Summary plus failed checks with errors |
| `--verbose` / `-v` | Full pass list | Full output, including passing checks |
| `--quiet` / `-q` | Nothing | Failure summary plus failure details |

Hard rule:

```text
Failure reasons must not be hidden behind --verbose.
```

A maintainer should not have to rerun a failed command just to learn why it failed.

### Quiet-mode decision

For first-slice scripts:

- `--quiet` success prints nothing.
- `--quiet` failure prints the same failure summary and failure details as default mode.
- `--quiet` preserves the same exit code as default mode.

Quiet mode is useful for wrappers and shell pipelines. Failure evidence remains visible because a maintainer should not need to rerun with another flag to learn why the command failed. If CI needs a minimal success line, that behavior belongs at the wrapper layer rather than script-level `--quiet`.

### Zero-test behavior

For first-slice test-runner scripts:

- zero executed tests is a failure when the suite expects one or more tests;
- zero selected checks may be valid only when the command is explicitly an audit, list, or dry-run mode that documents zero selection as an allowed outcome;
- default success output includes a nonzero pass or check count;
- a zero-test failure includes why no tests or checks were selected or run.

Example:

```text
[FAIL] test-select-validation: 0 tests run; expected at least 1 selected test
```

### JSON output

Do not add new `--json` support in the first slice.

If a touched script already has stable `--json` output, preserve it and ensure the output contract is not broken. If a touched script lacks `--json`, keep JSON as a follow-on proposal.

Future JSON work should define a stable machine-readable shape, likely including:

```json
{
  "suite": "test-select-validation",
  "status": "failed",
  "passed": 60,
  "failed": 2,
  "skipped": 0,
  "duration_seconds": 7.81,
  "failures": [
    {
      "id": "test_pr_mode_routes_adapter_fixture_to_adapter_checks",
      "message": "AssertionError: expected ['adapter.distribution'] but got ['skills.drift']",
      "location": "scripts/test-select-validation.py:412",
      "rerun": "python scripts/test-select-validation.py -k \"test_pr_mode_routes_adapter_fixture\""
    }
  ]
}
```

JSON output should not include terminal glyphs.

## Script classification

Not every script needs the same output treatment. Audit scripts into categories:

| Category | Default output expectation |
| --- | --- |
| Test runners | One-line success; failed tests expanded. |
| Validators | One-line success; failed checks expanded with stable IDs. |
| Selectors | One-line success for selected checks; failures show path/classification reason. |
| Builders | Summary success; failures show command, artifact, and missing/stale output. |
| Packaging scripts | Summary success with artifact counts; failures show path, checksum, or package mismatch. |
| Lifecycle validators | Summary success; failures show artifact path, field, and required fix. |
| Measurement scripts | Summary plus measured values; detailed tables behind `--verbose`. |

The output contract applies first to scripts that humans run directly or that CI surfaces directly.

## First-slice boundary

The first implementation slice is audit-first.

### Audit

Create a short script-output audit:

```text
docs/changes/<change-id>/script-output-audit.md
```

For each candidate script, record:

| Field | Meaning |
| --- | --- |
| Script path | Script being assessed. |
| User-facing? | Whether maintainers run or inspect it directly. |
| Current success lines | Approximate number of lines on success. |
| Current failure usefulness | Whether failure includes name, reason, location, rerun. |
| Proposed treatment | unchanged, wrapper-only, summary mode, full rewrite. |
| First-slice? | yes/no. |

### First-slice decision

The first implementation slice is:

1. script-output audit;
2. `scripts/test-select-validation.py` default, `--verbose`, and `--quiet` output shaping;
3. `scripts/ci.sh` wrapper adjustment only if the audit or runner change shows wrapper behavior must be updated to preserve quiet-on-success and loud-on-failure behavior.

Rationale:

- The observed noisy output comes from a test runner with many passing tests.
- The CI wrapper is a separate layer and should not be broadly rewritten in the first slice.
- If the audit shows wrapper behavior is already correct after the runner change, record `scripts/ci.sh` as unchanged.

Do not rewrite every script in the first slice.

## Expected behavior changes

- A passing noisy test suite prints one summary line by default.
- A failing suite suppresses passing detail and prints failed tests with actionable context.
- Existing verbose pass-list output remains available behind `--verbose`.
- CI success output becomes one line per check or suite.
- CI failure output expands only the failed check's details.
- Failure details remain visible even in quiet mode.
- Pass counts and durations are preserved on success.
- Exit codes remain unchanged.

## Architecture impact

| Surface | Impact |
| --- | --- |
| `scripts/test-select-validation.py` | Add default compact result output and `--verbose` behavior if not present. |
| `scripts/ci.sh` | Ensure passing checks are summarized and failed check output is surfaced. |
| `scripts/test-*` fixtures | Add output-shape tests for success, failure, quiet, and verbose modes. |
| CI logs | Less success noise; more focused failure evidence. |
| Validation behavior | No change. |
| Exit codes | No change. |
| Selected checks | No change. |
| Generated output | No change. |

## Proof route

A focused test spec for script output behavior is required before implementation begins.

A spec amendment is required only if the project lacks an existing script-output contract covering:

- default success summary;
- default failure detail;
- `--verbose`;
- `--quiet`;
- pass count and duration;
- failure evidence preservation;
- CI wrapper success/failure behavior.

Implementation must not begin until the plan names one approved route:

1. existing script-output contract plus focused test spec are sufficient; or
2. spec amendment plus focused test spec packet is approved.

The recommended route is to require a focused test spec and keep spec amendment conditional.

## Testing and verification strategy

| Check ID | What is verified |
| --- | --- |
| `OUT-001` | Default success prints one summary line with suite name, count, and duration. |
| `OUT-002` | Default success suppresses individual passing checks. |
| `OUT-003` | Default failure prints summary plus failed test/check details. |
| `OUT-004` | Failure output includes failure name, message, and location when available. |
| `OUT-005` | Failure output includes a scoped rerun command only when the filter is reliable, otherwise omits it or emits a safe broader rerun command. |
| `OUT-006` | `--verbose` preserves full pass-list output. |
| `OUT-007` | `--quiet` does not hide failure reason. |
| `OUT-008` | Exit codes are unchanged for pass/fail cases. |
| `OUT-009` | CI wrapper hides successful command output but expands failed command output. |
| `OUT-010` | Output caps do not truncate failure evidence. |
| `OUT-011` | Pass count detects nonzero test count and avoids silent empty-suite success. |
| `OUT-012` | Behavior-preservation matrix proves selected checks, exit codes, and failure detection are unchanged. |
| `OUT-013` | First-slice summaries use ASCII status words such as `[PASS]`, `[FAIL]`, and `[SKIP]`. |
| `OUT-014` | The first slice does not add new `--json` support; existing JSON output is preserved if present. |

Suggested tests:

```bash
python scripts/test-script-output.py
python scripts/test-select-validation.py --self-test-output
bash scripts/ci.sh --mode explicit --path <known-pass-path>
bash scripts/ci.sh --mode explicit --path <known-fail-fixture>
git diff --check --
```

Use the repository's actual test harness names if different.

## Behavior preservation

This proposal changes presentation only.

For each touched script, record:

| Behavior | Must remain unchanged |
| --- | --- |
| Exit code | Same pass/fail exit status. |
| Test/check selection | Same tests/checks run. |
| Failure detection | Same failures detected. |
| Failure data | Same or better failure reason surfaced. |
| Validation evidence | Required evidence still available. |
| CI semantics | Same check coverage and selected commands. |

A shorter log is not acceptable if it hides failures or changes selected checks.

## Behavior-preservation proof

For each touched script, implementation records a preservation matrix:

| Behavior | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| exit code on pass | command/output | command/output | unchanged |
| exit code on failure | command/output | command/output | unchanged |
| selected tests/checks | count/list/hash | count/list/hash | unchanged |
| failure detection | fixture failure | fixture failure | unchanged |
| failure evidence | baseline detail | new detail | same or more actionable |
| verbose output | baseline full list | `--verbose` output | preserved |
| quiet failure output | n/a or baseline | new proof | failure reason visible |
| CI semantics | wrapper command/output when touched | wrapper command/output when touched | unchanged except intended presentation |

A shorter success log is insufficient if the selected-check set changes.

## Rollout and rollback

Rollout:

1. Approve proposal.
2. Complete the proof route: focused test spec is required; spec amendment remains conditional on an existing-contract gap.
3. Plan the audit and first slice.
4. Implement output shaping for `scripts/test-select-validation.py`.
5. Update `scripts/ci.sh` only as needed to preserve quiet-on-success and loud-on-failure behavior.
6. Add fixture tests for success, failure, quiet, and verbose modes.
7. Run code review.
8. Verify selected CI logs are shorter on success and actionable on failure.

Rollback:

1. Restore previous output mode for the touched script.
2. Keep any harmless tests or fixtures only if they still match behavior.
3. Do not alter validation logic, check selection, or exit codes during rollback.
4. If `ci.sh` wrapper changes cause ambiguity, revert wrapper changes first and keep local script output improvements only if still useful.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Success output hides silent test collapse. | Always include pass count; fail zero executed tests when the first-slice suite expects tests. |
| Failure output becomes too terse. | Require failure name, reason, location, and rerun command when feasible. |
| `--quiet` hides errors. | Quiet mode still prints failure reasons. |
| Maintainers need full pass list for debugging. | Preserve current behavior under `--verbose`. |
| CI wrapper suppresses the useful part of a failure. | Wrapper expands failed command output and never truncates failure evidence. |
| Output formatting changes break tests. | Add stable output-shape tests. |
| Script-specific behavior gets overgeneralized. | Start with audit and one or two scripts. |
| Rerun command is wrong. | Include rerun command only when derivable with confidence; otherwise omit rather than mislead. |
| Colors or glyphs fail in logs. | Use ASCII status words in the first slice. |
| JSON support expands the first slice into a machine-readable compatibility contract. | Do not add new `--json` support in the first slice; route broad JSON behavior to a follow-on proposal. |

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| `AC-OUT-001` | Script-output audit exists and identifies first-slice scripts. |
| `AC-OUT-002` | First-slice success output is one summary line with suite/check name, pass count, and duration. |
| `AC-OUT-003` | First-slice success output hides individual passing checks by default. |
| `AC-OUT-004` | First-slice failure output includes failed check name, message, location when available, and a rerun command only when reliable. |
| `AC-OUT-005` | `--verbose` preserves full pass/check listing. |
| `AC-OUT-006` | `--quiet` does not suppress failure reasons. |
| `AC-OUT-007` | Exit codes and selected checks are unchanged. |
| `AC-OUT-008` | CI wrapper success output is summarized and failure output is expanded. |
| `AC-OUT-009` | Output-shape tests cover success, failure, quiet, and verbose modes. |
| `AC-OUT-010` | No validation evidence needed for repair is hidden behind a rerun. |
| `AC-OUT-011` | Representative CI log comparison shows reduced success noise. |
| `AC-OUT-012` | No generated adapters, skills, specs, or lifecycle artifacts are changed except those required for this script-output initiative. |
| `AC-OUT-013` | First-slice `--quiet` success prints nothing and failure still prints failure reasons. |
| `AC-OUT-014` | Zero executed tests fail for first-slice test-runner scripts unless an explicit mode allows zero selection. |
| `AC-OUT-015` | Behavior-preservation proof records baseline and new evidence for each touched script. |
| `AC-OUT-016` | First-slice summaries use ASCII status words in bracket form, including `[PASS]`, `[FAIL]`, and `[SKIP]` when applicable. |
| `AC-OUT-017` | Scoped rerun commands are emitted only when reliable; a missing scoped rerun is acceptable, and a wrong rerun command is a defect. |
| `AC-OUT-018` | The first slice does not add new `--json` support; existing `--json` output is preserved if already present. |

## Open questions

None for proposal-review.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-21 | Optimize script output around actionability. | Passing logs should not consume attention; failing logs should guide repair. | Keep full pass lists as default. |
| 2026-05-21 | Preserve verbose mode. | Full pass lists are useful when debugging runners. | Remove detailed output entirely. |
| 2026-05-21 | Preserve failure evidence in quiet mode. | A user should not rerun just to learn why a failure happened. | Make quiet suppress all details. |
| 2026-05-21 | Start audit-first. | RigorLoop has many scripts; not all need output changes. | Rewrite all scripts at once. |
| 2026-05-21 | Treat CI wrapper and test runner as separate layers. | Wrapper success hiding and script-local output shaping solve different parts of the noise problem. | Only modify CI wrapper. |
| 2026-05-21 | First slice targets audit plus `scripts/test-select-validation.py`, with `scripts/ci.sh` touched only if needed. | This resolves first-slice ambiguity while preserving the wrapper boundary. | Audit only; broad CI wrapper rewrite. |
| 2026-05-21 | Require a focused test spec before implementation. | The output-mode contract is new enough that planning needs an explicit proof route. | Let code review infer output-mode validity. |
| 2026-05-21 | Define `--quiet` success as no output for first-slice scripts. | Quiet mode should support wrappers and pipelines while still surfacing failure reasons. | Minimal script-level success summary in quiet mode. |
| 2026-05-21 | Treat zero executed tests as failure for first-slice test runners unless explicitly allowed. | Pass counts should prevent silent suite collapse. | Leave zero-test behavior to implementation. |
| 2026-05-21 | Require behavior-preservation proof for each touched script. | Output-shape tests alone do not prove selected checks, exit codes, or failure detection stayed unchanged. | Rely only on output-shape tests. |
| 2026-05-21 | Use ASCII bracketed status words for first-slice summaries. | `[PASS]`, `[FAIL]`, and `[SKIP]` are readable and portable in CI logs. | Unicode glyphs by default. |
| 2026-05-21 | Emit scoped rerun commands only when reliable. | A missing rerun command is acceptable, but a wrong rerun command is a defect. | Require scoped rerun commands for every runner. |
| 2026-05-21 | Defer new JSON support beyond the first slice. | JSON introduces a separate machine-readable compatibility contract. | Add new `--json` support during the first success-noise reduction slice. |

## Next artifacts

```text
proposal-review
spec only if existing script-output conventions are insufficient
test-spec for output-shape and behavior-preservation behavior
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Potential future proposals after the first slice:

- Common script-output helper library if multiple scripts adopt the same pattern.
- JSON output across validation scripts.
- Broader CI log standardization.
- Timing or performance regression summaries across validation suites.

## Follow-on artifacts

- `specs/script-output-optimization.md`

## Readiness

Accepted; downstream feature spec created at `specs/script-output-optimization.md`.

## Core invariant

```text
Script output should be proportional to actionability.

Success output should summarize what passed, how many checks ran, and how long
it took. Failure output should surface the exact failures, reasons, locations,
and rerun commands.

Shorter output is only better when it preserves validation behavior, exit codes,
selected checks, and failure evidence.
```
