# Bugfix Skill Simplification Test Specification

## Owning change record

`docs/changes/2026-08-20-bugfix-skill-simplification/change.yaml`

Boundary model version: boundary-first-v1

## Related spec and plan

- Spec: `specs/bugfix-skill-simplification.md`
- Plan: `docs/plans/2026-08-20-bugfix-skill-simplification.md`
- Architecture/ADRs: `docs/changes/2026-08-20-bugfix-skill-simplification/architecture-assessment.md`; architecture not required

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| feature spec | `specs/bugfix-skill-simplification.md` | `sha256:a3ff7c2894f8a51eb18f39a06b31ec3ba8cb53d0dfb2941e13b0fb44470d93d7` | `spec-review-r2`; `reviews/spec-review-r2.md` |
| execution plan | `docs/plans/2026-08-20-bugfix-skill-simplification.md` | commit `863ccb4a` | `plan-review-r2`; `reviews/plan-review-r2.md` and matching settlement retry |
| architecture assessment | `docs/changes/2026-08-20-bugfix-skill-simplification/architecture-assessment.md` | `architecture-not-required` | workflow-owned assessment bound to spec and review identities |

## Testing strategy

Use deterministic contract fixtures and repository-owned Python tests to prove classification, authority, phase gates, action precedence, terminal results, routing, write ownership, legacy preservation, measurements, and package parity. Focused tests run before broad skill, boundary, build, and adapter suites. Tests use local temporary directories and static fixture data only; no live repair, network, credentials, external platform, hosted CI, or target-agent execution is permitted.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T14-T15 | contract, integration | Flat package, truthful measurements, and parity. |
| R2-R3 | T2 | contract | Operation and concrete-defect input. |
| R4-R6 | T3-T4 | contract | Command/write authority, scope, and side effects. |
| R7-R9 | T5-T6 | contract | Closed evidence, restoration, and alternatives. |
| R10-R13 | T7-T9 | contract | Phase and proof identity gates. |
| R14-R18 | T10-T11 | contract | Cause, action, result, and owner routing. |
| R19 | T12 | contract | Independent-defect decomposition. |
| R20-R22 | T3, T13 | contract | Governed signals, write ownership, and evidence placement. |
| R23-R25 | T9-T11, T13 | contract | Validation, result, handoff, and forbidden claims. |
| R26-R27 | T1, T14-T15 | integration | Compatibility, package proof, and excluded machinery. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T2, T4 | Explicit diagnosis and no writes. |
| E2 | T2-T3 | Bare concrete bugfix and narrow portable scope. |
| E3 | T7-T8 | Proof authoring precedes correction. |
| E4 | T6, T8 | Infeasibility without complete proof blocks. |
| E5 | T10 | Contract gaps route upstream. |
| E6 | T9 | Changed proof cannot establish original success. |
| E7 | T10-T11 | Unknown cause cannot fix. |
| E8 | T13 | Invalid governed signals fail closed. |
| E9 | T11 | Completed correction wins before broad eligibility. |
| E10 | T11, T13 | Fix routes to code review only. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1: no concrete defect | T2 | Block before authority inference. |
| EC2: conflicting diagnosis and fix wording | T2 | Read-only diagnosis; mutation blocked. |
| EC3: unexpected command side effect | T4 | Stop and report mutation. |
| EC4: feasible testing with alternative only | T8 | Author automated proof. |
| EC5: incomplete alternative under infeasibility | T6, T8 | Block correction. |
| EC6: completed correction whose proof fails | T9, T11 | `stop-blocked` precedes phase rows. |
| EC7: changed fixture after correction | T9 | New proof identity; no fixed claim. |
| EC8: speculative test weakening | T10 | Route or block without mutation. |
| EC9: several symptoms | T12 | One invocation only for shared cause, basis, scope, and proof. |
| EC10: missing governed evidence path | T13 | Block recording; create no lifecycle surface. |
| EC11: external-dependency resilience patch | T10 | Require settled resilience basis and exact scope. |
| EC12: successful local fix | T11, T13 | No downstream readiness overclaim. |
| EC13: required truthful wording exceeds a prior count | T14 | Report the increase and pass only when semantics and parity remain complete. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | R2, R3, R7, R14, R15 | BND-INPUT-001 | T2, T5, T10-T11 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-002 | covered | R10, R11, R12, R13, R16, R23 | BND-STATE-001 | T7-T9, T11 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-003 | covered | R4, R5, R6, R8, R20, R21, R22 | BND-AUTH-001 | T3-T4, T6, T13 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-004 | covered | R17, R18, R19, R21, R24 | BND-COMPOSE-001 | T10-T13 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-005 | covered | R5, R13, R16, R23 | BND-TEMPORAL-001 | T3, T9, T11 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-006 | covered | R6, R9, R12, R16, R22, R23 | BND-RECOVERY-001 | T4, T6, T8-T9, T11, T13 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-007 | covered | R1, R21, R26 | BND-COMPAT-001 | T1, T13-T15 | integration | automated | CMD1-CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-008 | covered | R6, R9, R18, R27 | BND-ENV-001 | T4, T6, T10, T15 | integration | automated | CMD1-CMD6 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-009 | covered | R3, R4, R5, R20 | INT-001 | T2-T3, T13 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-010 | covered | R10, R11, R12, R16 | INT-002 | T7-T8, T11 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-011 | covered | R13, R23 | INT-003 | T9 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-012 | covered | R17, R18, R21 | INT-004 | T10, T13 | contract | automated | CMD1 | `evidence/m2-contract-implementation.md` | M2 | - | - |
| PRF-013 | covered | R6, R9, R27 | INT-005 | T4, T6, T15 | integration | automated | CMD1-CMD6 | `evidence/m3-package-proof.md` | M3 | - | - |
| PRF-014 | covered | R1, R21, R26 | INT-006 | T1, T13-T15 | integration | automated | CMD1-CMD7 | `evidence/m3-package-proof.md` | M3 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-skill-validator.py BugfixSkillSimplificationTests` | planned-for-implementation | M1 focused fixtures and validator tests | M1-M3 | M1 | Stop on any failed scenario or assertion. | Missing class or zero selected tests fails. | milestone evidence | Local fixtures and temporary directories only. |
| CMD2 | `python scripts/validate-skills.py skills/bugfix/SKILL.md` | existing/configured | repository skill validator | M2-M3 | M2 | Stop on structural or contract failure. | Not applicable; explicit skill path. | `evidence/m2-contract-implementation.md` | Reads canonical skill only. |
| CMD3 | `python scripts/test-skill-validator.py` | existing/configured | skill-validator regression suite | M2-M3 | M2 | Stop on any failure. | Zero discovered tests fails. | milestone evidence | Local tests and temporary fixtures only. |
| CMD4 | `python scripts/validate-boundary-first.py --check --path specs/bugfix-skill-simplification.md` | existing/configured | boundary-first validator | M1-M3 | test-spec-review | Stop on malformed, missing, stale, or unproved IDs. | Not applicable; explicit spec path. | review and M3 evidence | Read-only validation. |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | build regression suite | M2-M3 | M2 | Stop on build or projection regression. | Zero discovered tests fails. | `evidence/m3-package-proof.md` | Temporary package trees only. |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | adapter distribution suite | M3 | M3 | Stop on generated, archive, release-candidate, or install drift. | Zero discovered tests fails. | `evidence/m3-package-proof.md` | Temporary package and install trees; no publication. |
| CMD7 | `python scripts/build-skills.py --check` | existing/configured | repository skill builder | M2-M3 | M2 | Stop on canonical/generated drift. | Not applicable; explicit check mode. | `evidence/m3-package-proof.md` | Read-only check mode. |
| CMD8 | `python scripts/validate-change-metadata.py docs/changes/2026-08-20-bugfix-skill-simplification/change.yaml` | existing/configured | change-metadata validator | M1-M4 | M1 | Stop on lifecycle, vocabulary, evidence, or milestone inconsistency. | Not applicable; explicit record path. | stage-owned evidence | Read-only metadata validation. |
| CMD9 | `python scripts/validate-documentation-prose.py --mode audit --path specs/bugfix-skill-simplification.md --path specs/bugfix-skill-simplification.test.md --path docs/plans/2026-08-20-bugfix-skill-simplification.md` | existing/configured | documentation prose validator | M1-M4 | test-spec-review | Stop on errors; resolve warnings before claims. | Not applicable; explicit paths. | review and final verification evidence | Read-only audit mode. |
| CMD10 | `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | existing/configured | repository PR validation wrapper | M4 | M4 | Stop final closeout on any blocking check. | Wrapper policy applies. | `verify-report.md` | Local PR validation; no PR or hosted CI mutation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1-T6, T10-T15 | none | CMD1, CMD4, CMD8-CMD9 | preservation inventory and baseline evidence | M1 code review | Freeze semantics, literals, scenarios, size, and architecture boundary. |
| M2 | T2-T13 | none | CMD1-CMD5, CMD7-CMD9 | `evidence/m2-contract-implementation.md` | M2 code review | Prove the complete closed contract and one-file package. |
| M3 | T1, T9, T11, T13-T15 | none | CMD1-CMD9 | measurements, reconciliation, and `evidence/m3-package-proof.md` | M3 code review | Prove final semantics, truthful size reporting, metric-gaming prevention, boundaries, and package parity. |
| M4 | T1-T15 | none | CMD1-CMD10 | final review, explanation, resolution when required, and verify report | PR handoff | Final coherence after all implementation milestones close. |

## Test cases

### T1. Package shape and legacy inventory remain closed

- Covers: R1, R26-R27; AC1, AC12, AC15; BND-COMPAT-001, BND-ENV-001; INT-006.
- Level: integration
- Command IDs: CMD1, CMD3-CMD7
- Fixture/setup: Current skill lines, resource inventory, direct literal consumers, and package projections.
- Steps: Apply every rule and literal disposition, inspect the package, and validate projections.
- Expected result: One `SKILL.md`, no added package resource or runtime, one semantic owner per rule, and no lost consumer literal.
- Failure proves: Compression changed package shape or silently lost behavior.
- Evidence artifact: M1 inventories and `evidence/m3-package-proof.md`
- Automation location: `BugfixSkillSimplificationTests` plus build/distribution suites
- Required by milestone: M1 and M3

### T2. Intent and concrete-defect classification are deterministic

- Covers: R2-R3; E1-E2; EC1-EC2; AC2; BND-INPUT-001; INT-001.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Explicit diagnosis, explicit fix, bare concrete `$bugfix`, absent defect, conflicting intent, and late expansion.
- Steps: Classify each request, then attempt mutation or expansion.
- Expected result: Exactly one operation; absent defect blocks; conflict stays read-only; expansion reruns preflight.
- Failure proves: Wording grants ambiguous or stale mutation authority.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T3. Write authority and scope are exact

- Covers: R4-R5, R21; E2; AC2, AC4, AC10; BND-AUTH-001, BND-TEMPORAL-001; INT-001.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Portable and governed current, absent, stale, invalid, ambiguous, mismatched, and expanded scopes.
- Steps: Resolve every authority field and attempt in-scope and out-of-scope writes.
- Expected result: Only exact current scope writes; every missing or changed identity blocks.
- Failure proves: Fix intent or context grants broader mutation.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T4. Diagnosis command side effects fail closed

- Covers: R6; E1; EC3; AC3; BND-AUTH-001, BND-RECOVERY-001, BND-ENV-001; INT-005.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Read-only, generated, tracked, destructive, privileged, network, database, and external-state command descriptions.
- Steps: Resolve command authority and simulate expected and unexpected effects.
- Expected result: Only bounded commands run; unexpected durable mutation stops and is reported.
- Failure proves: Read-only operation silently mutates tracked or external state.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T5. Closed evidence vocabularies reject unknowns first

- Covers: R7, R14-R15; AC6, AC12; BND-INPUT-001.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Every valid and one unknown value for each closed set.
- Steps: Classify vocabulary before running consistency logic.
- Expected result: Valid values proceed; each unknown emits an explicit validation failure.
- Failure proves: Unknown values fall through or are accepted by consistency checks.
- Evidence artifact: M1 fixture evidence
- Automation location: `BugfixSkillSimplificationTests` tests containing `unknown_value` or `not_in_vocabulary`
- Required by milestone: M1

### T6. Restoration and deterministic alternatives require exact evidence

- Covers: R8-R9; E4-E5; EC5; AC8; BND-AUTH-001, BND-RECOVERY-001, BND-ENV-001; INT-005.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Current, stale, conflicting, implementation-only, report-only, repeatable, incomplete, and subjective evidence.
- Steps: Resolve restoration and alternative-proof records.
- Expected result: Only conflict-free authoritative restoration and objective repeatable alternatives qualify; infeasibility alone never does.
- Failure proves: Plausible expectation or subjective inspection authorizes correction.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T7. Proof authoring is writable before production correction

- Covers: R10-R11; E3; AC5; BND-STATE-001; INT-002.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Eligible diagnosis with missing automated proof and exact proof-only paths.
- Steps: Enter proof authoring and attempt test, fixture, helper, reproduction, and production writes.
- Expected result: Proof-only writes proceed; production behavior remains blocked.
- Failure proves: The gate is circular or prematurely authorizes production.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T8. Proof-action matrix is exhaustive and non-overlapping

- Covers: R12; E3-E4; EC4-EC5; AC5-AC6; BND-STATE-001, BND-RECOVERY-001; INT-002.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Cartesian set of recognized feasibility and proof values with completeness flag for alternatives.
- Steps: Evaluate the ordered proof-action table and count matches.
- Expected result: Exactly one reachable action for each admitted combination; no correction from missing or conflicting proof.
- Failure proves: A gap, overlap, or unreachable row exists.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T9. Proof identity remains unchanged through validation

- Covers: R13, R23; E6; EC6-EC7; AC7; BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-003.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Matching and changed commands, fixtures, inputs, environments, observations, and blast-radius checks.
- Steps: Record pre-fix proof, apply correction, rerun or alter one component, and derive result.
- Expected result: Only identity-equal passing proof and required surrounding checks permit completion.
- Failure proves: A different proof or failed check is presented as regression success.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T10. Cause and contract routing never invent behavior

- Covers: R14, R17-R18; E5, E7; EC8, EC11; AC8; BND-INPUT-001, BND-COMPOSE-001, BND-ENV-001; INT-004.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Every cause with settled, restoration, missing, conflicting, behavior-change, design, resilience, and owner evidence.
- Steps: Select owner and mutation eligibility.
- Expected result: Contract/design/system gaps route; unknown never fixes; test and resilience corrections require exact eligible basis.
- Failure proves: Bugfix changes another owner's contract or patches unrelated product code.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T11. Current actions and terminal results are deterministic

- Covers: R15-R16, R23-R25; E7, E9-E10; EC6, EC12; AC6-AC7, AC11; BND-INPUT-001, BND-STATE-001, BND-COMPOSE-001, BND-TEMPORAL-001, BND-RECOVERY-001; INT-002.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Every ordered action condition, completed pass/fail states, internal continuation, and return state.
- Steps: Count matching action rows, derive terminal result only on return, and inspect handoff claims.
- Expected result: Exactly one reachable action; completion rows win; exactly one terminal result; changed implementation names only code-review next.
- Failure proves: State overlap, shadowing, intermediate-result leakage, or downstream overclaim.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T12. Independent defects decompose

- Covers: R19; EC9; BND-COMPOSE-001.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: Multiple symptoms with shared and distinct causes, bases, scopes, and proof bundles.
- Steps: Apply the decomposition predicate.
- Expected result: Only a completely shared bundle remains one invocation.
- Failure proves: Unrelated defects gain one blended authority or proof claim.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T13. Governed signals, evidence placement, and write owners fail closed

- Covers: R20-R22, R24-R25; E8, E10; EC10, EC12; AC9-AC11; BND-AUTH-001, BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001; INT-001, INT-004, INT-006.
- Level: contract
- Command IDs: CMD1
- Fixture/setup: No, one valid, malformed, stale, escaped, duplicate, and conflicting signals; valid, missing, and ambiguous evidence paths; all forbidden owner surfaces.
- Steps: Classify context, attempt fallback, recording, every permitted write category, and each forbidden mutation.
- Expected result: Invalid signals never fall back; missing placement creates nothing; only exact bugfix surfaces write; no lifecycle or downstream claim changes.
- Failure proves: Governed context broadens authority or bugfix mutates another owner.
- Evidence artifact: `evidence/m2-contract-implementation.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M2

### T14. Size measurements are truthful and never override semantics

- Covers: R1, R26; AC1, AC14; BND-COMPAT-001; INT-006.
- Level: integration
- Command IDs: CMD1
- Fixture/setup: Frozen prior and proposed LF-normalized UTF-8 `SKILL.md` bytes, complete semantic/literal dispositions, and optional tokenizer-specific fixtures when a token estimate is reported.
- Steps: Count Unicode whitespace-separated words and UTF-8 bytes for root and complete package; identify the tokenizer or model basis for any token estimate; then test both decreasing and increasing truthful candidates against semantic, deterministic, safety, and parity gates.
- Expected result: Exact before/after counts and deltas are reported, the root equals the complete package, an optional token estimate names its basis, and a semantically complete increase passes while any metric-driven omission or relocation fails.
- Failure proves: Measurement is inconsistent, an unidentified token estimate is presented as comparable truth, or a size target overrides required behavior.
- Evidence artifact: `evidence/simplification-measurements.md`
- Automation location: `BugfixSkillSimplificationTests`
- Required by milestone: M3

### T15. Every package projection is byte-identical and static

- Covers: R1, R26-R27; AC13, AC15; BND-COMPAT-001, BND-ENV-001; INT-005, INT-006.
- Level: integration
- Command IDs: CMD2-CMD7
- Fixture/setup: Canonical source and generated, packed, archived, release-candidate, and clean-installed projections.
- Steps: Build temporary outputs, compare bytes and resource manifests, and inspect executed command boundaries.
- Expected result: Every projection matches, contains no new resource, and acceptance performs no live or external action.
- Failure proves: Shipped behavior drifts or acceptance exceeds its authority.
- Evidence artifact: `evidence/m3-package-proof.md`
- Automation location: existing skill build and adapter distribution suites
- Required by milestone: M3

## Fixtures and data

Use deterministic table fixtures under the owning change root or the existing skill-validator fixture surface. Fixtures include request wording, defect identity, authorities, evidence axes, phase state, proof identity components, cause, action expectations, result expectations, write attempts, owner routes, legacy rule dispositions, literal consumers, and package forms. No fixture uses time, randomness, network, secrets, external accounts, or shared mutable state.

## Mocking/stubbing policy

Model commands, files, governed signals, external effects, and package projections with local immutable fixture values and test-owned temporary directories. Do not mock away the outcome under test: action selection, path authorization, identity comparison, word/byte measurement, optional tokenizer-basis labeling, and package-byte comparison must use the real repository-owned functions or direct deterministic assertions.

## Migration or compatibility tests

T1, T13-T15 prove that historical evidence is untouched, every legacy rule and sensitive literal has a disposition, the package remains flat, direct consumers preserve meaning, and all package projections agree. No data migration is required.

## Observability verification

T11 and T13 assert every returned result exposes operation, terminal result, authority states, repository and defect scope, actual commands, proof identity, skipped checks, uncertainty, changed surfaces, blocker, and next owner without claiming unobserved downstream status.

## Security/privacy verification

T3-T4, T6, T10, and T13 cover exact path and command scope, destructive and privileged effects, network/database/external isolation, sensitive evidence placement, and forbidden cross-owner mutation. Static fixtures contain no credentials or private incident content.

## Performance checks

No runtime performance behavior is added. T14 reports word and byte deltas, identifies any optional token-estimate basis, and proves that counts cannot override semantics or safety. Focused CMD1 precedes broad CMD3, CMD5, and CMD6 to keep the inner proof loop bounded.

## Manual QA checklist

Not applicable. Every proof obligation is deterministic and automated; prose adequacy remains owned by independent lifecycle reviews rather than a manual test procedure.

## What not to test and why

- Do not run a live repair task or target agent; static contract fixtures prove the published text boundary.
- Do not access issues, incidents, networks, databases, secrets, hosted CI, or external platforms; these are excluded and unauthorized.
- Do not test language-specific debuggers or frameworks; project-specific commands remain project-owned.
- Do not treat implementation code, tests, or validation as complete during test-spec authoring or review.

## Uncovered gaps

None.

## Next artifacts

- Independent `test-spec-review`.
- Implementation only after formal approval and workflow selection.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `test-spec-review`. No test or production implementation has started, and no validation result is claimed.
