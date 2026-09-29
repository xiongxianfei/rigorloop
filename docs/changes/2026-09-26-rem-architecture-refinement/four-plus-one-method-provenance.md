# 4+1 method provenance and REM adaptation

The user requested a clear distinction between the original 4+1 method, REM's adaptation, and project presentation choices. This is a bounded documentation refinement of the existing method and application profile.

## Scope and sequence

1. Cite Philippe Kruchten's 1995 paper in the Architecture Views method and distinguish its five concerns from REM-specific entity, ownership, traceability, and generation rules.
2. Document optional Logical reading perspectives without creating additional standard views or mandatory pages. Preserve exact ownership and the distinction between presentation grouping and architectural structure.
3. Reconcile Principle 19, architecture-model guidance, and REM navigation through links to the method. Record RigorLoop's Skills/Commands grouping in its application profile, preserving current browser behavior and explicit production-mapping limits.
4. Validate changed prose and local links/anchors, review source attribution and method boundaries independently, and compare the pre-edit snapshot. Preserve canonical JSON, generators, browser outputs, earlier records, and unrelated work. No skills, CI, or commit are requested.

## Result

The Architecture Views method now cites the original publication and distinguishes its 1995 date from the author's 2020 manuscript deposit. It maps the original five concerns to REM's authoritative inputs and identifies generated projections, stable identities, allocation, ownership, and Scenario separation as REM's rules. The six Logical reading perspectives are explicitly optional within one view. Principle 19, the model, the REM entry page, and knowledge-reconstruction navigation point to that method-owned explanation.

RigorLoop's application profile records how the current browser presents those perspectives and groups Commands and Skills under Public capabilities. Exact public-contract and behavioral owners remain distinct. The profile retains the missing production-realization mapping and does not claim automatic generation of skill instructions or command implementations from REM entities. No browser change or new architecture entity is implied by this documentation refinement.

Focused checks:

- `python3 scripts/validate-documentation-prose.py --mode enforce` with explicit paths for the six changed documents and this record: zero errors and warnings. An initial source-line formatting finding was corrected before the successful rerun.
- Local reference inspection across those seven documents: 213 link targets and 72 Markdown/explicit anchors resolve.
- `git diff --check`: passed.
- Comparison with the pre-edit snapshot: only the six intended existing documents changed; 398 snapshotted files remain identical, including canonical JSON, generators, browser resources and outputs, and earlier supporting records. This record is newly added.

Independent review verified the original paper's publication information, view concerns, alternative Logical representations, and Scenario purpose against the author's manuscript and arXiv metadata. It found the REM/project distinction, optional perspectives, exact ownership, and remaining production limits coherent, with no blocking findings.

The evidence covers the documentation refinement and source attribution. No skills, CI, browser regeneration, or commit were performed.
