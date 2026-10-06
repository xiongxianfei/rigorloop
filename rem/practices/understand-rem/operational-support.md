# 5. Operational Support

## 5. Operational Support

REM Operational Support is built from the engineering-model and metamodel [Concepts](../../concepts/model-support.md#engineering-model-and-its-support), the metamodel and tool-independence [Principles](../../principles/README.md), and the [Operational Support model](../../models/operational-support.md).

Operational Support answers how the engineering model itself is:

- represented;
- named;
- validated;
- authored;
- maintained;
- migrated;
- versioned;
- interpreted across historical states.

The [Operational Support model](../../models/operational-support.md) deliberately separates universal REM semantics from project representation choices.

For example:

```text
REM concept:
stable engineering identity

project representation:
JSON field, database key, repository identifier, or another mechanism
```

This is why REM does not define Git, JSON, Rust, or filesystem layout as universal methodology requirements.

A dedicated Operational Support procedure has not yet been authored in [Methods](../../methods/README.md).
Until one exists, the model defines the required semantics while project-specific procedures remain outside the universal REM method.

---
