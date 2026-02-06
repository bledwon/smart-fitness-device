#!/usr/bin/env python3
"""Export charts as PNGs from processed CSVs for Tableau/Power BI/Slides."""
from pathlib import Path
import csv
import matplotlib.pyplot as plt

BASE = Path('/Users/benledwon/Desktop/Github_connection/Smart_fitness_device')
PROCESSED = BASE / 'data' / 'processed'
OUT = BASE / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
})

DAY_FULL = {
    'Mon': 'Monday',
    'Tue': 'Tuesday',
    'Wed': 'Wednesday',
    'Thu': 'Thursday',
    'Fri': 'Friday',
    'Sat': 'Saturday',
    'Sun': 'Sunday',
}


def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def plot_bar(x, y, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(x, y, color='#2E6F95')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=200)
    plt.close(fig)


def plot_line(x, y, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(x, y, marker='o', color='#2E6F95')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.ticklabel_format(style='plain', axis='y', useOffset=False)
    ax.grid(axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=200)
    plt.close(fig)


# Steps by day of week
rows = read_csv(PROCESSED / 'daily_by_dayofweek.csv')
rows.sort(key=lambda r: list(DAY_FULL.keys()).index(r['day_of_week']))
x = [DAY_FULL[r['day_of_week']] for r in rows]
y = [float(r['avg_steps']) for r in rows]
plot_bar(x, y, 'Average Steps by Day of Week', 'Day', 'Steps', 'avg_steps_by_day.png')

# Calories by day of week
x = [DAY_FULL[r['day_of_week']] for r in rows]
y = [float(r['avg_calories']) for r in rows]
plot_bar(x, y, 'Average Calories by Day of Week', 'Day', 'Calories', 'avg_calories_by_day.png')

# Active minutes by day of week
x = [DAY_FULL[r['day_of_week']] for r in rows]
y = [float(r['avg_active_minutes']) for r in rows]
plot_bar(x, y, 'Average Active Minutes by Day of Week', 'Day', 'Active Minutes', 'avg_active_minutes_by_day.png')

# Sleep by day of week
rows = read_csv(PROCESSED / 'sleep_by_dayofweek.csv')
rows.sort(key=lambda r: list(DAY_FULL.keys()).index(r['day_of_week']))
x = [DAY_FULL[r['day_of_week']] for r in rows]
y = [float(r['avg_sleep_minutes'])/60 for r in rows]
plot_bar(x, y, 'Average Sleep Hours by Day of Week', 'Day', 'Hours', 'avg_sleep_by_day.png')

# Steps by hour (avg per user-hour record)
rows = read_csv(PROCESSED / 'steps_by_hour.csv')
rows.sort(key=lambda r: int(r['hour']))
x = [int(r['hour']) for r in rows]
y = [float(r['avg_steps_per_user_hour']) for r in rows]
plot_line(x, y, 'Average Steps per User-Hour', 'Hour', 'Avg Steps', 'steps_by_hour.png')

print('Exported PNG charts to figures/.')
