---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "design-review",
  "target": "design",
  "reviewer": {
    "id": "record-format-rereview",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "design"
    },
    {
      "id": "user",
      "role": "human"
    }
  ],
  "independence_basis": "The separately delegated record-format-rereview agent independently reread the three complete current models after the ownership and EntryRef changes, checked the retained examples and v1 membership implementation, and authored none of these changes. The user and codex-root remain the contributors. Prior approval was stale; this is a new independent assessment of the exact current subjects, not approval restored by hashes alone.",
  "subjects": [
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:a3727f571eec0f9ae34bfdda31f9f7711e3903abdabd31e28903b8c3b69b2251"
    },
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:951c0f427e118914d70c1f326a02ae01efab47107a1cca897211b980b9d8d22c"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:6ddfcd350212437ddf2feaade14818fd66f9a04b8a00ccb01c5fb13291879eeb"
    },
    {
      "path": "docs/design/cli/examples/observation-freshness/expected.json",
      "identity": "sha256:1d22534396a88cb3f3edb8d19be15cc37b8fe77b458ac2344e9627816094cca8"
    },
    {
      "path": "docs/design/cli/examples/observation-freshness/scan-b.json",
      "identity": "sha256:4fde512f9fd9c9b25502d1e983bb9a22382812ac726af6af32e040f7c3ff8222"
    },
    {
      "path": "docs/design/cli/examples/observation-freshness/scan-c.json",
      "identity": "sha256:d271716355c2d96bd1110c24f37e01de1bfb2a53d011a2f2a884bbebda2b9593"
    },
    {
      "path": "docs/design/cli/examples/work-set/request.json",
      "identity": "sha256:f35f7b4c6fc54f3bbe5164b1d75ef2b786f7898a8d64199f0d15dab2c2b3018e"
    },
    {
      "path": "docs/design/cli/examples/work-set/response.json",
      "identity": "sha256:75c8d51fdb5756ad71879f183ca6c08b807b7eba3f8e4648e0adbb682a77ab96"
    },
    {
      "path": "docs/design/record-format/examples/finding-reassessment/after.json",
      "identity": "sha256:c13ffa7fe8d4189f2f30f7bb5c603c50c0e8d4d783dc394013d7db81883f32e0"
    },
    {
      "path": "docs/design/record-format/examples/finding-reassessment/before.json",
      "identity": "sha256:df39c9d8cb532e8fa48f3590e3558a4308bdfd815aab09b68866247be35d2f1d"
    },
    {
      "path": "docs/design/record-format/examples/incomplete-review.json",
      "identity": "sha256:2a3d109d1be88ae0fa2b72fa8e14b34b781fb7e65ac07b93a7b7baa4eb6ea735"
    },
    {
      "path": "docs/design/record-format/examples/minimal-change.json",
      "identity": "sha256:523ee35620d9deb9b393ecb59c414bd25e240be81a28dc76f347d412e0201cb6"
    },
    {
      "path": "docs/design/workflow/examples/correction-cycle.mmd",
      "identity": "sha256:2a42da7884e3aeff0020f814fcb36b98f88ad80fc385a8f52a2b5ddaf4aa0ca9"
    },
    {
      "path": "packages/rigorloop/dist/lib/record-store-contract.js",
      "identity": "sha256:72a9813be174d2fdeb9dd8c552a5c23fda916befa8d2338107b130ea5f90f458"
    }
  ],
  "judgment": "approved",
  "findings": [
    {
      "id": "rf-dr-001",
      "reporter": {
        "id": "record-format-rereview",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "design"
      },
      "subjects": [
        {
          "path": "docs/design/cli.md",
          "identity": "sha256:938c9aeea27174f6ba7e86e839365b84c68a9765c84455dd648d435a9b461761"
        }
      ],
      "evidence": "CLI model lines 258 and 274-278 define observation_identity as the hash of {schema_version: 1, revision, observations}, with diagnostics containing code, safe message and locations but no required observed external subject identity. Line 278 nevertheless promises conflict when an observed external subject changes. A retained subject identity A can observe B on the first scan and C on the next, both different from A. The registered revision and the subject-drift code, location and fixed safe message can all remain identical, so the explicitly defined digest input remains identical. This is a missing identity input, not a hash collision or an external edit during publication.",
      "required_outcome": "Make the exact observation digest input and continuation contract agree about changes to the observed external basis, including B-to-C drift that preserves the diagnostic category, location and message. Preserve bounded storage receipts and safe diagnostics; detail retrieval must not become a write prerequisite. Bind a deterministic observed path/identity basis, including absence, or define an equivalent identity-bearing diagnostic representation and acceptance case. Any deliberate narrowing to diagnostic-content stability must be an explicit reconciled Design decision and independently rereviewed.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "record-format-rereview",
          "role": "review"
        },
        "rationale": "Independently reassessed CLI-SR-20 and the complete three-model package. The internal preimage now explicitly includes schema_version 2, revision, observed_subjects and observations. Every schema-defined Subject path is observed once, deduplicated and sorted, with exact current digest or confirmed absence; candidate/current scans share scope and request-only reads remain separate. Both published example digests were independently recomputed: B and C produce distinct identities despite identical record revision and diagnostics. The stated B-to-C conflict guarantee is now supported without expanding the bounded receipt. The original evidence, subjects and required outcome remain unchanged; no runtime implementation claim is made.",
        "evidence_refs": []
      }
    }
  ]
}
---
# Design review of the Workflow, CLI and Record Format models

## Result

- Skill: design-review
- Review status: approved
- Package members: workflow = docs/design/workflow/workflow.md; cli = docs/design/cli/cli.md; record-format = docs/design/record-format/record-format.md. Exact model identities are in metadata. The ten relied-on examples and the bounded v1 compatibility-inspection subject are also identified there; the latter is evidence, not a code approval.
- Upstream review ID: proposal-review-r1, registered in this change; its approved proposal subject remains unchanged.
- Review ID: design-review, independent rereview of the ownership and EntryRef refinement recorded in commit 59e5152c.
- Material findings: none open; the previously resolved rf-dr-001 remains retained without changes to its evidence, original subjects or disposition.
- Correction targets: none required.
- Recording status: supported actor-owned review with explicit current applicability.
- Settlement status: no historical lifecycle settlement command or transition is claimed; this record owns the explicit exact-package Design judgment.
- Immediate next stage: isolated stop; no routing decision was made.
- Claim limitations: Design approval only. No implementation correctness, v2 activation, final Verify completion, branch readiness or release approval. Delivery must allocate and prove the accepted requirements.

## Finding RF-DR-001: original basis and current disposition

Stable stored ID: rf-dr-001. Original severity: medium. Scope: artifact-local, cli. Correction owner: codex-root, Design authoring. Reporter and disposition owner: record-format-rereview. The finding's original exact subject identity remains in its structured subjects and is not retargeted to the relocated model.

Original evidence: CLI model lines 258 and 274-278 define observation_identity as the hash of {schema_version: 1, revision, observations}, with diagnostics containing code, safe message and locations but no required observed external subject identity. Line 278 nevertheless promises conflict when an observed external subject changes. A retained subject identity A can observe B on the first scan and C on the next, both different from A. The registered revision and the subject-drift code, location and fixed safe message can all remain identical, so the explicitly defined digest input remains identical. This is a missing identity input, not a hash collision or an external edit during publication.

Original required outcome: Make the exact observation digest input and continuation contract agree about changes to the observed external basis, including B-to-C drift that preserves the diagnostic category, location and message. Preserve bounded storage receipts and safe diagnostics; detail retrieval must not become a write prerequisite. Bind a deterministic observed path/identity basis, including absence, or define an equivalent identity-bearing diagnostic representation and acceptance case. Any deliberate narrowing to diagnostic-content stability must be an explicit reconciled Design decision and independently rereviewed.

Original rationale: a stable diagnostic projection could hide an already-drifted subject changing again. The promised expected-observations check needed the observed identity as an input, rather than assuming that a different file necessarily produces a different message. The original supporting Design judgment was changes-requested because this gap made diagnostic continuation weaker than its stated guarantee.

Current disposition: resolved. Independently reassessed CLI-SR-20 and the complete three-model package. The internal preimage now explicitly includes schema_version 2, revision, observed_subjects and observations. Every schema-defined Subject path is observed once, deduplicated and sorted, with exact current digest or confirmed absence; candidate/current scans share scope and request-only reads remain separate. Both published example digests were independently recomputed: B and C produce distinct identities despite identical record revision and diagnostics. The stated B-to-C conflict guarantee is now supported without expanding the bounded receipt. The original evidence, subjects and required outcome remain unchanged; no runtime implementation claim is made.

The correction chooses stronger identity binding rather than narrowing the promised freshness guarantee. It specifies all Subject fields, including origin and supporting-judgment subjects, independent of applicability and selected page. Schema-only traversal excludes narrative and EntryRef strings. Unsafe/unreadable subjects cannot masquerade as absence. Stored subject references do not acquire the unrelated 256 request-read limit. The deterministic preimage uses recursively ordered object keys, defined array ordering and no final LF. Candidate/current reads reconstruct the same subject scope, with each observed path used consistently within the scan. The existing external-edit limit and reverted-between-scans limit remain explicit.

The B/C examples keep both registered revision and diagnostics identical. Independent compact UTF-8 encoding and SHA-256 recomputation matched the expected identities, and those identities differ. Temporal acceptance now includes this case, disappearance/reappearance, formerly matching subjects and duplicate references. Counts and one digest remain the receipt's entire diagnostic payload; detail volume still cannot block structurally valid correction recording.

## Current package assessment

The complete current package is coherent. Workflow identifies semantic responsibility; Record Format owns stored schema, reference interpretation and preservation; CLI owns targeted requests, encoding and shared safe persistence. The current paths, v2 evidence filenames and adoption inventories now identify their owners directly. Plain JSON remains the prospective v2 representation, with v1 paths and byte semantics preserved. Model requirements, adoption, examples and proof obligations remain in the user-authorized combined model layout.

The new EntryRef table defines every reference-bearing field. Resolution and Verify evidence references name checks; Verify review references name a review root rather than a finding. Material-decision source references admit the enumerated manifest entries, review roots/findings, checks and decisions. Per-file disjoint referenceable IDs make path/id resolution unique, while allowing the same ID in different files. Actor IDs, change identity, activity, applicability, Origin, JudgmentBasis and Verify itself are explicitly excluded as EntryRef targets. Subject identity remains a separate concept.

Purpose-specific operations still compose with this rule. A finding added with the containing review's root ID is an invalid final v2 candidate even though no finding with that ID existed before. Likewise, a work/model/blocker ID collision in the manifest is structurally rejected; the CLI cannot silently rename an actor's selected ID or mutate the neighboring collection. This does not conflict with target-exists for an already present selected entry, or overlap rejection for assigning the same selected field twice. Those are separate target/operation checks; Record Format owns final candidate validity. Valid distinct targets remain constructible through the existing commands.

Reference resolution occurs after complete candidate construction. A new check and a referencing disposition, or decisions that refer to one another, can therefore be saved together without an intermediate workflow gate. Duplicate reference pairs, wrong target collections, missing IDs, unregistered paths and cross-change references have explicit structural rejection outcomes. Self-links and decision cycles record links without recursively establishing evidence or manufacturing approval. Downstream actors remain responsible for rejecting circular or inadequate justification.

The field-specific interpretation and cross-collection uniqueness rule are explicitly v2-only. A bounded inspection of the existing record-store-contract.js collector confirms that v1 builds a path-to-ID membership set from root and collection IDs and checks membership without the new field-specific restriction. Retaining that behavior avoids silently rejecting old references or interpreting ambiguous historical membership as v2 meaning. No migration or broadening of v1 semantics is approved.

The existing diagnostic correction remains intact: the digest binds the revision, complete observed Subject basis and diagnostic content; an already-drifted external subject changing again alters that identity. Receipt bounds, explicit diagnostic retrieval, truthful publication reporting, normal final-report reads and record_contract plus revision remain consistent. Purpose-specific writes and advanced paths share structural validation, preservation, conflicts and recoverable publication. Findings and blockers retain reporter disposition responsibility; recording a correction after completed activity still requires no readiness gate.

All eight boundary dimensions and material composed hazards retain requirement-owned outcomes. RF-SR-02 now includes wrong-kind, ambiguous and missing references and same-batch target creation in its allocated acceptance scope. Concrete v2 runtime regression tests, consumer adoption, adapter proof and token measurements remain Delivery obligations. The examples remain illustrative rather than substitute authority. No new material finding was identified.

## Validation and recording evidence

- Parent-run python scripts/validate-boundary-first.py --check --path docs/design/cli/cli.md --path docs/design/workflow/workflow.md --path docs/design/record-format/record-format.md: passed, structure-and-references-only.
- Parent-run python scripts/validate-markdown-readability.py docs/design/cli/cli.md docs/design/workflow/workflow.md docs/design/record-format/record-format.md: passed with 244 audit-only warnings.
- git diff 59e5152c --exit-code -- docs/design: passed; reviewed model/example contents match the requested commit. This checks document identity, not workflow state.
- Independent Python example checks: all nine JSON examples parse; both diagnostic preimage hashes match the expected values and differ with equal revision/diagnostics; reassessment findings remain equal; complete Record Format examples satisfy the new disjoint referenceable-ID rule.
- Read packages/rigorloop/dist/lib/record-store-contract.js lines 236-246 to substantiate the narrow v1 membership compatibility claim; no runtime implementation test or general code review was performed.
- record-store inspect supplies the registered context, expected revision and record identities. The transient check/record request binds all relied-on model/example/compatibility/proposal identities, preserves the complete existing finding and updates only review evidence, its explicit applicability and matching review activity.

The exact three-model review remains independent of its author. No reviewed model was edited by the reviewer, no unsupported artifact or permanent request was created, and no routing or automatic downstream continuation was performed. The retained historical finding subject can still produce subject-drift because its old path is truthful; that does not invalidate this explicitly assessed current package or authorize rewriting historical evidence.
