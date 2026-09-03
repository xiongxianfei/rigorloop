# Verify report

Subject path: docs/plans/2026-09-03-relax-pr-evidence-tail.md
Subject identity: sha256:9b762060e3022f6d0310ad8197ff363c92228c3bb89ff3d92d59935541bf4494
Validation result: passed

```json final-verification-v3
{
  "always_current": [
    {
      "check_id": "current-change-and-repository-identity",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["git", "status", "--porcelain=v1", "--untracked-files=all"], "evidence_path": "docs/plans/2026-09-03-relax-pr-evidence-tail.md", "evidence_sha256": "sha256:9b762060e3022f6d0310ad8197ff363c92228c3bb89ff3d92d59935541bf4494", "kind": "command" }
    },
    {
      "check_id": "reviewed-subject-and-review-identity",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["git", "rev-parse", "9ade638ae857c2952b8748cc20333aa238e6052f"], "evidence_path": "docs/changes/2026-09-03-relax-pr-evidence-tail/reviews/code-review-final-r2.md", "evidence_sha256": "sha256:da63d1334ac6234472c3b4a1dacc9fd39963c8b02150d1793579e7c4fd272ec4", "kind": "command" }
    },
    {
      "check_id": "lifecycle-and-package-consistency",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["node", "packages/rigorloop/dist/bin/rigorloop.js", "lifecycle", "validate", "--change", "2026-09-03-relax-pr-evidence-tail", "--format", "json"], "evidence_path": "docs/plans/2026-09-03-relax-pr-evidence-tail.md", "evidence_sha256": "sha256:9b762060e3022f6d0310ad8197ff363c92228c3bb89ff3d92d59935541bf4494", "kind": "command" }
    },
    {
      "check_id": "review-closeout",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["python", "scripts/validate-review-artifacts.py", "--mode", "closeout", "docs/changes/2026-09-03-relax-pr-evidence-tail"], "evidence_path": "docs/changes/2026-09-03-relax-pr-evidence-tail/review-resolution.md", "evidence_sha256": "sha256:43beb8d961db2d380ecc5b99c1dcf53da9cd68df8a19d10debcba3ff98476215", "kind": "command" }
    },
    {
      "check_id": "unresolved-blocker-state",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["node", "packages/rigorloop/dist/bin/rigorloop.js", "workflow-context", "--change", "2026-09-03-relax-pr-evidence-tail", "--format", "json"], "evidence_path": "docs/changes/2026-09-03-relax-pr-evidence-tail/review-log.md", "evidence_sha256": "sha256:d018683948b46700a9586a3ba49f27bf33284fac613e14ebc70c6734007bcce0", "kind": "command" }
    },
    {
      "check_id": "final-diff-classification",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["git", "diff", "--binary", "92c0d5a82ed86d918689c59eb922e676a94d68eb..9ade638ae857c2952b8748cc20333aa238e6052f"], "evidence_path": "docs/changes/2026-09-03-relax-pr-evidence-tail/reviews/code-review-final-r2.md", "evidence_sha256": "sha256:da63d1334ac6234472c3b4a1dacc9fd39963c8b02150d1793579e7c4fd272ec4", "kind": "command" }
    },
    {
      "check_id": "required-artifact-and-evidence-existence",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["bash", "scripts/ci.sh", "--mode", "broad-smoke"], "evidence_path": "docs/changes/2026-09-03-relax-pr-evidence-tail/evidence/m2-adapter-parity.md", "evidence_sha256": "sha256:12c224e7c290d23aa30795ebad572313bb95414eb1d21756d03a7f663835b3a6", "kind": "command" }
    },
    {
      "check_id": "complete-verify-result-consistency",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["node", "--test", "packages/rigorloop/test/final-verification-protocol.test.js"], "evidence_path": "packages/rigorloop/test/final-verification-protocol.test.js", "evidence_sha256": "sha256:d1461da2b7063d722f5cf488fef3df120726d7fb01da40a2cf8a7d7f422f6af0", "kind": "command" }
    }
  ],
  "basis": {
    "base_branch": "main",
    "base_revision": "92c0d5a82ed86d918689c59eb922e676a94d68eb",
    "delivery_plan_id": "docs/plans/2026-09-03-relax-pr-evidence-tail.md",
    "design_package_id": "design-review-r1",
    "final_diff_sha256": "sha256:2253a2435652fb317b454f2311348ffcc33e271b5ca7c8c07ced94756e3cd886",
    "final_review_id": "code-review-final-r2",
    "governed_change_id": "2026-09-03-relax-pr-evidence-tail",
    "head_branch": "proposal/relax-pr-evidence-tail",
    "merge_base_revision": "92c0d5a82ed86d918689c59eb922e676a94d68eb",
    "remote_identity": "remote:sha256:865a587cf0280059126415338ada6a5ffff6c1546820b32a244c9f5560d9b44d",
    "repository_identity": "repo:sha256:68a102e8bfeda960778979cb352c515c329366043408fc2c2e0eb35ecce57f9d",
    "verified_subject_revision": "9ade638ae857c2952b8748cc20333aa238e6052f"
  },
  "basis_status": {
    "delivery_plan": "current",
    "design_package": "current",
    "final_diff": "current",
    "final_review": "current",
    "governed_change": "current",
    "repository": "current",
    "verified_subject": "current"
  },
  "blockers": [],
  "branch_ready": true,
  "ci_status": "not-required",
  "evidence": [
    {
      "authority_current": true, "cache_hit": false, "conflicting": false,
      "decision": "rerun", "decision_rationale": "The final change alters the public PR readiness predicate and its authority boundary, so the complete repository smoke was rerun after the exact final review was corrected and registered.",
      "environment_current": true, "evidence_id": "TG-FINAL-01", "execution": "actual-run", "existing_result": "pass", "freshness": "fresh-required", "identity_current": true, "new_obligation": false, "observed_result": "pass",
      "proof": { "command": ["bash", "scripts/ci.sh", "--mode", "broad-smoke"], "evidence_path": "docs/changes/2026-09-03-relax-pr-evidence-tail/evidence/m1-proportional-pr-contract.md", "evidence_sha256": "sha256:283e8cb29bd5f82fbc671c9967a496af65ff3b40e5bf170142759a65102fb99a", "kind": "command" },
      "proved_surfaces": ["runtime-behavior", "public-api", "state-or-persistence", "migration", "security-or-authority", "documentation", "lifecycle-governance", "external-environment"]
    },
    {
      "authority_current": true, "cache_hit": false, "conflicting": false,
      "decision": "rerun", "decision_rationale": "Canonical skill bytes affect supported adapter archives and current candidate identities, so final broad smoke reran the complete generation, package, metadata, and compatibility chain.",
      "environment_current": true, "evidence_id": "TG-FINAL-02", "execution": "actual-run", "existing_result": "pass", "freshness": "fresh-required", "identity_current": true, "new_obligation": false, "observed_result": "pass",
      "proof": { "command": ["bash", "scripts/ci.sh", "--mode", "broad-smoke"], "evidence_path": "docs/changes/2026-09-03-relax-pr-evidence-tail/evidence/m2-adapter-parity.md", "evidence_sha256": "sha256:12c224e7c290d23aa30795ebad572313bb95414eb1d21756d03a7f663835b3a6", "kind": "command" },
      "proved_surfaces": ["build", "packaging", "generated-output", "documentation", "repository-metadata", "dependencies"]
    }
  ],
  "explanation": {
    "important_choices": ["Classify the complete post-review suffix as none, evidence-only, or invalidating instead of enforcing an exact commit count or direct-parent topology.", "Permit evidence-only continuation only for current, attributable final-review, workflow, and Verify evidence; paths, filenames, messages, authors, and stage labels grant no authority.", "Keep the verified product subject fixed and compare the cumulative final product diff, so any protected, mixed, stale, cross-change, unknown, or non-ancestor drift blocks before external mutation.", "Keep Verify's successful result registration narrower and exact: the report plus its lifecycle registration; broader review and workflow evidence are inputs consumed by PR readiness.", "Preserve the existing remote identity, PR selection, push, hosted-CI, retry, draft, refresh, read-back, and lifecycle-ownership safeguards while refreshing only current unpublished adapter identities."],
    "limitations": ["The classifier remains instruction-driven and therefore depends on correct identification of governed authority and mixed content.", "Hosted CI, remote push, PR creation, release publication, and external archive download were not performed or claimed."],
    "requirements_and_design": "R1 through R24 are realized through approved Design package design-review-r1 and the M1-M2 allocation in the approved Delivery plan, including all eight boundary dimensions and INT-001 through INT-004.",
    "residual_risks": ["A future evidence type that is not covered by the closed categories must block until the governing contract is deliberately extended.", "Current unpublished adapter checksum updates are coherent locally, but publication remains a separate externally observed operation."],
    "supporting_evidence": ["TG-FINAL-01", "TG-FINAL-02", "skill-validator: 365 passed", "canonical skill validation: 20 passed", "adapter distribution: 157 passed", "validation selection: 154 passed", "npm package: 373 passed and 2 intentional skips", "final broad-smoke: 12 checks passed in 663 seconds", "final-verification protocol: 10 passed"],
    "what_changed": "RigorLoop now permits a reviewed subject to precede PR handoff by any number of commits and with any direct-parent topology only when the entire cumulative suffix is current, attributable final-review, workflow, and Verify evidence. The public contract, focused regressions, coupled Verify wording, supported adapter candidates, and current unpublished v0.5.1 metadata are synchronized.",
    "why": "The former one-direct-child rule was a stricter topology proxy than the safety property required. The refined contract optimizes for preventing unreviewed product drift while allowing legitimate evidence recording and lifecycle bookkeeping to accumulate without artificial squashing or repeated review solely because of commit shape."
  },
  "impact": [
    { "affirmative_evidence": [], "rationale": "Published PR and coupled Verify instructions change agent readiness behavior.", "state": "affected", "surface": "runtime-behavior" },
    { "affirmative_evidence": [], "rationale": "The public PR skill contract changes from exact direct-child topology to a closed cumulative-suffix classification.", "state": "affected", "surface": "public-api" },
    { "affirmative_evidence": ["No lifecycle schema, stored field, persistence format, or runtime state transition differs from base.", "Lifecycle validation and the final 12-check broad smoke passed against the existing state model."], "rationale": "The change interprets existing Git and lifecycle evidence without adding or changing persisted state.", "state": "unaffected", "surface": "state-or-persistence" },
    { "affirmative_evidence": [], "rationale": "Current PR handoffs adopt the proportional classifier while historical reviews, reports, releases, and merged PRs remain unchanged.", "state": "affected", "surface": "migration" },
    { "affirmative_evidence": ["No dependency manifest or lockfile differs from base.", "The final 12-check broad smoke passed without dependency installation changes."], "rationale": "No runtime, build, or package dependency version or graph changes.", "state": "unaffected", "surface": "dependencies" },
    { "affirmative_evidence": [], "rationale": "Canonical validation and adapter generation now assert and carry the proportional suffix contract.", "state": "affected", "surface": "build" },
    { "affirmative_evidence": [], "rationale": "Codex, Claude Code, and opencode candidates contain the revised PR and Verify wording.", "state": "affected", "surface": "packaging" },
    { "affirmative_evidence": [], "rationale": "Current candidate archive, tree, size, bundled metadata, and exact fixture identities change deterministically.", "state": "affected", "surface": "generated-output" },
    { "affirmative_evidence": [], "rationale": "Readiness authority is now based on current attributable content rather than commit shape or untrusted metadata, with fail-closed invalidation for product drift.", "state": "affected", "surface": "security-or-authority" },
    { "affirmative_evidence": [], "rationale": "Canonical skills, references, focused specification, architecture, plan, reviews, and change-local evidence document the revised rule.", "state": "affected", "surface": "documentation" },
    { "affirmative_evidence": [], "rationale": "Only current unpublished v0.5.1 adapter metadata and its trusted release-index identity are synchronized to regenerated candidates.", "state": "affected", "surface": "repository-metadata" },
    { "affirmative_evidence": [], "rationale": "PR consumes a broader evidence suffix while Verify keeps exact result registration and sole branch-readiness authority; no stage or transition is added.", "state": "affected", "surface": "lifecycle-governance" },
    { "affirmative_evidence": ["No new network call, remote mutation, environment variable, host requirement, or publication action was introduced.", "Existing remote identity, PR selection, push, CI, retry, and read-back clauses are covered by the 365-test skill validator and final broad smoke."], "rationale": "The external-operation contract is preserved; only the local pre-mutation readiness classifier changes.", "state": "unaffected", "surface": "external-environment" }
  ],
  "outcome": "successful",
  "protocol_version": 3,
  "residual_risks": ["The content classifier is intentionally strict about unknown or mixed evidence, but correct classification still depends on current governed identities being available and interpreted accurately."]
}
```
