import pandas as pd

# Importing the data
filtered_weather_data = pd.read_csv("C:/Users/mgray/OneDrive/Documents/Energy Forecasting/Data/Weather Data/filtered_weather_data.csv")
print(filtered_weather_data.head())


# We need to find how many rows have missing values

print(filtered_weather_data.isnull().sum())