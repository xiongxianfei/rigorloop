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
  "independence_basis": "The same separately delegated record-format-rereview agent independently reread all three current model files and all ten model-owned examples, verified the diagnostic digest examples, and reassessed its original finding. The reviewer authored none of the model, layout, plain-JSON or diagnostic corrections. Contributors remain user and codex-root. This is an actual independent rereview, not automatic approval from matching hashes or a new role label.",
  "subjects": [
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:2286a09a7a760013cebc8c6ec06758ae9a239618e2af72dce61789b0edc6bf20"
    },
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:532cc0b06ec6fc3417c3387a3139c8b12e31d80663adb6d09155e79c10c2551f"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:3a2e18d5df85101104f738dfc7ef7ca9c264437a5a332e0b0e3ac88427a7c108"
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
- Package members: workflow = docs/design/workflow/workflow.md; cli = docs/design/cli/cli.md; record-format = docs/design/record-format/record-format.md. The ten relied-on model-owned examples are included as exact subjects in metadata.
- Upstream review ID: proposal-review-r1, registered in this change; its approved proposal subject remains unchanged.
- Review ID: design-review, independent correction rereview by record-format-rereview.
- Material findings: none open; rf-dr-001 explicitly resolved after independent reassessment.
- Correction targets: none required for this Design judgment.
- Recording status: supported actor-owned review record, with explicit current applicability.
- Settlement status: no historical lifecycle settlement command or transition is claimed. This record owns the explicit Design judgment.
- Immediate next stage: isolated stop; no routing decision was made.
- Claim limitations: exact-package Design approval only. No implementation correctness, runtime activation, final Verify completion, branch readiness or release approval is established. Delivery must still allocate and prove the specified obligations.

## Finding RF-DR-001: original basis and current disposition

Stable stored ID: rf-dr-001. Original severity: medium. Scope: artifact-local, cli. Correction owner: codex-root, Design authoring. Reporter and disposition owner: record-format-rereview. The finding's original exact subject identity remains in its structured subjects and is not retargeted to the relocated model.

Original evidence: CLI model lines 258 and 274-278 define observation_identity as the hash of {schema_version: 1, revision, observations}, with diagnostics containing code, safe message and locations but no required observed external subject identity. Line 278 nevertheless promises conflict when an observed external subject changes. A retained subject identity A can observe B on the first scan and C on the next, both different from A. The registered revision and the subject-drift code, location and fixed safe message can all remain identical, so the explicitly defined digest input remains identical. This is a missing identity input, not a hash collision or an external edit during publication.

Original required outcome: Make the exact observation digest input and continuation contract agree about changes to the observed external basis, including B-to-C drift that preserves the diagnostic category, location and message. Preserve bounded storage receipts and safe diagnostics; detail retrieval must not become a write prerequisite. Bind a deterministic observed path/identity basis, including absence, or define an equivalent identity-bearing diagnostic representation and acceptance case. Any deliberate narrowing to diagnostic-content stability must be an explicit reconciled Design decision and independently rereviewed.

Original rationale: a stable diagnostic projection could hide an already-drifted subject changing again. The promised expected-observations check needed the observed identity as an input, rather than assuming that a different file necessarily produces a different message. The original supporting Design judgment was changes-requested because this gap made diagnostic continuation weaker than its stated guarantee.

Current disposition: resolved. Independently reassessed CLI-SR-20 and the complete three-model package. The internal preimage now explicitly includes schema_version 2, revision, observed_subjects and observations. Every schema-defined Subject path is observed once, deduplicated and sorted, with exact current digest or confirmed absence; candidate/current scans share scope and request-only reads remain separate. Both published example digests were independently recomputed: B and C produce distinct identities despite identical record revision and diagnostics. The stated B-to-C conflict guarantee is now supported without expanding the bounded receipt. The original evidence, subjects and required outcome remain unchanged; no runtime implementation claim is made.

The correction chooses stronger identity binding rather than narrowing the promised freshness guarantee. It specifies all Subject fields, including origin and supporting-judgment subjects, independent of applicability and selected page. Schema-only traversal excludes narrative and EntryRef strings. Unsafe/unreadable subjects cannot masquerade as absence. Stored subject references do not acquire the unrelated 256 request-read limit. The deterministic preimage uses recursively ordered object keys, defined array ordering and no final LF. Candidate/current reads reconstruct the same subject scope, with each observed path used consistently within the scan. The existing external-edit limit and reverted-between-scans limit remain explicit.

The B/C examples keep both registered revision and diagnostics identical. Independent compact UTF-8 encoding and SHA-256 recomputation matched the expected identities, and those identities differ. Temporal acceptance now includes this case, disappearance/reappearance, formerly matching subjects and duplicate references. Counts and one digest remain the receipt's entire diagnostic payload; detail volume still cannot block structurally valid correction recording.

## Complete package assessment

The current package was read in full, including the model directory layout and plain-JSON changes since the prior review. Record Format owns v2 .json paths and complete closed object layouts, including required body strings and immutable concern origin. CLI dispatches the two exact manifest candidates, rejects ambiguity and version/extension mismatch, constructs body string tokens losslessly, and preserves the separate v1 encoding. Workflow maintains actor-owned meaning and requires coordinated adoption rather than making prospective v2 an available runtime profile. Historical subjects are preserved instead of silently remapped by the directory move.

Purpose-specific commands and batch retain one structural and recoverable persistence boundary. Actor-supplied applicability, judgments and dispositions remain separate from mechanical registry construction. A failed Verify and new blocker can be recorded after completed activity; Route supplies a later explicit routing decision. Stale mutation revisions conflict before no-op recognition. The corrected diagnostic identity strengthens detail continuation without expanding publication's external-tool concurrency guarantee.

Normal reads expose record_contract and revision from the same snapshot, including empty selections. Final Verify and shared decisions narratives remain available through ordinary targeted reads, with identity, applicability and clear absent/missing/malformed outcomes. The new plain-JSON body representation preserves those semantics. Findings retain enough origin to explain the concern without old review rounds, while responsible actors still inspect current engineering subjects before relying on evidence.

All ten owned examples were read. Nine JSON examples parse; the reassessment pair preserves the complete finding value while explicitly changing the current review assessment. The workflow diagram depicts responsible actor sequencing, not automatic CLI permission. Work-set messages illustrate explicit status recording against a stated starting state. The observation examples are internal preimages with synthetic subject identities, not runtime proof.

All eight boundary dimensions and material composed hazards retain requirement-owned outcomes. No additional material finding was identified. Residual flat-path mentions in a generic subject-inspection illustration and the Workflow placement table are editorial inconsistencies: the explicit model-layout and contract-specific path owners resolve the intended paths. They do not expand the recording allowlist or authorize migration. Delivery and published guidance should consistently use the selected paths.

## Validation and recording evidence

- python scripts/validate-boundary-first.py --check --path docs/design/cli/cli.md --path docs/design/workflow/workflow.md --path docs/design/record-format/record-format.md: passed, structure-and-references-only.
- python scripts/validate-markdown-readability.py docs/design/cli/cli.md docs/design/workflow/workflow.md docs/design/record-format/record-format.md: passed with 239 audit-only warnings.
- git diff --check: passed before review recording.
- Independent Python JSON/SHA-256 check: parsed all nine JSON examples; confirmed equal B/C revision and diagnostics; matched both expected observation digests; confirmed different digests; confirmed the before/after finding arrays are equal.
- record-store inspect supplies current registered context and expected revision. The transient check/record request binds the current model/example/proposal identities and both changed record identities. No permanent operation request or unsupported review artifact is created.

The reviewer authored only this review and its explicit applicability/activity updates through the supported recorder. Review metadata includes all exact current relied-on subjects; the historical finding basis remains unchanged. Successful recording is storage-only and does not itself authenticate independence or run the proposed commands. No runtime implementation test was performed; Design approval does not replace Delivery Review, Code Review or Verify.
