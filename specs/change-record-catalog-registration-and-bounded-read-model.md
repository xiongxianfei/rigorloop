# Change-Record Catalog Registration and Bounded Read Model

## Status

approved

## Related proposal

- [Change-Record Catalog Registration and Bounded Read Model](../docs/proposals/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md), accepted.
- Proposal review: [proposal-review-r1](../docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/reviews/proposal-review-r1.md), approved with no material findings.

Dependency references:

- [Test Layering and Change-Scoped Validation](test-layering-and-change-scoped-validation.md) owns the validation selector and selected-check output contract.
- [Compact Change Validation Metadata](compact-change-validation-metadata.md) owns compact validation metadata shape, summary derivation, path variables, and legacy compatibility.
- [RigorLoop Workflow](rigorloop-workflow.md) owns lifecycle stage order, review status meanings, handoff boundaries, and required formal review recording.
- [Skill Contract](skill-contract.md) owns published skill structure and generated adapter compatibility boundaries.

This spec defines a new feature contract that depends on those surfaces without replacing their existing ownership.

## Goal and context

RigorLoop change records are durable evidence catalogs under `docs/changes/<change-id>/`. They currently support writing evidence and storing validation metadata, but recurring failures show two missing contracts:

- change-local evidence files are not registered by evidence class, so useful deterministic files can reach verify before the changed-path selector knows how to route them;
- common stage-owned questions do not have a bounded read/query contract, so agents may read all of `change.yaml` or an entire change record to answer a narrow question.

The goal is to make change records behave as queried catalogs. Deterministic change-local evidence files are registered and routed when introduced, and common change-record reads have bounded, stage-specific paths. Full forensic reconstruction remains available for audits, disputed evidence, migration checks, and whole-record review.

The approved rollout separates the work into two implementation workstreams:

- Workstream A: evidence registration and selector routing.
- Workstream B: bounded read/query model and stage-skill guidance.

Workstream A is the first implementation slice. Workstream B follows after query-helper commands are stable.

## Glossary

- `change record`: The change-local artifact set under `docs/changes/<change-id>/`.
- `change metadata`: `docs/changes/<change-id>/change.yaml`.
- `change-local evidence file`: A file under `docs/changes/<change-id>/` other than `change.yaml`, review records, review log, review resolution, explain-change, verify report, or other already governed lifecycle artifact.
- `evidence class`: A stable category for recurring change-local evidence files, such as `audit`, `identity`, `preservation`, `baseline`, or `token-cost`.
- `evidence class registry`: The repository-owned contract that maps evidence class IDs to allowed roots, filename patterns, selector routes, validators, lifecycle expectations, and allowed/required/forbidden conditions.
- `registered evidence file`: A change-local evidence file that matches exactly one supported evidence class entry.
- `unregistered evidence file`: A deterministic change-local evidence file that does not match any supported evidence class entry.
- `deterministic in-repo evidence`: A repository-tracked evidence file whose path and owning change root can be classified without external context.
- `selector route`: The changed-path selector outcome that selects the required validation check IDs and affected roots for a changed path.
- `manual-routing-required`: A selector diagnostic meaning the changed path cannot be safely routed by deterministic selector rules.
- `registration debt`: The required resolution work created when deterministic in-repo evidence produces `manual-routing-required`.
- `bounded read`: A read path that returns only the authoritative slice needed for a stage-owned question.
- `query helper`: A repository-owned command that exposes bounded change-record reads.
- `common-read slice`: The smallest authoritative fields or artifacts required to answer a recurring stage-owned question.
- `forensic read`: A deliberate full `change.yaml` or full change-record read used for audit, disputed evidence, migration checks, or whole-record review.

## Examples first

Example E1: registered evidence routes deterministically
Given `docs/changes/2026-05-22-example/behavior-preservation.md` matches a registered `preservation` evidence class
When the changed-path selector evaluates the actual changed paths for the branch
Then the selector selects the registered lifecycle/review validation routes
And the file does not produce `manual-routing-required`.

Example E2: unregistered deterministic evidence creates registration debt
Given `docs/changes/2026-05-22-example/new-proof.md` does not match a registered evidence class
When the changed-path selector evaluates the actual changed paths for the branch
Then selector output includes a stable `manual-routing-required` diagnostic for that path
And the active plan or change-local evidence records registration debt before verify.

Example E3: broad evidence patterns are rejected
Given a proposed evidence class pattern is `*.md` under `docs/changes/<change-id>/`
When the registry is validated
Then validation rejects the pattern as too broad because it can silently capture unrelated evidence classes.

Example E4: actual changed paths cannot be replaced by a fixture
Given a branch adds `docs/changes/2026-05-22-example/identity-proof.txt`
When implementation or code-review proof runs selector validation
Then it validates routing against the branch's actual changed paths
And any changed-set fixture is supplemental only.

Example E5: summary query avoids validation history
Given a compact or legacy `change.yaml` has artifact paths, review state, validation state, blockers, and validation event history
When `python scripts/query-change-record.py 2026-05-22-example summary` runs
Then output includes change ID, canonical artifact paths, review state, latest validation state, blockers, and detail pointers
And it does not require reading full validation event history to answer that summary question.

Example E6: latest validation query returns only latest validation evidence
Given a change record contains validation evidence for proposal-review, spec-review, plan-review, and code-review
When `python scripts/query-change-record.py 2026-05-22-example validation --latest` runs
Then output contains only the latest validation stage, bundles, result, counts, blockers, and transcript pointer when present.

Example E7: stage validation query is stage-scoped
Given a change record contains validation evidence for multiple stages
When `python scripts/query-change-record.py 2026-05-22-example validation --stage spec-review-r1` runs
Then output contains only validation evidence for `spec-review-r1`
And it does not include unrelated stage events except detail pointers needed to locate full history.

Example E8: full-read escalation remains available
Given a reviewer disputes whether the validation summary hides a failed command
When the reviewer requests forensic reconstruction
Then the workflow permits reading full `change.yaml`, validation events, transcript references, and related change-local evidence.

Example E9: stage skill names its slice
Given a stage skill needs final validation state
When the skill guidance is updated under Workstream B
Then it names the bounded slice or query-helper command it uses
And it names conditions that require full-read escalation.

## Requirements

### Evidence registration and selector routing

CRM-R1. The repository MUST define an evidence class registry for recurring deterministic change-local evidence files.

CRM-R2. Each registry entry MUST define a stable evidence class ID, allowed root, bounded filename pattern or exact filename, selector route, required validator, lifecycle stage, and allowed/required/forbidden conditions.

CRM-R3. Evidence class IDs MUST be stable ASCII identifiers with no whitespace.

CRM-R4. Registered filename patterns MUST be bounded to the evidence class they represent.

CRM-R5. Registry validation MUST reject broad catch-all patterns such as `*.md`, `*.txt`, or equivalent patterns under `docs/changes/<change-id>/`.

CRM-R6. Exact filename registration MUST remain allowed for genuinely novel evidence classes when no safe recurring pattern exists.

CRM-R7. A deterministic change-local evidence file MUST either match exactly one registered evidence class or produce a stable `manual-routing-required` diagnostic.

CRM-R8. A deterministic change-local evidence file MUST NOT silently pass changed-path selector routing when it is unregistered.

CRM-R9. A registered evidence file MUST route to the selector check IDs and affected roots declared by its evidence class.

CRM-R10. A registered evidence file MUST include its governing `docs/changes/<change-id>/change.yaml` in lifecycle validation when the selected route needs change-local context.

CRM-R11. Registry changes MUST trigger selector regression coverage.

CRM-R12. Selector routing for changed evidence files MUST be validated against the change's actual changed paths before verify.

CRM-R13. Changed-set fixtures MAY supplement selector proof but MUST NOT substitute for routing the branch's own actual changed paths.

CRM-R14. Explicit-path validation MAY supplement changed-path routing proof but MUST NOT replace changed-path routing proof when a new evidence class or new evidence file appears.

CRM-R15. Verify MUST NOT be the first stage that discovers `manual-routing-required` for deterministic in-repo evidence added earlier in the change.

CRM-R16. `manual-routing-required` for deterministic in-repo evidence MUST create registration debt.

CRM-R17. Registration debt MUST be resolved before verify unless an owner-approved deferral records that the evidence class is intentionally unsupported for this change.

CRM-R18. Owner-approved deferral for deterministic evidence MUST name the owner, path, reason, validation impact, and follow-up location.

CRM-R19. An unresolved `manual-routing-required` diagnostic for deterministic in-repo evidence MUST block verify readiness unless CRM-R18 is satisfied.

CRM-R20. The first implementation slice MUST cover Workstream A only: evidence class registry, registered pattern routing, actual changed-path routing proof, supplemental selector fixtures, and registration debt handling.

CRM-R21. Workstream A MUST NOT require implementation of the query helper or stage-skill guidance changes.

### Bounded read/query model

CRM-R22. The system MUST define a bounded read contract for common change-record questions.

CRM-R23. The bounded read contract MUST map each common question to the smallest authoritative surface that owns the answer.

CRM-R24. Current live workflow state MUST be read from the active plan `Current Handoff Summary`, not from historical change metadata.

CRM-R25. Durable rationale MUST be read from `explain-change.md` or its approved legacy equivalent.

CRM-R26. Review finding status MUST be read from `review-log.md` and `review-resolution.md` when those artifacts exist.

CRM-R27. Validation command/result inventory MAY be read from `change.yaml`.

CRM-R28. Final validation state MUST be read from `change.yaml.validation_summary` or the legacy equivalent recognized by the query helper.

CRM-R29. Owning artifact paths MUST be available from `change.yaml` artifact/path metadata or the query helper.

CRM-R30. The query helper MUST support at least these commands:

```text
python scripts/query-change-record.py <change-id> summary
python scripts/query-change-record.py <change-id> artifacts
python scripts/query-change-record.py <change-id> validation --latest
python scripts/query-change-record.py <change-id> validation --stage <stage>
```

CRM-R31. The query helper SHOULD support review, blockers, and forensic subcommands when the implementation slice includes those read paths.

CRM-R32. `summary` output MUST include change ID, canonical artifact paths, review state, latest validation state, open blockers, and detail pointers.

CRM-R33. `artifacts` output MUST include canonical artifact paths only.

CRM-R34. `validation --latest` output MUST include only the latest validation stage, bundles, result, counts, blockers, and transcript pointer when present.

CRM-R35. `validation --stage <stage>` output MUST include only the requested stage's validation evidence and detail pointers needed to locate full history.

CRM-R36. The query helper MUST support legacy and compact change metadata shapes that remain valid under existing metadata contracts.

CRM-R37. The query helper MUST report a stable unsupported-shape diagnostic when it cannot safely query a valid or invalid change metadata shape.

CRM-R38. The query helper MUST NOT hide failures, blockers, skipped validation, or unsupported-shape diagnostics.

CRM-R39. The query helper MUST NOT execute validation bundle commands while querying metadata.

CRM-R40. Query outputs MUST be deterministic for the same repository state and inputs.

CRM-R41. Query outputs MUST use repo-relative paths and MUST NOT emit machine-local path expansions.

CRM-R42. Common-read fields in new or amended compact metadata SHOULD appear before historical validation detail when the compact metadata spec permits that ordering.

CRM-R43. Full `change.yaml` or full change-record reads MUST remain allowed for forensic reconstruction, summary inconsistency investigation, disputed evidence, selector-routing debugging, legacy/compact migration validation, unsupported query-helper shapes, and whole-record review.

CRM-R44. Stage-skill guidance updated under Workstream B MUST name the bounded slice or query-helper command used for each stage-owned change-record question.

CRM-R45. Stage-skill guidance updated under Workstream B MUST name the escalation conditions that require a full read.

CRM-R46. Stage-skill guidance MUST NOT say only "read `change.yaml`" for a common stage-owned question when a bounded slice or query-helper command exists.

CRM-R47. Stage-skill guidance changes MUST be made only after query-helper commands referenced by those skills are stable.

CRM-R48. Generated adapter output MUST be validated when canonical stage-skill text changes.

### Compatibility, sequencing, and ownership

CRM-R49. This feature MUST NOT change lifecycle stage order, review status meanings, milestone state values, final readiness semantics, or branch/PR readiness semantics.

CRM-R50. This feature MUST NOT weaken validation selector safety, selected-check coverage, command exit behavior, failure detection, or required validation evidence.

CRM-R51. This feature MUST preserve existing valid change records during migration.

CRM-R52. Historical change records MUST NOT require bulk migration in the first implementation slice.

CRM-R53. A new query helper script MUST be used for query behavior rather than adding query semantics as a subcommand of `validate-change-metadata.py`.

CRM-R54. The evidence class registry SHOULD be centralized in one registry surface when the selector architecture supports that shape.

CRM-R55. If selector architecture does not support a centralized registry file in the first implementation slice, the selector MAY keep the registry table in selector-owned code, but fixture-backed tests MUST cover the registry behavior.

CRM-R56. The feature spec MUST remain the top-level contract for registration and read behavior while preserving explicit dependency references to selector, compact metadata, workflow, and skill-contract specs.

## Inputs and outputs

Inputs:

- Changed paths from the local worktree, explicit selector invocation, PR diff, or equivalent repository-owned changed-path source.
- Files under `docs/changes/<change-id>/`.
- Evidence class registry entries.
- Existing `change.yaml` files in legacy or compact metadata shape.
- Review artifacts, review logs, review resolutions, explain-change artifacts, active plans, and validation transcripts when referenced.
- Query helper command arguments.
- Stage-skill guidance text and generated adapter output when Workstream B changes skills.

Outputs:

- Selector output that routes registered evidence files or reports stable `manual-routing-required` diagnostics.
- Registration-debt evidence when deterministic evidence cannot route.
- Query-helper output for `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>`.
- Stable unsupported-shape diagnostics for unsupported query-helper inputs.
- Stage-skill guidance that names bounded change-record read slices and escalation conditions.
- Validation evidence proving actual changed-path routing before verify.

## State and invariants

- A change record is a queried catalog, not a transcript.
- Every deterministic change-local evidence file is either registered or explicitly diagnosed as registration debt.
- Registered evidence classes own selector routing for their matching files.
- Actual changed-path routing proof is required before verify for changes adding deterministic evidence files.
- Fixtures supplement, but do not replace, actual changed-path proof.
- `manual-routing-required` is a temporary diagnostic, not a durable workaround.
- `change.yaml` remains authoritative for validation inventory and summaries, but not for every workflow state question.
- The active plan remains authoritative for current live workflow state.
- Full forensic detail remains recoverable when needed.
- Workstream A and Workstream B have separate rollback surfaces.

## Error and boundary behavior

- An evidence file matching no registered class produces `manual-routing-required`.
- An evidence file matching multiple registered classes fails registry or selector validation as ambiguous.
- A registry pattern that captures an entire extension under `docs/changes/<change-id>/` fails validation as too broad.
- A registry entry missing selector route, validator, allowed root, or lifecycle expectations fails validation.
- A selector route that omits the governing change metadata when lifecycle context is required fails validation.
- A branch that adds deterministic evidence and reaches verify with unresolved `manual-routing-required` fails readiness unless owner-approved deferral is recorded.
- A query for an unknown change ID fails with a stable not-found diagnostic.
- A query for an unknown subcommand or invalid option fails with a stable usage diagnostic.
- `validation --stage <stage>` fails with a stable stage-not-found diagnostic when the requested stage is absent.
- Query helper output fails or reports unsupported shape rather than guessing when metadata is malformed, ambiguous, or unsupported.
- Query helper failures must not modify repository files.
- Stage-skill guidance must escalate to full reads when bounded evidence is missing, stale, contradictory, or insufficient.

## Compatibility and migration

- Existing selector behavior for already-routed paths remains valid unless intentionally changed by registered evidence routing.
- Existing valid legacy and compact `change.yaml` files remain valid.
- Existing change-local lifecycle artifacts remain governed by their existing validators.
- Historical unregistered evidence files do not need bulk migration in the first slice.
- New deterministic evidence classes introduced after Workstream A must register routing in the same change or record owner-approved unsupported status before verify.
- The query helper must accept both legacy and compact metadata shapes that existing validators accept, or report a stable unsupported-shape diagnostic where a shape cannot be queried safely.
- Rollback of Workstream A may remove registry-based routing but must not invalidate existing change records.
- Rollback of Workstream B may remove query helper and skill guidance changes without deleting evidence files or weakening existing validation.

## Observability

- Selector output MUST expose registered routes, selected check IDs, affected roots, and blocking `manual-routing-required` diagnostics through the existing selector output contract.
- Registration-debt records MUST be visible in the active plan, change-local evidence, or owner-approved deferral surface before verify.
- Query helper diagnostics MUST use stable labels suitable for test assertions.
- Query helper outputs MUST expose detail pointers so readers can escalate from bounded reads to full forensic reads.
- Validation evidence for implementation and review MUST name the actual changed-path selector command used.
- Generated adapter validation MUST be recorded when skill guidance changes affect published skill text.

## Security and privacy

- Registry entries, query-helper output, diagnostics, and detail pointers MUST use repository-relative paths.
- Query helper output MUST NOT expose secrets, credentials, tokens, private keys, proxy URLs, home-directory paths, machine-local usernames, or host-specific paths.
- Query helper behavior MUST NOT execute validation bundle commands or arbitrary commands from change metadata.
- Evidence class registration MUST NOT make untrusted paths outside `docs/changes/<change-id>/` routable as change-local evidence.
- Unsupported or malformed metadata MUST fail closed with a diagnostic rather than fall through to broad filesystem reads.

## Accessibility and UX

Not applicable to graphical UI accessibility.

Contributor UX requirements:

- Selector diagnostics should identify the path, evidence class decision, and required next action.
- Query-helper output should be concise enough for common stage-owned questions and should include detail pointers for deeper reads.
- Stage-skill wording should guide readers to bounded slices before full-file reads.

## Performance expectations

- Evidence class matching SHOULD be linear in the number of changed paths times the number of registered evidence patterns.
- Query helper `summary`, `artifacts`, `validation --latest`, and `validation --stage <stage>` SHOULD avoid loading unrelated transcript files.
- Query helper behavior MUST NOT execute validation commands.
- Selector routing validation over actual changed paths SHOULD remain suitable for implementation and code-review proof on ordinary branch diffs.
- Registry validation SHOULD reject broad patterns statically before selector routing depends on them.

## Edge cases

EC1. A changed file is `docs/changes/<change-id>/behavior-preservation.md` and matches `preservation`; it routes through the registered selector route.

EC2. A changed file is `docs/changes/<change-id>/behavior-preservation.md` but both `preservation` and `audit` patterns match; validation fails as ambiguous.

EC3. A changed file is `docs/changes/<change-id>/notes.md` and no registry entry matches; selector output includes `manual-routing-required`.

EC4. A new registry entry uses `*.md`; registry validation fails as too broad.

EC5. A new registry entry uses `*-audit.md`; registry validation can pass when selector routes, validators, and lifecycle rules are present.

EC6. A branch adds a registered evidence file and only runs explicit-path lifecycle validation; proof is incomplete until actual changed-path selector routing also runs.

EC7. A branch adds an unregistered evidence file and records owner-approved unsupported status before verify; verify may proceed only if the deferral includes owner, path, reason, validation impact, and follow-up.

EC8. A branch adds an unregistered evidence file and reaches verify with no owner-approved deferral; verify readiness fails.

EC9. `summary` runs on a compact `change.yaml`; it returns summary fields without transcript internals.

EC10. `summary` runs on a legacy `change.yaml`; it returns the best supported equivalent fields or reports unsupported shape when safe querying is impossible.

EC11. `validation --latest` runs when no validation evidence exists; it reports a stable no-validation-evidence diagnostic.

EC12. `validation --stage spec-review-r1` runs when only `proposal-review-r1` exists; it reports a stable stage-not-found diagnostic.

EC13. A query helper encounters malformed YAML; it fails with an unsupported-shape or parse diagnostic and does not modify files.

EC14. A stage skill needs to investigate disputed validation history; it escalates to full validation events or transcript references.

EC15. A stage skill only needs current live workflow state; it reads the active plan rather than `change.yaml`.

EC16. Stage-skill guidance is edited before query helper command names stabilize; spec review or implementation review rejects the sequencing.

EC17. Skill guidance changes but generated adapter output is not validated; readiness fails for the Workstream B slice.

EC18. The selector architecture cannot support a separate registry file in the first slice; an in-selector table with fixture-backed tests satisfies the first-slice registry contract.

## Non-goals

- Do not weaken changed-path selector safety.
- Do not make unregistered evidence files silently pass.
- Do not make `manual-routing-required` a permanent workaround for deterministic in-repo evidence.
- Do not require agents to read the whole `change.yaml` for stage-local questions.
- Do not replace the active plan, review log, review resolution, explain-change, or other authoritative state owners.
- Do not make `change.yaml` the default source for questions owned by another artifact.
- Do not remove existing validation, review, or lifecycle evidence.
- Do not bulk-migrate historical change records in the first slice.
- Do not change compact validation metadata semantics unless a later approved amendment requires it.
- Do not change workflow stage order, review status meanings, milestone state values, branch readiness, or PR readiness semantics.
- Do not add automated evidence-file scaffolding in this feature.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-CRM-001 | Registered evidence classes have bounded filename patterns or exact filenames, deterministic selector routes, validators, allowed roots, and lifecycle expectations. |
| AC-CRM-002 | A newly added evidence file matching a registered pattern routes without `manual-routing-required`. |
| AC-CRM-003 | A deterministic unregistered evidence file produces `manual-routing-required` with a stable diagnostic. |
| AC-CRM-004 | `manual-routing-required` for deterministic in-repo evidence is tracked as registration debt before verify or has owner-approved deferral. |
| AC-CRM-005 | Changed-path routing is validated against the change's actual changed paths before verify; fixtures are supplemental only. |
| AC-CRM-006 | Registry validation rejects broad catch-all patterns. |
| AC-CRM-007 | Ambiguous evidence class matches fail validation. |
| AC-CRM-008 | Query helper `summary` returns change ID, artifact paths, review state, latest validation state, blockers, and detail pointers without loading full validation history. |
| AC-CRM-009 | Query helper `artifacts` returns canonical artifact paths only. |
| AC-CRM-010 | Query helper `validation --latest` returns only the latest validation result, bundles, counts, blockers, and transcript pointer. |
| AC-CRM-011 | Query helper `validation --stage <stage>` returns only the requested stage's validation evidence. |
| AC-CRM-012 | Query helper supports valid legacy and compact metadata shapes, or reports a stable unsupported-shape diagnostic. |
| AC-CRM-013 | Stage-skill guidance names exact change-record slices or query-helper commands for stage-owned questions. |
| AC-CRM-014 | Full change-record reads remain allowed for forensic reconstruction, disputed evidence, unsupported shapes, and whole-record review. |
| AC-CRM-015 | Existing valid change records remain valid during migration. |
| AC-CRM-016 | Generated adapter output is validated when skill guidance changes. |
| AC-CRM-017 | No validation selection, review status, lifecycle state, final readiness, or branch/PR readiness semantics change. |

## Open questions

None.

## Next artifacts

```text
spec-review
architecture, when required by the architecture gate
architecture-review, when architecture is required
plan
plan-review
test-spec
implementation Workstream A
code-review
implementation Workstream B
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Spec review approved. Ready for `architecture`.
