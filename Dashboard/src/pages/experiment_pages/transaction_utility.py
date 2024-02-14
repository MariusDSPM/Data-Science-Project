# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
from PIL import Image
import pickle
from ast import literal_eval
import pandas as pd
import numpy as np
from collections import Counter
from utils.plotting_functions import TU_plot_results, TU2_plot_results, TU3_plot_results, extract_dollar_amounts
import dash_bootstrap_components as dbc

# TU3 will actually be second, since it is a continuation of TU1

dash.register_page(__name__, path='/transaction-utility', name='Transaction Utility', location='experiments')

##### Transaction Utility #####

# Load experiment results 
TU_results = pd.read_csv('data/Output/TU_results.csv')

# Load prompts
with open("data/Input/TU_prompts.pkl", "rb") as file:
    TU_prompts = pickle.load(file)

# Load TU prompt dictionary
with open("data/Input/TU_dictionaries.pkl", "rb") as file:
    TU_dictionaries = pickle.load(file)
TU_experiment_prompts_dict = TU_dictionaries[0]


##### Transaction Utility 2 #####

# Load experiment results
TU2_results = pd.read_csv('data/Output/TU2_results.csv')

# Load prompts
with open("data/Input/TU2_prompts.pkl", "rb") as file:
    TU2_prompts = pickle.load(file)

# Load TU2 prompt dictionary
with open("data/Input/TU2_dictionaries.pkl", "rb") as file:
    TU2_dictionaries = pickle.load(file)
TU2_experiment_prompts_dict = TU2_dictionaries[0]


def extract_dollar_amounts(answers):
    # Only return values that start with "$"
    valid_prices = [item for item in answers if item.startswith("$") and item[1:].replace(',', '').replace('.', '').isdigit()] # check if everything after $ is a digit, exlcuding commas
    # Delete the "$" from the beginning of each price
    prices = [item.replace('$', '') for item in valid_prices]
    return prices

##### Transaction Utility 3 #####

# Load experiment results
TU3_results = pd.read_csv('data/Output/TU3_results.csv')

# Load prompts
with open("data/Input/TU3_prompts.pkl", "rb") as file:
    TU3_prompts = pickle.load(file)

# Load TU3 prompt dictionary
with open("data/Input/TU3_dictionaries.pkl", "rb") as file:
    TU3_dictionaries = pickle.load(file)
TU3_experiment_prompts_dict = TU3_dictionaries[0]

configurations1 = pd.DataFrame(
    {
        "Initial_cost": [0, 0, 0, 0, 5, 5, 5, 5, 10, 10, 10, 10],
        "Orientation_price": [5, 5, 10, 10, 5, 5, 10, 10, 5, 5, 10, 10],
        "Buyer": ["Friend", "Stranger", "Friend", "Stranger", "Friend", "Stranger", "Friend", "Stranger", "Friend", "Stranger", "Friend", "Stranger"],
        "Configuration": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  

    }
)
table = dbc.Table.from_dataframe(configurations1, striped=True, bordered=True, hover=True)

### Layout ###
layout = [
    html.H1("Transaction Utility experiments", className="page-heading"),
     html.Hr(),
     dbc.Accordion(
         [
        dbc.AccordionItem(
            dcc.Markdown(["""
                          Richard Thaler differentiates between two forms of utility: *Acquisition utility* and *Transaction utility*. The first aspect depends on the value
                          of the product received relative to the money spent, while the second aspect relies solely on the perceived advantages of the transaction itself.
                          The assessment of transaction utility is influenced by the price an individual pays relative to some reference price. The total utility of a transaction,
                          although a rather abstract concept, then results as the sum of acquisition and transaction utility.    
                          Therefore, the reference price is crucial for assessing the perceived overall utility of a purchase. Thaler describes, that one important
                          determinant that drives the reference price is fairness, which in turn depends on the costs of the seller. Extentious overpricing would hence
                          be perceived as unfair and decrease transaction utility, even if acquisition utility is high.    
                          One prominent example that illustrates this phenomenon is water at the Airport. While the acquisition utility may be high, because individuals are 
                          thirsty and satisfying this need is crucial and definitely worth paying $6 for, people will still feel ripped off, because water is usually not
                          that expensive. Therefore the transaction utility of this deal would be rather low.    
                          As mentioned before, individuals' expectations about the seller's costs are a key determinant that drives the expectation of a fair reference price.
                          
                          In order to research to what extent buyers' expectation about the seller's costs influence individuals perception of a fair price, Thaler presented 
                          first-year MBA students with the following scenario: 

                          *"Imagine that you are going to a sold-out Cornell hockey playoff game, and you have an extra ticket to sell or give away.
                          The price marked on the ticket is $5 but you were given your tickets for free by a friend/which is what you paid for each ticket/
                          but you paid $10 each for your tickets when you bought them from another student. You get to the game early to make sure you get rid of the ticket.
                          An informal survey of people selling tickets indicates that the going price is $5. You find someone who wants the ticket and takes out his wallet to pay you.
                          He asks how much you want for the ticket. Assume that there is no law against charging a price higher than that marked on the ticket.
                          What price do you ask for if he is a friend?/he is a stranger?. What would you have said if instead you found the going market price was $10?"*

                          The slashes indicate variations of the question. The basic idea was, that the price people would charge a friend would be a good approximation for the
                          perceived fair price. Thaler found, that the modal answers in the friend condition were mostly equal to the initial costs (seller's costs), thus indicating
                          that seller's costs will significantly shape individuals' perception of a fair price.

                          This experiment was chosen as the first *open answer style* experiment, because answers can be expected to be strongly influenced by the anchors,
                          in form of reference prices, as given in the prompts. This is also reflected in the original results. Therefore, prior to the experiment, a clear
                          expectation of what the answers will look like was given, which makes post-processing the results more efficient.     
                          Furthermore, although consumers will most likely not be aware of the concept itself, online product reviews, on which the LLMs might have been trained
                          can be expected to be influenced by this phenomenon (e.g. through overpricing). Therefore, we can expect the model answers to also reflect this trait.
                          """]),
                    title = "Experiment Description"),
        dbc.AccordionItem(
                    dcc.Markdown(["""
                                  In the experiment below, we try to recreate the original study by Thaler published in 1985 with Large Language Models as respondents.
                                  In order to do so, we created 12 different prompts, and presented each prompt 100 times for GPT-3.5-Turbo and, for cost reasons,
                                  50 times for GPT-4-1106-Preview and LLama-2-70b.   
                                  When creating the prompts we tried to keep the phrasing as close to the original design as possible,
                                  while still being instructive enough to get answers that actually respond to our question and can be used for further analysis.    
                                  The number of maximum tokens was set to 2 for the openAI models and 10 for the LLama model, since the latter tended to start answers with blank spaces
                                  but still answer the question afterwards. On top of that, we saw that almost all answers that actually respond to the question at hand start with a 
                                  dollar sign. Other answers were often explanations of why a certain price was asked, or explanations as to why the question can not be answered
                                  with the given information. Therefore, we only regarded answers starting with a dollar sign as valid answers to analyze the distribution of.
                                  
                                  The aforementioned 12 different prompts resulted from the following input combinations:

                                  * Initial ticket price: Free, $5, $10 (3 options)
                                  * Current market price: $5, $10 (2 options)
                                  * Buyer type: Friend, Stranger (2 options)
                                         
                                  As in all experiments, the prompts were presented to each model over a range of different temperature values. However, the information about
                                  the participant being a student was omitted, since it is not relevant for the experiment. Formulating concise prompts is crucial and irrelevant
                                  information will not only lead to higher overall costs but might induce noise in the results. The instruction role was used to tell the model to
                                  "Answer by only giving a single price in dollars and cents without an explanation", which was also included in the prompt itself.

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
html.H2("Experiment 1: Recreation of hockey ticket study"),
html.Hr(),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select price paid", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-initial-cost-dropdown",
                        options=[
                            {"label": "Free", "value": 0},
                            {"label": "$5", "value": 5},
                            {"label": "$10", "value": 10},
                        ],
                        value=0,
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select current market price", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-current-cost-dropdown",
                        options=[
                            {"label": "$5", "value": 5},
                            {"label": "$10", "value": 10},
                        ],
                        value=5,
                        style={'width': '75%', 'margin': 'auto'},                        

                    ),
                    html.Label("Select buyer type", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id = "tu1-buyer-dropdown",
                        options=[
                            {"label": "Friend", "value": "friend"},
                            {"label": "Stranger", "value": "stranger"},
                        ],
                        value="friend",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu1-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu1-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None, # To only allow values as specified in marks
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu1-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt 
    html.Div(
            id='tu1-prompt',
            style={'textAlign': 'center', 'margin': '20px'},
    ),

    ########## Experiment 3
    html.Hr(),
    html.H2("Experiment 2: Hockey game tickets with alternative prices", className="page-heading"),
    html.Hr(),
    dbc.Accordion([
    dbc.AccordionItem(
        dcc.Markdown(["""
                      Analogous to the experiments concerning Prospect Theory and Mental Accounting we now purposely deviate from the original numbers used in the study.
                      That is because LLMs have been trained on, not only, but also text data that is freely available on the internet. This data might therefore
                      also include the original study along with its results. Therefore, we can expect that the  models' answers might be influenced by this.
                      Disregarding whether or not the results of the previous experiment support this assumption, we now introduce two new price levels for the tickets:
                      First, we scale all numbers mentioned in the prompt by the factor Pi, to see if odd numbers will produce different results, secondly we simply scale
                      all numbers by the factor 10. As a result, we now get 2 scenarios with 12 configurations each, resulting in 24 different prompts:

                      * Scenario 1: Prices multiplied by Pi
                        * Initial ticket price: Free, $5 * Pi, $5 * Pi * 2 (3 options)
                        * Current market price: $5 * Pi, $5 * Pi * 2 (2 options)
                        * Buyer type: Friend, Stranger (2 options) 
                      

                      * Scenario 2: Prices multiplied by 10
                        * Initial ticket price: Free, $50, $100 (3 options)
                        * Current market price: $50, $100 (2 options)
                        * Buyer type: Friend, Stranger (2 options)
                      
                      While the actual numbers mentioned in the prompts changed, the relation between the initial costs, the price marked on the ticket and the
                      current market price were kept constant.    
                      All prompts were presented to the Language Models over a range of different temperature values, querying GPT-3.5-Turbo 100 times and
                      GPT-4-1106-Preview and LLama-2-70b 50 times each. The information about the participant being a student was omitted again. In the instruction role we told
                      the model to "Answer by only giving a single price in dollars and cents without an explanation", which was also included in the prompt itself.
                      """]), title = "Description and implementation of the experiment"
    ),    
], start_collapsed=True,
),
    html.Br(),
    html.Hr(),
    html.H3("Scenario 1: Prices multiplied by Pi"),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select price paid", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-initial-cost-dropdown",
                        options=[
                            {"label": "Free", "value": 0},
                            {"label": "$5 * Pi", "value": 15.71},
                            {"label": "$5 * Pi * 2", "value": 31.42},
                        ],
                        value=0,
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select current market price", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-current-cost-dropdown",
                        options=[
                            {"label": "$5 * Pi", "value": 15.71},
                            {"label": "$5 * Pi * 2", "value": 31.42},
                        ],
                        value=15.71,
                        style={'width': '75%', 'margin': 'auto'},                        

                    ),
                    html.Label("Select buyer type", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id = "tu3-buyer-dropdown",
                        options=[
                            {"label": "Friend", "value": "friend"},
                            {"label": "Stranger", "value": "stranger"},
                        ],
                        value="friend",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu3-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu3-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None,
                                value=1,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu3-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt 
    html.Div(
            id='tu3-prompt',
            style={'textAlign': 'center', 'margin': '20px'},
    ),

    ##### Scenario 2
    html.H2("Scenario 2: Prices multiplied by 10"),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select price paid", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-initial-cost-dropdown2",
                        options=[
                            {"label": "Free", "value": 0},
                            {"label": "$50", "value": 50},
                            {"label": "$100", "value": 100},
                        ],
                        value=0,
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select current market price", style={'textAlign': 'center'}), 
                    dcc.Dropdown(
                        id="tu3-current-cost-dropdown2",
                        options=[
                            {"label": "$50", "value": 50},
                            {"label": "$100", "value": 100},
                        ],
                        value=50,
                        style={'width': '75%', 'margin': 'auto'},                        

                    ),
                    html.Label("Select buyer type", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id = "tu3-buyer-dropdown2",
                        options=[
                            {"label": "Friend", "value": "friend"},
                            {"label": "Stranger", "value": "stranger"},
                        ],
                        value="friend",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu3-language-model-dropdown2",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu3-temperature-slider2",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None, # To only allow values as specified in marks
                                value=1,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu3-plot2", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt 
    html.Div(
            id='tu3-prompt2',
            style={'textAlign': 'center', 'margin': '20px'},
    ),

    ########## Experiment 2
    html.Hr(),
    html.H2("Experiment 3: Beer consumption at the beach & income sensitivity"),
    html.Hr(),
     dbc.Accordion(
         [
        dbc.AccordionItem(
            dcc.Markdown(["""
                          The original experiment is also taken from Thaler's paper published in 1985 and aims to research the concept of transaction utility from a different
                          perspective. While the previous experiment demonstrated how the conception of a fair price is influenced by the seller's costs, and the individuals
                          had to name a price they would charge for a ticket, this experiment asks for a Willingness to Pay (WTP), making participants take the role of the buyer.
                          The original phrasing, presented to participants who claimed to be regular beer-drinkers, is as follows:    
                          
                          *"You are lying on the beach on a hot day. All you have to drink is ice water. For the last hour you have been thinking about how much you would enjoy
                           a nice cold bottle of your favorite brand of beer. A companion gets up to make a phone call and offers to bring back a beer from the only nearby place
                           where beer is sold: a fancy resort hotel/a small, run-down grocery store. He says that the beer might be expensive and so asks how much you are willing
                           to pay for the beer. He says that he will buy the beer if it costs as much or less than the price you state. But if it costs more than the price you state
                           he will not buy it. You trust your friend and there is no possibility of bargaining with the bartender/store owner. What price do you tell him?"*

                          The slashes indicate variations of the question. Thaler highlighted three important aspects of this experiment:    
                          1: The consumption act itself is exactly the same. The same kind of beer will be consumed at the beach.    
                          2: No strategic behavior is possible, since we can only name the WTP and the friend will make the purchase.    
                          3: The place of consumption is the exact same, thus no additional utility out of e.g. the atmosphere of the fancy resort hotel is consumed.    

                          Unfortunately, the paper does not report the original distribution of the answers but only states, that the **median WTP** for the **hotel was $2.65**
                          and **$1.50 for the grocery store**. This clearly reflects the concept of transaction utility, since paying $2.65 for beer at a grocery store would be considered
                          overpricing, while it seems an adequate price in a fancy resort hotel. Although the same beer will be consumed at the same place, significant differences
                          in the stated WTPs occured.

                          This experiment can be seen as a continuation of the hockey game ticket study, but with the roles reversed. As explained above, the human participants
                          exhibited, perhaps unknowingly, the concept of transaction utility in their thought process. Therefore, it is interesting to see, whether these patterns
                          will also be somehow reflected in the answers of Large Language Models, when they now have to state a Willingsness to Pay with no orientation price.
                          """]),
                    title = "Experiment Description"),
        dbc.AccordionItem(
                    dcc.Markdown(["""
                                  As mentioned above, the original study does not report the distribution of the answers, but only the median WTPs. Therefore, comparing the 
                                  models' answers to a ground truth is only possible to a limited extent. Furthermore, in this experiment, no orientation price is given in the
                                  prompts, that might serve as an anchor to base the WTP on. Therefore, apart from only alternating the place of purchase, we also reserched
                                  the aspect of *income sensitivity*. It can be expected, that the median, as well as the mean WTP for beer at both places of purchase
                                  will be higher for individuals with a higher income. The exact levels of income were oriented on the numbers used by Brand et al. (2023).
                                  In total, we used 8 different prompts, that we resulted from:

                                  * Place of purchase: Fancy resort hotel, Run-down grocery store (2 options)
                                  * Annual income: No information given, $50k, $70k, $120k (4 options)

                                  All prompts were again presented to every Language model over a range of different temperature values. The number of repeated requests
                                  per prompt and temperature value was 100 for GPT-3.5-Turbo and 50 for GPT-4-1106-Preview and LLama-2-70b. The prompts were designed to be 
                                  as close to the original phrasing as possible, with the addition of the income information. As instruction we told the model to 
                                  "Answer by only giving a single price in dollars and cents without an explanation", which was also included in the prompt itself.    
                                  The configuration, which is comparable to the original results, is the one where no information about the income is given. 
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
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Label("Select place of purchase", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-place-dropdown",
                        options=[
                            {"label": "Fancy resort hotel", "value": "hotel"},
                            {"label": "Run-down grocery store", "value": "grocery"},
                        ],
                        value="hotel",
                        style={'width': '75%', 'margin': 'auto'},
                    ),
                    html.Label("Select annual income", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-income-dropdown",
                        options=[
                            {"label": "No information given", "value": "0"},
                            {"label": "$50k", "value": "$50k"},
                            {"label": "$70k", "value": "$70k"},
                            {"label": "$120k", "value": "$120k"},
                        ],
                        value="0",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),

                    html.Label("Select language model", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id="tu2-language-model-dropdown",
                        options=[
                            {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                            {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                            {"label": "LLama-2-70b", "value": "llama-2-70b"},
                        ],
                        value="gpt-3.5-turbo",
                        style={'width': '75%', 'margin': 'auto'},                        
                    ),
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="tu2-temperature-slider",
                                min=0.01,
                                max=2,
                                marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                step = None,
                                value=0.5,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),
                ],
                style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id="tu2-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'},
    ),
    # Display of prompt
    html.Div(
            id='tu2-prompt',
            style={'textAlign': 'center', 'margin': '20px'},
    ),
]



### Callback ###

### Experiment 1
@dash.callback(
    [Output("tu1-plot", "figure"),
    Output('tu1-prompt', 'children')],
    [
        Input("tu1-initial-cost-dropdown", "value"),
        Input("tu1-current-cost-dropdown", "value"),
        Input("tu1-buyer-dropdown", "value"),
        Input("tu1-language-model-dropdown", "value"),
        Input("tu1-temperature-slider", "value"),
    ],
)


def update_tu1(initial_costs, orientation_price, selected_buyer, selected_model, selected_temperature):
    # Get prompt
    df = TU_results[(TU_results["Initial_cost"] == initial_costs) & (TU_results["Orientation_price"] == orientation_price) & (TU_results["Buyer"] == selected_buyer) &
                    (TU_results["Model"] == selected_model) & (TU_results["Temperature"] == selected_temperature)]            
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU_plot_results(df), prompt


### Experiment 3: Scenario 1
@dash.callback(
    [Output("tu3-plot", "figure"),
    Output('tu3-prompt', 'children')],
    [   Input("tu3-initial-cost-dropdown", "value"),
        Input("tu3-current-cost-dropdown", "value"),
        Input("tu3-buyer-dropdown", "value"),
        Input("tu3-language-model-dropdown", "value"),
        Input("tu3-temperature-slider", "value"),
    ],
)


def update_tu3(initial_costs, orientation_price, selected_buyer, selected_model, selected_temperature):
    # Subset df (manually select actual price to be 5 * Pi)
    df = TU3_results[(TU3_results["Actual_price"] == 15.71) & (TU3_results["Initial_cost"] == initial_costs) & (TU3_results["Orientation_price"] == orientation_price)
                  & (TU3_results["Buyer"] == selected_buyer) & (TU3_results["Model"] == selected_model) & (TU3_results["Temperature"] == selected_temperature)]        
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU3_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU3_plot_results(df), prompt


### Experiment 3: Scenario 2
@dash.callback(
    [Output("tu3-plot2", "figure"),
    Output('tu3-prompt2', 'children')],
    [   Input("tu3-initial-cost-dropdown2", "value"),
        Input("tu3-current-cost-dropdown2", "value"),
        Input("tu3-buyer-dropdown2", "value"),
        Input("tu3-language-model-dropdown2", "value"),
        Input("tu3-temperature-slider2", "value"),
    ],
)

def update_tu3_2(initial_costs, orientation_price, selected_buyer, selected_model, selected_temperature):
    # Subset df (manually select actual price to be 50)
    df = TU3_results[(TU3_results["Actual_price"] == 50) & (TU3_results["Initial_cost"] == initial_costs) & (TU3_results["Orientation_price"] == orientation_price)
                  & (TU3_results["Buyer"] == selected_buyer) & (TU3_results["Model"] == selected_model) & (TU3_results["Temperature"] == selected_temperature)]        
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU3_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU3_plot_results(df), prompt




### Experiument 2
@dash.callback(
    [Output("tu2-plot", "figure"),
     Output('tu2-prompt', 'children')],
    [
        Input("tu2-place-dropdown", "value"),
        Input("tu2-income-dropdown", "value"),
        Input("tu2-language-model-dropdown", "value"),
        Input("tu2-temperature-slider", "value"),
    ],
)

def update_tu2(selected_place, selected_income, selected_model, selected_temperature):
    df = TU2_results[(TU2_results["Place"] == selected_place) & (TU2_results["Income"] == selected_income) & 
                     (TU2_results["Model"] == selected_model) & (TU2_results["Temperature"] == selected_temperature)]
    experiment_id = df["Experiment_id"].iloc[0]
    prompt = TU2_experiment_prompts_dict[experiment_id]
    prompt = html.P(f"The prompt used in this experiment is: {prompt}")
    return TU2_plot_results(df), prompt