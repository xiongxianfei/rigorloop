# Packaging Model Design

Model validation contract: model-document-v1

Parent model: [Engineering](engineering.md#packaging).

Owning change: [three-model reconciliation](../../changes/2026-09-12-unified-validation-model/change.json).

## Introduction and Goals

Packaging owns deterministic generation of supported skill archives, CLI candidate composition and the shared metadata/identity contract consumed by CLI Installation and Release. It does not install into a project or authorize publication. The former Distribution contract is split by responsibility: its installation requirements and filesystem behavior now live in [Installation](../cli/installation.md). Original DIST requirement identities are retained; DIST-SR-01's combined ownership and DIST-DEC-01's no-split decision are superseded by the approved three-model direction.

## Context and Scope

Inputs are canonical skill/resource sources, supported target descriptors, CLI package source and release intent. Outputs are generated target archives, the npm package candidate and attributable metadata. Skill owns capability semantics; CLI owns its command behavior; Installation owns user filesystem changes; Release owns publication. Builds cannot adopt governance or declare their own checks passed.

## Architecture Constraints


Canonical skill source remains `skills/`. Target templates remain authored inputs under `scripts/adapter_templates/`. Generated public bodies and archives are not tracked source; `dist/adapters/README.md` and `dist/adapters/manifest.yaml` remain the tracked support surface. Generated output never supplies canonical input to another generator.

Reuse the existing Python adapter builder/validator and npm package tooling. Preserve archive names, integrity algorithms and supported target descriptors. Builds never read installation-state markers or mutate installed roots. Installation consumes the shared package representation under its own filesystem/diagnostic contract. Closed package target/schema/algorithm values reject before consistency checks.

Model adoption is repository-local governance, not automatic customer activation. Package production grants neither local installation permission nor publication permission. Safe local fixture proof is sufficient for implementation; actual public release evidence remains Release-owned and cannot be replaced by fixtures.

## Requirements

| ID | Required behavior |
| --- | --- |
| DIST-SR-03 | Generation MUST derive the exact supported inventory from canonical skills, approved inclusion/transform decisions and thin target templates. Codex installs at `.agents/skills`; Claude Code at `.claude/skills`. Untransformed resources MUST retain raw bytes and all mapped dependencies; transformed bodies MUST preserve selected skill behavior. Unsupported frontmatter/runtime dependencies MUST be rejected or excluded with a manifest reason, not silently shipped. |
| DIST-SR-04 | The current support manifest MUST agree with generated inventory and version, name no active OpenCode target or alias, and contain no generated bodies. Generation MUST be deterministic for identical inputs. Current packages MUST contain the expected entrypoint and skill resources, without `.claude/commands` wrappers, OpenCode output, secrets or permission-broadening instructions. |
| DIST-SR-05 | Build/check operations MUST use temporary or explicitly selected package-output locations and MUST NOT create or synchronize an active project skill installation. The separate `.codex/skills` generator and its normal validation obligation MUST retire. Existing runtime directories MUST NOT be automatically deleted, copied over or treated as authored input. |
| DIST-SR-06 | Public distribution MUST supply separate versioned archives for each supported target through the Release-authorized channel; an optional combined archive MUST contain only the selected supported population. Archive/member inventory, checksums, source identity, generator identity and actual validation results MUST agree with recorded metadata. Generated expectations MUST NOT assert unexecuted validation success. |
| DIST-SR-09 | `rigorloop-tree-hash-v1` MUST retain the representation below, including normalization, regular-file membership, path ordering and independent counts. Unknown algorithms MUST reject. Target root safety MUST be checked separately; excluding symlinks from a hash does not authorize writing through them. |
| DIST-SR-17 | Current generation, manifests, CLI help, package metadata, public guidance, CI selection, release candidates and installed smoke MUST agree on the two-target population. Historical three-target facts MUST remain unchanged and explicitly scoped. Current runtime rejection MUST precede any historical metadata selection that could otherwise reinstall OpenCode. |
| DIST-SR-18 | Required package proof MUST exercise real generated archives, trusted metadata and actual packed-CLI install-only operation for both supported targets, including default conflicts for identical/empty/existing destinations, whole-skill `--force` replacement, unrelated-file/state preservation, and rejection of unsafe destinations in both modes. Local helper success or dry-run alone MUST NOT prove the composed path. Release retains fresh public smoke and publication safeguards; retained integrity and protection against unauthorized data loss MUST survive. |
| DIST-SR-19 | Fully superseded source documents and the specifically obsolete scripts MUST be removed only after necessary meaning, decisions, current readers and protective proof are reconciled. Mixed sources retain explicit owners. Unknown consumers block affected removal; no blanket archive, test, directory or historical-record deletion is authorized. |
| DIST-SR-20 | Support withdrawal MUST be disclosed as a public compatibility break and consumed by Release versioning. Failed adoption MUST retain or restore a coherent source/consumer slice without rewriting published versions, old evidence or user state. Design approval alone MUST NOT claim source retirement, implementation or publication. |

## Solution Strategy


Keep one package-producing path and one explicitly requested installer path. `build-adapters.py` and `adapter_distribution.py` remain the package owners in code; remove the local mirror alternative rather than redirecting it into `.agents/skills`. Builds use output directories outside active installation roots, reject destinations that overlap canonical sources or active target roots, and never use build-time cleanup as an installer. `--check` performs generation and validation in temporary output, retaining support-manifest consistency without requiring tracked generated bodies.

Retain target descriptors for Codex and Claude Code; withdraw OpenCode from public dispatch and current generation. Retain only independently required historical release-evidence readers with identified consumers. They are separate from installation; neither historical evidence nor old project-state schemas reopen installer compatibility. Current archive production never recreates an OpenCode package; archived-version checks that require the old producer execute against their recorded source instead of a current OpenCode template.

## Building Block View

Canonical skills and `scripts/adapter_templates/` feed `build-adapters.py`, `adapter_distribution.py` and `validate-adapters.py`. The npm candidate is produced from `packages/rigorloop/` using the existing package layout and release tooling. Generation uses isolated non-installation output. It packages supported resources and command code; it does not make every skill invoke CLI or bundle this repository's validation executor into a customer product.

### Stable representations

| Surface | Retained representation and constraints |
| --- | --- |
| Target descriptor | `codex`: `.agents/skills`, `rigorloop-adapter-codex-<release>.zip`; `claude`: `.claude/skills`, `rigorloop-adapter-claude-<release>.zip`. Package entrypoints remain generated archive members; the CLI mutates only its declared installation roots, not project `AGENTS.md` or `CLAUDE.md`. |
| Support manifest | Existing version and skill inclusion/portable/reason fields remain. Portable means compatible with the current supported population. Omit the current `command_aliases.opencode` section; neither retained target generates command aliases. Unsupported target names or unexpected alias sections reject. |
| Archive evidence | Preserve YAML artifact report schema/version, source commit, release/date, generator command, canonical source, manifest reference, per-target archives/checksums/roots, validation command/result and timestamp. Release's immutable-candidate and observed-evidence separation takes precedence over any older prose treating generation as a pass. |
| Hash algorithm | Regular files only; exclude directories, symlinks, metadata/times/ownership, absolute paths, the lockfile and temporary files. Relative UTF-8 POSIX paths have no leading `./` or trailing `/` and sort lexicographically. Normalize generated text to UTF-8/LF and remove a BOM without trimming whitespace or semantic normalization; binary files retain raw bytes under the existing deterministic classification. Each file digest is SHA-256 of those bytes. Hash UTF-8 `rigorloop-tree-hash-v1\n` followed by sorted `<relative_path>\t<file_sha256>\n` rows. |

## Runtime and deployment

Generate the supported inventory into temporary or explicitly selected output; validate resources, transforms, descriptors and actual archive bytes. Compose and inspect the npm candidate's executable and bundled release metadata. CLI Installation verifies this shared representation before any project mutation. Release consumes both candidates' exact identities and actual observations. Changed bytes or target population require affected proof and release consideration; no historical release is backfilled with new metadata or support claims.

## Source displacement and preservation

The following source-qualified maps preserve the former Distribution consolidation decisions. References to its DIST-SR identifiers resolve to this model for generation/metadata and [Installation](../cli/installation.md) for acquisition/writes according to the [reconciliation evidence (`design-preservation-delta`)](../../changes/2026-09-12-unified-validation-model/evidence.json). They are original source dispositions, not a second combined current owner. Historical judgments retain their original subjects.


The five spec families below are selected for full source retirement, each with its matching `.test.md`: `skill-invocation-commands-for-adapters`, `stop-tracking-generated-public-adapter-skill-bodies`, `target-native-init`, `multi-adapter-init-and-proxy-aware-download`, and `rigorloop-cli-lockfile`. This selects ten files, not their operational fixtures, proposals, plans or historical review records. Numbered ranges include lettered subclauses. The disposition below reconciles superseded commands/schema versions before transferring meaning; no old command is restored by its historical ID.

| Selected source clauses | Destination or explicit disposition |
| --- | --- |
| Target-native TNI-R1–13, R29–35, R92–94 | DIST-SR-02–04/15/17: retained target-native commands, roots, no aliases/removed syntax, clear manual/pinned automation guidance. OpenCode operations and three-target lists explicitly superseded by the two-target population. |
| TNI-R14–28, R50–85 | DIST-SR-10–15 replace state interpretation, selected ownership/drift checks, schema definitions, state writing/migration and successful managed/disjoint installation with destination-conflict checks and explicit `--force` replacement. Preserve no-write/dry-run and applicable result envelopes; no historical state schema remains an installer input. |
| TNI-R36–49, R86–91 | DIST-SR-07–09/18 and Release REL-SR-08/09/13: trusted metadata/archive/install verification and actual packed/public smoke for supported targets. The prior three-target smoke population is superseded prospectively; historical smoke judgments remain unchanged. |
| TNI-DES-01–06; E-DES-01–06; BND-INPUT/STATE/AUTH/COMPOSE/TEMPORAL/RECOVERY/COMPAT/ENV-001 and INT-001–003 | DIST-SR-13/14 preserve candidate/installed inventory guards for supported projects, user content and unmanaged inspection/backup. Managed original-basis interpretation, replacement, state writes and transaction/retry paths are withdrawn. Destination conflict handling replaces managed-project interpretation; historical IDs and judgments retain their meaning. |
| Multi-adapter MAI-R1–16, R39–46 including subclauses | DIST-SR-02–05/12/17: descriptors and retained roots survive; `--adapter` already retired by TNI. OpenCode installation, aliases and skills-only fallback now explicitly withdrawn; legacy project-root interpretation is withdrawn; project state is not inspected. |
| MAI-R17–38 | DIST-SR-07–09 and representation table: metadata trust/index, compatible releases, exact official URLs, local fallback, identity/size/hash/path checks, passing metadata validation and installed counts. OpenCode alias metadata is historical read-only evidence. |
| MAI-R47–76 | DIST-SR-10–15 supersede state creation, updates, migration, schema parsing, selected recorded-root checks and successful compatibility operations. State contents are irrelevant; default destination conflicts preserve all installed files, and force replaces only declared candidate units. |
| MAI-R77–95 | DIST-SR-15–18: safe network diagnostics and existing output/flags; generated temporary-output proof and no hand edits. Supported-target changes do not relax integrity or privacy. |
| Lockfile R1–23 (including R17a–h, R18a–i and R23a–k) | DIST-SR-07–12/15 retain candidate metadata trust and delivery-mode truth while withdrawing installer lockfile shapes, strict state parsing, recorded identities, all writing/serialization and managed-project success. State files are neither read nor used as admission markers. |
| Lockfile R24–33 | DIST-SR-09 retains candidate tree hashing: normalized bytes, canonical framing, ordering and regular-file membership. Recorded manifest/tree verification is no longer an installer operation; retain shared hashing only for independently needed callers. |
| Lockfile R34–53 including R45a–e | DIST-SR-10–15 preserve no-write reporting and filesystem conflict protection. State-field validation, recorded-basis drift checks, state mutation and managed replacement all retire. No state-presence guard or schema diagnosis remains; file conflicts and explicit force scope determine installation. |
| Lockfile R54–66 | DIST-SR-15/20: stable init output/exit classes, no obsolete pending-approval warning, package-local and installed execution, project-state presence does not affect eligibility and publication is independent. Default identical-install no-ops are superseded by conflict rejection; `--force` selects explicit replacement. |
| Adapter invocation R1/2/14, R28–30, R35–39, R43/46/47 | DIST-SR-03/04/15/18 and Skill: canonical ownership, deterministic supported output, Claude native skill invocation without command wrappers or unsmoked one-shot claims, target-specific guidance, no ordinary installed-agent requirement and useful diagnostics. OpenCode portions of shared documentation clauses are withdrawn. |
| Adapter invocation R3–13, R15–27, R31–34, R38, R40–42/R44/45/48 | OpenCode current generation/alias/support obligations are superseded by DIST-SR-02/04/17. Exact v0.1.1 smoke, release-note and patch-only decisions remain historical; they do not classify this breaking withdrawal as patch-level. Preserve historical metadata validators and evidence consumers where still exercised. |
| Archive-install R0–2, R9–13, R25/31, R42, R46–50 | Preserve v0.1.2 compatibility-window and v0.1.3 untracking/public-archive history under DIST-SR-06/17/20; no repeat of completed releases or retroactive invalidation. Named historical release and measurement evidence stays in place. |
| Archive-install R3–8, R14–24, R26–41 including R15a–d/R41a–g, R43–45/R51 | DIST-SR-03–08/17–19: authored-once, complete supported packages, tracked support only, temporary generation, metadata/checksums/source identity, exact current navigation and release composition. OpenCode population/alias requirements are explicitly superseded. Current package changes must use actual builders and validators. |
| Archive-install R52–57 | Retain applicable measurement authority at `specs/token-cost-measurement-baseline-and-proposal-scope-preservation.md` and `specs/release-token-friendliness-benchmark-for-skills.md`, with `single-authored-skill-source-generated-output.md` R61–66 for source selection. These v0.1.3 historical report obligations do not introduce a new report/benchmark gate for this initiative. |
| Archive-install R58–68 | DIST-SR-19/20 and Validation: no history rewrite, unrelated skill optimization or ledger move; preserved cross-source, metadata, archive and tracked-fragment protection. Concrete allocation belongs to Delivery; no new standalone test specification is created. |

All five sources' unnumbered goals, glossary, inputs/outputs, state/invariants, error/compatibility, privacy, UX/performance, examples, edge cases and acceptance lists follow the corresponding outcomes above. Preserve no-write/dry-run, wrong archive, missing metadata, traversal/symlink, size/count/hash, unknown package-field/value, unmanaged file conflicts, partial failure, proxy secrecy and unsupported-target behavior. Linear archive/tree work and no unrelated-root reads remain quality constraints. OpenCode positive installation/alias examples cease to specify current behavior and gain explicit rejection/preservation outcomes. Their Status, Readiness, Next and Follow-on sections and appended prospective stage-owned lifecycle notices are historical authoring evidence, not current workflow instructions. Workflow, Record Format and Review and Closeout retain current lifecycle/settlement policy; no retired stage-owned format is restored.

The matching test-spec requirement maps, cases and fixture/mocking sections retain proof intent through DIST-SR-07–19 and the scenarios below: use real temporary filesystem/archive/metadata paths, do not mock a validator into success, keep independent hash oracles and real packed install, and use safe external substitutes for automated network checks. OpenCode and managed-state/upgrade success cases become historical validation or current rejection/state-preservation coverage according to their actual consumer. Positive compatibility tests and tests exclusive to old state parsing, recorded-tree verification, writers, schema migration or automatic replacement retire with those capabilities. Proof that project state is untouched and does not affect destination decisions replaces schema/marker permutations; preserve shared candidate hashing, archive integrity, containment and package proof. Exact old milestone commands and manual publication schedules are not universal obligations; useful tests cannot be removed just because their test-spec file is retired.
### ADR and mixed-source dispositions

| File or exact section | Disposition at coordinated implementation |
| --- | --- |
| `docs/adr/ADR-20260424-generated-adapter-packages.md` | Remove. DIST-DEC-01/02 preserve authored-once, thin templates, deterministic manifest and generated-from-canonical rationale. Tracked public output was superseded by archive installation; separate local mirror preservation is explicitly superseded now. |
| `docs/adr/ADR-20260513-v0-1-3-adapter-release-archive-install-surface.md` | Remove. DIST-DEC-02 preserves compatibility-window reasoning, archive-only public installation, temporary validation, complete packages and immutable history; historical measurement/source decisions retain the named measurement owners. |
| `docs/adr/ADR-20260516-rigorloop-cli-lockfile.md` | Remove. DIST-DEC-03 and DIST-SR-09–15 preserve candidate integrity, delivery-mode truth and bounded replacement and filesystem safety. State input parsing, recorded identity verification, writing and serialization are expressly withdrawn. Old schema/command choices retain historical meaning. |
| `docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md` | Remove. DIST-DEC-03/04 preserve descriptors, Codex root, trusted local fallback, no npm-bundled ZIPs, safe diagnostics and no new Undici dispatcher. OpenCode support and all project-state interpretation/writing are superseded within the selected installer population. |
| `docs/adr/ADR-20260524-target-native-init-state-boundary.md` | Remove. DIST-DEC-03 preserves target-native syntax and real install proof motivated by the v0.2.0 dry-run gap. Explicit state creation and schema interpretation are now withdrawn; destination conflicts and `--force` replace prior state-marker rejection. No hidden `--adapter` alias or full internal-name rewrite returns. |
| Mixed architecture: `Level 2 White-Box: RigorLoop CLI Package` | Transfer installer descriptor/acquisition/proxy/extraction/manifest/lockfile/mutation bullets and their introductory install responsibility here; retain the command parsing/output-envelope bullet and broader executable delivery boundary with a Distribution reference. |
| Mixed architecture: `CLI target-native init, download, state, and release-smoke flow` | Replace the complete 17-step subsection with Distribution Runtime and Release references. Shared command envelope and npm package responsibility remain with their existing owners. |
| Mixed architecture: `Generated output` | Replace its two paragraphs with Distribution's source/package boundary and a concise explicit v0.1.2/v0.1.3 historical note; no active local-mirror regeneration obligation survives. |
| Mixed architecture: `Release and adapter evidence` | Replace the first paragraph's current package-evidence definition with Distribution/Release references. Retain the second and third paragraphs as named-version history. |
| Mixed architecture: `CLI package, project scaffold, and lockfile boundary` | Transfer paragraphs beginning “For `0.3.0`”, “The generated project manifest”, “`rigorloop.lock`”, “State write ordering”, “The CLI updates”, “Local archive mode” and “Network archive download”. Retain opening package boundary, the two `new-change` paragraphs and final named-version npm history, with current install/smoke references to Distribution/Release. |
| Mixed architecture navigation and Architecture Decisions | Replace current links/summaries for the five removed ADRs and five spec families with Distribution; preserve the complete historical Follow-on artifacts section and unrelated diagrams/prose. No diagram is selected for deletion solely because it mentions an adapter. |
| `specs/single-authored-skill-source-generated-output.md` | Retain mixed measurement and historical migration authority. At adoption, R2/10–17/68/71 no longer mandate a separate local mirror; DIST-SR-05/18/19 replace that capability/proof. R1/3–5/18–42/49–60/67/69/70/72/73 refer to Distribution for current delivery with Skill content ownership; R47's approved support-change exception applies. R6–9/43–48 historical sequence and R61–66 measurement/source semantics retain their original scope. |
| `specs/multi-agent-adapters-first-public-release.md`, `public-adapter-artifact-migration-examples-concise-skill-release.md`, their tests and CLI package/init spec/ADR | Retain named-release, measurement, packaging/envelope and other mixed remainders. Current distribution/installation references resolve through this map and the new-profile ownership notices; historical three-target release judgments stay unchanged. They cannot mandate current OpenCode output or the retired local mirror. |
| `specs/published-skill-first-repository-simplification.md` | Retain its bounded operational remainder, existing Test exception and Release R7/R8 transfer. Current supported-target/package claims consume Distribution; this does not retire shared check selection or grant a general test-retirement exception. |

The selected source removal is ten spec/test-spec files and five ADRs. No other source deletion is implied. Historical activation inventories and operational baseline paths remain unchanged where they name original subjects; current validation must distinguish those identities from live navigation. If an actual reader of a selected source needs its bytes rather than transferred meaning, reconcile that reader or retain the exact source with a named unresolved need before removal.

### Script retirement and consumer reconciliation

| Surface | Exact selected outcome and protection |
| --- | --- |
| `scripts/build-skills.py` | Remove the standalone mirror producer, including its default `.codex/skills` and arbitrary mirror-output modes. No forwarding wrapper. Current canonical validation plus supported adapter generation supply necessary production/proof. Preserve unknown-value rejection and raw mapped-resource integrity in their actual owners. |
| `scripts/test-build-skills.py` | Remove only after its useful independent byte oracle, complete resource inventory, missing/stale resource failures and malformed generated-skill detection are represented in `test-adapter-distribution.py`/`test-skill-validator.py` against retained production paths. Mirror-specific CLI/default-output assertions retire with the capability. No claim that existing tests already provide equivalent protection. |
| `scripts/adapter_templates/opencode/AGENTS.md`; current OpenCode alias rendering/descriptor branches | Remove template and current producer/installer branches together. Retain only explicitly bounded independently required historical release-evidence parsing, not reusable current OpenCode production. |
| `build-adapters.py`, `validate-adapters.py`, `adapter_distribution.py`, CLI acquisition/lockfile helpers | Retain shared acquisition, package metadata parsing and candidate hashing. Remove readers, schema branches, recorded-tree verification, writers and positive tests exclusive to withdrawn project-state compatibility, along with their callers. Inspect actual function consumers before deleting a whole helper module; this Design does not claim that caller audit has already run. Amend the current target domain and actual affected consumers. A thin entrypoint remains useful when it offers an independent supported operation; filename age is not a retirement reason. |
| CI, validation selectors and release verifier | Remove `skills.generation_regression`/`skills.drift` mirror commands where they exclusively invoke the retired scripts. Supported package checks inherit necessary protection; historical check records retain their IDs/results without a fake pass alias. Reconcile selectors and command-manifest tests, including deleted-path selection, so no stale executable call remains. |
| Current README/package README, install guide, contributor governance, workflows and canonical skill guidance | Teach only current supported targets, archive/install paths and retained builder usage. Remove active OpenCode invocation examples, local mirror regeneration, state-conflict reporting and `--write-state`/managed-upgrade instructions and two-independent-model guidance; preserve explicitly historical statements. Skill method and customer permissions remain unchanged. |
| Release profiles, schema/metadata readers, fixtures and candidate builders | Reconcile current target validation, archives, public smoke and metadata together under Release. Inspect history-aware checks separately; do not shrink all historical target lists globally. No hardcoded version switch or fabricated checksum is introduced. |
| System, Skill and Design | Apply reciprocal model amendments in this package. Design's TNI-DES references resolve through Distribution's explicit preservation and supersession map after adoption; Skill's content/resource invariants stay unchanged. |
| Follow-up register FU-013 | Route records the combined owner and completed scope only when implementation and Verify establish adoption. Do not close FU-012, FU-014 or other consolidation work. |

## Acceptance and boundaries

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | DIST-SR-03, DIST-SR-04 | Unknown targets, malformed manifests and missing required resources reject before a valid candidate is claimed. |
| State/lifecycle | DIST-SR-05, DIST-SR-06 | Generation uses isolated output and does not repair or overwrite active installations; unexecuted checks remain unclaimed. |
| Identity/authority | DIST-SR-06, DIST-SR-09 | Archive identity, metadata, regular-file membership, algorithm and counts agree; unknown algorithms reject. |
| Composition/path | DIST-SR-17, DIST-SR-18 | Actual generated archives and the packed CLI demonstrate compatible metadata and installation behavior on both targets. |
| Temporal/retry | DIST-SR-03, DIST-SR-04 | Identical inputs produce identical declared outputs; changed source, generator or package bytes require affected validation. |
| Failure/recovery | DIST-SR-05, DIST-SR-18 | A failed build/check reports actual partial output and preserves active installations; no fixture replaces the check being claimed. |
| Compatibility/migration | DIST-SR-19, DIST-SR-20 | Current support excludes retired targets while historical evidence remains unchanged; removal follows exact consumer/proof disposition. |
| External/environment | DIST-SR-06, DIST-SR-18 | Local candidate proof does not establish a public release; Release owns real public identity and fresh installation observations. |

## Architecture Decisions

| ID | Context and decision | Alternatives and consequences |
| --- | --- | --- |
| DIST-DEC-02 | Retire the local mirror producer and use the supported adapter pipeline; preserve authored-once and archive-only public delivery. | Hand-authored target copies and generated-from-generated packages create competing truth. Keeping both active runtime copies repeats the observed discovery ambiguity. Redirecting a build into `.agents/skills` would make builds mutate user installations. Historical compatibility-window and former mirror-preservation choices retain their original reasons but no current production mandate. |
| DIST-DEC-06 | Remove fifteen fully superseded design sources and two obsolete mirror script/test files only with complete meaning and protection transferred. | Automatic archive copies preserve duplicate reading burden; deleting every adapter-related file loses operational readers and named-release evidence. Retain mixed remainders explicitly and test actual consumer corrections. |

Splitting package production from installation preserves the shared representation once here and makes user filesystem mutation a CLI responsibility. It replaces the original combined-model choice, not its integrity, resource or recovery protections.

## Quality and risks

A package-only success is insufficient when the packed CLI consumes stale metadata or installed guidance refers to unsupported commands. Required proof observes generated resources, archive identities and real candidate CLI behavior. Build output must not overlap authored content or active skill roots. Detailed release and installation risks remain with their respective owners; a module filename alone never justifies helper deletion.

## Next artifacts

Independent Design Review of the exact split, retained source maps and both consumers; Delivery allocates implementation/source retirement and packed-product proof. The hierarchy does not claim runtime adoption or publication.
