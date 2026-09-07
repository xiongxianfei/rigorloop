// Representation-only M1 foundation. No CLI dispatch, persistence or lifecycle engine.
import { readFileSync } from "node:fs";
import { isDeepStrictEqual } from "node:util";
import { parseDocument } from "yaml";

export const RECORDS_V2_SCHEMA = JSON.parse(readFileSync(new URL("../schemas/rigorloop-records-v2.schema.json", import.meta.url), "utf8"));
const KINDS = new Set(["change", "review", "evidence", "decisions", "verify", "request"]);
const MIB = 1024 * 1024;
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
    return validate(RECORDS_V2_SCHEMA.$defs[name], value);
  }
  if (schema.anyOf) {
    // All current unions are explicit nullable values. Preserve diagnostics from
    // the selected non-null branch instead of swallowing nested path failures.
    const branch=schema.anyOf.find(x=>value===null ? x.type==="null" : x.type!=="null");
    if(branch) return validate(branch,value);
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
      const key = plain(child) && Object.hasOwn(child, "id") && Object.hasOwn(child, "path") ? JSON.stringify([child.path, child.id])
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

export function v2PathKind(changeId, path) {
  validate(RECORDS_V2_SCHEMA.$defs.id, changeId); safePath(path);
  const prefix = `docs/changes/${changeId}/`;
  if (!path.startsWith(prefix)) fail("cross-change or unsupported path");
  const relative = path.slice(prefix.length);
  const fixed = {"change.json": "change", "evidence.json": "evidence", "material-decisions.json": "decisions", "verify-report.json": "verify"};
  if (Object.hasOwn(fixed, relative)) return fixed[relative];
  if (/^reviews\/[a-z0-9][a-z0-9-]{0,79}\.json$/.test(relative)) return "review";
  fail("unsupported record path");
}

export function validateV2Record(kind, value) {
  if (!KINDS.has(kind)) fail("unknown_value kind");
  jsonDomain(value);
  if (plain(value) && Object.hasOwn(value,"schema_version") && value.schema_version!==2) fail("unsupported-contract");
  if (["change","request"].includes(kind) && typeof value?.contract === "string" && value.contract !== "rigorloop-records-v2") fail("unsupported-contract");
  validate(RECORDS_V2_SCHEMA.$defs[kind], value);
  visit(value, entry => {
    if (plain(entry) && Object.hasOwn(entry, "required_outcome") && Object.hasOwn(entry, "resolution")) {
      if ((entry.state === "open") !== (entry.resolution === null)) fail("blocker resolution shape mismatch");
    }
  });
  if (kind === "change") {
    for (const record of value.records) if (v2PathKind(value.change_id, record.path) !== record.kind) fail("registry kind mismatch");
    const paths = new Set(value.records.map(r => r.path));
    if (value.applicability.length !== paths.size || value.applicability.some(a => !paths.has(a.path))) fail("applicability registry mismatch");
  }
  if (kind === "request") {
    const writePaths = new Set(value.writes.map(write => write.path));
    if (value.reads.some(read => writePaths.has(read.path))) fail("read/write path overlap");
    for (const write of value.writes) {
      v2PathKind(value.change_id, write.path);
      const parsed = parseV2Record(v2PathKind(value.change_id, write.path), write.content);
      if (parsed.change_id !== value.change_id) fail("candidate change identity mismatch");
    }
    for (const read of value.reads) if (read.path === ".rigorloop/record-store" || read.path.startsWith(".rigorloop/record-store/")) fail("transient decision basis");
  }
  const ids = kind === "change" ? [...value.models, ...value.work, ...value.blockers].map(x=>x.id)
    : kind === "review" ? [value.id, ...value.findings.map(x=>x.id)] : [];
  if (new Set(ids).size !== ids.length) fail("ambiguous referenceable identity");
  return value;
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

export function parseV2Record(kind, input) {
  if (!KINDS.has(kind)) fail("unknown_value kind");
  const text = decode(input, kind === "request" ? 8*MIB : MIB);
  return validateV2Record(kind, strictJSON(text));
}

export function validateV2Request(input) {
  return parseV2Record("request", input);
}

export function validateV2Creation(request, rootExists) {
  validateV2Record("request", request);
  if (typeof rootExists !== "boolean") fail("root existence must be explicit");
  if (request.expected_revision !== null || rootExists || request.writes.some(w => w.expected_identity !== null) || !request.writes.some(w => w.path === `docs/changes/${request.change_id}/change.json`)) fail("creation requires an absent root and absent write targets");
  return request;
}

// Reference namespaces belong to the stored format, never inferred from ID shape.
export function validateV2Set(changeId, files) {
  return parseSet(changeId,files,false);
}

function parseSet(changeId, files, before) {
  if (!plain(files)) fail("expected candidate file map");
  validate(RECORDS_V2_SCHEMA.$defs.id, changeId);
  const root=`docs/changes/${changeId}/`, manifest=root+"change.json";
  if (Object.hasOwn(files,root+"change.yaml")) fail("ambiguous manifest");
  if (Object.keys(files).length > 65) fail("candidate file limit");
  let total=0;
  for (const content of Object.values(files)) {
    if(before && content===null) continue;
    if (!(typeof content === "string" || Buffer.isBuffer(content))) fail("invalid candidate bytes");
    total+=Buffer.byteLength(content);
  }
  if (total>65*MIB) fail("candidate byte limit");
  if (!Object.hasOwn(files,manifest)) fail("broken-reference");
  const change=parseV2Record("change",files[manifest]);
  if (change.change_id!==changeId) fail("change identity mismatch");
  const parsed=new Map([[manifest,change]]), kinds=new Map([[manifest,"change"]]);
  for(const record of change.records) {
    if (!Object.hasOwn(files,record.path) || files[record.path]===null) {
      if(before) continue;
      fail("broken-reference");
    }
    const data=parseV2Record(record.kind,files[record.path]);
    if(data.change_id!==changeId) fail("record change identity mismatch");
    if(record.kind==="review" && record.path!==root+`reviews/${data.id}.json`) fail("review path identity mismatch");
    parsed.set(record.path,data);kinds.set(record.path,record.kind);
  }
  const membership=new Set([manifest,...change.records.map(r=>r.path)]);
  if(Object.keys(files).some(path=>!membership.has(path))) fail("unregistered candidate file");
  if(before) return parsed; // Missing/dangling prior content may be repaired.
  const targets=new Map();
  for(const [path,data] of parsed) {
    const ids=new Map();
    if(kinds.get(path)==="review") ids.set(data.id,"review");
    for(const collection of ["models","work","blockers","findings","checks","decisions"])
      for(const entry of data[collection]??[]) ids.set(entry.id,collection);
    targets.set(path,ids);
  }
  const resolveRefs=(refs,allowed)=> {
    for(const ref of refs) if(!allowed.includes(targets.get(ref.path)?.get(ref.id))) fail("broken-reference");
  };
  for(const [path,data] of parsed) {
    for(const concern of [...(data.blockers??[]),...(data.findings??[])])
      if(concern.resolution) resolveRefs(concern.resolution.evidence_refs,["checks"]);
    if(kinds.get(path)==="verify") {
      resolveRefs(data.evidence_refs,["checks"]);resolveRefs(data.review_refs,["review"]);
    }
    for(const decision of data.decisions??[]) resolveRefs(decision.source_refs,["models","work","blockers","review","findings","checks","decisions"]);
  }
  return parsed;
}

export function validateV2Preservation(changeId, beforeFiles, afterFiles) {
  const before=parseSet(changeId,beforeFiles,true), after=validateV2Set(changeId,afterFiles);
  const manifest=`docs/changes/${changeId}/change.json`;
  const membership=new Set(after.get(manifest).records.map(r=>r.path));
  if(before.get(manifest).records.some(r=>!membership.has(r.path))) fail("existing registry member removed");
  for(const [path,data] of before) {
    const next=after.get(path);
    if(!next) fail("existing record removed");
    for(const collection of ["blockers","findings"]) {
      for(const concern of data[collection]??[]) {
        const retained=next[collection]?.find(x=>x.id===concern.id);
        if(!retained || !isDeepStrictEqual(concern.origin,retained.origin)) fail("concern origin must be preserved");
      }
    }
  }
  return after;
}
