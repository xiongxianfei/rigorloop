// Format-neutral advanced result envelope. Snapshot contents belong to the stored-format validator.
import {readFileSync} from 'node:fs';
const TRANSPORT_SCHEMA=JSON.parse(readFileSync(new URL('../schemas/record-store-transport.schema.json',import.meta.url),'utf8'));
const fail = (message) => {
  const code = /limit/.test(message) ? "limit-exceeded" : /unsafe-path|cross-change|unsupported record path/.test(message) ? "unsafe-path"
    : message === "unsupported-contract" ? "unsupported-contract" : message === "broken-reference" ? "broken-reference" : "invalid-input";
  throw Object.assign(new Error(`record-store: ${message}`), {recordStoreCode:code});
};
const plain = v => v !== null && typeof v === "object" && !Array.isArray(v) && [Object.prototype, null].includes(Object.getPrototypeOf(v));

function unicode(text) {
  for (let i = 0; i < text.length; i++) {
    const c = text.charCodeAt(i);
    if (c >= 0xd800 && c <= 0xdbff) {
      const next = text.charCodeAt(++i);
      if (!(next >= 0xdc00 && next <= 0xdfff)) fail("invalid Unicode");
    } else if (c >= 0xdc00 && c <= 0xdfff) fail("invalid Unicode");
  }
}

function jsonDomain(value, depth = 0, ancestors = new Set()) {
  if (value === null || typeof value === "boolean") return;
  if (typeof value === "string") return unicode(value);
  if (typeof value === "number") { if (!Number.isFinite(value)) fail("nonfinite number"); return; }
  if ((!plain(value) && !Array.isArray(value)) || ancestors.has(value)) fail("invalid JSON value");
  if (depth >= 32) fail("nesting limit exceeded");
  ancestors.add(value);
  for (const [key, child] of Object.entries(value)) { unicode(key); jsonDomain(child, depth + 1, ancestors); }
  ancestors.delete(value);
}

function safePath(path) {
  if (typeof path !== "string" || !/^[\x20-\x7e]+$/.test(path) || path.length > 1024 || path.includes("\\") || path.startsWith("/") || /^[A-Za-z]:/.test(path) || path.split("/").some(p => !p || p === "." || p === "..")) fail("unsafe-path");
}

function validate(schema, value) {
  if (schema.$ref) {
    const name = schema.$ref.split("/").at(-1);
    if (name === "path") safePath(value);
    return validate(TRANSPORT_SCHEMA.$defs[name], value);
  }
  if (schema.anyOf) {
    for (const branch of schema.anyOf) { try { validate(branch, value); return; } catch {} }
    fail("invalid nullable value");
  }
  if (Object.hasOwn(schema, "const") && value !== schema.const) fail("unknown_value constant");
  if (schema.enum && !schema.enum.includes(value)) fail("unknown_value vocabulary");
  if (schema.type === "null" && value !== null) fail("expected null");
  if (schema.type === "string") {
    if (typeof value !== "string" || (schema.minLength !== undefined && value.length < schema.minLength) || (schema.maxLength !== undefined && value.length > schema.maxLength) || (schema.pattern && !new RegExp(schema.pattern).test(value))) fail("invalid string");
  }
  if (schema.type === "object") {
    if (!plain(value)) fail("expected object");
    if (Object.keys(value).some(k => !Object.hasOwn(schema.properties, k))) fail("unknown field");
    if (schema.required.some(k => !Object.hasOwn(value, k))) fail("missing field");
    for (const [key, child] of Object.entries(schema.properties)) validate(child, value[key]);
  }
  if (schema.type === "array") {
    if (!Array.isArray(value) || (schema.minItems !== undefined && value.length < schema.minItems) || (schema.maxItems !== undefined && value.length > schema.maxItems)) fail("invalid array limit");
    const seen = new Set();
    for (const child of value) {
      validate(schema.items, child);
      // IDs/paths are unique within their owning array. EntryRefs use both fields.
      const key = schema.items.$ref === "#/$defs/diagnostic" ? JSON.stringify([child.code, child.path, child.message])
        : plain(child) && Object.hasOwn(child, "id") && Object.hasOwn(child, "path") ? JSON.stringify([child.path, child.id])
        : plain(child) && Object.hasOwn(child, "id") ? child.id
          : plain(child) && Object.hasOwn(child, "path") ? child.path : JSON.stringify(child);
      if (seen.has(key)) fail("duplicate identity or path");
      seen.add(key);
    }
  }
}

function validateResultEnvelope(value) {
  if (value.operation === null || value.change_id === null) {
    if (value.status !== "rejected" || value.revision !== null || value.files.length || value.snapshot !== null || value.observations.length || value.transaction !== null || value.errors.length !== 1 || value.errors[0].code !== "invalid-input" || value.errors[0].path !== null) fail("invalid selector rejection");
    return;
  }
  const success = {inspect:["inspected"], check:["valid"], record:["saved", "unchanged"], recover:["recovered"]};
  const failures = ["rejected", "conflict", "busy", "recovery-required"];
  if (!success[value.operation].includes(value.status) && !failures.includes(value.status)) fail("operation/status mismatch");
  const observationCodes = ["absent-change", "subject-drift", "failed-evidence", "inconsistent-claim"];
  if (value.observations.some(d => !observationCodes.includes(d.code)) || value.errors.some(d => observationCodes.includes(d.code))) fail("diagnostic category mismatch");
  const inspected = value.operation === "inspect" && value.status === "inspected";
  if (inspected !== (value.snapshot !== null)) fail("snapshot presence mismatch");
  if (!inspected) return;
}

export function validateAdvancedEnvelope(value) {
 jsonDomain(value);
 validate(TRANSPORT_SCHEMA.$defs.result,value);
 validateResultEnvelope(value);
 return value;
}
