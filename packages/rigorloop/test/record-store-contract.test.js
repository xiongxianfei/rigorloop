import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { test } from "node:test";
import {
  RECORD_STORE_SCHEMA, parseRecordStore, validateRecordStoreRecord,
  validateRecordStoreSet, validateRecordStoreRequest, validateRecordStoreCreation,
} from "../dist/lib/record-store-contract.js";

const fixtureURL = new URL("../../../tests/fixtures/explicit-recording-v1/records.json", import.meta.url);
const fixtures = () => JSON.parse(readFileSync(fixtureURL, "utf8"));
const encode = (kind, data) => ["review", "decisions", "verify"].includes(kind)
  ? `---\n${JSON.stringify(data)}\n---\nRecorded rationale.\n` : `${JSON.stringify(data)}\n`;
const root = "docs/changes/example/";
const digest = text => `sha256:${createHash("sha256").update(text).digest("hex")}`;

test("TG-01 all record, request and result representations validate without mutation", () => {
  const f = fixtures();
  for (const [kind, value] of Object.entries(f)) {
    const before = JSON.stringify(value);
    assert.doesNotThrow(() => validateRecordStoreRecord(kind, value));
    assert.deepEqual(parseRecordStore(kind, encode(kind, value)), value);
    assert.equal(JSON.stringify(value), before);
  }
});

test("TG-07 packaged templates are canonical, valid and do not preapprove work", () => {
  const canonical=readFileSync(new URL("../../../templates/explicit-recording/records.json",import.meta.url));
  assert.deepEqual(readFileSync(new URL("../dist/templates/explicit-recording/records.json",import.meta.url)),canonical);
  const templates=JSON.parse(canonical);
  for(const [kind,value]of Object.entries(templates))validateRecordStoreRecord(kind,value);
  assert.equal(templates.change.activity.status,"pending");
  assert.equal(templates.review.judgment,"blocked");
  assert.deepEqual(templates.change.records,[]);
  assert.deepEqual(templates.change.applicability,[]);
  // Success-only Verify is a shape example, never included in initial creation.
  assert.equal(templates.verify.outcome,"success");
});

test("TG-01 canonical and packaged schemas have byte parity", () => {
  assert.equal(readFileSync(new URL("../../../schemas/explicit-recording-v1.schema.json", import.meta.url), "utf8"),
    readFileSync(new URL("../dist/schemas/explicit-recording-v1.schema.json", import.meta.url), "utf8"));
});

function visit(schema, value, path = []) {
  if (schema.$ref) return visit(RECORD_STORE_SCHEMA.$defs[schema.$ref.split("/").at(-1)], value, path);
  if (schema.anyOf) return schema.anyOf.flatMap(s => {
    if (s.type === "null" && value !== null || s.type !== "null" && value === null) return [];
    return visit(s, value, path);
  });
  const found = schema.enum || Object.hasOwn(schema, "const") ? [path] : [];
  if (schema.properties && value) for (const [k, s] of Object.entries(schema.properties)) found.push(...visit(s, value[k], [...path, k]));
  if (schema.items && Array.isArray(value)) value.forEach((v, i) => found.push(...visit(schema.items, v, [...path, i])));
  return found;
}

test("TG-01 unknown_value rejected at every exercised closed-vocabulary location", () => {
  let count = 0;
  for (const [kind, data] of Object.entries(fixtures())) for (const path of visit(RECORD_STORE_SCHEMA.$defs[kind], data)) {
    const value = structuredClone(data); let parent = value;
    for (const key of path.slice(0, -1)) parent = parent[key];
    parent[path.at(-1)] = "unknown_value";
    assert.throws(() => validateRecordStoreRecord(kind, value), undefined, `${kind}:${path.join(".")}`);
    count++;
  }
  assert.ok(count >= 25, `Only ${count} closed values exercised`);
});

test("TG-01 unknown_kind and missing or extra fields fail closed", () => {
  assert.throws(() => validateRecordStoreRecord("unknown_value", {}));
  for (const [kind, data] of Object.entries(fixtures())) {
    assert.throws(() => validateRecordStoreRecord(kind, {...data, unknown_value: true}));
    for (const key of Object.keys(data)) {
      const candidate = {...data}; delete candidate[key];
      assert.throws(() => validateRecordStoreRecord(kind, candidate), undefined, `${kind}:${key}`);
    }
  }
});

test("TG-01 JSON-only encoding rejects duplicate and escaped duplicate keys, YAML, bad Unicode and limits", () => {
  for (const text of ['{"a":1,"a":2}\n', '{"a":1,"\\u0061":2}\n', '{"nested":{"a":1,"a":2}}\n',
    'a: 1\n', '{"a":NaN}\n', '{"a":1e999}\n', '{"a":"\\ud800"}\n', '{}', '\ufeff{}\n', '{}\r\n',
    '{"a":1,}\n', '/*comment*/{}\n', '['.repeat(33)+']'.repeat(33)+'\n']) {
    assert.throws(() => parseRecordStore("change", text));
  }
  assert.throws(() => parseRecordStore("change", Buffer.from([0xff, 0x0a])));
  assert.throws(() => parseRecordStore("change", " ".repeat(1024*1024)+"{}\n"));
  const r = fixtures().review;
  assert.throws(() => parseRecordStore("review", `---\n${JSON.stringify(r)}\n---\n\n`));
  assert.throws(() => parseRecordStore("review", encode("change", r)));
});

function fileSet() {
  const f = fixtures();
  return Object.fromEntries([["change.yaml","change"],["reviews/design-review.md","review"],["evidence.yaml","evidence"],
    ["material-decisions.md","decisions"],["verify-report.md","verify"]].map(([p,k])=>[root+p,encode(k,f[k])]));
}

test("TG-01 complete candidate references validate without requiring current reviewed subject bytes", () => {
  const files = fileSet(); const before = structuredClone(files);
  assert.doesNotThrow(() => validateRecordStoreSet("example", files));
  assert.deepEqual(files, before);
  // No model/proposal files are present: historical subjects are not current-set foreign keys.
  assert.equal(Object.keys(files).length, 5);
});

test("TG-01 candidate rejects dangling references, missing registry members and mismatched identity", () => {
  const original = fileSet();
  for (const filename of Object.keys(original).filter(p=>!p.endsWith("change.yaml"))) {
    const files = {...original}; delete files[filename];
    assert.throws(() => validateRecordStoreSet("example", files));
  }
  for (const mutate of [f=>f.change.applicability.pop(), f=>f.change.records.push(f.change.records[0]),
    f=>f.review.change_id="another", f=>f.review.id="another", f=>f.decisions.decisions[0].source_refs[0].id="missing",
    f=>f.change.models.push(f.change.models[0]), f=>f.review.findings.push(f.review.findings[0])]) {
    const f=fixtures(); mutate(f); const files=fileSet();
    for(const [p,k] of [["change.yaml","change"],["reviews/design-review.md","review"],["material-decisions.md","decisions"]]) files[root+p]=encode(k,f[k]);
    assert.throws(()=>validateRecordStoreSet("example",files));
  }
});

test("TG-01 blocker shape consistency is enforced without lifecycle eligibility", () => {
  const f=fixtures(); f.change.activity.status="completed";
  assert.doesNotThrow(()=>validateRecordStoreRecord("change",f.change)); // Open blocker does not block recording.
  f.change.blockers[0].state="resolved";
  assert.throws(()=>validateRecordStoreRecord("change",f.change));
});

test("TG-02 unsupported contracts, unsafe writes and non-absent creation reject without mutation", () => {
  for(const contract of ["compact-current-state-v1","stage-owned-change-local-v3","unknown_value"]) {
    const r=fixtures().request; r.contract=contract; const before=structuredClone(r);
    assert.throws(()=>validateRecordStoreRequest(encode("request",r))); assert.deepEqual(r,before);
  }
  for(const path of ["../outside","/tmp/outside","docs/changes/other/change.yaml",root+"arbitrary.md",root+"reviews/../change.yaml","a\\b","a\u0000b"]) {
    const r=fixtures().request;r.writes[0].path=path;
    assert.throws(()=>validateRecordStoreRequest(encode("request",r)));
  }
  const r=fixtures().request;
  assert.doesNotThrow(()=>validateRecordStoreCreation(r,false));
  assert.throws(()=>validateRecordStoreCreation(r,true));
  r.writes[0].expected_identity="sha256:"+"a".repeat(64);
  assert.throws(()=>validateRecordStoreCreation(r,false));
});

test("TG-07 public recorder requires explicit selectors and never supplies a root", () => {
  const result=spawnSync(process.execPath,[new URL("../dist/bin/rigorloop.js",import.meta.url).pathname,"record-store","record","--format","json"],{encoding:"utf8"});
  assert.equal(result.status,2);
  const payload=JSON.parse(result.stdout);
  assert.equal(payload.status,"rejected");
  assert.equal(payload.change_id,null);
  assert.equal(payload.claim,"storage-only");
  assert.deepEqual(payload.files,[]);
});

test("TG-01 exact file and stdin byte boundaries", () => {
  for (const [kind, limit] of [["change", 1024*1024], ["request", 8*1024*1024]]) {
    const content = encode(kind, fixtures()[kind]);
    const atLimit = content.slice(0, -1) + " ".repeat(limit - Buffer.byteLength(content)) + "\n";
    assert.equal(Buffer.byteLength(atLimit), limit);
    assert.doesNotThrow(() => parseRecordStore(kind, atLimit));
    assert.throws(() => parseRecordStore(kind, " " + atLimit), /byte limit/);
  }
});

test("TG-01 exact ID, path, registry, write and read count limits", () => {
  const f = fixtures();
  f.review.id = "a".repeat(80);
  assert.doesNotThrow(() => validateRecordStoreRecord("review", f.review));
  f.review.id += "a";
  assert.throws(() => validateRecordStoreRecord("review", f.review));
  f.change.proposal.path = "a".repeat(1024);
  assert.doesNotThrow(() => validateRecordStoreRecord("change", f.change));
  f.change.proposal.path += "a";
  assert.throws(() => validateRecordStoreRecord("change", f.change));
  const change = fixtures().change;
  change.records = Array.from({length:64}, (_,i) => ({path:root+`reviews/r-${i}.md`,kind:"review"}));
  change.applicability = change.records.map(r => ({...fixtures().change.applicability[0],path:r.path}));
  assert.doesNotThrow(() => validateRecordStoreRecord("change", change));
  const request = fixtures().request;
  request.writes = [{...request.writes[0],content:encode("change",change)}, ...change.records.map((r,i) => ({
    path:r.path,expected_identity:null,content:encode("review",{...fixtures().review,id:`r-${i}`}),
  }))];
  request.reads = Array.from({length:256},(_,i)=>({path:`docs/basis-${i}.md`,expected_identity:null}));
  assert.doesNotThrow(() => validateRecordStoreRecord("request", request));
  request.reads.push({path:"docs/excess.md",expected_identity:null});
  assert.throws(() => validateRecordStoreRecord("request", request));
  request.reads.pop();
  request.writes.push({...request.writes[1],path:root+"reviews/excess.md"});
  assert.throws(() => validateRecordStoreRecord("request", request));
  change.records.push({path:root+"reviews/excess.md",kind:"review"});
  change.applicability.push({...change.applicability[0],path:root+"reviews/excess.md"});
  assert.throws(() => validateRecordStoreRecord("change", change));
});

test("ER-M1-001 decision-basis and write paths are disjoint", () => {
  const request = fixtures().request;
  assert.doesNotThrow(() => validateRecordStoreRecord("request", request));
  request.reads = [{path:request.writes[0].path,expected_identity:null}];
  assert.throws(() => validateRecordStoreRecord("request", request), /overlap/);
});

test("ER-M1-002 distinct diagnostics may share a path or no path", () => {
  for (const path of [root+"evidence.yaml", null]) {
    const result = fixtures().result;
    result.observations = ["failed-evidence","subject-drift"].map(code => ({code,path,message:"Observed condition"}));
    assert.doesNotThrow(() => validateRecordStoreRecord("result", result));
    result.status = "rejected";
    result.errors = ["invalid-input","broken-reference"].map(code => ({code,path,message:"Invalid representation"}));
    assert.doesNotThrow(() => validateRecordStoreRecord("result", result));
  }
});

function inspected(files = fileSet()) {
  const records = Object.entries(files).sort(([a],[b])=>a < b ? -1 : a > b ? 1 : 0).map(([path,content])=>({path,content}));
  const identities = records.map(({path,content})=>({path,identity:content === null ? null : digest(content)}));
  return {...fixtures().result,operation:"inspect",status:"inspected",files:identities,snapshot:{records},
    revision:records.length ? digest(JSON.stringify(identities.map(f=>[f.path,f.identity]))) : null,
    observations:records.length ? records.filter(r=>r.content === null).map(r=>({code:"subject-drift",path:r.path,message:"Missing record"}))
      : [{code:"absent-change",path:null,message:"Absent root"}]};
}

test("ER-M1-003 inspect represents complete, absent and missing-sidecar snapshots", () => {
  const missing = fileSet(); missing[root+"evidence.yaml"] = null;
  for (const files of [fileSet(), {}, missing]) {
    const result = inspected(files);
    assert.doesNotThrow(() => validateRecordStoreRecord("result", result));
    assert.deepEqual(parseRecordStore("result", encode("result",result)), result);
  }
});

test("ER-M1-003 inspect rejects invalid content, membership and absent-root fields", () => {
  for (const content of ["not a manifest\n", null, " ".repeat(1024*1024)+encode("change",fixtures().change)]) {
    assert.throws(() => validateRecordStoreRecord("result", inspected({...fileSet(),[root+"change.yaml"]:content})));
  }
  const extra = {...fileSet(),[root+"reviews/extra.md"]:encode("review",{...fixtures().review,id:"extra"})};
  const omitted = fileSet(); delete omitted[root+"evidence.yaml"];
  const wrongChange = {...fileSet(),[root+"evidence.yaml"]:encode("evidence",{...fixtures().evidence,change_id:"another"})};
  const wrongReview = {...fileSet(),[root+"reviews/design-review.md"]:encode("review",{...fixtures().review,id:"another"})};
  for (const files of [extra,omitted,wrongChange,wrongReview]) assert.throws(() => validateRecordStoreRecord("result",inspected(files)));
  const missing = fileSet(); missing[root+"evidence.yaml"]=null;
  const noObservation = inspected(missing); noObservation.observations=[];
  assert.throws(() => validateRecordStoreRecord("result",noObservation));
  for (const mutate of [r=>r.revision=digest("wrong"),r=>r.observations=[]]) {
    const absent=inspected({}); mutate(absent);
    assert.throws(() => validateRecordStoreRecord("result",absent));
  }
  const wrongRevision=inspected(); wrongRevision.revision=digest("wrong");
  assert.throws(() => validateRecordStoreRecord("result",wrongRevision));
});

test("TG-01 duplicate keys are rejected in otherwise valid records", () => {
  const encoded = encode("change", fixtures().change);
  assert.doesNotThrow(() => parseRecordStore("change",encoded));
  for (const key of ['"schema_version"','"schema_\\u0076ersion"']) {
    assert.throws(() => parseRecordStore("change",encoded.replace('"schema_version":1',`"schema_version":1,${key}:1`)), /duplicate/);
  }
  const nested=encoded.replace('"stage":"design"','"stage":"design","stage":"design"');
  assert.notEqual(nested,encoded);
  assert.throws(() => parseRecordStore("change",nested), /duplicate/);
});

test("ER-M2-001 unavailable result selectors have only the empty input-rejection shape", () => {
  const rejected={...fixtures().result,status:"rejected",revision:null,files:[],observations:[],
    errors:[{code:"invalid-input",path:null,message:"Invalid command arguments"}]};
  for (const selectors of [{operation:null},{change_id:null},{operation:null,change_id:null}]) {
    const result={...rejected,...selectors};
    assert.doesNotThrow(()=>validateRecordStoreRecord("result",result));
    for (const mutate of [r=>r.status="saved",r=>r.errors=[],r=>r.errors[0].code="io-failure",r=>r.revision=digest("x"),r=>r.observations=fixtures().result.observations]) {
      const invalid=structuredClone(result); mutate(invalid);
      assert.throws(()=>validateRecordStoreRecord("result",invalid));
    }
  }
  for (const key of ["operation","change_id"]) assert.throws(()=>validateRecordStoreRecord("result",{...rejected,[key]:"unknown_value"}));
});
