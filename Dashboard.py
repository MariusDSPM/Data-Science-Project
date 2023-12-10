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
from PIL import Image



#########################################  Data Import Functions  #########################################



# Load in results of Decoy Effect experiments
DE_probs = pd.read_csv("Output/DE_probs.csv", index_col = 0)

# Load in results and graphs of Prospect Theory experiments
PT_probs = pd.read_csv("Output/PT_probs.csv", index_col = 0)
PT_og_scenario1 = Image.open("Output/PT_og_scenario1.png")
PT_og_scenario2 = Image.open("Output/PT_og_scenario2.png")
PT_og_scenario3 = Image.open("Output/PT_og_scenario3.png")
PT_og_scenario4 = Image.open("Output/PT_og_scenario4.png")

# Second Prospect Theory experiment
PT2_probs = pd.read_csv("Output/PT2_probs.csv", index_col = 0)

# Function for getting data of Sunk Cost Experiment 1
def get_sunk_cost_data_1(selected_temperature, selected_sunk_cost):
    sunk_cost_1 = pd.read_csv('Output/Sunk_cost_experiment_1_with_llama.csv', index_col=0)
    df = sunk_cost_1[(sunk_cost_1['Temperature'] == selected_temperature) & 
                     (sunk_cost_1['Sunk Cost ($)'] == selected_sunk_cost)]
    
    return df

# Function for getting data of Sunk Cost Experiment 2
def get_sunk_cost_data_2(selected_temperature, selected_model):
    df = pd.read_csv('Output/Sunk_cost_experiment_2_with_llama.csv', index_col=0)
    df = df[(df['Temperature'] == selected_temperature) & 
            (df['Model'] == selected_model) |
            (df['Model'] == 'Real Experiment')]
    
    return df

# Function for getting data of Loss Aversion Experiment
def get_loss_aversion_data(selected_temperature):
    df = pd.read_csv('Output/Loss_aversion_experiment_with_llama.csv', index_col=0)
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
            marker=dict(color="#e9724d"),
        ),
        go.Bar(
            name="p(B)", 
            x=temperature, 
            y=df.loc["p(B)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
            marker=dict(color="#868686"),
            
        ),
        go.Bar(
            name="p(C)", 
            x=temperature, 
            y=df.loc["p(C)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
            marker=dict(color="#92cad1"),
        )
    ])

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        tickmode = 'array',
        tickvals = temperature,
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
        x = 0.5, # Center alignment horizontally
        y = 0.87,  # Vertical alignment
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
    
    cols_to_select = df.columns.tolist().index('$0')
    end_col = df.columns.tolist().index('-$55')

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
                        x=np.arange(len(df.columns[cols_to_select:end_col+1])) + (i * bar_width),
                        y=subset.iloc[0, cols_to_select:end_col+1].values,
                        width=bar_width,
                        name=f'Answer Option Order {i + 1}',
                        marker=dict(color=f'rgba({i * 50}, 0, 255, 0.6)'),
                        hovertemplate="%{y:.2f}",
                    ))
        elif model == 'Real Experiment':
                fig.add_trace(go.Bar(
                            x=np.arange(len(df.columns[cols_to_select:end_col+1])) + ((len(prompts)-1) * bar_width),
                            y=df.iloc[-1, cols_to_select:end_col+1].values,
                            width=bar_width,
                            name='Real Results',
                            marker=dict(color='rgba(0, 0, 0, 0.3)'),
                            hovertemplate="%{y:.2f}",
                        ))


    fig.update_layout(
        barmode='group',
        xaxis=dict(tickvals=np.arange(len(df.columns[cols_to_select:end_col+1])) + ((len(prompts) - 1) / 2 * bar_width),
                ticktext=['$0', '$20', '$20 plus interest', '$75', '-$55']),
        yaxis=dict(title='Share', range=[0, 1.1]),
        title=f'Shares for Answer Options (Model: {selected_model}, Temperature: {selected_temperature})',
        legend=dict(),
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
            hovertemplate="%{y:.2f}",
        ))

    # Update layout
    fig.update_layout(
        barmode='group',
        xaxis=dict(tickmode='array', tickvals=list(range(len(models))), ticktext=models),
        yaxis=dict(title='Shares for "B"'),
        title='Shares for "B" (risk-seeking option) by Model and Scenario',
        bargap=0.6  # Gap between bars
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
    html.Hr(),
    html.P(["""The decoy effect describes a phenomenon, in which  consumers preferences between two products change, once a third option is added. This third option is designed 
            to be asymmetrically dominated, meaning that it is entirely inferior to one of the previous options, but only partially inferior to the other. Once this asymetrically 
            dominated option, the Decoy, is present, more people will now tend to choose the dominating option than before. A decoy product can therefore be used to influence consumer's
            decision making and increase saless of a specific product merely through the presence of an additional alternative.""",
            html.Br(),
            html.Br(),
            """Our experiment aims to recreate the findings of Ariely in his 2008 book *Predictably Irrational*. There, he asked 100 students from MIT's Sloan School of Management 
            to choose between the following options:""",
            html.Br(),
            html.Br(),
            "A: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$.",
            html.Br(),
            "B: One-year subscription to the print edition of The Economist, priced at 125$.",
            html.Br(),
            "C: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.",
            html.Br(),
            html.Br(),
            "In this example, option B serves as the decoy option.",
            html.Br(), 
            "When presented with ", html.B("all three options"), " Ariely found, that ", html.B("84%"), " of the participants chose option ", html.B("C"), " while only ", html.B("16%"), " chose option ", html.B("A"),".",
            html.Br(),
            "However, once ", html.B("option B was removed"), " and the choice had to be made only between A and C, ", html.B("68%"), " of the participants chose option ", html.B("A"), " while only ", html.B("32%"), "chose option ", html.B("C"),".",
            html.Br(),
            html.Br(),
            """In the experiments below, we examine how various Large Language Models react to this kind of experiment. We therefore queried 3 different models over a range of possible 
            temperature values using either primed or unprimed prompts. On top of that, we investigated to what extent the models' responses change, when we rename and reorder the 
            answer options. In the case of primed prompts, we instructed the model to be a market researcher, who knows about the Decoy Effect in product pricing."""]),
            html.Br(),
            html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Dropdown(
                         id = "decoy-scenario-dropdown",
                         options = [
                              {"label": "Scenario 1: All options present", "value": 1},
                              {"label": "Scenario 2: Decoy option removed", "value": 2},
                         ],
                         value = 1,
                         style={'width': '75%'},
                    ),
                    dcc.Dropdown(
                         id = "decoy-priming-dropdown",
                         options = [
                              {"label": "Unprimed prompt", "value": 0},
                              {"label": "Primed prompt", "value": 1},
                            ],
                            value = 0,
                            style={'width': '75%'},
                    ),
                    dcc.Dropdown(
                         id = "decoy-reordering-dropdown",
                         options = [
                              {"label": "Original order", "value": 0},
                              {"label": "Answer options reordered", "value": 1},
                            ],
                            value = 0,
                            style={'width': '75%'},
                    ),
                    dcc.Dropdown(
                         id = "decoy-model-dropdown",
                         options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                              {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                              {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                            style={'width': '75%'},
                    ),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="decoy-plot-output", style={'width': '70%', 'height': '60vh'}),
        ],
        
        style={'display': 'flex', 'flexDirection': 'row'})]
   

# Prospect Page
prospect_page = [
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
                        "Mr. A was given tickets to lotteries involving the World Series. He won $50 in one lottery and $25 in the other.",
                        html.Br(),
                        "Mr. B was given a ticket to a single, larger World Series lottery. He won $75. Who was happier?",
                        html.Br(),
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario1, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario1-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario1-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot1", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
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
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario2, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario2-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario2-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot2", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
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
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario3, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario3-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario3-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot3", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
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
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario4, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario4-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario4-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot4", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
)]),
html.Br(),
html.Hr(),
html.H2("Experiment 2: Odd numbers and unfair scenarios")
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
                            {'label': 'gpt-4-1106-preview', 'value': 'gpt-4-1106-preview'},
                            {'label': 'llama-2-70b', 'value': 'llama-2-70b'},
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
        ], style={'width': '40%', 'display': 'inline-block', 'margin-bottom': '60px'}),

        html.Div([
            html.H6("Scenario with losses:"),
            html.P(["You are offered two choices. Which choice would you prefer?",
                    html.Br(),  # Line break
                    html.Br(),  # Line break
                    "A: A sure loss of $100.",
                    html.Br(),  # Line break
                    "B: A 50% chance to lose $200 and a 50% chance to lose $0."
            ]),
        ], style={'width': '40%', 'display': 'inline-block', 'margin-bottom': '60px'})
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
     [Input("prospect-scenario1-radio1", "value"), # priming
        Input("prospect-scenario1-radio2", "value")] # model

)
def update_prospect_plot1(selected_priming, selected_model):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 1) 

# Scenario 2
@app.callback(
        Output("prospect-plot2", "figure"),
        [Input("prospect-scenario2-radio1", "value"), # priming
        Input("prospect-scenario2-radio2", "value")] #  model

)
def update_prospect_plot2(selected_priming, selected_model):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 2) 


# Scenario 3
@app.callback(
        Output("prospect-plot3", "figure"),
        [Input("prospect-scenario3-radio1", "value"), # priming
        Input("prospect-scenario3-radio2", "value")] # model
)  
def update_prospect_plot3(selected_priming, selected_model):    
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 3)
    
# Scenario 4
@app.callback(
        Output("prospect-plot4", "figure"),
        [Input("prospect-scenario4-radio1", "value"), #  priming
        Input("prospect-scenario4-radio2", "value")] #  model
)
def update_prospect_plot4(selected_priming, selected_model):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 4)



# Callback for decoy page
@app.callback(
    Output("decoy-plot-output", "figure"),
    [Input("decoy-scenario-dropdown", "value"),
     Input("decoy-priming-dropdown", "value"),
     Input("decoy-reordering-dropdown", "value"),
     Input("decoy-model-dropdown", "value")]
)
def update_decoy_plot(selected_scenario, selected_priming, selected_reordering, selected_model):
    # Pre-select dataframe with desired answer design 
    df = DE_probs[DE_probs["Reorder"] == selected_reordering]
    return plot_results(scenario = selected_scenario, priming = selected_priming, model = selected_model, df = df)
    
    
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