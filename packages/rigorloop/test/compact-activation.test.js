import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  compactWriterStatus,
  loadPackagedCompactActivation,
} from "../dist/lib/compact-activation.js";
import { parseCompactYaml, validateCompactSet } from "../dist/lib/compact-contract.js";
import { buildNewChangeDraft } from "../dist/lib/new-change.js";

const expectedComponents = [
  "adapters", "canonical-guidance", "cli", "documentation", "fixtures",
  "node-validator", "python-validator", "schemas", "skills", "templates",
];

test("packaged and canonical compact activation matrices are identical and active", () => {
  const packaged = loadPackagedCompactActivation();
  const canonical = JSON.parse(readFileSync(new URL("../../../specs/compact-current-state-activation.yaml", import.meta.url), "utf8"));
  assert.deepEqual(packaged, canonical);
  assert.deepEqual(Object.keys(packaged.components), expectedComponents);
  assert.deepEqual(compactWriterStatus(packaged), { contract: "compact-current-state-v1", reader: true, writer: true, state: "active" });
});

test("mixed, unknown, and incomplete matrices fail closed while rollback keeps the reader", () => {
  const active = loadPackagedCompactActivation();
  for (const candidate of [
    { ...active, components: { ...active.components, cli: "stage-owned-change-local-v3" } },
    { ...active, components: { ...active.components, cli: "unknown_value" } },
    { ...active, components: Object.fromEntries(Object.entries(active.components).filter(([key]) => key !== "cli")) },
  ]) assert.throws(() => compactWriterStatus(candidate), /activation|component|unknown_value/);
  assert.deepEqual(compactWriterStatus({ ...active, state: "withheld" }), { contract: "compact-current-state-v1", reader: true, writer: false, state: "withheld" });
});

test("new-change emits a valid empty compact set only under active writer authority", () => {
  const active = loadPackagedCompactActivation();
  const draft = buildNewChangeDraft({ changeId: "compact-example", title: "Compact example" }, active);
  const source = draft.planned_change_metadata.content;
  const change = parseCompactYaml(source, "compact-change-v1");
  assert.equal(change.lifecycle_contract, "compact-current-state-v1");
  assert.equal(validateCompactSet({ changeBytes: source, files: {} }).change.change_id, "compact-example");
  assert.throws(
    () => buildNewChangeDraft({ changeId: "blocked-example", title: "Blocked" }, { ...active, state: "withheld" }),
    /writer is withheld/,
  );
});
