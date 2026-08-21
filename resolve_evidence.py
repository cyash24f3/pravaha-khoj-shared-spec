import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def current_git_revision() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)

    return digest.hexdigest()


def resolve(reference: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    expected_revision = reference["source_revision"]
    actual_revision = current_git_revision()

    if expected_revision != actual_revision:
        errors.append(
            f"source revision mismatch: expected={expected_revision} "
            f"actual={actual_revision}"
        )

    path = Path(reference["source_path"])

    if not path.is_file():
        errors.append(f"source path does not exist: {path}")
        return errors

    expected_sha256 = reference["content_sha256"]
    actual_sha256 = sha256_file(path)

    if actual_sha256 != expected_sha256:
        errors.append(
            f"checksum mismatch: expected={expected_sha256} actual={actual_sha256}"
        )

    logical_location = reference.get("logical_location")

    if logical_location is not None:
        content = path.read_text(encoding="utf-8")

        if logical_location not in content:
            errors.append(f"logical location not found: {logical_location}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: uv run python resolve_evidence.py <evidence-reference.json>")
        return 2

    reference_path = Path(sys.argv[1])

    with reference_path.open("r", encoding="utf-8") as file:
        reference = json.load(file)

    errors = resolve(reference)

    if errors:
        print(f"RESOLUTION FAILED: {reference_path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"RESOLUTION SUCCEEDED: {reference_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
