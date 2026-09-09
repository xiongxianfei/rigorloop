# M2 source transfer and consumer evidence

Owning change: [change.json](change.json). Implements M2/TG-04–05 after clean independent M1 review. Source adoption remains subject to complete independent review and successful Verify; this evidence is not that approval.

## Exact source dispositions

The four reviewed originals are byte-identical at their source-relative paths under [archive navigation](../../archive/skill-model/2026-09-08/README.md). The three fully superseded originals also retain their original-path bytes for historical links. The mixed Skill Contract now forwards common ownership to Skill and retains R37–R45 and R56–R63, their contract-era examples, current specialist owners and explicit proof supersessions. Current retained prose was joined into normal paragraphs without changing clauses; archived bytes were not reformatted. Every source hash is asserted against the pre-displacement inspected identity, not computed from another mutable copy.

Only the approved common portions of mixed architecture were replaced: resource flow items 1–7, the crosscutting common resource section, common content in its building-block bullet and current ADR decision navigation. Flow items 8–10 and the remaining architecture retain validation, installation and other owners. Historical source lists and judgments were not rewritten. The archive index exposes 73 resolving links, including source-resolved related navigation. One pre-existing unresolved reference is an illustrative `plans/YYYY-MM-DD-slug.md` target in the original source, explicitly documented rather than invented or silently repaired.

## Consumer disposition

| Consumer set | Inspected disposition |
| --- | --- |
| AGENTS.md, CONSTITUTION.md | Added scoped Skill ownership/adoption boundary and historical-original navigation. AGENTS' former common Skill Contract directive now distinguishes Skill from the retained specialist source. |
| specs/rigorloop-workflow.md | Replaced its active paragraph claiming common Skill Contract ownership with Skill and the retained remainder. Workflow policy is unchanged. |
| docs/project-map.md, specs/guide-system-source-of-truth-alignment.md, docs/learn/topics/skill-asset-design.md | Corrected current common-owner navigation only; no full map rewrite or specialist policy transfer. |
| scripts/test-skill-validator.py | Three original-contract text tests now explicitly test the archived historical source. New current-owner checks cover metadata, role summary, vocabulary, evidence reads, output shape, source/generation ownership and precise resource/lint/enforcement definitions. Archive tests verify original hashes, current retained clauses, removed common definitions and navigation. Existing behavior tests remain. Discovery-support's owner assertion now reads Skill. No test was deleted. |
| scripts/validate-guide-system.py and scripts/test-guide-system-validator.py | Added Skill to the existing current-authority check alongside the mixed source. A regression proves the new owner cannot reintroduce the retired workflow-guide authority. |
| scripts/validation_selection.py and scripts/test-select-validation.py | CI exposed five unclassified new archive paths. Added exactly those reviewed paths to existing selection, requiring skills.regression's archive byte/owner/link proof without treating historical prose as new lifecycle policy. Focused regression proves all five select the check and unknown archive paths still block. No broad archive bypass or new gate was introduced. |
| Operational boundary-first activation/manifests, templates/shared, schemas and package projections | Unchanged paths, bytes and consumers. They remain operational sources, not prose archives. Candidate and canonical skill content are unchanged from M1. |
| Other owning Designs and specialist spec/amendment/test references to Skill Contract | Retain their exact source-qualified mappings, amendments and historical meaning. The mixed source remains accessible and forwards common clauses to Skill while retaining specialist clauses. These links do not create an independently maintained common definition. |
| Historical proposals, plans, change records, reports, original ADR listings and learn-session evidence | Preserved. Original subjects/approvals are not retargeted to changed sources; the archive index supplies replacement and related navigation. |
| FU-015–018 and FU-012 | Existing follow-ups already name the 17 remaining skills in four families, maintainer/receiving capability owners, differences and next adoption decisions; verified unchanged. FU-012 retains separate Validation Execution work. No progress was copied into Skill. |

The common transfer is assessed against Skill's complete source-qualified maps and retained-contract table. Metadata/role/vocabulary and lint/enforcement populations are defined there, not replaced by a generic preserve-behavior sentence. Existing specialist output/method definitions and proof-policy supersessions remain explicit. Independent semantic review, rather than the textual checks above, judges preservation and one-owner adequacy.

## Proof actually run

- New `SkillOwnerTransferTests` failed before archive/ownership implementation (expected missing originals/current transfer), then passed. Original-byte, retained-owner and navigation checks are included in the full skill suite.
- `python scripts/test-skill-validator.py`: 358 tests passed. A final focused `-k skill_owner` run passed after formatting the current retained source.
- `python scripts/validate-skills.py`: Gate A passed for all 19 canonical skills.
- `python scripts/validate-guide-system.py` and `python scripts/test-guide-system-validator.py`: passed; nine guide tests.
- `python scripts/validate-boundary-first.py --check --path docs/design/skill/skill.md --path docs/design/system/system.md`: passed, structure/references only.
- `python scripts/validate-documentation-prose.py --mode enforce --path specs/skill-contract.md --path docs/archive/skill-model/2026-09-08/README.md`: passed after normalizing current retained paragraphs. Original snapshots were preserved byte-for-byte.
- `python scripts/validate-markdown-readability.py specs/skill-contract.md docs/archive/skill-model/2026-09-08/README.md`: passed with 88 advisory warnings.
- `python scripts/test-select-validation.py ValidationSelectionTests.test_skill_source_archive_selects_integrity_without_current_lifecycle`: passed after a failing-before reproduction of the missing archive classification.
- `bash scripts/ci.sh --mode local --timeout 1200 --jobs 4`: passed after the bounded selector correction. Selected checks: boundary_first.validate, skills.regression, skills.generation_regression, artifact_lifecycle.validate, guide_system.regression, guide_system.validate and selector.regression. This run covers M2's changed/untracked surfaces; final whole-branch selection additionally covers committed M1 surfaces.
- Python archive-navigation existence check: 73 links passed. `git diff --check`: passed.

M1's canonical resources, production skill validator, adapter comparison and generated current metadata are unchanged by M2. Its full 158-case adapter proof remains attributable to those unchanged package surfaces; this does not substitute for the final branch-selected checks or independent integrated review. The remaining steps are independent M2 review, final whole-change Code Review and distinct Verify before PR submission.
