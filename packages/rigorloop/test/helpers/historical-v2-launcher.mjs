// Reproduce a pre-adoption v2 creation journal with the shared engine, then use
// today's public dispatcher for continuation/recovery. This is not shipped.
import {readFileSync} from 'node:fs';
import {main} from '../../dist/bin/rigorloop.js';
import {parseRecordStoreArgs} from '../../dist/lib/record-store-cli.js';
import {historicalV2} from './historical-v2.mjs';
const argv=process.argv.slice(2),selected=parseRecordStoreArgs(argv.slice(1));
const fault=point=>{if(process.env.RIGORLOOP_TEST_RECORD_FAULT===point)process.exit(99);};
let input,request;
if(argv[0]==='record-store'&&!selected.invalid&&['check','record'].includes(selected.operation)){
 input=readFileSync(0);try{request=JSON.parse(input.toString());}catch{}
}
if(request?.contract==='rigorloop-records-v2'&&request.expected_revision===null){
 const r=historicalV2(selected.root,selected.operation,request,{fault});process.stdout.write(JSON.stringify(r.result)+'\n');process.exitCode=r.exitCode;
}else{
 const r=await main(argv,{recordStoreOptions:{fault,...(input?{input}:{})}}),output=r.render({});process.stdout.write(output.stdout);process.stderr.write(output.stderr);process.exitCode=r.exitCode;
}
