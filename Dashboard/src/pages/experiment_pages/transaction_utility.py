# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
from PIL import Image
import pickle
from ast import literal_eval
import pandas as pd
import numpy as np
from collections import Counter

dash.register_page(__name__, path='/transaction-utility', name='Transaction Utility', location='experiments')

### Setup ###

TU_results = pd.read_csv('Output/TU_results.csv')
TU_resullts2 = pd.read_csv('Output/TU2_results.csv')


# Function to extract the dollar amount of the answer from LLMs
def extract_dollar_amounts(answers):
    # Only return values that start with "$"
    valid_prices = [item for item in answers if item.startswith("$") and item[1:].replace('.', '').isdigit()] # check if everything after $ is a digit, exlcuding commas
    # Delete the "$" from the beginning of each price
    prices = [item.replace('$', '') for item in valid_prices]
    return prices

# Function to plot results of first experiment
def TU_plot_results(initial_costs, orientation_price, buyer, model, temperature, df):
    # Select requested subset of results
    df = df[(TU_results["Model"] == model) & (TU_results["Temperature"] == temperature) & (TU_results["Initial_cost"] == initial_costs) & (TU_results["Orientation_price"] == orientation_price) & (TU_results["Buyer"] == buyer)]
    # Transpose for plotting
    df = df.transpose().copy()
    # Get original and model answers
    og_answers = df.loc["Original"].apply(literal_eval).iloc[0]
    # Apply literal_eval to convert string to list
    answers = df.loc["Answers"].apply(literal_eval).iloc[0]
    # Get number of observations 
    n_observations = df.loc["Obs."].iloc[0] 
    # Get number of original answers
    n_original = df.loc["Original_count"].iloc[0]
    # Get stated WTP
    prices = extract_dollar_amounts(answers)
    # Get temperature value 
    temperature = temperature

    # Compute percentage of $0:
    percent_0 = (prices.count("0")/n_observations)*100
    # Compute percentage of $5:
    percent_5 = (prices.count("5")/n_observations)*100
    # Compute percentage of $10:
    percent_10 = (prices.count("10")/n_observations)*100
    # Compute percentage of $15:
    percent_15 = (prices.count("15")/n_observations)*100
    # Compute percentage of other answers:
    percent_other = 100-percent_0-percent_5-percent_10-percent_15

    fig = go.Figure(data = [
        go.Bar(
            name = "Model answers",
            x = ["$0", "$5", "$10", "$15", "Other"],
            y = [percent_0, percent_5, percent_10, percent_15, percent_other],
            customdata = [n_observations, n_observations, n_observations, n_observations, n_observations], 
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(55, 83, 109)"
        ),
        go.Bar(
            name = "Original answers",
            x = ["$0", "$5", "$10", "$15", "Other"],
            y = [og_answers[0], og_answers[1], og_answers[2], 0, og_answers[3]], # 0 because no-one answered $15, but model did 
            customdata = [n_original, n_original, n_original, n_original, n_original],
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(26, 118, 255)"
        )
    ])

    # Style figure and add labels 
    fig.update_layout(
    barmode = "group",
     xaxis = dict(
            title = "Price",
            titlefont_size = 18,
            tickfont_size = 16,
     ),
    yaxis = dict(
        title = "Percentage",
        titlefont_size = 18,
        tickfont_size = 16,
    ),
    title = dict(
    text =  f"Distribution of answers for temperature {temperature}, using model {model}",
    x = 0.5, 
    y = 0.95,
    font_size = 18,
    ),
    legend=dict(
        x=1.01,  # Adjust the position of the legend
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black',  # Set the legend border color
        borderwidth=2,  # Set the legend border width
    ),
    width = 1000,
    margin=dict(t=60)
    )
    
    return fig

# Function to plot results of second experiment
# This function is coded rather complicated. However, not converting the answers to strings has the advantage using the Histogram w/o bins.
def TU2_plot_results(place, income, model, temperature, df):
    
    # Select requested subset of results
    df = df[(df["Model"] == model) & (df["Temperature"] == temperature) & (df["Place"] == place) & (df["Income"] == income)]
    # Transpose for plotting
    df = df.transpose()
    # Get temperature value 
    temperature = temperature
    # Get number of observations 
    n_observations = df.loc["Obs."].iloc[0] 
    # Get place
    place = place
    # Adjust name of place for plot title
    if place == "grocery":
        place = "grocery store"

    # Apply literal_eval to work with list of strings
    answers = df.loc["Answers"].apply(literal_eval).iloc[0]
    # Get stated WTP
    prices = extract_dollar_amounts(answers)
    # Convert to float
    prices = [float(price) for price in prices]
    # Get max, mean and median
    median = np.median(prices)
    mean = np.mean(prices)
    max = np.max(prices)

    # Adjust prices so that every value above 30 is set to 30, deals with outliers
    prices = [30.00 if price > 30 else price for price in prices]

    # Create the histogram using custom bins
    fig = go.Figure(data=[
    go.Bar(
        x = list(Counter(prices).keys()),
        y = list(Counter(prices).values()),
        name="Model answers",
        customdata=[n_observations] * len(prices),
        hovertemplate="Value: %{x}<br>Number of observations: %{y}<br>Number of total observations: %{customdata}<extra></extra>",
        marker_color="rgb(55, 83, 109)",
        width=0.4 ,  # Adjust the width of the bars if needed
    ),
    # Add vertical line for median
    go.Scatter(
        x = [median, median], #start and enf of x
        y = [0, Counter(prices).most_common(1)[0][1]], # count of most common price
        mode="lines",
        name="Median",
        line=dict(color="red", width=4, dash="dash"),
        hovertemplate = "Median: %{x}<extra></extra>",
),
    # Add vertical line for mean
    go.Scatter(
        x = [mean, mean], #start and enf of x
        y = [0, Counter(prices).most_common(1)[0][1]], # count of most common price
        mode="lines",
        name="Mean",
        line=dict(color="green", width=4, dash="dash"),
        hovertemplate = "Mean: %{x}<extra></extra>",
    )
])


    # Layout
    fig.update_layout(
    xaxis = dict(
        title = "Willingness to pay (USD)",
        titlefont_size = 18,
        tickfont_size = 16,
        tickformat=".2f",
    ),
    yaxis = dict(
        title = "Frequency",
        titlefont_size = 18,
        tickfont_size = 16,
    ),
    title = dict(
    text =  f"Distribution of {model}'s WTP for beer at the {place} for temperature {temperature}",
    x = 0.5, 
    y = 0.95,
    font_size = 18,
    ),
    legend=dict(
        x=1.01, 
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black',  
        borderwidth=2,  
    ),
    showlegend = True,
    width = 1000,
    margin=dict(t=60)
    )
    # Adjust x-axis labels to show 30+ to symbolize aggregation
    fig.update_xaxes(
    tickvals = sorted(fig.data[0].x),
    ticktext=["$30+" if tick_value == 30.0 else tick_value for tick_value in sorted(set(fig.data[0].x))],
)

    print(f"The maximum WTP stated by {model} for beer at the {place} for temperature {temperature} is ${max}.")
    # Show the plot
    return fig

# Also return max(price)

# Prompts used in the first experiment
with open("data/Input/TU_prompts.pkl", "rb") as file:
    TU_prompts = pickle.load(file)
# Prompts used in the second experiment
with open("data/Input/TU2_prompts.pkl", "rb") as file:
    TU2_prompts = pickle.load(file)

# Dictionary of prompts used in first experiment
TU_experiment_prompts_dict = {
    "TU_1_1_1_1": TU_prompts[0],
    "TU_1_1_1_2": TU_prompts[1],
    "TU_1_1_2_1": TU_prompts[2],
    "TU_1_1_2_2": TU_prompts[3],
    "TU_1_2_1_1": TU_prompts[4],
    "TU_1_2_1_2": TU_prompts[5],
    "TU_1_2_2_1": TU_prompts[6],
    "TU_1_2_2_2": TU_prompts[7],
    "TU_1_3_1_1": TU_prompts[8],
    "TU_1_3_1_2": TU_prompts[9],
    "TU_1_3_2_1": TU_prompts[10],
    "TU_1_3_2_2": TU_prompts[11],
    "TU_2_1_1_1": TU_prompts[0],
    "TU_2_1_1_2": TU_prompts[1],
    "TU_2_1_2_1": TU_prompts[2],
    "TU_2_1_2_2": TU_prompts[3],
    "TU_2_2_1_1": TU_prompts[4],
    "TU_2_2_1_2": TU_prompts[5],
    "TU_2_2_2_1": TU_prompts[6],
    "TU_2_2_2_2": TU_prompts[7],
    "TU_2_3_1_1": TU_prompts[8],
    "TU_2_3_1_2": TU_prompts[9],
    "TU_2_3_2_1": TU_prompts[10],
    "TU_2_3_2_2": TU_prompts[11],
    "TU_3_1_1_1": TU_prompts[0],
    "TU_3_1_1_2": TU_prompts[1],
    "TU_3_1_2_1": TU_prompts[2],
    "TU_3_1_2_2": TU_prompts[3],
    "TU_3_2_1_1": TU_prompts[4],
    "TU_3_2_1_2": TU_prompts[5],
    "TU_3_2_2_1": TU_prompts[6],
    "TU_3_2_2_2": TU_prompts[7],
    "TU_3_3_1_1": TU_prompts[8],
    "TU_3_3_1_2": TU_prompts[9],
    "TU_3_3_2_1": TU_prompts[10],
    "TU_3_3_2_2": TU_prompts[11],
}

# Dictionary of prompts used in second experiment
TU2_experiment_prompts_dict = {
    "TU2_1_1_1": TU2_prompts[0],
    "TU2_1_1_2": TU2_prompts[1],
    "TU2_1_1_3": TU2_prompts[2],
    "TU2_1_1_4": TU2_prompts[3],
    "TU2_1_2_1": TU2_prompts[4],
    "TU2_1_2_2": TU2_prompts[5],
    "TU2_1_2_3": TU2_prompts[6],
    "TU2_1_2_4": TU2_prompts[7],
    "TU2_2_1_1": TU2_prompts[0],
    "TU2_2_1_2": TU2_prompts[1],
    "TU2_2_1_3": TU2_prompts[2],
    "TU2_2_1_4": TU2_prompts[3],
    "TU2_2_2_1": TU2_prompts[4],
    "TU2_2_2_2": TU2_prompts[5],
    "TU2_2_2_3": TU2_prompts[6],
    "TU2_2_2_4": TU2_prompts[7],
    "TU2_3_1_1": TU2_prompts[0],
    "TU2_3_1_2": TU2_prompts[1],
    "TU2_3_1_3": TU2_prompts[2],
    "TU2_3_1_4": TU2_prompts[3],
    "TU2_3_2_1": TU2_prompts[4],
    "TU2_3_2_2": TU2_prompts[5],
    "TU2_3_2_3": TU2_prompts[6],
    "TU2_3_2_4": TU2_prompts[7]
}





### Layout ###
layout = [
    html.H1("Transaction Utility Experiment", className="page-heading"),
    html.Hr(),
    
    html.H2("Experiment 1: Hockey game tickets"),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select initial ticket price", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-initial-cost-dropdown",
                        options=[
                            {"label": "Free", "value": 0},
                            {"label": "$5", "value": 5},
                            {"label": "$10", "value": 10},
                        ],
                        value=0,
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select current market price", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-current-cost-dropdown",
                        options=[
                            {"label": "$5", "value": 5},
                            {"label": "$10", "value": 10},
                        ],
                        value=5,
                        style={'width': '75%', 'margin': 'auto'},                        

                    ),
                    html.Label("Select buyer type", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id = "tu1-buyer-dropdown",
                        options=[
                            {"label": "Friend", "value": "friend"},
                            {"label": "Stranger", "value": "stranger"},
                        ],
                        value="friend",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu1-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None, # To only allow values as specified in marks
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu1-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt 
    html.Div(
            id='tu1-prompt',
            style={'textAlign': 'center', 'margin': '20px'},
    ),

    ########## Experiment 2
    html.Hr(),
    html.H2("Experiment 2: Beer at the grocery store"),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select place of purchase", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-place-dropdown",
                        options=[
                            {"label": "Fancy resort hotel", "value": "hotel"},
                            {"label": "Run-down grocery store", "value": "grocery"},
                        ],
                        value="hotel",
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select annual income", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-income-dropdown",
                        options=[
                            {"label": "No information given", "value": "0"},
                            {"label": "$50k", "value": "$50k"},
                            {"label": "$70k", "value": "$70k"},
                            {"label": "$120k", "value": "$120k"},
                        ],
                        value="0",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),

                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu2-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None,
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu2-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt
    html.Div(
            id='tu2-prompt',
            style={'textAlign': 'center', 'margin': '20px'},
    ),
]



### Callback ###

### Experiment 1
@dash.callback(
    [Output("tu1-plot", "figure"),
    Output('tu1-prompt', 'children')],
    [
        Input("tu1-initial-cost-dropdown", "value"),
        Input("tu1-current-cost-dropdown", "value"),
        Input("tu1-buyer-dropdown", "value"),
        Input("tu1-language-model-dropdown", "value"),
        Input("tu1-temperature-slider", "value"),
    ],
)


def update_tu1(initial_costs, orientation_price, buyer, model, temperature):
    # Get prompt
    df = TU_results[(TU_results["Model"] == model) & (TU_results["Temperature"] == temperature) & (TU_results["Initial_cost"] == initial_costs)
                     & (TU_results["Orientation_price"] == orientation_price) & (TU_results["Buyer"] == buyer)]
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU_plot_results(initial_costs, orientation_price, buyer, model, temperature, TU_results), prompt

### Experiument 2
@dash.callback(
    [Output("tu2-plot", "figure"),
     Output('tu2-prompt', 'children')],
    [
        Input("tu2-place-dropdown", "value"),
        Input("tu2-income-dropdown", "value"),
        Input("tu2-language-model-dropdown", "value"),
        Input("tu2-temperature-slider", "value"),
    ],
)

def update_tu2(place, income, model, temperature):
    # Get prompt
    df = TU_resullts2[(TU_resullts2["Model"] == model) & (TU_resullts2["Temperature"] == temperature) &
                       (TU_resullts2["Place"] == place) & (TU_resullts2["Income"] == income)]
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU2_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU2_plot_results(place, income, model, temperature, TU_resullts2), prompt