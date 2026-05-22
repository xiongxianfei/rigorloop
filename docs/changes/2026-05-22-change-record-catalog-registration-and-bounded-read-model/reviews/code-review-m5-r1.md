# Code Review M5 R1 - Lifecycle Evidence

Review ID: code-review-m5-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `9ab7bd7`
Status: changes-requested

## Review inputs

- Review surface: commit `9ab7bd7` (`M5: close change record catalog lifecycle`).
- Reviewed milestone: M5. Lifecycle evidence and final closeout.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Implementation files reviewed: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/explain-change.md`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`, `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plan.md`.
- Validation evidence reviewed: M5 validation entries in `change.yaml`, the M5 validation notes in the active plan, and direct rerun of `bash scripts/ci.sh --mode selected`.

## Diff summary

M5 adds the durable change rationale at `explain-change.md`, wires it into `change.yaml`, records M5 validation evidence, and moves the active plan and plan index to M5 code-review handoff. The rationale summarizes the Workstream A and Workstream B implementation slices, resolved review findings, validation evidence, compatibility boundaries, and follow-up work while avoiding final verification or PR-readiness claims.

## Findings

### CRM-M5-CR1: Final selected-CI command remains stale in governing artifacts

Finding ID: CRM-M5-CR1
Severity: major
Location: `specs/change-record-catalog-registration-and-bounded-read-model.test.md:21`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md:355`, `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md:345`, `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md:373`

Evidence: M5 correctly records that `bash scripts/ci.sh --mode selected` is unsupported and that `bash scripts/ci.sh --mode local` is the working changed-path selected-CI equivalent. Direct execution of the recorded final selected-CI command exits with:

```text
Unsupported ci.sh mode: selected
```

However, the approved test spec still says end-to-end proof includes final `bash scripts/ci.sh --mode selected`, and CRM-T023 still lists `bash scripts/ci.sh --mode selected` as the automation location. The active plan also still lists `bash scripts/ci.sh --mode selected` in M5 validation commands and the validation plan. Leaving those governing artifacts stale means downstream verify would follow a known failing command even though M5 already identified the correct current wrapper mode.

Required outcome: The M5 lifecycle artifacts must not leave unsupported final selected-CI commands as the governing verification path. The active plan and matching test spec must name the repository-supported selected changed-path proof command, or explicitly document the replacement command and reason in a way final verify can follow without rerunning a known-invalid command as required proof.

Safe resolution path: Update `specs/change-record-catalog-registration-and-bounded-read-model.test.md` CRM-T023 and the active plan M5/validation-plan command references to use `bash scripts/ci.sh --mode local` as the branch-local changed-path selected-CI proof. Preserve the recorded caveat that `--mode selected` is unsupported only as historical validation evidence, not as the command final verify should execute. Rerun `python scripts/validate-change-metadata.py`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths` over the touched spec/plan/change artifacts, `bash scripts/ci.sh --mode local`, and `git diff --check --`.

## Checklist coverage

- Spec alignment: concern. The M5 rationale preserves CRM-R49 through CRM-R52, but the unchanged test-spec command conflicts with the repository's current CI wrapper interface and the recorded M5 proof path.
- Test coverage: concern. Selector, query, metadata, skill, lifecycle, and local selected-CI proof are recorded, but the test spec still points final selected-CI proof at an unsupported mode.
- Edge cases: concern. CRM-T023's final selected-CI edge case is operationally covered by `--mode local`, but the governing artifact still names the failing command.
- Error handling: pass for the M5 implementation. M5 records the unsupported-mode failure instead of hiding it.
- Architecture boundaries: pass. M5 adds lifecycle rationale and metadata only; it does not change selector, query, validation, or adapter architecture.
- Compatibility: concern. Leaving a known-invalid final validation command in active governing artifacts creates downstream workflow incompatibility even though the implemented behavior remains compatible.
- Security/privacy: pass. The M5 rationale and metadata use repository-relative paths and do not introduce secrets or machine-local paths.
- Derived artifact currency: pass with note. M5 records the same adapter caveat as M4 and uses the current v0.1.5 archive-generation validation path; it does not change generated adapter semantics.
- Unrelated changes: pass. The diff is scoped to lifecycle evidence and plan/metadata handoff state.
- Validation evidence: concern. The recorded validation is credible for the actual command set, but the command set in the governing test spec and active plan needs correction before clean handoff.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M5. Lifecycle evidence and final closeout
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution / implement M5 fix
Remaining implementation milestones: M5 resolution
Verify readiness: not-claimed
