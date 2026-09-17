# Model-owned test design and concise executable tests

## Challenge

Test intent is difficult to maintain when it lives mainly in temporary delivery plans or is reconstructed from a large suite. Repeated setup and overlapping cases obscure the behavior being protected. Release, Skill and Authoring need durable coverage designs that contributors can use to select meaningful tests and fixtures, and ordinary validation must understand those designs.

## Goals

Keep shared testing rules under System and durable coverage with each owning model. Make Release, Skill and Authoring scenarios concrete enough to review and implement. Simplify their executable support by removing demonstrated redundancy, sharing small fixture builders and preserving meaningful failure observations. Admit the selected test-design documents through normal repository validation.

## Scope and non-goals

| User intent | Treatment | Destination |
| --- | --- | --- |
| Shared test organization, authoring and maintenance rules | core to this proposal | System policy and its published skill consumers. |
| Durable model test designs | first-slice candidate | Release, Skill parent and Authoring parent; other models retain their existing coverage until separately refined. |
| Concise executable tests and fixtures | core to this proposal | Existing Release and Skill suites, including Authoring structural support. |
| Document selection and validation | same-slice dependency | Exact shared guidance and three declared model packages through existing entrypoints. |
| Broader compatibility retirement | separate proposal | Preserved on branch `codex/retire-obsolete-compatibility`, proposal `docs/proposals/2026-09-16-retire-obsolete-compatibility.md`; no retirement approval is claimed here. |
| JSON-driven execution or a case-management CLI | out of scope | Catalogs describe intent and realization; native discovery and execution remain authoritative. |

This scope follows the user's explicit choice of a focused testing PR. Retained feature/proof authoring, validation, location defaults and historical path handling remain supported as at the base revision. Moving Release's living document into its model directory is included with live-link and selector reconciliation. Proposed catalog scenarios remain visible gaps; this change does not promise to implement every proposed procedure or to redesign every model's tests.

## Governing principle

Keep a test when it protects a supported outcome or material failure, and make that protection easy to understand and maintain.

## Proposed direction

Give common rules one System owner, with model-owned coverage packages for the three selected responsibilities. Keep logical scenarios distinct from executable methods, group equivalent variations and describe fixtures and independent observations. Teach Design authorship and its consumers to maintain those relationships. Refine the existing suites against that intent, retaining distinct authority, persistence and recovery protection. Integrate the declared documents into existing validation rather than creating a second test runner.

## Feasibility

Assessment: feasible within the selected scope. The original branch already contains the three catalogs, bounded test refinements and a working admission implementation; its stable local CI passed. That evidence establishes a credible extraction basis, not approval of this new subject. The focused package must remove contradictory retirement clauses, receive independent Design and Delivery assessment, and pass fresh review and validation after extraction. No new runtime dependency, record format or external service is required. Semantic review procedures cannot be certified by structural validation and remain explicitly proposed unless separately performed.

## Impact and major trade-offs

Durable catalogs add maintenance, so keep them proportional and avoid copying each implementation method into a separate design case. Shared policy changes require reconciliation of published skill guidance. Test deletion requires a reviewed protection mapping, not a numerical reduction target. Isolating this scope lets useful testing improvements land while preserving the broader retirement decision and its unresolved work separately.

## Decision requested

Approve the focused testing direction selected by the user: shared rules, the three model coverage packages, their bounded executable refinements and necessary document admission. Require fresh exact-package reviews and successful verification before PR submission. Defer compatibility retirement without declaring it complete.
