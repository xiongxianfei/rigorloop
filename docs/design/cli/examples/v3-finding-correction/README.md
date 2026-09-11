# Correct a finding through the CLI

[Request](request.json) explicitly updates finding-1 in design-review. [Saved response](saved-response.json) records storage success. The matching [stored and updated Review records](../../../record-format/examples/v3-finding-correction/README.md) show exactly what changes under [CLI-SR-26](../../cli.md#v3-finding-operations).

The hypothetical registered v3 store starts at revision b and saves at revision c; repeated-digit hashes and external subjects are synthetic. The request declares the current subject read separately from the finding’s reported basis. No basis or origin input is supplied, and no snapshot is constructed. Review assessment fields and applicability are preserved. This example assumes a validated v3 store. The [assessment update failure examples](../v3-assessment-update-errors/README.md) illustrate response dispatch before store validation.

The caller may explicitly correct any non-ID finding field. Supplying id, origin, basis or an unknown field in values rejects. State/resolution updates supply both and retain the existing consistency rules. Stale revisions conflict; equal values preserve bytes. Advanced complete-record replacement accepts the same valid correction, but rejects removal or renaming of an existing finding. Neither write path grants review approval or independently confirms the correction.

These are complete proposed envelopes, not current executable commands against v3. Only finding.set’s retained v2 form is supported at runtime today.


The complete [finding.show response](show-response.json) reads the corrected finding at revision c. The complete [summary context request](summary-request.json) and [response](summary-response.json) select that same finding and revision with fewer fields. Invoke finding show finding-1 --review design-review, or context --input - for the summary request, with the same root/change/format selectors. The d file identity remains synthetic.

Full fields equal the updated stored finding exactly. Summary omits only evidence and resolution and declares those omissions; complete:true means the requested selection was retrieved, not that its evidence was read. Neither response contains origin_available or lists nonexistent origin as omitted. Finding reads have no absent_fields extension. V2 findings and v2/v3 blockers retain their existing origin_available:true metadata and origin-bearing full fields; their summary scope still declares omitted origin. These examples do not change that retained transport contract.
