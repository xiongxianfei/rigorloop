# Code Review M2 Round 1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Target: commit `bb6c5de12baa6c054910cee563d5dce3bbdde01b`
Reviewed milestone: M2. Repository tree untracking and guidance alignment
Reviewed artifact: commit `bb6c5de`
Review date: 2026-05-13
Reviewer: Codex code-review
Recording status: recorded
Status: clean-with-notes

## Outcome

- Review status: clean-with-notes
- Material findings: none
- Blocking findings: none
- Review resolution: not required

## Review inputs

- Diff/review surface: `git show --stat --oneline --find-renames bb6c5de`, `git show --name-only --format=short bb6c5de`, and focused diffs for `dist/adapters/README.md`, root guidance, `scripts/ci.sh`, selector routing, and `scripts/test-adapter-distribution.py`.
- Governing spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`
- Test spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.test.md`
- Active plan: `docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
- Architecture and ADR: `docs/architecture/system/architecture.md`, `docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md`
- Validation evidence recorded in the active plan and rerun during review.

## Diff summary

M2 removes tracked generated adapter package fragments from `dist/adapters/codex/`, `dist/adapters/claude/`, and `dist/adapters/opencode/`, including generated skill bodies, instruction entrypoints, and opencode command wrappers. It leaves `dist/adapters/README.md` and `dist/adapters/manifest.yaml` as the tracked adapter support surface.

The implementation updates `dist/adapters/README.md`, `CONSTITUTION.md`, `AGENTS.md`, `README.md`, and `docs/workflows.md` so public adapter installation points to release archives or the adapter install-contract surface instead of the retired tracked package tree. It also updates broad CI and selector adapter checks to prove generated archive output through existing test fixtures rather than requiring `build-adapters.py --check` or `validate-adapters.py` against the retired repository tree.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The diff removes all tracked generated package fragments under the R9-R13 paths and keeps only `dist/adapters/README.md` and `dist/adapters/manifest.yaml`, matching R8-R15d. |
| Test coverage | pass | `test_public_adapter_support_surface_only_tracks_readme_and_manifest`, `test_public_adapter_readme_documents_archive_install_contract`, `test_root_guidance_points_to_adapter_install_contract_surface`, and `test_validate_adapters_cli_rejects_retired_repository_output` directly cover M2 behavior. |
| Edge cases | pass | Direct proof covers no tracked `dist/adapters/**/skills`, no generated entrypoints or command wrappers under `dist/adapters/`, root guidance stale-path rejection, and generated archive validation without the tracked package tree. |
| Error handling | pass | Repository-output adapter validation now rejects the retired tree; generated package completeness remains covered by archive-output validation and release-verify dry-run routing. |
| Architecture boundaries | pass | The tracked support surface remains metadata and install guidance, while generated adapter package correctness is proved from generated release output. |
| Compatibility | pass | `v0.1.2` compatibility language remains version-qualified, and historical release tests use fixture-generated adapter output rather than current tracked package files. |
| Security/privacy | pass | The diff removes generated text and changes guidance/tests; no secrets, credentials, auth logic, or unsafe logging are introduced. |
| Derived artifact currency | pass | `git ls-files 'dist/adapters/**'` shows only the approved tracked support files; `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3` builds v0.1.3 archive output and routes validation through that output. |
| Unrelated changes | pass | Changes are scoped to M2 deletion, guidance alignment, selector/CI validation routing, and lifecycle evidence for the active plan. |
| Validation evidence | pass | Review reran `git ls-files`, `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3`, and inspected recorded passes for adapter distribution, selector, artifact lifecycle, change metadata, and archive build/validate commands. |

## No-finding rationale

The reviewed diff completes the M2 storage and guidance migration without broadening into M3 release evidence or token-cost reports. The deleted paths match the generated package fragment boundary in the spec, the remaining tracked adapter surface is exactly the README and manifest, and root guidance no longer presents tracked adapter skill-body paths as the active install model. The validation updates are consistent with the approved replacement model because current checks exercise generated archive output rather than the retired repository package tree.

## Residual risks

- Full `v0.1.3` release evidence, adapter artifact metadata, release notes, and token-cost reports remain M3 scope.
- Final release verification and lifecycle closeout remain M4 scope.
- `docs/learn/sessions/2026-05-13-release-version-gate.md` remains an untracked separate learn artifact and is outside this M2 review surface.

## Recommended next stage

Close M2 and proceed to `implement M3`.
