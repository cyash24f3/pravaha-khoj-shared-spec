# Incident Input v1 Field Ownership

| Field                 | Owner           | Meaning                                                 |
| --------------------- | --------------- | ------------------------------------------------------- |
| schema_version        | caller/protocol | Version of the incident-input wire contract             |
| service_id            | caller          | Stable identity of the affected service                 |
| service_tier          | caller          | Operational tier of the affected service                |
| incident_description  | caller          | Human-readable description of observed incident context |
| log_summary           | caller          | Bounded summary of relevant observed logs               |
| observed_symptoms     | caller          | Explicit observed operational symptoms                  |
| recent_change_summary | caller          | Bounded description of known recent changes             |
| dependency_context    | caller          | Observable information about relevant dependencies      |
| impact_summary        | caller          | Explicitly observed or known impact                     |

## Fields forbidden from input

The following are prediction targets or server-owned metadata and must not appear in IncidentInputV1:

- severity
- incident_category
- failure_domain
- recommended_diagnostic_action_id
- abstain_reason
- model_version
- dataset_version
- release_version
- request_id
- expected_severity
- expected_category
- operator_final_category
