# Case Study Questions: Explicit Answers

## Ask
**Q: What are some trends in smart device usage?**
A: Users average ~7.4k steps/day, activity peaks midday and early evening, and sleep averages ~7 hours with ~44% of nights under 7 hours.

**Q: How could these trends apply to Bellabeat customers?**
A: Bellabeat customers likely face similar activity gaps and sleep deficits; app‑based coaching and reminders can target these specific usage patterns.

**Q: How could these trends help influence Bellabeat marketing strategy?**
A: Marketing can emphasize sleep improvement, targeted nudges during peak activity windows, and weekend challenge campaigns to raise engagement.

## Prepare
**Q: Where is your data stored?**
A: Raw data is stored locally in `data/raw/` with two date‑range subfolders. Processed outputs are in `data/processed/`.

**Q: How is the data organized?**
A: CSVs are organized by time granularity (daily, hourly, minute) and metric (activity, sleep, weight).

**Q: Are there issues with bias or credibility? Does it ROCCC?**
A: Data is original and public (CC0) but sample size is small (35 users) and may not represent all demographics.

**Q: How are you addressing licensing and privacy?**
A: Dataset is CC0 and contains no personally identifiable information. Results are reported in aggregate.

**Q: How did you verify integrity?**
A: Checked schema consistency, parsed dates, removed invalid rows, and de‑duplicated daily records.

**Q: How does it help answer the question?**
A: Provides behavior patterns across activity and sleep that directly reflect smart device usage trends.

## Process
**Q: What tools are you choosing and why?**
A: SQL for scalable queries, Python for reproducible processing, Excel/Tableau/Power BI for visualization.

**Q: What steps ensure the data is clean?**
A: Parsed timestamps, standardized schemas, removed invalid rows, and de‑duplicated overlapping dates.

## Analyze
**Q: What trends or relationships did you find?**
A: Activity peaks midday/early evening; only 31% of days meet 10k steps; sleep deficits are common; steps and calories correlate moderately (r=0.58).

## Share
**Q: What story does the data tell?**
A: Many users fall short of activity and sleep benchmarks, creating opportunities for coaching and behavior change messaging.

## Act
**Q: What are your high‑level recommendations?**
A: Focus on sleep improvement, time‑based activity nudges, and weekend engagement campaigns.
