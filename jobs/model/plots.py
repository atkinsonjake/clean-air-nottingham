
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sensor_data_fn = 'all_sensors.csv'
data = pd.read_csv(sensor_data_fn)

data = data.drop(columns = 'Unnamed: 0')
data['DateTime'] = pd.to_datetime(data['DateTime'])

data['day_of_week'] = data['DateTime'].dt.day_name()
data['Month'] = data['DateTime'].dt.month

variables = ['humidity', 'pm1', 'pm25', 'pm10', 'pressure','temperature']
groupbys = ['DateTime' , 'day_of_week', 'Month']

for grouping in groupbys:
    for var in variables:
        grouped_data = data.groupby(by = grouping).mean()
        plt.figure(figsize = (16,8))
        sns.lineplot(data = grouped_data[var])
        plt.title(f'{var}' , fontsize = 12)
        plt.show()
