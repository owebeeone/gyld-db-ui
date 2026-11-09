# Gyld DB UI bootstrap and reconnect

The setup scope is the dedicated UI database, project/Lens/session, reusable UI setup inputs and private evidence. Gyld DB product source is reference-only. Bootstrap does not authorize UI code, infrastructure changes, commits or publication. Existing runtime data must be preserved.

## Existing initialized database

Read `connection-profile.json` for the actual nonsecret profile and returned UUID references. The persistent Homebrew PostgreSQL server runs independently of this repository; do not start a throwaway cluster or rerun schema initialization over it.

From this repository, use the existing supported source route:

```sh
export PYTHONPATH="$PWD/../gyld-db/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m gyld_db --host /tmp --port 5432 --user owebeeone --database gyld_db_ui call < /path/to/request.json
```

Start with `{"operation":"context.get","session_ref":{"uuid":"actual-current-session"},"session_instance_ref":{"uuid":"actual-current-instance"}}`, using the actual pair from the profile. Consume the returned context and acknowledge its exact `delivery_token` with `context.ack` when an offer is returned. The initial bootstrap offer was subsequently consumed and acknowledged; a saved response path is historical evidence, not proof that an offer is still pending. Inspect the current reply rather than replaying a saved acknowledgement. Reconstruct the delivered `xg.protocol`, `xg.bootstrap` and `gyld.ui.setup` ordered Document children. Knowledge in the database is authoritative; setup inputs below are historical authored operational inputs.

`session.open` with the actual handle and Lens, then `session.bind` with the returned session pair, actual Lens and operational project, can create another session when explicitly needed. Preserve returned pairs. A reset fences the old instance. Connection secrets, if later required, belong outside code/instructions/evidence.

## A genuinely new database only

First check database presence through PostgreSQL administration. Create a dedicated database only when absent; stop and inspect existing data otherwise. Follow [product bootstrap](../../gyld-db/docs/BOOTSTRAP.md): install schema, then bootstrap kernel, capturing stdout/stderr to a fresh private evidence directory. Do not use this route to recover an existing initialized project.

After a successful kernel bootstrap, the reusable UI project initializer accepts its saved JSON result:

```sh
python3 scripts/bootstrap-project.py --host /path/to/socket --port 5432 --user actual-owner --database new-dedicated-database --kernel-result /private/new-run/bootstrap.stdout.json --evidence-dir /private/new-run
```

The script opens a project overlay, calls `project.init`, opens/binds a session, inspects delivered shared schema/context, and creates [initial-records.json](../bootstrap/initial-records.json) through `record.write`, explicitly injecting the returned project marker. It records exact requests/replies and refuses to reuse a directory containing an existing project initialization attempt. If interrupted, inspect its receipts and exact-retry rules; do not create a second project blindly. Review/update authored inputs for a future setup rather than treating current UI choices as a generic required ontology.

For a full initial or reset offer, check Document closure and ownership with:

```sh
python3 scripts/verify-context.py /private/run/full-context-reply.json /private/run/project-state.json
```

The verifier reads JSON only; it does not acknowledge context. Protocol/data reset verification does not establish a fresh model's reasoning recovery. Keep the distinction in reports.

Export using `python3 -m gyld_db ... export /private/new-run/archive`. Keep captures outside this source repository. The archive directory contains only archive files; logs/reports belong beside it. The exporter preserves unchanged bytes/mtimes and does not stage or commit.
