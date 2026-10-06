# Packaging and distribution

MOD-019 composes IR-010's customer and maintainer outcomes across Package production (MOD-013), Skill installation (MOD-014) and Release coordination (MOD-015). It provides IF-006 to Command handling (MOD-010); its child MOD-014 performs installation. IF-005 is the internal artifact boundary. Child Functions, state and detailed contracts remain authoritative; the parent adds no duplicate Function, AR or state store.

Customers obtain a complete compatible CLI, portable skills and the selected browser capability through the declared distribution path. Maintainers qualify, authorize, publish and report an identifiable version. These outcomes require a continuous identity relationship, but production, qualification, destination permission, publication authority and public observations remain separate facts. The Requirements view is an optional System view; this Module's Process view explains the cooperation behind its requirements.

## Candidate identity and ownership

[Package production](modules/MOD-013-product-package-production/README.md) assembles the selected canonical inventory and declared transformations in isolated output. Its [Packaging contract](modules/MOD-013-product-package-production/packaging.md) owns archive layout, supported targets, metadata algorithms and actual packed-artifact checks. The candidate passes through [IF-005](../../interfaces/IF-005-verifiable-product-candidate-artifacts/interface.json) with source/version/profile, actual member inventory, exact bytes/digests, compatibility domains and attributable observations. Missing or failed observations cannot become generated passes.

[Release coordination](modules/MOD-015-product-release-coordination/README.md) consumes that candidate and owns qualification, immutable retention, authority association, external publication and closeout. [Release](modules/MOD-015-product-release-coordination/release.md) defines the dependency order: archive bytes, archive metadata/release index, packed CLI containing its required metadata, then the outer retained candidate identity. No artifact must contain its own final digest. Qualification checks the actual retained artifacts against the same prepared source, profile and configuration; rebuilding later does not inherit their qualification. Compatibility withdrawal requires the accepted version decision, while historical artifact and verifier meanings remain intact. The current supported skill population is Codex and Claude Code under Release's explicit support transition; older three-target declarations do not authorize current production or execution.

[Skill installation](modules/MOD-014-verified-skill-installation/README.md) owns acquisition and destination effects under [Installation](modules/MOD-014-verified-skill-installation/installation.md). It establishes archive trust through the CLI's bundled metadata/release-index contract, then validates the exact archive, extraction boundaries and staged inventory before destination mutation. A matching caller-supplied digest is not that trust root. MOD-010 preserves the result under [IF-006](../../interfaces/IF-006-verified-skill-installation-execution/interface.json), including preliminary dry-run, conflict, partial effects and bounded private-safe diagnostics. Ordinary force permits replacement of candidate units only; supported obsolete-unit retirement needs its separately selected bounded workflow contract. Installing files does not adopt operational workflow policy or migrate records.

The browser-enabled candidate adds the MOD-004 generator/template/data contract and declared profile/renderer resources, with MOD-010 public command integration, MOD-013 assembly and MOD-015 publication. AR-049, AR-050 and AR-051 divide those SR-088 responsibilities. The package must qualify its exact runtime/platform/resource/reader combination through an acquired candidate, independent project generation and copied offline reading. Its isolated tool-prefix update preserves customer definitions, output snapshots and unrelated files. A reference website is a separately identified generated artifact, not evidence that the reusable customer generator is complete. The proposed first browser platform and actual qualification limits remain in the child designs; repository Python checks do not qualify the customer product.

## Produce, qualify, publish and obtain

The sequence is the proposed parent composition. Candidate-local installation exercises MOD-014 during qualification; customer acquisition occurs after actual public availability. It does not require live publication to perform an engineering Design assessment.

<!-- architecture-diagram: deliver-identified-product -->

```d2
shape: sequence_diagram
maintainer: "Maintainer / authorized workflow"
release: "Release coordination\nMOD-015"
production: "Package production\nMOD-013 / IF-005"
installation: "Skill installation\nMOD-014 / IF-006"
public: "Declared public distribution"
customer: "Customer / Command handling\nMOD-010"
maintainer -> release: "Select reviewed intent, version, profile and exact start authority"
release -> release: "Prepare owned projections and cheap preflight; no public effects"
release -> production: "Build isolated candidate from exact prepared basis"
production -> production: "Verify canonical inventory, resources and actual artifact metadata"
production -> installation: "Exercise actual packed CLI and trusted archives in clean fixtures"
installation -> production: "Actual scoped outcomes and preservation observations"
production -> release: "Retained candidate identity and actual qualification observations"
release -> release: "Check all applicable duties and exact authority before each write"
release -> public: "Publish retained bytes in authorized boundary order"
public -> release: "Authoritative observations; unknown and partial remain explicit"
release -> public: "Fresh public acquisition and installation smoke"
public -> release: "Actual public identities and effects"
release -> maintainer: "Durable version-bound closeout or explicit failure/recovery scope"
customer -> public: "Obtain supported identified CLI through declared trust path"
public -> customer: "Selected package and trusted distribution integrity"
customer -> installation: "Explicit target, source, destination and replacement scope"
installation -> installation: "Verify candidate; preflight all units; recheck and change bounded scope"
installation -> customer: "Actual installed units or attributable partial/blocked outcome"
```

The diagram's publication arrow expands into MOD-015's existing tag, GitHub assets and npm sequence, with durable intent, authority/identity rechecks and observation at every boundary. IF-009 supplies applicable governed-action authority; IF-010 supplies evidence applicability. Neither replaces the other's judgment. A valid workflow start authorizes its exact routine scope; successful applicable checks continue automatically without a second routine human approval. Local preparation or pull-request checks confer no publication authority. SCN-069's separate publication decision follows preparation of an approved support withdrawal; it does not add a second approval after SCN-066's authorized start.

## Failure and recovery boundaries

An incomplete inventory, unsupported compatibility/algorithm, inconsistent metadata or failed qualification blocks dependent release or installation effects. Cheap preflight and dry-run retain their preliminary limits: neither downloads and verifies an install candidate nor proves public success. Changed source, configuration or candidate bytes require renewed qualification and the applicable new start authority, rather than reuse of a previous candidate's pass.

An installation conflict blocks all selected units before mutation. Integrity, path, link and race protections remain mandatory under force. Where mutation later fails, the result identifies actual completed units, failures and any detached original retained outside discovery roots; it does not promise whole-project rollback. A retry verifies and preflights the actual current state afresh. Shared parents and unrelated work stay outside replacement authority.

Release failures distinguish no write, uncertain write and confirmed partial publication. Inspect authoritative provider state before a retry; never overwrite a published identity or blindly repeat an uncertain write. Matching already-published boundaries remain intact. Recovery may continue a confirmed missing authorized boundary, repair closeout without republishing, or use separately authorized fix-forward/channel/deprecation action. A failed fresh public smoke or lost report remains an explicit incomplete outcome even when publication already happened. Preserve original candidate, effects and evidence throughout. Exceptions require the complete owner/risk/follow-up/deadline basis allowed by Release and cannot waive its nondeferable identity, privacy, recovery and public-fact obligations. Optional timing telemetry is diagnostic, not a substitute for or independent veto of valid release evidence.

## SR allocation and AR rationale

The following existing single-owner allocations fully locate the lower behavior for SR-060–073. Their retained detailed clauses already specify the boundary decisions, effects and adverse outcomes. Adding an AR that repeats each SR would not introduce a distinct architectural obligation. These SRs therefore require no additional AR for this composition. SR-088 already has AR-049–051 because its packaged browser behavior crosses assembly, command and release responsibilities. This rationale describes design allocation; it neither judges implementation nor supplies qualification evidence.

| SR | Function and accountable Module | Existing lower contract and reason no additional AR is needed |
| --- | --- | --- |
| SR-060 | FUNC-060; MOD-013 | Packaging DIST-SR-03/04/17/24 and the browser candidate contract own canonical inventory, raw resource parity, authorized transformations, current targets and complete browser resources. One producer is accountable for these candidate outputs. |
| SR-061 | FUNC-060; MOD-013 | Packaging DIST-SR-04/05/21/22 own deterministic isolated generation, explicit safe output and manifest-independent check behavior, without active-root cleanup. This is the producer's existing generation boundary. |
| SR-062 | FUNC-061; MOD-013 | Packaging DIST-SR-06/09 owns actual-byte metadata, hash/version semantics and rejection of unknown algorithms. IF-005 carries facts; Installation owns consumption of the separate trusted metadata basis. No second metadata authority is needed. |
| SR-063 | FUNC-062; MOD-013 | Packaging DIST-SR-18/23 owns actual tarball inventory and clean-consumer checks, including real packed installation, conflicts, force and preservation. Release consumes those exact observations and blocks failed qualification. |
| SR-064 | FUNC-063; MOD-014 | Installation DIST-SR-02/07/08 owns early target/flag rejection, bundled trust, archive verification before extraction and staged inventory. IF-006 exposes this existing acquisition responsibility. |
| SR-065 | FUNC-064; MOD-014 | Installation DIST-SR-10/12/13/14 and its workflow replacement design own all-unit conflict admission, scoped replacement/retirement, safe detach/publish, truthful partial effects and fresh retry. Parent visibility adds no mutation authority. |
| SR-066 | FUNC-065; MOD-014 | Installation DIST-SR-15/16 and IF-006 own preliminary nonmutating plans, actual result/exit distinctions, exact replacement-loss scope and bounded private-safe network diagnostics. Command presentation preserves those outcomes. |
| SR-067 | FUNC-066; MOD-015 | Release REL-SR-01/02/03/25 and its support transition own exact eligible identity/population, no-op/conflict, compatibility decisions and rejection of unsupported historical execution. These are one release admission responsibility. |
| SR-068 | FUNC-067/068; MOD-015 | Release REL-SR-04/05/06/07/19 owns deterministic profile preparation, preservation, effect-free preflight, explicit remote uncertainty and closed inputs/regions. Preparation remains distinct from publication. |
| SR-069 | FUNC-068/069; MOD-015 | Release REL-SR-08/09/12/16/24/25 owns exact prepared-candidate qualification and the ordered artifact seal, required checks and bounded exceptions. IF-005 supplies the actual producer observations without duplicating qualification ownership. |
| SR-070 | FUNC-069/070; MOD-015 | Release REL-SR-11/12/17/22/23 owns applicable exact-candidate authority, authentication/provenance, immutable writes and uncertain/duplicate inspection. IF-009/010 preserve the authority/evidence distinction. |
| SR-071 | FUNC-071; MOD-015 | Release REL-SR-10/13/14/18/24/26 owns observed public identities, fresh public installed smoke, version-bound durable reporting, reporting-only recovery and diagnostic timing. No parent success state is introduced. |
| SR-072 | FUNC-072; MOD-015 | Release REL-SR-15/16/23 owns failure classification, authoritative inspection, immutable history, authorized recovery and bounded deferrals. The existing publication-recovery view exposes the same decisions. |
| SR-073 | FUNC-073; MOD-015 | Release REL-SR-22/23/24 owns automatic coordination from one authorized start, failed-check blocking, exact retained basis, safe retries and precise intervention. This does not create a new approval service or independent parent coordinator. |

## Integrated acceptance intent and realization limits

IR-010's direct customer outcome requires faithful complete tools, admitted compatibility, trusted acquisition and bounded effects that preserve unrelated work. Its maintainer outcome requires an identifiable qualified candidate, separately applicable publication authority, actual public observations and recoverable truthful limitations. Feature–Function links and the confirmed SCN-060–069/087 situations supply stakeholder paths; child SR coverage alone is not a direct assessment of these outcomes.

Use the existing Packaging and Installation acceptance procedures and [Release test design](modules/MOD-015-product-release-coordination/test-design/test-design.md) at their actual boundaries. The composed candidate case REL-CI-013 must use real builders and a packed CLI, while REL-AR-034 observes initiation, checks, publication dispatch and reporting with controlled providers. Vary candidate identity across the producer/consumer boundary, interrupt installation after a completed unit, lose a publication response, revoke authority between writes and fail closeout after publication. Observe byte preservation, provider write histories and retained identity independently of reported success. Real release-scoped public acquisition and platform qualification remain separate from local fixtures; browser qualification additionally exercises the acquired generator and copied offline reader.

Existing child realization facets distinguish observed source mappings from proposed customer-browser and workflow-replacement behavior. Their default-output conformance gap, incomplete dependency mapping, missing deterministic assertions, platform qualification and live provider/configuration evidence remain explicit. This parent composition supplies no release, install, migration, completed implementation or verification claim. Independent review judgments and execution results belong in operational records, not this design.
