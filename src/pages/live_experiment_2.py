# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html, State, dash_table

# Local imports
from components.live_experiment.answer_options_tab import answer_option_layout
from components.live_experiment.numeric_tab import numeric_layout


dash.register_page(__name__, path='/live-experiment-2', name='Live Experiment 2.0', location='sidebar')


layout = [
    html.H1("Conduct your own individual experiment", className="page-heading"),
    html.Hr(),
    html.P("""Think of a multiple-choice-style experiment to conduct. Choose a prompt, a model, and answer options to run the experiment yourself."""),
    html.Br(),
    html.Div(
        style={"display": "flex"},
        children=[
            # tab
            html.Div(
                [
                    dbc.Tabs(
                        id="live-experiment-tabs",
                        children=[
                            dbc.Tab(
                                label="Answer Options",
                                tab_id="answer_options",
                            ),
                            dbc.Tab(
                                label="Numeric",
                                tab_id="numeric",
                            ),
                        ],
                        active_tab="answer_options",
                    ),
                ]
            ),
        ],
    ),
    html.Br(),
    # Content
    html.Div(id="live-experiment-content"),
]


@dash.callback(
    [
        Output("live-experiment-content", "children"),
    ],
    [
        Input("live-experiment-tabs", "active_tab"),
    ]
)
def render_tab(tab_choice):
    if tab_choice == "answer_options":
        return [answer_option_layout()]
    elif tab_choice == "numeric":
        return [numeric_layout()]