import pandas as pd
import eurostat
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

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

# barplot consom index 2023-01 of different countries
cci_eu_df = df[(df["indic"] == "BS-CSMCI")
               & (df["s_adj"] == "NSA")]
cci_eu_df_202301 = cci_eu_df[["country", datetime(2023, 1, 1)]]
cci_eu_df_202301 = cci_eu_df_202301[(df["country"] != "EU27_2020") & (df["country"] != "UK")].set_index("country")

# exchange country shortnames with realnames
cci_eu_df_202301.index = [country_names[i] for i in cci_eu_df_202301.index]


# visualize df with sorted horizontal bar plot
cci_eu_df_202301.sort_values( datetime(2023, 1, 1), ascending=[False]).plot.barh(figsize=(16, 10))

# plot histogram
cci_eu_df_202301.plot.hist(bins=20)

# we want consum data since 2010 for all countries
columns_since_2010 = [c for c in df.columns if (isinstance(c, datetime) and (c.year >= 2010))]
cci_eu_df_since_2010 = cci_eu_df[columns_since_2010 + ['country']].set_index("country")

# exchange country shortnames with realnames
cci_eu_df_since_2010.index = [country_names[i] for i in cci_eu_df_since_2010.index]
cci_eu_df_since_2010_transposed = cci_eu_df_since_2010.transpose()
label_order = cci_eu_df_since_2010_transposed.median().sort_values().index

# boxplot with seaborn, unfortunately it needs a melt
plt.figure(figsize=(8, 10))
sns.boxplot(x="value", y="variable",  data=pd.melt(cci_eu_df_since_2010_transposed), order=label_order, palette="viridis")


# violineplot with density information (slidely changed order)
plt.figure()
sns.violinplot(x="value", y="variable", data=pd.melt( cci_eu_df_since_2010_transposed[["Greece", "Germany", "Sweden", "Denmark"]]), order=["Greece", "Germany", "Denmark", "Sweden"], palette="viridis")

# Part 2
# get table of indices:
# 'BS-CSMCI', 'BS-FS-LY', 'BS-FS-NY', 'BS-GES-LY', 'BS-GES-NY', 'BS-MP-NY', 'BS-MP-PR', 'BS-PT-LY', 'BS-PT-NY', 'BS-SFSH', 'BS-SV-NY', 'BS-SV-PR', 'BS-UE-NY'
y20 = [c for c in df.columns if (isinstance(c, datetime) and (c.year >= 2000) and (c.year < 2020))]
de20 = df[(df["s_adj"] == "NSA") & (df["country"] == "DE")].set_index("indic")[y20].transpose()
de20.index = pd.DatetimeIndex(de20.index)

# calculate Pearson Correlationindex
corr = []
indicators = de20.columns
for i1 in indicators:
    res = []
    for i2 in indicators:
        r, p = stats.pearsonr(de20[i1].values, de20[i2].values)
        res.append(r)
    corr.append(res)

# create pandas dataframe:
ihm = pd.DataFrame(corr, index=de20.columns, columns=de20.columns)
plt.figure(figsize=(12,12))
sns.heatmap(ihm, cmap="RdBu", vmin=-1, vmax=1)

# check corelation of BS-SFSH and "BS-CSMCI
# just as scatter plot
de20.plot.scatter(x="BS-SFSH", y="BS-CSMCI")

# as joint plot
# here with regression line and histogram of both indices
# temporal context ca be done via dimensionality of color
joint_plot_de20 = sns.jointplot(x=de20["BS-SFSH"], y=de20["BS-CSMCI"], scatter=False, kind="reg")
joint_plot_de20.ax_joint.text(x= 5.0, y=-25.0, s="pearsonr=%0.2f p=%e" %stats.pearsonr(de20["BS-SFSH"],de20["BS-CSMCI"]))

# take only first month
de20_1st = de20[de20.index.month==1].copy()
# take only even years
de20_1st_even = de20_1st[::2]
# remove M01 from index
de20_1st_even.index = de20_1st_even.index.map(str).str.replace("-01-01 00:00:00", "")
years_index_float = [float(c) for c in de20_1st_even.index]
sns.scatterplot(data=de20_1st_even, x="BS-SFSH", y="BS-CSMCI",
                hue=years_index_float, legend=True)
# detail plot without Legend
sns.scatterplot(data=de20, x="BS-SFSH", y="BS-CSMCI",
                hue=de20.index, legend=False)

# plot all graphs
plt.show()
