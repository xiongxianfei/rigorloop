# Bounded Plan Index and Completed-Plan Archive Review Resolution

## Summary

Closeout status: open

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: code-review-m2-r1

## Resolution Entries

### code-review-m2-r1

#### BPIX-M2-CR1

Finding ID: BPIX-M2-CR1
Disposition: accepted
Status: open
Owner: implementer
Owning stage: implement
Chosen action: Extend terminal conservation validation to scoped plan-body lifecycle marker changes.
Rationale: A plan body can acquire `Plan lifecycle state: done`, `abandoned`, or `superseded` without `docs/plan.md` or `docs/plan-archive.md` being in the explicit validation path. The validator must catch missing recent/archive placement for that scoped plan body.
Required outcome: Explicit terminal plan-body markers in validation scope must require exactly one valid recent/archive terminal location, except legacy prose-only plans remain unknown and migration-proof-owned.
Safe resolution path: Add a failing fixture for plan-body-only terminal conservation, update the conservation trigger to include scoped explicit terminal plan bodies, rerun targeted lifecycle tests and validation, and return M2 to code-review.
Validation target: `python scripts/test-artifact-lifecycle-validator.py` includes the new plan-body-only terminal conservation regression and passes.
Validation evidence: pending

### plan-review-r1

No material findings.

### proposal-review-r1

No material findings.

### spec-review-r1

## Findings

#### BPIX-SR1

Finding ID: BPIX-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add a deterministic plan body lifecycle-state marker.
Rationale: Terminal-plan conservation cannot safely infer lifecycle state from prose-heavy plan bodies, so the spec needs a compact validator-owned marker.
Required outcome: Define the deterministic source of terminal lifecycle state for plan bodies before validators or test specs rely on terminal-plan conservation.
Safe resolution path: Add requirements that identify one validator-owned terminal-state source, such as a normalized plan-body status field or a narrowly defined set of accepted lifecycle status lines. Specify unknown, missing, contradictory, and legacy prose behavior. Then update examples, edge cases, and acceptance criteria so tests can prove terminal detection without broad prose guessing.
Validation target: Revised `specs/plan-index-lifecycle-ownership.md` contains deterministic terminal lifecycle detection rules and the review rerun confirms BPIX-SR1 is resolved.
Resolution: Added a deterministic plan body lifecycle-state marker. Validators now detect terminal plan state only from the explicit top-level `## Status` fields `Plan lifecycle state` and `Terminal disposition`. The spec defines allowed values, terminal values, malformed and contradictory marker behavior, and legacy prose-only behavior. Validators must not infer terminal state from arbitrary plan prose.
Validation evidence: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md --path specs/plan-index-lifecycle-ownership.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-log.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md`, and `git diff --check --` passed after the spec revision. Lifecycle validation still reports the existing lifecycle-language warning for this spec.

### spec-review-r2

No material findings.

#### BPIX-SR2

Finding ID: BPIX-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define active supersession context as a structural marker in `docs/plan.md`.
Rationale: Superseded entries can remain in the common-read index only when they carry an explicit replacement pointer and rationale; otherwise, usefulness is too subjective for validation.
Required outcome: Make superseded archive placement testable and reviewable without relying on unstated judgment.
Safe resolution path: Define a structural rule or required rationale for superseded entries. For example, require `docs/plan.md` Superseded entries to include an active replacement link plus an explicit active-context marker or short rationale, and require entries without that marker to be archived. Alternatively, make superseded archive placement a manual code-review-owned semantic judgment and remove validator-implied enforcement for that boundary.
Validation target: Revised `specs/plan-index-lifecycle-ownership.md` defines the active-supersession boundary and the review rerun confirms BPIX-SR2 is resolved.
Resolution: Defined active supersession context as a structural marker in `docs/plan.md`. Superseded entries kept in the common-read index must include a superseded plan link, replacement plan link through `superseded by:`, and non-empty `active-context:` rationale. Entries without that marker belong in `docs/plan-archive.md`. Validators enforce structural fields, while code review owns rationale quality.
Validation evidence: `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md --path specs/plan-index-lifecycle-ownership.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-log.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md`, and `git diff --check --` passed after the spec revision. Lifecycle validation still reports the existing lifecycle-language warning for this spec.
