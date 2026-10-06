# Interpretation and validation

[MOD-003](module.json) owns declared-profile interpretation, identity and model-rule diagnostics, and explicit migration preparation. [Conformance and migration preparation](conformance-and-migration.md) defines IR-005 behavior, realization and acceptance intent. AR-010 retains selected-profile interpretation; AR-067–069 add whole-model scope, distinct result meaning and isolated candidates. These are proposed Design responsibilities.

## Conformance responsibilities

<!-- architecture-diagram: conformance-responsibilities -->

```d2
direction: down
participant: "Engineering participant\nSelected state, scope, mapping and supplied assessments"
coordinator: "MOD-003 request coordinator\nCapture before pure interpretation"
storage: "MOD-001 / IF-001\nImmutable raw content and membership"
checks: "MOD-003 / IF-002\nDeclared-profile diagnostics and candidate preparation"
result: "Attributable result\nFindings, unassessed scope, candidate and readiness limits"
participant -> coordinator
coordinator -> storage
coordinator -> checks
checks -> result
```

Arrows show responsibilities used, not execution order or separate processes. The coordinator supplies captured raw input to pure IF-002 operations. Interpretation never recursively requests interpreted retrieval. MOD-003 presents mechanical findings separately from supplied judgments; MOD-007 retains semantic assurance and MOD-006 retains controlled adoption authority.

## Migration preparation interaction

<!-- architecture-diagram: migration-preparation-interaction -->

```d2
shape: sequence_diagram
participant: "Maintainer"
coordinator: "MOD-003 coordinator"
storage: "MOD-001 / IF-001"
pure: "MOD-003 pure IF-002 operations"
participant -> coordinator: "Source, target profiles, mapping and consumer scope"
coordinator -> storage: "Capture immutable raw source and complete membership"
storage -> coordinator: "Exact captured basis or acquisition gap"
coordinator -> pure: "Prepare isolated candidate from explicit mapping"
pure -> pure: "Account for source facts and validate target rules"
pure -> coordinator: "Candidate, transformation report and unresolved checks"
coordinator -> participant: "Candidate for review and declared consumer checks"
participant -> coordinator: "Supply exact candidate-bound compatibility evidence"
coordinator -> pure: "Reassess unchanged candidate and support"
pure -> coordinator: "Conformance, compatibility and readiness limits"
coordinator -> participant: "Report preparation only; source remains unchanged"
```

Unavailable acquisition or ambiguous mapping returns its explicit limit; the ordinary sequence does not imply preparation can continue with an unestablished basis. Supplied consumer checks may be incomplete, adverse or inapplicable and keep readiness unresolved. Changed candidate, mapping or source requires a new identified preparation. The returned candidate never adopts a profile, mutates a retained source or invokes operational-record migration.

The owning contract explains Development and Physical composition in the proposed local engine and walks SCN-011–014. Runtime commands, supported profile-pair qualification and an adoption writer remain separate delivery work.
