import {historicalV2} from './helpers/historical-v2.mjs';
import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, existsSync, unlinkSync, symlinkSync, linkSync, renameSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { executeRecordStoreCli } from "../dist/lib/record-store-cli.js";
import { validateAdvancedResult } from "../dist/lib/record-store-format.js";
import { RecordFiles } from "../dist/lib/record-store-files.js";
import fs from "node:fs";
import { syncBuiltinESMExports } from "node:module";

const fixture=()=>JSON.parse(readFileSync(new URL("../../../tests/fixtures/rigorloop-records-v2/storage-safety.json",import.meta.url),"utf8"));
const manifest="docs/changes/example/change.json";
for (const level of ["off","unknown_value"]) for (const extra of [["--no-file-log"],["--console-log-level","unknown_value"],["--file-log-level","off"]]) test(`ER-M4-004 public recorder rejects historical logging flags ${extra[0]} with environment ${level}`,t=>{
  const root=setup(t);
  const result=spawnSync(process.execPath,[new URL("../dist/bin/rigorloop.js",import.meta.url).pathname,"record-store",...args(root,"record",extra)],{encoding:"utf8",input:"payload-must-not-appear",env:{...process.env,RIGORLOOP_CONSOLE_LOG_LEVEL:level}});
  assert.equal(result.status,2);
  const envelope=JSON.parse(result.stdout);
  assert.equal(envelope.status,"rejected");
  assert.equal(envelope.operation,"record");
  assert.equal(envelope.change_id,"example");
  assert.deepEqual(envelope.files,[]);
  assert.equal(envelope.snapshot,null);
  assert.equal(envelope.errors[0].code,"invalid-input");
  assert.equal(result.stderr,"");
  assert.equal(existsSync(join(root,manifest)),false);
  assert.equal(existsSync(join(root,".rigorloop")),false);
});
test("ER-M4-004 public recorder ignores historical logging environment",t=>{
  const root=setup(t);
  const result=spawnSync(process.execPath,[new URL("../dist/bin/rigorloop.js",import.meta.url).pathname,"record-store",...args(root,"inspect")],{encoding:"utf8",env:{...process.env,RIGORLOOP_CONSOLE_LOG_LEVEL:"unknown_value",RIGORLOOP_FILE_LOG_LEVEL:"unknown_value"}});
  assert.equal(result.status,0);
  assert.equal(JSON.parse(result.stdout).status,"inspected");
  assert.equal(result.stderr,"");
  assert.equal(existsSync(join(root,".rigorloop")),false);
});
const hash=s=>`sha256:${createHash("sha256").update(s).digest("hex")}`;
function setup(t) {
  const root=mkdtempSync(join(tmpdir(),"rigorloop-recorder-"));
  t.after(()=>rmSync(root,{recursive:true,force:true}));
  mkdirSync(join(root,"docs/changes"),{recursive:true});
  return root;
}
function request() { const r=fixture().request; r.reads=[]; return r; }
function args(root,op,extra=[]) { return [op,"--root",root,"--change","example","--format","json",...(["record","check"].includes(op)?["--input","-"]:[]),...extra]; }
function run(root,op,input,options={},extra=[]) {
  const execution=input?.contract==="rigorloop-records-v2"&&input.expected_revision===null?historicalV2(root,op,input,options):executeRecordStoreCli(args(root,op,extra),{...options,input:input===undefined?undefined:JSON.stringify(input)+"\n"});
  validateAdvancedResult(execution.result);
  return execution;
}
function update(root,status="completed") {
  const current=run(root,"inspect").result, r=request();
  r.expected_revision=current.revision; r.writes[0].expected_identity=current.files.find(f=>f.path===manifest).identity;
  const change=JSON.parse(r.writes[0].content); change.activity.status=status;
  r.writes[0].content=JSON.stringify(change,null,2)+"\n";
  return r;
}
function recover(root,result,action,options={}) {
  return run(root,"recover",undefined,options,["--transaction",result.transaction.id,"--expected-recovery",result.transaction.recovery_identity,"--action",action]);
}

for (const phase of ["after-preparation","after-commit"]) test(`ER-M2-002 pending ${phase} journal survives lock acquisition`,t=>{
  const root=setup(t); run(root,"record",request());
  const pending=update(root), original=RecordFiles.prototype.write;
  const journal=join(root,".rigorloop/record-store/example/journal.json");
  let injected=false, identity;
  RecordFiles.prototype.write=function(path,...rest) {
    if(!injected && path.endsWith("/lock")) {
      injected=true;
      assert.equal(run(root,"record",pending,{fault:p=>p===phase?"crash":undefined}).result.status,"recovery-required");
      identity=hash(readFileSync(journal));
    }
    return original.call(this,path,...rest);
  };
  let result;
  try { result=run(root,"record",pending).result; }
  finally { RecordFiles.prototype.write=original; }
  assert.equal(injected,true);
  assert.equal(result.status,"recovery-required");
  assert.equal(hash(readFileSync(journal)),identity);
});

for (const action of ["record","complete","restore"]) test(`ER-M2-003 late third state survives ${action}`,t=>{
  const root=setup(t); run(root,"record",request());
  const pending=update(root);
  const interrupted=action==="record"?null:run(root,"record",pending,{fault:p=>p==="after-replace:0"?"crash":undefined}).result;
  const original=RecordFiles.prototype.hash; let injected=false;
  RecordFiles.prototype.hash=function(path) {
    // Interpose the publication precondition itself, not the earlier known-set check.
    const caller=new Error().stack.split("\n")[2];
    if(!injected && path===manifest && caller.includes("Store.publish")) {
      injected=true; writeFileSync(join(root,manifest),"external-third-state\n");
    }
    return original.call(this,path);
  };
  let result;
  try { result=action==="record"?run(root,"record",pending).result:recover(root,interrupted,action).result; }
  finally { RecordFiles.prototype.hash=original; }
  assert.equal(injected,true); assert.equal(result.status,"recovery-required");
  assert.equal(readFileSync(join(root,manifest),"utf8"),"external-third-state\n");
});

for (const operation of ["write","exclusive","remove","mkdir","removeDirectory"]) test(`ER-M2-004 late parent substitution cannot redirect ${operation}`,t=>{
  const root=setup(t), outside=setup(t), parent=join(root,"records"), moved=join(root,"aside");
  mkdirSync(parent); writeFileSync(join(parent,"file"),"before");
  writeFileSync(join(outside,"file"),"outside");
  mkdirSync(join(parent,"empty")); mkdirSync(join(outside,"empty"));
  const access=new RecordFiles(root), directory=fs.statSync(join(parent,"empty"));
  const method={write:"renameSync",exclusive:"openSync",remove:"unlinkSync",mkdir:"mkdirSync",removeDirectory:"rmdirSync"}[operation];
  const original=fs[method], cwd=process.cwd(); let injected=false;
  fs[method]=function(...args) {
    const eligible=operation!=="exclusive" || (typeof args[1]==="number" && (args[1]&fs.constants.O_CREAT));
    if(!injected && eligible) {
      injected=true;
      if(operation==="write") {
        // Give the escaped directory the prepared temporary file too: old absolute rename succeeds.
        const temporary=fs.readdirSync(parent).find(p=>p.startsWith(".record-store-"));
        original(join(parent,temporary),join(outside,temporary));
      }
      fs.renameSync(parent,moved); symlinkSync(outside,parent);
    }
    return original(...args);
  };
  syncBuiltinESMExports();
  try {
    try {
      if(operation==="write")access.write("records/file",Buffer.from("candidate"),{expected:hash("before")});
      if(operation==="exclusive")access.write("records/new",Buffer.from("candidate"),{exclusive:true});
      if(operation==="remove")access.remove("records/file",hash("before"));
      if(operation==="mkdir")access.mkdir("records/new");
      if(operation==="removeDirectory")access.removeDirectory("records/empty",`${directory.dev}:${directory.ino}`);
    } catch(e) { assert.ok(e.recordStoreCode || e.code); }
  } finally { fs[method]=original; syncBuiltinESMExports(); }
  assert.equal(process.cwd(),cwd); assert.equal(injected,true);
  assert.equal(readFileSync(join(outside,"file"),"utf8"),"outside");
  assert.equal(existsSync(join(outside,"new")),false);
  assert.equal(existsSync(join(outside,"empty")),true);
});

test("TG-03 inspect/check are read-only; record is exact and has observations without eligibility",t=>{
  const root=setup(t), r=request();
  const absent=run(root,"inspect").result;
  assert.deepEqual(absent.snapshot,{records:[]}); assert.equal(absent.revision,null);
  assert.equal(run(root,"check",r).result.status,"valid");
  assert.equal(existsSync(join(root,".rigorloop")),false);
  assert.equal(existsSync(join(root,"docs/changes/example")),false);
  assert.equal(run(root,"record",r).result.status,"saved");
  assert.equal(readFileSync(join(root,manifest),"utf8"),r.writes[0].content);
  writeFileSync(join(root,"docs/changes/example/unrelated.txt"),"preserve\n");
  const updated=update(root), saved=run(root,"record",updated).result;
  assert.equal(saved.status,"saved"); assert.equal(saved.claim,"storage-only"); assert.equal(saved.snapshot,null);
  assert.ok(saved.observations.some(o=>o.code==="inconsistent-claim"));
  assert.equal(readFileSync(join(root,manifest),"utf8"),updated.writes[0].content);
  assert.equal(readFileSync(join(root,"docs/changes/example/unrelated.txt"),"utf8"),"preserve\n");
  assert.equal(run(root,"inspect").result.snapshot.records[0].content,updated.writes[0].content);
});

test("TG-04 exact revision/write/read preconditions and stale retry",t=>{
  const root=setup(t), r=request();
  assert.equal(run(root,"record",r).result.status,"saved");
  assert.equal(run(root,"record",r).result.status,"conflict");
  const u=update(root); assert.equal(run(root,"record",u).result.status,"saved");
  const same=update(root); assert.equal(run(root,"record",same).result.status,"unchanged");
  writeFileSync(join(root,"basis"),"before"); same.reads=[{path:"basis",expected_identity:hash("before")}];
  writeFileSync(join(root,"basis"),"after");
  assert.equal(run(root,"record",same).result.status,"conflict");
  same.reads=[]; same.writes[0].expected_identity=null;
  assert.equal(run(root,"record",same).result.status,"conflict");
});

test("ER-M2-001 malformed selectors produce truthful safe rejections before IO",()=>{
  for (const [argv,op,id,format] of [
    [["inspect","--format","json"],"inspect",null,"json"],
    [["unknown_value","--change","example","--format","json"],null,"example","json"],
    [["record","--change","../secret","--format","json"],"record",null,"json"],
    [["check","--change","example","--change","example","--format","json"],"check",null,"json"],
    [["inspect","--change","example","--format","unknown_value"],"inspect","example","text"],
    [["inspect","--change","example","--format","json","--format","json"],"inspect","example","text"],
  ]) {
    const result=executeRecordStoreCli(argv,{readInput:()=>assert.fail("must not read stdin")});
    assert.equal(result.exitCode,2); assert.equal(result.format,format);
    assert.equal(result.result.operation,op); assert.equal(result.result.change_id,id);
    validateAdvancedResult(result.result);
    assert.equal(JSON.stringify(result).includes("../secret"),false);
  }
});

test("TG-03 historical roots, unknown flags, unsafe paths and existing roots reject unchanged",t=>{
  const root=setup(t), r=request();
  mkdirSync(join(root,"docs/changes/example"));
  assert.equal(run(root,"record",r).result.status,"rejected");
  writeFileSync(join(root,manifest),'{"contract":"stage-owned-change-local-v3"}\n');
  const historical=readFileSync(join(root,manifest));
  assert.equal(run(root,"record",r).result.errors[0].code,"unsupported-contract");
  assert.deepEqual(readFileSync(join(root,manifest)),historical);
  assert.equal(run(root,"inspect",undefined,{},["--unknown_value","sensitive"]).result.errors[0].code,"invalid-input");
  unlinkSync(join(root,manifest)); symlinkSync(join(root,"outside"),join(root,manifest));
  assert.equal(run(root,"inspect").result.errors[0].code,"unsafe-path");
  unlinkSync(join(root,manifest)); writeFileSync(join(root,"outside"),r.writes[0].content);
  linkSync(join(root,"outside"),join(root,manifest));
  assert.equal(run(root,"inspect").result.errors[0].code,"unsafe-path");
});

test("TG-04 interruption has explicit complete/restore and never exposes a mixed snapshot",t=>{
  for (const action of ["complete","restore"]) {
    const root=setup(t), r=request();
    const interrupted=run(root,"record",r,{fault:p=>p==="after-replace:0"?"crash":undefined}).result;
    assert.equal(interrupted.status,"recovery-required");
    const blocked=run(root,"inspect").result;
    assert.equal(blocked.status,"recovery-required"); assert.equal(blocked.snapshot,null);
    assert.equal(recover(root,blocked,action).result.status,"recovered");
    assert.equal(existsSync(join(root,manifest)),action==="complete");
    if(action==="restore") assert.equal(existsSync(join(root,"docs/changes/example")),false);
  }
});

test("TG-04 third-state edits and stale recovery identity stop without overwrite",t=>{
  const root=setup(t), interrupted=run(root,"record",request(),{fault:p=>p==="after-replace:0"?"crash":undefined}).result;
  writeFileSync(join(root,manifest),"external\n");
  assert.equal(recover(root,interrupted,"restore").result.status,"recovery-required");
  assert.equal(readFileSync(join(root,manifest),"utf8"),"external\n");
  const stale=structuredClone(interrupted); stale.transaction.recovery_identity=hash("stale");
  assert.equal(recover(root,stale,"complete").result.status,"recovery-required");
});

test("TG-04 committed transaction refuses rollback and permits cleanup",t=>{
  const root=setup(t), r=request();
  const interrupted=run(root,"record",r,{fault:p=>p==="after-commit"?"crash":undefined}).result;
  assert.equal(interrupted.status,"recovery-required");
  assert.equal(recover(root,interrupted,"restore").result.status,"recovery-required");
  assert.equal(readFileSync(join(root,manifest),"utf8"),r.writes[0].content);
  assert.equal(recover(root,interrupted,"complete").result.status,"recovered");
});

test("TG-03 real public dispatcher supports text and JSON recording",t=>{
  const root=setup(t), launcher=new URL("../dist/bin/rigorloop.js",import.meta.url).pathname;
  run(root,"record",request()); // Existing v2 fixture, then real public continuation.
  for (const format of ["text","json"]) for (const op of ["inspect","check","record"]) {
    const input=op==="inspect"?undefined:JSON.stringify(existsSync(join(root,manifest))?update(root):request())+"\n";
    const argv=args(root,op); argv[argv.indexOf("json")]=format;
    const child=spawnSync(process.execPath,[launcher,"record-store",...argv],{input,encoding:"utf8"});
    assert.equal(child.status,0,child.stderr+child.stdout);
    if(format==="json") validateAdvancedResult(JSON.parse(child.stdout));
  }
  const child=spawnSync(process.execPath,[new URL("../dist/bin/rigorloop.js",import.meta.url).pathname,"record-store",...args(root,"inspect")],{encoding:"utf8"});
  assert.equal(child.status,0,child.stderr+child.stdout);
  assert.equal(JSON.parse(child.stdout).claim,"storage-only");
});

test("ER-M4-005 public text names available and absent record identities",t=>{
  const root=setup(t), launcher=new URL("../dist/bin/rigorloop.js",import.meta.url).pathname;
  const r=request(), change=JSON.parse(r.writes[0].content), path="docs/changes/example/evidence.json";
  change.records=[{path,kind:"evidence"}];
  change.applicability=[{...fixture().change.applicability[0],path}];
  r.writes[0].content=JSON.stringify(change)+"\n";
  r.writes.push({path,expected_identity:null,content:JSON.stringify(fixture().evidence)+"\n"});
  run(root,"record",r);const seeded=run(root,"inspect").result;r.expected_revision=seeded.revision;for(const w of r.writes)w.expected_identity=hash(w.content);
  const argv=args(root,"record"); argv[argv.indexOf("json")]="text";
  const saved=spawnSync(process.execPath,[launcher,"record-store",...argv],{encoding:"utf8",input:JSON.stringify(r)+"\n"});
  assert.equal(saved.status,0,saved.stdout+saved.stderr);
  const current=run(root,"inspect").result;
  assert.ok(saved.stdout.includes(`Revision: ${current.revision}\n`));
  for(const file of current.files) assert.ok(saved.stdout.includes(`${file.path}: ${file.identity}\n`));
  unlinkSync(join(root,path));
  const inspect=args(root,"inspect"); inspect[inspect.indexOf("json")]="text";
  const missing=spawnSync(process.execPath,[launcher,"record-store",...inspect],{encoding:"utf8"});
  assert.equal(missing.status,0,missing.stdout+missing.stderr);
  assert.ok(missing.stdout.includes(`${path}: absent\n`));
});

test("TG-03 missing registered records are visible and repairable; registry removal is rejected",t=>{
  const root=setup(t), r=request(), change=JSON.parse(r.writes[0].content), f=fixture();
  change.records=[{path:"docs/changes/example/evidence.json",kind:"evidence"}];
  change.applicability=[{...f.change.applicability[0],path:change.records[0].path}];
  r.writes[0].content=JSON.stringify(change)+"\n";
  r.writes.push({path:change.records[0].path,expected_identity:null,content:JSON.stringify(f.evidence)+"\n"});
  assert.equal(run(root,"record",r).result.status,"saved");
  unlinkSync(join(root,change.records[0].path));
  const inspected=run(root,"inspect").result;
  assert.equal(inspected.snapshot.records.find(e=>e.path.endsWith("evidence.json")).content,null);
  r.expected_revision=inspected.revision; r.writes=[r.writes[1]];
  assert.equal(run(root,"record",r).result.status,"saved");
  const remove=update(root); // Original fixture would drop the existing registry.
  assert.equal(run(root,"record",remove).result.status,"rejected");
  assert.equal(existsSync(join(root,change.records[0].path)),true);
});

test("TG-04 competing subprocess is busy; stale contender cannot overwrite the winner",t=>{
  const root=setup(t), r=request(), launcher=new URL("./helpers/historical-v2-launcher.mjs",import.meta.url).pathname;
  let competitor;
  const result=run(root,"record",r,{fault:point=>{
    if(point==="after-preparation")competitor=spawnSync(process.execPath,[launcher,"record-store",...args(root,"record")],{input:JSON.stringify(r)+"\n",encoding:"utf8"});
  }});
  assert.equal(result.result.status,"saved"); assert.equal(competitor.status,4);
  assert.equal(JSON.parse(competitor.stdout).status,"busy");
  assert.equal(run(root,"record",r).result.status,"conflict");
  assert.equal(readFileSync(join(root,manifest),"utf8"),r.writes[0].content);
});

test("TG-04 drift after replacement restores before bytes and leaves decision basis untouched",t=>{
  const root=setup(t); run(root,"record",request());
  const before=readFileSync(join(root,manifest),"utf8"), r=update(root);
  writeFileSync(join(root,"basis"),"before"); r.reads=[{path:"basis",expected_identity:hash("before")}];
  const result=run(root,"record",r,{fault:point=>{if(point==="before-commit")writeFileSync(join(root,"basis"),"external");}});
  assert.equal(result.result.status,"conflict");
  assert.equal(readFileSync(join(root,manifest),"utf8"),before);
  assert.equal(readFileSync(join(root,"basis"),"utf8"),"external");
  assert.equal(run(root,"inspect").exitCode,0);
});

test("TG-04 historical creation crash and public recover subprocesses preserve complete/restore in both formats",t=>{
  const launcher=new URL("./helpers/historical-v2-launcher.mjs",import.meta.url).pathname;
  for(const format of ["text","json"]) for(const action of ["complete","restore"]) {
    const root=setup(t), r=request();
    const child=spawnSync(process.execPath,[launcher,"record-store",...args(root,"record")],{input:JSON.stringify(r)+"\n",encoding:"utf8",env:{...process.env,RIGORLOOP_TEST_RECORD_FAULT:"after-replace:0"}});
    assert.equal(child.status,99);
    const blocked=run(root,"inspect").result; assert.equal(blocked.status,"recovery-required");
    const argv=args(root,"recover",["--transaction",blocked.transaction.id,"--expected-recovery",blocked.transaction.recovery_identity,"--action",action]);
    argv[argv.indexOf("json")]=format;
    const recovery=spawnSync(process.execPath,[launcher,"record-store",...argv],{encoding:"utf8"});
    assert.equal(recovery.status,0,recovery.stderr+recovery.stdout);
    if(format==="json")validateAdvancedResult(JSON.parse(recovery.stdout));
    assert.equal(existsSync(join(root,manifest)),action==="complete");
  }
});

test("TG-04 interrupted recovery is repeatable and missing/tampered/unknown_value journals stop",t=>{
  for(const fault of ["after-preparation","after-replace:0"]) {
    const root=setup(t), interrupted=run(root,"record",request(),{fault:p=>p===fault?"crash":undefined}).result;
    const again=recover(root,interrupted,"complete",{fault:p=>p==="after-replace:0"?"crash":undefined}).result;
    assert.equal(again.status,"recovery-required");
    const fresh=run(root,"inspect").result;
    assert.equal(recover(root,fresh,"complete").result.status,"recovered");
  }
  for(const mutate of [j=>j.phase="unknown_value",j=>j.candidate[manifest].content+=" ",j=>j.extra="unknown_value"]) {
    const root=setup(t), stopped=run(root,"record",request(),{fault:p=>p==="after-preparation"?"crash":undefined}).result;
    const path=join(root,".rigorloop/record-store/example/journal.json"), j=JSON.parse(readFileSync(path,"utf8")); mutate(j);
    writeFileSync(path,JSON.stringify(j)+"\n");
    stopped.transaction.recovery_identity=hash(readFileSync(path));
    assert.equal(recover(root,stopped,"complete").result.status,"recovery-required");
    assert.equal(existsSync(join(root,manifest)),false);
    unlinkSync(path);
    assert.equal(recover(root,stopped,"restore").result.status,"recovery-required");
  }
});

test("TG-04 multi-record partial publication restores exact prior bytes",t=>{
  const root=setup(t), r=request(), f=fixture(), evidence="docs/changes/example/evidence.json";
  const change=JSON.parse(r.writes[0].content);
  change.records=[{path:evidence,kind:"evidence"}];
  change.applicability=[{...f.change.applicability[0],path:evidence}];
  r.writes[0].content=JSON.stringify(change)+"\n";
  r.writes.push({path:evidence,expected_identity:null,content:JSON.stringify(f.evidence)+"\n"});
  assert.equal(run(root,"record",r).exitCode,0);
  const before=run(root,"inspect").result;
  r.expected_revision=before.revision;
  for(const w of r.writes)w.expected_identity=hash(w.content);
  change.activity.status="completed"; r.writes[0].content=JSON.stringify(change)+"\n";
  f.evidence.checks[0].summary="new proof"; r.writes[1].content=JSON.stringify(f.evidence)+"\n";
  const stopped=run(root,"record",r,{fault:p=>p==="after-replace:0"?"crash":undefined}).result;
  assert.equal(stopped.status,"recovery-required");
  assert.equal(readFileSync(join(root,manifest),"utf8"),r.writes[0].content);
  assert.notEqual(readFileSync(join(root,evidence),"utf8"),r.writes[1].content);
  assert.equal(run(root,"inspect").result.snapshot,null);
  assert.equal(recover(root,stopped,"restore").exitCode,0);
  for(const file of before.snapshot.records)assert.equal(readFileSync(join(root,file.path),"utf8"),file.content);
});

test("TG-03 public rejection is bounded and ordinary symlink launcher retains existing behavior",t=>{
  const root=setup(t), launcher=new URL("./helpers/historical-v2-launcher.mjs",import.meta.url).pathname;
  for(const argv of [["unknown_value","--format","json"],["inspect","--change","../sensitive","--format","json"],["inspect","--root",root,"--change","example","--input","secret","--format","json"]]) {
    const child=spawnSync(process.execPath,[launcher,"record-store",...argv],{encoding:"utf8"});
    assert.equal(child.status,2); const result=JSON.parse(child.stdout); validateAdvancedResult(result);
    assert.equal((child.stdout+child.stderr).includes("sensitive"),false);
    assert.equal(existsSync(join(root,".rigorloop")),false);
  }
  const alias=join(root,"rigorloop"); symlinkSync(new URL("../dist/bin/rigorloop.js",import.meta.url).pathname,alias);
  const version=spawnSync(process.execPath,[alias,"version"],{encoding:"utf8"});
  assert.equal(version.status,0); assert.equal(version.stdout.trim(), `@xiongxianfei/rigorloop ${JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8")).version}`);
});

test("TG-04 pre-journal failure changes no authoritative bytes",t=>{
  const root=setup(t), r=request();
  const result=run(root,"record",r,{fault:p=>p==="after-lock"?"fail":undefined});
  assert.equal(result.result.status,"rejected");
  assert.equal(existsSync(join(root,manifest)),false);
  assert.equal(run(root,"inspect").result.status,"inspected");
});

test("TG-03 unsupported request contracts and unsafe targets retain precise safe errors",t=>{
  const root=setup(t);
  for(const contract of ["stage-owned-change-local-v3","compact-current-state-v1","unknown_value"]) {
    const r=request(); r.contract=contract;
    assert.equal(run(root,"record",r).result.errors[0].code,"unsupported-contract");
  }
  const r=request(); r.writes[0].path="../outside";
  assert.equal(run(root,"record",r).result.errors[0].code,"unsafe-path");
  assert.equal(existsSync(join(root,".rigorloop")),false);
});

test("TG-04 unexpected IO failures are safe io-failure results",t=>{
  const root=setup(t);
  const result=run(root,"record",request(),{fault:p=>{if(p==="after-lock")throw Object.assign(new Error("private failure payload"),{code:"ENOSPC"});}});
  assert.equal(result.result.errors[0].code,"io-failure");
  assert.equal(JSON.stringify(result).includes("private failure payload"),false);
  assert.equal(existsSync(join(root,manifest)),false);
});

test("TG-04 concurrent ancestor substitution stops publication without escaped bytes",t=>{
  const root=setup(t); run(root,"record",request()); const r=update(root);
  const outside=join(root,"unrelated"); mkdirSync(outside); writeFileSync(join(outside,"change.json"),"external\n");
  let substituted=false;
  const result=run(root,"record",r,{fault:point=>{
    if(point==="before-replace:0"&&!substituted) {
      substituted=true; renameSync(join(root,"docs/changes/example"),join(root,"docs/changes/preserved"));
      symlinkSync(outside,join(root,"docs/changes/example"));
    }
  }});
  assert.equal(result.result.status,"recovery-required");
  assert.equal(readFileSync(join(outside,"change.json"),"utf8"),"external\n");
});

test("TG-04 inspection detects an overlapping completed writer",t=>{
  const root=setup(t); run(root,"record",request()); const r=update(root);
  let wrote=false;
  const inspected=run(root,"inspect",undefined,{fault:point=>{
    if(point==="during-inspect"&&!wrote) { wrote=true; assert.equal(run(root,"record",r).exitCode,0); }
  }});
  assert.equal(inspected.result.status,"conflict"); assert.equal(inspected.result.snapshot,null);
  assert.equal(run(root,"inspect").exitCode,0);
});
