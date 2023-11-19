from dash import register_page, html, callback, Input, Output

# register page in the registry
register_page(__name__, path="/")

layout = html.Div(
    [
        html.Div(id='container_page_1', children='landing page')
    ]
)
