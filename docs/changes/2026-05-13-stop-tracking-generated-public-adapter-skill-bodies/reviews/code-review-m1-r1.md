# Code Review M1 Round 1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Target: commit `4503926f08627dab6de9a4a238c9ea6a1d23ca9b`
Reviewed milestone: M1. Validation model migration and regression tests
Reviewed artifact: commit `4503926f08627dab6de9a4a238c9ea6a1d23ca9b`
Review date: 2026-05-13
Reviewer: Codex code-review
Review status: changes-requested
Recording status: recorded
Status: changes-requested

## Review inputs

- Diff/review surface: `git show 4503926f08627dab6de9a4a238c9ea6a1d23ca9b`
- Governing spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`
- Test spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.test.md`
- Active plan: `docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
- Validation evidence recorded in the active plan and commit body
- Direct check: `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3`

## Diff summary

M1 adds `v0.1.3` release-validation support in `scripts/adapter_distribution.py`, requires adapter archive metadata for `v0.1.3`, introduces an untracked public adapter surface branch, bypasses tracked adapter package drift validation for `v0.1.3`, validates the tracked support surface, and adds regression tests for release-output validation and tracked package-fragment rejection.

The lifecycle artifacts for the v0.1.3 untracking initiative were also added or updated, including proposal, spec, test spec, architecture, ADR, plan, review records, and change metadata.

## Material Findings

### CR-M1-1 - `release-verify.sh` still rejects `v0.1.3`

Finding ID: CR-M1-1

Severity: major

Location: `scripts/release-verify.sh:24`

Evidence: M1 requirement coverage includes `R41g`, which says replacement validation must prove release verification no longer depends on tracked generated adapter skill bodies. The M1 plan also says to update release validation and release verify so `v0.1.3` release readiness depends on generated output and archives, not tracked package trees. However `scripts/release-verify.sh` still allows only `v0.1.0-rc.1`, `v0.1.0`, `v0.1.1`, and `v0.1.2` in its target case statement. Running `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3` exits with `Unsupported release target: v0.1.3`.

Required outcome: `release-verify.sh` must support the `v0.1.3` target in the M1 validation model and must delegate to generated release-output/archive validation instead of tracked `dist/adapters/<adapter>/` package validation.

Safe resolution path: Update `scripts/release-verify.sh` to accept `v0.1.3`, build or use a release-output directory for v0.1.3 adapter archives, pass `--release-output-dir` and `--release-commit` to `scripts/validate-release.py`, and avoid required tracked `build-adapters.py --check` / `validate-adapters.py --version <adapter-version>` checks for the retired tracked package tree. Add a regression test that exercises `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3` and asserts the required generated-output/archive validation commands are invoked.

## Checklist coverage

- Spec alignment: concern. `validate_release_output()` now follows the v0.1.3 archive-validation direction, but the maintainer-facing release gate still rejects v0.1.3, leaving `R41g` incomplete.
- Test coverage: concern. New tests cover direct `validate_release_output()` behavior, but no test covers `release-verify.sh v0.1.3` command selection.
- Edge cases: concern. The named edge case that release verification must not depend on tracked adapter skill bodies lacks direct passing proof because the release gate exits before checks are selected.
- Error handling: pass. The new release-output validation branch reports missing support surfaces, tracked package fragments, archive errors, metadata errors, and release-note errors with actionable messages.
- Architecture boundaries: concern. The architecture says release verification delegates structured validation to generated release artifacts; the shell gate has not been updated to reach that path for v0.1.3.
- Compatibility: pass. Existing v0.1.1/v0.1.2 release-validation behavior remains version-gated.
- Security/privacy: pass. The reviewed diff does not introduce secrets, credential handling, or unsafe logging.
- Derived artifact currency: concern. Generated adapter package validation is correctly shifted to archives in `validate_release_output()`, but release verification still points at the tracked package drift path for supported non-v0.1.2 releases.
- Unrelated changes: pass. The code changes are scoped to adapter/release validation and matching tests; lifecycle artifact additions are the approved governing surfaces for this initiative.
- Validation evidence: concern. The reported tests are relevant and passing, but they do not include a passing `release-verify.sh v0.1.3` dry-run or real-run proof.

## Recommended next stage

Enter `review-resolution` for `CR-M1-1`, then return to `implement M1` for the targeted fix and rerun `code-review M1`.
