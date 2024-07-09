import random as rnd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats


# create linear data (20 values) with noise
data_x1 = [x for x in range(100)]
data_y2 = []
for i in data_x1:
    data_y2.append(i + 2* (rnd.random()-0.5))

data_x1 = np.array(data_x1).reshape((-1, 1))
data_y2 = np.array(data_y2)

# create linear regression model with help of sklearn library
model = LinearRegression().fit(data_x1, data_y2)
r_sq = model.score(data_x1, data_y2)

m1 = model.coef_
b1 = model.intercept_

print(f'y = {m1}x + {b1}')

# plot values
plt.scatter(data_x1, data_y2, c="blue")

# plot regression line
plt.plot([0, 99], [m1*0+b1, m1*99+b1], marker='o', color='red')

# 2nd way to create values with noise
ndat = 100
# make use of numpy pseudo random numer generator with different seeds
rng = np.random.default_rng(42)
rng2 = np.random.default_rng(43)


def lin_func_with_noise(x, m=4, b=20, e=0):
    return m * x + b + e


# create numpy arrays
# some x values between 0 and 50
data_x2 = rng.random(ndat)*50
# some random values between 0 and 10
e = rng2.normal(0, 10, len(data_x2))
# y is then a linear function of x + noise e
data_y2 = lin_func_with_noise(data_x2, e=e)
# put values into the scipy statistic regression model
scipymodel = scipy.stats.linregress(data_x2, data_y2)
m2 = scipymodel.slope
b2 = scipymodel.intercept
print(f'y = {m2:.2g}x + {b2:.3g}')

min_x2 = min(data_x2)
max_x2 = max(data_x2)

#plot values
plt.scatter(data_x2, data_y2, c="lightblue")
# plot regression line
plt.plot([min_x2, max_x2], [m2*min_x2+b2, m2*max_x2+b2],
         marker='o', color='orange')

plt.show()
