# Import required libraries 
import pandas as pd
import plotly.graph_objects as go


def plot_results(df, x_axis, groupby, iterations, temperature):

    # Filter based on x_axis
    if x_axis == "Model":
        df = df[df["Scenario"] == groupby]
    elif x_axis == "Scenario":
        df = df[df["Model"] == groupby]

    # Extract answer options columns
    answer_options = [col for col in df.columns if col.startswith('Share of ')]

    # Create a bar plot
    fig = go.Figure()

    # Create traces for each answer option
    for option in answer_options:
        fig.add_trace(go.Bar(
            x=df[x_axis],
            y=df[option],
            name=option,
            hovertemplate=f"{option}: %{{y:.2f}}<extra></extra>"
        ))

    fig.update_layout(
        barmode='group',
        xaxis=dict(title=x_axis),
        yaxis=dict(title='Share', range=[0, 1.1]),
        title=dict(text="Share of Answers for each Model (Temperature: " + str(temperature) + ", Iterations: " + str(iterations) + ")"),
        legend=dict(),
        bargap=0.3  # Gap between models
    )

    return fig