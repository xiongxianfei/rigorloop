# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M1 working tree implementation for `rigorloop new-change`
Status: changes-requested

## Scope

Reviewed M1 command contract helpers and metadata generation against the approved `new-change` spec, active test spec, active plan milestone, actual working tree diff, and recorded validation evidence.

## Review inputs

- Diff surface: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/lib/new-change.js`, `packages/rigorloop/test/cli.test.js`, active plan and change metadata updates.
- Governing spec: `specs/rigorloop-cli-new-change.md`.
- Test spec: `specs/rigorloop-cli-new-change.test.md`.
- Plan milestone: `docs/plans/2026-05-16-rigorloop-cli-new-change.md` M1.
- Architecture: `docs/architecture/system/architecture.md`.
- Validation evidence inspected:
  - `npm test --prefix packages/rigorloop`.
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path specs/rigorloop-cli-new-change.md --path specs/rigorloop-cli-new-change.test.md --path docs/plans/2026-05-16-rigorloop-cli-new-change.md --path docs/plan.md --path docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.
  - `git diff --check -- packages/rigorloop specs/rigorloop-cli-new-change.test.md docs/plans/2026-05-16-rigorloop-cli-new-change.md docs/plan.md docs/changes/2026-05-16-rigorloop-cli-new-change/change.yaml`.

## Diff summary

M1 adds a package-local `new-change` helper module with change-id, classification, risk, and profile validators plus deterministic metadata rendering. The CLI now exposes `new-change` in help, dispatches the command, returns invalid-usage JSON errors for invalid inputs, and supports a no-write `--dry-run --json` result containing the planned metadata content and command-specific `change` object. Package tests now cover the M1 command surface, option domains, metadata determinism, YAML quoting, and JSON envelope behavior while preserving existing `init` tests.

## Findings

### CR1-F1 - Generated change metadata omits required `review.unresolved_items`

Finding ID: CR1-F1
Severity: blocker
Location: `packages/rigorloop/dist/lib/new-change.js:42`

Evidence: The approved spec requires generated `change.yaml` to include `review.status: pending` and `review.unresolved_items: 0` in the normative shape (`specs/rigorloop-cli-new-change.md`, R30). The current renderer returns only:

```yaml
review:
  status: "pending"
```

The M1 test for deterministic metadata asserts `review.status: pending` but does not assert `review.unresolved_items: 0` (`packages/rigorloop/test/cli.test.js:464`).

Required outcome: Generated metadata must include `review.unresolved_items: 0`, and M1 tests must directly prove the required field is present in the deterministic output.

Safe resolution path: Add `unresolved_items: 0` under `review` in `renderChangeMetadata`, extend `TNC-006` to assert it, rerun `npm test --prefix packages/rigorloop`, selected M1 CI, and diff check, then rerun `code-review`.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | block | CR1-F1 violates R30 by omitting a required field from generated `change.yaml`. |
| Test coverage | concern | The M1 tests cover most value domains and output shape, but they miss direct proof for `review.unresolved_items: 0`. |
| Edge cases | pass | M1 named value-domain and unsafe-path cases are covered by `TNC-002` through `TNC-005`; filesystem edge cases are M2/M3. |
| Error handling | pass | Invalid usage maps to `status: error`, exit code `4`, and field-specific errors in the reviewed M1 paths. |
| Architecture boundaries | pass | The change stays inside the existing CLI package, uses a package-local helper, and adds no network, persistence, or dependency changes. |
| Compatibility | concern | The missing metadata field can produce scaffolded change metadata that does not match the approved first-slice shape. |
| Security/privacy | pass | M1 validators reject unsafe IDs and classification tokens; metadata rendering does not include local paths or environment data. |
| Derived artifact currency | pass | No generated adapter or skill output is affected by this milestone. |
| Unrelated changes | pass | The reviewed M1 diff is limited to CLI helper/dispatch/tests plus lifecycle handoff artifacts. |
| Validation evidence | concern | Recorded validation is relevant and passing, but it did not catch CR1-F1. |

## Recommended next stage

Stop after this isolated code review. Record review-resolution for `CR1-F1`, fix the renderer and test coverage in M1, return M1 to `review-requested`, and rerun `code-review` with a later round.
