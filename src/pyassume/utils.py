# =================================
# Module: Utils Helper Functions
# Author: Kenneth Leung
# Last Modified: 09 Jan 2022
# =================================
import pandas as pd
import matplotlib.pyplot as plt
from dash import html
import dash_table as dt
import dash_bootstrap_components as dbc
from io import BytesIO
import base64
from typing import Optional

# Styling settings
dt_font_size = 17
dt_font_family = 'Arial'
padding_size = '10px'
center_separator = '2px solid #FFD700'

def display_base64_plot(fig):
    """Convert plot (matplotlib or seaborn) into base64 image (png) object

    Args:
        fig: matplotlib figure

    Returns:
        base64 object: Image of plot
    """

    buf = BytesIO() # create in-memory file
    fig.savefig(buf, format='png', bbox_inches='tight') # save figure object in-memory
    buf.seek(0)
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html

    return f'data:image/png;base64, {data}'


def display_intro_header(assumption_name: str,
                         assumption_intro: str):

    return html.Div([html.H1(assumption_name)],
                    style={
                        'padding': '10px',
                        'text-align': 'center',
                        'background': '#1abc9c',
                        'color': 'white',
                        'font-size': '10px'
                        })
    # return dbc.Card([
    #                 dbc.CardHeader(html.H5(assumption_name)),
                    # dbc.CardBody(html.Small(assumption_intro))
                    # ])


def display_regression_summary(task_name: str, 
                               html_table_1: str,
                               html_table_2: str = Optional,
                               html_table_3: str = Optional):

    if task_name == 'Linear Regression':
        dbc_card_table_1 = _convert_summary_to_dashtable(html_table_1, table_type='ols_table_1')
        dbc_card_table_2 = _convert_summary_to_dashtable(html_table_2, table_type='ols_table_2')
        dbc_card_table_3 = _convert_summary_to_dashtable(html_table_3, table_type='ols_table_3')

        return dbc.Card([
                        dbc.CardHeader(html.H5(task_name)),
                        dbc.CardBody(children=[
                                    dbc_card_table_1,
                                    html.Hr(),
                                    dbc_card_table_2,
                                    html.Hr(),
                                    dbc_card_table_3                                
                                    ])
                        ])


# Define template layout for statistical results display
def display_stat_results(test_name: str,
                         interpretation: str,
                         test_table: dt.DataTable):

    layout = html.Div([
        dbc.Card([
            dbc.CardHeader([html.H5(test_name)]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6('Your Results'),
                        html.Div([test_table],
                                  style={'display':'flex',
                                         'align-items':'center',
                                         'justify-content':'center',
                                        },                                  
                                )
                    ], width=6,
                    style={'border-right': center_separator}),

                    dbc.Col([
                        html.H6(['Interpretation'],
                                style={'text-align': 'center'}),
                        html.Small(interpretation)
                    ], width=6,
                       style={'text-align': 'justify'}),                    
                    ])
                ])
            ])
        ])

    return layout


# Define template layout for plot display
def display_visual_plot(plot_name: str,
                        img_plot: base64,
                        img_examples: base64,
                        explainer: str):

    if img_examples=='None':
        left_width, right_width = 9,3
        example_div = html.Div()
        img_plot_width = '630px'
    else:
        left_width, right_width = 6,6
        img_plot_width = '440px'
        example_div = html.Div([
                        html.H6(['Examples'],
                                style={'text-align': 'center'}),
                        html.Img(src=img_examples,
                                 style={'max-width':img_plot_width,
                                        'padding-top':padding_size}),
                        html.Hr(),
                        html.P()
        ])

    layout = html.Div([
        dbc.Card([
            dbc.CardHeader([html.H5(plot_name)]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6('Your Plot'),
                        html.Img(src=img_plot,
                                 style={'max-width':img_plot_width,
                                        'padding-top':padding_size})
                    ], width=left_width,
                    style={'border-right':center_separator}),

                    dbc.Col([
                        example_div,
                        html.H6(['Plot Explanation'],
                                style={'text-align': 'center'}),
                        html.Small(explainer)
                    ], width=right_width,
                       style={'text-align':'justify'}),                    
                    ])
                ])
            ])
        ])

    return layout


# Define template layout for details of assumption check
def display_assumption_details(description: str,
                               solution: str):
    return html.Div([
        dbc.Card([
            dbc.CardHeader([html.H5('Details')]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6(['Description'],
                                style={'text-align': 'center'}),
                        html.Small(description)
                    ], width=6,
                    style={'border-right': center_separator,
                           'text-align':'justify'}),
                    dbc.Col([
                        html.H6(['Solution'],
                                style={'text-align':'center'}),
                        html.Small(solution)
                    ], width=6,
                       style={'text-align':'justify'}
                        ),                    
                ])
            ])
        ])
    ])


def display_logs(task_name: str):
    return html.Div([
        dbc.Card([
            dbc.CardHeader([html.H5('Logs')]),
            dbc.CardBody([
                dbc.Row(children=[
                    html.Small(f'[+] Running task: {task_name}'),
                    html.Small('Get logger info here!!')
                ], style={'text-align':'left'})
            ])
        ])
    ])


def _convert_summary_to_dashtable(html_table: str,
                                  table_type: str):
    col_names = ['Parameter', 'Value']

    def create_adjacent_tables(df_left: pd.DataFrame,
                               df_right: pd.DataFrame,
                               table_type: str):

        style_header = {'display':'none'}
        style_cell={'padding':padding_size,
                    'fontSize':dt_font_size, 
                    'font-family':dt_font_family}
        style_cell_conditional=[{
                                'if': {'column_id': 'Parameter'},
                                'fontWeight': 'bold',
                                }]

        return dbc.Row([
                        dbc.Col(
                                dt.DataTable( # OLS Left table
                                    id=f'{table_type}_left',
                                    columns=[{"name": i, "id": i} for i in df_left.columns],
                                    data=df_left.to_dict('records'),
                                    style_header = style_header, # Hide column headers
                                    style_cell=style_cell,
                                    style_cell_conditional=style_cell_conditional
                                            ) 
                                ),
                        dbc.Col(
                                dt.DataTable( # OLS Right table
                                    id=f'{table_type}_right',
                                    columns=[{"name": i, "id": i} for i in df_right.columns],
                                    data=df_right.to_dict('records'),
                                    style_header=style_header, # Hide column headers
                                    style_cell=style_cell,
                                    style_cell_conditional=style_cell_conditional
                                            )
                                )
                            ])

    # OLS Table 1 for overview parameters like R-squared, F statistic, AIC etc.
    if table_type == 'ols_table_1':
        raw_df = pd.read_html(html_table)[0]
        df_left = raw_df.iloc[:,:2]
        df_right = raw_df.iloc[:,-2:]
        df_left.columns = col_names
        df_right.columns = col_names
        df_right = df_right[df_right['Parameter'].notna()]
        dbc_output = create_adjacent_tables(df_left, df_right, table_type)

    # OLS Table 2 for feature coefficients, p-value and CI for each variable
    elif table_type == 'ols_table_2':
        raw_df = pd.read_html(html_table, header=0, index_col=0)[0].reset_index(drop=False)
        raw_df.rename(columns={"index": "variable"}, inplace=True)
        dbc_output = dbc.Row(                                    
                            dt.DataTable( # OLS table 1 - Left table
                                id=table_type,
                                columns=[{"name": i, "id": i} for i in raw_df.columns],
                                data=raw_df.to_dict('records'),
                                style_header={'fontWeight':'bold',
                                              'textAlign':'center'},
                                style_cell={'padding':padding_size,
                                            'fontSize':dt_font_size, 
                                            'font-family':dt_font_family,
                                            'textAlign':'center'},
                                style_cell_conditional=[{
                                    'if': {'column_id': 'variable'},
                                    'fontWeight': 'bold',
                                    }]              
                                        )
                            ) 

    # OLS Table 3 for auxiliary parameters like Omnibus, Kurtosis, Skew etc.
    elif table_type == 'ols_table_3':
        raw_df = pd.read_html(html_table)[0]
        df_left = raw_df.iloc[:,:2]
        df_right = raw_df.iloc[:,-2:]
        df_left.columns = col_names
        df_right.columns = col_names
        dbc_output = create_adjacent_tables(df_left, df_right, table_type)
    else:
        print('Table Type Not Recognized')

    return dbc_output

    
def _convert_stat_table_to_dashtable(stat_table: pd.DataFrame):
    dbc_output = dt.DataTable( 
                            id='stat_table',
                            columns=[{"name": i, "id": i} for i in stat_table.columns],
                            data=stat_table.to_dict('records'),
                            #  style_as_list_view=True,
                            style_cell={'padding':padding_size,
                                        'fontSize':dt_font_size, 
                                        'font-family':dt_font_family,
                                        'textAlign': 'center'},
                            style_header = {'fontWeight':'bold',
                                            'textAlign':'center'},
                            style_cell_conditional=[{
                                    'if': {'column_id': 'Feature'},
                                    'fontWeight': 'bold',
                                    }]           
                            )
                    
    return dbc_output


# Not using this function because we are loading example figures directly into HTML inside tabs.py
# def display_example_figures(check_type: str):
#     """Displays the example figures of assumption plots

#     Args:
#         check_type (str): Name of assumption check e.g. linearity, normality, independence, homosced
#     """
#     # response1 = plt.imread(f'https://raw.githubusercontent.com/pyassume/pyassume/main/figures/{check_type}_yes.png')
#     # response2 = plt.imread(f'https://raw.githubusercontent.com/pyassume/pyassume/main/figures/{check_type}_yes.png')
#     response1 = requests.get('https://avatars.githubusercontent.com/u/95085536?s=400&u=3fc5534c84bb4d5c78006713da9b25ffa80d6c58&v=4')
#     response2 = response1
#     img1 = Image.open(BytesIO(response1.content))
#     img2 = Image.open(BytesIO(response2.content))
    
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18,18), sharex=True, sharey=True)
#     ax1.axis('off')
#     ax1.imshow(img1)
#     ax2.axis('off')
#     ax2.imshow(img2)
#     plt.subplots_adjust(top=1, bottom=0, right=1, left=0, 
#                         hspace=0, wspace=0.03)
#     plt.margins(0,0)
#     plt.show()


# def main_section_header(x: str):
#     """Print title main header

#     Args:
#         x (str): Header title
#     """
#     print('\n')
#     print('*' * len(x))
#     print(x)
#     print('*' * len(x))
#     print('\n')
    

# def _check_target_type(df, target):
#     numerics = ["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
#     if df[target].dtype not in numerics:
#         raise ValueError(f'Target variable {target} needs to be numerical e.g. float, integer')