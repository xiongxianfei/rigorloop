import {createHash} from "node:crypto";
import {digest,stop} from "./record-store-files.js";
export const OBSERVATION_CODES=Object.freeze(["absent-change","subject-drift","failed-evidence","inconsistent-claim","missing-content"]);
export const canonicalJSON=value=>JSON.stringify(canonical(value));
function canonical(value){return Array.isArray(value)?value.map(canonical):value!==null&&typeof value==="object"?Object.fromEntries(Object.keys(value).sort().map(k=>[k,canonical(value[k])])):value;}
export const compare=(a,b)=>a<b?-1:a>b?1:0;

// Records have already passed their closed schema. Only Subject has exactly
// path/identity; EntryRef has path/id, and narrative strings are never traversed.
export function scanObservations({set,format,reader,revision}) {
 const parsed=new Map(),assertions=new Map(),locations=new Map();
 const add=(code,path,location)=>{
  if(!OBSERVATION_CODES.includes(code))stop("invalid-input");
  const key=path??"",entries=locations.get(key)??new Map();
  entries.set(`${location}\0${code}`,{code,path,location});locations.set(key,entries);
 };
 function subjects(value,path,location="") {
  if(!value||typeof value!=="object")return;
  if(!Array.isArray(value)&&Object.keys(value).length===2&&typeof value.path==="string"&&typeof value.identity==="string") {
   const refs=assertions.get(value.path)??[];refs.push({expected:value.identity,location:`${path}#${location}`});assertions.set(value.path,refs);return;
  }
  for(const key of Object.keys(value).sort())subjects(value[key],path,location+(Array.isArray(value)?`[${key}]`:(location?".":"")+key));
 }
 let change,manifest,failed=false;
 for(const path of Object.keys(set).sort()) {
  if(set[path]===null){add("subject-drift",path,"");add("missing-content",path,"");continue;}
  const kind=format.pathKind(path.split("/")[2],path),data=format.parse(kind,set[path]);
  if(data.change_id!==path.split("/")[2]||(kind==="review"&&!path.endsWith(`/reviews/${data.id}.${format.version===1?"md":"json"}`)))stop("invalid-input");
  parsed.set(path,data);subjects(data,path);
  if(kind==="change"){change=data;manifest=path;}
  for(const [i,check]of (data.checks??[]).entries())if(check.result==="failed"){failed=true;add("failed-evidence",path,`checks[${i}].result`);}
 }
 if(!Object.keys(set).length)add("absent-change",null,"");
 if(change?.activity.status==="completed"&&(failed||change.blockers.some(b=>b.state==="open")))add("inconsistent-claim",manifest,"activity.status");
 const observed=[];
 for(const path of [...assertions.keys()].sort()) {
  // Snapshot-owned subjects must use candidate/current bytes from this scan.
  const identity=Object.hasOwn(set,path)?digest(set[path]):reader.hash(path);
  observed.push({path,identity});
  for(const ref of assertions.get(path))if(ref.expected!==identity)add("subject-drift",path,ref.location);
 }
 const paths=[...locations.keys()].sort(),by_code=Object.fromEntries(OBSERVATION_CODES.map(c=>[c,0]));
 for(const map of locations.values())for(const {code}of map.values())by_code[code]++;
 function* diagnostics(){for(const path of paths)for(const d of [...locations.get(path).values()].sort((a,b)=>compare(a.location,b.location)||compare(a.code,b.code)))yield{code:d.code,path:d.path,message:`Record store: ${d.code}.`,location:d.location};}
 // Stream the largest preimage component; no complete diagnostic payload is built.
 const hash=createHash("sha256");hash.update('{"observations":[');let comma=false;
 for(const d of diagnostics()){if(comma)hash.update(",");hash.update(canonicalJSON(d));comma=true;}
 hash.update('],"observed_subjects":[');comma=false;
 for(const s of observed){if(comma)hash.update(",");hash.update(canonicalJSON(s));comma=true;}
 hash.update('],"revision":'+JSON.stringify(revision)+',"schema_version":2}');
 const identity=`sha256:${hash.digest("hex")}`,total=Object.values(by_code).reduce((a,b)=>a+b,0);
 return {parsed,subjects:observed,diagnostics,identity,total,by_code,
  summary:(scope="registered-snapshot")=>total?{scope,total,by_code:{...by_code},details_included:false,observation_identity:identity}:undefined};
}
