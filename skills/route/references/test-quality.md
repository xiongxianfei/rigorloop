# Test quality application

Apply this guidance when the project explicitly adopts Validation-model test criteria and the invoked work authors, allocates or assesses test obligations. The project's governing Design remains authoritative. This guidance defines useful-test criteria; responsible specialists assess actual plans, tests and evidence under the project's review policy. It grants no suite approval, evidence applicability, review waiver or execution permission. Historical contracts retain their meaning.

## Derive the protection

Identify the governing Design requirement or explicit engineering obligation, test objective, relevant condition, observable expected outcome and plausible violation the test or coherent group should detect. Use many-to-many references and group-level rationale where sufficient; do not require a record or identity for every test function.

Expected outcomes come from the governing contract, not merely current production output. Preserve a discovered regression or hazard when its intended behavior is unclear, and route that decision to the Design owner. Missing labels do not make existing protection useless. Planning owns milestone and integrated proof allocation; implementation owns fixtures and assertions.

## Select meaningful cases

Cover representative outcome partitions, boundaries and material hazards. An additional case needs a distinct outcome, path, state, timing, authority, failure/recovery, compatibility or environmental contribution, or a justified diagnostic contribution that materially helps identify the protected failure. Explain that contribution: another name or repeated assertion alone does not establish diagnostic value. Do not manufacture Cartesian combinations or use test counts and coverage percentages as substitutes for reasoning.

Observe the claimed outcome at a boundary capable of exposing its violation, including required absence of side effects. A mock or helper that bypasses public dispatch, persistence or an external interaction cannot prove that behavior. Keep lower-level and integrated tests when detection scope or useful failure localization differs.

## Check the oracle

Inspect how the setup and assertion distinguish correct behavior from the intended violation. A concrete counterexample or inspected failure mechanism should explain the detection. Expected results computed by the same potentially faulty production logic, assertions that cannot fail on the claimed defect and unchecked snapshot updates are insufficient. Mutation testing can help but is not a universal requirement.

Property-based and randomized tests are useful when they have a justified invariant, generated domain and relevant failure observation. Preserve enough counterexample and environment information to investigate or reproduce failure; a seed alone cannot reproduce uncontrolled external state. Concrete generated inputs need not all be enumerated in Design.

Missing intended behavior returns to Design, missing proof allocation to planning, and defective concrete tests to their implementation or correction owner. Test success does not replace independent review or determine whether evidence remains current.
