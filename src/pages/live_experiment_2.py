# Import required libraries 
import pandas as pd
import random
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
import plotly.graph_objects as go
from openai import OpenAI
import openai
import replicate
import os


dash.register_page(__name__, path='/live-experiment-2', name='Live Experiment 2.0', location='sidebar')


# Get openAI API key (previously saved as environmental variable)
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set client
client = OpenAI()

model_options = [
    {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
    {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
    {"label": "LLama-2-70b", "value": "llama-2-70b"},
]

# Update the default selected values
default_selected_models = ["gpt-3.5-turbo"]


# Page for individual experiment
layout = [
    html.H1("Conduct your own individual experiment", className="page-heading"),
    html.Hr(),
    html.P("""Think of a multiple-choice-style experiment to conduct. Choose a prompt, a model, and answer options to run the experiment yourself."""),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    # Left column - Answer options
                    html.Label("Select a scenario", style={'textAlign': 'center'}),
                    dcc.Textarea(
                        id='individual-prompt',
                        placeholder="You are a random pedestrian being chosen for a survey. The question is: Would you rather:",
                        style={'width': '100%', 'height': 100},
                    ),
                    # Answer options dynamically generated based on dropdown selection
                    html.Div(id='answer-options-container'),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '50%'},
            ),
            html.Div(
                children=[
                    # Right column - Dropdown menus and sliders
                    dbc.Card(
                        children=[
                            html.Label("Select number of answer options", style={'textAlign': 'center'}),
                            dbc.Input(
                                id="num-answer-options",
                                type="number",
                                value=3,
                                min=3,
                                max=6,
                                step=1,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px'},  # Adjust marginBottom
                            ),
                            html.Label("Select number of requests", style={'textAlign': 'center'}),
                            dbc.Input(
                                id="individual-iterations",
                                type="number",
                                value=50,
                                min=0,
                                max=100,
                                step=1,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px'},  # Adjust marginBottom
                            ),
                            html.Label("Select language models", style={'textAlign': 'center'}),
                            dcc.Checklist(
                                id="individual-model-checklist",
                                options=model_options,
                                value=default_selected_models,
                                inline=False,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px', 'lineHeight': '30px'},  # Adjust marginBottom
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Label("Select Temperature value", style={'textAlign': 'center'}),
                                            dcc.Slider(
                                                id="individual-temperature",
                                                min=0.01,
                                                max=2,
                                                step=0.01,
                                                marks={0.01: '0.01', 1: '1', 2: '2'},
                                                value=0.8,
                                                tooltip={'placement': 'top'},
                                            ),
                                        ],
                                        style={'width': '65%', 'margin': 'auto', 'marginBottom': '20px'},  # Adjust marginBottom
                                    ),
                                ],
                            ),
                            # Add a button to trigger callback
                            html.Button('Run the experiment', id='individual-update-button', n_clicks=None),
                        ],
                        style={'padding': '20px', 'width': '57%'},
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '50%'},
            ),
        ],
        style={'display': 'flex', 'flexWrap': 'wrap'}
    ),
    # Additional text section
    html.Div(
        id='individual-experiment-design',
        style={'textAlign': 'center', 'margin': '20px'},
    ),
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv"),
]

# Callback to dynamically generate answer options based on the dropdown selection
@dash.callback(
    Output('answer-options-container', 'children'),
    [Input('num-answer-options', 'value')]
)

def update_answer_options(num_options):
    answer_option_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    # placeholder_text = ['Win $50', 'Lose $100', 'Win $100', 'Lose $50', 'Win $200', 'Lose $200']
    placeholder_text = ['Win a car', 'Win a house', 'Win a boat', 'Win a plane', 'Win a bike', 'Win a motorcycle']
    
    answer_options = []
    textarea_style = {'width': '100%', 'height': 30} 

    for i in range(num_options):
        answer_options.extend([
            html.Label(f"Answer option {answer_option_labels[i]}:", style={'textAlign': 'center'}),
            dcc.Textarea(
                id=f'individual-answer-{answer_option_labels[i].lower()}',
                placeholder=placeholder_text[i],
                style=textarea_style,
            )
        ])

    return answer_options