# Import required libraries 
import numpy as np
import pandas as pd
import random
import time
from openai import OpenAI
from replicate.client import Client

class Experiment:
    
    """Class to run an experiment with OpenAI's GPT-3.5 and GPT-4 models and Replicate's Llama-2-70b model."""
    
    # Constants
    GPT_3_5_DELAY = 60/3500
    GPT_4_DELAY = 60/500
    LLAMA_DELAY = 1/50
    ANSWER_OPTION_LABELS = ['A', 'B', 'C', 'D', 'E', 'F']
    
    def __init__(self, api_keys, experiment_type, prompts, models, iterations, temperature, num_options, 
                 answers, instruction_checklist, instructions, shuffle_option=False):
        self.api_keys = api_keys
        self.experiment_type = experiment_type
        self.prompts = prompts
        self.models = models
        self.iterations = iterations
        self.temperature = temperature
        self.num_options = num_options
        self.answers = answers
        self.instruction_checklist = instruction_checklist
        self.instructions = instructions
        self.shuffle_options = shuffle_option
        self.replicate = None
        self.client = None
        self.max_tokens_openai = 1
        self.max_tokens_llama = 2
        self.model_answers_dict = {}
        self.raw_model_answers_dict = {}
        self.answer_option_labels = Experiment.ANSWER_OPTION_LABELS[:self.num_options]
        self.model_answers = None
        self.experiment_prompts = []
        self.low_answers_share_warning = False
        
    def run(self):
        
        # Set API keys
        self.set_api_keys()
        
        # Check experiment type
        if self.experiment_type == 'answer_options':
            if self.shuffle_options:
                self.shuffle_answers()
            self.create_prompts()
            
        elif self.experiment_type == 'numeric':
            self.experiment_prompts = self.prompts
            self.max_tokens_openai = 5
            self.max_tokens_llama = 5

        # Process instructions
        self.process_instructions()
        
        results_list = []

        # Iterate through models, prompts, and instructions
        for model in self.models:
            for i, (prompt, instruction) in enumerate(zip(self.experiment_prompts, self.instructions)):
                if model == 'llama-2-70b':
                    self.model_answers = self.run_experiment_with_llama(model, prompt, instruction)
                else:
                    self.model_answers = self.run_experiment_with_openai(model, prompt, instruction)
                
                # Store answers of corresponding model and scenario in a dictionary
                if model not in self.raw_model_answers_dict.keys():
                    self.raw_model_answers_dict[model] = {i: self.model_answers}
                else:
                    self.raw_model_answers_dict[model][i] = self.model_answers
                
                # Create a dictionary to store results for DataFrame
                result_dict = {
                    'Model': model,
                    'Scenario': i+1,
                    'Temperature': self.temperature,
                    'Iterations': self.iterations,
                }
                
                # Count answers depending on experiment type
                if self.experiment_type == 'answer_options':
                    # Check if the answers were shuffled
                    if not self.shuffle_options:
                        result_dict = self.count_answers(result_dict)
                    elif self.shuffle_options:
                        result_dict = self.count_answers_with_shuffle(result_dict, i)
                        
                elif self.experiment_type == 'numeric':
                    result_dict = self.count_answers_numeric(result_dict, model, i)
                    
                results_list.append(result_dict)
            
        self.results_df = pd.DataFrame(results_list)
        
        
    def set_api_keys(self):
        self.client = OpenAI(api_key=self.api_keys['openai'])
        self.replicate = Client(api_token=self.api_keys['replicate'])
                
                
    def run_experiment_with_openai(self, model, prompt, instruction):
        answers = []
        for i in range(self.iterations):
            response = self.openai_api_call(model, prompt, instruction)

            # Store the answer in the list
            answer = response.choices[0].message.content
            answers.append(answer.strip())
            
            # Add delay before the next API call
            if model == 'gpt-3.5-turbo-1106':
                time.sleep(Experiment.GPT_3_5_DELAY)
            else:
                time.sleep(Experiment.GPT_4_DELAY)

        return answers
    
    
    def run_experiment_with_llama(self, model, prompt, instruction):
        model = 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3'
        answers = []
        for i in range(self.iterations):
            response = self.replicate_api_call(model, prompt, instruction)

            # Store the answer in the list
            answer = ''
            for item in response:
                answer += item

            answers.append(answer.strip())
            
            # Add delay before the next API call
            time.sleep(Experiment.LLAMA_DELAY)

        return answers
    
    
    def create_prompts(self):
        # Split answers into sublists
        len_answer_sublists = len(self.answers) // self.num_options
        split_answer_lists = [self.answers[i * self.num_options:(i + 1) * self.num_options] for i in range(len_answer_sublists)]
        
        self.experiment_prompts = []
        
        # Combine prompts and answers to one string
        for prompt, answers in zip(self.prompts, split_answer_lists):
            
            experiment_prompts = f"""{prompt}\nA: {answers[0]}\nB: {answers[1]}"""

            # Add additional answer options if there are more than 2
            for i, label in enumerate(self.answer_option_labels[2:]):
                experiment_prompts += f"""\n{label}: {answers[i+2]}"""
                
            self.experiment_prompts.append(experiment_prompts)
            
    
    def process_instructions(self):
        # Check if the instruction checklist contains "add_instruction"
        if "add_instruction" in self.instruction_checklist:
            self.instructions = [text if text is not None else "" for text in self.instructions]
        # If not, set instructions to empty strings
        else:
            self.instructions = ["" for _ in range(len(self.prompts))]
            
            
    def count_answers(self, result_dict):
        # Count of "correct" answers
        len_correct = sum(1 for ans in self.model_answers if ans in self.answer_option_labels)
        
        result_dict['Correct Answers'] = len_correct
        
        # Check if the share of correct answers is less than 50%
        if (len_correct / self.iterations) < 0.5:
            self.low_answers_share_warning = True
        
        # Check if len_correct is non-zero before performing further calculations
        if len_correct > 0:
            # Counting results
            for label in self.answer_option_labels:
                label_share = self.model_answers.count(label) / len_correct
                result_dict['Share of ' + label] = round(label_share, 2)
        else:
            # Set NaN values for share of labels when len_correct is 0
            for label in self.answer_option_labels:
                result_dict['Share of ' + label] = float('nan')
                
        return result_dict
    
    
    def count_answers_with_shuffle(self, result_dict, i):
        # Count of "correct" answers
        len_correct = sum(1 for ans in self.model_answers if ans in self.answer_option_labels)
        
        result_dict['Correct Answers'] = len_correct
        
        # Check if the share of correct answers is less than 50%
        if (len_correct / self.iterations) < 0.5:
            self.low_answers_share_warning = True
        
        # Check if len_correct is non-zero before performing further calculations
        if len_correct > 0:
            for ans in self.answer_label_mapping[i].keys():
                label_share = self.model_answers.count(self.answer_label_mapping[i][ans]) / len_correct
                result_dict[f'Share of "{ans}"'] = round(label_share, 2)
            
        else: 
            for ans in self.answer_label_mapping[i].keys():
                result_dict[f'Share of "{ans}"'] = float('nan')  
                
        return result_dict
                
                
    def count_answers_numeric(self, result_dict, model, i):
        
        # Filter out valid prices
        valid_prices = [item for item in self.model_answers if item.startswith("$")]
        
        # Check if the share of valid prices is less than 50%
        if (len(valid_prices) / self.iterations) < 0.5:
            self.low_answers_share_warning = True
        
        # Remove commas and dollar signs, convert to float
        prices = [item.replace(',', '').rstrip('.') for item in valid_prices]
        prices = [float(item.replace('$', '')) for item in prices if item != '$']
        
        # Store answers of corresponding model and scenario in a dictionary
        if model not in self.model_answers_dict.keys():
            self.model_answers_dict[model] = {i: prices}
        else:
            self.model_answers_dict[model][i] = prices
        
        result_dict['Correct Answers'] = len(valid_prices)
        
        # Calculate the mean, median, and quartiles
        result_dict['Average'] = round(np.mean(prices), 2)
        
        if len(prices) > 1:
            result_dict['25th Percentile'] = round(np.percentile(prices, 25), 2)
        
        result_dict['Median'] = round(np.median(prices), 2)
        
        if len(prices) > 1:
            result_dict['75th Percentile'] = round(np.percentile(prices, 75), 2)
        
        return result_dict
        
            
    def openai_api_call(self, model, prompt, instruction):
        response = self.client.chat.completions.create(
                model=model,  
                messages=[
                    {"role": "system", "content": instruction},

                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens_openai,
                temperature=self.temperature
            )
        
        return response
    
    
    def replicate_api_call(self, model, prompt, instruction):
        response = self.replicate.run(model,
                                 input = {
                                     "temperature": self.temperature,
                                     "system_prompt": instruction,
                                     "prompt": prompt,
                                     "max_new_tokens": self.max_tokens_llama}
                                 )
        
        return response
    
    
    def shuffle_answers(self):
        num_shuffles = 2 if self.num_options == 2 else 3
        
        # Duplicate prompt
        self.prompts = [self.prompts[0]] * num_shuffles
        
        # Duplicate instructions
        if "add_instruction" in self.instruction_checklist:
            self.instructions = [self.instructions[0]] * num_shuffles
        else:
            self.instructions = None

        # Shuffle answers
        shuffled_answers1 = self.answers.copy()
        
        for i in range(num_shuffles-1):
            shuffled_answers2 = shuffled_answers1.copy()
            while shuffled_answers1 == shuffled_answers2:  # Make sure the answers are different
                random.shuffle(shuffled_answers1)
            self.answers += shuffled_answers1
        
        # Create answer-label dictionary to keep track which label corresponds to which answer
        self.answer_label_mapping = []
        # Iterate through answers and create dictionaries
        count = 0
        while count < len(self.answers):
            answers = self.answers[count:count+self.num_options]
            self.answer_label_mapping.append({answer: label for label, answer in zip(self.answer_option_labels, answers)})
            count += self.num_options