# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html, State, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd

# Local imports
from utils.experiment import Experiment
from utils.plotting import plot_results


# Constants
GPT_3_5_INPUT_COST = 0.0005
GPT_3_5_OUTPUT_COST = 0.0015
GPT_4_INPUT_COST = 0.01
GPT_4_OUTPUT_COST = 0.03
LLAMA_2_INPUT_COST = GPT_4_INPUT_COST  # Llama-2-70b through Replicate has approximately the same cost as GPT-4-1106-Preview
LLAMA_2_OUTPUT_COST = GPT_4_OUTPUT_COST  # Llama-2-70b through Replicate has approximately the same cost as GPT-4-1106-Preview

presets = {
    "Default": {
        "prompts": ["You are a random pedestrian being chosen for a survey. The question is: Would you rather:"],
        "num_scenarios": 1,
        "num_options": 3,
        "shuffle-checklist": [],
        "iterations": 5,
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
        "shuffle-checklist": [],
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
        "shuffle-checklist": [],
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
        "prompts": ["Suppose you bought a case of good Bordeaux in the futures market for $20 a bottle. The wine now sells at auction for about $75. You have decided to drink a bottle. Which of the following best captures your feeling of the cost to you of drinking the bottle?"],
        "num_scenarios": 1,
        "num_options": 5,
        "shuffle-checklist": ["shuffle_options"],
        "iterations": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-1106-preview", "llama-2-70b"],
        "temperature": 1,
        "answer_texts": ['$0. I already paid for it.', '$20, what I paid for.', '$20, plus interest.', '$75, what I could get if I sold the bottle.', '-$55, I get to drink a bottle that is worth $75 that I only paid $20 for so I save money by drinking the bottle.'],
        "instruction_checklist": ["add_instruction"],
        "instruction_text": ["Please complete the answer by only giving the letter of the answer option A, B, C, D or E."],
    },
}

input_style = {'width': '30%', 'marginBottom': '25px'}


# Page for individual experiment
def answer_option_layout():
    layout = [
        html.Div(
            children=[
                # Dropdown for presets
                html.Div(
                    children=[
                        html.H6("Load Preset", style={'textAlign': 'center'}),
                        dcc.Dropdown(
                            id="preset-dropdown",
                            options=[{"label": preset, "value": preset} for preset in presets.keys()],
                            value="Default",
                            style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'},
                            persistence=True,
                            persistence_type='session',
                        ),
                    ],
                    style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px'},
                ),
                dbc.Tooltip(
                    "Choose the settings of one of the pre-built experiments that you can find in the sidebar.",
                    target="preset-dropdown",
                    placement="top-start",
                ),
                # Left column
                html.Div(
                    children=[
                        html.Div(id='scenarios-container', style={'width': '100%', 'marginBottom': '20px'}),
                    ],
                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '50%'},
                ),
                # Right column
                dbc.Col(
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H5("Select Experiment Configuration")),
                                dbc.CardBody(
                                    children=[
                                        html.H6("Select number of scenarios"),
                                        dbc.Input(
                                            id="num-scenarios",
                                            type="number",
                                            value=1,
                                            min=1,
                                            max=4,
                                            step=1,
                                            style=input_style,
                                            persistence=True,
                                            persistence_type='session',
                                        ),
                                        dbc.Tooltip(
                                            "Each scenario with the corresponding answer options is presented to the selected models",
                                            target="num-scenarios",
                                        ),
                                        html.H6("Select number of answer options"),
                                        dbc.Input(
                                            id="num-answer-options",
                                            type="number",
                                            value=3,
                                            min=2,
                                            max=6,
                                            step=1,
                                            style=input_style,
                                            persistence=True,
                                            persistence_type='session',
                                        ),
                                        dbc.Tooltip(
                                            "Choose the number of answer options (A, B, C, etc.) for each scenario.",
                                            target="num-answer-options",
                                        ),
                                        html.H6("Select number of requests"),
                                        dbc.Input(
                                            id="individual-iterations",
                                            type="number",
                                            value=1,
                                            min=0,
                                            max=500,
                                            step=1,
                                            style=input_style,
                                            persistence=True,
                                            persistence_type='session',
                                        ),
                                        dbc.Tooltip(
                                            "This is how often the LLMs will answer the questions. The more iterations, the more accurate the answer distribution will be. However, the experiment will also be more expensive. The maximum is 500.",
                                            target="individual-iterations",
                                        ),
                                        dbc.Checklist(
                                            id="instruction-checklist",
                                            options=[
                                                {"label": "Add instruction", "value": "add_instruction"}
                                            ],
                                            value=["add_instruction"],
                                            switch=True,
                                            inline=False,
                                            style={'marginBottom': '25px'},
                                            inputStyle={'margin-right': '10px'},
                                            persistence=True,
                                            persistence_type='session',
                                        ),
                                        dbc.Tooltip(
                                            "The instruction role is to guide the LLMs to answer the questions in a specific way. For example, to answer only with the letter of the answer options.",
                                            target="instruction-checklist",
                                        ),
                                        html.Div(id='shuffle-checklist-container'),
                                        html.H6("Select language models"),
                                        dbc.Checklist(
                                            id="individual-model-checklist",
                                            options=[
                                                {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                                                {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                                                {"label": "LLama-2-70b", "value": "llama-2-70b"}
                                            ],
                                            value=["gpt-3.5-turbo"],
                                            inline=False,
                                            style={'marginBottom': '25px', 'lineHeight': '30px'},
                                            inputStyle={'margin-right': '10px'},
                                            persistence=True,
                                            persistence_type='session',
                                        ),
                                        html.Div(
                                            [
                                                html.H6("Select temperature value"),
                                                dcc.Slider(
                                                    id="individual-temperature",
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
                                            style={'width': '100%', 'marginBottom': '40px'}, 
                                        ),
                                        dbc.Tooltip(
                                            "The temperature value controls the randomness of the models' responses. A higher temperature value will result in more random answers, while a lower temperature value will result in more deterministic responses.",
                                            target="individual-temperature",
                                        ),
                                        dbc.Button('Run the experiment', id='individual-update-button', 
                                                    n_clicks=None, style={'marginBottom': '25px', 'width': '100%'}),
                                        html.Div(id='cost-estimate-container'),
                                        dbc.Spinner(
                                            html.Div(id="loading-output", 
                                                     style={'textAlign': 'center', 'word-wrap': 'break-word'}), 
                                            color="primary"),
                                    ],
                                    style={'display': 'flex', 'flexDirection': 'column', 'width': '100%'}
                                ),
                            ],   
                            style={'width': '55%'}
                        ),
                    ],
                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '100%'},
                ),
            ],
            style={'display': 'flex', 'flexWrap': 'wrap'}
        ),  
        html.Hr(),
        # Results
        html.Div(id='experiment_results'),
        html.Div(
            style={'display': 'flex'},
            children=[
                html.Div(
                    style={'width': '70%', 'padding': '20px'},
                    children=[
                        dbc.Col(dcc.Graph(id="graph_1"))
                    ]
                ),
                html.Div(
                    style={'width': '30%', 'padding': '20px'},
                    children=[
                        html.Div(id="graph_settings")
                    ]
                ),
            ],
        ),
        html.Div(id='raw-model-answers')
    ]
    
    return layout


#################### Callbacks ####################


# Callback to dynamically generate new scenarios and answer options
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
    answer_textarea_style = {'width': '100%', 'height': 60} 
    
    # Generate scenarios textareas
    for i in range(num_scenarios):
        container.extend([
            html.Div(
                children=[
                    html.Label(f"Scenario {i+1}:", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold'}),
                    dbc.Textarea(
                        id={"type": "individual-prompt", "index": i},
                        value="You are a random pedestrian being chosen for a survey. The question is: Would you rather:",
                        style={'width': '100%', 'height': 110},
                        persistence=True,
                        persistence_type='session',
                    ),
                ],
                style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px'},
            ),
        ])
        # Generate answer options textareas
        for j in range(num_options):
            container.extend([
                html.H6(f"Answer option {answer_option_labels[j]}:", style={'marginTop': '10px'}),
                dbc.Textarea(
                    id={"type": "individual-answer", "index": count},
                    value=placeholder_text[j],
                    style=answer_textarea_style,
                    persistence=True,
                    persistence_type='session',
                )
            ])
            count += 1
        
        # Generate instruction textarea
        if "add_instruction" in instruction:
            container.extend([
                html.Label(f"Instruction:", style={'textAlign': 'center', 'marginTop': '20px'}),
                dbc.Textarea(
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


# Callbacks to load preset values into the input elements
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
        Output({"type": "instruction-text", "index": ALL}, "value"),
        Output("shuffle-checklist", "value")
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
        preset_values["shuffle-checklist"],
    )
    
    
# Callback for cost estimate
@dash.callback(
    [
        Output("cost-estimate-container", "children"),
    ],
    [
        Input({"type": "individual-prompt", "index": ALL}, "value"),
        Input({"type": "individual-answer", "index": ALL}, "value"),
        Input("individual-iterations", "value"),
        Input("individual-model-checklist", "value"),
        Input("shuffle-checklist", "value"),
    ]
)
def update_cost_estimate(prompts, answers, iterations, models, shuffle_checklist):
    # Function to count words in a list of sentences
    def count_words(sentences_list):
        word_count = sum(len(sentence.split()) for sentence in sentences_list)
        return word_count
    
    # Calculate total tokens (if shuffle options is selected, multiply by 3)
    multiplier = 3 if "shuffle_options" in shuffle_checklist else 1
    total_tokens = (count_words(prompts) + count_words(answers)) * iterations * multiplier
    
    # Calculate estimated cost
    estimated_cost = 0
    if "gpt-3.5-turbo" in models:
        estimated_cost += GPT_3_5_INPUT_COST * (total_tokens / 1000) + GPT_3_5_OUTPUT_COST * (1/1000)
    if "gpt-4-1106-preview" in models:
        estimated_cost += GPT_4_INPUT_COST * (total_tokens / 1000) + GPT_4_OUTPUT_COST * (1/1000)
    if "llama-2-70b" in models:
        estimated_cost += LLAMA_2_INPUT_COST * (total_tokens / 1000) + LLAMA_2_OUTPUT_COST * (1/1000)
    
    
    cost_estimate = html.Div(
        [
            html.P(f"Estimated cost for Experiment: {estimated_cost:.2f} USD",
                    id='cost-estimate',
                    style={'text-align': 'center', 'marginBottom': '25px'}),
            dbc.Tooltip(
                "The costs depends on the number of tokens used in the experiment, the number of iterations, and the selected models. The costs are estimated based on the current token prices of the models. The costs of using the Replicate API (LLama-2-70b) can only be estimated and are approximately the same as for GPT-4-1101-Preview.",
                target="cost-estimate",
            )
        ]
    )
    
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
    # If there is only one scenario, show the shuffle checklist
    if num_scenarios == 1:
        return [[dbc.Checklist(
                    id="shuffle-checklist",
                    options=[
                        {"label": "Shuffle answer options", "value": "shuffle_options"}
                    ],
                    inline=False,
                    style={'marginBottom': '20px'},
                    inputStyle={'margin-right': '10px'},
                    switch=True,
                    persistence=True,
                    persistence_type='session',
                ),
                dbc.Tooltip(
                    "The order of the answer options will be shuffled two times if activated. This is to determine whether the order of the answer options has an influence on the answers of the models.",
                    target="shuffle-checklist",
                )
                ]]
    else:
        return [html.Div(id="shuffle-checklist")]

    
# Callback to run individual live experiment
@dash.callback(
    [
        Output("loading-output", "children"),
        Output("experiment_results", "children"),
        Output("graph_settings", "children"),
        Output("raw-model-answers", "children"),
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
        State("shuffle-checklist", "value"),
        State("user-api-keys", "data")
    ],
    prevent_initial_call=True
)
def update_individual_experiment(n_clicks, prompts, models, iterations, temperature, 
                                 num_options, answer_values, instruction_checklist, 
                                 instruction_text, shuffle_checklist, api_keys):
    # Check if button was clicked
    if n_clicks is not None:  
        
        # Check if shuffle option is selected
        if shuffle_checklist is not None:
            if "shuffle_options" in shuffle_checklist:
                shuffle_option = True
            else:
                shuffle_option = False
        else:
            shuffle_option = False
        
        # Create experiment object
        experiment = Experiment(
            api_keys=api_keys,
            experiment_type='answer_options',
            prompts=prompts,
            answers=answer_values,
            iterations=iterations,
            models=models,
            temperature=temperature,
            num_options=num_options,
            instruction_checklist=instruction_checklist,
            instructions=instruction_text,
            shuffle_option=shuffle_option,
        )
        
        # Run the experiment and catch errors
        try:
            experiment.run()
        except Exception as e:
            error_message = dbc.Alert(f'An error occurred: "{str(e)}". Please try again.', color="danger")
            return error_message, None, None, None
        
        n_clicks = None
        
        # Generate the output table 
        output_table = dash_table.DataTable(
            id='output-table',
            columns=[{'name': col, 'id': col} for col in experiment.results_df.columns],
            data=experiment.results_df.to_dict('records'),
            style_table={'margin-top': '10px', 'margin-bottom': '30px'},
            export_format='csv',
            persistence=True,
            persistence_type='session',
        )

        # Generate the results
        results = [
            html.H2("Results:", style={'margin-top': '50px', 'margin-bottom': '30px'}),
            html.Br(),
            dbc.Alert(
                "The share of correct answers (correct answers / iterations) is below 50% for at least one experiment. This might indicate that the models were not able to answer the questions correctly. Scroll down to see the raw answers of the models. It is helpful to guide the model to answer in the required format by using the instruction role or by writing it in the scenario text.",
                color="warning"
            ) if experiment.low_answers_share_warning else None,
            output_table
        ]
        
        # Generate graph settings
        graph_settings = html.Div(
            [
                html.Div([html.H3("Graph Settings")], style={'margin-bottom': '20px'}),
                html.Div(
                    [
                        html.H6('X-Axis'),
                        dcc.Dropdown(
                            id="graph_x_axis",
                            options=[
                                {"label": "Model", "value": "Model"},
                                {"label": "Scenario", "value": "Scenario"},
                            ],
                            value="Model",
                            style={'marginBottom': '20px'},
                            persistence=True,
                            persistence_type='session',
                        ),
                    ]
                ),
                html.Div(id="graph_groupby_container"),
            ]
        )
        
        # Generate alert for finished experiment
        loading = dbc.Alert("The experiment finished running. Please check the results below.", color="success")
        
        
        # Function to generate nested html to display raw model answers
        def generate_nested_html(dictionary):
            items = []
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    sublist = generate_nested_html(value)
                    items.append(html.Li([html.Strong(key + ": "), html.Ul(sublist)]))
                else:
                    items.append(html.Li([html.Strong(f"Scenario {key+1}: "), str(value)]))
            return items
        
        # Generate raw model answers
        items = generate_nested_html(experiment.raw_model_answers_dict)
        # Add header
        raw_model_answers = [
            html.H5("Raw model answers:"),
            html.Ul(items)
        ]


        return loading, results, graph_settings, raw_model_answers
    

# Callback to display graph settings
@dash.callback(
    [
        Output("graph_groupby_container", "children"),
    ],
    [
        Input("graph_x_axis", "value"),
        Input("output-table", "data"),
    ],
)
def graph_settings(x_axis, data):
    
    df = pd.DataFrame(data)
    
    # Generate groupby container
    if x_axis == "Model":
        groupby_container = html.Div(
            [
                html.H6('Select Scenario'),
                dcc.Dropdown(
                    id="graph_groupby",
                    options=[
                        {"label": scenario, "value": scenario}
                        for scenario in df["Scenario"].unique()
                    ],
                    value=df["Scenario"].unique()[0],
                    style={'marginBottom': '20px'},
                    persistence=True,
                    persistence_type='session',
                ),
            ]
        )
    else:
        groupby_container = html.Div(
            [
                html.H6('Select Model'),
                dcc.Dropdown(
                    id="graph_groupby",
                    options=[
                        {"label": model, "value": model}
                        for model in df["Model"].unique()
                    ],
                    value=df["Model"].unique()[0],
                    persistence=True,
                    persistence_type='session',
                ),
            ]
        )
    
    return [groupby_container]


# Callback to plot results
@dash.callback(
    [
        Output("graph_1", "figure"),
    ],
    [
        Input("graph_x_axis", "value"),
        Input("graph_groupby", "value"),
        Input("output-table", "data"),
        Input("individual-iterations", "value"),
        Input("individual-temperature", "value"),
    ],
)
def update_graph(x_axis, groupby, data, iterations, temperature):
    
    df = pd.DataFrame(data)
    
    figure = plot_results(df, x_axis, groupby, iterations, temperature)
    
    return [figure]
