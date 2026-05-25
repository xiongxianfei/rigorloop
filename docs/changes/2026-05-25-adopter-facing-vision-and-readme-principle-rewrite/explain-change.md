# Explain Change

## Summary

This change rewrites RigorLoop's durable vision and README landing surface so a
new adopter sees the user benefit first: AI-assisted software work remains
traceable, resumable, and reviewable in Git after the chat session ends.

It keeps `VISION.md` as the source of truth, updates the README marker block and
landing-page prose to reflect that vision, adds a Mermaid traceability chain,
keeps honest when-to-use / when-not-to-use guidance, and records proof for sync,
cold-read comprehension, behavior preservation, and review closeout.

## Problem

The prior public story used accurate internal principles but led with internal
mechanism language. A cold reader could see proposals, specs, plans, tests, and
review gates, but the README and vision did not make the adopter-facing value
plain quickly enough: why RigorLoop is different from using an AI coding agent
directly.

The accepted proposal reframed the durable public story as:

```text
AI coding agents produce output fast, but reasoning often vanishes.
RigorLoop turns that work into traceable, resumable, reviewable artifacts in Git.
```

## Decision Trail

| Decision | Source | Result |
| --- | --- | --- |
| Rewrite `VISION.md` first, then synchronize README public positioning from it. | Accepted proposal, proposal-review-r1 | `VISION.md` now leads with the adopter problem and durable value proposition. |
| Keep README marker content separate from landing-page prose. | Proposal README ownership boundary and plan context | `vision-readme-sync-proof.md` records marker-owned and manually-authored README surfaces. |
| Do not add a separate spec or test spec for this documentation/source-of-truth slice. | Maintainer decision in `review-resolution.md` for `VRP-PLAN1` | Plan uses proposal checks and proof artifacts instead. |
| Show the traceability chain visually and caption it as the full chain for complete delivery. | Proposal `VRP-005`, `VRP-019`, `AC-VRP-019` | README includes a Mermaid diagram and isolated-skill caption. |
| Put plan before test spec in public workflow copy. | Maintainer learning request and learn artifacts | README and `VISION.md` use proposal, spec, plan, test spec order. |
| Accept branch-specific cold-read evidence for M1. | Maintainer decision closing `VRP-CR-M1-F1` | `cold-read-review.md` records the accepted evidence and result fields. |
| Keep this as a stacked branch. | Maintainer decision closing `VRP-CR-M1-F2` | `behavior-preservation.md` scopes the no-runtime-change proof to M1 commits. |

## Diff Rationale By Area

| File or area | Change | Reason | Evidence |
| --- | --- | --- | --- |
| `VISION.md` | Rewrote pitch, differentiator, principles, audience, refusals, and falsifiability around adopter benefit. | Make the durable why readable to external adopters while preserving source-of-truth role. | Proposal `AC-VRP-001` through `AC-VRP-003`; sync proof. |
| `README.md` marker block | Updated concise marker-owned front matter from `VISION.md`. | Keep README vision content synchronized with the canonical vision. | `validate-readme.py README.md --vision-markers`; sync proof. |
| `README.md` landing prose | Added first-screen hook, short problem framing, Mermaid workflow diagram, worked example, and benefit-first principles. | Pass the three-second comprehension test and make traceability the public spine. | Cold-read evidence and code-review-m1-r3. |
| `README.md` when-to-use section | Preserved honest use / non-use guidance below the visual and worked example. | Avoid overmarketing and keep trust signal. | Proposal `AC-VRP-007`; cold-read result. |
| `vision-readme-sync-proof.md` | Added marker/prose ownership and claim-level sync check. | Prove README does not fork `VISION.md`. | Review artifacts validate structurally. |
| `cold-read-review.md` | Recorded accepted branch-specific cold-read evidence. | Prove a reviewer could identify value proposition, audience, first action, traceability chain, and learn framing. | `VRP-CR-M1-F1` closed. |
| `behavior-preservation.md` | Recorded scoped no-runtime-change proof and branch stacking boundary. | Preserve non-goals while keeping the published stacked branch intact by owner decision. | `VRP-CR-M1-F2` closed. |
| Review records and resolution | Recorded proposal review, plan review, code-review findings, owner decisions, and clean code-review rerun. | Keep formal lifecycle evidence durable. | Review artifact validation passes. |
| Plan and plan index | Tracked M1 state through implementation, findings, closeout, and next stage. | Keep lifecycle handoff current. | Lifecycle validation passes. |
| Learn artifacts | Captured the public-framing lesson that plan comes after spec and before test spec. | Prevent future public docs from confusing readers about workflow order. | `docs/learn/sessions/2026-05-25-plan-before-test-spec-public-framing.md`; topic guidance. |

## Tests Added Or Changed

No runtime tests were added or changed for this scoped M1 slice. The maintainer
explicitly decided that this documentation/source-of-truth rewrite does not need
a separate spec or test spec. The proof map is the accepted proposal checks,
manual evidence artifacts, README marker validation, lifecycle validation, review
artifact validation, metadata validation, and patch hygiene.

## Validation Evidence Available Before Final Verify

Validation run before this explain-change stage:

- `python scripts/validate-readme.py README.md --vision-markers`: passed
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite`: passed
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite`: passed
- `python scripts/validate-change-metadata.py docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml`: passed
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/change.yaml --path docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md --path docs/plan.md`: passed
- `git diff --check --`: passed

Final verification has not run yet.

## Review Resolution Summary

`review-resolution.md` is closed.

| Finding | Disposition | Result |
| --- | --- | --- |
| `VRP-PLAN1` | rejected | Maintainer decided no separate test spec is needed for this docs/source-of-truth change. |
| `VRP-CR-M1-F1` | accepted | Branch-specific cold-read evidence was accepted and recorded. |
| `VRP-CR-M1-F2` | accepted | Branch remains stacked; behavior-preservation proof is scoped to M1 commits. |

Code-review-m1-r3 recorded `clean-with-notes` and closed M1.

## Alternatives Rejected

- README-only rewrite: rejected because it would risk drift from `VISION.md`.
- New README generation tooling: rejected because the existing marker contract is
  enough for this slice.
- Fabricated worked example: rejected because the proposal requires real,
  public-suitable evidence or an honest follow-up.
- Clean branch recreation after `VRP-CR-M1-F2`: rejected by maintainer direction;
  the branch remains stacked and the proof boundary is recorded instead.

## Scope Control

This scoped M1 slice does not redefine workflow semantics, lifecycle stage
order, CLI behavior, skill behavior, adapter output, validators, release
process, npm behavior, or generated package output. The published branch remains
stacked on other work by maintainer decision, so branch-level review must account
for that base/merge-order boundary.

## Risks And Follow-Ups

- The branch remains stacked. Reviewers should use the intended stacked base or
  merge order when evaluating non-M1 files.
- Trust and reliability claims remain falsifiable goals. Continued cold-read or
  adoption evidence should refine them.
- A stronger public worked example can still be curated as follow-on adoption
  work.

## Readiness

Explain-change is complete for this slice. The next lifecycle stage is `verify`.
