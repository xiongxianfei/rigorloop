# Governed lifecycle routing

Load when the parent establishes an explicitly selected governed change requiring routing. This procedure applies contract-selected storage and actor-owned coordination; it grants no automation authority.

## Explicit recording

Use this profile when the project has adopted the RigorLoop Record Format and explicitly selected the change. Read the project's governing documents. The Workflow model owns coordination, Review and Closeout owns assessment policy, Record Format owns stored shapes, and CLI owns construction and persistence. Current storage uses `rigorloop-records-v3`; historical stores remain unchanged archival evidence. Select the actual record contract; never mix versions within a store. Retired or unknown stored formats are rejected without fallback. Do not migrate or reinterpret historical records; preserve their bytes and meaning as archival evidence. The project need not contain RigorLoop's internal design repository.

Use the contract-selected recording procedures in this skill and its conditional resources. Dispatch primary results by schema_version (2 or 3), then status and operation; a schema-3 error alone does not establish v3 storage. Read scope and omissions before relying on selected content. Retain substantive stage duties, permissions, independent assessment and proof obligations. Historical records grant no current execution authority.

Use `rigorloop context --root PATH --change ID --input - --format json` with explicitly selected kinds/filters and full detail. Expand the selection when needed: omitted content is not evidence of absence. Copy `record_contract` and `revision` into the targeted request's `contract` and `expected_revision`. Use `rigorloop subject inspect --root PATH --path FILE --content full --format json` for the exact engineering basis and mechanical identities; supply relied-on subjects as `reads` with their expected identities.

Make your decision, then use the purpose-specific command's `--help` and submit its targeted operation on stdin. Use `batch` for related explicit updates. Supply semantic values and any required applicability; the CLI constructs registry entries, preserves neighbors and serializes records. Do not reconstruct complete files or invoke historical eligibility first. Preview is optional; normal writes validate. A save does not approve work, establish readiness or select the next actor. Conflict requires rereading and reassessment; busy/recovery-required is not a save. Use explicit `record-store recover` for interrupted storage. Missing or stale evidence prevents reliance, not recording a correction.

Choose the current activity and responsible owner from the required engineering basis; status/context do not choose them. Record those decisions through activity set, work add/set and explicit applicability set as needed. Different actors may record in successive transactions. Corrections after completed work remain recordable. Do not manufacture another actor’s judgment, blocker disposition or final Verify assessment.

## Identity and basis

Use `rigorloop workflow-context` only for factual discovery and explicit target resolution. It does not choose work, report eligibility or recover storage. Read the selected v3 root using scoped primary context and subject inspection. Missing or corrupt current records stop reliance; unrelated archival records are neither current candidates nor inputs to old validators. Explicit retired input stops without fallback.

Read the current activity, work, exact engineering subjects, applicable reviews, evidence, findings and blockers needed for the decision. Expand omitted context when necessary. File existence and successful recording are not approval. Resolve missing, stale or contradictory required evidence before dependent continuation.

## Actor-owned updates

Choose and record activity and work using targeted `activity set` and `work add/set`, with current contract, expected revision and exact reads. Declare affected applicability explicitly; do not edit another actor's substantive judgment or retarget an approval. Plan may initialize absent work once from its approved Delivery package; route owns later work decisions. Preserve stage-owned evidence, finding IDs, and the immutable origins required for change-level blockers.

Corrections return to the owning author or implementation slice. Necessary owner decisions stay visible as blockers. Revised engineering subjects require the appropriate independent reassessment. Storage bookkeeping alone does not invalidate engineering assessment, but relevant new evidence must be considered before reliance. Follow the packaged review-reliance policy.

## Milestones and closeout

Select one exact authorized milestone from current work and the reviewed stable plan. Require current prerequisites. Implementation records proof, then an independent reviewer assesses the complete slice. Route may close that milestone only after approval and required corrections. A clean non-final review selects the next implementation milestone; it grants no final closeout.

After all milestones and required corrections are complete, require a fresh independent whole-change Code Review of the complete final diff and cross-milestone interactions. Earlier milestone reviews do not substitute. Then route to distinct final Verify. Failed Verify returns its evidence and concerns to the exact owner; it does not authorize Verify to repair upstream content. Successful Verify owns the final explanation and closeout assessment. PR and publication require their separate authority.

## Automation boundary

Legacy automation store adapters are unsupported. Do not create receipts, capabilities or a v2 automation representation by inference. An explicitly authorized sequence may invoke specialist stages within its existing bounds, but this does not restore retired persistent automation handlers. Use the conditional automation guidance for the selected invocation's supported or unsupported disposition.
