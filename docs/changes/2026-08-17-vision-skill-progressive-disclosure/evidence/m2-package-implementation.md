# M2 Vision Package Implementation Evidence

## Scope

Milestone M2 separates the canonical vision skill into one compact universal contract, two conditional procedural references, and two structural assets. The focused validator also carries forward compatibility-sensitive package consumers.

## Implemented package

- `skills/vision/SKILL.md`: universal operations, state and authority checks, resource classification, all six assemblies, secondary actions, manifest and recovery contract, safety, stops, claims, and output obligations.
- `skills/vision/references/strategic-vision-authoring.md`: strategic positioning, content quality, drafting heuristics, and word limits.
- `skills/vision/references/readme-vision-sync.md`: marker inspection, insertion, bounded replacement, derivation, preservation, and idempotence.
- `skills/vision/assets/vision-skeleton.md`: canonical vision structure only.
- `skills/vision/assets/strategic-positioning-skeleton.md`: strategic rationale structure only.
- `scripts/test-skill-validator.py`: focused package, authority, assembly, action, manifest, retry, asset, compatibility, and measurement assertions.

## Behavioral proof

The focused scenarios prove:

- the exact three-operation model and six loaded assemblies;
- independent strategic and README resource selection;
- universal authority and claim boundaries remaining inline;
- pre-resolved skip, late resource loading, source-first writes, complete read-back, exact retry, and fail-closed resource handling;
- durable governed manifest preparation before the first target write and complete zero-write skip identity and claim evidence;
- structural assets containing no lifecycle or adequacy policy;
- compatibility-sensitive existing vision contract phrases remaining available across the loaded package.

No runtime router, synchronization script, parsed transaction schema, lifecycle state, or new authority owner was introduced.

## Procedural measurements

| Resource | Words | Bytes |
| --- | ---: | ---: |
| Flat baseline `SKILL.md` | 2,268 | 15,845 |
| Compact `SKILL.md` | 1,262 | 9,945 |
| Strategic reference | 492 | 3,659 |
| README reference | 303 | 2,131 |
| Largest loaded procedural assembly | 2,057 | 15,735 |

Every loaded procedural assembly is smaller than the flat baseline in both normalized words and raw bytes. Asset and total-package measurements remain M3 evidence because assets are copied structure rather than loaded procedure.

## Validation evidence

| Command | Result |
| --- | --- |
| `python scripts/validate-skills.py skills/vision/SKILL.md` | pass; one canonical skill validated |
| `python scripts/test-skill-validator.py VisionSkillProgressiveDisclosureTests` | pass; 6 tests |
| `python scripts/test-skill-validator.py` | pass; 408 tests, 16 skipped |
| `python scripts/test-build-skills.py` | pass; 7 tests |
| `python scripts/build-skills.py --check` | pass; temporary generated package validated |

## Review handoff

Review the canonical package and validator changes for universal-policy leakage, missing conditional procedure, unsafe skip behavior, policy-bearing assets, incomplete retry semantics, and compatibility drift. M3 package-chain proof remains out of scope for this milestone.
