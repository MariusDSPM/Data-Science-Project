# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State


dash.register_page(__name__, path='/', name='Home', location='above-experiments')


# Start Page
layout = [html.H1("Do Large Language Models Behave like a Human?", className="page-heading"),
          html.P("""Large Language models hold huge potential for a wide range of applications either for private, but also for professional use. 
                    One possible question that is of especially interesting for market research, is whether these models behave human-like enough to be used as surrogates for 
                    human participants in experiments. This dashboard is a first attempt to answer this question."""),
          html.P("Feel free to explore more pages using the navigation menu."),
          dcc.Markdown("""
                       **The following pages are available:**
                       * [Experiments](/overview) - Explore the results of our experiments 
                       * [Chat Bot](/chat-bot) - Interact with LLMs to see how they behave (*API keys required*)
                       * [Live Experiment](/live-experiment) - Conduct your own experiment and search for similarities between the behaviour of LLMs and humans (*API keys required*)
                       """
                
            ),
          ]
