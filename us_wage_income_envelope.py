import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import seaborn as sns

wage_data = pd.read_csv("./data/wage.csv", index_col=0)

# get information about table
# wage_data.columns
# wage_data[['age','wage']]
# wage_data[['age','wage']].describe()

# plot data
fig1, ax1 = plt.subplots(figsize=(10, 4))
# subpolots
wage_data.plot.scatter(ax=ax1, x='age',y='wage')
wage_data.groupby('age')['wage'].median().plot(ax=ax1, color="pink")

# incomeme depending on education

edu_grad = wage_data.education.unique()
edu_grad.sort()
edu_grad_col_dict = {'1. < HS Grad': "red",
                     '2. HS Grad': "orange",
                     '3. Some College': "yellow",
                     '4. College Grad': "yellowgreen",
                     '5. Advanced Degree': "green"
                     }
patches = []
for grad in edu_grad:
    color=edu_grad_col_dict[grad]
    wage_data[wage_data['education'].isin([grad])].groupby('age')['wage'].median().plot(ax=ax1, color=color)
    patch = mpatches.Patch(color=color, label=grad)
    patches.append(patch)

ax1.legend(handles=patches)
plt.show()
