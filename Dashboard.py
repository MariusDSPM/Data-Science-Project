"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""


# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os

# Dictionary to look up which model to use for a given experiment id (used in function call). key: experiment id, value: model name
model_dict = {
    "1_1": "gpt-3.5-turbo",
    "1_2": "gpt-3.5-turbo",
    "1_3": "gpt-3.5-turbo",
    "1_4": "gpt-3.5-turbo",
    "1_5": "gpt-3.5-turbo",
    "1_6": "gpt-3.5-turbo",
    "1_7": "gpt-3.5-turbo",
    "1_8": "gpt-3.5-turbo",
    "2_1": "gpt-4-1106-preview",
    "2_2": "gpt-4-1106-preview",
    "2_3": "gpt-4-1106-preview",
    "2_4": "gpt-4-1106-preview",
    "2_5": "gpt-4-1106-preview",
    "2_6": "gpt-4-1106-preview",
    "2_7": "gpt-4-1106-preview",
    "2_8": "gpt-4-1106-preview",
    }

# Dictionary to look up, what the study design of each experiment was. key: experiment id, value: experiment design 
experiment_dict = {
    "1_1": f"Experiment 1_1 uses {model_dict['1_1']}, deals with the segregation of gains and is unprimed.",
    "1_2": f"Experiment 1_2 uses {model_dict['1_2']}, deals with the integration of losses and is unprimed.",
    "1_3": f"Experiment 1_3 uses {model_dict['1_3']}, deals with the cancellation of losses against larger gains and is unprimed.",
    "1_4": f"Experiment 1_4 uses {model_dict['1_4']}, deals with the segrgation of *silver linings* and is unprimed.",
    "1_5": f"Experiment 1_5 uses {model_dict['1_5']}, deals with the segregation of gains and is primed.",
    "1_6": f"Experiment 1_6 uses {model_dict['1_6']}, deals with the integration of losses and is primed.",
    "1_7": f"Experiment 1_7 uses {model_dict['1_7']}, deals with the cancellation of losses against larger gains and is primed.",
    "1_8": f"Experiment 1_8 uses {model_dict['1_8']}, deals with the segregation of *silver linings*, and is primed.",
    "2_1": f"Experiment 1_1 uses {model_dict['2_1']}, deals with the segregation of gains and is unprimed.",
    "2_2": f"Experiment 1_2 uses {model_dict['2_2']}, deals with the integration of losses and is unprimed.",
    "2_3": f"Experiment 1_3 uses {model_dict['2_3']}, deals with the cancellation of losses against larger gains and is unprimed.",
    "2_4": f"Experiment 1_4 uses {model_dict['2_4']}, deals with the segrgation of *silver linings* and is unprimed.",
    "2_5": f"Experiment 1_5 uses {model_dict['2_5']}, deals with the segregation of gains and is primed.",
    "2_6": f"Experiment 1_6 uses {model_dict['2_6']}, deals with the integration of losses and is primed.",
    "2_7": f"Experiment 1_7 uses {model_dict['2_7']}, deals with the cancellation of losses against larger gains and is primed.",
    "2_8": f"Experiment 1_8 uses {model_dict['2_8']}, deals with the segregation of *silver linings*, and is primed.",
}


#########################################  Data Import Functions  #########################################

# Read in experimental data as dictionary
# Decoy Effect
decoy_dfs = {}
for file in os.listdir("Output/DE_probs_dfs"):
        file_name = file.split(".")[0]
        df = pd.read_csv(f"Output/DE_probs_dfs/{file}", index_col = 0) # Set first column as index column 
        decoy_dfs[file_name] = df

# Load in Prospect Theory results
PT_probs = pd.read_csv("Output/PT_probs.csv", index_col = 0)
 

# Function for getting data of Sunk Cost Experiment 1
def get_sunk_cost_data_1(selected_temperature, selected_sunk_cost):
    sunk_cost_1 = pd.read_csv('Output/Sunk_cost_experiment_1.csv', index_col=0)
    df = sunk_cost_1[(sunk_cost_1['Temperature'] == selected_temperature) & 
                     (sunk_cost_1['Sunk Cost ($)'] == selected_sunk_cost)]
    
    return df

# Function for getting data of Sunk Cost Experiment 2
def get_sunk_cost_data_2(selected_temperature, selected_model):
    df = pd.read_csv('Output/Sunk_cost_experiment_2.csv', index_col=0)
    df = df[(df['Temperature'] == selected_temperature) & 
            (df['Model'] == selected_model) |
            (df['Model'] == 'Real Experiment')]
    
    return df

# Function for getting data of Loss Aversion Experiment
def get_loss_aversion_data(selected_temperature):
    df = pd.read_csv('Output/Loss_aversion_experiment.csv', index_col=0)
    df = df[(df['Temperature'] == selected_temperature)|
            (df['Model'] == 'Real Experiment')] 
    
    return df   
        
        

#########################################  Data Plotting Functions  #########################################

# Function for plotting results of decoy effect/prospect theory experiments
def plot_results(model, priming, df, scenario):
    
    # Get dataframe as specified by user (subset of df)
    df = df[(df['Model'] == model) & (df['Priming'] == priming) & (df['Scenario'] == scenario)]
    # Transpose for plotting
    df = df.transpose()
    
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."]
    
    # Get temperature values
    temperature = df.loc["Temp"]

    fig = go.Figure(data=[
        go.Bar(
            name="p(A)", 
            x=temperature, 
            y=df.loc["p(A)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br>Observations: %{customdata}<extra></extra>",
        ),
        go.Bar(
            name="p(B)", 
            x=temperature, 
            y=df.loc["p(B)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
            
        ),
        go.Bar(
            name="p(C)", 
            x=temperature, 
            y=df.loc["p(C)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
        )
    ])

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        tickmode = 'array',
        tickvals = np.arange(len(temperature)),
        ticktext = temperature,
        title = "Temperature",  
        title_font=dict(size=18),  
    ),
    yaxis = dict(
        title="Probability (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text="Distribution of answers per temperature value",
        x = 0.5,  # Center alignment
        font=dict(size=22),  
    ),
    legend = dict(
        title = dict(text="Probabilities"),
    ),
    bargap = 0.3  # Gap between temperature values
)
    return fig

# Function for plotting Sunk Cost Experiment 1
def plot_sunk_cost_1(selected_temperature, selected_sunk_cost):
    df_sunk_cost = get_sunk_cost_data_1(selected_temperature, selected_sunk_cost)
    
    # Create a bar plot
    fig_sunk_cost = go.Figure()
    fig_sunk_cost.add_trace(go.Bar(
        x=df_sunk_cost['Model'],
        y=df_sunk_cost['Share Theater Performance'],
        name='Share Theater Performance',
        hovertemplate="Theater Performance: %{y:.2f}<extra></extra>"
    ))
    fig_sunk_cost.add_trace(go.Bar(
        x=df_sunk_cost['Model'],
        y=df_sunk_cost['Share Rock Concert'],
        name='Share Rock Concert',
        hovertemplate="Rock Concert: %{y:.2f}<extra></extra>"
    ))
    
    fig_sunk_cost.update_layout(
        barmode='group',
        xaxis=dict(title='Model'),
        yaxis=dict(title='Share', range=[0, 1.1]),
        title=f"Shares for Answer Options (Sunk Cost: ${selected_sunk_cost}, Temperature: {selected_temperature})",
        legend=dict(),
        bargap=0.3  # Gap between models
    )

    return fig_sunk_cost


# Function for plotting Sunk Cost Experiment 2
def plot_sunk_cost_2(selected_temperature, selected_model):
    df = get_sunk_cost_data_2(selected_temperature, selected_model)
    
    # Get unique models and prompts
    models = df['Model'].unique()
    prompts = df['Prompt'].unique()

    # Set the width of the bars
    bar_width = 0.1

    fig = go.Figure()

    # Iterate over each model
    for model in models:
        if model != 'Real Experiment':
            for i, prompt in enumerate(prompts):
                subset = df[df['Prompt'] == prompt]

                if not subset.empty:
                    fig.add_trace(go.Bar(
                        x=np.arange(len(df.columns[3:])) + (i * bar_width),
                        y=subset.iloc[0, 3:].values,
                        width=bar_width,
                        name=f'Answer Option Order {i + 1}',
                        marker=dict(color=f'rgba({i * 50}, 0, 255, 0.6)'),
                        hovertemplate="%{y:.2f}",
                    ))
        elif model == 'Real Experiment':
            fig.add_trace(go.Bar(
                        x=np.arange(len(df.columns[3:])) + ((len(prompts)-1) * bar_width),
                        y=df.iloc[-1, 3:].values,
                        width=bar_width,
                        name='Real Results',
                        marker=dict(color='rgba(0, 0, 0, 0.3)'),
                        hovertemplate="%{y:.2f}",
                    ))


    fig.update_layout(
        barmode='group',
        xaxis=dict(tickvals=np.arange(len(df.columns[3:])) + ((len(prompts) - 1) / 2 * bar_width),
                ticktext=['$0', '$20', '$20 plus interest', '$75', '-$55']),
        yaxis=dict(title='Share', range=[0, 1.1]),
        title=f'Shares for Answer Options (Model: {selected_model}, Temperature: {selected_temperature})',
        legend=dict(title=dict(text="Categories")),
        bargap=0.3  # Gap between bars
    )

    return fig


# Function for plotting Loss Aversion Experiment
def plot_loss_aversion(selected_temperature):
    df = get_loss_aversion_data(selected_temperature)
    
    # Extract unique models
    models = df['Model'].unique()

    # Set up figure
    fig = go.Figure()

    # Plotting bars for 'B' for each prompt
    for i, prompt in enumerate(df['Scenario'].unique()):
        values_B = df[df['Scenario'] == prompt]['B']
        scenario_label = 'Scenario with gains' if prompt == 1 else 'Scenario with losses'
        fig.add_trace(go.Bar(
            x=models,
            y=values_B,
            name=scenario_label,
            offsetgroup=i,
            hovertemplate="%{y:.2f}"
        ))

    # Update layout
    fig.update_layout(
        barmode='group',
        xaxis=dict(tickmode='array', tickvals=list(range(len(models))), ticktext=models),
        yaxis=dict(title='Shares for "B"'),
        title='Shares for "B" (risk-seeking option) by Model and Scenario',
    )
    
    return fig






# Initialize the app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Optics of sidebar
SIDEBAR_STYLE = {
    "position": "fixed", # remains in place when scrolling
    "top": 0, # begins at top of page
    "left": 0, # begins at left of page
    "bottom": 0, # ends at bottom of page
    "width": "16rem", # obvious, rem is "unit" of indentation
    "padding": "1.5rem 1.5rem", # distance of sidebar entries from top and left
    "background-color": "#c8f7f3",
}

# Optics of main page content
CONTENT_STYLE = {
    "margin-left": "18rem", # indentation of main content from left side (sidebar is 16rem wide)
    "margin-right": "2rem", # indentation of main content from right side
    "padding": "2rem 2rem", # distance of main content from top and bottom
}

# Create the sidebar
sidebar = html.Div(
    [
        html.H2("Navigation", className="display-6"),
        html.Hr(),
        html.P(
            "Feel free to explore", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Overview", href = "/experiments/overview"),
                dbc.DropdownMenuItem("Decoy Effect", href="/experiments/decoy"),
                dbc.DropdownMenuItem("Prospect Theory", href="/experiments/prospect"),
                dbc.DropdownMenuItem("Sunk Cost Fallacy", href="/experiments/sunk-cost"),
                dbc.DropdownMenuItem("Ultimatum Game", href="/experiments/ultimatum"),
                dbc.DropdownMenuItem("Loss Aversion", href="/experiments/loss-aversion"),
            ],
            label="Experiments",
            nav=True,
        ),
                dbc.NavLink("Live Experiment", href="/page-2", active="exact"),
                dbc.NavLink("Chatbot", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

#########################################  Experiment Page Designs  #########################################
# Add content for pages
# Start Page
start_page = [
            html.H1("Do Large Language Models Behave like a Human?", className="page-heading"),
            html.P("""Large Language models hold huge potential for a wide range of applications either for private, but also for professional use. 
                   One possible question that is of especially interesting for market research, is whether these models behave human-like enough to be used as surrogates for 
                   human participants in experiments. This dashboard is a first attempt to answer this question."""),
            html.P("Feel free to explore more pages using the navigation menu.")]

# Decoy Page
decoy_page = [
    html.H1("Decoy Effect Experiment", className="page-heading"),
    dcc.Dropdown(
        id="decoy-plot-dropdown",
        options=[
            {'label': 'Experiment 1.1', 'value': 'DE_probs_1_1'},
            {'label': 'Experiment 1.2', 'value': 'DE_probs_1_2'},
            {'label': 'Experiment 1.3', 'value': 'DE_probs_1_3'},
            {'label': 'Experiment 1.4', 'value': 'DE_probs_1_4'},
            {'label': 'Experiment 1.5', 'value': 'DE_probs_1_5'},
            {'label': 'Experiment 1.6', 'value': 'DE_probs_1_6'},
            {'label': 'Experiment 1.7', 'value': 'DE_probs_1_7'},
            {'label': 'Experiment 1.8', 'value': 'DE_probs_1_8'},
            {'label': 'Experiment 2.1', 'value': 'DE_probs_2_1'},
            {'label': 'Experiment 2.2', 'value': 'DE_probs_2_2'},
            {'label': 'Experiment 2.3', 'value': 'DE_probs_2_3'},
            {'label': 'Experiment 2.4', 'value': 'DE_probs_2_4'},
            {'label': 'Experiment 2.5', 'value': 'DE_probs_2_5'},
            {'label': 'Experiment 2.6', 'value': 'DE_probs_2_6'},
            {'label': 'Experiment 2.7', 'value': 'DE_probs_2_7'},
            {'label': 'Experiment 2.8', 'value': 'DE_probs_2_8'},
        ],
        value='DE_probs_1_1',  
        style={'width': '50%'}
    ),
    dcc.Graph(id="decoy-plot-output"), 
    html.P("""The decoy effect is a phenomenon in which consumers change their preference between two options when presented with a third option that is asymmetrically dominated. 
           An example of this would be a choice between two ice cream cones, one large and one small. If the large one is chosen most often, a third option (the decoy) is added, 
           which is the same as the large one, but more expensive. This should make the large one more attractive, as it is now the middle option. 
           This experiment is a replication of the experiment conducted by Huber et al. (1982)."""),
]

# Prospect Page
prospect_page = [
     html.H1("Prospect Theory and Mental Accounting Experiment", className="page-heading"),
     html.Br(),
     html.P(["""According to Prospect Theory and Mental Accounting, financial gains and losses are booked into different fictitious accounts. On top of that, \
            relative to a reference point, losses weigh more heavily than gains and the perceived sum of two individual gains/losses will, in absolute terms, be larger than \
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
            """The practical implications each of these rules hold will become more obvious when looking at the experimens conducted below. The original results are taken
               from Thaler, Richard (1985), “Mental Accounting and Consumer Choice,” Marketing Science, 4 (3), 199–214 and the prompts we query the Language Models with are
               constructed so that we can stay as close to the original phrasing as possible, while still instructing the models sufficiently well to produce meaningful results."""]),

    # Scenario 1: Segregation of gains
    html.Div(
        children = [
        html.H2("Scenario 1: Segregation of gains"),
        dcc.RadioItems(
            id = "prospect-scenario1-radio1",
            options = [
                {'label': 'Unprimed', 'value': 0},
                {'label': 'Primed', 'value': 1},
            ],
            value = 0, 
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}),
        dcc.RadioItems(
            id = "prospect-scenario1-radio2",
            options = [
                {'label': 'GPT-3.5-Turbo', 'value': 'GPT-3.5-Turbo'},
                {'label': 'GPT-4-1106-Preview', 'value': 'GPT-4-1106-Preview'},
            ],
            value = 'GPT-3.5-Turbo',
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}
        ),
        dcc.Graph(id = "prospect-plot1"),   
    ]),  

    # Scenario 2: Integration of losses
    html.Div(
        children = [
        html.H2("Scenario 2: Integration of losses"),
        dcc.RadioItems(
            id = "prospect-scenario2-radio1",
            options = [
                {'label': 'Unprimed', 'value': 0},
                {'label': 'Primed', 'value': 1},
            ],
            value = 0,
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}),
        dcc.RadioItems(
            id = "prospect-scenario2-radio2",
            options = [
                {'label': 'GPT-3.5-Turbo', 'value': 'GPT-3.5-Turbo'},
                {'label': 'GPT-4-1106-Preview', 'value': 'GPT-4-1106-Preview'},
            ],
            value = 'GPT-3.5-Turbo',
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}
        ),
        dcc.Graph(id = "prospect-plot2"),        
    ]),

    # Scenario 3: Cancellation of losses against larger gains
    html.Div(
        children =[
        html.H2("Scenario 3: Cancellation of losses against larger gains"),
        dcc.RadioItems(
            id = "prospect-scenario3-radio1",
            options = [
                {'label': 'Unprimed', 'value': 0},
                {'label': 'Primed', 'value': 1},
            ],
            value = 0,
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}),
        dcc.RadioItems(
            id = "prospect-scenario3-radio2",
            options = [
                {'label': 'GPT-3.5-Turbo', 'value': 'GPT-3.5-Turbo'},
                {'label': 'GPT-4-1106-Preview', 'value': 'GPT-4-1106-Preview'},
            ],
            value = 'GPT-3.5-Turbo',
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}
        ),
        dcc.Graph(id = "prospect-plot3"),
    ]),

    # Scenario 4: Segregation of silver linings
    html.Div(
        children = [
        html.H2("Scenario 4: Segregation of silver linings"),
        dcc.RadioItems(
            id = "prospect-scenario4-radio1",
            options = [
                {'label': 'Unprimed', 'value': 0},
                {'label': 'Primed', 'value': 1},
            ],
            value = 0,
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}),
        dcc.RadioItems(
            id = "prospect-scenario4-radio2",
            options = [
                {'label': 'GPT-3.5-Turbo', 'value': 'GPT-3.5-Turbo'},
                {'label': 'GPT-4-1106-Preview', 'value': 'GPT-4-1106-Preview'},
            ],
            value = 'GPT-3.5-Turbo',
            inputStyle={'margin-right': '10px'},
            labelStyle={'display': 'inline-block', 'margin-right': '20px'},
            style = {'width': '50%'}
    ),
        dcc.Graph(id = "prospect-plot4"),
    ]),
]


# Sunk Cost Fallacy Page
sunk_cost_page = [
    html.H1("Sunk Cost Fallacy", className="page-heading"),
    html.P('Description of how the experiments were conducted: ...'),
    
    # Experiment 1
    html.H3("Experiment 1"),
    html.P(["""Assume that you have spent $90/$250/$10,000 for a ticket to a theater performance. \
            Several weeks later you buy a $30 ticket to a rock concert. You think you will \
                enjoy the rock concert more than the theater performance. As you are putting your \
                    just-purchased rock concert ticket in your wallet, you notice that both events \
                            are scheduled for the same evening. The tickets are non-transferable, nor \
                                can they be exchanged. You can use only one of the tickets and not the other. \
                                    Which ticket will you use? """,
                                    html.Br(),  # Line break
                                    html.Br(),  # Line break
                                    "A: Theater performance.",
                                    html.Br(),  # Line break
                                    "B: Rock concert."
    ]),

    html.Div(
        style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'},
        children=[
            html.Div(
                style={'width': '25%', 'margin-right': '30px', 'align-self': 'flex-start', 'margin-top': '170px'}, 
                children=[
                    html.H6('Temperature Value'),
                    dcc.Slider(
                        id="Temperature_1",
                        min=0.5,
                        max=1.5,
                        step=0.5,
                        marks={0.5: '0.5', 1: '1', 1.5: '1.5'},
                        value=1,
                    ),
                    
                    html.H6('Amount of Sunk Cost (Cost of Theater Performance)', style={'margin-top': '50px'}), 
                    dcc.Dropdown(
                        id="Sunk-Cost",
                        options=[
                            {'label': '$90', 'value': 90},
                            {'label': '$250', 'value': 250},
                            {'label': '$10,000', 'value': 10_000}
                        ],
                        value=90,
                        style={'width': '100%'}
                    ),
                ]
            ),
            
            dcc.Graph(id="sunk-cost-plot-1-output", style={'width': '65%', 'height': '70vh'}),
        ]
    ),
    
    # Experiment 2
    html.H3("Experiment 2"),
    html.P(["""Suppose you bought a case of good Bordeaux in the futures \
            market for $20 a bottle. The wine now sells at auction for about $75. \
                You have decided to drink a bottle. Which of the following best captures \
                    your feeling of the cost to you of drinking the bottle?""",
                    html.Br(),  # Line break
                    html.Br(),  # Line break
                    "A: $0. I alreadey paid for it.",
                    html.Br(),  # Line break
                    "B: $20, what I paid for.",
                    html.Br(),  # Line break
                    "C: $20, plus interest.",
                    html.Br(),  # Line break
                    "D: $75, what I could get if I sold the bottle.",
                    html.Br(),  # Line break
                    "E: -$55, I get to drink a bottle that is worth $75 that I only paid \
                        $20 for so I save money by drinking the bottle."
    ]),

    html.Div(
        style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'},
        children=[
            html.Div(
                style={'width': '25%', 'margin-right': '30px', 'align-self': 'flex-start', 'margin-top': '170px'},  
                children=[
                    html.H6('Temperature Value'),
                    dcc.Slider(
                        id="Temperature_2",
                        min=0.5,
                        max=1.5,
                        step=0.5,
                        marks={0.5: '0.5', 1: '1', 1.5: '1.5'},
                        value=1,
                    ),
                    
                    html.H6('Model', style={'margin-top': '50px'}),  
                    dcc.Dropdown(
                        id="Model",
                        options=[
                            {'label': 'gpt-3.5-turbo-1106', 'value': 'gpt-3.5-turbo-1106'},
                            {'label': 'gpt-4-1106-preview	', 'value': 'gpt-4-1106-preview'},
                        ],
                        value='gpt-3.5-turbo-1106',
                        style={'width': '100%'}  
                    ),
                ]
            ),
            
            dcc.Graph(id="sunk-cost-plot-2-output", style={'width': '65%', 'height': '70vh'}),  # Adjust height as needed
        ]
    ),
]


# Loss Aversion Page
loss_aversion_page = [
    html.H1("Loss Aversion", className="page-heading"),
    html.P('Description of how the experiment was conducted: ...'),
    
    html.Div([
        # Experiment 1
        html.Div([
            html.H6("Scenario with gains:"),
            html.P(["You are offered two choices. Which choice would you prefer?",
                    html.Br(),  # Line break
                    html.Br(),  # Line break
                    "A: A sure gain of $100.",
                    html.Br(),  # Line break
                    "B: A 50% chance to gain $200 and a 50% chance to lose $0."
            ]),
        ], style={'width': '30%', 'display': 'inline-block', 'margin-bottom': '60px'}),

        html.Div([
            html.H6("Scenario with losses:"),
            html.P(["You are offered two choices. Which choice would you prefer?",
                    html.Br(),  # Line break
                    html.Br(),  # Line break
                    "A: A sure loss of $100.",
                    html.Br(),  # Line break
                    "B: A 50% chance to lose $200 and a 50% chance to lose $0."
            ]),
        ], style={'width': '30%', 'display': 'inline-block', 'margin-bottom': '60px'})
    ]),

    html.Div(
        style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'},
        children=[
            html.Div(
                style={'width': '25%', 'margin-right': '30px', 'align-self': 'center'}, 
                children=[
                    html.H6('Temperature Value'),
                    dcc.Slider(
                        id="Temperature",
                        min=0.5,
                        max=1.5,
                        step=0.5,
                        marks={0.5: '0.5', 1: '1', 1.5: '1.5'},
                        value=1,
                    ),
                ]
            ),
            
            dcc.Graph(id="loss_aversion_plot_output", style={'width': '65%', 'height': '70vh'}),
        ]
    )
]

################################################## Callbacks ##################################################


### Callback for prospect page

# Scenario 1
@app.callback(
     Output("prospect-plot1", "figure"),
     [Input("prospect-scenario1-radio1", "value"), # model 
        Input("prospect-scenario1-radio2", "value")] # priming

)
def update_prospect_plot1(selected_model, selected_priming):
        print("Selected Model:", selected_model)
        print("Selected Priming:", selected_priming)
        return plot_results(model = selected_priming, priming = selected_model, df = PT_probs, scenario = 1) # order is mixed up -> WHY?!?!?!

# Scenario 2
@app.callback(
        Output("prospect-plot2", "figure"),
        [Input("prospect-scenario2-radio1", "value"), # model
        Input("prospect-scenario2-radio2", "value")] #  priming

)
def update_prospect_plot2(selected_model, selected_priming):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 2) # works for scenario 1.... 


# Scenario 3
@app.callback(
        Output("prospect-plot3", "figure"),
        [Input("prospect-scenario3-radio1", "value"), # model
        Input("prospect-scenario3-radio2", "value")] # priming
)  
def update_prospect_plot3(selected_model, selected_priming):    
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 3)
    
# Scenario 4
@app.callback(
        Output("prospect-plot4", "figure"),
        [Input("prospect-scenario4-radio1", "value"), #  model
        Input("prospect-scenario4-radio2", "value")] #  priming
)
def update_prospect_plot4(selected_model, selected_priming):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 4)



# Callback for decoy page
@app.callback(
    Output("decoy-plot-output", "figure"),
    [Input("decoy-plot-dropdown", "value")]
)
def update_decoy_plot(selected_plot):
    # Check if the selected plot exists in the dfs dictionary
    if selected_plot in decoy_dfs:
        # Call the plot_results function with the selected dataframe
        return plot_results(decoy_dfs[selected_plot])
    else:
        # Return an empty figure
        return []
    
    
# Callback for Sunk Cost Fallacy Experiment 1
@app.callback(
    Output("sunk-cost-plot-1-output", "figure"),
    [Input("Temperature_1", "value"),
     Input("Sunk-Cost", "value")]
)
def update_sunk_cost_plot_1(selected_temperature, selected_sunk_cost):
    return plot_sunk_cost_1(selected_temperature, selected_sunk_cost)
    
    
# Callback for Sunk Cost Fallacy Experiment 2
@app.callback(
    Output("sunk-cost-plot-2-output", "figure"),
    [Input("Temperature_2", "value"),
     Input("Model", "value")]
)
def update_sunk_cost_plot_2(selected_temperature, selected_model):
    return plot_sunk_cost_2(selected_temperature, selected_model)


# Callback for Loss Aversion Experiment
@app.callback(
    Output("loss_aversion_plot_output", "figure"),
    [Input("Temperature", "value")]
)
def update_loss_averion_plot(selected_temperature):
    return plot_loss_aversion(selected_temperature)

        

# Callback for navigation bar
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P(start_page)
    elif pathname == "/page-1":
        return html.P("Experiments are not yet implemented. Sorry!")
    elif pathname == "/experiments/overview":
        return html.P("Overview of experiments is not yet implemented. Sorry!")
    elif pathname == "/experiments/decoy":
        return html.P(decoy_page)
    elif pathname == "/experiments/prospect":
        return html.P(prospect_page)
    elif pathname == "/experiments/sunk-cost":
        return html.P(sunk_cost_page)
    elif pathname == "/experiments/ultimatum":
        return html.P("Ultimatum experiment is not yet implemented. Sorry!")
    elif pathname == "/experiments/loss-aversion":
        return html.P(loss_aversion_page)
    elif pathname == "/page-2":
        return html.P("Live experiment is not yet implemented. Sorry!")
    elif pathname == "/page-3":
        return html.P("This chatbot is not yet implemented. Sorry!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8888, debug = True)