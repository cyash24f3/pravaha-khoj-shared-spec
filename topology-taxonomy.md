# PRAVAHA/KHOJ Topology and Incident Taxonomy

## Topology

The shared domain is a fictional commerce system used consistently across PRAVAHA and KHOJ.

```text
Client
  |
  v
Gateway
  |
  v
Orders
  |
  +-------> Payments
  |
  +-------> PostgreSQL
  |
  v
Durable order-job table
  |
  v
Fulfillment worker
```

## Taxonomy summary

| Family             | Dominant evidence                                        |
| ------------------ | -------------------------------------------------------- |
| dependency_latency | Downstream dependency is slow                            |
| error_spike        | Failed operations rise materially                        |
| pool_exhaustion    | Waiting/failure acquiring pooled capacity                |
| slow_query         | Database query execution itself is slow                  |
| queue_backlog      | Pending durable work accumulates                         |
| worker_crash       | Worker process terminates or becomes unavailable         |
| bad_deployment     | Software deployment causes incident                      |
| bad_configuration  | Runtime configuration causes incident                    |
| retry_storm        | Retries amplify load and worsen failure                  |
| resource_pressure  | CPU/memory/disk/I/O or similar resource becomes limiting |

## Incident families

### dependency_latency

**Operational definition**

A downstream dependency responds significantly more slowly than expected, causing an upstream component to experience increased request latency even though the upstream component itself is not the primary source of delay.

**Positive example**

Orders requests become slow because the Payments dependency is responding slowly.

**Counterexample**

Orders requests are slow because an Orders database query itself is inefficient. That is not dependency latency merely because PostgreSQL is involved.

**Tie-break**

Use `dependency_latency` when the dominant evidence points to delay in a downstream dependency.

If the dominant evidence instead points to an inefficient query executed against PostgreSQL, classify the incident as `slow_query`.

**Insufficient evidence behavior**

If the evidence shows only that Orders is slow but does not identify whether the delay originates inside Orders or in one of its dependencies, do not force `dependency_latency`. Use the project’s insufficient-evidence behavior.

### error_spike

**Operational definition**

A component or dependency begins returning errors at a materially elevated rate compared with its normal behavior.

**Positive example**

The Payments service starts returning HTTP 500 responses for a large fraction of payment requests.

**Counterexample**

Payments responds successfully but slowly. That is latency, not an error spike.

**Tie-break**

Use `error_spike` when the dominant evidence is failed operations.

If operations mostly succeed but are delayed, prefer `dependency_latency`.

**Insufficient evidence behavior**

A small number of isolated errors without evidence of an elevated failure rate is insufficient to classify as `error_spike`.

### pool_exhaustion

**Operational definition**

A bounded resource pool has no immediately available capacity, causing callers to wait, time out, or fail when attempting to acquire a pooled resource.

**Positive example**

Orders cannot obtain PostgreSQL connections because every connection in its database pool is in use.

**Counterexample**

A database connection is available immediately, but the SQL query itself executes slowly. That is not pool exhaustion.

**Tie-break**

Use `pool_exhaustion` when acquisition of a pooled resource is the bottleneck.

Use `slow_query` when acquisition succeeds normally but database execution is slow.

**Insufficient evidence behavior**

High request latency without pool occupancy, acquisition-wait, or exhaustion evidence is insufficient.

### slow_query

**Operational definition**

One or more database queries have excessive execution time because of query shape, execution plan, indexing, locking, or database-side execution behavior.

**Positive example**

An Orders query performs an expensive sequential scan and takes several seconds to complete.

**Counterexample**

The SQL query executes normally once a connection is obtained, but requests wait several seconds to acquire a connection from the pool.

**Tie-break**

Use `slow_query` when the dominant delay occurs during query execution.

Use `pool_exhaustion` when the dominant delay occurs before execution while acquiring a database connection.

Use `dependency_latency` when PostgreSQL or another downstream system is generally slow but there is insufficient evidence tying the problem to a specific query.

**Insufficient evidence behavior**

Database involvement alone does not establish `slow_query`; query-execution evidence is required.

### queue_backlog

**Operational definition**

Pending durable work accumulates faster than it is completed, producing sustained growth in queue depth or job age.

**Positive example**

The durable order-job table contains a rapidly increasing number of unprocessed fulfillment jobs.

**Counterexample**

The fulfillment worker crashes once but restarts immediately and no persistent backlog develops.

**Tie-break**

Use `queue_backlog` when accumulated pending work is the dominant observable condition.

Use `worker_crash` when the primary evidence is worker-process failure and backlog has not become the defining system condition.

**Insufficient evidence behavior**

A temporarily nonzero queue does not establish backlog without evidence of sustained accumulation or excessive job age.

### worker_crash

**Operational definition**

A worker process terminates unexpectedly, repeatedly restarts, or becomes unavailable because of process-level failure.

**Positive example**

The fulfillment worker exits unexpectedly while processing jobs and must be restarted.

**Counterexample**

The worker process remains healthy but cannot keep up with incoming work, causing queue depth to rise.

**Tie-break**

Use `worker_crash` when process termination or loss of worker availability is the primary failure.

Use `queue_backlog` when workers remain operational but accumulated pending work is the primary condition.

**Insufficient evidence behavior**

A missing heartbeat or delayed job alone is insufficient to claim a crash without process or availability evidence.

### bad_deployment

**Operational definition**

A newly deployed software version introduces behavior that causes or strongly explains the incident.

**Positive example**

Immediately after deploying a new Orders release, error rates rise and rollback restores normal behavior.

**Counterexample**

An operator changes a connection-pool environment variable without deploying new application code.

**Tie-break**

Use `bad_deployment` when the causal recent change is a software release or deployment artifact.

Use `bad_configuration` when the causal change is configuration rather than application code or build output.

**Insufficient evidence behavior**

Temporal proximity to a deployment is not sufficient by itself; evidence must connect the deployed change to the incident.

### bad_configuration

**Operational definition**

An incorrect, incompatible, or unsafe runtime configuration causes or strongly explains the incident.

**Positive example**

Orders is configured with a database connection pool far smaller than required, causing acquisition failures under ordinary traffic.

**Counterexample**

A new Orders binary contains a software defect while configuration remains unchanged.

**Tie-break**

Use `bad_configuration` when the causal change is configuration data, environment, flags, limits, credentials, or runtime settings.

Use `bad_deployment` when the causal change is the deployed software artifact itself.

**Insufficient evidence behavior**

A suspicious configuration value without evidence linking it to observed behavior is insufficient.

### retry_storm

**Operational definition**

Retries triggered by failures or delays multiply request volume enough to amplify load and worsen the original incident.

**Positive example**

Payments becomes slow, causing Orders to retry aggressively until Payments receives several times the normal request rate.

**Counterexample**

A client retries one failed request once according to a bounded retry policy without materially affecting load.

**Tie-break**

Use `retry_storm` when retry amplification itself has become a major contributor to system load or failure.

If retries are merely a reaction and the dominant problem remains the original slow dependency, prefer `dependency_latency`.

**Insufficient evidence behavior**

The presence of retries alone is insufficient; there must be evidence of meaningful amplification.

### resource_pressure

**Operational definition**

A finite compute or operating-system resource such as CPU, memory, file descriptors, disk capacity, or I/O bandwidth approaches or exceeds safe capacity and degrades service behavior.

**Positive example**

The Orders process experiences sustained memory pressure and swapping, causing latency and failures.

**Counterexample**

Orders has adequate CPU and memory, but requests wait because all database-pool connections are occupied.

**Tie-break**

Use `resource_pressure` when the constrained resource itself is the dominant bottleneck.

Use a more specific family such as `pool_exhaustion`, `queue_backlog`, or `slow_query` when evidence identifies that more precise mechanism.

**Insufficient evidence behavior**

High CPU or memory usage alone is insufficient unless it is linked to degraded system behavior or exhaustion risk.

## Domain glossary

**Component**
A named part of the system topology, such as Orders, PostgreSQL, or the durable order-job table.

**Dependency**
A component whose behavior another component relies upon.

**Symptom**
An observable effect such as increased latency, failures, queue growth, or resource saturation.

**Incident family**
A closed operational classification describing the dominant failure mechanism supported by available evidence.

**Counterexample**
A superficially similar case that must not receive a particular incident-family label.

**Tie-break**
A deterministic rule used when evidence could plausibly support more than one incident family.

**Insufficient evidence**
A legitimate outcome used when available observations do not justify a specific incident-family classification.
