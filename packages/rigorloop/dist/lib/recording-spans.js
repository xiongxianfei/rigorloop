import {canonicalJSON} from './recording-observations.js';
import {stop} from './record-store-files.js';

// Storage presentation is separate from compact canonical encodings used in
// identities, cursors and machine results.
export const indentedJSON=value=>JSON.stringify(JSON.parse(canonicalJSON(value)),null,2);
const multiline=source=>source.trimEnd().includes('\n');
const indentation=(source,offset)=>source.slice(source.lastIndexOf('\n',offset-1)+1,offset).match(/^[ \t]*/)[0];
const tokenJSON=(value,indent)=>indentedJSON(value).replace(/\n/g,'\n'+indent);

// Input has passed the record decoder. Index token boundaries without reprinting
// existing syntax; offsets are JS string offsets, including non-ASCII strings.
function index(source) {
 let i=0;
 const space=()=>{while(/\s/.test(source[i]??'')&&i<source.length)i++;};
 function value(){space();const start=i,children=new Map();
  if(source[i]==='{'||source[i]==='['){const array=source[i++]==='[',end=array?']':'}';space();let n=0;
   while(source[i]!==end){let key=n++;if(!array){const k=value();key=JSON.parse(source.slice(k.start,k.end));space();if(source[i++]!==':')stop('invalid-input');}children.set(key,value());space();if(source[i]===end)break;if(source[i++]!==',')stop('invalid-input');}i++;
  }else if(source[i]==='"'){i++;while(i<source.length){if(source[i]==='\\'){i+=2;continue;}if(source[i++]==='"')break;}}
  else{while(i<source.length&&!/[\s,}\]]/.test(source[i]))i++;}
  if(i<=start)stop('invalid-input');return {start,end:i,children};
 }
 return value();
}
export function replaceValue(source,path,value){const tree=index(source);let node=tree;for(const key of path){node=node.children.get(key);if(!node)stop('invalid-input');}const token=source.slice(node.start,node.end);if(canonicalJSON(JSON.parse(token))===canonicalJSON(value))return source;const replacement=multiline(source)?tokenJSON(value,indentation(source,node.start)):canonicalJSON(value);return source.slice(0,node.start)+replacement+source.slice(node.end);}
export function appendValue(source,path,value){
 let node=index(source);for(const key of path){node=node.children.get(key);if(!node)stop('invalid-input');}if(source[node.start]!=='[')stop('invalid-input');
 if(!multiline(source))return source.slice(0,node.end-1)+(node.children.size?',':'')+canonicalJSON(value)+source.slice(node.end-1);
 const indent=indentation(source,node.start),childIndent=indent+'  ';
 const last=[...node.children.values()].at(-1),offset=last?last.end:node.start+1;
 const trailing=source.slice(offset,node.end-1);
 return source.slice(0,offset)+(last?',':'')+'\n'+childIndent+tokenJSON(value,childIndent)+(trailing.includes('\n')?'':'\n'+indent)+source.slice(offset);
}
export class RecordDocument {
 constructor(format,kind,source,data){this.format=format;this.kind=kind;this.source=source;this.data=data;}
 edit(path,value,append=false){this.source=(append?appendValue:replaceValue)(this.source,path,value);let node=this.data;for(const key of path.slice(0,-1))node=node[key];if(append){const array=path.length?node[path.at(-1)]:this.data;array.push(value);}else node[path.at(-1)]=value;}
 body(value){this.edit(['body'],value);}
}
