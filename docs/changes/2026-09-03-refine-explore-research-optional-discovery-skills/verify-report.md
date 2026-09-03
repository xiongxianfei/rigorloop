# Verify report

```json final-verification-v3
{
  "always_current": [
    {
      "check_id": "current-change-and-repository-identity",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["git", "status", "--porcelain=v1", "--untracked-files=all"], "evidence_path": "docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md", "evidence_sha256": "sha256:24f3acd041bdd46b56a5a45007f71ee38d9244d4ed07f48d2317718484d3c3fb", "kind": "command" }
    },
    {
      "check_id": "reviewed-subject-and-review-identity",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["git", "rev-parse", "5b51a5bdbdd4ae4a453e21c829bf3c20d0f3baf8"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/reviews/code-review-final-r1.md", "evidence_sha256": "sha256:2db79add3cea19d1504d03aeaf6a517efb6327a5c645f878fa738a5dcf147320", "kind": "command" }
    },
    {
      "check_id": "lifecycle-and-package-consistency",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["node", "packages/rigorloop/dist/bin/rigorloop.js", "lifecycle", "validate", "--change", "2026-09-03-refine-explore-research-optional-discovery-skills", "--format", "json"], "evidence_path": "docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md", "evidence_sha256": "sha256:24f3acd041bdd46b56a5a45007f71ee38d9244d4ed07f48d2317718484d3c3fb", "kind": "command" }
    },
    {
      "check_id": "review-closeout",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["python", "scripts/validate-review-artifacts.py", "--mode", "closeout", "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-resolution.md", "evidence_sha256": "sha256:6078bc3896a93c0b40f03f30c654b8433a571e5a8f979e1f42dc2dcce562f67b", "kind": "command" }
    },
    {
      "check_id": "unresolved-blocker-state",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["node", "packages/rigorloop/dist/bin/rigorloop.js", "workflow-context", "--change", "2026-09-03-refine-explore-research-optional-discovery-skills", "--format", "json"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-log.md", "evidence_sha256": "sha256:8fa49b5d7492c7867397cb91125b4f577f9ddf428763c607841f2fd5aa7d328f", "kind": "command" }
    },
    {
      "check_id": "final-diff-classification",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["git", "diff", "--binary", "7eec69b08d1de2390db084570e545328335b0be6..5b51a5bdbdd4ae4a453e21c829bf3c20d0f3baf8"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/reviews/code-review-final-r1.md", "evidence_sha256": "sha256:2db79add3cea19d1504d03aeaf6a517efb6327a5c645f878fa738a5dcf147320", "kind": "command" }
    },
    {
      "check_id": "required-artifact-and-evidence-existence",
      "execution": "actual-run",
      "observed_result": "pass",
      "proof": { "command": ["bash", "scripts/ci.sh", "--mode", "broad-smoke"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m3-adapter-parity.md", "evidence_sha256": "sha256:aeee39c58ddb4c53946d3449f1436f050f0ca3750c3808846c61427d1079f6b2", "kind": "command" }
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
    "base_revision": "7eec69b08d1de2390db084570e545328335b0be6",
    "delivery_plan_id": "docs/plans/2026-09-03-refine-explore-research-optional-discovery-skills.md",
    "design_package_id": "design-review-r2",
    "final_diff_sha256": "sha256:57ce38e26f17b68c3249eb34a2d307e428904ebd67b587b414eaf196e434e929",
    "final_review_id": "code-review-final-r1",
    "governed_change_id": "2026-09-03-refine-explore-research-optional-discovery-skills",
    "head_branch": "proposal/refine-explore-research-discovery",
    "merge_base_revision": "7eec69b08d1de2390db084570e545328335b0be6",
    "remote_identity": "remote:sha256:865a587cf0280059126415338ada6a5ffff6c1546820b32a244c9f5560d9b44d",
    "repository_identity": "repo:sha256:68a102e8bfeda960778979cb352c515c329366043408fc2c2e0eb35ecce57f9d",
    "verified_subject_revision": "5b51a5bdbdd4ae4a453e21c829bf3c20d0f3baf8"
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
      "decision": "rerun", "decision_rationale": "The final change alters both public discovery contracts, their routing semantics, and stage-authority guidance, so the complete repository smoke was rerun at final Verify.",
      "environment_current": true, "evidence_id": "TG-FINAL-01", "execution": "actual-run", "existing_result": "pass", "freshness": "fresh-required", "identity_current": true, "new_obligation": false, "observed_result": "pass",
      "proof": { "command": ["bash", "scripts/ci.sh", "--mode", "broad-smoke"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m2-routing-and-guidance.md", "evidence_sha256": "sha256:5e7cdbb622f16e7b012e001619fad412b7d1ac91611d73ef4c0bf12c998f2155", "kind": "command" },
      "proved_surfaces": ["runtime-behavior", "public-api", "state-or-persistence", "security-or-authority", "documentation", "lifecycle-governance", "external-environment"]
    },
    {
      "authority_current": true, "cache_hit": false, "conflicting": false,
      "decision": "rerun", "decision_rationale": "New package resources affect skill generation, archive inventory, clean installation, and current candidate metadata; final broad smoke reran the complete generated-output chain.",
      "environment_current": true, "evidence_id": "TG-FINAL-02", "execution": "actual-run", "existing_result": "pass", "freshness": "fresh-required", "identity_current": true, "new_obligation": false, "observed_result": "pass",
      "proof": { "command": ["bash", "scripts/ci.sh", "--mode", "broad-smoke"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m3-adapter-parity.md", "evidence_sha256": "sha256:aeee39c58ddb4c53946d3449f1436f050f0ca3750c3808846c61427d1079f6b2", "kind": "command" },
      "proved_surfaces": ["build", "packaging", "generated-output", "documentation", "repository-metadata", "dependencies"]
    },
    {
      "authority_current": true, "cache_hit": false, "conflicting": false,
      "decision": "rerun", "decision_rationale": "Compatibility and recovery cross canonical skills, validators, lifecycle evidence, adapters, npm metadata, and historical records, so final broad smoke was required after final review registration.",
      "environment_current": true, "evidence_id": "TG-FINAL-03", "execution": "actual-run", "existing_result": "pass", "freshness": "fresh-required", "identity_current": true, "new_obligation": false, "observed_result": "pass",
      "proof": { "command": ["bash", "scripts/ci.sh", "--mode", "broad-smoke"], "evidence_path": "docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m3-adapter-parity.md", "evidence_sha256": "sha256:aeee39c58ddb4c53946d3449f1436f050f0ca3750c3808846c61427d1079f6b2", "kind": "command" },
      "proved_surfaces": ["runtime-behavior", "public-api", "state-or-persistence", "migration", "build", "packaging", "generated-output", "security-or-authority", "repository-metadata", "lifecycle-governance", "external-environment"]
    }
  ],
  "explanation": {
    "important_choices": ["Explore and Research remain separate public skills with one central question each.", "Explicit invocations create concise standalone artifacts, while incidental stage-local reasoning remains artifact-free.", "A small canonical discovery-support block is copied into both self-contained packages and guarded by fail-closed byte-parity validation.", "Route selects Explore, Research, both, or neither, but only the named owning stage can adopt a conclusion.", "Existing generic adapter generation is reused; only the current unpublished v0.5.1 candidate identity changed when its generated resource inventory grew."],
    "limitations": ["The change does not guarantee higher invocation frequency; low usage remains acceptable when uncertainty does not warrant discovery work.", "Hosted CI, release publication, external archive download, and post-adoption usage metrics were not observed or claimed."],
    "requirements_and_design": "ER-R1 through ER-R38 are realized through approved Design package design-review-r2 and the M1-M3 allocation in the approved Delivery plan, including all eight boundary dimensions and INT-001 through INT-005.",
    "residual_risks": ["The skills remain judgment-driven, so weak routing judgment can still underuse or overuse discovery despite the clearer contract.", "Standalone artifacts add documentation when explicitly invoked; concise skeletons and stopping rules limit that cost."],
    "supporting_evidence": ["TG-FINAL-01", "TG-FINAL-02", "TG-FINAL-03", "skill-validator: 362 passed", "validation-selection: 154 passed", "adapter distribution: 157 passed", "npm package: 373 passed and 2 intentional skips", "final broad-smoke: 12 checks passed in 674 seconds"],
    "what_changed": "RigorLoop now defines Explore as proportional option discovery and Research as bounded evidence-based uncertainty reduction. Both produce standalone Git-tracked support artifacts only when explicitly invoked, carry no approval or lifecycle authority, hand conclusions to a named owner, use focused progressive-disclosure resources, and ship coherently through Codex, Claude Code, and opencode adapters.",
    "why": "The former skills overlapped in purpose and output, imposed avoidable procedural weight, and made artifact authority unclear. The refined model keeps the valuable divergent and convergent reasoning modes while making selection, stopping, artifact placement, and downstream adoption explicit."
  },
  "impact": [
    { "affirmative_evidence": [], "rationale": "Published Explore, Research, and Route instructions change agent execution behavior.", "state": "affected", "surface": "runtime-behavior" },
    { "affirmative_evidence": [], "rationale": "Public skill contracts, default artifact paths, and invocation outcomes change.", "state": "affected", "surface": "public-api" },
    { "affirmative_evidence": [], "rationale": "Explicit invocations now create or exactly revise standalone support artifacts under separate roots.", "state": "affected", "surface": "state-or-persistence" },
    { "affirmative_evidence": [], "rationale": "Current invocations adopt the refined contract while prior artifacts and release archives remain readable and unchanged.", "state": "affected", "surface": "migration" },
    { "affirmative_evidence": ["No dependency manifest or lockfile differs from base.", "The final 12-check broad smoke passed without dependency installation changes."], "rationale": "No runtime, build, or package dependency version or graph changes.", "state": "unaffected", "surface": "dependencies" },
    { "affirmative_evidence": [], "rationale": "Canonical skill validation and generation now carry eight new mapped resources.", "state": "affected", "surface": "build" },
    { "affirmative_evidence": [], "rationale": "All supported adapter packages gain the new Explore and Research resources.", "state": "affected", "surface": "packaging" },
    { "affirmative_evidence": [], "rationale": "Generated archive inventories, hashes, and the current unpublished candidate metadata change.", "state": "affected", "surface": "generated-output" },
    { "affirmative_evidence": [], "rationale": "Discovery approval exclusions, owner adoption, path containment, private-data limits, and contradiction routing are strengthened.", "state": "affected", "surface": "security-or-authority" },
    { "affirmative_evidence": [], "rationale": "Workflow, contributor, public, project-map, skill, template, and change-local documentation change.", "state": "affected", "surface": "documentation" },
    { "affirmative_evidence": [], "rationale": "The unpublished v0.5.1 bundled adapter metadata and its trusted index hash are synchronized to current generated packages.", "state": "affected", "surface": "repository-metadata" },
    { "affirmative_evidence": [], "rationale": "On-demand routing and authority guidance changes while lifecycle stage and transition vocabularies remain unchanged.", "state": "affected", "surface": "lifecycle-governance" },
    { "affirmative_evidence": [], "rationale": "Research source freshness and availability, filesystem artifact safety, and clean adapter installation are explicit changed boundaries.", "state": "affected", "surface": "external-environment" }
  ],
  "outcome": "successful",
  "protocol_version": 3,
  "residual_risks": ["Discovery remains a judgment-driven optional capability; validation proves contract coherence, not future invocation frequency or decision quality."]
}
```
