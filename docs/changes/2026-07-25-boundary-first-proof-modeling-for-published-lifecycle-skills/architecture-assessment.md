# Architecture Assessment: Boundary-First Proof Modeling

Stage: architecture-assessment
Applicability: required
Spec identity: sha256:29d7f1555f937ee835733d44b6e9386fae7a4203e596ef5ded483e3551bb76a3

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
