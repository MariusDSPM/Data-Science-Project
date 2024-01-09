# Import required libraries 
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
import plotly.graph_objects as go


dash.register_page(__name__, path='/decoy_effect', name='Decoy Effect', location='experiments')


# Load in results of Decoy Effect experiments
DE_probs = pd.read_csv("Output/DE_probs.csv", index_col = 0)


# Function for plotting results of decoy effect/prospect theory experiments
def plot_results(model, priming, df, scenario):
    
    # Get dataframe as specified by user (subset of df)
    df = df[(df['Model'] == model) & (df['Priming'] == priming) & (df['Scenario'] == scenario)]
    # Transpose for plotting
    df = df.transpose()
    
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."]
    
    # Get temperature values
    temperature = df.loc["Temp"]

    fig = go.Figure(data=[
        go.Bar(
            name="p(A)", 
            x=temperature, 
            y=df.loc["p(A)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br>Observations: %{customdata}<extra></extra>",
            marker=dict(color="#e9724d"),
        ),
        go.Bar(
            name="p(B)", 
            x=temperature, 
            y=df.loc["p(B)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
            marker=dict(color="#868686"),
            
        ),
        go.Bar(
            name="p(C)", 
            x=temperature, 
            y=df.loc["p(C)"],
            customdata = n_observations,
            hovertemplate="Temperature: %{x}<br>Probability: %{y:.2f}%<br> Observations: %{customdata}<extra></extra>",
            marker=dict(color="#92cad1"),
        )
    ])

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        tickmode = 'array',
        tickvals = temperature,
        ticktext = temperature,
        title = "Temperature",  
        title_font=dict(size=18),  
    ),
    yaxis = dict(
        title="Probability (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text="Distribution of answers per temperature value",
        x = 0.5, # Center alignment horizontally
        y = 0.87,  # Vertical alignment
        font=dict(size=22),  
    ),
    legend = dict(
        title = dict(text="Probabilities"),
    ),
    bargap = 0.3  # Gap between temperature values
)
    return fig


# Decoy Effect prompts
DE_prompt_1 = """You are presented with the following subscription alternatives for the "The Economist" magazine:
        A: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$.
        B: One-year subscription to the print edition of The Economist, priced at 125$.
        C: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.
        Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
DE_prompt_2 = """You are presented with the following subscription alternatives for the "The Economist" magazine:
        A: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$.
        B: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$. 
        Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
DE_prompt_3 = """You are a market researcher that knows about the Decoy Effect in pricing. 
        You are presented with the following subscription alternatives for the "The Economist" magazine:
        A: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$.
        B: One-year subscription to the print edition of The Economist, priced at 125$.
        C: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.
        Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
DE_prompt_4 = """You are a market researcher that knows about the Decoy Effect in pricing. 
         You are presented with the following subscription alternatives for the "The Economist" magazine:
         A: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$.
         B: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.
         Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
DE_prompt_5 = """You are presented with the following subscription alternatives for the "The Economist" magazine:
         Q: One-year subscription to the print edition of The Economist, priced at 125$.
         X: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.
         Y: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$. 
         Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
DE_prompt_6 = """You are presented with the following subscription alternatives for the "The Economist" magazine:
         X: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.
         Y: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$. 
         Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
DE_prompt_7 = """You are a market researcher that knows about the Decoy Effect in pricing. 
         You are presented with the following subscription alternatives for the "The Economist" magazine:
         Q: One-year subscription to the print edition of The Economist, priced at 125$.
         X: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.
         Y: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$. 
         Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
DE_prompt_8 = """You are a market researcher that knows about the Decoy Effect in pricing. 
         You are presented with the following subscription alternatives for the "The Economist" magazine:
         X: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$.
         Y: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$. 
         Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""


# Dictionary that returns the literal prompt for a given experiment id (used in function call). key: experiment_id, value: prompt
DE_experiment_prompts_dict = {
    "DE_1_1": DE_prompt_1,
    "DE_1_2": DE_prompt_2,
    "DE_1_3": DE_prompt_3,
    "DE_1_4": DE_prompt_4,
    "DE_1_5": DE_prompt_5,
    "DE_1_6": DE_prompt_6,
    "DE_1_7": DE_prompt_7,
    "DE_1_8": DE_prompt_8,
    "DE_2_1": DE_prompt_1,
    "DE_2_2": DE_prompt_2,
    "DE_2_3": DE_prompt_3,
    "DE_2_4": DE_prompt_4,
    "DE_2_5": DE_prompt_5,
    "DE_2_6": DE_prompt_6,
    "DE_2_7": DE_prompt_7,
    "DE_2_8": DE_prompt_8,
    "DE_3_1": DE_prompt_1,
    "DE_3_2": DE_prompt_2,
    "DE_3_3": DE_prompt_3,
    "DE_3_4": DE_prompt_4,
    "DE_3_5": DE_prompt_5,
    "DE_3_6": DE_prompt_6,
    "DE_3_7": DE_prompt_7,
    "DE_3_8": DE_prompt_8,
}

# It returns the variable name of the prompt that was used in the experiment. key: experiment_id, value: prompt_name
DE_prompt_ids_dict = {
    "DE_1_1": "DE_prompt_1",
    "DE_1_2": "DE_prompt_2",
    "DE_1_3": "DE_prompt_3",
    "DE_1_4": "DE_prompt_4",
    "DE_1_5": "DE_prompt_5",
    "DE_1_6": "DE_prompt_6",
    "DE_1_7": "DE_prompt_7",
    "DE_1_8": "DE_prompt_8",
    "DE_2_1": "DE_prompt_1",
    "DE_2_2": "DE_prompt_2",
    "DE_2_3": "DE_prompt_3",
    "DE_2_4": "DE_prompt_4",
    "DE_2_5": "DE_prompt_5",
    "DE_2_6": "DE_prompt_6",
    "DE_2_7": "DE_prompt_7",
    "DE_2_8": "DE_prompt_8",
    "DE_3_1": "DE_prompt_1",
    "DE_3_2": "DE_prompt_2",
    "DE_3_3": "DE_prompt_3",
    "DE_3_4": "DE_prompt_4",
    "DE_3_5": "DE_prompt_5",
    "DE_3_6": "DE_prompt_6",
    "DE_3_7": "DE_prompt_7",
    "DE_3_8": "DE_prompt_8",
}

# Dictionary to look up which model to use for a given experiment id (used in function call). key: experiment id, value: model name
DE_model_dict = {
    "DE_1_1": "gpt-3.5-turbo",
    "DE_1_2": "gpt-3.5-turbo",
    "DE_1_3": "gpt-3.5-turbo",
    "DE_1_4": "gpt-3.5-turbo",
    "DE_1_5": "gpt-3.5-turbo",
    "DE_1_6": "gpt-3.5-turbo",
    "DE_1_7": "gpt-3.5-turbo",
    "DE_1_8": "gpt-3.5-turbo",
    "DE_2_1": "gpt-4-1106-preview",
    "DE_2_2": "gpt-4-1106-preview",
    "DE_2_3": "gpt-4-1106-preview",
    "DE_2_4": "gpt-4-1106-preview",
    "DE_2_5": "gpt-4-1106-preview",
    "DE_2_6": "gpt-4-1106-preview",
    "DE_2_7": "gpt-4-1106-preview",
    "DE_2_8": "gpt-4-1106-preview",
    "DE_3_1": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "DE_3_2": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "DE_3_3": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "DE_3_4": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "DE_3_5": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "DE_3_6": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "DE_3_7": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "DE_3_8": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    }

# Dictionary to look up the original results of the experiments. key: experiment id, value: original result
DE_results_dict = {
    "DE_1_1": "A: 16%, B: 0%, C: 84%",
    "DE_1_2": "A: 68%, B: 0%, C: 32%",
    "DE_1_3": "A: 16%, B: 0%, C: 84%",
    "DE_1_4": "A: 68%, B: 0%, C: 32%",
    "DE_1_5": "A: 16%, B: 0%, C: 84%",
    "DE_1_6": "A: 68%, B: 0%, C: 32%",
    "DE_1_7": "A: 16%, B: 0%, C: 84%",
    "DE_1_8": "A: 68%, B: 0%, C: 32%",
    "DE_2_1": "A: 16%, B: 0%, C: 84%",
    "DE_2_2": "A: 68%, B: 0%, C: 32%",
    "DE_2_3": "A: 16%, B: 0%, C: 84%",
    "DE_2_4": "A: 68%, B: 0%, C: 32%",
    "DE_2_5": "A: 16%, B: 0%, C: 84%",
    "DE_2_6": "A: 68%, B: 0%, C: 32%",
    "DE_2_7": "A: 16%, B: 0%, C: 84%",
    "DE_2_8": "A: 68%, B: 0%, C: 32%",
    "DE_3_1": "A: 16%, B: 0%, C: 84%",
    "DE_3_2": "A: 68%, B: 0%, C: 32%",
    "DE_3_3": "A: 16%, B: 0%, C: 84%",
    "DE_3_4": "A: 68%, B: 0%, C: 32%",
    "DE_3_5": "A: 16%, B: 0%, C: 84%",
    "DE_3_6": "A: 68%, B: 0%, C: 32%",
    "DE_3_7": "A: 16%, B: 0%, C: 84%",
    "DE_3_8": "A: 68%, B: 0%, C: 32%",
}

# Dictionary to look up the scenario of each experiment. key: experiment id, value: scenario (1: With Decoy, 2: Without Decoy)
DE_scenario_dict = {
    "DE_1_1": 1,
    "DE_1_2": 2,
    "DE_1_3": 1,
    "DE_1_4": 2,
    "DE_1_5": 1,
    "DE_1_6": 2,
    "DE_1_7": 1,
    "DE_1_8": 2,
    "DE_2_1": 1,
    "DE_2_2": 2,
    "DE_2_3": 1,
    "DE_2_4": 2,
    "DE_2_5": 1,
    "DE_2_6": 2,
    "DE_2_7": 1,
    "DE_2_8": 2,
    "DE_3_1": 1,
    "DE_3_2": 2,
    "DE_3_3": 1,
    "DE_3_4": 2,
    "DE_3_5": 1,
    "DE_3_6": 2,
    "DE_3_7": 1,
    "DE_3_8": 2,
}

# Dictionary to look up, whether the experiment was primed or not. key: experiment id, value: priming (1: Primed, 0: Unprimed)
DE_priming_dict = {
    "DE_1_1": 0,
    "DE_1_2": 0,
    "DE_1_3": 1,
    "DE_1_4": 1,
    "DE_1_5": 0,
    "DE_1_6": 0,
    "DE_1_7": 1,
    "DE_1_8": 1,
    "DE_2_1": 0,
    "DE_2_2": 0,
    "DE_2_3": 1,
    "DE_2_4": 1,
    "DE_2_5": 0,
    "DE_2_6": 0,
    "DE_2_7": 1,
    "DE_2_8": 1,
    "DE_3_1": 0,
    "DE_3_2": 0,
    "DE_3_3": 1,
    "DE_3_4": 1,
    "DE_3_5": 0,
    "DE_3_6": 0,
    "DE_3_7": 1,
    "DE_3_8": 1,
}

# Dictionary to look up, whether answers were renamed and reordered or not. key: experiment id, value: indicator (1: Renamed and reordered, 0: Not renamed and reordered)
DE_reorder_dict = {
    "DE_1_1": 0,
    "DE_1_2": 0,
    "DE_1_3": 0,
    "DE_1_4": 0,
    "DE_1_5": 1,
    "DE_1_6": 1,
    "DE_1_7": 1,
    "DE_1_8": 1,
    "DE_2_1": 0,
    "DE_2_2": 0,
    "DE_2_3": 0,
    "DE_2_4": 0,
    "DE_2_5": 1,
    "DE_2_6": 1,
    "DE_2_7": 1,
    "DE_2_8": 1,
    "DE_3_1": 0,
    "DE_3_2": 0,
    "DE_3_3": 0,
    "DE_3_4": 0,
    "DE_3_5": 1,
    "DE_3_6": 1,
    "DE_3_7": 1,
    "DE_3_8": 1,
}


# Decoy Page
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
            html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Dropdown(
                         id = "decoy-scenario-dropdown",
                         options = [
                              {"label": "Scenario 1: All options present", "value": 1},
                              {"label": "Scenario 2: Decoy option removed", "value": 2},
                         ],
                         value = 1,
                         style={'width': '75%'},
                    ),
                    dcc.Dropdown(
                         id = "decoy-priming-dropdown",
                         options = [
                              {"label": "Unprimed prompt", "value": 0},
                              {"label": "Primed prompt", "value": 1},
                            ],
                            value = 0,
                            style={'width': '75%'},
                    ),
                    dcc.Dropdown(
                         id = "decoy-reordering-dropdown",
                         options = [
                              {"label": "Original order", "value": 0},
                              {"label": "Answer options reordered", "value": 1},
                            ],
                            value = 0,
                            style={'width': '75%'},
                    ),
                    dcc.Dropdown(
                         id = "decoy-model-dropdown",
                         options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                              {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                              {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                            style={'width': '75%'},
                    ),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="decoy-plot-output", style={'width': '70%', 'height': '60vh'}),
        ],
        
        style={'display': 'flex', 'flexDirection': 'row'})]


# Callback for decoy page
@dash.callback(
    Output("decoy-plot-output", "figure"),
    [Input("decoy-scenario-dropdown", "value"),
     Input("decoy-priming-dropdown", "value"),
     Input("decoy-reordering-dropdown", "value"),
     Input("decoy-model-dropdown", "value")]
     )
def update_decoy_plot(selected_scenario, selected_priming, selected_reordering, selected_model):
    # Pre-select dataframe (plot_results disregards reordering option)
    df = DE_probs[DE_probs["Reorder"] == selected_reordering]
    return plot_results(scenario = selected_scenario, priming = selected_priming, model = selected_model, df = df)