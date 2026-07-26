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
- `scripts/boundary_proof_behavior.py` is a standalone behavior harness that
  may import only the Python standard library and `boundary_proof_model`; it
  does not import the workflow-automation engine, lifecycle validators, test
  drivers, or third-party packages;
- the harness binds exactly the five participating skill packages and every
  current resource-map entry, the applicable repository instruction chain,
  the governing contracts, scenario inputs, candidate oracles, and its own two
  implementation components;
- the harness launches one child runtime with a fresh configuration home and
  isolated workspace, records runtime version and executable identity plus the
  child-reported model ID, and applies closed instruction and tool profiles;
- the parent accepts output only after independently observing an effective
  runtime-native sandbox/profile that gives child tools workspace-only
  filesystem access and no network, connectors, or subagents;
- model-service control-plane transport and opaque authentication belong to
  the identified runtime, stay outside child tool authority and
  sandbox-readable roots, and are never serialized into evidence;
- the exact outer prompt is a deterministic harness constant combined with
  the identity-bound scenario; transient access observations must contain no
  unmanifested input or capability and are discarded after their typed result
  is recorded;
- behavior generation validates and installs one immutable run, writes and
  fsyncs a prepared receipt, atomically replaces and fsyncs the current
  pointer, fsyncs the parent directory, and removes the reconciled receipt;
  the receipt makes these writes recoverable rather than jointly atomic;
  deterministic validation checks the run and current identities without
  reinvoking lifecycle skills or replacing its recorded invocation profile;
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
- Reuse the workflow-automation engine as the behavior harness: rejected
  because its dynamic state, migration, and validation dependencies create an
  open execution surface and make the proof mechanism depend on the mechanism
  being observed.
- Reconstruct a transitive repository dependency graph: rejected because
  dynamic imports, runtime instructions, conditionals, and resource loading
  make that graph incomplete and difficult to validate. A standalone
  two-module boundary is smaller and enforceable.
- Run lifecycle skills in the parent process: rejected because caller context,
  tools, configuration, and filesystem authority would become unbound inputs.
- Persist raw access logs as durable evidence: rejected because they can expose
  local paths or runtime details and still do not independently prove
  confinement. Parent-observed enforcement is reduced to bounded typed
  attestation and diagnostics.
- Permit general child-tool network access: rejected because it creates
  undeclared inputs and egress. Only the identified runtime's model-service
  control-plane transport is allowed outside the child tool profile.

## Consequences

- The implementation adds one typed model module, one validator CLI, one test
  module, one standalone behavior harness, one fixture family, selector
  registration, eight skill projections, copied mapped references, immutable
  behavior-run evidence, and one change-specific capability report.
- The copied reference increases packaged bytes but is loaded on demand and is
  identical across supported skills and adapter targets.
- Any vocabulary change requires a spec amendment before code changes.
- Unknown values, duplicate or orphan references, mismatched versions, missing
  fixtures, stale adapters, and asserted report results fail closed.
- Public activation and rollback operate on one release unit and cannot leave
  mixed `v1` surfaces.
- Capability-preserving progressive disclosure remains paused until the
  complete baseline and final verification pass.
- Canonical behavior generation requires a supported runtime-native sandbox,
  independently observable effective settings, and secure control-plane
  authentication; unsupported environments stop with
  `environment-unavailable`.
- Each behavior run incurs nondeterministic model execution cost; validation
  reuses bound immutable evidence and never reinvokes skills.
- Transient access observations reduce privacy exposure but limit later raw-log
  forensics; durable records retain bounded attestation, result, and
  diagnostics only.
- Immutable run installation, receipt persistence, pointer replacement,
  directory fsync, and receipt cleanup are separate recoverable writes and
  require explicit crash-point tests.

## Follow-up

- Architecture-review R4 accepted this amendment for plan and test-spec
  reliance.
- The execution plan must order typed model and fixtures before skill rollout.
- The test spec must map R28-R28z and R56-R56q before implementation.
- The revised plan begins with child-runtime sandbox and credential-isolation
  feasibility proof before the complete harness is implemented.
