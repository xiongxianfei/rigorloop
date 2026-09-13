# Validation cleanup map refinement

Owning change: [unified Validation](change.json).

The M5 current-reader audit found additional cache-only goals, constraints, evidence locations, measurement prose, quality/risk rows and glossary terms in the mixed system architecture. The original map enumerated narrower sections and explicitly retained unlisted responsibilities. Removing the additional clauses without naming them would exceed that exact map, even though the approved direction already retires validation-result caching.

The Validation Design now enumerates those exact clauses and selected applicability corrections. It preserves actual-execution, command identity, honest evidence, privacy and closeout-assessment meaning under existing VAL-SR-12/15/17 and Assessment. It does not recreate obsolete evidence-kind fields, an operational cache reader, or a deterministic cache-hit closeout gate. Neighboring query-helper Workstream A/B sequencing, token-cost reports, release remote-state-cache prohibition, package/CLI behavior and historical judgments remain unchanged. Transitional scheduler prohibitions defer to the current Validation owner only for this explicitly selected initiative; no general retirement or measurement waiver is added.

Classification: bounded new-profile source-disposition refinement under the user's existing total-design/cleanup authorization, not a new product direction or a forced migration of the mixed architecture. Stable requirements, scenarios, implementation behavior and the three-model hierarchy are unchanged. No additional architecture clauses have been removed yet.

Observed checks: `python scripts/validate-boundary-first.py --check --path docs/design/engineering/validation.md` and `git diff --check` pass. Structural checks do not approve the map. Independent Design reassessment must cover the exact amended model and mapped source clauses before M5 reliance. Existing M1–M4 reviews retain their original subjects and implementation judgments; none is retargeted to approve this refinement.

Delivery impact: the existing plan already allocates mixed-architecture/consumer retirement to M5, source/reader reconciliation to TG-ADOPT, actual execution and invalid retired inputs to TG-CACHE/COMPOSE, and final model/package proof to TG-FINAL. The added enumeration changes no milestone, runtime behavior or command. Plan ownership will assess whether that unchanged allocation remains adequate against the newly assessed map; independent Delivery reliance review precedes M5 implementation. No existing work entries will be reinitialized.
