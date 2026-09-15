# Risk-driven test redesign M1 Code Review

## Current assessment

- Skill: code-review.
- Review status: approved; no material findings.
- Milestone: M1 Skill recording-reference pilot.
- Recording status: recorded, advisory-durable/manual.
- Reviewer: `/root/validation_design_review`, separate from author `/root`.
- Artifacts changed by reviewer: this review only.
- Next stage: M2 under the existing implementation authorization; final whole-change review and distinct Verify remain required.
- Claim limits: no pending command pass, later-milestone completion or final Verify claim.

## Scope and source assessment

Review compares the six named implementation files against `/tmp/risk-driven-m1-before/` and `/tmp/risk-driven-m1.diff`, excluding unrelated accumulated branch edits. The exact approved risk-driven Design and Delivery plan govern M1. No published Skill or validator behavior changes are included: the only production modification routes three exact new Skill test-helper paths to existing checks.

The component suite replaces one sequential multi-fault canonical-copy case with nine independently initialized defects for both proposal pilots. Each fixture is first validated; each mutation changes its intended input; expected single diagnostics distinguish the intended failure from incidental invalid setup. Missing classification and missing load triggers now have distinct detection. Missing selected resources cannot be rescued by unrelated or inline content. Escape, undecodable bytes, missing heading, missing contract token and wrong mapping retain their negative boundaries. Canonical content validity remains separately observed.

The command/guidance split preserves existing TestCase/method selectors through non-TestCase mixins, avoiding duplicate registration. Real command execution succeeds with an empty target-tool PATH and with invocation traps; a swallowed target process failure still leaves a marker and fails the assertion. The scope is PATH-based dispatch, explicitly not all possible absolute tool paths or universal agent compliance. Structurally valid ambiguous prose remains accepted; the retained phrase guard explicitly disclaims semantic adequacy and is preserved while replacement equivalence is unknown. Existing byte-parity checks remain unchanged.

The selector adds only three known helper paths. Its new regression independently names Skill and Adapter checks, preserves the aggregate command and checks uniqueness. It failed for all three paths before routing correction. No permissive directory or unknown-path policy is introduced. The plan's directory shorthand is expanded to actual changed files because the existing selector rejects directory inputs; this is within the plan's explicit expansion requirement and does not weaken selected coverage.

Reviewer independently compared discovery: 280 original Skill IDs become 289, with exactly the original multi-fault selector removed and ten explicit replacements added (one canonical positive and nine component defects). Every other original ID remains. The old selector replacement is deliberate and permitted by the plan; mixed-in existing CLI/guidance selectors are preserved.

## Proof inspected so far

Direct full Skill suite passed 289 tests in 21.971 seconds. The nine ephemeral seeded validator defects are each detected for both pilots, and a real command mutation that attempts then swallows target invocation is detected by the trap marker. Reviewer inspected the mutation script and resulting ten observations; it changes the intended production branches in an isolated process/temporary command and restores the original references. This is bounded negative-sensitivity evidence, not a universal mutation score or a new repository subsystem.

Full selector and complete selected execution remain pending at this entry. No source issue currently requires correction; sufficient final execution is still needed for approval and isolated/concurrent consumer coverage.

## Exact subjects

The first six entries are the implementation slice; Design and plan are approved dependencies. Identities were captured through CLI subject inspection.

| Subject | SHA-256 identity |
| --- | --- |
| `tests/skill/test-skill-validator.py` | `sha256:69b9e56a03a7488416b92bd27d2c3a022366f40205875b080eb84d018cc4e710` |
| `tests/skill/skill_contract_tests.py` | `sha256:6c0096c7323720a31d030661ad5359bdae809cfbe05a974497110c408ba3a15f` |
| `tests/skill/skill_cli_tests.py` | `sha256:ed93b91247c55f04e2cf1243d7c786224e4290e791ea7ca42e67e76b663d6a18` |
| `tests/skill/skill_guidance_tests.py` | `sha256:6be23c8be3db051f302a4c6d543f0936aee90e4baa446739c39185441519ea7d` |
| `scripts/lib/validation/validation_selection.py` | `sha256:ecc28c80d20b9aeaec50004d29a918910045d5e80c02687ff70522cb2bee2c5e` |
| `tests/engineering/validation/test-select-validation.py` | `sha256:31fba7a21b0094136456159e3fc16f292474110c8c43e3f2bab267dc044c2d2a` |
| `docs/plans/2026-09-15-risk-driven-test-redesign.md` | `sha256:687849e708b45cdf80e42ca3f12d7dbf168a64fd47a695bdffdb8dddc7a938e5` |
| `docs/design/engineering/validation.md` | `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14` |

## Final milestone judgment

Approved on the exact subjects above. Completed direct selector proof passed all 182 cases in 181.41 seconds. The selected CI invocation expanded to the six actual changed file paths and exited 0 with all 537 result rows passed across `skills.regression`, `adapters.regression`, `selector.regression` and `validation_execution.regression`. It individually executed all 289 Skill cases, including the nine new component cases, under the existing shared execution budget. Reviewer inspected the log: no failed or unstarted row. Direct Skill, individual selected execution and discovery agree; caller protection and isolation are adequately demonstrated for M1.

Author evidence in `../contract-refinement.md` records the actual invocation, counts, source identities and limits; detailed logs are `/tmp/risk-driven-m1-skill.log`, `/tmp/risk-driven-m1-selector.log`, `/tmp/risk-driven-m1-ci.log` and `/tmp/risk-driven-m1-mutations.json`. The author also reports evidence prose and diff checks passed. Reviewer rechecked every recorded source/Design/plan identity after completed proof; all remain unchanged. Earlier pending statements above describe the initial inspection and are superseded by these actual results.

| First-pass criterion | Judgment and basis |
| --- | --- |
| Spec alignment | Pass: bounded M1 pilot implements independent fault fixtures and real command observation without semantic gate expansion. |
| Test coverage | Pass: all former fault mechanisms retained, canonical positive separate, nine seeded defects detected for both targets. |
| Edge cases | Pass: missing/escaping/undecodable selected resources, classification/load distinction and attempted swallowed runtime dispatch observed. |
| Error handling | Pass: precise component diagnostics, actual command status/output and marker absence; no failure suppression. |
| Architecture boundaries | Pass: component, command and canonical-guidance responsibilities split with retained aggregate loader. |
| Compatibility | Pass: every unchanged selector retained, intentional multi-fault selector replacement accounted for, exact helper routes select existing consumers. |
| Security/privacy | Pass for scope: invocation-owned temporary state and trap logs, no external runtime or publication introduced. PATH observation limits are explicit. |
| Derived artifact currency | Pass for affected scope: source unchanged; selected Adapter consumer protection passed and byte-parity tests retained. No packaged-source edit is claimed. |
| Unrelated changes | Pass: six-file baseline-relative diff reviewed; earlier dirty work excluded. |
| Validation evidence | Pass: direct full suites plus complete individually executed selected scope, bounded seeded proof and current exact identities. |

No finding or correction remains for M1. The semantic phrase drift guard is intentionally retained with an explicit claim limit while its replacement equivalence remains unknown, consistent with TEST-SR-09 and the approved plan; this does not block the pilot or approve those phrases as semantic proof. No speed improvement is inferred from timings or case count.

This is independent advisory-durable approval of the M1 implementation slice. It supports proceeding to M2 under the user's existing implementation authorization, without approving M2–M4, the entire dirty branch, final Verify, hosted CI, PR or publication. Required later milestone reviews, fresh final whole-change Code Review and distinct Verify remain separate.
