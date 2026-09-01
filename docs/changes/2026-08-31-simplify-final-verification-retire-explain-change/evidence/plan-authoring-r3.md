# Plan correction evidence

Artifact path: docs/plans/2026-08-31-simplify-final-verification-retire-explain-change.md
Artifact identity: sha256:5bdf89552ab9a0f88988c62f5d9ae57dae8e12a184d18bb678fc73254fa81514
Authoring result: complete

The revision binds Design Review R2 and removes the M5/M6 circularity. M5 produces a non-authoritative v3 candidate with this implementing change as the sole explicit preactivation exception. M6 closes the change through reviewed v2 source snapshot `585c2beecea0ddda0ae11ed8f0b1a53b24310052`, with archive, skill, CLI, mutation, and dual read-back proof. Only a separate post-M6 release action may prove zero nonterminal pre-v3 changes and activate v3.
