import pandas as pd
import geopandas
import matplotlib.pyplot as plt

bl_geo = geopandas.read_file("data/europe.geo.json")
bl_geo.loc[bl_geo["iso_a2"] == "GB", "iso_a2"] = "UK"
bl_geo = bl_geo[["iso_a2", "geometry"]]
bl_geo[~bl_geo["iso_a2"].isin(["RU", "IS", "UA", "BY", "MD"])].plot(figsize=(10,10))
plt.show()
