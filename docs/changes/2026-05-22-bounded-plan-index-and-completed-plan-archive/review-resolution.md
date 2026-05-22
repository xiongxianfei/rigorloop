# Bounded Plan Index and Completed-Plan Archive Review Resolution

## Summary

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m3-r1
Review closeout: code-review-m4-r1

## Resolution Entries

### code-review-m4-r1

#### BPIX-M4-CR1

Finding ID: BPIX-M4-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: review-resolution
Chosen action: Update plan guidance to include the missing R8a lifecycle ownership points.
Rationale: The finding is directly supported by the approved spec and is fixable inside the current M4 scope without a new product, architecture, or spec decision.
Required outcome: Plan guidance must explicitly include the missing R8a ownership points or record a spec-backed rationale for why another plan-guidance surface satisfies `R8a`.
Safe resolution path: Add concise wording to `skills/plan/SKILL.md` near the existing plan authoring rules that says `implement` owns ongoing plan-body progress/decision/validation updates, final lifecycle closeout owns lifecycle state transitions across the plan index surfaces and plan body, and `verify` challenges stale lifecycle state before `branch-ready`; then rerun the M4 skill, generated-output, adapter, metadata, lifecycle, and diff validation commands.
Validation target: `skills/plan/SKILL.md` includes all five R8a plan-guidance ownership points and the M4 validation commands pass after the fix.
Resolution: Added the three missing R8a ownership points to `skills/plan/SKILL.md`, mirroring the workflow-summary ownership model without adding new obligations. Strengthened T14 so R8a verification confirms each required ownership point in each named surface rather than relying on keyword or marker presence alone.
Validation evidence: `python - <<'PY' ... R8a direct ownership audit`, `python scripts/validate-skills.py skills/plan/SKILL.md`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir> && python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path AGENTS.md --path docs/examples/plans/example-plan.md --path specs/plan-index-lifecycle-ownership.test.md`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md`, and `git diff --check --` passed after the fix.

### code-review-m3-r1

No material findings.

### code-review-m2-r2

No material findings.

### code-review-m2-r1

#### BPIX-M2-CR1

Finding ID: BPIX-M2-CR1
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Extend terminal conservation validation to scoped plan-body lifecycle marker changes.
Rationale: A plan body can acquire `Plan lifecycle state: done`, `abandoned`, or `superseded` without `docs/plan.md` or `docs/plan-archive.md` being in the explicit validation path. The validator must catch missing recent/archive placement for that scoped plan body.
Required outcome: Explicit terminal plan-body markers in validation scope must require exactly one valid recent/archive terminal location, except legacy prose-only plans remain unknown and migration-proof-owned.
Safe resolution path: Add a failing fixture for plan-body-only terminal conservation, update the conservation trigger to include scoped explicit terminal plan bodies, rerun targeted lifecycle tests and validation, and return M2 to code-review.
Validation target: `python scripts/test-artifact-lifecycle-validator.py` includes the new plan-body-only terminal conservation regression and passes.
Resolution: Added a failing regression for a plan body scoped alone with `Plan lifecycle state: done` missing from both Done surfaces. Updated the conservation trigger so terminal conservation runs when either a plan index surface is in scope or any scoped plan body has an explicit terminal lifecycle marker. Legacy prose-only status remains exempt because the trigger only uses explicit marker state.
Validation evidence: `python scripts/test-artifact-lifecycle-validator.py -k plan_body_terminal_marker_alone_requires_done_location -k plan_lifecycle_marker_does_not_infer_terminal_state_from_prose`, `python scripts/test-artifact-lifecycle-validator.py`, `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py`, and `git diff --check --` passed after the fix.

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
