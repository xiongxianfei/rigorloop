import {opendirSync} from 'node:fs';
import {stop,MIB} from './record-store-files.js';
import {decode,strictJSON,plain} from './record-json.js';

// Recognition uses only format headers, never historical assessment semantics.
function header(reader,path){return strictJSON(decode(reader.read(path),MIB));}
function privateState(reader,id){
 const base=`.rigorloop/record-store/${id}`,lock=reader.read(`${base}/lock`);
 if(lock!==null){
  let owner;try{owner=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(lock));}catch{stop('recovery-needed');}
  let live=false;
  if(Number.isSafeInteger(owner?.pid)&&owner.pid>0){try{process.kill(owner.pid,0);live=true;}catch(e){live=e.code==='EPERM';}}
  stop(live?'store-busy':'recovery-needed');
 }
 if(reader.inspect(`${base}/journal.json`).info)stop('recovery-needed');
}
function* directoryEntries(reader,reviews){
 if(reader.list){yield* reader.list(reviews.target);return;}
 const dir=opendirSync(reviews.target);
 try{for(let entry;(entry=dir.readSync());)yield entry;}finally{dir.closeSync();}
}
export function classifyRecordDirectory(reader,id){
 const directory=`docs/changes/${id}`,root=reader.inspect(directory,true);
 if(!root.info)return 'absent';
 const json=reader.inspect(`${directory}/change.json`).info;
 const yaml=reader.inspect(`${directory}/change.yaml`).info;
 if(json&&yaml)stop('invalid-input');
 let archived=false;
 if(json){
  const value=header(reader,`${directory}/change.json`);
  if(!plain(value))stop('invalid-input');
  if(value.contract==='rigorloop-records-v3')return 'current';
  if(!Object.hasOwn(value,'contract'))stop('invalid-input');
  if(value.contract!=='rigorloop-records-v2')stop('unsupported-contract');
  if(!Object.hasOwn(value,'schema_version')||!Object.hasOwn(value,'change_id'))stop('invalid-input');
  if(value.schema_version!==2)stop('unsupported-contract');
  if(value.change_id!==id)stop('invalid-input');
  privateState(reader,id);archived=true;
 }
 let files=1;
 function member(path){
  if(!archived)stop('invalid-input');
  if(++files>65)stop('limit-exceeded');
  const value=header(reader,path);
  if(!plain(value)||value.schema_version!==2||value.change_id!==id)stop('invalid-input');
 }
 for(const name of ['evidence.json','material-decisions.json','verify-report.json'])if(reader.inspect(`${directory}/${name}`).info)member(`${directory}/${name}`);
 const reviews=reader.inspect(`${directory}/reviews`,true);
 if(reviews.info){
  let entries=0;
  for(const entry of directoryEntries(reader,reviews)){
   if(archived&&++entries>1024)stop('limit-exceeded');
   if(entry.isSymbolicLink())stop('unsafe-path');
   if(entry.name.endsWith('.json'))member(`${directory}/reviews/${entry.name}`);
  }
  reader.assert(reviews.chain);
 }
 reader.assert(root.chain);
 return archived||yaml?'archive':'noncurrent';
}
