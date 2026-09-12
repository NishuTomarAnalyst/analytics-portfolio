# Pipeline runbook

## Before the daily run

- Confirm the source watermark advanced.
- Confirm required connections are available through the deployment secret store.
- Confirm the reporting-date partition is expected.

## Failure response

1. Identify the first failed task; downstream failures may be symptoms.
2. Check source freshness, schema and row-count reconciliation.
3. Correct the cause before clearing a task.
4. Re-run only idempotent tasks for the affected date.
5. Confirm the BI refresh consumed the corrected partition.

## Definition of success

- Every required task succeeds.
- Source and reporting counts reconcile within an approved rule.
- No critical quality check fails.
- The reporting partition has the expected date.
- The BI refresh completes within the agreed SLA.
