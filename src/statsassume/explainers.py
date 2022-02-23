# ===========================================
# Module: Explanations of Assumption Checks
# Author: Kenneth Leung
# Last Modified: 22 Feb 2022
# ===========================================

# ---------------------------------
#   Overview - Linear Regression
# ----------------------------------
explain_description_linear_regression = """
There are a number of assumptions that justify the use of linear regression models for purposes \
of inference or prediction.

[1] Linearity of relationship between dependent and independent variables
[2] Statistical independence of errors (in particular, no correlation between consecutive \
errors (aka autocorrelation) for time series data)
[3] Homoscedasticity (constant variance) of errors
[4] Normality of error distribution
[5] No multicollinearity between independent variables

If any of the assumptions is violated, then the forecasts, confidence intervals, and scientific \
insights yielded by a regression model may be (at best) inefficient or (at worst) seriously biased \
or misleading.
"""

explain_solution_linear_regression = """
The best way to assess whether the dataset meets the assumptions of linear regression is to \
perform a series of assumption checks on the data.

StatsAssume simplifies the process of assumption checks by automatically running the statistical \
tests and generating visual plots for easy interpretation.

The results and information of each assumption check can be found in the Tabs above. Within each \
tab, there are also suggested strategies for handling the assumptions which have been violated.
"""

# ---------------------
#   Homoscedasticity
# ---------------------
explain_description_homosced = """
The variance of the residual errors should be constant across all values of the independent \
variables. Violations of homoscedasticity make it difficult to gauge the true standard \
deviation of the forecast errors, usually resulting in confidence intervals that are too \
wide or too narrow. This violation may also have the effect of giving too much weight to \
a small subset of the data (where error variance is largest) when estimating coefficients.
"""

explain_solution_homosced = """
If the dependent variable is strictly positive and if the residual-versus-predicted plot \
shows that the size of the errors is proportional to the size of the predictions (i.e., \
if errors seem consistent in percentage rather than absolute terms), a log transformation \
applied to the dependent variable may be appropriate. Heteroscedasticity can also be a \
byproduct of a significant violation of the linearity and/or independence assumptions, \
in which case it may also be fixed as a byproduct of fixing those problem.
"""

explain_plot_residual_homosced = """
The points and reference line in the residual plot should be horizontal, and should NOT be systematically getting larger or smaller \
in one direction by a significant amount (i.e., funnel shape).
"""

# ---------------------
#    Independence
# ---------------------
explain_description_independence = """
Residuals should be statistically independent of each other i.e., no autocorrelation \
(i.e., no correlation between consecutive errors or errors separated by some other \
number of periods). If in fact there is correlation among the error terms, then the \
estimated standard errors will tend to underestimate the true standard errors. As a \
result, confidence and prediction intervals will be narrower than they should be, and \
we may have an unwarranted sense of confidence in our model.

For example, a 95 percent confidence interval may in reality have a much lower \
probability than 0.95 of containing the true value of the parameter. In addition, \
pvalues will be lower than they should be, causing us to erroneously conclude that \
a parameter is statistically significant.

Autocorrelation is sometimes due to a violation of the linearity assumption. \
Autocorrelation also means that there is room for improvement in the model, \
and extreme autocorrelation is often a symptom of a badly mis-specified model.
"""

explain_solution_independence = """
For non-time-series models, resolve (if any) the violation of linearity assumption \
or bias that is explainable by omitted variables (e.g., interaction terms or dummies \
for identifiable conditions).

For time-series models, consider adding lags of the dependent variable and/or lags \
of some of the independent variables for minor cases of positive autocorrelation.
"""

explain_plot_acf = """
Most of the residual autocorrelation points should ideally fall randomly and \
symmetrically around zero and within the 95 percent (blue-coloured) confidence bands.
"""

# ---------------------
#      Linearity
# ---------------------
explain_description_linearity = """
There should be a linear relationship between dependent and independent variables. \
A linear relationship suggests that a change in Y due to one unit change in X \
is constant, regardless of the value of X.

If you fit a linear model to data which are nonlinearly or nonadditively related, \
your predictions are likely to be flawed, especially when you extrapolate beyond \
the range of the sample data.
"""

explain_solution_linearity = """
Consider applying a non-linear transformation to the dependent and/or independent variables \
as deemed appropriate and logical. For example, if the data are strictly positive, log \
transformation is an option. If a log transformation is applied to the dependent variable \
only, it assumes that it grows (or decays) exponentially as a function of the independent \
variables. If log transformation is applied to both dependent variable and independent \
variables, it assumes that the effects of independent variables are multiplicative rather \
than additive in their original units.

Another possibility is adding another regressor that is a nonlinear function of \
one of the other variables. If you have regressed Y on X, and the residual-vs-predicted \
plot shows a parabolic curve, then it may make sense to regress Y on both X and X^2.

Finally, it may be that you have overlooked some entirely different independent variable that \
explains the nonlinear pattern or interactions among variables seen in the residual plots. \
In that case, the shape of the pattern, together with economic or physical reasoning, may \
suggest some likely suspects. For example, if the strength of the linear relationship between Y \
and X1 depends on the level of some other variable X2, this could perhaps be addressed by creating \
a new independent variable that is the product of X1 and X2.
"""

explain_plot_residual_linearity = """
The points in the residual plot should be symmetrically distributed around the horizontal reference line \
with a roughly constant spread.
"""

explain_plot_pairplot = """
Each independent variable (x-axis) should have an approximate linear (straight-line) \
relationship with the dependent variable (y-axis).
"""

# ---------------------
#   Multicollinearity
# ---------------------
explain_description_multicollinearity = """
Independent variables should not be correlated with each other, meaning that \
there should be an absence of multicollinearity. When independent variables \
are correlated, it means that changes in one independent variable are associated \
with shifts in another independent variable. The stronger the correlation, the \
more difficult it becomes for the model to estimate the relationship between \
each independent variable and the dependent variable since the independent \
variables will tend to change in unison.

Multicollinearity reduces the precision of the estimated coefficients (and \
increases standard errors of estimates), which thus weakens the statistical \
power of your regression model. As such, it reduces the power of the model, \
and one may not be able to trust the p-values to identify independent variables \
that are statistically significant.
"""

explain_solution_multicollinearity = """
Some solutions include remove some of the highly correlated independent \
variables, linearly combining the independent variables (e.g.,adding them \
together) to form a new variable, or perform analyses designed for highly \
correlated variables like principal components analysis (PCA) or partial least \
squares regression.
"""

explain_plot_corrmatrix = """
An element within this heatmap matrix that is large in absolute value indicates \
a pair of highly correlated variables, and therefore suggests a collinearity \
issue in the data.
"""

# ---------------------
#      Normality
# ---------------------
explain_description_normality = """
The residuals must be approximately normally (aka Gaussian) distributed. Violations \
of normality create problems for determining whether model coefficients are significantly \
different from zero and for calculating confidence intervals for predictions. Since  \
parameter estimation is based on minimization of squared error, a few extreme observations \
can exert a disproportionate influence on parameter estimates. If the error distribution \
is significantly non-normal, confidence intervals may be too wide or too narrow.
"""

explain_solution_normality = """
Violations of normality often arise either because (a) distributions of dependent \
and/or independent variables are themselves significantly non-normal, and/or (b) \
the linearity assumption is violated. In such cases, a nonlinear transformation \
(e.g., log transformation) of variables might cure both problems.
"""

explain_plot_qq = """
If the distribution is normal, the points on the QQ plot should fall close to \
the diagonal reference line. An S-shaped pattern of deviations indicates that \
the residuals have excessive kurtosis.
"""

explainer_plot_residual_histogram = """
The histogram plot and kernel density estimation (KDE) curve should be approximately \
bell-shaped and symmetric about the mean.
"""
