# Explain Change: Architecture-Review Skill Simplification

## Summary

This change makes `architecture-review` smaller on every supported loading path while preserving its review judgment, durable recording, exact lifecycle settlement, retry, isolation, and claim boundaries. The flat skill became a compact universal `SKILL.md` plus one conditional architecture-package method reference and one conditional recording-and-settlement reference; no structural asset, runtime engine, lifecycle state, or persistence owner was added.

## Problem

The prior skill loaded universal review policy, detailed C4 and arc42 method, ADR procedure, durable recording, multi-target settlement, automation, and retry behavior together for every invocation. That made ordinary record-only reviews and isolated reviews carry procedure they did not use, obscured rule ownership, and made maintenance more likely to duplicate or weaken shared contracts.

## Decision trail

- The proposal selected Option 3: keep universal judgment inline and extract two references at real activation boundaries. Flat retention, editorial compression, method-only extraction, fragmented references, and an executable review engine were rejected because they either preserved common-path overload, left recording mechanics inline, added navigation, or introduced disproportionate runtime machinery.
- Requirements R1-R10 establish the three-resource package, universal ownership, exact resource behavior, and byte-identical shared recording block. R11-R19 close surfaces, modes, authority combinations, durable-recording triggers, isolation, and loaded assemblies. R20-R46 close review identity, governing basis, evidence-scoped target disposition, prepared settlement, retry, concurrency, and bounded mutation. R47-R58 govern result compatibility, preservation ledgers, measurement, package parity, portable language, runtime exclusion, and architecture fallback.
- The bounded architecture assessment concluded `architecture-not-required` because the existing packaged-skill model and formal-review Markdown evidence already support conditional references and a prepared settlement manifest without a new schema, durable artifact, lifecycle state, or write owner.
- M1 froze semantic rules, literal dependencies, scenario contracts, evidence capability, and size baselines. M2 implemented the compact package and focused contract tests. M3 proved real-profile reduction, semantic preservation, boundary coverage, and canonical-through-installed parity. M4 owns final review, explanation, and verification.

## Diff rationale by area

| Area | Change | Reason | Source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/architecture-review/SKILL.md` | Reduced the universal file to review authority, evidence, classification, judgment, materiality, shared isolation, stops, claims, resource triggers, and compact results. | Universal safety remains available for every invocation without loading conditional procedure. | R1-R19, R47-R49, R57 | T1-T5, T12-T14; focused package tests |
| `skills/architecture-review/references/architecture-package-review.md` | Added reviewer-specific C4, arc42, diagram, canonical-link, ADR, and package-consistency procedure. | Detailed architecture method now loads only for canonical-package and ADR surfaces. | R3-R7 | T1-T4 |
| `skills/architecture-review/references/architecture-review-recording-and-settlement.md` | Added durable placement, exact subject and basis, target dispositions, prepared manifests, retry, concurrency, automation, and settlement procedure. | Formal and durable review mechanics now have one conditional owner while preserving exact authority. | R4-R7, R15-R46 | T4-T11 |
| `scripts/test-skill-validator.py` | Added closed-vocabulary, package-assembly, shared-block, identity, disposition, prepared-manifest, missing-resource, claim, and profile-reduction tests; adjusted directly coupled assertions to the new owners. | Deterministic proof prevents semantic loss and unknown-value fall-through without freezing incidental prose. | R50-R56 | T1-T14 |
| Change-local ledgers and fixtures | Recorded one owner and disposition for every semantic rule and compatibility literal, 26 static transaction scenarios, invalid vocabulary fixtures, manifest capability, and the flat baseline. | The refactor can be reviewed as an ownership migration rather than assumed-equivalent prose movement. | R50-R54, R58 | CMD1; M1 evidence |
| Measurement and parity evidence | Recorded every loaded profile, each resource, the total package, semantic preservation, boundary proof, and adapter-chain parity. | A shorter main file alone is insufficient; real formal profiles and the complete package must improve and remain shippable. | R53-R56 | CMD2-CMD8; M3 evidence |
| Lifecycle and review artifacts | Recorded proposal, spec, plan, test-spec, milestone reviews, two final review findings, their resolutions, and clean rereview. | The governed workflow requires durable authority, review, correction, and closeout evidence. | Workflow contract and M4 | Review-artifact and metadata validation |

## Tests added or changed

The M1 ledger class proves closed rule owners, literal classifications, unique scenarios, prepared-manifest capability, and deterministic baseline identities. `ArchitectureReviewSkillSimplificationTests` contains nine focused tests that prove exact resource assemblies, missing-resource and claim stops, method ownership, shared-block identity, closed authority combinations, complete subject and basis identity, evidence-scoped target dispositions, prepared retry and concurrency, and real formal-profile reduction. Existing skill, build, adapter, boundary, metadata, and review validators remain the integration and package proof; no target-agent runtime or manual semantic-review gate was introduced.

The approved test specification maps R1-R58 to T1-T14. There are no manual-proof IDs because all selected acceptance behavior is deterministic contract, fixture, lifecycle, package, or parity behavior.

## Validation evidence available before final verify

- `ArchitectureReviewSkillSimplificationLedgerTests`, the nine focused simplification tests, and the four Markdown readability tests passed during implementation and holistic rereview.
- The full skill validator passed 371 tests with 16 documented skips during M3.
- Build tests, `build-skills.py --check`, skill validation, boundary validation, change metadata validation, and adapter distribution validation passed during milestone proof.
- Branch-wide `git diff --check` and closeout-mode review-artifact validation pass after final review correction.
- Final verify has not yet run the complete CMD1-CMD11 ledger, so branch or PR readiness is not claimed here.

## Review resolution summary

Nine material findings have accepted, closed dispositions: six proposal findings, one test-spec-review finding, and two final code-review findings. The proposal findings closed shared recording ownership, authority combinations, record-only settlement, exact subject and basis identity, evidence-scoped target mutation, and prepared retry. The test-spec finding added direct ADR intended-state proof. The final code-review findings normalized EOF formatting and durable review-record structure. The complete closeout is in [review-resolution.md](./review-resolution.md), and `code-review-final-r2` found no remaining material issue.

## Alternatives rejected

- Keeping the flat skill or applying only editorial compression would not create conditional loading or single ownership.
- Extracting only the architecture method would leave formal recording and settlement on every path.
- Splitting by every method and transaction topic would create excessive resource navigation and mixed-version risk.
- An executable review engine, transcript grader, prose classifier, tokenizer dependency, or target-agent acceptance journey would add architecture and nondeterminism unrelated to this content refactor.
- A new result asset was not added because the current compact inline result and finding shape did not justify another package resource.

## Scope control

The change does not redesign C4, arc42, ADR policy, review statuses, shared recording semantics, lifecycle ownership, workflow routing, adapter architecture, or target-agent behavior. It does not introduce partial semantic approval, new durable rationale artifacts, a new transaction schema, or automatic downstream continuation by `architecture-review`.

## Risks and follow-ups

The main residual risk is semantic drift between the universal file and conditional references; the rule ledger, exact shared-block test, closed resource map, focused scenarios, and package parity checks mitigate it. ARR1M shrinks only modestly by bytes, but it still decreases by 87 bytes and 196 words while retaining the complete method and recording procedure. No follow-up is required before final verify; any failure in CMD1-CMD11 must route back to its owning milestone or evidence surface before PR handoff.

## Readiness

The implementation milestones, material finding resolution, and final holistic code review are closed. The change is ready for `verify`, but verification and PR readiness remain unclaimed until the final report is durably recorded.
