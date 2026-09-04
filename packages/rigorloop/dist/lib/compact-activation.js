import { readFileSync } from "node:fs";

export const COMPACT_CURRENT_STATE_CONTRACT = "compact-current-state-v1";
export const COMPACT_ACTIVATION_STATES = Object.freeze(["withheld", "active"]);
export const COMPACT_ACTIVATION_COMPONENTS = Object.freeze([
  "adapters",
  "canonical-guidance",
  "cli",
  "documentation",
  "fixtures",
  "node-validator",
  "python-validator",
  "schemas",
  "skills",
  "templates",
]);
export const COMPACT_SUPPORTED_ADAPTERS = Object.freeze(["claude", "codex", "opencode"]);

function fail(message) {
  const error = new Error(message);
  error.code = "RL_INCOMPATIBLE_VERSION";
  throw error;
}

function exactKeys(value, expected, label) {
  if (!value || Array.isArray(value) || typeof value !== "object") fail(`${label} activation value must be an object`);
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    fail(`${label} activation fields must match the coherent component matrix`);
  }
}

export function compactWriterStatus(manifest) {
  exactKeys(manifest, ["schema_version", "contract", "state", "components", "supported_adapters"], "compact");
  if (manifest.schema_version !== 1) fail(`compact activation schema_version: unknown_value ${String(manifest.schema_version)}`);
  if (manifest.contract !== COMPACT_CURRENT_STATE_CONTRACT) fail(`compact activation contract: unknown_value ${String(manifest.contract)}`);
  if (!COMPACT_ACTIVATION_STATES.includes(manifest.state)) fail(`compact activation state: unknown_value ${String(manifest.state)}`);
  exactKeys(manifest.components, COMPACT_ACTIVATION_COMPONENTS, "compact component");
  for (const component of COMPACT_ACTIVATION_COMPONENTS) {
    if (manifest.components[component] !== COMPACT_CURRENT_STATE_CONTRACT) {
      fail(`compact activation component ${component}: unknown_value ${String(manifest.components[component])}`);
    }
  }
  if (!Array.isArray(manifest.supported_adapters)
    || manifest.supported_adapters.length !== COMPACT_SUPPORTED_ADAPTERS.length
    || manifest.supported_adapters.some((adapter, index) => adapter !== COMPACT_SUPPORTED_ADAPTERS[index])) {
    fail("compact activation supported adapters do not match the coherent component matrix");
  }
  return {
    contract: COMPACT_CURRENT_STATE_CONTRACT,
    reader: true,
    writer: manifest.state === "active",
    state: manifest.state,
  };
}

export function loadPackagedCompactActivation() {
  let manifest;
  try {
    manifest = JSON.parse(readFileSync(new URL("../metadata/compact-current-state-activation.json", import.meta.url), "utf8"));
  } catch (error) {
    fail(`compact activation metadata is unreadable: ${error.message}`);
  }
  compactWriterStatus(manifest);
  return manifest;
}
