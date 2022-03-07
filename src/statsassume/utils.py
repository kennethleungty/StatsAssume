# =================================
# Module: Utility Functions
# Author: Kenneth Leung
# Last Modified: 12 Jan 2022
# =================================
import pandas as pd
import matplotlib.pyplot as plt
import base64
import re
from dash import html
from dash import dash_table as dt
import dash_bootstrap_components as dbc
from io import BytesIO
from typing import Optional

# Default styling settings
dt_font_size = 14  # Font size for dash table cells
dt_font_family = 'Arial'  # Font family for dash table cells
padding_size = '8px'
center_separator = '2px solid #FFD700'


def display_base64_plot(fig):
    """Convert plot (matplotlib or seaborn) into base64 image (png) object

    Args:
        fig: matplotlib figure

    Returns:
        base64 object: Image of plot
    """

    buf = BytesIO()  # create in-memory file
    fig.savefig(buf, format='png', bbox_inches='tight')  # save figure object in-memory
    buf.seek(0)
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8")  # encode to html

    return f'data:image/png;base64, {data}'


def display_tab_header(assumption_name: str,
                       assumption_intro: str = Optional):
    """Displays title header of dashboard tab

    Args:
        assumption_name (str): Name of assumption check
        assumption_intro (str): Brief description of assumption check

    Returns:
        html.Div: Title header of dashboard tab
    """
    return html.Div([html.H5([assumption_name],
                             style={
                             'padding': '0px 0px 10px 0px',
                             'text-align': 'center',
                             # 'background': '#FFFEFB',
                             'color': 'black',
                             'font-size': '24px',
                             'margin': '0',
                             'border-bottom': '2px solid #FFD700'
                             })]
                    )


def display_card_header(card_header_title: str):
    """Displays card header for each section in dashboard tab

    Args:
        card_header_title (str): Name of section (e.g. plot, statistical check)

    Returns:
        html.Div: Header of card section
    """

    return dbc.CardHeader([html.H5(children=[card_header_title],
                                   style={'font-size': '20px',
                                          'padding': '6px 0'
                                          }
                                   )],
                          style={'background-color': '#F4F7FC',
                                 'padding': '5px 0',
                                 'margin': '0px'}
                          )


def display_card_subheader(card_subheader_title: str):
    """Displays subsection header of card

    Args:
        card_subheader_title (str): Name of subsection within card

    Returns:
        html.Div: Header of card subsection
    """
    return html.H6(children=[card_subheader_title],
                   style={'text-align': 'center'
                          })


def display_plot_img(img,
                     width: int):
    """Displays plot image

    Args:
        img (base64 object): Encoded image of plot
        width (int): Width of image

    Returns:
        html.Img: Wrapper for plot image display
    """
    return html.Img(src=img,
                    style={'max-width': width,
                           'padding-top': '8px'})


def display_text_paragraph(text: str):
    """Displays paragraph of text (e.g. explanation, plot interpretation)

    Args:
        text (str): Informational text

    Returns:
        html.Small: Wrapper for text paragraph
    """
    return html.P(children=[text],
                  style={'font-size': '14px',
                         'white-space': 'pre-wrap'
                         })


def display_regression_summary(results_name: str,
                               html_table_1: str,
                               html_table_2: str = Optional,
                               html_table_3: str = Optional):
    """Displays the summary results of regression modelling

    Args:
        results_name (str): Name of regression task
        html_table_1 (str): Summary table 1 from model results output
        html_table_2 (str, optional): Summary table 2 from model results output. Defaults to Optional.
        html_table_3 (str, optional): Summary table 3 from model results output. Defaults to Optional.

    Returns:
        dbc.Card: Regression summary within a Dash Bootstrap Card for display
    """

    if results_name == 'Linear Regression Results':
        dbc_card_table_1 = _convert_summary_to_dashtable(html_table_1, table_type='ols_table_1')
        dbc_card_table_2 = _convert_summary_to_dashtable(html_table_2, table_type='ols_table_2')
        dbc_card_table_3 = _convert_summary_to_dashtable(html_table_3, table_type='ols_table_3')

        return dbc.Card([
                        display_card_header(results_name),
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
    """Display results and interpretation of statistical test

    Args:
        test_name (str): Name of statistical test
        interpretation (str): Description on how to interpret test results
        test_table (dt.DataTable): Table displaying the statistics values of test

    Returns:
        html.Div: Template layout showing statistical test results and its corresponding interpretation
    """

    layout = html.Div([
        dbc.Card([
            display_card_header(test_name),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        display_card_subheader('Your Results'),
                        html.Div([test_table],
                                 style={'display': 'flex',
                                        'align-items': 'center',
                                        'justify-content': 'center',
                                        }
                                 )
                    ], width=6,
                        style={'border-right': center_separator}),
                    dbc.Col([
                            display_card_subheader('Interpretation'),
                            display_text_paragraph(interpretation)
                            ],
                            width=6,
                            style={'text-align': 'justify'}),
                ])
            ])
        ])
    ])

    return layout


def display_visual_plot(plot_name: str,
                        img_plot: base64,
                        img_examples: base64,
                        explainer: str):
    """Displays plot for visual interpretation

    Args:
        plot_name (str): Name of statistical plot
        img_plot (base64): Plot image object (base64-encoded)
        img_examples (base64): Example images for comparison with plot
        explainer (str): Explanation of the visual plot

    Returns:
        html.Div: Template layout showing statistical plot for visual analysis
    """

    if img_examples == 'None':
        left_width, right_width = 9, 3
        example_div = html.Div()
        img_plot_width = '630px'
    else:
        left_width, right_width = 6, 6
        img_plot_width = '440px'
        example_div = html.Div([display_card_subheader('Examples'),
                                display_plot_img(img_examples, img_plot_width),
                                html.Hr(),
                                html.P()
                                ])

    layout = html.Div([
        dbc.Card([
            display_card_header(plot_name),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                            display_card_subheader('Your Plot'),
                            display_plot_img(img_plot, img_plot_width)
                            ],
                            width=left_width,
                            style={'border-right': center_separator}),

                    dbc.Col([
                            example_div,
                            display_card_subheader('Plot Explanation'),
                            display_text_paragraph(explainer)
                            ],
                            width=right_width,
                            style={'text-align': 'justify'}),
                ])
            ])
        ])
    ])

    return layout


# Define template layout for details of assumption check
def display_assumption_details(description: str,
                               solution: str):
    """Displays the details (i.e. description and possible solution) of the assumption check

    Args:
        description (str): Description of the assumption check
        solution (str): Possible solutions if assumption is violated

    Returns:
        html.Div: Template layout showing details of assumption check
    """

    return html.Div([
        dbc.Card([
            display_card_header('Details'),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                            display_card_subheader('Description'),
                            display_text_paragraph(description)
                            ],
                            width=6,
                            style={'border-right': center_separator,
                                   'text-align': 'justify'}),
                    dbc.Col([
                            display_card_subheader('Solution'),
                            display_text_paragraph(solution)
                            ],
                            width=6,
                            style={'text-align': 'justify'}
                            ),
                ])
            ])
        ])
    ])


def display_logs():
    """Display the logs of the regression modelling

    Returns:
        html.Div: Logs of regression modelling process
    """

    log_list = _get_log_details()

    return html.Div([
        dbc.Card([
            display_card_header('Logs'),
            dbc.CardBody([
                dbc.Row([i], style={'font-size': '14px'}) for i in log_list
            ])
        ])
    ])


def _convert_summary_to_dashtable(html_table: str,
                                  table_type: str):
    """Convert HTML tables from regression modelling summary into Dash tables

    Args:
        html_table (str): HTML table of regression summary results
        table_type (str): Type of summary table

    Returns:
        dbc.Row: Summary output in Dash table format
    """

    col_names = ['Parameter', 'Value']

    def _create_adjacent_tables(df_left: pd.DataFrame,
                                df_right: pd.DataFrame,
                                table_type: str):

        style_header = {'display': 'none',
                        'padding': '0',
                        'margin': '0'}
        style_cell = {'padding': padding_size,
                      'fontSize': dt_font_size,
                      'font-family': dt_font_family}
        style_cell_conditional = [{'if': {'column_id': 'Parameter'},
                                   'fontWeight': 'bold',
                                   }]

        return dbc.Row([
                       dbc.Col(dt.DataTable(  # OLS Left table
                               id=f'{table_type}_left',
                               columns=[{"name": i, "id": i} for i in df_left.columns],
                               data=df_left.to_dict('records'),
                               style_header=style_header,  # Hide column headers
                               style_cell=style_cell,
                               style_cell_conditional=style_cell_conditional
                               )),
                       dbc.Col(dt.DataTable(  # OLS Right table
                               id=f'{table_type}_right',
                               columns=[{"name": i, "id": i} for i in df_right.columns],
                               data=df_right.to_dict('records'),
                               style_header=style_header,  # Hide column headers
                               style_cell=style_cell,
                               style_cell_conditional=style_cell_conditional
                               ))
                       ])

    # OLS Table 1 for overview parameters like R-squared, F statistic, AIC etc.
    if table_type == 'ols_table_1':
        raw_df = pd.read_html(html_table)[0]
        df_left = raw_df.iloc[:, :2]
        df_right = raw_df.iloc[:, -2:]
        df_left.columns = col_names
        df_right.columns = col_names
        df_right = df_right[df_right['Parameter'].notna()]
        dbc_output = _create_adjacent_tables(df_left, df_right, table_type)

    # OLS Table 2 for feature coefficients, p-value and CI for each variable
    elif table_type == 'ols_table_2':
        raw_df = pd.read_html(html_table, header=0, index_col=0)[0].reset_index(drop=False)
        raw_df.rename(columns={"index": "variable"}, inplace=True)
        dbc_output = dbc.Row(dt.DataTable(  # OLS table 1 - Left table
                             id=table_type,
                             columns=[{"name": i, "id": i} for i in raw_df.columns],
                             data=raw_df.to_dict('records'),
                             style_header={'fontWeight': 'bold',
                                           'textAlign': 'center'},
                             style_cell={'padding': padding_size,
                                         'fontSize': dt_font_size,
                                         'font-family': dt_font_family,
                                         'textAlign': 'center'},
                             style_cell_conditional=[{
                                 'if': {'column_id': 'variable'},
                                 'fontWeight': 'bold'}]
                             ))

    # OLS Table 3 for auxiliary parameters like Omnibus, Kurtosis, Skew etc.
    elif table_type == 'ols_table_3':
        raw_df = pd.read_html(html_table)[0]
        df_left = raw_df.iloc[:, :2]
        df_right = raw_df.iloc[:, -2:]
        df_left.columns = col_names
        df_right.columns = col_names
        dbc_output = _create_adjacent_tables(df_left, df_right, table_type)
    else:
        print('Table Type Not Recognized')

    return dbc_output


def _convert_stat_table_to_dashtable(stat_table: pd.DataFrame):
    dbc_output = dt.DataTable(id='stat_table',
                              columns=[{"name": i, "id": i} for i in stat_table.columns],
                              data=stat_table.to_dict('records'),
                              #  style_as_list_view=True,
                              style_cell={'padding': padding_size,
                                          'fontSize': dt_font_size,
                                          'font-family': dt_font_family,
                                          'textAlign': 'center'},
                              style_header={'fontWeight': 'bold',
                                            'textAlign': 'center'},
                              style_cell_conditional=[{'if': {'column_id': 'Feature'},
                                                       'fontWeight': 'bold',
                                                       }]
                              )

    return dbc_output


def _get_log_details(log_path: str = 'logs/statsassume.log'):
    """Read and print report logs

    Args:
        log_path (str, optional): Path to log file. Defaults to 'logs/statsassume.log'.

    Returns:
        list: Log details
    """
    log_list = []

    with open(log_path) as file:
        log_lines = file.read().splitlines()
        regexp = re.compile("[[+]](.*)")
    for line in log_lines:
        line = '>>' + str(regexp.search(line).group(1))
        log_list.append(line)

    return log_list

# def _check_target_type(df, target):
#     numerics = ["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
#     if df[target].dtype not in numerics:
#         raise ValueError(f'Target variable {target} needs to be numerical e.g. float, integer')
