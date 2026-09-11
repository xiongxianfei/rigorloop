# Observation identity changes when observed content changes

[Scan B](scan-b.json) and [scan C](scan-c.json) are complete internal observation-digest inputs under [CLI-SR-14/20](../../cli.md#requirements). Their schema_version 2 versions the digest preimage, not stored records or a public request. [Expected comparison](expected.json) is an explanatory expectation object, not an accepted record or CLI response.

Both scans share the same synthetic record revision and diagnostics. The referenced historical subject is A, while the observed identity changes from B to C. The observation digest must therefore change even though both scans report the same drift message. A continuation bound to the first observation identity conflicts against the second scan.

The two expected observation digests are reproducible: recursively sort object keys, retain array order, encode compact UTF-8 JSON without a final newline, and take sha256. The underlying repeated-digit subject/revision identities remain synthetic. This example demonstrates the digest relationship without claiming that a live continuation command was executed.
