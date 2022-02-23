# ===========================
# Module: Statistical Tests
# Author: Kenneth Leung
# Last Modified: 12 Jan 2022
# ===========================
import pandas as pd
import statsmodels.stats.diagnostic as smd
import statsmodels.stats.stattools as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
import scipy.stats as stats
import warnings
from .utils import _convert_stat_table_to_dashtable

warnings.filterwarnings("ignore")


# ---------------------
#   Homoscedasticity
# ---------------------
def _get_interpretation_homosced(test_name: str,
                                 pvalue: float,
                                 sig_level: float):
    """Displays p-value of the specific homoscedasticity test, along with the test result interpretation

    Args:
        test_name (str): Name of statistical test
        pvalue (float): Value of the p-value
        sig_level (float): Significance level of statistical test

    Returns:
        str: Interpretation of homoscedasticity statistical test
    """

    if pvalue < sig_level:
        interpretation = f'p-value of {test_name} ({round(pvalue,3)}) is <{sig_level}, suggesting that the assumption of homoscedasticity is VIOLATED'
    else:
        interpretation = f'p-value of {test_name} ({round(pvalue,3)}) is ≥{sig_level}, suggesting that the assumption of homoscedasticity is satisfied'

    return interpretation


def stat_breuschpagan(residuals: pd.Series,
                      X_constant: pd.DataFrame,
                      sig_level: float = 0.05):
    """Run Breusch-Pagan test (for homoscedasticity check) and display test results

    Args:
        residuals (pd.Series): Residual values from regression model
        X_constant (pd.DataFrame): Dataframe with predictor variables, and with constant (intercept) included
        sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

    Returns:
        Interpretation (str) and results (HTML table) of Breusch-Pagan test
    """

    test_name = 'Breusch-Pagan Test'
    test_df = pd.DataFrame(smd.het_breuschpagan(residuals, X_constant),
                           columns=['Value'],
                           index=['Lagrange multiplier (LM) statistic',
                                  'LM p-value', 'F statistic', 'F p-value'])
    test_df['Value'] = test_df['Value'].round(decimals=3)
    pvalue = test_df.loc['LM p-value'].values[0]

    # Display results and interpretation
    interpretation = _get_interpretation_homosced(test_name, pvalue, sig_level)

    # Convert pandas df to dash table
    test_df.reset_index(drop=False, inplace=True)
    test_df.columns = ['Parameter', 'Value']
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


def stat_white(residuals: pd.Series,
               X_constant: pd.DataFrame,
               sig_level: float = 0.05):
    """Run White test (for homoscedasticity check) and display test results

    Args:
        residuals (pd.Series): Residual values from regression model
        X_constant (pd.DataFrame): Predictor dataframe with constant (intercept) included
        sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

    Returns:
        Interpretation (str) and results (HTML table) of White test
    """

    test_name = 'White Test'
    test_df = pd.DataFrame(smd.het_white(residuals, X_constant),
                           columns=['Value'],
                           index=['Lagrange multiplier (LM) statistic',
                                  'LM p-value', 'F statistic', 'F p-value'])
    test_df['Value'] = test_df['Value'].round(decimals=3)
    pvalue = test_df.loc['LM p-value'].values[0]

    # Display results and interpretation
    interpretation = _get_interpretation_homosced(test_name, pvalue, sig_level)

    # Convert pandas df to dash table
    test_df.reset_index(drop=False, inplace=True)
    test_df.columns = ['Parameter', 'Value']
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


def stat_gq(residuals: pd.Series,
            X_constant: pd.DataFrame,
            sig_level: float = 0.05):
    """Run Goldfeld-Quandt test (for homoscedasticity check) and display test results

    Args:
        residuals (pd.Series): Residual values from regression model
        X_constant (pd.DataFrame): Predictor dataframe with constant (intercept) included
        sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

    Returns:
        Interpretation (str) and results (HTML table) of Goldfeld-Quandt test
    """

    test_name = 'Goldfeld-Quandt Test'
    test_df = pd.DataFrame(smd.het_goldfeldquandt(residuals, X_constant)[:-1],
                           columns=['value'],
                           index=['F statistic', 'F p-value'])
    pvalue = test_df.loc['F p-value'].values[0]

    # Display results and interpretation
    interpretation = _get_interpretation_homosced(test_name, pvalue, sig_level)

    # Convert pandas df to dash table
    test_df.reset_index(drop=False, inplace=True)
    test_df.columns = ['Parameter', 'Value']
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


# -----------------------------------
#     Independence / Autocorrelation
# -----------------------------------
def stat_durbin_watson(residuals: pd.Series):
    """Run Durbin-Watson test (for independence/autocorrelation check) and display test results

    Args:
        residuals (pd.Series): Residual values from regression model

    Returns:
        Interpretation (str) and results (HTML table) of Durbin-Watson test
    """

    test_name = 'Durbin-Watson Test'
    statistic = round(sms.durbin_watson(residuals), 3)
    lower_thresh, ideal, upper_thresh = 1.5, 2, 2.5
    test_df = pd.DataFrame(statistic,
                           columns=['Value'],
                           index=['Durbin-Watson Statistic'])

    # Display interpretation of test result
    if statistic < lower_thresh:
        interpretation = f'The {test_name} statistic of {statistic} is < {lower_thresh}, suggesting POSITIVE autocorrelation of residuals, and that assumption of observation independence is VIOLATED'
    elif statistic > upper_thresh:
        interpretation = f'The {test_name} statistic of {statistic} is > {upper_thresh}, suggesting NEGATIVE autocorrelation of residuals, and that assumption of observation independence is VIOLATED'
    else:
        interpretation = f'The {test_name} statistic of {statistic} is close to the value of {ideal}, suggesting NO autocorrelation of residuals, and that assumption of independence is satisfied'

    # Convert pandas df to dash table
    test_df.reset_index(drop=False, inplace=True)
    test_df.columns = ['Parameter', 'Value']
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


def stat_ljungbox(residuals: pd.Series,
                  sig_level: float = 0.05,
                  lags: int = None,
                  auto_lag: bool = True):
    """Run Ljung-Box test (for independence/autocorrelation check) and display test results

    Args:
        residuals (pd.Series): Residual values from regression model
        sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.
        lags (int, optional): Number of lags to test. Defaults to None.
        auto_lag (bool, optional): Flag indicating whether to automatically determine
            optimal lag length based on threshold of maximum correlation value. Defaults to True

    Returns:
        Interpretation (str) and results (HTML table) of Ljung-Box test
    """

    test_name = 'Ljung-Box Test'
    test_df = smd.acorr_ljungbox(residuals, lags=lags, auto_lag=auto_lag)
    test_df.columns = ['Ljung-Box statistic', 'p-value']
    test_df = test_df.round(3)

    pvalues = test_df['p-value'].values
    min_pvalue = round(float(min(pvalues)), 3)

    if min_pvalue < sig_level:
        interpretation = f'The p-value of {test_name} ({min_pvalue}) is <{sig_level}, suggesting that the assumption of observation independence (aka no autocorrelation) is VIOLATED'
    else:
        interpretation = f'The p-value of {test_name} ({min_pvalue}) is ≥{sig_level}, suggesting that the assumption of observation independence (aka no autocorrelation) is satisfied'

    # Convert pandas df to dash table
    test_df.reset_index(drop=False, inplace=True)
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


# ---------------------
#   Multicollinearity
# ---------------------
def stat_vif(X_constant: pd.DataFrame,
             threshold: int = 10):
    """Calculate Variance Inflation Factor (VIF) values for each variable (for multi-collinearity check). This is done on X_constant,
    where the constant (intercept) is already included in the VIF calculations.

    Args:
        X_constant (pd.DataFrame): Dataframe with predictor variables, and with constant (intercept) included
        threshold (int, optional): Threshold for VIF to indicate multicollinearity. Defaults to 10.

    Returns:
        - pandas.DataFrame: Dataframe containing VIF value for each predictor variable
        - str: Interpretation of VIF values based on threshold
    """

    vif = [variance_inflation_factor(X_constant.values, i) for i in range(X_constant.shape[1])]
    X_cols = [col for col in list(X_constant.columns) if col != 'const']  # Hide const value from table, but VIF calc ALREADY correctly done on X_constant
    test_df = pd.DataFrame({'VIF': vif[1:]}, index=X_cols)
    test_df.sort_values(by='VIF', inplace=True, ascending=False)
    test_df['Below threshold'] = test_df['VIF'].apply(lambda x: u'\u2713' if x < threshold else 'X')
    test_df['VIF'] = test_df['VIF'].round(decimals=1)

    count_below_thresh = (test_df['Below threshold'].values != 'X').sum()
    count_above_thresh = len(test_df) - count_below_thresh
    if count_above_thresh > 0:
        interpretation = f'Given there are {count_above_thresh} features with VIF greater than threshold value of {threshold}, the assumption of no multicollinearity is VIOLATED'
    else:
        interpretation = f'Given zero features with VIF greater than threshold value of {threshold}, the assumption of no multicollinearity is satisfied'

    # Convert pandas df to dash table
    test_df.reset_index(drop=False, inplace=True)
    test_df.columns = ['Feature', 'VIF', 'Below Threshold']
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


# ---------------------
#       Normality
# ---------------------
def _get_interpretation_normality(test_name: str,
                                  pvalue: float,
                                  sig_level: float):
    """Displays p-value of the specific normality test,
    along with test result interpretation

    Args:
        test_name (str): Name of statistical test
        pvalue (float): Value of the p-value
        sig_level (float): Significance level of statistical test

    Returns:
        str: Interpretation of normality statistical test
    """
    if pvalue < sig_level:
        interpretation = f'p-value of {test_name} ({round(pvalue,3)}) is <{sig_level}, suggesting the assumption of residual normality is VIOLATED'
    else:
        interpretation = f'p-value of {test_name} ({round(pvalue,3)}) is ≥{sig_level}, suggesting the assumption of residual normality is satisfied'

    return interpretation


def stat_anderson(residuals: pd.Series,
                  sig_level: float = 0.05):
    """Run Anderson-Darling test (for residual normality check) and display test results

    Args:
        residuals (pd.Series): Residual values from regression model
        sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

    Returns:
        Interpretation (str) and results (HTML table) of Anderson-Darling test
    """

    test_name = 'Anderson-Darling test'
    statistic = stats.anderson(residuals, dist='norm').statistic
    pvalue = round(stats.anderson(residuals, dist='norm').critical_values[2], 3)  # Get 5% critical value (significance level)

    test_df = pd.DataFrame.from_dict({'Anderson-Darling statistic': statistic,
                                     'p-value': pvalue},
                                     orient='index',
                                     columns=['Value'])

    # Display results and interpretation
    interpretation = _get_interpretation_normality(test_name, pvalue, sig_level)

    # Convert pandas df to dash table
    test_df.reset_index(drop=True, inplace=True)
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


def stat_shapiro(residuals: pd.Series,
                 sig_level: float = 0.05):
    """Run Shapiro-Wilk test (for residual normality check) and display test results

    Args:
        residuals (pd.Series): Residual values from regression model
        sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

    Returns:
        Interpretation (str) and results (HTML table) of Shapiro-Wilk test
    """

    test_name = 'Shapiro-Wilk test'
    statistic = stats.shapiro(residuals).statistic
    pvalue = round(stats.shapiro(residuals).pvalue, 3)

    test_df = pd.DataFrame.from_dict({'Shapiro-Wilk statistic': statistic,
                                     'p-value': pvalue},
                                     orient='index',
                                     columns=['Value'])
    test_df['Value'] = test_df['Value'].round(decimals=3)

    # Display results and interpretation
    interpretation = _get_interpretation_normality(test_name, pvalue, sig_level)

    # Convert pandas df to dash table
    test_df.reset_index(drop=False, inplace=True)
    test_df.columns = ['Parameter', 'Value']
    test_table = _convert_stat_table_to_dashtable(test_df)

    return interpretation, test_table


# def stat_lilliefors(residuals: pd.Series,
#                     sig_level: float = 0.05):
#     """Run Lilliefors corrected Kolmogorov-Smirnov test (for residual normality check) and display test results

#     Args:
#         residuals (pd.Series): Residual values from regression model
#         sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

#     Returns:
#         Interpretation (str) and results (HTML table) of Lilliefors corrected Kolmogorov-Smirnov test
#     """

#     test_name = 'Lilliefors corrected Kolmogorov-Smirnov test'
#     statistic = smd.lilliefors(residuals, 'norm', 'table')[0]
#     pvalue = smd.lilliefors(residuals, 'norm', 'table')[1]

#     # Display results and interpretation
#     interpretation = _get_interpretation_normality(test_name, pvalue, sig_level)

#     return interpretation


# def stat_jarque_bera(residuals: pd.Series,
#                      sig_level: float = 0.05):
#     """Run Jarque-Bera test (for residual normality check) and display test results

#     Args:
#         residuals (pd.Series): Residual values from regression model
#         sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

#     Returns:
#         Interpretation (str) and results (HTML table) of Jarque-Bera test
#     """

#     test_name = 'Jarque-Bera test'
#     statistic = stats.jarque_bera(residuals).statistic
#     pvalue = stats.jarque_bera(residuals).pvalue

#     # Display results and interpretation
#     interpretation = _get_interpretation_normality(test_name, pvalue, sig_level)

#     return interpretation


# def stat_ks(residuals: pd.Series,
#             sig_level: float = 0.05):
#     """Run Kolmogorov-Smirnov test (for residual normality check) and display test results

#     Args:
#         residuals (pd.Series): Residual values from regression model
#         sig_level (float, optional): Significance level of statistical test. Defaults to 0.05.

#     Returns:
#         Interpretation (str) and results (HTML table) of Kolmogorov-Smirnov test
#     """

#     test_name = 'Kolmogorov-Smirnov test'
#     statistic = stats.kstest(residuals, 'norm').statistic
#     pvalue = stats.kstest(residuals, 'norm').pvalue

#     # Display results and interpretation
#     interpretation = _get_interpretation_normality(test_name, pvalue, sig_level)

#     return interpretation
