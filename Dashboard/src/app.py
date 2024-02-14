# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import html


# Initialize the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                use_pages=True)
server = app.server

# Optics of sidebar
SIDEBAR_STYLE = {
    "position": "fixed", # remains in place when scrolling
    "top": 0, # begins at top of page
    "left": 0, # begins at left of page
    "bottom": 0, # ends at bottom of page
    "width": "16rem", # obvious, rem is "unit" of indentation
    "padding": "1.5rem 1.5rem", # distance of sidebar entries from top and left
    "background-color": "#c8f7f3",
}

# Optics of main page content
CONTENT_STYLE = {
    "margin-left": "18rem", # indentation of main content from left side (sidebar is 16rem wide)
    "margin-right": "2rem", # indentation of main content from right side
    "padding": "2rem 2rem", # distance of main content from top and bottom
}

# Create the sidebar
sidebar = html.Div(
    [
        html.H2("Navigation", className="display-6"),
        html.Hr(),
        html.P("Feel free to explore", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.Div(page['name'])],
                    href=page['path'],
                    active="exact",
                )
                for page in dash.page_registry.values()
                if page['location'] == 'above-experiments'
            ] +
            [
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem(
                            [html.Div(page['name'])],
                            href=page['path'],
                        )
                        for page in dash.page_registry.values()
                        if page['location'] == 'experiments'
                    ],
                    label="Experiments",
                    nav=True,
                )
            ] +
            [
                dbc.NavLink(
                    [html.Div(page['name'])],
                    href=page['path'],
                    active="exact",
                )
                for page in dash.page_registry.values()
                if page['location'] == 'below-experiments'
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ],
                style=SIDEBAR_STYLE),

            dbc.Col(
                [
                    dash.page_container
                ],
                style=CONTENT_STYLE)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run_server(port=8888, debug = False)