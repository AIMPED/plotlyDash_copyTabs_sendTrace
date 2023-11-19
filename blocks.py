import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.graph_objects as go


sidebar = dbc.Offcanvas(
    id="sidebar_left",
    title="Sidebar left",
    backdrop=False,
    is_open=False,
    class_name="rounded-end rounded-2 border border-2",
    style={'width': 300},
    children=dbc.Stack(
        [
            dcc.Dropdown(id='tab_selector', options=[]),
            dbc.Button(id='send_trace', children='send trace to tab')
        ],
        direction='vertical')
)


# create DataFrame (dummy data for MockUp)
def create_data(seed):
    np.random.seed(seed)
    cols = {
        24: list('ABCD'),
        42: list('EFGH')
    }[seed]
    return pd.DataFrame(np.random.randint(0, 20, size=(9, 4)), columns=cols)


# static layout for all pages
static_options = dbc.Container(
    [
        dbc.Stack(
            [
                html.Div(
                    dcc.Dropdown(
                        id='data_drop',
                        options=[
                            {'label': 'A', 'value': 24},
                            {'label': 'B', 'value': 42},
                        ],
                        placeholder='Select data...',
                        style={'width': '100%', 'min-height': '50px'}
                    ),
                    style={'width': '300px'}
                ),
                dbc.Button(id='copy_tab_btn', children='copy main tab'),
            ],
            direction='horizontal'
        ),
        html.H3('This is your static part for all pages')
    ],
    style={
        'height': '20vh',
        'background-color': 'gray'
    },
)


# function for tab creation
def create_tabs(num):
    return dbc.Tab(
        label=f"Tab-{num}",
        tab_id=f"tab-{num}",
        children=create_content(num)
    )


# function for creation of tab content
def create_content(num):
    return dbc.Stack(
        [
            dbc.Stack(
                [
                    html.Div(
                        children=dcc.Dropdown(
                            id={'type': 'xaxis', 'index': num},
                            multi=False,
                            style={'width': '100%', 'min-height': '50px'}
                        ),
                        style={'width': '30%'}
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id={'type': 'yaxis', 'index': num},
                            multi=True,
                            style={'width': '100%', 'min-height': '50px'}
                        ),
                        style={'width': '30%'}
                    ),
                    dbc.Button(
                        id={'type': 'plot_btn', 'index': num},
                        children='plot'
                    )
                ],
                direction='horizontal'
            ),
            dcc.Graph(
                id={'type': 'graph', 'index': num},
                figure=go.Figure(data=[])
                # ^^ this is needed, otherwise the sending of traces does not work
            ),
            dcc.Store(id={'type': 'local_tab_store', 'index': num})
        ],
        direction='vertical'
    )