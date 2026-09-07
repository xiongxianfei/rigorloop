---
{
  "schema_version": 1,
  "change_id": "2026-09-07-targeted-recording-primary-cli",
  "id": "code-review-m5",
  "target": "code",
  "reviewer": {
    "id": "m5-code-review",
    "role": "review"
  },
  "contributors": [
    {
      "id": "codex-root",
      "role": "implement"
    }
  ],
  "independence_basis": "Separate delegated reviewer independently reviewed all M5 changed implementation/guidance/package/test subjects at eaf9f44e, the exact approved model and plan basis, resource-closure dispositions and current execution evidence without authoring implementation. Recorded m5-cr-001 before correction, reread the two-phase fix, independently ran all seven final interaction/adoption tests, checked every M5 evidence subject and all 79 unchanged mapped resources, and assessed the controlled token results. Separately delegated Design Review classification is explicitly attributed in the existing design-review body; it does not retarget the original structured assessment. codex-root authored M5; reviewer owns this bounded Code Review. This is not final whole-change Code Review.",
  "subjects": [
    {
      "path": "AGENTS.md",
      "identity": "sha256:e84ddf0ea91213b89a76771b83e1a90689f5ee7fd2bcd4ee993a39f5321c7509"
    },
    {
      "path": "CONSTITUTION.md",
      "identity": "sha256:1a9962b1f3166b1b39fd8a99a1139ab31d0e9aa1ea6563215acfb5667d101c1f"
    },
    {
      "path": "dist/adapters/README.md",
      "identity": "sha256:f2a1939e435f7eb91b6c4a258169a15b2cfa94b620baefca21ed6e08fbf57f37"
    },
    {
      "path": "docs/architecture/system/architecture.md",
      "identity": "sha256:a8cdcf94d4aa4255ee5262bd338e8ca89813af4cbabc44b7bb6723931e2eb70c"
    },
    {
      "path": "packages/rigorloop/README.md",
      "identity": "sha256:84bf946cd45d80b0c0f1ef6dc34760d3461cee65e78d205a6eb42b072688d2c2"
    },
    {
      "path": "packages/rigorloop/dist/metadata/adapter-artifacts-v0.5.1.json",
      "identity": "sha256:f551e0039f52207234a20f2790b61210914de5ad43811b45f0ec394c4d97b646"
    },
    {
      "path": "packages/rigorloop/dist/metadata/releases.json",
      "identity": "sha256:16a3abd25399e7e59799df704d5aa07658c6e8886b12ebfa52d5403c1c091828"
    },
    {
      "path": "packages/rigorloop/test/cli.test.js",
      "identity": "sha256:a0cd778988994a42d018876b514e17e0371c2a71e44c5546ba3a7af9ae747daa"
    },
    {
      "path": "packages/rigorloop/test/fixtures/recording-interactions/README.md",
      "identity": "sha256:6d9e643a22c2e84f7b5c5dcb560fd872617c253d8135f73ef3610d7b4913ac81"
    },
    {
      "path": "packages/rigorloop/test/helpers/record-store-interactions.mjs",
      "identity": "sha256:9afe5f23fdc1c761488ddd810fad525b55a380011ddfb891026ab64bb1bfae98"
    },
    {
      "path": "packages/rigorloop/test/helpers/record-store-tokenize.py",
      "identity": "sha256:594cf6f36b3092f92f55953e4cf3a0603e0333af5f52f763601fbf9931ae1d9a"
    },
    {
      "path": "packages/rigorloop/test/record-store-adoption.test.js",
      "identity": "sha256:38c35af0ebd1fb7601fc8a8524eda916bdce1a73a77634751614b9c2820eb1b0"
    },
    {
      "path": "packages/rigorloop/test/record-store-interactions.test.js",
      "identity": "sha256:88b3c1ade09faca57b8a85f0b56a82c19cf3b8c5f89a9d31c6234b74485494f4"
    },
    {
      "path": "scripts/skill_validation.py",
      "identity": "sha256:cf0c653b6af5de161b5b03d50e4b1a6e834db856a42af8531e2c2c627a2d3e61"
    },
    {
      "path": "scripts/test-adapter-distribution.py",
      "identity": "sha256:fd9c8133e9069d7034fa16e8d4c03ffac4783ef7b4b0d5216e8fec8b5e7c2c5d"
    },
    {
      "path": "scripts/test-change-metadata-validator.py",
      "identity": "sha256:d9323bfd13fdced81847271eea344c26d198e1769b058650996976281e788c12"
    },
    {
      "path": "scripts/test-npm-package-publication.py",
      "identity": "sha256:808e00cda575d046d98e799b55b3bdef673c05a11eb2427fb7252dacc13fe1ae"
    },
    {
      "path": "scripts/test-select-validation.py",
      "identity": "sha256:adeea088ad41206dbc6514f7e04b0d677dfca6461f184037c5cfc18783576e18"
    },
    {
      "path": "scripts/test-skill-validator.py",
      "identity": "sha256:082951d1c8d22daf1f1a525adcb1cc00560c052643d36991240c9ae28a714106"
    },
    {
      "path": "scripts/validate-change-metadata.py",
      "identity": "sha256:2ba186075ec44e516a2cd638cd5edfb42c90a90fda08ce4b623655d47e89589f"
    },
    {
      "path": "scripts/validation_selection.py",
      "identity": "sha256:e705e7ae809e669c8817ab1f21855b292c095cee83e2bb56029830ee7268f3ed"
    },
    {
      "path": "skills/architecture/SKILL.md",
      "identity": "sha256:af2b685a29324851a7ab3c05c18411928a72a4c181e487c4eb7024cad8d7cb6a"
    },
    {
      "path": "skills/bugfix/SKILL.md",
      "identity": "sha256:8040e5f405773e381eb3cbbdfcdd75a1162ac71198b749ea6f909dddf8bcc168"
    },
    {
      "path": "skills/ci-maintenance/SKILL.md",
      "identity": "sha256:466cf560375c34fbe112b785491d47c07bfc5b1a8d604c06eb7eb004a667b454"
    },
    {
      "path": "skills/code-review/SKILL.md",
      "identity": "sha256:cd50ec999b33775b90c7fa2213a6df1d954e89338cf8759ed4d2fff730e3d864"
    },
    {
      "path": "skills/delivery-review/SKILL.md",
      "identity": "sha256:c9206e6dedad3d71ebb72773130d1aeebadbc240e96eaa9361a2f47ad34904ed"
    },
    {
      "path": "skills/design-review/SKILL.md",
      "identity": "sha256:ab39e151fda182b37af7000a19fd6555447efd9d8e9bda9f588334d7aa6e9874"
    },
    {
      "path": "skills/explore/SKILL.md",
      "identity": "sha256:50427e5ef1214666211ac1c769e83e0290329e35e11772f8961c39d501eb294f"
    },
    {
      "path": "skills/implement/SKILL.md",
      "identity": "sha256:705873dc7b39ba5712798f1e9b9b58e5fd7fd3aaa3d388be92bdf7ad3b0014c5"
    },
    {
      "path": "skills/learn/SKILL.md",
      "identity": "sha256:93d39ee13cf4e039dc0bec74a00a603ca3bc8588a1ef2cb0c49649e6675c4a00"
    },
    {
      "path": "skills/plan/SKILL.md",
      "identity": "sha256:06aeb75243eb4a54985ef11101500abf9bab86dba9a77945b911ad210c3f4c88"
    },
    {
      "path": "skills/pr/SKILL.md",
      "identity": "sha256:39d94432a201eb768bc610ebe19ab7926d05c8a487aa460b966bc1a0b724ae30"
    },
    {
      "path": "skills/proposal-review/SKILL.md",
      "identity": "sha256:a5b8203401338d1784216216012e87f1f687f5a89aa342a7d715cf9c0bb96ade"
    },
    {
      "path": "skills/proposal/SKILL.md",
      "identity": "sha256:71b0c787833e43b7fdc7bb4e1bbc052fde273874accead5b1155b234481a4902"
    },
    {
      "path": "skills/research/SKILL.md",
      "identity": "sha256:9205aefba69f3be8e924960922c92878fd2d05d24d3181e518eaf2ea917d922a"
    },
    {
      "path": "skills/route/SKILL.md",
      "identity": "sha256:60edf979c178d0a3c3c1a97e5c4ca739ddad610e71f2e549c97419df0f965c1a"
    },
    {
      "path": "skills/spec/SKILL.md",
      "identity": "sha256:4196c940f8d2f0b79b22db1cfea9a564e10e703143a0a6198d3d37183031e858"
    },
    {
      "path": "skills/verify/SKILL.md",
      "identity": "sha256:49260a6226269f17956fd705e7d5be7a62346f402f8299ae52b318c95fefcf73"
    },
    {
      "path": "specs/compact-current-state-change-record.md",
      "identity": "sha256:897a80e87c142fbc7abdab7be71c64a8e8d7b09fee49467374e3e678185bafe5"
    },
    {
      "path": "specs/governed-lifecycle-cli.md",
      "identity": "sha256:4dff8478a17c5689516f22ad9f29d92311a38e2f73e84c40319f9bf5faab5714"
    },
    {
      "path": "specs/rigorloop-workflow.md",
      "identity": "sha256:0eae07ea872452fe203d01d50049b47e5df97b82542237af520d644671198cbc"
    },
    {
      "path": "specs/skill-contract.md",
      "identity": "sha256:ced40b68fc8c4e610b3bd66b19c10d4f8c0b2c394cd14adf95cd18c41cf35ca3"
    },
    {
      "path": "docs/design/cli/cli.md",
      "identity": "sha256:951c0f427e118914d70c1f326a02ae01efab47107a1cca897211b980b9d8d22c"
    },
    {
      "path": "docs/design/workflow/workflow.md",
      "identity": "sha256:a3727f571eec0f9ae34bfdda31f9f7711e3903abdabd31e28903b8c3b69b2251"
    },
    {
      "path": "docs/design/record-format/record-format.md",
      "identity": "sha256:6ddfcd350212437ddf2feaade14818fd66f9a04b8a00ccb01c5fb13291879eeb"
    },
    {
      "path": "docs/plans/2026-09-07-targeted-recording-primary-cli.md",
      "identity": "sha256:2078ea15010d79a50941cc3bfaa80fa02d521972bb97c6cc01ee2e89cc5d393d"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
      "identity": "sha256:d12794ca199b9b7c0053a6b29113496084a2c6b35484cfc3bc3054408bc7a045"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/design-review.md",
      "identity": "sha256:0719f7cb5aa5e02f0bbb0bd80cfc72e94396f0f2ceeaba95a8688082bb3bac3f"
    },
    {
      "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/reviews/delivery-review.md",
      "identity": "sha256:f4ffd37cc3aa73448cf05c6731663c96cc18c62de040928619fddf35209ccb8d"
    }
  ],
  "judgment": "approved",
  "findings": [
    {
      "id": "m5-cr-001",
      "reporter": {
        "id": "m5-code-review",
        "role": "review"
      },
      "owner": {
        "id": "codex-root",
        "role": "implement"
      },
      "subjects": [
        {
          "path": "packages/rigorloop/test/helpers/record-store-interactions.mjs",
          "identity": "sha256:661f95ab8a28954437fafa382e465c3f43c7dfd4c821623beb09157698da9b74"
        }
      ],
      "evidence": "Finding ID: m5-cr-001. Severity: minor. Location: decisions() applicability-reassessment and runInteraction(). The named scenario starts from current applicability and only records one review reassessment with current applicability and a new reason. It does not explicitly revise applicability then later record reassessment as required by CLI token-evaluation procedure and M5 TG-08. Therefore the reported full interaction excludes the initial decision/write and intermediate reads required by that selected scenario.",
      "required_outcome": "Implement equivalent two-phase controlled interactions: explicitly change applicability, inspect the resulting current state/basis as needed, then later record reassessment and its applicability decision. Count both interfaces complete requests/responses/help and all follow-up reads; assert intermediate and final semantic equivalence, rerun pinned token evaluation, and disposition unfavorable/inconclusive results through Design before adoption recommendation. Safe resolution is benchmark implementation; no new numerical threshold.",
      "state": "resolved",
      "resolution": {
        "actor": {
          "id": "m5-code-review",
          "role": "review"
        },
        "rationale": "The applicability scenario now records an explicit stale declaration, reads its current state, then separately records review reassessment/current applicability and reads the result. Both interfaces compare intermediate and final semantic checkpoints and count both writes plus required help/reads. Independent interaction tests pass; pinned full-interaction remeasurement supports the bounded qualitative benefit.",
        "evidence_refs": [
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m5-recording"
          },
          {
            "path": "docs/changes/2026-09-07-targeted-recording-primary-cli/evidence.yaml",
            "id": "m5-token-evaluation"
          }
        ]
      }
    }
  ]
}
---
# M5 independent Code Review

Review status: clean-with-notes. Stored judgment: approved. This assessment covers the complete M5 increment at eaf9f44e only. Finding m5-cr-001 was recorded before correction and is resolved after independent rereview. Its original supporting evidence and subjects remain unchanged.

Reviewed every changed M5 implementation/guidance/distribution/test file, the approved three-model and delivery allocation, all 17 canonical stage/support profiles, scoped governance/spec/architecture navigation, metadata and selector routing, validation changes, generated candidate metadata, supported archive mapping, installed-package proof, controlled benchmark and public integration fixtures. Mutable routing and this review record are not self-referential subjects. All current M5 execution-evidence subjects and all 79 mapped resource subjects matched their recorded hashes. Unchanged resource dispositions preserve historical procedures under their contracts and retain substantive engineering methods; no required resource dependency is silently deferred.

| Checklist | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | M5 TG-07/TG-08 and allocated TG-FINAL integration implement CLI-SR-18, RF-SR-06/08 and WF-SR-03/07/08/09/10/11 without new workflow authority. |
| Test coverage | pass | Independently ran seven interaction/adoption tests successfully; registered m5-recording reports 184 passing recording tests and public cross-contract integration. |
| Edge cases | pass | Public v1/v2 correction, stale retry, interrupted batch/recovery, final explanation retrieval, B-to-C observation drift and nearly full one-MiB evidence remain covered. Two-phase applicability benchmark checkpoints are equivalent. |
| Error handling | pass | Unknown contracts fail closed; missing/stale evidence prevents reliance without preventing valid correction recording. Resource/archive parity and package-boundary failures retain owner-specific checks. |
| Architecture boundaries | pass | Workflow meaning, Record Format storage and CLI mechanical ownership remain distinct. Profiles use explicit scoped context, subject identities and targeted commands; no normal manual reconstruction or legacy eligibility path remains. |
| Compatibility | pass | Existing v1 and historical procedures retain explicit scope and identities; v2 primary creation is explicit. Historical skill-size tests retain their original measured profile while current complete guidance is counted by TG-08. |
| Security/privacy | pass | Independent review and actor-specific finding/blocker disposition remain duties; labels and saved results grant no authority. External publication/merge/release permissions remain separate. |
| Derived artifact currency | pass | Canonical profile bytes match Codex/Claude/OpenCode generated archives; regenerated local candidate metadata and installed CLI schema/template parity have current evidence. No generated archive or installed skill is authored. |
| Unrelated changes | pass | All changes correspond to approved M5 adoption surfaces or their necessary tests/metadata. Original stage introductions and historical remainder are preserved. |
| Validation evidence | pass | Current evidence: recording 184; package 649 plus 2 historical skips; skill 367; metadata 116; boundary 87; selector 164; adapter 158; publication 7; release 104. Schema/model, selected checks, skill build, guide/prose audits and owning metadata validation pass. |

The two grandfathered spec amendments are new-profile-only adoption amendments. The separately delegated independent Design Review classification in the existing design-review body names exact spec/model/plan identities and preserves original assessment attribution and historical remainder. No new Design decision or historical feature-format adoption is needed for these exact amendments. This Code Review relies on that Design-owned classification rather than substituting its own judgment for it.

TG-08 acceptance assessment: the revised scripted comparison preserves intermediate/final decisions and neighboring records, and the fixture's single narrow model is an adequate complete engineering basis for these selected operations. Complete loaded skill guidance, operation help, engineering read/hash, commands, requests, responses, selected preview and follow-up reads are counted with tiktoken 0.12.0 / cl100k_base and Node v24.14.1. The advanced comparison uses identical v2 fixtures with an explicitly counted amendment to historical guidance; it is not presented as a shipped v2 normal interface.

| Controlled task | Advanced tokens / calls | Targeted tokens / calls |
| --- | --- | --- |
| Finding with neighbors | 60,449 / 5 | 5,460 / 6 |
| Failed Verify correction | 39,136 / 4 | 7,835 / 6 |
| Applicability then reassessment | 63,412 / 6 | 5,439 / 8 |
| Final explanation read | 17,707 / 1 | 2,523 / 1 |

The results support reduced routine reconstruction and avoidable context for these selected tasks while retaining adequate basis and safety. More targeted calls are included in the total, not hidden. This is successful scripted-interaction evidence, not free-form agent trials, universal savings or a numerical adoption threshold. Retry/recovery correctness is separately proved; no successful recovery cost is omitted from these successful traces. No unfavorable or inconclusive result requires a new Design disposition here. Future different measurements must receive an honest owning decision before an adoption claim.

Reviewed milestone: M5. Milestone closeout: closed at the independent review boundary; Route owns recording work state. Required review-resolution: none outstanding; m5-cr-001 resolved. Remaining implementation milestones: none after Route closes M5. Next mandatory checkpoint: separate final whole-change Code Review of integrated M1-M5 subjects before M6 Verify. This M5-only assessment does not satisfy that checkpoint. Recording status: recorded. Review log and separate resolution ledger: not required by the selected explicit-recording-v1 contract.

The package is a coherent local candidate for further closeout review; release/customer activation is not authorized or performed. Final whole-change correctness, successful Verify, final closeout readiness and branch/PR readiness are not claimed. Existing external-editor limitations remain unchanged.
