# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html, State, dash_table
from dash.exceptions import PreventUpdate

# Local imports
from utils.experiment import Experiment


dash.register_page(__name__, path='/live-experiment-2', name='Live Experiment 2.0', location='sidebar')


presets = {
    "Default": {
        "prompts": ["You are a random pedestrian being chosen for a survey. The question is: Would you rather:"],
        "num_scenarios": 1,
        "num_options": 3,
        "iterations": 1,
        "models": ["gpt-3.5-turbo"],
        "temperature": 1,
        "answer_texts": ['Win a car.', 'Win a house.', 'Win a boat.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Only answer with the letter of the alternative you would choose without any reasoning."],
    },
    "Loss Aversion Settings": {
        "prompts": ["You are offered two choices. Which choice would you prefer?",
                    "You are offered two choices. Which choice would you prefer?"],
        "num_scenarios": 2,
        "num_options": 2,
        "iterations": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-1106-preview", "llama-2-70b"],
        "temperature": 1.5,
        "answer_texts": ['A sure gain of $100.', 'A 50% chance to gain $200 and a 50% chance to lose $0.',
                         'A sure loss of $100.', 'A 50% chance to lose $200 and a 50% chance to lose $0.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Please answer by only giving the letter of the answer option A or B.",
                             "Please answer by only giving the letter of the answer option A or B."],
    },
    "Sunk Cost Fallacy 1 Settings": {
        "prompts": ["Assume that you have spent $90 for a ticket to a theater performance. Several weeks later you buy a $30 ticket to a rock concert. You think you will enjoy the rock concert more than the theater performance. As you are putting your just-purchased rock concert ticket in your wallet, you notice that both events are scheduled for the same evening. The tickets are non-transferable, nor can they be exchanged. You can use only one of the tickets and not the other. Which ticket will you use?",
                    "Assume that you have spent $250 for a ticket to a theater performance. Several weeks later you buy a $30 ticket to a rock concert. You think you will enjoy the rock concert more than the theater performance. As you are putting your just-purchased rock concert ticket in your wallet, you notice that both events are scheduled for the same evening. The tickets are non-transferable, nor can they be exchanged. You can use only one of the tickets and not the other. Which ticket will you use?",
                    "Assume that you have spent $10000 for a ticket to a theater performance. Several weeks later you buy a $30 ticket to a rock concert. You think you will enjoy the rock concert more than the theater performance. As you are putting your just-purchased rock concert ticket in your wallet, you notice that both events are scheduled for the same evening. The tickets are non-transferable, nor can they be exchanged. You can use only one of the tickets and not the other. Which ticket will you use?",],
        "num_scenarios": 3,
        "num_options": 2,
        "iterations": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-1106-preview", "llama-2-70b"],
        "temperature": 1,
        "answer_texts": ['Theater performance.', 'Rock concert.',
                         'Theater performance.', 'Rock concert.',
                         'Theater performance.', 'Rock concert.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Please answer by only giving the letter of the answer option A or B.",
                             "Please answer by only giving the letter of the answer option A or B.",
                             "Please answer by only giving the letter of the answer option A or B."],
    },
    "Sunk Cost Fallacy 2 Settings": {
        "prompts": ["Suppose you bought a case of good Bordeaux in the futures market for $20 a bottle. The wine now sells at auction for about $75. You have decided to drink a bottle. Which of the following best captures your feeling of the cost to you of drinking the bottle?",
                    "Suppose you bought a case of good Bordeaux in the futures market for $20 a bottle. The wine now sells at auction for about $75. You have decided to drink a bottle. Which of the following best captures your feeling of the cost to you of drinking the bottle?",
                    "Suppose you bought a case of good Bordeaux in the futures market for $20 a bottle. The wine now sells at auction for about $75. You have decided to drink a bottle. Which of the following best captures your feeling of the cost to you of drinking the bottle?"],
        "num_scenarios": 3,
        "num_options": 5,
        "iterations": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-1106-preview", "llama-2-70b"],
        "temperature": 1,
        "answer_texts": ['$0. I already paid for it.', '$20, what I paid for.', '$20, plus interest.', '$75, what I could get if I sold the bottle.', '-$55, I get to drink a bottle that is worth $75 that I only paid $20 for so I save money by drinking the bottle.',
                         '$75, what I could get if I sold the bottle.', '-$55, I get to drink a bottle that is worth $75 that I only paid $20 for so I save money by drinking the bottle.', '$0. I already paid for it.', '$20, what I paid for.', '$20, plus interest.',
                         '-$55, I get to drink a bottle that is worth $75 that I only paid $20 for so I save money by drinking the bottle.', '$75, what I could get if I sold the bottle.', '$20, plus interest.', '$0. I already paid for it.', '$20, what I paid for.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Please complete the answer by only giving the letter of the answer option A, B, C, D or E.",
                             "Please complete the answer by only giving the letter of the answer option A, B, C, D or E.",
                             "Please complete the answer by only giving the letter of the answer option A, B, C, D or E."],
    },
}


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
                    html.Label("Load Preset", style={'textAlign': 'center'}),
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
                    html.Div(id='scenarios-container', style={'width': '100%', 'marginBottom': '20px'}),
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
                            html.Label("Select number of scenarios", style={'textAlign': 'center'}),
                            dbc.Input(
                                id="num-scenarios",
                                type="number",
                                value=1,
                                min=1,
                                max=4,
                                step=1,
                                style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px'},
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
                            html.Div(id='shuffle-checklist-container'),
                            html.Label("Select number of requests", style={'textAlign': 'center'}),
                            dbc.Input(
                                id="individual-iterations",
                                type="number",
                                value=1,
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
                                style={'width': '60%', 'margin': 'auto', 'marginBottom': '20px', 'lineHeight': '30px'},
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
                            html.Div(id='cost-estimate', style={'margin-top': '20px'})
                        ],
                        style={'padding': '20px', 'width': '57%'},
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '50%'},
            ),
        ],
        style={'display': 'flex', 'flexWrap': 'wrap'}
    ),  
    html.Hr(),
    # Additional text section
    html.Div(id='experiment_prompt'),
    html.Div(id="download-dataframe-csv-container"),
    dcc.Download(id="download-dataframe-csv"),
    dcc.Graph(id="graph_1", style={'width': '70%', 'height': '60vh'}),
]


#################### Callbacks ####################


# Callback to dynamically generate new scenarios
@dash.callback(
    Output('scenarios-container', 'children'),
    [Input('num-scenarios', 'value'),
     Input('num-answer-options', 'value'),
     Input('instruction-checklist', 'value')]
)

def update_num_scenarios(num_scenarios, num_options, instruction):
    
    container = []
    count = 0
    
    answer_option_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    placeholder_text = ['Win a car.', 'Win a house.', 'Win a boat.', 'Win a plane.', 'Win a bike.', 'Win a motorcycle.']
    answer_textarea_style = {'width': '100%', 'height': 30} 
    
    for i in range(num_scenarios):
        container.extend([
            html.Div(
                children=[
                    html.Label(f"Scenario {i+1}:", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold'}),
                    dcc.Textarea(
                        id={"type": "individual-prompt", "index": i},
                        value="You are a random pedestrian being chosen for a survey. The question is: Would you rather:",
                        style={'width': '100%', 'height': 100},
                        persistence=True,
                        persistence_type='session',
                    ),
                ],
                style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px'},
            ),
        ])
        for j in range(num_options):
            container.extend([
                html.Label(f"Answer option {answer_option_labels[j]}:", style={'textAlign': 'center'}),
                dcc.Textarea(
                    id={"type": "individual-answer", "index": count},
                    value=placeholder_text[j],
                    style=answer_textarea_style,
                    persistence=True,
                    persistence_type='session',
                )
            ])
            count += 1
        
        if "add_instruction" in instruction:
            container.extend([
                html.Label(f"Instruction:", style={'textAlign': 'center', 'marginTop': '20px'}),
                dcc.Textarea(
                    id={"type": "instruction-text", "index": i},
                    value='Only answer with the letter of the alternative you would choose without any reasoning.',
                    style=answer_textarea_style, 
                    persistence=True,
                    persistence_type='session',
                )
            ])
            
        # Add a larger space between scenarios
        container.append(html.Div(style={'height': '60px'}))
    
    return container

    
# Callback to run individual live experiment
@dash.callback(
    [
        Output("experiment_prompt", "children"),
        Output("download-dataframe-csv-container", "children"),
        Output("graph_1", "figure")
    ],
    [
        Input("individual-update-button", "n_clicks")
    ],
    [
        State({"type": "individual-prompt", "index": ALL}, "value"),
        State("individual-model-checklist", "value"),
        State("individual-iterations", "value"),
        State("individual-temperature", "value"),
        State("num-answer-options", "value"),
        State({"type": "individual-answer", "index": ALL}, "value"),
        State("instruction-checklist", "value"),
        State({"type": "instruction-text", "index": ALL}, "value"),
    ],
)
def update_individual_experiment(n_clicks, prompts, models, iterations, temperature, num_options, answer_values, instruction_checklist, instruction_text):
    # Check if button was clicked
    if n_clicks is not None:  
        
        # Create experiment object
        experiment = Experiment(
            prompts=prompts,
            answers=answer_values,
            iterations=iterations,
            models=models,
            temperature=temperature,
            num_options=num_options,
            instruction_checklist=instruction_checklist,
            instructions=instruction_text,
        )
            
        # Run experiment
        experiment.run()
        
        n_clicks = None

        # Generate the output table 
        output_table = dash_table.DataTable(
            id='output-table',
            columns=[{'name': col, 'id': col} for col in experiment.results_df.columns],
            data=experiment.results_df.to_dict('records'),
            style_table={'margin-top': '50px', 'margin-bottom': '30px'}
        )

        results = (
            [html.H2("Results:", style={'margin-top': '50px', 'margin-bottom': '30px'})] +
            [
                html.Div(
                    [html.H6(f"The prompt used in scenario {i+1}:", style={'margin-bottom': '10px'})] +
                    [html.P(paragraph, style={'margin-bottom': '5px'}) 
                    for paragraph in experiment_prompt.split('\n')]
                )
                for i, experiment_prompt in enumerate(experiment.experiment_prompts)
            ] +
            [output_table]
        )
        download_button = html.Button("Download CSV", id="btn_csv")
        
        figure = experiment.plot_results()

        return results, download_button, figure



# 2 Callbacks to load preset values into the input elements
# 1st Callback  to load preset values into the input elements 
@dash.callback(
    [
        Output("num-scenarios", "value"),
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
        preset_values["num_scenarios"],
        preset_values["num_options"],
        preset_values["iterations"],
        preset_values["models"],
        preset_values["temperature"],
        preset_values["instruction_checklist"],
        
    )
    
# 2nd Callback to fill in the textareas
@dash.callback(
    [
        Output({"type": "individual-prompt", "index": ALL}, "value"),
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
        preset_values["prompts"],
        preset_values["answer_texts"],
        preset_values["instruction_text"],
    )
    
    
# Callback for cost estimate
@dash.callback(
    [
        Output("cost-estimate", "children"),
    ],
    [
        Input({"type": "individual-prompt", "index": ALL}, "value"),
        Input({"type": "individual-answer", "index": ALL}, "value"),
        Input("individual-iterations", "value"),
        Input("individual-model-checklist", "value"),
    ]
)
def update_cost_estimate(prompts, answers, iterations, models):
    # Function to count words in a list of sentences
    def count_words(sentences_list):
        word_count = sum(len(sentence.split()) for sentence in sentences_list)
        return word_count
    
    total_tokens = (count_words(prompts) + count_words(answers)) * iterations
    
    estimated_cost = 0
    if "gpt-3.5-turbo" in models:
        estimated_cost += 0.001 * (total_tokens / 1000) + 0.002 * (1/1000)
    if "gpt-4-1106-preview" in models:
        estimated_cost += 0.01 * (total_tokens / 1000) + 0.03 * (1/1000)
    
    
    cost_estimate = html.P(f"Estimated cost for OpenAI models: {estimated_cost:.2f} USD",
                           style={'text-align': 'center'})
    
    return [cost_estimate]


# Callback for shuffle option
@dash.callback(
    [
        Output("shuffle-checklist-container", "children"),
    ],
    [
        Input("num-scenarios", "value"),
    ]
)
def update_shuffle_checklist(num_scenarios):
    if num_scenarios == 1:
        return [dcc.Checklist(
                    id="shuffle-checklist",
                    options=[
                        {"label": "Shuffle answer options", "value": "shuffle_options"}
                    ],
                    inline=False,
                    style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px', 'textAlign': 'center'},
                    inputStyle={'margin-right': '10px'},
                    persistence=True,
                    persistence_type='session',
                )]
    else:
        return [html.Div()]