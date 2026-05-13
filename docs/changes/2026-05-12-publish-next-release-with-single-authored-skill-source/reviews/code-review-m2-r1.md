# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M2. Release docs and adapter install guidance describe the transition
Reviewed artifact: committed M2 diff `918cb65`
Review date: 2026-05-13
Recording status: recorded
Status: changes-requested

## Review inputs

- Diff/review surface: committed diff `918cb65` for M2 documentation, release-note validation, tests, and lifecycle metadata.
- Active plan: `docs/plans/2026-05-13-publish-next-release-with-single-authored-skill-source.md`
- Plan index: `docs/plan.md`
- Spec: `specs/publish-next-release-with-single-authored-skill-source.md`
- Test spec: `specs/publish-next-release-with-single-authored-skill-source.test.md`
- Architecture: `docs/architecture/system/architecture.md`
- Learning follow-up: `docs/learn/sessions/2026-05-13-defensive-rule-preservation.md`
- Validation evidence recorded in the active plan and change metadata.
- Direct review checks run:
  - `git show --stat --oneline 918cb65`
  - `git show --unified=80 --format=short 918cb65 -- AGENTS.md CONSTITUTION.md README.md docs/workflows.md dist/adapters/README.md docs/releases/v0.1.1/release-notes.md`
  - `git show --unified=80 --format=short 918cb65 -- scripts/adapter_distribution.py scripts/test-adapter-distribution.py`
  - `rg -n 'hand-edit|Do not edit|public Codex adapter output|\.codex/skills/|local Codex' README.md docs/workflows.md AGENTS.md CONSTITUTION.md dist/adapters/README.md docs/releases/v0.1.1/release-notes.md`
  - `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_public_adapter_readme_documents_metadata_and_install_transition AdapterDistributionTests.test_v0_1_1_release_notes_document_transition_contract AdapterDistributionTests.test_contributor_docs_install_local_codex_from_public_adapter AdapterDistributionTests.test_validate_release_cli_accepts_repository_v0_1_1_artifacts`
  - `python scripts/validate-release.py --version v0.1.1`
  - `git ls-files -- .codex/skills/`
  - `git check-ignore -v .codex/skills/proposal/SKILL.md`

## Diff summary

- `dist/adapters/README.md` now states that `v0.1.1` uses repository-tree adapter installs under `dist/adapters/`, does not require downloadable adapter archives, fixes the adapter artifact metadata path to `<version>.yaml`, and keeps `.codex/skills/` out of the public adapter install path.
- `docs/releases/v0.1.1/release-notes.md` now states that `skills/` is canonical, `dist/adapters/` remains the public adapter install path, `.codex/skills/` generation is not release evidence, and no adapter archives are introduced.
- `scripts/adapter_distribution.py` now validates that `v0.1.1` release notes do not describe `.codex/skills/` generation as release evidence and do state that `.codex/skills/` generation is not release evidence.
- `scripts/test-adapter-distribution.py` adds direct assertions for adapter README transition guidance, release-note transition wording, contributor local Codex setup wording, and repository v0.1.1 release validation.
- Contributor/governance docs were updated to tell contributors to install or copy public Codex adapter output into ignored `.codex/skills/`.

## Findings

### CR-M2-F1

Finding ID: CR-M2-F1

Severity: major

Location:

- `CONSTITUTION.md:82`
- `AGENTS.md:34`
- `README.md:148`
- `docs/workflows.md:220`

Evidence:

- `CONSTITUTION.md:82` still leads with "Local Codex runtime state under `.codex/skills/` MUST NOT be hand-edited or tracked" before the public-adapter install instruction.
- `AGENTS.md:34` still leads with "Do not hand-edit local Codex runtime state in `.codex/skills/`."
- `README.md:148` and `docs/workflows.md:220` still classify `.codex/skills/` under "Do not hand-edit generated Codex compatibility output".
- The approved spec says contributor-facing local Codex setup guidance must tell contributors to install or copy from public Codex adapter output into `.codex/skills/`, keep `.codex/skills/` untracked, and edit canonical skills under `skills/` (`R24`, `R25`). The learning follow-up explicitly asked M2 code-review to evaluate whether the implementation preserved obsolete defensive `.codex/skills/` wording instead of deleting it.

Problem:

The M2 implementation correctly removes `.codex/skills/` from release evidence, but several contributor/governance surfaces still preserve the old rule shape as a prohibition about `.codex/skills/` itself. That keeps `.codex/skills/` prominent as a special internal output and contradicts the approved direction to describe the active behavior plainly: use the public Codex adapter path, install locally when needed, keep local state untracked, and edit `skills/`.

Required outcome:

Contributor and governance docs should stop preserving obsolete `.codex/skills/` hand-edit/generated-output rules and should keep only the concise active local setup rule required by `R24` and `R25`.

Safe resolution path:

Replace the cited wording with concise active guidance, for example:

```text
For local Codex use, install or copy public Codex adapter output from `dist/adapters/codex/.agents/skills/` into ignored `.codex/skills/`; keep `.codex/skills/` untracked and edit canonical skills under `skills/`.
```

Remove the separate "Do not hand-edit generated Codex compatibility output" classification for `.codex/skills/` from public/contributor docs, or narrow it to generated public adapter packages where that prohibition remains the active rule. Keep `dist/adapters/` generated-output guidance intact.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | concern | Adapter README and release notes satisfy R20-R23 and R26-R31, but CR-M2-F1 shows R24-R25 wording is implemented through stale defensive `.codex/skills/` rule shape. |
| Test coverage | concern | Focused M2 tests pass, but `test_contributor_docs_install_local_codex_from_public_adapter` only checks that required phrases exist and does not reject stale "do not hand-edit generated Codex compatibility output" wording for `.codex/skills/`. |
| Edge cases | pass | The docs and tests cover no-archive `v0.1.1`, public repository-tree adapter install, metadata path placeholder, and `.codex/skills/` not being public install or release evidence. |
| Error handling | pass | Release-note validation reports actionable errors when stale `.codex/skills` release-evidence wording appears. |
| Architecture boundaries | concern | Release evidence boundaries are correct, but CR-M2-F1 leaves local runtime state described as a special generated-output prohibition in contributor/governance surfaces. |
| Compatibility | pass | `dist/adapters/` remains the public install path; no adapter support or archive behavior is removed. |
| Security/privacy | pass | No local `.codex/skills/` contents, secrets, or machine-local paths are published as release evidence. |
| Derived artifact currency | pass | Generated public adapter skill bodies were not changed; public adapter package validation still passes. |
| Unrelated changes | pass | The diff is scoped to M2 docs, release-note validation, tests, and lifecycle metadata. |
| Validation evidence | concern | Targeted M2 checks and `validate-release.py` pass, but they do not catch the stale defensive wording identified in CR-M2-F1. |

## No-finding rationale

Not applicable; this review has one material finding.

## Residual risks

- M3 remains unimplemented and must still run the final release evidence pack after M2 review-resolution closes.
- The broader architecture still contains some historical generated-output language for `.codex/skills/`; the M2 fix should stay scoped to contributor/governance/public guidance touched by this milestone unless the approved architecture is found to conflict materially.

## Review outcome

- First-pass review status: changes-requested
- Material findings: CR-M2-F1
- Required review-resolution: required
- Reviewed milestone: M2
- Milestone state after review: resolution-needed
- Remaining implementation milestones: M2 resolution-needed, M3 planned
- Next stage: review-resolution M2
- Final closeout readiness: not ready because M2 has an open material finding and M3 is not implemented or reviewed
