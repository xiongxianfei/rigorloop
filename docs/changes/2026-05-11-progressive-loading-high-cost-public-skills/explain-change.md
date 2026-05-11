# Progressive Loading High-Cost Public Skills Explain Change

## Status

implementation rationale recorded; final explain-change review remains downstream after M4 code-review

## Summary

This change makes the measured high-cost public skills progressively loadable without changing workflow order, release token-friendliness gates, benchmark schema, or adapter layout.

The implementation added compact quick operating guides to `workflow`, `implement`, and `code-review`; added bounded handoff-state inspection guidance to `implement`; compressed repeated public skill prose where safe; moved or accounted workflow detail in contributor-facing workflow guidance and the optimization report; regenerated local and public adapter output; and reran static plus dynamic token-cost evidence.

## Why The Change Was Needed

The v0.1.1 Token-Friendliness report showed three concrete cost drivers:

- `implement-handoff` produced a 20,738 estimated-token command output.
- `workflow` was the largest public skill at 6,674 estimated tokens.
- `code-review` was above the warning range at 4,726 estimated tokens.

All ten required transition benchmarks also read active public skill files. The accepted direction was progressive loading: help the agent do the right narrow read first, not just delete text.

## What Changed

| Area | Change | Reason |
|---|---|---|
| `workflow` skill | Added quick guide and compressed long routing/lifecycle detail while preserving required safety anchors. | Route from a short top section while keeping claim boundaries and milestone safety. |
| `implement` skill | Added quick guide and `Handoff inspection budget`. | Start milestone handoff checks from active plan state and avoid broad repository searches as the first state-discovery step. |
| `code-review` skill | Added quick guide and compressed repeated input/template prose. | Preserve independent-review, mixed-evidence, material-finding, detailed-record, handoff, stop-condition, and result-format contracts while reducing repeated text. |
| `docs/workflows.md` | Added workflow detail ownership guidance. | Ensure summarized workflow safety topics have a durable owner surface. |
| generated output | Regenerated `.codex/skills/` and public adapters for Codex, Claude, and opencode. | Ensure dynamic benchmarks measure current public skill output. |
| optimization report | Recorded static and dynamic before/after evidence. | Make token-cost impact and remaining warnings reviewable. |

## Evidence Summary

Static measurement changed total skill cost from 54,294 to 52,843 estimated tokens.

Targeted skill sizes changed as follows:

- `workflow`: 6,674 to 4,857 estimated tokens.
- `implement`: 3,542 to 3,963 estimated tokens because the handoff inspection budget added new safety guidance.
- `code-review`: 4,726 to 4,671 estimated tokens.

Dynamic benchmarking reran the full required suite against regenerated public Codex adapter skills. The largest targeted command output improved from `implement-handoff` at 20,738 estimated tokens to `verify-final-pack` at 3,515 estimated tokens. `implement-handoff` itself fell to 3,098 estimated tokens.

Whole-skill-style reads persisted across the required suite, and broad-search signals did not fully improve. The optimization report records those remaining warnings instead of claiming complete runtime-cost resolution.

## Validation

Key validation evidence is recorded in `change.yaml` and the active plan. It includes:

- static skill validator tests;
- canonical skill validation;
- static token measurement;
- generated skill and adapter drift checks;
- adapter validation;
- adapter distribution tests;
- full required dynamic benchmark execution;
- token-cost measurement and report-validation tests;
- change metadata validation;
- artifact lifecycle validation; and
- diff hygiene checks.

## Remaining Workflow State

M4 implementation is ready for `code-review`. Final `explain-change`, `verify`, and `pr` readiness are not claimed until M4 review closes and downstream final closeout stages run.
