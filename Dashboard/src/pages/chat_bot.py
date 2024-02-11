# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State
from openai import OpenAI
from replicate.client import Client



dash.register_page(__name__, path='/chat-bot', name='Chatbot', location='below-experiments')


layout = dbc.Container(
    children=[
        html.H1("Chatbot", className="page-heading"),
        html.Hr(),
        dcc.Markdown("""This chatbot provides a simple way of interacting with the language models through individual, quick queries.   
                     It is not designed to handle complex conversations, as it has **no memory**! Giving the chatbot a memory would quickly make
                     its usage rather expensive.        
                     It serves as a tool to, for example, get a feeling of how the models' responses to the same prompt change, when different values for
                     temperature and maximum number of tokens are used.  
                     Therefore, you can freely select any temperature value in the range of 0.01 to 2 and experiment with the maximum number
                     of tokens the model should generate."""),
        html.Hr(),
        html.H6("To use the Chat Bot, you'll need to provide API keys to get access to the LLMs:"),
        html.Br(),
        html.Div(
            [
                dbc.Input(
                    id='input-openai-key-chatbot', 
                    placeholder="OpenAI API Key", 
                    type="password", 
                    persistence=True, 
                    persistence_type='session', 
                    style={'width': '30%'}),
                dbc.FormText("You'll need an OpenAI API key to use GPT-3.5-Turbo and GPT-4-1106-Preview. You can get one from the OpenAI website (https://platform.openai.com)."),
            ],
        ),
        html.Br(),
        html.Div(
            [
                dbc.Input(
                    id='input-replicate-key-chatbot', 
                    placeholder="Replicate API Key", 
                    type="password", 
                    persistence=True, 
                    persistence_type='session', 
                    style={'width': '30%'}),
                dbc.FormText("You'll need a Replicate API key to use Llama-2-70b. You can get one from the Replicate website (https://replicate.com)."),
            ],
        ),
        html.Hr(),
        html.Br(),
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
                            style={"marginBottom": "15px", 'margin-top': '20px'},
                        ),
                        html.Div(
                            [
                                html.Div("Enter instructions"),
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
                                                        dbc.Tooltip(
                                                        """The maximum number of tokens the model should generate. Note, that this is a hard cut-off limit, meaning the
                                                        models will not adjust their answers to fit the token limit. Once the limit is reached, the text generation will stop mid-sentence.""",
                                                        target="chatbot-max-tokens",
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
                                                        dbc.Tooltip(
                                                        """The temperature value controls the randomness of the models' responses. A higher temperature value
                                                          will result in more random answers, while a lower temperature value will result in more deterministic responses.""",
                                                        target="chatbot-temperature-slider",
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
    dbc.Card(
        [
            dbc.CardHeader("Response", style={'textAlign': 'left'}),
            dbc.CardBody(
                html.Div(
                        dcc.Loading(
                            children = [html.Div(id="chatbot-output")],
                    style={'textAlign': 'center', 'margin': '20px'}
                )
            ),
            )
        ],
        style={'margin': '20px', 'margin': 'auto', 'margin-top': '40px'}
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
     State("chatbot-temperature-slider", "value"),
     State("input-openai-key-chatbot", "value"),
     State("input-replicate-key-chatbot", "value")])


def update_chatbot_output(n_clicks, text_input, instruction_input, selected_model, 
                          selected_max_tokens, selected_temperature, openai_key, replicate_key):

    output = ""
    if n_clicks is not None:
        if selected_model == "llama-2-70b":
            
            replicate = Client(api_token=replicate_key)
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
                answer += item
            output = answer
            
        else: 
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                    model = "gpt-3.5-turbo", 
                    max_tokens = selected_max_tokens,
                    temperature = selected_temperature,
                    messages = [
                    {"role": "system", "content": f"{instruction_input}"},        
                    {"role": "user", "content": f"{text_input}"},
                        ])
            output = response.choices[0].message.content
        
    return output

