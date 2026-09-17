# Model-owned test design and concise tests

## Purpose / big picture

Deliver the focused testing scope: System-owned shared rules, Release/Skill/Authoring coverage packages, concise executable tests and admission through existing validation. Reconcile the extracted draft against the focused approved Designs, then establish fresh whole-change review and verification. Earlier draft implementation and broader-branch assessments do not supply approval of this package.

## Current Handoff Summary

- Owning change record: [focused testing](../changes/2026-09-17-model-test-design/change.json).

Mutable lifecycle state, milestone state, review status, blockers, routing and closeout readiness live only in that record.

## Source artifacts

- [Focused proposal](../proposals/2026-09-17-model-test-design.md).
- [System](../design/system.md#living-test-design-composition) and [shared rules](../design/test-design/rules.md).
- [Design authorship](../design/skill/authoring/design.md#living-test-design), its Authoring, Plan, Assessment and Workflow consumers, and Engineering/Skill composition.
- [Release](../design/engineering/release/test-design/test-design.md), [Skill](../design/skill/test-design/test-design.md) and [Authoring](../design/skill/authoring/test-design/test-design.md) strategies and their explicitly indexed case groups.
- [Validation](../design/engineering/validation.md#shared-test-design-guidance-admission): exact document admission and existing execution.
- No separate feature spec, test spec or ADR is required; decisions remain with these living owners.

## Context and orientation

The existing native entrypoints are `tests/engineering/release/test-release-transaction.py`, `tests/skill/test-skill-validator.py`, `tests/engineering/validation/test-boundary-first-validation.py` and `tests/engineering/validation/test-select-validation.py`. Tests remain in those owners. Small context managers acquire fresh temporary resources; the cases keep defining faults, operations and independently expected outcomes visible.

`model_layout.py` declares exact owners and catalog packages. `test_design_validation.py` implements package validation behind `validate-boundary-first.py`, reusing current model grammar and trusted native discovery. `validation_selection.py`, `validation_execution.py` and `ci.sh` preserve selected-command agreement and derive actual path provenance from caller input. Catalog metadata cannot select imports or execute tests.

## Non-goals

No withdrawal of feature/proof authoring, validation, location defaults or historical routing. Preserve supported generic flat-model grammar and existing alias handling; distinguish them from the actual moved Release owner. No new test runner, case-management CLI, shared public schema, required object hierarchy, per-method case quota or full hierarchy adoption. Proposed semantic review procedures and unrelated catalog gaps remain explicit design intent, not completion promises for this change.

## Requirements covered

| Basis | Allocation |
| --- | --- |
| System TEST-SR-01–22, SYS-DEC-05 | M1, TG-POLICY and TG-REFINEMENT: one shared policy owner, proportional model intent, meaningful observations, safe consolidation and source/fixture organization. |
| Design DES-SR-25/26; Authoring AUTH-SR-01–05; Skill parent coverage | M1, TG-POLICY: published authoring guidance, exact catalog representations and honest existing/partial/proposed claims. |
| Release REL-IN-001; Skill SKL-RC-001/002/003/004/007 | M1, TG-REFINEMENT: unknown vocabularies, resource semantics, inventory, containment and unknown-consumer precedence. Case IDs refer to model-owned designs, not new requirements. |
| Validation VAL-SR-35 and four admission contracts | M1, TG-ADMISSION and TG-INTEGRATION: exact package admission, safe read/shape/reference/native discovery, shared guidance and real selector/executor composition. |
| Existing supported compatibility and review/record contracts | M1, TG-INTEGRATION and final review: preserve baseline behavior outside the selected packages; new records do not retarget previous judgments. |

## Milestones

### M1. Reconcile and deliver the focused testing package

- Milestone kind: implementation.
- Engineering purpose: shared policy, catalog references, native tests and document admission must compose in one coherent change.
- Requirements: the complete allocation table above.
- Architecture responsibility: System policy, model-owned coverage, Design authorship and Validation execution remain separate owners.
- Dependencies: independent approval of the exact focused proposal, Design package and this delivery plan before relying on the extracted implementation as accepted work.
- Implementation scope: retain and reconcile the selected draft; resolve review corrections; leave compatibility retirement on its original branch.
- Files/components likely touched: declared `docs/design/` owners and test-design packages; shared policy templates and skill copies; `skills/design/` guidance; Release/Skill tests and helpers; Validation support modules, native tests and CI wrapper; live Release-path consumers.
- Required verification: TG-POLICY, TG-REFINEMENT, TG-ADMISSION and TG-INTEGRATION below.
- Evidence expectations: exact subjects, concrete removal/retained-protection rationale, failing-before/passing-after correction proof where feasible, native selected results and reviewed scope limitations.
- Implementation steps: reconcile scope and current links; preserve the independent fixture baselines and discovery identities; correct recorded defects with narrow proof first; run the complete selected validation; hand the whole slice to independent review.
- Validation commands: the native entrypoints and selected CI under Validation plan below.
- Expected observable result: ordinary validation accepts valid declared test-design packages and rejects malformed ones; linked tests remain discoverable; reduced suites preserve distinct observations and original supported compatibility.
- Completion criteria: all required checks pass, in-scope findings are resolved by their reporters, exact approved Design and Delivery subjects agree with the result, and independent milestone review approves the complete slice.
- Required evidence: implementation decisions and executions in the owning record, followed by exact independent review.
- Review handoff: complete diff against the PR base, including catalogs, public skill guidance, deleted fixtures, native discovery and selector/executor interactions.
- Optional commit boundary: `Add model-owned test designs and refine executable tests`.
- Risks: omitted test protection, misleading realization claims, catalog-selected code, symlink traversal, incomplete renamed-path routing or accidental retirement scope.
- Rollback/recovery: restore only focused owned edits from the current base or private extraction snapshot; preserve the original retirement worktree and records. Correct lost protection before relying on a reduced suite.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1 and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered change and its interactions; a milestone review is not a substitute.
- Evidence: exact final subjects, independent reviewer basis, judgment and reporter-owned concern dispositions.
- Successor: distinct final Verify; corrections return to their owner and require affected reassessment.

## Change-level verification

### TG-POLICY. Durable intent and honest coverage

Inspect shared owner transfer, portable published guidance, the three strategies and every indexed group. Check concrete conditions/actions/oracles, fixture roles, maintained stable IDs and references, and honest realization gaps. Native method inventory is not a design-case quota. Authoring's twelve review procedures remain proposed; structural phrase/resource checks do not claim semantic execution. Public skill parity and resource checks cover maintained shared copies and generated packages.

### TG-REFINEMENT. Retained fault detection with concise setup

Assess the exact removal mapping in the owning `test-refinement-protection-disposition` decision. Release's three unknown-value methods become one named table retaining all vocabularies and competing consistency faults; the real tag loader retains expected-path proof. Skill's resource scenarios retain accepted baselines, both directions of inventory disagreement, each distinct directory class, RUN failure instructions and path containment. Preserve generic unknown Design-resource rejection, current required-resource omissions and exact no-read unknown-consumer diagnostics. Each variation starts with fresh mutable resources. Remove exclusive static fixtures only after checking consumers; do not use method count as evidence of equivalent protection.

### TG-ADMISSION. Exact document validation

Exercise valid shared and all three model packages; owner/detail/no-path selection; review-only zero-link cases; no linked test-body execution; missing, escaped, symlinked, unindexed and mixed requests; malformed/duplicate/nonfinite JSON; complete field/type/closed-value validation before reference checks; duplicate identities; missing or cyclic fixtures; missing requirements, callables, review sections and undiscoverable methods; realization consistency; inline/reference Markdown links and lexical symlink traversal. Use independently declared private valid packages before each fault and assert the intended diagnostic. Verify actual repository packages through the public entrypoint, without claiming semantic adequacy from that pass.

### TG-INTEGRATION. Native execution, selection and compatibility

Run the existing native suites and full local selected CI. Demonstrate the actual `docs/design/engineering/release.md` move in unstaged, staged and Git-range selection, then the selector-to-CI-to-validator command path. Explicit missing or recreated input at that actual former location fails; existing unrelated flat aliases and generic flat model grammar remain supported. Keep current feature/proof and historical-path tests in the selected suites. Selected output must include real observations, not invented successful aliases. Record-only follow-up checks may run after evidence writes; unchanged engineering proof may be reused only with exact unaffected-basis reasoning.

## Validation plan

```bash
python tests/engineering/release/test-release-transaction.py
python tests/skill/test-skill-validator.py
python tests/engineering/validation/test-boundary-first-validation.py
python tests/engineering/validation/test-select-validation.py
python scripts/validate-boundary-first.py --check
bash scripts/ci.sh --mode local
git diff --check
git diff --cached --check
```

The full local selector exercises the native suites with attributable method rows, so it may supply those suite executions without redundant separate reruns. Begin corrections with exact native method selection. Use `bash scripts/ci.sh --mode explicit --path PATH` for changed records after recording. Before PR handoff, establish exact-revision PR selection/preflight and current record validity. Preserve failed evidence and rerun any invalidated proof after corrections. Hosted CI must be reported separately from local validation.

## Risks and recovery

JSON supplies data only; trusted repository entrypoints own discovery. Check lexical containment before resolution and complete shapes before references. Fresh private fixtures prevent cross-case mutation. Review the supported outcome before deleting a test. Separate original retirement artifacts from this focused change, preserve existing compatibility, and avoid claiming future review procedures as executed. Recover only affected focused files; never reset the original working tree.

## Dependencies

Design Review precedes reliance on this allocation; Delivery Review precedes acceptance of the extracted implementation and remaining corrections. Final independent whole-change review and successful Verify precede PR submission. The user already authorized that submission; no release, merge or publication is included.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-17 | One focused implementation milestone followed by a distinct final review checkpoint. | Policy, catalog references, source layout and admission are coupled; one slice avoids an intermediate tree whose own catalogs fail validation. | Treating earlier scoped reviews as full approval, bundling unfinished compatibility retirement, or splitting into independently invalid packages. |
| 2026-09-17 | Preserve native tests and use catalogs as design data. | Existing discovery provides reliable execution identity; metadata alone cannot establish semantic coverage. | A second runner, automatic case generation, mandatory inheritance or one case per method. |

## Readiness

See the owning change record for current workflow state. This stable plan records intent, not execution results or approval.
