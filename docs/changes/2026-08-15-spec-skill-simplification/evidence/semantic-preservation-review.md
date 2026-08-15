# Spec Semantic Preservation Review

- Reviewed package: `skills/spec/`
- Governing contract: `specs/spec-skill-simplification.md`
- Rule ledger: `spec-rule-disposition.yaml`
- Literal ledger: `spec-literal-compatibility.yaml`
- Result: passed after M2 correction and rereview

## Rule reconciliation

All 28 semantic rows were inspected against the final package and their requirements. The final ownership distribution is 15 retained inline, eight retained in the governed reference, two retained in the existing boundary references, two asset-owned, and one removed duplicate whose surviving owner remains inline.

| Rule group | IDs | Final result |
| --- | --- | --- |
| Purpose, evidence, placement, signals, portable operations | SRULE-001, SRULE-002, SRULE-004, SRULE-005, SRULE-007 | Present inline and available to both profiles. |
| Governed settlement, authority, creation, revision, retry, stale recovery | SRULE-003, SRULE-006, SRULE-008-SRULE-013 | Present in the conditional governed reference with explicit R21-R42 identities, writes, stops, and preservation. |
| Resource loading and failure | SRULE-014, SRULE-028 | Exact triggers and fail-safe behavior remain inline. |
| Boundary method and formal record | SRULE-015, SRULE-016 | Existing references are byte-identical to baseline and still load initially. |
| Structural composition | SRULE-017, SRULE-021 | The existing skeleton remains the structural owner and adds one marker only. |
| Block state, compatibility, and grandfathering | SRULE-018-SRULE-020 | Closed states, preservation, deactivation, anchors, and full-rewrite stops remain inline. |
| Contract quality, handoff, artifact history, readability, evidence | SRULE-022-SRULE-027 | Universal semantics remain inline or use the canonical skeleton; duplicate output prose was removed without losing its owner. |

The M2 R1 review caught incomplete wording for governed identities and retained-inline rules. `SPSIM-M2-CR1` and `SPSIM-M2-CR2` are closed by `code-review-M2-r2`; the focused tests now cover the corrected semantic groups.

## Literal reconciliation

All 50 exact literal rows retain one classification and disposition: 27 normative-contract, 21 parser-or-package-contract, one test-only-incidental, and one obsolete. Final dispositions are 41 preserve-exact, seven introduce-exact, one replace-with-owned-summary, and one remove-after-relocation. Exact shared evidence/readability blocks, resource paths and verbs, lifecycle vocabulary, boundary headings, skeleton headings, and the insertion marker match their classified treatment.

## Ownership and exclusions

No universal rule moved behind governed loading. The governed reference owns no portable policy, the boundary references remain unchanged, and the skeleton owns no applicability or lifecycle semantics. No target-agent runtime, prose classifier, manual semantic-review acceptance gate, tokenizer dependency, or new validator family was introduced.

## Conclusion

The final package preserves the approved observable, lifecycle, recovery, structural, portability, and claim contracts while reducing both loaded profiles. No unexplained semantic deletion or duplicate loaded owner remains.
