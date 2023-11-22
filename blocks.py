import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.graph_objects as go


sidebar = dbc.Offcanvas(
    id="sidebar_left",
    title="Copy trace",
    backdrop=False,
    is_open=False,
    class_name="border border-2",
    style={'width': 300},
    
    # content of the sidebar
    children=dbc.Stack(
        [
            dcc.Dropdown(
                id='tab_selector',
                options=[],
                style={'min-height': '50px'},
                className='pt-1 pb-1',
                placeholder='Select tab...'
            ),
            dbc.Button(
                id='send_trace',
                children='Send to tab'
            )
        ],
        direction='vertical'
    )
)


def create_data(seed: int) -> pd.DataFrame:
    """
    function creates a dummy DataFrame
    """
    # make the DataFrame reproducible
    np.random.seed(seed)
    
    cols = {
        24: list('ABCD'),
        42: list('EFGH')
    }[seed]
    return pd.DataFrame(
        np.random.randint(0, 20, size=(9, 4)), 
        columns=cols
        )


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
                    style={'width': '300px'},
                    className='me-1'
                ),
                dbc.Button(
                    id='copy_tab_btn',
                    children='copy main tab',
                    className='ms-1'
                ),
            ],
            direction='horizontal',
            className='pt-1'
        ),
        html.H3(
            children='This is the static part for all pages',
            className='pt-2'
        )
    ],
    style={
        'height': '12vh',
        # 'background-color': 'gray'
    },
    className='bg-primary'
)


def create_tabs(num: int) -> dbc.Tab:
    """
    function creates dbc.Tab components
    """
    return dbc.Tab(
        label=f"Tab-{num}",
        tab_id=f"tab-{num}",
        children=create_tab_content(num)
    )


def create_tab_content(num: int) -> dbc.Stack:
    """
    function creates the tab content
    """
    return dbc.Stack(
        [
            dbc.Stack(
                [
                    html.Div(
                        children=dcc.Dropdown(
                            id={'type': 'xaxis', 'index': num},
                            multi=False,
                            style={'width': '100%', 'min-height': '50px'},
                            placeholder='Select x- axis data'
                        ),
                        style={'width': '30%'},
                        className='pe-1'
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id={'type': 'yaxis', 'index': num},
                            multi=True,
                            style={'width': '100%', 'min-height': '50px'},
                            placeholder='Select y- axis data'

                        ),
                        style={'width': '30%'},
                        className='pe-1'

                    ),
                    dbc.Button(
                        id={'type': 'plot_btn', 'index': num},
                        children='plot chart'
                    )
                ],
                direction='horizontal',
                className='pb-1'
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
