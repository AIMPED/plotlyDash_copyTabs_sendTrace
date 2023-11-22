from dash import register_page, html


# register page in the registry
register_page(__name__, path="/")

# layout of the page (landing page)
layout = html.Div(
    [
        html.Div(id='container_page_1', children='This is just a dummy page')
    ]
)
