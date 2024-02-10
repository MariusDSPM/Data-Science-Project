# This is the live experiment page dealing with the experiments concerning:
# Prospect Theory
# Prospect Theory 2
# Decoy Effect
# Transaction Utility
# Transaction Utility 2
# Transaction Utility 3

# Importing the necessary libraries
from dash import Input, Output, dcc, html, State
import dash_bootstrap_components as dbc
import dash 
import plotly.graph_objects as go
import pickle
from ast import literal_eval
import replicate
import os 
from openai import OpenAI
import openai

# Get openAI API key (previously saved as environmental variable)
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set client
client = OpenAI()



##  Import every function in utils.experiment_functions
from utils.experiment_functions import *

## Import every plotting function in utils.plotting_functions
from utils.plotting_functions import *


dash.register_page(__name__, path='/experiment-recreation', name='Experiment Recreation', location='below-experiments')




### Layout ###
layout = [
    html.H1("Live Experiment Recreation", className="page-heading"),
    html.Hr(),
### Prospect Theory 1 ###
    html.H2("Prospect Theory Live Experiment"), 
    html.Hr(),
    html.P("""Choose an experiment configuration from the options below and run the experiment yourself. You can choose 4 different scenarios, 3 different models and 
           primed vs. unprimed prompts."""),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                            html.Label("Select a scenario", style={'textAlign': 'center'}),
                            dcc.Dropdown(
                            id = "prospect1-scenario-dropdown",
                            options = [
                              {"label": "Scenario 1: Segregation of gains", "value": 1},
                              {"label": "Scenario 2: Integration of losses", "value": 2},
                              {"label": "Scenario 3: Cancellation of losses against larger gains", "value": 3},
                              {"label": "Scenario 4: Segregation of silver linings", "value": 4},
                         ],
                         value = 1,
                        style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                            html.Label("Select a language model", style={'textAlign': 'center'}),
                            dcc.Dropdown(
                            id = "prospect1-model-dropdown",
                            options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                              {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                              {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                            html.Label("Select Prompt design", style={'textAlign': 'center'}),
                            dcc.Dropdown(
                            id = "prospect1-priming-dropdown",
                            options = [
                              {"label": "Unprimed", "value": 0},
                              {"label": "Primed", "value": 1},
                            ],
                            value = 0,
                        style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},

                    ),     
                            html.Label("Select number of requests", style={'textAlign': 'center'}),                
                            dcc.Input(
                            id = "prospect1-iteration-input", 
                            type = "number",
                            value = 1, 
                            min = 0, 
                            max = 100, 
                            step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),      
                    html.Div(
                        [
                                html.H6("Select Temperature value"),
                                dcc.Slider(
                                    id="prospect1-temperature-slider",
                                    min=0.01,
                                    max=2,
                                    step=0.01,
                                    marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                    value=1,
                                    tooltip={'placement': 'top'},
                                    persistence=True,
                                    persistence_type='session',
                                        ),
                        ],
                    ),

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'prospect1-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="prospect1-graph-output", style={'width': '70%', 'height': '60vh'})
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    dcc.Loading(html.Div(
            id='prospect1-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    html.Br(),
    html.Hr(),

### Prospect Theory 2 ###
    html.H2("Prospect Theory 2 Live Experiment: Odd numbers and unfair scenarios"), 
    html.Hr(),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                            html.Label("Select a scenario", style={'textAlign': 'center'}),
                            dcc.Dropdown(
                            id = "prospect2-scenario-dropdown",
                            options = [
                              {"label": "Scenario 1: Segregation of gains", "value": 1},
                              {"label": "Scenario 2: Integration of losses", "value": 2},
                              {"label": "Scenario 3: Cancellation of losses against larger gains", "value": 3},
                              {"label": "Scenario 4: Segregation of silver linings", "value": 4},
                         ],
                         value = 1,
                        style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                            html.Label("Select configuration", style={'margin': 'auto'}),
                            dcc.Dropdown(
                            id = "prospect2-configuration-dropdown",
                            options = [
                            {"label": "Configuration 1: Odd numbers 1", "value": 1},
                            {"label": "Configuration 2: Odd numbers 2", "value": 2},
                            {"label": "Configuration 3: A is better off by 25$", "value": 3},
                            {"label": "Configuration 4: A is better off by 50$", "value": 4},
                            {"label": "Configuration 5: B is better off by 25$", "value": 5},
                            {"label": "Configuration 6: B is better off by 50$", "value": 6},
                                ],
                                value = 1,
                                style = {'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                            html.Label("Select a language model", style={'textAlign': 'center'}),
                            dcc.Dropdown(
                            id = "prospect2-model-dropdown",
                            options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                              {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                              {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                            html.Label("Select number of requests", style={'textAlign': 'center'}),                
                            dcc.Input(
                            id = "prospect2-iteration-input", 
                            type = "number",
                            value = 1, 
                            min = 0, 
                            max = 100, 
                            step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),      
                    html.Div(
                        [
                                html.H6("Select Temperature value"),
                                dcc.Slider(
                                    id="prospect2-temperature-slider",
                                    min=0.01,
                                    max=2,
                                    step=0.01,
                                    marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                    value=1,
                                    tooltip={'placement': 'top'},
                                    persistence=True,
                                    persistence_type='session',
                                        ),
                        ],
                    ),

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'prospect2-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="prospect2-graph-output", style={'width': '70%', 'height': '60vh'})
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    dcc.Loading(html.Div(
            id='prospect2-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    html.Br(),
    html.Hr(),

########## Decoy Effect ##########
    html.H2("Decoy Effect Live Experiment"), 
    html.Hr(),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select a scenario"),
                    dcc.Dropdown(
                         id = "decoy-scenario-dropdown",
                         options = [
                              {"label": "Scenario 1: All options present", "value": 1},
                              {"label": "Scenario 2: Decoy option removed", "value": 2},
                         ],
                    value=1,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select prompt design"),
                    dcc.Dropdown(
                         id = "decoy-priming-dropdown",
                         options = [
                              {"label": "Unprimed", "value": 0},
                              {"label": "Primed", "value": 1},
                            ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select answer ordering"),
                    dcc.Dropdown(
                         id = "decoy-reordering-dropdown",
                         options = [
                              {"label": "Original order", "value": 0},
                              {"label": "Answer options reordered", "value": 1},
                            ],
                      value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select language model"),
                    dcc.Dropdown(
                         id = "decoy-model-dropdown",
                         options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                              {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                              {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                      value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),  
                    html.Label("Select number of requests", style={'textAlign': 'center'}),                
                    dbc.Input(
                        id = "decoy-iteration-input", 
                        type = "number",
                        value = 1, 
                        min = 0, 
                        max = 100, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),                  
                    html.Div(
                        [
                                html.H6("Select Temperature value"),
                                dcc.Slider(
                                    id="decoy-temperature-slider",
                                    min=0.01,
                                    max=2,
                                    step=0.01,
                                    marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                    value=1,
                                    tooltip={'placement': 'top'},
                                    persistence=True,
                                    persistence_type='session',
                                        ),
                        ],
                    ),

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'decoy-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="decoy-graph-output", style={'width': '70%', 'height': '60vh'})
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    dcc.Loading(html.Div(
            id='decoy-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    html.Br(),
    html.Hr(),   

    ########## Transaction Utility  ##########
    html.H2("Transaction Utility Live Experiment: Hockey game ticket"), 
    html.Hr(),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select price paid", style={'textAlign': 'center'}),
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
                    html.Label("Select number of requests", style={'textAlign': 'center'}),                
                    dbc.Input(
                        id = "tu1-iteration-input", 
                        type = "number",
                        value = 1, 
                        min = 0, 
                        max = 100, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
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

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu1-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu1-graph-output", style={'width': '70%', 'height': '60vh'})
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    dcc.Loading(html.Div(
            id='tu1-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    html.Br(),
    html.Hr(), 

    ########## Transaction Utility 3 (listed as 2 for better comparison) ##########
    html.H2("Transaction Utility 2 Live Experiment: Hockey game ticket"), 
    html.H3("Scenario 1: Price multiplied by Pi"),
    html.Hr(),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select price paid", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-initial-cost-dropdown",
                        options=[
                            {"label": "Free", "value": 0},
                            {"label": "$5 * Pi", "value": 15.71},
                            {"label": "$5 * Pi * 2", "value": 31.42},
                        ],
                        value=0,
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select current market price", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-current-cost-dropdown",
                        options=[
                            {"label": "$5 * Pi", "value": 15.71},
                            {"label": "$5 * Pi * 2", "value": 31.42},
                        ],
                        value=15.71,
                        style={'width': '75%', 'margin': 'auto'},                        

                    ),
                    html.Label("Select buyer type", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id = "tu3-buyer-dropdown",
                        options=[
                            {"label": "Friend", "value": "friend"},
                            {"label": "Stranger", "value": "stranger"},
                        ],
                        value="friend",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu3-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select number of requests", style={'textAlign': 'center'}),                
                    dbc.Input(
                        id = "tu3-iteration-input", 
                        type = "number",
                        value = 1, 
                        min = 0, 
                        max = 100, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ), 
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu3-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None,
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu3-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu3-graph-output", style={'width': '70%', 'height': '60vh'})
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    dcc.Loading(html.Div(
            id='tu3-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    html.Br(),
    html.Hr(), 

    ########## Transaction Utility 3: Scenario 2 ##########
    html.H3("Scenario 2: Price multiplied by 10"),
    html.Hr(),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select price paid", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-initial-cost-dropdown2",
                        options=[
                            {"label": "Free", "value": 0},
                            {"label": "$50", "value": 50},
                            {"label": "$100", "value": 100},
                        ],
                        value=0,
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select current market price", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-current-cost-dropdown2",
                        options=[
                            {"label": "$50", "value": 50},
                            {"label": "$100", "value": 100},
                        ],
                        value=50,
                        style={'width': '75%', 'margin': 'auto'},                        

                    ),
                    html.Label("Select buyer type", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id = "tu3-buyer-dropdown2",
                        options=[
                            {"label": "Friend", "value": "friend"},
                            {"label": "Stranger", "value": "stranger"},
                        ],
                        value="friend",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu3-language-model-dropdown2",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select number of requests", style={'textAlign': 'center'}),                
                    dbc.Input(
                        id = "tu3-iteration-input2", 
                        type = "number",
                        value = 1, 
                        min = 0, 
                        max = 100, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ), 
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu3-temperature-slider2",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None,
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu3-update-button2', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu3-graph-output2", style={'width': '70%', 'height': '60vh'})
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    dcc.Loading(html.Div(
            id='tu3-prompt-output2',
            style={'textAlign': 'center', 'margin': '20px'}),
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    html.Br(),
    html.Hr(), 


    ########## Transaction Utility 2 ##########
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
                    html.Label("Select number of requests", style={'textAlign': 'center'}),                
                    dbc.Input(
                        id = "tu2-iteration-input", 
                        type = "number",
                        value = 1, 
                        min = 0, 
                        max = 100, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
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

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu2-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu2-graph-output", style={'width': '70%', 'height': '60vh'})
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    dcc.Loading(html.Div(
            id='tu2-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    html.Br(),
    html.Hr(), 


]

#  Callback for Individual Prospect Theory Experiment
@dash.callback(
    [Output("prospect1-graph-output", "figure"),
     Output('prospect1-prompt-output', 'children')], 
    [Input("prospect1-update-button", "n_clicks")],
    [State("prospect1-scenario-dropdown", "value"),
     State("prospect1-model-dropdown", "value"),
     State("prospect1-priming-dropdown", "value"),
     State("prospect1-iteration-input", "value"),
     State("prospect1-temperature-slider", "value")]
     )
def update_prospect_live(n_clicks, selected_scenario, selected_model, selected_priming, selected_iterations, selected_temperature):
    # Check if the button was clicked
    if n_clicks is not None:
        if selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_priming == 0:
            experiment_id = "PT_1_1"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_priming == 0:
            experiment_id = "PT_1_2"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_priming == 0:
            experiment_id = "PT_1_3"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_priming == 0:
            experiment_id = "PT_1_4"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_priming == 1:
            experiment_id = "PT_1_5"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_priming == 1:
            experiment_id = "PT_1_6"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_priming == 1:
            experiment_id = "PT_1_7"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_priming == 1:
            experiment_id = "PT_1_8"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_priming == 0:
            experiment_id = "PT_2_1"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_priming == 0:
            experiment_id = "PT_2_2"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_priming == 0:
             experiment_id = "PT_2_3"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_priming == 0:
            experiment_id = "PT_2_4"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_priming == 1:
            experiment_id = "PT_2_5"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_priming == 1:
            experiment_id = "PT_2_6"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_priming == 1:
            experiment_id = "PT_2_7"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_priming == 1:
            experiment_id = "PT_2_8"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_priming == 0:
            experiment_id = "PT_3_1"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_priming == 0:
            experiment_id = "PT_3_2"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_priming == 0:
            experiment_id = "PT_3_3"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_priming == 0:
            experiment_id = "PT_3_4"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_priming == 1:
            experiment_id = "PT_3_5"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_priming == 1:
            experiment_id = "PT_3_6"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_priming == 1:
            experiment_id = "PT_3_7"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_priming == 1:
            experiment_id = "PT_3_8"
        else:
            experiment_id = None
        
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results, probs = PT_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature)
        else:
            results, probs = PT_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature)
        n_clicks = None
        
        prompt = html.P(f"The prompt used in this experiment is: {PT_experiment_prompts_dict[experiment_id]}")
        return PT_plot_results(probs), prompt

# Callback for Prospect Theory 2
@dash.callback(
    [Output("prospect2-graph-output", "figure"),
     Output('prospect2-prompt-output', 'children')], 
    [Input("prospect2-update-button", "n_clicks")],
    [State("prospect2-scenario-dropdown", "value"),
     State("prospect2-configuration-dropdown", "value"),
     State("prospect2-model-dropdown", "value"),
     State("prospect2-iteration-input", "value"),
     State("prospect2-temperature-slider", "value")]
     )
def update_prospect2_live(n_clicks, selected_scenario, selected_configuration, selected_model, selected_iterations, selected_temperature):
        # Check if button was clicked
    if n_clicks is not None:
        if selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_configuration == 1:
            experiment_id = "PT2_1_1_1"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_configuration == 2:
            experiment_id = "PT2_1_1_2"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_configuration == 3:
            experiment_id = "PT2_1_1_3"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_configuration == 4:
            experiment_id = "PT2_1_1_4"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_configuration == 5:
            experiment_id = "PT2_1_1_5"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_configuration == 6:
            experiment_id = "PT2_1_1_6"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_configuration == 1:
            experiment_id = "PT2_2_1_1"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_configuration == 2:
            experiment_id = "PT2_2_1_2"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_configuration == 3:
            experiment_id = "PT2_2_1_3"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_configuration == 4:
            experiment_id = "PT2_2_1_4"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_configuration == 5:
            experiment_id = "PT2_2_1_5"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_configuration == 6:
            experiment_id = "PT2_2_1_6"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_configuration == 1:
            experiment_id = "PT2_3_1_1"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_configuration == 2:
            experiment_id = "PT2_3_1_2"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_configuration == 3:
            experiment_id = "PT2_3_1_3"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_configuration == 4:
            experiment_id = "PT2_3_1_4"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_configuration == 5:
            experiment_id = "PT2_3_1_5"
        elif selected_scenario == 3 and selected_model == "gpt-3.5-turbo" and selected_configuration == 6:
            experiment_id = "PT2_3_1_6"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_configuration == 1:
            experiment_id = "PT2_4_1_1"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_configuration == 2:
            experiment_id = "PT2_4_1_2"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_configuration == 3:
            experiment_id = "PT2_4_1_3"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_configuration == 4:
            experiment_id = "PT2_4_1_4"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_configuration == 5:
            experiment_id = "PT2_4_1_5"
        elif selected_scenario == 4 and selected_model == "gpt-3.5-turbo" and selected_configuration == 6:
            experiment_id = "PT2_4_1_6"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_configuration == 1:
            experiment_id = "PT2_1_2_1"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_configuration == 2:
            experiment_id = "PT2_1_2_2"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_configuration == 3:
            experiment_id = "PT2_1_2_3"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_configuration == 4:
            experiment_id = "PT2_1_2_4"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_configuration == 5:
            experiment_id = "PT2_1_2_5"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_configuration == 6:
            experiment_id = "PT2_1_2_6"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_configuration == 1:
            experiment_id = "PT2_2_2_1"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_configuration == 2:
            experiment_id = "PT2_2_2_2"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_configuration == 3:
            experiment_id = "PT2_2_2_3"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_configuration == 4:
            experiment_id = "PT2_2_2_4"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_configuration == 5:
            experiment_id = "PT2_2_2_5"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_configuration == 6:
            experiment_id = "PT2_2_2_6"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_configuration == 1:
            experiment_id = "PT2_3_2_1"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_configuration == 2:
            experiment_id = "PT2_3_2_2"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_configuration == 3:
            experiment_id = "PT2_3_2_3"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_configuration == 4:
            experiment_id = "PT2_3_2_4"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_configuration == 5:
            experiment_id = "PT2_3_2_5"
        elif selected_scenario == 3 and selected_model == "gpt-4-1106-preview" and selected_configuration == 6:
            experiment_id = "PT2_3_2_6"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_configuration == 1:
            experiment_id = "PT2_4_2_1"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_configuration == 2:
            experiment_id = "PT2_4_2_2"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_configuration == 3:
            experiment_id = "PT2_4_2_3"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_configuration == 4:
            experiment_id = "PT2_4_2_4"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_configuration == 5:
            experiment_id = "PT2_4_2_5"
        elif selected_scenario == 4 and selected_model == "gpt-4-1106-preview" and selected_configuration == 6:
            experiment_id = "PT2_4_2_6"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_configuration == 1:
            experiment_id = "PT2_1_3_1"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_configuration == 2:
            experiment_id = "PT2_1_3_2"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_configuration == 3:
            experiment_id = "PT2_1_3_3"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_configuration == 4:    
            experiment_id = "PT2_1_3_4"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_configuration == 5:
            experiment_id = "PT2_1_3_5"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_configuration == 6:
            experiment_id = "PT2_1_3_6"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_configuration == 1:
            experiment_id = "PT2_2_3_1"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_configuration == 2:
            experiment_id = "PT2_2_3_2"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_configuration == 3:
            experiment_id = "PT2_2_3_3"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_configuration == 4:
            experiment_id = "PT2_2_3_4"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_configuration == 5:
            experiment_id = "PT2_2_3_5"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_configuration == 6:
            experiment_id = "PT2_2_3_6"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_configuration == 1:
            experiment_id = "PT2_3_3_1"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_configuration == 2:
            experiment_id = "PT2_3_3_2"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_configuration == 3:
            experiment_id = "PT2_3_3_3"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_configuration == 4:
            experiment_id = "PT2_3_3_4"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_configuration == 5:
            experiment_id = "PT2_3_3_5"
        elif selected_scenario == 3 and selected_model == "llama-2-70b" and selected_configuration == 6:
            experiment_id = "PT2_3_3_6"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_configuration == 1:
            experiment_id = "PT2_4_3_1"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_configuration == 2:
            experiment_id = "PT2_4_3_2"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_configuration == 3:
            experiment_id = "PT2_4_3_3"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_configuration == 4:
            experiment_id = "PT2_4_3_4"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_configuration == 5:
            experiment_id = "PT2_4_3_5"
        elif selected_scenario == 4 and selected_model == "llama-2-70b" and selected_configuration == 6:
            experiment_id = "PT2_4_3_6"
        else:
            experiment_id = None

        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results, probs = PT2_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature)
        else:
            results, probs = PT2_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature)
        n_clicks = None
        prompt = html.P(f"The prompt used in this experiment is: {PT2_experiment_prompts_dict[experiment_id]}")
        return PT2_plot_results(probs), prompt
    
# Callback for Decoy Effect
@dash.callback(
    [Output("decoy-graph-output", "figure"),
     Output('decoy-prompt-output', 'children')],
    [Input("decoy-update-button", "n_clicks")],
    [State("decoy-scenario-dropdown", "value"),
     State("decoy-priming-dropdown", "value"),
     State("decoy-reordering-dropdown", "value"),
     State("decoy-model-dropdown", "value"),
     State("decoy-iteration-input", "value"),
     State("decoy-temperature-slider", "value")]
     )
def update_decoy_live(n_clicks, selected_scenario, selected_priming, selected_reordering, selected_model, selected_iterations, selected_temperature):
    # Check if button was clicked
    if n_clicks is not None:
        if selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_priming == 0 and selected_reordering == 0:
            experiment_id = "DE_1_1"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_priming == 0 and selected_reordering == 0:
            experiment_id = "DE_1_2"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_priming == 1 and selected_reordering == 0:
            experiment_id = "DE_1_3"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_priming == 1 and selected_reordering == 0:
            experiment_id = "DE_1_4"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_priming == 0 and selected_reordering == 1:
            experiment_id = "DE_1_5"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_priming == 0 and selected_reordering == 1:
            experiment_id = "DE_1_6"
        elif selected_scenario == 1 and selected_model == "gpt-3.5-turbo" and selected_priming == 1 and selected_reordering == 1:
            experiment_id = "DE_1_7"
        elif selected_scenario == 2 and selected_model == "gpt-3.5-turbo" and selected_priming == 1 and selected_reordering == 1:
            experiment_id = "DE_1_8"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_priming == 0 and selected_reordering == 0:
            experiment_id = "DE_2_1"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_priming == 0 and selected_reordering == 0:
            experiment_id = "DE_2_2"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_priming == 1 and selected_reordering == 0:
            experiment_id = "DE_2_3"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_priming == 1 and selected_reordering == 0:
            experiment_id = "DE_2_4"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_priming == 0 and selected_reordering == 1:
            experiment_id = "DE_2_5"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_priming == 0 and selected_reordering == 1:
            experiment_id = "DE_2_6"
        elif selected_scenario == 1 and selected_model == "gpt-4-1106-preview" and selected_priming == 1 and selected_reordering == 1:
            experiment_id = "DE_2_7"
        elif selected_scenario == 2 and selected_model == "gpt-4-1106-preview" and selected_priming == 1 and selected_reordering == 1:
            experiment_id = "DE_2_8"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_priming == 0 and selected_reordering == 0:
            experiment_id = "DE_3_1"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_priming == 0 and selected_reordering == 0:
            experiment_id = "DE_3_2"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_priming == 1 and selected_reordering == 0:
            experiment_id = "DE_3_3"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_priming == 1 and selected_reordering == 0:
            experiment_id = "DE_3_4"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_priming == 0 and selected_reordering == 1:
            experiment_id = "DE_3_5"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_priming == 0 and selected_reordering == 1:
            experiment_id = "DE_3_6"
        elif selected_scenario == 1 and selected_model == "llama-2-70b" and selected_priming == 1 and selected_reordering == 1:
            experiment_id = "DE_3_7"
        elif selected_scenario == 2 and selected_model == "llama-2-70b" and selected_priming == 1 and selected_reordering == 1:
            experiment_id = "DE_3_8"
        
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results, probs = DE_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature)
        else:
            results, probs = DE_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature)
        n_clicks = None
        prompt = html.P(f"The prompt used in this experiment is: {DE_experiment_prompts_dict[experiment_id]}")
        return DE_plot_results(probs), prompt
    
# Callback for Transaction Utility
@dash.callback(
    [Output("tu1-graph-output", "figure"),
     Output('tu1-prompt-output', 'children')],
    [Input("tu1-update-button", "n_clicks")],
    [State("tu1-initial-cost-dropdown", "value"),
     State("tu1-current-cost-dropdown", "value"),
     State("tu1-buyer-dropdown", "value"),
     State("tu1-language-model-dropdown", "value"),
     State("tu1-iteration-input", "value"),
     State("tu1-temperature-slider", "value")]
     )

def update_tu1_live(n_clicks, selected_initial_cost, selected_current_cost, selected_buyer, selected_model, selected_iterations, selected_temperature):
    if n_clicks is not None:
        if selected_initial_cost == 0 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_1_2_2"
        elif selected_initial_cost == 5 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_2_1_1"
        elif selected_initial_cost == 5 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_2_1_2"
        elif selected_initial_cost == 5 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_2_2_1"
        elif selected_initial_cost == 5 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_2_2_2"
        elif selected_initial_cost == 10 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_3_1_1"
        elif selected_initial_cost == 10 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_3_1_2"
        elif selected_initial_cost == 10 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_3_2_1"
        elif selected_initial_cost == 10 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU_1_3_2_2"
        elif selected_initial_cost == 0 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_1_2_2"
        elif selected_initial_cost == 5 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_2_1_1"
        elif selected_initial_cost == 5 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_2_1_2"
        elif selected_initial_cost == 5 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_2_2_1"
        elif selected_initial_cost == 5 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_2_2_2"
        elif selected_initial_cost == 10 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_3_1_1"
        elif selected_initial_cost == 10 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_3_1_2"
        elif selected_initial_cost == 10 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_3_2_1"
        elif selected_initial_cost == 10 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU_2_3_2_2"
        elif selected_initial_cost == 0 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_1_2_2"
        elif selected_initial_cost == 5 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_2_1_1"
        elif selected_initial_cost == 5 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_2_1_2"
        elif selected_initial_cost == 5 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_2_2_1"
        elif selected_initial_cost == 5 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_2_2_2"
        elif selected_initial_cost == 10 and selected_current_cost == 5 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_3_1_1"
        elif selected_initial_cost == 10 and selected_current_cost == 5 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_3_1_2"
        elif selected_initial_cost == 10 and selected_current_cost == 10 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_3_2_1"
        elif selected_initial_cost == 10 and selected_current_cost == 10 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU_3_3_2_2"

        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature)
        else:
            results= TU_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature)
        n_clicks = None
        prompt = html.P(f"The prompt used in this experiment is: {TU_experiment_prompts_dict[experiment_id]}")
        return TU_plot_results(results), prompt
    
# Callback for Transaction Utility 3: Scenario 1
@dash.callback(
    [Output("tu3-graph-output", "figure"),
     Output('tu3-prompt-output', 'children')],
    [Input("tu3-update-button", "n_clicks")],
    [State("tu3-initial-cost-dropdown", "value"),
     State("tu3-current-cost-dropdown", "value"),
     State("tu3-buyer-dropdown", "value"),
     State("tu3-language-model-dropdown", "value"),
     State("tu3-iteration-input", "value"),
     State("tu3-temperature-slider", "value")]
     )
def update_tu3_live(n_clicks, selected_initial_cost, selected_current_cost, selected_buyer, selected_model, selected_iterations, selected_temperature):
    if n_clicks is not None:
        if selected_initial_cost == 0 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_1_2_2"
        elif selected_initial_cost == 15.71 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_2_1_1"
        elif selected_initial_cost == 15.71 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_2_1_2"
        elif selected_initial_cost == 15.71 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_2_2_1"
        elif selected_initial_cost == 15.71 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_2_2_2"
        elif selected_initial_cost == 31.42 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_3_1_1"
        elif selected_initial_cost == 31.42 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_3_1_2"
        elif selected_initial_cost == 31.42 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_3_2_1"
        elif selected_initial_cost == 31.42 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_1_3_2_2"
        elif selected_initial_cost == 0 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_1_2_2"
        elif selected_initial_cost == 15.71 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_2_1_1"
        elif selected_initial_cost == 15.71 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_2_1_2"
        elif selected_initial_cost == 15.71 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_2_2_1"
        elif selected_initial_cost == 15.71 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_2_2_2"
        elif selected_initial_cost == 31.42 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_3_1_1"
        elif selected_initial_cost == 31.42 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_3_1_2"
        elif selected_initial_cost == 31.42 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_3_2_1"
        elif selected_initial_cost == 31.42 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_1_3_2_2"
        elif selected_initial_cost == 0 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_1_2_2"
        elif selected_initial_cost == 15.71 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_2_1_1"
        elif selected_initial_cost == 15.71 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_2_1_2"
        elif selected_initial_cost == 15.71 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_2_2_1"
        elif selected_initial_cost == 15.71 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_2_2_2"
        elif selected_initial_cost == 31.42 and selected_current_cost == 15.71 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_3_1_1"
        elif selected_initial_cost == 31.42 and selected_current_cost == 15.71 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_3_1_2"
        elif selected_initial_cost == 31.42 and selected_current_cost == 31.42 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_3_2_1"
        elif selected_initial_cost == 31.42 and selected_current_cost == 31.42 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_1_3_2_2"
        
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU3_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature)
        else:
            results= TU3_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature)
        n_clicks = None
        prompt = html.P(f"The prompt used in this experiment is: {TU3_experiment_prompts_dict[experiment_id]}")
        return TU3_plot_results(results), prompt
    

# Callback for Transaction Utility 3: Scenario 2
@dash.callback(
    [Output("tu3-graph-output2", "figure"),
     Output('tu3-prompt-output2', 'children')],
    [Input("tu3-update-button2", "n_clicks")],
    [State("tu3-initial-cost-dropdown2", "value"),
     State("tu3-current-cost-dropdown2", "value"),
     State("tu3-buyer-dropdown2", "value"),
     State("tu3-language-model-dropdown2", "value"),
     State("tu3-iteration-input2", "value"),
     State("tu3-temperature-slider2", "value")]
     )
def update_tu3_2_live(n_clicks, selected_initial_cost, selected_current_cost, selected_buyer, selected_model, selected_iterations, selected_temperature):
    # Check if button was clicked
    if n_clicks is not None:
        # Get experiment id based on selected parameters
        if selected_initial_cost == 0 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_1_2_2"
        elif selected_initial_cost == 50 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_2_1_1"
        elif selected_initial_cost == 50 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_2_1_2"
        elif selected_initial_cost == 50 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_2_2_1"
        elif selected_initial_cost == 50 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_2_2_2"
        elif selected_initial_cost == 100 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_3_1_1"
        elif selected_initial_cost == 100 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_3_1_2"
        elif selected_initial_cost == 100 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_3_2_1"
        elif selected_initial_cost == 100 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "gpt-3.5-turbo":
            experiment_id = "TU3_1_2_3_2_2"
        elif selected_initial_cost == 0 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_1_2_2"
        elif selected_initial_cost == 50 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_2_1_1"
        elif selected_initial_cost == 50 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_2_1_2"
        elif selected_initial_cost == 50 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_2_2_1"
        elif selected_initial_cost == 50 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_2_2_2"
        elif selected_initial_cost == 100 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_3_1_1"
        elif selected_initial_cost == 100 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_3_1_2"
        elif selected_initial_cost == 100 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_3_2_1"
        elif selected_initial_cost == 100 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "gpt-4-1106-preview":
            experiment_id = "TU3_2_2_3_2_2"
        elif selected_initial_cost == 0 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_1_1_1"
        elif selected_initial_cost == 0 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_1_1_2"
        elif selected_initial_cost == 0 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_1_2_1"
        elif selected_initial_cost == 0 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_1_2_2"
        elif selected_initial_cost == 50 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_2_1_1"
        elif selected_initial_cost == 50 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_2_1_2"
        elif selected_initial_cost == 50 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_2_2_1"
        elif selected_initial_cost == 50 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_2_2_2"
        elif selected_initial_cost == 100 and selected_current_cost == 50 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_3_1_1"
        elif selected_initial_cost == 100 and selected_current_cost == 50 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_3_1_2"
        elif selected_initial_cost == 100 and selected_current_cost == 100 and selected_buyer == "friend" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_3_2_1"
        elif selected_initial_cost == 100 and selected_current_cost == 100 and selected_buyer == "stranger" and selected_model == "llama-2-70b":
            experiment_id = "TU3_3_2_3_2_2"

        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU3_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature)
        else:
            results= TU3_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature)
        n_clicks = None
        prompt = html.P(f"The prompt used in this experiment is: {TU3_experiment_prompts_dict[experiment_id]}")
        return TU3_plot_results(results), prompt
    

# Callback for Transaction Utility 2
@dash.callback(
    [Output("tu2-graph-output", "figure"),
     Output('tu2-prompt-output', 'children')],
    [Input("tu2-update-button", "n_clicks")],
    [State("tu2-place-dropdown", "value"),
     State("tu2-income-dropdown", "value"),
     State("tu2-language-model-dropdown", "value"),
     State("tu2-iteration-input", "value"),
     State("tu2-temperature-slider", "value")]
     )
def update_tu2_live(n_clicks, selected_place, selected_income, selected_model, selected_iterations, selected_temperature):
    if n_clicks is not None: 
        if selected_model == "gpt-3.5-turbo" and selected_place == "hotel" and selected_income == "0":
            experiment_id = "TU2_1_1_1"
        elif selected_model == "gpt-3.5-turbo" and selected_place == "hotel" and selected_income == "$50k":
            experiment_id = "TU2_1_1_2"
        elif selected_model == "gpt-3.5-turbo" and selected_place == "hotel" and selected_income == "$70k":
            experiment_id = "TU2_1_1_3"
        elif selected_model == "gpt-3.5-turbo" and selected_place == "hotel" and selected_income == "$120k":
            experiment_id = "TU2_1_1_4"
        elif selected_model == "gpt-3.5-turbo" and selected_place == "grocery" and selected_income == "0":
            experiment_id = "TU2_1_2_1"
        elif selected_model == "gpt-3.5-turbo" and selected_place == "grocery" and selected_income == "$50k":
            experiment_id = "TU2_1_2_2"
        elif selected_model == "gpt-3.5-turbo" and selected_place == "grocery" and selected_income == "$70k":
            experiment_id = "TU2_1_2_3"
        elif selected_model == "gpt-3.5-turbo" and selected_place == "grocery" and selected_income == "$120k":
            experiment_id = "TU2_1_2_4"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "hotel" and selected_income == "0":
            experiment_id = "TU2_2_1_1"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "hotel" and selected_income == "$50k":
            experiment_id = "TU2_2_1_2"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "hotel" and selected_income == "$70k":
            experiment_id = "TU2_2_1_3"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "hotel" and selected_income == "$120k":
            experiment_id = "TU2_2_1_4"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "grocery" and selected_income == "0":
            experiment_id = "TU2_2_2_1"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "grocery" and selected_income == "$50k":
            experiment_id = "TU2_2_2_2"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "grocery" and selected_income == "$70k":
            experiment_id = "TU2_2_2_3"
        elif selected_model == "gpt-4-1106-preview" and selected_place == "grocery" and selected_income == "$120k":
            experiment_id = "TU2_2_2_4"
        elif selected_model == "llama-2-70b" and selected_place == "hotel" and selected_income == "0":
            experiment_id = "TU2_3_1_1"
        elif selected_model == "llama-2-70b" and selected_place == "hotel" and selected_income == "$50k":
            experiment_id = "TU2_3_1_2"
        elif selected_model == "llama-2-70b" and selected_place == "hotel" and selected_income == "$70k":
            experiment_id = "TU2_3_1_3"
        elif selected_model == "llama-2-70b" and selected_place == "hotel" and selected_income == "$120k":
            experiment_id = "TU2_3_1_4"
        elif selected_model == "llama-2-70b" and selected_place == "grocery" and selected_income == "0":
            experiment_id = "TU2_3_2_1"
        elif selected_model == "llama-2-70b" and selected_place == "grocery" and selected_income == "$50k":
            experiment_id = "TU2_3_2_2"
        elif selected_model == "llama-2-70b" and selected_place == "grocery" and selected_income == "$70k":
            experiment_id = "TU2_3_2_3"
        elif selected_model == "llama-2-70b" and selected_place == "grocery" and selected_income == "$120k":
            experiment_id = "TU2_3_2_4"

        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU2_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature)
        else:
            results= TU2_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature)
        n_clicks = None
        prompt = html.P(f"The prompt used in this experiment is: {TU2_experiment_prompts_dict[experiment_id]}")
        return TU2_plot_results(results), prompt