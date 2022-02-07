<h2 align="center"><img src="https://raw.githubusercontent.com/kennethleungty/pyassume/main/media/logo_v1.png" alt="PyAssume" width="200"></h2>
<h3 align="center">Automated Assumption Checks for Regression Models</h3>

<p align="center">
  <a href="https://img.shields.io/badge/Build-Passing-green"><img src="https://img.shields.io/badge/Build-Passing-green?style=for-the-badge"></a>
  <!-- <a href="#"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/kennethleungty/pyassume/main_workflow?style=for-the-badge"></a>  -->
  <a href="#"><img alt="Codecov" src="https://img.shields.io/codecov/c/github/kennethleungty/pyassume?label=CODECOV&style=for-the-badge&token=4RJ4QXIHMH"></a> 
  <a href="#"><img src="https://img.shields.io/badge/Python-v3.7+-blue.svg?style=for-the-badge"></a>
  <a href="#"><img alt="PyPI" src="https://img.shields.io/pypi/v/pyassume?style=for-the-badge"></a>
  <a href="https://img.shields.io/badge/License-MIT-blue.svg"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#download">Download</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#motivation">Motivation</a> •
  <a href="#credits">Credits</a> •
  <a href="#additional-info">Additional Information</a>
</p>

## Features
PyAssume automates the assumption checks of regression models (e.g., linear and logistic regression) on your data and displays the results in a beautiful dashboard. 

This lets you easily verify whether regression modeling is justified and if the model output can be interpreted correctly.

> GIF coming soon!

- Automatically detects regression task (and relevant assumption checks) based on `target` variable.

- Automatically executes relevant statistical tests and visual plots for all relevant assumption checks.

- Generates clear visual output of results in an elegant dashboard (built on [Jupyter-Dash](https://github.com/plotly/jupyter-dash)).

- Automatically one-hot encodes categorical variables for successful regression modelling (unless manually specified otherwise).

- Displays useful information on assumption check concepts and possible solutions to violations.

<br/>

## Download
```bash
pip install pyassume
```
<br/>

## How to Use

### Quickstart
```bash
from pyassume import Check
from pyassume.datasets import load_data

df = load_data('Fish_processed')  # Get toy dataset (pre-processed)

assume = Check(df, target='Weight')  # Initiate Check class and define target variable
assume.report()  # Run assumption checks and generate dashboard report
```

Note: Dataset should ideally be pre-processed before assumption checks.  

<br/>

### Comprehensive Use
- While basic pre-processing should ideally be performed first, PyAssume comes with automatic encoding of categorical variables so that we can quickly commence modelling and assumption checks
- Here's a look at how to put the `Check` class (core object of PyAssume) to its best use:

```bash
assume = Check(df=df, 
               target='Weight',
               task='linear regression',
               predictors=['Height', 'Width', 'Length1', 'Species'],
               keep=True,
               categorical_features=['Species'],
               categorical_encoding='ohe',
               mode='inline')
```

#### Arguments
- `df`: 
- `target`: 
- `task`: 
- `predictors`: 
- `keep`: 
- `categorical_features`: 
- `categorical_encoding`: 
- `mode`: 

#### Notes
- Only `df` and `target` arguments are compulsory

<br/>

## Motivation
- Tedious to do assumption checks manually
- Lack of rigour and consistency in sources and notebooks online

<br/>

<!-- ## Credits
- [Kenneth Leung](https://github.com/kennethleungty)
- Contributor 2
- Contributor 3
- Contributor 4

<br/> -->

## Contributing
1. Have a look at the existing [Issues](https://github.com/kennethleungty/pyassume/issues) and [Pull Requests](https://github.com/kennethleungty/pyassume/pulls) that you would like to help with. 
2. Clone repo and create a new branch: `$ git checkout https://github.com/kennethleungty/pyassume -b name_of_new_branch`.
3. Make changes and test
4. Submit Pull Request with comprehensive description of changes

If you would like to request a feature or report a bug, please [create a GitHub Issue](https://github.com/kennethleungty/pyassume/issues) using one of the templates provided.

[See full contribution guide →](https://github.com/kennethleungty/pyassume/blob/main/CONTRIBUTING.md)

<br/>

## In the Works
- Assumption checks for Logistic Regression (meanwhile, have a look at this [article on logistic regression assumptions](https://towardsdatascience.com/assumptions-of-logistic-regression-clearly-explained-44d85a22b290))