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
meteors_per_country.columns = ["amount", "sum_mass"]

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


def amount_to_color(amount):
    if isinstance(amount, float):
        if amount.isnull():
            return '#B0B0B0'
    else:
        if not isinstance(amount, int):
            return '#B0B0B0'
    if (amount <= 10):
        return '#00FF00'
    elif (amount < 20):
        return '#FFFF00'
    elif (amount < 50):
        return '#FFA500'
    elif (amount < 100):
        return '#FF0000'
    else:
        return '#A020F0'


def value_to_color_with_thresholds(value, thresholds):
    if isinstance(value, float):
        if math.isnan(value):
            return '#B0B0B0'
    else:
        return '#B0B0B0'
    if (value <= thresholds[0]):
        return '#00FF00'
    elif (value < thresholds[1]):
        return '#FFFF00'
    elif (value < thresholds[2]):
        return '#FFA500'
    elif (value < thresholds[3]):
        return '#FF0000'
    else:
        return '#A020F0'


meteors_per_country["color"] = [amount_to_color(x) for x in meteors_per_country.amount]

gdf_with_mass_amount_percentiles = meteors_per_country.sum_mass.quantile([0.0,
                                                                          0.005,
                                                                          0.05,
                                                                          0.25,
                                                                          0.50,
                                                                          0.75,
                                                                          0.95,
                                                                          0.995,
                                                                          1.0])

mass_steps = gdf_with_mass_amount_percentiles[(gdf_with_mass_amount_percentiles > 0.1)]

meteors_per_country["color_mass"] = [value_to_color_with_thresholds(x, mass_steps.to_numpy()) for x in meteors_per_country.sum_mass.to_numpy()]
gdf_with_mass_amount = pd.merge(gdf, meteors_per_country, how="left",
                                left_on='ISO_A2', right_index=True)
gdf_with_mass_amount["color"] = gdf_with_mass_amount["color"].fillna("#B0B0B0")
gdf_with_mass_amount["color_mass"] = gdf_with_mass_amount["color_mass"].fillna("#B0B0B0")

print(gdf_with_mass_amount)

gdf_with_mass_amount.plot(color=gdf_with_mass_amount["color"])

gdf_with_mass_amount.to_csv("data/gdf_with_mass_amount.csv")

gdf_with_mass_amount.plot(color=gdf_with_mass_amount["color_mass"])

plt.show()
