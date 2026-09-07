import {executeRecordingQueryCli} from './recording-query-cli.js';
import {executeRecordingMutationCli} from './recording-mutation-cli.js';
export function executeRecordingCli(argv,options={}) {
 return ['status','context','subject'].includes(argv[0])||argv[1]==='show'
  ?executeRecordingQueryCli(argv,options):executeRecordingMutationCli(argv,options);
}
