# Code Review M5 R2 - CRM-M5-CR1 Re-review

Review ID: code-review-m5-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `977b309`
Status: clean-with-notes

## Review inputs

- Review surface: commit `977b309` (`Resolve M5 selected CI command drift`).
- Reviewed milestone: M5. Lifecycle evidence and final closeout.
- Prior finding under re-review: `CRM-M5-CR1`.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plan.md`.
- Lifecycle evidence reviewed: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md`, and `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`.
- Validation evidence reviewed: M5 and `CRM-M5-CR1` validation notes in the active plan and change metadata.

## Diff summary

The re-review commit resolves the governing-artifact command drift identified by `CRM-M5-CR1`. The matching test spec now lists `bash scripts/ci.sh --mode local` as the final branch-local changed-path selected-CI proof for `CRM-T023` and explicitly states that `bash scripts/ci.sh --mode selected` is unsupported and must not be used as final verification proof. The active plan's M5 commands, validation plan, progress, readiness state, and plan index now use the supported `--mode local` command. Review log, review resolution, and change metadata record the accepted finding resolution and validation evidence.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. The `CRM-T023` automation location and final proof wording now use `bash scripts/ci.sh --mode local`, preserving workflow and selected-CI compatibility semantics without listing the unsupported wrapper mode as required proof.
- Test coverage: pass. This is a governing-artifact command correction, not a runtime behavior change; direct proof is the recorded successful `bash scripts/ci.sh --mode local` validation and updated `CRM-T023` command reference.
- Edge cases: pass. The known unsupported `--mode selected` case remains recorded only as historical diagnostic evidence, so downstream verify is not pointed at a known-invalid command.
- Error handling: pass. The plan and test spec now distinguish supported proof from unsupported historical diagnostic output instead of treating a failing command as a required validation path.
- Architecture boundaries: pass. No selector, query-helper, validation-selection, lifecycle-schema, skill, or adapter behavior changed.
- Compatibility: pass. The resolution preserves existing stage order, review status meanings, readiness semantics, selected-check behavior, and valid change-record compatibility.
- Security/privacy: pass. The diff adds only repository-relative artifact references and local repository commands; no host-specific paths, credentials, or secret-like values are introduced.
- Derived artifact currency: pass. No generated skill or adapter output is in scope for this command-reference fix.
- Unrelated changes: pass. The diff is scoped to the test spec, active plan/index, review artifacts, and change metadata needed to resolve and record `CRM-M5-CR1`.
- Validation evidence: pass. Recorded validation includes `bash scripts/ci.sh --mode local`, change metadata validation, artifact lifecycle validation over the touched governing and review artifacts, review artifact closeout validation, and whitespace validation.

## No-finding rationale

`CRM-M5-CR1` required the governing final selected-CI proof to use the repository-supported local wrapper mode and to keep the unsupported `--mode selected` command out of required proof paths. The re-review diff does exactly that in `CRM-T023`, the active M5 command list, and the validation plan. The historical `--mode selected` reference remains only as an explanatory caveat, which is consistent with the finding's required outcome. The recorded `bash scripts/ci.sh --mode local` validation proves the replacement command is executable on the current branch-local changed-path surface.

## Residual risks

None identified for this re-review surface. Final lifecycle closeout still needs its own downstream proof and must not be inferred from this code-review result.

## Handoff

Reviewed milestone: M5. Lifecycle evidence and final closeout
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: final closeout
Remaining implementation milestones: none
Verify readiness: not-claimed
