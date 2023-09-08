import plotly.graph_objects as go

# Pie Chart Code
def polarity_pie_chart(df):
    # Get total count of positive, negative, and neutral tweet
    positive_count = len(df.loc[df["polarity_label"] == 'Positive'])
    negative_count = len(df.loc[df["polarity_label"] == 'Negative'])
    neutral_count = len(df.loc[df["polarity_label"] == 'Neutral'])
    
    fig = go.Figure(
        [
            go.Pie(
                labels=["Positive", "Negative", "Neutral"],
                values=[
                    positive_count,
                    negative_count,
                    neutral_count,
                ],
                name="Sentiment Distribution",
                marker_colors=[
                    "rgba(184, 247, 212, 0.6)",
                    "rgba(255, 50, 50, 0.6)",
                    "rgba(131, 90, 241, 0.6)",
                ],
                hole=0.45,
            )
        ]
    )
    fig.update_layout(
        template="simple_white",
        title = 'Tweet polarity distribution'
    )
    return fig