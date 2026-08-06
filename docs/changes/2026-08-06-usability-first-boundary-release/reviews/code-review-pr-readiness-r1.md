# PR-Readiness Research Selector Correction Code Review R1

Review ID: code-review-pr-readiness-r1
Stage: code-review
Round: 1
Reviewer: Codex independent blind-first code-review peer
Target: f309c296a796b5bb6bc02db2ff991297c8ff084c..baadc82f90f14eda2038e4da5cbee99a63748dae
Reviewed artifact: commit baadc82f90f14eda2038e4da5cbee99a63748dae
Reviewed milestone: post-verify PR-readiness selector correction; M1-M4 remain closed
Review date: 2026-08-06
Recording status: recorded
Status: clean-with-notes
Review status: clean-with-notes
Native review status: clean-with-notes
Review gate outcome: advance
Independence level: L1
Author context ID: root-pr-readiness-research-selector-fix
Reviewer context ID: pr-readiness-r1-fresh-independent-selector-reviewer
Context separation mechanism: separate-agent-blind-first
Author context excluded: true
Risk tier: medium
Risk-tier triggers: validation-selector-routing; pr-fail-closed-compatibility; post-verify-correction
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: CONSTITUTION.md; specs/test-layering-and-change-scoped-validation.md; specs/test-layering-and-change-scoped-validation.test.md; skills/research/SKILL.md; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml; docs/changes/2026-08-06-usability-first-boundary-release/evidence/pr-readiness-research-selector-bugfix.md; docs/changes/2026-08-06-usability-first-boundary-release/explain-change.md
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/test-layering-and-change-scoped-validation.md@baadc82f#sha256:6dcb5b405c815774e689fc61b5476ba9eb2ee7425d60d118f062526b33734bcc; specs/test-layering-and-change-scoped-validation.test.md@baadc82f#sha256:eb8512055d61c27d1dff8540dae64b0458297ffdd8aa76a273c2bbfc46acf390; skills/research/SKILL.md@baadc82f#sha256:c90956ae2d2d5d35ecd38f8fd4e1bcda9dd0b8a9f851e7ca5a17a7f609109cb4; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml@baadc82f#sha256:04e96056a407c9cbdb73341b843cd8f8b8fd4bcac89c84378a83378dd2752803; docs/changes/2026-08-06-usability-first-boundary-release/evidence/pr-readiness-research-selector-bugfix.md@baadc82f#sha256:b1c05fa37af608b850a75b10ae1c3a5aa50ae5827fb6a301992544d9d053a9d0; scripts/validation_selection.py@baadc82f#sha256:1db7f2626d87114e0e939d1ce74ea4f5d5626cabedf3b650cf8b8fc275b81b28; scripts/test-select-validation.py@baadc82f#sha256:fe2f1bc681c587c2f75634035bf64638711406381269e67c89bfe3b80afce3e5; range:f309c296a796b5bb6bc02db2ff991297c8ff084c..baadc82f90f14eda2038e4da5cbee99a63748dae.diff@baadc82f#sha256:2f01c56da506694f235eb90e87469ecaed5d5eba47bcf0bd14e9b4721db396bd
Prompt template version: code-review-v1
Initial packet hash: sha256:2f01c56da506694f235eb90e87469ecaed5d5eba47bcf0bd14e9b4721db396bd
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: research-artifact path classification and PR selected-check routing
Highest-impact failure modes: over-broad classification; wrong owned checks; partial execution with unknown paths; weak regression; stale lifecycle readiness
Changed boundaries: selector path classifier; path-to-check routing; regression matrix; post-verify workflow evidence
Evidence expected: exact diff; governing selector clauses; canonical and near-match probes; PR-mode path discovery; exact check commands; focused and full selector regression; lifecycle validation
Areas requiring direct inspection: research path predicate; research category routing; check catalog command synthesis; regression assertions; PR selector output; change-local handoff
Areas intentionally out of scope: release implementation; broad release rerun; hosted CI; PR opening; tag; publication; push; merge
Risk classes considered: requirement-fidelity=applicable; validation-routing=applicable; compatibility=applicable; lifecycle-closeout=applicable; release-behavior=not-applicable:selector-only-correction; live-publication=not-applicable:forbidden-lifecycle-action; external-mutation=not-applicable:forbidden-lifecycle-action
Falsifiable review questions: Does the canonical research Markdown path select exactly its two owned documentation checks? Do non-Markdown and unrelated unknown paths remain fail-closed? Does PR range discovery use the same classification without weakening mixed-path blockers?
Invocation manifest: `docs/changes/2026-08-06-usability-first-boundary-release/review-invocation-code-review-pr-readiness-r1.yaml`
Automated review: yes
Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: scripts/validation_selection.py; scripts/test-select-validation.py; docs/changes/2026-08-06-usability-first-boundary-release/evidence/pr-readiness-research-selector-bugfix.md; docs/changes/2026-08-06-usability-first-boundary-release/change.yaml; docs/changes/2026-08-06-usability-first-boundary-release/explain-change.md
Requirement-fidelity matched path triggers: scripts/*validator*; docs/changes/**/review-*.md
Requirement-fidelity matched category triggers: workflow routing contracts; spec-derived validators
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > decomposition > research output contract > correction diff > regression assertions > direct PR probes > validation evidence
Requirement-property decomposition evidence: present
Requirement-fidelity receipt: yes
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: none remaining
Requirement-fidelity no-finding rationale: The shared selector now recognizes the research skill's canonical Markdown output family, selects both path-scoped documentation checks, and preserves structured blocking for unsupported paths in explicit and PR-discovered changed sets.
Material findings: None
Immediate next stage: explain-change
Automatic downstream handoff: explain-change
Milestone closeout: post-verify correction closed; M1-M4 remain closed
Required review-resolution: no
Verify readiness: not-claimed
Final holistic review: approved

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this clean review receipt, invocation manifest, review log, review-resolution closeout, and change-local routing state
- Open blockers: none
- Next stage: explain-change
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-06-usability-first-boundary-release/reviews/code-review-pr-readiness-r1.md`
- Review log: `docs/changes/2026-08-06-usability-first-boundary-release/review-log.md`
- Review resolution: `docs/changes/2026-08-06-usability-first-boundary-release/review-resolution.md`
- Reviewed milestone: post-verify PR-readiness selector correction; M1-M4 remain closed
- Milestone closeout: closed
- Remaining implementation milestones: none
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs and diff summary

- The exact target changes five files: selector classification and routing, one focused regression, correction evidence, change metadata, and the durable explanation.
- `docs/research/*.md` is classified as `research-artifact` and routes to the existing path-scoped `documentation_prose.audit` and `markdown_readability.validate` checks.
- The target does not change either validator, selector status composition, check execution, PR path discovery, release behavior, generated output, or public artifacts.

## Findings

No blocking or required-change findings.

## Requirement and boundary reconciliation

- Selector spec R3a-R4e keeps one shared classifier across explicit and PR modes; the correction adds one artifact-centric category without duplicating mode logic.
- R13a is preserved: the correction range itself selects `selector.regression` through PR mode.
- R14-R15b remain fail-closed: an unsupported `docs/research/*.txt` near match exits 2 with `unclassified-path`, and mixed classified-plus-unknown inputs remain blocked rather than executing partial targeted proof.
- The research skill's preferred `docs/research/YYYY-MM-DD-slug.md` output is the canonical positive fixture. A historical PR range that added that artifact now classifies it and emits exactly the two owned, path-scoped commands.

## Validation evidence challenged

- Focused selector tests: the research route, unknown-path block, mixed-path block, and PR-mode unknown-path block all pass.
- Complete `python scripts/test-select-validation.py`: pass after the focused proof.
- Historical research-addition PR range: status `ok`, canonical path classified as `research-artifact`, no unclassified or blocking result, exactly the two owned commands for that path.
- Exact correction-range PR selection: status `ok`, no blocker, and `selector.regression` selected for both selector implementation and regression paths.
- Direct `documentation_prose.audit`: exit 0 in report-only mode with the recorded eight errors and ten warnings.
- Direct `markdown_readability.validate`: exit 0 with the recorded three non-blocking warnings.
- Change metadata and review-artifact structure validation pass before recording this receipt; scoped lifecycle validation passes with only pre-existing merge-language warnings.
- `git diff --check f309c296..baadc82f`: pass.

## Checklist coverage

- Spec alignment: pass; the category is artifact-centric, uses the shared selector, and preserves R13/R14 fail-closed routing.
- Test coverage: pass; exact category, exact selected IDs, no blockers, unknown-path rejection, mixed-path blocking, and PR discovery have direct proof.
- Edge cases: pass; non-Markdown near matches, unrelated unknown paths, mixed changed sets, and PR range discovery were challenged.
- Error handling: pass; unsupported paths still return structured blocking results and cannot silently receive empty targeted proof.
- Architecture boundaries: pass; selection remains in the repository-owned selector and existing validators remain independent proof executors.
- Compatibility: pass; explicit and PR modes share the new route, while existing unknown-path and selector-self-registration behavior remains intact.
- Security/privacy: pass; selected commands use repository-relative paths and no environment or credential values are exposed.
- Derived artifact currency: pass; no generated or release artifact changed, and durable correction evidence and explanation agree with the code.
- Unrelated changes: pass; the five-file diff is limited to the selector fix, regression, rationale, and lifecycle handoff.
- Validation evidence: pass; focused and full selector proof plus direct command and PR-mode probes cover the changed boundary without a broad release rerun.

## Clean-review sufficiency

Review target identity: `f309c296a796b5bb6bc02db2ff991297c8ff084c..baadc82f90f14eda2038e4da5cbee99a63748dae`.
Governing artifacts inspected: Constitution, approved selector spec and test spec, research skill output contract, owning change state, correction evidence, and durable explanation.
Adversarial hypotheses tested: over-broad non-Markdown match, wrong check identity, missing path scoping, explicit-only behavior, PR changed-set omission, selector-self-registration loss, mixed-path partial execution, and stale post-verify routing.
Direct proofs performed: exact diff inspection, canonical and near-match selection, historical PR range classification, exact correction-range PR selection, four focused regressions, complete selector regression, direct selected validators, metadata/lifecycle checks, and diff check.
Validation evidence challenged: yes; the correction evidence was not accepted alone, and its explicit-mode regression was supplemented with direct PR-range, command-string, near-match, and mixed-block probes.
Unreviewed surfaces: broad release validation, hosted CI, refreshed final verify, PR creation, and all external release operations.
Confidence: high.
No-finding rationale: the correction adds the missing canonical artifact route with exactly its existing documentation checks, proves the public PR discovery seam directly, and leaves unknown paths fail-closed.

## Residual risks

- The prose audit intentionally remains report-only, so its eight existing errors are visible but do not block selector status.
- Final verification must refresh branch-readiness evidence after this post-verify correction; code review does not claim verify or PR readiness.

## Handoff

The post-verify selector correction is clean and M1-M4 remain closed. Route to refreshed `explain-change`, then `verify`; no PR or external release action is authorized by this review.
