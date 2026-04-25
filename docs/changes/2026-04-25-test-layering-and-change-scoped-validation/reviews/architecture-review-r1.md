# Architecture Review R1

Review ID: architecture-review-r1
Stage: architecture-review
Round: 1
Reviewer: Codex architecture-review skill
Target: docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md
Status: revise

## Scope

Reviewed the architecture against `specs/test-layering-and-change-scoped-validation.md`, the accepted proposal, current validation scripts, and repository governance.

## Dimension Results

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | Broad-smoke trigger discovery and manual proof storage are underspecified. |
| Boundary clarity | concern | Selector, wrapper, and downstream validators are mostly separated, but artifact-trigger ownership is unclear. |
| Data ownership | concern | Manual proof durable storage is not designed. |
| Interface safety | concern | Fallback behavior is not settled enough for planning. |
| Failure handling | concern | Unclassified fallback behavior is ambiguous. |
| Security/privacy | pass | Repo-relative output, no `eval`, and no secret logging are addressed. |
| Performance/scalability | pass | Selector is path-based and does not run checks. |
| Observability | concern | Trigger-source visibility is not modeled. |
| Testing feasibility | concern | Missing trigger and manual-proof models make fixture expectations incomplete. |
| Complexity discipline | pass | The design stays path-based and avoids new dependencies. |
| ADR quality | pass | No separate ADR is required for this slice. |
| Plan readiness | concern | Revision is needed before execution planning. |

## Findings

### AR1-F1: Broad-smoke trigger discovery is underspecified

Finding ID: AR1-F1

Evidence: The spec requires broad smoke to come from authoritative sources including selector mode, `--broad-smoke`, active plan field, test-spec requirement, review-resolution requirement, and release metadata requirement (`specs/test-layering-and-change-scoped-validation.md:403`-`418`). The architecture says the selector owns broad-smoke trigger detection (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:18`), but `SelectionRequest` only models mode, paths, base/head, release version, explicit broad-smoke, and repo root (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:80`-`89`). The control flow only says to add broad-smoke state without defining how artifact-based trigger sources are discovered or passed (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:170`-`175`).

Required outcome: The architecture must state how each authoritative broad-smoke trigger source is detected, passed to the selector, represented in selector output, and consumed by `scripts/ci.sh` or downstream handoff gates.

Suggested resolution: Add a broad-smoke trigger-source subsection with a small `TriggerSource` model. For v1, either have the selector read explicit context paths for active plan, test spec, review-resolution, and release metadata, or state that those artifacts are evaluated by their owning validators and passed to the selector through an explicit broad-smoke override that preserves the original source in `rationale` or an optional `broad_smoke_triggers` field.

### AR1-F2: Manual proof has no durable data ownership or closeout interface

Finding ID: AR1-F2

Evidence: The architecture claims coverage for structured manual proof records and closeout behavior (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:29`). The spec requires manual proof records to include check ID, result, why manual, performer, evidence location, date, temporary blocked/not-run rationale, owner, and follow-up (`specs/test-layering-and-change-scoped-validation.md:432`-`448`). The architecture only says manual proof remains durable in workflow artifacts and blocks downstream closeout when missing or failed (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:260`, `286`), without naming the storage location, parseable shape, or validation owner.

Required outcome: The architecture must define where manual proof records live, which fields are required, and which validator or workflow stage enforces final handoff behavior.

Suggested resolution: Add a manual-proof data model. For change-local proof, use `docs/changes/<change-id>/verify-report.md` or `change.yaml` validation entries if the current schema is sufficient; for release proof, use the release metadata smoke matrix. State that selector output can name manual check IDs, but `verify` owns closeout validation of required manual-proof fields.

### AR1-F3: Conservative fallback behavior is not a chosen design

Finding ID: AR1-F3

Evidence: The spec requires any conservative fallback set to be repository-defined and deterministic, and requires blocking instead of guessing when no safe fallback exists (`specs/test-layering-and-change-scoped-validation.md:379`-`391`). The architecture assigns fallback policy to the selector module (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:48`) and repeatedly allows either `blocked` or `fallback` for unclassified paths (`docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md:175`, `252`), but it does not define the fallback set or state that v1 always blocks unclassified paths.

Required outcome: The architecture must choose the v1 behavior for unclassified paths so tests, `ci.sh`, and contributors have one predictable result.

Suggested resolution: Prefer the simpler v1 rule: unclassified paths return `status: "blocked"` with `unclassified-path`; `fallback` remains a supported status for future repository-defined fallback sets. If fallback is retained in v1, define the exact check IDs and version-inference behavior for the fallback set.
