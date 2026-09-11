import {classifyRecordDirectory} from './record-discovery.js';
import {scanObservations} from "./recording-observations.js";
// Explicit values only: no workflow transition evaluator or eligibility engine.
import {boundAdvancedObservations} from "./recording-result.js";
import { randomBytes } from "node:crypto";
import { RecordFiles, digest, stop, MIB } from "./record-store-files.js";
import {V2_FORMAT,V3_FORMAT,storedFormat,requestFormat,validateAdvancedRequest,validateAdvancedResult,preserveRecords} from "./record-store-format.js";

const decode = bytes => bytes === null ? null : new TextDecoder("utf-8",{fatal:true,ignoreBOM:true}).decode(bytes);
const encoded = data => Buffer.from(JSON.stringify(data)+"\n");
const entries = map => Object.keys(map).sort().map(path=>({path,identity:digest(map[path])}));
const revision = map => Object.keys(map).length ? digest(JSON.stringify(entries(map).map(f=>[f.path,f.identity]))) : null;
const message = code => ({code,path:null,message:`Record store: ${code}.`});
const live = pid => { if(!Number.isSafeInteger(pid)||pid<=0)return false; try { process.kill(pid,0); return true; } catch(e) { return e.code==="EPERM"; } };
const exact = (v,keys) => { if(!v || typeof v!=="object" || Array.isArray(v) || Object.keys(v).sort().join(",")!==[...keys].sort().join(",")) stop("recovery-needed"); };
// Two 65-file snapshots, worst-case JSON escaping, plus bounded path/read metadata.
const MAX_JOURNAL_BYTES = 2 * 65 * MIB * 6 + 2 * MIB;

export function emptyRecordResult(operation,changeId) {
  return {schema_version:1,operation,status:"rejected",change_id:changeId,revision:null,files:[],snapshot:null,observations:[],errors:[],transaction:null,claim:"storage-only"};
}

class Store {
  constructor(root,id,options) {
    V2_FORMAT.pathKind(id,`docs/changes/${id}/change.json`);
    this.fs=new RecordFiles(root); this.id=id; this.options=options;
    this.directory=`docs/changes/${id}`; this.selectFormat(V2_FORMAT);
    this.private=`.rigorloop/record-store/${id}`;
    this.journal=`${this.private}/journal.json`; this.lock=`${this.private}/lock`; this.epoch=`${this.private}/epoch`;
    this.token=null;
  }
  selectFormat(format) {
    this.format=format;this.manifest=`${this.directory}/${format.manifest}`;
    this.otherManifest=`${this.directory}/change.yaml`;
  }
  fault(point) {
    const action=this.options.fault?.(point);
    if(action) throw Object.assign(new Error("Injected interruption"),{recordStoreCode:"io-failure",simulatedCrash:action==="crash"});
  }
  gate() {
    const lock=this.fs.read(this.lock);
    if(lock!==null) {
      let owner; try { owner=JSON.parse(decode(lock)); } catch { stop("recovery-needed"); }
      stop(live(owner.pid)?"store-busy":"recovery-needed");
    }
    if(this.fs.inspect(this.journal).info) stop("recovery-needed");
    return this.fs.hash(this.epoch);
  }
  recoveryInfo() {
    try {
      const raw=this.fs.read(this.journal,MAX_JOURNAL_BYTES);
      if(raw===null) return null;
      const journal=JSON.parse(decode(raw));
      if(typeof journal.id!=="string" || !/^[a-f0-9]{32}$/.test(journal.id)) return null;
      return {id:journal.id,recovery_identity:digest(raw)};
    } catch { return null; }
  }
  readSet() {
    const classification=classifyRecordDirectory(this.fs,this.id);
    if(classification==='absent')return {};
    if(classification==='archive')stop('unsupported-contract');
    if(classification!=='current')stop('invalid-input');
    const raw=this.fs.read(this.manifest);
    let discriminator;
    try { discriminator=JSON.parse(decode(raw)); }
    catch { stop("invalid-input"); }
    this.selectFormat(storedFormat(discriminator));
    const change=this.format.parse("change",raw);
    if(change.change_id!==this.id) stop("invalid-input");
    const set={[this.manifest]:decode(raw)};
    for(const record of change.records) set[record.path]=decode(this.fs.read(record.path));
    return set;
  }
  observations(set,iterator=false) {
    if(!Object.keys(set).length) return [message("absent-change")];
    const found=new Map(); let failed=false;
    const add=(code,path) => found.set(`${code}:${path}`,{...message(code),path});
    const visit=value=>{
      if(!value || typeof value!=="object")return;
      if(typeof value.path==="string" && typeof value.identity==="string") {
        try { if(this.fs.hash(value.path)!==value.identity) add("subject-drift",value.path); }
        catch { add("subject-drift",value.path); }
      }
      for(const child of Object.values(value))visit(child);
    };
    let change;
    for(const [path,content] of Object.entries(set)) {
      if(content===null) { add("subject-drift",path); continue; }
      const data=this.format.parse(this.format.pathKind(this.id,path),content);
      if(path===this.manifest) change=data;
      visit(data);
      if(data.checks?.some(check=>check.result==="failed")) { failed=true; add("failed-evidence",path); }
    }
    if(change.activity.status==="completed" && (failed || change.blockers.some(b=>b.state==="open"))) add("inconsistent-claim",this.manifest);
    return iterator?found.values():[...found.values()];
  }
  snapshot(observe=set=>this.observations(set)) {
    const epoch=this.gate(), set=this.readSet();
    this.fault("during-inspect");
    const observations=observe(set);
    if(this.gate()!==epoch || revision(this.readSet())!==revision(set) || this.gate()!==epoch) stop("identity-conflict");
    return {set,observations};
  }
  basis(reads) { for(const read of reads) if(this.fs.hash(read.path)!==read.expected_identity) stop("identity-conflict"); }
  candidate(request,before) {
    if(request.change_id!==this.id) stop("invalid-input");
    if(revision(before)!==request.expected_revision) stop("identity-conflict");
    const format=requestFormat(request);
    if(Object.keys(before).length && format!==this.format)stop("unsupported-contract");
    if(!Object.keys(before).length)this.selectFormat(format);
    if(request.expected_revision===null) format.creation(request,!!this.fs.inspect(this.directory,true).info);
    const candidate={...before};
    for(const write of request.writes) {
      const exists=Object.hasOwn(before,write.path), actual=this.fs.hash(write.path);
      if(!exists && actual!==null) stop("invalid-input");
      if(actual!==write.expected_identity) stop("identity-conflict");
      candidate[write.path]=write.content;
    }
    preserveRecords(this.format,this.id,before,candidate);
    this.basis(request.reads);
    return candidate;
  }
  preparePrivate() {
    for(const path of [".rigorloop",".rigorloop/record-store",this.private]) this.fs.mkdir(path);
  }
  acquire(recovery=false) {
    this.preparePrivate();
    if(recovery) {
      const previous=this.fs.read(this.lock);
      if(previous!==null) {
        const owner=JSON.parse(decode(previous));
        if(live(owner.pid)) stop("store-busy");
        this.fs.remove(this.lock,digest(previous));
      }
    }
    this.token=encoded({pid:process.pid,nonce:randomBytes(16).toString("hex")});
    try { this.fs.write(this.lock,this.token,{exclusive:true}); }
    catch(e) {
      if(e.code==="EEXIST") { this.token=null; stop("store-busy"); }
      // Exclusive creation may have completed before a later fsync failed.
      // Keep the token so finally can remove only our exact bytes.
      throw e;
    }
    this.fs.write(this.epoch,randomBytes(16).toString("hex"));
  }
  own() { if(this.token===null || this.fs.hash(this.lock)!==digest(this.token)) stop("store-busy"); }
  release() {
    if(this.token===null)return;
    try { this.fs.remove(this.lock,digest(this.token)); this.token=null; }
    catch { stop("recovery-needed"); } // Partial/unknown locks require reconciliation.
  }
  saveJournal(journal) { this.own(); this.fs.write(this.journal,encoded(journal)); }
  loadJournal(expected,id) {
    const raw=this.fs.read(this.journal,MAX_JOURNAL_BYTES);
    if(raw===null || digest(raw)!==expected) stop("recovery-needed");
    let j; try { j=JSON.parse(decode(raw)); } catch { stop("recovery-needed"); }
    if(!encoded(j).equals(raw)) stop("recovery-needed");
    exact(j,["version","id","change_id","phase","before","candidate","writes","reads","created_dirs"]);
    if(![2,3].includes(j.version) || j.id!==id || !/^[a-f0-9]{32}$/.test(j.id) || j.change_id!==this.id || !["prepared","committed"].includes(j.phase)) stop("recovery-needed");
    this.selectFormat(j.version===3?V3_FORMAT:V2_FORMAT);
    for(const side of ["before","candidate"]) {
      const map=j[side]; if(!map || typeof map!=="object" || Array.isArray(map) || Object.keys(map).length>65) stop("recovery-needed");
      for(const [path,entry] of Object.entries(map)) {
        this.format.pathKind(this.id,path); exact(entry,["content","identity"]);
        if(entry.content!==null && (typeof entry.content!=="string" || Buffer.byteLength(entry.content)>MIB)) stop("recovery-needed");
        if(digest(entry.content)!==entry.identity) stop("recovery-needed");
      }
    }
    const before=this.unpack(j.before),candidate=this.unpack(j.candidate);
    preserveRecords(this.format,this.id,before,candidate);
    if(Object.keys(before).length) {
      const change=this.format.parse("change",before[this.manifest]);
      if(change.change_id!==this.id || [this.manifest,...change.records.map(r=>r.path)].sort().join("\n")!==Object.keys(before).sort().join("\n")) stop("recovery-needed");
    }
    if(!Array.isArray(j.writes)||!j.writes.length||j.writes.length>65||new Set(j.writes).size!==j.writes.length)stop("recovery-needed");
    for(const path of j.writes) if(!Object.hasOwn(candidate,path))stop("recovery-needed");
    for(const path of Object.keys(before)) if(!Object.hasOwn(candidate,path)||(!j.writes.includes(path)&&digest(before[path])!==digest(candidate[path])))stop("recovery-needed");
    for(const path of Object.keys(candidate)) if(!Object.hasOwn(before,path)&&!j.writes.includes(path))stop("recovery-needed");
    // The public request schema validates the journal's declared targets and basis too.
    validateAdvancedRequest({schema_version:2,contract:this.format.contract,change_id:this.id,expected_revision:revision(before),
      writes:j.writes.map(path=>({path,expected_identity:digest(before[path]??null),content:candidate[path]})),reads:j.reads});
    if(!Array.isArray(j.created_dirs)||j.created_dirs.length>2||new Set(j.created_dirs.map(d=>d.path)).size!==j.created_dirs.length)stop("recovery-needed");
    for(const d of j.created_dirs) { exact(d,["path","identity"]); if(![this.directory,`${this.directory}/reviews`].includes(d.path)||typeof d.identity!=="string"||!/^\d+:\d+$/.test(d.identity))stop("recovery-needed"); }
    return j;
  }
  unpack(map) { return Object.fromEntries(Object.entries(map).map(([path,e])=>[path,e.content])); }
  pack(map) { return Object.fromEntries(Object.entries(map).map(([path,content])=>[path,{content,identity:digest(content)}])); }
  known(j) {
    if(this.fs.read(this.otherManifest)!==null)stop("recovery-needed");
    for(const path of Object.keys(j.candidate)) {
      const actual=this.fs.hash(path),before=j.before[path]?.identity??null,after=j.candidate[path].identity;
      if(actual!==before && actual!==after) stop("recovery-needed");
      if(j.phase==="committed" && actual!==after) stop("recovery-needed");
    }
  }
  directories(j) {
    const paths=[this.directory,...(j.writes.some(p=>p.startsWith(`${this.directory}/reviews/`))?[`${this.directory}/reviews`]:[])];
    for(const path of paths) {
      const existing=this.fs.inspect(path,true).info;
      if(path===this.directory && !Object.keys(j.before).length && existing && !j.created_dirs.some(d=>d.path===path&&d.identity===`${existing.dev}:${existing.ino}`))stop("identity-conflict");
      if(!existing) {
        this.own(); if(!this.fs.mkdir(path))stop("identity-conflict");
        const info=this.fs.inspect(path,true).info;
        const recorded=j.created_dirs.find(d=>d.path===path);
        if(recorded)recorded.identity=`${info.dev}:${info.ino}`;
        else j.created_dirs.push({path,identity:`${info.dev}:${info.ino}`});
        this.saveJournal(j);
      }
    }
  }
  publish(j,side) {
    this.known(j);
    if(side==="candidate") { this.directories(j); this.basis(j.reads); }
    for(const [index,path] of j.writes.entries()) {
      this.own(); this.fault(`before-replace:${index}`); this.known(j);
      const expected=this.fs.hash(path), desired=j[side][path]??{identity:null,content:null};
      if(expected!==(j.before[path]?.identity??null) && expected!==j.candidate[path].identity) stop("recovery-needed");
      if(j.phase==="committed" && expected!==j.candidate[path].identity) stop("recovery-needed");
      if(expected!==desired.identity) {
        if(desired.content===null) this.fs.remove(path,expected);
        else this.fs.write(path,Buffer.from(desired.content),{expected});
      }
      this.fault(`after-replace:${index}`);
    }
    for(const path of Object.keys(j.candidate)) if(this.fs.hash(path)!==(j[side][path]?.identity??null))stop("recovery-needed");
    if(side==="before") for(const dir of [...j.created_dirs].reverse()) this.fs.removeDirectory(dir.path,dir.identity);
  }
  cleanup() { this.own(); this.fs.remove(this.journal,this.fs.hash(this.journal)); this.release(); }
  prepareResult(operation,status,set,beforeRevision=revision(set)) {
    this.fault("before-result");
    if(this.options.prepareResult)return this.options.prepareResult({operation,status,set,format:this.format,reader:this.fs,revision:revision(set),before_revision:beforeRevision});
    const result={...emptyRecordResult(operation,this.id),status,revision:revision(set),files:entries(set)};
    result.observations=boundAdvancedObservations(this.observations(set,true),8*MIB-Buffer.byteLength(JSON.stringify(result))-1);
    validateAdvancedResult(result);
    return result;
  }
  record(request,lockedSnapshot=null) {
    const initial=lockedSnapshot??this.snapshot(()=>[]), candidate=this.candidate(request,initial.set);
    let journal;
    try {
      if(!lockedSnapshot)this.acquire();
      // Recheck after exclusion; a check result and a stale retry reserve nothing.
      if(this.fs.inspect(this.journal).info) stop("recovery-needed");
      const before=this.readSet(); this.candidate(request,before);
      if(revision(before)!==revision(initial.set))stop("identity-conflict");
      const unchanged=revision(before)===revision(candidate);
      const prepared=this.prepareResult("record",unchanged?"unchanged":"saved",candidate);
      if(unchanged) { this.release(); return prepared; }
      this.fault("after-lock");
      journal={version:this.format.version,id:randomBytes(16).toString("hex"),change_id:this.id,phase:"prepared",before:this.pack(before),candidate:this.pack(candidate),
        writes:request.writes.map(w=>w.path),reads:request.reads,created_dirs:[]};
      this.saveJournal(journal); this.fault("after-preparation");
      this.basis(request.reads); this.publish(journal,"candidate");
      this.fault("before-commit"); this.basis(request.reads);
      journal.phase="committed"; this.saveJournal(journal); this.fault("after-commit");
      this.cleanup(); return prepared;
    } catch(e) {
      if(journal && !e.simulatedCrash && journal.phase!=="committed") {
        try { this.publish(journal,"before"); this.cleanup(); throw e; }
        catch(restoration) { if(restoration===e)throw e; stop("recovery-needed"); }
      }
      if(journal)stop("recovery-needed");
      throw e;
    } finally { this.release(); }
  }
  recover(id,expected,action) {
    if(!["complete","restore"].includes(action))stop("invalid-input");
    let journal=this.loadJournal(expected,id);
    try {
      this.acquire(true);
      journal=this.loadJournal(expected,id); this.known(journal);
      if(action==="restore" && journal.phase==="committed")stop("recovery-needed");
      if(action==="complete")this.basis(journal.reads);
      const set=this.unpack(action==="complete"?journal.candidate:journal.before);
      const prepared=this.prepareResult("recover","recovered",set);
      this.fault("before-recovery");
      this.publish(journal,action==="complete"?"candidate":"before");
      if(action==="complete") {
        try { this.basis(journal.reads); }
        catch(e) { if(journal.phase!=="committed")this.publish(journal,"before"); throw e; }
        journal.phase="committed"; this.saveJournal(journal);
      }
      this.fault("after-recovery");
      this.cleanup(); return prepared;
    } finally { this.release(); }
  }
}

export function executeRecordStore({root,changeId,operation,request,transaction,expectedRecovery,action},options={}) {
  const result=emptyRecordResult(operation,changeId); let store;
  try {
    if(!["inspect","check","record","recover"].includes(operation))stop("invalid-input");
    if(request)validateAdvancedRequest(request);
    store=new Store(root,changeId,options);
    let set;
    if(operation==="inspect") {
      const snapshot=store.snapshot(); set=snapshot.set; result.observations=snapshot.observations;
      result.status="inspected"; result.snapshot={records:Object.keys(set).sort().map(path=>({path,content:set[path]}))};
    } else if(operation==="check") {
      const snapshot=store.snapshot(()=>[]); set=store.candidate(request,snapshot.set); return store.prepareResult("check","valid",set,revision(snapshot.set));
    } else {
      return operation==="record"?store.record(request):store.recover(transaction,expectedRecovery,action);
    }
    result.revision=revision(set); result.files=entries(set);
    if(operation!=="inspect")result.observations=store.observations(set);
    validateAdvancedResult(result);
  } catch(e) {
    const code=e.recordStoreCode??(e.code?"io-failure":String(e.message).includes("limit")?"limit-exceeded":"invalid-input");
    result.status=operation==="recover"? (code==="store-busy"?"busy":"recovery-required")
      :({"identity-conflict":"conflict","store-busy":"busy","recovery-needed":"recovery-required"}[code]??"rejected");
    result.snapshot=null; result.files=[]; result.revision=null; result.observations=[];
    result.errors=[message(code)]; result.transaction=store?.recoveryInfo()??null;
  }
  return result;
}

// Internal primary adapters use the same before/after exclusion and identity
// checks without first constructing an advanced full-inspection response.
export function withRecordSnapshot(root,changeId,inspect,options={}) {
 const store=new Store(root,changeId,options);
 try{
  let failure;
  const result=store.snapshot(set=>{try{return inspect({set,format:store.format,reader:store.fs,revision:revision(set)});}catch(e){failure=e;}}).observations;
  if(failure){failure.snapshotVerified=true;throw failure;}return result;
 }
 catch(e){e.transaction=store.recoveryInfo();throw e;}
}

// Targeted writes construct under the same exclusion held through publication.
// Preview uses the coherent reader and never creates exclusion state.
export function executeTargetedStore({root,changeId,request,preview,construct,prepare},options={}) {
 const store=new Store(root,changeId,options);
 try {
  const before=store.snapshot(()=>[]);
  if(!preview)store.acquire();
  const build=set=>{
   if(revision(set)!==request.expected_revision)stop("identity-conflict");
   if(Object.keys(set).length&&store.format.contract!==request.contract)stop("unsupported-contract");
   const built=construct(request,set);
   validateAdvancedRequest(built.request);
   store.options.prepareResult=prepare(built);
   return built.request;
  };
  if(preview)return store.snapshot(set=>{
   const advanced=build(set),candidate=store.candidate(advanced,set);
   return store.prepareResult("check","valid",candidate,revision(set));
  }).observations;
  if(store.fs.inspect(store.journal).info)stop("recovery-needed");
  const set=store.readSet();
  if(revision(set)!==revision(before.set))stop("identity-conflict");
  const advanced=build(set);
  return store.record(advanced,{set});
 }catch(e){
  if(e.recordStoreCode==="broken-reference"){
   try{
    const diagnose=set=>({revision:revision(set),summary:scanObservations({set,format:store.format,reader:store.fs,revision:revision(set)}).summary()});
    let observed;
    if(store.token){store.own();const set=store.readSet();observed=diagnose(set);if(revision(store.readSet())!==observed.revision)stop("identity-conflict");store.own();}
    else observed=store.snapshot(diagnose).observations;
    e.revision=observed.revision;e.observation_summary=observed.summary;
   }catch{/* Unverified optional metadata is never attached. */}
  }
  e.transaction=store.recoveryInfo();throw e;
 }
 finally{store.release();}
}
