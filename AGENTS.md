# Gyld DB UI

Apply applicable ancestor instructions, including [workspace guidance](../AGENTS.md) and [GWZ rules](../AGENTS_GWZ.md). Repository: **gyld-db-ui**. This UI is the first dogfooding project whose development is managed using Gyld DB.

## Setup status

- Persistent database **gyld_db_ui** is initialized on the existing local PostgreSQL 18.1 Homebrew instance.
- Nonsecret connection: Unix socket **/tmp**, port **5432**, role **owebeeone**, database **gyld_db_ui**. No password is stored here. Existing local authentication is used.
- Live server data directory: **/opt/homebrew/var/postgresql@18**, outside Git repositories. Bootstrap did not change server configuration or existing databases.
- Schema initialization and kernel bootstrap completed separately through the documented [Gyld DB bootstrap tooling](../gyld-db/docs/BOOTSTRAP.md).
- Actual durable identities and the current fresh session pair are in [connection-profile.json](connection-profile.json). Its session is bound to the operational project and saved **gyld.ui.default** Lens. The initial and subsequent requirements context offers have been consumed and acknowledged; fetch the current context before further work. A later session/reset can supersede these references; update the profile then.
- Initial authoritative knowledge is the **gyld.ui.setup** Document with ordered scope, requirements, ontology, questions, work-items and handoff parts. It describes bootstrap requirements and pending choices; it is not a user-dictated UI product specification.
- The saved Lens delivers shared schema/protocol/bootstrap Documents and selected-project Artifacts/Documents. Reconnect and reset data/protocol checks verified 51 complete projected records and ordered required Document closure. This is not a fresh-model reasoning recovery trial.
- Logical export and repeated-export byte/mtime checks passed. Evidence: [private bootstrap capture](../gyld-db-evidence/captures/gyld-db-ui/run-20261109T055543Z/REPORT.md).
- The database-resident **gyld.ui.requirements** Document now holds user direction, source observations, proposals and open questions in ordered editable parts. Its durable reference is in the ignored local connection profile. No requirements Markdown file in this repository is authoritative.
- No UI framework/scaffold implementation has been created. Reference-source choices and unaccepted proposals remain distinct from user requirements.

## Starting or continuing work

1. Read [setup and reconnect guidance](docs/BOOTSTRAP.md), then use the actual profile/session references.
2. Call `context.get` with the current session and instance. Consume full available fields; reconstruct required shared and project Document children in stored order and check closure.
3. Acknowledge the exact `delivery_token` before writes or binding changes. Use scoped names or returned lowercase UUID references and fresh retry tokens as documented by the delivered protocol.
4. If the saved pair is fenced, use the returned current pair from the reset handoff or open/bind a new session through the supported JSON protocol. Do not reinitialize the store or project to recover context.
5. Continue only the user's authorized task. UI workflows, acceptance criteria, additional domain ontology and implementation choices remain pending.

Administrative bootstrap is the one-time setup path. After initialization, normal record changes use the controlled JSON protocol; they do not bypass it with direct metadata-setting SQL. Consult current tooling/reference material for exact API and CLI syntax.

## Development context and knowledge

After bootstrap, obtain project context through the Gyld DB session, handle and active lens. Keep project requirements, design questions, decisions, work items and generated knowledge Documents in Gyld DB. Documents may contain ordered, independently versioned parts so a section or paragraph can evolve without replacing the entire document.

Public JSON uses scoped symbolic names or UUID references, never local database IDs. The database generates normal write change numbers. Actual UUID input strings must be lowercase; do not infer identities from display titles or invent durable references.

Source code and reusable operational/bootstrap instructions remain in Git. When UI implementation begins, source belongs under src/. Use docs/ for end-user guidance and dev-docs/ for reusable development notes/design conventions; project knowledge remains authoritative in Gyld DB after bootstrap.

## Inputs, results and runtime state

Keep reusable bootstrap/test scripts, authored input definitions and operational seed inputs as source. Operational inputs are not execution results.

Generated bootstrap/test results, reports, traces, logical DB dumps/exports and frozen captures belong in the sibling private [gyld-db-evidence](../gyld-db-evidence/README.md) repository, using a UI-specific area such as captures/gyld-db-ui/. Use an explicit external output path or the supported GYLD_DB_EVIDENCE_DIR configuration. Current bootstrap captures use captures/gyld-db-ui/ in that private evidence checkout. Never retain these captures in the UI source repository.

Live PostgreSQL data files are runtime state outside all Git repositories. Logical exports go to evidence. Connection secrets stay outside committed code, instructions and captured reports.
