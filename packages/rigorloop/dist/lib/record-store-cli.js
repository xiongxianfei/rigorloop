import { readSync } from "node:fs";
import { executeRecordStore, emptyRecordResult } from "./record-store.js";
import { parseAdvancedRequest } from "./record-store-format.js";
import { MIB, stop } from "./record-store-files.js";

const OPERATIONS = ["inspect","check","record","recover"];
const EXITS = {inspected:0,valid:0,saved:0,unchanged:0,recovered:0,rejected:2,conflict:3,busy:4,"recovery-required":5};
const id = value => typeof value==="string" && /^[a-z0-9][a-z0-9-]{0,79}$/.test(value);
function input() {
  const chunks=[],buffer=Buffer.alloc(64*1024); let total=0,n;
  while((n=readSync(0,buffer,0,buffer.length,null))>0) {
    total+=n; if(total>8*MIB) throw new Error("limit");
    chunks.push(Buffer.from(buffer.subarray(0,n)));
  }
  return Buffer.concat(chunks);
}
export function parseRecordStoreArgs(args) {
  const operation=OPERATIONS.includes(args[0])?args[0]:null;
  const flags=new Map(); let invalid=operation===null;
  for(let i=1;i<args.length;i++) {
    const flag=args[i];
    if(!["--root","--change","--format","--input","--transaction","--expected-recovery","--action"].includes(flag)) { invalid=true; continue; }
    const values=flags.get(flag)??[];
    const next=args[i+1];
    values.push(next!==undefined&&!next.startsWith("--")?args[++i]:null);
    flags.set(flag,values);
  }
  const one=flag=>flags.get(flag)?.length===1?flags.get(flag)[0]:null;
  const changeId=id(one("--change"))?one("--change"):null;
  const format=one("--format")==="json"?"json":"text";
  if(changeId===null || !one("--root") || [...flags.values()].some(v=>v.length!==1||v[0]===null))invalid=true;
  if(flags.has("--format")&&!["text","json"].includes(one("--format")))invalid=true;
  const allowed=new Set(["--root","--change","--format"]);
  if(operation==="check"||operation==="record") { allowed.add("--input"); if(one("--input")!=="-")invalid=true; }
  if(operation==="recover") {
    for(const f of ["--transaction","--expected-recovery","--action"])allowed.add(f);
    if(!/^[a-f0-9]{32}$/.test(one("--transaction")??"") || !/^sha256:[a-f0-9]{64}$/.test(one("--expected-recovery")??"") || !["complete","restore"].includes(one("--action")))invalid=true;
  }
  if([...flags.keys()].some(f=>!allowed.has(f)))invalid=true;
  return {invalid,format,operation,changeId,root:one("--root"),transaction:one("--transaction"),expectedRecovery:one("--expected-recovery"),action:one("--action")};
}
function render(result) {
  let text=`Record store: ${result.status} (storage-only)\n`;
  text+=`Revision: ${result.revision??"unavailable"}\n`;
  for(const file of result.files)text+=`${file.path}: ${file.identity??"absent"}\n`;
  if(result.snapshot) for(const record of result.snapshot.records)text+=`\n${record.path}\n${record.content??"[missing]\n"}`;
  for(const diagnostic of [...result.observations,...result.errors])text+=`${diagnostic.code}${diagnostic.path?` ${diagnostic.path}`:""}: ${diagnostic.message}\n`;
  if(result.transaction)text+=`Transaction: ${result.transaction.id}\nRecovery identity: ${result.transaction.recovery_identity??"unavailable"}\n`;
  return text;
}
export function executeRecordStoreCli(args,options={}) {
  const selected=parseRecordStoreArgs(args);
  let result=emptyRecordResult(selected.operation,selected.changeId);
  if(selected.invalid)result.errors=[{code:"invalid-input",path:null,message:"Invalid record-store arguments."}];
  else {
    try {
      const request=["record","check"].includes(selected.operation)?parseAdvancedRequest(options.input??(options.readInput??input)()):undefined;
      // Public new-store adoption is coordinated with consumers in M4.
      if(request?.contract==="rigorloop-records-v3" && request.expected_revision===null)stop("unsupported-contract");
      result=executeRecordStore({...selected,request},options);
    } catch(e) {
      const code=e.recordStoreCode??(e.code?"io-failure":String(e.message).includes("limit")?"limit-exceeded":"invalid-input");
      result.errors=[{code,path:null,message:`Record store: ${code}.`}];
    }
  }
  return {result,format:selected.format,exitCode:EXITS[result.status],human:render(result)};
}
