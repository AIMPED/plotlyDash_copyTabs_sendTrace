import dash
from dash import dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import blocks


external_stylesheets = [
    dbc.themes.SLATE,
]

# initiate app
app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
)

# create a simple navbar containing dbc.Buttons() for navigation
navbar = dbc.Navbar(
    id='navbar',
    children=[
        dbc.Button(
            children=page['name'],
            href=page['path']
        )
        for page in dash.page_registry.values()
        if page['name'] != 'Not found 404'
    ],
    color='primary',
    className='mb-0',
    # ^^ no margin on bottom
    style={'height': '50px'}
)

app.layout = dbc.Container(
    [
        navbar,
        blocks.static_options,
        blocks.sidebar,
        dash.page_container,
        
        dcc.Store(id={'type': 'central_store', 'index': 0}),
        # ^^ selected dataset
        dcc.Store(id={'type': 'central_store', 'index': 1}),
        # ^^ column names of selected dataframe
        dcc.Store(id={'type': 'central_store', 'index': 2}),
        # ^^ trace of clicked data
    ],
)


# write selected data into central store
@callback(
    Output({'type': 'central_store', 'index': 0}, 'data'),
    Input('data_drop', 'value'),
    prevent_initial_call=True
)
def select_options(value):
    return value


# write columns of selected data into central store
@callback(
    Output({'type': 'central_store', 'index': 1}, 'data'),
    Input('data_drop', 'value'),
    prevent_initial_call=True
)
def select_options(dataset):
    df = blocks.create_data(dataset)
    return df.columns


if __name__ == "__main__":
    app.run(debug=True, port=8055)
