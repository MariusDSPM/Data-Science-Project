### Decoy Effect ###

# Required imports
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
import pickle
from ast import literal_eval
from utils.plotting_functions import DE_plot_results
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/decoy-effect', name='Decoy Effect', location='experiments')



# Load Decoy Effect experiment results
DE_probs = pd.read_csv("data/Output/DE_probs.csv")

# Load Decoy Effect prompts
with open ("data/Input/DE_prompts.pkl", "rb") as file:
    DE_prompts = pickle.load(file)

# Load Decoy Effect prompt dictionary
with open ("data/Input/DE_dictionaries.pkl", "rb") as file:
    DE_dictionaries = pickle.load(file)
DE_experiment_prompts_dict = DE_dictionaries[0]



# Layout
layout = [
    html.H1("Decoy Effect Experiment", className="page-heading"), 
    html.Hr(),
    html.Br(),
    dbc.Accordion(
         [
        dbc.AccordionItem(
            dcc.Markdown("""
                The decoy effect, also known as the asymmetric dominance effect, describes a phenomenon, in which consumers' preferences between two products change,
                once a third option is added.   
                This third option is designed to be asymmetrically dominated, meaning that it is entirely inferior to one of the previous options,
                but only partially inferior to the other.   
                Once this asymetrically dominated option, the Decoy, is present, more people will now tend to choose the dominating option than before.     
                A decoy product can therefore be used to influence consumer's decision making and increase sales of a specific product merely 
                through the presence of an additional alternative.       
                Our experiment aims to recreate the experiment of Dan Ariely in his 2008 book *Predictably Irrational*, which was based on a true story by the *The Economist* magazine:
                
                There, he asked 100 students from MIT's Sloan School of Management to choose between the following options:   
                
                A: One-year subscription to Economist.com. Includes online access to all articles from The Economist since 1997, priced at 59$        
                B: One-year subscription to the print edition of The Economist, priced at 125$       
                C: One-year subscription to the print edition of The Economist and online access to all articles from The Economist since 1997, priced at 125$       
                In this example, option B serves as the decoy option.

                When presented with **all three options** Ariely found, that **84%** of the participants chose option **C**, while only **16%**  chose option **A**.
                However, once **option B was removed** and the choice had to be made only between A and C, **68%** of the participants chose option **A**, while only **32%** chose option **C**.   
                Obviously, the presence and absence of the Decoy option had a significant impact on the participants' choices. 
                This suggests, that utilizing the Decoy Effect can be a valuable tool for Marketing purposes, for example in developing pricing strategies.    
                Since one important apsect
                          of this research is, whether Large Language Models can act as surrogates in the field of market research, it is especially interesting to see,
                whether those LLMs too exhibit this pattern in their decision-making process. On top of that, the study design being multiple choice between 3 or less options
                can easily be adapted to be conducted on LLMs. That is why we chose to conduct this specific experiment."""),
                title = "Description and motivation of the experiment"
            ),
        dbc.AccordionItem(
                dcc.Markdown("""
                In the experiment below, we examine how the three regarded Large Language Models respond when confronted with this decision.        
                To accomplish this, we used a total of 8 different prompts and presented each prompt 100 times for GPT-3.5-Turbo and, for cost reasons, 50 times for GPT-4-1106-Preview and LLama-2-70b.      
                The prompts will be displayed underneath the graph, once the respective experiment configuration is selected.   
                The phrasing of the prompts is designed to resemble the original format as close as possible, while still being instructive enough to produce meaningful results.    
                To avoid getting an essay-like response, we limited the number of tokens and instructed the models to only answer with the letter of the option they would choose, without any reasoning.    
                This instruction was also appended to the prompts themselves to maximize the number of answers that suit the desired output.                   
                On top of the Decoy Effect itself, we also regarded the aspect of *priming* and *renaming and reordering* the answer options.       
                In the case of *priming*, we specifically told the models to take the role of a market researcher knowing about the Decoy Effect in product pricing. With this, we 
                wanted to research, whether the extent to which the models' answers might adhere to the Decoy Effect, would change.       
                In the second case, we changed the order and names of the answer options, to research whether the extent to which the models' answers might reflect
                certain decision-making patterns present in humans, for example the A-bias, would change.   

                This leads to the aforementioned total of 8 different experiment configurations:

                * Decoy options present vs Decoy option removed (2 options)
                * Primed vs unprimed prompt (2 options)
                * Original order vs adjusted answer options (2 options)
                
                As in all experiments, all prompts were presented to the models over a range of different temperature parameters with multiple queries for each value."""),
                title = "Implementation of the experiment"
            ),
        dbc.AccordionItem(
            dcc.Markdown("""
                Ariely, Dan. Predictably Irrational : the Hidden Forces That Shape Our Decisions. New York :Harper Perennial, 2010.
                """),
                          title = "References"),                    
         ],
        start_collapsed=True,
        ),
        html.Br(),
        html.Hr(),
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
                        dbc.Tooltip(
                        """Note: For both openAI models, setting a temperature of 0 is possible. However, for the Llama model, a temperature of 0
                          is not a valid input parameter. The minimum temperature value for the Llama model is 0.01. Therefore, although it is possible
                            to select both values for every model, 0 only works for the openAI models, while 0.01 only works for the Llama model.""",
                        target="DE-temperature-slider",
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
    # Filter dataframe
    df = DE_probs[(DE_probs["Scenario"] == selected_scenario) & (DE_probs["Priming"] == selected_priming) &
                   (DE_probs["Reorder"] == selected_reordering) & (DE_probs["Model"] == selected_model) & (DE_probs["Temp"] == selected_temperature)] 
    # Grab experiment id to look up prompt
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = DE_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return DE_plot_results(df), prompt 