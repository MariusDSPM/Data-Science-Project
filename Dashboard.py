"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""

# Almost everything in here is just copy-pasted from examplatory code for now. 

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed", # remains in place when scrolling
    "top": 0, # begins at top of page
    "left": 0, # begins at left of page
    "bottom": 0, # ends at bottom of page
    "width": "16rem", # obvious, rem is "unit" of indentation
    "padding": "1.5rem 1.5rem", # distance of sidebar entries from top and left
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem", # indentation of main content from left side (sidebar is 16rem wide)
    "margin-right": "2rem", # indentation of main content from right side
    "padding": "2rem 2rem", # distance of main content from top and bottom
}

sidebar = html.Div(
    [
        html.H2("Navigation", className="display-6"),
        html.Hr(),
        html.P(
            "Feel free to explore", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Overview", href = "/experiments/overview"),
                dbc.DropdownMenuItem("Decoy Effect", href="/experiments/decoy"),
                dbc.DropdownMenuItem("Prospect Theory", href="/experiments/prospect"),
                dbc.DropdownMenuItem("Sunk Cost Fallacy", href="/experiments/sunk-cost"),
                dbc.DropdownMenuItem("Ultimatum Game", href="/experiments/ultimatum"),
                dbc.DropdownMenuItem("Loss Aversion", href="/experiments/loss-aversion"),
            ],
            label="Experiments",
            nav=True,
        ),
                dbc.NavLink("Live Experiment", href="/page-2", active="exact"),
                dbc.NavLink("Chatbot", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# Add content for pages
start_page = [
            html.H1("Do Large Language Models Behave like a Human?", className="page-heading"),
            html.P("""Large Language models hold huge potential for a wide range of applications either for private, but also for professional use. 
                   One possible question that is of especially interesting for market research, is whether these models behave human-like enough to be used as surrogates for 
                   human participants in experiments. This dashboard is a first attempt to answer this question."""),
            html.P("Feel free to explore more pages using the navigation menu.")]
        


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P(start_page)
    elif pathname == "/page-1":
        return html.P("Experiments are not yet implemented. Sorry!")
    elif pathname == "/experiments/overview":
        return html.P("Overview of experiments is not yet implemented. Sorry!")
    elif pathname == "/experiments/decoy":
        return html.P("Decoy experiment is not yet implemented. Sorry!")
    elif pathname == "/experiments/prospect":
        return html.P("Prospect experiment is not yet implemented. Sorry!")
    elif pathname == "/experiments/sunk-cost":
        return html.P("Sunk Cost experiment is not yet implemented. Sorry!")
    elif pathname == "/experiments/ultimatum":
        return html.P("Ultimatum experiment is not yet implemented. Sorry!")
    elif pathname == "/experiments/loss-aversion":
        return html.P("Loss Aversion experiment is not yet implemented. Sorry!")
    elif pathname == "/page-2":
        return html.P("Live experiment is not yet implemented. Sorry!")
    elif pathname == "/page-3":
        return html.P("This chatbot is not yet implemented. Sorry!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8888)