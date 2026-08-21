# PRAVAHA/KHOJ Shared Contract Bridge

## Scope

This specification defines versioned, technology-neutral data contracts shared by PRAVAHA and KHOJ. Each project will vendor an immutable released snapshot and remain independently runnable.

## Artifact inventory

| Artifact                            | Path                               | Status | Evidence                     |
| ----------------------------------- | ---------------------------------- | ------ | ---------------------------- |
| Incident input v1                   | schemas/incident-input.v1.json     | REUSE  | done S3                      |
| Incident triage v1                  | schemas/incident-triage.v1.json    | REUSE  | done S4                      |
| Service catalog v1                  | schemas/service-catalog.v1.json    | CREATE | File does not exist yet      |
| Fault scenario v1                   | schemas/fault-scenario.v1.json     | CREATE | File does not exist yet      |
| Evidence reference v1               | schemas/evidence-reference.v1.json | CREATE | File does not exist yet      |
| Tool call v1                        | schemas/tool-call.v1.json          | CREATE | File does not exist yet      |
| Positive/negative/semantic fixtures | fixtures/                          | CREATE | Directory does not exist yet |
| Enum semantics                      | topology-taxonomy.md               | CREATE | File does not exist yet      |
| Compatibility policy                | compatibility-policy.md            | CREATE | File does not exist yet      |
| Topology and taxonomy               | topology-taxonomy.md               | CREATE | File does not exist yet      |
| Validation evidence                 | evidence/                          | CREATE | Directory does not exist yet |

## Boundary

Allowed:

PRAVAHA → versioned payload → KHOJ

Forbidden:

- shared database
- cross-project database access
- live shared Python package
- shared runtime service
- cross-repository application imports
- NIRNAY implementation

## Non-goals

This bridge does not implement PRAVAHA, KHOJ, model inference, model training, retrieval, APIs, databases, or agent execution.
