// Test-only construction of pre-adoption v2 states and interrupted journals.
// Public creation policy is tested separately; continued writes/recovery use CLI.
import {executeRecordStore} from '../../dist/lib/record-store.js';
export function historicalV2(root,operation,request,options={}){
 const result=executeRecordStore({root,changeId:request.change_id,operation,request},options);
 const exitCode=({inspected:0,valid:0,saved:0,unchanged:0,recovered:0,rejected:2,conflict:3,busy:4,'recovery-required':5})[result.status];
 return{result,exitCode};
}
