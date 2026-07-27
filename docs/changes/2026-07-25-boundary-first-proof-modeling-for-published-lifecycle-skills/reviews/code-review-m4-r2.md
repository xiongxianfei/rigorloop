# Code Review M4 R2

Review ID: code-review-m4-r2

Stage: code-review

Round: 2

Reviewer: Codex code-review skill

Target: M4 correction through `09bd2758`

Reviewed artifact: implementation diff `f5757ac7..09bd2758`

Reviewed milestone: M4

Status: approved

Review status: clean-with-notes

Material findings: None

Immediate next stage: final holistic code review

Milestone closeout: closed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: clean-with-notes

Review gate outcome: advance

Independence level: L1

Author context ID: boundary-m4-resolution

Reviewer context ID: boundary-m4-review-r2-reset

Context separation mechanism: blind-first diff, typed-result, and canonical
reconstruction inspection before validation summaries or R1 finding content

Risk tier: elevated

Risk-tier triggers: generated evidence, public adapter parity, release
activation semantics, selector routing, canonical reconstruction, and final
capability aggregation

Risk-tier classifier: generated-evidence, requirement-fidelity, release, and
validation triggers

Governing artifacts: `specs/rigorloop-workflow.md` R28n-R28p and R28y-R28z;
`specs/rigorloop-workflow.test.md` T46, T47, T50, T52, and T54;
`docs/plans/2026-07-25-boundary-first-proof-modeling.md` M4

Formal criteria: fresh closed-operation execution, exact typed result and
dependency identities, complete report projection, reconstruction-only
validation, bounded correction outcome comparison, four-surface parity, exact
selector routing, and release non-activation

Initial packet inventory: specs/rigorloop-workflow.md@09bd2758#sha256:c339ceed9592ec069cb94efd4774ad60ab9829983320fab1a3f22ea128e06ced; specs/rigorloop-workflow.test.md@09bd2758#sha256:e627ff46ca104c7ec26114b42545e81500ecb2137540923f10bf5bd7c1eeccec; scripts/boundary_proof_model.py@09bd2758#sha256:ef2a23e4ecfe81de9958c960fd3de28a41fefd2b9767ccadb23b9ac7495bb67b; scripts/validate-boundary-proof.py@09bd2758#sha256:8d90032b83629c9ab027af1ae92d8e44e5f1960d78df2c2eb2a85cf5a834c7bb; scripts/test-boundary-proof.py@09bd2758#sha256:de67cad4520ce913dd690fd6cc974f6467e04e16915821c3bc83e0bbdd4e7022; docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md@09bd2758#sha256:4cfacf61164795d4e227e97f93211e70b8f1554162ee5381b8ef36bc24f33b1c

Prompt template version: code-review-template-v1

Initial packet hash: sha256:c4c4dd975546920c4edfebf8dceba1b0d018a5948e07870065732238e259a5c6

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: typed operation construction, report projection and
reconstruction, live outcome-envelope comparison, current behavior selection,
selector routing, adapter parity, and release activation proof.

Highest-impact failure modes: asserted pass rows, omitted operations, stale or
reordered dependencies, model-path-sensitive false negatives, current-pointer
staleness, partial parity, or report validation that trusts serialized output.

Changed boundaries: typed operation results versus report rows; JSON mapping
semantics versus normative sequence order; deterministic validation versus
lifecycle reinvocation; current candidate evidence versus immutable release
history.

Evidence expected: exactly one result for every closed operation, canonical
result identities, complete direct dependencies, current input/output
references, report reconstruction equality, closed outcome-envelope contrasts,
four-surface parity, selector proof, and explicit non-activation evidence.

Areas requiring direct inspection: `OPERATION_IDS`, result identity
construction, result projection, dependency checking, canonical report
generation and validation, scenario parsing/comparison, current pointer,
report bytes, selector changes, parity generation, and release fixtures.

Areas intentionally out of scope: release activation, publication, deployment,
PR creation, and progressive-disclosure resumption.

Risk classes considered: authorization=not-applicable;
generated-evidence=applicable; validation=applicable;
requirement-fidelity=applicable; release=applicable; security/privacy=applicable
only to retained bounded evidence and child-input isolation

Falsifiable review questions: Can a projected row pass without a freshly reconstructed typed result?
- Can a projected row pass without a freshly reconstructed typed result?
- Can a dependency identity or order change without invalidating validation?
- Can canonical object-key ordering create false failure or conceal a missing
  support operation?
- Can scenario expectations influence child requests or correction routing?
- Can the report claim adapter parity or activation without current evidence?

## Result

- Skill: code-review
- Status: completed
- Open blockers: none at the M4 milestone gate
- Next stage: final holistic code review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Reviewed milestone: M4
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no after R1 reconciliation
- Verify readiness: not-claimed

## Diff summary

The M4 correction adds one closed typed operation graph, derives every report
row from current operation results, records canonical result identities and
ordered direct dependencies, projects diagnostic and observation data, and
reconstructs the complete report before accepting it. It also replaces one
predicted live model path with the approved closed correction outcome envelope
and preserves both failed runs through explicit recovery. The final report
binds current behavior run `run-62735d2bff6ab29bfe208183cf33fc03`,
four durable adapter parity manifests, and current canonical skill resources.

## Prior finding reconciliation

`BFP-CR-M4-1`: resolved.

Direct inspection confirms:

- `OPERATION_IDS` contains the complete R28y registry in normative order;
- `_operation` computes canonical result identities from all eight typed
  fields other than `result_identity`;
- `_build_operation_results` owns fresh result construction and exact direct
  dependencies;
- `_report_from_operations` is the only production row projection;
- `validate_report` independently rebuilds results and requires exact report
  equality before computing pass; and
- the canonical report contains `support`, `simple_change`, diagnostic IDs,
  operation identities, dependency results, observations, and the computed
  aggregate.

The initial reconstruction failure also proved validation was not trusting the
writer. Its correction treats JSON mappings as unordered exact key sets while
retaining ordering for the operation registry, fixture list, evaluated skills,
check IDs, and dependency lists.

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R28y typed operations, selectors, outcome envelope, and non-activation are projected without widening scope. |
| Test coverage | pass | 115 boundary tests include missing support, dependency reorder/staleness, canonical mapping order, outcome membership, closed schema, and multiple-correction contrasts. |
| Edge cases | pass | Unknown values, missing operations, stale identities, invalid branch/role membership, repeated corrections, partial activation, and rollback are covered. |
| Error handling | pass | Invalid current evidence, report mismatches, stale dependencies, and unsupported values fail closed before pass. |
| Architecture boundaries | pass | Parent-only expectations, immutable behavior publication, sole report writer, and validation-only reuse remain intact. |
| Compatibility | pass | Canonical/generated/packed/installed parity and historical release regressions pass without changing published artifacts. |
| Security/privacy | pass | Scenario expectations remain outside child requests; retained evidence uses normalized references and no secret values. |
| Derived artifact currency | pass | The current pointer, behavior manifest, parity manifests, and report reconstruct against commit `09bd2758`. |
| Unrelated changes | pass | The amendment is limited to M4 proof, the exposed scenario contract flaw, required lifecycle evidence, and recovery records. |
| Validation evidence | pass | Selector 134, adapter 132, release 87, boundary 115, skill-validator 261, skill validation, generated-skill drift, adapter archive validation, behavior validation, and report reconstruction all pass. |

## Requirement-fidelity receipt

Applicability: applicable.

The review decomposed R28y into registry closure, typed field closure,
canonical identity, direct dependency identity/order, exact input/output
selection, report projection, validation-only reconstruction, current behavior
selection, outcome-envelope comparison, parity, aggregation, and
non-activation properties. Each property is present on its required model,
writer, validator, fixture/test, and evidence surface. No required property is
compressed into a global substring or asserted report value.

## Clean-review sufficiency receipt

Review target identity: `09bd2758f8f66358a14c1ecb54c39de27e47a10b`

Independence level: L1 tracked-artifact context reset.

Governing artifacts inspected: R28y/R28z feature contract, T46/T47/T50/T52/T54
proof map, M4 plan and validation record, R1 review resolution, typed model,
report writer/validator, focused tests, current run manifest, and canonical
report.

Adversarial hypotheses tested: asserted rows, missing support, reordered and
stale dependencies, unordered mapping reconstruction, expectation leakage,
excess corrections, stale behavior identity, partial parity, and accidental
release activation.

Direct proofs performed: inspected operation construction and projection;
mutated missing support, dependency order and identity, scenario envelopes,
and canonical mapping order; validated the current immutable run; regenerated
and independently reconstructed the canonical report; and ran selector,
adapter, release, boundary, and skill suites.

Validation evidence challenged: passing suites were accepted only after direct
inspection showed they exercise the changed boundary. The first failed
reconstruction was retained as evidence that writer output is independently
checked.

Unreviewed surfaces: no release publication or external adapter
installation was performed; those are explicitly outside M4.

Confidence: high for M4 milestone closure.

No-finding rationale: the implementation now has one executable typed graph,
one report projection, and one independent reconstruction path; direct
negative tests cover the named escape classes, and fresh current evidence
passes without claiming final R28o or release readiness.

## Handoff

M4 may close. A separate final holistic code review must cover the complete
cross-milestone diff and all resolved findings before `explain-change`.
