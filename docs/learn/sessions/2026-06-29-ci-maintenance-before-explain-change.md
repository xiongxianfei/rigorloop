# Learn Session: CI Maintenance Before Explain Change

## Status

- Session status: captured
- Trigger type: explicit maintainer request
- Trigger: `$learn if ci-maintance is required, it should be required before explain-change.`
- Session date: 2026-06-29
- Routing status: no derivative routing performed

## Frame

Scope:

- Capture whether CI-maintenance work should precede `explain-change` when the workflow discovers a CI or validation-infrastructure gap.
- Ground the observation in the release transaction automation workflow evidence.

Evidence reviewed:

- `docs/workflows.md`
- `docs/changes/2026-06-29-release-transaction-automation/verify-report.md`
- `docs/changes/2026-06-29-release-transaction-automation/explain-change.md`
- `docs/plans/2026-06-29-release-transaction-automation.md`
- `docs/plan.md`

Explicit exclusions:

- No workflow policy update in this session.
- No skill contract update in this session.
- No topic-file durable lesson entry in this session.
- No PR readiness, branch readiness, or CI status claim from this session.

## Observations

### O1 - The workflow order already places CI maintenance before explanation

Evidence:

- `docs/workflows.md` defines the standard flow as:
  `implement -> code-review -> review-resolution when triggered -> ci-maintenance when triggered -> explain-change -> verify -> pr`.

Observation:

The maintainer rule matches the existing workflow order. If `ci-maintenance` is known to be required, it should run before `explain-change`.

### O2 - This run discovered the CI-maintenance trigger too late

Evidence:

- The release transaction automation verify report recorded blocker `RTA-VERIFY-B1`: the repo-owned CI wrapper could not validate the final changed path set because selector routing rejected the new release transaction scripts and fixture directories.
- The active plan records the sequence: `explain-change` was recorded, then `verify` found the selector-routing blocker, then `ci-maintenance` added deterministic `release_transaction.regression` routing, then `explain-change` was refreshed.
- The refreshed explain-change explicitly covers the CI-maintenance selector-routing diff.

Observation:

The avoidable cost was not the formal stage order. The cost came from failing to detect the CI-maintenance need before the first `explain-change`.

### O3 - The reusable process check is pre-explanation CI-maintenance detection

Evidence:

- The blocker was exposed by selector/CI-wrapper coverage of the final changed path set.
- Once `ci-maintenance` added selector routing, the explanation had to be regenerated to include that new diff.

Observation:

Before writing final change rationale, the workflow should confirm whether the final changed path set is already covered by repo-owned CI routing. If selector or CI-wrapper routing is missing, route to `ci-maintenance` first, then write or refresh `explain-change`.

## Classification

| ID | Proposed classification | Final classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | none | maintainer request and workflow evidence | The stage order is already captured in `docs/workflows.md`; no new policy is needed from this observation alone. |
| O2 | process-follow-up | process-follow-up candidate | workflow or skill guidance update | pending contributor confirmation for derivative edit | The evidence shows an avoidable workflow loop in this run, but `learn` is not the authoritative policy owner. |
| O3 | artifact-update candidate | artifact-update candidate | add pre-explain CI-routing detection guidance to the owning workflow or skill artifact | pending contributor confirmation for derivative edit | The likely fix is an earlier detection check, not another release automation code change. |

## Route

No derivative routing was performed in this session.

Recommended follow-up for an owning workflow or skill artifact:

```text
Before explain-change, check whether the final changed path set requires CI
maintenance. If repo-owned selector or CI-wrapper routing is missing, run
ci-maintenance before writing or refreshing explain-change.
```

Candidate proof check:

```bash
bash scripts/ci.sh --mode explicit --path <final changed paths>
```

or, where cheaper and sufficient:

```bash
python scripts/select-validation.py --mode explicit --path <final changed paths>
```

## Outcome

The lesson captured here is:

```text
Known or discovered CI-maintenance work belongs before explain-change.

The practical guardrail is to detect CI-maintenance triggers before explanation,
especially selector or CI-wrapper gaps for the final changed path set.
```

This session does not make new workflow policy authoritative. It records the evidence and the recommended routing target.
