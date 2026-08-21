# Incident Triage v1 Field Ownership

## Model-owned fields

| Field                            | Owner |
| -------------------------------- | ----- |
| severity                         | model |
| incident_category                | model |
| failure_domain                   | model |
| recommended_diagnostic_action_id | model |
| abstain_reason                   | model |

## Protocol field

| Field          | Owner    |
| -------------- | -------- |
| schema_version | protocol |

## Server-owned fields excluded from this prediction contract

- request_id
- service_id
- model_version
- dataset_version
- release_version

## Forbidden model-authored pseudo-calibration

The model must not emit:

- confidence
- probability
- calibrated_confidence

A self-reported numeric value is not empirical calibration evidence.
