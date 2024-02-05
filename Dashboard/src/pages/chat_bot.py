# Import required libraries 
import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
import replicate
from openai import OpenAI
import openai
import os 


# Get openAI API key (previously saved as environmental variable)
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set client
client = OpenAI()


dash.register_page(__name__, path='/chat-bot', name='Chat Bot', location='sidebar')





layout = dbc.Container(
    children=[
        html.H1("Chatbot", className="page-heading"),
        html.P("""This chatbot provides a simple way of interacting with the language models through individual, quick queries. It is not designed to handle complex 
               conversations, as it has no memory! Giving the chatbot a memory would quickly make its usage rather expensive. 
               It serves as a tool to get a feeling of how the models' responses change when the input changes.
               Therefore, you can freely select any temperature value in the range of 0.01 to 2 and experiment with the maximum number of tokens the model should generate."""),
        dbc.Row(
            children=[
                # Left half with text input
                dbc.Col(
                    children=[
                        html.Div(
                            [
                                html.Label("Enter your message", style={'textAlign': 'center'}),
                                dbc.Textarea(
                                    id="text-input",
                                    size="lg",
                                    placeholder="Will robots take over the world?",
                                ),
                            ],
                            style={"marginBottom": "15px"},
                        ),
                        html.Div(
                            [
                                html.Div("Enter instructions:"),
                                dbc.Textarea(
                                    id="instruction-input",
                                    size="sm",
                                    placeholder="Base your answer on the Terminator Movie Series."
                                ),
                            ],
                            style={"marginBottom": "15px"},
                        ),
                    ],
                    width=7,
                ),
                # Right half with dbc.Card containing three dropdowns
                dbc.Col(
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Select Chatbot configuration"),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Label("Language model"),
                                                        dcc.Dropdown(
                                                            id="model-dropdown",
                                                            options=[
                                                                {"label": "GPT-3.5-Turbo", "value": "gpt-3.5-turbo"},
                                                                {"label": "GPT-4-1106-Preview", "value": "gpt-4-1106-preview"},
                                                                {"label": "LLama-2-70b", "value": "llama-2-70b"},
                                                            ],
                                                            value="gpt-3.5-turbo",
                                                            style={'width': '100%', 'margin': 'auto', 'margin-bottom': '15px'}
                                                        ),
                                                    ],
                                                    width=12,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("Maximum number of tokens"),
                                                        dcc.Input(
                                                            id="chatbot-max-tokens",
                                                            type="number",
                                                            value=20,
                                                            style={'width': '100%', 'margin': 'auto', 'margin-bottom': '15px'}
                                                        ),
                                                    ],
                                                    width=12,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H6("Select Temperature value"),
                                                        dcc.Slider(
                                                            id="chatbot-temperature-slider",
                                                            min=0.01,
                                                            max=2,
                                                            step=0.01,
                                                            marks={0.01: '0.01', 0.5: '0.5', 1: '1', 1.5: '1.5', 2: '2'},
                                                            value=1,
                                                            tooltip={'placement': 'top'},
                                                            persistence=True,
                                                            persistence_type='session',
                                                        ),
                                                    ],
                                                    width=12,
                                                    style={'width': '100%', 'marginBottom': '40px'},
                                                ),
                                            ],
                                            style={'width': '75%', 'margin': 'auto'},
                                        ),

                                        dbc.Button(
                                            'Send message',
                                            id='chatbot-update-button',
                                            n_clicks=None,
                                            style={'marginBottom': '25px', 'width': '100%', 'textAlign': 'center'}
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    width=5,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="chatbot-output",
                    style={'textAlign': 'center', 'margin': '20px', 'margin': 'auto'}
                )
            )
        )
    ],
    fluid=True
)





### Callbacks ###

@dash.callback(
    Output("chatbot-output", "children"),
    Input("chatbot-update-button", "n_clicks"),
    [State("text-input", "value"),
     State("instruction-input", "value"),
     State("model-dropdown", "value"),
     State("chatbot-max-tokens", "value"),
     State("chatbot-temperature-slider", "value")])


def update_chatbot_output(n_clicks, text_input, instruction_input, selected_model, selected_max_tokens, selected_temperature):
    print(f"Text input: {text_input}")
    print(f"Instruction input: {instruction_input}")
    print(f"Model: {selected_model}")
    print(f"Max tokens: {selected_max_tokens}")
    print(f"Temperature: {selected_temperature}")

    output = ""
    if n_clicks is not None:
        if selected_model == "llama-2-70b":
            response = replicate.run(
                'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
                input = {
                        "system_prompt": f"{instruction_input}",
                        "temperature": selected_temperature,
                        "max_new_tokens": selected_max_tokens, 
                        "prompt": f"{text_input}"
                            })
            answer = ""
            for item in response:
                output = answer + item
        else: 
            response = client.chat.completions.create(
                    model = "gpt-3.5-turbo", 
                    max_tokens = selected_max_tokens,
                    temperature = selected_temperature,
                    messages = [
                    {"role": "system", "content": f"{instruction_input}"},        
                    {"role": "user", "content": f"{text_input}"},
                        ])
            output = response.choices[0].message.content
        n_clicks = None
    return output
        