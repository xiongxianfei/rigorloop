# Proposal Review: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: proposal-review
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: `FID-01`, `FID-02`, `FID-03`, `FID-04`, `FID-05`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/proposal-review.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: open questions must be resolved in the proposal before spec or plan
- Immediate next stage: proposal author updates the proposal; then proposal-review may be rerun or the owner may accept the resolved proposal for spec authoring

## Scope

Reviewed proposal:

- `docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`

This review is isolated. It records findings and does not automatically hand off to downstream stages.

## Findings

### FID-01 - Lockfile schema version bump

Finding ID: FID-01
Severity: major
Location: Open questions section
Evidence: Multi-root adapters, especially opencode, require `installed_roots` and `root_hashes`, while Codex remains single-root.
Required outcome: Define lockfile schema versioning strategy before spec or implementation relies on multi-root entries.
Safe resolution path: Use `schema_version: 2` for multi-root support, preserve backward-compatible parsing for existing Codex single-root entries, and document migration behavior in the spec.

### FID-02 - Opencode command aliases

Finding ID: FID-02
Severity: major
Location: Open questions section
Evidence: opencode metadata may declare command aliases under `.opencode/commands`.
Required outcome: Define command-alias enforcement rules.
Safe resolution path: Require command aliases for new archives when metadata declares aliases. For older archives lacking aliases, emit a warning rather than a hard block. Descriptor validation should flag missing declared aliases.

### FID-03 - Proxy support implementation

Finding ID: FID-03
Severity: concern
Location: Open questions section
Evidence: Node env-proxy support is version-dependent; adding a programmatic Undici dispatcher increases first-slice dependency and runtime complexity.
Required outcome: Decide first-slice dependency scope.
Safe resolution path: Use Node built-in env-proxy support and diagnostics for the first implementation slice. Consider Undici proxy dispatcher support in a later follow-up if needed.

### FID-04 - Safe proxy reporting

Finding ID: FID-04
Severity: major
Location: Open questions section
Evidence: Proxy diagnostics can accidentally expose credentials, private hostnames, internal proxy URLs, tokens, or raw environment variable values.
Required outcome: Specify safe facts to report.
Safe resolution path: Report only adapter name, adapter release version, detected proxy environment variable names, Node env-proxy support status, download failure class, trusted public archive URL, and suggested `--from-archive` fallback.

### FID-05 - Codex lockfile single-root handling

Finding ID: FID-05
Severity: major
Location: Open questions section
Evidence: Codex continues as single-root `.agents/skills`, while new multi-root adapters could complicate lockfile logic.
Required outcome: Decide whether Codex keeps the existing single-root lockfile shape.
Safe resolution path: Keep Codex entries using existing `installed_root`; multi-root adapters use `installed_roots` and `root_hashes`. CLI and validation logic must handle both entry types concurrently.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Problem clarity | pass | CLI adapter gap and proxy-download problem are clear. |
| User value | pass | Multi-adapter init improves adoption. |
| Option diversity | pass | Alternatives include constants-only, fallback-only, and contract-first approaches. |
| Decision rationale | concern | Direction is sound, but open questions must be resolved before downstream reliance. |
| Scope control | pass | Non-goals exclude npm packaging, canonical skill source changes, and unrelated CLI commands. |
| Architecture awareness | concern | Adapter descriptors and lockfile boundaries are named, but lockfile schema decisions were open. |
| Testability | pass | Fixture-backed tests and hermetic proxy tests are identified. |
| Risk honesty | pass | Proxy leakage, opencode aliases, and lockfile risks are named. |
| Rollout realism | concern | Requires explicit lockfile versioning and compatibility behavior. |
| Readiness for spec | changes-requested | Proposal needs resolved decisions before spec authoring. |

## Scope Preservation

Scope preservation result: pass with changes requested.

The proposal preserves the requested adapter expansion, proxy diagnostics, local archive fallback, verified archive trust boundary, Codex `.agents/skills` install root, and exclusion of unrelated CLI work.

## Blocking Questions

The review supplied owner answers for all open questions:

- Use `schema_version: 2` for multi-root support.
- Require opencode command aliases when metadata declares them for new archives; warn for older archives lacking aliases.
- Use Node built-in env-proxy support and diagnostics for the first slice.
- Report only safe proxy facts.
- Keep Codex on the existing single-root `installed_root` lockfile field.

## Suggested Proposal Edits

- Move open-question answers into the proposal as decisions.
- Replace lockfile open question with `schema_version: 2` direction.
- Define mixed lockfile entry handling for Codex single-root and multi-root adapters.
- Define opencode alias enforcement and older-archive warning behavior.
- Define first-slice proxy implementation scope and exact safe reporting facts.

## Readiness

Changes requested before spec or plan. Once the proposal incorporates the supplied answers, it can proceed to proposal-review rerun or owner acceptance before spec authoring.
