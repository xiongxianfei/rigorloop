// Test-only primary interface harness; activation remains a later milestone.
import {executeRecordingQueryCli} from "../../dist/lib/recording-query-cli.js";
if (process.argv.length > 2) {
const output = executeRecordingQueryCli(process.argv.slice(2));
process.stdout.write(output.format === "text" ? output.human : output.json);
process.exitCode = output.exitCode;
}
