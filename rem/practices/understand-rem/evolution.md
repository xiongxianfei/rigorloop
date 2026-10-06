# 7. Change, Baseline, and Provenance

## 7. Change, Baseline, and Provenance

Evolution knowledge is built from the [Change, Baseline, Configuration Management, and Provenance concepts](../../concepts/evolution.md#evolution-and-history), Principles 10–12 and 15 in the [REM principles](../../principles/README.md), and the [Evolution model](../../models/README.md#evolution).

The core idea is:

```text
Baseline N
    │
    │ Change
    ▼
Baseline N+1
```

Current engineering definitions explain what is true now.
Changes explain why the current state evolved.
Configuration history preserves what was true before.

This is why REM is tool-independent.
A project may use Git or another configuration-management mechanism, but the REM concepts are Change, Baseline, Provenance, and recoverable history rather than Git-specific objects.

---
