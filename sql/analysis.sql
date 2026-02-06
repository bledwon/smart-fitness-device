-- Bellabeat Fitbit Analysis (BigQuery-style)

-- Example: load dailyActivity_merged.csv and sleepDay_merged.csv
-- into tables: my_dataset.daily_activity and my_dataset.sleep_day

-- Daily activity summary
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT Id) AS unique_users,
  AVG(TotalSteps) AS avg_steps_per_day,
  AVG(Calories) AS avg_calories_per_day,
  AVG(VeryActiveMinutes + FairlyActiveMinutes + LightlyActiveMinutes) AS avg_active_minutes
FROM my_dataset.daily_activity;

-- Percent of days with 10k+ steps
SELECT
  COUNTIF(TotalSteps >= 10000) / COUNT(*) AS pct_days_10k
FROM my_dataset.daily_activity;

-- Steps by day of week
SELECT
  FORMAT_DATE('%a', PARSE_DATE('%m/%d/%Y', ActivityDate)) AS day_of_week,
  AVG(TotalSteps) AS avg_steps,
  AVG(Calories) AS avg_calories
FROM my_dataset.daily_activity
GROUP BY day_of_week
ORDER BY day_of_week;

-- Sleep summary
SELECT
  AVG(TotalMinutesAsleep)/60 AS avg_sleep_hours,
  COUNTIF(TotalMinutesAsleep < 420) / COUNT(*) AS pct_sleep_lt_7h
FROM my_dataset.sleep_day;

-- Sleep by day of week
SELECT
  FORMAT_DATE('%a', PARSE_DATE('%m/%d/%Y', SleepDay)) AS day_of_week,
  AVG(TotalMinutesAsleep) AS avg_sleep_minutes
FROM my_dataset.sleep_day
GROUP BY day_of_week
ORDER BY day_of_week;

-- Hourly steps
SELECT
  EXTRACT(HOUR FROM PARSE_DATETIME('%m/%d/%Y %I:%M:%S %p', ActivityHour)) AS hour,
  SUM(StepTotal) AS total_steps
FROM my_dataset.hourly_steps
GROUP BY hour
ORDER BY hour;
