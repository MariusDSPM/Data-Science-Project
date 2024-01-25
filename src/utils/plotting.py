# Import required libraries 
import pandas as pd
import plotly.graph_objects as go


def plot_results(df, x_axis, groupby, iterations, temperature):

    df['Scenario'] = df['Scenario'].astype(str)
    groupby = str(groupby)
    
    filtered = "Model" if x_axis == "Scenario" else "Scenario"
    
    df = df[df[filtered] == groupby]

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
        title=dict(text=f"Share of Answers for each {x_axis} ({filtered}: {groupby}, Temperature: {temperature} , Iterations: {iterations})"),
        legend=dict(),
        bargap=0.3  # Gap between modelsS
    )

    return fig