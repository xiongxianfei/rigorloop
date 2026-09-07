// Test-only launcher through the real CLI dispatcher; not shipped package data.
import { main } from "../../dist/bin/rigorloop.js";
if(process.argv[2]==="record-store") {
  const execution=await main(process.argv.slice(2),{recordStoreOptions:{
    fault:point=>{ if(process.env.RIGORLOOP_TEST_RECORD_FAULT===point)process.exit(99); },
  }});
  const output=execution.render({});
  process.stdout.write(output.stdout); process.stderr.write(output.stderr);
  process.exitCode=execution.exitCode;
}
