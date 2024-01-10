# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go


dash.register_page(__name__, path='/loss-aversion', name='Loss Aversion', location='experiments')


# Function for getting data
def get_loss_aversion_data(selected_temperature):
    df = pd.read_csv('Output/Loss_aversion_experiment_with_llama.csv', index_col=0)
    df = df[(df['Temperature'] == selected_temperature)|
            (df['Model'] == 'Real Experiment')] 
    
    return df 


# Function for plotting
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
        title=dict(text='Shares for "B" (risk-seeking option) by Model and Scenario',
                   x=0.45),
        bargap=0.6  # Gap between bars
    )
    
    return fig



# Loss Aversion Page
layout = [
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


# Callback
@dash.callback(
    Output("loss_aversion_plot_output", "figure"),
    [Input("Temperature", "value")]
)
def update_loss_averion_plot(selected_temperature):
    return plot_loss_aversion(selected_temperature)