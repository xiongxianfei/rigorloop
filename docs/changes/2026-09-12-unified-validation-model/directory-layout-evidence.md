# Directory relocation evidence

Owning change: [unified validation and hierarchy](change.json). This evidence is scoped to the user-selected directory layout and its reader repairs, not the later validation executor or whole-initiative closeout.

## Exact model path map

| Previous subject path | Current subject path |
| --- | --- |
| `docs/design/system/system.md` | `docs/design/system.md` |
| `docs/design/design/design.md` | `docs/design/skill/authoring/design.md` |
| `docs/design/workflow/workflow.md` | `docs/design/skill/workflow.md` |
| `docs/design/review-closeout/review-closeout.md` | `docs/design/skill/assessment.md` |
| `docs/design/record-format/record-format.md` | `docs/design/cli/records.md` |
| `docs/design/installation/installation.md` | `docs/design/cli/installation.md` |
| `docs/design/validation/validation.md` | `docs/design/engineering/validation.md` |
| `docs/design/packaging/packaging.md` | `docs/design/engineering/packaging.md` |
| `docs/design/release/release.md` | `docs/design/engineering/release.md` |
| `docs/design/skill/skill.md` | `docs/design/skill/skill.md` |
| `docs/design/cli/cli.md` | `docs/design/cli/cli.md` |
| `docs/design/engineering/engineering.md` | `docs/design/engineering/engineering.md` |

Records examples move from `docs/design/record-format/examples/` to `docs/design/cli/examples/records/`; Workflow examples move from `docs/design/workflow/examples/` to `docs/design/skill/examples/workflow/`. CLI examples otherwise stay in place. Markdown links are rebased; JSON and Mermaid payloads retain their bytes and synthetic identities. Removed source directories are empty; no forwarding documents or symlinks are added.

## Preservation and authority

The pre-move snapshot contained 79 model/example files. Independent Design Review compared 50 JSON/Mermaid payloads byte-for-byte and 311 relative-link targets after relocation. Model requirement identities and text remain intact; System explicitly selects the layout and Design preserves its portable default with this project override. Historical records, prior reviews, proposals, plans and hash-bound retired method sources retain their original subjects. Current model registry entries retain their IDs and reference the relocated files.

## Actual checks and corrections

Before reader repair, the current-model regression failed at eight newly nested paths with BFR-MODEL-PATH; deleted-layout/example selection also failed to select the current owners. The repaired validator admits only the declared project paths in addition to existing portable paths and retains containment and symlink checks.

The first full selector run reported 23 failures and 143 passes: importing the shared map from the large boundary validator left the isolated wrapper fixtures without that transitive dependency. Independent Code Review recorded directory-selector-dependency. The correction places the constant in dependency-free `scripts/model_layout.py`, provides it to both isolated fixture constructors, and proves that changes to the map select both affected regression suites. Wrapper assertions remain unchanged.

The first combined CLI run passed 30 of 31 tests and exposed an old Workflow source/fixture-parent location. After updating both, the focused Workflow rerun passed both tests; the other 29 combined tests are unchanged and passed. No JSON example payload was edited to make a test pass.

## Final focused results

- `python scripts/test-boundary-first-validation.py`: 90 tests passed.
- `python scripts/test-select-validation.py`: 167 tests passed, including real isolated CI wrapper paths and shared-map reader classification.
- `python scripts/test-change-metadata-validator.py`: 8 tests passed against relocated Records fixtures.
- `node --test packages/rigorloop/test/record-store-model-examples.test.js packages/rigorloop/test/record-store-v3-contract.test.js packages/rigorloop/test/record-store-v3-reads.test.js packages/rigorloop/test/record-store-v3-mutations.test.js packages/rigorloop/test/record-store-workflow.test.js`: 30/31 passed initially; `node --test packages/rigorloop/test/record-store-workflow.test.js` passed 2/2 after its fixture path correction, closing the sole failure.
- `python scripts/validate-boundary-first.py --check --path <each of the twelve current mapped models>`: passed.
- `python scripts/validate-documentation-prose.py --mode enforce --path <each of the twelve current mapped models>`: zero errors/warnings.
- `git diff --check`: passed.

A final navigation scan also corrected the current CLI document's runnable validation example to use the relocated Workflow and Records paths. Historical source-disposition paths remain source-qualified history. Preexisting prose debt in untouched legacy paragraphs is not claimed repaired by this directory slice.
