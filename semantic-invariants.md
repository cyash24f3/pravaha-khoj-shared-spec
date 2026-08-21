# Incident Triage v1 Semantic Invariants

## Invariant 1 — Concrete prediction and abstention are mutually exclusive

If `abstain_reason` is present, then all model-owned classification fields must be `INSUFFICIENT_EVIDENCE`.

If a concrete classification is present, `abstain_reason` must be absent.

## Invariant 2 — Insufficient-evidence fields move together

If any of these fields is `INSUFFICIENT_EVIDENCE`:

- severity
- incident_category
- failure_domain
- recommended_diagnostic_action_id

then all four must be `INSUFFICIENT_EVIDENCE` and `abstain_reason` must be present.

## Invariant 3 — Incident category constrains failure domain

- dependency_latency → dependency
- error_spike → application or dependency
- pool_exhaustion → database or resource
- slow_query → database
- queue_backlog → queue
- worker_crash → worker
- bad_deployment → deployment
- bad_configuration → configuration
- retry_storm → application or dependency
- resource_pressure → resource

## Invariant 4 — Incident category constrains diagnostic action

- dependency_latency → inspect_dependency_latency
- error_spike → inspect_error_rates
- pool_exhaustion → inspect_connection_pool
- slow_query → inspect_query_execution
- queue_backlog → inspect_queue_depth
- worker_crash → inspect_worker_process
- bad_deployment → inspect_recent_deployment
- bad_configuration → inspect_runtime_configuration
- retry_storm → inspect_retry_behavior
- resource_pressure → inspect_resource_pressure

## Invariant 5 — No model-authored confidence

The prediction contract must not contain a `confidence`, `probability`, or similar pseudo-calibrated field.
