# ===============================
# Module: Dashboard Report Generation
# Author: Kenneth Leung
# Last Modified: 07 Mar 2022
# ===============================
import sys
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.utils.multiclass import type_of_target
from sklearn.preprocessing import OrdinalEncoder
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import warnings
from .layouts.linear_regression.layout import layout_linear_regression
from .layouts.linear_regression.tabs import *
from .layouts.placeholder.layout import layout_placeholder
from .layouts.placeholder.tabs import *
from .enums import TaskType
from .plots import *
from .stats import *
from .tasks import *
from .logger import logger

sys.path.insert(0, "/layouts")
warnings.filterwarnings("ignore")


@dataclass
class Check:
    df: pd.DataFrame
    target: str
    task: Optional[str] = None
    predictors: Optional[List[str]] = None
    keep: Optional[bool] = True
    categorical_features: Optional[List[str]] = None
    categorical_encoder: Optional[str] = None
    mode: str = 'inline'  # Other options: external, jupyterlab

    """Core object of StatsAssume. Initializes regression modelling, runs relevant assumption checks,
    and returns an output report in the form of a Dash dashboard
    """
    def __post_init__(self):
        pass
        # if os.path.exists(self.output):
        #     raise Exception("Output directory already exists. Please specify another folder name.")
        # os.makedirs(self.output, exist_ok=True)
        # logger.info(f"Output directory: {self.output}")
        # To include output: Optional[str] = 'output' inside parameters if using this function

    def _determine_task_type(self):
        """Sets type of regression task to run.
        If none specified, function will automatically
        infer type of regression based on target variable

        Raises:
            ValueError: If input string is not a valid regression task
            Exception: If target variable is not in the right format (i.e. 1D-array or column vector)
            Exception: If unable to infer type of regression based on target variable

        Returns:
            Type of regression modelling task to be executed
        """
        if self.task is not None:
            if self.task == 'linear regression':
                task_type = TaskType.linear_regression
            elif self.task == 'binary logistic regression':
                task_type = TaskType.binary_logistic_regression
            elif self.task == 'multinomial logistic regression':
                task_type = TaskType.multinomial_logistic_regression
            else:
                raise ValueError('Unable to infer type of regression task. If specifying manually, please choose from the following: \
                    "linear regression", "binary logistic regression" or "multinomial logistic regression"')

            logger.info(f"[+] Executing task type (specified by user): {task_type.name}")

        else:
            # Infer target type
            target_type = type_of_target(self.df[self.target].values)  # Using sklearn.utils.multiclass.type_of_target
            if target_type == "continuous":
                task_type = TaskType.linear_regression
            elif target_type == "binary":
                task_type = TaskType.binary_logistic_regression
            elif target_type == "multiclass":
                task_type = TaskType.multinomial_logistic_regression
            elif (target_type == "continuous-multioutput") or (target_type == "multilabel-indicator"):
                raise Exception('Target needs to be a 1D-array or column vector')
            else:
                raise Exception("Target type not supported. Please provide a Target variable with type compatible with linear or logistic regression")

            logger.info(f"[+] Executing task type (detected automatically): {task_type.name}")

        return task_type

    def _keep_predictors(self):
        """ Keeps or drops variables based on list of variables specified by user

        Returns:
            pd.DataFrame: Output dataframe after keeping/dropping predictor variables
        """
        if self.predictors is not None:
            # Keep defined columns
            if self.keep:
                selected_cols = self.predictors + [self.target]
                df_keep_predictors = self.df[selected_cols]
                logger.info(f'[+] Keep predictor variables specified by user: {selected_cols}')
            # Drop defined columns
            else:
                df_keep_predictors = self.df.drop(self.predictors, axis=1)
                logger.info(f'[+] Drop variables specified by user: {self.predictors}')
        else:
            df_keep_predictors = self.df

        return df_keep_predictors

    def _process_categorical_features(self, df):
        """Transform categorical features (via one-hot or ordinal encoding)
        so that input data can be parsed into statsmodel for modelling

        Args:
            df (pd.DataFrame): DataFrame with defined predictor and target variables
            categorical_features (list): List of features that are of categorical type (Manually defined)

        Raises:
            Exception: If categorical variables remain non-encoded

        Returns:
            pd.DataFrame: Output dataframe after encoding of categorical features
        """
        # Automatically detect categorical features
        categorical_features_auto = []
        features = [col for col in list(df.columns) if col != self.target]
        for col in features:
            if self.df[col].dtype == "object":
                categorical_features_auto.append(col)

        # Categorical features specified by user
        if self.categorical_features is not None:
            # Check whether there are additional categorical features not specified by user:
            categorical_features_diff = list(set(categorical_features_auto) - set(self.categorical_features))
            if len(categorical_features_diff) > 0:
                raise ValueError(f'These categorical features have not been encoded: {categorical_features_diff}')
            else:
                logger.info(f'[+] Categorical features specified by user: {categorical_features_auto}')
                categorical_features = self.categorical_features

        # No categorical features specified by user
        else:
            logger.info(f'[+] Categorical features automatically identified: {categorical_features_auto}')
            categorical_features = categorical_features_auto

        if len(categorical_features) > 0:
            if self.categorical_encoder == 'ohe':
                logger.info('[+] Proceeding with one-hot encoding of categorical features')
                df_encode = self.df.copy()
                for feature in categorical_features:
                    dummies = pd.get_dummies(df_encode[feature],
                                             prefix=feature,
                                             drop_first=True)
                    df_encode = pd.concat([df_encode, dummies], axis=1)
                    df_encode.drop([feature], axis=1, inplace=True)

                logger.info(f'[+] Completed one-hot encoding of categorical features: {categorical_features}')
                return df_encode

            elif self.categorical_encoder == 'ord':  # Ordinal encoding
                df_encode = self.df.copy()
                logger.info('[+] Proceeding with ordinal encoding of categorical features')
                ord_encoder = OrdinalEncoder(handle_unknown="use_encoded_value",
                                             unknown_value=np.nan)
                df_encode[categorical_features] = ord_encoder.fit_transform(df_encode[categorical_features].values)
                logger.info(f'[+] Completed ordinal encoding of categorical features: {categorical_features}')

                return df_encode
            else:
                raise ValueError(f'Please manually encode these categorical features (or use `categorical_encoder`) before continuing: {categorical_features} ')
        else:
            logger.info('[+] No non-encoded categorical features identified. Proceeding with regression')
            return self.df

    def report(self):
        """Run regression modeling and assumption checks, and display output report as JupyterDash dashboard

        Raises:
            Exception: If input string of regression type is not recognized

        Returns:
            JupyterDash dashboard (running on localhost server port 8090)
        """

        task_type = self._determine_task_type()
        df = self._keep_predictors()
        df = self._process_categorical_features(df)

        app = JupyterDash(__name__,
                          external_stylesheets=[dbc.themes.BOOTSTRAP]
                          )

        predictors = [col for col in list(df.columns) if col != self.target]
        X, y = df[predictors], df[self.target]
        X_constant = sm.add_constant(X)  # Add constant value for X

        if task_type == TaskType.linear_regression:
            task_name = 'Linear Regression'
            app.layout = layout_linear_regression
            residuals, fitted, summary_str = task_linear_regression(y, X_constant)

            @app.callback(Output('tab-content', 'children'),
                          [Input('tabs', 'value')])
            def render_content(tab):
                if tab == 'tab_summary':
                    return generate_tab_summary(summary_str, task_name)
                elif tab == 'tab_homosced':
                    return generate_tab_homosced(residuals, fitted, X_constant)
                elif tab == 'tab_independence':
                    return generate_tab_independence(residuals)
                elif tab == 'tab_linearity':
                    return generate_tab_linearity(df, self.target, residuals, fitted)
                elif tab == 'tab_multicollinearity':
                    return generate_tab_multicollinearity(X, X_constant)
                elif tab == 'tab_normality':
                    return generate_tab_normality(residuals)

        elif task_type == TaskType.binary_logistic_regression:
            task_name = 'Binary Logistic Regression'
            # task_binary_logistic_regression(y, X_constant)
            app.layout = layout_placeholder

            @app.callback(Output('tab-content', 'children'),
                          [Input('tabs', 'value')])
            def render_content(tab):
                if tab == 'tab_summary':
                    # Dummy placeholder layout
                    return generate_placeholder_layout(task_name)

        elif task_type == TaskType.multinomial_logistic_regression:
            task_name = 'Multinomial Logistic Regression'
            # task_multinomial_logistic_regression(y, X_constant)
            app.layout = layout_placeholder

            @app.callback(Output('tab-content', 'children'),
                          [Input('tabs', 'value')])
            def render_content(tab):
                if tab == 'tab_summary':
                    # Dummy placeholder layout
                    return generate_placeholder_layout(task_name)

        else:
            raise ValueError('Task type not recognized')

        app.run_server(mode=self.mode, port=8090)
