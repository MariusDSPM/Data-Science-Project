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
          dcc.Markdown("""
                      **Stuff worth mentioning in Overview (to be deleted)**
                      * What are LLMs? Which ones did we use?
                      * What is replicate? Why did we use it? Possibility to run llama remotely  
                      * General motivation -> trained on large amounts of data, can generate human-like text,....
                      * previous literature findings?
                      * behavioral biases: extremeness aversion, loss aversion, anchoring, etc.
                      * Instruction role: Sometimes instructions + prompt + instructions (at least in TU)
                      * Prompt engineering
                      * What is a token? Token ~ word count?
                      * What parameters did we (not) use? e.g. top_p
                      * Temperature range 0-5 in llama vs 0-2 in openai
                      * max_tokens as hard cut-off limit (already mentioned as hoverinfo in chatbot)
                      * Maybe table of prices?                         
                      * Further reading  
                      * Individual experience during the project?         
                      * workflow: how detailed? 
                       """)
          ]
