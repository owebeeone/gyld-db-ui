#!/usr/bin/env python3
"""Create one UI project after owner schema-init/kernel bootstrap; preserve JSON evidence."""
import argparse
import copy
import json
from pathlib import Path
import uuid

from gyld_db.client import Client, exact_json, read_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', default='5432')
    parser.add_argument('--user', required=True)
    parser.add_argument('--database', default='gyld_db_ui')
    parser.add_argument('--kernel-result', type=Path, required=True)
    parser.add_argument('--evidence-dir', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    evidence = args.evidence_dir.resolve()
    if evidence == source or source in evidence.parents:
        raise ValueError('Evidence must be outside the UI source repository')
    evidence.mkdir(parents=True, exist_ok=True)
    state_path = evidence / 'project-state.json'
    if state_path.exists() or (evidence / 'project-init-request.json').exists():
        raise ValueError('Project setup already attempted here; inspect receipts before continuing')
    client = Client(args.host, args.database, args.port, args.user)
    installed = read_json(args.kernel_result.read_text())

    def call(label, request):
        (evidence / (label + '-request.json')).write_text(exact_json(request) + '\n')
        reply = client.call(request)
        (evidence / (label + '-reply.json')).write_text(exact_json(reply) + '\n')
        return reply

    handle = call('handle-open', {'operation': 'handle.open',
                  'source_handle_ref': installed['handle_ref'], 'mode': 'overlay',
                  'name': 'Gyld DB UI persistent development'})['handle_ref']
    project = call('project-init', {'operation': 'project.init', 'handle_ref': handle,
                   'project_uuid': str(uuid.uuid4()), 'title': 'Gyld DB UI',
                   'bundle': {'bundle_uuid': str(uuid.uuid4()), 'version': 'ui-envelope-1',
                              'description': 'Operational project marker; knowledge authored through session writes.',
                              'records': []}})['project_ref']
    opened = call('initial-session-open', {'operation': 'session.open', 'handle_ref': handle,
                  'lens_ref': installed['lens_ref'], 'description': 'Gyld DB UI initial persistent project bootstrap'})
    session = {key: opened[key] for key in ('session_ref', 'session_instance_ref')}
    call('initial-session-bind', {'operation': 'session.bind', **session,
         'lens_ref': installed['lens_ref'], 'project_ref': project})
    initial = call('initial-context', {'operation': 'context.get', **session})
    # Validate the complete delivered graph before acknowledging it.
    assert initial['records'] and all(row['projection']['complete'] for row in initial['records'])
    call('initial-context-ack', {'operation': 'context.ack', **session,
         'delivery_token': initial['delivery_token']})
    definitions = call('initial-definitions', {'operation': 'definitions', 'handle_ref': handle})
    assert {'Concept', 'Property', 'Artifact', 'Document'} <= {r.get('symbolic_name') for r in definitions['records']}
    records = copy.deepcopy(read_json((source / 'bootstrap/initial-records.json').read_text()))
    for record in records:
        record['named_properties']['project'] = project
    written = call('initial-project-records', {'operation': 'record.write', **session,
                   'retry_token': 'gyld-ui-initial-records-v1', 'records': records})
    lens = next(row['record_ref'] for row in written['records']
                if row.get('symbolic_name') == 'gyld.ui.default')
    call('default-lens-bind', {'operation': 'session.bind', **session,
         'lens_ref': lens, 'project_ref': project})
    state = {'profile': {'host': args.host, 'port': int(args.port), 'user': args.user,
                        'database': args.database}, 'store_uuid': installed['store_uuid'],
             'kernel_handle_ref': installed['handle_ref'], 'kernel_lens_ref': installed['lens_ref'],
             'handle_ref': handle, 'project_ref': project, 'lens_ref': lens, **session,
             'initial_write_change': written['change_number']}
    state_path.write_text(json.dumps(state, indent=2) + '\n')
    print(json.dumps(state, indent=2))


if __name__ == '__main__':
    main()
