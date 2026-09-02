# Code Review M5 R1: Atomic V3 Publication Candidate

Review ID: code-review-m5-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review agent
Target: M5 implementation commit `85ec0825`; workflow handoff commit `17140ccb`
Reviewed artifact: exact M5 range `60136823..17140ccb`
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded
Material findings: FV-M5-CR1, FV-M5-CR2
Reviewed milestone: M5

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-m5-r1.yaml`, `review-log.md`, and `review-resolution.md`
- Open blockers: `FV-M5-CR1`, `FV-M5-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M5-CR1`, `FV-M5-CR2`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m5-r1.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M5
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5, M6
- Required review-resolution: yes
- Finding IDs: `FV-M5-CR1`, `FV-M5-CR2`
- Verify readiness: not-claimed

## Scope and authority

Reviewed the complete M5 candidate range against the accepted proposal, approved Design Review R2 package, approved Delivery Review R3 plan, M5 TG-19 through TG-23, FV-R1 through FV-R7, FV-R35, FV-R37, FV-R38, all eight approved boundary classes, INT-001 through INT-004, and the M5 implementation evidence. The review inspected lifecycle selection and mutation, historical read-only behavior, current stage and skill inventories, generated adapter candidates, public documentation, activation state, and release/history scope.

The review is isolated from implementation repair. It records findings and evidence only. The current runtime correctly reads this implementing v2 record as history and exposes no lifecycle mutation operation; no lifecycle state was changed by the reviewer.

## Actual-diff summary

- Makes v3 the only mutation-capable lifecycle contract and turns v1/v2 into read-only historical classifications.
- Removes standalone test-spec and explain-change stages from current runtime, automation, authored skill inventory, and adapter manifest.
- Makes new-change scaffold v3, keeps Delivery Review plan-only, and retains exact Verify correction and PR-consumption behavior.
- Leaves `specs/final-verification-contract-activation.yaml` in empty preactivation state and changes no release archive, tag, activation record, or historical explain-change artifact.
- Updates canonical and generated package tests, but omits two public guidance surfaces from the candidate parity boundary.

## Material findings

## Finding FV-M5-CR1

Finding ID: FV-M5-CR1
Severity: major
Location: `README.md:63,76,169-184,203,363,388`
Evidence: The root README is the public repository entrypoint and still presents `... -> code-review -> explain-change -> verify -> pr` as the recommended and canonical per-change chain, instructs users to invoke `explain-change`, advertises retired `spec-review` and `plan-review` commands, lists Explain Change as a current change-local artifact, and says ordinary non-trivial work requires `explain-change.md`. M5 deletes the skill and current runtime entrypoint, so following this documentation leads users to commands and prerequisites that no longer exist. The current tests validate README structure and links but do not assert the v3 route or retired-entrypoint absence. This violates FV-R1, FV-R2, FV-R3, FV-R35, FV-R37, FV-AC11, TG-19, TG-21, BND-STATE-001, BND-COMPOSE-001, BND-COMPAT-001, and INT-004.
Required outcome: The root README must describe one current v3 graph, successful Verify-owned explanation generation, no standalone explain-change or test-spec stage, and only current consolidated review entrypoints. Historical discussion must be explicitly non-executable.
Safe resolution path: Update every current workflow, best-practice, command, artifact-pack, and summary clause in `README.md`; add a focused regression that fails when the current README advertises `explain-change`, standalone test-spec, or retired artifact-review entrypoints as current. Preserve truly historical links only when clearly labeled as history.
needs-decision rationale: none; the approved candidate contract already selects the required current route.

## Finding FV-M5-CR2

Finding ID: FV-M5-CR2
Severity: major
Location: `scripts/adapter_templates/opencode/AGENTS.md:24`; generated OpenCode v3 candidate `AGENTS.md`; `dist/adapters/README.md:7-9`
Evidence: The current OpenCode template says generated aliases are `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `test-spec`, `implement`, `code-review`, and `pr`. A direct generated-candidate probe instead produced `architecture`, `code-review`, `delivery-review`, `design-review`, `implement`, `plan`, `pr`, `proposal`, `proposal-review`, and `spec`. Thus the shipped entrypoint advertises three retired aliases and omits three current aliases. Separately, `dist/adapters/README.md` says the tracked manifest still describes the released v2 package until activation, while M5 changes that manifest by removing `explain-change` as the candidate metadata. Existing adapter tests compare archive files and alias bodies but do not compare the entrypoint's declared alias inventory or support-guide contract to the candidate manifest. This violates FV-R35, FV-R37, FV-AC11, FV-AC14, TG-21, TG-23, BND-COMPOSE-001, BND-COMPAT-001, and INT-004.
Required outcome: Every generated adapter entrypoint and the tracked adapter support guide must truthfully describe the exact non-authoritative v3 candidate inventory, current aliases, preactivation status, and historical-release boundary; no generated current guidance may advertise a retired entrypoint or misclassify the tracked manifest.
Safe resolution path: Derive or update the OpenCode alias sentence from the canonical alias tuple, update `dist/adapters/README.md` to distinguish candidate metadata from released historical archives, and add generated-package regressions comparing the declared alias set and support-guide claims with the actual candidate manifest and archive contents.
needs-decision rationale: none; the implementation's alias tuple and approved preactivation boundary already determine the exact wording.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Runtime and skills implement v3, but public root and adapter guidance still direct users into retired current paths. |
| Test coverage | block | Broad suites pass without checking root README route semantics or generated entrypoint alias declarations against actual aliases. |
| Edge cases | pass | Runtime covers v1/v2 history, unknown/mixed contracts, retired stages, inactive v3, and exact owner correction. |
| Error handling | pass | Non-v3 mutation, inactive v3 progression, retired stages, unknown values, and mixed packages fail closed. |
| Architecture boundaries | concern | Executable ownership is correct, but published human entrypoints do not compose with it. |
| Compatibility | pass | Historical records remain readable without mutation authority; no allowlist revives them. |
| Security/privacy | pass | No credential, network, secret, or uncontrolled path authority was introduced. |
| Derived artifact currency | block | Generated OpenCode entrypoint prose contradicts its generated command set, and adapter support prose contradicts tracked candidate metadata. |
| Unrelated changes | pass | No activation file, release archive, tag, or historical explain-change artifact changed. |
| Validation evidence | concern | Named suites pass, but direct public-surface probes disprove complete candidate parity. |

## Validation performed

- `npm test --prefix packages/rigorloop` — passed, 333 tests with 2 intentional historical skips.
- `python scripts/test-lifecycle-cli-conformance.py` — passed.
- `python scripts/validate-governed-lifecycle-cli.py` — passed.
- `python scripts/test-change-metadata-validator.py` — passed, 107 tests.
- `python scripts/test-artifact-lifecycle-validator.py` — passed, 165 tests.
- `python scripts/test-workflow-automation.py` — passed, 78 tests.
- `python scripts/test-skill-validator.py` — passed, 376 tests.
- `python scripts/test-build-skills.py` — passed, 8 tests.
- `python scripts/build-skills.py --check` — passed.
- Direct staged-v3 OpenCode archive probe — reproduced the advertised-versus-generated alias mismatch.
- Direct README and adapter-support semantic scan — reproduced current retired-route and manifest-status contradictions.
- Activation/history path audit — `specs/final-verification-contract-activation.yaml` remained preactivation and the M5 range changed no release archive, tracked adapter ZIP, or historical explain-change artifact.
- `git diff --check 60136823..17140ccb` — passed.

## Handoff

- Reviewed milestone: M5
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5, M6
- Required review-resolution: yes
- Recommended next stage: review-resolution, bounded M5 correction, then Code Review M5 R2
- Final closeout readiness: not ready; current public package guidance is mixed, M5 remains open, and M6 has not begun
