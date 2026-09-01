# Code Review M4 R2: V3 Package Parity Corrections

Review ID: code-review-m4-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review agent
Target: corrected M4 implementation commit `64bd8791`
Reviewed artifact: complete M4 diff `585c2beecea0ddda0ae11ed8f0b1a53b24310052..64bd8791`, including the correction to Code Review M4 R1
Review date: 2026-09-01
Status: clean-with-notes
Recording status: recorded
Material findings: none
Reviewed milestone: M4

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-invocation-code-review-m4-r2.yaml`, `review-log.md`, and `review-resolution.md`
- Open blockers: none in the M4 implementation review; formal lifecycle progression remains blocked by package-authority state
- Next stage: workflow milestone closeout when package authority is restored
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none for durable review evidence; lifecycle recording/settlement not attempted because the current context permits only `route-correction`
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m4-r2.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M4
- Milestone closeout: blocked
- Remaining implementation milestones: M4, M5, M6
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Scope and authority

Reviewed the complete corrected M4 implementation against clean Design Review R2, clean Delivery Review R3, the revised approved design package, the exact primary plan at SHA-256 `5bdf89552ab9a0f88988c62f5d9ae57dae8e12a184d18bb678fc73254fa81514`, M4 TG-15 through TG-18, and the applicable FV, boundary, and interaction requirements. The review inspected canonical and generated skill semantics, staged adapter composition, parsed-YAML authority selection, compatibility boundaries, tests, and the M4 evidence record. It did not edit implementation or start M5.

The current lifecycle context reports revision `sha256:226db424130e15c9f64e71e4248ba630da619b473ffd49a80592451687024bd4`. It identifies `record-review` as the contextual registration operation but exposes only `route-correction` as a permitted state-changing operation because Design and Delivery package authority remains withheld. Therefore this review records durable evidence but does not attempt an unauthorized milestone transaction.

## Prior finding reconciliation

| Finding | R2 classification | Direct evidence |
| --- | --- | --- |
| `FV-M4-CR1` | resolved | Canonical Verify has no pre-Verify explanation input or correction route, generates explanation only after successful final readiness, and all three staged candidates omit `explain-change` while retaining the complete Verify resource closure. Current workflow text selects v3 alone; v1/v2 are readable history, and the implementing change's v2 closeout is isolated as a one-time plan bootstrap. |
| `FV-M4-CR2` | resolved | The shared safe-YAML mapping parser rejects repeated keys before assignment at every recursive depth. Boundary validation delegates to that parser and has no raw-text or top-level duplicate checker. Reversal tests cover `artifact_states`, `plan`, `kind`, `role`, and `path` for v2 and v3. |

## Actual-diff assessment

- The current canonical route is Code Review, triggered review resolution and CI maintenance, Verify, then PR. Verify owns the durable explanation only for a successful result; failed and inconclusive attempts emit none.
- Historical v1/v2 records and release archives remain readable but select no current route. The only preactivation v2 closeout exception is bound in the approved plan to this implementing change and is not encoded as a reusable current checker branch.
- Temporary Codex, Claude Code, and opencode v3 archives derive from canonical sources, omit the standalone explanation skill, include every mapped Verify reference and asset, and reject mixed inventory.
- Registered-plan boundary proof uses one semantic change-metadata parser. Duplicate keys at any mapping depth fail before lifecycle contract, artifact state, kind, role, or path can acquire authority.
- The corrected metadata-policy fixture now contains one `review` mapping, so its success does not rely on duplicate last-wins normalization.
- No tracked historical release archive or adapter ZIP changed in the complete M4 range. The active adapter manifest and final-verification activation state remain outside M4 publication authority.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The package implements the v3-only current route, success-only explanation, read-only history, and plan-isolated bootstrap approved by Design R2 and Delivery R3. |
| Test coverage | pass | Canonical semantics, all three adapter candidates, recursive duplicate orders and depths, corrected fixture, and active snapshot checks pass. |
| Edge cases | pass | Mixed archives, malformed and duplicate metadata, unsafe or missing plan paths, incomplete proof allocation, scoped Verify loading, and reverse duplicate order are direct regressions. |
| Error handling | pass | Unknown or ambiguous parsed authority fails closed before plan selection; candidate validation rejects unexpected `explain-change` entries. |
| Architecture boundaries | pass | Verify owns readiness and success-only rationale; Workflow owns routing; parser authority is shared; adapter publication remains staged. |
| Compatibility | pass | Historical v1/v2 are readable without current progression authority; the implementing-change bootstrap remains plan-bound and public activation is deferred. |
| Security/privacy | pass | No new network, credential, secret, or uncontrolled filesystem authority was introduced. |
| Derived artifact currency | pass | Canonical skills validate, generated skills are current, and all three temporary adapter candidates validate from canonical bytes. |
| Unrelated changes | pass | No historical archive or tracked adapter ZIP changed; the range is limited to the approved design/plan correction, M4 package work, tests, evidence, and review records. |
| Validation evidence | pass | Planned suites and direct adversarial probes reproduce both R1 failure families and show them rejected. |

## Direct adversarial evidence

- Direct parser probes reject duplicate `artifact_states`, `plan`, `kind`, `path`, and `role` mappings. The repository matrix repeats each authority-relevant case in both orders under v2 and v3.
- Source inspection confirms `boundary_first_validation.py` contains no raw-text or top-level duplicate scanner and loads `validate-change-metadata.py` as the sole parsed-YAML authority.
- The staged-archive suite opens each of the three generated archives, rejects an injected `explain-change` entry, verifies every Verify resource, and scans the published Verify body for the former prerequisite and handoff clauses.
- The complete M4 name set contains no `docs/releases/` path and no tracked adapter ZIP, so historical release bytes were not mutated.

## Validation performed

- `python scripts/test-skill-validator.py` — 386 tests passed.
- `python scripts/validate-skills.py` — 21 canonical skills passed.
- `python scripts/test-build-skills.py` — 8 tests passed.
- `python scripts/build-skills.py --check` — passed.
- `python scripts/test-boundary-first-validation.py` — 69 tests passed.
- `python scripts/validate-boundary-first.py --check` — passed, including active snapshot and rollback identities.
- `python scripts/test-change-metadata-validator.py` — 107 tests passed.
- `python scripts/test-adapter-distribution.py` — 156 tests passed.
- `python scripts/validate-documentation-prose.py --mode audit --path CONSTITUTION.md --path AGENTS.md --path docs/workflows.md --path specs/rigorloop-workflow.md --path skills/verify/SKILL.md --path skills/workflow/SKILL.md` — 0 errors and 48 review-visible warnings.
- Direct recursive duplicate parser probe — all five authority key families rejected.
- `git diff --check 585c2beecea0ddda0ae11ed8f0b1a53b24310052..64bd8791` — passed.
- Historical-path audit over the complete M4 name set — no release archive or tracked adapter ZIP changed.

## No-finding rationale and residual risks

Both R1 counterexamples now fail at their public or shared authority boundary, and the complete corrected M4 slice is coherent with the revised Design and Delivery decisions. No unresolved accepted M4 implementation fix remains.

Residual risk belongs to later milestones: M5 must assemble and validate the non-authoritative activation candidate, and M6 must close the implementing v2 record from the immutable snapshot before activation. This milestone-local review does not claim activation, lifecycle settlement, final holistic review, Verify success, branch readiness, or PR readiness.

## Handoff

- Reviewed milestone: M4
- Review status: clean-with-notes
- Milestone closeout: blocked by current lifecycle package authority, not by an M4 implementation finding
- Remaining implementation milestones: M4, M5, M6 until Workflow records closeout
- Required review-resolution: no
- Recommended next stage: restore current Design/Delivery package authority, then let Workflow record M4 completion and route to M5
- Final closeout readiness: not ready; M5 and M6 remain, and final holistic Code Review and Verify have not run
