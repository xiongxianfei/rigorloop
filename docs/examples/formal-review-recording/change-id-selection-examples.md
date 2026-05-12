# Change ID Selection Examples

These examples illustrate the normative rule in `specs/formal-review-recording.md`. They are not active lifecycle state.

## Existing Change Root

Reviewed work already has:

```text
docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml
```

Use:

```text
2026-05-12-review-recording-guardrail-and-downstream-status-settlement
```

## Reviewed Artifact Metadata

Reviewed artifact:

```text
docs/plans/2026-05-12-review-recording-guardrail-and-downstream-status-settlement.md
```

The artifact points to:

```text
docs/changes/2026-05-12-review-recording-guardrail-and-downstream-status-settlement/change.yaml
```

Use that change ID.

## Generated Fallback

Reviewed artifact:

```text
docs/plans/2026-05-11-ui-shell-visual-coherence.md
```

No existing active change root or unambiguous metadata is available.

Generate:

```text
2026-05-11-ui-shell-visual-coherence-review-recording
```

## Ambiguous Candidates

If two active change roots plausibly match the reviewed work and neither the artifact nor the user identifies one, report:

```text
Recording status: blocked
```

Then state the smallest action needed to select or create the change root.
