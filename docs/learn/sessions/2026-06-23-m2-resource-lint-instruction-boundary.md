# Learn Session: M2 Resource-Lint Instruction Boundary

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation after M2 received another
  code-review finding, asking why the milestone is still not fixed and what
  best practices should guide the next resolution.
- Trigger type: explicit maintainer request / repeated review findings within
  one milestone.
- Scope:
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r1.md`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r2.md`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r3.md`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
  - `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`
  - `scripts/skill_validation.py`
  - `scripts/test-skill-validator.py`
- Evidence in scope:
  - `SRI-M2-CR1`, which found ordinary load-condition wording such as
    `when relevant` could suppress recognized legacy resource-loading
    instructions.
  - `SRI-M2-CR2`, which found explicit external ownership was still applied at
    whole-line scope instead of per matched resource reference.
  - `SRI-M2-CR3`, which found the CR2 resolution now joins every contiguous
    nonblank non-heading line, allowing a loading verb in one Markdown list
    item to make a separate generated-artifact or example path fail.
  - prior learn session
    `docs/learn/sessions/2026-06-23-m2-resource-lint-review-root-cause.md`.
- Explicit exclusions:
  - this session does not fix `SRI-M2-CR3`;
  - this session does not close M2, claim M3 readiness, update validators,
    update specs, update skills, or claim branch/PR readiness;
  - this session does not update curated topic files without separate
    contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-06-23-m2-resource-lint-review-root-cause.md`
  - `docs/learn/README.md`
  - `docs/learn/topics/*` search for existing resource-lint or validator-test
    guidance.
- Session record path:
  `docs/learn/sessions/2026-06-23-m2-resource-lint-instruction-boundary.md`

## Observe

### O1 - M2 is failing because each fix repairs one classifier layer without rechecking the full pipeline

Evidence:

- `SRI-M2-CR1` fixed the suppressor vocabulary: broad project-local allowed
  terms no longer suppress ordinary `templates/... when relevant` instructions.
- `SRI-M2-CR2` fixed the suppressor decision unit: external ownership and
  illustrative context are evaluated per matched resource path.
- `SRI-M2-CR3` shows a different layer broke: instruction segmentation now
  joins independent Markdown list items, so a loading verb in one item applies
  to artifact/example paths in another item.

Observation:

The recurring issue is not that the previous fixes were fake. Each fix closed
the finding it targeted. The root problem is that the implementation has not
been treated as a small classifier pipeline with explicit stage boundaries:

```text
segment operative instructions
-> detect resource-loading intent within that segment
-> find skill-local-looking paths
-> classify ownership/context per path
-> apply exact temporary exceptions
-> emit diagnostics
```

CR1 changed the vocabulary stage. CR2 changed the per-path context stage. CR3
exposes that the segmentation stage is still underspecified.

### O2 - The CR2 resolution overcorrected to support wrapped instructions

Evidence:

- The CR2 implementation added `_iter_resource_instruction_lines`, which joins
  every contiguous nonblank non-heading line into one instruction.
- The CR2 tests include split-line mixed references such as:

```md
Use the user-provided references/external.md and
templates/architecture.md when relevant.
```

- The CR3 review fixture shows two independent list items are also joined:

```md
- Use the user-provided references/external.md.
- The generated artifact may contain the string templates/architecture.md.
```

Observation:

Supporting wrapped prose is valid, but the implementation used paragraph
joining as a substitute for Markdown instruction segmentation. That made the
fix pass wrapped-line cases while creating a false-positive path for adjacent
independent list items.

### O3 - The test suite is still example-driven instead of boundary-matrix-driven

Evidence:

- CR1 added single-reference false-negative and false-positive cases.
- CR2 added mixed-reference cases where one instruction contains two paths with
  different classifications.
- CR3 found a case involving two adjacent instruction segments: one operative
  resource load and one non-operative artifact/example string.

Observation:

The tests are improving, but they are being added one review finding at a time.
For this validator, the important matrix is not only path ownership. It also
needs segmentation boundaries:

```text
same line
wrapped continuation line
same Markdown list item
separate Markdown list item
separate paragraph
fenced example
Resource map section
```

A validator that classifies text should prove both "must catch" and "must not
catch" cases at every boundary where context could leak.

### O4 - The immediate best fix should be a small model correction, not a broad rewrite

Evidence:

- M2 scope is the canonical resource-integrity validator and fixtures.
- The active plan explicitly keeps architecture resource normalization,
  generated-resource parity, clean-install smoke, runtime fallback, and
  repository-wide enforcement out of this review-resolution slice.
- CR3's required outcome is local to instruction assembly and false-positive
  fixture coverage.

Observation:

The correct next move is narrow: define instruction segments safely and add the
missing regression. Do not redesign resource-map parsing, approved classes,
temporary architecture resource normalization, generated output parity, or
clean-install checks while resolving CR3.

## Root Cause

M2 is still not fixed because the legacy-resource lint has been treated as a
sequence of text-matching patches instead of a classifier with explicit
decision boundaries.

The deeper root cause is boundary drift across three layers:

1. `CR1`: ownership/load-condition vocabulary was too broad.
2. `CR2`: ownership context was evaluated at the wrong unit, the whole line
   instead of each resource reference.
3. `CR3`: instruction intent is now evaluated at the wrong unit, a joined block
   of contiguous lines instead of an operative Markdown instruction segment.

Each fix solved the named review example but did not fully re-derive the
classifier model and its test matrix. The latest failure is a false positive:
paragraph joining caused a loading verb in one list item to leak into a
separate artifact/example list item.

## Best Practices

1. Model the validator as a pipeline before editing.
   Name each stage and its input/output: instruction segment, loading intent,
   path match, path ownership, exception, diagnostic.

2. Define the decision unit for every stage.
   Loading intent belongs to one operative instruction segment. External
   ownership belongs to one matched path. Temporary exceptions belong to an
   exact skill/path/instruction contract.

3. Separate Markdown segmentation from path classification.
   First split the skill body into safe instruction segments. Only then run
   resource-loading and path-ownership classification inside each segment.

4. Join only true continuations.
   Wrapped prose in one instruction can be joined. Independent Markdown list
   items, blank-line-separated paragraphs, headings, fenced blocks, and
   `Resource map` entries must remain separate contexts.

5. Build a boundary matrix, not only examples.
   Include must-fail and must-pass cases for same-line, wrapped-line,
   same-list-item, separate-list-item, separate-paragraph, fenced-example, and
   Resource-map boundaries.

6. Use contrast tests after every review fix.
   For CR3, one test should prove wrapped mixed references still fail for the
   unqualified path, and another should prove an independent artifact/example
   list item after a resource load remains safe.

7. Fix the narrow boundary that failed.
   CR3 should adjust instruction assembly and tests only. Do not use it as an
   opportunity to change resource-map verbs, `templates/` policy, generated
   parity, clean-install smoke, architecture normalization, or runtime fallback.

8. Before returning to code-review, run a counterexample sweep.
   Manually or with tests, exercise the nearest false-negative and
   false-positive neighbors of the fix. The question is: "what context did this
   fix broaden or narrow?"

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | process-follow-up | pending confirmation | Candidate validator/test guidance for classifier pipeline boundaries | Not yet confirmed | Three M2 findings show a recurring boundary-model gap, but learn alone should not update authoritative validator policy. |
| O2 | observation | observation | Current SRI-M2-CR3 review-resolution context | Code-review M2 R3 evidence | Explains why CR2 fixed one edge while creating another. |
| O3 | process-follow-up | pending confirmation | Candidate test-spec or validator fixture guidance for boundary-matrix tests | Not yet confirmed | The gap is reusable, but routing changes need contributor confirmation and an action-owning artifact. |
| O4 | observation | observation | Current SRI-M2-CR3 review-resolution scope | Active plan M2 scope and CR3 record | Keeps the next implementation narrowly scoped. |

Contributor confirmation status: explicit maintainer request confirms recording
this retrospective and best-practice answer. It does not by itself confirm
updating topic files, specs, skills, workflow docs, or validator policy.

## Route

No derivative routing performed.

Candidate follow-up, not routed here: after SRI-M2-CR3 is resolved, consider
whether `specs/skill-contract.test.md` or validator fixture evidence should
name a generic boundary-matrix rule for text classifiers that match multiple
entities in Markdown.

## No Durable Route Rationale

This session has repeated-review evidence and useful guidance, but the
authoritative immediate action already belongs to the open `SRI-M2-CR3`
review-resolution. Broader guidance about classifier pipelines or
boundary-matrix tests would affect action-owning artifacts and requires
contributor-confirmed routing before updating topic files, specs, skills, or
workflow policy.
