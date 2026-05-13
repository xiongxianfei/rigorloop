# Stop Tracking Generated Public Adapter Skill Bodies for v0.1.3

## Status

accepted

## Problem

PR #51 introduced the adapter archive release-evidence slice for `v0.1.2` while intentionally preserving tracked generated public adapter skill bodies under `dist/adapters/**/skills` for the compatibility window.

That compatibility window is now satisfied by the published `v0.1.2` release: the release is public, non-prerelease, and includes downloadable adapter archives for Codex, Claude Code, and opencode. The repository still tracks generated public skill bodies under:

```text
dist/adapters/codex/.agents/skills/
dist/adapters/claude/.claude/skills/
dist/adapters/opencode/.opencode/skills/
```

Those trees are generated adapter output, not authored source. Keeping them tracked means skill edits continue to create duplicate generated diffs, review surfaces continue to include repeated skill text, and the single-authored-skill-source migration remains incomplete.

The next release should be `v0.1.3`, and its release scope should retire the repository-tree generated skill-body install path while keeping adapter archive installation as the public distribution path.

## Goals

- Stop tracking generated public adapter skill bodies under `dist/adapters/**/skills`.
- Keep `skills/` as the only authored skill source.
- Keep `dist/adapters/manifest.yaml` and `dist/adapters/README.md` as tracked adapter metadata and install guidance.
- Keep generated adapter archives as the public install surface.
- Validate generated adapter output from temporary build output or release artifact output rather than tracked generated skill trees.
- Preserve Codex, Claude Code, and opencode adapter support.
- Preserve token-cost benchmark behavior that uses public adapter output rather than `.codex/skills/`.
- Publish `v0.1.3` with release notes, adapter archive evidence, and release validation for the new source layout.
- Update affected root contributor and workflow guidance so the retired repository-tree adapter skill-body install model is no longer presented as the active contract.
- Avoid changing skill behavior in this cleanup slice.

## Non-goals

- Do not remove support for any adapter.
- Do not change workflow stage order.
- Do not rewrite Git history.
- Do not hand-edit generated adapter output.
- Do not change public skill text except where required to remove obsolete repository-tree generated-output references.
- Do not move `docs/changes/0001-skill-validator/` in this slice.
- Do not optimize `workflow`, `implement`, `code-review`, or other high-cost public skills in this slice.
- Do not add new token-cost threshold gates in this slice.
- Do not republish or redo the `v0.1.2` archive-introduction release.
- Do not treat this as a main-branch-only cleanup with release follow-up deferred; the requested continuation is a `v0.1.3` release slice.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to reviewable, traceable, trustworthy automation by keeping authored skill content in one source tree and validating generated adapter output through reproducible release and build evidence instead of repeated tracked copies.

## Context

`CONSTITUTION.md` says `skills/` is the only authored skill source and that public adapter packages under `dist/adapters/` remain tracked generated installable output during the compatibility window.

The accepted single-authored-skill-source proposal chose the long-term direction of canonical skills under `skills/`, small tracked adapter metadata, and generated public adapter packages distributed through release artifacts after packaging and install docs are ready.

The accepted public adapter artifact migration proposal kept `dist/adapters/**/skills` tracked for `v0.1.2` because `v0.1.1` had no downloadable adapter archives. It identified `v0.1.3` or later as the earliest likely release for tracked adapter skill-body removal unless compatibility policy changed.

PR #51 completed the archive-introduction and release-evidence slice. It added adapter archive generation and validation, adapter artifact metadata and checksums, install guidance, release notes, release verification evidence, retained-fixture rationale, and token-cost evidence while preserving tracked `dist/adapters/**/skills`.

The `v0.1.2` release was published on 2026-05-13 with these adapter archives attached:

```text
rigorloop-adapter-codex-v0.1.2.zip
rigorloop-adapter-claude-v0.1.2.zip
rigorloop-adapter-opencode-v0.1.2.zip
```

The next decision can therefore focus on whether the compatibility window is complete enough to retire the tracked generated public adapter skill bodies.

## Compatibility-window precondition

The compatibility-window precondition is satisfied when a stable public release exists that:

- keeps repository-tree adapter packages under `dist/adapters/`;
- publishes per-adapter downloadable archives;
- records adapter artifact metadata and checksums;
- documents both install paths or the transition path.

`v0.1.2` satisfies this precondition. The `v0.1.3` release can therefore remove tracked generated public adapter skill bodies without shortening the accepted compatibility window.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Do not redo PR #51. | in scope | Non-goals; Context |
| Do not combine all deferred work into one large PR. | in scope | Non-goals; Recommended direction |
| Publish `v0.1.2` first if not done. | satisfied precondition | Context; Decision log |
| Create a proposal to stop tracking generated public adapter skill bodies. | in scope | Problem; Goals; Recommended direction |
| Release `v0.1.3`. | in scope | Goals; Recommended direction; Testing and verification strategy; Rollout and rollback |
| Move the skill-validator proof pack only when references can be updated safely. | deferred follow-up | Non-goals; Open questions; Follow-on artifacts |
| Optimize high-cost public skills and token cost separately. | deferred follow-up | Non-goals; Follow-on artifacts |
| Preserve adapter support. | in scope | Goals; Non-goals; Risks and mitigations |
| Avoid breaking users who rely on adapters. | in scope | Rollout and rollback; Risks and mitigations |

## Options considered

### Option 1: Keep tracking `dist/adapters/**/skills`

This preserves the compatibility-window repository-tree install model indefinitely.

Advantages:

- Users can continue copying adapter skill trees from the repository.
- Existing tracked-output comparisons stay close to the current model.
- The immediate change is small.

Disadvantages:

- Skill changes continue to produce repeated generated diffs.
- Generated skill bodies continue to look like authored source.
- Review, token-cost, and static analysis workflows keep seeing duplicated public skill text.
- The single-authored-skill-source migration remains incomplete even though archive distribution now exists.

### Option 2: Stop tracking generated adapter skill bodies in `v0.1.3` and keep archive installation as the public path

This completes the source-boundary migration after the `v0.1.2` archive-introduction release.

Advantages:

- `skills/` becomes visibly authoritative as the only authored skill source.
- Ordinary diffs no longer include repeated generated adapter skill text.
- Release artifacts remain available as the public adapter install surface.
- Adapter validation can focus on generated output from canonical skills.

Disadvantages:

- Users who were copying adapter skill trees from the current repository branch need to switch to release archives.
- Validation and docs that still assume tracked adapter skill bodies need coordinated updates.
- `v0.1.3` release evidence, token-cost evidence, and release notes need to clearly communicate repository-tree skill-body retirement.

### Option 3: Land a main-branch cleanup first and publish `v0.1.3` later

This separates repository cleanup from release publication.

Advantages:

- Keeps the cleanup PR smaller.
- Lets release evidence be prepared after validation migration is complete.

Disadvantages:

- Leaves the public release transition unfinished after the cleanup.
- Creates an interim state where main has removed tracked skill bodies but no release has announced the retirement.
- Conflicts with the requested continuation to release `v0.1.3`.

### Option 4: Wait for another compatibility release before untracking

This extends the overlap period beyond `v0.1.2`.

Advantages:

- Gives users more time to move from repository-tree copying to release-archive installation.
- Reduces short-term compatibility risk.

Disadvantages:

- Continues duplicate generated diffs for another release.
- Keeps the repository in a half-migrated state after the archive path has already shipped.
- Delays the accepted single-authored-source cleanup without a known additional technical prerequisite.

## Recommended direction

Choose Option 2.

Proceed with a focused `v0.1.3` release slice now that `v0.1.2` has shipped with adapter archives and install evidence. The change should remove generated adapter skill bodies from tracked source, update validation to use generated output, and publish `v0.1.3` with release notes and evidence for the new source layout.

The default tracked adapter support surface should remain small:

```text
dist/adapters/manifest.yaml
dist/adapters/README.md
```

The spec must explicitly list any additional non-skill adapter files that remain tracked, such as adapter instruction entrypoints or command wrappers. Do not leave the retained `dist/adapters/` boundary implicit.

The steady-state model should become:

```text
Authored source:
  skills/

Tracked adapter metadata and guidance:
  dist/adapters/manifest.yaml
  dist/adapters/README.md

Generated public adapter packages:
  GitHub release archives
  temporary build output used by validation

Untracked/generated:
  dist/adapters/**/skills
  .codex/skills
```

The implementation should update validation so adapter correctness is proved from generated temporary output or downloaded/generated release artifacts, not from tracked generated skill trees.

This proposal intentionally does not bundle the skill-validator proof-pack move, broad public skill simplification, progressive-loading optimization, or new token-cost thresholds. Those are valid follow-up slices, but they should keep their own proposals or plans.

## Tracked adapter surface after migration

The tracked surface must be exact in the follow-on spec.

Expected tracked files:

```text
dist/adapters/README.md
dist/adapters/manifest.yaml
```

Potentially retained only if the spec explicitly keeps them:

```text
dist/adapters/codex/AGENTS.md
dist/adapters/claude/CLAUDE.md
dist/adapters/opencode/AGENTS.md
dist/adapters/opencode/.opencode/commands/*.md
```

Untracked generated skill bodies:

```text
dist/adapters/codex/.agents/skills/**
dist/adapters/claude/.claude/skills/**
dist/adapters/opencode/.opencode/skills/**
```

If adapter instruction files or opencode command wrappers remain tracked, the spec should classify them as tracked install guidance or command metadata, not authored skill source.

## Adapter validation after untracking

After this change, validation must not require tracked files under:

```text
dist/adapters/codex/.agents/skills/
dist/adapters/claude/.claude/skills/
dist/adapters/opencode/.opencode/skills/
```

Validation should prove adapter correctness by generating adapter output into a temporary release-output directory and validating that output. Any existing drift check that compares canonical skills to tracked `dist/adapters/**/skills` should be retired or replaced with temporary-output validation.

Acceptance should include tests or validation coverage that fail if generated skill bodies under `dist/adapters/**/skills` are still required and pass using generated temporary adapter output.

## Adapter install guidance

`dist/adapters/README.md` should become the repository-visible install-contract surface. It should state:

- `skills/` is the canonical authored source;
- generated adapter skill bodies are not tracked in the repository after this migration;
- users install adapters from GitHub release archives;
- the archive names for Codex, Claude Code, and opencode;
- the target install roots for each adapter;
- where artifact metadata and checksums are recorded;
- `dist/adapters/manifest.yaml` remains the support matrix.

The README should describe active behavior rather than retaining stale defensive warnings about old generated skill-body paths.

## Root guidance alignment

This release changes the public adapter installation and generated-output ownership contract.

The implementation must audit and update affected root and workflow guidance, including:

- `CONSTITUTION.md`
- `AGENTS.md`
- `docs/workflows.md`
- `dist/adapters/README.md`
- release notes for the target version

The updated guidance should state the active rule:

- canonical authored skills live under `skills/`;
- generated public adapter skill bodies are not tracked source after this migration;
- users install public adapters from GitHub release archives;
- `dist/adapters/manifest.yaml` and `dist/adapters/README.md` remain the tracked support and install-guidance surfaces;
- generated adapter output is validated from temporary build output or release artifact output, not from tracked adapter skill-body trees.

If any listed surface is not changed, the implementation should record a short unaffected rationale explaining why its current wording is already compatible with this release.

Historical compatibility-window wording should be removed from active rules or made explicitly version-qualified:

```text
v0.1.2 kept repository-tree adapter skill bodies during the compatibility window.
v0.1.3 and later install public adapters from release archives.
```

Root guidance should point ordinary contributors to `dist/adapters/README.md` as the active adapter install-contract surface rather than duplicating archive names, install roots, checksum metadata, and release-asset details.

## Expected behavior changes

Before this change:

```text
skill edit -> canonical skill diff + generated dist adapter skill diffs
```

After this change:

```text
skill edit -> canonical skill diff + adapter generation or validation evidence
```

Before this change:

```text
users may copy tracked adapter skill bodies from the repository tree
```

After this change:

```text
users install adapter archives from release assets
```

Before this change:

```text
dist/adapters/**/skills is tracked generated output
```

After this change:

```text
dist/adapters/ keeps metadata and install guidance only
```

For `v0.1.3`, users should observe release notes that explicitly retire repository-tree generated skill-body installation and point to adapter release archives.

## Architecture impact

No runtime architecture change is expected.

The affected boundaries are repository packaging, generated-output validation, release evidence, documentation, and token-cost benchmark inputs. Likely affected surfaces include:

```text
CONSTITUTION.md
AGENTS.md
docs/workflows.md
dist/adapters/
docs/releases/
docs/reports/adapter-artifacts/releases/
docs/reports/token-cost/releases/
scripts/build-adapters.py
scripts/validate-adapters.py
scripts/release-verify.sh
scripts/validate-release.py
scripts/test-adapter-distribution.py
scripts/run-token-cost-benchmarks.py
```

The implementation should remove or version-qualify stale compatibility-window wording from affected guidance surfaces.

The final design should preserve repo-owned scripts as the validation authority and keep GitHub Actions as thin wrappers where release automation is involved.

## Testing and verification strategy

Validation should prove that canonical skills validate, generated adapter archives can be built, generated adapter archives validate, release artifact metadata and checksums validate, release notes and install docs point users to archives, token-cost benchmark inputs remain public adapter output, and no generated adapter skill bodies remain tracked.

Validation should include a root-guidance audit proving that affected contributor and workflow guidance no longer presents tracked `dist/adapters/**/skills` as the active public install path. The audit should verify:

- `CONSTITUTION.md` reflects archive-based public adapter installation or records why no change is needed;
- `AGENTS.md` reflects archive-based public adapter installation or records why no change is needed;
- `docs/workflows.md` points users and agents to the active adapter install surface;
- `dist/adapters/README.md` remains the install-contract surface;
- no root guidance directs ordinary users to install from retired tracked adapter skill-body paths as the active model.

Because this is a `v0.1.3` release slice, `v0.1.2` token-cost evidence remains historical baseline evidence only. The release should add `v0.1.3` token-cost evidence or an explicitly accepted release policy exception. At minimum, validation must prove token-cost benchmark inputs still use generated public adapter output or release archive output after tracked `dist/adapters/**/skills` are removed.

Likely commands include:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-adapters.py --version v0.1.3 --output-dir <release-output-dir>
python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3
python scripts/test-adapter-distribution.py
python scripts/run-token-cost-benchmarks.py --release v0.1.3 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>
python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.3.yaml
bash scripts/release-verify.sh v0.1.3
git diff --check --
```

The `<public-adapter-skill-source>` should point at generated public adapter release output or temporary public adapter output, not `.codex/skills/`.

## Acceptance criteria

- Generated public adapter skill bodies under `dist/adapters/**/skills` are no longer tracked.
- `dist/adapters/manifest.yaml` and `dist/adapters/README.md` remain tracked.
- Adapter correctness is validated from temporary build output or release artifact output.
- `dist/adapters/README.md` is the active adapter install-contract surface.
- Affected root guidance surfaces are audited.
- `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` are updated or have explicit unaffected rationale.
- Active guidance points ordinary users to release archives or `dist/adapters/README.md` as the install-contract surface.
- Stale compatibility-window wording is removed or version-qualified.
- The proposal, spec, and plan do not rely on retired tracked adapter skill-body paths as active public install guidance.
- `v0.1.3` release notes explain the repository-tree adapter skill-body retirement.
- Token-cost benchmark source validation uses generated public adapter output or release archive output, not `.codex/skills/`.

## Rollout and rollback

Rollout should happen after the published archive-install release is confirmed. That precondition is currently satisfied by `v0.1.2`.

The rollout should:

- remove tracked generated adapter skill bodies;
- keep tracked adapter metadata and install guidance;
- update docs that still describe repository-tree skill bodies as the active public install surface;
- update validation to build and validate adapter output outside tracked source;
- create `v0.1.3` release notes that retire repository-tree adapter skill-body installation;
- publish `v0.1.3` with per-adapter archives attached.

Rollback is straightforward because the old generated adapter skill bodies can be regenerated from `skills/`:

```text
restore tracked dist/adapters/**/skills from generated output
keep archive metadata as historical evidence
defer untracking to a later release
```

If validation cannot be updated safely, keep tracked adapter skill bodies, document the blocker, and create a focused validator migration follow-up.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Users still rely on repository-tree adapter skill copying. | Keep release notes and `dist/adapters/README.md` explicit about release archives and install roots. |
| Adapter validation accidentally stops checking real generated output. | Require validation against temporary build output or release artifact output. |
| Token benchmarks regress to `.codex/skills/`. | Keep benchmark source set to generated public adapter output or archive output. |
| Docs continue to mention retired tracked skill-body paths. | Update release notes and install docs in the same slice. |
| Generated output drift becomes invisible. | Replace tracked-output drift checks with deterministic generation and validation checks. |
| The change grows into deferred work from PR #51. | Keep skill-validator migration, broad skill optimization, and token threshold work out of scope. |
| `v0.1.3` release evidence is incomplete. | Require release notes, adapter artifact metadata, checksums, token-cost evidence or approved exception, and `release-verify.sh v0.1.3`. |

## Open questions

- Should release validation for the retirement release require downloading published `v0.1.2` archives, or is generated temporary public adapter output sufficient?
- Should `dist/adapters/README.md` retain a short historical note for `v0.1.1` and `v0.1.2`, or only describe the active archive-install model?
- Which validation checks currently assume tracked `dist/adapters/**/skills`, and should they be replaced or retired?
- Which non-skill adapter files under `dist/adapters/` remain tracked for `v0.1.3`?
- Is a full `v0.1.3` token-cost report required, or is a scoped benchmark-source validation plus approved release policy exception sufficient?

These questions do not block proposal review, but they should be resolved before implementation planning.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-13 | Treat `v0.1.2` publication as the compatibility-window precondition for adapter untracking. | `v0.1.2` is published with per-adapter archives attached. | Redoing PR #51; untracking before archives shipped. |
| 2026-05-13 | Target the generated adapter skill-body retirement at `v0.1.3`. | The user requested `v0.1.3`, and release evidence is required to announce the public install-path change. | Main-branch-only cleanup with release deferred. |
| 2026-05-13 | Propose a focused adapter untracking release slice. | The archive path exists, and the remaining generated skill-body cleanup is separable. | Combining skill-validator migration, high-cost skill optimization, and token threshold gates. |
| 2026-05-13 | Keep `dist/adapters/manifest.yaml` and `dist/adapters/README.md` tracked. | The repository still needs a small support matrix and install-contract surface. | Removing all `dist/adapters/` content. |

## Next artifacts

```text
proposal-review
spec or spec amendment
spec-review
architecture if validation or release boundaries need a design record
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Spec: [Stop Tracking Generated Public Adapter Skill Bodies](../../specs/stop-tracking-generated-public-adapter-skill-bodies.md)

Deferred follow-up slices remain:

```text
docs/changes/0001-skill-validator proof-pack migration
high-cost public skill progressive-loading optimization
new token-cost threshold policy, if desired
```

## Readiness

Accepted after clean proposal-review.

The release precondition for this proposal is satisfied: `v0.1.2` is published and per-adapter archives are attached. This proposal chooses `v0.1.3` as the release target. Downstream specification is now drafted in `specs/stop-tracking-generated-public-adapter-skill-bodies.md`.
