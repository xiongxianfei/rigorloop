# Explicit Recording M3 — Advisory Code Review

## First-pass result (historical)

- Skill: code-review
- Status: completed
- Artifacts changed: this review only
- Open blockers: ER-M3-001 requires a bounded validator correction
- Next stage: isolated M3 correction and independent rereview; no automatic downstream handoff
- Review status: changes-requested
- Material findings: ER-M3-001
- Recording status: recorded (advisory only)
- Recording blocker: none for this explicitly assigned location
- Review record: `docs/reviews/explicit-recording-m3-code-review.md`
- Review log: not applicable
- Review resolution: dispositions belong in this record
- Reviewed milestone: M3 under explicit isolated user authority
- Milestone closeout: resolution-needed; no formal settlement claimed
- Remaining implementation milestones: M4–M5, outside this invocation
- Required review-resolution: yes
- Finding IDs: ER-M3-001
- Verify readiness: not-claimed

## Scope and independence

The reviewer authored none of this implementation or guidance. Basis: both current model documents, their approved advisory model-mapping rereview, the existing advisory Delivery M3 allocation, M2's clean-with-notes record and [M3 implementation evidence](../implementation/explicit-recording-m3.md). The reviewed diff is limited to the explicitly inventoried M3 amendments below. Existing compact implementation changes and other dirty work are excluded. The user-authorized one-file-per-model design, no OS investigation and approved external-edit limitation remain intact. No implementation was fixed before recording this finding.

## Finding ER-M3-001

- Finding ID: ER-M3-001
- Severity: minor
- Location: `scripts/boundary_first_validation.py:1834`, required-heading/table parsing in `validate_model_record`
- Evidence: The parser strips arbitrary indentation when locating headings and collecting table rows. It therefore recognizes Markdown indented code as the required authoritative sections. An otherwise-valid Workflow model fixture with the entire `## Requirements` and `### Boundary scan and acceptance scenarios` sections indented four spaces has zero live required headings, yet `validate_model_record` returns no issues. The existing fenced-code regression covers another example form, not this one. Workflow's Model validation and proof mapping requires each actual heading/table once; examples must not supply normative authority. A structural pass is incorrect even though it confers no semantic approval.
- Required outcome: Required headings/tables must be recognized in live document structure, not from indented code examples. Retain valid ordinary headings/tables and the existing fenced/comment handling.
- Safe resolution path: Add an otherwise-valid indented-code regression and narrowly correct model parsing so those sections cannot satisfy the contract. Include applicable indentation variants without changing historical feature-parser behavior or adding a new model format. Independently rereview the correction.
- needs-decision rationale: None; this is an implementation mismatch with the reviewed mapping, not a new Design choice.

The read-only reproduction loaded `docs/design/workflow.md`, prefixed four spaces to every nonempty line in each of the two required sections until the next heading, and called `validate_model_record(candidate, 'docs/design/workflow.md')`. Output: `live Requirements headings: 0`, `live scenario headings: 0`, `validator issues: []`. No file was modified by that probe.

## Checklist

| Item | Assessment | Evidence |
| --- | --- | --- |
| Spec alignment | concern | ER-M3-001 accepts absent live structural authority. Other mapping rules are represented: explicit marker, safe path, closed dimensions and local references. |
| Test coverage | concern | Seven model tests and two workflow tests pass; indented-code authority is not covered. |
| Edge cases | concern | Fenced examples are rejected, but indented examples can bypass required live sections. Missing/duplicate/unknown references and symlinks have focused tests. |
| Error handling | concern | Invalid model structure can be reported as passed; no recording or lifecycle mutation is performed by the validator. |
| Architecture boundaries | pass | Document validation is separate from record-store and semantic review; CLI-only fixture access remains unadopted. |
| Compatibility | pass within scope | Historical parser/activation flow is retained; model-only checks explicitly skip lifecycle activation, and mixed checks retain it. Ordinary adoption remains M4. |
| Security/privacy | pass within scope | Selected model paths are contained/nonsymlink; guidance preserves ownership and does not authenticate reviewer role text. |
| Derived artifact currency | pass on named evidence | Canonical skills validate; coordinator reports disposable skill generation check passing after quick-guide relocation. No installed/generated-adapter approval claimed. |
| Unrelated changes | pass | Seven governance/doc amendments, eleven stage profiles and named tooling/proof surfaces only; unrelated dirty changes preserved. |
| Validation evidence | concern | Named checks pass but miss the reproduced parser case; walkthrough and simulated actor tests are distinguished. |

## Guidance and scenario assessment

The eleven prospective stage profiles consistently select model-owned shapes and explicit recording while retaining substantive duties, permissions, independence and proof. Author/reviewer/route/Verify responsibilities remain separate. Historic transition/scaffold procedures are not made new-contract prerequisites. Quick-guide relocation changes placement, not duties. Governance scopes the prospective profile without activating writers or converting records.

The automated workflow scenario exercises actual fixture-dispatch recording: model drift leaves review bytes unchanged, applicability and reopening are explicit, Verify failure creates a blocker without a success report, and only submitted replacements resolve findings/complete activity. Its actor labels are correctly disclosed as simulated data, not provenance. The separately conducted walkthrough recorded in implementation evidence supplies an independent negative judgment: stale same-contributor approval and missing acceptance evidence did not justify completion; original findings persisted through four real check/record/inspect cycles. This reviewer read that evidence, rather than claiming to have conducted those cycles. No further material guidance issue was identified in the reviewed scope.

## Exact reviewed subjects

SHA-256 identifies complete current files; the reviewed ownership remains the bounded M3 diff.

| Path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `ade7635a4a8fb1f7e0fcc98e6c0f69c462e8a022899307cc7d1cb57d97c35148` |
| `CONSTITUTION.md` | `a6ea04fd7fa960486326108426758809090c8db75033a5962ec5266e56cab7f5` |
| `docs/architecture/system/architecture.md` | `20c093ca75a3b6e3780c6449d83ccc7f58bef60a0a83a7c1dcedde9f31e95856` |
| `specs/rigorloop-workflow.md` | `af9ec40714a995e1e4faffafbdf77b8763d66da9eb295ce8a1fcc93baf0d4956` |
| `specs/compact-current-state-change-record.md` | `2663991a0244c0d3c4c9731f00f8548368203978edbf94b8011ef97d9f8863e9` |
| `specs/skill-contract.md` | `85d9f928eb4bfcf1d89c186848011524d01aab97a1fba40ccac39cb763ac65fe` |
| `specs/boundary-first-proof-model.md` | `84064a4e8e538d94daad1fdf35e4119b0a83f8ee789b8a4ebd11466fffa94bdc` |
| `skills/architecture/SKILL.md` | `901a9178c496510aa454fb66b3b2f64bed4b3f9eabddc6e408c22c65de39ba1e` |
| `skills/spec/SKILL.md` | `b9ab180a44a925b9f8ae9c79292fc6a34f5328f95de9fc93ebde0692b740bba2` |
| `skills/route/SKILL.md` | `6b910ec60dffe35522ff8005f4c1bedcb736316989ca2983cc8360ff89648d7f` |
| `skills/proposal/SKILL.md` | `9517712d80bde49775705bc6f33dcd85149e0b33a2cacd273cb1fdaa463e7482` |
| `skills/proposal-review/SKILL.md` | `060ce2232a3329d1f20a078a74bdfc4201af9a0f52836aa737812e09f5a19f9a` |
| `skills/design-review/SKILL.md` | `40ae00f4c428b911a53db67d69b2fb7aeffe26312c2b44d59d6862cdef2d33b9` |
| `skills/plan/SKILL.md` | `37977c7cc2f1ed490088d0edfd6b55039623c76854a8736167a91a5d6bc85996` |
| `skills/delivery-review/SKILL.md` | `e1f01e7b89593b5296d11a0bc015a34b8be5ef87d628d6e0b64abf48354578a1` |
| `skills/implement/SKILL.md` | `bb58c953af90badaa51d18eb69a8dd9b14bc5d1337008b16db880ff4b1df4673` |
| `skills/code-review/SKILL.md` | `f0c0aaa4f1ad31fd9cc9ce618c50835ce5fd5cf5fa0f12169d939bce2cf2e283` |
| `skills/verify/SKILL.md` | `3b5906fd21eb7496b49aaf1e7c90aba0cb25079742d5250e234fd70be17211af` |
| `scripts/boundary_first_validation.py` | `9026d5f288436d58a590f949ea6601bab10ac1d79913e7aa9831376a0e2b941f` |
| `scripts/validate-boundary-first.py` | `8d6cd1d2f89df6c31cd4c2505a18a282aa19b5dc57daf087a0c4dc3a8bafa1ab` |
| `scripts/test-boundary-first-validation.py` | `c2ad7e8e247cae963632e339cf53a2280c1545c19ea4329acd70be6f5ef80d25` |
| `scripts/test-skill-validator.py` | `080fa0e3a02022c8af5c458c6bdcfad1a36760dca51041091a15c9225b7e6702` |
| `packages/rigorloop/test/record-store-workflow.test.js` | `af1128be485790dafdc27a0630e5814b830fe3ad3579dfb1e5922e7ef431caa7` |
| `docs/implementation/explicit-recording-m3.md` | `5862bbdb3304569b80d85ae0e889e8c88c7a17528eba356cb0fae1596088c88c` |

## Commands and limitations

Independently run: `python scripts/test-boundary-first-validation.py ModelRecordTests` (7 passed), `python scripts/validate-boundary-first.py --check --path docs/design/workflow.md --path docs/design/cli.md` (passed, structure-and-references-only), `python scripts/validate-skills.py skills` (20 canonical skills validated), and `node --test packages/rigorloop/test/record-store-workflow.test.js` (2 passed). The read-only Python indented-code probe reproduced ER-M3-001; source inspection used `git diff`, `sed`, `rg`, `cat` and exact subject hashes.

Coordinator-run evidence reports all 77 boundary tests, 366 skill tests, package 525 total / 523 passed / two existing skips / zero failed, disposable skill generation, schema parity and whitespace checks passing. Those broad checks were not independently rerun here. No public activation, generated-adapter scenario, final holistic review or Verify was performed. This first-pass record precedes correction; the reviewer made no source or lifecycle edits and stops before M4.

## Current correction rereview

- Skill: code-review
- Status: completed
- Review status: clean-with-notes
- Recording status: recorded, advisory only
- Artifacts changed by reviewer: this review only
- Finding disposition: ER-M3-001 resolved by independently reviewed implementation correction
- Open material findings / required review-resolution: none in reviewed M3 scope
- Milestone closeout: advisory M3 review complete; no formal settlement
- Next stage: stop at this requested review boundary; M4–M5 remain outside this invocation
- Verify readiness: not-claimed

The model-only table reader now excludes lines indented at least four columns, including tab-expanded indentation, before recognizing headings or rows. It preserves ordinary zero-to-three-space indentation and does not change the historical parser. The new otherwise-valid regression rejects all six whole-section/table-only combinations of four spaces, tabs and mixed indentation; its three-space positive control passes. This satisfies ER-M3-001 without changing the approved model format. No additional material finding was identified in this bounded correction rereview.

Current checklist: spec alignment, test coverage, edge cases, error handling and validation evidence now **pass** for the corrected issue. Architecture boundaries, compatibility, security/privacy, derived artifact currency and unrelated-change scope retain the first-pass **pass within the stated scope/evidence limits**. Structural validation still does not establish semantic adequacy, independent approval or lifecycle completion.

### Corrected subject identities

These SHA-256 identities replace the three corresponding first-pass subjects for this rereview; the remaining implementation subjects and their scoped assessments are unchanged.

| Path | SHA-256 |
| --- | --- |
| `scripts/boundary_first_validation.py` | `2faf8ec25f599168e7751801f9c92876a67d4d414db4d0f72e42ffb1da91bd3b` |
| `scripts/test-boundary-first-validation.py` | `a72bc0e310855278ee36f9ca0bc7398b1a9c69274d7a720afdbbe053962915d5` |
| `docs/implementation/explicit-recording-m3.md` | `4a4b6b9a34ae19c1d67ceb87237f578ae2574a33c549b60fca9fb9105626b0f1` |

Independently rerun: `python scripts/test-boundary-first-validation.py ModelRecordTests` (8 passed), `python scripts/test-boundary-first-validation.py` (78 passed), and `python scripts/validate-boundary-first.py --check --path docs/design/workflow.md --path docs/design/cli.md` (passed, structure-and-references-only). The coordinator's earlier 366 skill tests, disposable generation and 525-total package run remain evidence on unchanged subjects, not newly rerun reviewer proof. Implementation evidence intentionally remains the author's correction handoff; this review owns the independent disposition.

The first-pass reproduction and finding above remain historical evidence. No implementation, Design, plan, lifecycle state, public activation or M4 work was changed or authorized by this rereview. Generated-adapter execution and final integrated/whole-change review remain downstream work.
