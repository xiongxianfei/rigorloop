# Test-Spec Revision R2 Evidence

Date: 2026-08-12
Owner: test-spec
Review status before revision: approved by `test-spec-review-r2`

The test-case fields now use the closed authoring vocabulary owned by `test-spec`: T11 uses `Level: e2e`, and manual T12 uses `Command IDs: none`. The boundary proof map retains its separate `boundary-first-v1` vocabulary, including `Proof level: end-to-end` and the `-` sentinel where that schema requires them.

No requirement mapping, proof obligation, command, fixture, milestone, expected result, implementation scope, or boundary behavior changed. This substantive schema correction requires a fresh formal `test-spec-review` before implementation relies on the proof map.
