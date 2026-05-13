# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2. Release docs and adapter install guidance describe the transition
Reviewed artifact: committed M2 diff `918cb65` plus CR-M2-F1 resolution diff `e6c517d`
Review date: 2026-05-13
Recording status: recorded
Status: clean-with-notes

## Review inputs

- Diff/review surface: committed M2 implementation diff `918cb65` and accepted review-resolution fix `e6c517d`.
- Prior review: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/code-review-m2-r1.md`
- Review resolution: `docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/review-resolution.md`
- Active plan: `docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md`
- Spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Test spec: `specs/publish-next-release-with-single-authored-skill-source.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- Learning follow-up: `docs/learn/sessions/2026-05-13-defensive-rule-preservation.md`
- Direct review checks run:
  - `git show --unified=80 --format=short 918cb65 -- dist/adapters/README.md docs/releases/v0.1.1/release-notes.md scripts/adapter_distribution.py scripts/test-adapter-distribution.py AGENTS.md CONSTITUTION.md README.md docs/workflows.md`
  - `git show --unified=80 --format=short e6c517d -- AGENTS.md CONSTITUTION.md README.md docs/workflows.md scripts/test-adapter-distribution.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/review-resolution.md docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/review-log.md docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md docs/plan.md docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_contributor_docs_install_local_codex_from_public_adapter AdapterDistributionTests.test_public_adapter_readme_documents_metadata_and_install_transition AdapterDistributionTests.test_v0_1_1_release_notes_document_transition_contract AdapterDistributionTests.test_validate_release_cli_accepts_repository_v0_1_1_artifacts`
  - `python scripts/validate-release.py --version v0.1.1`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `rg -n 'Do not hand-edit local Codex runtime state|Do not hand-edit generated Codex compatibility output|MUST NOT be hand-edited or tracked|Regenerate it with `python scripts/build-skills.py` when needed\.' AGENTS.md CONSTITUTION.md README.md docs/workflows.md`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md --path docs/plan.md --path docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/change.yaml --path docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/review-log.md --path docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/review-resolution.md --path docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source/reviews/code-review-m2-r1.md`
  - `git diff --check -- AGENTS.md CONSTITUTION.md README.md docs/workflows.md dist/adapters/README.md docs/releases/v0.1.1/release-notes.md scripts/adapter_distribution.py scripts/test-adapter-distribution.py docs/plan.md docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md docs/changes/2026-05-12-publish-next-release-with-single-authored-skill-source`

## Diff summary

- `dist/adapters/README.md` documents the `v0.1.1` repository-tree public adapter install path, no required downloadable archives, and the `<version>.yaml` adapter artifact metadata path.
- `docs/releases/v0.1.1/release-notes.md` states that `skills/` is canonical, `dist/adapters/` remains the public install path, `.codex/skills/` generation is not release evidence, and no downloadable adapter archives are introduced.
- `scripts/adapter_distribution.py` validates that `v0.1.1` release notes do not describe `.codex/skills/` generation as release evidence and do state that `.codex/skills/` generation is not release evidence.
- Contributor/governance docs now describe active local Codex behavior: install or copy public Codex adapter output into ignored `.codex/skills/`, keep `.codex/skills/` untracked, and edit canonical `skills/`.
- `scripts/test-adapter-distribution.py` covers adapter README transition guidance, release-note transition guidance, contributor local Codex setup guidance, and rejects the stale defensive `.codex/skills/` phrases from CR-M2-F1.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | R20-R27 are satisfied by adapter README, release notes, and contributor docs; R24-R25 are satisfied by local Codex setup wording in `AGENTS.md`, `CONSTITUTION.md`, `README.md`, and `docs/workflows.md`. |
| Test coverage | pass | Focused tests directly cover adapter README guidance, release-note transition wording, contributor local Codex setup, and stale defensive phrase rejection. |
| Edge cases | pass | No-archive `v0.1.1`, metadata path placeholder, `.codex/skills/` not being public install source, and local setup from public Codex adapter output are covered by tests and manual line inspection. |
| Error handling | pass | Release-note validation reports actionable errors for stale `.codex/skills` release-evidence wording. |
| Architecture boundaries | pass | Docs and validation keep release evidence on canonical skills and public adapter output; local Codex use follows the public Codex adapter path. |
| Compatibility | pass | `dist/adapters/` remains the transition-release public install path and public adapter support for Codex, Claude Code, and opencode is unchanged. |
| Security/privacy | pass | The change does not publish local `.codex/skills/` contents, local paths, secrets, or credentials as release evidence. |
| Derived artifact currency | pass | Generated public adapter skill bodies were not modified; `python scripts/validate-adapters.py --version 0.1.1` passed. |
| Unrelated changes | pass | The reviewed diff is scoped to M2 docs, validation expectations, tests, and required lifecycle/review-resolution state. |
| Validation evidence | pass | Focused M2 tests, release validation, adapter validation, stale phrase scan, review artifact validation, lifecycle validation, and whitespace checks passed. |

## No-finding rationale

The M2 implementation and accepted CR-M2-F1 fix now match the transition-release contract: public adapter output under `dist/adapters/` remains the public install path, downloadable archives are deferred, release notes do not make `.codex/skills/` release evidence, and local Codex setup guidance uses the public Codex adapter path without preserving obsolete defensive `.codex/skills/` generated-output rules. The added tests include both positive transition guidance assertions and negative stale-wording assertions.

## Residual risks

- M3 still needs to run the final release evidence and validation pack before final closeout.
- This clean review closes only M2; it is not PR readiness or release readiness.

## Review outcome

- First-pass review status: clean-with-notes
- Material findings: none
- Required review-resolution: not required for this rerun; prior `CR-M2-F1` is closed
- Reviewed milestone: M2
- Milestone state after review: closed
- Remaining implementation milestones: M3 planned
- Next stage: implement M3
- Final closeout readiness: not ready because M3 is not implemented or reviewed
