# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
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
        xaxis=dict(
            title='Model',
            tickmode='array', 
            tickvals=list(range(len(models))), 
            ticktext=models,
            title_font=dict(size=18),  
        ),
        yaxis=dict(
            title='Shares for "B"',
            title_font=dict(size=18)
        ),
        title=dict(
            text='Shares for "B" (risk-seeking option) by Model and Scenario',
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
        bargap = 0.5
    )
    
    return fig



# Loss Aversion Page
layout = [
    html.H1("Loss Aversion", className="page-heading"),
    html.Hr(),
    html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P("The experiment presented participants with two scenarios, each involving decisions under conditions of gain and loss. In the scenario with gains, participants were asked to choose between a sure gain option (Option A: A sure gain of $100) and a risky option (Option B: A 50% chance to gain $200 and a 50% chance to lose $0). In the scenario with losses, participants were presented with a similar choice between a sure loss option (Option A: A sure loss of $100) and a risky option (Option B: A 50% chance to lose $200 and a 50% chance to lose $0)."),
                    ],
                    title="Description of Loss Aversion Experiment",
                ),
                dbc.AccordionItem(
                    [
                        html.P("The experiment taps into the concept of loss aversion, a fundamental principle in behavioral economics. Loss aversion suggests that individuals tend to strongly prefer avoiding losses over acquiring gains of equivalent value. This phenomenon has been widely observed and is a central component of many economic and psychological theories related to decision-making under uncertainty. The interesting aspect of this experiment lies in examining how participants weigh the certainty of outcomes against the potential for larger gains or losses. By comparing responses in scenarios involving gains and losses, researchers can gain insights into whether individuals exhibit consistent risk preferences across different contexts."),
                    ],
                    title="Motivation of the Experiment",
                ),
                dbc.AccordionItem(
                        html.Div([
                            html.Div([
                                html.H6("Scenario with gains:"),
                                html.P(["You are offered two choices. Which choice would you prefer?",
                                        html.Br(),  # Line break
                                        html.Br(),  # Line break
                                        "A: A sure gain of $100.",
                                        html.Br(),  # Line break
                                        "B: A 50% chance to gain $200 and a 50% chance to lose $0."
                                ]),
                            ], style={'width': '45%', 'display': 'inline-block'}),

                            html.Div([
                                html.H6("Scenario with losses:"),
                                html.P(["You are offered two choices. Which choice would you prefer?",
                                        html.Br(),  # Line break
                                        html.Br(),  # Line break
                                        "A: A sure loss of $100.",
                                        html.Br(),  # Line break
                                        "B: A 50% chance to lose $200 and a 50% chance to lose $0."
                                ]),
                            ], 
                            style={'width': '45%', 'display': 'inline-block'})
                        ]),
                    title="Prompts used in the Experiment",
                ),
                dbc.AccordionItem(
                    [
                        'From Thaler, Richard (2015), "Misbehaving"',
                    ],
                    title="References",
                ),
            ],
            always_open=True
        ),
        style={'margin-bottom': '50px'}
    ),  # End of Accordion
    

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