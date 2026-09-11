import {RECORDING_SCHEMA,validate,exact} from './recording-contract.js';
import {canonicalJSON} from './recording-observations.js';
import {RecordDocument,indentedJSON} from './recording-spans.js';
import {digest,stop} from './record-store-files.js';
import {V2_FORMAT,V3_FORMAT} from './record-store-format.js';

const producers=['review.record','evidence.record','decision.record','verify.record'];
function missing(field){throw Object.assign(new Error('missing-input'),{recordStoreCode:'missing-input',field});}
function requiredInputs(schema,value,location=''){
 if(schema.$ref)return requiredInputs(RECORDING_SCHEMA.$defs[schema.$ref.split('/').at(-1)],value,location);
 const branches=schema.oneOf??schema.anyOf;
 if(branches){const resolved=branches.map(b=>b.$ref?RECORDING_SCHEMA.$defs[b.$ref.split('/').at(-1)]:b),matching=resolved.filter(b=>b.type==='null'?value===null:b.type==='object'?value&&typeof value==='object'&&!Array.isArray(value)&&(!b.required?.length||b.required.some(k=>Object.hasOwn(value,k))):false);if(matching.length===1)requiredInputs(matching[0],value,location);return;}
 if(schema.type==='object'&&value&&typeof value==='object'&&!Array.isArray(value)){
  for(const key of schema.required??[])if(!Object.hasOwn(value,key))missing(location?location+'.'+key:key);
  for(const [key,child]of Object.entries(schema.properties))if(Object.hasOwn(value,key))requiredInputs(child,value[key],location?location+'.'+key:key);
 }
 if(schema.type==='array'&&Array.isArray(value))value.forEach((v,i)=>requiredInputs(schema.items,v,location+'['+i+']'));
}
export function validateMutationRequest(request,batch=false){
 exact(request,['schema_version','interface','contract','change_id','expected_revision','reads',batch?'operations':'operation']);
 const version=request.contract===V2_FORMAT.contract?2:request.contract===V3_FORMAT.contract?3:null;
 if(!version)stop('unsupported-contract');
 const operations=batch?request.operations:[request.operation];
 if(!Array.isArray(operations)||!operations.length||operations.length>64)stop('invalid-input');
 for(const [index,operation]of operations.entries()){
  try{
   const schema=RECORDING_SCHEMA.$defs[`v${version}-operation-${operation?.op}`];if(!schema)stop(['review.set','verify.set'].includes(operation?.op)?'unsupported-contract':'invalid-input');
   if(operation.op==='change.create'&&batch)stop('invalid-input');
   exact(operation,['op','target','values'],producers.includes(operation.op)?['applicability']:[]);
   if(!operation.values||typeof operation.values!=='object'||Array.isArray(operation.values))stop('invalid-input');
   if((version===2||operation.op.startsWith('blocker.'))&&(Object.hasOwn(operation.values,'origin')||(operation.op.endsWith('.set')&&Object.hasOwn(operation.values,'basis'))))stop('immutable-origin');
   for(const field of schema.properties.values.required??[])if(!Object.hasOwn(operation.values,field))missing(field);
   if(operation.op.endsWith('.set')&&!Object.keys(operation.values).length){if(['review.set','verify.set'].includes(operation.op))stop('invalid-input');missing('values');}
   if(['finding.set','blocker.set'].includes(operation.op)&&Object.hasOwn(operation.values,'state')!==Object.hasOwn(operation.values,'resolution'))missing(Object.hasOwn(operation.values,'state')?'resolution':'state');
   requiredInputs(schema.properties.values,operation.values);
   if(operation.applicability)requiredInputs(schema.properties.applicability,operation.applicability,'applicability');
   validate(schema,operation);
  }catch(e){e.operation_index=index;throw e;}
 }
 validate(RECORDING_SCHEMA.$defs['mutation-request'],request);
 if((request.expected_revision===null)!==(!batch&&request.operation.op==='change.create'))stop('invalid-input');
 const paths=new Set();for(const read of request.reads){if(paths.has(read.path)||read.path.startsWith('.rigorloop/record-store/'))stop('invalid-input');paths.add(read.path);}
 return version===3?V3_FORMAT:V2_FORMAT;
}

// Pure construction: all decisions and source bytes are inputs. The publisher
// independently owns containment, current-file checks and every filesystem write.
export function constructMutation(request,before){
 const format=request.contract===V3_FORMAT.contract?V3_FORMAT:V2_FORMAT;
 const prefix=`docs/changes/${request.change_id}/`,manifest=prefix+format.manifest;
 const docs=new Map(),touched=new Set(),assignments=new Set(),changed=[],effects=[];
 const operations=request.operations??[request.operation];let operation_index=0,edits=0,appEdits=0;
 for(const [path,source]of Object.entries(before))if(source!==null){const kind=format.pathKind(request.change_id,path),data=format.parse(kind,source);docs.set(path,new RecordDocument(format,kind,source,data));}
 let change=docs.get(manifest);
 const use=path=>{if(Object.hasOwn(before,path)&&before[path]===null)stop('broken-reference');const doc=docs.get(path);if(!doc)stop('target-not-found');return doc;};
 const claim=key=>{if(assignments.has(key))stop('overlapping-operation');assignments.add(key);};
 const effect=(path,target,fields,bookkeeping=false)=>effects.push({operation_index,path,target,changed_fields:fields,bookkeeping});
 function set(doc,path,value){const prior=doc.source;doc.edit(path,value);if(doc.source!==prior)edits++;touched.add(doc);}
 function append(doc,path,value){edits++;doc.edit(path,value,true);touched.add(doc);}
 function newDoc(path,kind,data,body){edits++;data={...data,...(body!==undefined?{body}:{})};const source=canonicalJSON(data)+'\n';const doc=new RecordDocument(format,kind,source,data);docs.set(path,doc);touched.add(doc);return doc;}
 function concern(values,id){const {basis,...current}=structuredClone(values);let supporting_judgment=basis.supporting_judgment;if(supporting_judgment?.snapshot)supporting_judgment=supporting_judgment.snapshot;else if(supporting_judgment?.from_review){const review=use(prefix+`reviews/${supporting_judgment.from_review}.json`).data;supporting_judgment={...Object.fromEntries(['reviewer','contributors','independence_basis','subjects','judgment'].map(k=>[k,structuredClone(review[k])])),rationale:supporting_judgment.rationale};}return{id,...current,origin:{...Object.fromEntries(['reporter','subjects','evidence','required_outcome'].map(k=>[k,structuredClone(current[k])])),rationale:basis.rationale,supporting_judgment}};}
 function applicable(path,value){const initial=edits;claim('applicability:'+path);const i=change.data.applicability.findIndex(x=>x.path===path),entry={path,...value};if(i<0)append(change,['applicability'],entry);else for(const [key,v]of Object.entries(value))set(change,['applicability',i,key],v);appEdits+=edits-initial;if(edits!==initial)changed.push({kind:'applicability',target:{path}});effect(manifest,{path},Object.keys(value),false);}
 function support(path,kind,op){if(Object.hasOwn(before,path)&&before[path]===null)stop('broken-reference');let doc=docs.get(path);if(!doc){if(change.data.records.some(r=>r.path===path))stop('broken-reference');if(op.applicability===undefined)missing('applicability');if(kind==='decisions'&&op.values.body===undefined)missing('body');const base={schema_version:format.version,change_id:request.change_id};if(kind==='review')Object.assign(base,{id:op.target.id,findings:[]});if(kind==='evidence')base.checks=[];if(kind==='decisions')base.decisions=[];doc=newDoc(path,kind,base,['review','decisions','verify'].includes(kind)?op.values.body:undefined);append(change,['records'],{path,kind});effect(manifest,{path},['records'],true);}if(op.applicability!==undefined)applicable(path,op.applicability);return doc;}
 function entry(doc,collection,id,values,mode){const namespace=[...docs].find(([,d])=>d===doc)[0]+":"+collection+":"+id;const i=doc.data[collection].findIndex(x=>x.id===id);if((mode==='add'||mode==='record')&&[...assignments].some(k=>k.startsWith(namespace+':')))stop('overlapping-operation');if(mode==='add'&&i>=0)stop('target-exists');if(mode==='set'&&i<0)stop('target-not-found');if(mode==='add'||mode==='record'){if([...assignments].some(k=>k.startsWith(namespace+":")))stop('overlapping-operation');claim(namespace+":whole");}else if(assignments.has(namespace+":whole"))stop('overlapping-operation');for(const key of Object.keys(values))claim(namespace+":"+key);if(i<0)append(doc,[collection],{id,...values});else for(const [key,value]of Object.entries(values))set(doc,[collection,i,key],value);}
 for(const op of operations){try{
  const startingEdits=edits,startingAppEdits=appEdits;const {target,values}=op;let path=manifest,kind=op.op.split('.')[0],doc=change;
  if(op.op==='change.create'){
   if(change)stop('target-exists');const blockers=values.blockers.map(b=>{const {id,...v}=b;return concern(v,id);});change=newDoc(manifest,'change',{schema_version:format.version,contract:format.contract,change_id:request.change_id,...values,blockers,records:[],applicability:[]});doc=change;
  }else{
   if(!change)stop('target-not-found');
   if(op.op==='change.link'){
    if(!request.reads.some(r=>r.path===values.subject.path&&r.identity===values.subject.identity))missing('reads');
    claim('link:'+target.kind+':'+(target.id??''));
    if(target.kind==='model'){const i=change.data.models.findIndex(m=>m.id===target.id);if(i<0)append(change,['models'],{id:target.id,subject:values.subject});else set(change,['models',i,'subject'],values.subject);}else set(change,[target.kind],values.subject);kind=target.kind;
   }else if(op.op==='activity.set'){claim('activity');set(change,['activity'],values);}
   else if(op.op.startsWith('work.'))entry(change,'work',target.id,values,op.op.split('.')[1]);
   else if(op.op.startsWith('blocker.')){entry(change,'blockers',target.id,op.op.endsWith('.add')?Object.fromEntries(Object.entries(concern(values,target.id)).filter(([k])=>k!=='id')):values,op.op.split('.')[1]);}
   else if(op.op.startsWith('finding.')){path=prefix+`reviews/${target.review}.${'json'}`;doc=use(path);entry(doc,'findings',target.id,op.op.endsWith('.add')&&format.version===2?Object.fromEntries(Object.entries(concern(values,target.id)).filter(([k])=>k!=='id')):values,op.op.split('.')[1]);}
   else if(op.op==='applicability.set'){if(!change.data.records.some(r=>r.path===target.path))stop('target-not-found');use(target.path);applicable(target.path,values);}
   else{
    const recordKind=kind==='decision'?'decisions':kind;
    path=prefix+(kind==='review'?`reviews/${target.id}.${'json'}`:kind==='evidence'?`evidence.${'json'}`:kind==='decision'?`material-decisions.${'json'}`:`verify-report.${'json'}`);
    doc=op.op.endsWith('.set')?use(path):support(path,recordKind,op);const {body,...fields}=values;
    if(kind==='evidence'||kind==='decision')entry(doc,kind==='evidence'?'checks':'decisions',target.id,fields,'record');
    else{
     const keys=Object.keys(fields);
     if(format.version===3&&op.op==='verify.record'&&!keys.includes('verification_basis'))keys.push('verification_basis');
     for(const key of keys){claim(path+':'+key);if(Object.hasOwn(fields,key))set(doc,[key],fields[key]);else if(Object.hasOwn(doc.data,key)){doc.remove([key]);edits++;touched.add(doc);}}
    }
    if(body!==undefined){claim(path+':body');if(Object.hasOwn(before,path)){const prior=doc.source;doc.body(body);if(doc.source!==prior)edits++;}else{doc.data.body=body;doc.newBody=body;}touched.add(doc);}
   }
  }
  if(edits-startingEdits!==appEdits-startingAppEdits)changed.push({kind,target:op.op==='change.link'?(target.kind==='model'?{id:target.id}:{}):target});effect(path,op.op==='change.link'?(target.id?{id:target.id}:{}):target,Object.keys(values));operation_index++;
 }catch(e){e.operation_index=operation_index;throw e;}}
 const writes=[];for(const [path,doc]of docs)if(touched.has(doc)){let content=doc.source;if(!Object.hasOwn(before,path)){content=indentedJSON(doc.data)+'\n';}writes.push({path,expected_identity:Object.hasOwn(before,path)?digest(before[path]):null,content});}
 return {request:{schema_version:2,contract:format.contract,change_id:request.change_id,expected_revision:request.expected_revision,reads:request.reads.map(r=>({path:r.path,expected_identity:r.identity})),writes},changed,effects};
}
