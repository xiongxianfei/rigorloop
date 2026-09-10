#!/usr/bin/env python3
"""Repository CI dispatcher; no public product command or approval bypass."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import subprocess

from release_coordination import (HostedServices, prepare_operation, execute_operation,
    read_evidence, summary, ENVIRONMENT)
from release_candidate import CandidateError
from release_execution import ExecutionError


def safe_error(exc):
    if isinstance(exc, (ExecutionError, CandidateError)):
        message = re.sub(r'; private diagnostic log: .*', '; inspect the failed check in the private worker diagnostics', str(exc))
    elif isinstance(exc, KeyError):
        message = 'required workflow input is missing'
    elif isinstance(exc, (OSError, subprocess.SubprocessError)):
        message = 'required filesystem, process or service access is unavailable'
    else:
        message = 'required release input is malformed'
    return message


def main(argv=None, *, services=None, root=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == 'check-ci':
        from release_candidate import check_ci
        try:
            return check_ci(argv[1:], root or Path(__file__).resolve().parents[1])
        except (CandidateError, KeyError, TypeError, AttributeError, OSError, ValueError, subprocess.SubprocessError) as exc:
            print('CI release preparation stopped: ' + safe_error(exc), file=sys.stderr)
            return 1
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['prepare', 'execute', 'read-evidence'])
    parser.add_argument('--tag')
    args = parser.parse_args(argv)
    services = services or HostedServices()
    settings = {'evidence_ref': os.environ.get('RELEASE_EVIDENCE_REF', ''),
        'trusted_publisher': os.environ.get('RELEASE_TRUSTED_PUBLISHER', '')}
    try:
        if args.operation == 'read-evidence':
            state = read_evidence(services, settings['evidence_ref'], args.tag or '')
            print(json.dumps(state, indent=2, sort_keys=True))
            return 0 if state['status'] == 'completed' else 1
        if os.environ.get('GITHUB_ACTIONS') != 'true':
            raise ExecutionError('hosted operation requires the configured workflow; use local tests for proof')
        event = {'run_id': int(os.environ['GITHUB_RUN_ID']), 'attempt': int(os.environ['GITHUB_RUN_ATTEMPT']),
            'source_commit': os.environ['GITHUB_SHA'], 'source_ref': os.environ['GITHUB_REF']}
        root = root or Path(__file__).resolve().parents[1]
        output = Path(os.environ['RUNNER_TEMP']) / 'release-candidate'
        if args.operation == 'prepare':
            result = prepare_operation(root, output, event, settings, services)
            values = {'ready': 'true' if result['status'] == 'ready' else 'false'}
            if result['status'] == 'ready':
                values['candidate_id'] = result['candidate']['candidate_id']
                for key in ['artifact_id', 'artifact_digest']:
                    if key in result.get('binding', {}): values[key] = str(result['binding'][key])
                text = summary(result['candidate'])
            else: text = 'Already-published unchanged source; no approval or publication requested.\n'
            with open(os.environ['GITHUB_OUTPUT'], 'a') as handle:
                for key, value in values.items():
                    if '\n' in value: raise ExecutionError('invalid workflow output')
                    handle.write(key + '=' + value + '\n')
        else:
            digest = os.environ['RELEASE_ARTIFACT_DIGEST']
            if re.fullmatch(r'[0-9a-f]{64}', digest): digest = 'sha256:' + digest
            binding = {'run_id': event['run_id'], 'artifact_id': int(os.environ['RELEASE_ARTIFACT_ID']),
                'artifact_digest': digest, 'candidate_id': os.environ['RELEASE_CANDIDATE_ID'],
                'environment': ENVIRONMENT, 'artifact_name': 'release-candidate-' + str(event['run_id'])}
            state = execute_operation(root, output, event, settings, binding, services)
            text = 'Release outcome: ' + state['status'] + '. Authoritative observations: ' + settings['evidence_ref'] + '.\n'
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as handle: handle.write(text)
        return 0
    except (ExecutionError, CandidateError, KeyError, ValueError, OSError, subprocess.SubprocessError) as exc:
        message = safe_error(exc)
        print('Release stopped: ' + message, file=sys.stderr)
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            try:
                with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as handle:
                    handle.write('Release incomplete: ' + message + '. Retain observation artifacts and inspect the evidence ref before retry.\n')
            except OSError:
                print('Release summary could not be written; retain available recovery observations.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
