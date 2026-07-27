# Architecture Assessment: Boundary-First Proof Modeling

Stage: architecture-assessment
Applicability: required
Spec identity: sha256:92637e7c7cb28a289da981c53024422c88f225e66e8a1952d4e5871b14f62563

Architecture is required because the approved amendment changes the ownership
and interaction of canonical workflow specifications, eight published skills,
packaged resources, structural validators, proof fixtures, selector
registration, generated adapters, installed-resource parity, release
activation evidence, and the change-local capability-baseline report.
The approved R28y amendment also introduces a standalone behavior harness,
isolated child-runtime workspace, closed invocation and transport profiles,
typed transport/output reconciliation, runtime diagnostic/checkpoint
boundaries, and lock/lease/receipt-backed immutable publication with
discard-only recovery.

The architecture update must preserve the approved ownership ledger:

- workflow specs own boundary vocabularies, adoption, stage gates, and baseline
  completion;
- the skill contract owns portable published-skill projection;
- feature specs own behavior-specific boundary models;
- matching test specs own executable proof maps;
- validators own syntax, closed vocabularies, and trace integrity;
- reviewers retain semantic completeness judgment.

The accepted architecture amendment must place the standalone harness without
making it a second workflow engine, distinguish child-tool network denial from
runtime model-service transport, keep raw access observations transient, and
bind the deterministic outer prompt through the harness and scenario
identities.

The approved R40 amendment changes one previously accepted interaction:
schema-constrained stage messages, rather than direct stage-agent filesystem
writes, carry stage-authored semantic bytes. Architecture must therefore:

- keep the stage-owning skill as the sole semantic author;
- bind lifecycle and canary artifact policies at their distinct ownership
  surfaces;
- separate bounded candidate collection, envelope reconciliation, exact-byte
  materialization, and structural lifecycle validation;
- retain timeout-observed candidates until reconciliation without persisting
  raw failed content;
- prove actual stage-envelope materialization during preflight;
- preserve immutable publication, recovery, runtime confinement, and the
  standalone two-module implementation boundary.

The approved R48 amendment strengthens that transport boundary:

- child commands and detached descendants have read-only workspace access and
  no writable root;
- one deny-only file-change authorization policy governs capability-state-
  appropriate proof, canary, lifecycle, retry, and no-child reconciliation
  behavior;
- the parent retains a root descriptor and completes bounded no-follow
  baseline/post-turn integrity inspection before materialization;
- one immutable typed projection binds exact launcher and runtime-package
  bytes, schemas, protocol and feature classifications, enabled/disabled
  features, and file-change capability state;
- both capability states require fresh invocation-owned conformance against
  the installed production deny-only dispatcher;
- exposed capability additionally requires a correlated live decline trace;
- reviewed non-exposure additionally requires the exact projection, a
  complete effective-tool projection, and drift-event rejection;
- current runtime attestation, preflight, and implementation-manifest evidence
  use v3; v2 is unsupported historical evidence; and
- the sole registered v1 manifest is exact-identity opaque history and cannot
  satisfy a current role.

Architecture must update the Runtime View, crosscutting trust and transport
boundaries, component diagram, permission-profile relationship, and one
acceptance-conditional superseding ADR without reopening the approved
semantic-envelope contract. Architecture-review approval is required before
the plan or test spec may project the v3 contract.
