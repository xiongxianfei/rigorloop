# Legacy Architecture Lifecycle Normalization Test Spec

## Status

- active

## Related spec and plan

- Governing spec: `specs/architecture-package-method.md`
- Existing broad method test spec: `specs/architecture-package-method.test.md`
- Plan: `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
- Canonical architecture package: `docs/architecture/system/architecture.md`
- Architecture method ADR: `docs/adr/ADR-20260428-architecture-package-method.md`
- Planned change-local pack:
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md`
- Plan-review findings: approved on 2026-04-29 after adding M0 routing, domain-split comparison, M3 canonical current-state sweep, and M5 validation for every legacy architecture document changed in M4.

## Testing strategy

- Use this focused test spec for the legacy architecture lifecycle normalization follow-on only.
- Reuse `specs/architecture-package-method.test.md` as the broad proof surface for the original C4, arc42, ADR, template, skill, generated-output, and first-package rollout.
- Use contract and manual review for domain comparison, merge-back judgment, ADR-need judgment, historical-content preservation, and canonical freshness.
- Use existing repository commands for selector routing, change metadata validation, artifact lifecycle validation, CI wrapper execution, and whitespace checks.
- Keep the first normalization implementation review-based. This test spec must not introduce required arc42 section validation, required C4-file validation, ADR-presence enforcement, or package-shape enforcement.
- Run the exact pass-gate commands named by the approved plan for the relevant milestone, then record validation evidence in the plan and change-local metadata.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R36`, `R40`-`R43`, `R49`-`R62` | `T12` | Broad method behavior remains covered by `specs/architecture-package-method.test.md`; this follow-on asserts it does not reopen or weaken that rollout. |
| `R37`-`R39` | `T3`, `T5`, `T6`, `T10`, `T11` | Durable current content from legacy records is compared, merged into the canonical package when accepted, and not left in change-local or legacy-only sources. |
| `R44`-`R48` | `T3`, `T5`, `T11`, `T12` | Durable decisions found during comparison are linked to existing ADRs or captured in new ADRs when required. |
| `R63`-`R66` | `T1`, `T2`, `T3`, `T7`, `T8`, `T10`, `T11` | Legacy artifacts are inventoried, classified, compared, normalized, and not claimed fully normalized before closeout proof passes. |
| `R67`-`R72` | `T4`, `T6`, `T10`, `T12` | Selector routing stays non-enforcement and no package-shape automation is added in this follow-on. |
| `R73`-`R75` | `T1`, `T7`, `T8`, `T9`, `T10`, `T11` | Touched artifacts remain publishable, readable, and free of secrets or machine-local debug data. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T3`, `T5`, `T12` | Adapter and generated-output legacy records are compared and merged only when they still describe current architecture. |
| `E2` | `T12` | Leaf-change exclusion remains owned by the broad method proof and is not widened by this normalization work. |
| `E3` | `T1`, `T5`, `T10`, `T11` | The change-local architecture delta is working evidence and durable content is merged back before closeout. |
| `E4` | `T3`, `T5`, `T11` | ADR links or new ADRs are required when comparison finds durable architecture decisions. |
| `E5` | `T5`, `T6`, `T12` | Canonical package updates preserve the approved method; no new package-shape enforcement is introduced here. |
| `E6` | `T1`, `T2`, `T7`, `T10`, `T11` | Legacy architecture documents are inventoried, classified, and normalized through an explicit follow-on. |

## Edge case coverage

- EC1, architecture inventory changes after planning: `T2`, `T10`
- EC2, a legacy document contains current architecture truth missing from the canonical package: `T3`, `T5`
- EC3, a legacy document conflicts with the canonical package: `T3`, `T5`, `T11`
- EC4, a legacy document contains a durable decision that is not represented by an ADR: `T3`, `T5`, `T11`
- EC5, a legacy document should be archived rather than superseded: `T7`, `T8`
- EC6, a legacy document should be superseded and needs a replacement pointer: `T7`, `T8`
- EC7, final closeout omits a legacy architecture document changed in M4: `T10`
- EC8, the canonical architecture still references the completed architecture-method rollout as active: `T6`, `T10`
- EC9, selector routing is mistaken for architecture-package enforcement: `T4`, `T12`
- EC10, touched artifacts include secrets, tokens, or machine-local debug data: `T9`

## Milestone coverage map

| Milestone | Test IDs | Notes |
| --- | --- | --- |
| M0 | `T1` | Change-local pack and test-spec routing before legacy content changes. |
| M1 | `T2` | Inventory refresh and comparison basis. |
| M2 | `T3`, `T4`, `T9` | Domain comparison, ADR review, and non-enforcement selector routing. |
| M3 | `T5`, `T6`, `T9`, `T12` | Canonical merge-back and current-state sweep. |
| M4 | `T7`, `T8`, `T9` | Legacy lifecycle dispositions and historical content preservation. |
| M5 | `T10`, `T11`, `T12` | Final closeout, full legacy-doc validation, metadata, and no forbidden automation. |

## Test cases

### T1. M0 creates routed change-local proof surfaces before legacy edits

- Covers: `R63`-`R66`, `R73`-`R75`, `E3`, `E6`
- Level: selector, lifecycle, contract
- Fixture/setup:
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
  - `specs/legacy-architecture-lifecycle-normalization.test.md`
  - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
- Steps:
  - Confirm `change.yaml` cites the governing spec, plan, canonical architecture, this test spec, and planned changed-file set.
  - Confirm the change-local architecture delta identifies itself as working evidence, not canonical architecture.
  - Confirm M0 does not change legacy architecture statuses.
  - Run the M0 selector, change metadata, change metadata regression, lifecycle, and `git diff --check` commands from the plan.
- Expected result:
  - The implementation has a routed change-local pack and active proof map before legacy architecture content or status changes begin.
- Failure proves:
  - Later merge-back and disposition work would rely on chat-only or unrouted evidence.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md --path specs/legacy-architecture-lifecycle-normalization.test.md --path docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md --path docs/plan.md`
  - `git diff --check -- docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization specs/legacy-architecture-lifecycle-normalization.test.md docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`

### T2. M1 inventory proof covers every current architecture path

- Covers: `R63`-`R66`, `E6`, EC1
- Level: contract, manual
- Fixture/setup:
  - current `docs/architecture/` tree
  - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
- Steps:
  - Run `find docs/architecture -type f | sort`.
  - Confirm every path from that output appears in the plan inventory.
  - Confirm every top-level legacy Markdown architecture file appears in the change-local architecture comparison surface.
  - Confirm M1 records comparison categories without changing canonical architecture content or legacy lifecycle status.
  - Run the M1 selector, change metadata, lifecycle, and `git diff --check` commands from the plan.
- Expected result:
  - Inventory and comparison inputs are complete before domain-level review starts.
- Failure proves:
  - A legacy architecture artifact could be silently skipped.
- Automation location:
  - `find docs/architecture -type f | sort`
  - `while IFS= read -r path; do rg -F -q "$path" docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md || printf 'missing-from-plan %s\n' "$path"; done < <(find docs/architecture -type f | sort)`
  - `while IFS= read -r path; do rg -F -q "$path" docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md || printf 'missing-from-delta %s\n' "$path"; done < <(find docs/architecture -maxdepth 1 -type f -name '*.md' | sort)`

### T3. M2 domain comparison records merge-back and ADR decisions

- Covers: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `E1`, `E4`, EC2, EC3, EC4
- Level: manual, contract
- Fixture/setup:
  - all eight legacy Markdown records under `docs/architecture/*.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
  - `scripts/validation_selection.py`
- Steps:
  - Confirm the change-local comparison groups source layout/generated output, workflow/lifecycle/review, and validation/CI records.
  - Confirm each legacy record has merge-back candidates, historical-only content, ADR links needed, and final disposition recommendation.
  - Confirm any discovered durable decision is linked to an existing ADR or marked as requiring a new ADR in M3.
  - Confirm conflicts between legacy records and the canonical package are recorded for M3 rather than resolved silently.
  - Run the M2 `rg`, selector, change metadata, lifecycle, and `git diff --check` commands from the plan.
- Expected result:
  - The branch has reviewable evidence for what will merge into the canonical package and what will remain historical.
- Failure proves:
  - Canonical merge-back or legacy disposition could become arbitrary or lossy.
- Automation location:
  - `rg -n "source layout|generated|adapter|workflow|lifecycle|review|validation|selector|CI|ADR|merge-back|historical-only" docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
  - manual comparison review during code-review

### T4. Selector routing remains non-enforcement for architecture support paths

- Covers: `R67`-`R72`, EC9
- Level: selector, contract
- Fixture/setup:
  - `scripts/validation_selection.py`
  - `docs/architecture/system/architecture.md`
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
- Steps:
  - Run selector inspection for changed canonical architecture, diagram source, and change-local architecture paths when those paths exist in the milestone.
  - Confirm selected checks are existing lifecycle or regression checks only.
  - Confirm no selected check claims to validate C4 content, arc42 section completeness, ADR presence, or architecture package shape.
  - Confirm selector output does not become a substitute for architecture-review or manual code-review evidence.
- Expected result:
  - Selector routing is deterministic for CI but remains non-enforcement for architecture sufficiency.
- Failure proves:
  - The follow-on introduced package-shape enforcement that the governing spec defers.
- Automation location:
  - milestone selector commands from M2, M3, M4, and M5
  - code-review inspection when selector code is touched

### T5. M3 canonical merge-back represents accepted durable content

- Covers: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `E1`, `E3`, `E4`, EC2, EC3, EC4
- Level: manual, lifecycle, contract
- Fixture/setup:
  - `docs/architecture/system/architecture.md`
  - `docs/architecture/system/diagrams/context.mmd`
  - `docs/architecture/system/diagrams/container.mmd`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
  - `docs/adr/` if M2 identifies a new durable decision
- Steps:
  - Confirm every accepted merge-back candidate from M2 is represented in the affected canonical arc42 section.
  - Confirm unchanged or rejected legacy content is recorded as intentionally historical in the change-local delta.
  - Confirm C4 diagrams are updated only when context or container boundaries changed.
  - Confirm section 9 links existing or new ADRs for durable decisions, or records why no ADR is required.
  - Run the M3 selector, CI wrapper, change metadata, lifecycle, and `git diff --check` commands from the plan.
- Expected result:
  - Durable current architecture truth is no longer stranded in legacy records or the change-local delta.
- Failure proves:
  - Downstream work could still rely on legacy architecture snapshots as current truth.
- Automation location:
  - M3 validation commands from the plan
  - manual architecture/code-review inspection

### T6. M3 canonical current-state sweep removes stale baseline wording

- Covers: `R37`-`R39`, `R66`, `R72`, `E5`, EC8, EC9
- Level: contract, manual
- Fixture/setup:
  - `docs/architecture/system/architecture.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
- Steps:
  - Inspect Related artifacts, Next artifacts, Readiness, Runtime View validation flow, and any completed-plan or old-milestone references in the canonical architecture.
  - Confirm the architecture no longer says the completed architecture-method rollout plan is active.
  - Confirm old M3/M4/M5 handoff text from the completed rollout is gone or replaced with current baseline wording.
  - Confirm selector-routing wording says architecture diagram source files and change-local architecture deltas route to existing non-enforcement lifecycle or regression checks, while diagram sufficiency and package completeness remain manual review evidence.
  - Run the stale-string assertion command from M3.
- Expected result:
  - The canonical architecture package is current after merge-back and does not preserve obsolete rollout-state guidance.
- Failure proves:
  - The canonical package remains stale even if legacy content was compared.
- Automation location:
  - `rg -n "manual-routed|selector routing|non-enforcement|change-local architecture|\\.mmd" docs/architecture/system/architecture.md docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/architecture.md`
  - `python -c 'from pathlib import Path; bt=chr(96); text=Path("docs/architecture/system/architecture.md").read_text(); stale=[p for p in ("docs/plans/2026-04-28-architecture-skills-c4-arc42-adr.md", "M3 "+bt+"code-review"+bt, "M3 "+bt+"verify"+bt, "M4 skill and generated-output update", "M5 legacy architecture normalization follow-on artifact before final completion claims", "diagrams and change-local architecture deltas remain manual-routed review evidence in the first adoption slice") if p in text]; assert not stale, stale'`

### T7. M4 assigns final lifecycle disposition to every legacy architecture record

- Covers: `R63`-`R66`, `R73`-`R75`, `E6`, EC5, EC6
- Level: lifecycle, manual
- Fixture/setup:
  - all eight legacy Markdown files under `docs/architecture/*.md`
  - `docs/architecture/system/architecture.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
- Steps:
  - Confirm each legacy Markdown record has a final accepted historical disposition: `superseded`, `archived`, or another approved historical state.
  - Confirm superseded records identify a replacement or merge-back target.
  - Confirm archived records explain archive rationale or point to the canonical package where appropriate.
  - Confirm no legacy document still implies it is the current architecture source of truth.
  - Run M4 selector, lifecycle, change metadata, `rg`, and `git diff --check` commands from the plan.
- Expected result:
  - Every legacy record has an explicit lifecycle disposition after merge-back decisions complete.
- Failure proves:
  - The repository could keep competing architecture sources or ambiguous historical records.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md --path docs/architecture/2026-04-20-artifact-status-lifecycle-ownership.md --path docs/architecture/2026-04-21-docs-changes-usage-policy.md --path docs/architecture/2026-04-21-workflow-stage-autoprogression.md --path docs/architecture/2026-04-24-multi-agent-adapter-distribution.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/architecture/2026-04-24-skill-invocation-commands-for-adapters.md --path docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md --path docs/architecture/system/architecture.md --path docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`

### T8. M4 preserves historical body content except lifecycle notes

- Covers: `R63`-`R66`, `R73`-`R75`, EC5, EC6
- Level: manual, diff review
- Fixture/setup:
  - M4 diff for all eight legacy Markdown files
- Steps:
  - Review each legacy file diff.
  - Confirm edits are limited to lifecycle metadata, replacement pointers, archive rationale, canonical references, or concise disposition and closeout notes.
  - Confirm historical architecture reasoning is not rewritten to match the current canonical package.
  - Confirm any intentionally unusual historical status is documented in the plan and change-local evidence.
- Expected result:
  - The normalization pass preserves historical evidence while clarifying lifecycle state.
- Failure proves:
  - The implementation may erase or rewrite historical architecture records beyond the approved scope.
- Automation location:
  - manual code-review diff inspection
  - `git diff --check -- docs/architecture docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`

### T9. Touched architecture and change-local artifacts are publishable and readable

- Covers: `R73`-`R75`, EC10
- Level: manual, security/privacy
- Fixture/setup:
  - touched Markdown files under `docs/architecture/`, `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/`, `docs/plans/`, and `specs/`
  - touched `.mmd` diagrams if any
  - touched ADRs if any
- Steps:
  - Inspect touched artifacts for secrets, credentials, private keys, tokens, and debug-only machine-local data.
  - Confirm command examples and paths are repository-relative unless a reviewed example explicitly justifies otherwise.
  - Confirm headings, classification text, lifecycle notes, and validation evidence are concise enough for ordinary review.
  - Confirm security/privacy concerns are described if a legacy comparison or merge-back changes trust boundaries, data exposure, or secret handling.
- Expected result:
  - The normalization work is safe to publish and efficient to review.
- Failure proves:
  - Architecture lifecycle cleanup leaked sensitive data or produced hard-to-review artifacts.
- Automation location:
  - manual code-review and verify inspection

### T10. M5 final closeout validates canonical freshness and every changed legacy document

- Covers: `R63`-`R66`, `R67`-`R72`, `R73`-`R75`, `E3`, `E6`, EC1, EC7, EC8, EC9
- Level: lifecycle, selector, smoke, contract
- Fixture/setup:
  - completed M1 through M4 changes
  - all eight legacy Markdown files changed in M4
  - `docs/architecture/system/architecture.md`
  - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
  - `docs/plan.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md`
- Steps:
  - Re-run inventory proof and confirm every current architecture path appears in the plan.
  - Run M5 selector validation for plan/index/change surfaces.
  - Run M5 selector validation for all eight changed legacy Markdown files and the canonical architecture package.
  - Run M5 lifecycle validation for plan/index/change surfaces, this test spec, and the canonical architecture package.
  - Run M5 lifecycle validation for all eight changed legacy Markdown files and the canonical architecture package.
  - Run M5 CI wrapper commands for both the plan/index/change surfaces and all changed legacy architecture files.
  - Run the stale canonical baseline assertion and legacy disposition `rg` command from the plan.
  - Run broad smoke only if selector output includes selected check `broad_smoke.repo`.
  - Run `git diff --check -- .`.
- Expected result:
  - Final closeout proves the canonical baseline is fresh and every changed legacy artifact reached its intended lifecycle state.
- Failure proves:
  - The closeout could claim normalization while omitting changed legacy architecture artifacts or stale canonical state.
- Automation location:
  - M5 validation commands from the approved plan

### T11. Final plan, plan index, change metadata, and explain-change evidence agree

- Covers: `R37`-`R39`, `R44`-`R48`, `R63`-`R66`, `R73`-`R75`
- Level: lifecycle, contract, manual
- Fixture/setup:
  - `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`
  - `docs/plan.md`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/explain-change.md`
- Steps:
  - Confirm the plan body and `docs/plan.md` agree on final lifecycle state after M5.
  - Confirm change metadata records actual changed files and validation commands run.
  - Confirm `explain-change.md` links the problem, spec requirements, plan milestones, canonical architecture updates, legacy lifecycle dispositions, tests, and validation evidence.
  - Confirm plan validation notes name commands actually run and do not claim hosted CI unless observed.
  - Confirm no downstream artifact treats the change-local architecture delta as canonical after merge-back.
- Expected result:
  - Reviewers can trace the implementation from requirement to diff to validation without relying on chat-only memory.
- Failure proves:
  - Final review or PR readiness would be based on stale or incomplete lifecycle evidence.
- Automation location:
  - `python scripts/validate-change-metadata.py docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/change.yaml`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - manual explain-change review

### T12. Normalization does not add forbidden enforcement or reopen completed rollout scope

- Covers: `R1`-`R36`, `R40`-`R43`, `R49`-`R62`, `R67`-`R72`, `E2`, `E5`, EC9
- Level: code review, manual
- Fixture/setup:
  - full implementation diff
  - `specs/architecture-package-method.test.md`
  - validation selector output
  - dependency metadata if changed
- Steps:
  - Confirm implementation does not add required arc42 section validation, required C4 diagram file validation, ADR-presence validation, package-shape validation, or new enforcement automation.
  - Confirm implementation does not change command output behavior or command exit behavior except where an approved plan and test explicitly allow it.
  - Confirm no new dependency is added for architecture lifecycle normalization.
  - Confirm broad architecture-method rollout surfaces remain governed by `specs/architecture-package-method.test.md` rather than being silently retested or rewritten here.
  - Confirm leaf-change and review-based rollout behavior from the approved method remain unchanged.
- Expected result:
  - This follow-on only normalizes legacy architecture lifecycle state and canonical merge-back evidence.
- Failure proves:
  - The branch exceeded the approved normalization scope.
- Automation location:
  - manual code-review and verify inspection
  - selector and CI wrapper outputs from milestone validation

## Fixtures and data

- Current inventory from `find docs/architecture -type f | sort`.
- The eight current legacy Markdown architecture records under `docs/architecture/*.md`.
- The canonical architecture package at `docs/architecture/system/architecture.md`.
- Canonical C4 diagram sources under `docs/architecture/system/diagrams/`.
- Existing ADRs under `docs/adr/`.
- Planned change-local pack under `docs/changes/2026-04-29-legacy-architecture-lifecycle-normalization/`.
- Existing repository scripts:
  - `scripts/select-validation.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/test-change-metadata-validator.py`
  - `scripts/ci.sh`
- Existing broad proof surface: `specs/architecture-package-method.test.md`.

## Mocking/stubbing policy

- Do not mock inventory commands, selector output, lifecycle validation, change metadata validation, CI wrapper execution, or final stale-string assertions.
- Use real repository files and real CLI commands for milestone proof.
- Manual review is acceptable for merge-back judgment, ADR-need judgment, historical-body preservation, security/readability inspection, and no-forbidden-automation inspection.

## Migration or compatibility tests

- This entire test spec is migration-focused: it proves legacy architecture artifacts move from ambiguous pre-canonical lifecycle state to explicit historical disposition after canonical merge-back.
- Compatibility proof is review-based and command-backed. It must show the canonical architecture package remains the current source of truth while legacy artifacts remain useful historical evidence.
- The implementation must not require immediate migration of unrelated future architecture artifacts or add new package-shape enforcement.

## Observability verification

- No runtime logs, metrics, traces, audit events, or service observability are required.
- Observable proof is repository artifact state, lifecycle validation, selector output, CI wrapper output, plan validation notes, change metadata, and explain-change evidence.

## Security/privacy verification

- `T9` is the security/privacy proof surface.
- No secrets, credentials, private keys, tokens, or machine-local debug-only data may be introduced in touched architecture, ADR, plan, test spec, change-local, or diagram files.

## Performance checks

- No runtime or performance behavior changes are in scope.
- Validation output should remain summary-first and failure-focused where repository scripts already support that behavior, but this follow-on must not change script output semantics.

## Manual QA checklist

- Every current `docs/architecture/` path appears in the inventory proof.
- Every top-level legacy architecture Markdown file appears in the change-local comparison matrix.
- Domain comparison records merge-back candidates, historical-only content, ADR links, and final disposition recommendation.
- Canonical architecture no longer contains stale active-plan, old milestone, readiness, or manual-routed selector wording.
- Every legacy architecture document changed in M4 has its final lifecycle disposition validated again in M5.
- Final change metadata and explain-change evidence agree with the actual diff and commands run.

## What not to test

- Do not retest the entire C4, arc42, ADR method rollout here; use `specs/architecture-package-method.test.md` for that broad proof.
- Do not add or require automated C4 diagram content validation.
- Do not add or require automated arc42 section presence validation beyond existing lifecycle compatibility.
- Do not add or require ADR-presence or architecture package-shape enforcement.
- Do not test generated `.codex/skills/` or `dist/adapters/` output unless implementation unexpectedly touches canonical skill guidance.
- Do not test runtime service behavior, public APIs, release packaging, or deployment infrastructure; this change is repository artifact lifecycle normalization.

## Uncovered gaps

- None known.
- If M2 comparison discovers a durable architecture decision with no suitable ADR and no clear no-ADR rationale, implementation must create the ADR or return to architecture review rather than hide the decision in prose.
- If implementation needs new enforcement automation, return to spec before coding it because `R67`-`R72` defer that automation.

## Next artifacts

- `implement` for M0 through M5 from `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`.

## Follow-on artifacts

- None yet.

## Readiness

This active test spec is the current proof-planning surface for `specs/architecture-package-method.md` legacy normalization requirements and `docs/plans/2026-04-28-legacy-architecture-lifecycle-normalization.md`.

After lifecycle validation passes for this test spec, implementation is ready to start at M0.
