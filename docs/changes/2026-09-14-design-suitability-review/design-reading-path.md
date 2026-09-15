# Design reading-path correction

## Scope and authority

The user authorized improving presentation while retaining the current decomposition after the advisory suitability assessment. This is isolated Design authoring, not continuation of the completed repository-cleanup delivery plan. The affected existing owners are System, Skill, Design and Engineering. Constitution's current-owner and retention rules, SYS-SR-02/06/10/12, SKL-SR-06/07/24 and DES-SR-02/08/11 govern the correction.

The earlier advisory remains an assessment of its original subjects. This author does not update or approve that assessment. Existing governing records remain attributable to their original scope; their completed status does not approve these edits.

## Execution outline

1. Capture the four existing subjects and inspect the sections to rearrange plus their consumers.
2. Add reading-path navigation and direct anchors for existing specialist responsibilities. Keep all model paths, requirements, decisions, examples, diagrams and public behavior.
3. Put current contracts before historical source-transfer material. Preserve the transfer content and its existing heading anchors; avoid creating archive copies or extracting new models.
4. Correct Engineering's obsolete retained-specification navigation to the existing current-owner contract.
5. Check preserved paragraphs, requirement/decision rows, diagrams, old anchors and local links against the captured basis; run repository-selected validation for the four changed models and diff hygiene.
6. Record actual results and hand the exact changed subjects to independent Design Review. Do not claim independent approval or governed closeout.

## Proof and recovery

Use a before/after content comparison to prove that section moves and new headings preserve existing contractual content. The one planned prose replacement is the obsolete Engineering retained-specification reference; review its replacement against System's complete-retirement boundary. Local Markdown links must resolve, and model structure must remain accepted by the existing validator. No new permanent test or behavior change is needed for these editorial operations.

Run `bash scripts/ci.sh --mode explicit` with the four exact changed Design paths, plus `git diff --check`. Existing selectors choose the dependent checks. CLI subject inspection supplies exact identities. Preserve the earlier untracked advisory report. Restore only a failed editorial slice from the captured source after checking for intervening edits; do not reset unrelated work or rewrite historical records.

## Consumer disposition

Current paths, existing heading anchors, model markers, requirements, decisions, examples and diagram bodies stay stable. Published skill sources, generated adapters, CLI schemas/runtime, tests and release inputs therefore need no implementation changes. New headings and reading tables are navigation within existing model ownership. Check actual repository-selected consumers before handoff rather than inferring a pass from this disposition.

## Authoring result and review handoff

System, Skill, Design and Engineering now have reading guides. Skill's existing specialist contracts precede the source-transfer inventories and have direct capability anchors. System's current retirement boundary and Design's current feature-format compatibility appear before their original transfer history. Selected historical maps are expandable in rendered Markdown; their text and existing heading anchors remain in the same files. Material decision rationale remains visible. Engineering's obsolete retained-specification sentence now points to the current Design owners.

No model, requirement, decision, diagram, example, public capability or source file was removed. A comparison against captured source bytes preserved every original nonblank line except the declared Engineering sentence, all old headings, all requirement/decision rows and all Mermaid bodies. Additional headings and navigation introduce no new responsibilities. The final direct model check passed; a diagnostic scan of all twelve model documents found no unresolved targets among 528 local inline Markdown links. This scan does not validate external URLs or certify browser rendering.

The initial diff-hygiene check caught two extra blank lines at EOF after section moves; those were removed and the check passed. The final placement of Design's retention subsection was checked again with the model validator. CLI full-content inspection initially exceeded its default response bound; repeating the same selection with an explicit 1 MiB response budget succeeded. No source or record writes occurred on that rejected read.

CLI context inspection found the earlier owning repository-cleanup activity completed, with prior subject-drift observations. That completed delivery plan and its assessments were not used as approval of these new edits. This isolated authoring result preserves historical record identities and the earlier advisory, and does not claim current applicability for their old subjects.

The exact four subjects below are the Design Review handoff. Relevant unchanged dependencies are System's shared-owner contracts and the model-document convention; the label-normalization example and all diagram bodies are unchanged. An independent reviewer should assess current-versus-historical presentation, navigation and preservation against the declared editorial scope. No independent approval or final Verify has been performed for this correction.

| Subject | Before identity | Authored identity |
| --- | --- | --- |
| `docs/design/system.md` | `sha256:d6c35b64cc3ea5ff9b170124fda92c4d16658974859266b50b5852273d10d63d` | `sha256:3bc11325ae7ef3474964bd08204066500f564b492c7794be6fcd478dc209df76` |
| `docs/design/skill/skill.md` | `sha256:ad80a8e44a1f3c2bcc5c79fa06e5b0ba6e62b248e66a8105a458f3505f68145e` | `sha256:f599ec7d5f0c330a2c09e6148e4ee25f5af724b114d957e8c196b7550104da36` |
| `docs/design/skill/design.md` | `sha256:d787cece629dd7eed0a12c53366a5d41aa52f59d5c1250881550b5eebe04ff0a` | `sha256:898080330861918288787f6d5c713516429a32818ecc3413892f5d4ab3c61ab8` |
| `docs/design/engineering/engineering.md` | `sha256:5cc2d2850fbc4147b1bd123a1f36c3f88baa49d4b698985bee00a6975ed03b4b` | `sha256:42fab5881ecf333e0e88ecbb6465ee47d75bdd8f54d9c465797bc13e85b19664` |

## Completed validation

Commands actually run on this correction:

```bash
bash scripts/ci.sh --mode explicit --path docs/design/system.md --path docs/design/skill/skill.md --path docs/design/skill/design.md --path docs/design/engineering/engineering.md
python scripts/validate-boundary-first.py --check --path docs/design/system.md --path docs/design/skill/skill.md --path docs/design/skill/design.md --path docs/design/engineering/engineering.md
git diff --check
```

The selected CI invocation exited 0 and reported “Selected CI checks passed.” Its selected checks were `record_store.schema`, `model.validate`, `boundary_first.regression`, `change_metadata.regression`, `rigorloop_cli.test`. Preflight also passed. The separate model validation on the final editorial layout and diff hygiene passed. Preservation and local-link observations above came from read-only Python comparisons, not new permanent tests. These results support the authored presentation change; they are not independent semantic approval, hosted CI, release qualification or lifecycle closeout.
