# Analysis Summary

## Executive Summary
User activity is moderate (avg **7,377 steps/day**) with limited consistency in hitting 10k steps (only **31.3%** of days). Sleep is below the recommended 7 hours for **44.2%** of nights, suggesting a strong opportunity for sleep‑focused insights and coaching.

## Key Metrics
- Avg steps/day: **7,377**
- Days ≥10k steps: **31.3%**
- Avg sleep: **6.99 hours**
- Nights <7 hours: **44.2%**
- Steps–calories correlation: **0.58**
- Peak hours: **12pm**, **6–7pm**
- Most active day: **Saturday**; lowest: **Sunday**

## Usage Trends
1. **Midday and evening activity peaks** suggest engagement windows for nudges.
2. **Weekend drop in steps** (especially Sunday) indicates opportunity for weekend campaigns.
3. **Sleep deficits** are common, making sleep improvement a high‑value feature for marketing.

## Visualization Ideas (Tableau / Power BI)
- Line chart: steps by hour
- Bar chart: average steps by day of week
- Histogram: distribution of average steps per user
- Bar chart: average sleep minutes by day of week
- Scatter plot: steps vs calories

## Outputs
Summary tables are in `data/processed/`:
- `summary_overall.csv`
- `daily_by_dayofweek.csv`
- `sleep_by_dayofweek.csv`
- `steps_by_hour.csv`
- `user_avg_steps.csv`
