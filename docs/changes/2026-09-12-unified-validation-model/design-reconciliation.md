# Three-model Design reconciliation

Owning change: [change.json](change.json). This author-owned map records source disposition, not review approval or runtime adoption.

## Exact input basis

| Source | Inspected identity | Final disposition |
| --- | --- | --- |
| `docs/design/cli/cli.md` | `sha256:c4cd40f5523c8d4d79a4e0d62464552be57ecd023a74f8e664f3274f02f91bed` | Executable parent with Command Interface and Persistence sections, Records child and Installation child; detailed interface and examples preserved. |
| `docs/design/design/design.md` | `sha256:c169fd0c8e942afdd804fe56448d7b5e8fea76f0dd30f7748dadefcd7e0cc770` | Skill Authoring design-method contract, preserved at stable path. |
| `docs/design/distribution/distribution.md` | `sha256:29820f18258a3b47e63b1355d2ddd86d1c12e41240d2d006ebdb104eab7c99a7` | Deleted after split: Packaging receives generation/metadata and source maps; Installation receives acquisition, destination mutation and bounded recovery. No stub or duplicate archive. |
| `docs/design/record-format/record-format.md` | `sha256:b021a86b073815e934a467ef1588806dbeae47033d0b4d37c8dd480a47b733f4` | CLI Records child, preserved at stable path. |
| `docs/design/release/release.md` | `sha256:765476620478f65522d9fade25fabacf9e661629212c755be73b24b52c226717` | Engineering Release child, preserved at stable path. |
| `docs/design/review-closeout/review-closeout.md` | `sha256:4ab2aca0b2f7aebc72ef0d2bb975975208f6451fd8ab975ad645b59191bfb251` | Skill Assessment child, preserved at stable path. |
| `docs/design/skill/skill.md` | `sha256:68464e5b3bbcbf243ddb502320db7368fe6e4db43510d1dbfb9eebc07541bb0c` | Expanded into product behavior parent with six named children; common/pilot SKL requirements preserved. |
| `docs/design/system/system.md` | `sha256:17230483857790b571963ad44b71ce9ca1d383ae1bcb17a1ef39132e6208e9a7` | Rewritten as composition of three parents; retains SYS requirements, decisions, scenarios and precise earlier source maps. |
| `docs/design/validation/validation.md` | `sha256:ba10375105bb3b57ee6b535b06248e0af6defbfab892d31e241ae76dc0f38697` | Engineering Validation child; generic proof criteria retain their original applicability and repository execution remains separate from customer skills. |
| `docs/design/workflow/workflow.md` | `sha256:8b4432132a894a02d9950e70f3bb85a44bf11a091d888ef3c4463dad4f03f1a4` | Skill Workflow child, preserved at stable path. |

## Exact combined-source split

| Former obligation | Receiving owner and meaning |
| --- | --- |
| DIST-SR-01; DIST-DEC-01 | Explicitly superseded only for combined ownership. System and ENG-SR-01/06/07 define separate Packaging and Installation responsibilities with one shared representation. Original transfer/preservation obligations survive in ENG-SR-10/12 and DIST-SR-19/20. |
| DIST-SR-03–06/09/17–20; DIST-DEC-02/06 | Packaging, unchanged requirement/decision rows. Includes target descriptors, archive identity, deterministic production, isolated output, composed proof and actual source/consumer retirement. |
| DIST-SR-02/07/08/10–16; DIST-DEC-03–05 | Installation, unchanged requirement/decision rows. Includes retired-input rejection, trust, extraction safety, default conflicts, state exclusion, explicit force, races, diagnostics and dry-run. |
| Stable representations | Packaging owns the exact shared descriptor/report/hash representation; Installation enforces it and owns installer failure classes and proxy diagnostics. |
| Destination conflicts and explicit replacement; Partial failure and retry | Installation preserves the entire inspected technical sections, including retained originals, two-parent anchoring and no-clobber publication. |
| Historical spec/ADR maps and exclusive script retirement | Packaging preserves the source-qualified maps; each DIST reference resolves to its receiver above. No historical record or proposal is rewritten. |

## Scope and implementation boundary

The new Engineering parent defines this repository's development and product-proof allocation; it references Skill behavior instead of copying it. Implementation and Project Support are named behavioral sections in Skill rather than placeholder child files. All fourteen logical children have actual contract locations. Former TEST-SR-01–14 remain together in Validation; reusable applicability is preserved and operational executor details are repository-specific. No Test model or cache is restored.

This Design optimization does not execute the source/script/cache removals assigned to implementation by Validation and the earlier package initiative. Their cleanup remains required, including the default disposable cache directory under its bounded inspection rule. Active Markdown ownership links follow the new Packaging/Installation destinations; historical proposals, plans and records retain original identifiers. The current scripts, schemas, package code, canonical skills, templates, CI and tracked adapter support were searched for the retired Distribution path; none reads that path directly. The README contributor pointer was updated. Historical references remain identities; this authoring stage does not silently patch runtime selectors or tests.

The removed System chronology consisted of repeated amendment introductions and candidate inventories. Original change records retain their judgments; the active requirements, decisions, scenarios and exact mixed/necessary-design source maps are preserved. The old assumption that all nine documents were peer components is explicitly superseded by the three-parent composition. No data-format or public-command compatibility is changed by hierarchy alone.

## Assessment handoff

Independent Design Review must assess the complete final parents/children, all declared current consumers, preserved examples and the mixed-source split. Author checks establish syntax, identity preservation, navigation and absence of new prose findings only. Remaining preexisting legacy prose debt must be reported honestly. Delivery owns concrete work/proof allocation; actual implementation and successful Verify establish adoption.

## Independent Design Review corrections

Installer exit classes and proxy diagnostics reside in CLI Installation; active Release and retained architecture consumers reference that owner. Packaging retains the shared artifact representations. Workflow uses v3 immutable finding IDs and editable current fields, with origin preservation limited to change-level blockers. Validation preserves TEST-SR-14’s complete five-row retained-check contract and its source/package/runtime applicability paragraphs from the removed Test source, in addition to the stable requirement rows. Skill Authoring links the retained specialist contracts directly. These corrections preserve historical records and do not change executable behavior.
