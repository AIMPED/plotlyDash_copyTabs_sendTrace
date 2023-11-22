from dash import register_page, html


# register page in the registry
register_page(__name__, path="/")

# layout of the page (landing page)
layout = html.Div(
    [
        html.H3(
            id='container_page_1',
            children='This is just a dummy page',
            className='pt-3'
        )
    ]
)
