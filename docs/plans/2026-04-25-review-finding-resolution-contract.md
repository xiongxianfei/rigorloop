# Review finding resolution contract implementation plan

- Status: active
- Owner: maintainer + Codex
- Start date: 2026-04-25
- Last updated: 2026-04-25
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the approved review finding resolution contract as a small, auditable workflow and validation change. The work should make material review findings actionable, preserve first-pass review history, create a deterministic review-log and review-resolution structure, validate those artifacts without judging review quality, and keep generated Codex and public adapter outputs synchronized when canonical skills change.

The implementation must preserve lightweight clean reviews. The full review artifact chain is required only when material findings or an independently created `reviews/` directory trigger it.

## Source artifacts

- Proposal: `docs/proposals/2026-04-24-review-finding-resolution-contract.md`
- Spec: `specs/review-finding-resolution-contract.md`
- Spec review: `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/spec-review-r1.md` and `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/spec-review-r2.md`
- Architecture: `docs/architecture/2026-04-24-review-finding-resolution-contract.md`
- Architecture review: `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/architecture-review-r1.md` and `docs/changes/2026-04-24-review-finding-resolution-contract/reviews/architecture-review-r2.md`
- Review resolution: `docs/changes/2026-04-24-review-finding-resolution-contract/review-resolution.md`
- Test spec: `specs/review-finding-resolution-contract.test.md`
- Existing workflow contract: `specs/rigorloop-workflow.md`
- Related docs changes architecture: `docs/architecture/2026-04-21-docs-changes-usage-policy.md`
- Related generated adapter ADR: `docs/adr/ADR-20260424-generated-adapter-packages.md`
- Project map: none exists. Existing source layout is small enough for this plan to orient from scripts, docs, specs, skills, and architecture.

## Context and orientation

- Change-local artifacts live under `docs/changes/<change-id>/`.
- Existing `scripts/validate-change-metadata.py` validates `change.yaml` shape and canonical artifact keys; it should not absorb detailed review Markdown parsing.
- Existing `scripts/artifact_lifecycle_validation.py` validates top-level proposal, spec, test-spec, architecture, and ADR lifecycle state; it should not become the per-change review-artifact validator.
- Existing CI orchestration lives in `scripts/ci.sh` and already delegates to repository-owned scripts.
- Existing validator tests are simple standard-library Python scripts such as `scripts/test-change-metadata-validator.py` and `scripts/test-artifact-lifecycle-validator.py`.
- Canonical workflow skills live under `skills/`.
- Generated local Codex skill output lives under `.codex/skills/` and must be regenerated through `python scripts/build-skills.py`.
- Public generated adapter output lives under `dist/adapters/` and must be regenerated through `python scripts/build-adapters.py --version 0.1.1` when shipped canonical skills change.
- The current workflow contract still names only `accepted`, `rejected`, and `deferred` in `R12a`; this feature must align it with `partially-accepted` and `needs-decision`.
- `review-resolution.md` for this change is already closed after `architecture-review-r2`; future implementation reviews may add new review records and must follow the same artifact contract.

## Non-goals

- Capturing maintainer PR review comments into `reviews/` in this version.
- Automating semantic review-quality judgment.
- Requiring a full review artifact pack for every non-trivial change.
- Requiring empty `review-resolution.md`, `review-log.md`, or `reviews/` files for clean reviews.
- Replacing human review, reviewer judgment, maintainer decisions, or the existing PR process.
- Changing runtime product behavior outside the repository workflow contract.
- Retiring `.codex/skills/` or changing the public adapter package layout.
- Adding third-party dependencies, network calls, credentials, secrets, or default permission changes.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R1d` | Review-stage skill guidance and workflow docs for complete material findings |
| `R2`-`R2o` | Review artifact parser, validator fixtures, workflow docs, and review-stage skill guidance |
| `R3`-`R3k` | Canonical `review-log.md` parser, ledger validation, fixtures, docs, and skills |
| `R4`-`R4c` | Finding ID parser, uniqueness checks, fixtures, docs, and skills |
| `R5`-`R5i` | `review-resolution.md` parser, resolution entry validation, docs, and skills |
| `R6`-`R6m` | Disposition vocabulary, top-level closeout status checks, closeout mode, docs, and skills |
| `R7`-`R7d` | Disposition-specific closeout field checks and validation fixtures |
| `R8`-`R8h` | `verify`, `explain-change`, and `pr` guidance plus closeout-gated validator mode |
| `R9`-`R10c` | `explain-change` and `pr` skill guidance for concise summary and linked resolution details |
| `R11`-`R11b` | `scripts/review_artifact_validation.py`, `scripts/validate-review-artifacts.py`, and `scripts/test-review-artifact-validator.py` |
| `R12`-`R12c` | Generated `.codex/skills/` and `dist/adapters/` sync after canonical skill changes |
| `R13`-`R13b` | Clean-review lightweight path in workflow docs, skills, and validator behavior |
| `R14`-`R14a` | `specs/rigorloop-workflow.md`, `docs/workflows.md`, `CONSTITUTION.md` or `AGENTS.md` summaries when affected, and canonical skills |

## Milestones

### M1. Review artifact parser and structure-mode validation

- Goal:
  - Add the repository-owned parser and structure-mode validator for detailed review files, canonical review-log blocks, material Finding IDs, and review-resolution references.
- Requirements:
  - `R2`-`R5i`, `R6`, `R11`, `R11a`, `R11b`, `R13`-`R13b`
- Files/components likely touched:
  - `scripts/review_artifact_validation.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/test-review-artifact-validator.py`
  - `tests/fixtures/review-artifacts/`
  - `docs/changes/2026-04-24-review-finding-resolution-contract/` only if the new validator needs this change as a live fixture
- Dependencies:
  - approved spec and architecture
  - no third-party packages
  - no reliance on external review tools
- Tests to add/update:
  - valid structure fixture with one review record, review-log entry, finding, and resolution entry
  - valid clean review fixture with `reviews/` and `review-log.md` but no material findings
  - `reviews/` exists without `review-log.md`
  - missing Review ID, stage, round, reviewer, target, or status
  - zero Review IDs and multiple Review IDs in one detailed review file
  - duplicate Review IDs in one change
  - canonical review-log entry missing a required field
  - Review ID prose mention outside a `### Review entry` block does not satisfy the ledger
  - review-log entry references an unknown detailed review file
  - duplicate Finding IDs in one change
  - material Finding ID missing from `review-resolution.md`
  - `review-resolution.md` references an unknown Finding ID
  - unsupported disposition value
  - reconstructed record missing required reconstructed metadata
- Implementation steps:
  - define line-based field extraction helpers with path and line-number reporting
  - parse `reviews/*.md` into `ReviewRecord` and `FindingRecord`
  - parse `review-log.md` only through canonical `### Review entry` blocks
  - parse top-level `Closeout status:` and finding-level `Finding ID:` plus `Disposition:` entries from `review-resolution.md`
  - implement structure-mode checks from the spec and architecture
  - implement the CLI default mode as `structure`
  - add fixture-driven tests using temporary directories where needed
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-04-24-review-finding-resolution-contract`
  - `git diff --check -- scripts tests docs/changes/2026-04-24-review-finding-resolution-contract docs/plans/2026-04-25-review-finding-resolution-contract.md`
- Expected observable result:
  - structure-mode validation catches malformed review artifacts while accepting open but structurally valid in-progress review-resolution records.
- Commit message: `M1: add review artifact structure validation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - parser accidentally counts incidental prose as a ledger reference
  - structure mode becomes too strict for in-progress review work
  - reconstructed-record validation may allow silent retroactive cleanup if metadata fields are too weak
- Rollback/recovery:
  - revert the new validator scripts and fixtures without changing workflow docs or skills
  - if parsing ambiguity appears, tighten accepted label forms before enabling CI

### M2. Closeout-mode validation and CI integration

- Goal:
  - Add closeout-gated validation for `verify`, `explain-change`, and `pr`, then wire structure validation into local CI for touched change roots.
- Requirements:
  - `R6a`-`R8h`, `R11`, `R13`-`R13b`
- Files/components likely touched:
  - `scripts/review_artifact_validation.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/ci.sh`
  - `tests/fixtures/review-artifacts/`
- Dependencies:
  - M1 parser and structure-mode validator
  - active test spec coverage for closeout conditions
- Tests to add/update:
  - `Closeout status: open` fails in closeout mode
  - `needs-decision` fails in closeout mode
  - accepted finding missing chosen action fails in closeout mode
  - accepted finding missing validation evidence fails in closeout mode
  - rejected finding missing rationale fails in closeout mode
  - deferred finding missing rationale fails in closeout mode
  - deferred finding missing follow-up owner, owning stage, or no-follow-up reason fails in closeout mode
  - partially accepted finding missing accepted portion, non-accepted portion, rationale, or validation evidence fails in closeout mode
  - closed fixture with all disposition-specific records passes
  - CI invokes structure-mode validation for changed `docs/changes/<change-id>/` roots without globally failing old historical examples
- Implementation steps:
  - add `--mode structure|closeout` to the CLI, defaulting to `structure`
  - implement closeout status and disposition-specific field checks
  - keep field presence validation structural and do not judge rationale quality
  - update `scripts/ci.sh` to discover changed `docs/changes/<change-id>/` roots and run structure mode
  - ensure generated paths are still excluded from authored artifact lifecycle validation
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract`
  - `bash scripts/ci.sh`
  - `git diff --check -- scripts tests docs/changes/2026-04-24-review-finding-resolution-contract docs/plans/2026-04-25-review-finding-resolution-contract.md`
- Expected observable result:
  - closeout mode blocks unresolved material findings, while CI can validate structure for active change roots without retroactive migration.
- Commit message: `M2: add review artifact closeout validation`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - CI may become noisy if it validates every historical change root
  - closeout mode may accidentally require clean reviews to create empty artifacts
  - field-presence checks may drift into semantic review-quality automation
- Rollback/recovery:
  - disable CI invocation first if it blocks unrelated work
  - keep the CLI available for explicit closeout checks while scope selection is fixed
  - narrow closeout checks to field presence rather than weakening disposition requirements

### M3. Workflow contract, skills, docs, and generated outputs

- Goal:
  - Align current workflow guidance, stage skills, generated Codex output, and public adapters with the expanded disposition vocabulary and review artifact flow.
- Requirements:
  - `R1`-`R1d`, `R5`-`R10c`, `R12`-`R12c`, `R14`-`R14a`
- Files/components likely touched:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `skills/code-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `.codex/skills/`
  - `dist/adapters/`
  - `dist/adapters/manifest.yaml`
- Dependencies:
  - M1 and M2 validator behavior
  - existing generated adapter version target `0.1.1`
  - approved generated adapter ADR
- Tests to add/update:
  - skill validation continues to accept updated canonical skills
  - generated skill drift check detects stale `.codex/skills/`
  - adapter drift check detects stale public adapters after shipped skill changes
  - adapter validation rejects unsupported tool-specific metadata leaks
  - grep/assertion checks that current guidance names `partially-accepted` and `needs-decision` where disposition vocabulary is authoritative
  - grep/assertion checks that PR guidance summarizes counts and links `review-resolution.md` instead of duplicating findings
- Implementation steps:
  - update `specs/rigorloop-workflow.md` to replace the old three-value disposition vocabulary with the approved expanded contract
  - update workflow summaries only where they summarize current behavior
  - update review, verify, explain-change, and PR skills to record complete findings, preserve first-pass records, use review-resolution closeout, and summarize PR review resolution
  - regenerate `.codex/skills/` after canonical skill changes
  - regenerate `dist/adapters/` after canonical shipped skill changes
  - avoid hand-editing generated outputs
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `rg -n "partially-accepted|needs-decision|Closeout status|review-resolution.md" specs/rigorloop-workflow.md docs/workflows.md CONSTITUTION.md AGENTS.md skills .codex/skills dist/adapters`
  - `git diff --check -- specs docs skills .codex/skills dist AGENTS.md CONSTITUTION.md`
- Expected observable result:
  - workflow-facing docs and skill packages no longer contradict the approved disposition and closeout contract, and generated outputs are in sync.
- Commit message: `M3: align review resolution workflow guidance`
- Milestone closeout:
  - [x] targeted validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - canonical skill changes may be portable in Codex but not in Claude Code or OpenCode adapters
  - summaries may overstate the standalone artifact requirement and break clean-review lightweight behavior
  - generated outputs may be stale if generation commands are skipped
- Rollback/recovery:
  - revert canonical skill and docs changes, then regenerate generated outputs from the reverted canonical state
  - if a skill becomes non-portable, either rewrite the tool-specific wording or exclude it through existing adapter validation

### M4. Lifecycle closeout, final validation, and PR readiness

- Goal:
  - Complete the change-local artifact pack, close plan lifecycle state when implementation is done, and prepare for code review, verify, explain-change, and PR.
- Requirements:
  - all in-scope requirements plus repository lifecycle and validation rules
- Files/components likely touched:
  - `docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `docs/changes/2026-04-24-review-finding-resolution-contract/explain-change.md`
  - `docs/changes/2026-04-24-review-finding-resolution-contract/review-log.md`
  - `docs/changes/2026-04-24-review-finding-resolution-contract/review-resolution.md`
  - `docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - `docs/plan.md`
  - `specs/review-finding-resolution-contract.test.md`
  - any touched authoritative artifacts whose readiness or follow-on state changed
- Dependencies:
  - M1 through M3 complete
  - `plan-review` complete
  - `test-spec` complete and active
  - implementation `code-review` complete or its findings recorded and resolved
- Tests to add/update:
  - final validator coverage named in the test spec
  - artifact lifecycle explicit-path validation for touched lifecycle artifacts
  - generated-output drift checks after skill and adapter changes
- Implementation steps:
  - keep this plan's progress, decision log, surprises, and validation notes current as milestones complete
  - update `change.yaml` with final artifacts, tests, changed files, validation commands, and review status
  - create `explain-change.md` after verification, not before final behavior is known
  - run `code-review` and record any material findings using this contract
  - run `verify` and block on stale artifacts, open review-resolution, generated drift, or missing validation evidence
  - move this plan from Active to Done in `docs/plan.md` only when implementation and verification are complete
- Validation commands:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `bash scripts/ci.sh`
  - `git diff --check -- .`
- Expected observable result:
  - the branch has validator-backed review artifact behavior, updated workflow guidance, synchronized generated outputs, closed review findings, and lifecycle artifacts ready for PR review.
- Commit message: `M4: close review resolution contract implementation`
- Milestone closeout:
  - [ ] targeted validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - final verification may reveal stale lifecycle state between `docs/plan.md` and this plan body
  - generated outputs may drift after last-minute skill edits
  - review-resolution closeout may be incomplete if implementation review findings are added late
- Rollback/recovery:
  - leave the plan active and review-resolution open until findings are resolved
  - revert final guidance and generated outputs together if generated drift cannot be reconciled
  - do not mark `docs/plan.md` done until verify evidence is recorded

## Validation plan

- Before implementation:
  - run `plan-review`
  - create and review `specs/review-finding-resolution-contract.test.md`
  - confirm architecture status is `approved`
- During each milestone:
  - run the milestone-specific unit or fixture tests first
  - run the focused validator or generation command that proves the changed surface
  - update this plan's progress and validation notes before moving to the next milestone
- Before PR:
  - run the final command set from M4
  - record accepted review-fix evidence in `review-resolution.md`
  - keep `explain-change.md` concise and link detailed review artifacts instead of duplicating them

## Risks and recovery

- Risk: parser rules reject valid author intent because Markdown is flexible.
- Recovery: document and test one canonical parseable form for v1; leave other prose as non-parseable context.
- Risk: validator scope blocks historical artifacts.
- Recovery: validate explicit, changed, or active change roots first; do not run repository-wide review-artifact validation until a migration is approved.
- Risk: closeout validation drifts into semantic review judgment.
- Recovery: limit closeout mode to required field presence, allowed values, known IDs, and documented status rules.
- Risk: workflow summaries overrequire full review packs.
- Recovery: keep clean-review lightweight behavior explicit in specs, docs, and skills.
- Risk: canonical skill changes stale generated outputs.
- Recovery: regenerate `.codex/skills/` and `dist/adapters/` from canonical `skills/`, then run drift and adapter validation.
- Risk: implementation review finds a spec or architecture gap.
- Recovery: stop implementation, update the governing artifact, rerun the appropriate review, and only then resume the plan.

## Dependencies

- `plan-review` must complete before implementation.
- `test-spec` must be created and active before implementation.
- No external services or network access are required.
- No real Codex, Claude Code, or OpenCode installation is required for non-smoke validation.
- `scripts/ci.sh` remains the repository-wide local validation wrapper.
- Generated outputs must be regenerated rather than hand-edited.

## Progress

- [x] 2026-04-25: Plan created.
- [x] 2026-04-25: Plan-review approved with no required edits.
- [x] 2026-04-25: Test spec created and activated.
- [x] M1. Review artifact parser and structure-mode validation.
- [x] 2026-04-25: M1 tests added first and confirmed red on missing `review_artifact_validation` module.
- [x] 2026-04-25: M1 structure-mode validator, CLI, and fixture coverage implemented.
- [x] 2026-04-25: M1 milestone commit.
- [x] M2. Closeout-mode validation and CI integration.
- [x] 2026-04-25: M2 tests added first and confirmed red on unsupported `closeout` mode plus missing CI review-artifact checks.
- [x] 2026-04-25: M2 closeout mode, blocking-review rerun or explicit closeout checks, and CI changed-root structure validation implemented.
- [x] 2026-04-25: M2 milestone commit.
- [x] 2026-04-25: `code-review-r1` finding `CR1-F1` recorded before fixes, accepted, fixed, and closed with explicit review closeout evidence.
- [x] 2026-04-25: M3 contract tests added first and confirmed red on missing expanded workflow guidance and stale generated adapters.
- [x] 2026-04-25: M3 workflow contract, governance summaries, review-stage skills, verify, explain-change, PR, and workflow skills aligned with the expanded review-resolution closeout contract.
- [x] 2026-04-25: M3 `.codex/skills/` and public adapter skill outputs regenerated from canonical `skills/`.
- [x] M3. Workflow contract, skills, docs, and generated outputs.
- [ ] M4. Lifecycle closeout, final validation, and PR readiness.

## Decision log

- 2026-04-25: Use a dedicated `review_artifact_validation.py` module instead of extending change metadata or artifact lifecycle validation. Rationale: the approved architecture keeps per-change review Markdown parsing separate from top-level lifecycle and `change.yaml` metadata validation.
- 2026-04-25: Split validator behavior into `structure` and `closeout` modes. Rationale: in-progress review-resolution records must be structurally valid before they are final.
- 2026-04-25: Keep generated adapter synchronization in the plan because canonical shipped skills will change. Rationale: public adapters are generated consumers of canonical workflow guidance.
- 2026-04-25: Treat `test-spec` as a prerequisite to implementation, not as an implementation milestone. Rationale: the repository workflow requires test planning before writing production code.
- 2026-04-25: Implement M1 with only `structure` mode exposed by `scripts/validate-review-artifacts.py`; `closeout` mode and CI discovery remain M2 scope. Rationale: M1 proves parseable artifact structure while preserving the planned milestone boundary.
- 2026-04-25: M2 recognizes same-stage nonblocking re-review and `Review closeout: <Review ID>` as structural proof that a blocking review outcome no longer blocks closeout. Rationale: the spec allows rerun or explicit reviewer/owner closeout, and both need deterministic parser-visible representations.
- 2026-04-25: After `code-review-r1`, same-stage nonblocking rerun proof now requires a strictly later numeric round. Rationale: a same-stage, same-round nonblocking entry is not a rerun; when round ordering cannot be proven, closeout must use explicit `Review closeout: <Review ID>` evidence naming the original blocking review.
- 2026-04-25: Keep `dist/adapters/manifest.yaml` unchanged for M3. Rationale: M3 changes shipped skill bodies and generated package contents, but not the supported skill set, adapter list, command aliases, generated file paths, or manifest-declared metadata.

## Surprises and discoveries

- 2026-04-25: The live change-local review artifacts already satisfy the new M1 canonical `review-log.md`, detailed review, Finding ID, and `review-resolution.md` structure.
- 2026-04-25: Full `bash scripts/ci.sh` now runs review-artifact fixture tests. The first run before plan/change metadata updates had no changed `docs/changes/` roots, so it correctly printed `No changed review artifact roots to validate`; the final M2 run after metadata updates validates the active change root.
- 2026-04-25: `code-review-r1` found that closeout mode accepted a same-stage approved entry with the same `Round: 1`; the regression test reproduced the false closeout before the production fix.
- 2026-04-25: Public adapter tests failed before adapter regeneration with stale generated adapter files for the review, verify, explain-change, PR, and workflow skills. Regenerating `dist/adapters/` resolved the drift without changing `dist/adapters/manifest.yaml`.

## Validation notes

- 2026-04-25: Plan creation validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml --path docs/plan.md --path docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - `git diff --check -- docs/proposals/2026-04-24-review-finding-resolution-contract.md specs/review-finding-resolution-contract.md docs/architecture/2026-04-24-review-finding-resolution-contract.md docs/changes/2026-04-24-review-finding-resolution-contract docs/plan.md docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - ASCII/trailing-whitespace scan over touched planning artifacts.
- 2026-04-25: Plan-review approved with no material findings. The review specifically called out duplicate Review IDs inside canonical `review-log.md` blocks as important test coverage; `T3` and `T13` in `specs/review-finding-resolution-contract.test.md` cover it.
- 2026-04-25: Test spec creation validation passed:
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml --path docs/plan.md --path docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - `git diff --check -- docs/proposals/2026-04-24-review-finding-resolution-contract.md specs/review-finding-resolution-contract.md specs/review-finding-resolution-contract.test.md docs/architecture/2026-04-24-review-finding-resolution-contract.md docs/changes/2026-04-24-review-finding-resolution-contract docs/plan.md docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - ASCII/trailing-whitespace scan over touched test-spec artifacts.
- 2026-04-25: M1 TDD red check passed as expected:
  - `python scripts/test-review-artifact-validator.py`
  - Result: failed with `ModuleNotFoundError: No module named 'review_artifact_validation'` before production validator code existed.
- 2026-04-25: M1 implementation validation passed:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml --path docs/plan.md --path docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - `git diff --check -- scripts tests docs/changes/2026-04-24-review-finding-resolution-contract docs/plans/2026-04-25-review-finding-resolution-contract.md`
- 2026-04-25: M1 code-review returned `clean-with-notes` after the implementation and governing artifacts were staged.
- 2026-04-25: M1 milestone closeout commit created with subject `M1: add review artifact structure validation`.
- 2026-04-25: M2 TDD red check passed as expected:
  - `python scripts/test-review-artifact-validator.py`
  - Result: failed because `closeout` mode was unsupported and `scripts/ci.sh` did not invoke review-artifact validation.
- 2026-04-25: M2 implementation validation passed:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract`
  - `bash scripts/ci.sh`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml --path docs/plan.md --path docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - `git diff --check -- scripts tests docs/changes/2026-04-24-review-finding-resolution-contract docs/plans/2026-04-25-review-finding-resolution-contract.md`
- 2026-04-25: M2 milestone closeout commit created with subject `M2: add review artifact closeout validation`.
- 2026-04-25: `CR1-F1` red regression check passed as expected:
  - `python scripts/test-review-artifact-validator.py`
  - Result: failed because a same-stage `Round: 1` approved entry was accepted as closeout for a blocking `Round: 1` review.
- 2026-04-25: `CR1-F1` implementation validation passed:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml --path docs/plan.md --path docs/plans/2026-04-25-review-finding-resolution-contract.md`
  - `git diff --check -- .`
  - `bash scripts/ci.sh`
- 2026-04-25: M3 TDD red checks passed as expected:
  - `python scripts/test-review-artifact-validator.py`
  - Result: failed because `specs/rigorloop-workflow.md`, `docs/workflows.md`, `CONSTITUTION.md`, `AGENTS.md`, and canonical review/closeout skills did not yet expose the expanded review-resolution contract.
  - `python scripts/test-adapter-distribution.py`
  - Result: failed after canonical skill edits because public adapter outputs were stale.
- 2026-04-25: M3 source and generated-output validation passed so far:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`
  - `python scripts/test-adapter-distribution.py`
- 2026-04-25: M3 final validation passed:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.test.md --path specs/rigorloop-workflow.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml --path docs/plan.md --path docs/plans/2026-04-25-review-finding-resolution-contract.md --path docs/workflows.md --path AGENTS.md --path CONSTITUTION.md --path scripts/test-review-artifact-validator.py --path skills/code-review/SKILL.md --path skills/workflow/SKILL.md --path skills/verify/SKILL.md --path skills/explain-change/SKILL.md --path skills/pr/SKILL.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/architecture-review/SKILL.md --path skills/plan-review/SKILL.md`
  - `rg -n "partially-accepted|needs-decision|Closeout status|review-resolution.md" specs/rigorloop-workflow.md docs/workflows.md CONSTITUTION.md AGENTS.md skills .codex/skills dist/adapters`
  - `git diff --check -- specs docs skills .codex/skills dist AGENTS.md CONSTITUTION.md scripts`
  - `python scripts/validate-release.py --version v0.1.1`
  - `bash scripts/ci.sh`

## Outcome and retrospective

- Active plan. M1 and M2 validator behavior are implemented, validated, and committed. M3 source and generated-output alignment is implemented and validated, with only the milestone commit remaining.

## Readiness

- M1 and M2 are complete.
- M3 implementation is ready for its milestone commit.

## Risks and follow-ups

- Re-run review-artifact closeout validation on this change once M1 and M2 provide the validator.
