# Token Cost Measurement

This topic is curated learn guidance. Authoritative release benchmark rules remain in `specs/release-token-friendliness-benchmark-for-skills.md`, `docs/reports/token-cost/releases/`, release validation scripts, and workflow guidance.

## 2026-05-11: Separate Static Size, Runtime Reads, Command Output, and Context Base

- Source session: `docs/learn/sessions/2026-05-11-dynamic-token-cost-root-cause.md`
- Primary classification: `durable-lesson`
- Secondary routes: candidate future optimization proposal; no authoritative artifact update in this session

Release token-friendliness needs both static and dynamic measurement. Static size identifies large public skill surfaces, but dynamic runs reveal whether agents actually read whole installed skill files, perform broad searches, or emit large command output during ordinary use.

The `v0.1.1` baseline showed this split clearly:

- `workflow` exceeded the static high-warning threshold.
- `code-review` exceeded the static warning threshold.
- all seven runtime benchmarks confirmed skill-file reads.
- `verify-final-pack` exceeded the dynamic input-token warning threshold.
- the largest single command output was below the command-output warning threshold, so total dynamic input could not be explained by command output alone.

Best practice is to diagnose token cost by category before optimizing:

- static skill size;
- dynamic input and cached input;
- command-output amplification;
- full-file, repeated-file, generated-output, and broad-search signals;
- public skill portability.

Optimize the largest repeated cost driver first, but preserve safety-critical guidance. Prefer progressive loading, tighter triggers, concise result shapes, targeted section reads, and bounded excerpts before deleting or weakening workflow, review, verification, or safety guidance.
