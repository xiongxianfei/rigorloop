# Installation Model Design

Model validation contract: model-document-v1

Parent model: [CLI](cli.md#product-responsibility-and-submodels).

Owning change: [three-model reconciliation](../../changes/2026-09-12-unified-validation-model/change.json).

## Introduction and Goals

Installation owns the observable `init codex` and `init claude` behavior: trusted package acquisition, destination preflight, explicit replacement, results and bounded recovery. Choosing this installation method requires the CLI; individual skill use does not. Package production and its shared metadata/hash representation belong to [Engineering Packaging](../engineering/packaging.md#stable-representations).

This child receives the installation portion of the former Distribution model without weakening integrity, default conflicts, explicit force scope or state preservation. The hierarchy changes ownership, not public permission. Original source maps and compatibility decisions remain attributable through [Packaging's retained source map](../engineering/packaging.md#source-displacement-and-preservation).

## Context and Scope

A user selects a supported target and trusted network or local archive source. The installer receives package-bundled metadata, the candidate archive and actual filesystem destinations. It returns planned, blocked, completed or partial operation results. Project-root state files are unrelated data: installation neither interprets them nor grants workflow adoption. The executable's record commands have a separate transaction and data contract.

## Requirements

| ID | Required behavior |
| --- | --- |
| DIST-SR-02 | Current target selection MUST accept exactly `codex` and `claude`. `init opencode`, its aliases, missing/unknown targets and removed `--adapter` syntax MUST reject before network acquisition, extraction, target or state writes. Diagnostics MUST identify supported target-native forms; a pinned old archive MUST NOT restore OpenCode installation in the current CLI. |
| DIST-SR-07 | Both network and `--from-archive` installation MUST verify package-bundled metadata against its release index before trusting archive identity. Metadata MUST identify target, compatible release, filename, exact official URL, SHA-256, available size, expected roots, tree algorithm, hashes, counts and passing validation. Missing compatible metadata blocks; supplied archive paths MUST NOT provide a substitute metadata trust root. |
| DIST-SR-08 | Acquisition MUST use only the selected trusted official URL or the explicitly supplied local archive. Wrong filename, target, release, hash or declared size MUST fail before extraction. Extraction MUST reject absolute, empty, parent-traversing, drive-letter and unsupported symlink entries and unexpected out-of-root files; only the declared package support entrypoint may exist outside install roots and it MUST NOT be installed into the project; installed candidate hashes and file counts MUST match trusted metadata before success. Unrelated unmanaged files remain untouched and are excluded from candidate-only verification. Candidate hashing does not read or validate any recorded managed-tree basis. |
| DIST-SR-10 | After acquiring, verifying and staging the selected package, installation MUST preflight every destination unit before changing installed files. Without `--force`, any existing destination skill directory or declared standalone file MUST be reported as a conflict, including empty directories and byte-identical content. Report all discovered conflicts and stop without installing any units, even when other destinations are absent. |
| DIST-SR-11 | The CLI MUST reject `--write-state` before acquisition, extraction or filesystem mutation, including dry-run, pinned-release and local-archive forms. Installation MUST NOT create, update, migrate or delete managed state. Diagnostics MUST explain that only install-only operation remains; no hidden alias or upgrade flag may restore state writing. |
| DIST-SR-12 | Conflict scope MUST be each candidate skill directory and any explicitly declared standalone install file, not the shared `.agents/skills` or `.claude/skills` parent. Existing project-root `rigorloop.yaml` and `rigorloop.lock` MUST remain untouched and MUST NOT be read, validated or checked as installation admission markers. Their presence, absence, contents or version MUST NOT select behavior. Unrelated skills and files remain outside replacement scope. |
| DIST-SR-13 | `--force` MUST explicitly permit replacement only of conflicting destination units from the verified candidate. Replace each conflicting skill directory completely, including obsolete files, rather than overlaying its contents; replace a conflicting standalone file at its exact path. An existing regular file or directory at a selected unit path is replaceable, but shared parents and unrelated units MUST NOT be replaced. Help and results MUST name the replacement scope and warn that local changes inside replaced skill directories will be lost. |
| DIST-SR-14 | Both modes MUST retain archive integrity, destination containment and symlink protections. Unsafe or inaccessible destinations, symlinked ancestors/units or symlinks within a replacement tree MUST block; `--force` MUST NOT bypass these checks. Preflight the whole candidate and stage verified bytes before mutations. Recheck the selected filesystem basis before replacement, stop on intervening changes, and use exclusive creation for absent destinations. No automatic managed upgrade, state migration, retired-skill cleanup or full-project replacement is authorized. |
| DIST-SR-15 | Dry-run MUST report planned destination checks, potential conflicts and explicit `--force` replacements without downloading, extracting or changing project files. Distinguish preliminary checks based on bundled inventory from complete archive-verified conflict preflight; unperformed checks MUST remain visible. Real installation MUST report its full conflict set after package verification and before installed-file mutation. Human and JSON results MUST preserve applicable envelopes/exit classes, distinguish blocked/planned/actual replacements, and never claim state writes. |
| DIST-SR-16 | Network/proxy diagnostics MUST retain the safe fields and closed values below, with no extra network probes or programmatic proxy dispatcher. Local archive fallback MUST retain all verification. Secrets, credentials, raw proxy values, private hosts, usernames, request headers and machine-local archive paths MUST NOT enter durable state, generated packages or diagnostics. |

## Architecture and interfaces

Reuse the existing CLI installer dispatch, adapter descriptors and archive/acquisition helpers. Shared code must not introduce a record-store eligibility or managed-upgrade dependency. The [Packaging representation](../engineering/packaging.md#stable-representations) owns target roots, archive naming, trusted metadata, hashing; this consumer enforces the selected trusted candidate and rejects unknown values. Packaging builds the metadata; a local archive does not provide a substitute trust root.

### Diagnostics

| Surface | Retained representation and constraints |
| --- | --- |
| Failure classes | Preserve successful exit 0; unexpected failure 1; unsupported target/installation context or recoverable missing metadata/network 2; archive/metadata/integrity verification 3; independently applicable configuration errors 4; mutation/file-type conflicts 5. Preserve current stable codes where applicable; retired OpenCode uses the current unsupported-target class with explicit retirement guidance, not a new successful no-op. Destination conflicts return blocked/exit 5 with their paths and `--force` guidance where replacement is safe. Unsafe-path errors remain blocking with `--force`. State files produce no installer diagnostic because they are not inspected. |
| Proxy diagnostics | Variable names only from `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `http_proxy`, `https_proxy`, `no_proxy`; `node_env_proxy_status` is `enabled`, `disabled`, `unsupported`, `unknown`; `download_failure_class` is `dns`, `tls`, `timeout`, `http-status`, `proxy`, `network`, `unknown`. Include selected target/release, trusted public `archive_url` and verified local-archive fallback. Uncertain runtime capability is `unknown`; no claimed support based on guessing. |

### Destination conflicts and explicit replacement

An installation unit is one complete skill directory from the verified candidate, such as `.agents/skills/proposal`, or an explicitly declared standalone install file. Shared target parents may already contain other skills; their existence alone is not a conflict. Package support entrypoints outside installation roots remain uninstalled under DIST-SR-08. Project-root state files are unrelated content and receive no special inspection, even when they are malformed, unreadable or symlinks.

| Request and starting condition | Required result |
| --- | --- |
| All candidate destination units are absent | Install after package verification and complete destination safety preflight. |
| Any candidate skill directory/file exists, including empty or byte-identical content; no `--force` | List all discovered conflicts after archive verification and stop before modifying any installed unit. |
| Some units conflict and others are absent; no `--force` | Stop the entire installation; do not install the non-conflicting subset. |
| `--force` with safe existing destination units | Report their replacement, replace each conflicting skill directory/file completely from staged candidate bytes, and install absent units. Obsolete content inside replaced directories is removed. |
| A destination or its ancestor is a symlink, a replacement tree contains symlinks, or safe containment/access cannot be established | Block in both modes; do not follow symlinks or treat uncertainty as absence. |
| Unrelated skills, `.opencode` files, or project-root state paths exist | Preserve them; their presence does not constitute a destination conflict. Do not open or validate state files. |
| Any OpenCode install or `--write-state` request, including pinned/local/dry-run forms | Reject before acquisition and all writes; `--force` does not restore removed support. |
| Existing `.codex/skills` mirror | Build/check ignores it and never repairs it. Force installation affects only the selected target's candidate units, never that unrelated mirror. |

For example, a default install whose verified candidate conflicts with two installed skills reports:

```text
Installation stopped: destination skills already exist:
  .agents/skills/proposal/
  .agents/skills/design/

Run again with --force to replace these skills.
Local changes inside replaced directories will be lost.
```

The `--force` help text is: “Replace existing destination skills. Local changes within replaced skill directories will be lost.” The option applies consistently to both targets and network/local archive acquisition. An agent still needs applicable execution authority to invoke it; defining the option does not authorize replacement of this repository's installed skills.

Candidate `spec`/`architecture` skills and aliases remain invalid. Installed retired authoring entries retain the Design-owned inventory guard and exact-path diagnostic; `--force` does not delete noncandidate retired entries or perform a workflow-to-route migration. TNI-DES-01/06 inventory/preservation intent survives with this explicit transition; TNI-DES-02–05 managed-basis, state-writing and transaction obligations remain withdrawn. The earlier unconditional no-force, identical-no-op and state-marker rejection choices are expressly superseded by DIST-SR-10–15; their historical judgments keep their original meaning.

### Partial failure and retry

Use a per-unit detach-and-publish sequence, reusing the filesystem primitives in `managed-authoring-replacement.js` without its lockfile eligibility, state publication, recovery schema, scanner or rollback controller:

1. Verify and stage the complete candidate. Preflight every unit and capture an in-memory snapshot of its regular-file bytes, types and directory membership, plus the device/inode identities of the project root and destination ancestors. Reject symlinks or inaccessible entries. This is a snapshot of actual destinations, not a stored managed-tree basis.
2. Before detachment, allocate a private retention directory such as `<project>/.rigorloop-install-retained-<random>` outside `.agents/skills`, `.claude/skills`, `.codex/skills`, `.opencode` and every other explicitly configured skill discovery root. If safe non-discovery placement cannot be established, stop force replacement. Require the retention directory and selected unit to be on the same filesystem, and establish anchored access to both parents. Use descriptor-relative rename or an equivalent operation that keeps both inspected parent objects fixed; if the platform cannot supply this capability, reject force before moving existing content. The existing single-parent helper is a useful primitive, not proof of this two-parent extension. Then recheck the unit snapshot and ancestor identities. Pin the verified destination parent using the existing synchronous parent-as-working-directory pattern and perform basename-only operations against that pinned parent. Check that the pinned inode matches the inspected parent; never reopen a mutable ancestor path for deletion, publication or chmod.
3. For a force conflict, move the existing unit directly into a fresh unpredictable name in the anchored retention directory. Never detach to a sibling beneath a runtime skill root, even temporarily. The move detaches the old object without recursively deleting a public path. Inspect the detached object immediately against the captured snapshot. If a writer won the source race or any basis changed, retain that object, stop and report its location; do not publish over a new public destination or roll back over an independent change.
4. Publish the staged candidate using no-clobber operations: exclusive directory creation and atomic same-filesystem hard-link publication for staged regular files. Pin and check each parent before child operations. A destination that appears after preflight causes a conflict even under force; do not detach it as a second, newly authorized replacement. Recheck expected filesystem contents and ancestor identities between unit operations and verify candidate hashes/counts before reporting success. If the platform/filesystem cannot provide the required primitives, stop safely rather than fall back to overwriting rename/copy.
5. Retain detached originals in that outside-discovery directory after both success and failure. An already-open writer may continue writing an old inode after the last check; retaining the original preserves those bytes without claiming that external writers were excluded. Runtime exclusion comes from placement outside discovery roots, not hidden-name filtering or CLI/package inventory. Normal agent discovery must not encounter a retained `SKILL.md`; guidance identifies retained paths as originals, never another active installation. The report names each original destination and retained path; operator inspection and explicit cleanup are separate from installation. Do not automatically delete, parse or restore retained originals on retry.

The installer does not promise to prevent all concurrent writes. It stops on detected changes, preserves detached originals and uses no-clobber publication so a competing destination is not overwritten. A changed staged file, detached original or installed candidate observed during verification is a failure, not successful installation. A late write through an old open handle remains in the retained original; success describes the verified active candidate at the observation point, not perpetual filesystem immutability.

A failure stops further writes and reports completed, failed and untouched units, including detached or partial destinations and retained-original locations. Unrelated content and project state remain untouched; there is no filesystem-wide rollback or automatic recovery. Retry repeats full acquisition/verification and preflight: completed or partial public units conflict by default, and the caller must explicitly supply `--force` again for replacement. Private retained names supply no eligibility or state-repair authority. This bounded retention is filesystem preservation, not a managed-state format or recovery service.

## Runtime and deployment

Parse the supported target and flags before network, extraction or writes. Dry-run reports its preliminary scope without acquisition or mutation. Real installation validates trusted metadata and archive identity, safely stages the candidate, preflights every destination and then performs the bounded writes. Default conflicts stop all writes; explicit `--force` does not bypass containment, symlink, stale-basis or preservation checks. Failure reports actual completed, detached, partial and untouched units rather than claiming rollback or success.

The packed CLI is the observation boundary, not just helper calls. Exercise both targets and both network/local acquisition with safe fixtures. Candidate metadata, actual archive bytes and filesystem results must agree. Public endpoint observations remain Release-owned. There is no automatic cleanup of retired noncandidate skills or unrelated state.

## Acceptance and boundaries

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | DIST-SR-02, DIST-SR-07 | Unknown/retired targets and removed syntax reject before acquisition; local archives cannot substitute untrusted metadata. |
| State/lifecycle | DIST-SR-10, DIST-SR-11 | Any candidate-unit conflict stops default installation, including empty or identical content, without state reads or partial subset writes. |
| Identity/authority | DIST-SR-07, DIST-SR-13 | Only explicitly selected force replacement of candidate units is permitted; package validity does not supply external permission. |
| Composition/path | DIST-SR-08, DIST-SR-12 | Actual packed-CLI installation preserves unrelated skills and state while enforcing the Packaging archive/root contract. |
| Temporal/retry | DIST-SR-13, DIST-SR-14 | Races and repeated installs recheck actual destinations; late open-handle writes remain in retained originals and retries require explicit force where applicable. |
| Failure/recovery | DIST-SR-08, DIST-SR-14, DIST-SR-15 | Unsafe extraction, symlinks, inaccessible destinations or unavailable anchored replacement fail safely; partial outcomes and retained originals are reported truthfully. |
| Compatibility/migration | DIST-SR-02, DIST-SR-11, DIST-SR-12 | No pinned or local form restores OpenCode, state writing or managed upgrades. Historical facts and unrelated retired-target content remain unchanged. |
| External/environment | DIST-SR-07, DIST-SR-15, DIST-SR-16 | Dry-run distinguishes unperformed checks; network/proxy diagnostics expose no secrets and local fallback retains all integrity checks. |

## Architecture Decisions

| ID | Context and decision | Alternatives and consequences |
| --- | --- | --- |
| DIST-DEC-03 | Default installation rejects every existing candidate unit; explicit `--force` completely replaces conflicting skill directories/files. Ignore project state and preserve unrelated content. | Identical-file no-ops hide the existence-based boundary; overlays leave obsolete files; state parsing or marker rejection adds an unrelated admission rule. Force is explicit filesystem replacement, not a managed upgrade or safety bypass. Packed archive/install proof remains required. |
| DIST-DEC-04 | Retain trusted package metadata for both network and local acquisition, descriptors, existing roots and safe Node proxy diagnostics. | Bundled ZIPs duplicate release artifacts; user metadata weakens trust; moving Codex roots adds migration without value; a new proxy dispatcher adds credential handling. Local fallback changes delivery, not the trust root. |
| DIST-DEC-05 | Withdraw OpenCode completely from current operations; retain only independently required historical release-evidence reading. | Continuing pinned/skills-only installation would preserve hidden support; treating old state as disposable risks data loss; project state stays untouched and has no admission role. Earlier read-only compatibility and marker-rejection designs retain their original judgments but are superseded by explicit destination-based installation. |

## Quality and risks

The former combined ownership decision is replaced by an explicit package-producer/installer-consumer interface. All retained replacement steps and negative outcomes remain obligations. Force replacement can remove local changes inside selected units, and its help/results must describe that scope. Retained originals are outside discovery roots; they are not a new eligibility ledger or automatic recovery service.

## Source transfer and next artifacts

The [reconciliation evidence (`design-preservation-delta`)](../../changes/2026-09-12-unified-validation-model/evidence.json) assigns DIST-SR-02/07/08/10–16 and DIST-DEC-03–05 here. Shared package representation and integrated proof remain Packaging-owned; Release retains publication. Independent Design Review assesses this split and exact consumers before Delivery allocates implementation and verification.
