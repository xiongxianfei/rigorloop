# Final impact analysis (v3 staged protocol)

Use this reference only after Workflow resolves one active v3 final-Verify target. While the final-verification activation manifest remains `preactivation`, this reference defines staged protocol and grants no current lifecycle authority.

Resolve exactly one repository, governed change, verified subject revision, final holistic Code Review, approved Design package, approved Delivery plan, and final diff. Record each as one immutable scalar identity and classify its authority as `current`, `stale`, `missing`, `conflicting`, or `ambiguous`. Anything except `current` blocks a successful result.

Start from the approved Delivery plan verification map. Do not replace it, weaken it, or invent semantic plan coverage. A material missing allocation routes to `plan` ownership.

Classify every relevant final-diff surface as `affected`, `unaffected`, or `unknown`: runtime behavior, public API, state or persistence, migration, dependencies, build, packaging, generated output, security or authority, documentation, repository metadata, lifecycle governance, and external environment.

For `unaffected`, record affirmative evidence showing why the final change cannot materially affect the surface. A filename, extension, directory, author assertion, or absence of an obvious match is not sufficient. `.gitignore`, Markdown, fixtures, dependencies, and generated files receive no categorical shortcut. `unknown` expands verification and never supports narrowing.

Structural validation checks vocabulary, completeness, identities, and the presence of rationale. Verify and Code Review retain responsibility for the semantic adequacy of non-impact reasoning.
