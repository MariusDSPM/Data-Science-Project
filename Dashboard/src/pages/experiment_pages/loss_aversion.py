# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


dash.register_page(__name__, path='/loss-aversion', name='Loss Aversion', location='experiments')


# Function for getting data
def get_loss_aversion_data(selected_temperature):
    df = pd.read_csv('data/Output/Loss_aversion_experiment_with_llama.csv', index_col=0)
    # Filter data based on selected temperature and results from real experiment
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
            font=dict(size=20)
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
                        html.P("The experiment presented participants with two scenarios, each involving decisions under conditions of gain and loss. In the scenario with gains, participants were asked to choose between a sure gain option (Option A: A sure gain of $100) and a risky option (Option B: A 50% chance to gain $200 and a 50% chance to lose $0). In the scenario with losses, participants were presented with a similar choice between a sure loss option (Option A: A sure loss of $100) and a risky option (Option B: A 50% chance to lose $200 and a 50% chance to lose $0). About two-thirds of the participants preferred the save option in the scenario with gains and the risky option in the scenario with losses."),
                        html.P("The interesting aspect of this experiment lies in examining how LLMs weigh the certainty of outcomes against the potential for larger gains or losses. By comparing responses in scenarios involving gains and losses, researchers can gain insights into whether LLMs exhibit consistent risk preferences across different contexts.")
                    ],
                    title="Description and motivation of the Experiment",
                ),
                dbc.AccordionItem(
                    [
                        html.P('Each LLM was asked 50 times to choose between the two options in both scenarios. To guide the model to answer only with the label of the answer option, the instruction role was set to "Please answer by only giving the letter of the answer option A or B.". The temperature parameter was set to 0.5, 1 and 1.5.'),
                        html.P('The phrasing of the prompts are exactly the same as the ones used in the real experiment. So it is possible that the experiment text was part of the training data for the models and the models are just memorizing the answers. This is a limitation of the experiment.')  
                    ],
                    title="Implementation of the Experiment",
                ),
                dbc.AccordionItem(
                    [
                        'Thaler, R.H., 2015. Misbehaving: The making of behavioral economics. WW Norton & Company.',
                    ],
                    title="References",
                ),
            ],
            always_open=True,
            start_collapsed=True,
        ),
        style={'margin-bottom': '50px'}
    ),  # End of Accordion
    html.H5('Prompts used in the experiment:'),
    html.Br(),
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