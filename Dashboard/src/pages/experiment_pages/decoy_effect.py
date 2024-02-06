# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
import pickle
from ast import literal_eval


dash.register_page(__name__, path='/decoy-effect', name='Decoy Effect', location='experiments')


### Decoy Effect ###

# Load Decoy Effect experiment results
DE_probs = pd.read_csv("src/data/Output/DE_probs.csv")

# Prompts for Decoy Effect experiments
with open ("src/data/Input/DE_prompts.pkl", "rb") as file:
    DE_prompts = pickle.load(file)

# Dictionary that returns the prompt for a given experiment
DE_experiment_prompts_dict = {
    "DE_1_1": DE_prompts[0],
    "DE_1_2": DE_prompts[1],
    "DE_1_3": DE_prompts[2],
    "DE_1_4": DE_prompts[3],
    "DE_1_5": DE_prompts[4],
    "DE_1_6": DE_prompts[5],
    "DE_1_7": DE_prompts[6],
    "DE_1_8": DE_prompts[7],
    "DE_2_1": DE_prompts[0],
    "DE_2_2": DE_prompts[1],
    "DE_2_3": DE_prompts[2],
    "DE_2_4": DE_prompts[3],
    "DE_2_5": DE_prompts[4],
    "DE_2_6": DE_prompts[5],
    "DE_2_7": DE_prompts[6],
    "DE_2_8": DE_prompts[7],
    "DE_3_1": DE_prompts[0],
    "DE_3_2": DE_prompts[1],
    "DE_3_3": DE_prompts[2],
    "DE_3_4": DE_prompts[3],
    "DE_3_5": DE_prompts[4],
    "DE_3_6": DE_prompts[5],
    "DE_3_7": DE_prompts[6],
    "DE_3_8": DE_prompts[7],
}



# Function for plotting results of decoy effect/prospect theory experiments
def DE_plot_results(df):

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
    bargap = 0.3  # Gap between temperature values
)
    return fig


# Layout
layout = [
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
            "However, once ", html.B("option B was removed"), " and the choice had to be made only between A and C, ", html.B("68%"), " of the participants chose option ", html.B("A"), " while only ", html.B("32%"), " chose option ", html.B("C"),".",
            html.Br(),
            html.Br(),
            """In the experiments below, we examine how various Large Language Models react to this kind of experiment. We therefore queried 3 different models over a range of possible 
            temperature values using either primed or unprimed prompts. On top of that, we investigated to what extent the models' responses change, when we rename and reorder the 
            answer options. In the case of primed prompts, we instructed the model to be a market researcher, who knows about the Decoy Effect in product pricing."""]),
            html.Br(),
            html.B("Note: "), """For both openAI models, setting a temperature of 0 is possible. However, for the Llama model, a temperature of 0 is not a valid input parameter.
            The minimum temperature value for the Llama model is 0.01. Therefore, although it is possible to select both values for every model, 0 only works for the
            openAI models, while 0.01 only works for the Llama model.""",
            html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select scenario"),
                    dcc.Dropdown(
                         id = "decoy-scenario-dropdown",
                         options = [
                              {"label": "Scenario 1: All options present", "value": 1},
                              {"label": "Scenario 2: Decoy option removed", "value": 2},
                         ],
                    value=1,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select prompt design"),
                    dcc.Dropdown(
                         id = "decoy-priming-dropdown",
                         options = [
                              {"label": "Unprimed", "value": 0},
                              {"label": "Primed", "value": 1},
                            ],
                    value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select answer ordering"),
                    dcc.Dropdown(
                         id = "decoy-reordering-dropdown",
                         options = [
                              {"label": "Original order", "value": 0},
                              {"label": "Answer options reordered", "value": 1},
                            ],
                      value=0,
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select language model"),
                    dcc.Dropdown(
                         id = "decoy-model-dropdown",
                         options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                              {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                              {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                      value="gpt-3.5-turbo",
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                html.Div(
                    [
                        html.Label("Select Temperature value"),             
                        dcc.Slider(
                        id="DE-temperature-slider",
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
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="decoy-plot-output", style={'width': '70%', 'height': '60vh'}),

        ],
        style={'display': 'flex', 'flexDirection': 'row'}),
            # Display of prompt
        html.Div(
        id='DE-prompt',
        style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'},
    )]


# Callback for decoy page
@dash.callback(
    [Output("decoy-plot-output", "figure"),
     Output("DE-prompt", "children")],
    [Input("decoy-scenario-dropdown", "value"),
     Input("decoy-priming-dropdown", "value"),
     Input("decoy-reordering-dropdown", "value"),
     Input("decoy-model-dropdown", "value"),
     Input("DE-temperature-slider", "value")]
     )
def update_decoy_plot(selected_scenario, selected_priming, selected_reordering, selected_model, selected_temperature):
    df = DE_probs[(DE_probs["Scenario"] == selected_scenario) & (DE_probs["Priming"] == selected_priming) &
                   (DE_probs["Reorder"] == selected_reordering) & (DE_probs["Model"] == selected_model) & (DE_probs["Temp"] == selected_temperature)] 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = DE_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return DE_plot_results(df), prompt 