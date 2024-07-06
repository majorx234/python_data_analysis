import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

wage_data = pd.read_csv("./data/wage.csv", index_col=0)

# get information about table
# wage_data.columns
# wage_data[['age','wage']]
# wage_data[['age','wage']].describe()

# plot data
fig, ax = plt.subplots()
# subpolots
wage_data.plot.scatter(ax=ax, x='age',y='wage')
wage_data.groupby('age')['wage'].median().plot(ax=ax, color="red")
plt.show()
