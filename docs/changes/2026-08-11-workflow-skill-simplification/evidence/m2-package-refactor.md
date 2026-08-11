# M2 Package Refactor Evidence

## Scope

Milestone M2 changed only the canonical workflow package and the existing skill-validator suite:

- shortened `skills/workflow/SKILL.md` to the universal dispatcher contract;
- added governed-lifecycle, bounded-automation, and guide-authoring references;
- kept the boundary-first reference and workflow-guide skeleton unchanged;
- redirected compatibility assertions to the conditional reference that now owns each rule;
- added focused predicate, assembly, bootstrap, ownership, and fail-safe assertions.

## Test-first proof

Before the package edit, this command failed as expected:

```text
python scripts/test-skill-validator.py WorkflowSkillSimplificationContractTests
```

Result: six tests ran; five failed and two errored because the three mapped references, four predicates, seven assemblies, bootstrap sequence, and reference-specific ownership clauses did not yet exist. The structural-skeleton test passed, confirming that the unchanged skeleton already remained policy-free.

## Final validation

The completed M2 package passed:

```text
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/test-build-skills.py
python scripts/build-skills.py --check
git diff --check
```

Results:

- canonical skill validation: 24 skills passed;
- skill-validator suite: 297 tests passed, 16 skipped;
- build-skill suite: 7 tests passed;
- generated-skill check: passed using temporary output;
- diff whitespace check: passed.

No target agent runtime was executed.

## Ownership result

| Contract | Final owner |
| --- | --- |
| Classification, source rank, unknown artifacts, isolation, universal stops, claims, handoff | `SKILL.md` |
| Governed identity, state interpretation, architecture applicability, transitions, milestone settlement, final closeout | `references/governed-lifecycle-routing.md` |
| Commands, bootstrap, stateless status/off, authorization, receipts, review gates, correction, target promotion | `references/bounded-workflow-automation.md` |
| Guide creation/refresh procedure, skeleton use, project customization, migration notes | `references/workflow-guide-authoring.md` |
| Boundary expansion method | existing `references/boundary-first-method-v1.md` |
| Guide labels and structure | existing `assets/workflows-skeleton.md` |

Automation asks the governed reference for lifecycle transitions and does not redefine them. Guide authoring renders established policy and does not own routing semantics.

## Preliminary size result

LF-normalized canonical file counts after M2:

| Resource | Lines | Words | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| `SKILL.md` | 261 | 2,627 | 19,500 |
| governed reference | 57 | 568 | 4,601 |
| automation reference | 65 | 724 | 5,689 |
| guide reference | 44 | 409 | 3,046 |
| boundary reference | 110 | 857 | 6,346 |
| guide skeleton | 234 | 1,236 | 9,551 |
| package total | 771 | 6,421 | 48,733 |

Compared with the M1 baseline, `SKILL.md` fell from 4,333 to 2,627 words (39.4 percent) and from 32,074 to 19,500 bytes (39.2 percent). Total package content fell from 6,426 to 6,421 words (0.1 percent), while bytes rose from 47,971 to 48,733 (1.6 percent). The small byte increase is the explicit trigger and ownership structure needed for progressive disclosure, not hidden deletion. M3 will record exact assembly-specific measurements and adapter/archive/install parity.

## Review-resolution evidence

Code review M2 R1 recorded WFSIM-CR1 through WFSIM-CR3 before correction. The accepted correction:

- made unknown stages, every unmatched or multiply matched predicate combination, and post-classification resource confirmation explicit inline;
- added automation-reference loading to the complete ordered bootstrap procedure and test;
- resolved all 25 semantic-rule destinations against actual final headings;
- reclassified the exact `Quick operating guide` heading from its approved R2-R2a authority and migrated the incidental `Workflow Categories` assertion to `Lifecycle overview`.

The final change-local proof reported `rules=25 literals=13 scenarios=16 destinations=resolved unknown_values=rejected`; the full permanent validation commands remained green.

## Unchanged surfaces

- lifecycle order, state vocabulary, stage authority, milestone semantics, review outcomes, and claims are unchanged;
- automation persistence schema and command implementation are unchanged;
- the boundary-first reference and workflow-guide skeleton bytes are unchanged;
- no generated package was hand-edited;
- no new runtime, state store, selector, scheduler, validator family, tokenizer dependency, or size gate was introduced.
