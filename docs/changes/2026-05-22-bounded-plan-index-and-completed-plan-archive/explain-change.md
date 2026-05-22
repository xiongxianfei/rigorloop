# Bounded Plan Index and Completed-Plan Archive Explain Change

## Status

Explain-change recorded for implementation closeout. Final `verify` and PR handoff remain downstream and are not claimed here.

## Summary

This change turns `docs/plan.md` back into a bounded common-read index for active, blocked, recent done, and active supersession context. Older terminal plan history now lives in `docs/plan-archive.md`, with validator and selector support so completed plans remain findable after both the first migration and future routine archival.

The implementation also adds explicit plan-body lifecycle markers, structural supersession rules, contributor guidance, selection routing, migration proof, and durable review evidence. A post-merge sync also updated the newly merged PR #85 plan body and index entry so `origin/main`'s merged state does not conflict with this branch's bounded index contract.

## Problem

The original `docs/plan.md` carried both live orientation state and an unbounded `Done` history. That made the file grow with accumulated project history instead of with the active working set, while the completed entries still needed to remain recoverable for provenance.

The accepted invariant was: keep Active and Blocked first and cheap to read, preserve every completed plan, cap recent Done history, and move older terminal history to an archive without changing plan lifecycle facts.

## Decision Trail

The proposal selected a summary/archive split: `docs/plan.md` stays the first-read plan index, and `docs/plan-archive.md` stores older terminal history. The proposal also settled the open questions: the first cap is 10 recent Done entries, ordering is newest-first, the common-read budget is structural rather than a separate line count, terminal superseded history is archived unless it carries active supersession context, and validators enforce structural shape while code review owns semantic quality.

Spec-review added two blocking clarifications before implementation: `BPIX-SR1` required deterministic terminal lifecycle detection, and `BPIX-SR2` required a testable supersession boundary. The spec now uses explicit `Plan lifecycle state` and `Terminal disposition` fields in the plan body and requires `superseded by:` plus non-empty `active-context:` for superseded entries kept in the main index.

Implementation followed the reviewed plan milestones:

- M1 refreshed the test spec for the archive contract.
- M2 implemented validator support and fixtures, then resolved `BPIX-M2-CR1` by making terminal conservation run when a scoped plan body has an explicit terminal marker.
- M3 migrated historical Done entries into the bounded index/archive split and recorded count preservation.
- M4 updated contributor guidance and the `plan` skill, then resolved `BPIX-M4-CR1` by adding the missing R8a lifecycle ownership bullets.
- M5 updated validation selection so plan index/archive changes and migration proof changes select lifecycle validation.
- M6 recorded final implementation evidence and kept the active plan in the correct downstream handoff state.

No separate architecture artifact was created because the approved plan records this as a workflow/validator/artifact contract change, not a new runtime architecture, persistence, deployment, or API boundary.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/plan.md` | Added an index policy comment, kept Active and Blocked first, renamed Done to `Done (recent)`, capped it at 10 entries, added the archive pointer, and compacted terminal entries to one line. | Satisfies the bounded common-read index contract while preserving recent completion context. | Proposal; `R2`, `R3c`-`R3f`, `R10`, `R10a`, `R11`, `R12`, `R15c`, `R15d` | Migration assertion; lifecycle validation over plan surfaces |
| `docs/plan-archive.md` | Added the archive and moved older terminal Done entries there newest-first. | Preserves completed-plan provenance without keeping all history in the common-read file. | Proposal; `R2a`, `R3c`, `R11`, `R12`, `R14`, `R16` | Migration proof: 75 pre-migration Done entries = 10 recent + 65 archive |
| `docs/changes/.../plan-index-migration.md` | Recorded pre/post counts, duplicate status, link preservation, and per-entry location. | Proves the first migration archived rather than deleted historical Done entries. | `R16`, proposal migration proof | Count/link assertion and lifecycle validation |
| `specs/plan-index-lifecycle-ownership.md` | Added archive definitions, structural common-read budget, explicit lifecycle marker, terminal conservation, active supersession context, cap, ordering, archive ownership, and validation obligations. | Converts the proposal into a testable lifecycle contract and resolves spec-review blockers. | `BPIX-SR1`, `BPIX-SR2`; `R3g`-`R3p`, `R10`-`R17i` | Spec lifecycle validation; spec-review R2 approval |
| `specs/plan-index-lifecycle-ownership.test.md` | Added traceable tests `T1`-`T18`, including terminal marker cases, conservation, archive cap, link checks, supersession structure, migration proof, guidance, and selector routing. | Makes every archive/lifecycle rule testable before and during implementation. | Test-spec from approved spec | Implemented in validator and selector test suites |
| `scripts/artifact_lifecycle_validation.py` | Parses explicit plan-body lifecycle markers, validates marker contradictions, checks recent/archive entries, enforces the cap and one-line terminal shape, checks links, rejects archive-only nonterminal plans, enforces supersession markers, and triggers conservation for explicit terminal plan bodies in scope. | Makes completed-plan conservation a standing invariant, not only a one-time migration proof. | `R3g`-`R3p`, `R7a`, `R15`-`R15d`, `R17d`, `R17e`, `BPIX-M2-CR1` | `python scripts/test-artifact-lifecycle-validator.py` |
| `scripts/test-artifact-lifecycle-validator.py` | Added fixture coverage for valid terminal placement, missing terminal entries, duplicates, cap overflow, nonterminal archive-only placement, malformed markers, legacy prose-only status, active supersession context, and archived `active-context:` rejection. | Proves the validator catches the archive failure modes the proposal identified while preserving legacy prose-only exemption. | `T1`-`T13`, `T15`-`T16`; `BPIX-M2-CR1` | Full lifecycle validator regression passed |
| `scripts/validation_selection.py` | Classifies `docs/plan.md` and `docs/plan-archive.md` as paired plan-index surfaces and routes migration proof changes with `docs/plan.md`, `docs/plan-archive.md`, and the owning `change.yaml`. | Ensures routine edits run the conservation checks over the union of recent and archived terminal entries. | `R15`, `R16`, M5 plan | Selector tests and explicit selected CI |
| `scripts/test-select-validation.py` | Added selector regressions for plan archive surfaces, migration proof routing, representative path categories, and workflow surface sets. | Prevents the archive file or migration proof from becoming invisible to selected validation. | `T17`, `T18`, M5 plan | `python scripts/test-select-validation.py` |
| `docs/workflows.md`, `AGENTS.md`, `docs/examples/plans/example-plan.md` | Documented the archive surface, bounded index shape, lifecycle marker, active supersession marker, and lifecycle ownership expectations. | Makes the new contract discoverable to contributors and future agents. | `R8`, `R8a`, M4 plan | M4 guidance audit; lifecycle validation |
| `skills/plan/SKILL.md` | Updated plan-authoring guidance for bounded index maintenance, archive updates, lifecycle markers, supersession markers, and the R8a ownership bullets. | Keeps the adopter-facing plan guidance self-contained instead of relying only on repository workflow docs. | `R8a`, `BPIX-M4-CR1` | Skill validation, build-skills check, adapter build/validation, R8a direct audit |
| `docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md` | Added the execution plan and kept Current Handoff Summary, progress, milestones, decisions, risks, and validation notes current through M6. | The plan owns current milestone and downstream handoff state for this planned initiative. | Active plan policy; M1-M6 | Code-review M6 clean-with-notes |
| `docs/changes/.../change.yaml`, `review-log.md`, review records, `review-resolution.md` | Recorded artifacts, requirements/tests, validation commands, review events, material findings, and dispositions. | Preserves durable workflow evidence and proves material findings were resolved before downstream handoff. | Workflow contract; review skills | Review-artifact closeout validation |
| `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md` | During sync with merged PR #85, changed its plan body from stale active/open wording to explicit `done` with `merged` disposition. | The merge brought in a plan that still said PR #85 was open; the bounded index now lists that plan in Done (recent), so the plan body needed to stop contradicting reality. | Plan lifecycle ownership `R3`, `R3b`, `R5`, `R7a` | Post-merge lifecycle validation over the plan body and index surfaces |

## Tests Added Or Changed

The lifecycle validator tests cover:

- explicit terminal and nonterminal marker parsing;
- malformed, contradictory, duplicated, and unknown marker fields;
- no terminal inference from legacy prose-only status;
- terminal plan missing from both Done surfaces;
- terminal plan duplicated across recent and archive;
- recent Done cap enforcement;
- broken terminal entry links;
- archive-only nonterminal placement;
- one-line terminal entry shape;
- active supersession context structure;
- archived superseded entries without `active-context:`.

The selector tests cover:

- plan index surface changes selecting lifecycle validation with both `docs/plan.md` and `docs/plan-archive.md`;
- migration proof changes selecting lifecycle validation with the migration proof, `change.yaml`, and both index surfaces;
- representative lifecycle/workflow path routing;
- unchanged broad-smoke selected-validation behavior around the new surfaces.

This level is appropriate because the risky behavior is structural artifact validation and selection routing, not application runtime behavior. Fixture-based validator tests directly exercise the failure modes, and selector tests prove the checks run when the relevant files change.

## Validation Evidence Available Before Final Verify

Implementation and review recorded these passing commands:

- `python scripts/test-artifact-lifecycle-validator.py`
- `python -m py_compile scripts/artifact_lifecycle_validation.py scripts/artifact_lifecycle_contracts.py`
- `python scripts/test-select-validation.py`
- `python -m py_compile scripts/validation_selection.py`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/change.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md --path specs/plan-index-lifecycle-ownership.md --path specs/plan-index-lifecycle-ownership.test.md`
- `python scripts/validate-skills.py skills/plan/SKILL.md`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir> && python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`
- `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path scripts/test-select-validation.py --path docs/plan-archive.md --path docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`
- `bash scripts/ci.sh`
- `git diff --check --`

Additional manual/scripted checks recorded:

- migration proof count/link assertion: 75 pre-migration Done entries, 10 recent, 65 archived, no duplicates, no broken links;
- M4 guidance audit for archive, lifecycle marker, and active-context guidance;
- R8a direct ownership audit for `docs/workflows.md` and `skills/plan/SKILL.md`;
- post-merge sync validation: conflict marker scan, `git diff --check --`, and explicit lifecycle validation over `docs/plan.md`, `docs/plan-archive.md`, and the PR #85 plan body.

Some lifecycle validation runs reported the existing lifecycle-language warning for merge-state wording in the governing spec. That warning was recorded in the plan validation notes and did not block the implementation milestones.

## Review Resolution Summary

Detailed review evidence is in `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-log.md` and `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/review-resolution.md`.

Material findings resolved:

- `BPIX-SR1`: accepted and resolved by defining explicit plan-body lifecycle-state markers and forbidding prose-based terminal inference.
- `BPIX-SR2`: accepted and resolved by defining structural active supersession context in `docs/plan.md`.
- `BPIX-M2-CR1`: accepted and resolved by adding the plan-body-only terminal conservation regression and trigger.
- `BPIX-M4-CR1`: accepted and resolved by adding missing R8a ownership guidance to `skills/plan/SKILL.md` and strengthening T14.

Clean review events with no material findings were recorded for spec-review R2, plan-review R1, code-review M2 R2, code-review M3 R1, code-review M4 R2, code-review M5 R1, and code-review M6 R1. `review-resolution.md` reports closeout status as closed with no unresolved material findings.

## Alternatives Rejected

- Keep the unbounded single-file Done history: rejected because it keeps common orientation cost proportional to historical volume.
- Delete old Done entries: rejected because it destroys provenance.
- Move Done lower in the same file: rejected because it does not bound file growth.
- Generate the plan index from a machine-readable registry now: rejected as larger mechanism than needed for this slice.
- Infer terminal lifecycle state from arbitrary plan prose: rejected by `BPIX-SR1` because prose-heavy plans are not deterministic enough for validation.
- Treat supersession placement as unlabeled prose: rejected by `BPIX-SR2` because the main-index/archive boundary must be structurally testable.
- Bulk-edit legacy plan bodies with lifecycle markers: rejected for this migration; legacy completed history is preserved through the migration proof as required by the spec.
- Hand-edit generated adapter output: not done; adapter proof used temporary generated output validation.
- Add CLI/scaffolding for automatic archive maintenance: deferred as a follow-up because validator and guidance are sufficient for the first slice.

## Scope Control

The implementation preserves the non-goals:

- It does not delete completed plan records.
- It does not remove plan files from `docs/plans/`.
- It does not bulk-rewrite individual legacy plan bodies solely for archival.
- It does not change milestone, PR, review, verify, or closeout semantics beyond the approved lifecycle/index contract.
- It does not hide active, blocked, review-requested, resolution-needed, or ambiguous work in the archive.
- It does not turn `docs/plan.md` into a long-form plan body.
- It does not add a generated registry, background synchronization, or CLI scaffolding.

The only non-core synced change is the PR #85 plan-body cleanup required after merging `origin/main`; it makes the plan body's lifecycle state match the newly merged PR and the bounded Done entry.

## Risks And Follow-Ups

Remaining risks:

- Manual archive maintenance can still drift if future contributors bypass validation.
- Code review still owns semantic quality of one-line summaries and `active-context:` rationales.
- Legacy prose-only completed plans remain migration-proof-owned unless they later receive explicit lifecycle markers.
- Final branch readiness is not claimed until the downstream `verify` stage reruns the required validation from the current synced branch.

Follow-ups already identified:

- Consider a generated plan-index registry if manual archive maintenance remains costly.
- Consider CLI/scaffolding support that updates `docs/plan.md` and `docs/plan-archive.md` together.
- Consider applying the compact index/archive pattern to other lifecycle indexes if similar growth appears.
