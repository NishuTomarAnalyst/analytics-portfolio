-- Illustrative GoogleSQL. Replace project and dataset names before execution.
CREATE OR REPLACE TABLE `demo.analytics.student_events_partitioned`
PARTITION BY event_date
CLUSTER BY center_id, batch_id
OPTIONS(require_partition_filter = TRUE) AS
SELECT
  DATE(event_timestamp) AS event_date,
  student_id,
  center_id,
  batch_id,
  event_name,
  score
FROM `demo.raw.student_events`;

-- Latest record per student and event without an extra subquery.
SELECT student_id, center_id, batch_id, event_name, score, event_timestamp
FROM `demo.analytics.student_events`
WHERE event_date BETWEEN @start_date AND @end_date
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY student_id, event_name
  ORDER BY event_timestamp DESC
) = 1;

-- Daily aggregate for a BI dashboard.
CREATE OR REPLACE TABLE `demo.analytics.center_daily_summary`
PARTITION BY event_date
CLUSTER BY center_id AS
SELECT
  event_date,
  center_id,
  COUNT(DISTINCT student_id) AS active_students,
  AVG(score) AS average_score,
  APPROX_QUANTILES(score, 100)[OFFSET(90)] AS p90_score
FROM `demo.analytics.student_events_partitioned`
WHERE event_date = @run_date
GROUP BY 1, 2;
