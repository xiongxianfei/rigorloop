# Spec Review R2 - RigorLoop npm Publication

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Target: specs/rigorloop-npm-publication.md
Reviewed artifact: specs/rigorloop-npm-publication.md
Review date: 2026-05-16
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SR2-F1
- Recording status: recorded
- Recording blocker: none
- Reviewed artifact: specs/rigorloop-npm-publication.md
- Review log: ../review-log.md
- Review resolution: ../review-resolution.md
- Immediate next stage: spec

## Scope

This rerun reviewed the revised `specs/rigorloop-npm-publication.md` after the accepted SR1-F1 and SR1-F2 changes.

## Prior Finding Closeout

SR1-F1 is resolved. The spec now defines exactly one selected publication mode, separates `trusted-publishing` and `bootstrap`, records mode evidence, and forbids `.github/workflows/release.yml` from also publishing `@xiongxianfei/rigorloop@0.1.4` in bootstrap mode.

SR1-F2 is resolved. The spec now requires actual non-dry-run Codex adapter install proof from the packed or published package before FU-010 closes, including official archive reachability, checksum, size, safe extraction, installed tree hash, generated files, and ordering-gap evidence.

## Findings

### SR2-F1 - Acceptance criterion conflicts with bootstrap publication mode

Finding ID: SR2-F1
Severity: major
Location: `specs/rigorloop-npm-publication.md` acceptance criterion AC8, requirements R36d and R53-R61d.

Evidence: R36d says that if the selected publication mode is `bootstrap`, `.github/workflows/release.yml` "MUST NOT also publish `@xiongxianfei/rigorloop@0.1.4`." R53 through R61d define bootstrap mode as a manual publication of the exact recorded tarball. AC8 still says: "`.github/workflows/release.yml` owns npm publication and rejects unsupported tags." That acceptance criterion is unconditional.

Problem: A bootstrap publication can satisfy the revised requirements only if `release.yml` does not publish `0.1.4`, but AC8 would still require release workflow ownership. Test-spec and implementation would have to guess whether AC8 overrides bootstrap mode or should be read as trusted-publishing-only.

Required outcome: Make acceptance criteria mode-aware.

Safe resolution path: Replace AC8 with wording such as:

```md
AC8. Publication evidence proves exactly one publication mode. In trusted-publishing mode, `.github/workflows/release.yml` owns npm publication and rejects unsupported tags. In bootstrap mode, `.github/workflows/release.yml` does not also publish `@xiongxianfei/rigorloop@0.1.4`, and bootstrap tarball identity evidence is complete.
```

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Requirement clarity | concern | Main requirements are clear, but AC8 contradicts bootstrap mode. |
| Normative language | pass | Revised mode requirements use testable `MUST` language. |
| Completeness | pass | Bootstrap identity and real install proof are now covered. |
| Testability | concern | Tests can be written once AC8 is made mode-aware. |
| Examples | pass | Examples cover bootstrap tarball identity and real Codex install smoke. |
| Compatibility | pass | Version mapping and deferred follow-ups remain explicit. |
| Observability | pass | Publication evidence now captures mode, tarball identity, and real install smoke. |
| Security/privacy | pass | Bootstrap hash identity and package-content boundaries are explicit. |
| Non-goals | pass | Scope exclusions remain enforceable. |
| Acceptance criteria | block | AC8 conflicts with bootstrap publication mode. |

## Readiness

Immediate next repository stage: spec revision.

Eventual test-spec readiness: not-ready.

Stop condition: Revise AC8 to be mode-aware, then rerun spec-review. No automatic downstream handoff.
