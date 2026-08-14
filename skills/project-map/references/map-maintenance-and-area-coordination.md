# Map maintenance and area coordination

Use this procedure only after `SKILL.md` selects `PMA1-maintenance-or-coordinated`. It specializes maintenance and coordination; it does not redefine universal evidence meanings, source ranking, command authority, map statuses, stops, claims, downstream ownership, or skeleton structure.

## Refresh procedure

Perform refresh trigger comparison between the recorded baseline and current evidence. Relevant triggers include changed top-level or package boundaries, runtime entry points, public interfaces, service calls, storage or schema surfaces, manifests, tests or commands, CI/release/deployment/infrastructure configuration, generated-source ownership, ownership boundaries, external integrations, and cited files whose change affects a conclusion. Unrelated changes do not make every map stale.

Use previous and current baseline evidence for changed-path targeting and affected-section selection. Reinspect affected claims and their dependencies, preserve unaffected supported content, update freshness metadata, and validate the complete result. A full rewrite remains a refresh strategy.

When the earlier map was wrong at its recorded baseline, add a correction note naming the affected section, corrected claim, and evidence path. A correction note does not create a fourth map status.

## Audit procedure

Audit resolves the target and current evidence, compares the baseline and cited surfaces, and reports current, partial, stale, contradictory, or `missing-map` findings without writing. Audit never repairs a map. A correction begins a separately classified refresh with freshly resolved evidence.

## Root and area coordination

The root remains the entry point and owns root registration. Each area map names its parent. The root summarizes each registered area's scope, baseline, freshness, and known gaps by filling the skeleton-owned registration table.

For overlapping maps, name the overlap, record overlap ownership for detail, and link from the other map rather than duplicating it. A contradiction, missing area, orphaned area, dangling registration, or ambiguous parent blocks clean maintenance; audit may report it without mutation.

## Area creation transaction

Area creation requires one existing structurally valid root map and never creates the root implicitly. A missing root stops and routes to repository root creation; area creation must be requested again after the root exists.

Before writing, bind the root path and content identity, area slug and normalized path, area parent/root identity, current evidence baseline, and expected root registration row. Confirm both the area target and registration are absent.

Use this order:

1. Resolve and validate the root identity and current registration state.
2. Prepare and validate complete area-map content.
3. Write the area map first.
4. Re-read the root and confirm its identity and relevant registration state are unchanged.
5. Write the exact root registration last as the transaction commit point.
6. Validate both artifacts and their reciprocal identities.

## Interrupted coordination and retry

An identical retry may complete only a missing registration when the existing area file and complete original transaction identities match. Revalidate the area before registration.

When both artifacts already match, return idempotent success without another write. A dangling registration, conflicting path or parent, changed root identity, multiple candidate files or rows, stale basis, or ambiguous state stops without overwrite. The skill must not adopt an area file whose identity or evidence basis differs.

Audit may identify partial transaction states but remains read-only. Repair requires a newly resolved refresh or other explicit correction authority.
