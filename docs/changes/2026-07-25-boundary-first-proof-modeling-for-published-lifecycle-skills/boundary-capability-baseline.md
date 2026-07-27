# Boundary Capability Baseline

This report is computed from repository-visible evidence.

```yaml
{
  "adapter_parity": {
    "blocking_reason": null,
    "dependency_results": [
      {
        "operation_id": "canonical-skill-resource-manifest",
        "result_identity": "sha256:2cf30132e3edb6fd1a5c380f27031defbdd0186e7b4da2a7c8be8ec4bb40ef78"
      }
    ],
    "diagnostic_id": "none",
    "evidence_refs": [
      {
        "identity": "sha256:8ca18bd34be44fd7c4f331b4325234ddc03c1b3dc3fead53b3921a528b233ef4",
        "path": "dist/adapters/manifest.yaml"
      },
      {
        "identity": "sha256:d3755beb0e8abb5a598a750faf34fef2d5c9887fa2aa32f64e209d5400c97fc4",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/canonical-skill-resource-manifest.json"
      },
      {
        "identity": "sha256:4331f2e3a9d01794755cc18e5a0b790fab079750f56bbdb3eb354b9a636ea0ad",
        "path": "scripts/adapter_distribution.py"
      },
      {
        "identity": "sha256:9ca2e208b310ee08ace9cf9c8b232eb4b27175f558c5eab89436c9f2f1984695",
        "path": "scripts/build-adapters.py"
      },
      {
        "identity": "sha256:ce949921155031797c55ba07aa3ab27e021cfb307b4e1cca1e42ecee6a87cd14",
        "path": "scripts/validate-adapters.py"
      },
      {
        "identity": "sha256:c5f3ddb58d8b54262803623b6ea75953450d005457675a56475a2f463e4de5cb",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/canonical.json"
      },
      {
        "identity": "sha256:13d3451cca189adb4478ea1578e6ceb6d3a6efbf527288e54df3bcbf071e6b15",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/generated.json"
      },
      {
        "identity": "sha256:de38dd87fc3719767c3db4612a1a39e4bbb6f075f1b93deb686f1674e7c68696",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/installed.json"
      },
      {
        "identity": "sha256:62ca28b1a125585426e4247f7cfd997f3efe142573b0f9a628ee93470c29d44b",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/adapter-parity/packed.json"
      }
    ],
    "observations": {},
    "operation_identity": "sha256:6eb46a450f4278d17fd1ba9e4c000a4a4f03ac6d69ff7e184b8314a2617b9132",
    "result": "pass"
  },
  "boundary_model_version": "v1",
  "checks": {
    "boundary-adapter-parity": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "adapter-parity",
          "result_identity": "sha256:6eb46a450f4278d17fd1ba9e4c000a4a4f03ac6d69ff7e184b8314a2617b9132"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [],
      "observations": {},
      "operation_identity": "sha256:5425c56178a13459927b7650058b8f628ed196f7490c382a9dfc184b7d7caf29",
      "result": "pass"
    },
    "boundary-capability-baseline": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "boundary-workflow-contract",
          "result_identity": "sha256:9255eda0bfdcaacc6731c23defb89d53ce074c253ddabac56ee88559a797dcfa"
        },
        {
          "operation_id": "boundary-skill-contract",
          "result_identity": "sha256:bb0801f367b390afd2c991b3a7afb4f2cd8c1f068cd436a50b8a2f3167d148c2"
        },
        {
          "operation_id": "boundary-traceability",
          "result_identity": "sha256:5a46e01b2066e731adb1137e498f7d6e1158848efc91265e2262df9a9fb37e23"
        },
        {
          "operation_id": "BFP-FX-CANONICAL-001",
          "result_identity": "sha256:b0c8dfbb33fa1005fa7e5a6b52b8e7775c1441f97b5b54ea60d8772c48ba17f3"
        },
        {
          "operation_id": "BFP-FX-VOCAB-001",
          "result_identity": "sha256:6c269a81f51de556f8bf454ce3e0ae292179e7e091b046d30461ff5e767ea540"
        },
        {
          "operation_id": "BFP-FX-TRANSITION-001",
          "result_identity": "sha256:575016016cfa2806ca86a3817049a5c7d078ac1212c0a4ecd77f857c059e7df3"
        },
        {
          "operation_id": "BFP-FX-IDENTITY-001",
          "result_identity": "sha256:5758681a0273828347c965f2373b1ac35f2a5eded373f2ecd6bcc9033b20b211"
        },
        {
          "operation_id": "BFP-FX-ATOMICITY-001",
          "result_identity": "sha256:30510e6fbef9c1af348e0acc35e28ee155be1d56bed3ab977dd2c96e96f61083"
        },
        {
          "operation_id": "BFP-FX-RECOVERY-001",
          "result_identity": "sha256:1af1bc9104562a18e6c0afb9639c4222ab4d2baf348853b9678e8a5f5d5d256b"
        },
        {
          "operation_id": "BFP-FX-COMPOSITION-001",
          "result_identity": "sha256:1b055674bf1be8b1cbc555b448fa4dd8949d3dea68cec41c6d49c58de3e0e6ce"
        },
        {
          "operation_id": "BFP-FX-SIBLING-001",
          "result_identity": "sha256:834655d42b3c9b02dfc58114e1e8baaf437da8b34577a7b9db1204176fb52b3b"
        },
        {
          "operation_id": "boundary-incident-replay",
          "result_identity": "sha256:43ee2d45e073b67cf7f7195195b6a80aeaed9f3eb6a0e5ba02e55d05b8b28efc"
        },
        {
          "operation_id": "preservation-manifest",
          "result_identity": "sha256:87baad80eb26078837ac3fe5d5d096e2daadc16d48b441f1bf46a0a4b27667c8"
        },
        {
          "operation_id": "preservation-behavior",
          "result_identity": "sha256:33cdeb6a00d69c004744ef4cb61ce076970f3fb1bea6934ac89c71e451afe7da"
        },
        {
          "operation_id": "preservation-claim-boundary",
          "result_identity": "sha256:c8741b9f16cf504aa562a5cf29069a982c921606f0903edd18a1917a3957e585"
        },
        {
          "operation_id": "preservation-review-recording",
          "result_identity": "sha256:1556cc615406ef01a97a655024e43dcb05d4a75060046575bc6eb01cf04187bc"
        },
        {
          "operation_id": "preservation-isolation",
          "result_identity": "sha256:7d055e5ddfa8981b8fbf2a6431b8134d092cf5f4bd0fe9f903f750004695aced"
        },
        {
          "operation_id": "preservation-handoff",
          "result_identity": "sha256:650c81d1fbb476e2bbfb747d5dc1d153faeebf86c00b662c1df3ced5be20dbe3"
        },
        {
          "operation_id": "behavior-implementation-manifest",
          "result_identity": "sha256:78bbcc47b4a26b55c33c553675d7a09e16370abb5f16c6a186858f878e90429a"
        },
        {
          "operation_id": "simple-change-behavior",
          "result_identity": "sha256:7617b819c29dc6852745d6a6b8a1c5df8a64c4bfe8c6821e6455c2a174ee4407"
        },
        {
          "operation_id": "canonical-skill-resource-manifest",
          "result_identity": "sha256:2cf30132e3edb6fd1a5c380f27031defbdd0186e7b4da2a7c8be8ec4bb40ef78"
        },
        {
          "operation_id": "adapter-parity",
          "result_identity": "sha256:6eb46a450f4278d17fd1ba9e4c000a4a4f03ac6d69ff7e184b8314a2617b9132"
        },
        {
          "operation_id": "boundary-adapter-parity",
          "result_identity": "sha256:5425c56178a13459927b7650058b8f628ed196f7490c382a9dfc184b7d7caf29"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [],
      "observations": {
        "duplicate_normative_owner_count": 0,
        "false_blocking_count": 0,
        "new_universal_artifact_count": 0,
        "simple_fixture_structure_correction_cycles": 0
      },
      "operation_identity": "sha256:47947c1a94206af31ce9be5389bbea6736f99a0ae49560326b2b194a361a5e0d",
      "result": "pass"
    },
    "boundary-incident-replay": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "BFP-FX-CANONICAL-001",
          "result_identity": "sha256:b0c8dfbb33fa1005fa7e5a6b52b8e7775c1441f97b5b54ea60d8772c48ba17f3"
        },
        {
          "operation_id": "BFP-FX-VOCAB-001",
          "result_identity": "sha256:6c269a81f51de556f8bf454ce3e0ae292179e7e091b046d30461ff5e767ea540"
        },
        {
          "operation_id": "BFP-FX-TRANSITION-001",
          "result_identity": "sha256:575016016cfa2806ca86a3817049a5c7d078ac1212c0a4ecd77f857c059e7df3"
        },
        {
          "operation_id": "BFP-FX-IDENTITY-001",
          "result_identity": "sha256:5758681a0273828347c965f2373b1ac35f2a5eded373f2ecd6bcc9033b20b211"
        },
        {
          "operation_id": "BFP-FX-ATOMICITY-001",
          "result_identity": "sha256:30510e6fbef9c1af348e0acc35e28ee155be1d56bed3ab977dd2c96e96f61083"
        },
        {
          "operation_id": "BFP-FX-RECOVERY-001",
          "result_identity": "sha256:1af1bc9104562a18e6c0afb9639c4222ab4d2baf348853b9678e8a5f5d5d256b"
        },
        {
          "operation_id": "BFP-FX-COMPOSITION-001",
          "result_identity": "sha256:1b055674bf1be8b1cbc555b448fa4dd8949d3dea68cec41c6d49c58de3e0e6ce"
        },
        {
          "operation_id": "BFP-FX-SIBLING-001",
          "result_identity": "sha256:834655d42b3c9b02dfc58114e1e8baaf437da8b34577a7b9db1204176fb52b3b"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:89b905a13567a2d833390d224fe7169c3a7e01f73fcbd34c00f4891075b5e0d1",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-ATOMICITY-001.json"
        },
        {
          "identity": "sha256:899c24bb094ad155bc319623181ba2b4c70f626c4640521b329d1ae21f6ce9ca",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-CANONICAL-001.json"
        },
        {
          "identity": "sha256:f9f8d489e2066ca34e93f7265085c745b0345a7a38723c30a1ea75b616c63eb5",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-COMPOSITION-001.json"
        },
        {
          "identity": "sha256:0478ae39e3976aa3c2d5565586a4ed002eb12aee6aadf129ec3c7f96d0142ceb",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-IDENTITY-001.json"
        },
        {
          "identity": "sha256:73163f87e2e42d99bbab9e29a6508440b978fdfdfe96650ecf5e617dec74bfaf",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-RECOVERY-001.json"
        },
        {
          "identity": "sha256:27e5c88f0f50022fc33ca5c98c173111c58a6fcff72c3ca035af00a43deb6b20",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-SIBLING-001.json"
        },
        {
          "identity": "sha256:f58580db445b04204092abda8778e02058768fb5e27915462c1564935d1e95f4",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-TRANSITION-001.json"
        },
        {
          "identity": "sha256:d880c3450fe4f7f2c6035eb6ba0d9788d31915e39fd03e3e99bfc47d45093d1f",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-VOCAB-001.json"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:43ee2d45e073b67cf7f7195195b6a80aeaed9f3eb6a0e5ba02e55d05b8b28efc",
      "result": "pass"
    },
    "boundary-skill-contract": {
      "blocking_reason": null,
      "dependency_results": [],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:9a6a96eeb9040fab96b5bbacaee2eeb94fc20dfd3f1384419aec4362e3916274",
          "path": "skills/code-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/code-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:a4067a4510f223a06db178dcd5f1c63906ae459af89f34ad3068b20fa78b5ff3",
          "path": "skills/implement/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/implement/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:6cbe16074ffc500294e50a49237d27120c3d1ee17121ddd3966de44dbb263cfd",
          "path": "skills/spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:81e15833869bb5cec374fc08e8c05bacc78573fbff07a89d1c4ccee3b7d7db7d",
          "path": "skills/spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:245d22ceb249bc531e80ee83af69cdb1acb641fec0bf54bd266ff39937de4d4f",
          "path": "skills/test-spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:27336177f4f82e7a2dccb7ee7220a4494d3458d67653ccfe00dcd4bdfa4cad11",
          "path": "skills/test-spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:6b78a3daed2c54d6651a3263605627dd40e18564476fe87ff464315d4f8438ee",
          "path": "skills/verify/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/verify/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:28fb8aaab0ff8405e3a325656feba8d6d570d43618bf7c802b2ea3961b0cd683",
          "path": "skills/workflow/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/workflow/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc",
          "path": "specs/skill-contract.md"
        },
        {
          "identity": "sha256:586e77d3b9587dcc016c447eb499eff5b0855ed0e77381b2368a4c62ca92da5d",
          "path": "specs/skill-contract.test.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:bb0801f367b390afd2c991b3a7afb4f2cd8c1f068cd436a50b8a2f3167d148c2",
      "result": "pass"
    },
    "boundary-traceability": {
      "blocking_reason": null,
      "dependency_results": [],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:2beb43894a0dafcfaa7eacb3f3de77faafd11bfc72dcb8cee29636c5a63c9572",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml"
        },
        {
          "identity": "sha256:c339ceed9592ec069cb94efd4774ad60ab9829983320fab1a3f22ea128e06ced",
          "path": "specs/rigorloop-workflow.md"
        },
        {
          "identity": "sha256:e627ff46ca104c7ec26114b42545e81500ecb2137540923f10bf5bd7c1eeccec",
          "path": "specs/rigorloop-workflow.test.md"
        },
        {
          "identity": "sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc",
          "path": "specs/skill-contract.md"
        },
        {
          "identity": "sha256:586e77d3b9587dcc016c447eb499eff5b0855ed0e77381b2368a4c62ca92da5d",
          "path": "specs/skill-contract.test.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:5a46e01b2066e731adb1137e498f7d6e1158848efc91265e2262df9a9fb37e23",
      "result": "pass"
    },
    "boundary-workflow-contract": {
      "blocking_reason": null,
      "dependency_results": [],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:c339ceed9592ec069cb94efd4774ad60ab9829983320fab1a3f22ea128e06ced",
          "path": "specs/rigorloop-workflow.md"
        },
        {
          "identity": "sha256:e627ff46ca104c7ec26114b42545e81500ecb2137540923f10bf5bd7c1eeccec",
          "path": "specs/rigorloop-workflow.test.md"
        }
      ],
      "observations": {
        "duplicate_normative_owner_count": 0
      },
      "operation_identity": "sha256:9255eda0bfdcaacc6731c23defb89d53ce074c253ddabac56ee88559a797dcfa",
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
      "dependency_results": [],
      "detected_stage": "spec-review",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:899c24bb094ad155bc319623181ba2b4c70f626c4640521b329d1ae21f6ce9ca",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-CANONICAL-001.json"
        }
      ],
      "expected_gate": "spec-review",
      "fixture_id": "BFP-FX-CANONICAL-001",
      "observations": {
        "detected_stage": "spec-review",
        "escaped_to_code_review": false,
        "expected_gate": "spec-review",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:b0c8dfbb33fa1005fa7e5a6b52b8e7775c1441f97b5b54ea60d8772c48ba17f3",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "dependency_results": [],
      "detected_stage": "test-spec-review",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:d880c3450fe4f7f2c6035eb6ba0d9788d31915e39fd03e3e99bfc47d45093d1f",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-VOCAB-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-VOCAB-001",
      "observations": {
        "detected_stage": "test-spec-review",
        "escaped_to_code_review": false,
        "expected_gate": "test-spec-review",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:6c269a81f51de556f8bf454ce3e0ae292179e7e091b046d30461ff5e767ea540",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "dependency_results": [],
      "detected_stage": "test-spec-review",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:f58580db445b04204092abda8778e02058768fb5e27915462c1564935d1e95f4",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-TRANSITION-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-TRANSITION-001",
      "observations": {
        "detected_stage": "test-spec-review",
        "escaped_to_code_review": false,
        "expected_gate": "test-spec-review",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:575016016cfa2806ca86a3817049a5c7d078ac1212c0a4ecd77f857c059e7df3",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "dependency_results": [],
      "detected_stage": "test-spec-review",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:0478ae39e3976aa3c2d5565586a4ed002eb12aee6aadf129ec3c7f96d0142ceb",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-IDENTITY-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-IDENTITY-001",
      "observations": {
        "detected_stage": "test-spec-review",
        "escaped_to_code_review": false,
        "expected_gate": "test-spec-review",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:5758681a0273828347c965f2373b1ac35f2a5eded373f2ecd6bcc9033b20b211",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "dependency_results": [],
      "detected_stage": "test-spec-review",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:89b905a13567a2d833390d224fe7169c3a7e01f73fcbd34c00f4891075b5e0d1",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-ATOMICITY-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-ATOMICITY-001",
      "observations": {
        "detected_stage": "test-spec-review",
        "escaped_to_code_review": false,
        "expected_gate": "test-spec-review",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:30510e6fbef9c1af348e0acc35e28ee155be1d56bed3ab977dd2c96e96f61083",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "dependency_results": [],
      "detected_stage": "test-spec-review",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:73163f87e2e42d99bbab9e29a6508440b978fdfdfe96650ecf5e617dec74bfaf",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-RECOVERY-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-RECOVERY-001",
      "observations": {
        "detected_stage": "test-spec-review",
        "escaped_to_code_review": false,
        "expected_gate": "test-spec-review",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:1af1bc9104562a18e6c0afb9639c4222ab4d2baf348853b9678e8a5f5d5d256b",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "dependency_results": [],
      "detected_stage": "test-spec-review",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:f9f8d489e2066ca34e93f7265085c745b0345a7a38723c30a1ea75b616c63eb5",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-COMPOSITION-001.json"
        }
      ],
      "expected_gate": "test-spec-review",
      "fixture_id": "BFP-FX-COMPOSITION-001",
      "observations": {
        "detected_stage": "test-spec-review",
        "escaped_to_code_review": false,
        "expected_gate": "test-spec-review",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:1b055674bf1be8b1cbc555b448fa4dd8949d3dea68cec41c6d49c58de3e0e6ce",
      "result": "pass",
      "sibling_bypass_remaining": false
    },
    {
      "blocking_reason": null,
      "dependency_results": [],
      "detected_stage": "implement",
      "diagnostic_id": "none",
      "escaped_to_code_review": false,
      "evidence_refs": [
        {
          "identity": "sha256:e16d41a1e0a0da61859d8093b6d5d847718c2fed1fad6102ff04b1cd0b12f9bb",
          "path": "tests/fixtures/boundary-proof/incident-registry.json"
        },
        {
          "identity": "sha256:27e5c88f0f50022fc33ca5c98c173111c58a6fcff72c3ca035af00a43deb6b20",
          "path": "tests/fixtures/boundary-proof/incidents/BFP-FX-SIBLING-001.json"
        }
      ],
      "expected_gate": "implement",
      "fixture_id": "BFP-FX-SIBLING-001",
      "observations": {
        "detected_stage": "implement",
        "escaped_to_code_review": false,
        "expected_gate": "implement",
        "sibling_bypass_remaining": false
      },
      "operation_identity": "sha256:834655d42b3c9b02dfc58114e1e8baaf437da8b34577a7b9db1204176fb52b3b",
      "result": "pass",
      "sibling_bypass_remaining": false
    }
  ],
  "new_universal_artifact_count": 0,
  "overall_result": "pass",
  "preservation_results": {
    "behavior": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "preservation-manifest",
          "result_identity": "sha256:87baad80eb26078837ac3fe5d5d096e2daadc16d48b441f1bf46a0a4b27667c8"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:f50e1f2219e8c13cdd2f7954d92743e2e153d4f97d3f7a6cb94909e4dc0d0bb8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/behavior.json"
        },
        {
          "identity": "sha256:5334ccea66935293387661749a8feeaaf0dd0226d5a2181e2cbce4f5418fb52a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/behavior.json"
        },
        {
          "identity": "sha256:5af151845c12a8caab00ea0869b835f2d8f53a114a411d155488ad25fa0b2a05",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/behavior.json"
        },
        {
          "identity": "sha256:50492a9268e542cddbc7cad373049159c9d552dcb64baa4c4f8a92bdd83ef3a6",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/behavior.json"
        },
        {
          "identity": "sha256:76cafd6a9b453862452976214077adc4a50ffb03632ce3a0306b83b6b1537f5b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/behavior.json"
        },
        {
          "identity": "sha256:b62af8bb712f5bc490d426108c018c249df2be744a39cd05325e094219a58a0c",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/behavior.json"
        },
        {
          "identity": "sha256:ca35a2bc223fd0a115a2a025d0cdd4878dadede1c40f7980666d3348ef82cbd2",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/behavior.json"
        },
        {
          "identity": "sha256:50d7de6d0e11a5a205b79e13ebc8ccf43d80ab746fcc1d696f7028d9a819275d",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/behavior.json"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/behavior.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/behavior.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/behavior.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/behavior.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/behavior.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/behavior.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/behavior.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/behavior.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:33cdeb6a00d69c004744ef4cb61ce076970f3fb1bea6934ac89c71e451afe7da",
      "result": "pass"
    },
    "claim-boundary": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "preservation-manifest",
          "result_identity": "sha256:87baad80eb26078837ac3fe5d5d096e2daadc16d48b441f1bf46a0a4b27667c8"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:0d69ff9b81334e9736e0a76ddd6d8c28a8327649d9bbffc50ca440710e8a226e",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/claim-boundary.json"
        },
        {
          "identity": "sha256:7ecb36d3c05aeeddb2b78766cbae90f6295ec3b38384586c2d24c48f177b88ff",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/claim-boundary.json"
        },
        {
          "identity": "sha256:0bfc05ce30ced5ccea2b85cf1c2a0b077473f20b1c0756643be461a0b28defc9",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/claim-boundary.json"
        },
        {
          "identity": "sha256:8a2c348a877985f482c2f33c1ff76abc8759091e5805156da88ae5caad4e9cc9",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/claim-boundary.json"
        },
        {
          "identity": "sha256:6055e4324d62bf2785c83519a0b8607c2a9257a1c4b81d1b5c7f615e3f3a1821",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/claim-boundary.json"
        },
        {
          "identity": "sha256:0c75c2eb70ba41498926cb797e7d79ce8a8fcda6ebe7d42295b0441d548734ac",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/claim-boundary.json"
        },
        {
          "identity": "sha256:74206bdbf716208af4f2c79943cd146e7c4fb7d53edc7af3192a320e8fc483c8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/claim-boundary.json"
        },
        {
          "identity": "sha256:68e63bc76ffba542f76476a02f479c1465ad3051fd39029618909439a74a0e28",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/claim-boundary.json"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/claim-boundary.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/claim-boundary.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/claim-boundary.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/claim-boundary.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/claim-boundary.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/claim-boundary.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/claim-boundary.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/claim-boundary.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:c8741b9f16cf504aa562a5cf29069a982c921606f0903edd18a1917a3957e585",
      "result": "pass"
    },
    "handoff": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "preservation-manifest",
          "result_identity": "sha256:87baad80eb26078837ac3fe5d5d096e2daadc16d48b441f1bf46a0a4b27667c8"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:3c8cf6a5a6d03e6a2884bf5a89399ab1c6dfc0114fb174778f10d8b8d7a74f32",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/handoff.json"
        },
        {
          "identity": "sha256:3b5fed9bd3efcc071a9e2493f29b43bfe1a57f782570cb59e76bb2dd0c02c8ed",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/handoff.json"
        },
        {
          "identity": "sha256:26dfde46c9746c1a79b8f5d1ea7412b2c87c08ada5f93ecb7823fcd20ce6b05d",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/handoff.json"
        },
        {
          "identity": "sha256:eb0d89b2c3179e0b97143d1dc8380dee669a5ea808d336504b92cf9c84929971",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/handoff.json"
        },
        {
          "identity": "sha256:2b2421155abecc917dac8a2cce51a6509224552a46b68719d90d2260782580fa",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/handoff.json"
        },
        {
          "identity": "sha256:f950e2cb2a786230c175ad7ec24e08a10b70a173b14279f8453d92b8fb58338a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/handoff.json"
        },
        {
          "identity": "sha256:bf36d0a678846220c6b57100747147dd826faadc95399c9d976137107e90deae",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/handoff.json"
        },
        {
          "identity": "sha256:1c6f44c746dda6e080a5743ac8c9eaabe5971376166aaab8fa8de0dbcdad9b33",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/handoff.json"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/handoff.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/handoff.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/handoff.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/handoff.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/handoff.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/handoff.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/handoff.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/handoff.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:650c81d1fbb476e2bbfb747d5dc1d153faeebf86c00b662c1df3ced5be20dbe3",
      "result": "pass"
    },
    "isolation": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "preservation-manifest",
          "result_identity": "sha256:87baad80eb26078837ac3fe5d5d096e2daadc16d48b441f1bf46a0a4b27667c8"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:5b406d8f6ed638965c51006928d62ddc0311652d063fc885a18292c8b7b86725",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/isolation.json"
        },
        {
          "identity": "sha256:ef74ea8687fb970d2016e73ba2a6ec1a63f2eea8c9c0c9d5661e7dbc7311bdd5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/isolation.json"
        },
        {
          "identity": "sha256:2496c47184288a2227e9f44d3fc36197fe2614e96a96de129b788066603bd7da",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/isolation.json"
        },
        {
          "identity": "sha256:c638b2331801571c2a9224e9420d8f0ef556692b34b9c9a180edfd4ad09dada5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/isolation.json"
        },
        {
          "identity": "sha256:e009a2d43444d8690b24fb6a10cb5a8b252919dece2676f38845f0ba61ba2338",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/isolation.json"
        },
        {
          "identity": "sha256:998cf6e0484a2c8909df364737c31651253903bec571627b571255c91410312f",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/isolation.json"
        },
        {
          "identity": "sha256:3095b7dd573d03d66d3c5cb7feace82647a7a4f4d0199b7b3b41d8c1731beb78",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/isolation.json"
        },
        {
          "identity": "sha256:218e54623639d127f03203bfb3c689bb071100ea98a5ee8349d744d6a12bac4a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/isolation.json"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/isolation.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/isolation.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/isolation.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/isolation.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/isolation.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/isolation.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/isolation.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/isolation.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:7d055e5ddfa8981b8fbf2a6431b8134d092cf5f4bd0fe9f903f750004695aced",
      "result": "pass"
    },
    "review-recording": {
      "blocking_reason": null,
      "dependency_results": [
        {
          "operation_id": "preservation-manifest",
          "result_identity": "sha256:87baad80eb26078837ac3fe5d5d096e2daadc16d48b441f1bf46a0a4b27667c8"
        }
      ],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:57241a9fe3c2e483ce6696b3f21e031cbc3ff83cdad3bd15c90928b9cb45dd99",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/review-recording.json"
        },
        {
          "identity": "sha256:23b15998f827fd656b4d406f1bd31392cbb4bee0af13fce88aacd5944084c0e1",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/review-recording.json"
        },
        {
          "identity": "sha256:85c958e32515185cda0897c276b04ea41a25c7816796696c4a6f6752e159a775",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/review-recording.json"
        },
        {
          "identity": "sha256:3a132c49dd3ee6df4a082067b2f99e54f4232456bba2d926fc4b1634fbf0d55f",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/review-recording.json"
        },
        {
          "identity": "sha256:a9aa65d0fc0ec5f0d349b49fc124cba584ec7a205531d557e43fab2ecacbaeca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/review-recording.json"
        },
        {
          "identity": "sha256:a386fe777e2638f3d8bcf15583e2c15f361f5cb8864da2676a321f2f17ee6eb5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/review-recording.json"
        },
        {
          "identity": "sha256:3023a123790e3a426f02b34b05144e2c7ce1b6973aec7ff8c83df96caacd0f52",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/review-recording.json"
        },
        {
          "identity": "sha256:4354f847a50d2aac73757babc4145a90b496e747c698cc5dbd3a518d8bf427b6",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/review-recording.json"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/review-recording.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/review-recording.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/review-recording.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/review-recording.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/review-recording.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/review-recording.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/review-recording.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/review-recording.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:1556cc615406ef01a97a655024e43dcb05d4a75060046575bc6eb01cf04187bc",
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
  "simple_change": {
    "blocking_reason": null,
    "dependency_results": [
      {
        "operation_id": "behavior-implementation-manifest",
        "result_identity": "sha256:78bbcc47b4a26b55c33c553675d7a09e16370abb5f16c6a186858f878e90429a"
      }
    ],
    "diagnostic_id": "none",
    "evidence_refs": [
      {
        "identity": "sha256:431fd8011869f3619b1729d9eec9211b0d2b4684b4252afd611bbf3ac6499780",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/behavior-implementation-manifest.json"
      },
      {
        "identity": "sha256:6cbe16074ffc500294e50a49237d27120c3d1ee17121ddd3966de44dbb263cfd",
        "path": "skills/spec-review/SKILL.md"
      },
      {
        "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
        "path": "skills/spec-review/references/boundary-proof-model.md"
      },
      {
        "identity": "sha256:81e15833869bb5cec374fc08e8c05bacc78573fbff07a89d1c4ccee3b7d7db7d",
        "path": "skills/spec/SKILL.md"
      },
      {
        "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
        "path": "skills/spec/references/boundary-proof-model.md"
      },
      {
        "identity": "sha256:245d22ceb249bc531e80ee83af69cdb1acb641fec0bf54bd266ff39937de4d4f",
        "path": "skills/test-spec-review/SKILL.md"
      },
      {
        "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
        "path": "skills/test-spec-review/references/boundary-proof-model.md"
      },
      {
        "identity": "sha256:27336177f4f82e7a2dccb7ee7220a4494d3458d67653ccfe00dcd4bdfa4cad11",
        "path": "skills/test-spec/SKILL.md"
      },
      {
        "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
        "path": "skills/test-spec/references/boundary-proof-model.md"
      },
      {
        "identity": "sha256:28fb8aaab0ff8405e3a325656feba8d6d570d43618bf7c802b2ea3961b0cd683",
        "path": "skills/workflow/SKILL.md"
      },
      {
        "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
        "path": "skills/workflow/references/boundary-proof-model.md"
      },
      {
        "identity": "sha256:7653a05392601a23eb93216e64be688efc5c3bc0081f43d6f06baac990e018c7",
        "path": "tests/fixtures/boundary-proof/simple-change/candidates/feature-spec.md"
      },
      {
        "identity": "sha256:733daae5d12b6123065196a5e93e8634a8dfc6019c4b3296bc5d96860f416d75",
        "path": "tests/fixtures/boundary-proof/simple-change/candidates/test-spec.md"
      },
      {
        "identity": "sha256:d1edc6c4c24e87d6bd52208a57ef273fe8a241641aa609b8eb96f5e464c26598",
        "path": "tests/fixtures/boundary-proof/simple-change/scenario.json"
      },
      {
        "identity": "sha256:0e83884b7eaf54af56bed53f20252855b532af8f8e5bf83a84f9524c2f666d53",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/current.json"
      },
      {
        "identity": "sha256:4281dc93ccdbbbfe345752090ac164f5f93aaa963a675cc51fc0f41c95e40366",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/feature-spec/portable-text-normalizer.md"
      },
      {
        "identity": "sha256:762c2a669f0dcc7c932fdad20f8d273a2c368cffc7a6e55b7a3117d34cde5561",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/review-evidence/spec-review-bundle.json"
      },
      {
        "identity": "sha256:9624cc815dce1f89bbff0dd0d382319f5bf85148d0ba73b97647c02760256ee8",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/review-evidence/spec-review-log.md"
      },
      {
        "identity": "sha256:d4ad6a99cc2081da66d09ca21f6bf04bd0dc765a567038182e2a1241c8640c56",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/review-evidence/spec-review-record.md"
      },
      {
        "identity": "sha256:3bfbf8afafebde3cde474e29d41a2d64da12ee81d1f2074258e69a8899c87c9f",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/review-evidence/test-spec-review-bundle.json"
      },
      {
        "identity": "sha256:8f2641b876249fbf1e09e82f7736524f5e929b9418a159058cc608463a024848",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/review-evidence/test-spec-review-log.md"
      },
      {
        "identity": "sha256:7e88165b329555284b4821438db073e22d0385a482ba7a82a0c5a5ad0031e45f",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/review-evidence/test-spec-review-record.md"
      },
      {
        "identity": "sha256:fe32c6712f9c2c5f88b52eb27bd8b7ef3f78ae942e109e1ca87f138519a41fb6",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/artifacts/test-spec/portable-text-normalizer.test.md"
      },
      {
        "identity": "sha256:776e425e261b321a59b529936c81a4ed239ce7c26e723e972b621ae68af3e7b4",
        "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/simple-change/runs/run-62735d2bff6ab29bfe208183cf33fc03/manifest.json"
      }
    ],
    "observations": {
      "false_blocking_count": 0,
      "final_feature_spec_snapshot_id": "output.feature-spec.one",
      "final_test_spec_snapshot_id": "output.test-spec.one",
      "new_universal_artifact_count": 0,
      "simple_fixture_structure_correction_cycles": 0
    },
    "operation_identity": "sha256:7617b819c29dc6852745d6a6b8a1c5df8a64c4bfe8c6821e6455c2a174ee4407",
    "result": "pass"
  },
  "simple_fixture_structure_correction_cycles": 0,
  "support": {
    "behavior-implementation-manifest": {
      "blocking_reason": null,
      "dependency_results": [],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:d23780b60c2eb0794d432a5cab22c436fd1586b938854985eebf414c96dc1430",
          "path": "AGENTS.md"
        },
        {
          "identity": "sha256:c175c4be7c31853fc4a7a6e3fe360756d8aaa3bba1409b7a876c957d3f57d0dd",
          "path": "CONSTITUTION.md"
        },
        {
          "identity": "sha256:f87c5dc2fbba64861ccf3aa2c333b278535e7c7165e36bd62b35650cd2c6b66d",
          "path": "docs/workflows.md"
        },
        {
          "identity": "sha256:a06a73b8304915cda130f5ef30341bc2565751ce8a0ab3ad8b45d8c34d14c1cc",
          "path": "scripts/boundary_proof_behavior.py"
        },
        {
          "identity": "sha256:ef2a23e4ecfe81de9958c960fd3de28a41fefd2b9767ccadb23b9ac7495bb67b",
          "path": "scripts/boundary_proof_model.py"
        },
        {
          "identity": "sha256:6cbe16074ffc500294e50a49237d27120c3d1ee17121ddd3966de44dbb263cfd",
          "path": "skills/spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:81e15833869bb5cec374fc08e8c05bacc78573fbff07a89d1c4ccee3b7d7db7d",
          "path": "skills/spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:245d22ceb249bc531e80ee83af69cdb1acb641fec0bf54bd266ff39937de4d4f",
          "path": "skills/test-spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:27336177f4f82e7a2dccb7ee7220a4494d3458d67653ccfe00dcd4bdfa4cad11",
          "path": "skills/test-spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:28fb8aaab0ff8405e3a325656feba8d6d570d43618bf7c802b2ea3961b0cd683",
          "path": "skills/workflow/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/workflow/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:c339ceed9592ec069cb94efd4774ad60ab9829983320fab1a3f22ea128e06ced",
          "path": "specs/rigorloop-workflow.md"
        },
        {
          "identity": "sha256:e627ff46ca104c7ec26114b42545e81500ecb2137540923f10bf5bd7c1eeccec",
          "path": "specs/rigorloop-workflow.test.md"
        },
        {
          "identity": "sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc",
          "path": "specs/skill-contract.md"
        },
        {
          "identity": "sha256:586e77d3b9587dcc016c447eb499eff5b0855ed0e77381b2368a4c62ca92da5d",
          "path": "specs/skill-contract.test.md"
        },
        {
          "identity": "sha256:431fd8011869f3619b1729d9eec9211b0d2b4684b4252afd611bbf3ac6499780",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/behavior-implementation-manifest.json"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:78bbcc47b4a26b55c33c553675d7a09e16370abb5f16c6a186858f878e90429a",
      "result": "pass"
    },
    "canonical-skill-resource-manifest": {
      "blocking_reason": null,
      "dependency_results": [],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:9a6a96eeb9040fab96b5bbacaee2eeb94fc20dfd3f1384419aec4362e3916274",
          "path": "skills/code-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/code-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:a4067a4510f223a06db178dcd5f1c63906ae459af89f34ad3068b20fa78b5ff3",
          "path": "skills/implement/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/implement/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:6cbe16074ffc500294e50a49237d27120c3d1ee17121ddd3966de44dbb263cfd",
          "path": "skills/spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:81e15833869bb5cec374fc08e8c05bacc78573fbff07a89d1c4ccee3b7d7db7d",
          "path": "skills/spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:245d22ceb249bc531e80ee83af69cdb1acb641fec0bf54bd266ff39937de4d4f",
          "path": "skills/test-spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:27336177f4f82e7a2dccb7ee7220a4494d3458d67653ccfe00dcd4bdfa4cad11",
          "path": "skills/test-spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:6b78a3daed2c54d6651a3263605627dd40e18564476fe87ff464315d4f8438ee",
          "path": "skills/verify/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/verify/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:28fb8aaab0ff8405e3a325656feba8d6d570d43618bf7c802b2ea3961b0cd683",
          "path": "skills/workflow/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/workflow/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:d3755beb0e8abb5a598a750faf34fef2d5c9887fa2aa32f64e209d5400c97fc4",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/canonical-skill-resource-manifest.json"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:2cf30132e3edb6fd1a5c380f27031defbdd0186e7b4da2a7c8be8ec4bb40ef78",
      "result": "pass"
    },
    "preservation-manifest": {
      "blocking_reason": null,
      "dependency_results": [],
      "diagnostic_id": "none",
      "evidence_refs": [
        {
          "identity": "sha256:d45b5577f797dc3922d9446c4d02709ad92dd67fcaa68e19c52e456bf44a1fab",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/boundary-proof-baseline.json"
        },
        {
          "identity": "sha256:f50e1f2219e8c13cdd2f7954d92743e2e153d4f97d3f7a6cb94909e4dc0d0bb8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/behavior.json"
        },
        {
          "identity": "sha256:0d69ff9b81334e9736e0a76ddd6d8c28a8327649d9bbffc50ca440710e8a226e",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/claim-boundary.json"
        },
        {
          "identity": "sha256:3c8cf6a5a6d03e6a2884bf5a89399ab1c6dfc0114fb174778f10d8b8d7a74f32",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/handoff.json"
        },
        {
          "identity": "sha256:5b406d8f6ed638965c51006928d62ddc0311652d063fc885a18292c8b7b86725",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/isolation.json"
        },
        {
          "identity": "sha256:57241a9fe3c2e483ce6696b3f21e031cbc3ff83cdad3bd15c90928b9cb45dd99",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/code-review/review-recording.json"
        },
        {
          "identity": "sha256:5334ccea66935293387661749a8feeaaf0dd0226d5a2181e2cbce4f5418fb52a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/behavior.json"
        },
        {
          "identity": "sha256:7ecb36d3c05aeeddb2b78766cbae90f6295ec3b38384586c2d24c48f177b88ff",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/claim-boundary.json"
        },
        {
          "identity": "sha256:3b5fed9bd3efcc071a9e2493f29b43bfe1a57f782570cb59e76bb2dd0c02c8ed",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/handoff.json"
        },
        {
          "identity": "sha256:ef74ea8687fb970d2016e73ba2a6ec1a63f2eea8c9c0c9d5661e7dbc7311bdd5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/isolation.json"
        },
        {
          "identity": "sha256:23b15998f827fd656b4d406f1bd31392cbb4bee0af13fce88aacd5944084c0e1",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/implement/review-recording.json"
        },
        {
          "identity": "sha256:5af151845c12a8caab00ea0869b835f2d8f53a114a411d155488ad25fa0b2a05",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/behavior.json"
        },
        {
          "identity": "sha256:0bfc05ce30ced5ccea2b85cf1c2a0b077473f20b1c0756643be461a0b28defc9",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/claim-boundary.json"
        },
        {
          "identity": "sha256:26dfde46c9746c1a79b8f5d1ea7412b2c87c08ada5f93ecb7823fcd20ce6b05d",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/handoff.json"
        },
        {
          "identity": "sha256:2496c47184288a2227e9f44d3fc36197fe2614e96a96de129b788066603bd7da",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/isolation.json"
        },
        {
          "identity": "sha256:85c958e32515185cda0897c276b04ea41a25c7816796696c4a6f6752e159a775",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec-review/review-recording.json"
        },
        {
          "identity": "sha256:50492a9268e542cddbc7cad373049159c9d552dcb64baa4c4f8a92bdd83ef3a6",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/behavior.json"
        },
        {
          "identity": "sha256:8a2c348a877985f482c2f33c1ff76abc8759091e5805156da88ae5caad4e9cc9",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/claim-boundary.json"
        },
        {
          "identity": "sha256:eb0d89b2c3179e0b97143d1dc8380dee669a5ea808d336504b92cf9c84929971",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/handoff.json"
        },
        {
          "identity": "sha256:c638b2331801571c2a9224e9420d8f0ef556692b34b9c9a180edfd4ad09dada5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/isolation.json"
        },
        {
          "identity": "sha256:3a132c49dd3ee6df4a082067b2f99e54f4232456bba2d926fc4b1634fbf0d55f",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/spec/review-recording.json"
        },
        {
          "identity": "sha256:76cafd6a9b453862452976214077adc4a50ffb03632ce3a0306b83b6b1537f5b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/behavior.json"
        },
        {
          "identity": "sha256:6055e4324d62bf2785c83519a0b8607c2a9257a1c4b81d1b5c7f615e3f3a1821",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/claim-boundary.json"
        },
        {
          "identity": "sha256:2b2421155abecc917dac8a2cce51a6509224552a46b68719d90d2260782580fa",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/handoff.json"
        },
        {
          "identity": "sha256:e009a2d43444d8690b24fb6a10cb5a8b252919dece2676f38845f0ba61ba2338",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/isolation.json"
        },
        {
          "identity": "sha256:a9aa65d0fc0ec5f0d349b49fc124cba584ec7a205531d557e43fab2ecacbaeca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec-review/review-recording.json"
        },
        {
          "identity": "sha256:b62af8bb712f5bc490d426108c018c249df2be744a39cd05325e094219a58a0c",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/behavior.json"
        },
        {
          "identity": "sha256:0c75c2eb70ba41498926cb797e7d79ce8a8fcda6ebe7d42295b0441d548734ac",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/claim-boundary.json"
        },
        {
          "identity": "sha256:f950e2cb2a786230c175ad7ec24e08a10b70a173b14279f8453d92b8fb58338a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/handoff.json"
        },
        {
          "identity": "sha256:998cf6e0484a2c8909df364737c31651253903bec571627b571255c91410312f",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/isolation.json"
        },
        {
          "identity": "sha256:a386fe777e2638f3d8bcf15583e2c15f361f5cb8864da2676a321f2f17ee6eb5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/test-spec/review-recording.json"
        },
        {
          "identity": "sha256:ca35a2bc223fd0a115a2a025d0cdd4878dadede1c40f7980666d3348ef82cbd2",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/behavior.json"
        },
        {
          "identity": "sha256:74206bdbf716208af4f2c79943cd146e7c4fb7d53edc7af3192a320e8fc483c8",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/claim-boundary.json"
        },
        {
          "identity": "sha256:bf36d0a678846220c6b57100747147dd826faadc95399c9d976137107e90deae",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/handoff.json"
        },
        {
          "identity": "sha256:3095b7dd573d03d66d3c5cb7feace82647a7a4f4d0199b7b3b41d8c1731beb78",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/isolation.json"
        },
        {
          "identity": "sha256:3023a123790e3a426f02b34b05144e2c7ce1b6973aec7ff8c83df96caacd0f52",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/verify/review-recording.json"
        },
        {
          "identity": "sha256:50d7de6d0e11a5a205b79e13ebc8ccf43d80ab746fcc1d696f7028d9a819275d",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/behavior.json"
        },
        {
          "identity": "sha256:68e63bc76ffba542f76476a02f479c1465ad3051fd39029618909439a74a0e28",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/claim-boundary.json"
        },
        {
          "identity": "sha256:1c6f44c746dda6e080a5743ac8c9eaabe5971376166aaab8fa8de0dbcdad9b33",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/handoff.json"
        },
        {
          "identity": "sha256:218e54623639d127f03203bfb3c689bb071100ea98a5ee8349d744d6a12bac4a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/isolation.json"
        },
        {
          "identity": "sha256:4354f847a50d2aac73757babc4145a90b496e747c698cc5dbd3a518d8bf427b6",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/after/workflow/review-recording.json"
        },
        {
          "identity": "sha256:9a6a96eeb9040fab96b5bbacaee2eeb94fc20dfd3f1384419aec4362e3916274",
          "path": "skills/code-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/code-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:a4067a4510f223a06db178dcd5f1c63906ae459af89f34ad3068b20fa78b5ff3",
          "path": "skills/implement/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/implement/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:6cbe16074ffc500294e50a49237d27120c3d1ee17121ddd3966de44dbb263cfd",
          "path": "skills/spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:81e15833869bb5cec374fc08e8c05bacc78573fbff07a89d1c4ccee3b7d7db7d",
          "path": "skills/spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:245d22ceb249bc531e80ee83af69cdb1acb641fec0bf54bd266ff39937de4d4f",
          "path": "skills/test-spec-review/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec-review/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:27336177f4f82e7a2dccb7ee7220a4494d3458d67653ccfe00dcd4bdfa4cad11",
          "path": "skills/test-spec/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/test-spec/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:6b78a3daed2c54d6651a3263605627dd40e18564476fe87ff464315d4f8438ee",
          "path": "skills/verify/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/verify/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:28fb8aaab0ff8405e3a325656feba8d6d570d43618bf7c802b2ea3961b0cd683",
          "path": "skills/workflow/SKILL.md"
        },
        {
          "identity": "sha256:d8fb036b6ce87dc10e1d2d03774ace33c0dc8abd5ac8abfd1e9024b7c85d5aea",
          "path": "skills/workflow/references/boundary-proof-model.md"
        },
        {
          "identity": "sha256:3a97deceab2d4807d39d013e888022b2baf1cddca76409c39a9320dcd0aac57f",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/manifest.json"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/behavior.md"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/claim-boundary.md"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/handoff.md"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/isolation.md"
        },
        {
          "identity": "sha256:7a9a46e91ff646d2cef7cd4758d07c43a803a160dc95ae05e675389710af752b",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/code-review/review-recording.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/behavior.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/claim-boundary.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/handoff.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/isolation.md"
        },
        {
          "identity": "sha256:ae27f31e1a60f163052163422471741baaf53139be4915b811af7c48277827ca",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/implement/review-recording.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/behavior.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/claim-boundary.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/handoff.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/isolation.md"
        },
        {
          "identity": "sha256:ea414731b1e464e7ef29af6a31458e061d8768781e41aaf43f5c969185df2631",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec-review/review-recording.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/behavior.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/claim-boundary.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/handoff.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/isolation.md"
        },
        {
          "identity": "sha256:8c7dc8892e0fdd57f81f84ced1a9604e17d6ef9eb0ab94ccfd88cb44549f11b5",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/spec/review-recording.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/behavior.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/claim-boundary.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/handoff.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/isolation.md"
        },
        {
          "identity": "sha256:d746b2b371fb7c1263cd836c4c8ee8b6878bf4e41549776610179a0270d5984a",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec-review/review-recording.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/behavior.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/claim-boundary.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/handoff.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/isolation.md"
        },
        {
          "identity": "sha256:4aace06ea479bfbe427b53ae54531d8833f3f1ed9f4bda88907e6cc68f99f717",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/test-spec/review-recording.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/behavior.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/claim-boundary.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/handoff.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/isolation.md"
        },
        {
          "identity": "sha256:3a075c2beb84913c7248c163c1685fa70a2bc0f434ab73170f197cc901832867",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/verify/review-recording.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/behavior.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/claim-boundary.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/handoff.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/isolation.md"
        },
        {
          "identity": "sha256:0917ca47aa179b2a2e84f5a4319d685626fb0c0c6371732dc2106560d75ee5ea",
          "path": "docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/run-21e1ee9615edbaa0feb47ea0905d2c1b/before/workflow/review-recording.md"
        }
      ],
      "observations": {},
      "operation_identity": "sha256:87baad80eb26078837ac3fe5d5d096e2daadc16d48b441f1bf46a0a4b27667c8",
      "result": "pass"
    }
  }
}
```
