# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
from PIL import Image
from ast import literal_eval
import pickle
import os 
from utils.plotting_functions import PT_plot_results
from utils.plotting_functions import PT2_plot_results
from utils.plotting_functions import PT_plot_og_results


dash.register_page(__name__, path='/prospect-theory', name='Prospect Theory', location='experiments')


# Load in results and graphs of Prospect Theory experiments
PT_probs = pd.read_csv("data/Output/PT_probs.csv")

# Second Prospect Theory experiment
PT2_probs = pd.read_csv("data/Output/PT2_probs.csv")
PT_og_results = pd.read_csv("data/Input/PT_og_results.csv")



### Prospect Theory 1 ###

# Prompts for PT experiments
with open ("data/Input/PT_prompts.pkl", "rb") as file:
    PT_prompts = pickle.load(file)


# Load PT prompt dictionary
with open ("data/Input/PT_dictionaries.pkl", "rb") as file:
    PT_dictionaries = pickle.load(file)
PT_experiment_prompts_dict = PT_dictionaries[0]


### Prospect Theory 2 ###

# Scenario 1
with open("data/Input/PT2_prompts_1.pkl", "rb") as file:
    PT2_prompts_1 = pickle.load(file)

# Scenario 2
with open("data/Input/PT2_prompts_2.pkl", "rb") as file:
    PT2_prompts_2 = pickle.load(file)

# Scenario 3
with open("data/Input/PT2_prompts_3.pkl", "rb") as file:
    PT2_prompts_3 = pickle.load(file)

# Scenario 4
with open("data/Input/PT2_prompts_4.pkl", "rb") as file:
    PT2_prompts_4 = pickle.load(file)

# Load PT2 prompt dictionary
with open("data/Input/PT2_dictionaries.pkl", "rb") as file:
    PT2_dictionaries = pickle.load(file)
PT2_experiment_prompts_dict = PT2_dictionaries[0]


# Prospect Page
layout = [
     html.H1("Prospect Theory and Mental Accounting Experiment", className="page-heading"),
     html.Hr(),
     html.P(["""According to Prospect Theory and Mental Accounting, financial gains and losses are booked into different fictitious accounts. On top of that, 
            relative to a reference point, losses weigh more heavily than gains and the perceived sum of two individual gains/losses will, in absolute terms, be larger than 
            one single gain/loss of the same amount. In the context of Marketing, four main rules can be derived by this theory:""",
            html.Br(),
            html.Br(),
            "1) Segregation of gains",
            html.Br(),
            "2) Integration of losses",
            html.Br(), 
            "3) Cancellation of losses against larger gains",
            html.Br(),
            "4) Segregation of silver linings",
            html.Br(),
            html.Br(),
            """One possible practical implication each of these rules hold, is each reflected in the different scenarios we examine below.""",
            html.Br(),
            """In order to research how Large Language models react to this kind of experiment, we queried multiple models over different temperature values and used either primed 
            or unprimed prompts. The results of our experiments are visualized below. The original results are taken
            from Thaler, Richard (1985), “Mental Accounting and Consumer Choice,” Marketing Science, 4 (3), 199–214 and the prompts we query the Language Models with are
            constructed so that we can stay as close to the original phrasing as possible, while still instructing the models sufficiently well to produce meaningful results.
            For every scenario, the participants could decide on either Mister A, Mister B or a No-difference option.
            In the case of primed experiments, we instructed the model to be a market researcher, that knows about Prospect Theory and Mental Accounting.""",
            html.Br(),
            html.Br(),
            ]),

html.H2("Experiment 1: Recreating the original study"),
html.Br(),
# Scenario 1: Segregation of gains
html.Div(
    children=[
        html.H3("Scenario 1: Segregation of gains"),
        html.Hr(),
        html.Div(
            children=[
                html.P(
                    [   html.Br(),
                        html.Br(),
                        "The original phrasing, used in the experiment by Thaler, is as follows:",
                        html.Br(),
                        "Mr. A was given tickets to lotteries involving the World Series. He won $50 in one lottery and $25 in the other. ",
                        "Mr. B was given a ticket to a single, larger World Series lottery. He won $75. Who was happier?",
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ],
                ),
            ],
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario1-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario1-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario1-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot1", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario1-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    )]),

    
# Scenario 2: Integration of losses
html.Div(
    children=[
        html.H3("Scenario 2: Integration of losses"),
        html.Hr(),
        html.Div(
            children=[
                html.P(
                    [   html.Br(),
                        html.Br(),
                        "The original phrasing, used in the experiment by Thaler, is as follows:",
                        html.Br(),
                        """Mr. A received a letter from the IRS saying that he made a minor arithmetical mistake on his
                        tax return and owed $100. He received a similar letter the same day from his state income tax
                        authority saying he owed $50. There were no other repercussions from either mistake.""",
                        html.Br(),
                        """Mr. B received a letter from the IRS saying that he made a minor arithmetical mistake on his tax
                        return and owed $150. There were no other repercussions from his mistake. Who was more upset?""",
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
               


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario2-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario2-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario2-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot2", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario2-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    )]),

    
# Scenario 3: Cancellation of losses against larger gains
html.Div(
    children=[
        html.H3("Scenario 3: Cancellation of losses against larger gains"),
        html.Hr(),
        html.Div(
            children=[
                html.P(
                    [   html.Br(),
                        html.Br(),
                        "The original phrasing, used in the experiment by Thaler, is as follows:",
                        html.Br(),
                        """Mr. A bought his first New York State lottery ticket and won $100. Also, in a freak accident,
                        he damaged the rug in his apartment and had to pay the landlord $80.""",
                        html.Br(),
                        "Mr. B bought his first New York State lottery ticket and won $20. Who was happier",
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                
            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario3-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario3-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario3-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot3", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario3-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    )]),

# Scenario 4: Segregation of silver linings
html.Div(
    children=[
        html.H3("Scenario 4: Segregation of silver linings"),
        html.Hr(),
        html.Div(
            children=[
                html.P(
                    [   html.Br(),
                        html.Br(),
                        "The original phrasing, used in the experiment by Thaler, is as follows:",
                        html.Br(),
                        """Mr. A's car was damaged in a parking lot. He had to spend $200 to repair the damage. 
                        The same day the car was damaged, he won $25 in the office football pool.""",
                        html.Br(),
                        "Mr. B's car was damaged in a parking lot. He had to spend $175 to repairthe damage. Who was more upset?",
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
            


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario4-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario4-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario4-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot4", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario4-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    )]),

html.Br(),
html.Hr(),


## Experiment 2
html.H2("Experiment 2: Odd numbers and unfair scenarios"),
html.Hr(),
html.P(["""The Prospect Theory value function explains why individuals tend to assess the perceived value of e.g. a sum of multiple gains as larger, 
        than one individual sum of the same amount. Since Large Language Models are trained on human data, including for example customer reviews on sales platforms,
        they might reflect these patterns.""",
        html.Br(), 
        """But how do LLMs react, if in the given scenarios, one individual is financially clearly better off than the other? And what if we did not deal with small,
        even numbers, but rather large and odd ones?""",
        html.Br(),
        "Another ", html.B("key concept of prospect theory is decreasing sensitivity"),":", 
        " A loss of 50$ subtracted from a total amount of 1000$ will not hurt as much, as if we initially only had 100$, hence losing 50% of our total possession.", 
        html.Br(),
        html.Br(),
        "In order to research these 2 aspects, we created 6 configurations for every scenario (1-4):",
        html.Br(),
        html.Br(),
        "- Configuration 1: Original numbers scaled by factor Pi * 100",
        html.Br(),
        "- Configuration 2: Original numbers scaled by factor Pi * 42",
        html.Br(),
        "- Configuration 3: A is better off by 25$",
        html.Br(),
        "- Configuration 4: A is better off by 50$",
        html.Br(),
        "- Configuration 5: B is better off by 25$",
        html.Br(),
        "- Configuration 6: B is better off by 50$",
        html.Br()]),
html.Div(
        children = [
            html.Div(
                children = [
                    html.Label("Select scenario", style={'margin': 'auto'}),
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
                    html.Label("Select language model", style={'margin': 'auto'}),
                    dcc.Dropdown(
                         id = "prospect2-model-dropdown",
                         options = [
                                {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                                {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                                {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                            style = {'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                        html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect2-temperature-slider",
                            min=0.5,
                            max=1.5,
                            marks={0.5: '0.5', 1: '1', 1.5: '1.5'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                    ],                 
    
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
            ),
            dcc.Graph(id = "prospect2-plot", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect2-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    ),
    html.Hr(),
    # Display of original results
    html.Div( 
    children=[
        html.Br(),
        html.H4("Comparison to original study", style={'margin-bottom': '0px'}),
        html.Div(
            style={'display': 'flex', 'align-items': 'center'},  
            children=[
            html.P(
                [
                    html.Br(),
                    html.Br(),
                    """In Experiment 2: Odd numbers and unfair scenarios, we purposely deviated from the original study design. Although this helps research to what 
                    extent the models' answers may somehow be influenced by the original study,  we do not observe a ground truth, i.e. original results. """,
                    html.Br(),
                    """Therefore, the graph on the right helps compare the models' answers to the original results. However, we have to keep in mind, that 
                    this can merely serve as some from of orientation, because the actual questions asked in the original experiments were, in terms of absolute values,
                    not identical to our prompts.""",
                    html.Br(),
                    html.Br(),
                    "Along the x-axis, the different scenarios are listed, being:",
                    html.Br(),
                    "Scenario 1: Segregation of gains",
                    html.Br(),
                    "Scenario 2: Integration of losses",
                    html.Br(),
                    "Scenario 3: Cancellation of losses against larger gains",
                    html.Br(),
                    "Scenario 4: Segregation of silver linings",
                ],
                style={'width': '30%', 'margin-bottom': '50px'}
            ),  # plot with original results 
                dcc.Graph(id="prospect2-og-plot", style={'width': '70%', 'height': '60vh', 'margin': 'auto'}),
            ]
        ),
    ]
)
]



### Callback for prospect page

## Experiment 1
# Scenario 1
@dash.callback(
     [Output("prospect-plot1", "figure"),
      Output("prospect-scenario1-prompt", "children")],
     [Input("prospect-scenario1-priming-dropdown", "value"), 
      Input("prospect-scenario1-model-dropdown", "value"),
      Input("prospect-scenario1-temperature-slider", "value")] 

)
def update_prospect1(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 1)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    print(os.getcwd())
    return PT_plot_results(df), prompt 

# Scenario 2
@dash.callback(
        [Output("prospect-plot2", "figure"),
         Output("prospect-scenario2-prompt", "children")],
        [Input("prospect-scenario2-priming-dropdown", "value"), 
        Input("prospect-scenario2-model-dropdown", "value"),
        Input("prospect-scenario2-temperature-slider", "value")] 

)
def update_prospect2(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 2)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return PT_plot_results(df), prompt 

# Scenario 3
@dash.callback(
        [Output("prospect-plot3", "figure"),
         Output("prospect-scenario3-prompt", "children")],
        [Input("prospect-scenario3-priming-dropdown", "value"), 
        Input("prospect-scenario3-model-dropdown", "value"),
        Input("prospect-scenario3-temperature-slider", "value")] 

)
def update_prospect3(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 3)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return PT_plot_results(df), prompt 

# Scenario 4
@dash.callback(
        [Output("prospect-plot4", "figure"),
         Output("prospect-scenario4-prompt", "children")],
        [Input("prospect-scenario4-priming-dropdown", "value"), 
        Input("prospect-scenario4-model-dropdown", "value"),
        Input("prospect-scenario4-temperature-slider", "value")] 

)
def update_prospect4(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 4)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return PT_plot_results(df), prompt 

## Experiment 2
@dash.callback(
        [Output("prospect2-plot", "figure"),
         Output("prospect2-prompt", "children"),
         Output("prospect2-og-plot", "figure")],
        [Input("prospect2-scenario-dropdown", "value"), 
        Input("prospect2-configuration-dropdown", "value"),
        Input("prospect2-model-dropdown", "value"),
        Input("prospect2-temperature-slider", "value")] 

)
def update_prospect_two(selected_scenario, selected_configuration, selected_model, selected_temperature):
    df = PT2_probs[(PT2_probs["Scenario"] == selected_scenario) & (PT2_probs["Configuration"] == selected_configuration) &
                   (PT2_probs["Model"] == selected_model) & (PT2_probs["Temp"] == selected_temperature)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT2_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    og_plot = PT_plot_og_results(PT_og_results) # Also being replotted for every new input right now. Not optimal, but no big issue. 
    return PT2_plot_results(df), prompt, og_plot 