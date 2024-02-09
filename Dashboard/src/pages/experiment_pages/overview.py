# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State


dash.register_page(__name__, path='/overview', name='Overview', location='experiments', order=0)


# Overview Page
layout = [html.H1("Overview", className="page-heading"),
          html.P("""We have conducted a series of experiments to investigate the behaviour of Large Language Models (LLMs)
                    in behavioural economics experiments. The results of these experiments are available on the Experiments pages."""),
          dcc.Markdown("""
                       **The results of the following experiments are available:**
                       * [Decoy Effect](/decoy-effect)
                            * In these experiments, we investigate the decoy effect, a phenomenon in which people change their preference 
                          between two options when presented with a third option that is asymmetrically dominated.
                       * [Loss Aversion](/loss-aversion)
                            * The interesting aspect of this experiment lies in examining how LLMs weigh the certainty of 
                            outcomes against the potential for larger gains or losses. By comparing responses in scenarios involving 
                            gains and losses, researchers can gain insights into whether LLMs exhibit consistent risk preferences 
                            across different contexts.
                       * [Prospect Theory](/prospect-theory)
                            * These experiments are designed to test the predictions of prospect theory, a behavioural economic theory 
                            that describes the way people choose between probabilistic alternatives that involve risk.
                       * [Sunk Cost Fallacy](/sunk-cost-fallacy)
                            * These experiments are designed to test the sunk cost fallacy, a behavioural economic theory that describes
                            the tendency of people to continue an endeavour once an investment in money, effort, or time has been made.
                       * [Transaction Utility](/transaction-utility)
                            * These experiments are designed to test the transaction utility theory, a behavioural economic theory that
                            describes the way people choose between probabilistic alternatives that involve risk.
                       """
                
            ),
          html.Br(),
          html.P("""Most of the experiments are known experiments that have already been carried out with real people. 
                 Where available, the human results are included for comparison. The sources for the experiments 
                 are noted on the pages. """),
          dcc.Markdown("""
                      **The general workflow of the experiments is as follows:**
                      
                      1. The experiment scenario is copied from the literature, 
                      while trying to keep the scenario text as close as possible to the original.
                      2. The LLMs are instructed to answer the experiments only with the respective 
                      letter of the answer option or to name a dollar amount, depending on the experiment. 
                      Answers that are not in the correct format are discarded.
                      3. Each model is asked to answer the experiment 50 times for each temperature value.
                      4. The answers are then evaluated and compared to the human answers.
                       """
                
            ),
          ]