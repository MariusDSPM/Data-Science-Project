# Collection of functions to run the experiments concerning:
# Prospect Theory
# Prospect Theory 2
# Decoy Effect
# Transaction Utility
# Transaction Utility 2
# Transaction Utility 3

# Import required libraries
from openai import OpenAI
from replicate.client import Client
import openai
import matplotlib.pyplot as plt
import os 
import numpy as np
import pandas as pd
from tqdm import tqdm
import replicate
from ast import literal_eval
import plotly.graph_objects as go
import pickle

##### General function to calculate costs of experiment (prices given per thousand tokens)
GPT_3_5_INPUT_COST = 0.0005
GPT_3_5_OUTPUT_COST = 0.0015
GPT_4_INPUT_COST = 0.01
GPT_4_OUTPUT_COST = 0.03
LLAMA_2_INPUT_COST = GPT_4_INPUT_COST 
LLAMA_2_OUTPUT_COST = GPT_4_OUTPUT_COST 

# Function to count words in prompts and estimate costs (we generously round output tokens to 5, to prevent underestimation)
def cost_estimate(prompt, selected_model, iterations):
    tokens = len(prompt.split())   # Counting words in the prompt
    if selected_model == "gpt-3.5-turbo":
        costs = (tokens * GPT_3_5_INPUT_COST + 5 * GPT_3_5_OUTPUT_COST) * iterations / 1000
    elif selected_model == "gpt-4-1106-preview":
        costs = (tokens * GPT_4_INPUT_COST + 5 * GPT_4_OUTPUT_COST) * iterations / 1000
    elif selected_model == "llama-2-70b":
        costs = (tokens * LLAMA_2_INPUT_COST + 5 * LLAMA_2_OUTPUT_COST) * iterations / 1000

    return costs



##### Import and assign prompts for every experiment
### Prospect Theory
with open('data/Input/PT_prompts.pkl', 'rb') as f:
    PT_prompts = pickle.load(f)

### Prospect Theory 2
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


### Decoy Effect
with open('data/Input/DE_prompts.pkl', 'rb') as f:
    DE_prompts = pickle.load(f)

### Transaction Utility
with open('data/Input/TU_prompts.pkl', 'rb') as f:
    TU_prompts = pickle.load(f)

### Transaction Utility 2
with open('data/Input/TU2_prompts.pkl', 'rb') as f:
    TU2_prompts = pickle.load(f)

### Transaction Utility 3
with open('data/Input/TU3_prompts.pkl', 'rb') as f:
    TU3_prompts = pickle.load(f)

## Import and assign dictionaries for every experiment
### Prospect Theory
with open('data/Input/PT_dictionaries.pkl', 'rb') as f:
    PT_dictionaries = pickle.load(f)
PT_experiment_prompts_dict, PT_prompt_ids_dict, PT_model_dict, PT_scenario_dict, PT_priming_dict, PT_results_dict, PT_answercount_dict = PT_dictionaries

### Prospect Theory 2
with open('data/Input/PT2_dictionaries.pkl', 'rb') as f:
    PT2_dictionaries = pickle.load(f)
(PT2_experiment_prompts_dict, PT2_prices_dict, PT2_results_dict, PT2_model_dict, PT2_prompt_ids_dict,
PT2_scenario_dict, PT2_configuration_dict) = PT2_dictionaries

### Decoy Effect
with open('data/Input/DE_dictionaries.pkl', 'rb') as f:
    DE_dictionaries = pickle.load(f)
(DE_experiment_prompts_dict, DE_prompt_ids_dict, DE_model_dict, DE_og_results_dict, DE_answercount_dict,
  DE_scenario_dict, DE_priming_dict, DE_reorder_dict) = DE_dictionaries

### Transaction Utility
with open('data/Input/TU_dictionaries.pkl', 'rb') as f:
    TU_dictionaries = pickle.load(f)
(TU_experiment_prompts_dict, TU_model_dict, TU_prompt_ids_dict, TU_initial_costs_dict, TU_orientation_prices_dict, TU_buyers_dict,
  TU_results_dict, TU_answercount_dict, TU_configurations_dict, TU_experiment_ids_dict) = TU_dictionaries

### Transaction Utility 2
with open('data/Input/TU2_dictionaries.pkl', 'rb') as f:
    TU2_dictionaries = pickle.load(f)
TU2_experiment_prompts_dict, TU2_model_dict, TU2_prompt_ids_dict, TU2_places_dict, TU2_income_dict, TU2_configuration_dict = TU2_dictionaries

### Transaction Utility 3
with open('data/Input/TU3_dictionaries.pkl', 'rb') as f:
    TU3_dictionaries = pickle.load(f)
(TU3_experiment_prompts_dict, TU3_model_dict, TU3_prompt_ids_dict, TU3_actual_price_dict,
                     TU3_initial_costs_dict, TU3_orientation_price_dict, TU3_configuration_dict, TU3_buyer_dict) = TU3_dictionaries



### Prospect Theory ### 

# openAI models
def PT_run_experiment_dashboard(experiment_id, n, temperature, openai_key):

    """
    Function to query ChatGPT multiple times with a survey having answers designed as: A, B, C.
    
    Args:
        experiment_id (str): ID of the experiment to be run. Contains info about prompt and model
        n (int): Number of queries to be made
        temperature (int): Degree of randomness with range 0 (deterministic) to 2 (random)
        max_tokens (int): Maximum number of tokens in response object
        
    Returns:
        results (list): List containing count of answers for each option, also containing experiment_id, temperature and number of observations
        probs (list): List containing probability of each option being chosen, also containing experiment_id, temeperature and number of observations
    """
    client = OpenAI(api_key=openai_key)
    answers = []
    for _ in range(n): 
        response = client.chat.completions.create(
            model = PT_model_dict[experiment_id], 
            max_tokens = 1,
            temperature = temperature, # range is 0 to 2
            messages = [
            {"role": "system", "content": "Only answer with the letter of the alternative you would choose without any reasoning."},        
            {"role": "user", "content": PT_experiment_prompts_dict[experiment_id]},
                   ])

        # Store the answer in the list
        answer = response.choices[0].message.content
        answers.append(answer.strip())

    # Counting results
    A = answers.count("A")
    B = answers.count("B")
    C = answers.count("C")

    # Count of "correct" answers, sums over indicator function thack checks if answer is either A, B or C
    len_correct = sum(1 for ans in answers if ans in ["A", "B", "C"])

    # Collecting results in a list
    results = [experiment_id, temperature, A, B, C, len_correct, PT_model_dict[experiment_id], PT_scenario_dict[experiment_id],
               PT_priming_dict[experiment_id], f"{PT_results_dict[experiment_id]}", PT_answercount_dict[experiment_id]]
    results = pd.DataFrame(results)
    results = results.set_index(pd.Index(["Experiment_id", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Original", "Original_count"]))
    results = results.transpose()

    # Getting percentage of each answer
    p_a = (A / len_correct) * 100 if len_correct != 0 else 0
    p_b = (B / len_correct) * 100 if len_correct != 0 else 0
    p_c = (C / len_correct) * 100 if len_correct != 0 else 0

    # Collect probabilities in a dataframe
    probs = [experiment_id, temperature, p_a, p_b, p_c, len_correct, PT_model_dict[experiment_id], PT_scenario_dict[experiment_id],
             PT_priming_dict[experiment_id], f"{PT_results_dict[experiment_id]}", PT_answercount_dict[experiment_id]]
    probs = pd.DataFrame(probs)
    probs = probs.set_index(pd.Index(["Experiment_id", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Original", "Original_count"]))
    probs = probs.transpose()
        
    # Give out results
    return results, probs

# LLama model
def PT_run_experiment_llama_dashboard(experiment_id, n, temperature, replicate_token):
    replicate = Client(api_token = replicate_token)
    answers = []
    for _ in range(n):
        response = replicate.run(
            PT_model_dict[experiment_id],
            input = {
                "system_prompt": "Only answer with the letter of the alternative you would choose without any reasoning.",
                "temperature": temperature,
                "max_new_tokens": 2, 
                "prompt": PT_experiment_prompts_dict[experiment_id]
            }
        )
        # Grab answer and append to list
        answer = "" # Set to empty string, otherwise it would append the previous answer to the new one
        for item in response:
            answer = answer + item
        answers.append(answer.strip())


    # Counting results
    A = answers.count("A")
    B = answers.count("B")
    C = answers.count("C")

    # Count of "correct" answers, sums over indicator function thack checks if answer is either A, B or C
    len_correct = sum(1 for ans in answers if ans in ["A", "B", "C"])
    
    # Collecting results in a list
    results = [experiment_id, temperature, A, B, C, len_correct, PT_model_dict[experiment_id], PT_scenario_dict[experiment_id],
               PT_priming_dict[experiment_id], f"{PT_results_dict[experiment_id]}", PT_answercount_dict[experiment_id]]
    results = pd.DataFrame(results)
    results = results.set_index(pd.Index(["Experiment_id", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Original", "Original_count"]))
    results = results.transpose()


    # Getting percentage of each answer
    p_a = (A / len_correct) * 100 if len_correct != 0 else 0
    p_b = (B / len_correct) * 100 if len_correct != 0 else 0
    p_c = (C / len_correct) * 100 if len_correct != 0 else 0

    # Collect probabilities in a dataframe
    probs = [experiment_id, temperature, p_a, p_b, p_c, len_correct, PT_model_dict[experiment_id], PT_scenario_dict[experiment_id],
             PT_priming_dict[experiment_id], f"{PT_results_dict[experiment_id]}", PT_answercount_dict[experiment_id]]
    probs = pd.DataFrame(probs)
    probs = probs.set_index(pd.Index(["Experiment_id", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Original", "Original_count"]))
    probs = probs.transpose()
        
    # Give out results
    return results, probs


### Prospect Theory 2 ###

# openAI models
def PT2_run_experiment_dashboard(experiment_id, n, temperature, openai_key):

    """
    Function to query ChatGPT multiple times with a survey having answers designed as: A, B, C.
    
    Args:
        experiment_id (str): ID of the experiment to be run. Contains info about prompt and model
        n (int): Number of queries to be made
        temperature (int): Degree of randomness with range 0 (deterministic) to 2 (random)
        max_tokens (int): Maximum number of tokens in response object
        
    Returns:
        results (list): List containing count of answers for each option, also containing experiment_id, temperature and number of observations
        probs (list): List containing probability of each option being chosen, also containing experiment_id, temeperature and number of observations
    """
    client = OpenAI(api_key=openai_key)
    answers = []
    for _ in range(n): 
        response = client.chat.completions.create(
            model = PT2_model_dict[experiment_id], 
            max_tokens = 1,
            temperature = temperature, # range is 0 to 2
            messages = [
            {"role": "system", "content": "Only answer with the letter of the alternative you would choose without any reasoning."},        
            {"role": "user", "content": PT2_experiment_prompts_dict[experiment_id]},
                   ])

        # Store the answer in the list
        answer = response.choices[0].message.content
        answers.append(answer.strip())

    # Counting results
    A = answers.count("A") 
    B = answers.count("B") 
    C = answers.count("C") 

    # Count of "correct" answers, sums over indicator function thack checks if answer is either A, B or C
    len_correct = sum(1 for ans in answers if ans in ["A", "B", "C"])

    # Collecting results in a list
    results = pd.DataFrame([experiment_id, temperature, A, B, C, len_correct, PT2_model_dict[experiment_id], PT2_scenario_dict[experiment_id], PT2_configuration_dict[experiment_id]])
    results = results.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Configuration"]))
    results = results.transpose()

   # Getting percentage of each answer
    p_a = (A / len_correct) * 100 if len_correct != 0 else 0
    p_b = (B / len_correct) * 100 if len_correct != 0 else 0
    p_c = (C / len_correct) * 100 if len_correct != 0 else 0

    # Collect probabilities in a dataframe
    probs = pd.DataFrame([experiment_id, temperature, p_a, p_b, p_c, len_correct, PT2_model_dict[experiment_id], PT2_scenario_dict[experiment_id], PT2_configuration_dict[experiment_id]])
    probs = probs.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Configuration"]))
    probs = probs.transpose() # Transpose to use existing plotting function

    # Give out results
    return results, probs

# Llama model
def PT2_run_experiment_llama_dashboard(experiment_id, n, temperature, replicate_token):
    answers = []
    replicate = Client(api_token = replicate_token)
    for _ in range(n):
        response = replicate.run(
            PT2_model_dict[experiment_id],
            input = {
                "system_prompt": "Only answer with the letter of the alternative you would choose without any reasoning.",
                "temperature": temperature,
                "max_new_tokens": 2, 
                "prompt": PT2_experiment_prompts_dict[experiment_id]
            }
        )
        # Grab answer and append to list
        answer = "" # Set to empty string, otherwise it would append the previous answer to the new one
        for item in response:
            answer = answer + item
        answers.append(answer.strip())


    # Counting results
    A = answers.count("A") 
    B = answers.count("B") 
    C = answers.count("C") 

    # Count of "correct" answers, sums over indicator function thack checks if answer is either A, B or C
    len_correct = sum(1 for ans in answers if ans in ["A", "B", "C"])

    # Collecting results in a list
    results = pd.DataFrame([experiment_id, temperature, A, B, C, len_correct, PT2_model_dict[experiment_id], PT2_scenario_dict[experiment_id], PT2_configuration_dict[experiment_id]])
    results = results.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Configuration"]))
    results = results.transpose()

   # Getting percentage of each answer
    p_a = (A / len_correct) * 100 if len_correct != 0 else 0
    p_b = (B / len_correct) * 100 if len_correct != 0 else 0
    p_c = (C / len_correct) * 100 if len_correct != 0 else 0
    
    # Collect probabilities in a dataframe
    probs = pd.DataFrame([experiment_id, temperature, p_a, p_b, p_c, len_correct, PT2_model_dict[experiment_id], PT2_scenario_dict[experiment_id], PT2_configuration_dict[experiment_id]])
    probs = probs.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Configuration"]))
    probs = probs.transpose()
    
    # Give out results
    return results, probs


### Decoy Effect ###

# Functions to process answers

def DE_count_answers(answers: list, experiment_id: str):
    if experiment_id in ["DE_1_1", "DE_1_3","DE_2_1", "DE_2_3", "DE_3_1", "DE_3_3"]:
        A = answers.count("A")
        B = answers.count("B")
        C = answers.count("C")
    elif experiment_id in ["DE_1_2", "DE_1_4", "DE_2_2", "DE_2_4", "DE_3_2", "DE_3_4"]:
        A = answers.count("A")
        B = 0 # Option B was removed
        C = answers.count("B") # makes comparison of results over prompts easier 
    elif experiment_id in ["DE_1_5", "DE_1_7", "DE_2_5", "DE_2_7", "DE_3_5", "DE_3_7"]:
        A = answers.count("Y")
        B = answers.count("Q")
        C = answers.count("X")
    elif experiment_id in ["DE_1_6", "DE_1_8", "DE_2_6", "DE_2_8", "DE_3_6", "DE_3_8"]:
        A = answers.count("Y")
        B = 0 # Option Q was removed
        C = answers.count("X")
    return A, B, C

def DE_correct_answers(answers: list, experiment_id: str):
    if experiment_id in ["DE_1_1", "DE_1_3","DE_2_1", "DE_2_3", "DE_3_1", "DE_3_3"]:
        len_correct = sum(1 for ans in answers if ans in ["A", "B", "C"])
    elif experiment_id in ["DE_1_2", "DE_1_4", "DE_2_2", "DE_2_4", "DE_3_2", "DE_3_4"]:
        len_correct = sum(1 for ans in answers if ans in ["A", "B"])
    elif experiment_id in ["DE_1_5", "DE_1_7", "DE_2_5", "DE_2_7", "DE_3_5", "DE_3_7"]:
        len_correct = sum(1 for ans in answers if ans in ["Y", "Q", "X"])
    elif experiment_id in ["DE_1_6", "DE_1_8", "DE_2_6", "DE_2_8", "DE_3_6", "DE_3_8"]:
        len_correct = sum(1 for ans in answers if ans in ["Y", "X"])
    return len_correct  

# Functions to run the experiment
# openAI models
def DE_run_experiment_dashboard(experiment_id: int, n: int, temperature: int, openai_key):
    """
    Function to query ChatGPT multiple times with a survey having answers designed as: A, B, C.
    
    Args:
        experiment_id (str): ID of the experiment to be run. Contains info about prompt and model
        n (int): Number of queries to be made
        temperature (int): Degree of randomness with range 0 (deterministic) to 2 (random)
        max_tokens (int): Maximum number of tokens in response object
        
    Returns:
        results (list): List containing count of answers for each option, also containing experiment_id, temperature and number of observations
        probs (list): List containing probability of each option being chosen, also containing experiment_id, temeperature and number of observations
    """
    answers = []
    client = OpenAI(api_key=openai_key)
    for _ in range(n): 
        response = client.chat.completions.create(
            model = DE_model_dict[experiment_id], 
            max_tokens = 5,
            temperature = temperature, # range is 0 to 2
            messages = [
            {"role": "system", "content": "Only answer with the letter of the alternative you would choose without any reasoning."},
            {"role": "user", "content": DE_experiment_prompts_dict[experiment_id]},
                   ])

        # Store the answer in the list
        answer = response.choices[0].message.content
        answers.append(answer.strip())

    # Count the answers
    A, B, C = DE_count_answers(answers, experiment_id)
    
    # Count of correct answers
    len_correct = int(DE_correct_answers(answers, experiment_id)) 

    # Collecting results in a list
    results = pd.DataFrame([experiment_id, temperature, A, B, C, len_correct, DE_model_dict[experiment_id], DE_scenario_dict[experiment_id],
                             DE_priming_dict[experiment_id], DE_reorder_dict[experiment_id], DE_og_results_dict[experiment_id], DE_answercount_dict[experiment_id]])
    results = results.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Reorder", "Original", "Original_count"]))
    results = results.transpose()
    
   # Getting percentage of each answer
    p_a = (A / len_correct) * 100 if len_correct != 0 else 0
    p_b = (B / len_correct) * 100 if len_correct != 0 else 0
    p_c = (C / len_correct) * 100 if len_correct != 0 else 0

    # Collect probabilities in a dataframe
    probs = pd.DataFrame([experiment_id, temperature, p_a, p_b, p_c, len_correct, DE_model_dict[experiment_id], DE_scenario_dict[experiment_id],
                           DE_priming_dict[experiment_id], DE_reorder_dict[experiment_id], f"{DE_og_results_dict[experiment_id]}", DE_answercount_dict[experiment_id]])
    probs = probs.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Reorder", "Original", "Original_count"]))
    probs = probs.transpose()

    return results, probs 

# Llama model
def DE_run_experiment_llama_dashboard(experiment_id, n, temperature, replicate_token):
    answers = []
    replicate = Client(api_token = replicate_token)
    for _ in range(n):
        response = replicate.run(
            DE_model_dict[experiment_id],
            input = {
                "system_prompt": "Only answer with the letter of the alternative you would choose without any reasoning.",
                "temperature": temperature,
                "max_new_tokens": 2, 
                "prompt": DE_experiment_prompts_dict[experiment_id]
            }
        )
        # Grab answer and append to list
        answer = "" # Set to empty string, otherwise it would append the previous answer to the new one
        for item in response:
            answer = answer + item
        answers.append(answer.strip())

    # Count the answers
    A, B, C = DE_count_answers(answers, experiment_id) # if/else statement of function deals with different answer options in different experiments
    
    # Count of correct answers
    len_correct = int(DE_correct_answers(answers, experiment_id)) # if/else of function makes sure that we count the correct answers according to the experiment id 

    # Collecting results in a list
    results = pd.DataFrame([experiment_id, temperature, A, B, C, len_correct, DE_model_dict[experiment_id], DE_scenario_dict[experiment_id],
                             DE_priming_dict[experiment_id], DE_reorder_dict[experiment_id], DE_og_results_dict[experiment_id], DE_answercount_dict[experiment_id]])
    results = results.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Reorder", "Original", "Original_count"]))
    results = results.transpose()

   # Getting percentage of each answer
    p_a = (A / len_correct) * 100 if len_correct != 0 else 0
    p_b = (B / len_correct) * 100 if len_correct != 0 else 0
    p_c = (C / len_correct) * 100 if len_correct != 0 else 0

    # Collect probabilities in a dataframe
    probs = pd.DataFrame([experiment_id, temperature, p_a, p_b, p_c, len_correct, DE_model_dict[experiment_id], DE_scenario_dict[experiment_id],
                           DE_priming_dict[experiment_id], DE_reorder_dict[experiment_id],  f"{DE_og_results_dict[experiment_id]}", DE_answercount_dict[experiment_id]])
    probs = probs.set_index(pd.Index(["Experiment", "Temp", "A", "B", "C", "Obs.", "Model", "Scenario", "Priming", "Reorder", "Original", "Original_count"]))
    probs = probs.transpose()
    # Give out results
    return results, probs


### Transaction Utility ###

# Functions to process answers
def extract_dollar_amounts(answers):
    # Only return values that start with "$"
    valid_prices = [item for item in answers if item.startswith("$") and item[1:].replace(',', '').replace('.', '').isdigit()] # check if everything after $ is a digit, exlcuding commas
    # Delete the "$" from the beginning of each price
    prices = [item.replace('$', '') for item in valid_prices]
    return prices

# openAI models
def TU_run_experiment_dashboard(experiment_id, n, temperature, openai_key):
    client = OpenAI(api_key=openai_key)
    answers = []
    for _ in range(n): 
        response = client.chat.completions.create(
            model = TU_model_dict[experiment_id], 
            max_tokens = 2,
            temperature = temperature, # range is 0 to 2
            messages = [
            {"role": "system", "content": "Answer by only giving a single price in dollars and cents without an explanation."},        
            {"role": "user", "content": 
             f"{TU_experiment_prompts_dict[experiment_id]} Answer by only giving a single price in dollars and cents without an explanation."}
                   ])

        # Store the answer in the list
        answer = response.choices[0].message.content
        answers.append(answer.strip())

    # Extract valid prices from answers
    valid_prices = extract_dollar_amounts(answers)

    # Compute number of valid answers
    n_observations = len(valid_prices)

    # Collect results 
    results = pd.DataFrame([experiment_id, temperature, TU_model_dict[experiment_id], TU_initial_costs_dict[experiment_id], TU_orientation_prices_dict[experiment_id],
                TU_buyers_dict[experiment_id], f"{answers}", n_observations, TU_configurations_dict[experiment_id], f"{TU_results_dict[experiment_id]}", TU_answercount_dict[experiment_id]])
    results = results.set_index(pd.Index(
        ["Experiment_id", "Temperature", "Model", "Initial_cost", "Orientation_price", "Buyer", "Answers", "Obs.", "Configuration", "Original", "Original_count"]))
    results = results.transpose()    

    # Give out results
    return results

# Llama model
def TU_run_experiment_llama_dashboard(experiment_id, n, temperature, replicate_token):
    answers = []
    replicate = Client(api_token = replicate_token)
    for _ in range(n):
        response = replicate.run(
            TU_model_dict[experiment_id],
            input = {
                "system_prompt":  "Answer by only giving a single price in dollars and cents without an explanation.",
                "temperature": temperature,
                "max_new_tokens": 10, 
                "prompt": f"{TU_experiment_prompts_dict[experiment_id]} Answer by only giving a single price in dollars and cents without an explanation."
            }
        )
        # Grab answer and append to list
        answer = "" # Set to empty string, otherwise it would append the previous answer to the new one
        for item in response:
            answer = answer + item
        answers.append(answer.strip())
   
    # Extract valid prices from answers
    valid_prices = extract_dollar_amounts(answers)

    # Compute number of valid answers
    n_observations = len(valid_prices)

    # Collect results 
    results = pd.DataFrame([experiment_id, temperature, TU_model_dict[experiment_id], TU_initial_costs_dict[experiment_id], TU_orientation_prices_dict[experiment_id],
                TU_buyers_dict[experiment_id], f"{answers}", n_observations, TU_configurations_dict[experiment_id], f"{TU_results_dict[experiment_id]}", TU_answercount_dict[experiment_id]])
    results = results.set_index(pd.Index(
        ["Experiment_id", "Temperature", "Model", "Initial_cost", "Orientation_price", "Buyer", "Answers", "Obs.", "Configuration", "Original", "Original_count"]))
    results = results.transpose()    

    # Give out results
    return results

### Transaction Utility 2 ###

# openAI models
def TU2_run_experiment_dashboard(experiment_id, n, temperature, openai_key):
    client = OpenAI(api_key=openai_key)
    answers = []
    for _ in range(n): 
        response = client.chat.completions.create(
            model = TU2_model_dict[experiment_id], 
            max_tokens = 2,
            temperature = temperature, # range is 0 to 2
            messages = [
            {"role": "system", "content": "Answer by only giving a single price in dollars and cents without an explanation."},        
            {"role": "user", "content": 
             f"{TU2_experiment_prompts_dict[experiment_id]} Answer by only giving a single price in dollars and cents without an explanation."}
                   ])

        # Store the answer in the list
        answer = response.choices[0].message.content
        answers.append(answer.strip())


    # Extract valid prices from answers
    valid_prices = extract_dollar_amounts(answers)

    # Compute number of valid answers
    n_observations = len(valid_prices)

    # Collect results 
    results = [experiment_id, temperature, TU2_model_dict[experiment_id], TU2_places_dict[experiment_id],
                TU2_income_dict[experiment_id], f"{answers}", n_observations, TU2_configuration_dict[experiment_id]]
    results = pd.DataFrame(results, index = ["Experiment_id", "Temperature", "Model", "Place", "Income", "Answers", "Obs.", "Configuration"]).T

    # Give out results
    return results

# Llama model
def TU2_run_experiment_llama_dashboard(experiment_id, n, temperature, replicate_token):
    answers = []
    replicate = Client(api_token = replicate_token)
    for _ in range(n):
        response = replicate.run(
            TU2_model_dict[experiment_id],
            input = {
                "system_prompt":  "Answer by only giving a single price in dollars and cents without an explanation.",
                "temperature": temperature,
                "max_new_tokens": 10, 
                "prompt": f"{TU2_experiment_prompts_dict[experiment_id]} Answer by only giving a single price in dollars and cents without an explanation."
            }
        )
        # Grab answer and append to list
        answer = "" # Set to empty string, otherwise it would append the previous answer to the new one
        for item in response:
            answer = answer + item
        answers.append(answer.strip())

   # Extract valid prices from answers
    valid_prices = extract_dollar_amounts(answers)

    # Compute number of valid answers
    n_observations = len(valid_prices)

    # Collect results 
    results = [experiment_id, temperature, TU2_model_dict[experiment_id], TU2_places_dict[experiment_id],
                TU2_income_dict[experiment_id], f"{answers}", n_observations, TU2_configuration_dict[experiment_id]]
    results = pd.DataFrame(results, index = ["Experiment_id", "Temperature", "Model", "Place", "Income", "Answers", "Obs.", "Configuration"]).T
    
    # Give out results
    return results

### Transaction Utility 3 ###

# openAI models
def TU3_run_experiment_dashboard(experiment_id, n, temperature, openai_key):
    client = OpenAI(api_key=openai_key)
    answers = []
    for _ in range(n): 
        response = client.chat.completions.create(
            model = TU3_model_dict[experiment_id], 
            max_tokens = 2,
            temperature = temperature, # range is 0 to 2
            messages = [
            {"role": "system", "content": "Answer by only giving a single price in dollars and cents without an explanation."},        
            {"role": "user", "content": 
             f"{TU3_experiment_prompts_dict[experiment_id]} Answer by only giving a single price in dollars and cents without an explanation."}
                   ])

        # Store the answer in the list
        answer = response.choices[0].message.content
        answers.append(answer.strip())

    # Extract valid prices from answers
    valid_prices = extract_dollar_amounts(answers)

    # Compute number of valid answers
    n_observations = len(valid_prices)

    # Collect results 
    results = pd.DataFrame([experiment_id, temperature, TU3_model_dict[experiment_id], TU3_actual_price_dict[experiment_id], TU3_initial_costs_dict[experiment_id],
                TU3_orientation_price_dict[experiment_id], TU3_configuration_dict[experiment_id], n_observations, f"{valid_prices}", TU3_buyer_dict[experiment_id]])
    results = results.set_index(pd.Index(["Experiment_id", "Temperature", "Model", "Actual_price", "Initial_cost", "Orientation_price", "Configuration", "Obs.", "Answers", "Buyer"]))
    results = results.transpose()
    



    # Give out results
    return results

# Llama model
def TU3_run_experiment_llama_dashboard(experiment_id, n, temperature, replicate_token):
    answers = []
    replicate = Client(api_token = replicate_token)
    for _ in range(n):
        response = replicate.run(
            TU3_model_dict[experiment_id],
            input = {
                "system_prompt":  "Answer by only giving a single price in dollars and cents without an explanation.",
                "temperature": temperature,
                "max_new_tokens": 10, 
                "prompt": f"{TU3_experiment_prompts_dict[experiment_id]} Answer by only giving a single price in dollars and cents without an explanation."
            }
        )
        # Grab answer and append to list
        answer = "" # Set to empty string, otherwise it would append the previous answer to the new one
        for item in response:
            answer = answer + item
        answers.append(answer.strip())
   
    # Extract valid prices from answers
    valid_prices = extract_dollar_amounts(answers)

    # Compute number of valid answers
    n_observations = len(valid_prices)

    # Collect results 
    results = pd.DataFrame([experiment_id, temperature, TU3_model_dict[experiment_id], TU3_actual_price_dict[experiment_id], TU3_initial_costs_dict[experiment_id],
                TU3_orientation_price_dict[experiment_id], TU3_configuration_dict[experiment_id], n_observations, f"{valid_prices}", TU3_buyer_dict[experiment_id]])
    results = results.set_index(pd.Index(["Experiment_id", "Temperature", "Model", "Actual_price", "Initial_cost", "Orientation_price", "Configuration", "Obs.", "Answers", "Buyer"]))
    results = results.transpose()
    

    # Give out results
    return results















