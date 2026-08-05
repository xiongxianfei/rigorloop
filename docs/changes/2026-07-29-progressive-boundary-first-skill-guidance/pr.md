# Pull Request Handoff

| Field | Value |
| --- | --- |
| PR URL | https://github.com/xiongxianfei/rigorloop/pull/129 |
| PR state | open |
| Base branch | main |
| Head branch | proposal/progressive-boundary-first-guidance |

## Title

feat: make boundary-first guidance automatic and progressive

## Summary

- Apply a concise boundary scan automatically in the skills that write, review,
  implement, or verify behavior, without requiring users to name the method.
- Keep one canonical boundary model while loading detailed authoring and proof
  guidance only at the stages that own it.
- Project resources deterministically through canonical skills and public
  adapter packages, with atomic activation and rollback proof.
- Stop skill-only changes from selecting the unrelated artifact-lifecycle
  checker while preserving lifecycle validation for governed artifacts.

## Why

The existing boundary-first method was useful but inconvenient: related skills
used it only when users explicitly requested it, while copying the full model
everywhere would make routine work noisy and complex. This change makes the
small, high-value boundary scan the default and progressively reveals deeper
guidance only when the work actually needs it.

## Spec / plan / architecture

- Proposal:
  `docs/proposals/2026-07-29-progressive-boundary-first-skill-guidance.md`
- Spec:
  `specs/progressive-boundary-first-skill-guidance.md`
- Test spec:
  `specs/progressive-boundary-first-skill-guidance.test.md`
- Architecture:
  `docs/architecture/system/architecture.md`
- ADR:
  `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`
- Plan:
  `docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md`

## What changed

- Added the compact four-question scan and stage-specific boundary resources to
  the ten governed skills, with shared canonical source and parity checks.
- Added a closed resource manifest, projection tooling, activation state, and
  clean-install proof across Codex, Claude, and opencode adapters.
- Updated feature authoring, proof mapping, implementation, review, and verify
  guidance so downstream stages consume approved boundary IDs instead of
  recreating the model.
- Corrected validation selection so published skill changes use skill-owned
  checks and only governed lifecycle paths select lifecycle validation.
- Aligned architecture/ADR lifecycle pointers and plan initialization with the
  existing stage-owned change-local state contract.

## Tests and verification

- [x] `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` — 18 selected checks passed.
- [x] `bash scripts/ci.sh --mode broad-smoke` — all 12 checks passed in 510 seconds.
- [x] Post-R5 focused CI — review, lifecycle, metadata regression, and metadata validation passed.
- [x] `git diff --check origin/main...HEAD` — passed.
- [x] Formal review closeout — 54 reviews, 71 resolved findings, zero open findings.
- [ ] Hosted CI — pending after PR creation.

## Requirement coverage

- PBS-R001–R004 → capability state, canonical references, and activation compatibility.
- PBS-R005–R024 → prompt-independent compact scan and stage-owned progressive guidance.
- PBS-R025–R031 → selector ownership and mixed-path lifecycle behavior.
- PBS-R032–R038 → projection parity, clean installation, atomic activation, and rollback.
- PRF-001–PRF-023 → approved test-spec proof map across milestones M1–M4.

## Review resolution summary

- Accepted: 70
- Rejected: 1
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0
- Open findings: 0
- Review resolution:
  `docs/changes/2026-07-29-progressive-boundary-first-skill-guidance/review-resolution.md`

## Risks and rollback

- Risk: automatic guidance could become verbose. The default is limited to the
  compact scan; detailed resources load only for the owning stage and observed
  risk.
- Risk: canonical and packaged resources could drift. Closed-manifest,
  projection, adapter, and clean-install checks fail on mismatches.
- Rollback: keep the capability state pending or atomically restore the prior
  activation state; generated package output remains derived and untracked.

## Reviewer notes

- Review the compact-versus-progressive split in the governed skill bodies.
- Review `specs/boundary-first-resources.yaml` and projection validation for
  closed-vocabulary and exact-parity behavior.
- Review selector regressions proving skill-only and mixed-path behavior.
- Review activation/rollback containment; this PR does not publish or activate
  the pending candidate.

## Follow-ups

Actual capability activation and publication remain separate explicit actions.
