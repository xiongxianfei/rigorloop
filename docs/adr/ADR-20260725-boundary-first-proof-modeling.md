# ADR-20260725-boundary-first-proof-modeling: Boundary-First Proof Architecture

## Status

accepted

## Context

Examples demonstrate behavior but do not enumerate trust, identity, state,
authority, mutation, recovery, composition, compatibility, outcome, and
evidence boundaries.
The approved boundary-first amendments require one versioned model across
feature specs, test specs, eight public lifecycle skills, deterministic
validation, incident replay, generated adapters, and release activation.

The architecture must preserve normative ownership in approved specs, avoid a
new lifecycle stage or universal per-change artifact, make installed skills
self-contained, and prevent structural validators from claiming semantic
completeness.

## Decision

Use one spec-normative boundary model with these projections:

- `specs/rigorloop-workflow.md` owns boundary vocabulary, artifact records,
  adoption, lifecycle gates, fixtures, report aggregation, and activation;
- `specs/skill-contract.md` owns the eight-skill portable projection;
- `scripts/boundary_proof_model.py` is the only typed executable projection of
  closed constants, record parsing, and pure capability aggregation;
- `scripts/validate-boundary-proof.py` performs structural, vocabulary,
  traceability, version-parity, fixture, and aggregate validation and is the
  only component permitted to serialize or replace the canonical capability
  report;
- `tests/fixtures/boundary-proof/` and
  `scripts/test-boundary-proof.py` own deterministic regression proof;
- `templates/shared/boundary-proof-model.md` is copied byte-for-byte into a
  mapped `references/boundary-proof-model.md` resource for each of the eight
  in-scope skills;
- stage-specific triggers, stops, claims, and handoffs remain in each
  `SKILL.md`;
- existing adapter generation and resource-integrity validation carry the
  mapped reference through generated, packed, and installed outputs;
- the first capability result is computed in the one R28y change-local report;
- tracked release notes activate `v1` only by binding an actual release tag to
  the passing report's raw-byte SHA-256.

Reviewers retain semantic completeness judgment.
No validator may infer domain completeness from table presence.
The pure evaluator performs no filesystem mutation, and release tooling reads
the validated report identity without rewriting the report.

## Alternatives considered

- Keep the model only in skill prose: rejected because eight copies would
  become competing normative contracts.
- Put one repository-root reference outside skill packages: rejected because
  installed public skills would not be self-contained.
- Duplicate independently authored references in eight skills: rejected
  because drift would be likely and difficult to audit.
- Generate references into canonical skill source: rejected because
  `skills/` must remain authored source and existing resource rules already
  support reviewed copies and drift checks.
- Add a standalone boundary artifact or lifecycle stage: rejected by the
  approved proposal and spec.
- Let validators score semantic completeness: rejected because applicability,
  meaningful partitions, hazards, and adversarial sufficiency require review
  judgment.

## Consequences

- The implementation adds one typed model module, one validator CLI, one test
  module, one fixture family, selector registration, eight skill projections,
  copied mapped references, and one change-specific capability report.
- The copied reference increases packaged bytes but is loaded on demand and is
  identical across supported skills and adapter targets.
- Any vocabulary change requires a spec amendment before code changes.
- Unknown values, duplicate or orphan references, mismatched versions, missing
  fixtures, stale adapters, and asserted report results fail closed.
- Public activation and rollback operate on one release unit and cannot leave
  mixed `v1` surfaces.
- Capability-preserving progressive disclosure remains paused until the
  complete baseline and final verification pass.

## Follow-up

- Architecture review must accept this ADR before planning.
- The execution plan must order typed model and fixtures before skill rollout.
- The test spec must map R28-R28z and R56-R56q before implementation.
- On architecture-review approval, change this ADR to `accepted`.
