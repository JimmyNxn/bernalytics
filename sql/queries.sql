-- Sample SQL Queries for Bernalytics Data Analysis
-- Copy and paste these into the Supabase SQL Editor

-- ============================================================
-- BASIC QUERIES
-- ============================================================

-- View all data, most recent first
SELECT * FROM job_counts
ORDER BY week_starting DESC;

-- View recent data using the built-in view
SELECT * FROM recent_job_counts;

-- Get data for a specific location
SELECT * FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;


-- ============================================================
-- TREND ANALYSIS
-- ============================================================

-- Calculate week-over-week change
SELECT
  week_starting,
  data_engineer,
  data_engineer - LAG(data_engineer) OVER (ORDER BY week_starting) as weekly_change,
  ROUND(
    ((data_engineer - LAG(data_engineer) OVER (ORDER BY week_starting))::numeric /
    NULLIF(LAG(data_engineer) OVER (ORDER BY week_starting), 0) * 100),
    1
  ) as percent_change
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;

-- Calculate total job postings per week
SELECT
  week_starting,
  (data_engineer + junior_data_engineer + senior_data_engineer) as total_jobs,
  data_engineer,
  junior_data_engineer,
  senior_data_engineer
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;

-- Moving average (4-week)
SELECT
  week_starting,
  data_engineer,
  ROUND(AVG(data_engineer) OVER (
    ORDER BY week_starting
    ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
  )) as moving_avg_4weeks
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;


-- ============================================================
-- AGGREGATIONS
-- ============================================================

-- Monthly averages
SELECT
  DATE_TRUNC('month', week_starting) as month,
  ROUND(AVG(data_engineer)) as avg_data_engineer,
  ROUND(AVG(junior_data_engineer)) as avg_junior,
  ROUND(AVG(senior_data_engineer)) as avg_senior,
  ROUND(AVG(data_engineer + junior_data_engineer + senior_data_engineer)) as avg_total
FROM job_counts
WHERE location = 'Berlin, Germany'
GROUP BY month
ORDER BY month DESC;

-- Quarterly statistics
SELECT
  DATE_TRUNC('quarter', week_starting) as quarter,
  COUNT(*) as weeks_tracked,
  ROUND(AVG(data_engineer)) as avg_data_engineer,
  MIN(data_engineer) as min_data_engineer,
  MAX(data_engineer) as max_data_engineer,
  ROUND(STDDEV(data_engineer)) as std_dev
FROM job_counts
WHERE location = 'Berlin, Germany'
GROUP BY quarter
ORDER BY quarter DESC;

-- Year-over-year comparison
SELECT
  EXTRACT(YEAR FROM week_starting) as year,
  EXTRACT(WEEK FROM week_starting) as week_number,
  data_engineer,
  junior_data_engineer,
  senior_data_engineer
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY year DESC, week_number DESC;


-- ============================================================
-- SENIORITY ANALYSIS
-- ============================================================

-- Percentage of junior vs senior roles
SELECT
  week_starting,
  data_engineer as total,
  junior_data_engineer,
  senior_data_engineer,
  ROUND((junior_data_engineer::numeric / NULLIF(data_engineer, 0) * 100), 1) as pct_junior,
  ROUND((senior_data_engineer::numeric / NULLIF(data_engineer, 0) * 100), 1) as pct_senior
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;

-- Average split between junior and senior
SELECT
  ROUND(AVG(junior_data_engineer::numeric / NULLIF(data_engineer, 0) * 100), 1) as avg_pct_junior,
  ROUND(AVG(senior_data_engineer::numeric / NULLIF(data_engineer, 0) * 100), 1) as avg_pct_senior
FROM job_counts
WHERE location = 'Berlin, Germany';


-- ============================================================
-- GROWTH METRICS
-- ============================================================

-- Month-over-month growth rate
WITH monthly_data AS (
  SELECT
    DATE_TRUNC('month', week_starting) as month,
    ROUND(AVG(data_engineer)) as avg_jobs
  FROM job_counts
  WHERE location = 'Berlin, Germany'
  GROUP BY month
)
SELECT
  month,
  avg_jobs,
  avg_jobs - LAG(avg_jobs) OVER (ORDER BY month) as monthly_change,
  ROUND(
    ((avg_jobs - LAG(avg_jobs) OVER (ORDER BY month))::numeric /
    NULLIF(LAG(avg_jobs) OVER (ORDER BY month), 0) * 100),
    1
  ) as pct_change
FROM monthly_data
ORDER BY month DESC;

-- Best and worst weeks
SELECT
  'Highest' as metric,
  week_starting,
  data_engineer as count
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY data_engineer DESC
LIMIT 5

UNION ALL

SELECT
  'Lowest' as metric,
  week_starting,
  data_engineer as count
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY data_engineer ASC
LIMIT 5;


-- ============================================================
-- DATA QUALITY
-- ============================================================

-- Check for missing weeks (gaps in data)
SELECT
  week_starting,
  LEAD(week_starting) OVER (ORDER BY week_starting) as next_week,
  LEAD(week_starting) OVER (ORDER BY week_starting) - week_starting as days_gap
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;

-- Summary statistics
SELECT
  COUNT(*) as total_records,
  MIN(week_starting) as first_week,
  MAX(week_starting) as last_week,
  MAX(week_starting) - MIN(week_starting) as days_tracked,
  ROUND(AVG(data_engineer)) as avg_data_engineer,
  MIN(data_engineer) as min_data_engineer,
  MAX(data_engineer) as max_data_engineer
FROM job_counts
WHERE location = 'Berlin, Germany';


-- ============================================================
-- EXPORT QUERIES
-- ============================================================

-- Export-ready format for CSV download
SELECT
  week_starting,
  data_engineer as "Data Engineer",
  junior_data_engineer as "Junior Data Engineer",
  senior_data_engineer as "Senior Data Engineer",
  (data_engineer + junior_data_engineer + senior_data_engineer) as "Total",
  collected_at as "Collected At"
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;

-- Weekly summary with ratios
SELECT
  week_starting,
  data_engineer,
  junior_data_engineer,
  senior_data_engineer,
  ROUND(senior_data_engineer::numeric / NULLIF(junior_data_engineer, 0), 2) as senior_to_junior_ratio,
  collected_at
FROM job_counts
WHERE location = 'Berlin, Germany'
ORDER BY week_starting DESC;


-- ============================================================
-- VISUALIZATION READY
-- ============================================================

-- Time series data (perfect for charting)
SELECT
  week_starting as date,
  data_engineer as value,
  'Data Engineer' as series
FROM job_counts
WHERE location = 'Berlin, Germany'

UNION ALL

SELECT
  week_starting as date,
  junior_data_engineer as value,
  'Junior' as series
FROM job_counts
WHERE location = 'Berlin, Germany'

UNION ALL

SELECT
  week_starting as date,
  senior_data_engineer as value,
  'Senior' as series
FROM job_counts
WHERE location = 'Berlin, Germany'

ORDER BY date DESC, series;


-- ============================================================
-- CUSTOM ANALYSIS
-- ============================================================

-- Find significant changes (>20% week-over-week)
WITH changes AS (
  SELECT
    week_starting,
    data_engineer,
    LAG(data_engineer) OVER (ORDER BY week_starting) as prev_week,
    ROUND(
      ((data_engineer - LAG(data_engineer) OVER (ORDER BY week_starting))::numeric /
      NULLIF(LAG(data_engineer) OVER (ORDER BY week_starting), 0) * 100),
      1
    ) as pct_change
  FROM job_counts
  WHERE location = 'Berlin, Germany'
)
SELECT * FROM changes
WHERE ABS(pct_change) > 20
ORDER BY week_starting DESC;

-- Seasonality analysis (average by month of year)
SELECT
  EXTRACT(MONTH FROM week_starting) as month_number,
  TO_CHAR(week_starting, 'Month') as month_name,
  COUNT(*) as weeks_sampled,
  ROUND(AVG(data_engineer)) as avg_jobs
FROM job_counts
WHERE location = 'Berlin, Germany'
GROUP BY month_number, month_name
ORDER BY month_number;
