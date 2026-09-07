import {readFileSync} from "node:fs";
import {stop,digest} from "./record-store-files.js";
import {canonicalJSON} from "./recording-observations.js";
export const RECORDING_SCHEMA=JSON.parse(readFileSync(new URL("../schemas/targeted-recording-v1.schema.json",import.meta.url),"utf8"));
export const id=v=>typeof v==="string"&&/^[a-z0-9][a-z0-9-]{0,79}$/.test(v);
export const isDigest=v=>typeof v==="string"&&/^sha256:[a-f0-9]{64}$/.test(v);
export function safePath(path){if(typeof path!=="string"||!path.length||path.length>1024||!/^[\x20-\x7e]+$/.test(path)||path.includes("\\")||/^[A-Za-z]:/.test(path)||path.split("/").some(p=>!p||p==="."||p===".."))stop("unsafe-path");return path;}
export function exact(v,required,optional=[]){if(!v||typeof v!=="object"||Array.isArray(v)||required.some(k=>!Object.hasOwn(v,k))||Object.keys(v).some(k=>![...required,...optional].includes(k)))stop("invalid-input");}
function validate(schema,value){
 if(schema.$ref){const key=schema.$ref.split("/").at(-1);if(key.endsWith("-path"))safePath(value);return validate(RECORDING_SCHEMA.$defs[key],value);}
 if(schema.anyOf||schema.oneOf){let matches=0,unsafe;for(const branch of schema.anyOf??schema.oneOf){try{validate(branch,value);matches++;if(schema.anyOf)return;}catch(e){if(e.recordStoreCode==="unsafe-path")unsafe=e;}}if(schema.oneOf&&matches===1)return;if(!matches&&unsafe)throw unsafe;stop("invalid-input");}
 if(Object.hasOwn(schema,"const")&&schema.const!==value)stop("invalid-input");if(schema.enum&&!schema.enum.includes(value))stop("invalid-input");
 if(schema.type==="null"&&value!==null)stop("invalid-input");
 if(schema.type==="boolean"&&typeof value!=="boolean")stop("invalid-input");
 if(schema.type==="integer"&&(!Number.isSafeInteger(value)||value<schema.minimum||value>schema.maximum))stop("invalid-input");
 if(schema.type==="string"&&(typeof value!=="string"||(schema.minLength!==undefined&&value.length<schema.minLength)||(schema.maxLength!==undefined&&value.length>schema.maxLength)||(schema.pattern&&!new RegExp(schema.pattern).test(value))))stop("invalid-input");
 if(schema.type==="object"){exact(value,schema.required,Object.keys(schema.properties).filter(k=>!schema.required.includes(k)));for(const [key,child]of Object.entries(schema.properties))if(Object.hasOwn(value,key))validate(child,value[key]);}
 if(schema.type==="array"){if(!Array.isArray(value)||(schema.minItems!==undefined&&value.length<schema.minItems)||(schema.maxItems!==undefined&&value.length>schema.maxItems))stop("invalid-input");for(const child of value)validate(schema.items,child);if(schema.uniqueItems&&new Set(value.map(canonicalJSON)).size!==value.length)stop("invalid-input");}
}
export function validateQueryInput(value){validate(RECORDING_SCHEMA.$defs.query,value);return value;}
export function validatePrimaryResult(r){
 validate(RECORDING_SCHEMA.$defs.result,r);
 if(r.observation_summary){const s=r.observation_summary;if(s.total!==Object.values(s.by_code).reduce((a,b)=>a+b,0))stop("invalid-input");if(["saved","unchanged","inspected"].includes(r.status)&&s.scope!=="registered-snapshot")stop("invalid-input");if(r.status==="valid"&&s.scope!=="candidate-snapshot")stop("invalid-input");}
 if((r.observations!==undefined)!==(r.observations_scope!==undefined))stop("invalid-input");if(r.observations&&r.operation!=="subject.inspect")stop("invalid-input");if(r.operation==="subject.inspect"&&(r.change_id!==undefined||r.revision!==undefined||r.observation_summary!==undefined))stop("invalid-input");
 if(r.status!=="inspected")return r;
 if(r.operation==="subject.inspect"){
  const s=r.data.subjects;if(new Set(s.map(x=>x.path)).size!==s.length)stop("invalid-input");if(r.data.contents){if(r.data.contents.length!==s.length)stop("invalid-input");r.data.contents.forEach((c,i)=>{if(c.path!==s[i].path||digest(c.content)!==s[i].identity)stop("invalid-input");});}
  for(const subject of s)if(subject.identity===null&&!r.observations?.some(d=>d.path===subject.path))stop("invalid-input");return r;
 }
 if((r.record_contract===null)!==(r.revision===null))stop("invalid-input");
 if(r.operation==="status"){
  if(r.data){for(const group of Object.values(r.data.counts))if(group.known_total!==Object.values(group.by_value).reduce((a,b)=>a+b,0)||(group.total===null)!==(group.missing_paths.length>0)||(group.total!==null&&group.total!==group.known_total))stop("invalid-input");}
  if(r.scope.complete!==(r.scope.missing_paths.length===0))stop("invalid-input");return r;
 }
 const scope=r.scope,rows=r.data.items??r.data.observations;
 if(scope.returned!==rows.length||(scope.total!==null&&scope.total<scope.returned))stop("invalid-input");
 if(scope.complete!==(scope.next===null&&!(scope.missing_paths?.length)))stop("invalid-input");
 if(r.operation==="observations.show")return r;
 if((scope.total===null)!==(scope.missing_paths.length>0))stop("invalid-input");
 for(const item of rows){if(item.fields?.schema_version!==undefined&&item.fields.schema_version!==(r.record_contract==="rigorloop-records-v2"?2:1))stop("invalid-input");if(item.origin_available!==undefined&&item.origin_available!==(r.record_contract==="rigorloop-records-v2"))stop("invalid-input");if(r.operation.endsWith(".show")&&item.kind!==r.operation.split(".")[0])stop("invalid-input");}
 return r;
}
