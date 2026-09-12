import {spawnSync} from 'node:child_process';
import {parseV3Record,validateV3Record} from '../dist/lib/record-format-v3.js';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {test} from 'node:test';
import {digest} from '../dist/lib/record-store-files.js';
import {validateAdvancedResult} from '../dist/lib/record-store-format.js';
const fixtures=()=>JSON.parse(readFileSync(new URL('../../../tests/fixtures/rigorloop-records-v3/storage-safety.json',import.meta.url)));
const root='docs/changes/example/';
const encode=(kind,data)=>JSON.stringify(data)+'\n';
function fileSet(){const f=fixtures();return {[root+'change.json']:encode('change',f.change),...Object.fromEntries(f.change.records.map(r=>[r.path,encode(r.kind,f[r.kind])]))};}
test("ER-M1-002 distinct diagnostics may share a path or no path", () => {
  for (const path of [root+"evidence.json", null]) {
    const result = fixtures().result;
    result.observations = ["failed-evidence","subject-drift"].map(code => ({code,path,message:"Observed condition"}));
    assert.doesNotThrow(() => validateAdvancedResult( result));
    result.status = "rejected";
    result.errors = ["invalid-input","broken-reference"].map(code => ({code,path,message:"Invalid representation"}));
    assert.doesNotThrow(() => validateAdvancedResult( result));
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
  const missing = fileSet(); missing[root+"evidence.json"] = null;
  for (const files of [fileSet(), {}, missing]) {
    const result = inspected(files);
    assert.doesNotThrow(() => validateAdvancedResult( result));
  }
});

test("ER-M1-003 inspect rejects invalid content, membership and absent-root fields", () => {
  for (const content of ["not a manifest\n", null, " ".repeat(1024*1024)+encode("change",fixtures().change)]) {
    assert.throws(() => validateAdvancedResult( inspected({...fileSet(),[root+"change.json"]:content})));
  }
  const extra = {...fileSet(),[root+"reviews/extra.json"]:encode("review",{...fixtures().review,id:"extra"})};
  const omitted = fileSet(); delete omitted[root+"evidence.json"];
  const wrongChange = {...fileSet(),[root+"evidence.json"]:encode("evidence",{...fixtures().evidence,change_id:"another"})};
  const wrongReview = {...fileSet(),[root+"reviews/design-review.json"]:encode("review",{...fixtures().review,id:"another"})};
  for (const files of [extra,omitted,wrongChange,wrongReview]) assert.throws(() => validateAdvancedResult(inspected(files)));
  const missing = fileSet(); missing[root+"evidence.json"]=null;
  const noObservation = inspected(missing); noObservation.observations=[];
  assert.throws(() => validateAdvancedResult(noObservation));
  for (const mutate of [r=>r.revision=digest("wrong"),r=>r.observations=[]]) {
    const absent=inspected({}); mutate(absent);
    assert.throws(() => validateAdvancedResult(absent));
  }
  const wrongRevision=inspected(); wrongRevision.revision=digest("wrong");
  assert.throws(() => validateAdvancedResult(wrongRevision));
});

test("ER-M2-001 unavailable result selectors have only the empty input-rejection shape", () => {
  const rejected={...fixtures().result,status:"rejected",revision:null,files:[],observations:[],
    errors:[{code:"invalid-input",path:null,message:"Invalid command arguments"}]};
  for (const selectors of [{operation:null},{change_id:null},{operation:null,change_id:null}]) {
    const result={...rejected,...selectors};
    assert.doesNotThrow(()=>validateAdvancedResult(result));
    for (const mutate of [r=>r.status="saved",r=>r.errors=[],r=>r.errors[0].code="io-failure",r=>r.revision=digest("x"),r=>r.observations=fixtures().result.observations]) {
      const invalid=structuredClone(result); mutate(invalid);
      assert.throws(()=>validateAdvancedResult(invalid));
    }
  }
  for (const key of ["operation","change_id"]) assert.throws(()=>validateAdvancedResult({...rejected,[key]:"unknown_value"}));
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
    assert.doesNotThrow(() => parseV3Record(kind, atLimit));
    assert.throws(() => parseV3Record(kind, " " + atLimit), /byte limit/);
  }
});

test("TG-01 exact ID, path, registry, write and read count limits", () => {
  const f = fixtures();
  f.review.id = "a".repeat(80);
  assert.doesNotThrow(() => validateV3Record("review", f.review));
  f.review.id += "a";
  assert.throws(() => validateV3Record("review", f.review));
  f.change.proposal.path = "a".repeat(1024);
  assert.doesNotThrow(() => validateV3Record("change", f.change));
  f.change.proposal.path += "a";
  assert.throws(() => validateV3Record("change", f.change));
  const change = fixtures().change;
  change.records = Array.from({length:64}, (_,i) => ({path:root+`reviews/r-${i}.json`,kind:"review"}));
  change.applicability = change.records.map(r => ({...fixtures().change.applicability[0],path:r.path}));
  assert.doesNotThrow(() => validateV3Record("change", change));
  const request = fixtures().request;
  request.writes = [{...request.writes[0],content:encode("change",change)}, ...change.records.map((r,i) => ({
    path:r.path,expected_identity:null,content:encode("review",{...fixtures().review,id:`r-${i}`}),
  }))];
  request.reads = Array.from({length:256},(_,i)=>({path:`docs/basis-${i}.json`,expected_identity:null}));
  assert.doesNotThrow(() => validateV3Record("request", request));
  request.reads.push({path:"docs/excess.json",expected_identity:null});
  assert.throws(() => validateV3Record("request", request));
  request.reads.pop();
  request.writes.push({...request.writes[1],path:root+"reviews/excess.json"});
  assert.throws(() => validateV3Record("request", request));
  change.records.push({path:root+"reviews/excess.json",kind:"review"});
  change.applicability.push({...change.applicability[0],path:root+"reviews/excess.json"});
  assert.throws(() => validateV3Record("change", change));
});

test("ER-M1-001 decision-basis and write paths are disjoint", () => {
  const request = fixtures().request;
  assert.doesNotThrow(() => validateV3Record("request", request));
  request.reads = [{path:request.writes[0].path,expected_identity:null}];
  assert.throws(() => validateV3Record("request", request), /overlap/);
});
