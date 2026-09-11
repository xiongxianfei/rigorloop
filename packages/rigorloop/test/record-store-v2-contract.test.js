import assert from "node:assert/strict";
import {test} from "node:test";
import {readFileSync, mkdtempSync, mkdirSync, writeFileSync, rmSync, symlinkSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, dirname} from "node:path";
import {spawnSync} from "node:child_process";
import {
  RECORDS_V2_SCHEMA, validateV2Record, parseV2Record, validateV2Set,
  validateV2Preservation, validateV2Creation, v2PathKind,
} from "../dist/lib/record-format-v2.js";

const root = "docs/changes/example/";
const encode = x => JSON.stringify(x) + "\n";
const fixture = () => JSON.parse(readFileSync(new URL("../../../tests/fixtures/rigorloop-records-v2/records.json", import.meta.url)));
const files = () => {
  const f = fixture();
  return Object.fromEntries(["change", ...f.change.records.map(r => r.kind)].map(kind => [
    kind === "change" ? root+"change.json" : f.change.records.find(r=>r.kind===kind).path, encode(f[kind]),
  ]));
};
const reject = (fn, code="invalid-input") => assert.throws(fn, e=>e.recordStoreCode===code);

test("TG-01 v2 complete fixtures and packaged templates validate without mutation", () => {
  const f=fixture();
  for (const [kind, value] of Object.entries(f)) {
    const before=encode(value);
    assert.deepEqual(parseV2Record(kind, before),value);
    assert.equal(encode(value),before);
  }
  assert.equal(validateV2Set("example",files()).size,5);
  const templates=JSON.parse(readFileSync(new URL("../../../templates/rigorloop-records-v2/records.json",import.meta.url)));
  for(const [kind,value] of Object.entries(templates)) validateV2Record(kind,value);
  for(const path of ["schemas/rigorloop-records-v2.schema.json","templates/rigorloop-records-v2/records.json"]) {
    assert.deepEqual(readFileSync(new URL("../../../"+path,import.meta.url)),readFileSync(new URL("../dist/"+path,import.meta.url)));
  }
});

test("TG-01 unknown_value closed vocabularies fail before consistency", () => {
  const f=fixture();
  const cases=[
    ["change",x=>x.contract="unknown_value"],["change",x=>x.schema_version=99],
    ["change",x=>x.activity.stage="unknown_value"],["change",x=>x.activity.status="unknown_value"],
    ["change",x=>x.activity.owner.role="unknown_value"],["change",x=>x.records[0].kind="unknown_value"],
    ["change",x=>x.applicability[0].value="unknown_value"],["review",x=>x.target="unknown_value"],
    ["review",x=>x.judgment="unknown_value"],["review",x=>x.findings[0].state="unknown_value"],
    ["evidence",x=>x.checks[0].result="unknown_value"],["verify",x=>x.outcome="unknown_value"],
    ["request",x=>x.schema_version=1],["review",x=>x.findings[0].origin.supporting_judgment.judgment="unknown_value"],
  ];
  for(const [kind,mutate]of cases) {
    const value=structuredClone(f[kind]);mutate(value);
    assert.throws(()=>validateV2Record(kind,value),e=>["invalid-input","unsupported-contract"].includes(e.recordStoreCode));
  }
  reject(()=>validateV2Record("unknown_value",{}));
  assert.ok(RECORDS_V2_SCHEMA.$defs.origin);
});

test("TG-01 plain JSON rejects front matter trailing narrative duplicate keys and invalid encoding", () => {
  const text=encode(fixture().review);
  for(const bad of ["---\n"+text+"---\nbody\n",text+"body\n",text.slice(0,-1),"\ufeff"+text,text.replace("\n","\r\n"),text.replace('"id":','"id":"duplicate","id":')])
    reject(()=>parseV2Record("review",bad));
  reject(()=>parseV2Record("review",Buffer.from([0xff,10])));
  for(const body of [null,"",4]) {const r=fixture().review;r.body=body;reject(()=>validateV2Record("review",r));}
  const r=fixture().review;r.body='Quoted "text"\nUnicode 确认 and \\ escapes';
  assert.equal(parseV2Record("review",encode(r)).body,r.body);
  r.extra=true;reject(()=>validateV2Record("review",r));
});

test("TG-01 byte/depth/path limits and JSON domain reject", () => {
  const r=fixture().review;r.body="a".repeat(1024*1024);
  reject(()=>parseV2Record("review",encode(r)),"limit-exceeded");
  reject(()=>parseV2Record("review","[".repeat(33)+"]".repeat(33)+"\n"),"limit-exceeded");
  for(const p of ["../escape","/absolute","C:/escape","a\\b","a//b","a/./b","x".repeat(1025)])
    reject(()=>v2PathKind("example",p),"unsafe-path");
  const r2=fixture().review;r2.body="\ud800";reject(()=>validateV2Record("review",r2));
});

test("TG-01 namespaces reject wrong extensions dual manifests mixed versions and wrong review id", () => {
  reject(()=>v2PathKind("example",root+"evidence.yaml"),"unsafe-path");
  const dual=files();dual[root+"change.yaml"]=dual[root+"change.json"];
  reject(()=>validateV2Set("example",dual));
  const f=files();const r=fixture().review;r.schema_version=1;f[root+"reviews/design-review.json"]=encode(r);
  reject(()=>validateV2Set("example",f),"unsupported-contract");
  r.schema_version=2;r.id="other";f[root+"reviews/design-review.json"]=encode(r);
  reject(()=>validateV2Set("example",f));
});

test("TG-01 disjoint referenceable ids reject even without a reference", () => {
  const c=fixture().change;
  c.work.push({id:c.models[0].id,status:"pending",owner:c.activity.owner,requirement_refs:[]});
  reject(()=>validateV2Record("change",c));
  const r=fixture().review;r.findings[0].id=r.id;reject(()=>validateV2Record("review",r));
});

test("TG-01 every EntryRef field resolves only its permitted collection", () => {
  const reviewPath=root+"reviews/design-review.json", ev=root+"evidence.json";
  const cases=[
    ["review",r=>r.findings[0].resolution.evidence_refs,reviewPath],
    ["change",r=>r.blockers[0].resolution.evidence_refs,root+"change.json"],
    ["verify",r=>r.evidence_refs,root+"verify-report.json"],
    ["verify",r=>r.review_refs,root+"verify-report.json"],
    ["decisions",r=>r.decisions[0].source_refs,root+"material-decisions.json"],
  ];
  for(const [kind,refs,path]of cases) {
    const f=fixture(), map=files(), r=f[kind];
    assert.doesNotThrow(()=>validateV2Set("example",map));
    const list=refs(r);list.splice(0,list.length,{path:ev,id:"missing"});map[path]=encode(r);
    reject(()=>validateV2Set("example",map),"broken-reference");
  }
  const f=files(),v=fixture().verify;
  v.review_refs=[{path:reviewPath,id:"finding-1"}];f[root+"verify-report.json"]=encode(v);
  reject(()=>validateV2Set("example",f),"broken-reference");
  v.review_refs=[{path:reviewPath,id:"design-review"}];v.evidence_refs=[{path:reviewPath,id:"design-review"}];f[root+"verify-report.json"]=encode(v);
  reject(()=>validateV2Set("example",f),"broken-reference");
});

test("TG-01 source references cover manifest collections review root findings checks and decisions", () => {
  const f=fixture(),map=files(),d=f.decisions;
  d.decisions[0].source_refs=[
    ...["model-1","work-1","blocker-1"].map(id=>({path:root+"change.json",id})),
    ...["design-review","finding-1"].map(id=>({path:root+"reviews/design-review.json",id})),
    {path:root+"evidence.json",id:"check-1"},{path:root+"material-decisions.json",id:"decision-1"},
  ];
  map[root+"material-decisions.json"]=encode(d);
  assert.doesNotThrow(()=>validateV2Set("example",map)); // Self-link is not recursive evaluation.
  for(const ref of [{path:root+"verify-report.json",id:"example"},{path:root+"change.json",id:"example"},{path:"docs/changes/other/evidence.json",id:"check-1"}]) {
    d.decisions[0].source_refs=[ref];map[root+"material-decisions.json"]=encode(d);
    reject(()=>validateV2Set("example",map),"broken-reference");
  }
});

test("TG-01 registry applicability duplicates and final candidate references", () => {
  for(const mutate of [c=>c.applicability.pop(),c=>c.records[0].kind="evidence",c=>c.records.push(c.records[0])]) {
    const c=fixture().change;mutate(c);reject(()=>validateV2Record("change",c));
  }
  const map=files();delete map[root+"evidence.json"];reject(()=>validateV2Set("example",map),"broken-reference");
  map[root+"evidence.json"]=encode(fixture().evidence);assert.doesNotThrow(()=>validateV2Set("example",map));
});

test("TG-01 origin required and preserved through current changes and resolved state", () => {
  for(const mutate of [r=>delete r.findings[0].origin,r=>r.findings[0].origin=null]) {
    const r=fixture().review;mutate(r);reject(()=>validateV2Record("review",r));
  }
  const before=files(),after=files(),path=root+"reviews/design-review.json",r=fixture().review;
  r.findings[0].evidence="Current evidence updated";r.judgment="approved";after[path]=encode(r);
  assert.doesNotThrow(()=>validateV2Preservation("example",before,after));
  r.findings[0].origin.rationale="rewritten";after[path]=encode(r);
  reject(()=>validateV2Preservation("example",before,after));
  r.findings=[];after[path]=encode(r);
  const decisions=fixture().decisions;decisions.decisions[0].source_refs=[];after[root+"material-decisions.json"]=encode(decisions);
  reject(()=>validateV2Preservation("example",before,after));
  const absent=fixture().review;absent.findings[0].origin.supporting_judgment=null;assert.doesNotThrow(()=>validateV2Record("review",absent));
});

test("TG-01 v2 advanced request validates candidate bytes and explicit absent creation", () => {
  const request=fixture().request;
  assert.doesNotThrow(()=>validateV2Creation(request,false));
  reject(()=>validateV2Creation(request,true));
  request.reads=[{path:request.writes[0].path,expected_identity:null}];reject(()=>validateV2Record("request",request));
});

test("TG-01 model stored examples parse and reassessment retains origin", () => {
  for(const name of ["v2-minimal-change/change.json","v2-review-without-subjects/review.json","v2-review-reassessment/before.json","v2-review-reassessment/after.json"]) {
    const x=readFileSync(new URL("../../../docs/design/record-format/examples/"+name,import.meta.url));
    parseV2Record(name==="v2-minimal-change/change.json"?"change":"review",x);
  }
});

test("TG-01 standalone v2 validation is read-only and rejects symlink/mixed manifests", () => {
  const dir=mkdtempSync(join(tmpdir(),"records-v2-"));
  try {
    const map=files();
    for(const [path,content] of Object.entries(map)) {mkdirSync(dirname(join(dir,path)),{recursive:true});writeFileSync(join(dir,path),content);}
    const script=new URL("../../../scripts/validate-record-store.mjs",import.meta.url);
    const run=()=>spawnSync(process.execPath,[script.pathname,join(dir,root+"change.json")],{encoding:"utf8"});
    assert.equal(run().status,0);
    for(const [path,content]of Object.entries(map))assert.equal(readFileSync(join(dir,path),"utf8"),content);
    writeFileSync(join(dir,root+"change.yaml"),"{}\n");assert.notEqual(run().status,0);
    rmSync(join(dir,root+"change.yaml"));
    const ev=join(dir,root+"evidence.json");rmSync(ev);symlinkSync(join(dir,root+"change.json"),ev);assert.notEqual(run().status,0);
  } finally {rmSync(dir,{recursive:true,force:true});}
});


test("TG-01 unknown_value regression reaches every stored and request vocabulary occurrence", () => {
  const cases=fixture(), covered=new Set();
  function walk(schema,value,path,kind) {
    if(schema.$ref) return walk(RECORDS_V2_SCHEMA.$defs[schema.$ref.split("/").at(-1)],value,path,kind);
    if(schema.anyOf) {
      const branch=schema.anyOf.find(x=>value===null?x.type==="null":x.type!=="null");
      return walk(branch,value,path,kind);
    }
    if(schema.enum || Object.hasOwn(schema,"const")) {
      const candidate=structuredClone(cases[kind]);let target=candidate;
      for(const key of path.slice(0,-1)) target=target[key];
      target[path.at(-1)]="unknown_value";
      assert.throws(()=>validateV2Record(kind,candidate),e=>["invalid-input","unsupported-contract"].includes(e.recordStoreCode),`${kind}.${path.join(".")}`);
      covered.add(kind+"."+path.join("."));
    }
    if(schema.type==="object") for(const [key,child] of Object.entries(schema.properties)) walk(child,value[key],[...path,key],kind);
    if(schema.type==="array") value.forEach((entry,index)=>walk(schema.items,entry,[...path,index],kind));
  }
  for(const [kind,value] of Object.entries(cases)) walk(RECORDS_V2_SCHEMA.$defs[kind],value,[],kind);
  assert.ok(covered.size>35);
});

test("TG-01 nested optional references retain unsafe-path diagnostics", () => {
  const review=fixture().review;
  review.findings[0].resolution.evidence_refs[0].path="../escape";
  reject(()=>validateV2Record("review",review),"unsafe-path");
  review.findings[0].resolution.evidence_refs[0].path=root+"evidence.json";
  review.findings[0].origin.supporting_judgment.subjects[0].path="../escape";
  reject(()=>validateV2Record("review",review),"unsafe-path");
});

test("TG-01 either manifest entry rejects dual manifests live and at an exact Git snapshot", () => {
  const dir=mkdtempSync(join(tmpdir(),"records-dispatch-"));
  try {
    mkdirSync(join(dir,root),{recursive:true});
    writeFileSync(join(dir,root+"change.yaml"),"Uninterpreted archival bytes\n");
    writeFileSync(join(dir,root+"change.json"),encode(JSON.parse(readFileSync(new URL("../../../templates/rigorloop-records-v2/records.json",import.meta.url))).change));
    const git=args=>{const r=spawnSync("git",["-C",dir,...args],{encoding:"utf8"});assert.equal(r.status,0,r.stderr);return r.stdout.trim();};
    git(["init","-q"]);git(["add","docs"]);
    git(["-c","user.name=Fixture","-c","user.email=fixture@example.invalid","-c","commit.gpgsign=false","commit","-qm","Fixture"]);
    const revision=git(["rev-parse","HEAD"]);
    for(const name of ["change.yaml","change.json"]) for(const suffix of [[],["--revision",revision]]) {
      const r=spawnSync(process.execPath,[new URL("../../../scripts/validate-record-store.mjs",import.meta.url).pathname,join(dir,root+name),...suffix],{encoding:"utf8"});
      assert.notEqual(r.status,0,`${name} ${suffix.join(" ")}`);
    }
  } finally {rmSync(dir,{recursive:true,force:true});}
});

test("TG-01 preservation permits repair of missing members and broken prior refs", () => {
  const after=files(),before=files();delete before[root+"evidence.json"];
  assert.doesNotThrow(()=>validateV2Preservation("example",before,after));
  before[root+"evidence.json"]=null;
  assert.doesNotThrow(()=>validateV2Preservation("example",before,after));
  const broken=files(),review=fixture().review;
  review.findings[0].resolution.evidence_refs[0].id="missing";
  broken[root+"reviews/design-review.json"]=encode(review);
  assert.doesNotThrow(()=>validateV2Preservation("example",broken,after));
  review.findings[0].origin=null;broken[root+"reviews/design-review.json"]=encode(review);
  reject(()=>validateV2Preservation("example",broken,after));
  const removed=files(),manifest=fixture().change;
  manifest.records=manifest.records.filter(x=>x.kind!=="verify");
  manifest.applicability=manifest.applicability.filter(x=>x.path!==root+"verify-report.json");
  removed[root+"change.json"]=encode(manifest);delete removed[root+"verify-report.json"];
  before[root+"verify-report.json"]=null;
  reject(()=>validateV2Preservation("example",before,removed));
});


test("TG-01 unknown_value version and contract pairs reject unsupported-contract", () => {
  for(const [kind,value] of Object.entries(fixture())) {
    value.schema_version=99;reject(()=>validateV2Record(kind,value),"unsupported-contract");
    value.schema_version=1;reject(()=>validateV2Record(kind,value),"unsupported-contract");
  }
  for(const kind of ["change","request"]) {
    const value=fixture()[kind];value.contract="explicit-recording-v1";
    reject(()=>validateV2Record(kind,value),"unsupported-contract");
  }
});
