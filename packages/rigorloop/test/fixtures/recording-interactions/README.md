# Controlled recording interactions

The fixture builder and public subprocess harness are in [record-store-interactions.mjs](../../helpers/record-store-interactions.mjs). The four named cases are finding-with-neighbors, failed-verify-correction, applicability-reassessment and final-explanation-read. Every run creates and removes its own isolated project. It starts from identical v3 records containing 24 neighboring findings, 12 checks and complete review/decision/Verify narratives. These are scripted successful workflows, not agent trials. The single fixture model is the entire engineering decision basis for these narrowly defined tasks; no additional model, history, chat or resource reading is assumed. Engineering subjects contain the preservation and correction requirements and use actual byte identities.

Run semantic equivalence and public command checks with:

```sh
node --test packages/rigorloop/test/record-store-interactions.test.js
```

Both sides read the same engineering bytes and mechanically compute their identity. Finding append includes a non-writing preview on both sides. Applicability reassessment first records an explicit stale declaration, reads the resulting state, then records the independently supplied reassessment and current declaration in a separate transaction; both intermediate and final values must match between interfaces. Mutation cases include a follow-up read; the final-explanation case needs only its initial full report read. Stale retries and recovery are covered separately by TG-05/TG-FINAL tests. The baseline uses one combined read/hash tool call; targeted uses subject inspect.

Advanced operations inspect the complete store, construct full replacement records, check when preview is selected, record, then inspect the complete store again. Targeted operations select review/activity context, inspect the subject, load operation help, submit targeted edits and inspect affected entries. Final-report reads compare full advanced inspection with an explicit full Verify context selector. Both result sets are checked for identical stored semantic values and retained neighbors; byte formatting is intentionally a separate source-preservation proof.
