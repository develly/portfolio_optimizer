import numpy as np
from typing import List
from scipy.optimize import minimize

TOLERANCE = 1e-20


def get_weights(num_of_asset: int):
    # Equal weight example.
    weight = 1 / num_of_asset
    weights = np.repeat(weight, num_of_asset)
    return weights


def get_covariances(data):
    # Calculate covariance matrix.
    covariance = data.cov()
    return covariance


def _get_risk_contribution(weights, covariance):
    # Optional: convert dataframe to numpy array.
    covariance = covariance.to_numpy()
    # Convert 1d array to 2d array (n x 1).
    weights = weights.reshape(-1, 1)
    # Calculate portfolio variance.
    variance = weights.T @ covariance @ weights
    # Calculate portfolio sigma.
    sigma = np.sqrt(variance)
    # Calculate mrc.
    mrc = 1 / sigma * (covariance @ weights)
    # Calculate rc.
    rc = np.multiply(weights, mrc)
    # Normalize.
    rc = rc / sum(rc)
    return rc


def _get_error(weights, covariance):
    # Get rc.
    rc_matrix = _get_risk_contribution(weights, covariance)
    # Calculate error.
    error = np.sum(np.square(rc_matrix - rc_matrix.T))
    return error


def _get_opt_weights(covariance: List[float]):
    # Constraints: sum of weights is 1, weight is more than 0.
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}, {'type': 'ineq', 'fun': lambda x: x})
    # Setting max iteration number.
    options = {'maxiter': 800}
    # Get initial weights (Equal weights).
    initial_weights = get_weights(len(covariance))
    # Optimisation process in scipy.
    optimize_result = minimize(fun=_get_error,
                               x0=initial_weights,
                               args=covariance,
                               method='SLSQP',
                               constraints=constraints,
                               tol=TOLERANCE,
                               options=options)
    # Recover the weights from the optimised object.
    weights = optimize_result.x
    # It returns the optimised weights.
    return weights


if __name__ == "__main__":
    from pandas_datareader import data
    import pandas as pd

    # Set date.
    start_date = '2018-01-01'
    end_date = '2021-10-31'
    # Load data.
    google_data = data.DataReader('GOOGL', 'yahoo', start_date, end_date)
    apple_data = data.DataReader('AAPL', 'yahoo', start_date, end_date)
    asml_data = data.DataReader('ASML', 'yahoo', start_date, end_date)
    # Resample.
    google_data = google_data.resample('M').last()
    apple_data = apple_data.resample('M').last()
    asml_data = asml_data.resample('M').last()
    # Calculate returns.
    returns_of_google = google_data['Adj Close'].pct_change()
    returns_of_apple = apple_data['Adj Close'].pct_change()
    returns_of_asml = asml_data['Adj Close'].pct_change()
    # Concat series.
    data = pd.concat([returns_of_google, returns_of_apple, returns_of_asml], axis=1)
    # Rename columns.
    data.columns = ['GOOGL', 'AAPL', 'ASML']
    data = data.dropna()

    # Get covariance.
    covariance_matrix = get_covariances(data)
    # Get optimum weights.
    weight_matrix = _get_opt_weights(covariance_matrix)

    print(weight_matrix)
