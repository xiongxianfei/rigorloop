# Review Artifact Recording

This topic is curated learn guidance. Authoritative review-recording rules remain in `CONSTITUTION.md`, `docs/workflows.md`, `specs/rigorloop-workflow.md`, review skills, active plans, and review artifact validators.

## 2026-05-20: Start Material Findings With Parser-Owned Fields

- Source session: `docs/learn/sessions/2026-05-20-review-artifact-field-shape.md`
- Primary classification: `durable-lesson`
- Secondary routes: none

Material findings are not only readable Markdown. They are parsed records.

When recording a material finding, create the machine-readable field block before adding explanatory prose:

```text
Finding ID:
Severity:
Location:
Evidence:
Required outcome:
Safe resolution path:
```

The root cause of the 2026-05-20 review artifact miss was source-shape substitution: the finding had the right human concepts, but they were written as prose bullets, so `review-log.md` and `review-resolution.md` referenced a Finding ID that the detailed review record did not expose as `Finding ID:`.

Best practice:

- draft from the exact field labels first;
- only then add narrative context;
- before linking a finding from `review-log.md` or `review-resolution.md`, confirm the detailed review record contains literal `Finding ID: <id>`;
- run `python scripts/validate-review-artifacts.py --mode structure docs/changes/<change-id>` while findings remain open.

Use closeout mode only when review-resolution is intentionally closed.