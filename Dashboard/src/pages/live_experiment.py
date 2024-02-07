# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html

# Local imports
from components.live_experiment.answer_options_tab import answer_option_layout
from components.live_experiment.numeric_tab import numeric_layout


dash.register_page(__name__, path='/live-experiment', name='Live Experiment', location='below-experiments')


layout = [
    html.H1("Conduct your own individual experiment", className="page-heading"),
    html.Hr(),
    html.H6("To run your own individual experiment, you'll need to provide API keys to get access to the LLMs:"),
    html.Br(),
    html.Div(
        [
            dbc.Input(
                id='input-openai-key', 
                placeholder="OpenAI API Key", 
                type="password", 
                persistence=True, 
                persistence_type='session', 
                style={'width': '30%'}),
            dbc.FormText("You'll need an OpenAI API key to use GPT-3.5-Turbo and GPT-4-1106-Preview. You can get one from the OpenAI website (https://platform.openai.com)."),
        ],
    ),
    html.Br(),
    html.Div(
        [
            dbc.Input(
                id='input-replicate-key', 
                placeholder="Replicate API Key", 
                type="password", 
                persistence=True, 
                persistence_type='session', 
                style={'width': '30%'}),
            dbc.FormText("You'll need a Replicate API key to use Llama-2-70b. You can get one from the Replicate website (https://replicate.com)."),
        ],
    ),
    dcc.Store(id='user-api-keys'),
    html.Hr(),
    html.Br(),
    html.P("""Choose scenarios, models, and answer options to run the experiment yourself."""),
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
    
    
@dash.callback(
    [
        Output("user-api-keys", "data"),
    ],
    [
        Input("input-openai-key", "value"),
        Input("input-replicate-key", "value"),
    ]
)
def update_api_keys(openai_key, replicate_key):
    return [{"openai": openai_key, "replicate": replicate_key}]