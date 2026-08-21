# Evidence Resolution Semantics

## Structural validity

An evidence reference is structurally valid when it satisfies
`evidence-reference.v1.json`.

Structural validity does not prove that the referenced evidence exists
or matches the expected content.

## Successful resolution

Resolution succeeds only when:

1. the referenced source path exists;
2. the requested immutable source revision is supported;
3. the exact source content is read;
4. its SHA-256 matches `content_sha256`;
5. the declared logical location can be found when one is provided.

## Fail-closed behavior

Resolution must fail when:

- source revision is missing or unsupported;
- source path does not exist;
- checksum differs;
- logical location cannot be located;
- schema version is unsupported.

The resolver must not silently substitute:

- `latest`;
- `main`;
- a nearby file;
- a nearby section;
- a guessed database row;
- another revision.

## Cross-project boundary

PRAVAHA and KHOJ exchange versioned payloads.

Neither project may expose or require the other's:

- database connection string;
- table name;
- internal row identifier;
- private migration state;
- live Python package.
