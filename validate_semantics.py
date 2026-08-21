import json
import sys
from pathlib import Path
from typing import Any


CATEGORY_TO_DOMAINS: dict[str, set[str]] = {
    "dependency_latency": {"dependency"},
    "error_spike": {"application", "dependency"},
    "pool_exhaustion": {"database", "resource"},
    "slow_query": {"database"},
    "queue_backlog": {"queue"},
    "worker_crash": {"worker"},
    "bad_deployment": {"deployment"},
    "bad_configuration": {"configuration"},
    "retry_storm": {"application", "dependency"},
    "resource_pressure": {"resource"},
}

CATEGORY_TO_ACTION: dict[str, str] = {
    "dependency_latency": "inspect_dependency_latency",
    "error_spike": "inspect_error_rates",
    "pool_exhaustion": "inspect_connection_pool",
    "slow_query": "inspect_query_execution",
    "queue_backlog": "inspect_queue_depth",
    "worker_crash": "inspect_worker_process",
    "bad_deployment": "inspect_recent_deployment",
    "bad_configuration": "inspect_runtime_configuration",
    "retry_storm": "inspect_retry_behavior",
    "resource_pressure": "inspect_resource_pressure",
}

CLASSIFICATION_FIELDS = (
    "severity",
    "incident_category",
    "failure_domain",
    "recommended_diagnostic_action_id",
)

INSUFFICIENT = "INSUFFICIENT_EVIDENCE"


def validate_semantics(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    has_abstain_reason = "abstain_reason" in payload

    insufficient_fields = [
        field for field in CLASSIFICATION_FIELDS if payload.get(field) == INSUFFICIENT
    ]

    if has_abstain_reason:
        if len(insufficient_fields) != len(CLASSIFICATION_FIELDS):
            errors.append(
                "abstain_reason requires every classification field "
                "to be INSUFFICIENT_EVIDENCE"
            )

    elif insufficient_fields:
        errors.append(
            "INSUFFICIENT_EVIDENCE requires all classification fields "
            "to be INSUFFICIENT_EVIDENCE and abstain_reason to be present"
        )

    if insufficient_fields:
        return errors

    category = payload["incident_category"]
    domain = payload["failure_domain"]
    action = payload["recommended_diagnostic_action_id"]

    allowed_domains = CATEGORY_TO_DOMAINS[category]
    if domain not in allowed_domains:
        errors.append(f"{category} does not permit failure_domain={domain}")

    expected_action = CATEGORY_TO_ACTION[category]
    if action != expected_action:
        errors.append(
            f"{category} requires recommended_diagnostic_action_id={expected_action}"
        )
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: uv run python validate_semantics.py <fixture.json>")
        return 2

    path = Path(sys.argv[1])

    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    errors = validate_semantics(payload)

    if errors:
        print(f"SEMANTIC INVALID: {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"SEMANTIC VALID: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
