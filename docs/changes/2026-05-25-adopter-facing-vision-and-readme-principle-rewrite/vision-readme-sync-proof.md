# Vision / README Sync Proof

## Source of truth

- Vision source: `VISION.md`
- README marker block: content between `<!-- vision:start -->` and `<!-- vision:end -->`
- README landing-page prose: public hook, Quick Start adjacency, workflow diagram, worked example, when-to-use guidance, and principle section outside the marker block

## Marker ownership

| README surface | Owner | Result |
| --- | --- | --- |
| Marker block | generated from `VISION.md` | updated as a concise reflection of the rewritten vision |
| Landing-page prose outside marker | `README.md`, constrained by `VISION.md` | updated manually and checked for consistency |
| Quick Start commands | current README / CLI adoption work | unchanged |

## Sync check

| Claim | Source in `VISION.md` | README reflection | Status |
| --- | --- | --- | --- |
| Traceable AI work | `Pitch`, `What makes this different`, `Traceable from idea to PR` | marker block, hook, workflow diagram, worked example | synced |
| Resumable work | `Pitch`, `Resumable across sessions and agents`, `What it commits to` | marker block, hook, principle section | synced |
| Reviewable artifacts | `Reviewable artifacts`, `What it commits to` | marker block, worked example, principle section | synced |
| Human-understandable AI work | `Human-understandable AI work`, `What it commits to` | principle section and public hook | synced |
| Learn / reliability | `Durable lessons` | principle section | synced |
| Vision boundary | `What it refuses to be`, `Who it is not for` | when-to-use / when-not-to-use and ownership sections | synced |

## Drift result

No independent README vision claim conflicts with `VISION.md`.

The public traceability chain now follows the repository workflow order:
proposal, proposal-review, spec, spec-review, plan, plan-review, test-spec,
implementation, code-review, explain-change, verify, and PR. The README worked
example lists plan before test spec to match the same order.

The README marker block remains bounded by exactly one marker pair. README
landing-page prose outside the marker block is manually authored and constrained
by `VISION.md`, but it is not treated as generated marker content.

## Command-source result

Exact Quick Start command examples were not changed. No command-source proof is
needed for this slice.
