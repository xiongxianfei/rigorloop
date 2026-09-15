# Current Design suitability — advisory assessment

## Result

- Skill: design-review.
- Review status: inconclusive for complete package approval; the inspected decomposition and contract boundaries support retaining the current architecture.
- Scope: current Design hierarchy after repository spec retirement; ownership, navigation, authoring method, selected cross-model contracts and structural validation.
- Package: the twelve model documents listed below. Semantic inspection concentrated on System, Design, Engineering and the skill/CLI/record, packaging/installation and validation/assessment boundaries. This is not a complete clause-by-clause assessment of every model and example.
- Upstream review ID: not selected; this is a new isolated advisory request, not a reassessment or settlement of an existing change.
- Review ID and round: design-suitability-advisory, round 1.
- Reviewer: current Codex reviewing actor; no reviewed Design was edited during this invocation. Independent provenance for complete package approval was not established.
- Material findings: none established within the inspected scope. The recommendations below are advisory, not required corrections or unresolved defect records.
- Correction targets: none mandated; recommended editorial work belongs to Design authors at the existing owners.
- Recording: advisory-durable/manual; this document only. No change manifest, lifecycle activity, applicability declaration or previous judgment is changed.
- Open limitation: complete semantic preservation, every relied-on example and package-wide approval basis were not assessed.
- Immediate next stage: isolated stop. Any authoring or formal package review is separately scoped work.
- Claim limits: no implementation, final Verify, release, customer-adoption or full Design-package approval claim.

## Assessment

The three main owners are a useful decomposition. System defines their composition; Skill owns published capabilities; CLI owns executable operations; Engineering owns building, proving and delivering them. The shared-interface and handoff tables in System make the producers, consumers and decision boundaries explicit. There is no demonstrated reason in this assessment to replace that hierarchy or restore separate specifications and architecture documents.

The method supports self-contained engineering contracts: stable requirements, technical realization, embedded decisions, representative acceptance outcomes and explicitly owned shared interfaces. Design DES-SR-03/06/08/10/16 preserves behavioral precision and downstream proof allocation. Its small label-normalization example demonstrates that a model can justify unnecessary supporting views without inventing additional components.

The inspected operational boundaries have substantive detail. CLI distinguishes persistence from approval, specifies coherent transactions and stale-basis rejection, and declares numerical resource limits. Records owns stored types rather than workflow judgment. Installation specifies full-candidate preflight, candidate-unit replacement, preservation of detached originals and partial-failure reporting. Packaging owns the artifact/trust representation consumed by Installation. Validation defines protective evidence; Assessment judges applicability and adequacy. These boundaries give implementers meaningful outcomes and failure cases to demonstrate.

“Self-contained” should mean current behavior and rationale resolve through current owners and their explicitly owned resources. It need not mean that one document contains every schema, example, CLI field and historical source. Working links and valid tables establish navigability and structure; they do not establish complete semantic preservation or adequate implementation proof.

## Advisory recommendations

### A1 — Separate current requirements from completed migration instructions

Evidence: [System's adoption and source reconciliation](../../../design/system.md#adoption-and-source-reconciliation), [Design's selected replacement map](../../../design/skill/design.md#selected-replacement-map), and [Engineering's source disposition](../../../design/engineering/engineering.md#source-disposition-and-follow-through). The documents explicitly qualify historical maps, so their presence alone is not a current contract contradiction. Nevertheless, readers encounter instructions to retain or amend sources that later retirement sections supersede. Engineering also still says that detailed retained specifications remain named authorities for unmigrated obligations.

Recommended outcome: a reader can identify current behavior without mentally applying successive migration amendments. Retain still-applicable decisions and constraints at their current owner; give completed transfer inventories a concise provenance reference where current reliance permits. Reconcile any apparent retained-authority wording with the actual current population. Preserve original review bytes and live operational inputs, including Release's explicitly retained literal baseline. Do not delete history or a source map merely because it is old.

Owner: Design authors for System, Design and Engineering, expanding to affected consumers only where necessary. This is an editorial recommendation; this assessment has not demonstrated lost behavior or authority that requires emergency correction.

### A2 — Make each diagram answer a distinct question

Evidence: [Installation's overview](../../../design/cli/installation.md#architecture-overview), [Building Block View](../../../design/cli/installation.md#building-block-view) and [Runtime View](../../../design/cli/installation.md#runtime-view). Acquisition, preflight, writes and results recur across views. The runtime view adds useful conflict/force branching; the structural view largely repeats the overview pipeline.

Recommended outcome: keep the required overview and every necessary supporting view, but make structural views explain actual responsibility boundaries and runtime views explain decisions, ordering and failure paths. Where two views answer the same question, reconsider their necessity under DES-SR-22 rather than mechanically retaining or deleting diagrams. This is a readability opportunity, not a missing-view finding.

Owner: the affected model's Design author. No new diagram quota or model split is proposed.

### A3 — Improve direct navigation to specialist capability contracts

Evidence: [Skill's remaining specialist contracts](../../../design/skill/skill.md#remaining-specialist-contracts) places Implement, Bugfix, CI maintenance, Vision, Project Map, Learn and PR procedures in long shared subsections, followed by a combined vocabulary table. Skill currently has 655 lines; the twelve model documents together have 5,643 lines. Counts describe reading scope, not a quality threshold.

Recommended outcome: use capability-specific anchors and a compact navigation table so a contributor can reach the applicable behavior, vocabulary and result contract directly. Keep short responsibilities in sections; create a separate child only if it has a distinct responsibility and reason to change independently. Preserve the current single ownership of shared policy.

Owner: Skill's Design author. This assessment does not claim that the existing specialist behavior is absent.

## Evidence and validation

Observed baseline: `38a3042e63c7c2462ecf8ffed29f4ac0cbb8923f` with a clean initial worktree. Repository source inspection was used instead of relying on Project Map freshness. Governing basis: Constitution, System, Design and the scoped Workflow/Assessment rules; VISION supplies product intent.

Commands actually run:

```bash
node packages/rigorloop/dist/bin/rigorloop.js workflow-context --format json
node packages/rigorloop/dist/bin/rigorloop.js subject inspect --root . --path docs/design/system.md --path docs/design/skill/design.md --path docs/design/skill/skill.md --path docs/design/skill/workflow.md --path docs/design/skill/assessment.md --path docs/design/cli/cli.md --path docs/design/cli/records.md --path docs/design/cli/installation.md --path docs/design/engineering/engineering.md --path docs/design/engineering/validation.md --path docs/design/engineering/packaging.md --path docs/design/engineering/release.md --format json
bash scripts/ci.sh --mode explicit --path docs/design/system.md --path docs/design/skill/skill.md --path docs/design/skill/design.md --path docs/design/skill/workflow.md --path docs/design/skill/assessment.md --path docs/design/cli/cli.md --path docs/design/cli/records.md --path docs/design/cli/installation.md --path docs/design/engineering/engineering.md --path docs/design/engineering/validation.md --path docs/design/engineering/packaging.md --path docs/design/engineering/release.md
```

Workflow discovery succeeded and reported six current candidate stores without selecting one. Initial exploratory `workflow-context --help` and `workflow-context --root . --format json` invocations rejected as invalid input; the documented invocation above succeeded. No store was mutated.

The explicit CI command exited 0: preflight passed, followed by `record_store.schema`, `model.validate`, `boundary_first.regression`, `change_metadata.regression` and `rigorloop_cli.test`. The wrapper reported “Selected CI checks passed.” No hosted CI, full release qualification or fresh public smoke was performed.

Two read-only Python scans inspected Markdown links in the twelve model documents. No unresolved local file targets or local heading fragments were found. These were diagnostic scans of ordinary inline Markdown links, not a complete Markdown-renderer or external-link validator. No network validation was needed or performed.

Subject identities below came from CLI subject inspection. Identity inspection and structural validation cover all listed models; they do not imply full semantic reading or approval of every listed subject or its examples.

| Model path | Exact SHA-256 identity |
| --- | --- |
| `docs/design/system.md` | `d6c35b64cc3ea5ff9b170124fda92c4d16658974859266b50b5852273d10d63d` |
| `docs/design/skill/design.md` | `d787cece629dd7eed0a12c53366a5d41aa52f59d5c1250881550b5eebe04ff0a` |
| `docs/design/skill/skill.md` | `ad80a8e44a1f3c2bcc5c79fa06e5b0ba6e62b248e66a8105a458f3505f68145e` |
| `docs/design/skill/workflow.md` | `ca2ba146c7cd45409b8b37a22d2baece26efed668f3ddad9309f495056ee1623` |
| `docs/design/skill/assessment.md` | `ae3b59ec189fd66962ddb3f50a4c0e48422fc9a1086aae641c54dd1481fd715b` |
| `docs/design/cli/cli.md` | `eef25314c2f34d4cceca2b8e2a12675fd9773da34fa949fd92cb224ed6a456e7` |
| `docs/design/cli/records.md` | `c088b648eb0a8308c8cae1deb7f5be562cf5fb81ceed2552d5256851ca69acf7` |
| `docs/design/cli/installation.md` | `756a282dbfe5f363eb4eb39986e0f68cf607501bfb9de2a98d96de66b0819578` |
| `docs/design/engineering/engineering.md` | `5cc2d2850fbc4147b1bd123a1f36c3f88baa49d4b698985bee00a6975ed03b4b` |
| `docs/design/engineering/validation.md` | `a8e0b1f979c2eb004e0a370a944895df81b29d093543b1a3913d26efb6c61607` |
| `docs/design/engineering/packaging.md` | `6dfe2436431bc52be7b3715e9249559bb7a893b08f6211e0a43b1a936b6096fd` |
| `docs/design/engineering/release.md` | `4e64ece2c8b1147778fa31becc2ecb1d08469b7610cf53d29ecf40b49865441e` |

## Remaining basis for complete approval

A formal whole-package Design Review would need complete semantic assessment of all selected models and relied-on examples, applicable proposal/review authority, actual contributor separation and reconciliation of prior findings. To establish complete retirement preservation specifically, it would also need to assess the authoritative transfer dispositions and any material omitted obligations. This advisory does not infer those results from a green suite, working references or prior completed-change status.
