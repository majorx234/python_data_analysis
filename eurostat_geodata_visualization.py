import pandas as pd
import eurostat
from datetime import datetime
import geopandas
import matplotlib.pyplot as plt

country_names = {"HU": 'Hungary',
                 "EL": "Greece",
                 "PT": "Portugal",
                 "SI": "Slovenia",
                 "LV": "Latvia",
                 "EE": "Estonia",
                 "SK": "Slovakia",
                 "BG": "Bulgaria",
                 "RO": "Romania",
                 "MK": "North Macedonia",
                 "AT": "Austria",
                 "SE": "Sweden",
                 "NL": "Netherlands",
                 "ES": "Spain",
                 "CZ": "Czechia",
                 "HR": "Croatia",
                 "TR": "Türkiye",
                 "EU27_2020": "European Union",
                 "EA20": "EuroArea",
                 "FR": "France",
                 "CY": "Cyprus",
                 "IE": "Ireland",
                 "DE": "Germany",
                 "IT": "Italy",
                 "AL": "Albania",
                 "LU": "Luxembourg",
                 "BE": "Belgium",
                 "PL": "Poland",
                 "DK": "Denmark",
                 "FI": "Finnland",
                 "MT": "Malta",
                 "RS": "Servia",
                 "ME": "Montenegro",
                 "LT": "Lithuania",
                 "UK": "United Kingdom"
                 }

df = eurostat.get_data_df("ei_bsco_m")

# Edit dataframe
# edit column names
df = df.rename(columns={'geo\TIME_PERIOD': "country"})
df.columns = [datetime.strptime(f.split("-")[0] + "-" + f.split("-")[1] + "-01", "%Y-%m-%d")
              if f.startswith("19") or f.startswith("20") else f
              for f in df.columns]

bl_geo = geopandas.read_file("data/europe.geo.json")
bl_geo.loc[bl_geo["iso_a2"] == "GB", "iso_a2"] = "UK"
bl_geo = bl_geo[["iso_a2", "geometry"]]
bl_geo[~bl_geo["iso_a2"].isin(["RU", "IS", "UA", "BY", "MD"])].plot(figsize=(10, 10))

bl_geo_eu = bl_geo[~bl_geo["iso_a2"].isin(["RU", "IS", "UA", "BY", "MD"])]
df_data = df[(df["indic"] == "BS-CSMCI") & (df["s_adj"] == "NSA")]
ghm = geopandas.GeoDataFrame(pd.merge(df_data, bl_geo_eu, left_on="country",
                                      right_on='iso_a2', how="outer"))
ghm.plot(column=datetime(2020, 8, 1), legend=True,
         legend_kwds={'orientation': "horizontal"},
         missing_kwds={"color": "lightgrey"},
         figsize=(10, 10))
plt.show()
