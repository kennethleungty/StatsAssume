# ==========================
# Module: Regression Tasks
# Author: Kenneth Leung
# Last Modified: 22 Feb 2022
# ==========================
import pandas as pd
import statsmodels.api as sm
# from statsmodels.genmod.generalized_linear_model import GLM
# from statsmodels.genmod import families


def task_linear_regression(y: pd.Series,
                           X: pd.DataFrame):
    """Run linear regression task (ordinary least squares) with statsmodel library

    Args:
        y (pd.Series): Series of target variable
        X (pd.DataFrame): DataFrame of predictor variables

    Returns:
        Returns the regression model residuals, fitted values, and
        the OLS regression summary table
    """

    model = sm.OLS(y, X)
    results = model.fit()
    residuals = results.resid
    fitted = results.fittedvalues
    summary = results.summary()

    return residuals, fitted, summary


# # Binary Logistic Regression Assumption Checks - COMING SOON
# def task_binary_logistic_regression(y: pd.Series,
#                                     X: pd.DataFrame,
#                                     task_summary: bool = True):
#     model = GLM(y, X, family=families.Binomial())
#     results = model.fit()
#     summary = results.summary()

#     return results, summary


# # Multinomial Logistic Regression Assumption Checks - COMING SOON
# def task_multinomial_logistic_regression(y: pd.Series,
#                                          X: pd.DataFrame):
#     # model = GLM(y, X, family=families.Binomial()) # To amend to MN logit
#     print('Multinomial Logistic Regression Assumption Checks - COMING SOON')
