# Import required libraries 
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go
from PIL import Image


dash.register_page(__name__, path='/prospect-theory', name='Prospect Theory', location='experiments')


# Load in results and graphs of Prospect Theory experiments
PT_probs = pd.read_csv("Output/PT_probs.csv", index_col = 0)
PT_og_scenario1 = Image.open("Output/PT_og_scenario1.png")
PT_og_scenario2 = Image.open("Output/PT_og_scenario2.png")
PT_og_scenario3 = Image.open("Output/PT_og_scenario3.png")
PT_og_scenario4 = Image.open("Output/PT_og_scenario4.png")

# Second Prospect Theory experiment
PT2_probs = pd.read_csv("Output/PT2_probs.csv", index_col = 0)


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


### Prospect Theory ###
PT_prompt_1 = """Mr. A was given tickets involving the World Series. He won 50$ in one lottery and $25 in the other. 
          Mr. B was given a ticket to a single, larger World Series lottery. He won $75. Based solely on this information, Who is happier? 
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
         Mr. B bought his first New York State lottery ticket and won $20. Based solely on this information, who is happier? 
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_4 = """Mr. A's car was damaged in a parking lot. He had to spend $200 to repair the damage. The same day the car was damaged, he won $25 in the office football pool.
         Mr. B's car was damaged in a parking lot. He had to spend $175 to repair the damage. Based solely on this information, who is more upset?
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_5 = """You are a market researcher and focus on Prospect Theory and Mental Accounting. In a survey you are presented the following situation: 
          Mr. A was given tickets involving the World Series. He won 50$ in one lottery and 25$ in the other. 
          Mr. B was given a ticket to a single, larger World Series lottery. He won 75$. Based solely on this information, who is happier?
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
         Mr. B bought his first New York State lottery ticket and won $20? Based solely on this information, who is happier?
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""
PT_prompt_8 = """You are a market researcher and focus on Prospect Theory and Mental Accounting. In a survey you are presented the following situation:
         Mr. A's car was damaged in a parking lot. He had to spend $200 to repair the damage. The same day the car was damaged, he won $25 in the office football pool.
         Mr. B's car was damaged in a parking lot. He had to spend $175 to repair the damage. Based solely on this information, who is more upset?
         A: Mister A
         B: Mister B
         C: No difference.
         Which option would you choose? Please answer by only giving the letter of the alternative you would choose without any reasoning."""


# Original results for Prospect Theory Experiments
PT_p_scenario1 = [f"p(A): {round((56/(56+16+15)*100), 2)}%", f"p(B): {round((16/(56+16+15)*100), 2)}%", f"p(C): {round((15/(56+16+15)*100), 2)}%"]
PT_p_scenario2 = [f"p(A): {round((66/(66+14+7)*100), 2)}%", f"p(B): {round((14/(66+14+7)*100), 2)}%", f"p(C): {round((7/(66+14+7)*100), 2)}%"]
PT_p_scenario3 = [f"p(A): {round((22/(22+61+4)*100), 2)}%", f"p(B): {round((61/(22+61+4)*100), 2)}%", f"p(C): {round((4/(22+61+4)*100), 2)}%"]
PT_p_scenario4 = [f"p(A): {round((19/(19+63+5)*100), 2)}%", f"p(B): {round((63/(19+63+5)*100), 2)}%", f"p(C): {round((5/(19+63+5)*100), 2)}%"]

# Dictionary that returns the literal prompt for a given experiment id (used in function call). key: experiment_id, value: prompt
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

# It returns the variable name of the prompt that was used in the experiment. key: experiment_id, value: prompt_name
PT_prompt_ids_dict = {
    "PT_1_1": "PT_prompt_1",
    "PT_1_2": "PT_prompt_2",
    "PT_1_3": "PT_prompt_3",
    "PT_1_4": "PT_prompt_4",
    "PT_1_5": "PT_prompt_5",
    "PT_1_6": "PT_prompt_6",
    "PT_1_7": "PT_prompt_7",
    "PT_1_8": "PT_prompt_8",
    "PT_2_1": "PT_prompt_1",
    "PT_2_2": "PT_prompt_2",
    "PT_2_3": "PT_prompt_3",
    "PT_2_4": "PT_prompt_4",
    "PT_2_5": "PT_prompt_5",
    "PT_2_6": "PT_prompt_6",
    "PT_2_7": "PT_prompt_7",
    "PT_2_8": "PT_prompt_8",
    "PT_3_1": "PT_prompt_1",
    "PT_3_2": "PT_prompt_2",
    "PT_3_3": "PT_prompt_3",
    "PT_3_4": "PT_prompt_4",
    "PT_3_5": "PT_prompt_5",
    "PT_3_6": "PT_prompt_6",
    "PT_3_7": "PT_prompt_7",
    "PT_3_8": "PT_prompt_8",
}

# Dictionary to look up which model to use for a given experiment id (used in function call). key: experiment id, value: model name
PT_model_dict = {
    "PT_1_1": "gpt-3.5-turbo",
    "PT_1_2": "gpt-3.5-turbo",
    "PT_1_3": "gpt-3.5-turbo",
    "PT_1_4": "gpt-3.5-turbo",
    "PT_1_5": "gpt-3.5-turbo",
    "PT_1_6": "gpt-3.5-turbo",
    "PT_1_7": "gpt-3.5-turbo",
    "PT_1_8": "gpt-3.5-turbo",
    "PT_2_1": "gpt-4-1106-preview",
    "PT_2_2": "gpt-4-1106-preview",
    "PT_2_3": "gpt-4-1106-preview",
    "PT_2_4": "gpt-4-1106-preview",
    "PT_2_5": "gpt-4-1106-preview",
    "PT_2_6": "gpt-4-1106-preview",
    "PT_2_7": "gpt-4-1106-preview",
    "PT_2_8": "gpt-4-1106-preview",
    "PT_3_1": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "PT_3_2": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "PT_3_3": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "PT_3_4": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "PT_3_5": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "PT_3_6": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "PT_3_7": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    "PT_3_8": 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
    }

# Dictionary to look up the original results of the experiments. key: experiment id, value: original result
PT_results_dict = {
    "PT_1_1": PT_p_scenario1,
    "PT_1_2": PT_p_scenario2,
    "PT_1_3": PT_p_scenario3,
    "PT_1_4": PT_p_scenario4,
    "PT_1_5": PT_p_scenario1,
    "PT_1_6": PT_p_scenario2,
    "PT_1_7": PT_p_scenario3,
    "PT_1_8": PT_p_scenario4,
    "PT_2_1": PT_p_scenario1,
    "PT_2_2": PT_p_scenario2,
    "PT_2_3": PT_p_scenario3,
    "PT_2_4": PT_p_scenario4,
    "PT_2_5": PT_p_scenario1,
    "PT_2_6": PT_p_scenario2,
    "PT_2_7": PT_p_scenario3,
    "PT_2_8": PT_p_scenario4,
    "PT_3_1": PT_p_scenario1,
    "PT_3_2": PT_p_scenario2,
    "PT_3_3": PT_p_scenario3,
    "PT_3_4": PT_p_scenario4,
    "PT_3_5": PT_p_scenario1,
    "PT_3_6": PT_p_scenario2,
    "PT_3_7": PT_p_scenario3,
    "PT_3_8": PT_p_scenario4,
}

# Dictionary to look up the scenario number of a given experiment ID. key: experiment id, value: scenario number
PT_scenario_dict = {
    "PT_1_1": 1,
    "PT_1_2": 2,
    "PT_1_3": 3,
    "PT_1_4": 4,
    "PT_1_5": 1,
    "PT_1_6": 2,
    "PT_1_7": 3,
    "PT_1_8": 4,
    "PT_2_1": 1,
    "PT_2_2": 2,
    "PT_2_3": 3,
    "PT_2_4": 4,
    "PT_2_5": 1,
    "PT_2_6": 2,
    "PT_2_7": 3,
    "PT_2_8": 4,
    "PT_3_1": 1,
    "PT_3_2": 2,
    "PT_3_3": 3,
    "PT_3_4": 4,
    "PT_3_5": 1,
    "PT_3_6": 2,
    "PT_3_7": 3,
    "PT_3_8": 4,
}   

# Dictionary to look up, whether an experiment used a primed or unprimed prompt. key: experiment id, value: 1 if primed, 0 if unprimed
PT_priming_dict = {
    "PT_1_1": 0,
    "PT_1_2": 0,
    "PT_1_3": 0,
    "PT_1_4": 0,
    "PT_1_5": 1,
    "PT_1_6": 1,
    "PT_1_7": 1,
    "PT_1_8": 1,
    "PT_2_1": 0,
    "PT_2_2": 0,
    "PT_2_3": 0,
    "PT_2_4": 0,
    "PT_2_5": 1,
    "PT_2_6": 1,
    "PT_2_7": 1,
    "PT_2_8": 1,
    "PT_3_1": 0,
    "PT_3_2": 0,
    "PT_3_3": 0,
    "PT_3_4": 0,
    "PT_3_5": 1,
    "PT_3_6": 1,
    "PT_3_7": 1,
    "PT_3_8": 1,
}

# Dictionary to look up original results of the Prospect Theory experiments. Key: experiment id, value: original results
PT_results_dict = {
    "PT_1_1": PT_p_scenario1,
    "PT_1_2": PT_p_scenario2,
    "PT_1_3": PT_p_scenario3,
    "PT_1_4": PT_p_scenario4,
    "PT_1_5": PT_p_scenario1,
    "PT_1_6": PT_p_scenario2,
    "PT_1_7": PT_p_scenario3,
    "PT_1_8": PT_p_scenario4,
    "PT_2_1": PT_p_scenario1,
    "PT_2_2": PT_p_scenario2,
    "PT_2_3": PT_p_scenario3,
    "PT_2_4": PT_p_scenario4,
    "PT_2_5": PT_p_scenario1,
    "PT_2_6": PT_p_scenario2,
    "PT_2_7": PT_p_scenario3,
    "PT_2_8": PT_p_scenario4,
    "PT_3_1": PT_p_scenario1,
    "PT_3_2": PT_p_scenario2,
    "PT_3_3": PT_p_scenario3,
    "PT_3_4": PT_p_scenario4,
    "PT_3_5": PT_p_scenario1,
    "PT_3_6": PT_p_scenario2,
    "PT_3_7": PT_p_scenario3,
    "PT_3_8": PT_p_scenario4,
    }


# Dictionary to look up the original results for a given experiment id. key: experiment id, value: original answer probabilities
PT2_results_dict = {
    "PT2_1_1_1": PT_p_scenario1,
    "PT2_1_1_2": PT_p_scenario1,
    "PT2_1_1_3": PT_p_scenario1,
    "PT2_1_1_4": PT_p_scenario1,
    "PT2_1_1_5": PT_p_scenario1,
    "PT2_1_1_6": PT_p_scenario1,
    "PT2_2_1_1": PT_p_scenario2,
    "PT2_2_1_2": PT_p_scenario2,
    "PT2_2_1_3": PT_p_scenario2,
    "PT2_2_1_4": PT_p_scenario2,
    "PT2_2_1_5": PT_p_scenario2,
    "PT2_2_1_6": PT_p_scenario2,
    "PT2_3_1_1": PT_p_scenario3,
    "PT2_3_1_2": PT_p_scenario3,
    "PT2_3_1_3": PT_p_scenario3,
    "PT2_3_1_4": PT_p_scenario3,
    "PT2_3_1_5": PT_p_scenario3,
    "PT2_3_1_6": PT_p_scenario3,
    "PT2_4_1_1": PT_p_scenario4,
    "PT2_4_1_2": PT_p_scenario4,
    "PT2_4_1_3": PT_p_scenario4,
    "PT2_4_1_4": PT_p_scenario4,
    "PT2_4_1_5": PT_p_scenario4,
    "PT2_4_1_6": PT_p_scenario4,
    "PT2_1_2_1": PT_p_scenario1,
    "PT2_1_2_2": PT_p_scenario1,
    "PT2_1_2_3": PT_p_scenario1,
    "PT2_1_2_4": PT_p_scenario1,
    "PT2_1_2_5": PT_p_scenario1,
    "PT2_1_2_6": PT_p_scenario1,
    "PT2_2_2_1": PT_p_scenario2,
    "PT2_2_2_2": PT_p_scenario2,
    "PT2_2_2_3": PT_p_scenario2,
    "PT2_2_2_4": PT_p_scenario2,
    "PT2_2_2_5": PT_p_scenario2,
    "PT2_2_2_6": PT_p_scenario2,
    "PT2_3_2_1": PT_p_scenario3,
    "PT2_3_2_2": PT_p_scenario3,
    "PT2_3_2_3": PT_p_scenario3,
    "PT2_3_2_4": PT_p_scenario3,
    "PT2_3_2_5": PT_p_scenario3,
    "PT2_3_2_6": PT_p_scenario3,
    "PT2_4_2_1": PT_p_scenario4,
    "PT2_4_2_2": PT_p_scenario4,
    "PT2_4_2_3": PT_p_scenario4,
    "PT2_4_2_4": PT_p_scenario4,
    "PT2_4_2_5": PT_p_scenario4,
    "PT2_4_2_6": PT_p_scenario4,
    "PT2_1_3_1": PT_p_scenario1,
    "PT2_1_3_2": PT_p_scenario1,
    "PT2_1_3_3": PT_p_scenario1,
    "PT2_1_3_4": PT_p_scenario1,   
    "PT2_1_3_5": PT_p_scenario1,
    "PT2_1_3_6": PT_p_scenario1,
    "PT2_2_3_1": PT_p_scenario2,
    "PT2_2_3_2": PT_p_scenario2,
    "PT2_2_3_3": PT_p_scenario2,
    "PT2_2_3_4": PT_p_scenario2,
    "PT2_2_3_5": PT_p_scenario2,
    "PT2_2_3_6": PT_p_scenario2,
    "PT2_3_3_1": PT_p_scenario3,
    "PT2_3_3_2": PT_p_scenario3,
    "PT2_3_3_3": PT_p_scenario3,
    "PT2_3_3_4": PT_p_scenario3,
    "PT2_3_3_5": PT_p_scenario3,
    "PT2_3_3_6": PT_p_scenario3,
    "PT2_4_3_1": PT_p_scenario4,
    "PT2_4_3_2": PT_p_scenario4,
    "PT2_4_3_3": PT_p_scenario4,
    "PT2_4_3_4": PT_p_scenario4,
    "PT2_4_3_5": PT_p_scenario4,
    "PT2_4_3_6": PT_p_scenario4,
}

# Dictionary to look up which model to use for a given experiment id. key: experiment id, value: model name
PT2_model_dict = {
    "PT2_1_1_1": "gpt-3.5-turbo",  
    "PT2_1_1_2": "gpt-3.5-turbo",
    "PT2_1_1_3": "gpt-3.5-turbo",
    "PT2_1_1_4": "gpt-3.5-turbo",
    "PT2_1_1_5": "gpt-3.5-turbo",
    "PT2_1_1_6": "gpt-3.5-turbo",
    "PT2_2_1_1": "gpt-3.5-turbo",
    "PT2_2_1_2": "gpt-3.5-turbo",
    "PT2_2_1_3": "gpt-3.5-turbo",
    "PT2_2_1_4": "gpt-3.5-turbo",
    "PT2_2_1_5": "gpt-3.5-turbo",
    "PT2_2_1_6": "gpt-3.5-turbo",
    "PT2_3_1_1": "gpt-3.5-turbo",
    "PT2_3_1_2": "gpt-3.5-turbo",
    "PT2_3_1_3": "gpt-3.5-turbo",
    "PT2_3_1_4": "gpt-3.5-turbo",
    "PT2_3_1_5": "gpt-3.5-turbo",
    "PT2_3_1_6": "gpt-3.5-turbo",
    "PT2_4_1_1": "gpt-3.5-turbo",
    "PT2_4_1_2": "gpt-3.5-turbo",
    "PT2_4_1_3": "gpt-3.5-turbo",
    "PT2_4_1_4": "gpt-3.5-turbo",
    "PT2_4_1_5": "gpt-3.5-turbo",
    "PT2_4_1_6": "gpt-3.5-turbo",
    "PT2_1_2_1": "gpt-4-1106-preview",
    "PT2_1_2_2": "gpt-4-1106-preview",
    "PT2_1_2_3": "gpt-4-1106-preview",
    "PT2_1_2_4": "gpt-4-1106-preview",
    "PT2_1_2_5": "gpt-4-1106-preview",
    "PT2_1_2_6": "gpt-4-1106-preview",
    "PT2_2_2_1": "gpt-4-1106-preview",
    "PT2_2_2_2": "gpt-4-1106-preview",
    "PT2_2_2_3": "gpt-4-1106-preview",
    "PT2_2_2_4": "gpt-4-1106-preview",
    "PT2_2_2_5": "gpt-4-1106-preview",
    "PT2_2_2_6": "gpt-4-1106-preview",
    "PT2_3_2_1": "gpt-4-1106-preview",
    "PT2_3_2_2": "gpt-4-1106-preview",
    "PT2_3_2_3": "gpt-4-1106-preview",
    "PT2_3_2_4": "gpt-4-1106-preview",
    "PT2_3_2_5": "gpt-4-1106-preview",
    "PT2_3_2_6": "gpt-4-1106-preview",
    "PT2_4_2_1": "gpt-4-1106-preview",
    "PT2_4_2_2": "gpt-4-1106-preview",
    "PT2_4_2_3": "gpt-4-1106-preview",
    "PT2_4_2_4": "gpt-4-1106-preview",
    "PT2_4_2_5": "gpt-4-1106-preview",
    "PT2_4_2_6": "gpt-4-1106-preview",
    "PT2_1_3_1": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_1_3_2": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_1_3_3": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_1_3_4": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_1_3_5": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_1_3_6": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_2_3_1": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_2_3_2": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_2_3_3": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_2_3_4": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_2_3_5": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_2_3_6": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_3_3_1": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_3_3_2": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_3_3_3": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_3_3_4": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_3_3_5": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_3_3_6": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_4_3_1": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_4_3_2": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_4_3_3": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_4_3_4": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_4_3_5": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    "PT2_4_3_6": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"
    }

# Dictionary to look up scenario number for a given experiment id. key: experiment id, value: scenario number
PT2_scenario_dict = {
    "PT2_1_1_1": 1,
    "PT2_1_1_2": 1,
    "PT2_1_1_3": 1,
    "PT2_1_1_4": 1,
    "PT2_1_1_5": 1,
    "PT2_1_1_6": 1,
    "PT2_2_1_1": 2,
    "PT2_2_1_2": 2,
    "PT2_2_1_3": 2,
    "PT2_2_1_4": 2,
    "PT2_2_1_5": 2,
    "PT2_2_1_6": 2,
    "PT2_3_1_1": 3,
    "PT2_3_1_2": 3,
    "PT2_3_1_3": 3,
    "PT2_3_1_4": 3,
    "PT2_3_1_5": 3,
    "PT2_3_1_6": 3,
    "PT2_4_1_1": 4,
    "PT2_4_1_2": 4,
    "PT2_4_1_3": 4,
    "PT2_4_1_4": 4,
    "PT2_4_1_5": 4,
    "PT2_4_1_6": 4,
    "PT2_1_2_1": 1,
    "PT2_1_2_2": 1,
    "PT2_1_2_3": 1,
    "PT2_1_2_4": 1,
    "PT2_1_2_5": 1,
    "PT2_1_2_6": 1,
    "PT2_2_2_1": 2,
    "PT2_2_2_2": 2, 
    "PT2_2_2_3": 2,
    "PT2_2_2_4": 2,
    "PT2_2_2_5": 2,
    "PT2_2_2_6": 2,
    "PT2_3_2_1": 3,
    "PT2_3_2_2": 3,
    "PT2_3_2_3": 3,
    "PT2_3_2_4": 3,
    "PT2_3_2_5": 3,
    "PT2_3_2_6": 3,
    "PT2_4_2_1": 4,
    "PT2_4_2_2": 4,
    "PT2_4_2_3": 4,
    "PT2_4_2_4": 4,
    "PT2_4_2_5": 4,
    "PT2_4_2_6": 4,
    "PT2_1_3_1": 1,
    "PT2_1_3_2": 1,
    "PT2_1_3_3": 1,
    "PT2_1_3_4": 1,
    "PT2_1_3_5": 1,
    "PT2_1_3_6": 1,
    "PT2_2_3_1": 2,
    "PT2_2_3_2": 2,
    "PT2_2_3_3": 2,
    "PT2_2_3_4": 2,
    "PT2_2_3_5": 2,
    "PT2_2_3_6": 2,
    "PT2_3_3_1": 3,
    "PT2_3_3_2": 3,
    "PT2_3_3_3": 3,
    "PT2_3_3_4": 3,
    "PT2_3_3_5": 3,
    "PT2_3_3_6": 3,
    "PT2_4_3_1": 4,
    "PT2_4_3_2": 4,
    "PT2_4_3_3": 4,
    "PT2_4_3_4": 4,
    "PT2_4_3_5": 4,
    "PT2_4_3_6": 4,
}

# Dictionary to look up scenario configuration based on experiment id. key: experiment id, value: scenario configuration
PT2_configuration_dict = {
    "PT2_1_1_1": 1,
    "PT2_1_1_2": 2,
    "PT2_1_1_3": 3,
    "PT2_1_1_4": 4,
    "PT2_1_1_5": 5,
    "PT2_1_1_6": 6,
    "PT2_2_1_1": 1,
    "PT2_2_1_2": 2,
    "PT2_2_1_3": 3,
    "PT2_2_1_4": 4,
    "PT2_2_1_5": 5,
    "PT2_2_1_6": 6,
    "PT2_3_1_1": 1,
    "PT2_3_1_2": 2,
    "PT2_3_1_3": 3,
    "PT2_3_1_4": 4,
    "PT2_3_1_5": 5,
    "PT2_3_1_6": 6,
    "PT2_4_1_1": 1,
    "PT2_4_1_2": 2,
    "PT2_4_1_3": 3,
    "PT2_4_1_4": 4,
    "PT2_4_1_5": 5,
    "PT2_4_1_6": 6,
    "PT2_1_2_1": 1,
    "PT2_1_2_2": 2,
    "PT2_1_2_3": 3,
    "PT2_1_2_4": 4,
    "PT2_1_2_5": 5,
    "PT2_1_2_6": 6,
    "PT2_2_2_1": 1,
    "PT2_2_2_2": 2,
    "PT2_2_2_3": 3,
    "PT2_2_2_4": 4,
    "PT2_2_2_5": 5,
    "PT2_2_2_6": 6,
    "PT2_3_2_1": 1,
    "PT2_3_2_2": 2,
    "PT2_3_2_3": 3,
    "PT2_3_2_4": 4,
    "PT2_3_2_5": 5,
    "PT2_3_2_6": 6,
    "PT2_4_2_1": 1,
    "PT2_4_2_2": 2,
    "PT2_4_2_3": 3,
    "PT2_4_2_4": 4,
    "PT2_4_2_5": 5,
    "PT2_4_2_6": 6,
    "PT2_1_3_1": 1,
    "PT2_1_3_2": 2,
    "PT2_1_3_3": 3,
    "PT2_1_3_4": 4,
    "PT2_1_3_5": 5,
    "PT2_1_3_6": 6,
    "PT2_2_3_1": 1,
    "PT2_2_3_2": 2,
    "PT2_2_3_3": 3,
    "PT2_2_3_4": 4,
    "PT2_2_3_5": 5,
    "PT2_2_3_6": 6,
    "PT2_3_3_1": 1,
    "PT2_3_3_2": 2,
    "PT2_3_3_3": 3,
    "PT2_3_3_4": 4,
    "PT2_3_3_5": 5,
    "PT2_3_3_6": 6,
    "PT2_4_3_1": 1,
    "PT2_4_3_2": 2,
    "PT2_4_3_3": 3,
    "PT2_4_3_4": 4,
    "PT2_4_3_5": 5,
    "PT2_4_3_6": 6,
}


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
                        "Mr. A was given tickets to lotteries involving the World Series. He won $50 in one lottery and $25 in the other.",
                        html.Br(),
                        "Mr. B was given a ticket to a single, larger World Series lottery. He won $75. Who was happier?",
                        html.Br(),
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario1, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario1-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario1-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot1", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
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
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario2, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario2-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario2-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot2", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
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
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario3, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario3-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario3-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot3", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
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
                        html.Br(),
                        "A: Mister A",
                        html.Br(),
                        "B: Mister B",
                        html.Br(),
                        "C: No difference",
                    ]
                ),
                html.Img(src=PT_og_scenario4, style={'max-width': '100%', 'max-height': '300px', 'margin-left': '60px', 'margin-top': '20px'}),


            ],
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
html.Div(
    children=[
        html.Div(
            children=[
                html.H5("Select experiment design:"),
                dcc.RadioItems(
                    id="prospect-scenario4-radio1",
                    options=[
                        {"label": "Unprimed", "value": 0},
                        {"label": "Primed", "value": 1},
                    ],
                    value=0,
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
                dcc.RadioItems(
                    id="prospect-scenario4-radio2",
                    options=[
                        {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                        {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                        {"label": "LLama-2-70b", "value": "llama-2-70b"},
                    ],
                    value="gpt-3.5-turbo",
                    inputStyle={"margin-right": "10px"},
                    labelStyle={
                        "display": "inline-block",
                        "margin-right": "20px",
                    },
                ),
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
        ),
        dcc.Graph(id="prospect-plot4", style={'width': '70%', 'height': '60vh'}),
    ],
    style={'display': 'flex', 'flexDirection': 'row'},
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
                    html.H5("Select experiment design:", style = {'margin-left': '-75px'}),
                    dcc.Dropdown(
                        id = "prospect2-scenario-dropdown",
                        options = [
                            {"label": "Scenario 1: Segregation of gains", "value": 1},
                            {"label": "Scenario 2: Integration of losses", "value": 2},
                            {"label": "Scenario 3: Cancellation of losses against larger gains", "value": 3},
                            {"label": "Scenario 4: Segregation of silver linings", "value": 4},
                        ],
                        value = 1,
                        style = {'width': '75%'},
                    ),
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
                                style = {'width': '75%'},
                    ),
                    dcc.Dropdown(
                         id = "prospect2-model-dropdown",
                         options = [
                              {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                                {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                                {"label": "LLama-2-70b", "value": "llama-2-70b"},
                            ],
                            value = "gpt-3.5-turbo",
                            style = {'width': '75%'},
                    )],                 
    
                style = {'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'width': '50%', 'align-self': 'center'},
            ),
            dcc.Graph(id = "prospect2-plot", style={'width': '70%', 'height': '60vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'row'})]



### Callback for prospect page

## Experiment 1
# Scenario 1
@dash.callback(
     Output("prospect-plot1", "figure"),
     [Input("prospect-scenario1-radio1", "value"), # priming
        Input("prospect-scenario1-radio2", "value")] # model

)
def update_prospect_plot1(selected_priming, selected_model):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 1) 

# Scenario 2
@dash.callback(
        Output("prospect-plot2", "figure"),
        [Input("prospect-scenario2-radio1", "value"), # priming
        Input("prospect-scenario2-radio2", "value")] #  model

)
def update_prospect_plot2(selected_priming, selected_model):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 2) 


# Scenario 3
@dash.callback(
        Output("prospect-plot3", "figure"),
        [Input("prospect-scenario3-radio1", "value"), # priming
        Input("prospect-scenario3-radio2", "value")] # model
)  
def update_prospect_plot3(selected_priming, selected_model):    
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 3)
    
# Scenario 4
@dash.callback(
        Output("prospect-plot4", "figure"),
        [Input("prospect-scenario4-radio1", "value"), #  priming
        Input("prospect-scenario4-radio2", "value")] #  model
)
def update_prospect_plot4(selected_priming, selected_model):
        return plot_results(model = selected_model, priming = selected_priming, df = PT_probs, scenario = 4)

## Experiment 2
@dash.callback(
     Output("prospect2-plot", "figure"),
     [Input("prospect2-scenario-dropdown", "value"),
      Input("prospect2-configuration-dropdown", "value"),
      Input("prospect2-model-dropdown", "value")]
)
def update_prospect2_plot(selected_scenario, selected_configuration, selected_model):
    df = PT2_probs[PT2_probs["Configuration"] == selected_configuration]
    return plot_results(model = selected_model, df = df, scenario = selected_scenario, priming = 0) # all experiments are unprimed
