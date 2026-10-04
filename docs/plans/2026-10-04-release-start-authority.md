# Release workflow-start authority

## Purpose / big picture

Implement the reviewed release policy: an authorized main-push workflow start permits publication of its subsequently qualified retained packages without another human approval. Preserve exact source/configuration binding, source protection, authentication, evidence persistence, public observation and bounded recovery.

## Current Handoff Summary

Owning Change: `2026-10-04-release-start-authority`; resume with `rigorloop change context --root . --change 2026-10-04-release-start-authority`. Mutable progress and assessments belong there.

## Source artifacts

- Requirement basis: IR-010; SR-069/070/073; SCN-065/066 and FEAT-020 in `design/requirements/` and `design/system/`.
- Logical behavior: FUNC-069/070/073.
- Architecture: [Release](../../design/architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md), IF-009/010, MOD-015; REL-DEC-06/08.
- Proof allocation: [Release test design](../../design/architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/test-design/test-design.md), especially REL-AR-001/028/034/036.
- Prior contract: historical approvals retain their meaning; no approval-era active candidate is silently adopted by the new path.

## Context and orientation

`.github/workflows/release.yml` composes `release_coordination.py`, candidate construction and `release_execution.py`; `release_provider.py` owns GitHub/npm reads and writes. Existing tests exercise controlled services with real candidate/artifact/evidence files. The separate Git evidence ref remains. No hosted publication is needed for qualification.

## Non-goals

No evidence-store replacement, version bump, dependency change, manual dispatch trigger, new approval mode, remote configuration change, merge or public release. PR preparation does not authorize merging. Existing local design work is part of this delivered scope and must be preserved.

## Requirements covered

SR-069 retains qualification and exact bytes. SR-070 binds initiation and execution authority. SR-073 supplies automatic continuation. SR-071/072 retain truthful public results and recovery. Shared IF-009/010 keep authority distinct from evidence.

## Milestones

### M1 — Replace approval admission with workflow authority

Refactor provider/coordinator/executor inputs and candidate/state consumers to initiating event/run authority. Inspect repository, protected main branch, exact event/source/workflow, environment configuration and artifact provenance; reject required-reviewer configuration and unsupported triggers. Bind the originating run and configuration into the sealed candidate. Recheck current run authority before every write. Preserve the existing evidence compare-and-swap and active-attempt rules. Rename obsolete internal approval helpers and consumers without aliases or dual writes.

Completion: focused tests prove valid no-reviewer admission; PR/local/unsupported triggers, changed source/run/config, wrong artifacts, failed checks and cancellation prevent affected writes. Old active approval-only candidates/records stop for explicit disposition; historical original bytes are not rewritten.

### M2 — Integrate workflow, recovery and documentation

Keep main-push, read-only preparation, retained artifact expiry, serialized execution and write/OIDC boundary. Retain `release` only as a branch/credential scope with no reviewers; remove approval-only deployment-read permission/API use. Reconcile fixture builders, catalog cases, summaries, source-owned views and adoption instructions. No executable test reduction without preserving its surviving obligation.

Completion: actual coordinator composition proves successful preparation through publication without a reviewer API, a failed check prevents publication, retries reuse original bytes and do not repeat matching writes, cancellation stops later boundaries, and reporting failure retains recovery support.

## Final review checkpoint

One independent whole-change Code Review after M1/M2 and required checks, then distinct final Verify. Corrections are reassessed within that same gate; milestones do not require separate approvals.

## Change-level verification

TG-FINAL-1 covers exact event/source/configuration → retained candidate → public writes → durable outcomes across SR-069/070/073 and retained recovery. Use the actual coordinator/build/executor with controlled external providers; do not stub authority or candidate validators into passing. Assert write histories and retained bytes, not only returned status. Real publication and remote configuration are separately observed prerequisites and are not claimed by fixtures.

## Validation plan

- `python tests/engineering/release/test-release-transaction.py ReleaseAuthorityTests ReleaseCoordinationTests ReleaseExecutorTests` runs focused authority/coordinator/executor proof after the class rename. Then `python tests/engineering/release/test-release-transaction.py` runs the complete owning Release suite, including real candidate/coordinator integration.
- `bash scripts/ci.sh --mode local` runs the repository-selected final checks, with actual durations/results retained privately. Use the qualified Node/D2/browser environment already established for this checkout.
- Regenerate architecture browser with `python scripts/render-rem-architecture-browser.py`, then `--check`; run affected model/browser checks through the existing selector.
- Inspect the complete workflow against approved events, permissions, dependency and no-reviewer behavior; validate actual parsed YAML via existing coordinator tests.

## Risks and recovery

Initiation does not identify packages before they exist: seal the initiating run/source/configuration reference with the later candidate, then compare provider artifact producer/digest and exact packages at execution. A passing local check is never that grant.

An existing approval-era candidate, waiting run or old execution state must not acquire new authority through an upgrade. Stop with an explicit new-run/recovery disposition and preserve records; after any possible public write inspect state before replacing work. Do not auto-convert old approvals or overwrite matching published assets.

Remote reviewer configuration may still block the new run. Validate and report that setup mismatch before preparation; document the required maintainer setup without modifying it in this task. Reverting implementation does not undo a publication or justify rewriting evidence.

## Dependencies

Independent Requirement and integrated Design Reviews are recorded on the owning Change. Delivery Review precedes implementation. Runtime adoption evidence may justify changing diagram qualification from proposed to observed only after checks and independent assessment.

## Material rationale

Remove the redundant human gate, not exact-artifact checks or recovery. Reuse existing workflow, artifact and evidence facilities so this change can ship independently of evidence-store simplification.

## Readiness

See the owning CLI handoff for current status.
