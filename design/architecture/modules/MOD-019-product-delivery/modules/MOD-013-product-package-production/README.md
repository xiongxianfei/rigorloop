# Package production: workflow replacement identity

This proposed extension realizes AR-041 and supplies [Installation's bounded replacement contract](../MOD-014-verified-skill-installation/README.md). Existing [Packaging](packaging.md) retains archive acquisition, target descriptors, tree-hash algorithms, normalization and qualification ownership. No current package is relabeled or claimed qualified by this design.

## Exact package member

Generate a UTF-8 JSON support member `rigorloop-workflow.json` at the archive root. Its closed shape is:

```json
{
  "schema_version": 1,
  "workflow_contract": "requirement-first-v1",
  "record_contract": "rigorloop-records-v4",
  "recording_interface": "targeted-recording-v2",
  "required_skills": ["requirement-analysis", "requirement-review", "system-design", "architecture-design", "route", "design-review", "plan", "delivery-review", "implement", "code-review", "verify"],
  "retired_skills": ["proposal", "proposal-review", "design"]
}
```

For this profile every value and array membership/order above is exact; missing, extra, duplicate or unknown entries reject. It is a replacement contract, not an extensible arbitrary path list or project profile system. Optional support skills remain ordinary verified candidate members; they do not belong in required_skills. The two target roots derive from the trusted selected target descriptor, never from strings in this member.

The member is included in the archive byte checksum and complete archive inventory, but is not installed as project policy or included in the skill-root tree hash. Root tree counts remain scoped to their declared roots; archive member counts include the support member. Existing trusted metadata/versioning and v1/v2 tree-hash compatibility remain unchanged. A local archive cannot provide its own substitute checksum trust root.

Publish this replacement only under a new release identity with matching CLI-bundled trusted metadata; never replace an earlier release's archive or metadata at the same identity. The current installer checks bundled metadata against its own package release and the exact archive checksum. Therefore an old binary retains its old trusted candidate and cannot accept the new archive merely because it ignores the new support member. Qualification must exercise that old-binary/new-candidate rejection with the actual prior released binary, as well as new-binary/profile validation. A failed compatibility check cannot be bypassed with force or local-archive mode.

## Production and consumer parity

Canonical methods remain in `rem/`; authored entrypoints/resources remain in `skills/`. Generate the descriptor from the same fixed supported-contract constants used by package validation and installation, without independent hand-maintained target copies. Include the needed versioned method resources through the packaging boundary. Validate the actual built archive: every required entrypoint exists under the selected target root, obsolete entries/aliases are absent, and each selected conditional resource resolves within the candidate. Verify remaining workflow consumers use the same stage and review meanings; presence of four new directories alone is insufficient.

Release qualifies the exact resulting candidate and CLI capability report together. This descriptor expresses required compatibility; it does not prove the installed CLI supplies it. Guidance must inspect actual capability availability and remain portable or explicitly unavailable for governed recording when no supported v4 backend exists. Installation validates identity and applies authorized units; Governance decides adoption against current policy, actual guidance and operational compatibility.

## Verification intent

Use real generated archives, independent archive/member counts and hashes, and installed smoke under both supported targets. Negative cases include each new unknown closed-vocabulary value, missing descriptor, duplicate/extra list entries, a retired skill alias, a missing transitive conditional reference, mismatched CLI capability identity and an unchanged source tree paired with stale generated output. Compare the actual archive and installed candidate, not two values produced by the same generation helper. These are new proof obligations; existing Packaging results do not automatically cover them.

The archive checksum binds the new member without changing the established trusted metadata format or skill-root hash preimage. This avoids a second trust mechanism and preserves unrelated public packaging guarantees. No publication, install, workflow adoption or SQLite qualification is inferred from generation.


## Browser candidate contract

[Views and traceability’s Build and resources design](../../../MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#build-and-resources) supplies the browser’s required software/resource relationships. Package production consumes that definition and owns assembly, the exact candidate inventory and its qualification. Customer snapshot generation remains MOD-004 runtime behavior; a generated snapshot does not establish a qualified distributable candidate.

SR-060 and AR-049 extend the CLI candidate with the shared browser generator, reusable browser template, browser-data contract definitions, profile schemas/interpretation resources, declared renderer binaries and licenses. FUNC-083 qualifies the actual packaged artifact. Browser support is selected explicitly in candidate metadata with `browser-v1`, exact profile IDs/resource digests, runtime/platform tuples, renderer version/digest and tested reader configurations. Missing inventory or unknown compatibility rejects qualification; a sample site is a distinct artifact with its own source/generator identity.

For the target browser subtree, package production assembles authored `packages/rigorloop/browser/` generator/template/contract sources and selected profile/renderer resources into `dist/browser/`. Preserve the supported CLI entry and package the complete internal data-contract resources with the template and generator. This does not reclassify other existing `dist/` contents. Candidate qualification checks their compatibility against the MOD-004-owned [browser-data contract](../../../MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#browser-data-contract) and exercises a project website with project-specific data; it must not rely on RigorLoop-specific identities embedded in the template. The generated website contains platform and project data, not a reader-side generator dependency. Its assembly is MOD-004 product behavior, separate from production of this CLI candidate.

The first target is Linux x86-64/Node 24 with a bundled Rust engine and D2 0.9.0; exact runtime patch, binary and reader versions are frozen for each candidate. The engine build target is `x86_64-unknown-linux-musl`; inspect actual binary dependencies and qualify the combined Node/engine/D2 runtime and filesystem behavior. This does not establish support for arbitrary Linux installations. The candidate must require neither Python nor Rust/Cargo, a customer-side product build or undeclared resource acquisition. Existing nonbrowser CLI behavior and skill-archive metadata retain their contracts; a browser-incompatible environment cannot silently enable a fallback generation path. No release availability is claimed by this target matrix.

Compile the authored Rust crate with a pinned stable toolchain and committed Cargo lockfile during product build, recording source, toolchain, target, dependency/license inventory and executable digest. Assemble that executable under generated `dist/browser/generator/` with the existing Node adapter, matched `browser-engine-v1` protocol, profile resources, template/data compatibility identity and D2 binary/licenses. The CLI selects the exact installed executable through the candidate manifest, not PATH or customer configuration. Qualify protocol/resource mismatch rejection before writes, executable permissions, clean-prefix acquisition and cancellation/response-loss recovery in addition to ordinary generation. The Node adapter and engine ship as one matched candidate; no independent engine download, native Node addon or install-time compilation is introduced. Scope browser platform admission to browser operations rather than narrowing the whole package's existing CLI compatibility.

Supported acquisition/update uses the existing package-manager trust/integrity path into an explicit isolated tool prefix outside customer model and generated-output roots. The candidate declares no install hooks and never rewrites customer snapshots as an update side effect. Test initial acquisition, compatible update and rejected/corrupt/incomplete candidate outcomes in clean prefixes, retaining actual effects and proving unchanged model/output and unrelated files. The public artifact's integrity must be independently obtained through the declared trusted distribution path, not trusted because a caller provided a matching hash.

RigorLoop's own repository is the first supported project. Qualify an actual installed candidate through IF-012's public command boundary using an explicitly selected immutable snapshot of this model; the repository wrapper must invoke that candidate rather than import a separate source-tree generator. Keep a minimal independent model as a supplementary check for accidental project assumptions. Check generated content, optional missing views, source attribution, safe output failure/recovery, bundled binary/resource completeness and copied offline reading without the checkout, network or generator. Record the exact candidate and configurations; untested platforms remain unsupported. MOD-015 receives those observations through IF-005 and separately applies release authority and observes publication. No customer-package support claim follows from the existing repository Python tests.

The first candidate supports one fixed engineering-model contract, one generator and its matched static reader. Internal data-contract definitions may be implemented with the producer/reader; they are not a separately distributed universal schema or template SDK. Generated reference documentation uses the same supported path as customer websites. The [first-project adoption design](../../../MOD-016-engineering-model-management/modules/MOD-004-engineering-context-and-traceability/README.md#rigorloop-as-the-first-supported-project) owns the current gap assessment and cutover conditions. This narrowing does not relax the no-customer-Python, complete-resource, input identity or safe-publication obligations.

## Supporting contracts

These documents retain detailed clauses and proof under this Module; they are not additional REM entities.

- [Packaging Model Design](packaging.md)
