# ===============================================
# Module: Dashboard Layout for Linear Regression
# Author: Kenneth Leung
# Last Modified: 02 Jan 2022
# ==============================================
from dash import html, dcc

# Setup HTML layout for linear regression dashboard report
layout_linear_regression = html.Div([
    html.P(dcc.Tabs(id="tabs", value='tab_summary',
                    children=[dcc.Tab(label='Regression Summary',
                                      value='tab_summary',
                                      className='tab_summary'),
                              dcc.Tab(label='Linearity',
                                      value='tab_linearity',
                                      className='tab_linearity'),
                              dcc.Tab(label='Independence',
                                      value='tab_independence',
                                      className='tab_independence'),
                              dcc.Tab(label='Multicollinearity',
                                      value='tab_multicollinearity',
                                      className='tab_multicollinearity'),
                              dcc.Tab(label='Normality',
                                      value='tab_normality',
                                      className='tab_normality'),
                              dcc.Tab(label='Homoscedasticity',
                                      value='tab_homosced',
                                      className='tab_homosced'),
                              ],
                    colors={"border": "white",
                            "primary": "gold",
                            "background": "#F7F7F7"
                            },
                    style={'font-size': '16px',
                           'text-align': 'center',
                           'border-width': '4px',
                           'padding': '0px 0px 0px 0px'
                           }
                    )),
    html.Div(id='tab-content'),
])
