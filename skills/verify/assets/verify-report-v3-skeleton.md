# Verify report: <change title>

> Inactive until the `stage-owned-change-local-v3` final-verification contract is activated.

## Result payload

```json final-verification-v3
{
  "protocol_version": 3,
  "outcome": "<pending | successful | failed | inconclusive | interrupted | stale>",
  "basis": {
    "repository_identity": "repo:sha256:<64 lowercase hex>",
    "remote_identity": "remote:sha256:<64 lowercase hex>",
    "base_branch": "<resolved branch>",
    "base_revision": "<immutable Git revision>",
    "merge_base_revision": "<immutable Git revision>",
    "head_branch": "<resolved branch>",
    "verified_subject_revision": "<immutable Git revision>",
    "governed_change_id": "<safe change ID>",
    "final_review_id": "<safe review ID>",
    "design_package_id": "<safe Design package ID>",
    "delivery_plan_id": "docs/plans/<plan>.md",
    "final_diff_sha256": "sha256:<64 lowercase hex>"
  },
  "basis_status": {
    "repository": "<current | stale | missing | conflicting | ambiguous>",
    "governed_change": "<status>",
    "verified_subject": "<status>",
    "final_review": "<status>",
    "design_package": "<status>",
    "delivery_plan": "<status>",
    "final_diff": "<status>"
  },
  "impact": [
    {
      "surface": "<closed impact surface>",
      "state": "<affected | unaffected | unknown>",
      "rationale": "<reason>",
      "affirmative_evidence": ["<required for unaffected>"]
    }
  ],
  "evidence": [
    {
      "evidence_id": "<safe ID>",
      "proved_surfaces": ["<classified surface>"],
      "freshness": "<always-current | fresh-required | impact-sensitive>",
      "existing_result": "<closed evidence result>",
      "authority_current": true,
      "identity_current": true,
      "environment_current": true,
      "conflicting": false,
      "new_obligation": false,
      "decision": "<reuse | rerun | newly-required>",
      "decision_rationale": "<reason>",
      "execution": "actual-run",
      "observed_result": "pass",
      "cache_hit": false,
      "proof": {
        "kind": "command",
        "command": ["<exact argv>"],
        "evidence_path": "<repository-relative path>",
        "evidence_sha256": "sha256:<64 lowercase hex>"
      }
    }
  ],
  "always_current": [
    {
      "check_id": "<one required always-current check ID>",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": {
        "kind": "command",
        "command": ["<exact argv>"],
        "evidence_path": "<repository-relative path>",
        "evidence_sha256": "sha256:<64 lowercase hex>"
      }
    }
  ],
  "ci_status": "<passed | failed | pending | unavailable | not-required>",
  "blockers": "<list>",
  "residual_risks": "<list>",
  "branch_ready": "<true only for a complete registered success>",
  "explanation": "<complete successful explanation object, otherwise null>"
}
```

## Lifecycle registration

- Selector: `lifecycle_cli.validations.verify-result`
- Evidence path: `docs/changes/<change-id>/verify-report.md`
- Evidence SHA-256: `<exact report content identity>`
- Verified subject revision: `<immutable Git revision>`
- Stage authority: `verify`
