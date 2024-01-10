# Import required libraries 
import pandas as pd
import random
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
import plotly.graph_objects as go
from openai import OpenAI
import openai
import replicate
import os


dash.register_page(__name__, path='/live-experiment', name='Live Experiment', location='sidebar')


# Get openAI API key (previously saved as environmental variable)
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set client
client = OpenAI()


instructions = "Which alternative would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."
def create_prompt2(prompt_design, answers):
    prompt = f"""{prompt_design} Option A: {answers[0]} Option B: {answers[1]} Option C: {answers[2]}. {instructions}"""
    return prompt

def create_prompt(prompt_design, answers):
    if len(answers) == 2:
        prompt = f"""{prompt_design} Option A: {answers[0]} Option B: {answers[1]}. {instructions}"""
    elif len(answers) == 3:
        prompt = f"""{prompt_design} Option A: {answers[0]} Option B: {answers[1]} Option C: {answers[2]}. {instructions}"""
    elif len(answers) == 4:
        prompt = f"""{prompt_design} Option A: {answers[0]} Option B: {answers[1]} Option C: {answers[2]} Option D: {answers[3]}. {instructions}"""
    elif len(answers) == 5:
        prompt = f"""{prompt_design} Option A: {answers[0]} Option B: {answers[1]} Option C: {answers[2]} Option D: {answers[3]} Option E: {answers[4]}. {instructions}"""
    elif len(answers) == 6:
        prompt = f"""{prompt_design} Option A: {answers[0]} Option B: {answers[1]} Option C: {answers[2]} Option D: {answers[3]} Option E: {answers[4]} Option F: {answers[5]}. {instructions}"""
    return prompt

def answer_randomization(options: list):
    # Generation of random letters 
    letters = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', len(options))

    # Create a dictionary to map random letters to randomly ordered options
    options_random = random.sample(options, len(options))
    letter_mapping = {letters[i]: options_random[i] for i in range(len(options))}

    # Create the output string
    answer_options = ', '.join([f'{letters[i]}: {options_random[i]}' for i in range(len(options))])
    
    return answer_options


# Function to run individual experiment with OpenAI models
def run_individual_experiment_openai(prompt, model, iterations, temperature):
    model_answers = []
    for _ in range(iterations): 
        response = client.chat.completions.create(
            model = model, 
            max_tokens = 1,
            temperature = temperature, # range is 0 to 2
            messages = [
            {"role": "system", "content": "Only answer with the letter of the alternative you would choose without any reasoning."},        
            {"role": "user", "content": prompt},
                   ])

        # Store the answer in the list
        answer = response.choices[0].message.content
        model_answers.append(answer.strip())

    # Counting results
    A = model_answers.count("A")
    B = model_answers.count("B")
    C = model_answers.count("C")

    # Count of "correct" answers, sums over indicator function thack checks if answer is either A, B or C
    len_correct = sum(1 for ans in model_answers if ans in ["A", "B", "C"])

    # Collecting results in a list
    results = pd.DataFrame([temperature, A, B, C, len_correct, model])
    results = results.set_index(pd.Index(["Temp", "A", "B", "C", "Obs.", "Model"]))

    # Getting percentage each answer
    p_a = (A / (len_correct + 0.000000001)) * 100
    p_b = (B / (len_correct + 0.000000001)) * 100 
    p_c = (C / (len_correct + 0.000000001)) * 100

    # Collect probabilities in a dataframe
    probs = pd.DataFrame([temperature, p_a, p_b, p_c, len_correct, model])
    probs = probs.set_index(pd.Index(["Temp", "p(A)", "p(B)", "p(C)", "Obs.", "Model"]))
    
    # Give out results
    return results, probs

# Function to run individual experiment with Meta's llama model
def run_individual_experiment_llama(prompt, model, iterations, temperature):
    model_answers = []
    for _ in range(iterations):
        response = replicate.run(
            model,
            input = {
                "system_prompt": "Only answer with the letter of the alternative you would choose without any reasoning.",
                "temperature": temperature,
                "max_new_tokens": 2, 
                "prompt": prompt
            }
        )
        # Grab answer and append to list
        answer = "" # Set to empty string, otherwise it would append the previous answer to the new one
        for item in response:
            answer = answer + item
        model_answers.append(answer.strip())

    # Counting results
    A = model_answers.count("A") 
    B = model_answers.count("B") 
    C = model_answers.count("C") 

    # Count of "correct" answers, sums over indicator function thack checks if answer is either A, B or C
    len_correct = sum(1 for ans in model_answers if ans in ["A", "B", "C"])

    # Collecting results in a list
    results = pd.DataFrame([temperature, A, B, C, len_correct, model])
    results = results.set_index(pd.Index(["Temp", "A", "B", "C", "Obs.", "Model"]))

    # Getting percentage each answer
    p_a = (A / (len_correct + 0.000000001)) * 100
    p_b = (B / (len_correct + 0.000000001)) * 100
    p_c = (C / (len_correct + 0.000000001)) * 100

    # Collect probabilities in a dataframe
    probs = pd.DataFrame([temperature, p_a, p_b, p_c, len_correct, model])
    probs = probs.set_index(pd.Index(["Temp", "p(A)", "p(B)", "p(C)", "Obs.", "Model"]))
    
    # Give out results
    return results, probs



# Function to plot results of individual experiment
def plot_results_individual(df):
    
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."]
    
    # Get temperature values
    temperature = df.loc["Temp"]

    # Get model
    model = df.loc["Model"][0]

    # Rename for better readability
    if model == "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3":
        model = "llama-2-70b-chat"


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
        text= f"Results of experiment with {model}",
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



# Page for individual experiment
layout = [
    html.H1("Conduct your own individual experiment", className="page-heading"), 
    html.Hr(),
    html.P("""Think of multiple-choice-style experiment to conduct. Choose a prompt, a model, and answer options to run the experiment yourself."""),
    html.Br(),
    html.Div(
        children=[
            html.Div(
                children=[
                            html.Label("Select a scenario", style={'textAlign': 'center'}),
                            dcc.Textarea(
                            id='individual-prompt',
                            value="You are a random pedestrian being chosen for a survey. The question is: Would you rather:",
                            style={'width': '100%', 'height': 300},
                             ),
                            # Answer option A 
                            html.Label("Answer option A", style={'textAlign': 'center'}),
                            dcc.Textarea(
                            id='individual-answer-a',
                            value='Win 50$',
                            style={'width': '100%', 'height': 300},
                             ),
                            # Answer option B
                            html.Label("Answer option B", style={'textAlign': 'center'}),
                            dcc.Textarea(
                            id='individual-answer-b',
                            value='Lose 50$',
                            style={'width': '100%', 'height': 300},
                             ),   
                            # Answer option C   
                            html.Label("Answer option C", style={'textAlign': 'center'}),
                            dcc.Textarea(
                            id='individual-answer-c',
                            value='Win 100$',
                            style={'width': '100%', 'height': 300},
                             ),                                            
                            html.Label("Select a language model", style={'textAlign': 'center'}),
                            dcc.Dropdown(
                            id = "individual-model-dropdown",
                            options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                              {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                              {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                            style={'width': '75%', 'margin': 'auto'},
                    ),

                            html.Label("Select number of requests", style={'textAlign': 'center'}),                
                            dbc.Input(
                            id = "individual-iterations", 
                            type = "number",
                            value = 0, 
                            min = 0, 
                            max = 100, 
                            step = 1,
                            style={'width': '57%', 'margin': 'auto'}, # apparently default width for input is different from dropdown
                    ),      
                    html.Div(
                        [
                            html.Label("Select Temperature value"),             
                            dcc.Slider(
                                id="individual-temperature",
                                min=0.01,
                                max=2,
                                step=0.01,
                                marks={0.01: '0.01', 2: '2'},
                                value=0.8,
                                tooltip={'placement': 'top'},
                            ),
                        ],
                    ),

                    # Add a button to trigger calback
                    html.Button('Run the experiment', id = 'individual-update-button', n_clicks = None),
                         ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
        dcc.Graph(id="individual-output", style={'width': '70%', 'height': '60vh'}),
        ],
    style={'display': 'flex', 'flexDirection': 'row'}
    ),
    # Additional text section
    html.Div(
            id='individual-experiment-design',
            style={'textAlign': 'center', 'margin': '20px'},
    ),
    html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
]


# Callback for individual live experiment
@dash.callback(
    [Output("individual-output", "figure"),
     Output('individual-experiment-design', 'children')],
    [Input("individual-update-button", "n_clicks")],
    [State("individual-prompt", "value"),
     State("individual-answer-a", "value"),
     State("individual-answer-b", "value"),
     State("individual-answer-c", "value"),
     State("individual-model-dropdown", "value"),
     State("individual-iterations", "value"),
     State("individual-temperature", "value")]
     )

def update_individual_experiment(n_clicks, prompt, answer_a, answer_b, answer_c, selected_model, selected_iterations, selected_temperature):
    # Check if button was clicked
    if n_clicks is not None:
        answers = [answer_a, answer_b, answer_c]
        prompt = create_prompt2(prompt, answers)
        print(f"Prompt: {prompt}")
        print(f" Selected model: {selected_model}")
        print(f"Selected iterations: {selected_iterations}")
        print(f"Selected temperature: {selected_temperature}")
        if selected_model == "llama-2-70b":
            selected_model = "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"
            results, probs = run_individual_experiment_llama(prompt, selected_model, selected_iterations, selected_temperature)
        else:
            results, probs = run_individual_experiment_openai(prompt, selected_model, selected_iterations, selected_temperature)
        n_clicks = None
        prompt = html.P(f"The prompt used in this experiment is: {prompt}")
        return plot_results_individual(probs), prompt             
        # Run Experiment for selected parameters