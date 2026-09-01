# Final impact analysis (v3 staged protocol)

Use this reference only after Workflow resolves one active v3 final-Verify target. While the final-verification activation manifest remains `preactivation`, this reference defines staged protocol and grants no current lifecycle authority.

Resolve exactly one repository, governed change, verified subject revision, final holistic Code Review, approved Design package, approved Delivery plan, and final diff. Record each as one immutable scalar identity and classify its authority as `current`, `stale`, `missing`, `conflicting`, or `ambiguous`. Anything except `current` blocks a successful result.

Use canonical identities: privacy-preserving SHA-256 fingerprints for repository and remote identity, resolved Git refs for base and head branches, immutable 40- or 64-hex Git revisions, safe change/review/package IDs, a normalized `docs/plans/*.md` path, and `sha256:<64 lowercase hex>` for the final diff. Commands, prose, numbers, placeholders, unsafe paths, and unresolved names are not identities.

Start from the approved Delivery plan verification map. Do not replace it, weaken it, or invent semantic plan coverage. A material missing allocation routes to `plan` ownership.

Classify every relevant final-diff surface as `affected`, `unaffected`, or `unknown`: runtime behavior, public API, state or persistence, migration, dependencies, build, packaging, generated output, security or authority, documentation, repository metadata, lifecycle governance, and external environment.

For `unaffected`, record affirmative evidence showing why the final change cannot materially affect the surface. A filename, extension, directory, author assertion, or absence of an obvious match is not sufficient. `.gitignore`, Markdown, fixtures, dependencies, and generated files receive no categorical shortcut. `unknown` expands verification and never supports narrowing.

Every evidence item's proved surfaces must be unique members of the same closed vocabulary and must each appear in the attempt's impact classification. Close those references before applying freshness or decision precedence.

Structural validation checks vocabulary, completeness, identities, and the presence of rationale. Verify and Code Review retain responsibility for the semantic adequacy of non-impact reasoning.
