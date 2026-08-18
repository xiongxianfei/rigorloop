# README vision synchronization

Load when README procedure or marker inspection is required. The parent skill owns operation, insertion or skip authority, manifest identity, target ordering, stops, and claims. This reference owns deterministic marker and derived-content mechanics.

## README Front-Matter

README front-matter is bounded by the exact marker pair:

```markdown
<!-- vision:start -->
<!-- vision:end -->
```

Generated content includes only the pitch, differentiator, target audience, and a link to `VISION.md` for goals, non-goals, and falsifiability. Derive it from `VISION.md`; never author it as an independent source of truth.

Classify marker state before replacement. One ordered, non-nested pair is valid. Missing, malformed, nested, or multiple vision marker pairs stop unless the parent operation has exact current insertion or skip authority. This is the same gate as existing guidance that says the user explicitly authorizes marker insertion or skipping README mirroring.

Automatic marker insertion is allowed only when creating the initial `VISION.md`. For authorized insertion with a Markdown H1, insert immediately after the first H1 block: the first `# <title>` line plus immediately following badge or image lines and attached blank lines. Without an H1, insert at the file start. Preserve existing content order.

When updating an existing `VISION.md` or syncing README, missing or malformed markers stop the skill before file modification unless exact current insertion or skip authority applies. If one valid block exists, replace only its interior and preserve every byte outside it. Do not edit outside content except an authorized insertion.

Before writing, derive intended front-matter from canonical vision, validate marker state and prior README identity, and revalidate them at the manifest commit boundary. Matching content is unchanged. Identical retry is idempotent and preserves outside bytes.

Report README front-matter as created, replaced, unchanged, skipped, or blocked. Never claim marker validity when the parent selected a pre-resolved skip without loading this reference.
