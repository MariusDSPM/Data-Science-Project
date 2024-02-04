# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
from PIL import Image
from ast import literal_eval
import pickle


dash.register_page(__name__, path='/prospect-theory', name='Prospect Theory', location='experiments')


# Load in results and graphs of Prospect Theory experiments
PT_probs = pd.read_csv("Output/PT_probs.csv")

# Second Prospect Theory experiment
PT2_probs = pd.read_csv("Output/PT2_probs.csv")
PT_og_results = pd.read_csv("Output/PT_og_results.csv")



### Prospect Theory 1 ###
PT_prompt_1 = """Mr. A was given tickets involving the World Series. He won 50$ in one lottery and $25 in the other. 
          Mr. B was given a ticket to a single, larger World Series lottery. He won $75. Based solely on this information, Who was happier? 
          A: Mister A
          B: Mister B
          C: No difference.         
          Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_2 = """Mr. A received a letter from the IRS saying that he made a minor arithmetical mistake on his tax return and owed $100. 
         He received a similar letter the same day from his state income tax authority saying he owed $50. There were no other repercussions from either mistake. 
         Mr. B received a letter from the IRS saying that he made a minor arithmetical mistake on his tax return and owed $150. There were no other repercussions from his mistake. 
         Based solely on this information, who was more upset? 
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_3 = """Mr. A bought his first New York State lottery ticket and won $100. Also, in a freak accident, he damaged the rug in his apartment and had to pay the landlord $80.
         Mr. B bought his first New York State lottery ticket and won $20. Based solely on this information, who was happier? 
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_4 = """Mr. A's car was damaged in a parking lot. He had to spend $200 to repair the damage. The same day the car was damaged, he won $25 in the office football pool.
         Mr. B's car was damaged in a parking lot. He had to spend $175 to repair the damage. Based solely on this information, who was more upset?
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_5 = """You are a market researcher and focus on Prospect Theory and Mental Accounting. In a survey you are presented the following situation: 
          Mr. A was given tickets involving the World Series. He won 50$ in one lottery and 25$ in the other. 
          Mr. B was given a ticket to a single, larger World Series lottery. He won 75$. Based solely on this information, who was happier?
          A: Mister A
          B: Mister B
          C: No difference.
          Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_6 = """You are a market researcher and focus on Prospect Theory and Mental Accounting. In a survey you are presented the following situation:
         Mr. A received a letter from the IRS saying that he made a minor arithmetical mistake on his tax return and owed $100. 
         He received a similar letter the same day from his state income tax authority saying he owed $50. There were no other repercussions from either mistake. 
         Mr. B received a letter from the IRS saying that he made a minor arithmetical mistake on his tax return and owed $150. There were no other repercussions from his mistake. 
         Based solely on this information, who was more upset? 
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_7 = """You are a market researcher and focus on Prospect Theory and Mental Accounting. In a survey you are presented the following situation:
         Mr. A bought his first New York State lottery ticket and won $100. Also, in a freak accident, he damaged the rug in his apartment and had to pay the landlord $80.
         Mr. B bought his first New York State lottery ticket and won $20? Based solely on this information, who was happier?
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_8 = """You are a market researcher and focus on Prospect Theory and Mental Accounting. In a survey you are presented the following situation:
         Mr. A's car was damaged in a parking lot. He had to spend $200 to repair the damage. The same day the car was damaged, he won $25 in the office football pool.
         Mr. B's car was damaged in a parking lot. He had to spend $175 to repair the damage. Based solely on this information, who was more upset?
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""

# Dictionary to look up prompt for a given PT experiment id. key: experiment_id, value: prompt
PT_experiment_prompts_dict = {
    "PT_1_1": PT_prompt_1,
    "PT_1_2": PT_prompt_2,
    "PT_1_3": PT_prompt_3,
    "PT_1_4": PT_prompt_4,
    "PT_1_5": PT_prompt_5,
    "PT_1_6": PT_prompt_6,
    "PT_1_7": PT_prompt_7,
    "PT_1_8": PT_prompt_8,
    "PT_2_1": PT_prompt_1,
    "PT_2_2": PT_prompt_2,
    "PT_2_3": PT_prompt_3,
    "PT_2_4": PT_prompt_4,
    "PT_2_5": PT_prompt_5,
    "PT_2_6": PT_prompt_6,
    "PT_2_7": PT_prompt_7,
    "PT_2_8": PT_prompt_8,
    "PT_3_1": PT_prompt_1,
    "PT_3_2": PT_prompt_2,
    "PT_3_3": PT_prompt_3,
    "PT_3_4": PT_prompt_4,
    "PT_3_5": PT_prompt_5,
    "PT_3_6": PT_prompt_6,
    "PT_3_7": PT_prompt_7,
    "PT_3_8": PT_prompt_8,
}

# Function to plot results of PT experiments
def PT_plot_results(df):

    # Transpose for plotting
    df = df.transpose()  
    # Get language model name
    model = df.loc["Model"].iloc[0]
    # Get temperature value
    temperature = df.loc["Temp"].iloc[0]
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."].iloc[0]
    # Get original answer probabilities
    og_answers = df.loc["Original"].apply(literal_eval).iloc[0]
    # Get number of original answers
    n_original = df.loc["Original_count"].iloc[0]

    fig = go.Figure(data=[
        go.Bar(
            name = "Model answers",
            x = ["p(A)", "p(B)", "p(C)"],
            y = [df.loc["p(A)"].iloc[0], df.loc["p(B)"].iloc[0], df.loc["p(C)"].iloc[0]],
            customdata = [n_observations, n_observations, n_observations], 
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(55, 83, 109)"
        ),
        go.Bar(
            name = "Original answers",
            x = ["p(A)","p(B)", "p(C)"],
            y = [og_answers[0], og_answers[1], og_answers[2]],
            customdata = [n_original, n_original, n_original],
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(26, 118, 255)"
        )
    ])

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        title = "Answer options",  
        title_font=dict(size=18),  
    ),
    yaxis = dict(
        title="Probability (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text=f"Distribution of answers for temperature {temperature}, using model {model}",
        x = 0.5, # Center alignment horizontally
        y = 0.87,  # Vertical alignment
        font=dict(size=22),  
    ),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black', 
        borderwidth=2,  
    ),
)
    return fig

### Prospect Theory 2 ###
# Scenario 1
with open("Output/PT2_prompts_1.pkl", "rb") as file:
    PT2_prompts_1 = pickle.load(file)

# Scenario 2
with open("Output/PT2_prompts_2.pkl", "rb") as file:
    PT2_prompts_2 = pickle.load(file)

# Scenario 3
with open("Output/PT2_prompts_3.pkl", "rb") as file:
    PT2_prompts_3 = pickle.load(file)

# Scenario 4
with open("Output/PT2_prompts_4.pkl", "rb") as file:
    PT2_prompts_4 = pickle.load(file)

# Dictionary to look up prompt for a given PT2 experiment id. key: experiment id, value: prompt
PT2_experiment_prompts_dict = {
    "PT2_1_1_1": PT2_prompts_1[0],
    "PT2_1_1_2": PT2_prompts_1[1],
    "PT2_1_1_3": PT2_prompts_1[2],
    "PT2_1_1_4": PT2_prompts_1[3],
    "PT2_1_1_5": PT2_prompts_1[4],
    "PT2_1_1_6": PT2_prompts_1[5],
    "PT2_2_1_1": PT2_prompts_2[0],
    "PT2_2_1_2": PT2_prompts_2[1],
    "PT2_2_1_3": PT2_prompts_2[2],
    "PT2_2_1_4": PT2_prompts_2[3],
    "PT2_2_1_5": PT2_prompts_2[4],
    "PT2_2_1_6": PT2_prompts_2[5],
    "PT2_3_1_1": PT2_prompts_3[0],
    "PT2_3_1_2": PT2_prompts_3[1],
    "PT2_3_1_3": PT2_prompts_3[2],
    "PT2_3_1_4": PT2_prompts_3[3],
    "PT2_3_1_5": PT2_prompts_3[4],
    "PT2_3_1_6": PT2_prompts_3[5],
    "PT2_4_1_1": PT2_prompts_4[0],
    "PT2_4_1_2": PT2_prompts_4[1],
    "PT2_4_1_3": PT2_prompts_4[2],
    "PT2_4_1_4": PT2_prompts_4[3],
    "PT2_4_1_5": PT2_prompts_4[4],
    "PT2_4_1_6": PT2_prompts_4[5],
    "PT2_1_2_1": PT2_prompts_1[0],
    "PT2_1_2_2": PT2_prompts_1[1],
    "PT2_1_2_3": PT2_prompts_1[2],
    "PT2_1_2_4": PT2_prompts_1[3],
    "PT2_1_2_5": PT2_prompts_1[4],
    "PT2_1_2_6": PT2_prompts_1[5],
    "PT2_2_2_1": PT2_prompts_2[0],
    "PT2_2_2_2": PT2_prompts_2[1],
    "PT2_2_2_3": PT2_prompts_2[2],
    "PT2_2_2_4": PT2_prompts_2[3],
    "PT2_2_2_5": PT2_prompts_2[4],
    "PT2_2_2_6": PT2_prompts_2[5],
    "PT2_3_2_1": PT2_prompts_3[0],
    "PT2_3_2_2": PT2_prompts_3[1],
    "PT2_3_2_3": PT2_prompts_3[2],
    "PT2_3_2_4": PT2_prompts_3[3],
    "PT2_3_2_5": PT2_prompts_3[4],
    "PT2_3_2_6": PT2_prompts_3[5],
    "PT2_4_2_1": PT2_prompts_4[0],
    "PT2_4_2_2": PT2_prompts_4[1],
    "PT2_4_2_3": PT2_prompts_4[2],
    "PT2_4_2_4": PT2_prompts_4[3],
    "PT2_4_2_5": PT2_prompts_4[4],
    "PT2_4_2_6": PT2_prompts_4[5],
    "PT2_1_3_1": PT2_prompts_1[0],
    "PT2_1_3_2": PT2_prompts_1[1],
    "PT2_1_3_3": PT2_prompts_1[2],
    "PT2_1_3_4": PT2_prompts_1[3],
    "PT2_1_3_5": PT2_prompts_1[4],
    "PT2_1_3_6": PT2_prompts_1[5],
    "PT2_2_3_1": PT2_prompts_2[0],
    "PT2_2_3_2": PT2_prompts_2[1],
    "PT2_2_3_3": PT2_prompts_2[2],
    "PT2_2_3_4": PT2_prompts_2[3],
    "PT2_2_3_5": PT2_prompts_2[4],
    "PT2_2_3_6": PT2_prompts_2[5],
    "PT2_3_3_1": PT2_prompts_3[0],
    "PT2_3_3_2": PT2_prompts_3[1],
    "PT2_3_3_3": PT2_prompts_3[2],
    "PT2_3_3_4": PT2_prompts_3[3],
    "PT2_3_3_5": PT2_prompts_3[4],
    "PT2_3_3_6": PT2_prompts_3[5],
    "PT2_4_3_1": PT2_prompts_4[0],
    "PT2_4_3_2": PT2_prompts_4[1],
    "PT2_4_3_3": PT2_prompts_4[2],
    "PT2_4_3_4": PT2_prompts_4[3],
    "PT2_4_3_5": PT2_prompts_4[4],
    "PT2_4_3_6": PT2_prompts_4[5],
}

# Function to plot results of PT2 experiments (no ground truth present)
def PT2_plot_results(df):
    # Grab experiment id
    experiment_id = df["Experiment_id"].iloc[0]
    # Transpose for plotting
    df = df.transpose()  
    # Get language model name
    model = df.loc["Model"].iloc[0]
    # Get temperature value
    temperature = df.loc["Temp"].iloc[0]
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."].iloc[0]

    fig = go.Figure(data=[
        go.Bar(
            name = "Model answers",
            x = ["p(A)", "p(B)", "p(C)"],
            y = [df.loc["p(A)"].iloc[0], df.loc["p(B)"].iloc[0], df.loc["p(C)"].iloc[0]],
            customdata = [n_observations, n_observations, n_observations], 
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(55, 83, 109)",
            showlegend = True,
        ),
    ])

    fig.update_layout(
    xaxis = dict(
        title = "Answer options",  
        title_font=dict(size=18),  
    ),
    yaxis = dict(
        title="Probability (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text=f"Distribution of answers for temperature {temperature}, using model {model}",
        x = 0.5, # Center alignment horizontally
        y = 0.87,  # Vertical alignment
        font=dict(size=22),  
    ),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black', 
        borderwidth=2,  
        
    ),
)
    return fig

# Function to plot original results with hovertemplate
def PT_plot_og_results(df):
    n_original = df["Obs."]  # number of answer options 
    fig = go.Figure(data=[
        go.Bar(
                name = "p(A)",
                x = [0.1, 0.3, 0.5, 0.7],
                y = [df["p(A)"][0], df["p(A)"][1], df["p(A)"][2], df["p(A)"][3]],
                customdata = n_original,
                hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
                marker_color="black",
            ),
        go.Bar(
                name = "p(B)",
                x = [0.15, 0.35, 0.55, 0.75],
                y = [df["p(B)"][0], df["p(B)"][1], df["p(B)"][2], df["p(B)"][3]],
                customdata = n_original,
                hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
                marker_color="rgb(55, 83, 109)",

            ),
        go.Bar(
                name = "p(C)",
                x = [0.2, 0.4, 0.6, 0.8],
                y = [df["p(C)"][0], df["p(C)"][1], df["p(C)"][2], df["p(C)"][3]],
                customdata = n_original,
                hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
                marker_color="rgb(26, 118, 255)",
        )
    ])
  

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        title = "Scenarios",  
        title_font=dict(size=18),
        tickfont=dict(size=16),  
    ),
    yaxis = dict(
        title="Probability (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text=f"Distribution of original answers per scenario",
        x = 0.5, 
        y = 0.87,  
        font=dict(size=22),  
    ),
    width = 1000,
    margin=dict(t=100),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black', 
        borderwidth=2,  
    ),
    
)
    # Adjust x-axis labels to show 30+ to symbolize aggregation
    fig.update_xaxes(
    tickvals =[0.15, 0.35, 0.55, 0.75],
    ticktext=["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4"],
)
    return fig
    

# Prospect Page
layout = [
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
                        "Mr. A was given tickets to lotteries involving the World Series. He won $50 in one lottery and $25 in the other. ",
                        "Mr. B was given a ticket to a single, larger World Series lottery. He won $75. Who was happier?",
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ],
                ),
            ],
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario1-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario1-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario1-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot1", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario1-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
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
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
               


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario2-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario2-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario2-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot2", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario2-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
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
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                
            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario3-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario3-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario3-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot3", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario3-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
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
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
            


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.Label("Select prompt design:"),
                dcc.Dropdown(
                    id="prospect-scenario4-priming-dropdown",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                ),
                html.Label("Select language model:"),
                dcc.Dropdown(
                    id="prospect-scenario4-model-dropdown",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'}
                ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect-scenario4-temperature-slider",
                            min=0.00,
                            max=2,
                            marks={0.00: '0.01', 0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
        ),
        dcc.Graph(id="prospect-plot4", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect-scenario4-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    )]),

html.Br(),
html.Hr(),


## Experiment 2
html.H2("Experiment 2: Odd numbers and unfair scenarios"),
html.Hr(),
html.P(["""The Prospect Theory value function explains why individuals tend to assess the perceived value of e.g. a sum of multiple gains as larger, 
        than one individual sum of the same amount. Since Large Language Models are trained on human data, including for example customer reviews on sales platforms,
        they might reflect these patterns.""",
        html.Br(), 
        """But how do LLMs react, if in the given scenarios, one individual is financially clearly better off than the other? And what if we did not deal with small,
        even numbers, but rather large and odd ones?""",
        html.Br(),
        "Another ", html.B("key concept of prospect theory is decreasing sensitivity"),":", 
        " A loss of 50$ subtracted from a total amount of 1000$ will not hurt as much, as if we initially only had 100$, hence losing 50% of our total possession.", 
        html.Br(),
        html.Br(),
        "In order to research these 2 aspects, we created 6 configurations for every scenario (1-4):",
        html.Br(),
        html.Br(),
        "- Configuration 1: Original numbers scaled by factor Pi * 100",
        html.Br(),
        "- Configuration 2: Original numbers scaled by factor Pi * 42",
        html.Br(),
        "- Configuration 3: A is better off by 25$",
        html.Br(),
        "- Configuration 4: A is better off by 50$",
        html.Br(),
        "- Configuration 5: B is better off by 25$",
        html.Br(),
        "- Configuration 6: B is better off by 50$",
        html.Br()]),
html.Div(
        children = [
            html.Div(
                children = [
                    html.Label("Select scenario", style={'margin': 'auto'}),
                    dcc.Dropdown(
                        id = "prospect2-scenario-dropdown",
                        options = [
                            {"label": "Scenario 1: Segregation of gains", "value": 1},
                            {"label": "Scenario 2: Integration of losses", "value": 2},
                            {"label": "Scenario 3: Cancellation of losses against larger gains", "value": 3},
                            {"label": "Scenario 4: Segregation of silver linings", "value": 4},
                        ],
                        value = 1,
                    style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select configuration", style={'margin': 'auto', 'margin-bottom': '5px'}),
                    dcc.Dropdown(
                         id = "prospect2-configuration-dropdown",
                            options = [
                                {"label": "Configuration 1: Odd numbers 1", "value": 1},
                                {"label": "Configuration 2: Odd numbers 2", "value": 2},
                                {"label": "Configuration 3: A is better off by 25$", "value": 3},
                                {"label": "Configuration 4: A is better off by 50$", "value": 4},
                                {"label": "Configuration 5: B is better off by 25$", "value": 5},
                                {"label": "Configuration 6: B is better off by 50$", "value": 6},
                                ],
                                value = 1,
                                style = {'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select language model", style={'margin': 'auto'}),
                    dcc.Dropdown(
                         id = "prospect2-model-dropdown",
                         options = [
                                {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                                {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                                {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                            style = {'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                        html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="prospect2-temperature-slider",
                            min=0.5,
                            max=1.5,
                            marks={0.5: '0.5', 1: '1', 1.5: '1.5'},
                            step = None,
                            value=0.5,
                            tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                    ],                 
    
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center', 'margin': 'auto'},
            ),
            dcc.Graph(id = "prospect2-plot", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
),
    # Display of prompt
    html.Div(
    id='prospect2-prompt',
    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    ),
    # Display of original results
    dcc.Graph(id = "prospect2-og-plot", style={'width': '70%', 'height': '60vh', 'margin':'auto'})
]



### Callback for prospect page

## Experiment 1
# Scenario 1
@dash.callback(
     [Output("prospect-plot1", "figure"),
      Output("prospect-scenario1-prompt", "children")],
     [Input("prospect-scenario1-priming-dropdown", "value"), 
      Input("prospect-scenario1-model-dropdown", "value"),
      Input("prospect-scenario1-temperature-slider", "value")] 

)
def update_prospect1(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 1)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return PT_plot_results(df), prompt 

# Scenario 2
@dash.callback(
        [Output("prospect-plot2", "figure"),
         Output("prospect-scenario2-prompt", "children")],
        [Input("prospect-scenario2-priming-dropdown", "value"), 
        Input("prospect-scenario2-model-dropdown", "value"),
        Input("prospect-scenario2-temperature-slider", "value")] 

)
def update_prospect2(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 2)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return PT_plot_results(df), prompt 

# Scenario 3
@dash.callback(
        [Output("prospect-plot3", "figure"),
         Output("prospect-scenario3-prompt", "children")],
        [Input("prospect-scenario3-priming-dropdown", "value"), 
        Input("prospect-scenario3-model-dropdown", "value"),
        Input("prospect-scenario3-temperature-slider", "value")] 

)
def update_prospect2(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 3)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return PT_plot_results(df), prompt 

# Scenario 4
@dash.callback(
        [Output("prospect-plot4", "figure"),
         Output("prospect-scenario4-prompt", "children")],
        [Input("prospect-scenario4-priming-dropdown", "value"), 
        Input("prospect-scenario4-model-dropdown", "value"),
        Input("prospect-scenario4-temperature-slider", "value")] 

)
def update_prospect2(selected_priming, selected_model, selected_temperature):
    df = PT_probs[(PT_probs["Priming"] == selected_priming) & (PT_probs["Model"] == selected_model) &
                   (PT_probs["Temp"] == selected_temperature) & (PT_probs["Scenario"] == 4)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return PT_plot_results(df), prompt 

## Experiment 2
@dash.callback(
        [Output("prospect2-plot", "figure"),
         Output("prospect2-prompt", "children"),
         Output("prospect2-og-plot", "figure")],
        [Input("prospect2-scenario-dropdown", "value"), 
        Input("prospect2-configuration-dropdown", "value"),
        Input("prospect2-model-dropdown", "value"),
        Input("prospect2-temperature-slider", "value")] 

)
def update_prospect_two(selected_scenario, selected_configuration, selected_model, selected_temperature):
    df = PT2_probs[(PT2_probs["Scenario"] == selected_scenario) & (PT2_probs["Configuration"] == selected_configuration) &
                   (PT2_probs["Model"] == selected_model) & (PT2_probs["Temp"] == selected_temperature)] # select scenario manually!!! 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = PT2_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    og_plot = PT_plot_og_results(PT_og_results)
    return PT2_plot_results(df), prompt, og_plot 