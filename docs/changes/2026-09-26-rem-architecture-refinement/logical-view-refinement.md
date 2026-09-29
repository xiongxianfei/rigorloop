# Logical view comprehension refinement

This bounded refinement follows the user's review of the generated Logical view. It improves how the existing architecture is explained and exposes incomplete collaboration. It does not approve architecture, add undocumented contracts, change allocations, or execute product behavior. Earlier review records retain their original subjects.

## Scope and sequence

1. Preserve the current working model and distinguish missing architecture from presentation defects.
2. Clarify the REM view method and repository projection contract: show recorded limitations with the overview, disclose parent → child → allocation details, and keep readable navigation separate from canonical provenance.
3. Refine the existing renderer and its focused tests. Retain the five output pages, deterministic UTF-8 rendering, exact-byte read-only checking, and rejection before writes. Keep non-Logical views unchanged when their inputs have not changed.
4. Regenerate the Logical page, reconcile navigation, check preservation, and independently review the actual generated result and tests. Assess relevant Scenario paths to identify the next missing collaboration analysis without asserting invented Interfaces.

## Projection contract and proof allocation

The first Logical diagram continues to show the highest useful Module level and only declared visible Interfaces. A concise coverage table beside it distinguishes direct and descendant allocations and reports declared Interface participation. Counts describe modeled content, not requirement satisfaction or architectural completeness. Recorded top-level `design_limits` remain visible near the overview with their owning source; do not infer missing contracts from absent edges, synthesize draft arrows, or guess semantic categories from keywords in prose. Child limits remain accessible in their relevant context.

Readable Module details follow actual containment. Only top-level responsibilities appear at the initial Module navigation level; expanding a parent reveals child responsibility summaries and declared collaboration. Child definitions stay within their parent's expansion recursively, including deeper nesting. Expanding a child exposes its responsibilities, significant state, and limits. Direct allocations and full descendant/provenance inventories are separate optional expansions so understanding collaboration does not require reading all trace links. Module navigation within this Logical page targets stable identity-based detail anchors, with separately labeled canonical-record links. Generated anchors do not become engineering identities.

An owner without a direct AR allocation must not imply that descendant AR coverage exists when none does. Leaf wording reports absence directly; parent summaries show actual descendant counts and retain exact accountable owners. Record-specific deferrals may be displayed from the owning definition without inventing a generic lifecycle conclusion. An empty `owned_state` list means no directly owned state is recorded; it does not imply that descendants own no state.

Focused proof covers the user-visible failure mechanisms: flattened children, hidden known limitations, Module links bypassing readable context, unseparated inventories, false descendant coverage, and changed or invented ownership/Interfaces. Existing public-command projection tests retain deeper hierarchy, deterministic regeneration, source preservation, and rejection-without-writes coverage. Use independent expected containment and known source text in assertions, not renderer-generated expected structure. Direct link/anchor and diagram-source checks complement independent review of comprehension; they do not establish browser rendering or runtime conformance.

## Scenario analysis of the remaining collaboration scope

Read-only inspection found three concrete analysis slices for later contract derivation. These paths identify applicable participants and obligations; they do not establish runtime sequences or a new Interface.

| Scenario basis | Responsibility analysis | Current disposition |
| --- | --- | --- |
| [SCN-019 — Establish an identifiable baseline](../../../design/requirements/scenarios/SCN-019-establish-an-identifiable-baseline-for-later-engineering-reliance.json) informs SR-020, which confirms FUNC-020 under MOD-005 / MOD-017. | The retained baseline must preserve identifiable model content and interpretation. The Scenario and Module limits indicate a need to analyze collaboration with Engineering model management; they do not identify a defined MOD-005-to-MOD-001 contract. | MOD-005 defers storage/change-control Interfaces; MOD-016 defers cross-boundary contracts. IF-001/IF-002 remain internal. |
| [SCN-053 — Produce a usable result through specialist guidance](../../../design/requirements/scenarios/SCN-053-produce-a-usable-result-through-specialist-guidance.json) informs SR-053, whose `confirms` references include FUNC-053 / MOD-012 and FUNC-032/033 / MOD-008. | Published specialist invocation and canonical model-authoring guidance have distinct accountable responsibilities across Engineering operations and Engineering governance. | MOD-017 and MOD-012 expressly defer the cooperation/specialist contracts. |
| [SCN-066 — Approve and publish one exact qualified candidate](../../../design/requirements/scenarios/SCN-066-approve-and-publish-one-exact-qualified-candidate.json) informs SR-070 → FUNC-069/070 / MOD-015 and SR-007 → FUNC-026 / MOD-006. | Product delivery requires applicable governance authority. FEAT-020 also references assurance Functions FUNC-027–031 / MOD-007; that broader Feature context does not imply every Function executes in SCN-066. | MOD-015 defers authority/evidence collaboration Interfaces and ARs. Existing IF-006 covers installation and does not define this release contract. |

The authoritative deferrals remain in Module `design_limits`; this record retains the basis of the bounded inspection. The generated overview must not upgrade these needs to declared collaborations. Finishing their logical contracts, allocation, and ordinary/adverse Scenario outcomes is separate architecture analysis.

## Result

The Logical view now has four root Module disclosures and 15 child disclosures nested under their actual parents. Same-page Module links reach stable readable detail anchors; canonical JSON links remain separately available. Responsibilities, state, child collaboration, and local limits precede optional direct-allocation and descendant inventories. The overview shows all 13 recorded top-level design limits and distinguishes direct/descendant allocation counts from declared Interface counts. Leaf Modules state missing direct AR allocations without suggesting nonexistent descendant coverage; empty state lists report only the absence of directly recorded state.

Three added regression cases reproduced the previous failures before the renderer correction: flat Module disclosure, hidden recorded limitations, and false descendant-allocation wording. The refined suite checks independent HTML containment, explicit expected parentage including a deeper level, readable anchors, separate inventories, and preservation of source text without relying on deferral keywords. Existing projection and rejection protections remain active.

The following commands ran successfully:

```bash
python3 tests/engineering/validation/architecture_view_tests.py
python3 scripts/render-rem-architecture-views.py
python3 scripts/render-rem-architecture-views.py --check
git diff --check
```

All 14 projection tests passed. Generation changed only the Logical page; the other four generated pages remain byte-identical to the pre-refinement snapshot. The read-only renderer check confirmed all five outputs are current. Direct navigation inspection checked 3,094 local links, including 344 anchors, across 42 current REM/design Markdown files and this record. Independent structural inspection confirmed all 19 Module disclosure parents and balanced expansion boundaries. The nine Mermaid graph blocks across the architecture views have distinct declared node IDs and resolving edge endpoints. Whitespace and final-newline checks passed for all seven changed files and this new record, including untracked output.

Preservation comparison found exactly seven changed preexisting files and 339 unchanged files in the 346-file snapshot. All 298 design JSON files retain their population and bytes, including the schemas, 63 Function allocations, 28 AR allocations, Module/Interface contracts, and 14 realization facets. The three earlier work records and both user archives are unchanged. The seven changed files are `rem/methods/architecture-views.md`, `design/support/README.md`, `design/architecture/README.md`, `design/architecture/views/README.md`, `design/architecture/views/logical.md`, `scripts/render-rem-architecture-views.py`, and `tests/engineering/validation/architecture_view_tests.py`.

Independent scope review found one wording ambiguity in this record: “confirmed Functions” could imply lifecycle confirmation. The Scenario table now names the `confirms` relationship explicitly; Function records remain draft. Final independent review of the actual renderer, tests, generated artifact, and supporting scope found no remaining findings. It independently checked counts, hierarchy, navigation, exact ownership, source-preserving disclosure, and unchanged non-Logical output. This review establishes bounded presentation and model-projection consistency.

Reviewed SHA-256 identities:

```text
renderer: 1c3be54f370a2e7203987f78a2cb35105b35dc39e9c772fafe738b8fd22f04e3
projection tests: 1138c3b7b8e0f95983264f1516adaaff0021bcf166beb59ac792a294c16cd112
Logical view: 09de5eaa99d47f3a65fbdfc9d9b09d386147196ae971f844392052b51a545ae3
```

The canonical view source identity remains `1020bbbc4f13e88cc9f7ff97023187b3a96f7790e254ed17442363ee33deac88` for 269 entities and 14 realization facets. Working subject identity: `a667a8321e791e1f28d0b830476e6771bcb3c6d2181e5b44edab4876679999e5`. This covers the seven changed files listed above plus all 298 `design/**/*.json` files: 305 files. Compute SHA-256 over sorted repository-relative path, NUL, lowercase hexadecimal file SHA-256, and newline. This record is excluded to avoid circular identity; earlier subjects are not retargeted.

Browser rendering and product runtime conformance were not assessed. The three missing collaboration slices above remain explicit architecture work; no new Interface or satisfaction claim is introduced. No skills, CI, release, or commit ran for this refinement.
