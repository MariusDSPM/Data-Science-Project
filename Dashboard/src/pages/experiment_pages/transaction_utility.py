# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
from PIL import Image
import pickle
from ast import literal_eval
import pandas as pd
import numpy as np
from collections import Counter
from utils.plotting_functions import TU_plot_results, TU2_plot_results, extract_dollar_amounts


dash.register_page(__name__, path='/transaction-utility', name='Transaction Utility', location='experiments')

### Transaction Utility ###

# Load experiment results 
TU_results = pd.read_csv('Dashboard/src/data/Output/TU_results.csv')

# Load prompts
with open("Dashboard/src/data/Input/TU_prompts.pkl", "rb") as file:
    TU_prompts = pickle.load(file)

# Load TU prompt dictionary
with open("Dashboard/src/data/Input/TU_dictionaries.pkl", "rb") as file:
    TU_dictionaries = pickle.load(file)
TU_experiment_prompts_dict = TU_dictionaries[0]


### Transaction Utility 2 ###

# Load experiment results
TU2_results = pd.read_csv('Dashboard/src/data/Output/TU2_results.csv')

# Load prompts
with open("Dashboard/src/data/Input/TU2_prompts.pkl", "rb") as file:
    TU2_prompts = pickle.load(file)

# Load TU2 prompt dictionary
with open("Dashboard/src/data/Input/TU2_dictionaries.pkl", "rb") as file:
    TU2_dictionaries = pickle.load(file)
TU2_experiment_prompts_dict = TU2_dictionaries[0]


def extract_dollar_amounts(answers):
    # Only return values that start with "$"
    valid_prices = [item for item in answers if item.startswith("$") and item[1:].replace(',', '').replace('.', '').isdigit()] # check if everything after $ is a digit, exlcuding commas
    # Delete the "$" from the beginning of each price
    prices = [item.replace('$', '') for item in valid_prices]
    return prices



### Layout ###
layout = [
    html.H1("Transaction Utility Experiment", className="page-heading"),
    html.Hr(),
    
    html.H2("Experiment 1: Hockey game tickets"),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select initial ticket price", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-initial-cost-dropdown",
                        options=[
                            {"label": "Free", "value": 0},
                            {"label": "$5", "value": 5},
                            {"label": "$10", "value": 10},
                        ],
                        value=0,
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select current market price", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-current-cost-dropdown",
                        options=[
                            {"label": "$5", "value": 5},
                            {"label": "$10", "value": 10},
                        ],
                        value=5,
                        style={'width': '75%', 'margin': 'auto'},                        

                    ),
                    html.Label("Select buyer type", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id = "tu1-buyer-dropdown",
                        options=[
                            {"label": "Friend", "value": "friend"},
                            {"label": "Stranger", "value": "stranger"},
                        ],
                        value="friend",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu1-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None, # To only allow values as specified in marks
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu1-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt 
    html.Div(
            id='tu1-prompt',
            style={'textAlign': 'center', 'margin': '20px'},
    ),

    ########## Experiment 2
    html.Hr(),
    html.H2("Experiment 2: Beer at the grocery store"),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select place of purchase", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-place-dropdown",
                        options=[
                            {"label": "Fancy resort hotel", "value": "hotel"},
                            {"label": "Run-down grocery store", "value": "grocery"},
                        ],
                        value="hotel",
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select annual income", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-income-dropdown",
                        options=[
                            {"label": "No information given", "value": "0"},
                            {"label": "$50k", "value": "$50k"},
                            {"label": "$70k", "value": "$70k"},
                            {"label": "$120k", "value": "$120k"},
                        ],
                        value="0",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),

                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu2-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None,
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu2-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt
    html.Div(
            id='tu2-prompt',
            style={'textAlign': 'center', 'margin': '20px'},
    ),
]



### Callback ###

### Experiment 1
@dash.callback(
    [Output("tu1-plot", "figure"),
    Output('tu1-prompt', 'children')],
    [
        Input("tu1-initial-cost-dropdown", "value"),
        Input("tu1-current-cost-dropdown", "value"),
        Input("tu1-buyer-dropdown", "value"),
        Input("tu1-language-model-dropdown", "value"),
        Input("tu1-temperature-slider", "value"),
    ],
)


def update_tu1(initial_costs, orientation_price, selected_buyer, selected_model, selected_temperature):
    print()

    # Get prompt
    df = TU_results[(TU_results["Initial_cost"] == initial_costs) & (TU_results["Orientation_price"] == orientation_price) & (TU_results["Buyer"] == selected_buyer) &
                    (TU_results["Model"] == selected_model) & (TU_results["Temperature"] == selected_temperature)]            
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU_plot_results(df), prompt

### Experiument 2
@dash.callback(
    [Output("tu2-plot", "figure"),
     Output('tu2-prompt', 'children')],
    [
        Input("tu2-place-dropdown", "value"),
        Input("tu2-income-dropdown", "value"),
        Input("tu2-language-model-dropdown", "value"),
        Input("tu2-temperature-slider", "value"),
    ],
)

def update_tu2(selected_place, selected_income, selected_model, selected_temperature):
    df = TU2_results[(TU2_results["Place"] == selected_place) & (TU2_results["Income"] == selected_income) & 
                     (TU2_results["Model"] == selected_model) & (TU2_results["Temperature"] == selected_temperature)]
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU2_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU2_plot_results(df), prompt