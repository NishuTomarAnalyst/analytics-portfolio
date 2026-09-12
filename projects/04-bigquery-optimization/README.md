# BigQuery Migration and Query Optimization Lab

![Dashboard](../../assets/bigquery-optimization-dashboard.jpg)

## Business decision

Demonstrate how workload grain, date partitioning, clustering and pre-aggregation can reduce scanned data and improve dashboard responsiveness.

## Proposed architecture

```text
Operational source -> Raw landing -> Partitioned fact tables -> Scheduled aggregates -> BI semantic model
```

## Data model

The modeled fact table is one row per student event. It is partitioned by event date and clustered by common reporting dimensions such as center and batch. Daily BI summaries use one row per date and center.

## Design choices

- Partition large event facts by event or reporting date, not a high-cardinality entity ID.
- Cluster on frequently filtered dimensions such as center and batch.
- Require partition filters for expensive fact tables.
- Use scheduled aggregate tables for stable dashboard grains.
- Inspect bytes processed before running costly queries.

## Implementation

- [GoogleSQL examples](sql/analysis.sql)
- [Cost and validation controls](docs/validation.md)

## Validation

The design requires dry-run estimates, source-to-target reconciliation, grain checks, partition-pruning verification and retained job evidence before any performance claim is published.

## Evidence status

Independent simulated case study. It does not claim production GCP ownership, employer deployment or independently measured cost savings. The dashboard values are illustrative until queries are executed and retained in a controlled BigQuery environment.
