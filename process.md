# Process: Data Cleaning and Preparation

## Tools Selected
- SQL (BigQuery‑style) for scalable analysis
- Python for reproducible summaries
- Excel/Tableau/Power BI for visualization

## Data Preparation Steps
1. Downloaded Fitbit datasets from Kaggle (two date ranges).
2. Stored raw CSVs in `data/raw/` with date‑range subfolders.
3. Standardized date parsing and merged overlapping files.
4. De‑duplicated daily records by `Id + ActivityDate`.
5. Created derived fields: day of week, hour of day.

## Data Integrity Checks
- Verified schema consistency across both exports.
- Dropped records with invalid dates.
- Ensured numeric fields (steps, minutes, calories) parse cleanly.

## Cleaning Decisions
- Overlapping daily records were de‑duplicated by date and user.
- Sleep data uses `SleepDay` timestamps; converted to date.

## Reproducibility
- `scripts/analyze_bellabeat.py` rebuilds all summary tables.
- `sql/analysis.sql` contains BigQuery‑style queries for the same metrics.
- `r/analysis.R` provides an R workflow template.
