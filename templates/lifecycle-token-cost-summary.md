# Lifecycle Token-Cost Summary Template

Use this template only when a lifecycle token-cost summary trigger applies. The report path is `docs/reports/token-cost/lifecycle/<change-id>.md`.

Lifecycle token-cost summaries are warning-only diagnostic evidence. They are not a hard token gate, hard release gate, or CI blocker based on token totals. Use bounded evidence and summarize large output instead of copying raw logs.

## Identity

- Change ID:
- Title:
- Report date:
- Source artifacts:
  - Proposal:
  - Spec:
  - Plan:
  - Test spec:
  - Change metadata:
  - Review records:
  - Release or benchmark report, if any:

## Trigger

- Trigger reason: large workflow-governance change / release change / dynamic benchmark warning / broad-search incident / explicit maintainer request
- Requested by or owning artifact:
- Date identified:
- Trigger rationale:

## Scope

- Stages covered:
- Stages excluded:
- Summary basis:
- Advisory numeric data: not measured / not applicable / linked evidence with rationale

## Source Artifacts

List durable repo-relative evidence used by the summary. Link release Token-Friendliness reports instead of duplicating them.

- 

## Observed Cost Drivers

Record each item as `observed`, `not observed`, `not measured`, or `not applicable`, with rationale.

| Driver | Status | Evidence or rationale |
|---|---|---|
| Broad searches |  |  |
| Large command outputs |  |  |
| Full-skill reads |  |  |
| Repeated file reads |  |  |
| Generated-output reads |  |  |
| Review rounds |  |  |
| Validation runs |  |  |

## Largest Observed Event

- Type:
- Source:
- Estimated tokens or lines:
- Evidence:
- Bounded-evidence rationale:

## Result / Rationale

- Status: informational
- Largest driver:
- Recommended follow-up:
- No-follow-up rationale:
- Follow-up routing:

## Boundary Checks

- Hard token gate introduced: no
- Hard release gate introduced: no
- CI blocker based on lifecycle token totals introduced: no
- Before/after dynamic benchmark comparison required: no, unless a benchmark actually ran or a later accepted artifact requires it
- Release Token-Friendliness report replaced: no
- Generated adapter skill bodies treated as authored skill truth: no
