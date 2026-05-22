# Code Review M4 R1 - Stage-Skill Bounded Read Guidance

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `8398efb`
Status: clean-with-notes

## Review inputs

- Review surface: commit `8398efb` (`M4: add bounded change record read guidance`).
- Reviewed milestone: M4. Stage-skill read guidance and generated adapter proof.
- Governing artifacts: `specs/change-record-catalog-registration-and-bounded-read-model.md`, `specs/change-record-catalog-registration-and-bounded-read-model.test.md`, `docs/adr/ADR-20260522-change-record-catalog-registration-and-bounded-read-model.md`, and `docs/plans/2026-05-22-change-record-catalog-registration-and-bounded-read-model.md`.
- Implementation files reviewed: `skills/proposal-review/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md`, `skills/pr/SKILL.md`, `skills/plan/SKILL.md`, and `scripts/test-skill-validator.py`.
- Lifecycle evidence reviewed: `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-log.md`, `docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/review-resolution.md`, and the M4 validation notes in the active plan.

## Diff summary

M4 adds bounded change-record read guidance to the affected stage skills after the M3 query-helper commands are stable. The skill text now points proposal review to the proposal, user intent, `review-log.md`, and `review-resolution.md`; points code review to the active plan, `artifacts`, `validation --stage <stage>`, and review-resolution slices; points verify and PR to `summary`, `artifacts`, and `validation --latest`; and keeps plan state owned by the active plan while allowing `artifacts` for canonical path discovery. Each changed skill names full `change.yaml` escalation conditions. The skill validator now asserts the bounded-read sections, referenced helper commands, and full-read escalation terms.

## Findings

No blocking or required-change findings.

## Checklist coverage

- Spec alignment: pass. CRM-R44 through CRM-R47 require affected Workstream B skills to name bounded slices or query-helper commands, retain full-read escalation, avoid broad-only `change.yaml` guidance, and wait for stable helper commands. The M4 diff does so after M3 closed.
- Test coverage: pass. `scripts/test-skill-validator.py` adds CRM-T021-style assertions that each affected skill contains bounded-read guidance, required query commands or authoritative slices, and full-read escalation terms.
- Edge cases: pass. The changed skills preserve full reads for forensic reconstruction, unsupported-shape diagnostics, disputed evidence, selector-routing debugging or behavior, migration compatibility where stage-relevant, and whole-record review.
- Error handling: pass. The guidance does not convert bounded query output into a substitute for required validation commands, final verification, PR readiness, or active plan live state.
- Architecture boundaries: pass. Querying remains owned by `scripts/query-change-record.py`; validation remains separate; stage skills reference the helper without adding new workflow or metadata semantics.
- Compatibility: pass. No lifecycle state values, review status meanings, validation selection semantics, branch readiness, final readiness, or PR readiness semantics changed.
- Security/privacy: pass. The diff adds repo-relative command and artifact references only and does not introduce credential, hostname, or local absolute-path handling.
- Derived artifact currency: pass with note. Canonical skill checks, skill build check, adapter distribution tests, selected adapter drift checks, and release-archive adapter generation/validation were recorded. The plan's baseline `python scripts/build-adapters.py --check` command still fails against retired tracked adapter-tree expectations, but current repository guidance for v0.1.3 and later treats public adapter skill bodies as release archives; M4 recorded the caveat and ran the supported archive validation path.
- Unrelated changes: pass. The diff is scoped to the affected skills, static skill proof, and lifecycle state/evidence updates for M4.
- Validation evidence: pass. Recorded validation includes the expected failing pre-edit skill test, passing `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/build-skills.py --check`, active query-helper summary smoke, adapter distribution tests, release-archive adapter validation, selected CI for the changed skills/test/helper paths, lifecycle validation, review-artifact closeout, and whitespace.

## No-finding rationale

The M4 implementation satisfies the stage-skill guidance contract without broadening workflow semantics. Each affected skill names the bounded read surface needed for its stage-owned questions and preserves full-read escalation for audit, unsupported, disputed, selector, migration, or whole-record cases. The static validator now guards those references and confirms the query helper exposes the referenced command names. The recorded adapter caveat is not a material finding for M4 because the supported v0.1.5 archive generation and validation path passed, and the selected explicit CI recorded adapter drift coverage for the changed skill surfaces.

## Residual risks

- The stale baseline `python scripts/build-adapters.py --check` command remains a documented validation caveat outside the M4 skill-text change. M4 did not change adapter packaging semantics and used the current archive-based adapter validation proof.

## Handoff

Reviewed milestone: M4. Stage-skill read guidance and generated adapter proof
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Next stage: implement M5
Remaining implementation milestones: M5
Verify readiness: not-claimed
