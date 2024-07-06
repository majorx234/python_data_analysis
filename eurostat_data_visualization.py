import pandas as pd
import eurostat
from datetime import datetime
import matplotlib.pyplot as plt

df = eurostat.get_data_df("ei_bsco_m")

# Edit dataframe
# edit column names
df = df.rename(columns={'geo\TIME_PERIOD': "country"})
df.columns = [datetime.strptime(f.split("-")[0] + "-" + f.split("-")[1] + "-01", "%Y-%m-%d")
              if f.startswith("19") or f.startswith("20") else f
              for f in df.columns]

# filter out Data from Germany and Sweden
se_vs_de_df = df[(df["country"].isin(["DE", "EA20", "SE"])) & (df["indic"] == "BS-CSMCI") & (df["s_adj"] == "NSA")]

# transpose data and take country as index
se_vs_de_df_only_data = se_vs_de_df[[c for c in df.columns if (isinstance(c, datetime) and c.year>=2000) or c == "country"]].set_index("country").transpose()

se_vs_de_df_only_data.index = pd.DatetimeIndex(se_vs_de_df_only_data.index)
se_vs_de_df_only_data.plot()
se_vs_de_df_only_data.resample("Q").mean().plot()
plt.show()
