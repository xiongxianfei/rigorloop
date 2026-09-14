# Script Output Optimization

This topic is curated learn guidance. [Validation](../../design/engineering/validation.md) owns current execution and reporting behavior.

## 2026-05-22: Optimize Every Output Layer, Not Just One Producer

- Source session: `docs/learn/sessions/2026-05-22-layered-script-output-compaction.md`
- Primary classification: `durable-lesson`
- Secondary routes: future proposal candidate for broad-smoke and remaining unittest fixture script output

When script output remains noisy after an output-compaction change, check whether the optimization covered every layer that can print:

- producer scripts;
- wrapper scripts;
- CI orchestration modes;
- test-runner defaults;
- UI transcript folding.

The source session describes a historical wrapper implementation. Current catalog execution is in `scripts/validation_execution.py`; its output and case receipts must preserve failures across producer, wrapper and runner boundaries.

Best practice:

- map all output layers before scoping the change;
- capture child output in wrappers and print it only on failure or `--verbose`;
- give each high-use unittest script a compact default success line, actionable failure output, and a `--verbose` escape hatch;
- avoid global redirection that hides failure evidence;
- treat UI transcript truncation as display behavior, not script-output optimization.

The root invariant remains evidence preservation: output should shrink only after pass/fail status, counts, durations, failure reasons, rerun guidance, and exit behavior stay available.
