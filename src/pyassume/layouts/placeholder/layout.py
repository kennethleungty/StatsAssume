# ===============================================
# Module: Dashboard Layout (Placeholder)
# Author: Kenneth Leung
# Last Modified: 13 Feb 2022
# ==============================================
from dash import html, dcc

# Setup HTML layout for dashboard report
layout_placeholder = html.Div([
    html.P(dcc.Tabs(id="tabs", value='tab_summary',
                    children=[dcc.Tab(label='Coming Soon!',
                                      value='tab_summary',
                                      className='tab_summary')
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
