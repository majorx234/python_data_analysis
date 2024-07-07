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

# change index transform datetime-obj into datetime64
se_vs_de_df_only_data.index = pd.DatetimeIndex(se_vs_de_df_only_data.index)
# plot normal curve and a flatted one
se_vs_de_df_only_data.plot()
se_vs_de_df_only_data.resample("QE").mean().plot()

# Barplot consum index germany 2023
de_cci_22or23_df = df[(df["country"] == "DE")
                      & (df["indic"] == "BS-CSMCI")
                      & (df["s_adj"] == "NSA")]
de_cci_22or23_df_data = de_cci_22or23_df[[c for c in df.columns
                                          if (isinstance(c, datetime)
                                              and (c.year == 2022
                                                   or c.year == 2023))]]
de_cci_22or23_df_data.index = ["Consumer confidence indicator"]

# transpose date
de_cci_22or23_df_data_t = de_cci_22or23_df_data.transpose()[::-1]
# change index transform datetime-obj into datetime64
de_cci_22or23_df_data_t.index = pd.DatetimeIndex(de_cci_22or23_df_data_t.index)
de_cci_22or23_df_data_t.plot.bar(figsize=(16, 10))

# plot graphs
plt.show()
