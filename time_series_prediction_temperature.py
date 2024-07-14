import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.preprocessing import MinMaxScaler
from os.path import exists

city_temperature_file_exists = exists("data/city_temperature.csv")

if not city_temperature_file_exists:
    print("need to download temperature data: https://huggingface.co/spaces/Epitech/IOT_temperature/blob/main/city_temperature.csv")
    exit()

df = pd.read_csv("data/city_temperature.csv", dtype={'State': object})

# take average temperatur of Frankfurt
df = df[df["City"] == "Munich"][['Year', 'Month', 'Day', 'AvgTemperature']]
df = df[df['AvgTemperature'] > -70]

# create Date column
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df = df[['Date', 'AvgTemperature']].set_index('Date')

# Fahrenheit to Celsius
df['AvgTemperature'] = (df['AvgTemperature']-32)*5/9

df['AvgTemperature'].plot()

# are there missing dates?
# get missing dates:
first_index = df.index[0]
last_index = df.index[-1]
missing_dates = pd.date_range(start=first_index, end=last_index).difference(df.index)
num_missing_dates = len(missing_dates)
print("days missing: {} missing dates: {}".format(num_missing_dates, missing_dates))


# 1st daily resampling
dg = df.copy()
resamp = 'D'
# fill days with NaN
dg = dg.resample(resamp).mean()
days_with_nan = dg[dg['AvgTemperature'].isna()]
print('Missing: ', resamp, ': ', int(df.loc[:, :].isnull().sum()))

# doing linear interpolation
dg = dg.interpolate(method='linear')
dg.plot()

# 2nd weekly resampling
dw = df.copy()
resamp = '2W'
dw = dw.resample(resamp).mean()
weeks_with_nan = dg[dg['AvgTemperature'].isna()]
print('Missing: ', resamp, ': ', int(dw.loc[:, :].isnull().sum()))
dw = dw.interpolate(method='linear')
dw.plot()

# smoothing
# 1st moving average
# like 2week average (with overlapping)
# window width gives information about smoothening


# exponential smoothing
# Holt-Winters 3rd exponential smothening
dh = dg.copy()
sc = MinMaxScaler(feature_range=(0.00001, 1))
dh['scal'] = sc.fit_transform(dh)
model = ExponentialSmoothing(dh['scal'], trend='add',  seasonal='add',
                             use_boxcox=False, seasonal_periods=26)
dmodel1 = model.fit(
    smoothing_level=0.1,
    smoothing_trend=0.5,
    smoothing_seasonal=0.1,
    optimized=False
    )

dhfc = pd.DataFrame(dmodel1.forecast(60), columns=['forecast'])
dhfc['forecast'] = sc.inverse_transform([dhfc.loc[:, 'forecast'].tolist()])[0, :]
dh['fitted'] = sc.inverse_transform([dmodel1.fittedvalues.tolist()])[0, :]

hw_param = f"({dmodel1.params['smoothing_level']:.2g}, \
{dmodel1.params['smoothing_trend']:.2g}, \
{dmodel1.params['smoothing_seasonal']:.2g})"

fig, ax = plt.subplots()
dh['AvgTemperature'].plot(ax=ax)
dh['fitted'].plot(ax=ax)
dhfc['forecast'].plot(ax=ax)
ax.legend(['org', 'fitted'])
ax.set_xlim('2014-04-01', '2022-12-30')
plt.title('Holt-Winters (' + hw_param)

print(dmodel1.mle_retvals)
print('-'*3)
print(dmodel1.params)
print('-'*3)
print(dmodel1.params_formatted)
dmodel1.summary()

# Fit-version
dmodel2 = model.fit()
dhfc = pd.DataFrame(dmodel1.forecast(60), columns=['forecast'])
dhfc['forecast'] = sc.inverse_transform([dhfc.loc[:, 'forecast'].tolist()])[0, :]
dh['fitted'] = sc.inverse_transform([dmodel1.fittedvalues.tolist()])[0, :]

hw_param = f"({dmodel1.params['smoothing_level']:.2g}, \
{dmodel1.params['smoothing_trend']:.2g}, \
{dmodel1.params['smoothing_seasonal']:.2g})"

fig, ax = plt.subplots()
dh['AvgTemperature'].plot(ax=ax)
dh['fitted'].plot(ax=ax)
dhfc['forecast'].plot(ax=ax)
ax.legend(['org', 'fitted'])
ax.set_xlim('2014-04-01', '2022-12-30')
plt.title('Holt-Winters(Fit) (' + hw_param)

plt.show()
