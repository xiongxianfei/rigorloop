# Architecture Assessment: Boundary-First Proof Modeling

Stage: architecture-assessment
Applicability: required
Spec identity: sha256:cce7047761aaa99d81263cf226261e73de3de35e9064e93732274d3a3a8ae1f8

Architecture is required because the approved amendment changes the ownership
and interaction of canonical workflow specifications, eight published skills,
packaged resources, structural validators, proof fixtures, selector
registration, generated adapters, installed-resource parity, release
activation evidence, and the change-local capability-baseline report.
The R13 amendment also introduces a standalone behavior harness, isolated
child-runtime workspace, closed invocation profile, and immutable-run
publication/recovery boundary.

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
