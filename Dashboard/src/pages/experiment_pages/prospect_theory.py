# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from PIL import Image
from ast import literal_eval
import pickle
import os 
from utils.plotting_functions import PT_plot_results
from utils.plotting_functions import PT2_plot_results
from utils.plotting_functions import PT_plot_og_results


dash.register_page(__name__, path='/prospect-theory', name='Prospect Theory', location='experiments')


# Load in results and graphs of Prospect Theory experiments
PT_probs = pd.read_csv("data/Output/PT_probs.csv")

# Second Prospect Theory experiment
PT2_probs = pd.read_csv("data/Output/PT2_probs.csv")
PT_og_results = pd.read_csv("data/Input/PT_og_results.csv")



### Prospect Theory 1 ###

# Prompts for PT experiments
with open ("data/Input/PT_prompts.pkl", "rb") as file:
    PT_prompts = pickle.load(file)


# Load PT prompt dictionary
with open ("data/Input/PT_dictionaries.pkl", "rb") as file:
    PT_dictionaries = pickle.load(file)
PT_experiment_prompts_dict = PT_dictionaries[0]


### Prospect Theory 2 ###

# Scenario 1
with open("data/Input/PT2_prompts_1.pkl", "rb") as file:
    PT2_prompts_1 = pickle.load(file)

# Scenario 2
with open("data/Input/PT2_prompts_2.pkl", "rb") as file:
    PT2_prompts_2 = pickle.load(file)

# Scenario 3
with open("data/Input/PT2_prompts_3.pkl", "rb") as file:
    PT2_prompts_3 = pickle.load(file)

# Scenario 4
with open("data/Input/PT2_prompts_4.pkl", "rb") as file:
    PT2_prompts_4 = pickle.load(file)

# Load PT2 prompt dictionary
with open("data/Input/PT2_dictionaries.pkl", "rb") as file:
    PT2_dictionaries = pickle.load(file)
PT2_experiment_prompts_dict = PT2_dictionaries[0]


# Prospect Page
layout = [
     html.H1("Prospect Theory and Mental Accounting Experiment", className="page-heading"),
     html.Hr(),
     dbc.Accordion(
         [
        dbc.AccordionItem(
            dcc.Markdown(["""
                          Prospect Theory, as described by Kahneman/Tversky (1979), is an important concept which holds numerous implications that can be utilized 
                          in the context of Marketing and generally help to better understand consumer behavior.   
                          It describes how individuals make decisions under uncertainty and how they perceive and process information in this situation.       
                          According to Prospect Theory, perceived gains and losses are evaluated relative to a reference point, suggesting the effectiveness of *framing*
                          in affecting consumers choices.   
                          On top of that, losses weigh more heavily than gains, which leads to the so-called *Endowment Effect*.   
                          Together with the notion of decreasing sensitivity, the representative S-shape of the Prospect Theory value function results.     
                          This value function is concave for gains and convex for losses, implying that individuals are *risk-averse* for gains but *risk-seeking* for losses.    
                          Furthermore, the difference between $50 and $60 is perveiced to be greater than the difference between $100 and $110. Although identical in 
                          absolute numbers, the relative difference plays a bigger role in the individual's decision.

                          **4 main principles** can be derived from this Theory that utilized for practical application: 

                          **1) Segregation of gains:** Do not add up gains, but communicate them seperately.
                          * The perceived value of gaining $50 twice will be higher than gaining $100 once. Communicate positive product characteristica separately. 

                          **2) Integration of losses:** Do not communicate occurring losses separately, but add them up with other occurring losses or ideally gains.    
                          * The perceived loss of losing $50 twice will be greater than losing $100 once. Credit cards pool multiple individual losses into one. 

                          **3) Cancellation of losses against larger gains:** When confronted with mixed gains, clearly communicate the positive net outcome.     
                          * Taxes are immediately deducted from paychecks. Initial losses in stock trading seem negligible, once the stock goes up. 
                          * Consumers tend to book losses and gains into different fictitious accounts (*Mental Accounting*). Cancellation of losses against larger gains prevents this.

                          **4) Segregation of silver linings:** Communicate the positive aspects of a product separately from the negative ones.    
                          * Car dealerships often give *special* discounts on the almost final offer to persuade the customer to buy.

                          The implications, that Prospect Theory holds are applied in a wide range fields and can be especially effective in the context of Marketing.     
                          To research, whether Large Language Models also abide by the aforementioned principles, we recreated an experiment originally conducted by Richard Thaler in 1985.
                          There, he confronted 87 students in an undergraduate statistics class at Cornell University with 4 different scenarios, each dealing with one of the
                          above mentioned principles. The exact phrasing of the scenarios can be found below.    
                          The experiment was chosen, especially because of the practical relevance, that Prospect Theory and Mental Accounting hold. On top of that, the original work
                          by Kahneman and Tversky, as well as the work by Richard Thaler are considered to be of enormous importance in the field of Behavioral Economics and
                          Consumer Psychology.    
                          Furthermore, the original study design can be adapted and reapplied on Large Language models, without having to change a lot of
                          the original setup. This is especially important, to maximize the comparability of the original results and the ones obtained by this research.                       
                          """]),
                    title = "Experiment Description"),
        dbc.AccordionItem(
                    dcc.Markdown(["""
                                  The experiment below aims to research to what extent the Large Language models abide by the rules of Prospect Theory and Mental Accounting.    
                                  To achieve this, we used a total of 8 different prompts and presented each prompt 100 times for GPT-3.5-Turbo and, for cost reasons,
                                  50 times for GPT-4-1106-Preview and LLama-2-70b.      
                                  The prompts used to query the LLMs as well as the original phrasing by Thaler (1985) will be displayed below and next to the graph.     
                                  In constructing the prompts, we tried to stick to the original phrasing as close as possible, while still instructing the models sufficiently well
                                  to produce meaningful results.   
                                  As in all experiments, we limited the number of maximum tokens to be generated and used the instruction role to tell the models only to answer
                                  with the letter of the option they would choose, without providing any reasoning.   
                                  To achieve more meaningful results, the instruction text was also included in the prompts themselves.   
                                  Furthermore, all prompts were presented to each language model over a range of temperature values. This was done to research how the models' answers
                                  might change depending on this parameter, and if there may be an *optimal* temperature value that leads to an approximation of the original
                                  results as obtained by Thaler.   
                                  Similar to the Decoy Effect experiment, we again also regarded the aspect of *Priming*. Here, we specifically told the model, to take the role
                                  of a market researcher, that focusses on Prospect Theory and Mental Accounting. Since *Priming* is proven to have a significant impact on human
                                  decision making processes, it is especially interesting to see, if this phenomenon also occurs in the models' answers. 

                                  Therefore, the aforementioned 8 different prompts resulted from:

                                  * 4 scenarios (4 options)
                                    * Integration of losses
                                    * Segragation of gains
                                    * Cancellation of losses against larger gains
                                    * Segregation of silver linings
                                  
                                  
                                 * Primed and unprimed prompts (2 options)                          
                            """]),
                    title = "Implementation of the experiment"),
        dbc.AccordionItem(
            dcc.Markdown("""
                Thaler, Richard. “Mental Accounting and Consumer Choice.” Marketing Science, vol. 4, no. 3, 1985, pp. 199–214. JSTOR, http://www.jstor.org/stable/183904. Accessed 12 Feb. 2024.
                """),
                          title = "References"), 
                    
         ],
        start_collapsed=True,
        ),
html.Br(),
html.Hr(),
html.H2("Experiment 1: Recreating the original study"),
html.Hr(),
# Scenario 1: Segregation of gains
html.Div(
    children=[
        html.H3("Scenario 1: Segregation of gains"),
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
                        dbc.Tooltip(
                        """Note: For both openAI models, setting a temperature of 0 is possible. However, for the Llama model, a temperature of 0
                          is not a valid input parameter. The minimum temperature value for the Llama model is 0.01. Therefore, although it is possible
                            to select both values for every model, 0 only works for the openAI models, while 0.01 only works for the Llama model.""",
                        target="prospect-scenario1-temperature-slider",
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

html.Hr(),    
# Scenario 2: Integration of losses
html.Div(
    children=[
        html.H3("Scenario 2: Integration of losses"),
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
                        dbc.Tooltip(
                        """Note: For both openAI models, setting a temperature of 0 is possible. However, for the Llama model, a temperature of 0
                          is not a valid input parameter. The minimum temperature value for the Llama model is 0.01. Therefore, although it is possible
                            to select both values for every model, 0 only works for the openAI models, while 0.01 only works for the Llama model.""",
                        target="prospect-scenario2-temperature-slider",
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

html.Hr(),    
# Scenario 3: Cancellation of losses against larger gains
html.Div(
    children=[
        html.H3("Scenario 3: Cancellation of losses against larger gains"),
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
                        dbc.Tooltip(
                        """Note: For both openAI models, setting a temperature of 0 is possible. However, for the Llama model, a temperature of 0
                          is not a valid input parameter. The minimum temperature value for the Llama model is 0.01. Therefore, although it is possible
                            to select both values for every model, 0 only works for the openAI models, while 0.01 only works for the Llama model.""",
                        target="prospect-scenario3-temperature-slider",
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

html.Hr(),
# Scenario 4: Segregation of silver linings
html.Div(
    children=[
        html.H3("Scenario 4: Segregation of silver linings"),
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
                        dbc.Tooltip(
                        """Note: For both openAI models, setting a temperature of 0 is possible. However, for the Llama model, a temperature of 0
                          is not a valid input parameter. The minimum temperature value for the Llama model is 0.01. Therefore, although it is possible
                            to select both values for every model, 0 only works for the openAI models, while 0.01 only works for the Llama model.""",
                        target="prospect-scenario4-temperature-slider",
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
dbc.Accordion(
    [
    dbc.AccordionItem(
    dcc.Markdown(["""
                  In the previous experiment, we regarded whether or not LLMs abide by the rules of Prospect Theory and Mental Accounting. However, as mentioned on the Start Page,
                  Large Language Models, among other sources, are trained on text data that is freely available on the internet. Parts of this might also include the original study,
                  or at least discussions about it, by Thaler (1985).     
                  Disregarding the actual outcome of the previous experiment, it is possible that the models' answers are influenced by the original study, if it 
                  was in fact, to some extent, part of the training data.   
                  Therefore, it is interesting to research how the models' answers might change, once we deviate from the original numbers used in the experiment.     
                  Furthermore, one key concept of the Prospect Theory experiment is, that in every situation, both described individuals do actually gain or lose the same amount of money.
                  But how do LLMs react, if in the given scenarios, one individual is financially clearly better off than the other?     
                  Another important notion of Prospect Theory is *decreasing sensitivity*. A loss of $50 subtracted from a total amount of $1000 will not hurt as much, as losing
                  $50, when we initially only had $100. Will the models take this into consideration? And how will the answers change, if we do not deal with round numbers anymore?

                  To research this, we created 6 different configurations for each of the 4 scenarios as they are described in the previous experiment:

                  * Configuration 1: Original numbers scaled by factor Pi * 100
                  * Configuration 2: Original numbers scaled by factor Pi * 42
                  * Configuration 3: A is better off by 25$
                  * Configuration 4: A is better off by 50$
                  * Configuration 5: B is better off by 25$
                  * Configuration 6: B is better off by 50$

                  Note, that in configurations 1 & 2 the numbers used in the prompt are scaled by the factor Pi to create odd numbers, but the relation between the numbers remains the same.
                  Combining 4 scenarios with 6 configurations each resulted in a total of 24 prompts. Again, the exact prompts used in the experiment will be displayed below the graph.     
                  Similar to all other experiments we presented each prompt 100 times for GPT-3.5-Turbo and, for cost reasons, 50 times for GPT-4-1106-Preview and LLama-2-70b. 
                  On top of that, we only used the temperature values 0.5, 1 and 1.5, since we already regard broader ranges of temperature values in other experiments.
                  The aspect of *Priming* will also not be considered in this experiment.
                 """]), title = "Description and implementation of the experiment")
    ],        
    start_collapsed=True,
),

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
                    style={'width': '75%', 'margin': 'auto', 'margin-bottom': '5px'},
                    ),
                    html.Label("Select configuration", style={'margin': 'auto'}),
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
    html.Hr(),
    # Display of original results
    html.Div( 
    children=[
        html.Br(),
        html.H4("Comparison to original study", style={'margin-bottom': '0px'}),
        html.Div(
            style={'display': 'flex', 'align-items': 'center'},  
            children=[
            html.P(
                [
                    html.Br(),
                    html.Br(),
                    """In Experiment 2: Odd numbers and unfair scenarios, we purposely deviated from the original study design. Although this helps research to what 
                    extent the models' answers may somehow be influenced by the original study,  we do not observe a ground truth, i.e. original results. """,
                    html.Br(),
                    """Therefore, the graph on the right helps compare the models' answers to the original results. However, we have to keep in mind, that 
                    this can merely serve as some from of orientation, because the actual questions asked in the original experiments were, in terms of absolute values,
                    not identical to our prompts.""",
                    html.Br(),
                    html.Br(),
                    "Along the x-axis, the different scenarios are listed, being:",
                    html.Br(),
                    "Scenario 1: Segregation of gains",
                    html.Br(),
                    "Scenario 2: Integration of losses",
                    html.Br(),
                    "Scenario 3: Cancellation of losses against larger gains",
                    html.Br(),
                    "Scenario 4: Segregation of silver linings",
                ],
                style={'width': '30%', 'margin-bottom': '50px'}
            ),  # plot with original results 
                dcc.Graph(id="prospect2-og-plot", style={'width': '70%', 'height': '60vh', 'margin': 'auto'}),
            ]
        ),
    ]
)
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
    print(os.getcwd())
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
def update_prospect3(selected_priming, selected_model, selected_temperature):
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
def update_prospect4(selected_priming, selected_model, selected_temperature):
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
    og_plot = PT_plot_og_results(PT_og_results) # Also being replotted for every new input right now. Not optimal, but no big issue. 
    return PT2_plot_results(df), prompt, og_plot 