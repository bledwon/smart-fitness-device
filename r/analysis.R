# Bellabeat Fitbit Analysis (R template)

library(readr)
library(dplyr)
library(lubridate)

# Update these paths as needed
activity <- read_csv("data/raw/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv")
sleep <- read_csv("data/raw/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv")

activity <- activity %>%
  mutate(ActivityDate = mdy(ActivityDate),
         day_of_week = wday(ActivityDate, label = TRUE))

sleep <- sleep %>%
  mutate(SleepDay = mdy_hms(SleepDay),
         sleep_date = as.Date(SleepDay),
         day_of_week = wday(sleep_date, label = TRUE))

# Summary metrics
activity %>% summarise(
  avg_steps = mean(TotalSteps, na.rm = TRUE),
  pct_10k = mean(TotalSteps >= 10000, na.rm = TRUE)
)

sleep %>% summarise(
  avg_sleep_hours = mean(TotalMinutesAsleep, na.rm = TRUE) / 60,
  pct_lt_7h = mean(TotalMinutesAsleep < 420, na.rm = TRUE)
)

# Day-of-week trends
activity %>% group_by(day_of_week) %>% summarise(avg_steps = mean(TotalSteps, na.rm = TRUE))

sleep %>% group_by(day_of_week) %>% summarise(avg_sleep_min = mean(TotalMinutesAsleep, na.rm = TRUE))
