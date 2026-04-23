# Multi-agent adapters first public release change explanation

## M1 adapter portability core

M1 adds the shared adapter distribution core before any generated package output is written.

The new adapter model defines the approved first-public-release tools and target paths for Codex, Claude Code, and opencode. This keeps later generator and validator work tied to one source for adapter roots, instruction entrypoints, and per-tool skill locations.

The portable-core validator classifies one canonical `SKILL.md` at a time. It validates portable names and descriptions, permits explicitly transformed `argument-hint` metadata for non-Codex adapters, rejects unsupported frontmatter or Codex-only assumptions from non-Codex adapters, and records deterministic inclusion decisions for later manifest generation.

The fixture-driven tests cover the M1 proof surface from the active test spec: adapter path contracts, portable skill inclusion, invalid metadata rejection, Codex-only exclusion reasons, generic artifact path portability, explicit transforms, and deterministic manifest rendering for partial portability.

No `dist/adapters/` files are generated in M1. Generated adapter packages are planned for M2 after the adapter core is reviewable.

## M1 review resolution

The first M1 code-review pass found that manifest exclusion reasons could be rendered as invalid YAML when the human-readable reason contained `: `, such as `Uses unsupported frontmatter: codex-only-field.`.

The follow-up quotes generated manifest reason strings and escapes double-quoted YAML control characters before rendering. The adapter regression suite now includes the unsupported-frontmatter fixture as a manifest-rendering case so the colon-bearing reason path remains covered before M2 writes `dist/adapters/manifest.yaml`.
