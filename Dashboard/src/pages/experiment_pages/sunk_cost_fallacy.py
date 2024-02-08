# Import required libraries 
import pandas as pd
import numpy as np
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go


dash.register_page(__name__, path='/sunk-cost-fallacy', name='Sunk Cost Fallacy', location='experiments')


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
        xaxis=dict(
            title='Model',
            title_font=dict(size=18),
        ),
        yaxis=dict(
            title='Share', 
            range=[0, 1.1],
            title_font=dict(size=18)
        ),
        title=dict(
            text=f"Shares for Answer Options (Sunk Cost: ${selected_sunk_cost}, Temperature: {selected_temperature})",
            x=0.43,
            y = 0.9,
            font=dict(size=22)
        ),
        legend=dict(
            x=1.01,  
            y=0.9,
            font=dict(family='Arial', size=12, color='black'),
            bordercolor='black',  
            borderwidth=2
        ),
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
        xaxis=dict(
            title='Answer Option',
            tickvals=np.arange(len(df.columns[cols_to_select:end_col+1])) + ((len(prompts) - 1) / 2 * bar_width),
            ticktext=['$0', '$20', '$20 plus interest', '$75', '-$55'],
            title_font=dict(size=18),
        ),
        yaxis=dict(
            title='Share', 
            range=[0, 1.1],
            title_font=dict(size=18)
        ),
        title=dict(
            text=f'Shares for Answer Options (Model: {selected_model}, Temperature: {selected_temperature})',
            x=0.45,
            y = 0.9,
            font=dict(size=22)
        ),
        legend=dict(
            x=1.01,  
            y=0.9,
            font=dict(family='Arial', size=12, color='black'),
            bordercolor='black',  
            borderwidth=2, 
        ),
        bargap=0.3  # Gap between bars
    )

    return fig



# Sunk Cost Fallacy Page
layout = [
    html.H1("Sunk Cost Fallacy", className="page-heading"),
    html.P('Description of how the experiments were conducted: ...'),
    
    # Experiment 1
    html.H3("Experiment 1"),
    html.P(id='experiment-1-prompt'),

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
                    your feeling of the cost to you of drinking the bottle?"""
    ]),
    html.P('(Same answer options, but in different order):'),
    html.Div([
        html.Div([
            html.H6('Answer Option Order 1', style={'margin-top': '15px'}),
            html.P(["A: $0. I already paid for it.",
                    html.Br(),  # Line break
                    "B: $20, what I paid for.",
                    html.Br(),  # Line break
                    "C: $20, plus interest.",
                    html.Br(),  # Line break
                    "D: $75, what I could get if I sold the bottle.",
                    html.Br(),  # Line break
                    "E: -$55, I get to drink a bottle that is worth $75 that I only paid \
                        $20 for so I save money by drinking the bottle."]),
        ], style={'width': '40%', 'display': 'inline-block', 'margin-bottom': '60px', 'vertical-align': 'top'}),

        html.Div([
            html.H6('Answer Option Order 2', style={'margin-top': '15px'}),
            html.P(["A: $75",
                    html.Br(),  # Line break
                    "B: -$55",
                    html.Br(),  # Line break
                    "C: $0",
                    html.Br(),  # Line break
                    "D: $20",
                    html.Br(),  # Line break
                    "E: $20, plus interest"]),
        ], style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '60px', 'vertical-align': 'top'}),

        html.Div([
            html.H6('Answer Option Order 3', style={'margin-top': '15px'}),
            html.P(["A: -$55",
                    html.Br(),  # Line break
                    "B: $75",
                    html.Br(),  # Line break
                    "C: $20 plus interest",
                    html.Br(),  # Line break
                    "D: $0",
                    html.Br(),  # Line break
                    "E: $20"]),
        ], style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '60px', 'vertical-align': 'top'}),
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


# Callback for Sunk Cost Fallacy Experiment 1
@dash.callback(
    [Output("sunk-cost-plot-1-output", "figure"),
     Output("experiment-1-prompt", "children")],
    [Input("Temperature_1", "value"),
     Input("Sunk-Cost", "value")]
)
def update_sunk_cost_plot_1(selected_temperature, selected_sunk_cost):
    figure = plot_sunk_cost_1(selected_temperature, selected_sunk_cost)
    
    # Update the description of Experiment 1
    experiment_description = [
        f"""Assume that you have spent ${selected_sunk_cost} for a ticket to a theater performance. \
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
    ]

    return figure, experiment_description
    
    
# Callback for Sunk Cost Fallacy Experiment 2
@dash.callback(
    Output("sunk-cost-plot-2-output", "figure"),
    [Input("Temperature_2", "value"),
     Input("Model", "value")]
)
def update_sunk_cost_plot_2(selected_temperature, selected_model):
    return plot_sunk_cost_2(selected_temperature, selected_model)