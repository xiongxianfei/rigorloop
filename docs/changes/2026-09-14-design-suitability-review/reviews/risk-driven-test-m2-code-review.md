# Risk-driven test redesign M2 Code Review

## Initial result

- Skill: code-review.
- Review status: approved after correction.
- Finding: RT-M2-CR-01 resolved; no open material finding.
- Scope: the two-file M2 baseline-relative change only.
- Recording status: recorded, advisory-durable/manual.
- Reviewer: `/root/validation_design_review`; author: `/root`.
- Required full execution remains pending and is not claimed passed.

## RT-M2-CR-01

- Severity: major.
- Location: `tests/engineering/packaging/test-adapter-distribution.py`, replacement for `test_optional_discovery_packages_have_archive_and_clean_install_parity` in the independent archive-inventory case; related transferred canonical assertion in `tests/skill/skill_guidance_tests.py`.
- Evidence: the removed case rejected four repository-specific byte strings across complete emitted archive SKILL.md and selected resource contents. The transferred assertion now examines canonical input only. The retained inventory compares complete bytes for resources/Codex but only the body after frontmatter for Claude. Therefore forbidden repository content introduced by transformation into an otherwise supported Claude metadata field is outside both replacement assertions. Existing unsupported-metadata-key proof is a different boundary. Archive validation using production rendering is not an independent oracle for a rendering defect shared with its expected output.
- Governing requirement: TEST-SR-04/05/07/08 and M2's preservation of distinct current detection before consolidation.
- Required outcome: retain the original complete emitted-content portability check, including Claude frontmatter, for the optional-discovery selected members while reusing the consolidated actual archive fixture. Do not add another full build or weaken the ownership transfer's canonical checks.
- Safe resolution: independently assert the original forbidden bytes are absent from the relevant actual archive member bytes in the already-running inventory case, and demonstrate sensitivity to a producer-only forbidden metadata injection or equivalent inspected counterexample. Reassess affected current proof after correction; preserve pending/failed observations truthfully.
- Correction owner: implementation.

Other reviewed changes appear coherent so far: the current archive inventory retains complete resource/body identity, real installation selects the union of discovery/proposal consumers, drift negatives establish a valid one-skill baseline, and selection preflight rejects before missing archive access. This finding is recorded before any reviewer-requested correction. No engineering files were edited by the reviewer.

## Final correction disposition

RT-M2-CR-01 is resolved. The consolidated inventory now directly checks all four original forbidden byte strings in each actual archived explore/research SKILL.md, including transformed Claude frontmatter. Exact resource-byte parity plus the transferred canonical resource checks preserve the original resource-content contribution. Reviewer inspected the counterexample mechanism: a producer-only forbidden string in Claude frontmatter is directly included in the new `assertNotIn` input instead of being discarded by the body comparison. This is an inspected failure mechanism, not a claim that an additional seeded mutation run occurred. No additional build was added.

Fresh corrected independent inventory plus actual clean installation passed in 16.512 seconds. The correction changed only this test method; the other test/production subjects and observations remain unaffected. Reviewer rechecked the exact identities below before final judgment.

## Complete equivalence and execution assessment

The removed optional-discovery archive case transfers its source portability/resource expectations to Skill and retains actual output constraints through the corrected independent archive inventory. Its real installer consumers are included in the union `(explore, research, proposal, proposal-review)`. The removed targeted-profile case is covered by independent complete resource/body parity, including Design's resources, plus the transferred canonical primary-interface assertions. The removed proposal happy path is represented by actual installation of both proposal skills from the same current candidate. The old hardcoded version literals supplied current source fixtures, not distinct supported historical-version behavior; retained candidate/version tests continue to own that boundary.

The actual install operation executes the packed CLI for both targets and checks installed resource hashes against canonical expectations. Reviewer inspected its implementation and its claim limits; this is not a mocked builder or an exit-only claim. Existing conflict, force, traversal, unsafe-type and unrelated-state tests remain. The separate boundary-first tree/archive/install digest scenario is retained because it protects a distinct composed observation. Small drift fixtures retain both named boundary layer paths, establish a passing baseline, then corrupt actual archive bytes and require layer-specific parity diagnostics. Selection preflight now runs before any archive exists and asserts the intended error, strengthening detection of wrong ordering without unnecessary builds.

Reviewer independently compared discovery: Packaging 96→93 removes exactly the three assessed groups; Skill 289→291 adds the two transferred guidance groups and loses none. Every other original case identity remains. Existing helper routing reaches both owners; no production change or new runtime dependency is introduced.

Actual complete evidence:

- Direct Packaging: 93 passed in 184.413 seconds.
- Direct npm package: 8 passed in 28.086 seconds.
- Direct Skill: 291 passed in 21.408 seconds.
- Selected execution: 305 passed result rows, boundary scope passed, no failed/unstarted rows.
- Real `ReleaseCandidateIntegrationTests.test_actual_candidate_build_and_packed_metadata_chain`: passed in 80.647 seconds.
- Fresh corrected inventory with actual installation: passed in 16.512 seconds.

The initial candidate invocation used the wrong class and produced a loader error; it supplies no candidate evidence. The corrected real invocation above is the applicable observation. Complete runs began before the final inventory assertion correction, so their applicability excludes that modified method. Fresh corrected inventory execution replaces its earlier observation; unchanged other cases retain their actual results. This combined evidence is adequate under Assessment RC-SR-15 without calling the earlier entire run a run of final bytes or rerunning unchanged expensive proof.

Durable author rationale, exact commands and limits are in `../contract-refinement.md`. Detailed temporary logs are `/tmp/risk-driven-m2-packaging.log`, `/tmp/risk-driven-m2-npm.log`, `/tmp/risk-driven-m2-skill.log`, `/tmp/risk-driven-m2-ci.log`, `/tmp/risk-driven-m2-candidate-corrected.log` and `/tmp/risk-driven-m2-inventory-corrected.log`. The author reports evidence prose and diff checks passed. No runtime improvement is inferred from these measurements.

## Checklist

| Criterion | Judgment and basis |
| --- | --- |
| Spec alignment | Pass: M2 preserves important protection while separating canonical guidance and artifact/consumer observations. |
| Test coverage | Pass after RT-M2-CR-01: every removed group's identified assertions have retained or transferred detection. |
| Edge cases | Pass: exact resource drift, selected-input preflight, two-target installation and retained unsafe-path/type cases. |
| Error handling | Pass: valid drift baseline, intended diagnostic and nonzero command observations; wrong candidate invocation remains reported as failed. |
| Architecture boundaries | Pass: Skill owns canonical guidance; Packaging retains actual generated and installed product proof. |
| Compatibility | Pass: deliberate three-group consolidation accounted for; unchanged case IDs and actual aggregate/selected consumers retained. |
| Security/privacy | Pass for scope: owned temporary fixtures, retained containment/mutation checks and restored emitted portability constraints. |
| Derived artifact currency | Pass: actual archives, packed installer, npm suite and real prepared candidate observed. |
| Unrelated changes | Pass: two-file baseline-relative scope only; previous dirty work is not approved here. |
| Validation evidence | Pass: complete relevant execution plus fresh corrected method; limits and exact basis preserved. |

## Exact final subjects

The two test files are the implementation slice. Design and plan are approved dependencies and remain unchanged. CLI subject inspection and reviewer byte recheck establish the final identities.

| Subject | SHA-256 identity |
| --- | --- |
| `tests/engineering/packaging/test-adapter-distribution.py` | `sha256:3b87d65ba9625e562d0b8b5497fe03c0cce656f4b05c4dd60a4789f09313c3e4` |
| `tests/skill/skill_guidance_tests.py` | `sha256:ac28ed085d26772f1aaedb7454e0ef66a79336f5ca09509af31ee778ba40b970` |
| `docs/plans/2026-09-15-risk-driven-test-redesign.md` | `sha256:687849e708b45cdf80e42ca3f12d7dbf168a64fd47a695bdffdb8dddc7a938e5` |
| `docs/design/engineering/validation.md` | `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14` |

M2 is approved with no unresolved concern. This independent advisory-durable milestone judgment supports M3 under the existing implementation authorization. It does not approve later milestones, the entire dirty branch, final Verify, hosted CI or publication. Fresh final whole-change Code Review and distinct Verify remain required after all implementation and corrections.

## Additional negative-sensitivity observation

After the approval above, an isolated producer mutation wrapped the real Claude renderer and injected `templates/shared` into explore's transformed description only. The real archive validation and packed installation completed before the case failed specifically at the restored complete emitted-byte assertion. Reviewer inspected `/tmp/risk-driven-m2-frontmatter-seed.py` and its successful detection log. This directly confirms RT-M2-CR-01's counterexample and correction; it strengthens the prior inspected-mechanism basis without changing engineering subjects, scope or judgment. No persistent production mutation or broad mutation-score claim is involved.
