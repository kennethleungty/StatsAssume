# ==========================
# Module: Diagnostic Plots
# Author: Kenneth Leung
# Last Modified: 06 Jan 2022
# ==========================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.tsa.api as smt
import warnings

from .utils import display_base64_plot
warnings.filterwarnings("ignore")


# ---------------------
#   Homoscedasticity
# ---------------------
def plot_residual_fit(fitted: pd.Series,
                      residuals: pd.Series,
                      check_type: str,
                      batch_size: int = 10):
    """Generate and display the regression residual plot (fitted vs residuals)

    Args:
        fitted (pd.Series): Fitted (aka predicted) values from model
        residuals (pd.Series): Residual values from model
        check_type (str): Set the residual plot layout specific to the assumption check (i.e. homoscedasticity or linearity)
        batch_size (int, optional): Number of data points used to compute each quantile point. Defaults to 10.

    Returns:
        base64 object: Encoded image of residual plot
    """

    sns.set_style('white')  # Define seaborn layout theme
    upper_quantile_value, lower_quantile_value = 80, 20  # Set quantile ranges for upper and lower quantile lines

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.set(xlabel='Fitted', ylabel='Residual')

    # Scatter plot of fitted (x axis) vs residuals (y axis)
    plt.scatter(fitted,
                residuals,
                color='gray',
                alpha=0.6)

    # Show horizontal dotted line at y=0
    plt.axhline(y=0, color='black', linestyle='dotted')

    # Display different types of lines based on whether it is homoscedasticity or linearity check
    if check_type == 'linearity':
        reg_line, outer_quantiles = True, False
    elif check_type == 'homosced':
        reg_line, outer_quantiles = False, True
    else:
        reg_line, outer_quantiles = True, True

    if reg_line:
        sns.regplot(x=fitted,
                    y=residuals,
                    lowess=True,
                    ax=ax,
                    scatter=False,
                    line_kws={'color': 'red'})

    if outer_quantiles:
        resid_fit_df = pd.concat([fitted, residuals], axis=1)
        resid_fit_df.columns = ['fitted', 'residuals']
        resid_fit_df.sort_values(by='fitted', inplace=True)
        resid_fit_df.reset_index(drop=True, inplace=True)

        quantile_df = pd.DataFrame()
        indices = resid_fit_df.index.tolist()

        # Generate data points to plot quantile lines
        for i in range(0, len(indices), batch_size):
            index_array = indices[i:i + batch_size]
            mid_index = index_array[len(index_array) // 2]
            fitted_mid_value = resid_fit_df['fitted'].iloc[mid_index]
            resid_mid_value = resid_fit_df['residuals'].iloc[mid_index]
            resid_array = resid_fit_df['residuals'].iloc[index_array].values.tolist()
            upper_quantile = np.percentile(resid_array, upper_quantile_value)
            lower_quantile = np.percentile(resid_array, lower_quantile_value)

            resid_dict = {'fitted': fitted_mid_value,
                          'residual': resid_mid_value,
                          'lower_quantile': lower_quantile,
                          'upper_quantile': upper_quantile}

            quantile_df = quantile_df.append(resid_dict, ignore_index=True)

        sns.regplot(x=quantile_df['fitted'].values,
                    y=quantile_df['upper_quantile'].values,
                    lowess=True,
                    ax=ax,
                    scatter=False,
                    line_kws={'color': '#0171C0'})

        sns.regplot(x=quantile_df['fitted'].values,
                    y=quantile_df['lower_quantile'].values,
                    lowess=True,
                    ax=ax,
                    scatter=False,
                    line_kws={'color': '#0171C0'})

    # Save plot as base64 image object for display
    output_plot = display_base64_plot(fig)

    return output_plot


# ---------------------
#    Independence
# ---------------------
def plot_acf(residuals: pd.Series,
             alpha: float = 0.05):
    """Generate and display Auto-Correlation Function (ACF) plot

    Args:
        residuals (pd.Series): Residual values from model
        alpha (float, optional): The level for obtaining the confidence intervals.
            For e.g.,if alpha=0.05, 95% confidence intervals are returned.
            Defaults to 0.05.

    Returns:
        base64 object: Encoded image of ACF plot
    """

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    smt.graphics.plot_acf(residuals, alpha=alpha, ax=ax)

    # Save plot as base64 image object for display
    output_plot = display_base64_plot(fig)

    return output_plot


# ---------------------
#      Linearity
# ---------------------
def plot_pairplot(df: pd.DataFrame,  # Main dataframe
                  target: str,
                  hide_categorical: bool = True,
                  reg_line: bool = False):
    """Generate and display pairplot for visualization of pair-wise linear relationships

    Args:
        df (pd.DataFrame): Dataframe of pre-processed data containing predictors and target variables
        hide_categorical (bool, optional): Hide the categorical variables from being displayed
            in pairplots. Defaults to True.
        reg_line (bool, optional): Whether to include regression lines in the pairplots. Defaults to False.

    Returns:
        base64 object: Encoded image of pair-plots
    """

    if hide_categorical:
        X_cols = [col for col in df.columns.tolist() if col != target]
        bool_cols = [col for col in df if np.isin(df[col].dropna().unique(), [0, 1]).all()]
        X_cols = [item for item in X_cols if item not in bool_cols]

    if reg_line:
        plot_kind = 'reg'  # Show regression line
    else:
        plot_kind = 'scatter'  # Show scatter points without regression line

    pairplot = sns.pairplot(data=df,
                            y_vars=target,
                            x_vars=X_cols,
                            aspect=0.9,
                            kind=plot_kind)

    fig = pairplot.fig

    # Save plot as base64 image object for display
    output_plot = display_base64_plot(fig)

    return output_plot


# ---------------------
#   Multicollinearity
# ---------------------
def plot_corr_heatmap(X: pd.DataFrame,
                      corner: bool,
                      cmap: str = "YlGnBu",
                      axes_style: str = 'white'):
    """Generate and display correlation heatmap to assess correlation amongst variables

    Args:
        X (pd.DataFrame): Dataframe containing only predictor variables (i.e. exclude target variable)
        corner (bool): Display diagonal heatmap (as opposed to standard square heatmap)
        cmap (str, optional): Colour map of correlation heatmap. Defaults to "YlGnBu".
        axes_style (str, optional): Layout style of heatmap plot axes. Defaults to 'white'.

    Returns:
        base64 object: Encoded image of ACF plot
    """

    # Generate correlation values
    corrMatrix = X.corr()
    fig, ax = plt.subplots(figsize=(7, 7))
    if corner is False:
        sns.heatmap(corrMatrix,
                    annot=True,
                    square=True,
                    cmap=cmap)
    else:
        mask = np.zeros_like(corrMatrix)
        mask[np.triu_indices_from(mask)] = True

        with sns.axes_style(axes_style):
            sns.heatmap(corrMatrix,
                        mask=mask,
                        annot=True,
                        vmax=.3,
                        square=True,
                        cmap=cmap)

    # Save plot as base64 image object for display
    output_plot = display_base64_plot(fig)

    return output_plot


# ---------------------
#      Normality
# ---------------------
def plot_qq(residuals: pd.Series):
    """Generate and display Quantile-Quantile (QQ) plot

    Args:
        residuals (pd.Series): Residual values from model

    Returns:
        base64 object: Encoded image of QQ plot
    """

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    fig = sm.ProbPlot(residuals).qqplot(line='s',
                                        ax=ax,
                                        marker='.',
                                        markersize='11',
                                        markerfacecolor='gray',
                                        markeredgecolor='gray',
                                        alpha=0.8)

    # Save plot as base64 image object for display
    output_plot = display_base64_plot(fig)

    return output_plot


def plot_residual_histogram(residuals: pd.Series):
    """Generate and display histogram of residuals

    Args:
        residuals (pd.Series): Residual values from model

    Returns:
        base64 object: Encoded image of residual histogram
    """
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    sns.histplot(residuals,
                 kde=True,
                 ax=ax)

    # Save plot as base64 image object for display
    output_plot = display_base64_plot(fig)

    return output_plot


# ---------------------
#      Outliers
# ---------------------
# def check_outliers(results,
#                    residuals):

#     # Get influence measures
#     influence = results.get_influence()

#     # Obtain summary df of influence measures
#     summary_df = influence.summary_frame()

#     # # Filter summary df to Cook distance
#     cook_df = summary_df.loc[:,['cooks_d']]

#     # Append absolute standardized residual values
#     cook_df['std_resid'] = stats.zscore(results.resid_pearson)
#     cook_df['std_resid'] = cook_df.loc[:,'std_resid'].apply(lambda x: np.abs(x))

#     # Sort by Cook's Distance
#     cook_df.sort_values("cooks_d", ascending=False, inplace=True)

#     # Set Cook's distance threshold
#     cook_threshold = round(4 / len(residuals),3)

#     print(f"Threshold for Cook's Distance = {cook_threshold}")
#     print(f"Displaying Top 5 observations based on Cook's Distance")

#     # Plot influence measures (Cook's distance)
#     fig = influence.plot_index(y_var="cooks", threshold=cook_threshold)
#     fig.tight_layout(pad=1)
#     plt.axhline(y=cook_threshold, ls="--", color='red')
#     plt.show()
