# Plan Index Lifecycle Ownership Test Spec

## Status

- active
- Approval: approved by maintainer on 2026-05-22 for M2 implementation.

## Related spec and plan

- Spec: `specs/plan-index-lifecycle-ownership.md`
- Proposal: `docs/proposals/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Plan: `docs/plans/2026-05-22-bounded-plan-index-and-completed-plan-archive.md`
- Plan review: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/plan-review-r1.md`
- Spec review: `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/reviews/spec-review-r2.md`

## Testing strategy

- Unit tests cover parser-level lifecycle marker detection, malformed marker rejection, one-line terminal entry shape, archive link shape, and supersession structural fields.
- Integration tests use artifact-lifecycle fixtures under `tests/fixtures/artifact-lifecycle/` to prove `docs/plan.md`, `docs/plan-archive.md`, and plan bodies interact correctly.
- Smoke tests run the repo-owned validator and selector commands after implementation milestones.
- Manual tests cover semantic quality that the spec assigns to code review, including whether compact terminal summaries and `active-context:` rationales are truthful and useful.
- Contract tests prove validators do not infer terminal state from arbitrary prose and do not allow missing or duplicate terminal entries once explicit lifecycle markers exist.
- Migration tests prove the first archive split preserves the pre-migration Done list by count, link, duplicate status, terminal disposition, and new location.
- Compatibility tests prove legacy prose-only terminal plans are preserved by the migration table without becoming parser input for standing validation.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1` | `T14` | manual, integration | Unplanned work is not forced into lifecycle indexing. |
| `R2`, `R2a` | `T1`, `T8`, `T14` | contract, manual | Main index and archive keep distinct roles. |
| `R3`, `R3a`, `R3b` | `T3`, `T8`, `T9`, `T14` | integration, manual | Index surfaces and plan bodies remain synchronized. |
| `R3c`, `R15`, `R15a` | `T3`, `T4`, `T5`, `T6`, `T15` | integration, migration | Terminal plans appear exactly once across recent and archive. |
| `R3d`, `R3e`, `R3f`, `R10`, `R10a` | `T1`, `T2`, `T7` | integration, contract | `docs/plan.md` satisfies the structural common-read budget. |
| `R3g`, `R3h`, `R3i`, `R3j`, `R3k`, `R3l`, `R3m`, `R3n`, `R3o`, `R3p` | `T10`, `T11`, `T12`, `T13` | unit, integration, contract | Lifecycle marker detection is explicit and deterministic. |
| `R4`, `R5`, `R6`, `R6a`, `R6b` | `T14`, `T17` | manual, integration | Contributor guidance preserves lifecycle ownership and timing rules. |
| `R7`, `R7a` | `T3`, `T4`, `T8`, `T9`, `T17` | integration, manual | Stale lifecycle state blocks readiness. |
| `R8`, `R8a` | `T14`, `T17` | manual, smoke | Guidance makes archive maintenance and lifecycle ownership discoverable. |
| `R9` | `T15` | migration, manual | Known stale baseline state is corrected during migration when in scope. |
| `R11`, `R11a`, `R12`, `R15b`, `R15d` | `T2`, `T7` | unit, integration, manual | Terminal entries link to plan files, use compact shape, and sort newest-first. |
| `R13` | `T6`, `T8`, `T9` | integration | Nonterminal work is not stored only in the archive. |
| `R14` | `T15`, `T18` | migration, manual | Archive edits are limited to allowed maintenance and migration. |
| `R15c` | `T1`, `T5` | integration | Recent Done cap is enforced. |
| `R16` | `T15` | migration | Initial migration proof records count and link preservation. |
| `R17`, `R17a`, `R17b`, `R17c`, `R17d`, `R17e`, `R17f`, `R17g`, `R17h`, `R17i` | `T16` | unit, integration, manual | Superseded placement depends on structural active context. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T14`, `T17` | Done-before-PR timing remains contributor-visible. |
| `E2` | `T14`, `T17` | Merge-gated done timing remains a narrow exception. |
| `E3` | `T8`, `T14` | Blocked plans move out of Active when the block is known. |
| `E4` | `T9`, `T16` | Superseded plans move to the proper live or archived surface. |
| `E5` | `T14` | `learn` remains retrospective and not lifecycle bookkeeping authority. |
| `E6` | `T1`, `T5`, `T15` | Recent Done stays capped and displaced terminal entries remain archived. |
| `E7` | `T3`, `T4`, `T5`, `T15` | Routine archival preserves every explicit terminal plan exactly once. |
| `E8` | `T6`, `T8`, `T9` | Active, blocked, and review-needed work stays in `docs/plan.md`. |
| `E9` | `T16` | Terminal superseded history moves to archive when active context is absent. |
| `E10` | `T10`, `T3` | Explicit terminal marker is detected and conserved. |
| `E11` | `T11`, `T6` | Explicit nonterminal marker is detected and must not be archive-only. |
| `E12` | `T12` | Contradictory lifecycle marker fails validation. |
| `E13` | `T13`, `T15` | Legacy prose-only status is not parsed as terminal. |
| `E14` | `T16` | Active supersession entry with required fields passes. |
| `E15` | `T16` | Main-index supersession entry without `active-context:` fails. |

## Edge case coverage

- EC1 active while implementation or review remains outstanding: `T14`, `T17`.
- EC2 done when repository integration is the deciding completion event: `T14`, `T17`.
- EC3 replacement plan supersedes old plan: `T9`, `T16`.
- EC4 blocked plan moves without waiting for retrospective: `T8`, `T14`.
- EC5 later automation remains optional: `T18`.
- EC6 recent completed plan may stay in `Done (recent)` until cap is exceeded: `T1`, `T5`.
- EC7 terminal plan can move from recent to archive without lifecycle-state change: `T15`.
- EC8 terminal superseded plan remains in main index only with active context: `T16`.
- EC9 temporary migration duplication must be documented and resolved before readiness: `T4`, `T15`.
- EC10 legacy prose-only terminal plan is preserved through migration proof, not parser inference: `T13`, `T15`.
- EC11 active lifecycle plus merged disposition fails: `T12`.
- EC12 duplicated terminal plan fails unless covered by unresolved migration transaction that blocks readiness: `T4`, `T15`.
- EC13 superseded main-index entry lacking `active-context:` fails: `T16`.
- EC14 archived superseded entry retaining `active-context:` fails: `T16`.

## Test cases

### T1. Bounded main index shape

- Covers: `R2`, `R3d`, `R3e`, `R3f`, `R10`, `R10a`, `R15c`, `E6`, `EC6`
- Level: integration
- Fixture/setup:
  - Valid fixture with `docs/plan.md`, `docs/plan-archive.md`, and at most 10 `Done (recent)` entries.
  - Invalid fixtures for missing archive pointer, Done above cap, and Done before Active or Blocked.
- Steps:
  - Run `python scripts/test-artifact-lifecycle-validator.py` after adding fixtures.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plan-archive.md` against the real migration state.
- Expected result:
  - Valid bounded shape passes.
  - Missing archive link, cap overflow, and incorrect section ordering fail with stable diagnostics.
- Failure proves:
  - `docs/plan.md` can grow or reorder in ways that break the common-read index contract.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; `scripts/artifact_lifecycle_validation.py`.

### T2. Terminal entry link, line shape, and ordering

- Covers: `R11`, `R11a`, `R12`, `R15b`, `R15d`
- Level: unit, integration, manual
- Fixture/setup:
  - Valid recent and archived terminal entries with one Markdown plan link each.
  - Invalid entries with no plan link, broken plan link, multiline terminal transcript, and malformed link target.
- Steps:
  - Run validator fixture tests for valid and invalid terminal entries.
  - Manually review real migrated entries for truthful compact summaries and newest-first ordering.
- Expected result:
  - Structural failures are rejected by the validator.
  - Semantic summary quality is explicitly reviewed, not guessed by automation.
- Failure proves:
  - Terminal entries may become unfindable, too verbose, or misleading.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; manual review during M3 code review.

### T3. Terminal conservation success

- Covers: `R3`, `R3c`, `R7a`, `R15`, `R15a`, `E7`, `E10`
- Level: integration
- Fixture/setup:
  - Fixture with plan bodies marked `done`, `abandoned`, and `superseded`.
  - Each terminal plan appears exactly once across `Done (recent)` and `Done (archive)`.
- Steps:
  - Run artifact-lifecycle fixture tests.
  - Run explicit-path validation against real `docs/plan.md`, `docs/plan-archive.md`, and plan bodies changed by the migration.
- Expected result:
  - All explicit terminal plans are accepted when each appears exactly once in recent or archive.
- Failure proves:
  - The validator cannot prove the core "no completed plan becomes unfindable" invariant.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; `scripts/validate-artifact-lifecycle.py`.

### T4. Terminal conservation rejects missing and duplicate entries

- Covers: `R3c`, `R7a`, `R15`, `R15a`, `E7`, `EC9`, `EC12`
- Level: integration
- Fixture/setup:
  - Invalid fixture where an explicit terminal plan appears in neither recent nor archive.
  - Invalid fixture where an explicit terminal plan appears in both recent and archive without a documented migration exception.
- Steps:
  - Run artifact-lifecycle fixture tests.
  - Assert diagnostics identify missing or duplicate terminal entries and the owning plan path.
- Expected result:
  - Missing and duplicate terminal placement fail validation.
- Failure proves:
  - Routine archival could silently drop or duplicate terminal history.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`.

### T5. Recent Done cap and recurring archival

- Covers: `R3e`, `R15`, `R15a`, `R15c`, `E6`, `E7`, `EC6`
- Level: integration, migration
- Fixture/setup:
  - Valid fixture with exactly 10 `Done (recent)` entries and older terminal entries in archive.
  - Invalid fixture with 11 `Done (recent)` entries.
- Steps:
  - Run validator fixture tests.
  - In M3 migration proof, record pre-migration Done count, post-migration recent count, and archive count.
- Expected result:
  - Exactly 10 recent entries pass; more than 10 fail.
  - Count conservation proves displaced entries moved to archive.
- Failure proves:
  - The bounded index can regress into unbounded completed history.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`.

### T6. Nonterminal work is not archive-only

- Covers: `R3a`, `R13`, `E8`, `E11`
- Level: integration
- Fixture/setup:
  - Plan bodies marked `active` and `blocked`.
  - Invalid fixture where one appears only in `docs/plan-archive.md`.
- Steps:
  - Run validator fixture tests.
  - Confirm diagnostics name archive-only nonterminal placement.
- Expected result:
  - Nonterminal plans remain in `docs/plan.md` and archive-only placement fails.
- Failure proves:
  - Active or blocked work can be hidden from the common-read index.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`.

### T7. Terminal entries link to existing plan files

- Covers: `R11`, `R15b`, `R15d`
- Level: integration
- Fixture/setup:
  - Valid fixture with every terminal entry linked to an existing `docs/plans/*.md` file.
  - Invalid fixture with a broken link and a non-plan link.
- Steps:
  - Run validator fixture tests.
  - Run explicit-path lifecycle validation on real index/archive files after migration.
- Expected result:
  - Broken or non-plan terminal links fail validation.
- Failure proves:
  - Archived history may be present but not recoverable.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; `scripts/validate-artifact-lifecycle.py`.

### T8. Active and blocked synchronization

- Covers: `R3`, `R3a`, `R3b`, `R7`, `R7a`, `R13`, `E3`, `E8`, `EC4`
- Level: integration, manual
- Fixture/setup:
  - Valid fixtures for active and blocked plan markers matching `docs/plan.md`.
  - Invalid fixtures for plan body/index disagreement.
- Steps:
  - Run validator fixture tests for known stale plan/index disagreement.
  - Manually review real Active and Blocked entries after migration for complete common-read visibility.
- Expected result:
  - Matching active/blocked state passes.
  - Conflicting state or archive-only nonterminal placement fails.
- Failure proves:
  - The main index and plan body can disagree about live work.
- Automation location:
  - Existing and new artifact-lifecycle fixtures; manual review during M3/M6.

### T9. Superseded synchronization and placement

- Covers: `R3`, `R3a`, `R3b`, `R7`, `R7a`, `R13`, `R17`, `E4`, `EC3`, `EC8`
- Level: integration, manual
- Fixture/setup:
  - Superseded plan body with active context in `docs/plan.md`.
  - Superseded plan body without active context in archive.
- Steps:
  - Run validator fixture tests.
  - Manually compare replacement links and plan-body lifecycle marker during migration.
- Expected result:
  - Superseded state is synchronized, with live active-context pointers only in `docs/plan.md`.
- Failure proves:
  - Superseded work can remain active-looking or disappear from terminal history.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; manual review during M3.

### T10. Valid lifecycle marker parsing

- Covers: `R3g`, `R3h`, `R3i`, `R3j`, `R3k`, `R3l`, `R3m`, `E10`, `E11`
- Level: unit, integration
- Fixture/setup:
  - Valid plan bodies for `active` plus `none`, `blocked` plus `none`, `done` plus `merged`, `abandoned` plus `abandoned`, and `superseded` plus `superseded`.
- Steps:
  - Run parser-level tests or fixture tests through `validate_repository`.
  - Assert detected lifecycle classifications match expected terminal or nonterminal state.
- Expected result:
  - Valid markers are detected only from top-level `## Status` fields.
- Failure proves:
  - Terminal conservation is not anchored to a deterministic source.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; parser helpers in `scripts/artifact_lifecycle_validation.py`.

### T11. Nonterminal disposition rules

- Covers: `R3k`, `R3l`, `E11`
- Level: unit, integration
- Fixture/setup:
  - Valid nonterminal markers with `Terminal disposition: none`.
  - Invalid nonterminal markers with terminal dispositions.
- Steps:
  - Run fixture tests.
  - Assert invalid nonterminal disposition fails with a stable marker diagnostic.
- Expected result:
  - `active` and `blocked` markers require `Terminal disposition: none`.
- Failure proves:
  - Nonterminal plans can look terminal to humans or automation.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`.

### T12. Malformed, duplicated, contradictory, and unknown markers fail

- Covers: `R3g`, `R3h`, `R3l`, `R3m`, `R3o`, `E12`, `EC11`
- Level: unit, integration
- Fixture/setup:
  - Fixtures for duplicate lifecycle fields, duplicate disposition fields, unknown lifecycle value, unknown disposition value, missing field, malformed field, and active plus merged disposition.
- Steps:
  - Run fixture tests.
  - Assert each failure reports the marker problem when the plan file is in validation scope.
- Expected result:
  - Contradictory, malformed, duplicated, or unknown marker fields fail.
- Failure proves:
  - The validator may accept ambiguous lifecycle state.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`.

### T13. Legacy prose-only status is not terminal input

- Covers: `R3i`, `R3n`, `R3p`, `E13`, `EC10`
- Level: unit, integration, migration
- Fixture/setup:
  - Plan body with prose-only status containing words such as done, finished, closed, or merged.
  - Migration proof row preserving any legacy terminal entry from the pre-migration Done list.
- Steps:
  - Run fixture tests and assert no terminal state is inferred from prose-only status.
  - During M3, confirm legacy pre-migration Done entries are preserved by `plan-index-migration.md`.
- Expected result:
  - Prose-only status is unknown for standing validation.
  - First-migration preservation comes from the migration proof, not prose matching.
- Failure proves:
  - The validator may recreate the unsafe broad prose inference rejected by spec review.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; migration proof manual review.

### T14. Contributor guidance and ownership split

- Covers: `R1`, `R2`, `R2a`, `R4`, `R5`, `R6`, `R6a`, `R6b`, `R8`, `R8a`, `E1`, `E2`, `E3`, `E5`, `EC1`, `EC2`, `EC4`
- Level: manual, smoke
- Fixture/setup:
  - `docs/workflows.md`
  - `AGENTS.md`
  - `docs/examples/plans/example-plan.md`
  - `skills/plan/SKILL.md` if changed
- Steps:
  - Review touched guidance for plan/index/archive ownership.
  - Confirm unplanned work is not forced into plan lifecycle indexing.
  - Confirm closeout, blocked, superseded, and merge-gated done timing are discoverable.
  - Run skill validation and build checks if canonical skill text changes.
- Expected result:
  - Contributors can maintain the archive contract without chat-only knowledge.
- Failure proves:
  - The validator may enforce behavior that contributor-facing guidance does not explain.
- Automation location:
  - Manual review during M4; `python scripts/validate-skills.py`; `python scripts/build-skills.py --check`.

### T15. Initial migration proof preserves history

- Covers: `R3c`, `R9`, `R14`, `R16`, `E6`, `E7`, `E13`, `EC7`, `EC9`, `EC10`, `EC12`
- Level: migration
- Fixture/setup:
  - Pre-migration Done inventory from `docs/plan.md`.
  - `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`.
  - Post-migration `docs/plan.md` and `docs/plan-archive.md`.
- Steps:
  - Record every pre-migration Done entry and plan link.
  - Record new location, terminal state or disposition, duplicate status, and preservation result.
  - Verify pre-migration Done count equals post-migration recent count plus archive count, allowing only documented migration rows that are resolved before readiness.
  - Run lifecycle validation on index/archive surfaces and migration proof path.
- Expected result:
  - Every pre-migration Done entry remains locatable exactly once after migration.
- Failure proves:
  - The archive split deleted, duplicated, or obscured completed-plan provenance.
- Automation location:
  - `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`; `scripts/validate-artifact-lifecycle.py`.

### T16. Active supersession structure

- Covers: `R17`, `R17a`, `R17b`, `R17c`, `R17d`, `R17e`, `R17f`, `R17g`, `R17h`, `R17i`, `E9`, `E14`, `E15`, `EC8`, `EC13`, `EC14`
- Level: unit, integration, manual
- Fixture/setup:
  - Valid main-index superseded entry with superseded plan link, `superseded by:` replacement link, and non-empty `active-context:`.
  - Invalid main-index superseded entries missing replacement link, missing `active-context:`, or blank rationale.
  - Valid archived superseded entry with replacement link and no `active-context:`.
  - Invalid archived superseded entry retaining `active-context:`.
- Steps:
  - Run validator fixture tests.
  - Manually review active-context rationale quality where such entries remain in `docs/plan.md`.
- Expected result:
  - Structural supersession fields are enforced; semantic usefulness remains review-owned.
- Failure proves:
  - Terminal superseded history can remain in the common-read index without a testable reason, or archived history can retain active-context ambiguity.
- Automation location:
  - `scripts/test-artifact-lifecycle-validator.py`; manual review during M3 code review.

### T17. Verify/readiness lifecycle evidence

- Covers: `R5`, `R7`, `R7a`, `R8a`, `E1`, `E2`, `EC1`, `EC2`
- Level: manual, smoke
- Fixture/setup:
  - Active plan validation notes.
  - `docs/plan.md`, `docs/plan-archive.md`, and touched plan bodies.
  - Final verify commands from the active plan.
- Steps:
  - Confirm final validation evidence names the plan index surfaces and lifecycle marker surfaces reviewed.
  - Confirm stale lifecycle state is not present before readiness is claimed.
  - Run final broad validation named by the active plan unless the implementation records an approved narrower scope.
- Expected result:
  - Readiness evidence is tied to concrete lifecycle surfaces and no stale state remains.
- Failure proves:
  - A branch could claim readiness while lifecycle state is stale or unproven.
- Automation location:
  - Final `verify`; active plan validation notes.

### T18. Scope, archive maintenance, and no unapproved automation

- Covers: `R14`, `EC5`, security/privacy, performance expectations
- Level: manual, smoke
- Fixture/setup:
  - Diff for `docs/plan-archive.md`, validator scripts, selector scripts, and guidance.
- Steps:
  - Confirm archive edits are limited to migration, formatting normalization, deduplication, correcting broken links, or allowed maintenance.
  - Confirm no background synchronization, generated registry, CLI scaffolding, fake merge state, fake CI state, secrets, private paths, or host-only state are introduced.
  - Run `git diff --check --`.
- Expected result:
  - The change stays inside the approved first-slice scope.
- Failure proves:
  - Implementation expanded beyond the approved contract or introduced unsafe repository claims.
- Automation location:
  - Manual diff review; `git diff --check --`.

## Fixtures and data

- Existing fixture root: `tests/fixtures/artifact-lifecycle/`.
- New validator fixtures should be grouped by behavior, for example:
  - `plan-index-archive-valid`
  - `plan-index-archive-recent-over-cap`
  - `plan-index-archive-missing-terminal`
  - `plan-index-archive-duplicate-terminal`
  - `plan-index-archive-broken-link`
  - `plan-lifecycle-marker-valid-terminal`
  - `plan-lifecycle-marker-valid-active`
  - `plan-lifecycle-marker-contradictory`
  - `plan-lifecycle-marker-unknown-value`
  - `plan-lifecycle-marker-prose-only`
  - `plan-supersession-valid-active-context`
  - `plan-supersession-missing-active-context`
  - `plan-supersession-archived-active-context`
- Real migration data:
  - `docs/plan.md`
  - `docs/plan-archive.md`
  - `docs/plans/*.md` files referenced by pre-migration Done entries
  - `docs/changes/2026-05-22-bounded-plan-index-and-completed-plan-archive/plan-index-migration.md`
- Command surfaces:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-select-validation.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path ...`
  - `python scripts/validate-skills.py` when canonical skill text changes
  - `python scripts/build-skills.py --check` when canonical skill text changes
  - `bash scripts/ci.sh` for final broad smoke unless the active plan records an approved narrower scope
  - `git diff --check --`

## Mocking/stubbing policy

- Do not mock repository lifecycle surfaces when real fixture repositories can exercise validator behavior.
- Do not use snapshots as the primary proof for plan-index behavior.
- Use synthetic fixture repositories only to force invalid states that should not be committed to the real repo.
- Use real repository files and the migration proof for the historical Done preservation test.
- Do not stub out filesystem link checks; broken plan links are part of the contract.

## Migration or compatibility tests

- `T13` proves legacy prose-only status is not parsed as terminal by standing validation.
- `T15` proves first-migration preservation for legacy and compacted entries through the migration table.
- `T5` proves future routine archival remains safe after the first migration.
- `T18` proves rollback and archive maintenance stay within the allowed edit classes.

## Observability verification

- Validator diagnostics must name missing terminal entries, duplicate terminal entries, broken plan links, cap violations, malformed markers, contradictory dispositions, active-work-in-archive failures, missing supersession fields, and archived `active-context:` markers.
- Migration proof must expose pre/post counts and link preservation in a reviewer-readable table.
- Final validation notes in the active plan must name the commands run and the lifecycle surfaces reviewed.
- Manual review owns semantic quality of compact terminal summaries and `active-context:` rationales.

## Security/privacy verification

- `T18` verifies the archive does not introduce secrets, private local paths, credentials, or host-only state.
- Guidance and validation must not claim merge state, CI state, review completion, or lifecycle completion that is not evidenced in tracked artifacts.
- Plan index and archive state must remain in tracked repository files rather than chat-only notes or local machine state.

## Performance checks

- No benchmark is required.
- Validator checks should remain lightweight structural scans over touched plan index surfaces and relevant plan bodies.
- Terminal conservation should run when `docs/plan.md`, `docs/plan-archive.md`, or relevant plan bodies change, not as continuous background synchronization.
- If implementation needs heavier automation, return to spec or architecture before expanding scope.

## Manual QA checklist

- [ ] `docs/plan.md` lists complete Active and Blocked sections before Done history.
- [ ] `Done (recent)` has no more than 10 entries.
- [ ] `docs/plan.md` links to `docs/plan-archive.md` when older terminal history exists.
- [ ] Terminal entries are one-line summaries with valid plan links.
- [ ] Every explicit terminal plan appears exactly once across recent and archive.
- [ ] No nonterminal plan is stored only in archive.
- [ ] Lifecycle markers are present and valid for plan bodies intentionally brought under standing validation.
- [ ] Legacy prose-only terminal entries from the pre-migration Done list are preserved in the migration table.
- [ ] Main-index superseded entries have `superseded by:` and non-empty `active-context:`.
- [ ] Archived superseded entries do not retain `active-context:`.
- [ ] Contributor guidance explains archive maintenance and lifecycle ownership.
- [ ] Validation notes name the commands run and any warnings.

## What not to test

- Do not test a generated plan-index registry; it is out of scope.
- Do not test CLI scaffolding for plan/archive updates; it is out of scope.
- Do not require exact prose wording for compact summaries or active-context rationales beyond structural fields.
- Do not infer terminal state from arbitrary status prose.
- Do not run hosted PR or branch-protection behavior end to end for this contract.
- Do not rewrite unrelated plan bodies solely to make fixtures easier.

## Uncovered gaps

None under the approved spec and plan.

If implementation discovers that terminal conservation cannot be enforced without broader registry design, return to spec before weakening the invariant.

## Next artifacts

implement
code-review
review-resolution when triggered
explain-change
verify
pr

## Follow-on artifacts

None yet.

## Readiness

Active proof map for M2 validator fixtures and contract checks. M3 migration must wait until M2 validator behavior can prove the archive split structurally.
