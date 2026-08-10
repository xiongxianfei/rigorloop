# M1 Code Review R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: Codex independent contract-first code-review peer
Target: e77a351c..09459a5f
Reviewed artifact: commit 09459a5f
Reviewed milestone: M1
Review date: 2026-08-10
Status: changes-requested
Recording status: recorded
Review status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review invocation manifest, and review log
- Open blockers: PSR-CR-M1-R1-001 and PSR-CR-M1-R1-002
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PSR-CR-M1-R1-001, PSR-CR-M1-R1-002
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/code-review-m1-r1.md
- Review log: docs/changes/2026-08-10-published-skill-first-repository-simplification/review-log.md
- Review resolution: required before fixes
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5, M6
- Required review-resolution: yes
- Finding IDs: PSR-CR-M1-R1-001, PSR-CR-M1-R1-002
- Verify readiness: not-claimed

## Review inputs

- Diff/review surface: `e77a351c..09459a5f`, eight changed files.
- Tracked governing branch state: `28b57df6`, with M1 `review-requested`.
- Governing artifacts: approved simplification spec R14-R20 and R24-R29;
  BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, and
  BND-COMPAT-001; approved plan M1; test cases T1, T10, T12, and T14.
- Formal criteria: code-review-first-pass-v1,
  independent-review-gate-v1, and requirement-fidelity-gate-v1.
- Independence: L1 same-session blind-first context reset; the risk map was
  recorded before validation evidence was inspected.

## Diff summary

The slice adds a retirement-ledger library and regression test, inventories
the selector catalog and top-level proof scripts, records prospective R26
clause dispositions, and adds contributor script-admission guidance. It does
not delete or reroute existing acceptance checks.

## Finding PSR-CR-M1-R1-001

Finding ID: PSR-CR-M1-R1-001
Severity: major
Location: `scripts/retirement_ledger.py:94-102` and `scripts/test-retirement-ledger.py:93-106`
Evidence: Changing the first repository entry from `inventoried` to
  `removable` while leaving its existing strings `M2 dual proof pending`, `M2
  evidence pending; no M1 deletion`, and `Revert the bounded M2 consolidation
  commit` produces `[]` from `validate_ledger`. The validator checks only that
  three prose fields are nonempty; it does not require the completed
  old-versus-replacement comparison, exact command/results, removal decision,
  or prior `dual-proof` evidence required by R17-R20 and BND-STATE-001.
Required outcome: Make removal eligibility depend on structured, complete
  dual-proof, comparison, retirement-decision, and rollback evidence; add
  negative tests proving pending or placeholder evidence cannot become
  `removable` or `retired`.
Safe resolution path: Replace free-form eligibility fields with a small
  closed structured proof object (or validate an equally explicit existing
  structure), retain prose for human context, add unknown/incomplete/contradictory
  regression cases, and keep every M1 ledger entry `inventoried`.
needs-decision rationale: none
- Auto fix class: declared-safe. Inputs are the approved R17-R20 state model
  and current ledger; outputs are the library, tests, and M1 evidence only;
  forbidden paths are CI, selector, release, package, and skill bodies;
  acceptance is the targeted ledger suite plus existing M1 commands.

## Finding PSR-CR-M1-R1-002

Finding ID: PSR-CR-M1-R1-002
Severity: major
Location: `scripts/retirement_ledger.py:115-121` and `scripts/test-retirement-ledger.py:108-118`
Evidence: Changing `r26_disposition.R35` from
  `superseded-prospectively` to `still-required` produces `[]`. Both production
  validation and the test compare only the key set. This fails the exact
  prospective-disposition requirement in R26/T12 and violates the repository
  fail-closed rule for a new closed vocabulary.
Required outcome: Validate every R26 disposition value against the one
  approved value, reject unknown or contradictory values explicitly, and add
  a regression test named for the unknown-value failure.
Safe resolution path: Define the approved R26 value as a closed constant,
  compare both keys and values, and add a focused mutation test; do not change
  the governed clause list or deterministic parity clauses.
needs-decision rationale: none
- Auto fix class: mechanical. The exact value and clause set already exist in
  the approved spec and ledger; validation is `python scripts/test-retirement-ledger.py`.

## Checklist coverage

1. Spec alignment: block — both findings compress normative M1 properties.
2. Test coverage: block — current positive suite misses the two demonstrated mutations.
3. Edge cases: block — pending proof and unknown disposition values pass.
4. Error handling: concern — owner/state/disposition vocabularies fail closed, but R26 values and eligibility evidence do not.
5. Architecture boundaries: pass — the implementation is a library, not a new CLI, selector, cache, or scheduler.
6. Compatibility: pass — current acceptance invocation is unchanged and historical evidence remains present.
7. Security/privacy: pass — repository-local YAML only; no runtime, network, credentials, prompts, or transcripts.
8. Derived artifact currency: pass — no generated skill or package source changed.
9. Unrelated changes: pass — the diff is bounded to M1 inventory, contract disposition, admission guidance, tests, and evidence.
10. Validation evidence: concern — named M1 commands pass, but adversarial direct probes demonstrate their insufficiency.

## Requirement-fidelity result

Applicable and failed. R18-R20 require evidence before `removable`; T12
requires exact clause disposition. The implementation represents the fields
but omits their required properties, which is requirement compression.

## Milestone handoff

M1 remains open and moves to `resolution-needed`. Review-resolution must record
both accepted findings before implementation fixes. M2-M6 remain planned;
final closeout and verify are not ready.
