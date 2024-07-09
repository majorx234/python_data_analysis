import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

df = pd.read_csv("city_temperature.csv", dtype={'State': object})

# take average temperatur of Frankfurt
df = df[df["City"] == "Munich"][['Year', 'Month', 'Day', 'AvgTemperature']]
df = df[df['AvgTemperature'] > -70]

# create Date column
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df = df[['Date', 'AvgTemperature']].set_index('Date')

# Fahrenheit to Celsius
df['AvgTemperature'] = (df['AvgTemperature']-32)*5/9

df['AvgTemperature'].plot()
plt.show()
