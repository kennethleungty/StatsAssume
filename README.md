<h2 align="center"><img src="https://raw.githubusercontent.com/kennethleungty/statsassume/main/media/logo_v1.png" alt="StatsAssume" width="300"></h2>
<h3 align="center">Automating Assumption Checks for Regression Models</h3>


<p align="center">
  <a href="https://img.shields.io/badge/Build-Passing-green"><img src="https://img.shields.io/badge/Build-Passing-green?style=for-the-badge"></a>
  <!-- <a href="#"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/kennethleungty/statsassume/main_workflow?style=for-the-badge"></a>  -->
  <!-- <a href="#"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/kennethleungty/statsassume?label=CODECOV&style=for-the-badge&token=4RJ4QXIHMH"></a>  -->
  <a href="#"><img src="https://img.shields.io/badge/Python-v3.7+-blue.svg?style=for-the-badge"></a>
  <a href="#"><img alt="PyPI" src="https://img.shields.io/pypi/v/statsassume?style=for-the-badge"></a>
  <a href="https://img.shields.io/badge/License-MIT-blue.svg"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#download">Download</a> •
  <a href="#usage">Usage</a> •
  <a href="#motivation">Motivation</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#upcoming">Upcoming</a>
</p>

## Features
StatsAssume automates the assumption checks of regression models (e.g., linear and logistic regression) on your data and displays the results in an elegant dashboard. 

<img src="https://raw.githubusercontent.com/kennethleungty/statsassume/main/media/demo.gif"/>

- Automatically detects regression task (and relevant assumption checks) based on `target` variable.

- Automatically executes statistical tests and visual plots for all relevant assumption checks.

- Generates clear visual output of results in a beautiful dashboard (built on [Jupyter-Dash](https://github.com/plotly/jupyter-dash)).

- Automatically one-hot encodes categorical variables for successful regression modelling (unless manually specified otherwise).

- Displays insightful information on assumption concepts and (possible) solutions to violations.

## Download
```bash
pip install statsassume
```

## Usage

### Quickstart
```bash
from statsassume import Check
from statsassume.datasets import load_data

df = load_data('Fish_processed')  # Get toy dataset (pre-processed)

assume = Check(df, target='Weight')  # Initiate Check class and define target variable
assume.report()  # Run assumption checks and generate dashboard report
```

Note: Dataset should ideally be pre-processed before running assumption checks.  


### Comprehensive Usage
- While pre-processing should ideally be performed prior, StatsAssume comes with automatic encoding of categorical variables so that we can quickly commence model runs and assumption checks
- Here's how to put the `Check` class (core object of StatsAssume) to its best use:

```bash
df = load_data('Fish')  # Get toy dataset (raw)

assume = Check(df=df, 
               target='Weight',
               task='linear regression',
               predictors=['Height', 'Width', 'Length1', 'Species'],
               keep=True,
               categorical_features=['Species'],
               categorical_encoder='ohe',
               mode='inline')
```
#### Attributes
- `df`: pd.DataFrame
<br> Dataset (in pandas DataFrame format)

- `target`: str
<br> Column name of target (dependent) variable

- `task`: str 
<br> Type of regression task to be performed. Options include: ***'linear regression'***(More tasks to come soon). If None specified, task will be automatically determined based on `target` variable. 

- `predictors`: list
<br> List of column names of predictor (independent) features. If None specified, all columns other than `target` will be regarded as predictors

- `keep`: bool
<br> If ***True***, variables in `predictors` list will be kept as predictor variables, and other non-target variables will be dropped. If ***False***, variables in `predictors` list will be dropped, and other non-target variables will be retained. Default is ***True***.

- `categorical_features`: list
<br> List of column names deemed categorical, so that appropriate encoding can be performed. If None specified, the categorical variables will be automatically detected and encoded into numerical format for regression modelling. Default is ***None***.

- `categorical_encoding`: str
<br> Type of encoding technique to be performed on categorical variables. Options include: ***ohe*** (i.e. one-hot encoding) and ***ord*** (i.e. ordinal encoding). Default is ***ohe***.

- `mode`: str
<br> Type of display for dashboard report. Options include ***inline*** (displayed as output directly in Jupyter notebook), ***external*** (displayed in a new full-screen browser tab), or ***jupyterlab*** (displayed in separate tab right inside JupyterLab). Default is ***inline***.

#### Notes
- Only `df` and `target` attributes are compulsory

## Motivation
- Tedious to perform assumption checks manually
- Lack of rigour and consistency in references and notebooks online

<!-- ## Credits
- [Kenneth Leung](https://github.com/kennethleungty)
- Contributor 2
- Contributor 3
- Contributor 4
 -->

## Contributing
1. Have a look at the existing [Issues](https://github.com/kennethleungty/statsassume/issues) and [Pull Requests](https://github.com/kennethleungty/statsassume/pulls) that you would like to help with. 
2. Clone repo and create a new branch: `$ git checkout https://github.com/kennethleungty/statsassume -b name_of_new_branch`.
3. Make changes and test
4. Submit **Pull Request** with comprehensive description of changes

If you would like to request a feature or report a bug, please [create a GitHub Issue](https://github.com/kennethleungty/statsassume/issues) using one of the templates provided.

[See full contribution guide →](https://github.com/kennethleungty/statsassume/blob/main/CONTRIBUTING.md)

## Upcoming
- Assumption checks for Logistic Regression (meanwhile, take a look at this [article on logistic regression assumptions](https://towardsdatascience.com/assumptions-of-logistic-regression-clearly-explained-44d85a22b290))