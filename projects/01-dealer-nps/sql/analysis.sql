-- Dealer NPS and funnel analysis (ANSI-style SQL).
WITH valid_surveys AS (
  SELECT dealer_id, customer_id, survey_date, nps_score
  FROM survey
  WHERE nps_score BETWEEN 0 AND 10
),
weekly AS (
  SELECT
    dealer_id,
    DATE_TRUNC('week', survey_date) AS week_start,
    COUNT(*) AS responses,
    100.0 * (
      SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END)
      - SUM(CASE WHEN nps_score <= 6 THEN 1 ELSE 0 END)
    ) / NULLIF(COUNT(*), 0) AS nps
  FROM valid_surveys
  GROUP BY 1, 2
),
trended AS (
  SELECT *,
    AVG(nps) OVER (
      PARTITION BY dealer_id ORDER BY week_start
      ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS rolling_4_week_nps
  FROM weekly
),
latest AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY dealer_id ORDER BY week_start DESC) AS recency
  FROM trended
)
SELECT
  d.region,
  d.dealer_name,
  l.responses,
  ROUND(l.nps, 1) AS nps,
  ROUND(l.rolling_4_week_nps, 1) AS rolling_4_week_nps,
  DENSE_RANK() OVER (PARTITION BY d.region ORDER BY l.nps DESC) AS regional_rank
FROM latest l
JOIN dealer d ON d.dealer_id = l.dealer_id
WHERE l.recency = 1;

-- Funnel denominators are kept explicit.
SELECT
  COUNT(*) AS call_attempts,
  SUM(CASE WHEN outcome = 'connected' THEN 1 ELSE 0 END) AS connected_calls,
  COUNT(DISTINCT CASE WHEN outcome = 'connected' THEN customer_id END) AS connected_customers
FROM call_log;
