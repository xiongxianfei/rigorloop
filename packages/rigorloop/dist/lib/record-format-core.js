import {MIB,fail,plain,jsonDomain,decode,strictJSON} from "./record-json.js";


// Shared mechanics; each selected schema retains its own closed contract.
export function createRecordFormat(schemaDocument, {version, contract}) {
const KINDS = new Set(["change", "review", "evidence", "decisions", "verify"]);
function safePath(path) {
  if (typeof path !== "string" || !/^[\x20-\x7e]+$/.test(path) || path.length > 1024 || path.includes("\\") || path.startsWith("/") || /^[A-Za-z]:/.test(path) || path.split("/").some(p => !p || p === "." || p === "..")) fail("unsafe-path");
}

function validate(schema, value) {
  if (schema.$ref) {
    const name = schema.$ref.split("/").at(-1);
    if (name === "path") safePath(value);
    return validate(schemaDocument.$defs[name], value);
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
    for (const [key, child] of Object.entries(schema.properties)) if (Object.hasOwn(value,key)) validate(child, value[key]);
  }
  if (schema.type === "array") {
    if(!Array.isArray(value) || (schema.minItems!==undefined && value.length<schema.minItems)) fail("invalid array shape");
    if (!Array.isArray(value) || (schema.minItems !== undefined && value.length < schema.minItems) || (schema.maxItems !== undefined && value.length > schema.maxItems)) fail("invalid array limit");
    const seen = new Set();
    for (const child of value) {
      validate(schema.items, child);
      // IDs/paths are unique within their owning array. EntryRefs use both fields.
      const key = plain(child) && Object.hasOwn(child, "id") && Object.hasOwn(child, "path") ? JSON.stringify([child.path, child.id])
        : plain(child) && Object.hasOwn(child, "id") ? child.id
          : plain(child) && Object.hasOwn(child, "path") ? child.path : JSON.stringify(child);
      if (schema.uniqueItems && seen.has(key)) fail("duplicate identity or path");
      seen.add(key);
    }
  }
}

function visit(value, fn) {
  if (!value || typeof value !== "object") return;
  fn(value);
  for (const child of Object.values(value)) visit(child, fn);
}

function pathKind(changeId, path) {
  validate(schemaDocument.$defs.id, changeId); safePath(path);
  const prefix = `docs/changes/${changeId}/`;
  if (!path.startsWith(prefix)) fail("cross-change or unsupported path");
  const relative = path.slice(prefix.length);
  const fixed = {"change.json": "change", "evidence.json": "evidence", "material-decisions.json": "decisions", "verify-report.json": "verify"};
  if (Object.hasOwn(fixed, relative)) return fixed[relative];
  if (/^reviews\/[a-z0-9][a-z0-9-]{0,79}\.json$/.test(relative)) return "review";
  fail("unsupported record path");
}

function validateRecord(kind, value) {
  if (!KINDS.has(kind)) fail("unknown_value kind");
  jsonDomain(value);
  if (plain(value) && Object.hasOwn(value,"schema_version") && value.schema_version!==version) fail("unsupported-contract");
  if (kind === "change" && typeof value?.contract === "string" && value.contract !== contract) fail("unsupported-contract");
  validate(schemaDocument.$defs[kind], value);
  visit(value, entry => {
    if (plain(entry) && Object.hasOwn(entry, "required_outcome") && Object.hasOwn(entry, "resolution")) {
      if ((entry.state === "open") !== (entry.resolution === null)) fail("blocker resolution shape mismatch");
    }
  });
  if (kind === "change") {
    for (const record of value.records) if (pathKind(value.change_id, record.path) !== record.kind) fail("registry kind mismatch");
    const paths = new Set(value.records.map(r => r.path));
    if (value.applicability.length !== paths.size || value.applicability.some(a => !paths.has(a.path))) fail("applicability registry mismatch");
  }
  const ids = kind === "change" ? [...value.models, ...value.work, ...value.blockers].map(x=>x.id)
    : kind === "review" ? [value.id, ...value.findings.map(x=>x.id)] : [];
  if (new Set(ids).size !== ids.length) fail("ambiguous referenceable identity");
  return value;
}

function parseRecord(kind, input) {
  if (!KINDS.has(kind)) fail("unknown_value kind");
  const text = decode(input, MIB);
  return validateRecord(kind, strictJSON(text));
}

// Reference namespaces belong to the stored format, never inferred from ID shape.
function validateSet(changeId, files) {
  return parseSet(changeId,files);
}

function parseSet(changeId, files) {
  if (!plain(files)) fail("expected candidate file map");
  validate(schemaDocument.$defs.id, changeId);
  const root=`docs/changes/${changeId}/`, manifest=root+"change.json";
  if (Object.hasOwn(files,root+"change.yaml")) fail("ambiguous manifest");
  if (Object.keys(files).length > 65) fail("candidate file limit");
  let total=0;
  for (const content of Object.values(files)) {
    if (!(typeof content === "string" || Buffer.isBuffer(content))) fail("invalid candidate bytes");
    total+=Buffer.byteLength(content);
  }
  if (total>65*MIB) fail("candidate byte limit");
  if (!Object.hasOwn(files,manifest)) fail("broken-reference");
  const change=parseRecord("change",files[manifest]);
  if (change.change_id!==changeId) fail("change identity mismatch");
  const parsed=new Map([[manifest,change]]), kinds=new Map([[manifest,"change"]]);
  for(const record of change.records) {
    if (!Object.hasOwn(files,record.path) || files[record.path]===null) {
      fail("broken-reference");
    }
    const data=parseRecord(record.kind,files[record.path]);
    if(data.change_id!==changeId) fail("record change identity mismatch");
    if(record.kind==="review" && record.path!==root+`reviews/${data.id}.json`) fail("review path identity mismatch");
    parsed.set(record.path,data);kinds.set(record.path,record.kind);
  }
  const membership=new Set([manifest,...change.records.map(r=>r.path)]);
  if(Object.keys(files).some(path=>!membership.has(path))) fail("unregistered candidate file");
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

return {parseRecord,validateRecord,validateSet,pathKind};
}
