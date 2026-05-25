# Documentation Prose

This topic is curated learn guidance. Authoritative documentation contracts
remain in `VISION.md`, README marker-sync rules, accepted proposals, active
plans, workflow docs, and validator scripts.

## 2026-05-25: Use Semantic Line Breaks For Review-Critical Prose

- Source session: `docs/learn/sessions/2026-05-25-documentation-prose-line-wrapping.md`
- Primary classification: `durable-lesson`
- Secondary routes: none

For human-authored documentation prose, optimize source line breaks for review,
not just rendered Markdown.

Prefer semantic line breaks for adopter-facing, source-of-truth, or
review-critical prose:

- one sentence per line when practical;
- one natural clause per line for long sentences;
- keep paired phrases together, such as `AI agents`, `proposal to spec`, and
  `reviewable in Git`;
- avoid splitting lifecycle chains at confusing points;
- use bullets, tables, or diagrams when dense chains become hard to scan in
  source form.

The line-wrapping issue in the adopter-facing vision/README rewrite came from
hard wrapping prose around a column width. That made the rendered Markdown fine
but the source awkward to review, especially around lifecycle chains and value
propositions.

Hard wrapping is not forbidden. It is the wrong default when line breaks split
meaningful phrases, obscure lifecycle order, or make public positioning copy
harder to review.
