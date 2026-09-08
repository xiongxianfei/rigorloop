import {validateAdvancedEnvelope} from "./record-store-transport.js";
// Version dispatch for the advanced storage interface. No historical conversion.
import {parseRecordStore,validateRecordStoreRecord,validateRecordStoreSet,validateRecordStoreCreation,recordStorePathKind} from "./record-store-contract.js";
import {parseV2Record,validateV2Record,validateV2Set,validateV2Preservation,validateV2Creation,v2PathKind,parseRequestJSON} from "./record-format-v2.js";
import {digest,stop} from "./record-store-files.js";

export const V1_FORMAT=Object.freeze({version:1,contract:"explicit-recording-v1",manifest:"change.yaml",parse:parseRecordStore,validate:validateRecordStoreRecord,set:validateRecordStoreSet,creation:validateRecordStoreCreation,pathKind:recordStorePathKind});
export const V2_FORMAT=Object.freeze({version:2,contract:"rigorloop-records-v2",manifest:"change.json",parse:parseV2Record,validate:validateV2Record,set:validateV2Set,creation:validateV2Creation,pathKind:v2PathKind});
export function requestFormat(request) {
  if(!request || typeof request!=="object" || Array.isArray(request) || typeof request.contract!=="string" || !Object.hasOwn(request,"schema_version"))stop("invalid-input");
  const format=request?.contract===V1_FORMAT.contract?V1_FORMAT:request?.contract===V2_FORMAT.contract?V2_FORMAT:null;
  if(!format || request.schema_version!==format.version) stop("unsupported-contract");
  return format;
}
export function parseAdvancedRequest(input) {
  const request=parseRequestJSON(input);
  validateAdvancedRequest(request);
  return request;
}
export function validateAdvancedRequest(request) {
  return requestFormat(request).validate("request",request);
}
export function preserveRecords(format,id,before,candidate) {
  if(format===V2_FORMAT && Object.keys(before).length) validateV2Preservation(id,before,candidate);
  else format.set(id,candidate);
}
function exact(value,keys) {
  if(!value||typeof value!=="object"||Array.isArray(value)||Object.keys(value).sort().join(",")!==[...keys].sort().join(","))stop("invalid-input");
}

export function validateAdvancedResult(result) {
  if(result?.operation!=="inspect" || result.status!=="inspected" || !(Array.isArray(result.snapshot?.records) && result.snapshot.records.some(r=>r?.path===`docs/changes/${result.change_id}/change.json`)))
    return result?.operation==="inspect" && result.status==="inspected" ? validateRecordStoreRecord("result",result) : validateAdvancedEnvelope(result);
  // Transport schema 1 is independent of stored v1. Validate the actual envelope
  // before checking the v2 snapshot against its own representation contract.
  validateAdvancedEnvelope(result);
  exact(result.snapshot,["records"]);
  const records=result.snapshot.records;
  if(!Array.isArray(records)||records.length!==result.files.length||records.length>65)stop("invalid-input");
  const manifest=`docs/changes/${result.change_id}/change.json`, entry=records.find(r=>r.path===manifest);
  const change=parseV2Record("change",entry.content);
  if(change.change_id!==result.change_id)stop("invalid-input");
  const membership=new Set([manifest,...change.records.map(r=>r.path)]);
  if(membership.size!==records.length)stop("invalid-input");
  for(let i=0;i<records.length;i++) {
    const record=records[i],file=result.files[i];exact(record,["path","content"]);
    if(record.path!==file.path||!membership.has(record.path)||(i&&records[i-1].path>=record.path))stop("invalid-input");
    if(record.content===null) {
      if(file.identity!==null||!result.observations.some(o=>o.code==="subject-drift"&&o.path===record.path))stop("invalid-input");
    } else {
      const kind=v2PathKind(result.change_id,record.path),data=parseV2Record(kind,record.content);
      if(data.change_id!==result.change_id || (kind==="review"&&record.path!==`docs/changes/${result.change_id}/reviews/${data.id}.json`) || digest(record.content)!==file.identity)stop("invalid-input");
    }
  }
  if(result.revision!==digest(JSON.stringify(result.files.map(f=>[f.path,f.identity]))))stop("invalid-input");
  return result;
}
