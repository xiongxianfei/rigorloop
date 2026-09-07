import {validatePrimaryResult} from "./recording-contract.js";
import {stop} from "./record-store-files.js";
import {scanObservations,canonicalJSON} from "./recording-observations.js";
export const QUERY_KINDS=Object.freeze(["work","review","finding","blocker","evidence","decision","verify","decisions","model","proposal","plan","activity","applicability"]);
export const MUTATIONS=Object.freeze(["change.create","change.link","activity.set","work.add","work.set","review.record","finding.add","finding.set","blocker.add","blocker.set","evidence.record","applicability.set","decision.record","verify.record","batch"]);
export const ERROR_CODES=Object.freeze(["invalid-input","unsupported-contract","unsafe-path","broken-reference","identity-conflict","store-busy","recovery-needed","io-failure","limit-exceeded","missing-input","target-not-found","target-exists","overlapping-operation","invalid-cursor","immutable-origin"]);
export const EXITS=Object.freeze({inspected:0,valid:0,saved:0,unchanged:0,rejected:2,conflict:3,busy:4,"recovery-required":5});
export {exact,id,isDigest,safePath,validatePrimaryResult} from "./recording-contract.js";
export function renderPrimary(r){return `Record: ${r.status} (storage-only)\n`+(Object.hasOwn(r,"record_contract")?`Record contract: ${r.record_contract??"none (no stored contract)"}\n`:"")+JSON.stringify(r,null,2)+"\n";}
export function serializePrimary(result,maxBytes=8388608,{format="json"}={}){validatePrimaryResult(result);const json=JSON.stringify(result)+"\n",human=renderPrimary(result);if(Buffer.byteLength(json)>maxBytes||(format==="text"&&Buffer.byteLength(human)>maxBytes))stop("limit-exceeded");return{result,json,human,exitCode:EXITS[result.status]};}
export function preparePrimaryReceipt({details,...result}){result={schema_version:2,claim:"storage-only",...result};if(result.observation_summary===undefined)delete result.observation_summary;if(details!==undefined){const expanded={...result,details:{included:true,...details}};try{return serializePrimary(expanded,8388608,{format:"text"});}catch(e){if(e.recordStoreCode!=="limit-exceeded")throw e;result.details={included:false,reason:"response-limit"};}}return serializePrimary(result,8388608,{format:"text"});}
export function boundAdvancedObservations(iterable,budget){const counts=new Map(),items=[];let bytes=2,overflow=false;for(const d of iterable){if(!["absent-change","subject-drift","failed-evidence","inconsistent-claim"].includes(d.code))stop("invalid-input");counts.set(d.code,(counts.get(d.code)??0)+1);bytes+=Buffer.byteLength(JSON.stringify(d))+1;if(bytes>budget){overflow=true;items.length=0;}if(!overflow)items.push(d);}return overflow?[...counts].map(([code,count])=>({code,path:null,message:`Record store: ${count} ${code} observations; details omitted. Use observations show for current detail.`})):items;}

// The constructor supplies explicit changed targets. The engine still owns all
// structural, conflict and recovery checks; this hook only prepares output.
export function primaryReceiptPreparer({operation,changeId,changed,details}) {
 return ({status,set,format,reader,revision,before_revision})=>{
  const scan=scanObservations({set,format,reader,revision}),preview=status==="valid";
  return preparePrimaryReceipt({operation,status,change_id:changeId,revision:preview?before_revision:revision,...(preview?{candidate_revision:revision}:{}),changed:status==="unchanged"?[]:[...new Map(changed.map(c=>[canonicalJSON(c),c])).values()],observation_summary:scan.summary(preview?"candidate-snapshot":"registered-snapshot"),...(details!==undefined?{details}:{} )});
 };
}
