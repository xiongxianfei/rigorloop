# REM architecture refinement: retained review and migration evidence

This supporting record preserves evidence still relied on during the user's manual REM refactor. It does not register an operational workflow, confer approval, or claim successful Verify or governed completion. Historical excerpts and the separately identified walkthrough-retirement result describe distinct subjects. Current architectural definitions, decisions, and cross-module explanations belong to the [Module and Interface records](../../../design/architecture/README.md) and their [derived views](../../../design/architecture/views/README.md).

## Source and historical scope

The sections below were retained from the uncommitted `design/architecture/cli.md` walkthrough before its removal. The source file's complete bytes have SHA-256 `1cb6ff27ad7df9fa7c27cb784831c87a17245d37b5a22c66976b5698a4c01c96`. This attribution identifies the original working-tree artifact; it does not claim that artifact was committed at the implementation revision `9055b3c0` cited within its evidence.

Only the historical review/validation sections and the completed directory-migration plan and result are retained here. The walkthrough's current architecture definitions, Scenario explanations, allocated-obligation index, and 44-row coverage argument belong to their current model or view owners and are not copied into this record.

The retained sections preserve their original wording and separate review subjects. Present-tense expressions such as “current model,” “current subjects,” “this pass,” and “record findings and results here” refer to the original walkthrough and the historical state described by that section. Findings, commands, results, digest populations, and limitations remain assertions of those earlier passes. They are not retargeted to this documentation cleanup or to later modifications. The inline-realization self-review and the independently reviewed directory migration remain distinct assessments.

## Walkthrough retirement scope

The user requested removal of the mixed-purpose architecture walkthrough after redistributing its useful content. The bounded sequence is to preserve the historical evidence below, retain all 44 acceptance-contribution arguments as attributed analysis on their eight owning SRs, derive current cooperation and coverage views from the existing records, reconcile current links and provenance locators, and remove the walkthrough after preservation and structural checks.
Requirements, acceptance criteria, allocations, Scenarios, Interface behavior, realization choices, and schema shapes are unchanged. This cleanup changes analysis placement and navigation. The existing production CLI contract under `docs/design/cli/cli.md` remains intact.

## Review and validation

### Historical logical-allocation review

The following retained result describes the pre-realization subject identified by its digest. It does not cover the later realization fields or schema extension.

The reviewed extension contains 18 draft ARs beneath SR-040 through SR-047, refinements to MOD-010/MOD-011 and IF-003/IF-004, and this nine-Scenario walkthrough with a contribution argument for all 44 parent acceptance criteria. Eight new ARs belong to MOD-010 and ten to MOD-011. The current model contains 265 entities, including 28 ARs overall.

Independent reviews assessed the two AR groups against their unchanged parent requirements and retained source contracts. A separate integrated review assessed all 18 ARs, their 5W2H analyses and sources, both Modules and Interfaces, all nine Scenario walkthroughs, and all 44 contribution rows. No material finding remains within that bounded subject.
Review and reconciliation made five boundaries explicit:

- A first read discovers the observed stored contract and revision from the same checked snapshot; caller knowledge of that contract is not a read prerequisite.
- Check/preview construction cannot write filesystem, lock, reservation, or transaction state. New targeted writes reconstruct against a fresh snapshot under writer exclusion; advanced publication validates the supplied bytes, and recovery uses verified retained bytes without reconstructing edits.
- MOD-010 owns bounded public receipt serialization; MOD-011 supplies exact guarded facts and preserves the actual publication result. Optional diagnostics and later output failure cannot change committed publication into rejection.
- The manifest owns the stored `contract` field; the manifest and registered supporting records each declare stored schema version 3. No extra contract field is imposed on supporting records.
- A journal's committed state permits completion/cleanup only, even if its success response was lost. Rollback permission does not depend on whether the caller observed an acknowledgement.

All findings were corrected by the owning authors and closed by independent rereview. These are architectural analysis results, not implementation approval or executed satisfaction evidence.

The following commands were run against the reconciled records and passed:

```bash
python3 tests/engineering/validation/requirement_schema_tests.py
python3 tests/engineering/validation/system_design_schema_tests.py
python3 tests/engineering/validation/architecture_schema_tests.py
```

The suites passed 13, 18, and 11 tests respectively: 42 total. They validate record shapes and the selected identity, naming, containment, source, typed-reference, and Interface participation properties, including independent malformed fixtures.
Additional direct inspection confirmed all eight SRs have allocated contributors; all 44 acceptance positions appear exactly once in the contribution table; every contributing AR resolves; and each criterion has an AR under its own parent SR, alongside any explicit supporting contribution.
Independent navigation review found the derived indexes, current/deferred scope, and historical review references consistent with the canonical records. Final direct inspection passed 1,826 local Markdown path/anchor checks across 30 documents, whitespace inspection of modified and new text files, and `git diff --check`.
Compared with `9055b3c0`, 243 of the prior 247 entities remain byte-identical. Only the two Modules and two Interfaces named above changed. All prior requirements, Scenarios, Features, Functions, the other architecture entities, and all eight schemas retain their bytes. REM, existing `docs/` contracts, runtime packages, skills, and tests are unchanged.

Review subject SHA-256: `6487bb78b313919717350ab8da7061913da71044f419ba67ddfff8ee1bd3dd53`.
This digest covers the sorted repository-relative paths and SHA-256 content digests of all 265 entity JSON files under `design/`, excluding schemas, with `path + NUL + content_digest + newline` for each manifest entry. Earlier 118-, 139-, and 247-entity review subjects remain historical and are not retargeted by this result.
No skills or CI were run. No runtime behavior, acceptance criterion, installation, publication, or public adoption was executed or claimed by this design pass.

### Historical inline-realization profile and consistency checks

The following result describes the inline profile before the directory migration below. Its record and schema digests retain that earlier meaning.

The subsequent pass adds optional subordinate views to the Module and Interface schemas and populates the two CLI Modules and their two Interfaces. It adds no entity, changes no parentage or allocation, and retains the existing 265-entity population.
Author self-review checked the views against refined Architecture Design and the unchanged logical contracts. It confirmed that the shared process/package does not merge responsibility or authority, that shared files identify distinct contributions, that receipt callbacks preserve the command/store ownership boundary, and that operational persistence remains separate from REM definition storage.
Material choices have rationale, alternatives, consequences, and revisit conditions. Runtime/platform qualification and implementation conformance remain explicit deferrals. No independent review of these newly authored views has been performed; the earlier independent review applies only to its retained logical subject.

The three direct schema suites listed above passed 13, 18, and 15 tests: 46 total. Four new architecture tests exercise partial views, required observation attribution/content, decision reasoning, and rejection of empty or undeclared structures. The shared source check now includes observation sources.
Direct preservation inspection found 261 of the prior 265 entities byte-identical. The four extended records preserve their logical fields, relationships, identities, and prior provenance; the two Module limits now acknowledge this bounded mapping. All pre-task REM files and the six unaffected schemas retain their bytes.
All 18 unique mapped source artifacts match the pinned `9055b3c0` source revision. These source comparisons and schema checks provide no executed evidence of CLI behavior.

Local Markdown inspection found no unresolved link in `design/`. Two pre-existing references in `rem/knowledge-reconstruction.md` still target `scenario-analysis.md#step-1-confirm-or-reuse-the-feature`; the heading currently yields `step-1--confirm-or-reuse-the-feature`. The user's in-progress REM files were left unchanged. Whitespace checks passed.

Inline-realization entity subject SHA-256: `ddafd473a92c0f39e007149dd7ddd62dddd877d10666fab26b7f7aae92d63808`, using the entity-manifest rule above.
The extended schema SHA-256 values are `069bc687433c60f2318a54cf64cb2f97dd2dc154410131e978fe0b80ac6d3872` for `module.schema.json` and `dfea748255c0268fef393f76650a2fc142e4042bca7ef29a7a6033a5f606e994` for `interface.schema.json`.
These identify the authored record and schema states for this bounded self-review; they do not retarget the historical independent review or establish product satisfaction. No skills, CI, runtime qualification, installation, release, or adoption ran in this pass.

## Directory profile migration

The selected representation places each logical Module or Interface in its own stable-ID/title directory, with `module.json` or `interface.json` and optional subordinate files under `realization/`. Aggregate views live under `architecture/views/` and derive from those records.
This is a draft authoring-profile migration; current product contracts, runtime formats, requirement parentage, allocation, and entity identities are unchanged.

The bounded execution sequence is to reconcile REM ownership principles and the application profile, update self-contained schemas and discovery checks, relocate the 21 logical architecture records, split the four populated realization views without losing observations/choices/deferrals, reconcile links and derived views, then validate and independently inspect the resulting state.
Before relying on the new profile, check all current entities and facet files, reject old inline and misplaced records, compare logical content and realization content with the pre-migration snapshot, check navigation, and record findings and results here. Earlier review subjects remain historical. No CI or runtime qualification is part of this migration.

### Migration result and review

The directory migration is complete for the authored architecture population: 15 Module directories, six Interface directories, and 14 populated realization facet files. The six aggregate perspectives and their navigation page derive from the logical records and applicable facets. Seven self-contained facet schemas supplement the eight entity schemas; Module and Interface schemas now reject inline realization.

Direct preservation comparison against the pre-migration working state confirmed:

- All 265 logical entities retain their definitions, identities, relationships, and provenance. The 244 entities outside the Module/Interface collections remain byte-identical at their prior paths.
- All 21 relocated logical records equal their previous JSON after removing only the inline realization property where present. The 17 records without that property retain their original bytes at the new paths.
- Combining the 14 facet files recovers every observed field and its exact source attribution, all six complete proposed choices, and all seven deferrals from the four earlier views. Each choice and deferral has one authored facet owner.
- The 18 mapped source artifacts still match the pinned implementation revision. Six unaffected entity schemas retain their bytes; no runtime source or public format changed.

The three direct commands in the retained validation section passed 13 requirement tests, 18 system-design tests, and 20 architecture tests: 51 total. The architecture suite now selects logical entities separately from facets, checks facet source registration, and rejects flat legacy files, inline realization, orphan or misplaced records, unknown facets, and wrong-owner facets using independent fixtures.
All inspected local Markdown paths and anchors across the 37 `design/` and `rem/` documents resolve. The two earlier REM Scenario Step 1 links were corrected. `git diff --check` and direct whitespace inspection of newly created text passed.

An independent reviewer assessed the directory/facet profile, REM ownership rules, schema and discovery changes, logical and realization preservation, derived views, and historical review boundaries. The review independently confirmed exact logical preservation and recovery of all realization content. It identified stale naming examples and two README sentence errors; those documentation issues were corrected. No material finding remains within this bounded architecture/profile migration. This review does not establish full workflow completion, runtime conformance, platform support, installation, or release qualification.

The current subjects use SHA-256 over sorted repository-relative paths, each followed by NUL, the file-content SHA-256, and newline:

| Subject | Population | SHA-256 |
| --- | --- | --- |
| Logical entities | 265 declared IR/SR/AR/Scenario/Feature/Function/Module/Interface records; excludes facet and schema files | `89f0b1563fbbb286e8136e8550219fc4618dc14c2976fb9504ca9a135b3dbf34` |
| Realization facets | 14 JSON files beneath an owner's `realization/` | `766e634d9b31cfe9fe5a47550aa24aec6e1ee5e242d1d122690ec4321f487a5d` |
| Authoring schemas | Eight entity and seven facet schemas | `20a6275258c14e18a466a1c1a29130fc294e87e37787dbb7e7baf66376adf8ad` |

The explicit populations matter: subordinate facets are no longer counted as logical engineering entities. Earlier subject hashes continue to identify their original flat or inline representations. No skills or CI ran, and no implementation verification, installation, publication, or product adoption was performed.

## Walkthrough retirement result

The mixed-purpose walkthrough was removed after transferring its useful content. All 44 acceptance-contribution arguments now have one attributed owner across SR-040 through SR-047 using the existing `sources` shape. The logical view renders those arguments; the dependency view retains the composed cooperation and nine Scenario summaries as derived explanations. Current source locators and Markdown links resolve to those owners or the retained review evidence. No replacement top-level CLI architecture document was created.

The requirements retain their prior statements, 5W2H analysis, acceptance criteria, identities, status, and containment. All Function allocations and logical Module/Interface definitions are unchanged. Eight SRs gain attributed analysis entries, and four architecture records receive source-locator repairs. Of the 265 logical entities, the other 253 retain their exact bytes. All 15 schemas are unchanged.

Thirteen of the 14 realization facets retain their bytes. MOD-011's software facet additionally retains the former walkthrough's exact limitation that construction without write authority is an architectural constraint, not a claim of JavaScript capability sandboxing. This clarification has one canonical owner and imposes no new requirement. The retained historical review and completed-migration excerpts above remain verbatim, with their original subjects and scope.

The following direct checks passed:

```bash
python3 tests/engineering/validation/requirement_schema_tests.py
python3 tests/engineering/validation/system_design_schema_tests.py
python3 tests/engineering/validation/architecture_schema_tests.py
```

Results: 13 requirement tests, 18 system-design tests, and 20 architecture tests; 51 total. The architecture suite also passed after the final realization clarification. Direct inspection confirmed exact retention of all 44 contribution arguments and nine Scenario summaries, view agreement with the SR-owned arguments, unchanged historical excerpts, no active retired-path reference in `design/`, and resolution of all 1,876 inspected local links/anchors across 37 Markdown files. Whitespace checks passed. The existing production CLI contract and runtime code were not changed.

Independent read-only review assessed preservation, ownership, current views, source references, and historical scope. It identified the capability-sandbox clarification and two wording errors; all were corrected and independently rechecked. No material finding remains within this bounded retirement review. These results do not establish runtime conformance or full workflow completion. No skills or CI ran.

The current logical-entity subject SHA-256 is `d8118fd5475fbd5df0a9ffda8f633e168cff60e8ec11f7ad3582465e41dfb0cb`; the current realization-facet subject SHA-256 is `30a37768ead00dcae15d3656f800060d2cca4c2c2fb21768053bfd790a541884`. They use the sorted path/NUL/content-digest/newline manifest rule above, with the same explicit 265-entity and 14-facet populations. The schema subject remains unchanged. Earlier hashes retain their original historical meaning.
