# Simplified Proposal Contract Test Specification

## Owning change record

`docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml`

## Related spec and plan

- Spec: `specs/simplified-proposal-contract.md`
- Plan: `docs/plans/2026-08-30-simplify-rigorloop-proposal-contract.md`
- Architecture/ADRs: `docs/architecture/2026-08-30-simplified-proposal-contract.md`; no ADR applies

## Input artifact identities

| Input | Path | Artifact ID | Review evidence |
| --- | --- | --- | --- |
| Specification | `specs/simplified-proposal-contract.md` | `spec` | `design-review-r2` at `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/design-review-r2.md` |
| Architecture | `docs/architecture/2026-08-30-simplified-proposal-contract.md` | `architecture` | `design-review-r2` at `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/reviews/design-review-r2.md` |
| Execution plan | `docs/plans/2026-08-30-simplify-rigorloop-proposal-contract.md` | `plan` | pending Delivery Review |

## Testing strategy

Use focused contract and integration tests at the existing proposal-skill, artifact-lifecycle, review-artifact, build, and adapter boundaries. Structural tests prove exact section order, forbidden metadata, closed vision outcomes, ownership, compatibility selection, and generated resource parity. Semantic Proposal Review judgment remains hybrid: deterministic fixtures establish required and forbidden behavior, while independent review confirms decision sufficiency and that downstream detail is not demanded.

The proof map intentionally reuses existing test owners. It does not create a new validator family, proposal version, compatibility interpreter, hash check, CLI command, or repository-wide inventory.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| SPC-R1, SPC-R2, SPC-R3 | SPC-T01, SPC-T02 | contract | Exact required order, conditional impact position, nested headings, and unknown level-two sections. |
| SPC-R4, SPC-R5 | SPC-T02, SPC-T03 | contract | Forbidden lifecycle/vision metadata and proportional non-empty feasibility. |
| SPC-R6, SPC-R7, SPC-R8 | SPC-T04 | integration | Portable and governed ownership paths; static absence checks cover forbidden new mechanisms. |
| SPC-R9, SPC-R10, SPC-R11 | SPC-T05, SPC-T06 | contract, hybrid | Proposal Review judgment, closed alignment outcome, and material-conflict handling. |
| SPC-R12, SPC-R13, SPC-R14 | SPC-T06, SPC-T07 | contract, hybrid | Approval authority and too-vague/too-detailed review behavior. |
| SPC-R15, SPC-R16 | SPC-T08 | integration | Current-path enforcement and untouched settled historical readability. |
| SPC-R17, SPC-R18 | SPC-T09, SPC-T10 | integration, smoke | Coordinated canonical surfaces and canonical-to-published parity. |
| SPC-R19 | SPC-T07 | contract | No fixed length or token gate; proportional decision sufficiency remains the review criterion. |
| SPC-R20 | SPC-T06 | integration | Direct review records or settles only its proposal and does not start Design. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | SPC-T01, SPC-T03 | Ordinary proposal has seven sections, proportional feasibility, and no routine impact or metadata. |
| E2 | SPC-T01, SPC-T05 | Material impact is admitted only in the defined position and affects review judgment. |
| E3 | SPC-T04 | Governing path and state are recorded only in `change.yaml`. |
| E4 | SPC-T05 | Routine alignment is recorded in review evidence. |
| E5 | SPC-T05 | Undisclosed material conflict withholds approval. |
| E6 | SPC-T08 | Untouched settled legacy evidence remains readable. |

## Edge case coverage

| Edge case | Covered by | Expected proof |
| --- | --- | --- |
| EC1 | SPC-T02 | Misordered `Decision requested` fails with an order diagnostic. |
| EC2 | SPC-T05 | Routine impact is judged proportionately and is not rejected solely for existing. |
| EC3 | SPC-T04 | Portable authoring and isolated review work without governed settlement. |
| EC4 | SPC-T04 | Wrong governed proposal path blocks reliance without editing proposal Markdown. |
| EC5 | SPC-T05 | Missing vision uses `no-vision-bootstrap` and blocks without an explicit bootstrap decision. |
| EC6 | SPC-T08 | Untouched settled historical metadata remains readable. |
| EC7 | SPC-T08 | Unsettled legacy work must adopt the current contract before settlement. |
| EC8 | SPC-T10 | Stale or mixed adapter projection blocks package validation. |

## Proof map

Boundary model version: boundary-first-v1
Boundary model scope: SPC-R1, SPC-R2, SPC-R3, SPC-R4, SPC-R5, SPC-R6, SPC-R7, SPC-R8, SPC-R9, SPC-R10, SPC-R11, SPC-R12, SPC-R13, SPC-R14, SPC-R15, SPC-R16, SPC-R17, SPC-R18, SPC-R19, SPC-R20

| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRF-001 | covered | SPC-R1, SPC-R2, SPC-R3, SPC-R4, SPC-R5 | BND-INPUT-001 | SPC-T01, SPC-T02, SPC-T03 | contract | automated | CMD-01, CMD-03 | `evidence/m1-canonical-contract.md`, `evidence/m2-validation-and-compatibility.md` | M1, M2 | - | - |
| PRF-002 | covered | SPC-R6, SPC-R7, SPC-R12, SPC-R15, SPC-R20 | BND-STATE-001 | SPC-T04, SPC-T06, SPC-T08 | integration | automated | CMD-03, CMD-04 | `evidence/m2-validation-and-compatibility.md` | M2 | - | - |
| PRF-003 | covered | SPC-R7, SPC-R9, SPC-R10, SPC-R11, SPC-R12, SPC-R20 | BND-AUTH-001 | SPC-T04, SPC-T05, SPC-T06 | contract | hybrid | CMD-01, CMD-04 | `evidence/m1-canonical-contract.md`, `evidence/m2-validation-and-compatibility.md` | M1, M2 | MP-001 | - |
| PRF-004 | covered | SPC-R6, SPC-R7, SPC-R17, SPC-R18 | BND-COMPOSE-001 | SPC-T04, SPC-T09, SPC-T10 | end-to-end | automated | CMD-06, CMD-07, CMD-08 | `evidence/m3-publication-parity.md` | M3 | - | - |
| PRF-005 | covered | SPC-R15, SPC-R16, SPC-R20 | BND-TEMPORAL-001 | SPC-T06, SPC-T08 | integration | automated | CMD-03, CMD-04 | `evidence/m2-validation-and-compatibility.md` | M2 | - | - |
| PRF-006 | covered | SPC-R11, SPC-R16, SPC-R17 | BND-RECOVERY-001 | SPC-T05, SPC-T08, SPC-T10 | integration | automated | CMD-03, CMD-04, CMD-07 | `evidence/m2-validation-and-compatibility.md`, `evidence/m3-publication-parity.md` | M2, M3 | - | - |
| PRF-007 | covered | SPC-R8, SPC-R15, SPC-R16, SPC-R17 | BND-COMPAT-001 | SPC-T04, SPC-T08, SPC-T10 | integration | automated | CMD-03, CMD-07 | `evidence/m2-validation-and-compatibility.md`, `evidence/m3-publication-parity.md` | M2, M3 | - | - |
| PRF-008 | covered | SPC-R6, SPC-R7, SPC-R12 | INT-001 | SPC-T04, SPC-T06 | integration | automated | CMD-03, CMD-04 | `evidence/m2-validation-and-compatibility.md` | M2 | - | - |
| PRF-009 | covered | SPC-R9, SPC-R10, SPC-R11 | INT-002 | SPC-T05 | contract | hybrid | CMD-01, CMD-04 | `evidence/m1-canonical-contract.md`, `evidence/m2-validation-and-compatibility.md` | M1, M2 | MP-001 | - |
| PRF-010 | covered | SPC-R15, SPC-R16, SPC-R17, SPC-R18 | INT-003 | SPC-T08, SPC-T09, SPC-T10 | smoke | automated | CMD-03, CMD-06, CMD-07, CMD-08 | `evidence/m3-publication-parity.md` | M3 | - | - |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD-01 | `python scripts/test-skill-validator.py` | existing/configured | skill validation | M1 | M1 | Any failure blocks M1 handoff. | Zero discovered tests is failure. | `evidence/m1-canonical-contract.md` | Local read/test execution; fixtures and temporary files only. |
| CMD-02 | `python scripts/validate-skills.py skills/proposal/SKILL.md && python scripts/validate-skills.py skills/proposal-review/SKILL.md` | existing/configured | skill validation | M1 | M1 | Any package or resource error blocks M1. | Not applicable; direct validation must inspect both targets. | `evidence/m1-canonical-contract.md` | Read-only canonical package validation. |
| CMD-03 | `python scripts/test-artifact-lifecycle-validator.py` | existing/configured | lifecycle validation | M2 | M2 | Any fixture failure blocks M2. | Zero discovered tests is failure. | `evidence/m2-validation-and-compatibility.md` | Local test execution with temporary fixtures. |
| CMD-04 | `python scripts/test-review-artifact-validator.py` | existing/configured | review validation | M2 | M2 | Any review-shape or vocabulary failure blocks M2. | Zero discovered tests is failure. | `evidence/m2-validation-and-compatibility.md` | Local test execution with temporary fixtures. |
| CMD-05 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-08-30-simplify-rigorloop-proposal-contract.md --path skills/proposal/SKILL.md --path skills/proposal-review/SKILL.md` | existing/configured | lifecycle validation | M2 | M2 | Current-path drift blocks M2; unrelated baseline debt is reported separately. | Not applicable; explicit paths must be classified. | `evidence/m2-validation-and-compatibility.md` | Read-only explicit-path validation. |
| CMD-06 | `python scripts/test-build-skills.py && python scripts/build-skills.py --check` | existing/configured | skill build | M3 | M3 | Build or drift failure blocks M3. | Zero build assertions is failure; check must select canonical skills. | `evidence/m3-publication-parity.md` | Temporary generated mirror; no authored generated output. |
| CMD-07 | `python scripts/test-adapter-distribution.py` | existing/configured | adapter distribution | M3 | M3 | Archive, resource, or parity failure blocks M3. | Zero adapter tests is failure. | `evidence/m3-publication-parity.md` | Temporary archives/install roots; no network requirement. |
| CMD-08 | `python scripts/validate-release.py --version v0.4.1 --recorded-source-auto` | release-owned | release validation | M3 | M3 | Published release identity or recorded-source failure blocks cutover. | Not applicable; recorded-source validation must execute for all supported adapters. | `evidence/m3-publication-parity.md` | Read-only historical release validation; current temporary archive and install parity is owned by CMD-07. |
| CMD-09 | `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/skill-contract.md` | existing/configured | documentation validation | M1 | M1 | Errors block M1; warnings require explicit disposition. | Not applicable; all named paths must be inspected. | `evidence/m1-canonical-contract.md` | Read-only prose audit. |
| CMD-10 | `npm test --prefix packages/rigorloop` | existing/configured | lifecycle CLI package | M1 | final holistic review | Any regression blocks final closeout. | Zero package tests is failure. | final holistic review receipt | Local tests; dependency installation is separate and no publish occurs. |
| CMD-11 | `python scripts/validate-change-metadata.py docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/change.yaml && python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-30-simplify-rigorloop-proposal-contract` | existing/configured | lifecycle evidence validation | lifecycle closeout | Delivery Review | Any metadata or evidence inconsistency blocks the next gate. | Not applicable; both explicit targets must validate. | Delivery Review and final verification evidence | Read-only validation of the owning change pack. |
| CMD-12 | `python scripts/validate-boundary-first.py --check --path specs/simplified-proposal-contract.test.md` | existing/configured | boundary validation | M2 | Delivery Review | Any missing or contradictory proof mapping blocks Delivery Review. | Not applicable; the proof record and its linked feature contract must be checked. | Delivery Review receipt | Read-only structural boundary validation. |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | SPC-T01, SPC-T02, SPC-T03, SPC-T05, SPC-T06, SPC-T07, SPC-T09 | MP-001 | CMD-01, CMD-02, CMD-09 | `evidence/m1-canonical-contract.md` | M1 code review | Canonical contract and governance must agree before validator cutover. |
| M2 | SPC-T02, SPC-T03, SPC-T04, SPC-T05, SPC-T06, SPC-T08, SPC-T09 | none | CMD-03, CMD-04, CMD-05, CMD-11, CMD-12 | `evidence/m2-validation-and-compatibility.md` | M2 code review | Current-path and historical-path proof must remain distinct. |
| M3 | SPC-T09, SPC-T10 | none | CMD-06, CMD-07, CMD-08 | `evidence/m3-publication-parity.md` | M3 code review | Generated outputs remain temporary derived proof. |
| M4 | SPC-T01, SPC-T02, SPC-T03, SPC-T04, SPC-T05, SPC-T06, SPC-T07, SPC-T08, SPC-T09, SPC-T10 | MP-001 | CMD-01, CMD-02, CMD-03, CMD-04, CMD-05, CMD-06, CMD-07, CMD-08, CMD-09, CMD-10, CMD-11, CMD-12 | final review, explanation, and verify report | PR handoff | Final holistic review covers the CLI prerequisite fix and cross-milestone interaction. |

## Test cases

### SPC-T01. Accept the simplified proposal section grammar

- Covers: SPC-R1, SPC-R2, SPC-R3, E1, E2, SPC-AC1, SPC-AC2.
- Level: contract
- Command IDs: CMD-01, CMD-03
- Fixture/setup: ordinary seven-section proposal, material-impact proposal, and nested-heading proposal fixtures.
- Steps: validate each fixture through its current authoring and lifecycle structure path.
- Expected result: required sections pass in order; conditional impact passes only between Feasibility and Decision requested; nested headings do not count as extra level-two sections.
- Failure proves: the simplified content grammar is not implemented consistently.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m1-canonical-contract.md`
- Automation location: existing proposal skill and artifact-lifecycle validator tests.
- Required by milestone: M1, M2

### SPC-T02. Reject malformed or forbidden proposal structure

- Covers: SPC-R1-SPC-R5, EC1, SPC-AC6.
- Level: contract
- Command IDs: CMD-01, CMD-03
- Fixture/setup: missing, duplicate, misordered, unknown, empty-feasibility, embedded Status, owning-pointer, and routine Vision-fit fixtures.
- Steps: validate each negative fixture and inspect its diagnostic class.
- Expected result: every malformed current proposal fails with the exact structural or forbidden-metadata reason; nested valid structure remains accepted.
- Failure proves: invalid current proposals can pass or diagnostics cannot identify the correction owner.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m2-validation-and-compatibility.md`
- Automation location: proposal skill and artifact-lifecycle validator tests.
- Required by milestone: M1, M2

### SPC-T03. Require proportionate credible feasibility

- Covers: SPC-R5, E1, SPC-AC1.
- Level: contract
- Command IDs: CMD-01, CMD-03
- Fixture/setup: ordinary concise assessment, constrained assessment, empty assessment, unsupported claim, and explicit blocker.
- Steps: run structural checks and Proposal Review fixture evaluation.
- Expected result: concise credible evidence passes; empty or non-credible feasibility and unresolved blockers withhold approval without requiring architecture or proof design.
- Failure proves: Feasibility is either ceremonial or prematurely owns downstream design.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m1-canonical-contract.md`
- Automation location: skill validator fixtures plus MP-001 semantic review.
- Required by milestone: M1, M2

### SPC-T04. Preserve portable and governed ownership boundaries

- Covers: SPC-R6-SPC-R8, E3, EC3, EC4, SPC-AC3, SPC-AC4, SPC-AC8, INT-001.
- Level: integration
- Command IDs: CMD-03, CMD-05
- Fixture/setup: portable proposal with no change record; governed proposal with matching path; governed proposal with mismatched path; static changed-surface scan.
- Steps: validate portable authoring, governed reliance, and forbidden mechanism absence.
- Expected result: portable work remains valid without settlement; governed state comes only from matching `change.yaml`; mismatches block without rewriting the proposal; no new CLI, field, version, hash, or reverse pointer exists.
- Failure proves: ownership is duplicated, portable use is broken, or forbidden lifecycle machinery was introduced.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m2-validation-and-compatibility.md`
- Automation location: artifact-lifecycle validator tests and explicit-path validation.
- Required by milestone: M2

### SPC-T05. Record vision judgment and disclose material conflict

- Covers: SPC-R9-SPC-R11, E2, E4, E5, EC2, EC5, SPC-AC5, INT-002.
- Level: contract
- Command IDs: CMD-01, CMD-04
- Fixture/setup: each closed vision-alignment outcome, an unknown outcome, routine alignment, disclosed conflict, undisclosed conflict, and missing-vision bootstrap.
- Steps: validate review result shape and independently inspect the decision outcome through MP-001.
- Expected result: exactly one known outcome is recorded; ordinary alignment remains review evidence; undisclosed or ownerless material issues withhold approval; unknown outcomes fail before consistency checks.
- Failure proves: vision responsibility is duplicated, hidden, or structurally ambiguous.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m2-validation-and-compatibility.md`
- Automation location: proposal-review skill and review-artifact validator tests.
- Required by milestone: M1, M2

### SPC-T06. Bound proposal approval and preserve review isolation

- Covers: SPC-R12-SPC-R14, SPC-R20, SPC-AC5, INT-001.
- Level: integration
- Command IDs: CMD-01, CMD-04
- Fixture/setup: approved proposal, vague direction, premature architecture/API/test plan, absent routine downstream detail, and direct formal review lifecycle fixture.
- Steps: evaluate review outcomes, record or settle the exact proposal when governed, and inspect workflow routing.
- Expected result: approval locks only proposal-level direction and authorizes architecture/specification authoring; vague or prematurely detailed proposals receive findings; missing routine downstream detail does not; direct review does not start Design.
- Failure proves: Proposal Review grants excessive authority or demands decisions owned downstream.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m1-canonical-contract.md`
- Automation location: proposal-review skill tests, review validator tests, and MP-001.
- Required by milestone: M1, M2

### SPC-T07. Judge proportionality without a size gate

- Covers: SPC-R13, SPC-R14, SPC-R19.
- Level: contract
- Command IDs: CMD-01
- Fixture/setup: concise sufficient proposal, longer material-impact proposal, vague short proposal, and overly detailed proposal.
- Steps: inspect skill output criteria and representative review outcomes.
- Expected result: no fixed word or token threshold exists; sufficiency, materiality, vagueness, and premature detail determine the outcome.
- Failure proves: simplification became a mechanical length rule or stopped protecting downstream authority.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m1-canonical-contract.md`
- Automation location: proposal and proposal-review skill fixtures plus MP-001.
- Required by milestone: M1

### SPC-T08. Enforce cutover without rewriting settled history

- Covers: SPC-R15, SPC-R16, E6, EC6, EC7, SPC-AC6, BND-TEMPORAL-001, BND-COMPAT-001.
- Level: integration
- Command IDs: CMD-03, CMD-05
- Fixture/setup: untouched settled legacy proposal, changed settled proposal, unsettled legacy proposal, and new simplified proposal.
- Steps: run compatibility-aware current-path validation for each state.
- Expected result: untouched settled evidence remains readable; changed, unsettled, and new current work use the simplified contract before settlement; no historical file is rewritten.
- Failure proves: compatibility is too permissive or historical evidence is forced through migration.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m2-validation-and-compatibility.md`
- Automation location: artifact-lifecycle validator compatibility fixtures.
- Required by milestone: M2

### SPC-T09. Keep canonical governance and examples coherent

- Covers: SPC-R17, SPC-R18, SPC-AC7, INT-003.
- Level: integration
- Command IDs: CMD-01, CMD-02, CMD-09
- Fixture/setup: canonical skills, assets, references, governance, workflow guide, skill contract, and representative examples.
- Steps: validate skill resources, run focused conformance assertions, and audit changed governing prose.
- Expected result: all canonical surfaces describe the same seven-section contract, review outcome, ownership, and handoff boundaries without maintainer details leaking into public skill output.
- Failure proves: cutover is internally mixed before generation.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m1-canonical-contract.md`
- Automation location: skill validation, skill tests, and prose audit.
- Required by milestone: M1, M2

### SPC-T10. Project the canonical contract through supported publication paths

- Covers: SPC-R17, SPC-R18, EC8, SPC-AC7, BND-COMPOSE-001, INT-003.
- Level: smoke
- Command IDs: CMD-06, CMD-07, CMD-08
- Fixture/setup: canonical proposal and Proposal Review packages plus temporary supported adapter build and install roots.
- Steps: build, drift-check, package current temporary archives, validate and clean-install both changed skills, then validate the published v0.4.1 evidence through its recorded source without publishing or rewriting it.
- Expected result: current temporary projections contain the canonical resources and contract; missing, stale, escaped, or mixed resources block; published v0.4.1 evidence remains valid; tracked generated bodies are not introduced.
- Failure proves: the public release can activate a different contract from canonical source.
- Evidence artifact: `docs/changes/2026-08-30-simplify-rigorloop-proposal-contract/evidence/m3-publication-parity.md`
- Automation location: existing skill build, adapter distribution, and release validation.
- Required by milestone: M3

## Fixtures and data

Reuse existing proposal, stage-owned lifecycle, review-artifact, skill-build, and adapter fixtures. Add only focused simplified-current and untouched-settled-historical cases needed by SPC-T01 through SPC-T10. Fixtures contain synthetic public data and no credentials or machine-local paths.

## Mocking/stubbing policy

Use temporary repositories, change records, skill mirrors, archives, and install roots provided by existing test helpers. Do not mock the proposal parser or canonical resource loader when their public composed path is under test. No network or hosted service is required.

## Migration or compatibility tests

SPC-T08 directly proves historical readability and current cutover behavior. Migration is not performed: fixtures demonstrate that untouched settled evidence remains readable and that new, changed, or unsettled work must conform before settlement.

## Observability verification

Structural diagnostics must identify the missing, duplicate, misordered, unknown, forbidden, stale, or mismatched surface. Proposal Review results must expose status, material findings, one vision-alignment outcome, authority granted or withheld, and next owner without repository-maintainer implementation details.

## Security/privacy verification

Static and fixture inspection confirms the change introduces no credentials, network calls, private context, external trust boundary, or publication action. Existing archive traversal and resource-containment checks remain part of CMD-07 and CMD-08.

## Performance checks

No benchmark gate applies. Review and validation remain bounded to selected proposal, change record when governed, changed canonical skills, and existing package checks. SPC-T07 confirms no fixed proposal word or token budget is introduced.

## Manual QA checklist

### MP-001. Independent semantic proposal-contract review

- Confirm an ordinary proposal can be responsibly approved from the seven required sections and proportional feasibility.
- Confirm material impact is disclosed only when it can change approval.
- Confirm Proposal Review records routine vision alignment but withholds approval for undisclosed material conflict.
- Confirm reviewers do not demand APIs, schemas, architecture, milestones, test cases, rollout mechanics, or other downstream detail.
- Confirm vague direction and premature downstream settlement both remain material findings.
- Record the result in the owning milestone code-review evidence.

## What not to test and why

- Do not test a new CLI command, proposal version, hash, reverse pointer, or compatibility interpreter because each is forbidden by SPC-R8.
- Do not rewrite or normalize historical proposal files; compatibility proof treats them as immutable evidence.
- Do not enumerate every proposal length or every combination of boundary partitions; the selected cases cover each distinct observable outcome and composed hazard.
- Do not use generated adapter bodies as authored truth or require network publication.
- Do not test Design Review, Delivery Review, Code Review, or Verify semantics beyond ensuring Proposal Review does not claim their authority.

## Uncovered gaps

None.

## Next artifacts

- Delivery Review over this test specification and `docs/plans/2026-08-30-simplify-rigorloop-proposal-contract.md`.
- Implementation begins only after the exact Delivery package is approved and initialized.

## Follow-on artifacts

None yet.

## Readiness

Ready for Delivery Review after governed registration and structural validation. This authoring result does not authorize implementation.
