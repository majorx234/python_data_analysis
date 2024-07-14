import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime
from ast import literal_eval as make_tuple

df = pd.read_csv("data/Meteorite_Landings_20240714.csv")
gdf = gpd.read_file('data/ne_10m_admin_0_countries.shp')

bl_geo = gpd.read_file("data/europe.geo.json")
bl_geo.loc[bl_geo["iso_a2"] == "GB", "iso_a2"] = "UK"
bl_geo = bl_geo[["iso_a2", "geometry"]]

longitude = []
latitude = []
df = df[df.GeoLocation.apply(lambda x: not isinstance(x, (float, float)))]
df = df[df.GeoLocation.apply(lambda x: not (x == (0.0, 0.0)))]

for index, meteor in df.iterrows():
    location = make_tuple(meteor["GeoLocation"])
    latitude.append(location[0])
    longitude.append(location[1])

df['Longitude'] = pd.Series(longitude)
df['Latitude'] = pd.Series(latitude)

gdf_meteors = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326"
)

fig, ax = plt.subplots(figsize=(14, 7))
gdf.plot(ax=ax)
gdf_meteors.plot(ax=ax, alpha=0.7, color="red")

plt.show()

# lets find all amount of metears fallen on Countries in the european union
