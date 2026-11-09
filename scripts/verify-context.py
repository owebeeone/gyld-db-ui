#!/usr/bin/env python3
"""Check full initial/reset Lens delivery without modifying a database."""
import argparse
import json
from pathlib import Path


def verify(offer, project_ref):
    assert offer['mode'] == 'full', 'Verification requires a new-instance full offer'
    rows = offer['records']
    assert all(row['projection']['complete'] for row in rows), 'Unknown projected fields'
    by_uuid = {row['record_ref']['uuid']: row for row in rows}
    by_name = {row['symbolic_name']: row for row in rows if row.get('symbolic_name')}
    properties = {key: by_name[key]['record_ref']['uuid'] for key in ['body', 'children', 'project']}

    def values(row, key):
        return next((p['values'] for p in row['properties']
                     if p['property_ref']['uuid'] == properties[key]), [])

    def document(key, visiting=None):
        visiting = set() if visiting is None else visiting
        row = by_name[key]
        identifier = row['record_ref']['uuid']
        assert identifier not in visiting, 'Document child cycle'
        children = values(row, 'children')
        body = values(row, 'body')
        assert children or (len(body) == 1 and isinstance(body[0], str) and body[0]), key
        ordered = [key]
        for ref in children:
            assert ref['uuid'] in by_uuid, 'Undelivered child: ' + str(ref)
            child = by_uuid[ref['uuid']]
            ordered.extend(document(child['symbolic_name'], visiting | {identifier}))
        return ordered

    closure = {key: document(key) for key in ['xg.protocol', 'xg.bootstrap', 'gyld.ui.setup']}
    for key, row in by_name.items():
        if key.startswith('gyld.ui.'):
            assert values(row, 'project') == [project_ref], 'Wrong project ownership: ' + key
    expected = json.loads((Path(__file__).resolve().parents[1] / 'bootstrap/initial-records.json').read_text())
    expected_keys = {record['record_ref']['name'] for record in expected}
    assert expected_keys <= by_name.keys(), 'Missing initial UI context'
    return {'verified': True, 'mode': offer['mode'], 'cutoff_change_number': offer['cutoff_change_number'],
            'selected_records': len(rows), 'complete_projections': True,
            'ordered_document_closure': closure, 'project_ownership_verified': sorted(expected_keys),
            'scope': 'Protocol/data reconstruction; not a fresh-model reasoning trial.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('offer', type=Path)
    parser.add_argument('state', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.offer.read_text()), json.loads(args.state.read_text())['project_ref']), indent=2))


if __name__ == '__main__':
    main()
