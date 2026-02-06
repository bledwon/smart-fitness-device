#!/usr/bin/env python3
"""Analyze Bellabeat Fitbit dataset with Python stdlib only.
Generates Excel-friendly summary tables in data/processed/.
"""
from __future__ import annotations

import csv
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from math import sqrt

BASE = Path('/Users/benledwon/Desktop/Github_connection/Smart_fitness_device')
RAW1 = BASE / 'data' / 'raw' / 'mturkfitbit_export_3.12.16-4.11.16' / 'Fitabase Data 3.12.16-4.11.16'
RAW2 = BASE / 'data' / 'raw' / 'mturkfitbit_export_4.12.16-5.12.16' / 'Fitabase Data 4.12.16-5.12.16'
OUT = BASE / 'data' / 'processed'

DAY_NAMES = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    v = value.strip()
    # Common format: 4/12/2016
    for fmt in ('%m/%d/%Y', '%m/%d/%Y %I:%M:%S %p'):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    # Some files have 4/12/2016 12:00:00 AM
    try:
        return datetime.strptime(v, '%m/%d/%Y %I:%M:%S %p')
    except ValueError:
        return None


def parse_dt(value: str) -> datetime | None:
    if not value:
        return None
    v = value.strip()
    # format: 4/12/2016 1:00:00 AM
    for fmt in ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S'):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    return None


def read_csv(path: Path):
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def write_csv(path: Path, headers: list[str], rows: list[list]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


# ---------- DAILY ACTIVITY ----------
activity_rows = {}
activity_ids = set()

for p in [RAW1/'dailyActivity_merged.csv', RAW2/'dailyActivity_merged.csv']:
    if not p.exists():
        continue
    for r in read_csv(p):
        dt = parse_date(r['ActivityDate'])
        if not dt:
            continue
        key = (r['Id'], dt.date())
        # De-duplicate by Id+date (prefer latest file if overlap)
        activity_rows[key] = r
        activity_ids.add(r['Id'])

# Aggregate stats
steps_total = 0
calories_total = 0
rows_count = 0

steps_by_day = defaultdict(int)
steps_by_dow = defaultdict(list)
calories_by_dow = defaultdict(list)
active_minutes_by_dow = defaultdict(list)

user_days = defaultdict(int)
user_steps_total = defaultdict(int)

steps_cal_pairs = []

for (uid, date), r in activity_rows.items():
    rows_count += 1
    steps = int(float(r['TotalSteps']))
    calories = int(float(r['Calories']))
    v_active = int(float(r['VeryActiveMinutes']))
    f_active = int(float(r['FairlyActiveMinutes']))
    l_active = int(float(r['LightlyActiveMinutes']))
    total_active = v_active + f_active + l_active

    steps_total += steps
    calories_total += calories

    dow = DAY_NAMES[date.weekday()]
    steps_by_dow[dow].append(steps)
    calories_by_dow[dow].append(calories)
    active_minutes_by_dow[dow].append(total_active)

    user_days[uid] += 1
    user_steps_total[uid] += steps

    steps_cal_pairs.append((steps, calories))

# avg steps per user per day
user_avg_steps = {u: (user_steps_total[u]/user_days[u]) for u in user_days}

# percent days >= 10k steps
days_10k = sum(1 for (uid, date), r in activity_rows.items() if int(float(r['TotalSteps'])) >= 10000)

# Pearson correlation steps vs calories
n = len(steps_cal_pairs)
if n:
    sum_x = sum(s for s, _ in steps_cal_pairs)
    sum_y = sum(c for _, c in steps_cal_pairs)
    sum_x2 = sum(s*s for s, _ in steps_cal_pairs)
    sum_y2 = sum(c*c for _, c in steps_cal_pairs)
    sum_xy = sum(s*c for s, c in steps_cal_pairs)
    denom = sqrt((n*sum_x2 - sum_x**2) * (n*sum_y2 - sum_y**2))
    corr = (n*sum_xy - sum_x*sum_y) / denom if denom else 0
else:
    corr = 0

# ---------- SLEEP ----------
sleep_rows = {}
sleep_ids = set()

for p in [RAW1/'sleepDay_merged.csv', RAW2/'sleepDay_merged.csv']:
    if not p.exists():
        continue
    for r in read_csv(p):
        dt = parse_dt(r['SleepDay']) or parse_date(r['SleepDay'])
        if not dt:
            continue
        key = (r['Id'], dt.date())
        sleep_rows[key] = r
        sleep_ids.add(r['Id'])

sleep_minutes = []
sleep_by_dow = defaultdict(list)

for (uid, date), r in sleep_rows.items():
    mins = int(float(r['TotalMinutesAsleep']))
    sleep_minutes.append(mins)
    dow = DAY_NAMES[date.weekday()]
    sleep_by_dow[dow].append(mins)

sleep_lt_7 = sum(1 for m in sleep_minutes if m < 7*60)

# ---------- HOURLY STEPS ----------
hourly_rows = []
for p in [RAW1/'hourlySteps_merged.csv', RAW2/'hourlySteps_merged.csv']:
    if not p.exists():
        continue
    for r in read_csv(p):
        dt = parse_dt(r['ActivityHour'])
        if not dt:
            continue
        hourly_rows.append((r['Id'], dt.hour, int(float(r['StepTotal']))))

steps_by_hour = defaultdict(int)
users_by_hour = defaultdict(set)
rows_by_hour = defaultdict(int)
for uid, hour, steps in hourly_rows:
    steps_by_hour[hour] += steps
    users_by_hour[hour].add(uid)
    rows_by_hour[hour] += 1

# ---------- WEIGHT LOG ----------
weight_rows = []
for p in [RAW1/'weightLogInfo_merged.csv', RAW2/'weightLogInfo_merged.csv']:
    if not p.exists():
        continue
    for r in read_csv(p):
        weight_rows.append(r)

# ---------- OUTPUTS ----------
# Overall summary
summary_rows = [
    ['total_daily_activity_rows', rows_count],
    ['unique_activity_users', len(activity_ids)],
    ['unique_sleep_users', len(sleep_ids)],
    ['avg_steps_per_day', round(steps_total/rows_count, 2) if rows_count else 0],
    ['avg_calories_per_day', round(calories_total/rows_count, 2) if rows_count else 0],
    ['percent_days_10k_steps', round(days_10k/rows_count, 4) if rows_count else 0],
    ['steps_calories_correlation', round(corr, 4)],
    ['avg_sleep_hours', round(sum(sleep_minutes)/len(sleep_minutes)/60, 2) if sleep_minutes else 0],
    ['percent_sleep_lt_7h', round(sleep_lt_7/len(sleep_minutes), 4) if sleep_minutes else 0],
    ['weight_log_rows', len(weight_rows)],
]
write_csv(OUT/'summary_overall.csv', ['metric','value'], summary_rows)

# Day-of-week summaries
rows = []
for dow in DAY_NAMES:
    if steps_by_dow[dow]:
        rows.append([dow, round(sum(steps_by_dow[dow])/len(steps_by_dow[dow]),2), round(sum(calories_by_dow[dow])/len(calories_by_dow[dow]),2), round(sum(active_minutes_by_dow[dow])/len(active_minutes_by_dow[dow]),2)])
write_csv(OUT/'daily_by_dayofweek.csv', ['day_of_week','avg_steps','avg_calories','avg_active_minutes'], rows)

# Sleep by day of week
rows = []
for dow in DAY_NAMES:
    if sleep_by_dow[dow]:
        rows.append([dow, round(sum(sleep_by_dow[dow])/len(sleep_by_dow[dow]),2)])
write_csv(OUT/'sleep_by_dayofweek.csv', ['day_of_week','avg_sleep_minutes'], rows)

# Steps by hour (average per user-hour record)
rows = []
for h in range(24):
    total = steps_by_hour.get(h, 0)
    users = len(users_by_hour.get(h, []))
    row_count = rows_by_hour.get(h, 0)
    avg = (total / row_count) if row_count else 0
    rows.append([h, round(avg, 2), total, users, row_count])
write_csv(OUT/'steps_by_hour.csv', ['hour','avg_steps_per_user_hour','total_steps','active_users','row_count'], rows)

# User average steps distribution
rows = [[uid, round(avg,2)] for uid, avg in sorted(user_avg_steps.items())]
write_csv(OUT/'user_avg_steps.csv', ['id','avg_steps_per_day'], rows)

print('Done.')
