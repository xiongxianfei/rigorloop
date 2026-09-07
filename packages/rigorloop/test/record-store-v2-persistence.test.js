import assert from "node:assert/strict";
import {test} from "node:test";
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,rmSync,existsSync,unlinkSync,symlinkSync,linkSync,renameSync} from "node:fs";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {spawnSync} from "node:child_process";
import {executeRecordStoreCli} from "../dist/lib/record-store-cli.js";
import {RecordFiles,digest} from "../dist/lib/record-store-files.js";
import {validateAdvancedResult} from "../dist/lib/record-store-format.js";

const prefix="docs/changes/example/", manifest=prefix+"change.json", review=prefix+"reviews/design-review.json", evidence=prefix+"evidence.json";
const encode=x=>JSON.stringify(x)+"\n";
const fixture=()=>JSON.parse(readFileSync(new URL("../../../tests/fixtures/rigorloop-records-v2/records.json",import.meta.url)));
function setup(t) {const root=mkdtempSync(join(tmpdir(),"record-v2-persistence-"));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,"docs/changes"),{recursive:true});return root;}
const argv=(root,op,extra=[])=>[op,"--root",root,"--change","example","--format","json",...(["check","record"].includes(op)?["--input","-"]:[]),...extra];
function run(root,op,request,options={},extra=[]) {const x=executeRecordStoreCli(argv(root,op,extra),{...options,input:request?encode(request):undefined});validateAdvancedResult(x.result);return x.result;}
function create(root) {const r=fixture().request;assert.equal(run(root,"record",r).status,"saved");return r;}
function update(root) {const s=run(root,"inspect");assert.equal(s.status,"inspected");const r=fixture().request;r.expected_revision=s.revision;r.writes=s.snapshot.records.map(x=>({path:x.path,expected_identity:digest(x.content),content:x.content}));return r;}
function edit(r,path,fn) {const w=r.writes.find(x=>x.path===path),v=JSON.parse(w.content);fn(v);w.content=encode(v);}
const recover=(root,s,action,options={})=>run(root,"recover",undefined,options,["--transaction",s.transaction.id,"--expected-recovery",s.transaction.recovery_identity,"--action",action]);
function sameBytes(root,request) {for(const w of request.writes)assert.equal(readFileSync(join(root,w.path),"utf8"),w.content);}

test("TG-02 v2 advanced public check/create/inspect retains version-1 storage envelope and exact bytes",t=>{
 const root=setup(t),r=fixture().request;
 assert.equal(run(root,"check",r).status,"valid");assert.equal(existsSync(join(root,".rigorloop")),false);
 const bin=new URL("../dist/bin/rigorloop.js",import.meta.url).pathname;
 for(const op of ["record","inspect"]) {
  const child=spawnSync(process.execPath,[bin,"record-store",...argv(root,op)],{encoding:"utf8",input:op==="record"?encode(r):undefined});
  assert.equal(child.status,0,child.stdout+child.stderr);const result=JSON.parse(child.stdout);validateAdvancedResult(result);assert.equal(result.schema_version,1);assert.equal(result.claim,"storage-only");
 }
 sameBytes(root,r);assert.equal(existsSync(join(root,prefix+"change.yaml")),false);
 const s=run(root,"inspect");assert.equal(s.snapshot.records.length,5);assert.ok(s.observations.some(o=>o.code==="failed-evidence"));
 const bad=structuredClone(s);bad.snapshot.records[0].content+=" ";assert.throws(()=>validateAdvancedResult(bad));
});

test("TG-02 v2 stale revision target/read basis and lost-success retry never merge",t=>{
 const root=setup(t),r=create(root);assert.equal(run(root,"record",r).status,"conflict");
 const next=update(root);assert.equal(run(root,"record",next).status,"unchanged");
 next.writes[0].expected_identity=null;assert.equal(run(root,"record",next).status,"conflict");
 const fresh=update(root);writeFileSync(join(root,"basis"),"new");fresh.reads=[{path:"basis",expected_identity:digest("old")}];
 assert.equal(run(root,"record",fresh).status,"conflict");sameBytes(root,r);
});

test("TG-02 advanced origin preservation and missing evidence restoration share candidate validation",t=>{
 const root=setup(t);create(root);const r=update(root);edit(r,review,x=>x.findings[0].origin.rationale="rewrite");
 assert.equal(run(root,"check",r).errors[0].code,"invalid-input");assert.equal(run(root,"record",r).status,"rejected");
 unlinkSync(join(root,evidence));const s=run(root,"inspect");assert.equal(s.snapshot.records.find(x=>x.path===evidence).content,null);
 const repair=fixture().request;repair.expected_revision=s.revision;repair.writes=repair.writes.filter(w=>w.path===evidence);
 assert.equal(run(root,"record",repair).status,"saved");
 const correction=update(root);edit(correction,review,x=>{x.judgment="approved";x.body="New explicit judgment";});assert.equal(run(root,"record",correction).status,"saved");
});

for(const phase of ["after-preparation","after-replace:0","before-commit","after-commit"]) for(const action of ["restore","complete"]) test(`TG-02 v2 ${phase} interruption ${action} preserves exact coherent state`,t=>{
 const root=setup(t),before=create(root),r=update(root);edit(r,manifest,x=>x.activity.reason="Correction");edit(r,evidence,x=>x.checks[0].summary="New observed result");
 const stopped=run(root,"record",r,{fault:p=>p===phase?"crash":undefined});assert.equal(stopped.status,"recovery-required");
 assert.equal(run(root,"inspect").snapshot,null);
 const result=recover(root,stopped,action);
 if(phase==="after-commit"&&action==="restore") {assert.equal(result.status,"recovery-required");sameBytes(root,r);return;}
 assert.equal(result.status,"recovered");sameBytes(root,action==="complete"?r:before);assert.equal(run(root,"inspect").status,"inspected");
});

for(const action of ["complete","restore"]) test(`TG-02 absent v2 creation crash recovers ${action} through subprocess`,t=>{
 const root=setup(t),r=fixture().request,launcher=new URL("./helpers/record-store-launcher.mjs",import.meta.url).pathname;
 const child=spawnSync(process.execPath,[launcher,"record-store",...argv(root,"record")],{input:encode(r),encoding:"utf8",env:{...process.env,RIGORLOOP_TEST_RECORD_FAULT:"after-replace:0"}});
 assert.equal(child.status,99,child.stdout);const stopped=run(root,"inspect");assert.equal(stopped.status,"recovery-required");
 const result=recover(root,stopped,action);assert.equal(result.status,"recovered");
 if(action==="complete")sameBytes(root,r);else assert.equal(existsSync(join(root,prefix)),false);
});

test("TG-02 v2 readers and mixed-version contenders share writer exclusion",t=>{
 const root=setup(t),r=fixture().request;let reached=false;
 const bin=new URL("../dist/bin/rigorloop.js",import.meta.url).pathname;
 const result=run(root,"record",r,{fault:p=>{if(p!=="after-preparation")return;reached=true;
  for(const op of ["inspect","record"])for(const version of [1,2]) {
   const request=version===2?r:JSON.parse(readFileSync(new URL("../../../tests/fixtures/explicit-recording-v1/records.json",import.meta.url))).request;
   const child=spawnSync(process.execPath,[bin,"record-store",...argv(root,op)],{encoding:"utf8",input:op==="record"?encode({...request,reads:[]}):undefined});
   assert.equal(child.status,4,child.stdout);assert.equal(JSON.parse(child.stdout).snapshot,null);
  }
 }});assert.ok(reached);assert.equal(result.status,"saved");sameBytes(root,r);
});

test("TG-02 observed v2 basis drift after publication restores before bytes",t=>{
 const root=setup(t),before=create(root),r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");writeFileSync(join(root,"basis"),"before");r.reads=[{path:"basis",expected_identity:digest("before")}];
 const result=run(root,"record",r,{fault:p=>{if(p==="before-commit")writeFileSync(join(root,"basis"),"after");}});
 assert.equal(result.status,"conflict");sameBytes(root,before);assert.equal(readFileSync(join(root,"basis"),"utf8"),"after");
});

for(const mutate of [j=>j.version=99,j=>j.phase="unknown_value",j=>{const x=JSON.parse(j.candidate[review].content);x.findings[0].origin.rationale="tampered";j.candidate[review].content=encode(x);j.candidate[review].identity=digest(j.candidate[review].content);}]) test("TG-02 unknown_value or rewritten-origin recovery journal fails closed",t=>{
 const root=setup(t),before=create(root),r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");
 const stopped=run(root,"record",r,{fault:p=>p==="after-preparation"?"crash":undefined});
 const path=join(root,".rigorloop/record-store/example/journal.json"),j=JSON.parse(readFileSync(path));mutate(j);writeFileSync(path,encode(j));stopped.transaction.recovery_identity=digest(readFileSync(path));
 assert.equal(recover(root,stopped,"complete").status,"recovery-required");sameBytes(root,before);
});

for(const fault of ["symlink","hardlink","ancestor","EACCES","ENOSPC"]) test(`TG-02 v2 ${fault} cannot overwrite unsafe or failed targets`,t=>{
 const root=setup(t),r=create(root),next=update(root);edit(next,evidence,x=>x.checks[0].summary="candidate");
 if(fault==="symlink"||fault==="hardlink") {writeFileSync(join(root,"outside"),"outside");unlinkSync(join(root,evidence));(fault==="symlink"?symlinkSync:linkSync)(join(root,"outside"),join(root,evidence));assert.equal(run(root,"record",next).errors[0].code,"unsafe-path");assert.equal(readFileSync(join(root,"outside"),"utf8"),"outside");}
 else if(fault==="ancestor") {mkdirSync(join(root,"outside"));writeFileSync(join(root,"outside/evidence.json"),"outside");const x=run(root,"record",next,{fault:p=>{if(p==="before-replace:0"){renameSync(join(root,prefix),join(root,"aside"));symlinkSync(join(root,"outside"),join(root,prefix));}}});assert.equal(x.status,"recovery-required");assert.equal(readFileSync(join(root,"outside/evidence.json"),"utf8"),"outside");}
 else {const write=RecordFiles.prototype.write;RecordFiles.prototype.write=function(path,...args){if(path===evidence)throw Object.assign(new Error("private"),{code:fault});return write.call(this,path,...args);};try{assert.equal(run(root,"record",next).errors[0].code,"io-failure");}finally{RecordFiles.prototype.write=write;}sameBytes(root,r);}
});

test("TG-02 dual manifests and cross-contract writes never migrate roots",t=>{
 const root=setup(t);create(root);const legacy=JSON.parse(readFileSync(new URL("../../../tests/fixtures/explicit-recording-v1/records.json",import.meta.url))).request;legacy.reads=[];
 assert.equal(run(root,"record",legacy).status,"conflict");
 const r=update(root);writeFileSync(join(root,prefix+"change.yaml"),"{}\n");
 for(const op of ["inspect","check","record"])assert.equal(run(root,op,op==="inspect"?undefined:r).errors[0].code,"invalid-input");
});

test("TG-02 standalone v2 validation cannot read through an unfinished transaction",t=>{
 const root=setup(t);create(root);const r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");
 const stopped=run(root,"record",r,{fault:p=>p==="after-replace:0"?"crash":undefined});assert.equal(stopped.status,"recovery-required");
 const child=spawnSync(process.execPath,[new URL("../../../scripts/validate-record-store.mjs",import.meta.url).pathname,join(root,manifest)],{encoding:"utf8"});
 assert.notEqual(child.status,0);
});

test("TG-02 completed v2 save performs no fallible diagnostic reads after commit",t=>{
 const root=setup(t);create(root);const r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");
 const hash=RecordFiles.prototype.hash;let committed=false,lateReads=0;
 RecordFiles.prototype.hash=function(path,...args){if(committed && path==="docs/proposals/example.md")lateReads++;return hash.call(this,path,...args);};
 let result;try {result=run(root,"record",r,{fault:p=>{if(p==="after-commit")committed=true;}});}finally{RecordFiles.prototype.hash=hash;}
 assert.equal(result.status,"saved");sameBytes(root,r);assert.equal(lateReads,0);
});

for(const operation of ["record","recover"]) test(`TG-02 ${operation} prepares its storage receipt before publication`,t=>{
 const root=setup(t),before=create(root),r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");
 let stopped;
 if(operation==="recover") stopped=run(root,"record",r,{fault:p=>p==="after-preparation"?"crash":undefined});
 const result=operation==="record"?run(root,"record",r,{fault:p=>p==="before-result"?"fail":undefined}):recover(root,stopped,"complete",{fault:p=>p==="before-result"?"fail":undefined});
 assert.equal(result.status,operation==="record"?"rejected":"recovery-required");sameBytes(root,before);
});

for(const phase of ["after-lock","after-preparation","after-replace:1"]) test(`TG-02 absent root ownership and late counterpart at ${phase} never overwrite external state`,t=>{
 const root=setup(t),r=fixture().request;let external;
 const result=run(root,"record",r,{fault:p=>{if(p===phase){mkdirSync(join(root,prefix),{recursive:true});external=join(root,prefix+"change.yaml");writeFileSync(external,"external\n");}}});
 assert.notEqual(result.status,"saved");assert.equal(readFileSync(external,"utf8"),"external\n");
});

test("TG-02 recovery cannot overwrite a third state or use a stale recovery identity",t=>{
 const root=setup(t);create(root);const r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");
 const stopped=run(root,"record",r,{fault:p=>p==="after-replace:0"?"crash":undefined});
 const stale=structuredClone(stopped);stale.transaction.recovery_identity=digest("old");assert.equal(recover(root,stale,"complete").status,"recovery-required");
 writeFileSync(join(root,evidence),"external\n");
 for(const action of ["complete","restore"])assert.equal(recover(root,stopped,action).status,"recovery-required");
 assert.equal(readFileSync(join(root,evidence),"utf8"),"external\n");
});

test("TG-02 overlapping completed writer makes inspection conflict without a mixed snapshot",t=>{
 const root=setup(t);create(root);const r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");
 const result=run(root,"inspect",undefined,{fault:p=>{if(p==="during-inspect")assert.equal(run(root,"record",r).status,"saved");}});
 assert.equal(result.status,"conflict");assert.equal(result.snapshot,null);sameBytes(root,r);
});

test("TG-02 failure writing exclusion epoch releases the owned lock before returning",t=>{
 const root=setup(t),write=RecordFiles.prototype.write;
 RecordFiles.prototype.write=function(path,...args){if(path.endsWith("/epoch"))throw Object.assign(new Error("private"),{code:"EIO"});return write.call(this,path,...args);};
 try{assert.equal(run(root,"record",fixture().request).errors[0].code,"io-failure");}finally{RecordFiles.prototype.write=write;}
 assert.equal(run(root,"inspect").status,"inspected");assert.equal(existsSync(join(root,manifest)),false);
});

test("TG-02 malformed advanced requests and unknown_value version pairs reject precisely",t=>{
 const root=setup(t);
 for(const input of [null,{},[],{schema_version:2},{contract:"rigorloop-records-v2"}]) {
  const x=executeRecordStoreCli(argv(root,"record"),{input:encode(input)}).result;
  assert.equal(x.status,"rejected");assert.equal(x.errors[0].code,"invalid-input");
 }
 for(const version of [1,2,99])for(const contract of ["explicit-recording-v1","rigorloop-records-v2","unknown_value"]) {
  if((version===1&&contract==="explicit-recording-v1")||(version===2&&contract==="rigorloop-records-v2"))continue;
  const r=fixture().request;r.schema_version=version;r.contract=contract;
  assert.equal(run(root,"check",r).errors[0].code,"unsupported-contract");
 }
});

test("TG-02 current version mismatch and selected standalone path fail closed",t=>{
 const root=setup(t);mkdirSync(join(root,prefix),{recursive:true});
 const c=JSON.parse(readFileSync(new URL("../../../templates/explicit-recording/records.json",import.meta.url))).change;
 c.schema_version=2;writeFileSync(join(root,prefix+"change.yaml"),encode(c));
 assert.equal(run(root,"inspect").errors[0].code,"unsupported-contract");
 c.schema_version=1;writeFileSync(join(root,prefix+"change.yaml"),encode(c));
 const child=spawnSync(process.execPath,[new URL("../../../scripts/validate-record-store.mjs",import.meta.url).pathname,join(root,manifest)],{encoding:"utf8"});
 assert.notEqual(child.status,0);
});

test("TG-02 v2 recovery can be interrupted again and restores on observed late basis drift",t=>{
 const root=setup(t),before=create(root),r=update(root);edit(r,evidence,x=>x.checks[0].summary="candidate");writeFileSync(join(root,"basis"),"before");r.reads=[{path:"basis",expected_identity:digest("before")}];
 const stopped=run(root,"record",r,{fault:p=>p==="after-preparation"?"crash":undefined});
 assert.equal(recover(root,stopped,"complete",{fault:p=>p==="after-replace:0"?"crash":undefined}).status,"recovery-required");
 const latest=run(root,"inspect");
 const result=recover(root,latest,"complete",{fault:p=>{if(p==="after-replace:1")writeFileSync(join(root,"basis"),"after");}});
 assert.equal(result.status,"recovery-required");sameBytes(root,before);
 const restored=recover(root,run(root,"inspect"),"restore");assert.equal(restored.status,"recovered");
 assert.equal(readFileSync(join(root,"basis"),"utf8"),"after");
});

test("TG-02 public v2 text and JSON report the same storage outcome and identities",t=>{
 const root=setup(t),r=create(root),bin=new URL("../dist/bin/rigorloop.js",import.meta.url).pathname;
 const args=argv(root,"inspect");args[args.indexOf("json")]="text";
 const child=spawnSync(process.execPath,[bin,"record-store",...args],{encoding:"utf8"});assert.equal(child.status,0,child.stderr);
 const result=run(root,"inspect");assert.ok(child.stdout.includes("inspected (storage-only)"));assert.ok(child.stdout.includes(result.revision));
 for(const w of r.writes)assert.ok(child.stdout.includes(`${w.path}: ${digest(w.content)}`));
});

for(const state of ["owned","partial","third-state"]) test(`TG-02 lock write failure preserves ${state} ownership boundary`,t=>{
 const root=setup(t),write=RecordFiles.prototype.write,lock=".rigorloop/record-store/example/lock";
 RecordFiles.prototype.write=function(path,...args){
  const result=write.call(this,path,...args);
  if(path===lock) {
   if(state!=="owned")writeFileSync(join(root,lock),state==="partial"?'{"pid":':"external\n");
   throw Object.assign(new Error("private failure after creation"),{code:"EIO"});
  }
  return result;
 };
 let result;try{result=run(root,"record",fixture().request);}finally{RecordFiles.prototype.write=write;}
 assert.equal(existsSync(join(root,manifest)),false);
 if(state==="owned") {
  assert.equal(result.status,"rejected");assert.equal(result.errors[0].code,"io-failure");
  assert.equal(existsSync(join(root,lock)),false);assert.equal(run(root,"inspect").status,"inspected");create(root);
 } else {
  assert.equal(result.status,"recovery-required");assert.equal(run(root,"inspect").status,"recovery-required");
  assert.equal(readFileSync(join(root,lock),"utf8"),state==="partial"?'{"pid":':"external\n");
 }
});
