# Import required libraries 
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, State


dash.register_page(__name__, path='/overview', name='Overview', location='experiments', order=0)


# Overview Page
layout = [html.H1("Overview", className="page-heading"),
          html.Hr(),
          dcc.Markdown("""
                       **The following experiments were conducted:**
                       * [Decoy Effect](/decoy-effect)
                            * Multiple choice style: In pricing, consumers' preferences between two options can be influenced by the introduction of a specific third option.
                              Will the models' choices also be influenced by this so called *Decoy*?
                       * [Loss Aversion](/loss-aversion)
                            * Multiple choice style: The interesting aspect of this experiment lies in examining how LLMs weigh the certainty of 
                            outcomes against the potential for larger gains or losses. By comparing responses in scenarios involving 
                            gains and losses, researchers can gain insights into whether LLMs exhibit consistent risk preferences 
                            across different contexts.
                       * [Prospect Theory](/prospect-theory)
                            * Multiple choice style: Although mathematically equivalent, gains and losses of the same magnitude are perceived differently by humans. 
                              Losses weigh heavier than gains and the sensitivity to changes decreases with higher absolute values. Do LLMs also exhibit this behavior? 
                       * [Sunk Cost Fallacy](/sunk-cost-fallacy)
                            * Multiple choice style: These experiments are designed to test the sunk cost fallacy, a behavioural economic theory that describes
                            the tendency of people to continue an endeavour once an investment in money, effort, or time has been made.
                       * [Transaction Utility](/transaction-utility)
                            * Open answer style: Additional to pure acquisition utility, consumers also derive a so-called transaction utility from a purchase.
                              Is this concept also present in Large Language Models and reflected in their answers?
                       """
                
            ),
          html.Br(),
          html.P("""                 
                 In the selection process of our experiments, the main focus lied on experiments that are well known in the field of behavioral economics and
                 where previous empirical findings were available to compare our model results to. We first conducted a series of multiple choice style experiments,
                 since the results can more easily be compared to existing literature. Compared to the open answer style experiments, the multiple choice style
                 experiments are also less prone to the models' tendency of generating answers that are not in the desired format. Open answer style experiments
                 require more prompt engineering, as well as additional post-processing steps to gain meaningful insights.        
                 A more detailed description of the experiments as well as the motivation behind it can be found on the respective experiment page.
                 """),
          html.Hr(),
          dcc.Markdown("""
                      **The general workflow for conducting an experiment is:**
                      
                      1. Search the literature for either a well-known, or well-implementable experiment in the field of behavioral economics.
                      2. Adapt the experiment design, most importantly the phrasing, to suit the context of querying LLMs. In doing so, it is important to stick
                         as close to the original design as possible to maximize the comparability of results. 
                      3. Before going into repeated interations, experiment with the prompt itself and the instruction role to optimize the expected answers.
                      4. Run the experiment on a larger scale, i.e. let each model answer the same prompt at least 50 times for a given temperature value.
                      5. Collect and post-process the results, i.e. filter out answers that are not in the right format and further analyze the remaining ones. 
                      6. Visualize the results and compare them to the original findings.   
                      
                       """),
       
          dbc.Accordion([
              dbc.AccordionItem(
                  dcc.Markdown("""
                               **Models**: We used the OpenAI models GPT-3.5-Turbo, and GPT-4-1106-preview, as well as Meta's Llama-2-70b-chat model.
                               All models were accessed through an API, which allows for repeated queries by the use of a simple for-loop. For the LLama model, 
                               we used  *Replicate*, which allows for the remote execution of the model. This was necessary, since the model is not
                               available through the OpenAI API and we did not want to use a (smaller) local version. 
                               For further information you can go to https://replicate.com/meta/llama-2-70b-chat.

                               **Temperature:** One key input parameter for the LLMs is the so-called temperature. It controls the *randomness* of the answers. 
                               With a temperature of 0, the models responses will be deterministic, always returning the most likely answer. Higher temperature values
                               then introduce a degree of randomness, resulting in more creative answers. For factual use cases, it is actually suggested to use a temperature of 0.
                               In our context, we are interested in the distribution of answers and therefore regard multiple temperature values. 
                               Note, that for the Llama model, this range actually spans from 0.01 to 5, while for the OpenAI models, it spans from 0 to 2. 
                               However, with a temperature value of 2 we already received a substantial amount of replies that were not suited for post-processing, since
                               the models did not regard the instructions closely enough. Therefore, we decided to to limit the temperature range from 0 to 2 for both models. 

                               **System Instructions:** On top of the prompt itself, the models can receive a message in form of an instruction. This serves as a means of
                               guiding the models general behavior. One very illustrative example would for example be to answer the given prompt as if the model was Forrest
                               Gump.   
                               For our purpose however, we used the instruction role to obtain more consistent answers by:
                               - Multiple choice: Only answer with the letter of the alternative you would choose, without any reasoning. 
                               - Open style prompts: Answer by only giving a single price in dollars and cents without an explanation.
                               Since for higher temperature values, the models still tended to give answers that were not in the desired format, we decided
                               to also include the instruction in the prompt itself. This way, more answers were valid and could be used for further analysis.

                               **Max Tokens:** This parameter sets the maximum number of output tokens the model should generate. This is a hard cut-off limit,
                               meaning that the model will not format its answer to suit the given token limit, but stop its answer generation mid-sentence.
                               Note, that tokens are not identical to the exact word or character count of a sentence. To get a better understanding of this you can
                               visit https://platform.openai.com/tokenizer.

                               **Prompt Engineering:** Designing prompts that are concise and state exactly what you want the model to answer is crucial. 
                               With the increasing usage of LLMs, prompt engineering has actually become a field of its own. In the context of our research,
                               we tried to stick to the original phrasing of a given experiment as closely as possible, while still providing sufficient 
                               additional instructions to obtain meaningful answers. A lot of time and effort can and should be invested in fine-tuning
                               the prompts such that the models results are as informative as possible and require less post-processing.

                               **Costs**: While compared to traditional market research approaches, the costs of running the conducted experiments are diminishingly low,
                               one should at least consider the differences in costs between different LLMs. As of 11.02.2024, the costs for openAI's GPT-3.5-Turbo model
                               are $0.0005/1000 Input tokens and $0.0015/Output tokens. For GPT-4 these costs are $0.03/1000 Input tokens and $0.06 for 1000 Output tokens.
                               While still being relatively cheap to use, the relative difference in costs is substantial.   
                               Since we used the Llama model through replicate, this also generated costs. Unfortunately, the usage is priced depending on the time the model
                               takes to handle a given request, making cost estimates difficult. From our experience however, GPT-4 and Llama were in the same price range.
                               For further information you can visit https://replicate.com/pricing and https://openai.com/pricing. 
                               In applications were cost estimates are displayed in this application, we used the simplification of equating word count to token count. 
                               Throughout our work, cost estimates obtained by this approach were very close to the actual costs. On top of that, costs are generously rounded up, to
                               prevent any unexpected surprises.

                               **Post-processing**: The answers of Large Language Models are very rarely in a format that allows for direct comparison to previous empirical results.     
                               Along with the aspect of *prompt engineering*, thorough post-processing is crucial for obtaining meaningful insights.    
                               Therefore, at the beginning of each experiment, we visually inspected model answers for higher maximum token values to see what the models would *like* to answer.   
                               This way, suitable post-processing functions can be implemented, once the expected format of the model answers is known.       
                               For example in the context of the *Transaction Utility* experiments, we quickly saw that each answer containing valid information started with
                               a dollar sign. Other answers often tended to be a rather creative explanation for the decision, lead up with a small greeting or an 
                               answer with no informative content at all. Therefore, we disregarded all answers that did not start with a dollar sign.      
                               Of course, this approach has do be done with caution and re-evaluated for every experiment individually, since it is very important to not exclude answers
                               that might have a systematic impact on the answer distribution.
                              """),
               title = "Technical aspects"),
          ], start_collapsed = True,
          )
              
          ]