# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State


dash.register_page(__name__, path='/chat-bot', name='Chat Bot', location='sidebar')


# Start Page
layout = [html.P("This chatbot is not yet implemented. Sorry!")]