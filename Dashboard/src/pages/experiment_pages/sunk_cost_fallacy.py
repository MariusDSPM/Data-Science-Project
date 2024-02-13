# Import required libraries 
import pandas as pd
import numpy as np
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


dash.register_page(__name__, path='/sunk-cost-fallacy', name='Sunk Cost Fallacy', location='experiments')


# Function for getting data of Sunk Cost Experiment 1
def get_sunk_cost_data_1(selected_temperature, selected_sunk_cost):
    sunk_cost_1 = pd.read_csv('data/Output/Sunk_cost_experiment_1_with_llama.csv', index_col=0)
    df = sunk_cost_1[(sunk_cost_1['Temperature'] == selected_temperature) & 
                     (sunk_cost_1['Sunk Cost ($)'] == selected_sunk_cost)]
    
    return df

# Function for getting data of Sunk Cost Experiment 2
def get_sunk_cost_data_2(selected_temperature, selected_model):
    df = pd.read_csv('data/Output/Sunk_cost_experiment_2_with_llama.csv', index_col=0)
    # Filter data based on selected temperature and model 
    df = df[(df['Temperature'] == selected_temperature) & 
            (df['Model'] == selected_model) |
            (df['Model'] == 'Real Experiment')]  # Results from real experiment
    
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
            font=dict(size=20)
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
            font=dict(size=18)
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
    html.Hr(),
    
    # Experiment 1
    html.H3("Experiment 1"),
    html.Br(),
    html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P("Participants are presented with a hypothetical scenario where they have purchased tickets to two different events: a theater performance and a rock concert. The theater ticket costs $90, while the rock concert ticket costs $30. Weeks later, they realize that both events are scheduled for the same evening. They think they will enjoy the rock concert more than the theater performance. The tickets are non-transferable and cannot be exchanged. Participants must choose which event to attend, knowing they will miss out on the other."),
                        html.P("The majority of the participants would choose the theater performance, despite being told that they would enjoy the rock concert more."),
                        html.P("By analyzing LLMs' choices in this experiment, researchers gain insights into how LLMs prioritize experiences, weigh opportunity costs, and allocate resources, shedding light on the complexities of LLM decision-making under constraints."),
                    ],
                    title="Description and motivation of the experiment",
                ),
                dbc.AccordionItem(
                    [
                        html.P('Each LLM was asked 50 times to choose between the two options. To guide the model to answer only with the label of the answer option, the instruction role was set to "Please answer by only giving the letter of the answer option A or B.". The temperature parameter was set to 0.5, 1 and 1.5.'),
                        html.P("Furthermore, the cost of the theater performance is varied to examine how LLMs respond to different sunk costs. Raising the cost of the theater performance ticket to $250 or $10,000 provides an intriguing variable to observe whether LLMs' decision-making changes significantly in the face of a higher initial investment, potentially highlighting the influence of sunk costs on choices."), 
                        html.P("To mitigate the problem that the experimental text from the literature was part of the training data of the LLMs, the experimental text was changed. Soman (2001) conducted the experiment with time investments. Arkes and Blumer (1985) dealt with cost for a ski trip. The experiment here is therefore a mixture of these two experiments and no real human results are available.")
                    ],
                    title="Implementation of the experiment",
                ),
                dbc.AccordionItem(
                    [
                        'Soman, D. 2001. The mental accounting of sunk time costs: why time is not like money. Journal of Behavioral Decision Making 14(3): 169–185.',
                        html.Br(),  
                        html.Br(),
                        'Arkes, H.R., and C. Blumer. 1985. The psychology of sunk cost. Organizational Behavior and Human Decision Processes 35(1): 124–140.'
                    ],
                    title="References",
                ),
            ],
            always_open=True,
            start_collapsed=True,
        ),
        style={'margin-bottom': '50px'}
    ),  # End of Accordion
    
    html.H5('Prompt used in the experiment:'),
    html.Br(),
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
    html.Hr(),
    html.Br(),
    # Experiment 2
    html.H3("Experiment 2"),
    html.Br(),
    html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P("Participants are presented with a scenario involving a case of Bordeaux wine purchased in the futures market for $20 a bottle, which now sells at auction for $75. They are asked to choose the option that best reflects their perception of the cost of drinking one bottle from the case (A: $0, B: $20, C: $20 plus interest, D: $75, E: -$55)."),
                        html.P('The correct answer according to economic theory is $75. But the majority of the participants chose either option A or E, indicating that they perceive drinking the bottle was either free or saved them money. (Fun fact: Regarding answer option E, Thaler (2015) writes: "When we included option (e), which we found greatly amusing, we were not sure anyone would select it. We wondered whether there were really people who are so sophisticated in their use of mental accounting that they can consider the drinking of an expensive bottle of wine as an act that saves them money.")'),
                        html.P("This experiment explores LLMs' understanding of sunk costs, opportunity costs, and perceived value in consumption decisions. By analyzing LLMs' responses, researchers can gain insights into how LLMs conceptualize the costs associated with consuming goods they have already invested in, shedding light on decision-making biases and rationality in economic behavior."),
                    ],
                    title="Description and motivation of the experiment",
                ),
                dbc.AccordionItem(
                    [
                        html.P('Each LLM was asked 50 times to choose between the five options. To guide the model to answer only with the label of the answer option, the instruction role was set to "Please answer by only giving the letter of the answer option A, B, C, D or E.". The temperature parameter was set to 0.5, 1 and 1.5.'),   
                        html.P("Furthermore, the order of the answer options has been shuffled two times, offering researchers insights into the impact of response order on LLMs' decision-making tendencies, thereby uncovering potential biases in LLMs' responses."), 
                    ],
                    title="Implementation of the experiment",
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
            html.P(["A: $75 [...]",
                    html.Br(),  # Line break
                    "B: -$55 [...]",
                    html.Br(),  # Line break
                    "C: $0 [...]",
                    html.Br(),  # Line break
                    "D: $20 [...]",
                    html.Br(),  # Line break
                    "E: $20, plus interest."]),
        ], style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '60px', 'vertical-align': 'top'}),

        html.Div([
            html.H6('Answer Option Order 3', style={'margin-top': '15px'}),
            html.P(["A: -$55 [...]",
                    html.Br(),  # Line break
                    "B: $75 [...]",
                    html.Br(),  # Line break
                    "C: $20 plus interest.",
                    html.Br(),  # Line break
                    "D: $0 [...]",
                    html.Br(),  # Line break
                    "E: $20 [...]"]),
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