# Review and verification

Responsibility and allocation are defined in [module.json](module.json).

## Supporting contracts

These documents retain detailed clauses and proof under this Module; they are not additional REM entities.

- [Review and Closeout](assessment.md)
- [Assurance content and current reliance](assurance-content.md)

## Assurance responsibilities

The proposed IR-004 design separates attributable content preparation from recording and execution. AR-062–066 constrain MOD-007's FUNC-027–031; MOD-017 owns the external preparation contract. Arrows below mean contract use and contribution, not execution order or process containment.

<!-- architecture-diagram: assurance-responsibilities -->

```d2
direction: right
participant: "Accountable assessor\nMethods, observations and reasoning"
guide: "MOD-012\nGuided assessment and recording"
governance: "MOD-017 / IF-014\nAssurance content preparation"
assurance: "MOD-007 / AR-062–066\nDefinition, observation, applicability,\ncoverage and judgment meaning"
operations: "MOD-018 / IF-004\nExplicit command outcome"
records: "MOD-011 / IF-003\nActual retained content and basis"
participant -> guide
guide -> governance
governance -> assurance
guide -> operations
operations -> records
```

MOD-010 mediates IF-003 within MOD-018. IF-010 supplies claim-support analysis; IF-009 supplies separate authority. MOD-007 contributes semantics without directly calling storage. A saved result cannot supply an engineering conclusion, and prepared content cannot establish retention. The owning [contract](assurance-content.md) defines Development, Physical and Scenario composition and its manual/agent-assisted realization.

## Assurance preparation and retention

<!-- architecture-diagram: assurance-preparation-and-retention -->

```d2
shape: sequence_diagram
assessor: "Assessor"
guide: "MOD-012"
governance: "MOD-017 / MOD-007"
operations: "MOD-018 / MOD-010 / MOD-011"
assessor -> guide: "Supply actual content and exact basis"
guide -> governance: "IF-014: prepare and inspect content"
governance -> guide: "Prepared content, gaps and reliance limits"
guide -> assessor: "Expose unresolved semantic decisions"
assessor -> guide: "Supply accountable resolution or incomplete content"
guide -> governance: "If content or basis changed: prepare revised candidate"
governance -> guide: "Revised content and reliance limits"
guide -> operations: "IF-004: explicit selected recording request"
operations -> guide: "Actual saved, conflict, failed or unresolved outcome"
guide -> operations: "Scoped readback when effects are uncertain"
operations -> guide: "Retained content and observed basis, or remaining limits"
guide -> assessor: "Report actual retention; preserve judgment scope"
```

The recording step applies only to an admitted actor-selected candidate under the chosen contract. Changed semantic content or basis takes the conditional preparation loop; unchanged admitted content can proceed directly. Unresolved semantic content can be retained as incomplete where supported, never as justified favorable reliance. A conflict requires fresh context and reassessment; readback is not automatic replay. Technique execution precedes an actual observation and remains outside these recording interactions.
