# ========================================
# Module: Dash Tabs for Linear Regression
# Author: Kenneth Leung
# Last Modified: 22 Feb 2022
# =======================================
from dash import html
import pandas as pd
from urllib.request import urlopen

from ...plots import *
from ...stats import *
from ...utils import *
from ...explainers import *

# Define regression task
task = 'linear_regression'


# Define function to retrieve example figures
def _get_example_fig(task: str,
                     check: str):
    """Retrieve base64 encoded file of example figures (for visual plot comparison)

    Args:
        task (str): Name of task (e.g. linear_regression)
        check (str): Name of check (e.g. normality)

    Returns:
        base64 encoded file of png image
    """
    fig_url = f'https://raw.githubusercontent.com/kennethleungty/statsassume/main/figures/{task}'

    return base64.b64encode(urlopen(f'{fig_url}/{check}.png').read())

    # Testing
    # fig_url = 'https://raw.githubusercontent.com/kennethleungty/COVID19-Vaccine-Sentiment-Analysis/main/Images/composite_sentiments_by_max_voting.png'
    # return base64.b64encode(urlopen(f'{fig_url}').read())


def generate_tab_summary(summary,
                         task_type: str):
    """Display OLS regression summary as HTML

    Args:
        summary (statsmodels.iolib.summary.Summary): statsmodel OLS regression summary (comprising 3 tables)
        task_type (str): Type of regression task that was executed

    Returns:
        html.Div: OLS regression summary
    """

    # TODO: Need to adjust this to accomodate logistic regression in the future
    ols_table_1 = summary.tables[0].as_html()
    ols_table_2 = summary.tables[1].as_html()
    ols_table_3 = summary.tables[2].as_html()

    tab_summary = html.Div(children=[
                           display_tab_header(assumption_name='Summary',
                                              assumption_intro='Brief description of regression results'),
                           html.Br(),
                           display_regression_summary('Linear Regression Results',
                                                      ols_table_1,
                                                      ols_table_2,
                                                      ols_table_3),
                           html.Br(),
                           display_logs(),
                           html.Br(),
                           display_assumption_details(explain_description_linear_regression,
                                                      explain_solution_linear_regression)
                           ],
                           style={'text-align': 'center'})

    return tab_summary


def generate_tab_homosced(residuals: pd.Series,
                          fitted: pd.Series,
                          X_constant: pd.DataFrame):
    """Generate and display HTML tab report of homoscedasticity assumption check

    Args:
        residuals (pd.Series): Residual values of regression model
        fitted (pd.Series): Fitted (aka predicted) values from model
        X_constant (pd.DataFrame): Predictor dataframe with constant (intercept) included

    Returns:
        html.Div: Report of homoscedasticity assumption check
    """

    check_type = 'homosced'
    output_plot_residual = plot_residual_fit(residuals, fitted, check_type)
    fig_homosced = _get_example_fig(task, check_type)
    interpretation_bp, table_bp = stat_breuschpagan(residuals, X_constant)
    interpretation_white, table_white = stat_white(residuals, X_constant)
    # output_str_gq = stat_gq(residuals, X_constant)

    tab_homosced = html.Div(style={'text-align': 'center'},
                            children=[
                            display_tab_header(assumption_name='Assumption Check - Homoscedasticity',
                                               assumption_intro='Brief description of specific assumption check'),
                            html.Br(),
                            display_visual_plot(plot_name='Residual Plot',
                                                img_plot=output_plot_residual,
                                                img_examples=f'data:image/png;base64,{fig_homosced.decode()}',
                                                explainer=explain_plot_residual_homosced),
                            html.Br(),
                            display_stat_results(test_name='Breusch-Pagan Test',
                                                 interpretation=interpretation_bp,
                                                 test_table=table_bp),
                            html.Br(),
                            display_stat_results(test_name='White Test',
                                                 interpretation=interpretation_white,
                                                 test_table=table_white),
                            html.Br(),
                            display_assumption_details(explain_description_homosced,
                                                       explain_solution_homosced)
                            ])

    return tab_homosced


def generate_tab_independence(residuals: pd.Series):
    """Generate and display HTML tab report of independence assumption check

        Args:
            residuals (pd.Series): Residual values of regression model

        Returns:
            html.Div: Report of independence assumption check
        """

    check_type = 'independence'
    interpretation_dw, table_dw = stat_durbin_watson(residuals)
    interpretation_lb, table_lb = stat_ljungbox(residuals)
    output_plot_acf = plot_acf(residuals)
    fig_independence = _get_example_fig(task, check_type)

    tab_independence = html.Div(style={'text-align': 'center'},
                                children=[
                                display_tab_header(assumption_name='Assumption Check - Independence',
                                                   assumption_intro='Brief description of specific assumption check'),
                                html.Br(),
                                display_visual_plot(plot_name='Autocorrelation Function (ACF) Plot',
                                                    img_plot=output_plot_acf,
                                                    img_examples=f'data:image/png;base64,{fig_independence.decode()}',
                                                    explainer=explain_plot_acf),
                                html.Br(),
                                display_stat_results(test_name='Durbin-Watson Test',
                                                     interpretation=interpretation_dw,
                                                     test_table=table_dw),
                                html.Br(),
                                display_stat_results(test_name='Ljung-Box Test',
                                                     interpretation=interpretation_lb,
                                                     test_table=table_lb),
                                html.Br(),
                                display_assumption_details(explain_description_independence,
                                                           explain_solution_independence)
                                ])

    return tab_independence


def generate_tab_linearity(df: pd.DataFrame,
                           target: str,
                           residuals: pd.Series,
                           fitted: pd.Series):
    """Generate and display HTML tab report of linearity assumption check

    Args:
        df (pd.DataFrame): Dataframe of pre-processed data containing predictors and target variables
        target (str): Name of target variable
        residuals (pd.Series): Residual values from regression model
        fitted (pd.Series): Fitted (aka predicted) values from model

    Returns:
        html.Div: Report of linearity assumption check
    """

    check_type = 'linearity'
    output_plot_residual = plot_residual_fit(residuals, fitted, check_type)
    fig_linearity = _get_example_fig(task, check_type)
    output_plot_pairplot = plot_pairplot(df, target)

    tab_linearity = html.Div(style={'text-align': 'center'},
                             children=[
                             display_tab_header(assumption_name='Assumption Check - Linearity',
                                                assumption_intro='Brief description of specific assumption check'),
                             html.Br(),
                             display_visual_plot(plot_name='Residual Plot',
                                                 img_plot=output_plot_residual,
                                                 img_examples=f'data:image/png;base64,{fig_linearity.decode()}',
                                                 explainer=explain_plot_residual_linearity),
                             html.Br(),
                             display_visual_plot(plot_name='Pair-Plot',
                                                 img_plot=output_plot_pairplot,
                                                 img_examples='None',
                                                 explainer=explain_plot_pairplot),
                             html.Br(),
                             display_assumption_details(explain_description_linearity,
                                                        explain_solution_linearity)
                             ])

    return tab_linearity


def generate_tab_multicollinearity(X: pd.DataFrame,
                                   X_constant: pd.DataFrame):
    """Generate and display HTML tab report of multi-collinearity assumption check

    Args:
        X (pd.DataFrame): Dataframe with predictor variables (without intercept)
        X_constant (pd.DataFrame): Dataframe with predictor variables, and with constant (intercept) included

    Returns:
        html.Div: Report of multi-collinearity assumption check
    """

    output_plot_corr_heatmap = plot_corr_heatmap(X, corner=True)  # Show corr matrix as corner
    interpretation_vif, table_vif = stat_vif(X_constant)

    tab_multicollinearity = html.Div(style={'text-align': 'center'},
                                     children=[
                                     display_tab_header(assumption_name='Assumption Check - Multicollinearity',
                                                        assumption_intro='Brief description of specific assumption check'),
                                     html.Br(),
                                     display_visual_plot(plot_name='Correlation Matrix',
                                                         img_plot=output_plot_corr_heatmap,
                                                         img_examples='None',
                                                         explainer=explain_plot_corrmatrix),
                                     html.Br(),
                                     display_stat_results(test_name='Variance Inflation Factor (VIF)',
                                                          interpretation=interpretation_vif,
                                                          test_table=table_vif),
                                     html.Br(),
                                     display_assumption_details(explain_description_multicollinearity,
                                                                explain_solution_multicollinearity)
                                     ])

    return tab_multicollinearity


def generate_tab_normality(residuals: pd.Series):
    """Generate and display HTML tab report of residual normality assumption check

    Args:
        residuals (pd.Series): Residual values from regression model

    Returns:
        html.Div: Report of residual normality assumption check
    """
    check_type = 'normality'
    output_plot_residual_histogram = plot_residual_histogram(residuals)
    output_plot_qq = plot_qq(residuals)
    fig_normality = _get_example_fig(task, check_type)
    interpretation_shapiro, table_shapiro = stat_shapiro(residuals)

    # Only showing the main statistical test i.e. Shapiro
    # output_str_anderson = stat_anderson(residuals)
    # output_str_jarque_bera = stat_jarque_bera(residuals)
    # output_str_lilliefors = stat_lilliefors(residuals)

    tab_normality = html.Div(style={'text-align': 'center'},
                             children=[
                             display_tab_header(assumption_name='Assumption Check - Normality',
                                                assumption_intro='Brief description of specific assumption check'
                                                ),
                             html.Br(),
                             display_visual_plot(plot_name='Quantile-Quantile (QQ) Plot',
                                                 img_plot=output_plot_qq,
                                                 img_examples=f'data:image/png;base64,{fig_normality.decode()}',
                                                 explainer=explain_plot_qq
                                                 ),
                             html.Br(),
                             display_visual_plot(plot_name='Histogram of Residuals',
                                                 img_plot=output_plot_residual_histogram,
                                                 img_examples='None',
                                                 explainer=explainer_plot_residual_histogram
                                                 ),
                             html.Br(),
                             display_stat_results(test_name='Shapiro-Wilk Test',
                                                  interpretation=interpretation_shapiro,
                                                  test_table=table_shapiro
                                                  ),
                             html.Br(),
                             display_assumption_details(explain_description_normality,
                                                        explain_solution_normality
                                                        )
                             ])

    return tab_normality
