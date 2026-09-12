import {parseProjectYaml,findRepositoryRoot} from './project-files.js';
import {existsSync,lstatSync,readFileSync,opendirSync} from 'node:fs';
import {isAbsolute,join,relative,resolve,sep} from 'node:path';
import {RecordFiles,stop,MIB} from './record-store-files.js';
import {classifyRecordDirectory} from './record-discovery.js';
import {withRecordSnapshot} from './record-store.js';
import {id as safeId,isDigest,exact} from './recording-contract.js';
import {validateAdvancedEnvelope} from './record-store-transport.js';
import {emptyRecordResult} from './record-store.js';
export const WORKFLOW_CONTEXT_FORMATS=Object.freeze(['human','json']);
export const WORKFLOW_CONFIG_SCHEMA_VERSIONS=Object.freeze([1]);
const CONFIG_PATH='rigorloop.workflow.yaml';
const TEMPLATE_VARIABLES=new Set(['change-id','date','slug','review-round','stage','milestone-id']);
const ENTRY_FIELDS=new Set(['path_template','owner']);
export const BUNDLED_WORKFLOW_DEFAULTS = Object.freeze({
  schema_version: 1,
  artifact_locations: Object.freeze({
    "change-record": Object.freeze({ path_template: "docs/changes/<change-id>/change.json", owner: "workflow" }),
    proposal: Object.freeze({ path_template: "docs/proposals/<change-id>.md", owner: "proposal" }),
    spec: Object.freeze({ path_template: "specs/<slug>.md", owner: "spec" }),
    architecture: Object.freeze({ path_template: "docs/architecture/<change-id>.md", owner: "architecture" }),
    adr: Object.freeze({ path_template: "docs/adr", owner: "architecture" }),
    plan: Object.freeze({ path_template: "docs/plans/<change-id>.md", owner: "plan" }),
    "proposal-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/proposal-review.json", owner: "proposal-review" }),
    "design-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/design-review.json", owner: "design-review" }),
    "delivery-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/delivery-review.json", owner: "delivery-review" }),
    "code-review-record": Object.freeze({ path_template: "docs/changes/<change-id>/reviews/code-review.json", owner: "code-review" }),
    "implementation-evidence": Object.freeze({ path_template: "docs/changes/<change-id>/evidence.json", owner: "implement" }),
    "verification-report": Object.freeze({ path_template: "docs/changes/<change-id>/verify-report.json", owner: "verify" }),
  }),
});


const SUPPORTED_KINDS=new Set(Object.keys(BUNDLED_WORKFLOW_DEFAULTS.artifact_locations));
const EXPECTED_OWNERS=Object.fromEntries(Object.entries(BUNDLED_WORKFLOW_DEFAULTS.artifact_locations).map(([k,v])=>[k,v.owner]));
const RECORD_KINDS=new Set([...SUPPORTED_KINDS].filter(k=>!['proposal','spec','architecture','adr','plan'].includes(k)));
function diagnostic(code,invariant,path=null){
 code=code==='RL_CONTEXT_PATH_UNSAFE'?'unsafe-path':code.startsWith('RL_CONTEXT_')?'invalid-input':code;
 return {code,path,message:`Workflow context: ${code}.`};
}
function safeRepositoryPath(root, candidate) {
  if (typeof candidate !== "string" || !candidate || candidate.includes("\\") || isAbsolute(candidate) || /^[A-Za-z]:/.test(candidate)) return false;
  const parts = candidate.split("/");
  if (parts.some((part) => !part || part === "." || part === "..")) return false;
  const absolute = resolve(root, candidate);
  const rel = relative(root, absolute);
  if (rel === ".." || rel.startsWith(`..${sep}`) || rel.startsWith(sep)) return false;
  let cursor = root;
  for (const part of parts) {
    cursor = join(cursor, part);
    let info; try { info=lstatSync(cursor); } catch(e) { if(e.code!=="ENOENT") throw e; }
    if (info?.isSymbolicLink()) return false;
  }
  return true;
}

function validateTemplate(root, artifactKind, template) {
  if (!safeRepositoryPath(root, template)) return diagnostic("RL_CONTEXT_PATH_UNSAFE", "workflow-context-path", CONFIG_PATH, artifactKind, [artifactKind]);
  const variables = [...template.matchAll(/<([^>]+)>/g)].map((match) => match[1]);
  if (variables.some((value) => !TEMPLATE_VARIABLES.has(value)) || template.replace(/<[^>]+>/g, "").includes("<") || template.replace(/<[^>]+>/g, "").includes(">")) {
    return diagnostic("RL_CONTEXT_CONFIG_INVALID", "workflow-context-template-variable", CONFIG_PATH, artifactKind, [artifactKind]);
  }
  return null;
}

function invalidConfiguration(code, invariant, artifactKind = null) {
  return { error: diagnostic(code, invariant, CONFIG_PATH, artifactKind, artifactKind ? [artifactKind] : []) };
}

function loadConfiguration(root) {
  const configAbsolute = join(root, CONFIG_PATH);
  const effective = Object.fromEntries(Object.entries(BUNDLED_WORKFLOW_DEFAULTS.artifact_locations).map(([kind, value]) => [kind, { ...value, provenance: "bundled-default" }]));
  let configStat; try { configStat=lstatSync(configAbsolute); } catch(e) { if(e.code!=="ENOENT") throw e; }
  if (!configStat) return { configuration: { schema_version: 1, source: "bundled-default", path: null }, effective };
  if (!configStat.isFile() || configStat.isSymbolicLink()) return invalidConfiguration("RL_CONTEXT_PATH_UNSAFE", "workflow-context-config-source");
  let parsed;
  try { parsed = parseProjectYaml(readFileSync(configAbsolute, "utf8")); }
  catch { return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-config-syntax"); }
  if (!WORKFLOW_CONFIG_SCHEMA_VERSIONS.includes(parsed.schema_version)) return invalidConfiguration("RL_CONTEXT_CONFIG_UNSUPPORTED", "workflow-context-config-version");
  if (Object.keys(parsed).some((key) => !["schema_version", "artifact_locations"].includes(key)) || !parsed.artifact_locations || Array.isArray(parsed.artifact_locations) || typeof parsed.artifact_locations !== "object") {
    return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-config-fields");
  }
  for (const [kind, entry] of Object.entries(parsed.artifact_locations)) {
    if (!SUPPORTED_KINDS.has(kind)) return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-artifact-kind", kind);
    if (!entry || Array.isArray(entry) || typeof entry !== "object" || Object.keys(entry).some((key) => !ENTRY_FIELDS.has(key)) || typeof entry.path_template !== "string") {
      return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-location-shape", kind);
    }
    if (entry.owner !== undefined && entry.owner !== EXPECTED_OWNERS[kind]) return invalidConfiguration("RL_CONTEXT_CONFIG_INVALID", "workflow-context-owner", kind);
    if (RECORD_KINDS.has(kind) && entry.path_template !== BUNDLED_WORKFLOW_DEFAULTS.artifact_locations[kind].path_template) return invalidConfiguration("invalid-input", "record-template");
    const templateError = validateTemplate(root, kind, entry.path_template);
    if (templateError) return { error: templateError };
    effective[kind] = { path_template: entry.path_template, owner: EXPECTED_OWNERS[kind], provenance: "repository-override" };
  }
  return { configuration: { schema_version: 1, source: CONFIG_PATH, path: CONFIG_PATH }, effective };
}


function validateResolvedPlacement(root,locations,changeId){
 if(changeId===null)return;
 const dated=/^(\d{4}-\d{2}-\d{2})-(.+)$/.exec(changeId);
 const variables={'change-id':changeId,date:dated?.[1],slug:dated?.[2]??changeId},paths=new Set();
 for(const entry of Object.values(locations)){
  const path=entry.path_template.replace(/<([^>]+)>/g,(match,key)=>variables[key]??match);
  if(/[<>]/.test(path)||paths.has(path))stop('invalid-input');
  if(!safeRepositoryPath(root,path))stop('unsafe-path');
  paths.add(path);
 }
}

function parseArgs(args){
 let change=null,format='human',changeSeen=false,formatSeen=false;
 for(let i=0;i<args.length;i++){
  if(args[i]==='--change'&&!changeSeen&&args[i+1]){changeSeen=true;change=args[++i];}
  else if(args[i]==='--format'&&!formatSeen&&args[i+1]){formatSeen=true;format=args[++i];}
  else if(args[i]==='--json'&&!formatSeen){formatSeen=true;format='json';}
  else return {change:null,format,error:true};
 }
 const error=!WORKFLOW_CONTEXT_FORMATS.includes(format)||(change!==null&&!safeId(change));
 return {change:safeId(change)?change:null,format:WORKFLOW_CONTEXT_FORMATS.includes(format)?format:'human',error};
}
export function workflowContextHuman(r){
 const lines=[`Workflow context: ${r.status}`,`Requested change: ${r.selection.requested_change??'none'}`,`Scope: ${r.scope.mode}; complete=${r.scope.complete}; directories=${r.scope.inspected_directories}; excluded=${r.scope.excluded_noncurrent}; candidates=${r.scope.candidate_count}`];
 if(r.configuration)lines.push(`Configuration: ${r.configuration.source}`);
 for(const [kind,v]of Object.entries(r.locations))lines.push(`Location ${kind}: ${v.path_template} [${v.provenance}]`);
 for(const c of r.candidates)lines.push(`Candidate ${c.change_id}: ${c.path} (${c.record_contract}; ${c.revision})`);
 for(const e of r.errors)lines.push(`Error: ${e.code}${e.path?' at '+e.path:''}`);
 return lines.join('\n')+'\n';
}
export function executeWorkflowContext(args,options={}){
 const parsed=parseArgs(args),r={schema_version:2,command:'workflow-context',status:'success',configuration:null,locations:{},selection:{requested_change:parsed.change},candidates:[],scope:{mode:parsed.change===null?'discovery':'explicit',inspected_directories:0,excluded_noncurrent:0,candidate_count:0,complete:true},errors:[]};
 const fail=(code,path=null)=>{r.status='rejected';r.scope.complete=false;const error=diagnostic(code,null,path);if(!r.errors.some(e=>e.code===error.code&&e.path===error.path))r.errors.push(error);};
 const budget=()=>{if(Buffer.byteLength(JSON.stringify(r))+1>8*MIB)stop('limit-exceeded');};
 try{
  if(parsed.error)stop('invalid-input');
  options.beforeRepositoryRead?.();
  const root=findRepositoryRoot(options.cwd??process.cwd());
  if(!existsSync(join(root,'.git'))&&!existsSync(join(root,'docs/changes')))stop('invalid-input');
  const loaded=loadConfiguration(root);
  if(loaded.error){fail(loaded.error.code,loaded.error.path);}
  else{
   validateResolvedPlacement(root,loaded.effective,parsed.change);
   r.configuration=loaded.configuration;r.locations=loaded.effective;budget();
   const reader=new RecordFiles(root);
   const inspect=id=>{
    const path=`docs/changes/${id}`;
    try{
     if(reader.inspect(path,true).info){r.scope.inspected_directories++;if(r.scope.inspected_directories>1024)stop('limit-exceeded');}
     const readCandidate=()=>{
      if(!safeId(id))stop('invalid-input');
      return withRecordSnapshot(root,id,({set,format,revision})=>{
      if(!Object.keys(set).length)return null;
      format.set(id,set);
      return {change_id:id,path:path+'/change.json',record_contract:format.contract,revision};
      });
     };
     let candidate;
     if(parsed.change!==null)candidate=readCandidate();
     else{
      const kind=classifyRecordDirectory(reader,id);
      if(kind==='absent')return;
      if(kind==='archive'||kind==='noncurrent'){r.scope.excluded_noncurrent++;return;}
      candidate=readCandidate();
      if(!candidate)stop('identity-conflict');
     }
     if(!candidate)return;
     if(r.candidates.length===64)stop('limit-exceeded');
     r.candidates.push(candidate);r.scope.candidate_count=r.candidates.length;budget();
    }catch(e){fail(e.recordStoreCode??(e.code?'io-failure':'invalid-input'),safeId(id)?path:null);}
   };
   if(parsed.change!==null)inspect(parsed.change);
   else{
    const directory=reader.inspect('docs/changes',true);
    if(directory.info){
     const dir=opendirSync(directory.target),ids=[];
     try{for(let entry;(entry=dir.readSync());){
      if(entry.isSymbolicLink())stop('unsafe-path');
      if(entry.isDirectory()){ids.push(entry.name);if(ids.length>1024)stop('limit-exceeded');}
     }}finally{dir.closeSync();}
     reader.assert(directory.chain);
     for(const id of ids.sort())inspect(id);
     reader.assert(directory.chain);
    }
   }
  }
  budget();
 }catch(e){fail(e.recordStoreCode??(e.code?'io-failure':'invalid-input'));}
 // A rejected response still obeys the response budget; never claim truncation is complete.
 if(Buffer.byteLength(JSON.stringify(r))+1>8*MIB){r.locations={};r.candidates=[];r.scope.candidate_count=0;r.errors=[diagnostic('limit-exceeded')];r.status='rejected';r.scope.complete=false;}
 validateWorkflowContextResult(r);
 return {result:r,exitCode:r.status==='success'?0:2,format:parsed.format,human:workflowContextHuman(r)};
}

// Validate the public factual envelope independently of rendering. Closed values
// reject before cross-field consistency; this does not decide workflow readiness.
export function validateWorkflowContextResult(r){
 exact(r,['schema_version','command','status','configuration','locations','selection','candidates','scope','errors']);
 if(r.schema_version!==2||r.command!=='workflow-context'||!['success','rejected'].includes(r.status))stop('invalid-input');
 exact(r.selection,['requested_change']);if(r.selection.requested_change!==null&&!safeId(r.selection.requested_change))stop('invalid-input');
 exact(r.scope,['mode','inspected_directories','excluded_noncurrent','candidate_count','complete']);
 if(!['explicit','discovery'].includes(r.scope.mode)||typeof r.scope.complete!=='boolean')stop('invalid-input');
 for(const k of ['inspected_directories','excluded_noncurrent','candidate_count'])if(!Number.isSafeInteger(r.scope[k])||r.scope[k]<0)stop('invalid-input');
 if(r.configuration!==null){exact(r.configuration,['schema_version','source','path']);if(r.configuration.schema_version!==1||!['bundled-default',CONFIG_PATH].includes(r.configuration.source)||r.configuration.path!==(r.configuration.source===CONFIG_PATH?CONFIG_PATH:null))stop('invalid-input');}
 if(!r.locations||typeof r.locations!=='object'||Array.isArray(r.locations))stop('invalid-input');
 for(const [kind,v]of Object.entries(r.locations)){
  if(!SUPPORTED_KINDS.has(kind))stop('invalid-input');exact(v,['path_template','owner','provenance']);
  if(v.owner!==EXPECTED_OWNERS[kind]||!['bundled-default','repository-override'].includes(v.provenance)||typeof v.path_template!=='string'||!v.path_template.length)stop('invalid-input');
  if(RECORD_KINDS.has(kind)&&v.path_template!==BUNDLED_WORKFLOW_DEFAULTS.artifact_locations[kind].path_template)stop('invalid-input');
 }
 if(!Array.isArray(r.candidates))stop('invalid-input');
 for(const [i,c]of r.candidates.entries()){
  exact(c,['change_id','path','record_contract','revision']);
  if(!safeId(c.change_id)||c.path!==`docs/changes/${c.change_id}/change.json`||!['rigorloop-records-v3'].includes(c.record_contract)||!isDigest(c.revision)||(i&&r.candidates[i-1].change_id>=c.change_id))stop('invalid-input');
 }
 validateAdvancedEnvelope({...emptyRecordResult('inspect','discovery'),errors:r.errors});
 if(r.scope.candidate_count!==r.candidates.length||(r.status==='success')!==(r.errors.length===0)||r.scope.complete!==(r.status==='success')||(r.scope.mode==='explicit')!==(r.selection.requested_change!==null))stop('invalid-input');
 if(r.scope.complete&&(r.scope.inspected_directories>1024||r.candidates.length>64))stop('invalid-input');
 if(Buffer.byteLength(JSON.stringify(r))+1>8*MIB)stop('limit-exceeded');
 return r;
}
