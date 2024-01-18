# Import required libraries 
import pandas as pd
import random
import time
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html, State, dash_table
from dash.exceptions import PreventUpdate
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



presets = {
    "Default": {
        "prompt": "You are a random pedestrian being chosen for a survey. The question is: Would you rather:",
        "num_options": 3,
        "iterations": 50,
        "models": ["gpt-3.5-turbo"],
        "temperature": 1,
        "answer_texts": ['Win a car', 'Win a house', 'Win a boat'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Only answer with the letter of the alternative you would choose without any reasoning."],
    },
    "Loss Aversion Settings": {
        "prompt": "You are offered two choices. Which choice would you prefer?",
        "num_options": 2,
        "iterations": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-1106-preview", "llama-2-70b"],
        "temperature": 1.5,
        "answer_texts": ['A sure gain of $100.', 'A 50% chance to gain $200 and a 50% chance to lose $0.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Please answer by only giving the letter of the answer option A or B."],
    },
    "Sunk Cost Fallacy 1 Settings": {
        "prompt": "Assume that you have spent $90 for a ticket to a theater performance. Several weeks later you buy a $30 ticket to a rock concert. You think you will enjoy the rock concert more than the theater performance. As you are putting your just-purchased rock concert ticket in your wallet, you notice that both events are scheduled for the same evening. The tickets are non-transferable, nor can they be exchanged. You can use only one of the tickets and not the other. Which ticket will you use?",
        "num_options": 2,
        "iterations": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-1106-preview", "llama-2-70b"],
        "temperature": 1,
        "answer_texts": ['Theater performance.', 'Rock concert.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Please answer by only giving the letter of the answer option A or B."],
    },
    "Sunk Cost Fallacy 2 Settings": {
        "prompt": "Suppose you bought a case of good Bordeaux in the futures market for $20 a bottle. The wine now sells at auction for about $75. You have decided to drink a bottle. Which of the following best captures your feeling of the cost to you of drinking the bottle?",
        "num_options": 5,
        "iterations": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-1106-preview", "llama-2-70b"],
        "temperature": 1,
        "answer_texts": ['$0. I already paid for it.', '$20, what I paid for.', '$20, plus interest.', '$75, what I could get if I sold the bottle.', '-$55, I get to drink a bottle that is worth $75 that I only paid $20 for so I save money by drinking the bottle.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Please complete the answer by only giving the letter of the answer option A, B, C, D or E."],
    },
}




def run_experiment_with_openai(model, prompt, instruction, temperature, n, max_tokens=1):
    answers = []
    for _ in range(n):
        response = client.chat.completions.create(
            model=model,  
            messages=[
                {"role": "system", "content": instruction},

                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Store the answer in the list
        answer = response.choices[0].message.content
        answers.append(answer.strip())
        
        # Add delay before the next API call
        if model == 'gpt-3.5-turbo-1106':
            # 3500 requests per minute
            time.sleep(60/3500)
        else:
            # 500 requests per minute
            time.sleep(60/500)

    return answers


def run_experiment_with_llama(model, prompt, instruction, temperature, n, max_tokens=2):
    model = 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3'
    answers = []
    for _ in range(n):
        response = replicate.run(model,
                                 input = {
                                    "temperature": temperature,
                                    "system_prompt": instruction,
                                    "prompt": prompt,
                                    "max_new_tokens": max_tokens}
                                )

        # Store the answer in the list
        answer = ''
        for item in response:
            answer += item

        answers.append(answer.strip())
        
        # Add delay before the next API call
        # 50 requests per second
        time.sleep(1/50)

    return answers


def run_individual_experiment(models, prompt, instruction, n, temperature, num_options):
    results_list = []
    
    

    for model in models:
        if model == 'llama-2-70b':
            answers = run_experiment_with_llama(model, prompt, instruction, temperature, n)
        else:
            answers = run_experiment_with_openai(model, prompt, instruction, temperature, n)
            
            
        answer_option_labels = ['A', 'B', 'C', 'D', 'E', 'F']
        answer_option_labels = answer_option_labels[:num_options]
        
        # Count of "correct" answers
        len_correct = sum(1 for ans in answers if ans in answer_option_labels)
        
        result_dict = {
            'Model': model,
            'Temperature': temperature,
            'Iterations': n,
            'Correct Answers': len_correct
        }
        
        # Check if len_correct is non-zero before performing further calculations
        if len_correct > 0:
            # Counting results
            for label in answer_option_labels:
                label_share = answers.count(label) / len_correct
                result_dict['Share of ' + label] = label_share
        else:
            # Set NaN values for share of labels when len_correct is 0
            for label in answer_option_labels:
                result_dict['Share of ' + label] = float('nan')
            
        results_list.append(result_dict)
        
    df = pd.DataFrame(results_list)    
    
    return df


def create_prompt(prompt, answer_prompts):
    answer_option_labels = ['A', 'B', 'C', 'D', 'E', 'F'] 
    
    prompt = f"""{prompt}\nA: {answer_prompts[0]}\nB: {answer_prompts[1]}"""
    
    for i, label in enumerate(answer_option_labels[2:len(answer_prompts)]):
        prompt += f"""\n{label}: {answer_prompts[i+2]}"""
    
    return prompt



# Page for individual experiment
layout = [
    html.H1("Conduct your own individual experiment", className="page-heading"),
    html.Hr(),
    html.P("""Think of a multiple-choice-style experiment to conduct. Choose a prompt, a model, and answer options to run the experiment yourself."""),
    html.Br(),
    html.Div(
        children=[
            # Dropdown for presets
            html.Div(
                children=[
                    html.Label("Select Preset", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="preset-dropdown",
                        options=[{"label": preset, "value": preset} for preset in presets.keys()],
                        value="Default",
                        style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px'},
                        persistence=True,
                        persistence_type='session',
                    ),
                ],
                style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px'},
            ),
            html.Div(
                children=[
                    # Left column
                    html.Label("Select a scenario", style={'textAlign': 'center'}),
                    dcc.Textarea(
                        id='individual-prompt',
                        value="You are a random pedestrian being chosen for a survey. The question is: Would you rather:",
                        style={'width': '100%', 'height': 100},
                        persistence=True,
                        persistence_type='session',
                    ),
                    # Answer options dynamically generated based on dropdown selection
                    html.Div(id='answer-options-container', style={'width': '100%'}),
                    # Instruction text
                    html.Div(id='instruction-text-container', style={'width': '100%', 'marginTop': 30}),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '50%'},
            ),
            html.Div(
                children=[
                    # Right column
                    dbc.Card(
                        children=[
                            dcc.Checklist(
                                id="instruction-checklist",
                                options=[
                                    {"label": "Add instruction", "value": "add_instruction"}
                                ],
                                value=["add_instruction"],
                                inline=False,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px', 'textAlign': 'center'},
                                inputStyle={'margin-right': '10px'},
                                persistence=True,
                                persistence_type='session',
                            ),
                            html.Label("Select number of answer options", style={'textAlign': 'center'}),
                            dbc.Input(
                                id="num-answer-options",
                                type="number",
                                value=3,
                                min=2,
                                max=6,
                                step=1,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px'},
                                persistence=True,
                                persistence_type='session',
                            ),
                            html.Label("Select number of requests", style={'textAlign': 'center'}),
                            dbc.Input(
                                id="individual-iterations",
                                type="number",
                                value=50,
                                min=0,
                                max=100,
                                step=1,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px'},
                                persistence=True,
                                persistence_type='session',
                            ),
                            html.Label("Select language models", style={'textAlign': 'center'}),
                            dcc.Checklist(
                                id="individual-model-checklist",
                                options=[
                                    {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                                    {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                                    {"label": "LLama-2-70b", "value": "llama-2-70b"}
                                ],
                                value=["gpt-3.5-turbo"],
                                inline=False,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px', 'lineHeight': '30px'},
                                inputStyle={'margin-right': '10px'},
                                persistence=True,
                                persistence_type='session',
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
                                                value=1,
                                                tooltip={'placement': 'top'},
                                                persistence=True,
                                                persistence_type='session',
                                            ),
                                        ],
                                        style={'width': '65%', 'margin': 'auto', 'marginBottom': '20px'}, 
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
    html.Div(id="output-table-container"),
]


#################### Callbacks ####################

# Callback to add instruction text
@dash.callback(
    Output('instruction-text-container', 'children'),
    [Input('instruction-checklist', 'value')]
)
def update_instruction_field(instruction_checklist):
    instruction_field = []

    if "add_instruction" in instruction_checklist:
        instruction_field.extend([
            html.Label(f"Instruction:", style={'textAlign': 'center'}),
            dcc.Textarea(
                id={"type": "instruction-text", "index": 0},
                value='Only answer with the letter of the alternative you would choose without any reasoning.',
                style={'width': '100%', 'height': 30}, 
                persistence=True,
                persistence_type='session',
            )
        ])

    return instruction_field


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
                id={"type": "individual-answer", "index": i},
                value=placeholder_text[i],
                style=textarea_style,
                persistence=True,
                persistence_type='session',
            )
        ])

    return answer_options  

    
# Callback to run individual live experiment
@dash.callback(
    [Output("output-table-container", "children")],
    [Input("individual-update-button", "n_clicks")],
    [State("individual-prompt", "value"),
     State("individual-model-checklist", "value"),
     State("individual-iterations", "value"),
     State("individual-temperature", "value"),
     State("num-answer-options", "value"),
     State({"type": "individual-answer", "index": ALL}, "value"),
     State("instruction-checklist", "value"),
     State({"type": "instruction-text", "index": ALL}, "value")]
)
def update_individual_experiment(n_clicks, prompt, selected_models, selected_iterations, selected_temperature, num_options, answer_values, instruction_checklist, instruction_text):
    # Check if button was clicked
    if n_clicks is not None:
        experiment_prompt = create_prompt(prompt, answer_values)

        # Check if the instruction checklist is checked
        if "add_instruction" in instruction_checklist and instruction_text is not None:
            instruction = instruction_text[0]
        else:
            instruction = ""

        df = run_individual_experiment(selected_models, experiment_prompt, instruction, selected_iterations, selected_temperature, num_options)
        n_clicks = None

        # Generate the output table 
        output_table = dash_table.DataTable(
            id='output-table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records'),
        )

        # Return the DataTable
        return [output_table]


# 2 Callbacks to load preset values into the input elements

# 1st. Callback  to load preset values into the input elements 
@dash.callback(
    [
        Output("individual-prompt", "value"),
        Output("num-answer-options", "value"),
        Output("individual-iterations", "value"),
        Output("individual-model-checklist", "value"),
        Output("individual-temperature", "value"),
        Output("instruction-checklist", "value"),
    ],
    [Input("preset-dropdown", "value")]
)
def update_preset(selected_preset):
    if not selected_preset:
        raise PreventUpdate

    preset_values = presets[selected_preset]
    return (
        preset_values["prompt"],
        preset_values["num_options"],
        preset_values["iterations"],
        preset_values["models"],
        preset_values["temperature"],
        preset_values["instruction_checklist"],
        
    )
    
# 2nd. Callback to load preset values into the input elements
@dash.callback(
    [
        Output({"type": "individual-answer", "index": ALL}, "value"),
        Output({"type": "instruction-text", "index": ALL}, "value")
    ],
    [   
        Input("preset-dropdown", "value")
    ]
)
def update_preset(selected_preset):
    if not selected_preset:
        raise PreventUpdate

    preset_values = presets[selected_preset]
    return (
        preset_values["answer_texts"],
        preset_values["instruction_text"],
    )