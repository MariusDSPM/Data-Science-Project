# Collection of functions to plot the live results of the experiments concerning:
# Prospect Theory
# Prospect Theory 2
# Decoy Effect
# Transaction Utility
# Transaction Utility 2
# Transaction Utility 3

# Import necessary libraries
import plotly.graph_objects as go
from ast import literal_eval
import pandas as pd
import numpy as np
import re
from collections import Counter 


### Prospect Theory ###
def PT_plot_results(df):

    # Transpose for plotting
    df = df.transpose()  
    # Get language model name
    model = df.loc["Model"].iloc[0]
    if model == 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3':
        model = "llama-2-70b" # change for plot title 
    # Get temperature value
    temperature = df.loc["Temp"].iloc[0]
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."].iloc[0]
    # Get original answer probabilities
    og_answers = df.loc["Original"].apply(literal_eval).iloc[0]
    # Get number of original answers
    n_original = df.loc["Original_count"].iloc[0]

    fig = go.Figure(data=[
        go.Bar(
            name = "Model answers",
            x = ["A", "B", "C"],
            y = [df.loc["A"].iloc[0], df.loc["B"].iloc[0], df.loc["C"].iloc[0]],
            customdata = [n_observations, n_observations, n_observations], 
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(55, 83, 109)"
        ),
        go.Bar(
            name = "Original answers",
            x = ["A", "B", "C"],
            y = [og_answers[0], og_answers[1], og_answers[2]],
            customdata = [n_original, n_original, n_original],
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(26, 118, 255)"
        )
    ])

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        title = "Answer options",  
        title_font=dict(size=18),  
    ),
    yaxis = dict(
        title="Share (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text=f"Distribution of {model}'s answers for temperature {temperature}",
        x = 0.5, # Center alignment horizontally
        y = 0.87,  # Vertical alignment
        font=dict(size=18),  
    ),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black',  
        borderwidth=2,  
    ),
    bargap = 0.3  # Gap between temperature values
)
    return fig


### Prospect Theory 2 ###
def PT2_plot_results(df):

    # Transpose for plotting
    df = df.transpose()  
    # Get language model name
    model = df.loc["Model"].iloc[0]
    if model == 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3':
        model = "llama-2-70b" 
    # Get temperature value
    temperature = df.loc["Temp"].iloc[0]
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."].iloc[0]

    fig = go.Figure(data=[
        go.Bar(
            name = "Model answers",
            x = ["A", "B", "C"],
            y = [df.loc["A"].iloc[0], df.loc["B"].iloc[0], df.loc["C"].iloc[0]],
            customdata = [n_observations, n_observations, n_observations], 
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(55, 83, 109)",
            showlegend = True,
        ),
    ])

    fig.update_layout(
    xaxis = dict(
        title = "Answer options",  
        title_font=dict(size=18),  
    ),
    yaxis = dict(
        title="Share (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text=f"Distribution of {model}'s answers for temperature {temperature}",
        x = 0.5, # Center alignment horizontally
        y = 0.87,  # Vertical alignment
        font=dict(size=18),  
    ),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black', 
        borderwidth=2,  
    ),
)
    return fig

def PT_plot_og_results(df):
    n_original = df["Obs."]  # number of answer options 
    fig = go.Figure(data=[
        go.Bar(
                name = "p(A)",
                x = [0.1, 0.3, 0.5, 0.7],
                y = [df["A"][0], df["A"][1], df["A"][2], df["A"][3]],
                customdata = n_original,
                hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
                marker_color="black",
            ),
        go.Bar(
                name = "p(B)",
                x = [0.15, 0.35, 0.55, 0.75],
                y = [df["B"][0], df["B"][1], df["B"][2], df["B"][3]],
                customdata = n_original,
                hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
                marker_color="rgb(55, 83, 109)",

            ),
        go.Bar(
                name = "p(C)",
                x = [0.2, 0.4, 0.6, 0.8],
                y = [df["C"][0], df["C"][1], df["C"][2], df["C"][3]],
                customdata = n_original,
                hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
                marker_color="rgb(26, 118, 255)",
        )
    ])
  

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        title = "Scenarios",  
        title_font=dict(size=18),
        tickfont=dict(size=16),  
    ),
    yaxis = dict(
        title="Share (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text=f"Distribution of original answers per scenario",
        x = 0.5, 
        y = 0.87,  
        font=dict(size=18),  
    ),
    width = 1000,
    margin=dict(t=100),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black', 
        borderwidth=2,  
    ),
    
)
    # Adjust x-axis labels to show 30+ to symbolize aggregation
    fig.update_xaxes(
    tickvals =[0.15, 0.35, 0.55, 0.75],
    ticktext=["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4"],
)
    return fig 


### Decoy Effect ###
def DE_plot_results(df):

    # Transpose for plotting
    df = df.transpose()  
    # Get language model name
    model = df.loc["Model"].iloc[0]
    if model == 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3':
        model = "llama-2-70b" 
    # Get temperature value
    temperature = df.loc["Temp"].iloc[0]
    # Get number of observations per temperature value
    n_observations = df.loc["Obs."].iloc[0]
    # Get original answer probabilities
    og_answers = df.loc["Original"].apply(literal_eval).iloc[0]
    # Get number of original answers
    n_original = df.loc["Original_count"].iloc[0]

    fig = go.Figure(data=[
        go.Bar(
            name = "Model answers",
            x = ["A", "B", "C"],
            y = [df.loc["A"].iloc[0], df.loc["B"].iloc[0], df.loc["C"].iloc[0]],
            customdata = [n_observations, n_observations, n_observations], 
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(55, 83, 109)"
        ),
        go.Bar(
            name = "Original answers",
            x = ["A", "B", "C"],
            y = [og_answers[0], og_answers[1], og_answers[2]],
            customdata = [n_original, n_original, n_original],
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of observations: %{customdata}<extra></extra>",
            marker_color = "rgb(26, 118, 255)"
        )
    ])

    fig.update_layout(
    barmode = 'group',
    xaxis = dict(
        title = "Answer options",  
        title_font=dict(size=18),  
    ),
    yaxis = dict(
        title="Share (%)",  
        title_font=dict(size=18), 
    ),
    title = dict(
        text=f"Distribution of {model}'s answers for temperature {temperature}",
        x = 0.5, # Center alignment horizontally
        y = 0.87,  # Vertical alignment
        font=dict(size=18),  
    ),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black',  
        borderwidth=2,  
    ),
    bargap = 0.3  # Gap between temperature values
)
    return fig


### Transaction Utility ###
# Function to extract dollar amounts from answers
def extract_dollar_amounts(answers):
    # Only return values that start with "$"
    valid_prices = [item for item in answers if item.startswith("$") and item[1:].replace(',', '').replace('.', '').isdigit()] # check if everything after $ is a digit, exlcuding commas
    # Delete the "$" from the beginning of each price
    prices = [item.replace('$', '') for item in valid_prices]
    return prices

# Function to plot results of first experiment 
def TU_plot_results(df):
    # Capitalize column names
    df.columns = df.columns.str.capitalize() 
    # Transpose for plotting
    df = df.transpose()
    # Get original and model answers
    og_answers = df.loc["Original"].apply(literal_eval).iloc[0]
    # Apply literal_eval to convert string to list
    answers = df.loc["Answers"].apply(literal_eval).iloc[0]
    # Get number of observations 
    n_observations = df.loc["Obs."].iloc[0] 
    # Get number of original answers
    n_original = df.loc["Original_count"].iloc[0]
    # Get stated WTP
    prices = extract_dollar_amounts(answers)
    # Get temperature value 
    temperature = df.loc["Temperature"].iloc[0]
    # Get model name
    model = df.loc["Model"].iloc[0]
    if model == "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3":
        model = "llama-2-70b"

    # Compute percentage of $0:
    percent_0 = (prices.count("0")/n_observations)*100
    # Compute percentage of $5:
    percent_5 = (prices.count("5")/n_observations)*100
    # Compute percentage of $10:
    percent_10 = (prices.count("10")/n_observations)*100
    # Compute percentage of $15:
    percent_15 = (prices.count("15")/n_observations)*100
    # Compute percentage of other answers:
    percent_other = 100-percent_0-percent_5-percent_10-percent_15

    fig = go.Figure(data = [
        go.Bar(
            name = "Model answers",
            x = ["$0", "$5", "$10", "$15", "Other"],
            y = [percent_0, percent_5, percent_10, percent_15, percent_other],
            customdata = [n_observations, n_observations, n_observations, n_observations, n_observations], 
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of total observations: %{customdata}<extra></extra>",
            marker_color = "rgb(55, 83, 109)"
        ),
        go.Bar(
            name = "Original answers",
            x = ["$0", "$5", "$10", "$15", "Other"],
            y = [og_answers[0], og_answers[1], og_answers[2], 0, og_answers[3]], # 0 because no-one answered $15, but model did 
            customdata = [n_original, n_original, n_original, n_original, n_original],
            hovertemplate = "Percentage: %{y:.2f}%<br>Number of total observations: %{customdata}<extra></extra>",
            marker_color = "rgb(26, 118, 255)"
        )
    ])

    # Style figure and add labels 
    fig.update_layout(
    barmode = "group",
     xaxis = dict(
            title = "Price",
            titlefont_size = 18,
            tickfont_size = 16,
     ),
    yaxis = dict(
        title = "Share (%)",
        titlefont_size = 18,
        tickfont_size = 16,
    ),
    title = dict(
    text=f"Distribution of {model}'s answers for temperature {temperature}",
    x = 0.5, 
    y = 0.95,
    font_size = 18,
    ),
    legend=dict(
        x=1.01,  
        y=0.9,
        font=dict(family='Arial', size=12, color='black'),
        bordercolor='black',  
        borderwidth=2,  
    ),
    width = 1000,
    margin=dict(t=60)
    )
    
    return fig 

# Function to plot results of second experiment
def TU2_plot_results(df):

    # Transpose for plotting
    df = df.transpose()
    # Get model name
    model = df.loc["Model"].iloc[0]
    if model == "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3":
        model = "llama-2-70b"

    # Get temperature value 
    temperature = df.loc["Temperature"].iloc[0]
    # Get number of observations 
    n_observations = df.loc["Obs."].iloc[0] 
    # Get place
    place = df.loc["Place"].iloc[0]
    # Adjust name of place for plot title
    if place == "grocery":
        place = "Grocery store"
    if place == "hotel":
        place = "Hotel"
    # Get income
    income = df.loc["Income"].iloc[0]
    if income == "0":
        income = "No information"
    # Apply literal_eval to work with list of strings
    answers = df.loc["Answers"].apply(literal_eval).iloc[0]
    # Get stated WTP
    prices = extract_dollar_amounts(answers)
    sorted_prices = sorted(prices, key=lambda x: float(x))
    numeric_prices = [float(price) for price in prices]
    # Get mean and median
    mean = np.round(np.mean(numeric_prices),2).astype(str)
    median = np.round(np.median(numeric_prices),2).astype(str)
    # Get number of unique answers
    num_unique_answers = len(set(prices))
   

    fig = go.Figure(data = [
    go.Histogram(x = sorted_prices,
                    customdata = [n_observations] * num_unique_answers,
                    hovertemplate = "Price asked: $%{x} <br>Frequency: %{y}<br>Total answers: %{customdata}<br>Mean: $" + mean + "<br>Median: $" + median +"<extra></extra>",
                    marker_color = "rgb(55, 83, 109)",
                    name = f"Place: {place}<br>Income: {income}<br>Mean: ${mean}<br>Median: ${median}",
),
    ])

    # Layout
    fig.update_layout(
        xaxis=dict(
            title="Price asked ($)",
            titlefont_size=18,
            tickfont_size=16,
            tickformat=".2f",
        ),
        yaxis=dict(
            title="Frequency",
            titlefont_size=18,
            tickfont_size=16,
        ),
        title=dict(
            text=f"Distribution of {model}'s WTP for temperature {temperature}",
            x=0.5,
            y=0.95,
            font_size=18,
        ),
        legend=dict(
            x=1.01,  
            y=0.9,
            font=dict(family='Arial', size=16, color='black'),
            bordercolor='black',  
            borderwidth=2,           
        ),
        showlegend=True,
        width=1000,
        margin=dict(t=60),
    )
    

    # Show the plot
    return fig

# Function to plot results of third experiment
def TU3_plot_results(df):

    # Transpose for plotting
    df = df.transpose()
    # Extract model name from the dataframe
    model = df.loc["Model"].iloc[0]
    if model == "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3":
        model = "llama-2-70b"

    # Get temperature value 
    temperature = df.loc["Temperature"].iloc[0]
    # Get number of observations 
    n_observations = df.loc["Obs."].iloc[0]
    # Extract model answers
    answers = df.loc["Answers"].apply(literal_eval).iloc[0]
    sorted_answers = sorted(answers, key=lambda x: float(x))
    numeric_answers = [float(answer) for answer in answers]

    # Get number of unique answers
    num_unique_answers = len(set(answers))
    # Get actual ticker price
    actual_price = df.loc["Actual_price"].iloc[0]
    # Get current market price
    current_price = df.loc["Orientation_price"].iloc[0]
    # Get price paid
    initial_cost = df.loc["Initial_cost"].iloc[0]
    # Get buyer 
    buyer = df.loc["Buyer"].iloc[0].capitalize()
    # Compute mean
    mean = np.round(np.mean(numeric_answers),2).astype(str)
    median = np.round(np.median(numeric_answers),2).astype(str)
   

    fig = go.Figure(data = [
    go.Histogram(x = sorted_answers,
                    customdata = [n_observations] * num_unique_answers,
                    hovertemplate = "Price asked: $%{x} <br>Frequency: %{y}<br>Total answers: %{customdata}<br><extra></extra>",

                    marker_color = "rgb(55, 83, 109)",
                    name = f"Actual price: ${actual_price}<br>Initial costs: ${initial_cost}<br>Current price: ${current_price}<br>Buyer: {buyer}<br>Mean: ${mean}<br>Median: ${median}"),
    ])

    # Layout
    fig.update_layout(
        xaxis=dict(
            title="Price asked ($)",
            titlefont_size=18,
            tickfont_size=16,
            tickformat=".2f",
        ),
        yaxis=dict(
            title="Frequency",
            titlefont_size=18,
            tickfont_size=16,
        ),
        title=dict(
            text=f"Distribution of {model}'s answers for temperature {temperature}",
            x=0.45,
            y=0.95,
            font_size=18,
        ),
        legend=dict(
            x=1.01,  
            y=0.9,
            font=dict(family='Arial', size=16, color='black'),
            bordercolor='black',  
            borderwidth=2,           
        ),
        showlegend=True,
        width=1000,
        margin=dict(t=60),
    )
    

    # Show the plot
    return fig