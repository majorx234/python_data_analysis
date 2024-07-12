import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pymc as pm

df = pd.read_csv("data/boston_house_prices.csv", skiprows=1)
y = df['MEDV']
X = df.loc[:, df.columns != 'MEDV']
labels = X.columns


# classic linear Regression:
scaler = StandardScaler()
X_standardized = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

lr = LinearRegression().fit(X_standardized, y)
r_sq = lr.score(X_standardized, y)

fig, ax = plt.subplots(1,1)
ax.barh(labels, lr.coef_)
ax.set_xlabel("Coefficient value")
ax.set_ylabel("Feature name")
ax.set_title("Linear Regression coefficients", fontsize=14)

# critism: calculate the percentual error:
y_pred = lr.predict(X_standardized)


def mape(y, y_hat):
    """Calculates the Mean Absolute Percentage Error (MAPE)"""
    return np.mean(np.abs(y - y_hat) / y)

def overview_plot(y, y_pred, instance_start=0, instance_end=None):
    if y_pred.ndim > 1:
        comp = pd.DataFrame({"y": y, "y_pred": y_pred.mean(axis=0)})
        comp["bound_5"] = np.nanpercentile(y_pred, 5.0, axis=0)
        comp["bound_10"] = np.nanpercentile(y_pred, 10.0, axis=0)
        comp["bound_20"] = np.nanpercentile(y_pred, 20.0, axis=0)
        comp["bound_80"] = np.nanpercentile(y_pred, 80.0, axis=0)
        comp["bound_90"] = np.nanpercentile(y_pred, 90.0, axis=0)
        comp["bound_95"] = np.nanpercentile(y_pred, 95.0, axis=0)
    else:
        comp = pd.DataFrame({"y": y, "y_pred": y_pred})

    end = comp.shape[0] if instance_end is None else instance_end
    comp_subset = comp.iloc[instance_start:end].copy()
    comp_subset["instance_id"] = comp_subset.index
    plot_width = min(24, end * 0.2)
    fig, ax = plt.subplots(1, 1, figsize=(plot_width, 6))
    if y_pred.ndim > 1:
        ax.vlines(comp_subset.instance_id, comp_subset.bound_5,
                  comp_subset.bound_95, color="orange", alpha=0.3, linewidth=1,
                  zorder=0, label="90 percent")
        ax.vlines(comp_subset.instance_id, comp_subset.bound_10,
                  comp_subset.bound_90, color="orange", alpha=0.2,
                  linewidth=3, zorder=0, label="80 percent")
        ax.vlines(comp_subset.instance_id, comp_subset.bound_20,
                  comp_subset.bound_80, color="orange", alpha=0.2,
                  linewidth=5, zorder=0, label="60 percent")

    ax.scatter(comp_subset.instance_id, comp_subset.y, color="steelblue",
               zorder=1, s=15, label="Actual")
    ax.scatter(comp_subset.instance_id, comp_subset.y_pred, color="orange",
               zorder=1, s=15, label="Prediction")
    ax.vlines(comp_subset.instance_id, comp_subset.y, comp_subset.y_pred,
              linestyle="--", color="black", linewidth=1, zorder=0, alpha=0.3)
    ax.set_xlabel("Instance IDs")
    ax.set_ylabel("Target value (price)")
    ax.set_title("Overview of instances", fontsize=14)
    ax.legend()
    return ax


def uncertainty_plot(y, y_pred, instance_start=0, instance_end=None):
    comp = pd.DataFrame({"y": y, "y_pred": y_pred.mean(axis=0)})
    comp["uncertainty"] = y_pred.std(axis=0)

    end = comp.shape[0] if instance_end is None else instance_end
    comp_subset = comp.iloc[instance_start:end].copy()
    comp_subset["instance_id"] = comp_subset.index
    plot_width = min(24, end * 0.2)
    fig, ax = plt.subplots(1, 1, figsize=(plot_width, 6))

    ax.bar(comp_subset.instance_id, comp_subset.uncertainty, color="steelblue",
           zorder=1, label="Uncertainty")
    ax.set_xlabel("Instance IDs")
    ax.set_ylabel("Uncertainty")
    ax.set_title("Overview of instances", fontsize=14)
    return ax


print("MAPE: %f" % mape(y, y_pred))
overview_plot(y, y_pred, 0, 50);
uncertainty_plot(y, y_pred, 0, 50);


# 2nd part bayesian_linear_regression
model = pm.Model()
with model:
    sigma = pm.HalfCauchy('sigma', beta=10, initval=1.)
    intercept = pm.Normal('Intercept', 0, sigma=20)

    weights = intercept

    for c in X_standardized.columns:
        weights += pm.Normal(c, mu=0, sigma=1) * X_standardized[c]

    y_hat = pm.Normal('y_hat', mu=weights, sigma=sigma, observed=y)

with model:
    step = pm.Metropolis()
    trace = pm.sample(9000, step=step)
    burned_trace = trace.sample_stats["accept"][6000:]

y_pred_samples = pm.sample_prior_predictive(burned_trace, model=model, samples=506)
y_pred = y_pred_samples.prior_predictive["y_hat"].mean(axis=0)
print("MAPE: %.4f" % mape(y, y_pred))
overview_plot(y, y_pred)
overview_plot(y, y_pred, 0, 50)
uncertainty_plot(y, y_pred)
plt.show()
