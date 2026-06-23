# Learn Session: M2 Resource-Lint Review Root Cause

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why M2 fixed the first code-review finding but received a new review finding, what the root cause was, and what best practices should guide the next fix.
- Trigger type: explicit maintainer request / repeated review findings within one milestone.
- Scope:
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r1.md`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r2.md`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
- Evidence in scope:
  - `SRI-M2-CR1`, which found broad project-local allowlist reuse suppressed ordinary load-condition wording such as `when relevant`;
  - the accepted SRI-M2-CR1 resolution, which replaced the broad allowlist with resource-lint-specific context rules and added direct single-reference regression tests;
  - `SRI-M2-CR2`, which found the replacement still applied explicit external ownership context at whole-line scope and could suppress unrelated unqualified resource references on the same line;
  - direct review reproduction using a mixed instruction containing a user-provided reference and an unqualified `templates/...` reference.
- Explicit exclusions:
  - this session does not fix `SRI-M2-CR2`;
  - this session does not close M2, claim M3 readiness, update validators, update specs, update skill behavior, or claim branch/PR readiness;
  - this session does not update curated topic files without separate contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
  - `docs/learn/sessions/2026-05-09-implement-review-fix-handoff-drift.md`
  - `docs/learn/README.md`
- Session record path: `docs/learn/sessions/2026-06-23-m2-resource-lint-review-root-cause.md`

## Observe

### O1 - The first review finding was resolved for the named case, not for the full classifier boundary

Evidence:

- `SRI-M2-CR1` required that ordinary conditional wording such as `when relevant`, `when available`, and `when needed` must not suppress resource lint.
- The SRI-M2-CR1 implementation added table-driven tests for single-reference lines such as `Use templates/architecture.md when relevant.`
- Those tests directly covered the reported false negative and the validator suite passed.

Observation:

The first fix was real. It removed the incorrect dependency on the broad project-local allowlist and proved the specific false-negative family named in `SRI-M2-CR1`.

The miss was that the fix did not fully restate the lint's unit of analysis. The desired classifier was not "does this line have external-context wording?" It was "does this resource reference have external ownership or illustrative context?"

### O2 - The new finding came from preserving a line-level classifier after changing the vocabulary

Evidence:

- `SRI-M2-CR2` records that `_iter_unmapped_skill_local_resource_references` checks external context on the whole line before iterating resource references.
- A direct fixture command using `Use the user-provided references/external.md and templates/architecture.md when relevant.` validated successfully.
- In that sentence, `user-provided` qualifies `references/external.md`, but not `templates/architecture.md`.

Observation:

The implementation changed the suppressor vocabulary but kept the old suppressor granularity. That made the solution pass the single-reference tests while still failing a mixed-reference edge case.

The underlying bug class is a classifier-boundary mismatch: line-level suppression is too coarse for a rule whose contract is per resource reference.

### O3 - The tests proved examples, not the decision model

Evidence:

- The SRI-M2-CR1 tests included must-fail single-reference cases for `assets/`, `references/`, `scripts/`, and `templates/`.
- The false-positive tests included single-reference external or illustrative cases.
- No test combined an explicitly external path and an unqualified skill-local resource path in the same loading instruction.

Observation:

The test set had good positive and negative examples, but no contrast case proving that the classifier can make two different decisions inside one instruction line.

When a validator decides over multiple matched entities, the test suite needs at least one mixed decision case.

### O4 - Review did its job; the second finding is not proof the first fix was worthless

Evidence:

- `code-review-m2-r2` acknowledges that SRI-M2-CR1's broad allowlist reuse was removed and that single-reference conditional load wording now fails correctly.
- The new finding is narrower: external context is now resource-specific in wording but still line-wide in application.

Observation:

This was a refinement failure, not a total failure. The first fix closed the broad allowlist problem. The second review found the remaining granularity problem.

That distinction matters because the correct next fix should be smaller: move external-context evaluation to per-reference context and add the missing mixed-reference regression.

## Root Cause

The root cause was solving the visible false negative without re-deriving the validator's decision unit.

`SRI-M2-CR1` exposed that the suppressor vocabulary was too broad. The fix correctly narrowed the vocabulary. But the implementation kept the suppressor decision at whole-line scope, so any qualifying external-context phrase suppressed every resource-looking path on that line.

For this lint, the correct decision unit is the individual resource reference, not the Markdown line.

## Best Practices

1. Restate the classifier's decision unit before editing.
   If the rule is "each resource reference must be classified," design the helper around each matched path, not around the line that contains it.

2. Convert the review finding into an invariant, not only examples.
   For SRI-M2-CR1, the invariant was: load-condition wording never changes ownership classification; explicit external ownership suppresses only the reference it qualifies.

3. Add mixed-decision tests whenever one input can contain multiple matches.
   Include a line where one resource should be suppressed and another resource on the same line should fail.

4. Keep suppressors local.
   External ownership words such as `user-provided`, `repository-root`, or `project-provided` should be evaluated in bounded context around the matched path, not as a blanket line skip.

5. Prove both sides after a review fix.
   A good review-resolution test set should include the original failing example, existing false-positive examples, and a near-miss that would fail if the fix is too broad.

6. Treat a second review finding as signal about the abstraction boundary.
   When a re-review finds a nearby edge case, ask what model the first fix preserved by accident.

7. Keep the next implementation narrow.
   For SRI-M2-CR2, do not redesign mapped-resource validation or architecture normalization. Change the unmapped legacy-resource lint to evaluate external context per reference and add the mixed-line regression.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Current SRI-M2-CR2 review-resolution context | Review records and accepted SRI-M2-CR1 resolution | Explains why the first fix was real but incomplete. |
| O2 | process-follow-up | pending confirmation | Possible future validator-design checklist or test guidance | Not yet confirmed | The pattern is reusable, but action-owning artifact changes need confirmation. |
| O3 | process-follow-up | pending confirmation | Possible test-spec or validator fixture guidance for mixed-decision cases | Not yet confirmed | The test gap is concrete, but routing changes belongs outside learn alone. |
| O4 | observation | observation | None | Code-review M2 R2 evidence | The second finding narrows the first fix rather than invalidating all M2 work. |

Contributor confirmation status: explicit maintainer request confirms recording this retrospective and best-practice answer. It does not by itself confirm updating topic files, validator guidance, specs, skills, or workflow policy.

## Route

No derivative routing performed.

Candidate follow-up, not routed here: if this pattern recurs, update the action-owning validator/test guidance to require mixed-decision cases for validators that classify multiple matched entities inside one source line or block.

## No Durable Route Rationale

This session captures a useful implementation lesson, but the authoritative next action already belongs to `SRI-M2-CR2` review-resolution. A broader rule about classifier decision units or mixed-decision tests would affect validator/test guidance and should be routed through an action-owning artifact only after contributor confirmation or recurrence.
