# Import required libraries 
import pandas as pd
import plotly.graph_objects as go
import random
import time
from openai import OpenAI
import openai
import replicate
import os


# Get openAI API key (previously saved as environmental variable)
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set client
client = OpenAI()


class Experiment:
    
    OPENAI_MAX_TOKENS = 1
    LLAMA_MAX_TOKENS = 2
    GPT_3_5_DELAY = 60/3500
    GPT_4_DELAY = 60/500
    LLAMA_DELAY = 1/50
    ANSWER_OPTION_LABELS = ['A', 'B', 'C', 'D', 'E', 'F']
    
    def __init__(self, prompts, models, iterations, temperature, num_options, 
                 answers, instruction_checklist, instructions, shuffle_option=False):
        self.prompts = prompts
        self.models = models
        self.iterations = iterations
        self.temperature = temperature
        self.num_options = num_options
        self.answers = answers
        self.instruction_checklist = instruction_checklist
        self.instructions = instructions
        self.shuffle_options = shuffle_option
        self.model_answers_dict = {}
        self.answer_option_labels = Experiment.ANSWER_OPTION_LABELS[:self.num_options]
        
    def run(self):
        
        if self.shuffle_options:
            self.shuffle_answers()
        self.create_prompts()
        self.process_instructions()
        
        results_list = []
    
        for model in self.models:
            for i, (prompt, instruction) in enumerate(zip(self.experiment_prompts, self.instructions)):
                if model == 'llama-2-70b':
                    self.model_answers = self.run_experiment_with_llama(model, prompt, instruction)
                else:
                    self.model_answers = self.run_experiment_with_openai(model, prompt, instruction)
                
                # Store answers of corresping model and scenario in a dictionary
                self.model_answers_dict[f'{model} - {i}'] = self.model_answers
        
                # Count of "correct" answers
                len_correct = sum(1 for ans in self.model_answers if ans in self.answer_option_labels)
                
                result_dict = {
                    'Model': model,
                    'Scenario': i+1,
                    'Temperature': self.temperature,
                    'Iterations': self.iterations,
                    'Correct Answers': len_correct
                }
                
                if not self.shuffle_options:
                    result_dict = self.count_answers(len_correct, result_dict)
                if self.shuffle_options:
                    self.count_answers_with_shuffle(len_correct, result_dict, i)
                    
                results_list.append(result_dict)
            
        self.results_df = pd.DataFrame(results_list)    
                
                
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
        len_answer_sublists = len(self.answers) // self.num_options
        split_answer_lists = [self.answers[i * self.num_options:(i + 1) * self.num_options] for i in range(len_answer_sublists)]
        
        self.experiment_prompts = []
        
        for prompt, answers in zip(self.prompts, split_answer_lists):
            
            experiment_prompts = f"""{prompt}\nA: {answers[0]}\nB: {answers[1]}"""
            
            for i, label in enumerate(self.answer_option_labels[2:]):
                experiment_prompts += f"""\n{label}: {answers[i+2]}"""
                
            self.experiment_prompts.append(experiment_prompts)
            
    
    def process_instructions(self):
        if "add_instruction" in self.instruction_checklist:
            self.instructions = [text if text is not None else "" for text in self.instructions]
        else:
            self.instructions = ["" for _ in range(len(self.prompts))]
            
            
    def count_answers(self, len_correct, result_dict):
        # Check if len_correct is non-zero before performing further calculations
        if len_correct > 0:
            # Counting results
            for label in self.answer_option_labels:
                label_share = self.model_answers.count(label) / len_correct
                result_dict['Share of ' + label] = label_share
        else:
            # Set NaN values for share of labels when len_correct is 0
            for label in self.answer_option_labels:
                result_dict['Share of ' + label] = float('nan')
                
        return result_dict
    
    
    def count_answers_with_shuffle(self, len_correct, result_dict, i):
        # Check if len_correct is non-zero before performing further calculations
        if len_correct > 0:
            for ans in self.answer_label_mapping[i].keys():
                label_share = self.model_answers.count(self.answer_label_mapping[i][ans]) / len_correct
                result_dict[f'Share of "{ans}"'] = label_share
            
        else: 
            for ans in self.answer_label_mapping[i].keys():
                result_dict[f'Share of "{ans}"'] = float('nan')  
            
            
    def openai_api_call(self, model, prompt, instruction):
        response = client.chat.completions.create(
                model=model,  
                messages=[
                    {"role": "system", "content": instruction},

                    {"role": "user", "content": prompt}
                ],
                max_tokens=Experiment.OPENAI_MAX_TOKENS,
                temperature=self.temperature
            )
        
        return response
    
    
    def replicate_api_call(self, model, prompt, instruction):
        response = replicate.run(model,
                                 input = {
                                     "temperature": self.temperature,
                                     "system_prompt": instruction,
                                     "prompt": prompt,
                                     "max_new_tokens": Experiment.LLAMA_MAX_TOKENS}
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
            while shuffled_answers1 == shuffled_answers2:
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
    
    
    def plot_results(self):
        # Extract answer options columns
        answer_options = [col for col in self.results_df.columns if col.startswith('Share of ')]

        # Create a bar plot
        fig = go.Figure()

        # Create traces for each answer option
        for option in answer_options:
            fig.add_trace(go.Bar(
                x=self.results_df['Model'],
                y=self.results_df[option],
                name=option,
                hovertemplate=f"{option}: %{{y:.2f}}<extra></extra>"
            ))

        fig.update_layout(
            barmode='group',
            xaxis=dict(title='Model'),
            yaxis=dict(title='Share', range=[0, 1.1]),
            title=dict(text="Share of Answers for each Model (Temperature: " + str(self.temperature) + ", Iterations: " + str(self.iterations) + ")"),
            legend=dict(),
            bargap=0.3  # Gap between models
        )

        return fig