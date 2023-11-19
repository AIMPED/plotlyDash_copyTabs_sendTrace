from dash import register_page, callback, Input, Output, State, ALL, MATCH, Patch
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import blocks

# register page in the registry
register_page(__name__, path="/dissolution")

layout = dbc.Tabs(
    id='diss_tabs',
    children=[
        dbc.Tab(
            label="Main",
            tab_id="tab-0",
            children=blocks.create_content(num=0)
        )
    ],
    active_tab="tab-0",
)


# callback for updating the secondary drop-down options
@callback(
    Output({'type': 'xaxis', 'index': ALL}, 'options'),
    Output({'type': 'yaxis', 'index': ALL}, 'options'),
    Input({'type': 'central_store', 'index': 1}, 'data'),
    State({'type': 'yaxis', 'index': ALL}, 'options')
)
def select_options(column_names, dropdowns):
    if column_names is None:
        raise PreventUpdate

    return [column_names] * len(dropdowns), [column_names] * len(dropdowns)


# callback for plotting the chart
@callback(
    Output({'type': 'graph', 'index': MATCH}, 'figure', allow_duplicate=True),
    State({'type': 'xaxis', 'index': MATCH}, 'value'),
    State({'type': 'yaxis', 'index': MATCH}, 'value'),
    State({'type': 'central_store', 'index': 0}, 'data'),
    Input({'type': 'plot_btn', 'index': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def plot_chart(x, y, selected_data, _):
    df = blocks.create_data(selected_data)
    return go.Figure(data=[go.Scatter(x=df[x], y=df[i]) for i in y])


# copy tabs, add options to drop down
@callback(
    Output('diss_tabs', 'children'),
    Input('copy_tab_btn', 'n_clicks'),
    prevent_innitial_call=True
)
def copy(clicks):
    if clicks is None:
        raise PreventUpdate
    patched = Patch()
    patched.append(blocks.create_tabs(clicks))
    return patched


# add options to drop down
@callback(
    Output('tab_selector', 'options'),
    Input('diss_tabs', 'children'),
    prevent_innitial_call=True
)
def copy(tabs):
    return [*range(1, len(tabs))]


# open sidebar on click in trace on main tab
@callback(
    Output('sidebar_left', 'is_open', allow_duplicate=True),
    Output({'type': 'central_store', 'index': 2}, 'data'),
    Input({'type': 'graph', 'index': 0}, 'clickData'),
    State({'type': 'graph', 'index': 0}, 'figure'),
    State('sidebar_left', 'is_open'),
    prevent_initial_call=True
)
def open_sidebar(clickData, figure, is_open):
    if clickData is None:
        raise PreventUpdate

    clicked_series = clickData['points'][0]['curveNumber']
    trace = figure['data'][clicked_series]
    return not is_open, trace


# copy trace to selected tab
@callback(
    Output({'type': 'graph', 'index': ALL}, 'figure'),
    Output('sidebar_left', 'is_open'),
    Input('send_trace', 'n_clicks'),
    State('tab_selector', 'value'),
    State({'type': 'graph', 'index': ALL}, 'figure'),
    State({'type': 'central_store', 'index': 2}, 'data'),
    State('sidebar_left', 'is_open'),
)
def copy_trace(click, selected_tab, figures, trace_to_copy, is_open):
    if selected_tab is None:
        raise PreventUpdate

    patched = Patch()
    patched['data'].append(trace_to_copy)

    figures[selected_tab] = patched

    return figures, not is_open




