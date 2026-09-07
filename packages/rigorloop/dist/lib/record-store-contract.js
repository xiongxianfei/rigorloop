// Representation-only M1 foundation. No CLI dispatch, persistence or lifecycle engine.
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { parseDocument } from "yaml";

export const RECORD_STORE_SCHEMA = JSON.parse(readFileSync(new URL("../schemas/explicit-recording-v1.schema.json", import.meta.url), "utf8"));
const KINDS = new Set(["change", "review", "evidence", "decisions", "verify", "request", "result"]);
const MARKDOWN = new Set(["review", "decisions", "verify"]);
const MIB = 1024 * 1024;
const fail = (message) => {
  const code = /limit/.test(message) ? "limit-exceeded" : /unsafe-path|cross-change|unsupported record path/.test(message) ? "unsafe-path"
    : message === "unsupported-contract" ? "unsupported-contract" : message === "broken-reference" ? "broken-reference" : "invalid-input";
  throw Object.assign(new Error(`record-store: ${message}`), {recordStoreCode:code});
};
const hash = (text) => `sha256:${createHash("sha256").update(text).digest("hex")}`;
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
    return validate(RECORD_STORE_SCHEMA.$defs[name], value);
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

function visit(value, fn) {
  if (!value || typeof value !== "object") return;
  fn(value);
  for (const child of Object.values(value)) visit(child, fn);
}

export function recordStorePathKind(changeId, path) {
  validate(RECORD_STORE_SCHEMA.$defs.id, changeId); safePath(path);
  const prefix = `docs/changes/${changeId}/`;
  if (!path.startsWith(prefix)) fail("cross-change or unsupported path");
  const relative = path.slice(prefix.length);
  const fixed = {"change.yaml": "change", "evidence.yaml": "evidence", "material-decisions.md": "decisions", "verify-report.md": "verify"};
  if (Object.hasOwn(fixed, relative)) return fixed[relative];
  if (/^reviews\/[a-z0-9][a-z0-9-]{0,79}\.md$/.test(relative)) return "review";
  fail("unsupported record path");
}

export function validateRecordStoreRecord(kind, value) {
  if (!KINDS.has(kind)) fail("unknown_value kind");
  jsonDomain(value);
  if (["change","request"].includes(kind) && typeof value?.contract === "string" && value.contract !== "explicit-recording-v1") fail("unsupported-contract");
  validate(RECORD_STORE_SCHEMA.$defs[kind], value);
  visit(value, entry => {
    if (plain(entry) && Object.hasOwn(entry, "required_outcome") && Object.hasOwn(entry, "resolution")) {
      if ((entry.state === "open") !== (entry.resolution === null)) fail("blocker resolution shape mismatch");
    }
  });
  if (kind === "change") {
    for (const record of value.records) if (recordStorePathKind(value.change_id, record.path) !== record.kind) fail("registry kind mismatch");
    const paths = new Set(value.records.map(r => r.path));
    if (value.applicability.length !== paths.size || value.applicability.some(a => !paths.has(a.path))) fail("applicability registry mismatch");
  }
  if (kind === "request") {
    const writePaths = new Set(value.writes.map(write => write.path));
    if (value.reads.some(read => writePaths.has(read.path))) fail("read/write path overlap");
    for (const write of value.writes) {
      recordStorePathKind(value.change_id, write.path);
      const parsed = parseRecordStore(recordStorePathKind(value.change_id, write.path), write.content);
      if (parsed.change_id !== value.change_id) fail("candidate change identity mismatch");
    }
    for (const read of value.reads) if (read.path === ".rigorloop/record-store" || read.path.startsWith(".rigorloop/record-store/")) fail("transient decision basis");
  }
  if (kind === "result") validateResult(value);
  return value;
}

function validateResult(value) {
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
  const records = value.snapshot.records;
  if (records.length !== value.files.length) fail("snapshot membership mismatch");
  if (!records.length) {
    if (value.revision !== null || !value.observations.some(d => d.code === "absent-change")) fail("absent snapshot mismatch");
    return;
  }
  const manifestPath = `docs/changes/${value.change_id}/change.yaml`;
  const manifest = records.find(record => record.path === manifestPath);
  if (!manifest || manifest.content === null) fail("missing snapshot manifest");
  const change = parseRecordStore("change", manifest.content);
  if (change.change_id !== value.change_id) fail("snapshot change identity mismatch");
  const membership = new Set([manifestPath, ...change.records.map(record => record.path)]);
  if (membership.size !== records.length || records.some(record => !membership.has(record.path))) fail("snapshot registry mismatch");
  for (let i=0; i<records.length; i++) {
    const record=records[i], file=value.files[i];
    if (record.path !== file.path || (i && records[i-1].path >= record.path)) fail("snapshot order mismatch");
    const kind = recordStorePathKind(value.change_id, record.path);
    if (record.content === null) {
      if (!value.observations.some(d => d.code === "subject-drift" && d.path === record.path)) fail("missing snapshot observation");
    } else {
      const data = parseRecordStore(kind, record.content);
      if (data.change_id !== value.change_id || (kind === "review" && record.path !== `docs/changes/${value.change_id}/reviews/${data.id}.md`)) fail("snapshot record identity mismatch");
    }
    if (record.content === null ? file.identity !== null : file.identity !== hash(record.content)) fail("snapshot identity mismatch");
  }
  if (value.revision !== hash(JSON.stringify(value.files.map(file => [file.path, file.identity])))) fail("snapshot revision mismatch");
}

function decode(input, limit) {
  if (!(typeof input === "string" || Buffer.isBuffer(input))) fail("expected UTF-8 text");
  if (Buffer.byteLength(input) > limit) fail("byte limit exceeded");
  let text;
  try { text = typeof input === "string" ? input : new TextDecoder("utf-8", {fatal:true, ignoreBOM:true}).decode(input); }
  catch { fail("invalid UTF-8"); }
  unicode(text);
  if (text.startsWith("\ufeff") || text.includes("\r") || !text.endsWith("\n")) fail("invalid record encoding");
  return text;
}

function strictJSON(text) {
  // Bound nesting before either parser sees the payload, ignoring quoted delimiters.
  let depth=0, quoted=false, escaped=false;
  for (const c of text) {
    if (quoted) { if (escaped) escaped=false; else if (c === "\\") escaped=true; else if (c === '"') quoted=false; }
    else if (c === '"') quoted=true;
    else if (c === "{" || c === "[") { if (++depth > 32) fail("nesting limit exceeded"); }
    else if (c === "}" || c === "]") depth--;
  }
  let value;
  try {
    value = JSON.parse(text); // YAML extensions are never admitted.
    const document = parseDocument(text, {uniqueKeys:true, strict:true, prettyErrors:false});
    if (document.errors.length) fail("duplicate or invalid JSON keys");
  } catch { fail("invalid JSON or duplicate keys"); }
  jsonDomain(value);
  return value;
}

export function parseRecordStore(kind, input) {
  if (!KINDS.has(kind)) fail("unknown_value kind");
  // Results have no separate wire-size limit; authoritative snapshot files do.
  const text = decode(input, kind === "request" ? 8*MIB : kind === "result" ? Infinity : MIB);
  let json=text;
  if (MARKDOWN.has(kind)) {
    if (!text.startsWith("---\n")) fail("missing Markdown metadata");
    const end=text.indexOf("\n---\n",4);
    if (end < 0 || !text.slice(end+5).trim()) fail("missing Markdown rationale");
    json=text.slice(4,end);
  }
  return validateRecordStoreRecord(kind, strictJSON(json));
}

export function validateRecordStoreRequest(input) {
  return parseRecordStore("request", input);
}

export function validateRecordStoreCreation(request, rootExists) {
  validateRecordStoreRecord("request", request);
  if (typeof rootExists !== "boolean") fail("root existence must be explicit");
  if (request.expected_revision !== null || rootExists || request.writes.some(w => w.expected_identity !== null) || !request.writes.some(w => w.path === `docs/changes/${request.change_id}/change.yaml`)) fail("creation requires an absent root and absent write targets");
  return request;
}

export function validateRecordStoreSet(changeId, files) {
  if (!plain(files)) fail("expected candidate file map");
  const root=`docs/changes/${changeId}/`, manifestPath=root+"change.yaml";
  const change=parseRecordStore("change",files[manifestPath]);
  if (change.change_id !== changeId) fail("change identity mismatch");
  const parsed = new Map([[manifestPath,change]]);
  for (const record of change.records) {
    const data=parseRecordStore(record.kind,files[record.path]);
    if (data.change_id !== changeId) fail("record change identity mismatch");
    if (record.kind === "review" && record.path !== root+`reviews/${data.id}.md`) fail("review path identity mismatch");
    parsed.set(record.path,data);
  }
  if (Object.keys(files).length !== parsed.size || Object.keys(files).some(p=>!parsed.has(p))) fail("unregistered candidate file");
  const entries=new Map();
  for (const [path,data] of parsed) {
    const ids=new Set();
    if (data.id) ids.add(data.id);
    for (const key of ["blockers","findings","checks","decisions","work","models"]) for (const entry of data[key] ?? []) ids.add(entry.id);
    entries.set(path,ids);
  }
  for (const data of parsed.values()) visit(data, entry => {
    if (plain(entry) && Object.keys(entry).length === 2 && Object.hasOwn(entry,"path") && Object.hasOwn(entry,"id") && !entries.get(entry.path)?.has(entry.id)) fail("broken-reference");
  });
  return parsed;
}
