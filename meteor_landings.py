import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime
from ast import literal_eval as make_tuple
import math
from shapely.geometry import Point

df = pd.read_csv("data/Meteorite_Landings_20240714.csv")
gdf = gpd.read_file('data/ne_10m_admin_0_countries.zip')

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

# lets find all amount of meteors fallen on Countries in the european union
countries = gdf[(gdf.ISO_A2 != "-99")].ISO_A2.unique()

gdf_meteors = gdf_meteors[~ (gdf_meteors["Longitude"].isnull() | (gdf_meteors["Latitude"].isnull())) ]
meteors_per_country = pd.DataFrame(0, index=countries, columns=range(2))
meteors_per_country.columns = ["amount", "sum mass"]

for country in countries:
    print("next country: {}".format(country))
    country_shape = gdf[gdf.ISO_A2 == country]
    for index, meteor in gdf_meteors.iterrows():
        if country_shape["geometry"].contains(Point(meteor["Longitude"],
                                                    meteor["Latitude"])).any():
            meteors_per_country.loc[country, "amount"] += 1
            mass = gdf_meteors.loc[index, "mass (g)"]
            if isinstance(mass, float):
                meteors_per_country.loc[country, "sum_mass"] += mass

print(meteors_per_country)
meteors_per_country.to_csv("data/meteors_per_country.csv")
gdf_with_mass_amount = pd.merge(gdf, meteors_per_country, how="left",
                                left_on='ISO_A2', right_index=True)
print(gdf_with_mass_amount)
meteors_per_country.to_csv("data/gdf_with_mass_amount.csv")

plt.show()
