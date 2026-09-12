-- Cohort-safe retention and batch utilization.
WITH cohort AS (
  SELECT
    student_id,
    batch_id,
    DATE_TRUNC('month', enrollment_date) AS cohort_month,
    status,
    fee_amount
  FROM enrollment
  WHERE enrollment_date < :period_end
),
batch_metrics AS (
  SELECT
    b.center_id,
    c.batch_id,
    c.cohort_month,
    b.capacity,
    COUNT(DISTINCT c.student_id) AS starting_students,
    COUNT(DISTINCT CASE WHEN c.status = 'active' THEN c.student_id END) AS active_students,
    SUM(CASE WHEN c.status IN ('active', 'completed') THEN c.fee_amount ELSE 0 END) AS recognized_revenue
  FROM cohort c
  JOIN batch b ON b.batch_id = c.batch_id
  GROUP BY 1, 2, 3, 4
)
SELECT
  center_id,
  batch_id,
  cohort_month,
  recognized_revenue,
  active_students * 1.0 / NULLIF(starting_students, 0) AS retention_rate,
  active_students * 1.0 / NULLIF(capacity, 0) AS utilization_rate
FROM batch_metrics;
