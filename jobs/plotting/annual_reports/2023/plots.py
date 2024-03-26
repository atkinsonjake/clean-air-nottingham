import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar


comparisons = pd.read_csv('processed_data_can_sensors_hourly_calibrated.csv')
comparisons.dropna(inplace=True)
comparisons['sensor_index'] = comparisons['sensor_index'].astype('category')

mean_std_data = comparisons.groupby('fields').agg(mean_val=('reading', 'mean'), std_dev=('reading', 'std')).reset_index()
mean_std_data['threshold'] = 2 * mean_std_data['std_dev']

comparisons = comparisons.join(mean_std_data.set_index('fields'), on='fields')
comparisons = comparisons[abs(comparisons['reading'] - comparisons['mean_val']) <= comparisons['threshold']]

comparisons['date_only'] = pd.to_datetime(comparisons['datetime']).dt.date
comparisons['day_of_week'] = comparisons['date_only'].apply(lambda x: x.strftime('%A'))
weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
comparisons['day_of_week'] = pd.Categorical(comparisons['day_of_week'], categories=weekday_names, ordered=True)

bank_holidays = ["2022-12-27", "2023-01-02", "2023-04-07", "2023-04-10", "2023-05-01", "2023-05-29"]
comparisons['is_bank_holiday'] = comparisons['date_only'].isin(bank_holidays).replace({True: 'Yes', False: 'No'})

comparisons_no_bank_hols = comparisons[~comparisons['date_only'].isin(bank_holidays)]

CAN_COLOURS = ["#3d5a80", "#98c1d9", "#ee6c4d", "#e0fbfc"]

# Plot 1 (mean pollution levels)
grouped_df = comparisons.groupby(['sensor_index', 'fields'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_df, x='sensor_index', y='reading', hue='fields', palette=CAN_COLOURS)
plt.title('Mean pollution levels')
plt.xlabel('Sensor')
plt.ylabel('Reading (μgm-3)')
plt.legend(title='Pollutant')
plt.show()

# Plot 2: How does pollution change across the week?
avg_data = comparisons_no_bank_hols.groupby(['day_of_week', 'fields'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=avg_data, x='day_of_week', y='reading', hue='fields', palette=CAN_COLOURS)
plt.title('How does pollution change across the week?')
plt.xlabel('Day')
plt.ylabel('Mean reading (μgm-3)')
plt.legend(title='Pollutant')
plt.show()

# Plot 3: How does pollution change across the day?
comparisons['hour'] = pd.to_datetime(comparisons['time']).dt.hour
avg_data = comparisons.groupby(['hour', 'fields'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=avg_data, x='hour', y='reading', hue='fields', palette=CAN_COLOURS)
plt.title('How does pollution change across the day?')
plt.xlabel('Hour of day')
plt.ylabel('Mean reading (μgm-3)')
plt.legend(title='Pollutant')
plt.show()

# Plot 4: Do public holidays make a difference?
grouped_df = comparisons.groupby(['fields', 'is_bank_holiday'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_df, x='fields', y='reading', hue='is_bank_holiday', palette=CAN_COLOURS)
plt.title('Do public holidays make a difference?')
plt.xlabel('Pollutant')
plt.ylabel('Mean reading (μgm-3)')
plt.legend(title='Bank Holiday')
plt.show()

# Plot 5: Mean daily reading
grouped_df = comparisons.groupby(['date_only', 'fields'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped_df, x='date_only', y='reading', hue='fields', palette=CAN_COLOURS)
plt.title('Mean daily reading')
plt.xlabel('Date')
plt.ylabel('Mean reading (μgm-3)')
plt.xticks(rotation=45)
plt.legend(title='Pollutant')
plt.show()

# Plot 6: PM1, mean daily reading
pm_1 = comparisons[comparisons['fields'] == "pm1.0_atm"]
grouped_df = pm_1.groupby(['date_only'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped_df, x='date_only', y='reading', color=CAN_COLOURS[0])
plt.title('PM1, mean daily reading')
plt.xlabel('Date')
plt.ylabel('Mean reading (μgm-3)')
plt.xticks(rotation=45)
plt.show()

# Plot 7: PM2.5, mean daily reading with horizontal lines
pm_25 = comparisons[comparisons['fields'] == "pm2.5_atm"]
grouped_df = pm_25.groupby(['date_only'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped_df, x='date_only', y='reading', color=CAN_COLOURS[1])
plt.axhline(y=5, color=CAN_COLOURS[2], linestyle='--')
plt.axhline(y=20, color=CAN_COLOURS[0], linestyle='--')
plt.title('PM2.5, mean daily reading')
plt.xlabel('Date')
plt.ylabel('Mean reading (μgm-3)')
plt.xticks(rotation=45)
plt.show()

# Plot 8: PM10, mean daily reading with horizontal lines
pm_10 = comparisons[comparisons['fields'] == "pm10.0_atm"]
grouped_df = pm_10.groupby(['date_only'])['reading'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped_df, x='date_only', y='reading', color=CAN_COLOURS[1])
plt.axhline(y=15, color=CAN_COLOURS[2], linestyle='--')
plt.axhline(y=40, color=CAN_COLOURS[0], linestyle='--')
plt.title('PM10, mean daily reading')
plt.xlabel('Date')
plt.ylabel('Mean reading (μgm-3)')
plt.xticks(rotation=45)
plt.show()

# Plot 9: PM1 levels by sensor
plt.figure(figsize=(10, 6))
sns.boxplot(data=pm_1, x='sensor_index', y='reading', color=CAN_COLOURS[0])
plt.title('PM1 levels by sensor')
plt.xlabel('Sensor')
plt.ylabel('Reading (μgm-3)')
plt.show()

# Plot 10: PM2.5 levels by sensor
plt.figure(figsize=(10, 6))
sns.boxplot(data=pm_25, x='sensor_index', y='reading', color=CAN_COLOURS[1])
plt.title('PM2.5 levels by sensor')
plt.xlabel('Sensor')
plt.ylabel('Reading (μgm-3)')
plt.show()

# Plot 11: PM10 levels by sensor
plt.figure(figsize=(10, 6))
sns.boxplot(data=pm_10, x='sensor_index', y='reading', color=CAN_COLOURS[1])
plt.title('PM10 levels by sensor')
plt.xlabel('Sensor')
plt.ylabel('Reading (μgm-3)')
plt.show()
