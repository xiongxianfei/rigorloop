# M6 CI Cutover and Retirement Evidence

## Result

Hosted PR and main CI now enter a transparent sequential graph in `scripts/ci.sh`:

1. Gate A canonical skill integrity, regressions, generated currency, and boundary structure;
2. Gate B all-target adapter regressions, archive build, and archive parity;
3. Gate C release-integrity regressions plus public npm package contracts;
4. lifecycle, change metadata, review evidence, workflow, fidelity, and retirement governance; and
5. deterministic README, vision-marker, Markdown, and guide structure.

The graph ends with the public lifecycle owner in `pr-ci` or `push-main-ci`
mode. It does not invoke the selector, validation cache, broad-smoke scheduler,
target runtimes, prompts, transcripts, model matrices, or dynamic benchmarks.

Local, explicit, and release selector modes, inner-loop lifecycle caching, and
explicit legacy broad smoke remain available and independently tested. Their
active contracts are not deleted or silently reinterpreted in this initiative.

## Old-versus-replacement comparison

Against `e77a351c..3512a547`, the old PR selector took 1.57 seconds to classify
17 checks and then blocked on three newly approved but unregistered surfaces:
the retirement ledger, its focused library, and its test. Satisfying that route
would require adding new selector registration solely to maintain the
indirection this change is removing.

The replacement dry graph selected 26 direct commands in 0.01 seconds and
returned success without executing them. Its command inventory directly covers
every retained product gate and governance owner, including deterministic
contributor surfaces that the old 17-check result selected only indirectly.
This timing is diagnostic only; replacement acceptance rests on negative-path
coverage and the real command results below, not command count or speed.

## Contract disposition

- Selector and broad-smoke implementation: retained for local, explicit,
  release, and legacy compatibility; absent from default PR/main acceptance.
- Validation cache: retained for explicit-path inner loops; absent from default
  PR/main acceptance and all closeout proof.
- Semantic documentation prose heuristics: not called by the direct acceptance
  graph; semantic quality stays review-owned.
- Deterministic contributor structure, requirement fidelity, workflow state,
  public package, release, skill, adapter, and lifecycle failures: directly
  retained.
- New standalone validator CLIs, selectors, caches, and schedulers: zero.

## Test-first evidence

The first direct-graph regression failed because PR mode still called the
selector and returned its `empty-changed-paths` blocker. After the cutover, PR
and main dry-run tests prove exact lifecycle range forwarding, stable owner
commands, selector absence, and target-runtime/transcript exclusion. Existing
selector forwarding tests now cover only the compatibility modes they still
own.

The first real graph also found a stale adapter assertion that still expected
the pre-M4 phrase `packed install smoke`; it now asserts the approved
`filesystem materialization` boundary. A second run proved that
`test-npm-package-publication.py` is release-profile proof: after a canonical
skill change, newly generated archives intentionally cannot match bundled
v0.4.0 metadata. The command remains in Gate C release verification, while
PR/main uses the npm package's own deterministic tests.

## CI maintenance result

- Skill: `ci-maintenance`
- Status: updated
- Workflow: `.github/workflows/ci.yml`
- PR checks: direct product, package, release-regression, governance, and deterministic contributor gates
- Boundary checks: release publication remains in release workflow; legacy broad smoke remains explicit
- Permissions: unchanged least-privilege `contents: read`
- Caching: no Actions cache and no repository validation cache in PR/main acceptance
- Secrets, write permissions, `pull_request_target`, matrices, publication, and target runtimes: absent
- Open blockers: none for the approved partial cutover; full deletion of compatibility machinery remains out of scope pending exact contract retirement

## Validation

- `bash -n scripts/ci.sh` — pass.
- Targeted direct PR/main graph tests — pass.
- `python scripts/test-retirement-ledger.py` — pass; 14 tests.
- `python scripts/test-select-validation.py` — pass; 152 tests in 65.84 seconds.
- `bash scripts/ci.sh --mode pr --base e77a351c --head 3512a547b1964e4f8505defc1132e4adb8035cf4` — pass; 26 direct checks in 618 seconds.
- `git diff --check` — pass.

## Metrics and rollback

Default hosted acceptance changes from one selector-mediated entry to 26 named
direct commands. No executable file is deleted: the safe rollback is to restore
PR/main dispatch to `run_selected_mode` and the prior contributor/current-state
wording. Gate A, Gate B, Gate C, governance composition, focused compatibility
tests, and release automation remain independently recoverable.
