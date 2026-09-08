import {opendirSync} from 'node:fs';
import {stop} from './record-store-files.js';

// Presence only: never decode an archive or invent a registry from loose files.
export function classifyRecordDirectory(reader,id){
 const directory=`docs/changes/${id}`,root=reader.inspect(directory,true);
 if(!root.info)return 'absent';
 const json=reader.inspect(`${directory}/change.json`).info;
 const yaml=reader.inspect(`${directory}/change.yaml`).info;
 if(json&&yaml)stop('invalid-input');
 if(json)return 'current';
 for(const name of ['evidence.json','material-decisions.json','verify-report.json'])if(reader.inspect(`${directory}/${name}`).info)stop('invalid-input');
 const reviews=reader.inspect(`${directory}/reviews`,true);
 if(reviews.info){
  const dir=opendirSync(reviews.target);
  try{for(let entry;(entry=dir.readSync());){if(entry.isSymbolicLink())stop('unsafe-path');if(entry.name.endsWith('.json'))stop('invalid-input');}}
  finally{dir.closeSync();}
  reader.assert(reviews.chain);
 }
 reader.assert(root.chain);
 return yaml?'archive':'noncurrent';
}
