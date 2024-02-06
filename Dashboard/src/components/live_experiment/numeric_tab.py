# Import required libraries 
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html, State, dash_table

# Local imports
from utils.experiment import Experiment
from utils.plotting import plot_results_numeric



input_style = {'width': '25%', 'marginBottom': '25px'}

def numeric_layout():
    layout = [
        dcc.Store(id='experiment-data-numeric', storage_type='session'),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(id='scenarios-container-numeric', style={'width': '100%', 'marginBottom': '20px'}),
                    ],
                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '50%'},
                ),
                html.Div(
                    children=[
                        # Right column
                        dbc.Card(
                            children=[
                                html.H3("Experiment Settings", style={'marginBottom': '30px'}),
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
                                html.H6("Select number of requests"),
                                dbc.Input(
                                    id="individual-iterations-numeric",
                                    type="number",
                                    value=1,
                                    min=0,
                                    max=100,
                                    step=1,
                                    style=input_style,
                                    persistence=True,
                                    persistence_type='session',
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
                                        html.H6("Select Temperature value"),
                                        dcc.Slider(
                                            id="individual-temperature-numeric",
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
                                    style={'width': '100%', 'marginBottom': '40px'}, 
                                ),
                                # Add a button to trigger callback
                               dbc.Button('Run the experiment', id='individual-update-button-numeric', 
                                            n_clicks=None, style={'marginBottom': '25px', 'width': '100%'}),
                                html.Div(id='cost-estimate-numeric'),
                                dbc.Spinner(html.Div(id="loading-output-numeric", style={'textAlign': 'center'})),
                            ],
                            style={'padding': '20px', 'width': '55%', 'marginBottom': '30px'},
                        ),
                    ],
                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '50%'},
                ),
            ],
            style={'display': 'flex', 'flexWrap': 'wrap'}
        ),  
        html.Hr(),
        # Additional text section
        html.Div(id='experiment-prompt-numeric'),
        html.Div(
            style={'display': 'flex'},
            children=[
                html.Div(
                    style={'width': '70%', 'padding': '20px'},
                    children=[
                        dbc.Col(dcc.Graph(id="graph_1-numeric"))
                    ]
                ),
                html.Div(
                    style={'width': '30%', 'padding': '20px'},
                    children=[
                        html.Div(id="graph_settings-numeric")
                    ]
                ),
            ],
        )
        ,
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
    count = 0
    
    answer_textarea_style = {'width': '100%', 'height': 30} 
    
    for i in range(num_scenarios):
        container.extend([
            html.Div(
                children=[
                    html.Label(f"Scenario {i+1}:", style={'textAlign': 'center', 'font-size': '18px', 'font-weight': 'bold'}),
                    dcc.Textarea(
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
        
        if "add_instruction" in instruction:
            container.extend([
                html.Label(f"Instruction:", style={'textAlign': 'center', 'marginTop': '20px'}),
                dcc.Textarea(
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



# Callback to run individual live experiment
@dash.callback(
    [
        Output("loading-output-numeric", "children"),
        Output("experiment-prompt-numeric", "children"),
        Output("experiment-data-numeric", "data")
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
            
        # Run experiment
        experiment.run()
        
        n_clicks = None
        
        # Generate the output table 
        output_table = dash_table.DataTable(
            id='output-table',
            columns=[{'name': col, 'id': col} for col in experiment.results_df.columns],
            data=experiment.results_df.to_dict('records'),
            style_table={'margin-top': '10px', 'margin-bottom': '30px'},
            export_format='csv'
        )

        results = (
            [html.H2("Results:", style={'margin-top': '50px', 'margin-bottom': '30px'})] +
            [html.Br()] +
            [output_table]
        )
        
        loading = html.H6('The experiment finished running. Please check the results below.')

        return [loading, results, experiment.model_answers_dict]
    
    
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


# Callback for cost estimate
@dash.callback(
    [
        Output("cost-estimate-numeric", "children"),
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
    
    total_tokens = count_words(prompts) * iterations
    
    estimated_cost = 0
    if "gpt-3.5-turbo" in models:
        estimated_cost += 0.001 * (total_tokens / 1000) + 0.002 * (5/1000)
    if "gpt-4-1106-preview" in models:
        estimated_cost += 0.01 * (total_tokens / 1000) + 0.03 * (5/1000)
    
    
    cost_estimate = html.P(f"Estimated cost for OpenAI models: {estimated_cost:.2f} USD",
                           style={'text-align': 'center', 'marginBottom': '25px'})
    
    return [cost_estimate]