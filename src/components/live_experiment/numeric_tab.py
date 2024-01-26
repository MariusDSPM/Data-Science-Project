# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ALL, dcc, html, State, dash_table

# Local imports
from utils.experiment import Experiment


def numeric_layout():
    layout = [
        html.Div(
            children=[
                # Dropdown for presets
                html.Div(
                    children=[
                        html.Label("Load Preset", style={'textAlign': 'center'}),
                    ],
                    style={'width': '100%', 'textAlign': 'center', 'marginBottom': '20px'},
                ),
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
                                dcc.Checklist(
                                    id="instruction-checklist-numeric",
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
                                    id="num-scenarios-numeric",
                                    type="number",
                                    value=1,
                                    min=1,
                                    max=4,
                                    step=1,
                                    style={'width': '57%', 'margin': 'auto', 'marginBottom': '20px'},
                                    persistence=True,
                                    persistence_type='session',
                                ),
                                html.Label("Select number of requests", style={'textAlign': 'center'}),
                                dbc.Input(
                                    id="individual-iterations-numeric",
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
                                    id="individual-model-checklist-numeric",
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
                                            style={'width': '65%', 'margin': 'auto', 'marginBottom': '20px'}, 
                                        ),
                                    ],
                                ),
                                # Add a button to trigger callback
                                html.Button('Run the experiment', id='individual-update-button-numeric', n_clicks=None),
                                html.Div(id='cost-estimate-numeric', style={'margin-top': '20px'})
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
        html.Div(id='experiment_prompt-numeric'),
        html.Div(id="download-dataframe-csv-container-numeric"),
        dcc.Download(id="download-dataframe-csv-numeric"),
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
        Output("experiment_prompt-numeric", "children"),
        # Output("graph_settings", "children")
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
    ],
    prevent_initial_call=True
)
def update_individual_experiment(n_clicks, prompts, models, iterations, temperature, 
                                 instruction_checklist, instruction_text):
    # Check if button was clicked
    if n_clicks is not None:  
        
        # Create experiment object
        experiment = Experiment(
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
            style_table={'margin-top': '50px', 'margin-bottom': '30px'},
        )

        results = (
            [html.H2("Results:", style={'margin-top': '50px', 'margin-bottom': '30px'})] +
            [output_table] +
            [html.Button("Download CSV", id="btn_csv")]
        )

        return [results]