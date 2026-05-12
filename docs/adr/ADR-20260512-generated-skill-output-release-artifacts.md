# ADR-20260512-generated-skill-output-release-artifacts: Generated Skill Output and Adapter Release Artifacts

## Status

accepted

## Context

RigorLoop already separates canonical authored skills from generated output. `skills/` is the authored source, `.codex/skills/` is generated local Codex runtime output, and `dist/adapters/` contains generated public adapter packages for Codex, Claude Code, and opencode.

The earlier source-layout and adapter-package ADRs intentionally kept generated trees tracked so first-release compatibility and drift validation were easy to inspect. That decision now creates review and maintenance cost: every skill wording change can appear in the canonical skill, the local Codex mirror, and three public adapter skill trees. It also makes generated output look like ordinary authored Git state.

The approved `specs/single-authored-skill-source-generated-output.md` changes the long-lived generated-output boundary. The architecture must preserve adapter support and reproducible release evidence while reducing duplicate generated skill bodies in day-to-day tracked state.

## Decision

Keep `skills/` as the only authored skill source.

Move generated skill output out of ordinary authored Git state in stages:

1. Remove `.codex/skills/` from tracked Git state first. Keep it as generated local Codex runtime output that can be produced on demand from `skills/`.
2. Keep public adapter skill copies under `dist/adapters/**/skills` tracked during the first slice and during the public compatibility window.
3. Publish generated adapter packages as release artifacts after release-artifact packaging, metadata, validation, benchmark inputs, and install docs are ready.
4. Remove tracked public adapter skill copies only after at least one stable public release has provided downloadable adapter artifacts and release-artifact installation docs while repository-tree adapter installation remains available.

Keep these tracked support and release evidence surfaces:

```text
dist/adapters/manifest.yaml
dist/adapters/README.md
docs/reports/adapter-artifacts/releases/<version>.yaml
```

Do not commit generated adapter archives by default. Generate them in CI or the release workflow, upload them as release assets, and track checksums and provenance metadata.

Use temp-output validation for generated trees that are no longer tracked. For `.codex/skills/`, tracked-file drift checks are replaced by generation and structural validation against non-tracked output. For public adapter skill copies, tracked drift checks remain while those copies are tracked, then move to temp-output or release-artifact validation after the public adapter migration.

## Alternatives considered

### Keep all generated skill copies tracked

Rejected because it preserves the existing review noise, token-cost overcounting risk, drift confusion, and accidental generated-output edit risk.

### Untrack all generated output immediately

Rejected because public users may currently install adapters by copying `dist/adapters/<adapter>/` from the repository tree. Public adapter migration needs release artifacts, install docs, checksums, and a compatibility window.

### Track generated adapter archives in Git

Rejected by default because generated binary or archive files would create repository churn. Release assets plus tracked checksums and metadata provide distribution and reproducibility evidence without making archives authored repository content.

### Move all adapter metadata into release assets only

Rejected for this migration because a small tracked support matrix and install guidance surface keeps adapter support visible after generated skill bodies leave the repository tree.

## Consequences

- Contributors edit skill behavior only in `skills/` or approved canonical templates and generator inputs.
- `.codex/skills/` can be absent from Git without breaking validation after the first migration slice.
- Local Codex mirror validation proves generation rather than tracked-file equality.
- Public adapter skill copies continue to protect current repository-tree installation during the compatibility window.
- Release artifacts become the long-term public adapter distribution surface.
- Adapter releases need tracked artifact metadata with source commit, generator command, archive list, checksums, validation command, and validation result.
- Release validation must be able to validate generated adapter output from temp directories or release artifact directories.
- Token-cost public-surface benchmarks must avoid `.codex/skills/` and use public adapter output, generated temporary adapter output, or release artifact output.
- The earlier ADRs remain valid history for first-release decisions, but this ADR supersedes their tracked generated-output assumptions after the staged migration points defined here.

## Follow-up

- Update the canonical architecture package to describe staged generated-output and adapter release artifact flow.
- Update specs, test specs, plans, docs, scripts, and CI selectors to replace `.codex/skills/` tracked drift checks with temp-output validation.
- Add or retain `dist/adapters/README.md` before public adapter skill copies are untracked.
- Add adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml` for releases that publish adapter archives.
- Preserve public adapter skill copies for at least one stable release after downloadable artifacts and install docs are available.
