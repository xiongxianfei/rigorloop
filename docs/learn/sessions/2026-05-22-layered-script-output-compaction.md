# Learn Session: Layered Script Output Compaction

## Frame

- Date: 2026-05-22
- Status: session-recorded; durable lesson routed to topic guidance
- Trigger: contributor explicitly invoked `learn` after final verify still produced hundreds of lines from `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped` and verbose `unittest` output from `python scripts/test-change-metadata-validator.py`, despite the recent script-output optimization work.
- Trigger type: explicit contributor observation after verification.
- Scope: why prior script-output compaction did not eliminate broad-smoke and other test-runner output volume; best-practice guidance for future output optimization.
- Session path: `docs/learn/sessions/2026-05-22-layered-script-output-compaction.md`

## Evidence Reviewed

- Contributor trigger text showing:
  - broad smoke output summarized by the UI as `... +453 lines`;
  - `python scripts/test-change-metadata-validator.py` printing one `... ok` line per passing test.
- `specs/script-output-optimization.md`
  - The first-slice contract targeted `scripts/test-select-validation.py` and a minimal `scripts/ci.sh` wrapper boundary.
  - The change was presentation-only and had to preserve validation coverage, selected checks, failure detection, and exit-code semantics.
- `specs/script-output-optimization.test.md`
  - The test strategy explicitly said broad tests for every repository script were out of scope.
  - Wrapper checks focused on selected CI hiding successful child output by default and showing it with `--verbose`.
- `docs/changes/2026-05-21-script-output-optimization/script-output-audit.md`
  - The audit selected `scripts/test-select-validation.py` as the first implementation target.
  - It left `scripts/ci.sh` conditional because selected-check wrapper behavior already hid successful child output.
- `docs/changes/2026-05-21-script-output-optimization/behavior-preservation.md`
  - M3 changed only `scripts/test-select-validation.py`.
  - M4 left `scripts/ci.sh` unchanged because selected-CI wrapper behavior preserved quiet-success and loud-failure behavior for the scoped path.
- `scripts/ci.sh`
  - `run_broad_smoke` invokes many scripts through `run_check`.
  - `run_check` prints the label, command, and then streams child stdout/stderr directly.
  - The selected-CI path has separate Python result-capturing and default success-output hiding, but broad-smoke does not use that selected-check capture layer.
- `scripts/test-change-metadata-validator.py`
  - The script ends with `unittest.main(verbosity=2)`, which prints one line per test result on success.
- Prior learn topic:
  - `docs/learn/topics/evidence-preserving-compaction.md` captures the broader lesson that compaction must preserve behavior/evidence, but it does not yet capture the layered-output boundary that caused this incident.

## Exclusions

- No script behavior is changed by this learn session.
- No proposal, spec, test spec, CI wrapper, or validator contract is amended here.
- No final verification, PR readiness, hosted CI status, or branch state is claimed by this learn session.
- The separate untracked learn session `docs/learn/sessions/2026-05-21-evidence-preserving-compaction.md` and topic `docs/learn/topics/evidence-preserving-compaction.md` are treated as prior context, not rewritten here.

## Prior Learnings Reviewed

- `docs/learn/topics/evidence-preserving-compaction.md`:
  - Relevant because it says noisy output or metadata should be compacted only after preserved behavior/evidence is named.
  - Insufficient for this incident because it does not distinguish producer output, wrapper output, broad-smoke orchestration, and UI transcript truncation as separate layers.

## Observations

### O1: The previous output optimization was correctly scoped, but the scope was narrower than the user's current expectation

The script-output work optimized `scripts/test-select-validation.py` and selected-CI wrapper behavior. It did not claim to compact every test script or the broad-smoke orchestration path.

Evidence:

- The script-output audit chose `scripts/test-select-validation.py` as first-slice and left other scripts out of scope.
- The test spec explicitly says not to add broad tests for every repository script because the first slice targeted `scripts/test-select-validation.py` and conditional `scripts/ci.sh` behavior.
- The contributor's current output examples come from `broad-smoke` and `test-change-metadata-validator.py`, not from `test-select-validation.py`.

### O2: Broad-smoke still streams child output directly

Selected CI and broad smoke are different output paths in `scripts/ci.sh`.

Evidence:

- The selected-CI path captures each selected check result and hides successful child output unless `--verbose` is set.
- `run_broad_smoke` calls `run_check`, and `run_check` prints the command and runs the child script directly without capturing successful output.
- Therefore every verbose child script remains verbose inside broad smoke even if selected CI is compact.

### O3: Several child scripts still use verbose unittest defaults

The current `test-change-metadata-validator.py` still prints per-test success lines because it delegates directly to `unittest.main(verbosity=2)`.

Evidence:

- `scripts/test-change-metadata-validator.py` ends with `unittest.main(verbosity=2)`.
- The contributor's example shows one `... ok` line per passing change-metadata validator test.
- Broad-smoke also runs other fixture suites that can produce the same style of output.

### O4: UI transcript compaction is not script-output compaction

The interface collapsed the broad-smoke transcript as `... +453 lines`, but that does not mean the repository scripts emitted compact output.

Evidence:

- The terminal transcript still contains full child output when expanded.
- UI truncation protects the chat surface after the fact. It does not improve local terminal readability, CI log scanability, or generated validation evidence.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | Topic guidance | Contributor explicit `learn` request and supplied examples | The pattern generalizes: output optimization must name all output layers in scope, not only one producer. |
| O2 | durable-lesson | durable-lesson | Topic guidance; future proposal candidate | Contributor explicit `learn` request and script evidence | Wrapper capture needs to be applied at every orchestration path, including broad smoke, if compact output is the goal. |
| O3 | durable-lesson | durable-lesson | Topic guidance; future proposal candidate | Contributor explicit `learn` request and script evidence | Each verbose child script remains a noise source until it gets its own default/verbose/quiet contract or is wrapped by a capture layer. |
| O4 | observation | observation | Session record only | Contributor explicit `learn` request and transcript behavior | UI transcript truncation explains why chat looks compacted, but it is not durable repository behavior. |

Contributor confirmation status: confirmed for learn capture by explicit contributor `learn` invocation and request for root cause and best practices.

## Routing Results

- Observation routing: recorded in this session.
- Durable lesson routing: added `docs/learn/topics/script-output-optimization.md`.
- Direction / proposal routing: no proposal opened in this session. A future proposal is the right owner if the project decides to compact broad-smoke output and other unittest-based scripts.
- Artifact update routing: none in this session.
- Process follow-up routing: no issue tracker was used; no active plan owns the broad-smoke follow-up.

## Root Cause

The root cause is a scope and layering mismatch.

The previous script-output optimization compacted one noisy producer, `scripts/test-select-validation.py`, and verified selected-CI wrapper behavior. It did not convert the repository to a uniform output contract. Broad smoke still uses a separate `run_check` path that streams child output, and many child scripts still use verbose `unittest` output. As a result, output volume is still proportional to the amount of work performed whenever the broad-smoke path or an unoptimized child script runs.

In short:

```text
optimized:
  selected CI wrapper output
  scripts/test-select-validation.py

not yet optimized:
  broad-smoke run_check streaming
  scripts/test-change-metadata-validator.py
  other unittest fixture suites
  UI transcript expansion behavior
```

## Best Practices

1. Map output layers before optimizing.

Separate producer scripts, wrapper scripts, CI orchestration modes, and UI transcript behavior. A fix at one layer does not automatically compact the others.

2. Define one output contract per script class.

For Python unittest fixture scripts, use a shared pattern: compact default success, actionable default failure, full detail behind `--verbose`, and silent success under `--quiet` when useful.

3. Make wrapper modes consistent.

If selected CI captures successful child output, broad smoke should either use the same capture policy or explicitly document why broad smoke remains transcript-style.

4. Preserve failure evidence first.

Do not hide stdout/stderr globally. Capture it, print a compact success summary, and expand full output only on failure or `--verbose`.

5. Optimize by audit, not by blanket suppression.

Rank scripts by observed output volume and maintainer read frequency. Convert the worst offenders first and add behavior-preservation proof for each touched script.

6. Keep UI truncation out of the contract.

Chat or terminal transcript folding is a display convenience, not repository-owned output behavior.

## Follow-Ups

- Recommended future proposal: broad script-output standardization for `scripts/ci.sh --mode broad-smoke` and remaining verbose unittest fixture suites.
- Candidate first follow-up targets:
  - add broad-smoke child-output capture similar to selected CI;
  - add default/verbose/quiet output shaping to `scripts/test-change-metadata-validator.py`;
  - audit other `unittest.main(verbosity=2)` fixture scripts before broad rewrites.
