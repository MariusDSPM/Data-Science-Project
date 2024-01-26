# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
from PIL import Image
import pickle
from ast import literal_eval
import pandas as pd

dash.register_page(__name__, path='/transaction-utility', name='Transaction Utility', location='experiments')

### Setup ###

TU_results = pd.read_csv('Output/TU_results.csv')
#TU_resullts2 = pd.read_csv('Output/TU_results2.csv')

# Function to extract the dollar amount of the answer from LLMs
def extract_dollar_amounts(answers):
    # Only return values that start with "$"
    valid_prices = [item for item in answers if item.startswith("$")]
    # Delete the "$" from the beginning of each price
    prices = [item.replace('$', '') for item in valid_prices]
    return prices

# Function for plottings results of transaction utility experiments
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

# Prompts used in the experiment
with open("Output/TU_prompts.pkl", "rb") as file:
    TU_prompts = pickle.load(file)

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
                                min=0.5,
                                max=1.5,
                                step=0.5,
                                marks={0.5: '0.5', 1: '1', 1.5: '1.5'},
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
]


### Callback ###
# Experiment 1
@dash.callback(
    Output("tu1-plot", "figure"),
    [
        Input("tu1-initial-cost-dropdown", "value"),
        Input("tu1-current-cost-dropdown", "value"),
        Input("tu1-buyer-dropdown", "value"),
        Input("tu1-language-model-dropdown", "value"),
        Input("tu1-temperature-slider", "value"),
    ],
)


def update_tu1_plot(initial_costs, orientation_price, buyer, model, temperature):
    print(f"Selected initial costs: {initial_costs}"),
    print(f"Selected current costs: {orientation_price}"),
    print(f"Selected buyer: {buyer}"),
    print(f"Selected model: {model}"),
    print(f"Selected temperature: {temperature}"),
    
    return TU_plot_results(initial_costs, orientation_price, buyer, model, temperature, TU_results)

