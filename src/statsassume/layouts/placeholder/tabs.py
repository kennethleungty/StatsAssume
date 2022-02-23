# ========================================
# Module: Dash Tabs (Placeholder)
# Author: Kenneth Leung
# Last Modified: 13 Feb 2022
# =======================================
from dash import html

# Define regression task
# task = 'linear_regression'


def generate_placeholder_layout(task_type: str):
    tab_summary = html.Div(children=[
                           html.Small(f'Successfully detected regression task to be {task_type}. However, \
                                        automated assumption checks for this task is still in the works. \
                                        Follow the PyAssume repo (github.com/kennethleungty/pyassume) \
                                        to stay updated with the latest developments!'),
                           html.Br(),
                           ],
                           style={'text-align': 'center'})

    return tab_summary
