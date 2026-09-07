# Controlled recording interactions

The fixture builder and public subprocess harness are in [record-store-interactions.mjs](../../helpers/record-store-interactions.mjs). The four named cases are finding-with-neighbors, failed-verify-correction, applicability-reassessment and final-explanation-read. Every run creates and removes its own isolated project. It starts from identical v2 records containing 24 neighboring findings, 12 checks and complete review/decision/Verify narratives. These are scripted successful workflows, not agent trials. The single fixture model is the entire engineering decision basis for these narrowly defined tasks; no additional model, history, chat or resource reading is assumed. Engineering subjects contain the preservation and correction requirements and use actual byte identities.

Run semantic equivalence and public command checks with:

```sh
node --test packages/rigorloop/test/record-store-interactions.test.js
```

For token measurement, provide a Python environment with tiktoken==0.12.0 installed and run:

```sh
RIGORLOOP_TOKENIZER_PYTHON="$TOKENIZER_ENV/bin/python" node packages/rigorloop/test/helpers/record-store-interactions.mjs --measure
```

The tokenizer uses cl100k_base. The report records its actual version, Node version, per-category totals, call counts and call names. Setup/cleanup, fixture storage, assertions and measurement code do not contribute tokens; they are not actor interactions. Requests and responses remain in memory, are counted through stdin, and are never committed. Preserve only totals and interpretation in the owning change's evidence.

The advanced baseline loads the complete owning skill at baseline commit bd1c4bd3, plus an explicit comparative-use amendment selecting advanced v2 transport; that old skill's v1-only selection was never a shipped v2 normal interface. The targeted side loads the complete current owning skill plus every used mutation's help. Both sides read the same engineering bytes and mechanically compute their identity. Finding append includes a non-writing preview on both sides. Applicability reassessment first records an explicit stale declaration, reads the resulting state, then records the independently supplied reassessment and current declaration in a separate transaction; both intermediate and final values must match between interfaces. Mutation cases include a follow-up read; the final-explanation case needs only its initial full report read. These successful sequences incur no retry. Stale retries and recovery are separate TG-05/TG-FINAL tests, not silently counted as zero-cost successful recovery. The baseline uses one combined read/hash tool call; targeted uses subject inspect.

Advanced operations inspect the complete store, construct full replacement records, check when preview is selected, record, then inspect the complete store again. Targeted operations select review/activity context, inspect the subject, load operation help, submit targeted edits and inspect affected entries. Final-report reads compare full advanced inspection with an explicit full Verify context selector. Both result sets are checked for identical stored semantic values and retained neighbors; byte formatting is intentionally a separate source-preservation proof.

The comparison counts complete loaded guidance, command text, input requests, output responses and required follow-up reads. It excludes free-form model reasoning and model-specific message framing equally. It measures these explicit controlled workflows, not every possible agent interaction or a guaranteed percentage saving. Review must assess whether the selected context supplies an adequate decision basis and whether the result supports reduced routine reconstruction and avoidable context. An unfavorable or inconclusive result returns to the owning Design decision before adoption can be recommended. No fixed threshold or safety relaxation is allowed.
