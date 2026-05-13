# Review Resolution

Closeout status: closed

### code-review-m2-r1

Finding ID: CR-M2-F1
Disposition: accepted
Owner: implementer
Owning stage: implement
Chosen action: Simplify contributor and governance local Codex setup guidance so it describes the active public-adapter install path into ignored `.codex/skills/`, keeps `.codex/skills/` untracked, and directs authors to edit `skills/`, without preserving obsolete `.codex/skills/` hand-edit/generated-output prohibition wording.
Rationale: The code-review finding is correct. The approved transition-release contract and learning follow-up both prefer concise active behavior over preserving the old `.codex/skills/` generated-output rule shape.
Validation target: Update the cited docs, add or tighten static coverage so stale `.codex/skills/` generated-output and hand-edit wording is rejected where appropriate, then rerun the focused M2 adapter-distribution tests, release validation, review artifact validation, change metadata validation, lifecycle validation for touched artifacts, and whitespace validation.
Validation evidence: Simplified `.codex/skills/` local setup wording in `AGENTS.md`, `CONSTITUTION.md`, `README.md`, and `docs/workflows.md`; tightened `scripts/test-adapter-distribution.py` so contributor-doc checks reject the obsolete defensive phrases; added the M2 review-resolution checklist item to the active plan. `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_contributor_docs_install_local_codex_from_public_adapter AdapterDistributionTests.test_public_adapter_readme_documents_metadata_and_install_transition AdapterDistributionTests.test_v0_1_1_release_notes_document_transition_contract AdapterDistributionTests.test_validate_release_cli_accepts_repository_v0_1_1_artifacts` passed. `python scripts/validate-release.py --version v0.1.1` passed. `rg -n 'Do not hand-edit local Codex runtime state|Do not hand-edit generated Codex compatibility output|MUST NOT be hand-edited or tracked|Regenerate it with `python scripts/build-skills.py` when needed\.' AGENTS.md CONSTITUTION.md README.md docs/workflows.md` returned no matches.

### code-review-m2-r2

No material findings.
