import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv("data/Meteorite_Landings_20240714.csv")
gdf = gpd.read_file('data/ne_10m_admin_0_countries.shp')

gdf.plot()
plt.show()

# lets find all amount of metears fallen on Countries in the european union
