# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State


dash.register_page(__name__, path='/', name='Home', location='above-experiments')


# Start Page
layout = [html.H1("Do Large Language Models behave like a Human?", className="page-heading"),
          html.Hr(),
          dcc.Markdown("""
                       Large Language Models (LLMs) are a type of Artificial Intelligence, able to generate text in real time.     
                       They have been trained on an enormous amount of text data generated by humans, allowing them to not only learn mere facts, but also
                       learn the underlying structure and logic of human language.    
                       In their very nature, they are designed to respond to a prompt with the most likely continuation of the text.  
                       Since the text data used to train these models has been written by humans, one might expect the output of these models to be 
                       human-like.   
                       This would mean, that specific patterns, biases, preferences or even irrational behavior, as exhibited by humans, might 
                       also be reflected in the answers the LLMs generate. Examples, that are especially interesting in our context, would be: 
                       Extremeness Aversion, Loss Aversion, Anchoring Biases or numerous other behavioral phenomena.    
                       Furthermore, because the training data, among other things, contains text that is freely available on the internet, parts of it 
                       are also: Product reviews, forum posts, blog articles, or other forms in which consumers might express their opinions or preferences
                       regarding the products they buy or use.   
                       Therefore, we can expect the answers generated by the models to also contain the underlying reasoning and preferences of the
                       consumers from the training data.   
                       This suggests, that LLMs could be used to simulate human behavior in numerous applications. 
                       One possible application is the field of market research.   
                       Traditional market research methods, such as surveys, conjoint analysis or focus group discussions can be very expensive
                       and take time. With the use of LLMs, it might be possible to gain meaningful insights about a certain product, service or planned
                       marketing measure by simply asking a language model.  
                       If the results obtained by this approach are actually comparable to the results obtained by traditional market research methods,
                       the use of LLMs in this field could hold huge potential for future applications.   

                       To research whether Large Language models actually reflect typical patterns in consumer behavior, we conducted a series of
                       experiments, which each deal with one specific behavioral phenomenon exhibited by humans. 
                       """),
          html.Hr(),
          dcc.Markdown("""
                       **The following pages are available:**      

                      You can use the navigation menu to regard the results of the conducted experiments, send individual queries to LLMs via a messaging interface
                      and even conduct your own experiments.    
                       * [Experiments](/overview) - Explore the results of the conducted experiments 
                       * [Chatbot](/chat-bot) - Interact with LLMs to see how they behave (*API keys required*)
                       * [Live Experiment](/live-experiment) - Conduct your own experiment and search for similarities between the behavior of LLMs and humans (*API keys required*)
                       * [Experiment Recreation](/experiment-recreation) - Recreate the conducted experiments yourself (*API keys required*)    
                       
                      On each experiment page, you can find a detailed description of the original experiment or phenomenon, the motivation for conducting the experiment, 
                       as well as some information about the implementation. Each experiments' results are also visualized on the respective page.    
                      The experiment overview page also provides some further insights into some rather technical aspects in this context of research. 
                       """               
            ),
          ]
