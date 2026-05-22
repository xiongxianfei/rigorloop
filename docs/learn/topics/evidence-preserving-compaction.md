# Evidence-Preserving Compaction

This topic is curated learn guidance. Authoritative behavior, validation, workflow, and data-contract rules remain in accepted proposals, approved specs, active plans, validator scripts, and review-resolution artifacts.

## 2026-05-21: Compress the Safe Surface, Pin the Preservation Mechanism

- Source session: `docs/learn/sessions/2026-05-21-evidence-preserving-compaction.md`
- Primary classification: `durable-lesson`
- Secondary routes: existing compact-metadata review-resolution owns open spec fixes; no new follow-up created

When noisy output or metadata is expensive to read, first separate the surface that is safe to compress from the evidence or behavior that must be preserved.

Safe compression examples include presentation output, common-read summaries, repeated command templates, repeated path prefixes, and extracted skeleton text. Preserved invariants include selected checks, exit behavior, failure detection, exact commands and path sets, parser-owned fields, status vocabularies, structured counts, blockers, and transcript recoverability.

Do not claim that a compact form is reconstructable, parser-valid by construction, or behavior-preserving until the mechanism is explicit and testable. Examples:

- path-expanding validation bundles need deterministic accumulation or full resolved path sets;
- review findings need parser-owned field labels, not only equivalent prose;
- quiet script output needs unchanged command selection, exit codes, and failure reporting.

Efficiency metrics are useful only under a preservation gate. A byte, token, or output-line reduction proves the mechanism helped, but it cannot compensate for lost audit evidence or changed validation behavior.
