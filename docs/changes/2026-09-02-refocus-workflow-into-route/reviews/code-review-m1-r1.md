# Code Review M1 R1: Read-only Workflow Context

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: commit 47a87bb8
Reviewed artifact: M1 commit 47a87bb8
Reviewed milestone: M1
Review date: 2026-09-02
Status: changes-requested
Review status: changes-requested
Material findings: RFR-M1-CR1, RFR-M1-CR2, RFR-M1-CR3
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m1-r1.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Open blockers: RFR-M1-CR1, RFR-M1-CR2, RFR-M1-CR3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RFR-M1-CR1, RFR-M1-CR2, RFR-M1-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: RFR-M1-CR1, RFR-M1-CR2, RFR-M1-CR3
- Verify readiness: not-claimed

## Review inputs

- Actual diff: commit `47a87bb8` against its first parent, with implementation files isolated from the accompanying tracked Design and Delivery authority.
- Approved Design package: `design-review-r1`, exact architecture, specification, and ADR members current with granted authority.
- Approved Delivery package: `delivery-review-r1`, exact plan member at sha256 `825e74a85b56a43db8f8a47191882794d95dd27cf65ffe0e968358b7203b162d`, current with granted authority.
- Current milestone: M1 in `review-requested`; M2 and M3 remain planned.
- Implementation evidence: `docs/changes/2026-09-02-refocus-workflow-into-route/evidence/m1-workflow-context.md`.
- Validation evidence: focused 41-test final run, plan-selected 162-test run, package 347-pass/2-skip run, 107 change-metadata tests, schema parse, direct CLI invocation, and whitespace check.
- Additional evidence loaded: the complete M1 architecture/configuration sections were needed because the implementation's generic review-location ownership could not be judged safely from the requirement table alone.

## Actual-diff summary

M1 adds a top-level `workflow-context` command, a new context/configuration module, a governed-change discovery export, observability classification, a closed JSON schema, public CLI documentation, and 14 focused tests. The implementation is additive and does not yet rename the workflow skill or remove its guide. The normalized result composes current lifecycle interpretation and exposes project or exact-change facts.

## Findings

### Finding RFR-M1-CR1

Finding ID: RFR-M1-CR1
Severity: major
Location: `packages/rigorloop/dist/lib/workflow-context.js:27`; `schemas/rigorloop-workflow-v1.schema.json:15`
Evidence: The bundled model defines one `review-records` location owned by `code-review`, although current formal records in that directory are separately owned by proposal-review, design-review, delivery-review, and code-review. It returns only the shared directory, not deterministic stage-specific review output locations. This collapses distinct review authorities and cannot satisfy RT-R4, RT-R8, BND-AUTH-001, or the architecture rule that a resolved location never transfers artifact authority.
Required outcome: Represent formal-review locations without assigning proposal, Design, or Delivery review outputs to code-review, and expose deterministic stage-owned review locations while preserving every current review authority.
Safe resolution path: Replace the generic owner-bearing entry with closed stage-specific review kinds or an explicitly non-authorizing shared-root surface plus separately resolved stage outputs; align the schema/parser and add positive and wrong-owner regressions for every formal review stage.
needs-decision rationale: none; the approved Design already preserves existing stage ownership.

### Finding RFR-M1-CR2

Finding ID: RFR-M1-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/workflow-context.js:161`; `packages/rigorloop/dist/lib/workflow-context.js:186`; `packages/rigorloop/dist/lib/workflow-context.js:282`; `packages/rigorloop/dist/lib/workflow-context.js:310`
Evidence: Candidate, milestone, budget, receipt, and package projections have no count or encoded-size bound. A direct review fixture with 131 active changes returned all 131 candidates in a 23,296-byte result. Several exact-change identifiers are passed through without the allowlist used for automation: setting `current_stage` to `/private/host/path` produced exit 0 and echoed that absolute value in JSON. Therefore the implementation does not yet meet RT-R7, RT-R8, RT-R35, RT-R36, or the bounded-output/privacy side of BND-ENV-001.
Required outcome: Every projected collection and identifier must have an explicit deterministic bound, invalid lifecycle identifiers must fail closed or be safely redacted, and neither human nor JSON output may echo machine-local absolute or unbounded caller-controlled values.
Safe resolution path: Centralize bounded identifier/list/map projection, validate current stage and related closed values before output, return count/truncation or explicit blocker facts without semantic selection, and add large-candidate, large-automation, malformed-stage, private-sentinel, and exact encoded-bound tests.
needs-decision rationale: none; bounded structural output and privacy are already approved requirements.

### Finding RFR-M1-CR3

Finding ID: RFR-M1-CR3
Severity: major
Location: `packages/rigorloop/dist/lib/workflow-context.js:53`; `packages/rigorloop/dist/lib/workflow-context.js:71`; `packages/rigorloop/dist/lib/workflow-context.js:99`; `packages/rigorloop/dist/lib/workflow-context.js:249`; `packages/rigorloop/dist/lib/lifecycle-read.js:101`; `packages/rigorloop/test/workflow-context.test.js:21`
Evidence: Filesystem discovery and path checks use `existsSync` followed by unguarded `lstatSync`/`readdirSync` paths, while `executeWorkflowContext` has no complete failure boundary; a race, permission failure, or injected read fault escapes to the CLI's generic `Unexpected internal error` path instead of a normalized workflow-context result. The lifecycle-reader refactor also makes exact `selectGovernedChange` parse every unrelated change, expanding the prior exact-read failure and cost surface. Focused tests snapshot only one `change.yaml` and contain no direct identical-result retry, post-mutation stale-revision, filesystem/interruption, unrelated-malformed-change exact-selection, or complete governed/config tree identity proof required by TG-05 and the M1 completion criteria.
Required outcome: Filesystem and dependency failures must return bounded normalized context diagnostics without mutation; exact change reads must remain isolated from unrelated candidates; and TG-05 must have direct proof for success, failure, ambiguity, identical retry, interruption, and stale-after-mutation behavior over the complete governed/config surface.
Safe resolution path: Restore exact selection to read only the requested change while retaining a separate project discovery API, add a narrow injectable/read error boundary that normalizes expected filesystem failures, snapshot all governed/config bytes and entries, and add retry/freshness/fault tests before rerunning every M1 command.
needs-decision rationale: none; the approved plan already allocates these outcomes to M1.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | RFR-M1-CR1 and RFR-M1-CR2 violate RT-R4, RT-R7, RT-R8, RT-R35, and RT-R36. |
| Test coverage | block | RFR-M1-CR3 identifies missing direct TG-05 proof; RFR-M1-CR1 and RFR-M1-CR2 lack ownership and output-bound regressions. |
| Edge cases | block | Large candidate/automation sets, malformed structural identifiers, read faults, and post-mutation freshness are not safely closed. |
| Error handling | block | Expected filesystem failures can escape the normalized result boundary. |
| Architecture boundaries | block | The generic review location assigns a multi-owner surface to code-review. |
| Compatibility | concern | Exact change lookup now reads every unrelated change instead of only the requested record. |
| Security/privacy | block | An invalid absolute current-stage value is emitted with a successful result. |
| Derived artifact currency | pass | M1 has no generated adapter obligation; schema and package documentation are present, while adapter parity remains M3. |
| Unrelated changes | concern | The lifecycle-reader exact-selection expansion is unnecessary for the project-discovery API. |
| Validation evidence | concern | Named commands pass, but they do not directly prove several mandatory M1 outcomes. |

## No automatic downstream handoff

This explicit Code Review stops after recording. Review Resolution must accept and scope RFR-M1-CR1, RFR-M1-CR2, and RFR-M1-CR3 before implementation changes begin. No owner decision is needed; all three corrections are bounded by the approved Design and Delivery packages. Every correction requires M1 rereview, and M2 must not start while M1 remains open.
