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
from io import StringIO
import pandas as pd
from openai import OpenAI
from replicate.client import Client


##  Import every function in utils.experiment_functions
from utils.experiment_functions import *

## Import every plotting function in utils.plotting_functions
from utils.plotting_functions import *

dash.register_page(__name__, path='/experiment-recreation', name='Experiment Recreation', location='below-experiments')

configurations = pd.read_csv("data/Input/configurations.csv", index_col = False)

### Layout ###
layout = [
    html.H1("Live Experiment Recreation", className="page-heading"),
    html.Hr(),
    dcc.Markdown("""
           On this page you can recreate the findings of our experiments concerning:
           * Prospect Theory
           * Prospect Theory 2: Odd numbers and unfair scenarios
           * Decoy Effect
           * Transaction Utility 1: Spare hockey game ticket
           * Transaction Utility 2: Hockey game ticket with alternative numbers
           * Transaction Utility 3: Beer from hotel vs. grocery store 
           
           You can choose the desired experiment configuration from the dropdowns and the prompt will automatically be adjusted and displayed.     
           Factoring in the selected number of iterations (i.e. how often the LLM should answer the same prompt) as well as the token count of 
           prompt and expected output, a cost estimate for runnig the experiment will also be displayed. If you are uncertain about the aspect of costs,
           you can revisit our [Overview page](/overview) or go to https://openai.com/pricing for further information.     
           Once you select the desired temperature value, you can start the experiment by clicking the "Run the experiment" button.    
           Afterwards, the results will automatically be visualized and you can download the raw results in form of a csv-file.    
                                   
           In every experiment on this page, we used *Experiment IDs* to uniquely identify them. In the downloadable results dataframes from the experiments
           below, this ID along with a column called *Configuration* will be included. In order to look up, which configuration and Experiment ID corresponds to
           which study design, you can download the configuration info from the button below."""),
            
            # Download for experiment configurations
            html.Button("Download configuration info", id="configuration-csv-button"),
            dcc.Download(id="configuration-csv-download"),
            html.Hr(),
            html.Div(
            [
                dbc.Input(
                    id='openai-api-key', 
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
                    id='replicate-api-token', 
                    placeholder="Replicate API Key", 
                    type="password", 
                    persistence=True, 
                    persistence_type='session', 
                    style={'width': '30%'}),
                dbc.FormText("You'll need a Replicate API key to use Llama-2-70b. You can get one from the Replicate website (https://replicate.com)."),
            ],
        ),
        html.Br(),
        html.Hr(),
### Prospect Theory 1 ###
    html.H2("Prospect Theory Live Experiment"), 
    html.Hr(),
    dcc.Markdown("""To look up the original study design of the Prospect Theory experiments, as well as the implementation for the LLMs, 
                 you can visit the [Prospect Theory page](/prospect-theory)."""),
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
                            max = 500, 
                            step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),     
                    dbc.Tooltip(
                    """The number of requests determines how often the same prompt is answered by the LLM. A higher number of requests will
                      however also result in higher costs. The maximum input value is set to 500.""",
                    target="prospect1-iteration-input",
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
                    dbc.Tooltip(
                        "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                        target="prospect1-temperature-slider",
                    ),

                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'prospect1-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Loading(
            dcc.Graph(id="prospect1-graph-output"),
            ),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='prospect1-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),
    dcc.Store(id='prospect1-id-store', storage_type='memory'),
    dcc.Store(id='prospect1-data-store', storage_type='memory'),
    html.Button("Download CSV", id="pt1-csv-button"),
        dcc.Download(id="prospect1-csv-download"),
    html.Br(),
    html.Hr(),

### Prospect Theory 2 ###
    html.H2("Prospect Theory 2 Live Experiment: Odd numbers and unfair scenarios"), 
    html.Hr(),
        dcc.Markdown("""To look up the original study design of the second Prospect Theory experiment, as well as the implementation for the LLMs, 
                 you can visit the [Prospect Theory page](/prospect-theory)."""),
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
                            max = 500, 
                            step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),     
                    dbc.Tooltip(
                    """The number of requests determines how often the same prompt is answered by the LLM. A higher number of requests will
                      however also result in higher costs. The maximum input value is set to 500.""",
                    target="prospect2-iteration-input",
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
                    dbc.Tooltip(
                        "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                        target="prospect2-temperature-slider",
                    ),


                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'prospect2-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Loading(
            dcc.Graph(id="prospect2-graph-output")
            ),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='prospect2-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}),

    dcc.Store(id='prospect2-id-store', storage_type='memory'),
    dcc.Store(id='prospect2-data-store', storage_type='memory'),
    html.Button("Download CSV", id="pt2-csv-button"),
        dcc.Download(id="prospect2-csv-download"),
    html.Br(),
    html.Hr(),

########## Decoy Effect ##########
    html.H2("Decoy Effect Live Experiment"), 
    html.Hr(),
    dcc.Markdown("""To look up the original study design of the Decoy Effect experiments, as well as the implementation for the LLMs, 
                 you can visit the [Decoy Effect page](/decoy-effect)."""),
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
                              {"label": "Answer options renamed & reordered", "value": 1},
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
                        max = 500, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),  
                    dbc.Tooltip(
                    """The number of requests determines how often the same prompt is answered by the LLM. A higher number of requests will
                      however also result in higher costs. The maximum input value is set to 500.""",
                    target="decoy-iteration-input",
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
                    dbc.Tooltip(
                        "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                        target="decoy-temperature-slider",
                    ),


                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'decoy-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Loading(
            dcc.Graph(id="decoy-graph-output")
            ),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='decoy-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}
            ),
    dcc.Store(id='decoy-id-store', storage_type='memory'),
    dcc.Store(id='decoy-data-store', storage_type='memory'),
    html.Button("Download CSV", id="decoy-csv-button"),
        dcc.Download(id="decoy-csv-download"),
    html.Br(),
    html.Hr(),   

    ########## Transaction Utility  ##########
    html.H2("Transaction Utility Live Experiment 1: Hockey game ticket"), 
    html.Hr(),
    dcc.Markdown("""To look up the original study design of the Transaction Utility experiments, as well as the implementation for the LLMs, 
                 you can visit the [Transaction Utility page](/transaction-utility)."""),
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
                        max = 500, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ), 
                    dbc.Tooltip(
                    """The number of requests determines how often the same prompt is answered by the LLM. A higher number of requests will
                      however also result in higher costs. The maximum input value is set to 500.""",
                    target="tu1-iteration-input",
                    ), 
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu1-temperature-slider",
                                min=0.01,
                                step = 0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                    dbc.Tooltip(
                        "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                        target="tu1-temperature-slider",
                    ),


                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu1-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Loading(
            dcc.Graph(id="tu1-graph-output")
            ),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='tu1-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}
            ),

    dcc.Store(id='tu1-id-store', storage_type='memory'),
    dcc.Store(id='tu1-data-store', storage_type='memory'),
    html.Button("Download CSV", id="tu1-csv-button"),
        dcc.Download(id="tu1-csv-download"),
    html.Br(),
    html.Br(),
    html.Hr(), 

    ########## Transaction Utility 3 (listed as 2 for better comparison) ##########
    html.H2("Transaction Utility Live Experiment 2: Hockey game ticket with alternative numbers"), 
    html.Hr(),
    dcc.Markdown("""To look up the original study design of the second Transaction Utility experiment, as well as the implementation for the LLMs, 
                 you can visit the [Transaction Utility page](/transaction-utility)."""),
    html.Br(),
    html.H3("Scenario 1: Prices scaled by factor Pi"),
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
                        max = 500, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ), 
                    dbc.Tooltip(
                    """The number of requests determines how often the same prompt is answered by the LLM. A higher number of requests will
                      however also result in higher costs. The maximum input value is set to 500.""",
                    target="tu3-iteration-input",
                    ), 
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu3-temperature-slider",
                                min=0.01,
                                max=2,
                                step = 0.01,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                    dbc.Tooltip(
                        "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                        target="tu3-temperature-slider",
                    ),


                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu3-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Loading(
            dcc.Graph(id="tu3-graph-output")
            ),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='tu3-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}
            ),    
    dcc.Store(id='tu3-id-store', storage_type='memory'),
    dcc.Store(id='tu3-data-store', storage_type='memory'),
    html.Button("Download CSV", id="tu3-csv-button"),
        dcc.Download(id="tu3-csv-download"),
    html.Br(),
    html.Hr(), 

    ########## Transaction Utility 3: Scenario 2 ##########
    html.H3("Scenario 2: Prices scaled by factor 10"),
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
                        max = 500, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ), 
                    dbc.Tooltip(
                    """The number of requests determines how often the same prompt is answered by the LLM. A higher number of requests will
                      however also result in higher costs. The maximum input value is set to 500.""",
                    target="tu3-iteration-input2",
                    ), 
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu3-temperature-slider2",
                                min=0.01,
                                max=2,
                                step = 0.01,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                    dbc.Tooltip(
                        "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                        target="tu3-temperature-slider2",
                    ),


                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu3-update-button2', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Loading(
            dcc.Graph(id="tu3-graph-output2")
            ),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='tu3-prompt-output2',
            style={'textAlign': 'center', 'margin': '20px'}
            ),
    dcc.Store(id='tu3-id-store2', storage_type='memory'),
    dcc.Store(id='tu3-data-store2', storage_type='memory'),
    html.Button("Download CSV", id="tu3-csv-button2"),
        dcc.Download(id="tu3-csv-download2"),
    html.Br(),

    ########## Transaction Utility 2 ##########
    html.Hr(),
    html.H2("Transaction Utility expriment 3: Beer from hotel vs. grocery store"),
    html.Hr(),
    dcc.Markdown("""To look up the original study design of the third Transaction Utility experiment, as well as the implementation for the LLMs, 
                 you can visit the [Transaction Utility page](/transaction-utility)."""),
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
                        max = 500, 
                        step = 1,
                        style={'width': '56%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ), 
                    dbc.Tooltip(
                    """The number of requests determines how often the same prompt is answered by the LLM. A higher number of requests will
                      however also result in higher costs. The maximum input value is set to 500.""",
                    target="tu2-iteration-input",
                    ), 
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu2-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                    dbc.Tooltip(
                        "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                        target="tu2-temperature-slider",
                    ),


                    # Add a button to trigger calback
                    dbc.Button('Run the experiment', id = 'tu2-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Loading(
            dcc.Graph(id="tu2-graph-output")
            ),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='tu2-prompt-output',
            style={'textAlign': 'center', 'margin': '20px'}
            ),    
    dcc.Store(id='tu2-id-store', storage_type='memory'),
    dcc.Store(id='tu2-data-store', storage_type='memory'),
    html.Button("Download CSV", id="tu2-csv-button"),
        dcc.Download(id="tu2-csv-download"),

]


##### Callback for download of configuration csv #####
@dash.callback(
    Output("configuration-csv-download", "data"),
    Input("configuration-csv-button", "n_clicks"),
)
def download_configuration_csv(n_clicks):
    if n_clicks:
        return dcc.send_data_frame(configurations.to_csv, "Configurations.csv")
    else:
        return dash.no_update


######  Callback for Individual Prospect Theory prompt and costs #####
@dash.callback(
    [Output('prospect1-prompt-output', 'children'),    
     Output('prospect1-id-store', 'data'),],
    [Input("prospect1-scenario-dropdown", "value"),
     Input("prospect1-model-dropdown", "value"),
     Input("prospect1-priming-dropdown", "value"),
     Input("prospect1-iteration-input", "value")]
     )
def update_prospect_prompt(selected_scenario, selected_model, selected_priming, selected_iterations):
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

        text = PT_experiment_prompts_dict[experiment_id]
        costs = cost_estimate(text, selected_model, selected_iterations)
        prompt = html.P([f"The prompt used in this experiment is: {PT_experiment_prompts_dict[experiment_id]}",
                         html.Br(),
                        f"The total costs of running this experiment are estimated to be ${np.round(costs, 6)}."])
        return prompt, experiment_id
    
# Callback to run experiment
@dash.callback(
    [Output("prospect1-graph-output", "figure"),
     Output('prospect1-data-store', 'data')],
     Input("prospect1-update-button", "n_clicks"),
    [State("prospect1-model-dropdown", "value"),
     State("prospect1-iteration-input", "value"),
     State("prospect1-temperature-slider", "value"),
     State("openai-api-key", "value"),
     State("replicate-api-token", "value"),
     State('prospect1-id-store', 'data')]
     )    

def prospect_run_experiment(n_clicks, selected_model, selected_iterations, selected_temperature, openai_key, replicate_token, experiment_id):
    if n_clicks is not None:  
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results, probs = PT_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature, replicate_token)
        else:
            results, probs = PT_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature, openai_key)
        n_clicks = None
        return PT_plot_results(probs), results.to_json(date_format='iso', orient='split')

    
# Callback for PT download
@dash.callback(
    Output("prospect1-csv-download", "data"),
    [Input("pt1-csv-button", "n_clicks")],
    [State('prospect1-data-store', 'data')]
)
def prospect_download_csv(n_clicks, stored_data):
    if n_clicks:
        # Convert stored data back to dataframe
        stored_df = pd.read_json(StringIO(stored_data), orient='split')
        return dcc.send_data_frame(stored_df.to_csv, "PT_results.csv")
    else:
        return dash.no_update
    

##### Callback for Prospect Theory 2 prompt and costs #####
@dash.callback(
     [Output('prospect2-prompt-output', 'children'),
     Output('prospect2-id-store', 'data')], 
    [Input("prospect2-scenario-dropdown", "value"),
     Input("prospect2-configuration-dropdown", "value"),
     Input("prospect2-model-dropdown", "value"),
     Input("prospect2-iteration-input", "value")]
)

def update_prospect2_prompt(selected_scenario, selected_configuration, selected_model, selected_iterations):
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

        text = PT2_experiment_prompts_dict[experiment_id]
        costs = cost_estimate(text, selected_model, selected_iterations)
        prompt = html.P([f"The prompt used in this experiment is: {PT2_experiment_prompts_dict[experiment_id]}",
                         html.Br(),
                        f"The total costs of running this experiment are estimated to be ${np.round(costs, 6)}."])
        return prompt, experiment_id

# Callback to run PT2 experiment
@dash.callback(
    [Output("prospect2-graph-output", "figure"),
     Output('prospect2-data-store', 'data')],
    [Input("prospect2-update-button", "n_clicks")],
    [State("prospect2-model-dropdown", "value"),
    State("prospect2-iteration-input", "value"),
    State("prospect2-temperature-slider", "value"),
    State("openai-api-key", "value"),
    State("replicate-api-token", "value"),
    State('prospect2-id-store', 'data')]
)
def prospect2_run_experiment(n_clicks, selected_model, selected_iterations, selected_temperature, openai_key, replicate_token, experiment_id):
    if n_clicks is not None:  
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results, probs = PT2_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature, replicate_token)
        else:
            results, probs = PT2_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature, openai_key)
        n_clicks = None
        return PT2_plot_results(probs), results.to_json(date_format='iso', orient='split')
    
# Callback for PT2 download
@dash.callback(
    Output("prospect2-csv-download", "data"),
    [Input("pt2-csv-button", "n_clicks")],
    [State('prospect2-data-store', 'data')]
)
def download_csv(n_clicks, stored_data):
    if n_clicks:
        # Convert stored data back to dataframe
        stored_df = pd.read_json(StringIO(stored_data), orient='split')
        return dcc.send_data_frame(stored_df.to_csv, "PT2_results.csv")
    else:
        return dash.no_update

    
    
##### Callback for Decoy Effect prompt and costs #####
@dash.callback(
    [Output('decoy-prompt-output', 'children'),
     Output('decoy-id-store', 'data')],
    [Input("decoy-scenario-dropdown", "value"),
     Input("decoy-priming-dropdown", "value"),
     Input("decoy-reordering-dropdown", "value"),
     Input("decoy-model-dropdown", "value"),
     Input("decoy-iteration-input", "value")]
     )

def update_decoy_prompt(selected_scenario, selected_priming, selected_reordering, selected_model, selected_iterations):
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

    text = DE_experiment_prompts_dict[experiment_id]
    costs = cost_estimate(text, selected_model, selected_iterations)
    prompt = html.P([f"The prompt used in this experiment is: {DE_experiment_prompts_dict[experiment_id]}",
                         html.Br(),
                        f"The total costs of running this experiment are estimated to be ${np.round(costs, 6)}."])
    return prompt, experiment_id

# Callback to run DE experiment
@dash.callback(
    [Output("decoy-graph-output", "figure"),
     Output('decoy-data-store', 'data')],
    [Input("decoy-update-button", "n_clicks")],
    [State("decoy-model-dropdown", "value"),
     State("decoy-iteration-input", "value"),
     State("decoy-temperature-slider", "value"),
     State("openai-api-key", "value"),
     State("replicate-api-token", "value"),
     State('decoy-id-store', 'data')]
)
def decoy_run_experiment(n_clicks, selected_model, selected_iterations, selected_temperature, openai_key, replicate_token, experiment_id):
    if n_clicks is not None:      
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results, probs = DE_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature, replicate_token)
        else:
            results, probs = DE_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature, openai_key)
        n_clicks = None

        return DE_plot_results(probs), results.to_json(orient='split')
    
# Callback for DE download
@dash.callback(
    Output("decoy-csv-download", "data"),
    [Input("decoy-csv-button", "n_clicks")],
    [State('decoy-data-store', 'data')]
)
def download_csv(n_clicks, stored_data):
    if n_clicks:
        # Convert stored data back to dataframe
        stored_df = pd.read_json(StringIO(stored_data), orient='split')
        return dcc.send_data_frame(stored_df.to_csv, "DE_results.csv")
    else:
        return dash.no_update
    
    
##### Callback for Transaction Utility prompt and costs #####
@dash.callback(
    [Output('tu1-prompt-output', 'children'),
     Output('tu1-id-store', 'data')],
    [Input("tu1-initial-cost-dropdown", "value"),
     Input("tu1-current-cost-dropdown", "value"),
     Input("tu1-buyer-dropdown", "value"),
     Input("tu1-language-model-dropdown", "value"),
     Input("tu1-iteration-input", "value")]
     )

def update_tu1_prompt(selected_initial_cost, selected_current_cost, selected_buyer, selected_model, selected_iterations):

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

    text = TU_experiment_prompts_dict[experiment_id]
    costs = cost_estimate(text, selected_model, selected_iterations)
    prompt = html.P([f"The prompt used in this experiment is: {TU_experiment_prompts_dict[experiment_id]}",
                    html.Br(),
                    f"The total costs of running this experiment are estimated to be ${np.round(costs, 6)}."])
    return prompt, experiment_id
    
# Callback to run TU1 experiment
@dash.callback(
    [Output("tu1-graph-output", "figure"),
     Output('tu1-data-store', 'data')],
    [Input("tu1-update-button", "n_clicks")],
    [State("tu1-language-model-dropdown", "value"),
     State("tu1-iteration-input", "value"),
     State("tu1-temperature-slider", "value"),
     State("openai-api-key", "value"),
     State("replicate-api-token", "value"),
     State("tu1-id-store", "data")]
     )
def tu1_run_experiment(n_clicks, selected_model, selected_iterations, selected_temperature, openai_key, replicate_token, experiment_id):
    if n_clicks is not None:
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature, replicate_token)
        else:
            results= TU_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature, openai_key)
        n_clicks = None
        return TU_plot_results(results), results.to_json(orient='split') 
    
# Callback for TU1 download
@dash.callback(
    Output("tu1-csv-download", "data"),
    [Input("tu1-csv-button", "n_clicks")],
    [State('tu1-data-store', 'data')]
)
def download_csv(n_clicks, stored_data):
    if n_clicks:
        # Convert stored data back to dataframe
        stored_df = pd.read_json(StringIO(stored_data), orient='split')
        return dcc.send_data_frame(stored_df.to_csv, "TU_results.csv")
    else:
        return dash.no_update
    
    
##### Callback for Transaction Utility 3: Scenario 1 prompt and costs #####
@dash.callback(
    [Output('tu3-prompt-output', 'children'),
     Output('tu3-id-store', 'data')],
    [Input("tu3-initial-cost-dropdown", "value"),
     Input("tu3-current-cost-dropdown", "value"),
     Input("tu3-buyer-dropdown", "value"),
     Input("tu3-language-model-dropdown", "value"),
     Input("tu3-iteration-input", "value")]
     )
def update_tu3_prompt(selected_initial_cost, selected_current_cost, selected_buyer, selected_model, selected_iterations):
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

    text = TU3_experiment_prompts_dict[experiment_id]
    costs = cost_estimate(text, selected_model, selected_iterations)
    prompt = html.P([f"The prompt used in this experiment is: {TU3_experiment_prompts_dict[experiment_id]}",
                     html.Br(),
                    f"The total costs of running this experiment are estimated to be ${np.round(costs, 6)}."])
    return prompt, experiment_id
    
# Callback to run TU3 experiment
@dash.callback(
    [Output("tu3-graph-output", "figure"),
     Output('tu3-data-store', 'data')],
    [Input("tu3-update-button", "n_clicks")],
    [State("tu3-language-model-dropdown", "value"),
     State("tu3-iteration-input", "value"),
     State("tu3-temperature-slider", "value"),
     State("openai-api-key", "value"),
     State("replicate-api-token", "value"),
     State("tu3-id-store", "data")]
        )
def tu3_run_experiment(n_clicks, selected_model, selected_iterations, selected_temperature, openai_key, replicate_token, experiment_id):
    if n_clicks is not None:        
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU3_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature, replicate_token)
        else:
            results = TU3_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature, openai_key)
        n_clicks = None
        return TU3_plot_results(results), results.to_json(orient='split')
    
# Callback for TU3 Scenario 1 download
@dash.callback(
    Output("tu3-csv-download", "data"),
    [Input("tu3-csv-button", "n_clicks")],
    [State('tu3-data-store', 'data')]
)
def download_csv(n_clicks, stored_data):
    if n_clicks:
        # Convert stored data back to dataframe
        stored_df = pd.read_json(StringIO(stored_data), orient='split')
        return dcc.send_data_frame(stored_df.to_csv, "TU2_scenario_1_results.csv")
    else:
        return dash.no_update
    
    

##### Callback for Transaction Utility 3: Scenario 2 prompt and costs #####
@dash.callback(
    [Output('tu3-prompt-output2', 'children'),
     Output('tu3-id-store2', 'data')],
    [Input("tu3-initial-cost-dropdown2", "value"),
     Input("tu3-current-cost-dropdown2", "value"),
     Input("tu3-buyer-dropdown2", "value"),
     Input("tu3-language-model-dropdown2", "value"),
     Input("tu3-iteration-input2", "value")]
)   
def update_tu3_2_live(selected_initial_cost, selected_current_cost, selected_buyer, selected_model, selected_iterations):
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

    text = TU3_experiment_prompts_dict[experiment_id]
    costs = cost_estimate(text, selected_model, selected_iterations)
    prompt = html.P([f"The prompt used in this experiment is: {TU3_experiment_prompts_dict[experiment_id]}",
                    html.Br(),
                    f"The total costs of running this experiment are estimated to be ${np.round(costs, 6)}."])
    return prompt, experiment_id

# Callback to run TU3 Scenario 2 experiment
@dash.callback(
    [Output("tu3-graph-output2", "figure"),
     Output('tu3-data-store2', 'data')],
    [Input("tu3-update-button2", "n_clicks")],
    [State("tu3-language-model-dropdown2", "value"),
     State("tu3-iteration-input2", "value"),
     State("tu3-temperature-slider2", "value"),
     State("openai-api-key", "value"),
     State("replicate-api-token", "value"),
     State("tu3-id-store2", "data")]
        )

def tu3_run_experiment2(n_clicks, selected_model, selected_iterations, selected_temperature, openai_key, replicate_token, experiment_id):
    if n_clicks is not None:        
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU3_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature, replicate_token)
        else:
            results = TU3_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature, openai_key)
        n_clicks = None
        return TU3_plot_results(results), results.to_json(orient='split')
    
    
# Callback for TU3 Scenario 2 download
@dash.callback(
    Output("tu3-csv-download2", "data"),
    [Input("tu3-csv-button2", "n_clicks")],
    [State('tu3-data-store2', 'data')]
)
def download_csv(n_clicks, stored_data):
    if n_clicks:
        # Convert stored data back to dataframe
        stored_df = pd.read_json(StringIO(stored_data), orient='split')
        return dcc.send_data_frame(stored_df.to_csv, "TU2_scenario_2_results.csv")
    else:
        return dash.no_update
    

##### Callback for Transaction Utility 2 prompt and costs #####
@dash.callback(
    [Output('tu2-prompt-output', 'children'),
     Output('tu2-id-store', 'data')],
    [Input("tu2-place-dropdown", "value"),
     Input("tu2-income-dropdown", "value"),
     Input("tu2-language-model-dropdown", "value"),
     Input("tu2-iteration-input", "value")]
)
def update_tu2_prompt(selected_place, selected_income, selected_model, selected_iterations):
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


    text = TU2_experiment_prompts_dict[experiment_id]
    costs = cost_estimate(text, selected_model, selected_iterations)
    prompt = html.P([f"The prompt used in this experiment is: {TU2_experiment_prompts_dict[experiment_id]}",
                    html.Br(),
                    f"The total costs of running this experiment are estimated to be ${np.round(costs, 6)}."])
    return prompt, experiment_id
    
# Callback to run TU2 experiment
@dash.callback(
    [Output("tu2-graph-output", "figure"),
     Output('tu2-data-store', 'data')],
    [Input("tu2-update-button", "n_clicks")],
    [State("tu2-language-model-dropdown", "value"),
     State("tu2-iteration-input", "value"),
     State("tu2-temperature-slider", "value"),
     State("openai-api-key", "value"),
     State("replicate-api-token", "value"),
     State("tu2-id-store", "data")]
        )
def tu2_run_experiment(n_clicks, selected_model, selected_iterations, selected_temperature, openai_key, replicate_token, experiment_id):
    if n_clicks is not None:
        # Run Experiment for selected parameters
        if selected_model == "llama-2-70b":
            results = TU2_run_experiment_llama_dashboard(experiment_id, selected_iterations, selected_temperature, replicate_token)
        else:
            results= TU2_run_experiment_dashboard(experiment_id, selected_iterations, selected_temperature, openai_key)
        n_clicks = None
        return TU2_plot_results(results), results.to_json(orient='split')

    
# Callback for TU2 download
@dash.callback(
    Output("tu2-csv-download", "data"),
    [Input("tu2-csv-button", "n_clicks")],
    [State('tu2-data-store', 'data')]
)
def download_csv(n_clicks, stored_data):
    if n_clicks:
        # Convert stored data back to dataframe
        stored_df = pd.read_json(StringIO(stored_data), orient='split')
        return dcc.send_data_frame(stored_df.to_csv, "TU3_results.csv")
    else:
        return dash.no_update
    
