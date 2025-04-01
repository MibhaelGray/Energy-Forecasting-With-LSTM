import pandas as pd


df = pd.read_csv('Data\WeatherData.csv')

columns_to_keep = ['STATION', 'DATE', 'HourlyDryBulbTemperature', 
                   'HourlyRelativeHumidity', 'HourlyWindSpeed']

df_filtered = df[columns_to_keep]
df_filtered.to_csv('filtered_weather_data.csv', index=False)

print(f"Filtered data saved with {len(df_filtered)} rows and {len(columns_to_keep)} columns")
print(f"Columns kept: {columns_to_keep}")