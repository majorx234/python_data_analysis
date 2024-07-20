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
    - script: `time_series_prediction.py`
    - show two examples
      - 1st with sklearn.linear_model.LinearRegression
      - 2nd with scipy.stats.linregress
  - temperature data of cities:
    - data: https://huggingface.co/spaces/Epitech/IOT_temperature/resolve/main/city_temperature.csv?download=true
    - script: time_series_prediction_temperature.py
- 4. bayesian linear regression
  - scrip `bayesian_linear_regression.py`
  - linear regression using bayesian therorems
  - to gain information about uncertainty
  - uses PyMC: https://www.pymc.io
  - https://towardsdatascience.com/introduction-to-bayesian-linear-regression-e66e60791ea7
  - https://medium.com/@vanillaxiangshuyang/bayesian-linear-regression-with-tensorflow-probability-5a967b133367
- 5. ideas from tutrial by Stefanie Molin
  - https://github.com/stefmolin/pandas-workshop
  - script: `meteor_landings.py`
  - use data with GPS information and a world map
  - use GeoPands to integrade information
    - 1. Take world map and draw impacts of meteorids:
      - idea from https://geopandas.org/en/latest/gallery/create_geopandas_from_pandas.html
    - 2. count impacts for each country (is point in georegion)
      - idea from here:
        - https://stackoverflow.com/questions/63884865/how-can-i-get-country-name-by-coordinates-without-external-api
        - https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html
      - doesn't work that well
      - need better check if point is in a region:
        - https://gis.stackexchange.com/questions/437956/best-way-to-check-if-a-point-is-in-a-region
