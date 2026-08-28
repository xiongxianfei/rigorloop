# Code Review M3 R1: Invocation Integration and Log Inspection

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: fresh main-agent review
Reviewer context ID: root-m3-r1
Author context ID: root-m3-implementation
Target: current M3 invocation integration, log inspection, wrapper, selector, tests, and evidence
Reviewed artifact: M3 implementation/test/evidence bundle `sha256:b2ef0a7fb4d2cf548d06e636145d361d58c4ca8455ded0d1862b97834df28303`
Reviewed milestone: M3
Review date: 2026-08-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L0
Context separation mechanism: explicit assumption reset followed by authority-first inspection and new public-path probes
Author context excluded: false
Risk tier: elevated
Risk-tier triggers: privacy-sensitive lookup; diagnostic severity; lifecycle semantic isolation; production-wrapper compatibility; validation-routing fidelity
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`
Formal criteria: code-review-v1; requirement-fidelity-gate-v1; boundary-first-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:7693844003af6bd1b270d6dede9405c64b976afe838aaf4ab6444208710608ba; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:5e98900b19ff15a759dd59923c80d6a052281d345eec477d1814d82953a5a19e; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; packages/rigorloop/dist/bin/rigorloop.js@working-tree#sha256:c87b6879e4276b49ac03019d156ce902c04a64b5f3c842bd1fcc6b3736543264; packages/rigorloop/dist/lib/cli-observability.js@working-tree#sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c; packages/rigorloop/dist/lib/log-inspection.js@working-tree#sha256:cdb97a2686f03a0d52ee428b19793c18698d53b19e4134a03645f65b27d0c463; packages/rigorloop/dist/lib/lifecycle-cli.js@working-tree#sha256:c4e547996db586cb7759083bf04610e15b522fd41be52866633fec29e18f794b; packages/rigorloop/test/cli-invocation-observability.test.js@working-tree#sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08; packages/rigorloop/test/cli-observability.test.js@working-tree#sha256:4f47224080fc9d2266be1af2d10051d87a7327118d7720166d69bfef74c89f3f; scripts/validate-governed-lifecycle-cli.py@working-tree#sha256:6e6be3b9829b3be38f8de4151ed1f702064ca7d2cbb1b43c328b6cb82eb3d144; scripts/test-governed-lifecycle-cli-validator.py@working-tree#sha256:2f1d0fdda8f29148390155d89babadac4d0b42502c04cc492cc4bc26ba653880; scripts/validation_selection.py@working-tree#sha256:d27040dbf2a2f4d14d23c71ac9d00fcfc6e23ede1885f10f22f2a334386bbc75; scripts/test-select-validation.py@working-tree#sha256:b73733d1d8de590c208bf1ded64b1fc21e0518b82ee166ce4264fb308b863307; docs/changes/2026-08-25-cli-observability-token-efficient-results/evidence/m3-invocation-integration.md@working-tree#sha256:ee7c02b2855c4d5072ab5252832c01f34175762421d76e9543eef0d247449d01
Prompt template version: code-review-v1
Initial packet hash: sha256:b2ef0a7fb4d2cf548d06e636145d361d58c4ca8455ded0d1862b97834df28303
Manifest owner: direct reviewer
Forbidden initial context excluded: not-applicable to isolated manual review
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: public invocation correlation, log lookup and rendering, diagnostic severity, production-wrapper consumption, and validation selection
Highest-impact failure modes: returning unvalidated private fields; reflecting unsafe lookup input; suppressing internal failures at the default console level; declaring wrapper parity without executing the wrapper contract
Changed boundaries: BND-INPUT-001; BND-AUTH-001; BND-COMPOSE-001; BND-RECOVERY-001; BND-COMPAT-001; INT-001; INT-003; INT-004
Evidence expected: T06-T09 and T12-T14 public-path proof plus the exact M3 validation commands
Areas requiring direct inspection: `cli-observability.js`; `log-inspection.js`; top-level `rigorloop.js`; wrapper and selector scripts; M3 public-path tests; M3 evidence
Areas intentionally out of scope: M4 measurement and package-adoption decision; M1/M2 closeout already consumed by workflow; lifecycle mutation; final holistic review; verification; PR readiness
Risk classes considered: privacy; closed schemas; invalid input; severity; semantic isolation; wrapper compatibility; validation selection; evidence fidelity
Falsifiable review questions: Can a retained schema-1 object bypass the event allowlist? Can invalid identity text cross into output? Can lifecycle internal failure be recorded below error? Does a wrapper change select and execute the T13 matrix?
Automated review: no
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: packages/rigorloop/dist/bin/rigorloop.js; packages/rigorloop/dist/lib/cli-observability.js; packages/rigorloop/dist/lib/log-inspection.js; scripts/validate-governed-lifecycle-cli.py; scripts/test-governed-lifecycle-cli-validator.py; scripts/validation_selection.py; scripts/test-select-validation.py
Requirement-fidelity matched path triggers: specs/; docs/changes/**/reviews/
Requirement-fidelity matched category triggers: closed enums; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > plan milestone > test-spec case > implementation diff > direct probe > validation evidence
Relevant spec clauses decomposed: yes
Property matrix complete: no; four failing properties stop clean promotion
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested
Material findings: CLIOBS-M3-R1-F1, CLIOBS-M3-R1-F2, CLIOBS-M3-R1-F3, CLIOBS-M3-R1-F4
Immediate next stage: review-resolution
Automatic downstream handoff: none; direct isolated review stops on material findings
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `reviews/code-review-m3-r1.md`; `review-log.md`; `review-resolution.md`
- Open blockers: `CLIOBS-M3-R1-F1`, `CLIOBS-M3-R1-F2`, `CLIOBS-M3-R1-F3`, `CLIOBS-M3-R1-F4`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M3-R1-F1, CLIOBS-M3-R1-F2, CLIOBS-M3-R1-F3, CLIOBS-M3-R1-F4
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M3-R1-F1, CLIOBS-M3-R1-F2, CLIOBS-M3-R1-F3, CLIOBS-M3-R1-F4
- Verify readiness: not-claimed

## Finding CLIOBS-M3-R1-F1

Finding ID: CLIOBS-M3-R1-F1
Severity: major
Location: `packages/rigorloop/dist/lib/log-inspection.js:11-14`; `packages/rigorloop/test/cli-invocation-observability.test.js:391-400`
Evidence: Lookup treats every parsed object with `schema_version: 1` and a matching `invocation_id` as a valid event. A direct public CLI probe placed `{"schema_version":1,"invocation_id":"a1b2c3d4e5f60718","event":"invocation-start","private":"M3_LOOKUP_PRIVATE_SENTINEL"}` in the retained file; `rigorloop logs show ... --format json --no-file-log` exited 0 and returned the unapproved `private` field. The tracked lookup test uses an underspecified three-field object as its accepted event, so it entrenches the bypass instead of proving the closed event schema.
Required outcome: Exact lookup must return only fully validated schema-1 diagnostic events with the closed common and family-specific field sets; malformed, incomplete, unknown-field, and wrong-type matching records must fail or warn without returning their content.
Safe resolution path: Add a reusable read-side diagnostic-event validator derived from the same closed vocabulary as event construction, validate each parsed record before identity selection or rendering, and add public lookup regressions for unknown fields, missing required fields, wrong family extensions, invalid types, unsupported schema, and a private sentinel.
needs-decision rationale: none; R5-R9, R19-R20, E5, T08, and T09 already require validated allowlisted lookup output.

## Finding CLIOBS-M3-R1-F2

Finding ID: CLIOBS-M3-R1-F2
Severity: minor
Location: `packages/rigorloop/dist/bin/rigorloop.js:192-199`
Evidence: `handleLogs` copies the raw positional identity into the JSON result before grammar validation and interpolates it into the human error. Direct public probes with `M3_INVALID_PRIVATE_SENTINEL` exited 4 but returned the sentinel once in JSON and once on stderr. The M3 suite has no invalid-ID private-marker assertion across both formats.
Required outcome: Invalid invocation identities must produce the stable code without echoing, persisting, or otherwise returning the rejected raw value.
Safe resolution path: Validate the identity before constructing output, include `invocation_id` only after it passes the exact grammar, use a constant bounded human diagnostic on rejection, and add JSON/human public-path sentinel regressions.
needs-decision rationale: none; the safe invalid-input and T09 privacy boundaries already determine the outcome.

## Finding CLIOBS-M3-R1-F3

Finding ID: CLIOBS-M3-R1-F3
Severity: major
Location: `packages/rigorloop/dist/lib/cli-observability.js:18-21,82-107`; `packages/rigorloop/test/cli-invocation-observability.test.js:96-128`
Evidence: Terminal severity is inferred only from the numeric exit code, and exit codes 2, 3, 4, and 5 all map to warning. Lifecycle uses exit 3 for internal or otherwise unclassified operational failure. A direct controller probe returning lifecycle exit 3 produced an `invocation-complete` event with `status:error`, `severity:warning`, and no default-console diagnostic. The tracked severity matrix tests only success 0, blocked 2, and thrown/internal 1, so the lifecycle internal partition is absent.
Required outcome: Unexpected internal, unsafe-recovery, and logging failures must be recorded at error and meet the default error console threshold, while expected policy and input failures remain warning, without changing the semantic exit code.
Safe resolution path: Carry a normalized semantic exit class or terminal diagnostic class from dispatch into the invocation controller instead of treating the numeric exit code as the severity oracle. Add lifecycle exit-3 internal, logging-unavailable, unsafe-recovery, expected validation, usage, stale, and blocked public/controller cases that prove severity, status, console policy, and unchanged exit codes.
needs-decision rationale: none; R4 and the ADR already distinguish expected rejection from internal and logging failure.

## Finding CLIOBS-M3-R1-F4

Finding ID: CLIOBS-M3-R1-F4
Severity: major
Location: `scripts/test-governed-lifecycle-cli-validator.py:1-42`; `scripts/validation_selection.py:250-259,1986-1997,2378-2385`; `scripts/test-select-validation.py:2998-3003`
Evidence: The declared T13 command passed three tests, but all three call only `baseline_matches()` in-process. They never execute `validate-governed-lifecycle-cli.py`, inject child lifecycle results, check successful-output suppression, or cover success, blocked, usage, invalid-repository, stale, and internal exit classifications in detailed and concise formats. Selector routing classifies wrapper paths as generic `rigorloop-cli` and selects only `npm test --prefix packages/rigorloop` plus package publication; neither selected check executes the focused Python wrapper test. This contradicts the plan's focused wrapper-selection requirement and the M3 evidence claim.
Required outcome: The production wrapper must have executable T13 parity coverage, and changing either the wrapper or its test must deterministically select that focused check in addition to any broader package checks.
Safe resolution path: Expand the Python test to invoke the wrapper with a controlled child CLI across every T13 result/exit partition and assert one-time structured consumption, no duplicate successful child stdout, and preserved classification. Add a dedicated selector check ID for that command, route both wrapper paths to it, and add selector regressions proving the exact command is selected and failures propagate.
needs-decision rationale: none; R31, T13, the approved M3 plan, and CLIOBS-PLR2 already assign this proof.

## Actual-diff and boundary assessment

- Invocation controller: concern. Public correlation and ordinary success/blocking behavior work, but severity loses the semantic distinction between expected and internal exit-3 outcomes.
- Log inspection: concern. Bounded five-file scanning and exact identity filtering exist, but read-side event validation and safe invalid-input rendering are incomplete.
- Semantic isolation: pass for the exercised recorded, disabled, unsafe-path, and lock-exhaustion lifecycle-status matrix; the four modes preserved semantic output and repository bytes in the tracked test.
- Wrapper and selector: concern. The production wrapper runs successfully on the current repository, but the approved child-result matrix is neither implemented nor selected.
- Evidence adequacy: concern. Passing broad suites do not exercise the three direct failures and do not satisfy T13.

## Checklist coverage

- Spec alignment: concern; R4, R19-R20, and R31 have direct or proof failures.
- Test coverage: concern; invalid-ID privacy, read-side event validation, lifecycle exit-3 severity, and the production wrapper matrix are absent.
- Edge cases: concern; matching malformed records and semantic classes sharing one numeric exit code change outcomes.
- Error handling: concern; rejected identity text is reflected and internal exit 3 is downgraded.
- Architecture boundaries: concern; the controller lacks the normalized semantic classification needed by the ADR's severity boundary.
- Compatibility: concern; wrapper classification parity is asserted without executable coverage. Existing v0.4.x output tests otherwise passed.
- Security/privacy: concern; lookup returns unapproved retained fields and echoes rejected caller input.
- Derived artifact currency: concern; M3 evidence overstates wrapper and lookup proof. M4 package/measurement currency is outside this review.
- Unrelated changes: pass for the bounded M3 target; lifecycle-deadlock corrections and M4 proof were excluded from this verdict.
- Validation evidence: concern; declared gates pass, but three direct probes fail and the wrapper test does not exercise the production boundary.

## Validation evidence challenged

- `npm test --prefix packages/rigorloop`: passed 256/256.
- `python3 scripts/test-governed-lifecycle-cli-validator.py`: passed 3/3, but inspection shows all cases are pure `baseline_matches()` tests and none execute T13.
- `python3 scripts/test-select-validation.py`: passed 154/154.
- `python3 scripts/validate-governed-lifecycle-cli.py`: passed for 29 governed records with one declared baseline warning and no failures.
- Direct retained-event probe: exit 0 returned the unapproved `M3_LOOKUP_PRIVATE_SENTINEL` field.
- Direct invalid-identity probes: JSON and human paths each returned `M3_INVALID_PRIVATE_SENTINEL` with exit 4.
- Direct severity probe: lifecycle exit 3 produced `severity: warning`, `status: error`, and no default-console error event.

## Handoff

This direct review is isolated. There is no automatic downstream handoff, lifecycle mutation, milestone closeout, verification claim, CI claim, or PR-readiness claim. Review-resolution must accept and resolve `CLIOBS-M3-R1-F1` through `CLIOBS-M3-R1-F4`; implementation correction and a fresh M3 rereview must follow before workflow can settle M3 or consume the already-authored M4 evidence.
