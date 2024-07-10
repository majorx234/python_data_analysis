# Info
- learning data science with python, pandas...
## Project1: data visualization
- `pip install scikit-learn statsmodels eurostat notebook matplotlib seaborn pandas`
- or just: `pip install -r requirements.txt`
- 1. work with eurostat data
  - script: `eurostat_data_visualization.py`
  - ideas taken from `iX Magazin issue: 2021/01 page: 56f`
  - https://github.com/datanizing/ix-jupyter-visualisierung
  - have different plots: curve, Barplot, horizontal Barplot, histogram, Boxplot
  - make use of matplotlib and seaborn
- 2. work with US-Income data:
  - ideas taken from: GratzerLinuxTage 2019: presentation by Claus Aichinger
  - https://media.ccc.de/v/glt19-87-using-python-pandas-for-data-analysis
  - https://github.com/caichinger/glt2019_ml_intro
  - create a scatter plot with further subplots to draw mean values as a curve
  - script: `us_wage_income_envelope.py`
- 3. work with time series data (prediction and analysis)
  - linea regression:
    - script: time_series_prediction.py
    - show two examples
      - 1st with sklearn.linear_model.LinearRegression
      - 2nd with scipy.stats.linregress
  - temperature data of cities:
    - data: https://huggingface.co/spaces/Epitech/IOT_temperature/resolve/main/city_temperature.csv?download=true
    - script: time_series_prediction_temperature.py

