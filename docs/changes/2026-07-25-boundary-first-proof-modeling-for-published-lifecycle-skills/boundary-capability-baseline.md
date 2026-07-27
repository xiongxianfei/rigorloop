# Boundary Capability Baseline

This report is computed from repository-visible evidence.

```yaml
{
  "adapter_parity": {
    "blocking_reason": null,
    "evidence_refs": [
      {
        "identity": "sha256:c5f3ddb58d8b54262803623b6ea75953450d005457675a56475a2f463e4de5cb",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/canonical.json"
      },
      {
        "identity": "sha256:13d3451cca189adb4478ea1578e6ceb6d3a6efbf527288e54df3bcbf071e6b15",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/generated.json"
      },
      {
        "identity": "sha256:62ca28b1a125585426e4247f7cfd997f3efe142573b0f9a628ee93470c29d44b",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/packed.json"
      },
      {
        "identity": "sha256:de38dd87fc3719767c3db4612a1a39e4bbb6f075f1b93deb686f1674e7c68696",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/installed.json"
      }
    ],
    "result": "pass"
  },
  "boundary_model_version": "v1",
  "checks": {
    "boundary-adapter-parity": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:c5f3ddb58d8b54262803623b6ea75953450d005457675a56475a2f463e4de5cb",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/canonical.json"
        },
        {
          "identity": "sha256:13d3451cca189adb4478ea1578e6ceb6d3a6efbf527288e54df3bcbf071e6b15",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/generated.json"
        },
        {
          "identity": "sha256:62ca28b1a125585426e4247f7cfd997f3efe142573b0f9a628ee93470c29d44b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/packed.json"
        },
        {
          "identity": "sha256:de38dd87fc3719767c3db4612a1a39e4bbb6f075f1b93deb686f1674e7c68696",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/installed.json"
        }
      ],
      "result": "pass"
    },
    "boundary-capability-baseline": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:d53feed3ed042453798fe2d1e5a0b62e42e87a7ee63792884982bbe6e4355bd8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m3-r2.md"
        },
        {
          "identity": "sha256:734b63757952d2162e512f721aa0e20a4fc274489927004e6b4892ff5194c1e5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/current.json"
        }
      ],
      "result": "pass"
    },
    "boundary-incident-replay": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        }
      ],
      "result": "pass"
    },
    "boundary-skill-contract": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc",
          "path": "specs/skill-contract.md"
        }
      ],
      "result": "pass"
    },
    "boundary-traceability": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:431e30ef05ff2720e77a589b48ac2794d79d76878f17c8dbe6be335d165d8f87",
          "path": "specs/rigorloop-workflow.test.md"
        }
      ],
      "result": "pass"
    },
    "boundary-workflow-contract": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:7b035049f01e8e197809e79dbfb7f8481a2c61f63fc3bf992116544a4250c819",
          "path": "specs/rigorloop-workflow.md"
        }
      ],
      "result": "pass"
    }
  },
  "duplicate_normative_owner_count": 0,
  "evaluated_skills": [
    "spec",
    "spec-review",
    "test-spec",
    "test-spec-review",
    "implement",
    "code-review",
    "verify",
    "workflow"
  ],
  "false_blocking_count": 0,
  "fixtures": [
    {
      "blocking_reason": null,
      "detected_stage": "spec-review",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:899c24bb094ad155bc319623181ba2b4c70f626c4640521b329d1ae21f6ce9ca",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-CANONICAL-001.json"
        }
      ],
      "expected_gate": "spec-review",
      "fixture_id": "BFP-FX-CANONICAL-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "detected_stage": "test-spec-review",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:d880c3450fe4f7f2c6035eb6ba0d9788d31915e39fd03e3e99bfc47d45093d1f",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-VOCAB-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-VOCAB-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "detected_stage": "test-spec-review",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:f58580db445b04204092abda8778e02058768fb5e27915462c1564935d1e95f4",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-TRANSITION-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-TRANSITION-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "detected_stage": "test-spec-review",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:0478ae39e3976aa3c2d5565586a4ed002eb12aee6aadf129ec3c7f96d0142ceb",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-IDENTITY-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-IDENTITY-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "detected_stage": "test-spec-review",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:89b905a13567a2d833390d224fe7169c3a7e01f73fcbd34c00f4891075b5e0d1",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-ATOMICITY-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-ATOMICITY-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "detected_stage": "test-spec-review",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:73163f87e2e42d99bbab9e29a6508440b978fdfdfe96650ecf5e617dec74bfaf",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-RECOVERY-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-RECOVERY-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "detected_stage": "test-spec-review",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:f9f8d489e2066ca34e93f7265085c745b0345a7a38723c30a1ea75b616c63eb5",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-COMPOSITION-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-COMPOSITION-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "detected_stage": "implement",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:27e5c88f0f50022fc33ca5c98c173111c58a6fcff72c3ca035af00a43deb6b20",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-SIBLING-001.json"
        }
      ],
      "expected_gate": "implement",
      "fixture_id": "BFP-FX-SIBLING-001",
      "result": "pass",
      "sibling_bypass_remaining": false
    }
  ],
  "new_universal_artifact_count": 0,
  "overall_result": "pass",
  "preservation_results": {
    "behavior": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:d53feed3ed042453798fe2d1e5a0b62e42e87a7ee63792884982bbe6e4355bd8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m3-r2.md"
        }
      ],
      "result": "pass"
    },
    "claim-boundary": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:d53feed3ed042453798fe2d1e5a0b62e42e87a7ee63792884982bbe6e4355bd8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m3-r2.md"
        }
      ],
      "result": "pass"
    },
    "handoff": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:d53feed3ed042453798fe2d1e5a0b62e42e87a7ee63792884982bbe6e4355bd8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m3-r2.md"
        }
      ],
      "result": "pass"
    },
    "isolation": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:d53feed3ed042453798fe2d1e5a0b62e42e87a7ee63792884982bbe6e4355bd8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m3-r2.md"
        }
      ],
      "result": "pass"
    },
    "review-recording": {
      "blocking_reason": null,
      "evidence_refs": [
        {
          "identity": "sha256:d53feed3ed042453798fe2d1e5a0b62e42e87a7ee63792884982bbe6e4355bd8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m3-r2.md"
        }
      ],
      "result": "pass"
    }
  },
  "required_check_ids": [
    "boundary-workflow-contract",
    "boundary-skill-contract",
    "boundary-traceability",
    "boundary-incident-replay",
    "boundary-adapter-parity",
    "boundary-capability-baseline"
  ],
  "schema_version": "boundary-capability-baseline-v1",
  "simple_fixture_structure_correction_cycles": 0
}
```
