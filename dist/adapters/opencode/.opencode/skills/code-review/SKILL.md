---
name: code-review
description: >
  Perform an independent implementation review against the spec, architecture, plan, test spec, actual diff, and validation evidence. Use after implementation or before PR readiness decisions.
---

# Independent implementation review

You are reviewing in independent-review mode with fresh eyes.

Your job is to determine whether the implementation satisfies the approved contract safely, not whether it merely looks plausible.

## Inputs to read

Read:

- actual diff or changed files;
- feature spec;
- test spec;
- concrete plan;
- architecture doc and ADRs when relevant;
- plan validation notes;
- test and CI results;
- invocation context for `workflow-managed`, isolated, or review-only behavior;
- explicit user instructions to stop after review;
- `AGENTS.md` and `CONSTITUTION.md`;
- related code paths and tests when needed.

Prefer a fresh session, separate reviewer, or separate agent when available. If not, intentionally reset assumptions before reading the diff.

## Independent-review mode

- Ground the review in the actual diff or changed files, approved upstream artifacts, checklist coverage, and available validation evidence.
- Do not treat remembered implementation intent, chat memory, or passing tests alone as sufficient review grounding.
- If you cannot inspect the actual diff, relevant tests, or authoritative upstream artifacts, do not return `clean-with-notes`. Use `changes-requested` or `blocked` when the review surface independently supports a finding; otherwise use `inconclusive`.

## Review surface and tracked governing branch state

- The review surface may be changed files, a staged diff, an unstaged diff, a PR diff, a commit range, an explicit patch, or another local review target.
- Tracked governing branch state is the tracked Git state that can support branch-scoped conclusions about cleanliness, authority, or readiness.
- This review does not require every reviewed implementation change to already be committed.
- If you cite a proposal, spec, test spec, plan, architecture document, or ADR as authoritative support for a clean branch-scoped conclusion, confirm that artifact is present in tracked governing branch state.
- Local-only governing artifacts may inform reviewer background understanding, but they must not support a clean branch-scoped conclusion.

## Mixed-evidence handling

- Missing tracked governing authority blocks `clean-with-notes`.
- Missing tracked governing authority does not suppress independently supported `changes-requested` or `blocked` findings.
- Use `inconclusive` only when missing evidence prevents both a supported finding and a clean conclusion.

## Direct proof for named edge cases

- Clean review conclusions for named edge cases must cite direct proof from a targeted test, targeted validation output, or an explicit manual verification note when manual verification is allowed.
- Code-shape inference alone is insufficient direct proof for a named edge case.
- When a named edge-case proof gap is actionable within approved scope, report it as a finding instead of a clean result.
- When the reviewer cannot inspect enough evidence to assess a named edge case credibly, use `inconclusive` rather than a clean result.

## First-pass checklist coverage

Evaluate each check with `pass`, `concern`, or `block`, and cite concrete evidence from the diff, tests, or governing artifacts:

1. **Spec alignment**: the changed behavior matches the approved spec and non-goals.
2. **Test coverage**: tests prove the changed behavior and regressions at the right level.
3. **Edge cases**: named edge cases and failure paths are handled as specified.
4. **Error handling**: invalid states, partial failures, permissions, and fallbacks are handled safely.
5. **Architecture boundaries**: the diff respects approved design boundaries and ADR decisions.
6. **Compatibility**: existing workflow expectations, contributor contracts, and migrations remain valid.
7. **Security/privacy**: no secret leakage, unsafe logging, auth bypass, or policy regression.
8. **Generated output drift**: canonical/generated outputs remain synchronized when generation is involved.
9. **Unrelated changes**: the reviewed diff does not quietly include unrelated edits.
10. **Validation evidence**: named commands and results are present, relevant, and credible.

For sensitive change classes, explicitly cite the relevant governing requirements, risks, or checklist items instead of relying on a generic clean summary.

## First-pass statuses

Use exactly one first-pass review status:

- `clean-with-notes`: the review passes and no unresolved accepted fix is required before `verify`.
- `changes-requested`: one or more fixable findings exist within current approved scope and with sufficient evidence to act.
- `blocked`: the review cannot safely auto-enter `review-resolution` under current approved scope without a new decision.
- `inconclusive`: the reviewer cannot inspect enough evidence to produce a credible clean or actionable result.

Issues that are clearly fixable within current approved scope and with sufficient evidence to act use `changes-requested`, not `blocked`.

## Severity

Use:

- `blocker`: unsafe to merge or violates a `MUST`.
- `major`: should be fixed before PR approval.
- `minor`: improvement that does not block.
- `nit`: optional style/readability suggestion.
- `positive`: good pattern worth keeping.

## Material findings

For every material finding, include evidence, the required outcome, and a safe resolution path.

If a safe resolution cannot be chosen without an owner decision, use a `needs-decision` rationale that names the decision needed and owning stage. A material finding lacking evidence, required outcome, or safe resolution or `needs-decision` rationale is incomplete.

When workflow-managed review findings are recorded under `docs/changes/<change-id>/reviews/`, preserve the first-pass review record before fixes and record dispositions in `review-resolution.md`.

## Rules

- Produce a first-pass review record before any review-driven fix is applied or any `review-resolution` work begins.
- The first-pass review record must include: review status, review inputs, diff summary, findings, checklist coverage, no-finding rationale when no findings exist, and recommended next stage.
- Surfacing findings first means the findings are visible before fixes begin. It does not create a new user decision gate unless a stop condition applies.
- This feature does not create a new standalone `review-resolution.md` requirement by itself.
- Do not confuse passing tests with compliance.
- Do not review from memory; use the actual diff.
- Do not request broad rewrites when a targeted fix is enough.
- Do not claim a credible clean result when required evidence or tracked governing authority is missing; use `inconclusive` instead unless the review surface independently supports a finding.
- Do not require positive notes in a clean review. Include them only when they provide specific, evidence-backed information useful to future maintainers.
- Do not emit generic praise such as `looks good` without checklist coverage and no-finding rationale. That is an invalid clean review.
- Do not expose secrets, credentials, or sensitive runtime values from the diff or validation outputs.

## Workflow handoff behavior

- In a workflow-managed full-feature flow, emit the first-pass review record before any review-driven fix begins.
- In a workflow-managed full-feature flow, `clean-with-notes` hands off to `verify` when no stop condition applies.
- In a workflow-managed full-feature flow, `changes-requested` enters the `review-resolution` loop, addresses the findings, and reruns `code-review` when no stop condition applies.
- In a workflow-managed full-feature flow, `blocked` stops and reports the blocker.
- In a workflow-managed full-feature flow, `inconclusive` stops and reports the missing evidence. It does not enter `review-resolution`.
- Stop instead of auto-entering `review-resolution` when the request is review-only, the request is isolated `code-review`, a finding requires a product/spec/architecture/ADR/scope decision, a higher-priority repository policy requires human review, the actual diff/tests/upstream artifacts are unavailable, or the user explicitly asked to stop after review.
- Direct `code-review` requests remain isolated by default unless the user explicitly asks to continue beyond the review result.

## Recommended clean review template

```md
Code Review

## Review status

clean-with-notes

## Review inputs

- Diff range:
- Review surface:
- Tracked governing branch state:
- Spec:
- Test spec:
- Plan milestone:
- Architecture / ADR:
- Validation evidence:

## Diff summary

<What changed, based on the actual diff.>

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Notes |
|---|---|---|
| Spec alignment | pass | <evidence> |
| Test coverage | pass | <evidence> |
| Edge cases | pass | <evidence> |
| Error handling | pass | <evidence> |
| Architecture boundaries | pass | <evidence> |
| Compatibility | pass | <evidence> |
| Security/privacy | pass | <evidence> |
| Generated output drift | pass | <evidence> |
| Unrelated changes | pass | <evidence> |

## No-finding rationale

No blocking findings were found because:

- the diff matches the approved spec and plan scope
- tests cover the changed behavior
- no unrelated files are present in the reviewed diff
- validation evidence supports the implemented behavior

## Residual risks

- None identified.
```

## Expected output

- first-pass review record with:
  - review status using `clean-with-notes`, `changes-requested`, `blocked`, or `inconclusive`;
  - review inputs;
  - diff summary;
- findings with exact file/path references;
- checklist coverage;
- no-finding rationale when applicable;
- any missing tracked governing artifacts or direct-proof gaps that affected the result;
- optional positive notes only when they add specific evidence-backed value; and
- recommended next stage or stop reason.
