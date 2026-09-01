# Strategic vision authoring

Load only when `strategic_authoring_context` is true. The parent skill owns operation, authority, actions, manifests, writes, stops, and claims. This reference owns detailed strategic judgment and drafting procedure.

## Strategic Positioning

Before initial drafting or material repositioning, identify project category, primary user, primary pain, primary promise, core mechanism, alternatives, tradeoff, compatibility surfaces, refusals, and falsifiability. Write it to `docs/vision/strategic-positioning.md` as supporting rationale. `VISION.md` remains canonical; rationale never overrides it.

For editorial updates, README-only sync, or narrow edits, do not update rationale unless strategic assumptions changed or a conflict was found. For substantive repositioning in a governed repository, require the successful final Verify report to summarize the delta and link the rationale path.

Treat repository layout, Git, CI, pull requests, runtime, package format, hosting platform, language, and template mechanics as compatibility surfaces unless genuinely the product.

For a methodology, workflow, protocol, or operating model, use methodology-as-product framing: pillars or operating loop are identity. Add one optional methodology-oriented section only from concrete inputs; otherwise report an open question.

Use fixture-style checks: RigorLoop-style inputs lead with an AI-agent software engineering workflow or methodology and avoid `Git-first starter kit` as category; a Windows-native file manager leads with the file-manager category; a Git extension may lead with Git because Git is the product category.

## Vision Content

Root `VISION.md` should normally stay at or under 750 words. Methodology-like vision may exceed that only with explicit owner permission for category, pillars, tradeoff, refusals, or falsifiability. It MUST NOT exceed 900 words.

Use plain language and do not use `MUST`, `SHOULD`, or `MAY` as requirements vocabulary in vision text. Do not include feature lists, implementation details, architecture diagrams, status fields, decision logs, stakeholder tables, or priority columns. Use plain Markdown understandable without rendered tables, diagrams, HTML layout, or generated assets.

The standard structure covers pitch, what makes this different, who it is for, who it is not for, commitments, refusals, falsifiability, and open questions only when vision-level uncertainty remains.

## Drafting Heuristics

Use these as authoring checks, not additional `VISION.md` sections:

- Differentiator: name an alternative class or specific tool and the tradeoff; this does not require naming a specific competitor.
- Pain points: embed pain points in the differentiator rather than add a complaint list.
- Commitments: make them concrete and checkable.
- Falsifiability: use observable failure conditions.
- Audience: rule out at least one plausible non-fit.
- Refusals: make them concrete enough to block misaligned proposals.
- Category: do not mistake a compatibility surface for project identity.

Before completion, check that the first sentence names the highest-level category; the differentiator includes a tradeoff; the core mechanism appears when essential; compatibility surfaces are not the main identity; audience non-fit is visible; commitments are checkable; refusals block tempting scope creep; falsifiability is observable; and the vision can guide proposal-fit review without chat history.

For initial or materially repositioned visions, return a concise strategic-positioning summary and rationale path. Do not grant write authority or settle the parent operation from this reference.
