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

# Read in experimental data as dictionary
# Decoy Effect
decoy_dfs = {}
for file in os.listdir("Output/DE_probs_dfs"):
        file_name = file.split(".")[0]
        df = pd.read_csv(f"Output/DE_probs_dfs/{file}", index_col = 0) # Set first column as index column 
        decoy_dfs[file_name] = df

# Prospect Theory
prospect_dfs = {}
for file in os.listdir("Output/PT_probs_dfs"):
    file_name = file.split(".")[0]
    df = pd.read_csv(f"Output/PT_probs_dfs/{file}", index_col = 0) # Set first column as index column
    prospect_dfs[file_name] = df
    

# Function for getting data of Sunk Cost Experiment 1
def get_sunk_cost_data(selected_temperature, selected_sunk_cost):
    sunk_cost_1 = pd.read_csv('Output/Sunk_cost_experiment_1.csv', index_col=0)
    df = sunk_cost_1[(sunk_cost_1['Temperature'] == selected_temperature) & 
                     (sunk_cost_1['Sunk Cost ($)'] == selected_sunk_cost)]
    
    return df
        
        

# Function for plotting results of decoy effect/prospect theory experiments
def plot_results(df):

    # Get experiment id and model name for plot title from dictionaries
    experiment_id = df.iloc[0, 1]
    model = model_dict[experiment_id]
    n_observations = df.loc["Obs."]
    
    # Set
    temperature = df.loc["Temp"]

    fig = go.Figure(data=[
        go.Bar(
            name="p(A)", 
            x=temperature, 
            y=df.loc["p(A)"].str.rstrip('%').astype('float'),
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br>Observations: %{customdata}<extra></extra>",
        ),
        go.Bar(
            name="p(B)", 
            x=temperature, 
            y=df.loc["p(B)"].str.rstrip('%').astype('float'),
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
            
        ),
        go.Bar(
            name="p(C)", 
            x=temperature, 
            y=df.loc["p(C)"].str.rstrip('%').astype('float'),
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
        )
    ])

    fig.update_layout(
        barmode='group',
        xaxis=dict(tickmode='array', tickvals=np.arange(len(temperature)), ticktext=temperature),
        xaxis_title="Temperature",
        yaxis_title="Probability (%)",
        title=f"Distribution of answers per temperature value for experiment {experiment_id} using {model}",
        legend=dict(title=dict(text="Probabilities")),
        bargap=0.3  # Gap between temperature values
    )

    return fig 


# Function for plotting Sunk Cost Experiment 1
def plot_sunk_cost_1(selected_temperature, selected_sunk_cost):
    # Assuming you have a function to get data for Sunk Cost Fallacy experiment based on selected temperature
    df_sunk_cost = get_sunk_cost_data(selected_temperature, selected_sunk_cost)
    
    # Create a bar plot using Plotly.graph_objects
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
        title=f"Sunk Cost Fallacy Experiment - Temperature: {selected_temperature}; Sunk Cost: ${selected_sunk_cost}",
        legend=dict(),
        bargap=0.3  # Gap between models
    )

    return fig_sunk_cost


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

#####################################################################################################################################################################
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
     html.H1("Prospect Theory Experiment", className="page-heading"),
     dcc.Dropdown( 
          id = "prospect-plot-dropdown",
          options = [
                {'label': 'Experiment 1.1', 'value': 'PT_probs_1_1'},
                {'label': 'Experiment 1.2', 'value': 'PT_probs_1_2'},
                {'label': 'Experiment 1.3', 'value': 'PT_probs_1_3'},
                {'label': 'Experiment 1.4', 'value': 'PT_probs_1_4'},
                {'label': 'Experiment 1.5', 'value': 'PT_probs_1_5'},
                {'label': 'Experiment 1.6', 'value': 'PT_probs_1_6'},
                {'label': 'Experiment 1.7', 'value': 'PT_probs_1_7'},
                {'label': 'Experiment 1.8', 'value': 'PT_probs_1_8'},
                {'label': 'Experiment 2.1', 'value': 'PT_probs_2_1'},
                {'label': 'Experiment 2.2', 'value': 'PT_probs_2_2'},
                {'label': 'Experiment 2.3', 'value': 'PT_probs_2_3'},
                {'label': 'Experiment 2.4', 'value': 'PT_probs_2_4'},
                {'label': 'Experiment 2.5', 'value': 'PT_probs_2_5'},
                {'label': 'Experiment 2.6', 'value': 'PT_probs_2_6'},
                {'label': 'Experiment 2.7', 'value': 'PT_probs_2_7'},
                {'label': 'Experiment 2.8', 'value': 'PT_probs_2_8'},
          ],
          value = 'PT_probs_1_1',
            style = {'width': '50%'}
        ),
        dcc.Graph(id="prospect-plot-output"),
        html.P("""Prospect theory is a theory of decision making under risk. It is based on the idea that people evaluate their options relative to a reference point, 
               and that losses and gains are valued differently. This experiment is a replication of the experiment conducted by Tversky and Kahneman (1981)."""),
]

# Sunk Cost Fallacy Page
sunk_cost_page = [
    html.H1("Sunk Cost Fallacy", className="page-heading"),
    
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
        style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'},  # Adjust align-items
        children=[
            html.Div(
                style={'width': '25%', 'margin-right': '30px', 'align-self': 'flex-start', 'margin-top': '170px'},  # Adjust margin-top for slider
                children=[
                    html.H5('Temperature Value'),
                    dcc.Slider(
                        id="Temperature",
                        min=0.5,
                        max=1.5,
                        step=0.5,
                        marks={0.5: '0.5', 1: '1', 1.5: '1.5'},
                        value=1,
                    ),
                    
                    html.H6('Amount of Sunk Cost (Cost of Theater Performance)', style={'margin-top': '50px'}),  # Adjust margin-top for dropdown
                    dcc.Dropdown(
                        id="Sunk-Cost",
                        options=[
                            {'label': '$90', 'value': 90},
                            {'label': '$250', 'value': 250},
                            {'label': '$10,000', 'value': 10_000}
                        ],
                        value=90,
                        style={'width': '100%'}  # Adjust the width as needed
                    ),
                ]
            ),
            
            dcc.Graph(id="sunk-cost-plot-1-output", style={'width': '65%', 'height': '70vh'}),  # Adjust height as needed
        ]
    ),
    
    html.P("""Sunk Cost Fallacy experiment description goes here..."""),
]


# Callback for prospect page
@app.callback(
    Output("prospect-plot-output", "figure"),
    [Input("prospect-plot-dropdown", "value")]
)
def update_prospect_plot(selected_plot):
    # Check if the selected plot exists in the dfs dictionary
    if selected_plot in prospect_dfs:
        # Call the plot_results function with the selected dataframe
        return plot_results(prospect_dfs[selected_plot])
    else:
        # Return an empty figure
        return []


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
    
    
# Callback for Sunk Cost Fallacy page
@app.callback(
    Output("sunk-cost-plot-1-output", "figure"),
    [Input("Temperature", "value"),
     Input("Sunk-Cost", "value")]
)
def update_decoy_plot(selected_temperature, selected_sunk_cost):
    return plot_sunk_cost_1(selected_temperature, selected_sunk_cost)
    


        

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
        return html.P("Loss Aversion experiment is not yet implemented. Sorry!")
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
    app.run_server(port=8888)