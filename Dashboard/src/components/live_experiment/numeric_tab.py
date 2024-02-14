# Import required libraries 
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html, State, dash_table
import json

# Local imports
from utils.experiment import Experiment
from utils.plotting import plot_results_numeric


# Constants
GPT_3_5_INPUT_COST = 0.0005
GPT_3_5_OUTPUT_COST = 0.0015
GPT_4_INPUT_COST = 0.01
GPT_4_OUTPUT_COST = 0.03
LLAMA_2_INPUT_COST = GPT_4_INPUT_COST  # Llama-2-70b through Replicate has approximately the same cost as GPT-4-1106-Preview
LLAMA_2_OUTPUT_COST = GPT_4_OUTPUT_COST  # Llama-2-70b through Replicate has approximately the same cost as GPT-4-1106-Preview


input_style = {'width': '30%', 'marginBottom': '25px'}

def numeric_layout():
    layout = [
        dcc.Store(id='experiment-data-numeric', storage_type='session'),
        html.Div(
            children=[
                # Left column
                html.Div(
                    children=[
                        html.Div(id='scenarios-container-numeric', style={'width': '100%', 'marginBottom': '20px'}),
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
                                            id="num-scenarios-numeric",
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
                                                    "Each scenario is presented to the selected models",
                                                    target="num-scenarios-numeric",
                                                ),
                                        html.H6("Select number of requests"),
                                        dbc.Input(
                                            id="individual-iterations-numeric",
                                            type="number",
                                            value=5,
                                            min=0,
                                            max=500,
                                            step=1,
                                            style=input_style,
                                            persistence=True,
                                            persistence_type='session',
                                        ),
                                        dbc.Tooltip(
                                            "This is how often the LLMs will answer the questions. The more iterations, the more accurate the answer distribution will be. However, the experiment will also be more expensive. The maximum is 500.",
                                            target="individual-iterations-numeric",
                                        ),
                                        dbc.Checklist(
                                            id="instruction-checklist-numeric",
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
                                            "The instruction role is to guide the LLMs to answer the questions in a specific way. For example, to answer with a dollar amount only.",
                                            target="instruction-checklist-numeric",
                                        ),
                                        html.H6("Select language models"),
                                        dbc.Checklist(
                                            id="individual-model-checklist-numeric",
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
                                                    id="individual-temperature-numeric",
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
                                            target="individual-temperature-numeric",
                                        ),
                                        dbc.Button('Run the experiment', id='individual-update-button-numeric', 
                                                        n_clicks=None, style={'marginBottom': '25px', 'width': '100%'}),
                                        html.Div(id='cost-estimate-numeric-container'),
                                        dbc.Spinner(
                                            html.Div(id="loading-output-numeric", 
                                                     style={'textAlign': 'center'}),
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
        html.Div(id='experiment-prompt-numeric'),
        html.Div(dcc.Graph(id="graph_1-numeric")),
        html.Div(id='raw-model-answers-numeric')
    ]
    
    return layout


# Callback to dynamically generate new scenarios
@dash.callback(
    Output('scenarios-container-numeric', 'children'),
    [Input('num-scenarios-numeric', 'value'),
     Input('instruction-checklist-numeric', 'value')]
)

def update_num_scenarios(num_scenarios, instruction):
    
    container = []
    
    answer_textarea_style = {'width': '100%', 'height': 30} 
    
    # Generate scenarios textareas
    for i in range(num_scenarios):
        container.extend([
            html.Div(
                children=[
                    html.Label(f"Scenario {i+1}:", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold'}),
                    dbc.Textarea(
                        id={"type": "individual-prompt-numeric", "index": i},
                        value="How much does a chair cost?",
                        style={'width': '100%', 'height': 100},
                        persistence=True,
                        persistence_type='session',
                    ),
                ],
                style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px'},
            ),
        ])
        
        # Add instruction textarea
        if "add_instruction" in instruction:
            container.extend([
                html.Label(f"Instruction:", style={'textAlign': 'center', 'marginTop': '20px'}),
                dbc.Textarea(
                    id={"type": "instruction-text-numeric", "index": i},
                    value='Answer by only giving a single price in dollars and cents without an explanation.',
                    style=answer_textarea_style, 
                    persistence=True,
                    persistence_type='session',
                )
            ])
            
        # Add a larger space between scenarios
        container.append(html.Div(style={'height': '60px'}))
    
    return container



# Callback for cost estimate
@dash.callback(
    [
        Output("cost-estimate-numeric-container", "children"),
    ],
    [
        Input({"type": "individual-prompt-numeric", "index": ALL}, "value"),
        Input("individual-iterations-numeric", "value"),
        Input("individual-model-checklist-numeric", "value"),
    ]
)
def update_cost_estimate(prompts, iterations, models):
    # Function to count words in a list of sentences
    def count_words(sentences_list):
        word_count = sum(len(sentence.split()) for sentence in sentences_list)
        return word_count
    
    # Calculate the total number of tokens
    total_tokens = count_words(prompts) * iterations
    
    # Calculate the estimated cost
    estimated_cost = 0
    if "gpt-3.5-turbo" in models:
        estimated_cost += GPT_3_5_INPUT_COST * (total_tokens / 1000) + GPT_3_5_OUTPUT_COST * (5/1000)
    if "gpt-4-1106-preview" in models:
        estimated_cost += GPT_4_INPUT_COST * (total_tokens / 1000) + GPT_4_OUTPUT_COST * (5/1000)
    if "llama-2-70b" in models:
        estimated_cost += LLAMA_2_INPUT_COST * (total_tokens / 1000) + LLAMA_2_OUTPUT_COST * (5/1000)
    
    cost_estimate = html.Div(
        [
            html.P(f"Estimated cost for Experiment: {estimated_cost:.2f} USD",
                    id='cost-estimate-numeric',
                    style={'text-align': 'center', 'marginBottom': '25px'}),
            dbc.Tooltip(
                "The costs depends on the number of tokens used in the experiment, the number of iterations, and the selected models. The costs are estimated based on the current token prices of the models. The costs of using the Replicate API (LLama-2-70b) can only be estimated and are approximately the same as for GPT-4-1101-Preview.",
                target="cost-estimate-numeric",
            )
        ]
    )
    
    return [cost_estimate]



# Callback to run individual live experiment
@dash.callback(
    [
        Output("loading-output-numeric", "children"),
        Output("experiment-prompt-numeric", "children"),
        Output("experiment-data-numeric", "data"),
        Output("raw-model-answers-numeric", "children")
    ],
    [
        Input("individual-update-button-numeric", "n_clicks")
    ],
    [
        State({"type": "individual-prompt-numeric", "index": ALL}, "value"),
        State("individual-model-checklist-numeric", "value"),
        State("individual-iterations-numeric", "value"),
        State("individual-temperature-numeric", "value"),
        State("instruction-checklist-numeric", "value"),
        State({"type": "instruction-text-numeric", "index": ALL}, "value"),
        State("user-api-keys", "data")
    ],
    prevent_initial_call=True
)
def update_individual_experiment(n_clicks, prompts, models, iterations, temperature, 
                                 instruction_checklist, instruction_text, api_keys):
    # Check if button was clicked
    if n_clicks is not None:  
        
        # Create experiment object
        experiment = Experiment(
            api_keys=api_keys,
            experiment_type='numeric',
            prompts=prompts,
            answers=None,
            iterations=iterations,
            models=models,
            temperature=temperature,
            num_options=None,
            instruction_checklist=instruction_checklist,
            instructions=instruction_text,
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
            output_table,
        ]
        
        # Generate alert if the experiment finished running
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

        return [loading, results, experiment.model_answers_dict, raw_model_answers]
    

# Callback to plot results
@dash.callback(
    [
        Output("graph_1-numeric", "figure"),
    ],
    [
        Input("experiment-data-numeric", "data"),
    ]
)
def plot_results(data):
    df = pd.DataFrame(data)
    
    figure = plot_results_numeric(df)
    
    return [figure]
